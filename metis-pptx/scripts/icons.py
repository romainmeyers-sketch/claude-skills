"""
Lucide icon helpers for the metis-pptx skill.

Provides programmatic, royalty-free graphical icons in Metis-branded
PowerPoint decks. Replaces the manual copy-from-Icon_Lib.pptx workflow
with a one-line call that handles download, brand recoloring, and
rasterization automatically.

Public API
----------
    lucide_icon(name, color=DARK_NAVY_HEX, size_px=256) -> Path
        Returns a local PNG path for the requested icon, downloading
        and rasterizing on first use, cached on disk thereafter.

    add_lucide_icon(slide, name, left, top, size, color=DARK_NAVY_HEX)
        Inserts a Lucide icon as a Picture shape on the given slide.

    lucide_icon_card(slide, icon, title, body, left, top, width,
                     accent_color=METIS_BLUE_HEX, icon_color=DARK_NAVY_HEX,
                     height=Inches(1.6))
        Metis component: icon + title + body in a clean card. Drop-in
        replacement for `icon_circle_text` when a real graphical icon
        communicates the concept better than a number-in-a-circle.

Design notes
------------
- Default library is Lucide (https://lucide.dev). Fallback hierarchy if
  a Lucide icon is missing for a concept: Heroicons -> Tabler ->
  Font Awesome Free. Never substitute emoji or hand-drawn shapes.
- All icons are downloaded as SVG, recolored by replacing
  `stroke="currentColor"` with the requested hex, and rasterized at
  256px (or higher for hero icons). Vector-quality at any on-slide size.
- Rendering priority: cairosvg (best quality) -> pycairo (ships native
  DLL on Windows/macOS, no system libcairo needed). pycairo parses SVG
  path data directly via a built-in SVG path interpreter.
- Cache lives under `~/.cache/metis-pptx/lucide/`. Safe to delete; will
  be re-populated on next use.
- macOS Apple Silicon note: brew cairo is not on Python's default search
  path. This module auto-sets `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`
  before importing cairosvg so callers don't have to.
"""
from __future__ import annotations

import hashlib
import os
import platform
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# macOS: point cairocffi at brew's libcairo before importing cairosvg.
# Safe no-op on Linux/Windows.
# ---------------------------------------------------------------------------
if platform.system() == "Darwin":
    _BREW_LIB = "/opt/homebrew/lib"
    if Path(_BREW_LIB).exists():
        current = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
        if _BREW_LIB not in current.split(":"):
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
                f"{_BREW_LIB}:{current}" if current else _BREW_LIB
            )

# ---------------------------------------------------------------------------
# SVG rasterizer: try cairosvg first, fall back to pycairo (ships its own DLL
# on Windows and macOS wheels, so no system libcairo needed).
# ---------------------------------------------------------------------------
_RENDERER = None  # "cairosvg" | "pycairo"

try:
    import cairosvg  # noqa: E402
    _RENDERER = "cairosvg"
except (OSError, ImportError):
    pass

if _RENDERER is None:
    try:
        import cairo as _pycairo  # pycairo  # noqa: E402
        import math as _math
        _RENDERER = "pycairo"
    except ImportError:
        raise ImportError(
            "No SVG rasterizer found. Install one of:\n"
            "  pip install cairosvg   (+ system libcairo)\n"
            "  pip install pycairo    (ships its own binary on Windows/macOS)\n"
        )

from pptx.util import Inches, Pt, Emu  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402

# ---------------------------------------------------------------------------
# Brand defaults (kept here so this module is self-contained; mirrors
# metis-brand.md). Callers can pass any hex string.
# ---------------------------------------------------------------------------
DARK_NAVY_HEX = "#20206E"
METIS_BLUE_HEX = "#256BA2"
MINT_HEX = "#3BDAC0"
DARK_GRAY_HEX = "#4A4A4A"
LIGHT_GRAY_HEX = "#F2F2F2"

LUCIDE_CDN = "https://cdn.jsdelivr.net/npm/lucide-static@latest/icons"
DEFAULT_STROKE_WIDTH = 2

CACHE_ROOT = Path(
    os.environ.get("METIS_ICON_CACHE")
    or Path.home() / ".cache" / "metis-pptx" / "lucide"
)
CACHE_ROOT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _normalize_color(color) -> str:
    """Accept '#RRGGBB', 'RRGGBB', or a python-pptx RGBColor; return '#RRGGBB'."""
    if isinstance(color, RGBColor):
        return "#" + str(color)
    s = str(color).strip()
    if not s.startswith("#"):
        s = "#" + s
    if len(s) != 7:
        raise ValueError(f"Expected hex color like '#20206E', got {color!r}")
    return s.upper()


