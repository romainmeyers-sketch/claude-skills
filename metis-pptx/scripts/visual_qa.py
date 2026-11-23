"""Export PPTX slides as images using PowerPoint COM automation.

Uses Microsoft PowerPoint to render each slide as a high-fidelity PNG image
for visual quality assurance inspection.

Usage:
    python visual_qa.py <pptx_file> [output_dir] [--dpi 150] [--format png|jpg]

Examples:
    python visual_qa.py output.pptx qa_images/
    python visual_qa.py output.pptx --dpi 200
"""

import argparse
import os
import subprocess
import sys
import time


def _powerpoint_is_running():
    """Check if PowerPoint is already running before we start COM."""
    try:
        out = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return "POWERPNT.EXE" in out
    except Exception:
        return False


def export_slides(pptx_path, output_dir, dpi=150, fmt="PNG"):
    """Export each slide from a PPTX file as an image using PowerPoint COM.

    Args:
        pptx_path: Path to the PPTX file.
        output_dir: Directory to save exported images.
        dpi: Resolution in dots per inch (default 150).
        fmt: Image format - 'PNG' or 'JPG' (default 'PNG').

    Returns:
        List of exported image file paths.
    """
    try:
        import win32com.client
    except ImportError:
        print("Error: pywin32 is not installed. Install with: pip install pywin32",
              file=sys.stderr)
        sys.exit(1)

    pptx_path = os.path.abspath(pptx_path)
    output_dir = os.path.abspath(output_dir)

    if not os.path.exists(pptx_path):
        print(f"Error: {pptx_path} does not exist", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    was_running = _powerpoint_is_running()
    ppt = None
    prs = None
    try:
        ppt = win32com.client.DispatchEx("PowerPoint.Application")
        ppt.DisplayAlerts = 0  # ppAlertsNone

        # Open read-only, headless (no window)
        prs = ppt.Presentations.Open(
            pptx_path,
            ReadOnly=True,
            Untitled=False,
            WithWindow=False,
        )

        # Calculate export dimensions from slide size and DPI
        # PowerPoint reports dimensions in points (72 points = 1 inch)
        slide_w_pts = prs.PageSetup.SlideWidth
        slide_h_pts = prs.PageSetup.SlideHeight
        scale = dpi / 72.0
        export_w = int(slide_w_pts * scale)
        export_h = int(slide_h_pts * scale)

        total = prs.Slides.Count
        exported = []
        ext = fmt.lower()

        for i in range(1, total + 1):
            slide = prs.Slides(i)
            out_file = os.path.join(output_dir, f"slide-{i}.{ext}")
            slide.Export(out_file, fmt, export_w, export_h)
            exported.append(out_file)
            print(f"  Exported slide {i}/{total}: {out_file}")

        print(f"\nExported {len(exported)} slides to {output_dir}")
        return exported

    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        try:
            if prs is not None:
                prs.Close()
        except Exception:
            pass
        if not was_running:
            try:
                if ppt is not None:
                    ppt.Quit()
            except Exception:
                pass
            time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export PPTX slides as images for visual QA"
    )
    parser.add_argument("pptx_file", help="PPTX file to export")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="qa_images",
        help="Output directory (default: qa_images/)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="Export resolution in DPI (default: 150)",
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpg", "PNG", "JPG"],
        default="PNG",
        dest="fmt",
        help="Image format (default: PNG)",
    )
    args = parser.parse_args()

    export_slides(args.pptx_file, args.output_dir, dpi=args.dpi, fmt=args.fmt.upper())
