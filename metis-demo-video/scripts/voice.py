"""Voiceover: turn the storyboard's narration lines into audio with ElevenLabs, or with Kokoro on this computer (no key).

  python voice.py storyboard.json                 generate (cached) -> out/voice/manifest.json
  python voice.py storyboard.json --voice romain  every line in another speaker's voice
  python voice.py storyboard.json --dry           no API calls: estimate durations (for timing tests)

Storyboard block:
  "voiceover": {
    "model": "eleven_multilingual_v2",
    "voices": {"rohan": "<voice id>", "romain": "<voice id>"},
    "default": "rohan",
    "settings": {"stability": 0.5, "similarity_boost": 0.85, "style": 0.15, "use_speaker_boost": true},
    "lines": {"intro": "text", "close": {"text": "text", "voice": "romain"}}
  }
Pauses (use sparingly: inserted silence tends to sound like a full stop; separate lines with a "gap" sound more natural):
write {pause 0.5} anywhere in a line for a deliberate beat ("Your first day, {pause 0.5} handled."). The voice
speaks the line in ONE natural take, untouched (no tags, no breath sounds), then clean silence is inserted at that spot, and
the word timings shift with it, so captions and actions stay in sync. A pause is the TOTAL gap wanted: the voice's own gap
counts toward it. "cadence": {"sentence": 0.4, "comma": 0.15} adds automatic pauses after sentences/commas inside a line;
"gap" (seconds, default 0.45) is the silence between lines, and a line can override it with its own "gap".
A line can be {"text": "Read the guide.", "say": "Reed the guide."}: the voice gets "say", captions and the screen keep "text"
(same number of words). Words that can be said two ways (read, lead, live, close, record, present...) are flagged before any
audio is generated, and must be resolved with "say" or acknowledged with "ok": ["word"].
Engine: add "engine": "kokoro" to the block to speak with Kokoro-82M on this computer instead of ElevenLabs: no account, no key,
no network at all (setup.py --kokoro installs it from scripts/kokoro.lock.json, hash-checked and scanned; this script refuses to
run if the installed packages or model files do not match that lock). Then "voices" maps names to Kokoro voice ids
("af_heart", "am_michael", "bf_emma", ...) and "model", "settings" and "seed" are ignored (Kokoro is deterministic, so takes.py has
nothing to audition). Stock voices only: Kokoro cannot reproduce a cloned voice. Everything else (pronounce, say, pauses, cadence,
gap, captions, ducking) works the same. Default engine is "elevenlabs", so existing storyboards are untouched.
Scenes and app steps reference a line with  "vo": "intro".  Changing the speaker is one edit:
"default", a line's "voice", or --voice on the command line. Audio is cached per (voice, text, settings),
so re-running only pays for lines that changed.

The ElevenLabs API key is read from $ELEVENLABS_API_KEY or from ~/.metis/demo-video/elevenlabs.key (never from the
storyboard, never printed). Only clone a voice with that person's consent.
"""
import argparse, hashlib, json, os, re, subprocess, sys, urllib.request, urllib.error
from common import Board, ffmpeg

KEY_FILE = os.path.expanduser('~/.metis/demo-video/elevenlabs.key')


def api_key():
    k = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not k and os.path.exists(KEY_FILE):
        k = open(KEY_FILE).read().strip()
    return k


def duration(path):
    err = subprocess.run([ffmpeg(), '-i', path], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])


def synth(key, voice_id, model, text, settings, out, seed=None):
    """Speak `text`; save the mp3 and return word timings [[word, start, end], ...] in seconds."""
    import base64
    payload = {'text': text, 'model_id': model, 'voice_settings': settings}
    if seed is not None:
        payload['seed'] = int(seed)                       # same text + same seed = the same take every time
    body = json.dumps(payload).encode()
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128' % voice_id, data=body,
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit('ElevenLabs refused the request (HTTP %d): %s' % (e.code, e.read().decode('utf-8', 'replace')[:300]))
    with open(out, 'wb') as f:
        f.write(base64.b64decode(d['audio_base64']))
    al = d.get('alignment') or d.get('normalized_alignment')
    ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    words, cur, w0, w1, in_tag = [], '', None, None, False
    for c, a0, a1 in zip(ch, st, en):
        if c == '<': in_tag = True
        if in_tag:                                         # <break .../> tags are silence, not words
            if c == '>': in_tag = False
            continue
        if c.isspace():
            if cur: words.append([cur, round(w0, 3), round(w1, 3)]); cur = ''
            continue
        if not cur: w0 = a0
        cur += c; w1 = a1
    if cur: words.append([cur, round(w0, 3), round(w1, 3)])
    return words


