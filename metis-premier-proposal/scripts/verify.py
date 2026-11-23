"""
verify.py — QA verification for Metis premier proposal PDFs.

Usage:
  python verify.py --pdf output.pdf --mode overlaps
  python verify.py --pdf output.pdf --mode fill
  python verify.py --pdf output.pdf --mode render --out verify/
  python verify.py --pdf output.pdf --mode content
  python verify.py --pdf output.pdf --mode all --out verify/
"""
import argparse
import os
import sys

try:
    import fitz
except ImportError:
    print('ERROR: PyMuPDF not installed. Run: pip install pymupdf')
    sys.exit(1)


# ---------------------------------------------------------------------------
# Overlap detection
# ---------------------------------------------------------------------------
def rects_overlap(r1, r2, threshold=3):
    x_overlap = min(r1[2], r2[2]) - max(r1[0], r2[0])
    y_overlap = min(r1[3], r2[3]) - max(r1[1], r2[1])
    return x_overlap > threshold and y_overlap > threshold


FOOTER_SKIP = ['Proprietary', 'Confidential', '© 2026', 'Page ']


def check_overlaps(pdf_path):
    doc = fitz.open(pdf_path)
    total_overlaps = 0
    for i, page in enumerate(doc):
        spans = []
        for b in page.get_text('dict')['blocks']:
            if 'lines' not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    t = span['text'].strip()
                    if len(t) < 2:
                        continue
                    if any(skip in t for skip in FOOTER_SKIP):
                        continue
                    spans.append((span['bbox'], t))

        overlaps = 0
        for j, (b1, t1) in enumerate(spans):
            for k, (b2, t2) in enumerate(spans):
                if j >= k:
                    continue
                if t1.strip() == t2.strip():
                    continue
                if rects_overlap(b1, b2):
                    overlaps += 1
                    print(f'  Page {i+1} OVERLAP: "{t1[:40]}" × "{t2[:40]}"')
        if overlaps:
            print(f'Page {i+1}: {overlaps} overlap(s)')
        total_overlaps += overlaps
    doc.close()
    if total_overlaps == 0:
        print('PASS: No overlaps detected.')
    else:
        print(f'FAIL: {total_overlaps} overlap(s) across all pages.')
    return total_overlaps == 0


# ---------------------------------------------------------------------------
# Content fill check (bottom text > 85% of page height)
# ---------------------------------------------------------------------------
def check_fill(pdf_path, skip_pages=None):
    skip_pages = skip_pages or []
    doc = fitz.open(pdf_path)
    page_h = doc[0].rect.height
    threshold = page_h * 0.85
    failures = []
    for i, page in enumerate(doc):
        if i in skip_pages:
            continue
        max_y = 0
        for b in page.get_text('dict')['blocks']:
            if 'lines' not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    y = span['origin'][1]
                    if y > max_y:
                        max_y = y
        pct = max_y / page_h * 100
        status = 'PASS' if max_y >= threshold else 'WARN'
        print(f'Page {i+1}: bottom text at {max_y:.0f}pt ({pct:.0f}%) [{status}]')
        if max_y < threshold:
            failures.append(i + 1)
    doc.close()
    if failures:
        print(f'WARN: Pages {failures} may have excess whitespace (text below 85% fill).')
    else:
        print('PASS: All pages meet fill threshold.')
    return len(failures) == 0


# ---------------------------------------------------------------------------
# Render to PNG for visual review
# ---------------------------------------------------------------------------
def render_pages(pdf_path, out_dir, zoom=1.5):
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(zoom, zoom)
    page_count = len(doc)
    for i in range(page_count):
        pix = doc[i].get_pixmap(matrix=mat)
        out_path = os.path.join(out_dir, f'page-{i+1:02d}.png')
        pix.save(out_path)
        print(f'  Rendered page {i+1} → {out_path}')
    doc.close()
    print(f'Rendered {page_count} pages to {out_dir}/')


# ---------------------------------------------------------------------------
# Banned content check
# ---------------------------------------------------------------------------
BANNED = {
    'em_dash':   ['\u2014', '\u2013'],
    'absolutes': ['Zero digital', 'Never ', 'Always ', 'Every '],
    'ai_tells':  ['leverage', 'utilize', 'impactful', 'synergies', 'best-in-class',
                  'game-changing', 'mission-critical', 'robust solution'],
}


def check_content(pdf_path):
    doc = fitz.open(pdf_path)
    hits = []
    for i, page in enumerate(doc):
        text = page.get_text()
        for category, words in BANNED.items():
            for w in words:
                if w.lower() in text.lower():
                    hits.append((i + 1, w, category))
                    print(f'  Page {i+1}: banned "{w}" [{category}]')
    doc.close()
    if not hits:
        print('PASS: No banned content found.')
    else:
        print(f'WARN: {len(hits)} banned content hit(s). Review each — some may be legitimate.')
    return len(hits) == 0


# ---------------------------------------------------------------------------
# Title extraction — reverse-outline check (polish-pass Pass 3)
# ---------------------------------------------------------------------------
def print_titles(pdf_path):
    """Extract and print the largest-font text block per page.

    The reverse-outline check: read these in sequence. If they don't tell
    the story, the structure is wrong. See references/polish-pass.md.
    """
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        candidates = []
        for b in page.get_text('dict')['blocks']:
            if 'lines' not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    t = span['text'].strip()
                    if len(t) < 3:
                        continue
                    if any(skip in t for skip in FOOTER_SKIP):
                        continue
                    candidates.append((span['size'], span['bbox'][1], t))
        if not candidates:
            print(f'Page {i+1:2d}: [no text]')
            continue
        candidates.sort(key=lambda c: (-c[0], c[1]))
        max_size = candidates[0][0]
        title_spans = [c for c in candidates if c[0] >= max_size - 0.5]
        title_spans.sort(key=lambda c: c[1])
        title = ' '.join(c[2] for c in title_spans)
        print(f'Page {i+1:2d}: {title}')
    doc.close()


