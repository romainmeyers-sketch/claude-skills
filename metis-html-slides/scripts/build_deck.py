"""Assemble a self-contained HTML presentation from slide content.

Takes an HTML file containing slide divs and packages it with inlined CSS,
auto-generated sidebar navigation, and embedded brand assets into a single
portable HTML file.

Usage:
    python build_deck.py <slides_html> <output_html> [--theme <theme.css>] [--title <title>] [--subtitle <subtitle>]

Examples:
    python build_deck.py slides.html presentation.html
    python build_deck.py slides.html deck.html --theme client-theme.css --title "Q1 Review"
    python build_deck.py slides.html deck.html --title "Strategy Update" --subtitle "Prepared for Acme Corp"
"""

import argparse
import base64
import os
import re
import sys
from pathlib import Path
from html import escape


def find_skill_dir():
    """Locate the skill's templates directory."""
    candidates = [
        Path(__file__).parent.parent / "templates",
        Path.home() / ".metis/skills/.tessl/tiles/metis-strategy/metis-html-slides/templates",
        Path.home() / ".metis/skills/.agents/skills/tessl__metis-html-slides/templates",
    ]
    for d in candidates:
        if d.is_dir() and (d / "base.html").exists():
            return d
    raise FileNotFoundError("Cannot find metis-html-slides templates directory")


def find_logo():
    """Locate the Metis Strategy logo and return base64-encoded img tag."""
    logo_candidates = [
        Path("G:/Shared drives/Knowledge Management/New Brand Assets/Metis Strategy Logo/Metis Strategy Black-Mint RGB Logo.png"),
        Path.home() / ".metis/assets/Metis Strategy Black-Mint RGB Logo.png",
    ]
    for logo_path in logo_candidates:
        if logo_path.exists():
            data = base64.b64encode(logo_path.read_bytes()).decode("ascii")
            return f'<img class="sidebar-logo" src="data:image/png;base64,{data}" alt="Metis Strategy">'

    # Fallback: text-based logo
    return '<div class="sidebar-logo" style="font-size:0.85rem;font-weight:700;color:#20216f;letter-spacing:0.12em;text-transform:uppercase;">Metis Strategy</div>'


def inline_images(html_content, base_dir):
    """Replace image src paths with base64 data URIs for portability."""
    def replace_src(match):
        prefix = match.group(1)
        src = match.group(2)
        suffix = match.group(3)

        if src.startswith("data:") or src.startswith("http"):
            return match.group(0)

        # Try relative to base_dir first, then absolute
        img_path = Path(base_dir) / src
        if not img_path.exists():
            img_path = Path(src)
        if not img_path.exists():
            return match.group(0)

        ext = img_path.suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".webp": "image/webp",
        }
        mime = mime_types.get(ext, "application/octet-stream")

        data = base64.b64encode(img_path.read_bytes()).decode("ascii")
        return f'{prefix}data:{mime};base64,{data}{suffix}'

    html_content = re.sub(
        r'(src=["\'])([^"\']+)(["\'])',
        replace_src,
        html_content,
    )
    return html_content


def parse_sections(slides_content):
    """Parse data-section-num, data-section-title, and data-sub-label from slide divs.

    Returns a list of section dicts:
        [{ num: "1", title: "Introduction", slides: [
            { index: 0, sub_label: "" },
            { index: 1, sub_label: "Market Analysis" },
        ]}]
    """
    sections = []
    section_map = {}  # num -> section dict

    # Find all slide divs with their data attributes
    pattern = re.compile(
        r'<div\s+class="slide[^"]*"'
        r'(?:\s+data-section-num="([^"]*)")?'
        r'(?:\s+data-section-title="([^"]*)")?'
        r'(?:\s+data-sub-label="([^"]*)")?',
        re.IGNORECASE,
    )

    # We need a more robust approach since attributes can be in any order
    slide_pattern = re.compile(r'<div\s+class="slide[^"]*"([^>]*)>', re.IGNORECASE)
    attr_pattern = re.compile(r'data-(section-num|section-title|sub-label)="([^"]*)"')

    slide_index = 0
    for match in slide_pattern.finditer(slides_content):
        attrs_str = match.group(1)
        attrs = {}
        for attr_match in attr_pattern.finditer(attrs_str):
            attrs[attr_match.group(1)] = attr_match.group(2)

        sec_num = attrs.get("section-num", "")
        sec_title = attrs.get("section-title", "")
        sub_label = attrs.get("sub-label", "")

        if sec_num:
            if sec_num not in section_map:
                section = {
                    "num": sec_num,
                    "title": sec_title,
                    "slides": [],
                }
                section_map[sec_num] = section
                sections.append(section)

            section_map[sec_num]["slides"].append({
                "index": slide_index,
                "sub_label": sub_label,
            })

        slide_index += 1

    return sections