_KOKORO = {}


def kokoro_pipeline(lang, lock):
    """One Kokoro pipeline per language, built on first use from the model files the lock has just verified. Nothing is
    fetched here: Hugging Face is set offline and the config, model and voices are passed as explicit local paths."""
    if lang not in _KOKORO:
        import warnings
        import kokoro_lock
        os.environ.setdefault('HF_HUB_OFFLINE', '1')
        warnings.filterwarnings('ignore', category=FutureWarning)                  # torch deprecations raised inside kokoro
        warnings.filterwarnings('ignore', category=UserWarning, module='torch')
        from kokoro import KModel, KPipeline
        if not _KOKORO.get('_model'):
            _KOKORO['_model'] = KModel(repo_id=lock['model']['repo'], config=kokoro_lock.model_file(lock, 'config.json'),
                                       model=kokoro_lock.model_file(lock, 'kokoro-v1_0.pth')).eval()
        _KOKORO[lang] = KPipeline(lang_code=lang, repo_id=lock['model']['repo'], model=_KOKORO['_model'])
    return _KOKORO[lang]


def synth_kokoro(text, voice, out):
    """Speak `text` with Kokoro-82M on this computer; save the mp3 and return word timings [[word, start, end], ...] in
    seconds, the same shape synth() returns. Kokoro yields one chunk per ~500 phonemes, each with its own audio and
    token timings that restart at zero, so chunks are concatenated and every timing is offset by the audio before it.
    Tokens are grouped back into words at whitespace (so "day," is one word, as in text.split()); a token Kokoro left
    untimed (start_ts or end_ts None, or an end of 0) contributes its text but no time, and a word with no timed token
    at all is dropped with a note. A voice id's first letter is its language ('a' American, 'b' British English)."""
    import time
    import numpy as np
    import kokoro_lock
    SR = 24000
    lock = kokoro_lock.ensure(voice)                         # packages, model and this voice all match scripts/kokoro.lock.json, or stop
    pipe = kokoro_pipeline('b' if voice.startswith('b') else 'a', lock)
    t0 = time.time()
    pieces, words, offset, dropped = [], [], 0.0, []
    for r in pipe(text, voice=kokoro_lock.voice_file(lock, voice)):
        audio = r.audio.detach().cpu().numpy().astype(np.float32) if r.audio is not None else np.zeros(0, np.float32)
        txt, w0, w1 = '', None, None
        for t in r.tokens or []:
            txt += t.text
            if t.start_ts is not None and t.end_ts is not None and t.end_ts > 0:
                if w0 is None: w0 = offset + t.start_ts
                w1 = offset + t.end_ts
            if t.whitespace:                                 # this token ends a word
                if txt.strip():
                    if w0 is None or w1 is None: dropped.append(txt)
                    else: words.append([txt, round(w0, 3), round(w1, 3)])
                txt, w0, w1 = '', None, None
        if txt.strip():                                      # last word of the chunk has no trailing space
            if w0 is None or w1 is None: dropped.append(txt)
            else: words.append([txt, round(w0, 3), round(w1, 3)])
        pieces.append(audio)
        offset += len(audio) / SR
    if dropped:
        print('  note: Kokoro gave no timing for %s; captions will show the spoken spelling for this line' % ', '.join('"%s"' % d for d in dropped))
    pcm_ = (np.concatenate(pieces) if pieces else np.zeros(0, np.float32)).astype(np.float32)
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-',
                    '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '128k', out], input=pcm_.tobytes(), check=True)
    print('  kokoro: %d words, %.1fs of audio, %.1fs to make' % (len(words), offset, time.time() - t0), flush=True)
    return words


