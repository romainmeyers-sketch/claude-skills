"""One continuous world instead of slides: the eight scenes become stations side by side, a 3D Lumen copilot
walks from station to station and the camera travels with it. Reads storyboard.json (made by make_storyboard.py)
and the scene HTML, writes assets/scenes/journey.html and storyboard_journey.json."""
import copy, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SC = os.path.join(HERE, 'assets', 'scenes')
WX = 2200                        # station spacing: a little gap of plain teal between pages, so the travel reads
TRAVEL = 1700                    # ms to walk from one station to the next

base = json.load(open(os.path.join(HERE, 'storyboard.json'), encoding='utf-8'))
stations = base['scenes']

# where the guide stands at each station (station coordinates), its size there, and what it says on arrival
GUIDE = [((220, 760), 'Hi, I am a Lumen copilot. Follow me.'),
         ((1520, 640), ''),
         ((1650, 640), ''),
         ((150, 800), ''),
         ((1745, 520), ''),
         ((1745, 40), 'Teams change first.'),
         ((1690, 40), ''),
         ((865, 715), '')]
GS = 150                          # guide size (px wide)

css = None
parts = []
for i, sc in enumerate(stations):
    html = open(os.path.join(HERE, sc['html']), encoding='utf-8').read()
    m = re.match(r'\s*(<style>.*?</style>)', html, re.S)
    if m:
        css = css or m.group(1); html = html[m.end():]
    bg = sc.get('bg')
    style = 'left:%dpx;top:0;width:1920px;height:1080px;' % (i * WX)
    cls = 'station st%d' % i
    if bg == 'white':
        style += 'background:#fff;'; cls += ' light'
    elif bg and bg.endswith('.png'):
        style += 'background:url(%s) center/cover;' % bg
    if i == len(stations) - 1:                          # finale: the five agents join the guide
        for k, (acc, x) in enumerate([('glasses', 470), ('hardhat', 640), ('headset', 1110), ('tie', 1280), ('glasses tie', 1450)]):
            html += ('<mascot class="fin drop" kind="bot" color="#36C6C6" size="120" acc="%s" style="left:%dpx;top:745px;'
                     '--eyec:#B2FFF6;--ant:#B2FFF6;--hat:#B2FFF6;--tie:#0F3133"></mascot>' % (acc, x))
    parts.append('<div class="%s" style="position:absolute;%s">%s</div>' % (cls, style, html))

# the guide and its speech bubbles live in the world, outside the stations
gx, gy = GUIDE[0][0]
guide = ('<mascot class="guide drop" kind="bot" color="#36C6C6" size="%d" acc="" name="" '
         'style="left:%dpx;top:%dpx;z-index:6;--eyec:#B2FFF6;--ant:#B2FFF6"></mascot>' % (GS, gx, gy))
bubbles = ''
for i, ((x, y), line) in enumerate(GUIDE):
    if line:
        bx = i * WX + x
        right = x > 900
        below = y < 200                                # a guide near the top talks below itself
        bubbles += ('<div class="bubble%s in-p gb%d" style="%s;top:%dpx;z-index:7;font-size:36px;white-space:nowrap%s">%s</div>'
                    % (' r' if right else '', i, ('left:%dpx' % (bx - 420)) if right else ('left:%dpx' % (bx + 120)),
                       y + 200 if below else y - 100, ';transform-origin:80% 0' if below else '', line))
extra = '<style>.light .kin b{color:#0F3133}.station .rule{z-index:1}</style>'
open(os.path.join(SC, 'journey.html'), 'w', encoding='utf-8').write((css or '') + extra + ''.join(parts) + guide + bubbles)


def pre(sel, i):
    return '.st%d %s' % (i, sel)


def shift(ev, i, t0):
    e = copy.deepcopy(ev)
    e['at'] = t0 + e.get('at', 0)
    for k in ('show', 'hide', 'stagger', 'words', 'morph', 'click'):
        if k in e:
            e[k] = pre(e[k], i)
    for k in ('style', 'count'):
        if k in e:
            e[k][0] = pre(e[k][0], i)
    if 'cam' in e:
        c = e['cam']
        if c.get('focus'):
            c['focus'] = pre(c['focus'], i)
            if 'x' in c:
                c['x'] += i * WX
        else:
            c['x'] = c.get('x', 960) + i * WX
    return e


events, t = [], 0
events.append({"at": 200, "show": ".guide"})
for i, sc in enumerate(stations):
    X = i * WX
    if i:                                               # travel: camera eases out, follows the guide, settles in
        (x, y), _ = GUIDE[i]
        events.append({"at": t, "hide": ".gb%d" % (i - 1)})
        events.append({"at": t, "move": ".guide", "to": [X + x, y], "ms": TRAVEL})
        events.append({"at": t, "cam": {"x": X - WX / 2 + 960, "y": 560, "s": 0.82, "ms": TRAVEL // 2, "ease": "inout", "rx": 0, "ry": 0, "rz": 0}})
        events.append({"at": t + TRAVEL // 2, "cam": {"x": X + 960, "y": 540, "s": 1, "ms": TRAVEL // 2, "ease": "spring-soft"}})
        events.append({"at": t, "cue": "travel"})
        t += TRAVEL
    st = sc.get('start') or {}
    if st and (st.get('s', 1) != 1 or st.get('rx') or st.get('ry')):  # the station's own opening framing
        c = dict(st, ms=600, ease='spring-soft')
        if c.get('focus'):
            c['focus'] = pre(c['focus'], i)
        else:
            c['x'] = c.get('x', 960) + X
        events.append({"at": t, "cam": c})
    if GUIDE[i][1]:
        events.append({"at": t + 300, "show": ".gb%d" % i})
        events.append({"at": t + 300, "show": ".guide", "cls": "talk"})
        events.append({"at": t + 1800, "hide": ".guide", "cls": "talk"})
    events.append({"at": t + 400, "show": ".guide", "cls": "happy" if i % 2 == 0 else "look-l"})
    events.append({"at": t + 2400, "hide": ".guide", "cls": "happy" if i % 2 == 0 else "look-l"})
    for ev in sc.get('events', []):
        events.append(shift(ev, i, t))
    t += sc['duration']
# finale: the guide waves
events.append({"at": t - 3800, "stagger": ".st7 .fin", "gap": 180})
events.append({"at": t - 2600, "show": ".guide", "cls": "waving"})
events.append({"at": t - 2600, "show": ".st7 .fin", "cls": "happy"})
events.sort(key=lambda e: e['at'])

sb = {k: v for k, v in base.items() if k != 'scenes'}
sb['output_name'] = 'lumen-pom-ai-journey'
sb['scenes'] = [{"type": "motion", "html": "assets/scenes/journey.html", "duration": t,
                 "start": {"x": 960, "y": 540, "s": 1.06}, "events": events}]
json.dump(sb, open(os.path.join(HERE, 'storyboard_journey.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('journey: %d stations, %d events, %.0f s' % (len(stations), len(events), t / 1000))