def build_sidebar_nav(sections):
    """Generate sidebar navigation HTML from parsed sections."""
    lines = []

    for i, sec in enumerate(sections):
        num_display = f"{int(sec['num']):02d}" if sec['num'].isdigit() else sec['num']
        first_slide_idx = sec['slides'][0]['index'] if sec['slides'] else 0
        active_class = ' active' if i == 0 else ''

        lines.append(f'        <div class="nav-section{active_class}" data-section="{escape(sec["num"])}">')
        lines.append(f'          <div class="nav-section-header" data-slide="{first_slide_idx}">')
        lines.append(f'            <span class="nav-number">{escape(num_display)}</span>')
        lines.append(f'            <span class="nav-dot"></span>')
        lines.append(f'            <span class="nav-label">{escape(sec["title"])}</span>')
        lines.append(f'          </div>')

        # Add sub-items if there are multiple slides in this section with sub-labels
        has_sub_labels = any(s['sub_label'] for s in sec['slides'])
        if len(sec['slides']) > 1 and has_sub_labels:
            lines.append(f'          <div class="nav-sub-items">')
            for slide_info in sec['slides']:
                if slide_info['sub_label']:
                    lines.append(
                        f'            <div class="nav-sub-item" '
                        f'data-slide-index="{slide_info["index"]}">'
                        f'{escape(slide_info["sub_label"])}</div>'
                    )
            lines.append(f'          </div>')

        lines.append(f'        </div>')

    return "\n".join(lines)


def build(slides_html, output_path, theme_css=None, title="Presentation", subtitle=""):
    """Assemble a self-contained HTML presentation.

    Args:
        slides_html: Path to HTML file containing slide <div> elements,
                     or a string of HTML content.
        output_path: Path for the output HTML file.
        theme_css: Optional path to a custom theme CSS file.
                   Defaults to metis-theme.css.
        title: Presentation title for the HTML <title> tag.
        subtitle: Deck subtitle shown in the sidebar header.
    """
    templates_dir = find_skill_dir()

    # Read template files
    base_template = (templates_dir / "base.html").read_text(encoding="utf-8")
    components_css = (templates_dir / "components.css").read_text(encoding="utf-8")

    # Read theme CSS
    if theme_css and Path(theme_css).exists():
        theme = Path(theme_css).read_text(encoding="utf-8")
    else:
        theme = (templates_dir / "metis-theme.css").read_text(encoding="utf-8")

    # Read slides content
    slides_path = Path(slides_html)
    if slides_path.exists():
        slides_content = slides_path.read_text(encoding="utf-8")
        base_dir = slides_path.parent
    else:
        slides_content = slides_html
        base_dir = Path(".")

    # Inline any local images
    slides_content = inline_images(slides_content, base_dir)

    # Parse sections and build sidebar nav
    sections = parse_sections(slides_content)
    sidebar_nav = build_sidebar_nav(sections)

    # Get logo
    logo_html = find_logo()

    # Assemble
    html = base_template
    html = html.replace("{{TITLE}}", escape(title))
    html = html.replace("{{SUBTITLE}}", escape(subtitle or title))
    html = html.replace("{{THEME_CSS}}", theme)
    html = html.replace("{{COMPONENTS_CSS}}", components_css)
    html = html.replace("{{SLIDES}}", slides_content)
    html = html.replace("{{SIDEBAR_NAV}}", sidebar_nav)
    html = html.replace("{{LOGO}}", logo_html)

    # Write output
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")

    # Stats
    size_kb = output.stat().st_size / 1024
    slide_count = len(re.findall(r'class="slide[\s"]', slides_content))
    section_count = len(sections)
    print(f"Built: {output_path} ({size_kb:.0f} KB, {slide_count} slides, {section_count} sections)")

    return str(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Assemble a self-contained HTML presentation"
    )
    parser.add_argument("slides_html", help="HTML file containing slide content")
    parser.add_argument("output_html", help="Output HTML file path")
    parser.add_argument(
        "--theme", help="Custom theme CSS file (default: metis-theme.css)"
    )
    parser.add_argument(
        "--title", default="Presentation", help="Presentation title"
    )
    parser.add_argument(
        "--subtitle", default="", help="Deck subtitle for sidebar"
    )
    args = parser.parse_args()

    build(
        args.slides_html,
        args.output_html,
        theme_css=args.theme,
        title=args.title,
        subtitle=args.subtitle,
    )