# Words spelled the same but said differently depending on tense or part of speech. A voice has to guess from context,
# and a short line gives it almost none ("Read the guide." came out as past tense "red"). Each flagged word must be
# resolved per line: give the line a "say" (spoken form) or list the word under "ok" when the default is what you want.
HETERONYMS = {
    'read': 'present "reed" (Reed the guide) / past "red" (Red the report)',
    'lead': 'verb "leed" / the metal or "in the lead" "led"',
    'live': 'verb "liv" / adjective "lyve" (a lyve demo)',
    'lives': 'verb "livs" / plural noun "lyvz"',
    'close': 'verb "cloze" / adjective or "nearby" "clohss"',
    'wind': 'noun "wihnd" / verb "wynd"',
    'tear': 'noun (cry) "teer" / verb (rip) "tair"',
    'wound': 'injury "woond" / past of wind "wownd"',
    'bass': 'fish "bass" / music "base"',
    'record': 'noun "REH-cord" / verb "rih-CORD"',
    'present': 'noun or adjective "PREZ-ent" / verb "prih-ZENT"',
    'content': 'noun "KON-tent" / adjective "kon-TENT"',
    'project': 'noun "PRAH-ject" / verb "pruh-JECT"',
    'resume': 'verb "rih-ZOOM" / noun "REZ-oo-may"',
    'minute': 'time "MIN-it" / tiny "my-NOOT"',
    'object': 'noun "OB-ject" / verb "ub-JECT"',
    'desert': 'noun "DEZ-ert" / verb "dih-ZERT"',
    'refuse': 'verb "rih-FYOOZ" / noun "REF-yoos"',
    'permit': 'noun "PER-mit" / verb "per-MIT"',
    'produce': 'noun "PROH-doos" / verb "pruh-DOOS"',
    'row': 'line "roh" / argument "rau"',
    'bow': 'tie "boh" / bend "bau"',
    'dove': 'bird "duv" / past of dive "dohv"',
    'sow': 'plant "soh" / pig "sau"',
    'does': 'verb "duz" / plural deer "dohz"',
    'axes': 'plural of axe "AK-siz" / plural of axis "AK-seez"',
}


PAUSE = re.compile(r'\s*\{pause\s+([0-9.]+)\}\s*')


def display_text(line):
    """What is shown on screen: the text with pause markers removed."""
    t = line if isinstance(line, str) else line['text']
    return re.sub(r'\s+', ' ', PAUSE.sub(' ', t)).strip()


def build_spoken(vo, line):
    """What the voice is given: the 'say' form if any, with pronunciation respellings, and NOTHING else.
    No tags, no markers: the voice delivers each line in one natural take. Pauses are added afterwards as silence."""
    d = line if isinstance(line, dict) else {}
    t = d.get('say') or (line if isinstance(line, str) else line['text'])
    t = PAUSE.sub(' ', t)
    for k, v in vo.get('pronounce', {}).items():
        t = re.sub(r'\b%s\b' % re.escape(k), v, t)
    return re.sub(r'\s+', ' ', t).strip()


def plan_pauses(vo, line):
    """{index of the word the pause comes AFTER: total gap wanted in seconds}.
    Explicit  {pause N}  markers, plus voiceover.cadence: {"sentence": 0.4, "comma": 0.15} for the automatic ones."""
    raw = line if isinstance(line, str) else line['text']
    d = line if isinstance(line, dict) else {}
    plan, tokens, pos = {}, 0, 0
    for m in PAUSE.finditer(raw):
        tokens += len(raw[pos:m.start()].split())
        if tokens: plan[tokens - 1] = float(m.group(1))
        pos = m.end()
    words = display_text(line).split()
    cad = vo.get('cadence', {})
    sent = float(d.get('sentence_pause', cad.get('sentence', 0.0)))
    comma = float(cad.get('comma', 0.0))
    for i, w in enumerate(words[:-1]):
        if i in plan: continue
        if sent and re.search(r'[.?!]["\')\]]*$', w): plan[i] = sent
        elif comma and w.endswith(','): plan[i] = comma
    return plan


