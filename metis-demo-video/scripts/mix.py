"""Step 2: finish the video: music (its big lift on a chosen moment), fades, standard color and audio.

  python mix.py storyboard.json         -> out/<name>.mp4

storyboard "music": {"file": "track.mp3", "lift_on": "app_in", "volume": 0.9}
  lift_on  a cue from out/cues.json ("app_in" = the app flying in, "scene:3", or seconds)
The track's biggest jump in loudness is found automatically and placed on that moment.
If the track is too short it is extended on the beat before its outro; if too long it
is trimmed and faded. Without "music" the video gets silent audio and fades only.
"""
import os, subprocess, sys
import numpy as np
from common import Board, ffmpeg, pcm

SR = 48000


def envelope(a, hop=480):                       # 10 ms loudness
    m = np.abs(a.mean(axis=1)) if a.ndim == 2 else np.abs(a)
    n = len(m) // hop
    return m[:n * hop].reshape(n, hop).mean(axis=1)


def find_lift(env):
    """Biggest sustained jump in loudness: 0.5 s after vs 0.5 s before (ignores leading silence)."""
    db = np.maximum(20 * np.log10(env + 1e-6), -60)
    best, at, w = -1e9, 0, 50
    for i in range(w, len(db) - w):
        j = db[i:i + w].mean() - db[i - w:i].mean()
        if j > best:
            best, at = j, i
    return at / 100.0


def extend(a, env, need, before):
    """Insert >= need seconds by repeating the stretch ending at `before`, cut where the beat lines up best."""
    if need <= 0:
        return a
    onset = np.maximum(np.diff(env), 0)
    i1 = int(before * 100)
    seg = onset[i1 - 400:i1]
    best, lag = -1, int(need * 100)
    for L in range(int(need * 100), int((need + 4) * 100)):
        ref = onset[i1 - 400 - L:i1 - L]
        if len(ref) == len(seg) and len(seg):
            c = float(np.dot(seg - seg.mean(), ref - ref.mean()) / (np.linalg.norm(seg - seg.mean()) * np.linalg.norm(ref - ref.mean()) + 1e-9))
            if c > best:
                best, lag = c, L
    cut, back, xf = i1 * 480, i1 * 480 - lag * 480, int(0.03 * SR)
    ramp = np.linspace(0, 1, xf)[:, None]
    seam = a[cut - xf:cut] * (1 - ramp) + a[back - xf:back] * ramp
    print('  music extended by %.1fs (beat match %.2f)' % (lag / 100, best))
    return np.concatenate([a[:cut - xf], seam, a[back:]])


