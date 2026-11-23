"""
Admin tool — re-render the Metis Timesaver PNG library on the shared drive.

The skill itself does NOT call this script during normal use. The shared-drive
PNG library at the path below is the single source of truth for `metis-pptx`'s
Path B (Timesaver) workflow; the skill reads those PNGs directly and never
renders them on the fly.

Run this only when:
  - The source Timesaver pptx has been updated (slides added, edited, reordered).
  - An admin needs to rebuild the shared library after a brand refresh.

Default source:
    G:\\Shared drives\\Knowledge Management\\New Brand Assets\\PPT Assets\\
    Metis_Timesaver Slides.pptx

Default destination (the canonical shared library that the skill reads):
    G:\\Shared drives\\Knowledge Management\\New Brand Assets\\PPT Assets\\
    timesaver_pngs\\

Override with --output-dir, or set METIS_TIMESAVER_PNG_DIR.

Requires Windows + Microsoft PowerPoint + pywin32 + write access to the
target folder. Running this overwrites every slide-N.png in --output-dir.
"""
import argparse
import os
import subprocess
import sys

DEFAULT_SOURCE = (
    r"G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets"
    r"\Metis_Timesaver Slides.pptx"
)
DEFAULT_OUTPUT = (
    r"G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets"
    r"\timesaver_pngs"
)


def _powerpoint_is_running():
    try:
        out = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"],
            stderr=subprocess.DEVNULL, text=True,
        )
        return "POWERPNT.EXE" in out
    except Exception:
        return False


def render(source_path: str, output_dir: str, width: int = 1600, height: int = 900):
    """Render every slide of the source deck to <output_dir>/slide-N.png via PowerPoint COM."""
    import win32com.client

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(source_path):
        sys.exit(f"Source not found: {source_path}")

    output_dir = os.path.abspath(output_dir).replace("/", "\\")
    source_path = os.path.abspath(source_path).replace("/", "\\")

    was_running = _powerpoint_is_running()
    ppt = win32com.client.DispatchEx("PowerPoint.Application")
    ppt.Visible = 1
    try:
        pres = ppt.Presentations.Open(source_path, WithWindow=False, ReadOnly=True)
        n = pres.Slides.Count
        print(f"Source: {source_path}")
        print(f"Slides: {n}")
        print(f"Output: {output_dir}")
        for idx in range(1, n + 1):
            out = os.path.join(output_dir, f"slide-{idx}.png")
            pres.Slides(idx).Export(out, "PNG", width, height)
            if idx % 20 == 0 or idx == n:
                print(f"  rendered {idx}/{n}")
        pres.Close()
    finally:
        if not was_running:
            ppt.Quit()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="Path to Metis_Timesaver Slides.pptx (default: shared G:\\ drive)")
    ap.add_argument("--output-dir",
                    default=os.environ.get("METIS_TIMESAVER_PNG_DIR", DEFAULT_OUTPUT),
                    help=f"Folder to write slide-N.png into (default: shared library at {DEFAULT_OUTPUT})")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=900)
    args = ap.parse_args()

    render(args.source, args.output_dir, args.width, args.height)
    print(f"\nDone. {len(os.listdir(args.output_dir))} previews available at:\n  {args.output_dir}")


if __name__ == "__main__":
    main()