def apply_pauses(raw_mp3, words, plan, out_mp3):
    """Insert clean silence into the finished take at the natural gap after the planned words.
    A pause is the TOTAL gap you want, so the voice's own gap counts toward it. Returns the re-timed words."""
    import numpy as np
    SR = 44100
    pcm_ = subprocess.run([ffmpeg(), '-loglevel', 'error', '-i', raw_mp3, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm_, np.float32)
    pieces, last, shift = [], 0, 0.0
    new_words = [list(w) for w in words]
    fade = int(0.008 * SR)
    for idx in sorted(plan):
        if idx + 1 >= len(words): continue
        gap = words[idx + 1][1] - words[idx][2]
        add = plan[idx] - max(gap, 0.0)
        if add <= 0.02: continue
        cut = int(((words[idx][2] + words[idx + 1][1]) / 2 if gap > 0 else words[idx + 1][1]) * SR)
        seg = a[last:cut].copy()
        if len(seg) > fade: seg[-fade:] *= np.linspace(1, 0, fade)
        pieces += [seg, np.zeros(int(add * SR), np.float32)]
        last = cut
        for j in range(idx + 1, len(new_words)):
            new_words[j][1] = round(new_words[j][1] + add, 3); new_words[j][2] = round(new_words[j][2] + add, 3)
        shift += add
    tail = a[last:].copy()
    if pieces and len(tail) > fade: tail[:fade] *= np.linspace(0, 1, fade)
    out = np.concatenate(pieces + [tail]) if pieces else a
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'libmp3lame', '-b:a', '128k', out_mp3],
                   input=out.astype(np.float32).tobytes(), check=True)
    return new_words


def speak_line(key, vo, line, lid, outdir, vid, seed=None, tag=''):
    """One line, in one natural take, then the planned silence. Both steps are cached.
    Returns (mp3 path, words with display spelling)."""
    model = vo.get('model', 'eleven_multilingual_v2')
    settings = vo.get('settings', {'stability': 0.5, 'similarity_boost': 0.85, 'style': 0.15, 'use_speaker_boost': True})
    say_text = build_spoken(vo, line)
    engine = vo.get('engine', 'elevenlabs')
    if engine == 'kokoro':                                   # model, settings and seed do not apply: same words, same voice, same take
        import kokoro_lock
        rev = kokoro_lock.load()['model']['revision'][:12]  # a new pinned model commit regenerates the audio
        h = hashlib.sha1(json.dumps(['kokoro', rev, vid, say_text, 'ts1'], sort_keys=True).encode()).hexdigest()[:12]
    else:
        h = hashlib.sha1(json.dumps([vid, model, say_text, settings, 'ts1', seed], sort_keys=True).encode()).hexdigest()[:12]
    raw = os.path.join(outdir, '%s%s_%s.mp3' % (tag, lid, h))
    wj = raw + '.words.json'
    if not (os.path.exists(raw) and os.path.exists(wj)):
        print('  speaking %s%s' % (tag, lid), flush=True)
        words = synth_kokoro(say_text, vid, raw) if engine == 'kokoro' else synth(key, vid, model, say_text, settings, raw, seed)
        json.dump(words, open(wj, 'w'))
    words = json.load(open(wj))
    disp = display_text(line).split()
    if len(disp) == len(words):                          # show the real spelling, keep the spoken timing
        words = [[d, w[1], w[2]] for d, w in zip(disp, words)]
    else:
        print('  note: line "%s" has a different word count when spoken, so captions show the spoken spelling' % lid)
    plan = plan_pauses(vo, line) if len(disp) == len(words) else {}
    if not plan:
        return raw, words
    ph = hashlib.sha1(json.dumps(sorted(plan.items())).encode()).hexdigest()[:8]
    out = raw[:-4] + '_p%s.mp3' % ph
    if not os.path.exists(out + '.words.json'):
        nw = apply_pauses(raw, words, plan, out)
        json.dump(nw, open(out + '.words.json', 'w'))
    return out, json.load(open(out + '.words.json'))


def heteronym_problems(vo):
    """Lines that contain an ambiguous word and neither a "say" nor an "ok" acknowledgement."""
    out = []
    for lid, line in vo['lines'].items():
        text = display_text(line)
        d = line if isinstance(line, dict) else {}
        if d.get('say'):
            continue
        ok = {w.lower() for w in d.get('ok', [])}
        found = sorted({re.sub(r"[^a-z]", '', w.lower()) for w in text.split()} & set(HETERONYMS) - ok)
        if found:
            out.append((lid, text, found))
    return out