def add_voice(board, cues, a, m):
    """Lay the voiceover lines on top at their cue times; the music dips while someone is speaking."""
    man = board.json_in('voice_manifest.json')
    if not man or not cues.get('vos'):
        return a
    voice = np.zeros_like(a)
    clips = []
    for t, lid in cues['vos']:
        e = man.get(lid)
        if not e or not e.get('file'):
            continue
        raw = subprocess.run([ffmpeg(), '-loglevel', 'error', '-i', os.path.join(board.out, e['file']), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                             capture_output=True, check=True).stdout
        v = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
        fi, fo = int(float(m.get('voice_fade_in', 0.05)) * SR), int(float(m.get('voice_fade_out', 0.18)) * SR)
        if len(v) > fi + fo:                                  # soft start and a gentle tail, never a hard edge
            v[:fi] *= np.linspace(0, 1, fi)[:, None]
            v[-fo:] *= np.linspace(1, 0, fo)[:, None]
        clips.append((t, v))
    if m.get('voice_match', True) and clips:                  # same loudness on every line, so a handoff between voices does not jump
        def level(x):
            mono = np.abs(x).mean(axis=1); live = mono[mono > 0.02]
            return float(np.sqrt((live ** 2).mean())) if len(live) else 0.0
        lv = [level(v) for _, v in clips]
        target = float(np.median([x for x in lv if x > 0]))
        lo, hi = 0.63, 1.58                                   # at most about 4 dB of correction per line
        for k, (t, v) in enumerate(clips):
            if lv[k] > 0:
                v *= min(max(target / lv[k], lo), hi)
        print('  voice levels matched: %d lines, correction %.1f to %.1f dB' % (len(clips),
              min(20 * np.log10(min(max(target / x, lo), hi)) for x in lv if x > 0), max(20 * np.log10(min(max(target / x, lo), hi)) for x in lv if x > 0)))
    for t, v in clips:
        i = int(t * SR); n = min(len(v), len(voice) - i)
        if n > 0:
            voice[i:i + n] += v[:n]
    env = np.abs(voice).mean(axis=1)
    hop = SR // 100
    k = len(env) // hop
    act = (env[:k * hop].reshape(k, hop).max(axis=1) > 0.012).astype(np.float32)
    act = np.convolve(act, np.ones(30), 'same').clip(0, 1)                        # hold the dip across short gaps
    look = int(float(m.get('duck_lead', 0.3)) * 100)                              # start dipping before the voice does
    act = np.concatenate([act[look:], np.zeros(look, np.float32)]) if look else act
    rel = max(8, int(float(m.get('duck_release', 0.7)) * 100))
    act = np.convolve(act, np.hanning(rel) / np.hanning(rel).sum(), 'same')       # smooth attack and a slow release
    gain = 1 - float(m.get('duck', 0.55)) * np.repeat(act, hop)
    gain = np.concatenate([gain, np.full(len(env) - len(gain), gain[-1] if len(gain) else 1.0)])
    print('  voiceover: %d lines mixed, music ducked %.0f%% under speech' % (len(cues['vos']), float(m.get('duck', 0.55)) * 100))
    return a * gain[:, None] + voice * float(m.get('voice_volume', 1.15))


def fit_music(board, length, cues):
    m = board.data['music']
    raw = subprocess.run([ffmpeg(), '-loglevel', 'error', '-i', board.rel(m['file']), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    lift_on = m.get('lift_on', 'app_in')
    if isinstance(lift_on, (int, float)):
        target = float(lift_on)
    else:
        marks = {k: t for k, t in cues['marks']}
        hits = [t for t, k in cues['cues'] if k == lift_on] or [t for k, t in marks.items() if k.startswith(str(lift_on).replace('scene:', '') + ':')]
        target = hits[0] if hits else 0.0
    lift = m.get('lift_at', None)
    lift = find_lift(envelope(a)) if lift is None else float(lift)
    offset = lift - target
    print('  music: lift at %.1fs in the track, placed at %.1fs in the video' % (lift, target))
    if offset < 0:
        a = np.concatenate([np.zeros((int(-offset * SR), 2), np.float32), a]); offset = 0
    a = a[int(offset * SR):]
    if len(a) / SR < length + 0.5:                 # too short: extend before the outro
        env = envelope(a)
        loud = np.convolve(20 * np.log10(env + 1e-6), np.ones(50) / 50, 'same') > -16
        outro = (np.nonzero(loud)[0][-1] / 100.0 - 2.0) if loud.any() else len(a) / SR - 8
        a = extend(a, env, length - len(a) / SR + 0.5, max(outro, 6.0))
    a = a[:int(length * SR)] * float(m.get('volume', 0.55 if board.data.get('sfx') else 0.9))   # quieter under sound effects
    if len(a) < int(length * SR):
        a = np.concatenate([a, np.zeros((int(length * SR) - len(a), 2), np.float32)])
    a = add_voice(board, cues, a, m)
    a = add_sfx(board, a, cues, length)
    f = int(min(2.0, length / 4) * SR)
    a[-f:] *= np.linspace(1, 0, f)[:, None]
    a[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))[:, None]
    wav = os.path.join(board.out, 'music_fit.wav')
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', wav],
                   input=a.astype(np.float32).tobytes(), check=True)
    return wav


def load(board, f):
    raw = subprocess.run([ffmpeg(), '-loglevel', 'error', '-i', board.rel(f), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def add_sfx(board, a, cues, length):
    """"sfx": {"click": "assets/sfx/click.wav", "flood": {"file": "...", "volume": 0.4}, "pop": "...", "volume": 0.5}
    Keys are cue kinds: click, zoom, flood, scene, notify, or your own from a {"cue": "pop"} event.
    Every cue of that kind gets the sound, shifted so its loudest moment lands exactly on the cue."""
    cfg = board.data.get('sfx') or {}
    vol, n = float(cfg.get('volume', 0.5)), len(a)
    used = 0
    for kind, f in cfg.items():
        if kind == 'volume' or not f:
            continue
        f, v = (f.get('file'), float(f.get('volume', vol))) if isinstance(f, dict) else (f, vol)
        snd = load(board, f) * v
        peak = int(np.argmax(np.abs(snd).sum(axis=1)))
        last = -9.0
        for t, k in cues['cues']:
            if k != kind or t - last < 0.15:            # no machine-gun repeats
                continue
            last = t
            at = int(t * SR) - peak
            s0, s1 = max(0, at), min(n, at + len(snd))
            if s1 > s0:
                a[s0:s1] += snd[s0 - at:s1 - at]; used += 1
    if used:
        print('  sfx: %d sounds placed on cues' % used)
    return a


def main():
    board = Board(sys.argv[1])
    cues = board.json_in('cues.json')
    if not cues:
        sys.exit('Run render.py first.')
    if cues.get('preview'):
        print('  note: this is a preview render (--until); render the full video before delivering.')
    length = cues['length']
    name = board.data.get('output_name') or os.path.splitext(os.path.basename(board.path))[0]
    out = os.path.join(board.out, name + '.mp4')
    vf = 'scale=in_range=full:out_range=tv,format=yuv420p,fade=t=in:st=0:d=0.4,fade=t=out:st=%.2f:d=0.7' % (length - 0.7)
    if not board.data.get('music') and board.data.get('sfx'):
        a = add_sfx(board, np.zeros((int(length * SR), 2), np.float32), cues, length)
        wav = os.path.join(board.out, 'music_fit.wav')
        subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', wav],
                       input=a.astype(np.float32).tobytes(), check=True)
        audio = ['-i', wav, '-filter_complex', '[1:a]loudnorm=I=-16:TP=-2:LRA=11,alimiter=limit=0.84:level=disabled,aresample=48000[m]', '-map', '0:v', '-map', '[m]']
    elif board.data.get('music'):
        wav = fit_music(board, length, cues)
        audio = ['-i', wav, '-filter_complex', '[1:a]loudnorm=I=-16:TP=-2:LRA=11,alimiter=limit=0.84:level=disabled,aresample=48000[m]', '-map', '0:v', '-map', '[m]']
    else:
        print('  note: no "music" in the storyboard, so the video is silent. Add "music": {"file": ..., "lift_on": "app_in"}'
              ' with a track you have the rights to use (see SKILL.md, Music).')
        audio = ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-map', '0:v', '-map', '1:a', '-shortest']
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', os.path.join(board.out, 'frames.mp4')] + audio +
                   ['-vf', vf, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-color_range', 'tv',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
    print('wrote', out)


if __name__ == '__main__':
    main()
