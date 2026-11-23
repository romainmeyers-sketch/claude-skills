"""Audition several takes of a narration line, so you can pick the one that sounds right and lock it in.

  python takes.py storyboard.json hook reveal            3 takes of each named line (default)
  python takes.py storyboard.json hook --n 4             four takes
  python takes.py storyboard.json hook --seeds 11 22 33  your own seeds

Writes out/takes.mp3: for each line and take, the voice says "<line>, take one." and then the line itself,
using the storyboard's voice, pronunciation map and settings. Listen, then lock the winner in the storyboard:

    "lines": {"hook": {"text": "Your first day started with a PDF.", "seed": 101}}

The same text with the same seed gives the same take every time, so the line sounds identical on every re-render.
Why this exists: a voice does not say a word the same way every time, so a tricky word (a brand name, say) can
come out right in one take and wrong in the next. Audition, pick, lock.
With "engine": "kokoro" there are no takes: Kokoro gives the same audio for the same words every time, so this script
says so and stops. Change the words, a "pronounce" respelling, or the voice id instead.
"""
import argparse, os, re, subprocess, sys
from common import Board, ffmpeg
import voice

NUMS = ['one', 'two', 'three', 'four', 'five', 'six']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('storyboard'); ap.add_argument('lines', nargs='+')
    ap.add_argument('--n', type=int, default=3); ap.add_argument('--seeds', nargs='*', type=int)
    ap.add_argument('--voice')
    a = ap.parse_args()
    board = Board(a.storyboard)
    vo = board.data['voiceover']
    if vo.get('engine', 'elevenlabs') == 'kokoro':
        print('Nothing to audition: this storyboard uses Kokoro, which gives the same take for the same words in the same voice every time.\n'
              'To change how a line sounds, change its words or its "pronounce" respelling, or pick another voice id in voiceover.voices.')
        return
    key = voice.api_key()
    if not key:
        sys.exit('No ElevenLabs key found. See references/voiceover.md.')
    model, settings = vo.get('model', 'eleven_multilingual_v2'), vo.get('settings', {'stability': 0.5, 'similarity_boost': 0.85, 'style': 0.15, 'use_speaker_boost': True})
    pron = vo.get('pronounce', {})
    seeds = a.seeds or [101 * (i + 1) for i in range(a.n)]
    d = os.path.join(board.out, 'voice', 'takes'); os.makedirs(d, exist_ok=True)

    def spoken(t):
        for k, v in pron.items():
            t = re.sub(r'\b%s\b' % re.escape(k), v, t)
        return t

    def sp(text, f, vid, seed=None):                 # short spoken labels
        if not os.path.exists(f):
            voice.synth(key, vid, model, text, settings, f, seed)
        return f

    def silence(sec, f):
        subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', str(sec), '-c:a', 'libmp3lame', f], check=True)
        return f

    s1, s2 = silence(0.8, os.path.join(d, 's1.mp3')), silence(1.6, os.path.join(d, 's2.mp3'))
    files = []
    for lid in a.lines:
        line = vo['lines'][lid]
        text = voice.display_text(line)
        who = a.voice or (line.get('voice') if isinstance(line, dict) else None) or vo['default']
        vid = vo['voices'][who]
        for i, seed in enumerate(seeds):
            files += [sp('%s, take %s.' % (lid, NUMS[i]), os.path.join(d, 'lab_%s_%d.mp3' % (lid, i)), vid), s1,
                      voice.speak_line(key, vo, line, lid, d, vid, seed, tag='take%d_' % seed)[0], s2]
    lst = os.path.join(d, 'list.txt')
    with open(lst, 'w') as f:
        f.write(''.join("file '%s'\n" % x for x in files))
    out = os.path.join(board.out, 'takes.mp3')
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-ar', '44100', '-ac', '1', '-c:a', 'libmp3lame', out], check=True)
    print('wrote %s  (take 1 = seed %d, take 2 = seed %d, ...)' % (out, seeds[0], seeds[1] if len(seeds) > 1 else seeds[0]))


if __name__ == '__main__':
    main()