def segments(words, maxc=58):
    """Caption phrases: sentences, split at commas when a sentence is long."""
    segs, cur = [], []
    def flush():
        if cur:
            segs.append({'text': ' '.join(w[0] for w in cur), 'start': cur[0][1], 'end': cur[-1][2], 'i0': cur[0][3], 'i1': cur[-1][3]})
    for i, w in enumerate(words):
        cur.append([w[0], w[1], w[2], i])
        txt = ' '.join(x[0] for x in cur)
        if re.search(r'[.?!]$', w[0]) or (w[0].endswith(',') and len(txt) > maxc * 0.55):
            flush(); cur = []
    flush()
    return segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('storyboard'); ap.add_argument('--voice'); ap.add_argument('--dry', action='store_true'); ap.add_argument('--allow-heteronyms', action='store_true')
    a = ap.parse_args()
    board = Board(a.storyboard)
    vo = board.data.get('voiceover')
    if not vo:
        sys.exit('No "voiceover" block in the storyboard.')
    voices, model = vo['voices'], vo.get('model', 'eleven_multilingual_v2')
    settings = vo.get('settings', {'stability': 0.5, 'similarity_boost': 0.85, 'style': 0.15, 'use_speaker_boost': True})
    outdir = os.path.join(board.out, 'voice'); os.makedirs(outdir, exist_ok=True)
    prev = board.json_in('voice_manifest.json')
    if a.dry and prev and any(v.get('file') for v in prev.values()) and not os.environ.get('VOICE_DRY_FORCE'):
        sys.exit('Refusing --dry: out/voice_manifest.json holds real generated audio. A dry run would replace it with estimates.\n'
                 'Copy the project to test timing, or set VOICE_DRY_FORCE=1 if you really want to overwrite it.')
    engine = vo.get('engine', 'elevenlabs')
    if engine not in ('elevenlabs', 'kokoro'):
        sys.exit('voiceover.engine must be "elevenlabs" (the default) or "kokoro", not "%s".' % engine)
    key = '' if (a.dry or engine == 'kokoro') else api_key()
    if not a.dry and engine == 'elevenlabs' and not key:
        sys.exit('No ElevenLabs key found. Save it once with:\n  read -s -p "ElevenLabs key: " K; printf %s "$K" > %s; chmod 600 %s; unset K' % (KEY_FILE, KEY_FILE, KEY_FILE))
    probs = heteronym_problems(vo)
    if probs and not a.allow_heteronyms:
        print('Stopped before generating any audio: these lines contain words that can be pronounced two ways.')
        print('Fix each one in the storyboard (nothing is spent until they are resolved):\n')
        for lid, text, found in probs:
            print('  line "%s": %s' % (lid, text))
            for w in found:
                print('     "%s": %s' % (w, HETERONYMS[w]))
            print('     -> give the line a spoken form, for example')
            print('        "%s": {"text": "%s", "say": "<the same sentence, respelled so the word cannot be misread>"}' % (lid, text.replace('"', "'")))
            print('        or, if the default reading is already right: {"text": "...", "ok": ["%s"]}\n' % found[0])
        sys.exit(2)
    manifest = {}
    for lid, line in vo['lines'].items():
        text = display_text(line)
        who = a.voice or (line.get('voice') if isinstance(line, dict) else None) or vo.get('default')
        vid = voices.get(who)
        if not vid:
            sys.exit('Speaker "%s" has no voice id in voiceover.voices.' % who)
        gap = line.get('gap') if isinstance(line, dict) else None
        if a.dry:
            ws, t = [], 0.0
            for w in text.split():
                ws.append([w, round(t, 3), round(t + 0.35, 3)]); t += 0.38
            manifest[lid] = {'file': None, 'dur': round(len(text.split()) / 2.6 + 0.4, 2), 'voice': who, 'text': text, 'words': ws, 'segs': segments(ws), 'gap': gap}
            continue
        seed = line.get('seed') if isinstance(line, dict) else None
        f, words = speak_line(key, vo, line, lid, outdir, vid, seed)
        manifest[lid] = {'file': os.path.relpath(f, board.out), 'dur': round(duration(f), 2), 'voice': who, 'text': text,
                         'words': words, 'segs': segments(words), 'gap': gap}
    manifest['_gap'] = vo.get('gap', 0.45)
    board.json_out('voice_manifest.json', manifest)
    lines_ = {k: v for k, v in manifest.items() if not k.startswith('_')}
    print('%d lines, %.0fs of speech%s' % (len(lines_), sum(m['dur'] for m in lines_.values()), ' (estimated)' if a.dry else (' (Kokoro, on this computer)' if engine == 'kokoro' else '')))


if __name__ == '__main__':
    main()