# ---------------------------------------------------------------------------
# Layout repetition check (content-rules: no pattern repeats 3+ in a row)
# ---------------------------------------------------------------------------
def check_repetition(pdf_path):
    """Fingerprint each page by its rough layout shape and flag 3+ in a row.

    Fingerprint: sorted tuple of (rounded y-band, rounded x-band, text-length-bucket)
    for the 6 largest text blocks. Crude but stable.
    """
    doc = fitz.open(pdf_path)
    fingerprints = []
    for i, page in enumerate(doc):
        blocks = []
        for b in page.get_text('dict')['blocks']:
            if 'lines' not in b:
                continue
            text = ''.join(s['text'] for ln in b['lines'] for s in ln['spans'])
            if len(text.strip()) < 3:
                continue
            bb = b['bbox']
            blocks.append((bb, len(text)))
        blocks.sort(key=lambda x: -x[1])
        top = blocks[:6]
        ph = page.rect.height
        pw = page.rect.width
        fp = tuple(sorted((round(bb[1] / ph * 8), round(bb[0] / pw * 8),
                          min(tl // 50, 10))
                         for bb, tl in top))
        fingerprints.append(fp)
    doc.close()

    runs = []
    run_start = 0
    for i in range(1, len(fingerprints)):
        if fingerprints[i] != fingerprints[i - 1]:
            if i - run_start >= 3:
                runs.append((run_start, i - 1))
            run_start = i
    if len(fingerprints) - run_start >= 3:
        runs.append((run_start, len(fingerprints) - 1))

    if runs:
        for s, e in runs:
            print(f'  WARN: pages {s+1}-{e+1} share a layout fingerprint '
                  f'({e - s + 1} in a row). Break one with a divider or alternate pattern.')
        print(f'WARN: {len(runs)} repetition run(s) found.')
        return False
    print('PASS: No 3+ consecutive pages share a layout.')
    return True


# ---------------------------------------------------------------------------
# Basic metadata checks
# ---------------------------------------------------------------------------
def check_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    file_size_mb = os.path.getsize(pdf_path) / 1024 / 1024

    page = doc[0]
    w, h = page.rect.width, page.rect.height
    doc.close()

    print(f'Pages: {page_count}')
    print(f'File size: {file_size_mb:.1f} MB')
    print(f'Page dimensions: {w:.0f} × {h:.0f} pt')

    size_ok = 3 <= file_size_mb <= 25
    dim_ok = abs(w - 960) < 5 and abs(h - 540) < 5
    print(f'File size check: {"PASS" if size_ok else "WARN (outside 3–25 MB range)"}')
    print(f'Dimensions check: {"PASS" if dim_ok else f"FAIL — expected ~960x540pt, got {w:.0f}x{h:.0f}"}')
    return size_ok and dim_ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Verify a Metis proposal PDF.')
    parser.add_argument('--pdf', required=True, help='Path to the PDF file')
    parser.add_argument('--mode', default='all',
                        choices=['overlaps', 'fill', 'render', 'content', 'metadata',
                                 'titles', 'repetition', 'all'],
                        help='Which check to run')
    parser.add_argument('--out', default='verify', help='Output directory for rendered PNGs')
    parser.add_argument('--skip', nargs='*', type=int, default=[],
                        help='0-indexed page numbers to skip for fill check (cover, dividers)')
    parser.add_argument('--print-titles', action='store_true',
                        help='Extract and print page titles (reverse-outline check)')
    parser.add_argument('--check-repetition', action='store_true',
                        help='Flag 3+ consecutive pages with identical layout fingerprint')
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f'ERROR: File not found: {args.pdf}')
        sys.exit(1)

    print(f'\n=== Verifying: {args.pdf} ===\n')
    results = {}

    if args.mode in ('metadata', 'all'):
        print('--- Metadata ---')
        results['metadata'] = check_metadata(args.pdf)
        print()

    if args.mode in ('overlaps', 'all'):
        print('--- Overlap check ---')
        results['overlaps'] = check_overlaps(args.pdf)
        print()

    if args.mode in ('fill', 'all'):
        print('--- Fill check ---')
        results['fill'] = check_fill(args.pdf, skip_pages=args.skip)
        print()

    if args.mode in ('content', 'all'):
        print('--- Content check ---')
        results['content'] = check_content(args.pdf)
        print()

    if args.mode in ('render', 'all'):
        print('--- Rendering pages ---')
        render_pages(args.pdf, args.out)
        print()

    if args.mode == 'titles' or args.print_titles:
        print('--- Page titles (reverse-outline check) ---')
        print_titles(args.pdf)
        print()

    if args.mode == 'repetition' or args.check_repetition:
        print('--- Layout repetition check ---')
        results['repetition'] = check_repetition(args.pdf)
        print()

    if args.mode == 'all':
        failed = [k for k, v in results.items() if not v]
        if failed:
            print(f'\nSUMMARY: Issues found in: {", ".join(failed)}')
            print('Review the output above, then render pages and do visual verification.')
        else:
            print('\nSUMMARY: All programmatic checks passed.')
            print(f'Next step: visually review rendered PNGs in {args.out}/')


if __name__ == '__main__':
    main()
