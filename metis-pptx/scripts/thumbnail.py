"""Create a thumbnail grid of PPTX slides using PowerPoint COM.

Generates a visual overview grid with slide numbers and filenames as labels.

Usage:
    python thumbnail.py <pptx_file> [output_prefix] [--cols N]

Examples:
    python thumbnail.py presentation.pptx
    python thumbnail.py presentation.pptx my_deck --cols 4
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import defusedxml.minidom

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is not installed. Install with: pip install Pillow",
          file=sys.stderr)
    sys.exit(1)


# Configuration
THUMBNAIL_WIDTH = 300
DEFAULT_COLS = 3
MAX_COLS = 6
LABEL_HEIGHT = 20
PADDING = 10
BG_COLOR = (255, 255, 255)
LABEL_COLOR = (80, 80, 80)
BORDER_COLOR = (200, 200, 200)
HIDDEN_X_COLOR = (200, 50, 50)
JPEG_QUALITY = 95
MAX_SLIDES_PER_GRID = 12


def get_slide_info(pptx_path):
    """Extract slide metadata (order and visibility) from the PPTX file."""
    slides = []

    with zipfile.ZipFile(pptx_path, "r") as zf:
        try:
            pres_xml = zf.read("ppt/presentation.xml").decode("utf-8")
            dom = defusedxml.minidom.parseString(pres_xml)
        except Exception:
            return slides

        try:
            rels_xml = zf.read("ppt/_rels/presentation.xml.rels").decode("utf-8")
            rels_dom = defusedxml.minidom.parseString(rels_xml)
        except Exception:
            return slides

        rid_to_file = {}
        for rel in rels_dom.getElementsByTagName("Relationship"):
            rid = rel.getAttribute("Id")
            target = rel.getAttribute("Target")
            rel_type = rel.getAttribute("Type")
            if "slide" in rel_type and target.startswith("slides/"):
                rid_to_file[rid] = target.replace("slides/", "")

        for sld_id in dom.getElementsByTagName("p:sldId"):
            rid = sld_id.getAttributeNS(
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
                "id"
            )
            if not rid:
                rid = sld_id.getAttribute("r:id")

            filename = rid_to_file.get(rid)
            if not filename:
                continue

            hidden = False
            try:
                slide_xml = zf.read(f"ppt/slides/{filename}").decode("utf-8")
                if 'show="0"' in slide_xml:
                    hidden = True
            except Exception:
                pass

            slides.append({
                "filename": filename,
                "hidden": hidden,
                "number": len(slides) + 1,
            })

    return slides


def create_hidden_placeholder(width, height):
    """Create a placeholder image with an X pattern for hidden slides."""
    img = Image.new("RGB", (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.line([(0, 0), (width, height)], fill=HIDDEN_X_COLOR, width=2)
    draw.line([(width, 0), (0, height)], fill=HIDDEN_X_COLOR, width=2)
    try:
        draw.text((width // 2 - 25, height // 2 - 8), "HIDDEN",
                   fill=HIDDEN_X_COLOR)
    except Exception:
        pass
    return img


def create_grid(slide_images, labels, cols, output_path):
    """Arrange slide thumbnails in a labeled grid."""
    if not slide_images:
        return

    thumb_w = THUMBNAIL_WIDTH
    sample = slide_images[0]
    aspect = sample.height / sample.width
    thumb_h = int(thumb_w * aspect)

    rows = (len(slide_images) + cols - 1) // cols

    grid_w = PADDING + cols * (thumb_w + PADDING)
    grid_h = PADDING + rows * (thumb_h + LABEL_HEIGHT + PADDING)

    grid = Image.new("RGB", (grid_w, grid_h), BG_COLOR)
    draw = ImageDraw.Draw(grid)

    for idx, (img, label) in enumerate(zip(slide_images, labels)):
        row = idx // cols
        col = idx % cols

        x = PADDING + col * (thumb_w + PADDING)
        y = PADDING + row * (thumb_h + LABEL_HEIGHT + PADDING)

        thumb = img.resize((thumb_w, thumb_h), Image.LANCZOS)

        draw.rectangle(
            [x - 1, y - 1, x + thumb_w, y + thumb_h],
            outline=BORDER_COLOR
        )

        grid.paste(thumb, (x, y))

        try:
            draw.text((x + 2, y + thumb_h + 2), label, fill=LABEL_COLOR)
        except Exception:
            pass

    grid.save(output_path, "JPEG", quality=JPEG_QUALITY)
    print(f"Saved thumbnail grid: {output_path}")


def _powerpoint_is_running():
    try:
        out = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"],
            stderr=subprocess.DEVNULL, text=True,
        )
        return "POWERPNT.EXE" in out
    except Exception:
        return False


def convert_to_images_with_pptx(pptx_path, temp_dir):
    """Convert slides to images using PowerPoint COM automation."""
    try:
        import win32com.client
    except ImportError:
        print("Error: pywin32 not installed", file=sys.stderr)
        sys.exit(1)

    import time

    abs_path = os.path.abspath(pptx_path)
    abs_temp = os.path.abspath(temp_dir)

    was_running = _powerpoint_is_running()
    ppt = None
    prs = None
    try:
        ppt = win32com.client.DispatchEx("PowerPoint.Application")
        ppt.DisplayAlerts = 0

        prs = ppt.Presentations.Open(abs_path, ReadOnly=True, Untitled=False, WithWindow=False)

        # Export at 3x thumbnail size for quality
        slide_w_pts = prs.PageSetup.SlideWidth
        slide_h_pts = prs.PageSetup.SlideHeight
        aspect = slide_h_pts / slide_w_pts
        export_w = THUMBNAIL_WIDTH * 3
        export_h = int(export_w * aspect)

        images = []
        for i in range(1, prs.Slides.Count + 1):
            out_file = os.path.join(abs_temp, f"slide-{i}.png")
            prs.Slides(i).Export(out_file, "PNG", export_w, export_h)
            images.append(out_file)

        return images

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


def main():
    parser = argparse.ArgumentParser(description="Create a thumbnail grid of PPTX slides")
    parser.add_argument("pptx_file", help="PPTX file to thumbnail")
    parser.add_argument("output_prefix", nargs="?", default="thumbnails",
                        help="Output filename prefix (default: thumbnails)")
    parser.add_argument("--cols", type=int, default=DEFAULT_COLS,
                        help=f"Number of columns (default: {DEFAULT_COLS}, max: {MAX_COLS})")
    args = parser.parse_args()

    cols = min(args.cols, MAX_COLS)

    if not os.path.exists(args.pptx_file):
        print(f"Error: {args.pptx_file} not found", file=sys.stderr)
        sys.exit(1)

    slide_info = get_slide_info(args.pptx_file)
    if not slide_info:
        print("Error: Could not read slide information", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(slide_info)} slides")

    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = convert_to_images_with_pptx(args.pptx_file, temp_dir)

        slide_images = []
        labels = []

        for info in slide_info:
            num = info["number"]
            fname = info["filename"]

            if num <= len(image_paths):
                img = Image.open(image_paths[num - 1])
            else:
                img = create_hidden_placeholder(THUMBNAIL_WIDTH, int(THUMBNAIL_WIDTH * 0.5625))

            if info["hidden"]:
                img = img.copy()
                draw = ImageDraw.Draw(img)
                draw.line([(0, 0), (img.width, img.height)], fill=HIDDEN_X_COLOR, width=3)
                draw.line([(img.width, 0), (0, img.height)], fill=HIDDEN_X_COLOR, width=3)

            slide_images.append(img)
            label = f"#{num} {fname}"
            if info["hidden"]:
                label += " [HIDDEN]"
            labels.append(label)

        if len(slide_images) <= MAX_SLIDES_PER_GRID:
            output_path = f"{args.output_prefix}.jpg"
            create_grid(slide_images, labels, cols, output_path)
        else:
            for chunk_idx in range(0, len(slide_images), MAX_SLIDES_PER_GRID):
                chunk_imgs = slide_images[chunk_idx:chunk_idx + MAX_SLIDES_PER_GRID]
                chunk_labels = labels[chunk_idx:chunk_idx + MAX_SLIDES_PER_GRID]
                grid_num = chunk_idx // MAX_SLIDES_PER_GRID + 1
                output_path = f"{args.output_prefix}-{grid_num}.jpg"
                create_grid(chunk_imgs, chunk_labels, cols, output_path)


if __name__ == "__main__":
    main()
