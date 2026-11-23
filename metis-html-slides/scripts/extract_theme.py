"""Extract brand colors/fonts from a PPTX file and generate a CSS theme.

Wraps the metis-pptx extract_brand.py logic and outputs CSS custom properties
compatible with the metis-html-slides component library.

Usage:
    python extract_theme.py <pptx_file> [--output client-theme.css]

Examples:
    python extract_theme.py client_deck.pptx
    python extract_theme.py client_deck.pptx --output parker-theme.css
"""

import argparse
import json
import os
import sys
from pathlib import Path


def find_extract_brand():
    """Locate the metis-pptx extract_brand.py script."""
    candidates = [
        Path(__file__).parent.parent.parent / "metis-pptx" / "scripts" / "extract_brand.py",
        Path.home() / ".metis/skills/.tessl/tiles/metis-strategy/metis-pptx/scripts/extract_brand.py",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def extract_brand_tokens(pptx_path):
    """Extract brand tokens from PPTX. Uses metis-pptx's extract_brand if available."""
    brand_script = find_extract_brand()

    if brand_script:
        # Use the metis-pptx extractor
        import subprocess
        python_exe = sys.executable
        result = subprocess.run(
            [python_exe, str(brand_script), pptx_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return json.loads(result.stdout)

    # Fallback: basic extraction using python-pptx directly
    try:
        from pptx import Presentation
        from pptx.util import Emu
    except ImportError:
        print("Error: python-pptx not installed", file=sys.stderr)
        sys.exit(1)

    prs = Presentation(pptx_path)
    # Minimal extraction for theme generation
    return {
        "slide_dimensions": {
            "width_inches": round(Emu(prs.slide_width).inches, 2),
            "height_inches": round(Emu(prs.slide_height).inches, 2),
        },
        "colors": {},
        "fonts": {"primary": "Calibri"},
    }


def tokens_to_css(tokens):
    """Convert brand tokens JSON to CSS custom properties."""
    colors = tokens.get("colors", {})
    fonts = tokens.get("fonts", {})
    all_colors = tokens.get("all_colors", {})

    # Map extracted roles to CSS variable names
    color_map = {
        "primary_fill": "--color-primary",
        "body_text": "--color-text",
        "secondary_fill": "--color-secondary",
        "accent": "--color-accent",
        "secondary_text": "--color-text-muted",
    }

    lines = [
        "/* ═══════════════════════════════════════════════════════════",
        "   Client Brand Theme (auto-extracted from PPTX)",
        "   ═══════════════════════════════════════════════════════════ */",
        "",
        ":root {",
    ]

    # Colors
    for role, var_name in color_map.items():
        if role in colors:
            lines.append(f"  {var_name}: {colors[role]};")

    # Defaults for any missing colors
    defaults = {
        "--color-primary": "#333333",
        "--color-secondary": "#666666",
        "--color-accent": "#0078D4",
        "--color-text": "#333333",
        "--color-text-muted": "#999999",
        "--color-white": "#FFFFFF",
        "--color-bg-light": "#F5F5F5",
        "--color-tier-light": "#E8F0FE",
        "--color-tier-med": "#C5D9F0",
        "--color-tier-dark": "#8FB8DE",
    }
    existing = {line.split(":")[0].strip() for line in lines if line.strip().startswith("--")}
    for var_name, default in defaults.items():
        if var_name not in existing:
            lines.append(f"  {var_name}: {default};  /* default — not found in PPTX */")

    # Fonts
    primary_font = fonts.get("primary", "Calibri")
    title_info = fonts.get("title", {})
    body_info = fonts.get("body", {})

    lines.append("")
    lines.append(f"  --font-family: '{primary_font}', 'Segoe UI', sans-serif;")

    if title_info:
        size_pt = title_info.get("size_pt", 28)
        lines.append(f"  --font-size-title: {size_pt / 12:.1f}rem;")

    if body_info:
        size_pt = body_info.get("size_pt", 14)
        lines.append(f"  --font-size-body: {size_pt / 12:.1f}rem;")

    lines.append(f"  --font-size-subtitle: 1.1rem;")
    lines.append(f"  --font-size-small: 0.85rem;")
    lines.append(f"  --font-size-caption: 0.75rem;")

    # Footer
    lines.append("")
    lines.append('  --footer-text: "Confidential";')
    lines.append("  --footer-border-color: var(--color-accent);")

    lines.append("}")
    lines.append("")

    # Append color reference as comments
    if all_colors:
        lines.append("/* ── All colors found in PPTX (reference) ──")
        for color, desc in list(all_colors.items())[:10]:
            lines.append(f"   {color}: {desc}")
        lines.append("*/")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract a CSS theme from a PPTX file"
    )
    parser.add_argument("pptx_file", help="PPTX file to extract brand from")
    parser.add_argument(
        "--output", "-o",
        help="Output CSS file (default: print to stdout)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.pptx_file):
        print(f"Error: {args.pptx_file} not found", file=sys.stderr)
        sys.exit(1)

    tokens = extract_brand_tokens(args.pptx_file)
    css = tokens_to_css(tokens)

    if args.output:
        Path(args.output).write_text(css, encoding="utf-8")
        print(f"Theme CSS written to {args.output}")
    else:
        print(css)


if __name__ == "__main__":
    main()
