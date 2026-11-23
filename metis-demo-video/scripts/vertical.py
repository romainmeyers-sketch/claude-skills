"""Step 2b (optional): a 9:16 cut for Instagram, LinkedIn mobile and TikTok, made from the finished 16:9 video.

  python vertical.py storyboard.json        -> out/<name>-vertical.mp4 (1080x1920)

storyboard "vertical": {"title": "Your agent said done.\\nIt wasn't.", "handle": "Metis Strategy", "bg": "plain"}
The reels layout: a big title in the top third that stays on screen the whole time (the hook people
read while the video loops), the 16:9 video in the middle with rounded corners, a small handle below,
all on the scene's environment (same CSS as the stage, so it matches the video's look).
"""
import html, os, subprocess, sys
from common import Board, SKILL_DIR, check_deps, ffmpeg

W, H = 1080, 1920
VW = 1032                                  # video width inside the frame (24 px margins)
VH = round(VW * 9 / 16 / 2) * 2


def page(board, v, brand, mask=False):
    css = open(os.path.join(SKILL_DIR, 'assets', 'stage', 'stage.css'), encoding='utf-8').read()
    vars_ = ':root{%s}' % ''.join('--%s:%s;' % (k, val if k != 'font' else "'%s'" % val) for k, val in brand.items() if k != 'font_url')
    font = brand.get('font', 'Archivo')
    link = brand.get('font_url') or 'https://fonts.googleapis.com/css2?family=%s:wght@400;600;700&display=swap' % font.replace(' ', '+')
    y = (H - VH) // 2 + v.get('offset', 120)
    if mask:
        body = '<div style="position:absolute;left:0;top:0;width:%dpx;height:%dpx;border-radius:%dpx;background:#fff"></div>' % (VW, VH, v.get('radius', 34))
        return '<!doctype html><html><head><style>*{margin:0}html,body{width:%dpx;height:%dpx;background:#000}</style></head><body>%s</body></html>' % (VW, VH, body)
    title = '<br>'.join(html.escape(l) for l in v.get('title', '').split('\n'))
    title = title.replace('**', '')                # keep the title plain: one look, one colour
    bgv = v.get('bg', 'plain')                   # plain: the brand background, so the video reads as a clean card
    bgdiv = '' if bgv == 'plain' else '<div class="sbg bgv bg-%s" style="z-index:0"></div>' % html.escape(bgv)
    body = ('%s'
            '<div style="position:absolute;left:70px;right:70px;top:%dpx;transform:translateY(-100%%);text-align:center;font-size:%dpx;font-weight:700;line-height:1.1;letter-spacing:-.03em;color:var(--text);white-space:nowrap">%s</div>'
            '<div style="position:absolute;left:0;right:0;top:%dpx;text-align:center;font-size:34px;font-weight:600;color:var(--muted)">%s</div>'
            % (bgdiv, y - 70, v.get('size', 80), title, y + VH + 60, html.escape(v.get('handle', ''))))
    return ('<!doctype html><html><head><meta charset="utf-8"><link href="%s" rel="stylesheet"><style>%s\n%s\n'
            'html,body{width:%dpx!important;height:%dpx!important;overflow:hidden}</style></head><body>%s</body></html>' % (link, vars_, css, W, H, body))


def main():
    check_deps()
    from playwright.sync_api import sync_playwright
    from render import DEFAULT_BRAND, launch
    board = Board(sys.argv[1])
    v = board.data.get('vertical')
    if not v:
        sys.exit('No "vertical" block in the storyboard.')
    name = board.data.get('output_name') or os.path.splitext(os.path.basename(board.path))[0]
    src = os.path.join(board.out, name + '.mp4')
    if not os.path.exists(src):
        sys.exit('Run mix.py first (%s is missing).' % src)
    brand = dict(DEFAULT_BRAND, **board.data.get('brand', {}))
    bg_png, mask_png = os.path.join(board.out, 'vertical_bg.png'), os.path.join(board.out, 'vertical_mask.png')
    with sync_playwright() as pw:
        b = launch(pw)
        for f, w, h, m in ((bg_png, W, H, False), (mask_png, VW, VH, True)):
            p = b.new_page(viewport={'width': w, 'height': h})
            p.set_content(page(board, v, brand, m)); p.wait_for_load_state('networkidle'); p.evaluate('document.fonts.ready')
            p.wait_for_timeout(300); p.screenshot(path=f); p.close()
        b.close()
    y = (H - VH) // 2 + v.get('offset', 120)
    out = os.path.join(board.out, name + '-vertical.mp4')
    fc = ('[0:v]scale=%d:%d,format=rgba[v];[2:v]format=gray,scale=%d:%d[m];[v][m]alphamerge[r];'
          '[1:v]format=rgba[b];[b][r]overlay=%d:%d,format=yuv420p[o]' % (VW, VH, VW, VH, (W - VW) // 2, y))
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', src, '-loop', '1', '-framerate', '30', '-i', bg_png, '-loop', '1', '-framerate', '30', '-i', mask_png,
                    '-filter_complex', fc, '-map', '[o]', '-map', '0:a?', '-shortest', '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    '-color_range', 'tv', '-c:a', 'copy', '-movflags', '+faststart', out], check=True)
    print('wrote', out)


if __name__ == '__main__':
    main()
