"""Make what the Video Hub needs after a render: a share copy under 18 MB and a small contact sheet.

  python hub_preview.py out/<name>.mp4 [--max-mb 18]

Writes next to the video:
  <name>-share.mp4      720p H.264 + AAC, sized to fit the hub's upload limit (for the gallery)
  <name>-sheet.jpg      12 frames in a 4x3 grid, 960 px wide
  <name>-sheet.b64      the sheet as base64 (under 180 KB) to store in the hub's sheets/v<N> doc
and prints a JSON summary (duration, sizes, paths).
"""
import base64, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return 'ffmpeg'


def duration(ff, path):
    out = subprocess.run([ff, '-i', path], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    src = os.path.abspath(args[0])
    max_mb = float(args[args.index('--max-mb') + 1]) if '--max-mb' in args else 18.0
    ff = ffmpeg_exe()
    base = os.path.splitext(src)[0]
    dur = duration(ff, src) or 1.0

    share = base + '-share.mp4'
    audio_kbps = 128
    video_kbps = max(400, int(max_mb * 8192 * 0.92 / dur) - audio_kbps)
    video_kbps = min(video_kbps, 3500)
    src_kbps = int(os.path.getsize(src) * 8 / 1024 / dur)          # never make the share copy bigger than the source
    video_kbps = max(300, min(video_kbps, src_kbps - audio_kbps if src_kbps > audio_kbps + 300 else src_kbps))
    subprocess.run([ff, '-loglevel', 'error', '-y', '-i', src, '-vf', 'scale=-2:720', '-c:v', 'libx264',
                    '-preset', 'medium', '-b:v', '%dk' % video_kbps, '-maxrate', '%dk' % int(video_kbps * 1.3),
                    '-bufsize', '%dk' % (video_kbps * 2), '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '%dk' % audio_kbps,
                    '-movflags', '+faststart', share], check=True)

    sheet = base + '-sheet.jpg'
    step = max(dur / 12.0, 0.5)
    for q in (4, 6, 9, 12):
        subprocess.run([ff, '-loglevel', 'error', '-y', '-i', src, '-vf',
                        'fps=1/%.3f,scale=240:-2,tile=4x3' % step, '-frames:v', '1', '-q:v', str(q), sheet], check=True)
        if os.path.getsize(sheet) < 130 * 1024:
            break
    with open(sheet, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    with open(base + '-sheet.b64', 'w') as f:
        f.write(b64)

    print(json.dumps({
        'video': src, 'duration_s': round(dur, 1), 'size_mb': round(os.path.getsize(src) / 1048576, 1),
        'share_path': share, 'share_mb': round(os.path.getsize(share) / 1048576, 1),
        'sheet_path': sheet, 'sheet_b64_path': base + '-sheet.b64', 'sheet_b64_kb': round(len(b64) / 1024, 1),
    }, indent=2))


if __name__ == '__main__':
    main()