def _cache_key(name: str, color_hex: str, size_px: int, stroke_w: float) -> Path:
    h = hashlib.md5(
        f"{name}|{color_hex}|{size_px}|{stroke_w}".encode("utf-8")
    ).hexdigest()[:12]
    return CACHE_ROOT / f"{name}__{color_hex.lstrip('#')}__{size_px}__{h}.png"


def _download_svg(name: str) -> str:
    """Fetch the raw Lucide SVG text, with a small on-disk cache of SVGs."""
    svg_cache = CACHE_ROOT / "_svg"
    svg_cache.mkdir(exist_ok=True)
    svg_path = svg_cache / f"{name}.svg"
    if svg_path.exists():
        return svg_path.read_text(encoding="utf-8")
    url = f"{LUCIDE_CDN}/{name}.svg"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(
                f"Lucide has no icon named {name!r}. Browse names at "
                f"https://lucide.dev/icons/ — use kebab-case (e.g. 'arrow-right')."
            ) from e
        raise
    svg_path.write_text(data, encoding="utf-8")
    return data


def _recolor(svg: str, color_hex: str, stroke_w: float) -> str:
    """Replace Lucide's currentColor with our color and normalize stroke width."""
    svg = svg.replace('stroke="currentColor"', f'stroke="{color_hex}"')
    svg = re.sub(r'stroke-width="[\d.]+"', f'stroke-width="{stroke_w}"', svg)
    return svg


# ---------------------------------------------------------------------------
# pycairo SVG path renderer (used when cairosvg is unavailable)
# ---------------------------------------------------------------------------
def _parse_svg_elements(svg_text: str):
    """Extract drawable elements from a Lucide SVG string."""
    paths = re.findall(r'd="([^"]+)"', svg_text)
    circles = re.findall(
        r'<circle[^>]*?cx="([^"]+)"[^>]*?cy="([^"]+)"[^>]*?r="([^"]+)"', svg_text)
    lines = re.findall(
        r'<line[^>]*?x1="([^"]+)"[^>]*?y1="([^"]+)"[^>]*?x2="([^"]+)"[^>]*?y2="([^"]+)"',
        svg_text)
    polylines = re.findall(r'<polyline[^>]*?points="([^"]+)"', svg_text)
    polygons = re.findall(r'<polygon[^>]*?points="([^"]+)"', svg_text)
    rects = re.findall(
        r'<rect[^>]*?x="([^"]*)"[^>]*?y="([^"]*)"[^>]*?width="([^"]*)"[^>]*?height="([^"]*)"'
        r'(?:[^>]*?rx="([^"]*)")?', svg_text)
    return paths, circles, lines, polylines, polygons, rects


