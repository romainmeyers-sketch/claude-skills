"""Step 1: render the storyboard to video, frame by frame.

  python render.py storyboard.json             full video  -> out/frames.mp4, out/cues.json
  python render.py storyboard.json --until 2   only scenes 0..2 (fast preview while iterating)

The stage (1920x1080) holds every scene and, for "app" scenes, the real app in a
browser window under a moving camera. A frozen clock (assets/stage/clock.js)
advances exactly one frame at a time and every frame is screenshotted, so the
result is perfectly smooth no matter how heavy the page is.
"""
import argparse, base64, functools, html, http.server, json, os, re, subprocess, threading, time
from common import Board, SKILL_DIR, check_deps, ffmpeg

STAGE = os.path.join(SKILL_DIR, 'assets', 'stage')
FPS = 30
RATE = FPS                                         # frames captured per second; FPS x "motion_blur" subframes
XFADE = 300                                        # ms between one scene starting to leave and the next one coming in
CH = 46                                            # browser-window title bar height
DEFAULT_BRAND = {'bg': '#11294d', 'glow1': 'rgba(75,132,207,.32)', 'glow2': 'rgba(244,152,19,.14)', 'accent': '#f49813',
                 'text': '#ffffff', 'muted': '#c7d6ee', 'font': 'Archivo'}
E = html.escape


def rich(text, accent=True):
    """**word** -> bold accent."""
    return re.sub(r'\*\*(.+?)\*\*', (r'<b>\1</b>' if accent else r'\1'), E(text))


def words_of(line):
    """'in a **Word document?**' -> [['in', False], ['a', False], ['Word', True], ['document?', True]]"""
    out, bold = [], False
    for tok in line.split(' '):
        b0 = tok.startswith('**'); t = tok.strip('*')
        if b0: bold = True
        out.append([t, bold])
        if tok.endswith('**'): bold = False
    return [w for w in out if w[0]]


def rise(text, d0=100, step=70):
    """Words that rise in one after another; **marked** words in the accent color."""
    out = []
    for i, (w, b) in enumerate(words_of(text)):
        span = '<span class="r" style="--d:%dms">%s</span>' % (d0 + i * step, E(w))
        out.append('<b>%s</b>' % span if b else span)
    return ' '.join(out)


# ------------------------------------------------------------------ scene HTML
def crop_card(board, c, idx):
    from PIL import Image
    img = board.rel(c['image'])
    iw, ih = Image.open(img).size
    x, y, w, h = c.get('crop', [0, 0, iw, ih * 0.6])
    cw = c.get('width', 430); s = cw / float(w); chh = h * s
    spots = [(110, 90, 22, -3), (1390, 80, -20, 3), (170, 720, 18, 2), (1340, 690, -18, -2)]
    left, top, ry, rz = spots[idx % 4]
    return ('<div class="fl" style="left:%dpx;top:%dpx;--ry:%ddeg;--rz:%ddeg;--d:%dms"><div class="crop" style="width:%dpx;height:%dpx;'
            'background-image:url(%s);background-size:%dpx auto;background-position:%dpx %dpx"></div></div>'
            % (left, top, ry, rz, idx * 110, cw, chh, web(board, img), iw * s, -x * s, -y * s))


def web(board, path):
    return '/' + os.path.relpath(path, board.dir).replace('\\', '/')


def vo_of(board, sc):
    """Narration timing for a scene (words and caption phrases), or None."""
    m = board.json_in('voice_manifest.json') or {}
    return m.get(sc.get('vo'))


def clip_frames(board, sc):
    """Image sequence for a "clip" scene (a Remotion render with --sequence), in frame order."""
    d = board.rel(sc['frames'])
    fr = sorted(os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(('.png', '.jpg', '.jpeg'))) if os.path.isdir(d) else []
    if not fr:
        raise SystemExit('Clip scene: no frames in %s. Render them first, see references/remotion.md.' % d)
    return fr[sc.get('start', 0):sc.get('end', len(fr))]


ARC_SVG = ('<svg class="arc-mark" viewBox="0 0 230 120"><path d="M18 112A97 97 0 0 1 212 112" fill="none" stroke="var(--accent)" '
           'stroke-width="16" stroke-linecap="round"/></svg>')


PILL_ICONS = {
    'play': '<svg viewBox="0 0 24 24"><path d="M7 4l13 8-13 8z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>',
    'search': '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    'arrow': '<svg viewBox="0 0 24 24"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'user': '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
}


def _attrs(s):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', s))


def expand_tags(body):
    """Shorthand tags for motion scenes:
    <mascot class="m1" kind="bot|box|blob" color="#3bdac0" size="220" acc="tie|hardhat|headset|glasses" name="Chief of Staff" style="left:..;top:.."></mascot>
    <wave n="26"></wave> (bars for a call card; they move while an ancestor has class "talking")"""
    def mascot(m):
        a = _attrs(m.group(1))
        acc = ''.join('<i class="m-acc %s"></i>' % E(x) for x in a.get('acc', '').split() if x)
        tag = '<div class="m-tag">%s</div>' % E(a['name']) if a.get('name') else ''
        return ('<div class="masc %s %s" style="--mc:%s;--ms:%spx;%s"><div class="m-shadow"></div><div class="m-in">'
                '<i class="m-ant"></i><i class="m-arm l"></i><i class="m-arm r"></i><div class="m-body">'
                '<div class="m-face"><div class="m-eyes"><i></i><i></i></div><i class="m-mouth"></i><i class="m-blush l"></i><i class="m-blush r"></i></div>'
                '</div>%s</div>%s</div>' % (E(a.get('kind', 'bot')), E(a.get('class', '')), E(a.get('color', '#7aa2ff')),
                                            E(a.get('size', '220')), a.get('style', ''), acc, tag))
    body = re.sub(r'<mascot\b([^>]*)>\s*</mascot>', mascot, body)
    body = re.sub(r'<wave\b([^>]*)>\s*</wave>', lambda m: '<div class="wave">%s</div>' % ('<i></i>' * int(_attrs(m.group(1)).get('n', 24))), body)
    return body


