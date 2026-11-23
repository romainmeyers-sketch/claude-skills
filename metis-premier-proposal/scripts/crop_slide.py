"""
crop_slide.py — Crop exported PPTX slide images before embedding in proposals.

Removes slide titles, subtitles, and footers so the embedded image shows
only the diagram/visual content. Always verify the output visually.

Usage:
  python crop_slide.py --input slide-10.png --output slide-10-cropped.png
  python crop_slide.py --input slide-10.png --top 120 --bottom 45
  python crop_slide.py --batch slides/ --top 120 --bottom 45 --suffix -cropped

The default --top 120 --bottom 45 works for standard Metis 16:9 slides
exported at 1920×1080. If titles are larger or the layout differs, adjust.

After cropping, open the output PNG and verify:
  - Top edge: clean content, no title text bleeding in
  - Bottom edge: clean content, no Metis logo or footer text
"""
import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    print('ERROR: Pillow not installed. Run: pip install Pillow')
    sys.exit(1)


def crop_slide(input_path, output_path, top_px=120, bottom_px=45, left_px=0, right_px=0):
    img = Image.open(input_path)
    w, h = img.size
    crop_box = (
        left_px,
        top_px,
        w - right_px,
        h - bottom_px,
    )
    cropped = img.crop(crop_box)
    cropped.save(output_path)
    cw, ch = cropped.size
    print(f'  {os.path.basename(input_path)} ({w}×{h}) → {os.path.basename(output_path)} ({cw}×{ch})')
    print(f'  Cropped: top={top_px}px, bottom={bottom_px}px, left={left_px}px, right={right_px}px')
    return output_path


def batch_crop(input_dir, top_px, bottom_px, suffix='-cropped'):
    pngs = sorted(f for f in os.listdir(input_dir) if f.endswith('.png') and suffix not in f)
    if not pngs:
        print(f'No PNG files found in {input_dir}')
        return
    for fname in pngs:
        base, ext = os.path.splitext(fname)
        out_name = base + suffix + ext
        crop_slide(
            os.path.join(input_dir, fname),
            os.path.join(input_dir, out_name),
            top_px=top_px,
            bottom_px=bottom_px,
        )
    print(f'\nBatch complete: {len(pngs)} slide(s) cropped in {input_dir}/')


def main():
    parser = argparse.ArgumentParser(description='Crop PPTX slide images for proposal embedding.')
    parser.add_argument('--input', help='Single input PNG file')
    parser.add_argument('--output', help='Output path for single crop')
    parser.add_argument('--batch', help='Directory for batch crop (all PNGs without suffix)')
    parser.add_argument('--top', type=int, default=120, help='Pixels to remove from top (default: 120)')
    parser.add_argument('--bottom', type=int, default=45, help='Pixels to remove from bottom (default: 45)')
    parser.add_argument('--left', type=int, default=0, help='Pixels to remove from left (default: 0)')
    parser.add_argument('--right', type=int, default=0, help='Pixels to remove from right (default: 0)')
    parser.add_argument('--suffix', default='-cropped', help='Suffix for batch output files (default: -cropped)')
    args = parser.parse_args()

    if args.batch:
        if not os.path.isdir(args.batch):
            print(f'ERROR: Directory not found: {args.batch}')
            sys.exit(1)
        batch_crop(args.batch, args.top, args.bottom, args.suffix)

    elif args.input:
        if not os.path.exists(args.input):
            print(f'ERROR: File not found: {args.input}')
            sys.exit(1)
        out = args.output or args.input.replace('.png', f'{args.suffix}.png')
        crop_slide(args.input, out, args.top, args.bottom, args.left, args.right)
        print(f'\nVerify the output visually before embedding in the proposal.')

    else:
        parser.print_help()
        print('\nExamples:')
        print('  python crop_slide.py --input slide-10.png --top 120 --bottom 45')
        print('  python crop_slide.py --batch ./slides/ --top 140 --bottom 60')


if __name__ == '__main__':
    main()
