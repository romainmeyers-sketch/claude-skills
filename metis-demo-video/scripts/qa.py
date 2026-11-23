"""Step 3: look at it. Contact sheets of every scene, so problems are caught before the user sees them.

  python qa.py storyboard.json [video.mp4]              -> out/qa/scenes_*.jpg (+ a printed checklist)
  python qa.py storyboard.json [video.mp4] --every 1.5  -> also out/qa/timeline_*.jpg, one frame every 1.5 s

Each scene gets three labelled frames (just after it starts, the middle, just before it ends).
The timeline sheets sample the whole video at a fixed step with timestamps: use them to catch
what happens between those three frames (blank gaps between scenes, a caption change, a click).
Frames are 960 px wide so text reads at its real size; open every sheet and check them against
references/quality-checklist.md.
"""
import argparse, os, subprocess
from PIL import Image, ImageDraw
from common import Board, ffmpeg

W = 960


def grab(video, t, f):
    subprocess.run([ffmpeg(), '-loglevel', 'error', '-y', '-ss', '%.2f' % t, '-i', video, '-frames:v', '1', '-vf', 'scale=%d:-1' % W, f], check=True)


def sheets(shots, qa, prefix, per=9, cols=3):
    out = []
    for k in range(0, len(shots), per):
        group = shots[k:k + per]
        ims = [Image.open(f) for f, _ in group]
        w, h = ims[0].size
        rows = (len(group) + cols - 1) // cols
        sheet = Image.new('RGB', (w * cols, h * rows), 'white')
        for j, (im, (_, lab)) in enumerate(zip(ims, group)):
            dr = ImageDraw.Draw(im)
            dr.rectangle([0, 0, 8 + 7 * len(lab), 22], fill='black'); dr.text((6, 5), lab, fill='white')
            sheet.paste(im, ((j % cols) * w, (j // cols) * h))
        p = os.path.join(qa, '%s_%d.jpg' % (prefix, k // per + 1))
        sheet.save(p, quality=85); out.append(p)
    for f, _ in shots:
        os.remove(f)
    return out


def pops(video, fps=30):
    """Single-frame pops: a frame that differs from both neighbours far more than the motion around it
    (a flash, an element that blinks in for one frame). Returns the times to check."""
    import numpy as np
    w, h = 160, 90
    raw = subprocess.run([ffmpeg(), '-loglevel', 'error', '-i', video, '-vf', 'scale=%d:%d,format=gray' % (w, h), '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
    if len(fr) < 8:
        return []
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))           # d[i] = change from frame i to i+1
    back = np.abs(fr[2:] - fr[:-2]).mean(axis=(1, 2))          # frame i-1 vs i+1: small if frame i was the odd one
    out = []
    for i in range(1, len(d) - 1):
        ctx = np.median(np.concatenate([d[max(0, i - 6):i - 1], d[i + 2:i + 8]])) if i > 2 else d[i]
        if d[i - 1] > 6 and d[i] > 6 and min(d[i - 1], d[i]) > 3 * max(ctx, 1) and back[i - 1] < 0.5 * min(d[i - 1], d[i]):
            out.append(round(i / float(fps), 2))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('storyboard')
    ap.add_argument('video', nargs='?')
    ap.add_argument('--every', type=float, help='also make timeline sheets with one frame every N seconds (e.g. 1.5)')
    a = ap.parse_args()
    board = Board(a.storyboard)
    cues = board.json_in('cues.json')
    if not cues:
        raise SystemExit('Run render.py first.')
    name = board.data.get('output_name') or os.path.splitext(os.path.basename(board.path))[0]
    video = a.video or os.path.join(board.out, name + '.mp4')
    if not os.path.exists(video):
        video = os.path.join(board.out, 'frames.mp4')
    qa = os.path.join(board.out, 'qa')
    os.makedirs(qa, exist_ok=True)
    for f in os.listdir(qa):                       # no stale sheets from an earlier, longer render
        if f.endswith('.jpg'):
            os.remove(os.path.join(qa, f))
    marks = cues['marks']
    shots = []
    for (label, t0), (_, t1) in zip(marks, marks[1:]):
        for frac, tag in ((0.12, 'start'), (0.5, 'mid'), (0.9, 'end')):
            t = t0 + (t1 - t0) * frac
            f = os.path.join(qa, 'f_%07.2f.jpg' % t)
            grab(video, t, f)
            shots.append((f, 'scene %s  %s  %.1fs' % (label, tag, t)))
    out = sheets(shots, qa, 'scenes')
    if a.every:
        shots, t = [], 0.0
        while t < cues['length'] - 0.05:
            f = os.path.join(qa, 't_%07.2f.jpg' % t)
            grab(video, t, f)
            shots.append((f, '%.1fs' % t)); t += a.every
        out += sheets(shots, qa, 'timeline', per=12, cols=3)
    print('video: %s  (%.1fs)' % (video, cues['length']))
    print('contact sheets (open every one):')
    for p in out:
        print('  ' + p)
    zooms = sum(1 for _, k in cues['cues'] if k == 'zoom')
    caps = [k[4:] for _, k in cues['cues'] if k.startswith('cap:')]
    print('captions (%d): %s' % (len(caps), ' | '.join(caps)))
    print('camera moves: %d   length: %.0fs %s' % (zooms, cues['length'], '(over 2 min: consider cutting)' if cues['length'] > 120 else ''))
    if a.every:
        p = pops(video)
        print('single-frame pops: %s' % (', '.join('%.2fs' % t for t in p) + '  (check each with qa.py --every 0.1 around it)' if p else 'none'))


if __name__ == '__main__':
    main()
