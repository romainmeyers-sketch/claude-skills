"""Helper: make the "before" page images for a pages scene from small HTML files.

  python make_pages.py page1.html page2.html ... --out assets/     -> assets/page1.png, assets/page2.png, ...
  python make_pages.py --example assets/old_p1.html                 -> writes a starter page to edit

Each page renders at the size the pages scene uses (560 x 725, at 2x for sharpness), so a mock
slide, email thread, meeting notes or tracker looks like a real printed page in the fanned stack.
Use realistic but fictional content. To find the "highlight" box for the scene, open the PNG and
convert the pixel box to percentages of its width and height.
"""
import argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE_W, PAGE_H = 560, 725

EXAMPLE = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:560px;height:725px;overflow:hidden;font-family:Calibri,Arial,sans-serif;color:#222;background:#fff}
.pad{padding:34px 36px} h1{font-size:22px;margin:0 0 4px;color:#1f3864} .sub{font-size:11px;color:#777;margin-bottom:16px}
table{border-collapse:collapse;width:100%;font-size:11px} td,th{border:1px solid #bbb;padding:5px 6px;text-align:left} th{background:#d9e2f3}
.tbd{background:#fff2a8}
</style></head><body><div class="pad">
<h1>Decisions &amp; next steps</h1><div class="sub">Slide 37 of 52</div>
<table><tr><th>#</th><th>Decision</th><th>Owner</th><th>Due</th></tr>
<tr><td>1</td><td>One platform for both regions</td><td class="tbd">TBD</td><td>TBD</td></tr>
<tr><td>2</td><td>Retire the legacy tool by Q2</td><td>Sam</td><td>Q2</td></tr>
<tr><td>3</td><td>Freeze changes until cutover</td><td class="tbd">TBD</td><td>?</td></tr>
</table></div></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pages', nargs='*', help='HTML files, one per page')
    ap.add_argument('--out', help='folder for the PNGs (default: next to each HTML file)')
    ap.add_argument('--example', help='write a starter page to this path and stop')
    a = ap.parse_args()
    if a.example:
        with open(a.example, 'w', encoding='utf-8') as f:
            f.write(EXAMPLE)
        print('wrote', a.example); return
    if not a.pages:
        ap.error('give one or more HTML files, or --example <path>')
    sys.path.insert(0, HERE)
    from common import check_deps
    check_deps()
    from playwright.sync_api import sync_playwright
    from render import launch
    with sync_playwright() as pw:
        browser = launch(pw)
        page = browser.new_page(viewport={'width': PAGE_W, 'height': PAGE_H}, device_scale_factor=2)
        for src in a.pages:
            src = os.path.abspath(src)
            out_dir = os.path.abspath(a.out) if a.out else os.path.dirname(src)
            os.makedirs(out_dir, exist_ok=True)
            png = os.path.join(out_dir, os.path.splitext(os.path.basename(src))[0] + '.png')
            page.goto('file:///' + src.replace('\\', '/'))
            page.wait_for_load_state('load')
            page.screenshot(path=png)
            print('wrote', png)
        browser.close()


if __name__ == '__main__':
    main()