def scene_html(board, i, sc):
    t = sc['type']; sid = 's%d' % i
    if t == 'clip':
        return '<section class="scene clip" id="%s"><img class="clip-img" id="%s-img" src="%s" alt=""></section>' % (
            sid, sid, web(board, clip_frames(board, sc)[0]))
    if t == 'hook':
        cards = ''.join(crop_card(board, c, k) for k, c in enumerate(sc.get('cards', [])))
        rows = ''.join('<div class="row%s" id="row%d"><div class="tw" id="tw%d"><span class="txt"></span><i class="caret"></i></div></div>'
                       % (' row2' if k else '', k + 1, k + 1) for k in range(len(sc['lines'])))
        return '<section class="scene" id="s-hook" data-i="%d">%s%s</section>' % (i, cards, rows)
    if t == 'reveal':
        mark = ''
        stack = ''
        if sc.get('logo') == 'arc':
            mark, stack = ARC_SVG, ' stack'
        elif sc.get('logo') == 'arcs':
            mark = ('<svg class="logo-mark" viewBox="0 0 170 100"><path d="M10 92A75 75 0 0 1 160 92" fill="none" stroke="var(--text)" stroke-opacity=".55" stroke-width="12" stroke-linecap="round"/>'
                    '<path d="M32 92A53 53 0 0 1 138 92" fill="none" stroke="var(--text)" stroke-opacity=".75" stroke-width="12" stroke-linecap="round"/>'
                    '<path d="M54 92A31 31 0 0 1 116 92" fill="none" stroke="var(--text)" stroke-width="12" stroke-linecap="round"/>'
                    '<path d="M68 92A17 17 0 0 1 102 92Z" fill="var(--accent)"/></svg>')
        elif sc.get('logo'):
            mark = '<img class="logo-mark" src="%s" alt="">' % web(board, board.rel(sc['logo']))
            stack = ' stack' if sc.get('stack') else ''
        pill = ''
        if sc.get('pill'):
            pill = '<div class="pill"><span class="star">&#10022;</span><span id="ptxt">%s</span></div>' % ' '.join(
                '<span class="pw">%s</span>' % E(w) for w in sc['pill'].split(' '))
        return ('<section class="scene" id="s-reveal" data-i="%d"><div class="meet" id="meet">%s</div>'
                '<div class="logo-row%s">%s<div class="logo-txt">%s</div></div>%s</section>'
                % (i, E(sc.get('intro', 'Meet')), stack, mark, E(sc['name']), pill))
    if t == 'pages':
        imgs = sc['images'][:4]
        fan = [('translateX(-20px) translateZ(-260px) rotateY(24deg) rotateZ(-4deg)', 0), ('translateZ(-160px) rotateY(16deg) rotateZ(-2deg)', 150),
               ('translateZ(-60px) rotateY(9deg) rotateZ(-1deg)', 300), ('rotateY(4deg)', 430)][-len(imgs):]
        hl = sc.get('highlight')
        pages = ''
        for k, img in enumerate(imgs):
            inner = ''
            if hl and k == (hl.get('page', len(imgs) - 1) % len(imgs)):
                l, tp, w, h = hl['box']
                inner = '<div class="hl" style="left:%s%%;top:%s%%;width:%s%%;height:%s%%"></div>' % (l, tp, w, h)
                if hl.get('label'):
                    inner += '<div class="hl-tag" style="right:%s%%;top:%s%%">%s</div>' % (max(0, 100 - l - w), max(0, tp - 6), E(hl['label']))
            pages += '<div class="pg" style="left:%dpx;--d:%dms;--t:%s;background-image:url(%s)">%s</div>' % (
                fan[k][1], 100 + k * 150, fan[k][0], web(board, board.rel(img)), inner)
        vo = vo_of(board, sc)
        def pd(k):
            if vo and len(vo['segs']) > k + 1: return int(vo['segs'][k + 1]['start'] * 1000 + 150)
            return 1500 + k * 800
        pts = ''.join('<div class="point" style="--d:%dms"><i>%s</i><div><b>%s</b><span>%s</span></div></div>'
                      % (pd(k), E(p.get('icon', '×')), E(p['title']), E(p.get('body', ''))) for k, p in enumerate(sc.get('points', [])))
        return ('<section class="scene" id="%s"><div style="position:absolute;left:150px;top:110px"><div class="k">%s</div>'
                '<div class="mid" style="margin-top:14px;font-size:64px">%s</div></div><div class="pages"><div class="pages-in">%s</div></div>'
                '<div class="points">%s</div></section>' % (sid, E(sc.get('kicker', '')), rich(sc.get('title', '')), pages, pts))
    if t == 'quote':
        return ('<section class="scene" id="%s"><div class="left" style="width:1400px"><div class="k">%s</div>'
                '<p class="quote" style="margin-top:40px"><span class="mark r">&ldquo;</span>%s</p><p class="who r" style="--d:900ms">%s</p></div></section>'
                % (sid, E(sc.get('kicker', '')), rise(sc['text'], 150, 55), E(sc.get('who', ''))))
    if t == 'statement':
        return ('<section class="scene" id="%s"><div class="left"><div class="k">%s</div><div class="mid" style="margin-top:30px">%s</div>'
                '<p class="lead" style="margin-top:34px">%s</p>%s</div></section>' % (sid, E(sc.get('kicker', '')), rise(sc['title']), E(sc.get('sub', '')),
                '<p class="foot r" style="--d:%dms">%s</p>' % ((int(vo_of(board, sc)['segs'][1]['start'] * 1000) if vo_of(board, sc) and len(vo_of(board, sc)['segs']) > 1 else sc.get('foot_ms', 2000)), E(sc['foot'])) if sc.get('foot') else ''))
    if t == 'cards':
        vo = vo_of(board, sc)
        def cd(k):
            if vo and len(vo['segs']) > k: return int(vo['segs'][k]['start'] * 1000 + 100)
            return 500 + k * 250
        cards = ''.join('<div class="card" style="--d:%dms"><div class="n">%02d</div><h3>%s</h3><p>%s</p></div>'
                        % (cd(k), k + 1, E(c['title']), E(c.get('body', ''))) for k, c in enumerate(sc['cards']))
        return ('<section class="scene" id="%s"><div class="left" style="width:1620px"><div class="k">%s</div><div class="mid" style="margin-top:26px">%s</div>'
                '<div class="cards" style="--n:%d">%s</div></div></section>' % (sid, E(sc.get('kicker', '')), rise(sc.get('title', '')), len(sc['cards']), cards))
    if t == 'inset':
        parts, k = [], 0
        for tok in sc['text'].split(' '):
            if tok == '[img]':
                im = sc['image'] if isinstance(sc['image'], dict) else {'file': sc['image']}
                parts.append('<span class="ins" style="--d:%dms;--w:%s;--pos:%s"><img src="%s" alt=""></span>'
                             % (sc.get('open_ms', 1500), im.get('width', '4.6em'), im.get('position', '50% 0'), web(board, board.rel(im['file']))))
                continue
            b = tok.startswith('**') or tok.endswith('**'); w = tok.strip('*')
            span = '<span class="r" style="--d:%dms">%s</span>' % (150 + k * sc.get('word_ms', 220), E(w)); k += 1
            parts.append('<b>%s</b>' % span if b else span)
        return '<section class="scene" id="%s"><div class="center"><div class="ins-line" style="font-size:%dpx">%s</div></div></section>' % (sid, sc.get('size', 96), ' '.join(parts))
    if t == 'prompt':
        chips = ''.join('<span class="pr-chip">%s</span>' % E(c) for c in sc.get('chips', ['+']))
        return ('<section class="scene" id="%s"><div class="pr-box"><div class="pr-txt"><span class="ph">%s</span><span class="t"></span><i class="caret"></i></div>'
                '<div class="pr-bar">%s<span class="pr-send">&uarr;</span></div></div></section>' % (sid, E(sc.get('placeholder', '')), chips))
    if t == 'motion':
        body = sc.get('html', '')
        if re.search(r'\.html?$', body.strip()):
            body = open(board.rel(body.strip()), encoding='utf-8').read()
        body = expand_tags(body)
        body = re.sub(r'url\((["\']?)(assets/[^)"\']+)\1\)', lambda m: 'url(%s)' % web(board, board.rel(m.group(2))), body)
        body = re.sub(r'src="(assets/[^"]+)"', lambda m: 'src="%s"' % web(board, board.rel(m.group(1))), body)
        return '<section class="scene%s" id="%s"><div class="mt"><div class="mc">%s<i class="mcur"></i></div></div></section>' % (
            ' glowtop' if sc.get('glow') == 'top' else '', sid, body)
    if t == 'beats':
        return '<section class="scene%s" id="%s">%s</section>' % (' blurin' if sc.get('anim') == 'blur' else '', sid, ''.join('<div class="bt" style="--fs:%dpx"><span>%s</span></div>' % (min(190, int(1650 / (0.56 * max(1, len(w.replace('*', '')))))), rich(w)) for w in sc['words']))
    if t == 'chat':
        items = ''
        for m in sc['messages']:
            if 'divider' in m:
                items += '<div class="ch-div"><span>%s</span></div>' % E(m['divider']); continue
            card = ''
            if m.get('card'):
                card = '<div class="ch-card"><i class="cc-bar"></i><div><b>%s</b><span>%s</span></div></div>' % (E(m['card'].get('title', '')), E(m['card'].get('url', '')))
            ini = m.get('initials') or ''.join(w[0] for w in m['name'].split()[:2]).upper()
            items += ('<div class="msg"><div class="av" style="background:%s">%s</div><div><div class="nm">%s<span>%s</span></div><div class="tx">%s</div>%s</div></div>'
                      % (E(m.get('color', '#4a5bd4')), E(ini), E(m['name']), E(m.get('time', '')), rich(m.get('text', '')), card))
        return ('<section class="scene" id="%s"><div class="chat"><div class="ch-head"><b>%s</b><span>%s</span></div><div class="ch-body">%s</div></div><i class="ccur"></i></section>'
                % (sid, E(sc.get('channel', '# team')), E(sc.get('subtitle', '')), items))
    if t == 'phone':
        lap = ''
        if sc.get('laptop'):
            lap = ('<div class="ph-lap"><div class="lid"><div class="scr" style="background-image:url(%s)"></div></div><div class="base"></div></div>'
                   % web(board, board.rel(sc['laptop'])))
        return ('<section class="scene" id="%s">%s<div class="phone"><div class="ph-scr"><iframe name="phone" src="app.html"></iframe></div></div></section>'
                % (sid, lap))
    if t == 'endcard':
        return ('<section class="scene endcard" id="%s"><div class="center">%s<div class="mid">%s</div><p class="lead">%s</p></div></section>'
                % (sid, ('<img class="end-logo" src="%s" alt="">' % web(board, board.rel(sc['logo']))) if sc.get('logo') else (ARC_SVG if sc.get('arc', True) else ''),
                   rise(sc['title'], 700), E(sc.get('sub', ''))))
    if t == 'pill':
        return ('<section class="scene" id="%s"><div class="gp-wrap"><div class="gpill">%s<span>%s</span></div></div><i class="gp-hand"></i></section>'
                % (sid, PILL_ICONS.get(sc.get('icon', 'play'), ''), rich(sc['text'])))
    if t == 'float':
        from PIL import Image
        spots = [(-560, -360, -120, 18), (420, -380, -300, -16), (-620, 120, 60, 14), (380, 90, 160, -12), (-60, -140, 320, 0), (720, -60, -80, -20)]
        pcs = ''
        for k, img in enumerate(sc['images'][:6]):
            f, w = (img['file'], img.get('width', 640)) if isinstance(img, dict) else (img, 640)
            x, y, z, ry = spots[k]
            iw, ih = Image.open(board.rel(f)).size
            pcs += ('<div class="fpc" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;--z:%dpx;--ry:%ddeg;--d:%dms;--y0:%dpx;background-image:url(%s)"></div>'
                    % (960 + x - w // 2, 470 + y, w, int(w * ih / iw), z, ry, 120 + k * 140, 260 + k * 40, web(board, board.rel(f))))
        return ('<section class="scene" id="%s"><div class="fl3"><div class="fl3-in">%s</div></div><div class="fl3-t">%s</div></section>'
                % (sid, pcs, rise(sc.get('title', ''), 900)))
    if t == 'device':
        return ('<section class="scene" id="%s"><div class="dev%s"><div class="lap"><div class="lid"><div class="scr" style="background-image:url(%s)"></div></div><div class="base"></div></div></div></section>'
                % (sid, ' float' if sc.get('float') else '', web(board, board.rel(sc['screen']))))
    if t == 'app':
        return ''
    raise SystemExit('Unknown scene type "%s" (scene %d). See references/storyboard.md.' % (t, i))


LIGHT_BGS = ('light', 'shadow', 'desk', 'yellow', 'ice', 'studio')


def scene_bg(d, i, sc):
    """The scene's environment: its own "bg", or with "auto_bg": true a default that follows the story
    (problem scenes stay on the brand background, the reveal rises into the sunrise, the app sits on the
    moving brand mesh, beats are warm, the closing card is brand blue)."""
    if sc.get('bg') or not d.get('auto_bg'):
        return sc.get('bg')
    t, last = sc['type'], i == len(d['scenes']) - 1
    if t == 'reveal': return 'rise'
    if t == 'app': return 'mesh'
    if t == 'beats': return 'sunrise'
    if t == 'endcard' or (last and t == 'statement'): return 'blue'
    return None


def with_bg(board, sc, h, v=None):
    """Give a scene its own environment: "bg": "light" | "shadow" | "mesh" | "desk" | "dark" | an image file."""
    v = v or sc.get('bg')
    if not v or sc['type'] == 'app' or not h:
        return h
    if re.search(r'\.(png|jpe?g|webp)$', v, re.I):
        div = '<div class="sbg bgv bg-image" style="background-image:url(%s)"></div>' % web(board, board.rel(v))
    elif ':' in v:                                  # "studio:#cfe3ff": an environment with its own colour
        v, col = v.split(':', 1)
        div = '<div class="sbg bgv bg-%s" style="--%s:%s"></div>' % (E(v), E(v), E(col))
    else:
        div = '<div class="sbg bgv bg-%s"></div>' % E(v)
    light = sc.get('theme', 'light' if v in LIGHT_BGS else 'dark') == 'light'
    h = h.replace('class="scene"', 'class="scene%s"' % (' light' if light else ''), 1)
    k = h.index('>') + 1
    return h[:k] + div + h[k:]


def stage_html(board):
    d = board.data
    brand = dict(DEFAULT_BRAND, **d.get('brand', {}))
    if d.get('auto_bg'):                           # environments the brand doesn't colour itself are mixed from bg and accent
        mix = lambda a, b, p: 'color-mix(in srgb, %s %d%%, %s)' % (a, p, b)
        bg, ac = brand['bg'], brand['accent']
        for k, v in {'mesh-bg': bg, 'mesh1': mix(ac, 'transparent', 45), 'mesh2': mix(bg, '#ffffff', 80),
                     'mesh3': mix(ac, 'transparent', 25), 'sun1': bg, 'sun2': mix(bg, ac, 75), 'sun3': mix(bg, ac, 50),
                     'sun4': mix(ac, '#ffffff', 60), 'sun5': ac, 'blue': mix(bg, ac, 85), 'blue-hi': mix(bg, ac, 65)}.items():
            brand.setdefault(k, v)
    # the glow light is mixed from the brand (never a stock orange): accent for the warm light, a cool tint for glow-cool
    mix = lambda a, b, p: 'color-mix(in srgb, %s %d%%, %s)' % (a, p, b)
    bg, ac = brand['bg'], brand['accent']
    for k, v in {'glow-top': mix(bg, '#000', 55), 'glow-base': bg, 'glow-hot': mix(ac, '#ffffff', 45), 'glow-mid': ac,
                 'glow-edge': mix(ac, 'transparent', 35), 'cool-hot': mix(brand.get('good', ac), '#ffffff', 50),
                 'cool-mid': brand.get('good', ac), 'cool-edge': mix(bg, '#6a7cff', 40)}.items():
        brand.setdefault(k, v)
    app = d.get('app') or {}
    aw, ah = app.get('viewport', [1440, 900])
    ch = 0 if app.get('frame') == 'none' else CH
    # "caption_safe" (default on): the fitted window leaves a band at the bottom for the caption pill,
    # so a caption on a full-window shot never sits over the app's content
    safe = app.get('caption_safe', True)
    fit_scale = min(1700.0 / aw, (880.0 if safe else 960.0) / (ah + ch)) * 0.96
    fit_cy = 470 if safe else 500
    font = brand['font']
    font_link = brand.get('font_url') or 'https://fonts.googleapis.com/css2?family=%s:wght@300;400;500;600;700&display=swap' % font.replace(' ', '+')
    css = open(os.path.join(STAGE, 'stage.css'), encoding='utf-8').read()
    js = open(os.path.join(STAGE, 'stage.js'), encoding='utf-8').read()
    vars_ = ':root{%s}' % ''.join('--%s:%s;' % (k, v if k != 'font' else "'%s'" % v) for k, v in brand.items() if k != 'font_url')
    scenes = ''.join(with_bg(board, sc, scene_html(board, i, sc), scene_bg(d, i, sc)) for i, sc in enumerate(d['scenes']))
    rig = ''
    if app:
        bar = ('<div class="bar" style="height:%dpx"><i class="dot"></i><i class="dot"></i><i class="dot"></i><div class="url">%s</div></div>'
               % (ch, E(app.get('url_label', '')))) if ch else ''
        rig = ('<div id="rig"><div id="tilt"><div id="win" class="%s" style="width:%dpx">%s<iframe id="app" name="app" src="app.html" style="width:%dpx;height:%dpx"></iframe></div></div></div>'
               % ('' if ch else 'noframe', aw, bar, aw, ah))
    # icons: <i data-lucide="target"></i> anywhere in scene HTML becomes a Lucide SVG (assets/stage/lucide.min.js, ISC)
    icons = ''
    if 'data-lucide' in scenes:
        icons = '<script>%s\nlucide.createIcons();</script>' % open(os.path.join(STAGE, 'lucide.min.js'), encoding='utf-8').read()
    return ('<!doctype html><html><head><meta charset="utf-8"><link href="%s" rel="stylesheet"><style>%s\n%s\n%s</style></head><body>'
            '<div id="bg"></div><div id="wipe"></div><div id="stripe"></div><div id="flood"></div>%s%s<div id="note"><div class="av"></div><div><b></b><span></span></div></div><div id="cap"></div>'
            '%s<script>window.__STAGE__=%s;</script><script>%s\nif(window.fit&&document.getElementById("win")){fit(0);tilt(0,0,0,0);}</script></body></html>'
            % (font_link, vars_, css, d.get('extra_css', ''), rig, scenes, icons,
               json.dumps({'aw': aw, 'ah': ah, 'ch': ch, 'fitScale': fit_scale, 'fitCy': fit_cy}), js))


def app_html(board):
    """The app page, with <base> so its relative files still load, and an optional script injected first (e.g. a fake backend)."""
    app = board.data['app']
    page = board.rel(app['page'])
    src = open(page, encoding='utf-8').read()
    base = '<base href="/%s/">' % os.path.relpath(os.path.dirname(page), board.dir).replace('\\', '/').strip('./')
    if base == '<base href="//">':
        base = '<base href="/">'
    inject = ''
    for f in ([app['inject']] if isinstance(app.get('inject'), str) else app.get('inject', [])):
        inject += '<script>\n%s\n</script>' % open(board.rel(f), encoding='utf-8').read()
    m = re.search(r'<head[^>]*>', src, re.I)
    head = (base + inject)
    return src[:m.end()] + head + src[m.end():] if m else head + src


# ------------------------------------------------------------------ the director
class Director:
    def __init__(self, board, page, sink, cdp, pace):
        self.b, self.p, self.sink, self.cdp, self.pace = board, page, sink, cdp, pace
        self.app = page.frame(name='app')
        self.vt = 0.0; self.t0 = None; self.frames = 0
        self.marks, self.cues = [], []
        self.vo = {}; self.vo_end = 0.0; self.vos = []; self.vo_pending = None; self.timed = []; self.cap_on = False
        self.capture = True

    # time
    def tick(self):
        dt = 1000.0 / RATE
        while self.timed and self.timed[0][0] <= self.vt:
            _, code, arg = self.timed.pop(0)
            self.js(code, arg)
        for f in self.p.frames:
            try:
                f.evaluate('dt => window.__step && window.__step(dt)', dt)
            except Exception:
                pass
        self.vt += dt
        if self.t0 is not None and not self.capture:
            self.t0 += dt                              # unfilmed time does not count
        if self.t0 is not None and self.capture:
            shot = self.cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 92})
            self.sink.write(base64.b64decode(shot['data']))
            self.frames += 1
            if self.frames % (RATE * 10) == 0:
                print('  [frames] %ds' % (self.frames // RATE), flush=True)

    def hold(self, ms):
        for _ in range(max(1, round(ms * RATE / 1000.0))):
            self.tick()

    def wait(self, ms):
        self.hold(ms * self.pace)

    def now(self):
        return (self.vt - self.t0) / 1000.0 if self.t0 is not None else 0.0

    def say(self, lid):
        """Start a voiceover line now (after the previous one has finished)."""
        if not lid or lid not in self.vo:
            return
        gap = self.vo[lid].get('gap')                     # silence between lines: the line's own, else voiceover.gap
        if gap is None: gap = self.vo.get('_gap', 0.45)
        if self.vo_end and self.now() < self.vo_end + gap:
            self.hold((self.vo_end + gap - self.now()) * 1000.0)
        self.vos.append([round(self.now(), 2), lid])
        self.vo_end = self.now() + self.vo[lid]['dur']
        if self.cap_on:                                   # captions are the spoken words, shown as they are spoken
            for sg in self.vo[lid].get('segs', []):
                self.cue('cap:' + sg['text'])
                self.timed.append((self.vt + sg['start'] * 1000.0, 't => cap(t)', sg['text']))
            self.timed.sort(key=lambda e: e[0])

    def finish_vo(self):
        if self.now() < self.vo_end:
            self.hold((self.vo_end - self.now()) * 1000.0 + 200)

    def mark(self, name):
        self.marks.append([name, round(self.now(), 2)]); print('  [scene] %s at %.1fs' % (name, self.now()), flush=True)

    def cue(self, kind):
        self.cues.append([round(self.now(), 2), kind])

    def js(self, code, arg=None):
        return self.p.evaluate(code, arg)

    # app helpers
    def rect(self, sel):
        r = self.app.evaluate("""s => { const e = document.querySelector(s); if (!e) return null;
            let r = e.getBoundingClientRect();
            if (r.width && (r.bottom < 0 || r.top > innerHeight)) { e.scrollIntoView({block: 'center', behavior: 'instant'}); r = e.getBoundingClientRect(); }
            return [r.x, r.y, r.width, r.height]; }""", sel)
        if not r or (r[2] == 0 and r[3] == 0):
            print('  ! selector not visible: %s (hidden by a tab, filter or overlay?) - camera move skipped' % sel)
            return None
        return r

    def focus(self, sel, scale=1.6, ms=1100, dx=0, dy=0, cy=None):
        r = self.rect(sel)
        if not r: return
        ms = ms * self.pace
        self.cue('zoom')
        self.js('([x,y,s,ms,cy]) => cam(x,y,s,ms,960,cy)', [r[0] + r[2] / 2 + dx, r[1] + r[3] / 2 + dy, scale, ms, cy])
        self.hold(ms)

    def point(self, sel, ms=700):
        r = self.rect(sel)
        if not r: return None
        x, y = r[0] + r[2] / 2, r[1] + r[3] / 2
        self.app.evaluate('([x,y,ms]) => window.__cursor(x,y,ms)', [x, y, ms * self.pace])
        self.wait(ms + 100)
        return x, y

    def click(self, sel, after=500):
        xy = self.point(sel)
        if xy is None: return
        self.cue('click:' + sel[:40])
        self.app.evaluate('([x,y]) => window.__ripple(x,y)', list(xy))
        self.app.evaluate('s => document.querySelector(s).click()', sel)
        self.wait(after)

    def step(self, s):
        if 'vo' in s: self.say(s['vo'])
        if 'caption' in s and (not self.vo or s.get('keep_caption')):
            if s['caption']: self.cue('cap:' + s['caption'])
            self.js('t => cap(t)', s['caption'] or None)
        if 'notify' in s:
            if s['notify']: self.cue('notify')
            self.js('d => note(d)', s['notify'] or None)
        if 'dim' in s: self.js('d => dim(d)', bool(s['dim']))
        if 'js' in s: self.app.evaluate('() => { %s }' % s['js'])
        if 'stage_js' in s: self.js('() => { %s }' % s['stage_js'])
        if 'tilt' in s:
            rx, ry, rz = (s['tilt'] + [0, 0, 0])[:3]
            self.js('([a,b,c,m]) => tilt(a,b,c,m)', [rx, ry, rz, s.get('ms', 1400) * self.pace])
        if 'select' in s:
            sel, val = s['select']
            self.point(sel, 600); self.cue('click')
            self.app.select_option(sel, val)
        if 'type' in s:
            sel, text = s['type']
            self.point(sel, 600)
            self.app.evaluate("""([s, t, ms]) => { const e = document.querySelector(s); e.focus(); e.value = ''; let i = 0;
                (function k(){ i++; e.value = t.slice(0, i); e.dispatchEvent(new Event('input', {bubbles: true})); if (i < t.length) setTimeout(k, ms); })(); }""",
                              [sel, text, 55])
            self.hold(len(text) * 55 + 200)
        if 'click' in s: self.click(s['click'], s.get('after', 500)); return
        if 'focus' in s:
            self.focus(s['focus'], s.get('scale', 1.6), s.get('ms', 1100), s.get('dx', 0), s.get('dy', 0), s.get('cy'))
        if 'fit' in s:
            self.js('ms => fit(ms)', s.get('ms', 1100) * self.pace); self.wait(s.get('ms', 1100))
        if 'scroll_to' in s:
            y = self.app.evaluate('([s,o]) => { const e = document.querySelector(s); return e ? e.getBoundingClientRect().top - o : 0; }',
                                  [s['scroll_to'], s.get('offset', 110)])
            self.app.evaluate('([dy,ms]) => { window.__scroll(dy,ms); }', [y, s.get('ms', 1200) * self.pace]); self.wait(s.get('ms', 1200) + 50)
        if 'scroll' in s:
            self.app.evaluate('([dy,ms]) => { window.__scroll(dy,ms); }', [s['scroll'], s.get('ms', 1200) * self.pace]); self.wait(s.get('ms', 1200) + 50)
        if 'scroll_el' in s:
            sel, dy = s['scroll_el'][:2]
            self.app.evaluate("""([s, dy, ms]) => { const el = document.querySelector(s), y0 = el.scrollTop, t0 = performance.now();
                (function k(t){ const p = Math.min((t - t0) / ms, 1), e = p < .5 ? 2*p*p : 1 - Math.pow(-2*p + 2, 2) / 2; el.scrollTop = y0 + dy * e; if (p < 1) requestAnimationFrame(k); })(t0); }""",
                              [sel, dy, s.get('ms', 1100) * self.pace]); self.wait(s.get('ms', 1100) + 50)
        if 'wait' in s: self.wait(s['wait'])
        if 'hold' in s: self.hold(s['hold'])
        if 'after' in s and 'click' not in s: self.wait(s['after'])

    # scenes
    def run_scene(self, i, sc):
        t = sc['type']
        if t != 'app': self.finish_vo()
        if t == 'phone':
            self.phone_prep(sc)
        self.mark('%d:%s' % (i, t))
        if getattr(self, 'flood', None):              # the previous scene flooded the frame: contract into this one
            fx, fy, fms = self.flood; self.flood = None
            self.js('() => { window.__instant = true; }')
            self.js('([x,y,m]) => setTimeout(() => floodOut(x,y,m), 60)', [fx, fy, fms])
        if sc.get('vo'): self.vo_pending = sc['vo']
        if sc.get('wipe'):
            self.js('() => stripeWipe()' if sc['wipe'] == 'stripe' else '() => arcWipe()'); self.cue('wipe'); self.hold(380)
        getattr(self, 'scene_' + t)(i, sc)
        self.vo_pending = None

    def scene_hook(self, i, sc):
        gap = sc.get('word_ms', 300)
        self.js("() => scene('s-hook', true)"); self.hold(300); self.say(sc.get('vo'))
        lines = [words_of(l) for l in sc['lines']]
        vo = self.vo.get(sc.get('vo')) or {}
        wl = vo.get('words') or []
        aligned = len(wl) == sum(len(w) for w in lines)
        t, idx = 250, 0
        for k, ws in enumerate(lines):
            if aligned:
                times = [wl[idx + j][1] * 1000 + 60 for j in range(len(ws))]; idx += len(ws)
                if k: self.js('ms => hookSwitch(ms)', max(0, times[0] - 350))
            else:
                if k:
                    self.js('ms => hookSwitch(ms)', t - 150); t += 250
                times = [t + j * gap for j in range(len(ws))]
            self.js('([id,w,t]) => typeTimed(id,w,t)', ['tw%d' % (k + 1), ws, times])
            t = times[-1] + sc.get('line_pause', 900)
        if len(lines) == 1:
            self.js("() => document.querySelectorAll('#s-hook .fl').forEach(e => e.classList.add('early'))")
        else:                                       # bring every line back so the whole question is on screen
            self.js('ms => setTimeout(hookStack, ms)', times[-1] + 500)
            t += sc.get('stack_hold', 900)
        if aligned: t = max(t - sc.get('line_pause', 900) + 500, vo.get('dur', 0) * 1000)
        self.hold(t + sc.get('hold', 900))
        self.js("() => scene('s-hook', false)"); self.hold(XFADE)

    def scene_reveal(self, i, sc):
        vo = self.vo.get(sc.get('vo')) or {}
        wl, segs = vo.get('words') or [], vo.get('segs') or []
        self.js("() => { scene('s-reveal', true); meet(true); }"); self.cue('scene'); self.say(sc.get('vo'))
        t_vo = self.vos[-1][0] if self.vos and sc.get('vo') in self.vo else None
        intro = sc.get('intro_ms', 1300)
        if t_vo is not None and len(wl) > 2:                      # the logo lands on the word after "Meet the"
            intro = max(500, wl[2][1] * 1000 - 450)
        self.hold(intro)
        self.js('() => meet(false)'); self.hold(250)
        self.js('() => logo(true)'); self.cue('scene')
        n = len(sc.get('pill', '').split(' ')) if sc.get('pill') else 0
        times = [950 + j * 150 for j in range(n)]
        if t_vo is not None and len(segs) > 1 and segs[1]['i1'] - segs[1]['i0'] + 1 == n:
            el = (self.now() - t_vo) * 1000
            times = [max(0, wl[segs[1]['i0'] + j][1] * 1000 - el) for j in range(n)]
        if n: self.js('t => pillTimed(t)', times)
        self.hold((times[-1] if n else 900) + sc.get('hold', 1600))
        self.js("() => scene('s-reveal', false)"); self.hold(XFADE)

    def _simple(self, i, sc, default):
        sid = 's%d' % i
        self.js('s => scene(s, true)', sid); self.cue('scene')
        t0 = self.now(); self.say(sc.get('vo'))
        self.hold(max(sc.get('duration', default), ((self.vo_end - t0) * 1000 + 500) if sc.get('vo') in self.vo else 0))
        if not getattr(self, 'last', False):        # the closing card stays up; mix.py fades it out
            self.js('s => scene(s, false)', sid); self.hold(XFADE)

    def scene_pages(self, i, sc): self._simple(i, sc, 7600)
    def scene_quote(self, i, sc): self._simple(i, sc, 5600)
    def scene_statement(self, i, sc): self._simple(i, sc, 5600)
    def scene_cards(self, i, sc): self._simple(i, sc, 7600)

    def scene_inset(self, i, sc): self._simple(i, sc, 4200)

    def scene_clip(self, i, sc):
        """A pre-rendered Remotion clip, one source frame per video frame (both 30 fps)."""
        sid = 's%d' % i
        self.js('s => scene(s, true)', sid); self.cue('scene')
        self.say(sc.get('vo'))
        for f in clip_frames(self.b, sc):
            self.js('([id, u]) => { const im = document.getElementById(id); im.src = u; return im.decode(); }', [sid + '-img', web(self.b, f)])
            self.tick()
        if sc.get('vo') in self.vo and self.now() < self.vo_end:   # last frame holds while the line finishes
            self.hold((self.vo_end - self.now()) * 1000 + 500)
        self.hold(sc.get('hold', 0))
        if not getattr(self, 'last', False):
            self.js('s => scene(s, false)', sid); self.hold(650)

    def scene_prompt(self, i, sc):
        sid, ms = 's%d' % i, sc.get('char_ms', 42)
        self.js('s => scene(s, true)', sid); self.cue('scene'); self.hold(700)
        send = len(sc['text']) * ms + sc.get('pause', 700)
        self.js('([s,t,m,a]) => promptType(s,t,m,a)', [sid, sc['text'], ms, send])
        self.hold(send + 1100)
        self.js('s => scene(s, false)', sid); self.hold(300)

    def scene_beats(self, i, sc):
        sid, gap = 's%d' % i, sc.get('word_ms', 650)
        ids = sc.get('vos')
        if ids and all(x in self.vo for x in ids):          # one spoken line per beat, with a pause between them
            self.js('s => scene(s, true)', sid); self.cue('scene')
            self.finish_vo()
            t, cur, starts = self.now(), 0.0, []
            for x in ids:
                starts.append(cur); self.vos.append([round(t + cur, 2), x]); cur += self.vo[x]['dur'] + sc.get('pause_ms', 800) / 1000.0
            self.vo_end = t + cur - sc.get('pause_ms', 800) / 1000.0
            self.js('([s,t]) => beatsTimed(s,t)', [sid, [x * 1000 + 40 for x in starts]])
            self.hold((cur - sc.get('pause_ms', 800) / 1000.0) * 1000 + sc.get('hold', 900))
            if not getattr(self, 'last', False):
                self.js('s => scene(s, false)', sid); self.hold(450)
            return
        self.js('s => scene(s, true)', sid); self.cue('scene'); self.say(sc.get('vo'))
        times = [j * gap for j in range(len(sc['words']))]
        sg = (self.vo.get(sc.get('vo')) or {}).get('segs') or []
        if len(sg) == len(sc['words']): times = [x['start'] * 1000 + 40 for x in sg]
        self.js('([s,t]) => beatsTimed(s,t)', [sid, times])
        self.hold(times[-1] + sc.get('hold', 900))
        if not getattr(self, 'last', False):
            self.js('s => scene(s, false)', sid); self.hold(XFADE)

    def scene_motion(self, i, sc):
        """A designed world (HTML) under its own camera; "events" fire at fixed ms from the scene start."""
        sid = 's%d' % i
        self.js('([s,k]) => mcam(s,k)', [sid, dict(sc.get('start', {}), ms=0)])
        self.js('s => scene(s, true)', sid); self.cue('scene')
        t = 0
        for ev in sorted(sc.get('events', []), key=lambda e: e.get('at', 0)):
            if ev.get('at', 0) > t:
                self.hold(ev['at'] - t); t = ev['at']
            self.motion_event(sid, ev)
        end = sc.get('duration', t + 1500)
        if end > t: self.hold(end - t)
        self.js('() => cap(null)')
        if getattr(self, 'last', False):
            return
        if isinstance(sc.get('exit'), dict) and sc['exit'].get('flood'):
            # flood: a shape grows from a point (or an element) to cover the frame, then contracts into the next scene
            f = sc['exit']; ms = f.get('ms', 420)
            x, y = (960, 540) if isinstance(f.get('from'), str) else f.get('from', [960, 540])
            if isinstance(f.get('from'), str):
                p = self.js('([s,q]) => { const sc = document.getElementById(s), el = sc.querySelector(q); if (!el) return null; const r = el.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; }', [sid, f['from']])
                x, y = p or (960, 540)
            self.cue('flood'); self.js('([x,y,c,m]) => floodIn(x,y,c,m)', [x, y, f['flood'], ms]); self.hold(ms + 60)
            self.js('s => { const e = document.getElementById(s); e.style.transition = "none"; e.classList.remove("on"); }', sid)
            to = f.get('to', [960, 540]); self.flood = (to[0], to[1], f.get('out_ms', 520))
            return
        if sc.get('exit') == 'dive':                 # the camera flies into the frame and the next scene comes up behind it
            self.js('s => { const e = document.getElementById(s); e.style.transformOrigin = "960px 540px"; e.classList.add("dive"); }', sid); self.hold(700)
            self.js('s => { const e = document.getElementById(s); e.classList.remove("on", "dive"); }', sid)
        else:
            self.js('s => scene(s, false)', sid); self.hold(XFADE)

    def motion_event(self, sid, ev):
        if 'cam' in ev:
            self.cue('zoom'); self.js('([s,k]) => mcam(s,k)', [sid, ev['cam']])
        if 'show' in ev: self.js('([s,q,c]) => mcls(s,q,c,true)', [sid, ev['show'], ev.get('cls', 'in')])
        if 'hide' in ev: self.js('([s,q,c]) => mcls(s,q,c,false)', [sid, ev['hide'], ev.get('cls', 'in')])
        if 'stagger' in ev: self.js('([s,q,g,c]) => mstagger(s,q,g,c)', [sid, ev['stagger'], ev.get('gap', 140), ev.get('cls', 'in')])
        if 'words' in ev: self.js('([s,q,g]) => mwords(s,q,g)', [sid, ev['words'], ev.get('gap', 140)])
        if 'style' in ev:
            q, prop, val = ev['style']; self.js('([s,q,p,v,m]) => mstyle(s,q,p,v,m)', [sid, q, prop, val, ev.get('ms', 1200)])
        if 'count' in ev:
            q, to = ev['count']
            self.js('([s,q,t,m,a,b,d]) => mcount(s,q,t,m,a,b,d)', [sid, q, to, ev.get('ms', 1600), ev.get('pre', ''), ev.get('suf', ''), ev.get('dec', 0)])
        if 'caption' in ev:
            if ev['caption']: self.cue('cap:' + ev['caption'])
            self.js('t => cap(t)', ev['caption'] or None)
        if 'click' in ev:
            self.js('([s,q,m]) => mclick(s,q,m)', [sid, ev['click'], ev.get('ms', 700)])
            self.cues.append([round(self.now() + ev.get('ms', 700) / 1000.0, 2), 'click'])
        if 'move' in ev:                               # a character travels: {"move": ".guide", "to": [x, y], "ms": 1600}
            self.js('([s,q,x,y,m]) => mmove(s,q,x,y,m)', [sid, ev['move'], ev['to'][0], ev['to'][1], ev.get('ms', 1600)])
        if 'morph' in ev: self.js('([s,q,t,m]) => morph(s,q,t,m)', [sid, ev['morph'], ev.get('to', {}), ev.get('ms', 700)])
        if 'stage_js' in ev: self.js('() => { %s }' % ev['stage_js'])
        if 'cue' in ev: self.cue(ev['cue'])

    def scene_endcard(self, i, sc): self._simple(i, sc, 5200)
    def scene_float(self, i, sc): self._simple(i, sc, 4200)

    def scene_pill(self, i, sc):
        sid = 's%d' % i
        self.js('s => scene(s, true)', sid); self.cue('scene'); self.hold(sc.get('hold', 700))
        self.js('s => gpClick(s)', sid); self.cue('click'); self.hold(2000)
        self.js('s => scene(s, false)', sid); self.hold(60)

    def phone_prep(self, sc):
        """Reload the phone's copy of the app (it picks up the team and role chosen earlier), seed it, scroll it. Not filmed."""
        ph = self.p.frame(name='phone')
        if not ph: return
        self.capture = False
        ph.evaluate('() => location.reload()')
        ready = sc.get('ready', self.b.data['app'].get('ready', "document.readyState === 'complete'"))
        for _ in range(600):
            self.tick()
            try:
                if ph.is_detached(): ph = self.p.frame(name='phone')
                if ph and ph.evaluate('() => !!(%s)' % ready): break
            except Exception:
                ph = self.p.frame(name='phone')
        def run(code, arg=None):                         # self-unpacking pages may navigate once more: retry on a fresh frame
            nonlocal ph
            for _ in range(5):
                try:
                    return ph.evaluate(code, arg)
                except Exception:
                    self.hold(500); ph = self.p.frame(name='phone')
                    for _ in range(300):
                        self.tick()
                        try:
                            if ph and ph.evaluate('() => !!(%s)' % ready): break
                        except Exception:
                            ph = self.p.frame(name='phone')
            print('  ! phone step failed: %s' % code[:80])
        self.hold(800)
        js = self.b.data['app'].get('setup_js')
        if js: run('() => { %s }' % js)
        for code in sc.get('setup', []):                 # one step at a time, with a few frames between (buttons enable, panels open)
            run('() => { %s }' % code); self.hold(400)
        if sc.get('scroll_to'):
            run("""s => { const e = document.querySelector(s); if (e) e.scrollIntoView({block: 'center', behavior: 'instant'}); }""", sc['scroll_to'])
        self.hold(300)
        self.capture = True
        self.ph = ph

    def scene_phone(self, i, sc):
        sid = 's%d' % i
        self.js('v => setBg(v)', sc.get('stage_bg') or None)
        self.js('s => scene(s, true)', sid); self.cue('scene'); self.hold(1500)
        self.js('s => phoneTurn(s)', sid)
        for s in sc.get('steps', []):
            if 'caption' in s:
                if s['caption']: self.cue('cap:' + s['caption'])
                self.js('t => cap(t)', s['caption'] or None)
            if 'tap' in s:
                self.cue('click')
                self.ph.evaluate("""s => { const e = document.querySelector(s); if (!e) return; const r = e.getBoundingClientRect(), d = document.createElement('div');
                    d.style.cssText = 'position:fixed;left:' + (r.x + r.width / 2 - 32) + 'px;top:' + (r.y + r.height / 2 - 32) + 'px;width:64px;height:64px;border-radius:50%;background:rgba(8,117,225,.35);z-index:99999;pointer-events:none;transform:scale(.3);transition:transform .5s,opacity .6s';
                    document.body.appendChild(d); requestAnimationFrame(() => { d.style.transform = 'scale(1.5)'; d.style.opacity = '0'; }); setTimeout(() => d.remove(), 800); e.click(); }""", s['tap'])
            if 'js' in s: self.ph.evaluate('() => { %s }' % s['js'])
            if 'wait' in s: self.wait(s['wait'])
        self.js('() => cap(null)')
        if not getattr(self, 'last', False):
            self.js('s => scene(s, false)', sid); self.hold(XFADE)

    def scene_chat(self, i, sc):
        sid = 's%d' % i
        self.js('s => scene(s, true)', sid); self.cue('scene')
        times, t = [], 700
        for m in sc['messages']:
            times.append(t); t += m.get('wait', 600 if 'divider' in m else 1500)
        self.js('([s,t]) => chatTimed(s,t)', [sid, times])
        self.hold(t + sc.get('hold', 300))
        if any(m.get('card') for m in sc['messages']) and sc.get('click', True):
            self.js('s => chatClick(s)', sid); self.cue('click'); self.hold(2300)
            self.js('s => scene(s, false)', sid); self.hold(100)
        else:
            self.js('s => scene(s, false)', sid); self.hold(XFADE)

    def scene_device(self, i, sc):
        sid = 's%d' % i
        self.js('s => scene(s, true)', sid); self.cue('scene')
        self.hold(sc.get('hold', 1900))
        if sc.get('push', True):
            self.js('s => devPush(s)', sid); self.hold(1500)
            self.js('s => scene(s, false)', sid); self.hold(80)
        else:
            self.js('s => scene(s, false)', sid); self.hold(XFADE)

    def scene_app(self, i, sc):
        self.cap_on = True
        enter = sc.get('enter', 'flyin')
        self.js('v => setBg(v)', scene_bg(self.b.data, i, sc) or None)
        if isinstance(enter, dict) and enter.get('macro'):          # start on an extreme close-up, tilted
            m = enter['macro']
            tx = m.get('tilt', [34, -28, 6])
            self.js('([a,b,c]) => tilt(a,b,c,0)', tx)
            r = self.rect(m['selector'])
            if r: self.js('([x,y,s]) => cam(x,y,s,0,960,520)', [r[0] + r[2] / 2, r[1] + r[3] / 2, m.get('scale', 3.0)])
            self.js('() => rig(true)'); self.hold(500)
        elif enter == 'zoomout':
            self.js('() => { tilt(0,0,0,0); cam(%d,%d,%.4f,0,960,540); }' % (self.aw / 2, self.ah / 2, 1990.0 / self.aw))
            self.cue('app_in'); self.js('() => rig(true)'); self.hold(250)
            self.js('() => fit(1500)'); self.hold(1500)
        elif enter == 'flyin':
            self.js('() => { tilt(18,-16,2,0); cam(%d,%d,0.7,0,960,520); }' % (self.aw / 2, self.ah / 2))
            self.cue('app_in'); self.js('() => rig(true)'); self.hold(60)
            self.js('() => tilt(0,0,0,1600)'); self.js('() => fit(1600)'); self.hold(1600)
        else:
            self.js('() => { tilt(0,0,0,0); fit(0); rig(true); }'); self.cue('app_in'); self.hold(800)
        for s in sc.get('steps', []):
            self.step(s)
        self.js('() => cap(null)'); self.js('() => note(null)')
        exit_ = sc.get('exit', 'flyout')
        if exit_ == 'flyout':
            self.cue('flyout')
            self.js('() => { tilt(14,-22,3,1300); cam(%d,%d,0.55,1300,1280,560); }' % (self.aw / 2, self.ah / 2)); self.wait(700)
            self.js('() => rig(false)'); self.wait(700)
        elif exit_ == 'fade':
            self.js('() => rig(false)'); self.hold(800)
        self.js("() => { dim(false); }")
        self.finish_vo(); self.cap_on = False


def serve(root):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    handler.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def launch(pw):
    for kw in ({'channel': 'msedge'}, {'channel': 'chrome'}, {}):
        try:
            return pw.chromium.launch(**kw)
        except Exception:
            continue
    raise SystemExit('No browser found: install Edge or Chrome, or run "python -m playwright install chromium".')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('storyboard')
    ap.add_argument('--until', type=int, help='render scenes 0..N only (preview)')
    a = ap.parse_args()
    check_deps()
    from playwright.sync_api import sync_playwright
    board = Board(a.storyboard)
    d = board.data
    if not d.get('auto_bg') and not any(sc.get('bg') for sc in d['scenes']):
        print('  tip: every scene uses the default background. Set "bg" per scene, or "auto_bg": true, so the look follows the story.')
    with open(os.path.join(board.out, 'stage.html'), 'w', encoding='utf-8') as f:
        f.write(stage_html(board))
    if d.get('app'):
        with open(os.path.join(board.out, 'app.html'), 'w', encoding='utf-8') as f:
            f.write(app_html(board))
    srv = serve(board.dir)
    rel_out = os.path.relpath(board.out, board.dir).replace('\\', '/')
    frames_mp4 = os.path.join(board.out, 'frames.mp4')
    # "motion_blur": N renders N subframes per frame and averages them (real motion blur on fast camera moves)
    global RATE
    sub = max(1, int(d.get('motion_blur', 1)))
    RATE = FPS * sub
    blur = ['-vf', 'tmix=frames=%d,fps=%d' % (sub, FPS)] if sub > 1 else []
    enc = subprocess.Popen([ffmpeg(), '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(RATE), '-c:v', 'mjpeg', '-i', '-'] + blur + [
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', frames_mp4], stdin=subprocess.PIPE)
    clock = open(os.path.join(STAGE, 'clock.js'), encoding='utf-8').read()
    started = time.time()
    with sync_playwright() as pw:
        browser = launch(pw)
        ctx = browser.new_context(viewport={'width': 1920, 'height': 1080})
        ctx.add_init_script('window.__FAKE_DATE__=%s;\n%s' % (json.dumps((d.get('app') or {}).get('fake_date')), clock))
        page = ctx.new_page()
        page.goto('http://127.0.0.1:%d/%s/stage.html' % (srv.server_address[1], rel_out))
        page.wait_for_load_state('load')
        page.evaluate('document.fonts.ready')
        dr = Director(board, page, enc.stdin, ctx.new_cdp_session(page), float(d.get('pace', 0.82)))
        dr.vo = board.json_in('voice_manifest.json') or {}
        if d.get('voiceover') and not dr.vo: print('  ! voiceover declared but no out/voice_manifest.json: run voice.py first')
        if d.get('app'):
            dr.aw, dr.ah = d['app'].get('viewport', [1440, 900])
            ready = d['app'].get('ready', "document.readyState === 'complete'")
            for _ in range(900):                       # step the frozen clock until the app says it is ready
                dr.tick()
                if dr.app.evaluate('() => !!(%s)' % ready):
                    break
            else:
                print('  ! app never became ready (%s)' % ready)
            if d['app'].get('setup_js'):
                dr.app.evaluate('() => { %s }' % d['app']['setup_js'])
            dr.hold(400)
        dr.t0 = dr.vt
        for i, sc in enumerate(d['scenes']):
            if a.until is not None and i > a.until:
                break
            dr.last = i == len(d['scenes']) - 1
            dr.run_scene(i, sc)
        dr.finish_vo()
        dr.hold(int(d.get('end_hold', 1200)))
        dr.mark('end')
        ctx.close(); browser.close()
    enc.stdin.close(); enc.wait(); srv.shutdown()
    board.json_out('cues.json', {'length': round(dr.frames / RATE, 2), 'fps': FPS, 'marks': dr.marks, 'cues': dr.cues, 'vos': dr.vos,
                                 'preview': a.until is not None})
    print('wrote %s  (%.1fs, %d frames, rendered in %.0fs)' % (frames_mp4, dr.frames / RATE, dr.frames, time.time() - started))


if __name__ == '__main__':
    main()