def _draw_svg_path(ctx, d: str):
    """Parse an SVG path d attribute and draw it onto a pycairo context."""
    tokens = re.findall(
        r'[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d)
    i = 0
    cx, cy = 0.0, 0.0
    sx, sy = 0.0, 0.0
    last_cmd = ''
    prev_cx2, prev_cy2 = 0.0, 0.0

    def nxt():
        nonlocal i
        while i < len(tokens) and tokens[i].isalpha():
            i += 1
        if i < len(tokens):
            v = float(tokens[i]); i += 1; return v
        return 0.0

    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t; i += 1
        else:
            cmd = last_cmd

        if cmd == 'M':
            cx, cy = nxt(), nxt()
            ctx.move_to(cx, cy); sx, sy = cx, cy; last_cmd = 'L'
        elif cmd == 'm':
            cx += nxt(); cy += nxt()
            ctx.move_to(cx, cy); sx, sy = cx, cy; last_cmd = 'l'
        elif cmd == 'L':
            cx, cy = nxt(), nxt(); ctx.line_to(cx, cy); last_cmd = 'L'
        elif cmd == 'l':
            cx += nxt(); cy += nxt(); ctx.line_to(cx, cy); last_cmd = 'l'
        elif cmd == 'H':
            cx = nxt(); ctx.line_to(cx, cy); last_cmd = 'H'
        elif cmd == 'h':
            cx += nxt(); ctx.line_to(cx, cy); last_cmd = 'h'
        elif cmd == 'V':
            cy = nxt(); ctx.line_to(cx, cy); last_cmd = 'V'
        elif cmd == 'v':
            cy += nxt(); ctx.line_to(cx, cy); last_cmd = 'v'
        elif cmd == 'C':
            x1, y1 = nxt(), nxt(); x2, y2 = nxt(), nxt(); cx, cy = nxt(), nxt()
            ctx.curve_to(x1, y1, x2, y2, cx, cy)
            prev_cx2, prev_cy2 = x2, y2; last_cmd = 'C'
        elif cmd == 'c':
            x1 = cx + nxt(); y1 = cy + nxt()
            x2 = cx + nxt(); y2 = cy + nxt()
            dx, dy = nxt(), nxt()
            ctx.curve_to(x1, y1, x2, y2, cx + dx, cy + dy)
            prev_cx2, prev_cy2 = x2, y2; cx += dx; cy += dy; last_cmd = 'c'
        elif cmd == 'S':
            x1 = 2*cx - prev_cx2; y1 = 2*cy - prev_cy2
            x2, y2 = nxt(), nxt(); cx, cy = nxt(), nxt()
            ctx.curve_to(x1, y1, x2, y2, cx, cy)
            prev_cx2, prev_cy2 = x2, y2; last_cmd = 'S'
        elif cmd == 's':
            x1 = 2*cx - prev_cx2; y1 = 2*cy - prev_cy2
            x2 = cx + nxt(); y2 = cy + nxt(); dx, dy = nxt(), nxt()
            ctx.curve_to(x1, y1, x2, y2, cx + dx, cy + dy)
            prev_cx2, prev_cy2 = x2, y2; cx += dx; cy += dy; last_cmd = 's'
        elif cmd == 'Q':
            qx, qy = nxt(), nxt(); ex, ey = nxt(), nxt()
            c1x = cx + 2/3*(qx - cx); c1y = cy + 2/3*(qy - cy)
            c2x = ex + 2/3*(qx - ex); c2y = ey + 2/3*(qy - ey)
            ctx.curve_to(c1x, c1y, c2x, c2y, ex, ey)
            cx, cy = ex, ey; last_cmd = 'Q'
        elif cmd == 'q':
            qx = cx + nxt(); qy = cy + nxt(); dx, dy = nxt(), nxt()
            ex, ey = cx + dx, cy + dy
            c1x = cx + 2/3*(qx - cx); c1y = cy + 2/3*(qy - cy)
            c2x = ex + 2/3*(qx - ex); c2y = ey + 2/3*(qy - ey)
            ctx.curve_to(c1x, c1y, c2x, c2y, ex, ey)
            cx, cy = ex, ey; last_cmd = 'q'
        elif cmd in ('A', 'a'):
            _rx = nxt(); _ry = nxt(); _xrot = nxt()
            _large = int(nxt()); _sweep = int(nxt())
            if cmd == 'A':
                ex, ey = nxt(), nxt()
            else:
                ex = cx + nxt(); ey = cy + nxt()
            ctx.line_to(ex, ey); cx, cy = ex, ey; last_cmd = cmd
        elif cmd in ('Z', 'z'):
            ctx.close_path(); cx, cy = sx, sy; last_cmd = cmd
        else:
            i += 1


def _rasterize_pycairo(svg_text: str, out_path: Path, size_px: int,
                       color_hex: str, stroke_w: float):
    """Render a Lucide SVG to PNG using pycairo's native drawing API."""
    r, g, b = [int(color_hex.lstrip('#')[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

    surface = _pycairo.ImageSurface(_pycairo.FORMAT_ARGB32, size_px, size_px)
    ctx = _pycairo.Context(surface)

    scale = size_px / 24.0
    ctx.scale(scale, scale)
    ctx.set_line_width(stroke_w)
    ctx.set_line_cap(_pycairo.LINE_CAP_ROUND)
    ctx.set_line_join(_pycairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(r, g, b, 1.0)

    paths, circles, lines, polylines, polygons, rects = _parse_svg_elements(svg_text)

    for d in paths:
        ctx.new_path()
        _draw_svg_path(ctx, d)
        ctx.stroke()

    for cx_s, cy_s, r_s in circles:
        ctx.new_path()
        ctx.arc(float(cx_s), float(cy_s), float(r_s), 0, 2 * _math.pi)
        ctx.stroke()

    for x1, y1, x2, y2 in lines:
        ctx.new_path()
        ctx.move_to(float(x1), float(y1))
        ctx.line_to(float(x2), float(y2))
        ctx.stroke()

    for pts_str in polylines:
        pts = re.findall(r'[-+]?\d+\.?\d*', pts_str)
        if len(pts) >= 4:
            ctx.new_path()
            ctx.move_to(float(pts[0]), float(pts[1]))
            for j in range(2, len(pts), 2):
                ctx.line_to(float(pts[j]), float(pts[j+1]))
            ctx.stroke()

    for pts_str in polygons:
        pts = re.findall(r'[-+]?\d+\.?\d*', pts_str)
        if len(pts) >= 4:
            ctx.new_path()
            ctx.move_to(float(pts[0]), float(pts[1]))
            for j in range(2, len(pts), 2):
                ctx.line_to(float(pts[j]), float(pts[j+1]))
            ctx.close_path()
            ctx.stroke()

    for x, y, w, h, *rx in rects:
        fx, fy, fw, fh = float(x), float(y), float(w), float(h)
        ctx.new_path()
        ctx.rectangle(fx, fy, fw, fh)
        ctx.stroke()

    surface.write_to_png(str(out_path))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def lucide_icon(
    name: str,
    color=DARK_NAVY_HEX,
    size_px: int = 256,
    stroke_width: float = DEFAULT_STROKE_WIDTH,
) -> Path:
    """Download, recolor, and rasterize a Lucide icon to PNG. Cached.

    Parameters
    ----------
    name : str
        Lucide icon name in kebab-case, e.g. 'arrow-right', 'shield-check'.
        See https://lucide.dev/icons/ for the catalog.
    color : str | RGBColor
        Hex color for the icon stroke. Defaults to Metis Dark Navy.
    size_px : int
        Raster output size in pixels (square). Use 256 for content-slide
        icons, 512+ for hero/title icons. Vector quality at any size.
    stroke_width : float
        SVG stroke width override (Lucide default is 2). Increase to ~2.5
        for stronger visual weight; decrease for lighter feel.

    Returns
    -------
    Path
        Absolute filesystem path to the cached PNG.
    """
    color_hex = _normalize_color(color)
    out = _cache_key(name, color_hex, size_px, stroke_width)
    if out.exists():
        return out
    svg = _recolor(_download_svg(name), color_hex, stroke_width)
    if _RENDERER == "cairosvg":
        cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            write_to=str(out),
            output_width=size_px,
            output_height=size_px,
        )
    else:
        _rasterize_pycairo(svg, out, size_px, color_hex, stroke_width)
    return out


def add_lucide_icon(
    slide,
    name: str,
    left,
    top,
    size,
    color=DARK_NAVY_HEX,
    stroke_width: float = DEFAULT_STROKE_WIDTH,
):
    """Insert a Lucide icon as a Picture shape on the slide.

    Parameters
    ----------
    slide : pptx.slide.Slide
        Target slide.
    name : str
        Lucide icon name (kebab-case).
    left, top : Emu
        Position of the icon's top-left corner (use Inches()).
    size : Emu
        Width AND height of the icon (icons are square). Use Inches().
    color : str | RGBColor
        Stroke color.

    Returns
    -------
    pptx.shapes.picture.Picture
    """
    # Render at ~2x the on-slide pixel size for crispness
    on_slide_inches = float(size) / 914400.0
    target_px = max(256, int(on_slide_inches * 200))
    png_path = lucide_icon(name, color=color, size_px=target_px,
                           stroke_width=stroke_width)
    return slide.shapes.add_picture(str(png_path), left, top, size, size)


def lucide_icon_card(
    slide,
    icon: str,
    title: str,
    body: str,
    left,
    top,
    width,
    *,
    height=Inches(1.6),
    icon_color=DARK_NAVY_HEX,
    title_color=DARK_NAVY_HEX,
    body_color=DARK_GRAY_HEX,
    card_fill=LIGHT_GRAY_HEX,
    icon_size=Inches(0.55),
    font_name: str = "Calibri",
):
    """Metis component: real graphical icon + title + body in a clean card.

    Drop-in replacement for `icon_circle_text` when a Lucide glyph
    communicates the concept better than a number/letter in a circle.

    Layout: icon top-left, title to the right of the icon, body below
    spanning the full card width. Matches the visual weight of other
    Metis cards in patterns.md.

    Parameters
    ----------
    slide : pptx.slide.Slide
    icon : str
        Lucide icon name in kebab-case (e.g. 'shield-check', 'users').
    title : str
        Short header text (2-4 words).
    body : str
        One-sentence description.
    left, top, width : Emu
        Card position and width (use Inches()).
    height : Emu
        Card height. Defaults to 1.6" — increase for longer body text.
    icon_color, title_color, body_color, card_fill : str
        Hex colors. Defaults match Metis brand.
    icon_size : Emu
        Icon glyph size (square). Defaults to 0.55".
    font_name : str
        Defaults to 'Calibri' (Metis body font).

    Returns
    -------
    list[Shape]
        [card, icon, title_textbox, body_textbox] for further tweaking.
    """
    # Card background
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor.from_string(
        _normalize_color(card_fill).lstrip("#")
    )
    card.line.fill.background()
    card.shadow.inherit = False

    pad = Inches(0.20)
    # Icon (top-left of card)
    icon_shape = add_lucide_icon(
        slide, icon,
        left + pad, top + pad,
        icon_size,
        color=icon_color,
    )

    # Title (right of icon, vertically centered against icon)
    title_left = left + pad + icon_size + Inches(0.15)
    title_top = top + pad
    title_w = width - pad - icon_size - Inches(0.15) - pad
    title_tb = slide.shapes.add_textbox(title_left, title_top,
                                         title_w, icon_size)
    tf = title_tb.text_frame
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = title
    r.font.name = font_name
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor.from_string(
        _normalize_color(title_color).lstrip("#")
    )

    # Body (below icon + title row)
    body_top = top + pad + icon_size + Inches(0.10)
    body_h = height - (body_top - top) - pad
    body_tb = slide.shapes.add_textbox(left + pad, body_top,
                                        width - 2 * pad, body_h)
    btf = body_tb.text_frame
    btf.margin_left = btf.margin_right = Emu(0)
    btf.margin_top = btf.margin_bottom = Emu(0)
    btf.word_wrap = True
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.LEFT
    br = bp.add_run()
    br.text = body
    br.font.name = font_name
    br.font.size = Pt(11)
    br.font.color.rgb = RGBColor.from_string(
        _normalize_color(body_color).lstrip("#")
    )

    return [card, icon_shape, title_tb, body_tb]


# ---------------------------------------------------------------------------
# Auto-icon selection from concept map
# ---------------------------------------------------------------------------
_ICON_MAP = None
_ICON_MAP_PATH = Path(__file__).parent.parent / "references" / "icon-map.json"


def _load_icon_map() -> dict:
    """Load and flatten the concept-to-icon map into a single keyword->icon dict."""
    global _ICON_MAP
    if _ICON_MAP is not None:
        return _ICON_MAP
    import json
    if not _ICON_MAP_PATH.exists():
        _ICON_MAP = {}
        return _ICON_MAP
    with open(_ICON_MAP_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    flat = {}
    for category, mappings in raw.items():
        if category.startswith("_"):
            continue
        if isinstance(mappings, dict):
            for keyword, icon_name in mappings.items():
                flat[keyword.lower()] = icon_name
    _ICON_MAP = flat
    return _ICON_MAP


def suggest_icon(title: str, fallback: str = "circle-dot") -> str:
    """Suggest a Lucide icon name based on a card/item title.

    Scans the title against the concept-to-icon map (references/icon-map.json).
    Returns the best match or the fallback icon.

    Parameters
    ----------
    title : str
        Card title, column header, or short description.
    fallback : str
        Icon to return if no concept matches. Defaults to 'circle-dot'.

    Returns
    -------
    str
        Lucide icon name in kebab-case.
    """
    icon_map = _load_icon_map()
    title_lower = title.lower()
    best_match = None
    best_len = 0
    for keyword, icon_name in icon_map.items():
        if keyword in title_lower and len(keyword) > best_len:
            best_match = icon_name
            best_len = len(keyword)
    return best_match or fallback


# ---------------------------------------------------------------------------
# CLI: render a single icon for inspection / debug
# ---------------------------------------------------------------------------
def _cli():
    import argparse
    ap = argparse.ArgumentParser(
        description="Render a single Lucide icon to PNG for inspection."
    )
    ap.add_argument("name", help="Lucide icon name (kebab-case)")
    ap.add_argument("--color", default=DARK_NAVY_HEX, help="hex color (default: Metis navy)")
    ap.add_argument("--size", type=int, default=512, help="output px (default: 512)")
    ap.add_argument("--out", help="output path (default: ./<name>.png)")
    args = ap.parse_args()
    path = lucide_icon(args.name, color=args.color, size_px=args.size)
    if args.out:
        import shutil
        shutil.copyfile(path, args.out)
        print(args.out)
    else:
        target = Path.cwd() / f"{args.name}.png"
        import shutil
        shutil.copyfile(path, target)
        print(str(target))


if __name__ == "__main__":
    _cli()
