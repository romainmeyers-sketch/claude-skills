"""Extract brand tokens from an existing PPTX file.

Analyzes slides to extract the color palette, fonts, spacing, and content area
boundaries used in the presentation. Output is a JSON dict of brand tokens
that can be used when adding new slides to match the existing style.

Usage:
    python extract_brand.py <pptx_file> [--output brand_tokens.json]

Examples:
    python extract_brand.py client_deck.pptx
    python extract_brand.py client_deck.pptx --output tokens.json
"""

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict


def extract_brand(pptx_path):
    """Extract brand tokens from a PPTX file.

    Returns a dict with colors, fonts, spacing, layouts, and slide dimensions.
    """
    try:
        from pptx import Presentation
        from pptx.util import Emu
    except ImportError:
        print("Error: python-pptx is not installed. Install with: pip install python-pptx",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(pptx_path):
        print(f"Error: {pptx_path} does not exist", file=sys.stderr)
        sys.exit(1)

    prs = Presentation(pptx_path)

    # Slide dimensions
    slide_w = prs.slide_width
    slide_h = prs.slide_height
    slide_w_in = round(Emu(slide_w).inches, 2)
    slide_h_in = round(Emu(slide_h).inches, 2)

    # Collectors
    fill_colors = Counter()       # RGB hex -> count
    text_colors = Counter()       # RGB hex -> count
    font_names = Counter()        # font name -> count
    font_sizes = defaultdict(list)  # font name -> [sizes]
    bold_font_sizes = []          # sizes used with bold
    regular_font_sizes = []       # sizes used without bold
    shape_positions = []          # (left, top, width, height) in inches

    # Per-shape analysis
    for slide in prs.slides:
        for shape in slide.shapes:
            # Position tracking
            if shape.left is not None and shape.top is not None:
                left_in = round(Emu(shape.left).inches, 2)
                top_in = round(Emu(shape.top).inches, 2)
                w_in = round(Emu(shape.width).inches, 2) if shape.width else 0
                h_in = round(Emu(shape.height).inches, 2) if shape.height else 0
                shape_positions.append((left_in, top_in, w_in, h_in))

            # Fill color extraction
            if shape.shape_type is not None:
                try:
                    fill = shape.fill
                    if fill.type is not None:
                        try:
                            rgb = fill.fore_color.rgb
                            if rgb:
                                fill_colors[str(rgb)] += 1
                        except (AttributeError, TypeError):
                            pass
                except Exception:
                    pass

            # Text analysis
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        font = run.font
                        # Font name
                        if font.name:
                            font_names[font.name] += 1
                        # Font size
                        if font.size:
                            size_pt = round(font.size.pt, 1)
                            if font.name:
                                font_sizes[font.name].append(size_pt)
                            if font.bold:
                                bold_font_sizes.append(size_pt)
                            else:
                                regular_font_sizes.append(size_pt)
                        # Font color
                        try:
                            if font.color and font.color.rgb:
                                text_colors[str(font.color.rgb)] += 1
                        except (AttributeError, TypeError):
                            pass

            # Table analysis
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        # Cell fill
                        try:
                            if cell.fill.type is not None:
                                rgb = cell.fill.fore_color.rgb
                                if rgb:
                                    fill_colors[str(rgb)] += 1
                        except (AttributeError, TypeError):
                            pass
                        # Cell text
                        for para in cell.text_frame.paragraphs:
                            for run in para.runs:
                                if run.font.name:
                                    font_names[run.font.name] += 1
                                try:
                                    if run.font.color and run.font.color.rgb:
                                        text_colors[str(run.font.color.rgb)] += 1
                                except (AttributeError, TypeError):
                                    pass

    # --- Analyze collected data ---

    # Color clustering: group similar colors (distance < 30 in RGB space)
    def hex_to_rgb(h):
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def rgb_distance(c1, c2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    def cluster_colors(color_counter, threshold=30):
        """Group similar colors, returning representative + total count."""
        items = [(hex_to_rgb(h), h, c) for h, c in color_counter.most_common()]
        clusters = []
        used = set()
        for i, (rgb1, hex1, count1) in enumerate(items):
            if i in used:
                continue
            cluster_count = count1
            for j, (rgb2, hex2, count2) in enumerate(items[i + 1:], i + 1):
                if j in used:
                    continue
                if rgb_distance(rgb1, rgb2) < threshold:
                    cluster_count += count2
                    used.add(j)
            clusters.append((hex1, cluster_count))
            used.add(i)
        return sorted(clusters, key=lambda x: -x[1])

    clustered_fills = cluster_colors(fill_colors)
    clustered_text = cluster_colors(text_colors)

    # Classify colors by role
    colors = {}
    if clustered_text:
        colors["body_text"] = f"#{clustered_text[0][0]}"
    if len(clustered_text) > 1:
        colors["secondary_text"] = f"#{clustered_text[1][0]}"
    if clustered_fills:
        colors["primary_fill"] = f"#{clustered_fills[0][0]}"
    if len(clustered_fills) > 1:
        colors["secondary_fill"] = f"#{clustered_fills[1][0]}"
    if len(clustered_fills) > 2:
        colors["accent"] = f"#{clustered_fills[2][0]}"

    # All unique colors for reference
    all_colors = {}
    for hex_val, count in clustered_fills[:10]:
        all_colors[f"#{hex_val}"] = f"fill ({count} occurrences)"
    for hex_val, count in clustered_text[:5]:
        key = f"#{hex_val}"
        if key in all_colors:
            all_colors[key] += f", text ({count} occurrences)"
        else:
            all_colors[key] = f"text ({count} occurrences)"

    # Font analysis
    fonts = {}
    if font_names:
        primary_font = font_names.most_common(1)[0][0]
        fonts["primary"] = primary_font

        # Title font: largest bold size
        if bold_font_sizes:
            title_size = max(Counter(bold_font_sizes).most_common(3), key=lambda x: x[0])[0]
            fonts["title"] = {"name": primary_font, "size_pt": title_size, "bold": True}

        # Body font: most common regular size
        if regular_font_sizes:
            body_size = Counter(regular_font_sizes).most_common(1)[0][0]
            fonts["body"] = {"name": primary_font, "size_pt": body_size, "bold": False}

        # Caption: smallest size
        all_sizes = bold_font_sizes + regular_font_sizes
        if all_sizes:
            caption_size = min(Counter(all_sizes).most_common(5), key=lambda x: x[0])[0]
            fonts["caption"] = {"name": primary_font, "size_pt": caption_size, "bold": False}

    if len(font_names) > 1:
        fonts["secondary"] = font_names.most_common(2)[1][0]

    # Content area estimation
    content_area = {}
    if shape_positions:
        # Filter out full-slide-width shapes (likely backgrounds)
        content_shapes = [
            (l, t, w, h) for l, t, w, h in shape_positions
            if w < slide_w_in * 0.95 and h < slide_h_in * 0.95
        ]
        if content_shapes:
            lefts = sorted([s[0] for s in content_shapes])
            tops = sorted([s[1] for s in content_shapes])
            rights = sorted([s[0] + s[2] for s in content_shapes])
            bottoms = sorted([s[1] + s[3] for s in content_shapes])

            # Use 10th and 90th percentiles for robustness
            p10 = max(0, len(lefts) // 10)
            p90 = min(len(lefts) - 1, len(lefts) * 9 // 10)

            content_area = {
                "left": round(lefts[p10], 2),
                "top": round(tops[p10], 2),
                "right": round(rights[p90], 2),
                "bottom": round(bottoms[p90], 2),
            }
            content_area["width"] = round(content_area["right"] - content_area["left"], 2)
            content_area["height"] = round(content_area["bottom"] - content_area["top"], 2)

    # Layout enumeration
    layouts_used = set()
    all_layouts = []
    for slide in prs.slides:
        layout_name = slide.slide_layout.name
        layouts_used.add(layout_name)

    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            entry = {"name": layout.name, "used": layout.name in layouts_used}
            all_layouts.append(entry)

    # Build output
    tokens = {
        "slide_dimensions": {
            "width_inches": slide_w_in,
            "height_inches": slide_h_in,
        },
        "content_area": content_area,
        "colors": colors,
        "all_colors": all_colors,
        "fonts": fonts,
        "all_fonts": dict(font_names.most_common(10)),
        "layouts": all_layouts,
        "slide_count": len(prs.slides),
    }

    return tokens


def main():
    parser = argparse.ArgumentParser(
        description="Extract brand tokens from a PPTX file"
    )
    parser.add_argument("pptx_file", help="PPTX file to analyze")
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file (default: print to stdout)",
    )
    args = parser.parse_args()

    tokens = extract_brand(args.pptx_file)

    output = json.dumps(tokens, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Brand tokens written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
