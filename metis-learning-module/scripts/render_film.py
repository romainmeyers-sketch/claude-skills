"""Turn a film HTML file into a real video file.

    python render_film.py films/intro.html
    python render_film.py films/intro.html --fps 30 --scale 1 --out out/intro.mp4

It does not screen-record. It calls the film's own __FILMRENDER.frame(t) once
per frame and captures the canvas, so the result is perfectly smooth however
slowly the page draws, and it is identical on every machine. That only works
if frame(t) is deterministic: see references/film-format.md.

Audio: the music bed is rendered offline through the film's __FILMRENDER
.audio() and muxed in. Narration is NOT captured, because speechSynthesis
cannot be rendered offline by any browser. For a film that needs a voice in
the MP4, record the lines, drop the WAV next to the film as <name>.vo.wav,
and this script will mix it under the music.

Needs: pip install playwright imageio-ffmpeg numpy pillow  (then: playwright install chromium)
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile


def need(mod, pip):
    try:
        return __import__(mod)
    except ImportError:
        sys.exit("Missing dependency. Run: pip install " + pip)


def ffmpeg_exe():
    imageio_ffmpeg = need("imageio_ffmpeg", "imageio-ffmpeg")
    return imageio_ffmpeg.get_ffmpeg_exe()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film", help="path to the film HTML file")
    ap.add_argument("--out", help="output .mp4 (default: next to the film)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--scale", type=float, default=1.0,
                    help="1.0 renders at the canvas size, 0.5 at half")
    ap.add_argument("--until", type=float, default=None,
                    help="stop after N seconds, for a quick look while iterating")
    args = ap.parse_args()

    film = os.path.abspath(args.film)
    if not os.path.exists(film):
        sys.exit("No such file: " + film)
    out = os.path.abspath(args.out or os.path.splitext(film)[0] + ".mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    need("playwright", "playwright")
    from playwright.sync_api import sync_playwright

    tmp = tempfile.mkdtemp(prefix="film-")
    frames_dir = os.path.join(tmp, "frames")
    os.makedirs(frames_dir)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required",
                                           "--disable-lcd-text"])
        page = browser.new_page(viewport={"width": 1280, "height": 760},
                                device_scale_factor=1)
        page.goto("file:///" + film.replace("\\", "/") + "?embed=1")
        page.wait_for_function("window.__FILMRENDER && window.__FILMRENDER.total > 0",
                               timeout=20000)

        info = page.evaluate("() => ({total: __FILMRENDER.total,"
                             " w: __FILMRENDER.canvas.width,"
                             " h: __FILMRENDER.canvas.height})")
        total = float(args.until or info["total"])
        w = int(info["w"] * args.scale) // 2 * 2
        h = int(info["h"] * args.scale) // 2 * 2
        n = int(round(total * args.fps))
        print("film   %s" % os.path.basename(film))
        print("length %.2fs, %d frames at %dfps, %dx%d" % (total, n, args.fps, w, h))

        # Hide the chrome so only the picture is captured.
        page.evaluate("""() => {
            ['cover','ctrl'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.style.display = 'none';
            });
        }""")

        for i in range(n):
            t = i / float(args.fps)
            data = page.evaluate(
                """(t) => { __FILMRENDER.frame(t);
                            return __FILMRENDER.canvas.toDataURL('image/png'); }""", t)
            raw = base64.b64decode(data.split(",", 1)[1])
            with open(os.path.join(frames_dir, "f%06d.png" % i), "wb") as fh:
                fh.write(raw)
            if i % args.fps == 0:
                sys.stdout.write("\r  frame %d/%d" % (i, n))
                sys.stdout.flush()
        print("\r  frames done     ")

        # The music bed, rendered offline so it lines up with the frames.
        wav = os.path.join(tmp, "music.wav")
        try:
            pcm = page.evaluate("""async () => {
                const buf = await __FILMRENDER.audio(48000);
                const ch = [buf.getChannelData(0), buf.getChannelData(1)];
                const n = buf.length, out = new Int16Array(n * 2);
                for (let i = 0; i < n; i++){
                    for (let c = 0; c < 2; c++){
                        let v = Math.max(-1, Math.min(1, ch[c][i]));
                        out[i*2+c] = v < 0 ? v * 0x8000 : v * 0x7FFF;
                    }
                }
                return Array.from(new Uint8Array(out.buffer));
            }""")
            write_wav(wav, bytes(bytearray(pcm)), 48000, 2)
        except Exception as exc:                       # noqa: BLE001
            print("  no audio track (%s)" % exc)
            wav = None

        browser.close()

    # A recorded narration track, if one was supplied next to the film.
    vo = os.path.splitext(film)[0] + ".vo.wav"
    vo = vo if os.path.exists(vo) else None
    if vo:
        print("  mixing narration from %s" % os.path.basename(vo))

    ff = ffmpeg_exe()
    cmd = [ff, "-y", "-loglevel", "error",
           "-framerate", str(args.fps), "-i", os.path.join(frames_dir, "f%06d.png")]
    if wav:
        cmd += ["-i", wav]
    if vo:
        cmd += ["-i", vo]

    if wav and vo:
        cmd += ["-filter_complex", "[1:a]volume=0.35[m];[2:a]volume=1.0[v];[m][v]amix=inputs=2:duration=first[a]",
                "-map", "0:v", "-map", "[a]"]
    elif wav or vo:
        cmd += ["-map", "0:v", "-map", "1:a"]

    cmd += ["-vf", "scale=%d:%d:flags=lanczos" % (w, h),
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if wav or vo:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += [out]

    subprocess.run(cmd, check=True)
    size = os.path.getsize(out) / 1024.0 / 1024.0
    print("wrote %s  (%.1f MB)" % (out, size))
    if not vo:
        print("note: no narration in the MP4. Captions are burned into the film's "
              "own canvas only if the film draws them; record the lines to "
              "%s to add a voice." % os.path.basename(os.path.splitext(film)[0] + ".vo.wav"))


def write_wav(path, pcm_bytes, rate, channels):
    """A 16-bit PCM wav, written by hand to avoid another dependency."""
    import struct
    data_len = len(pcm_bytes)
    with open(path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_len))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, channels, rate,
                            rate * channels * 2, channels * 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", data_len))
        f.write(pcm_bytes)


if __name__ == "__main__":
    main()
