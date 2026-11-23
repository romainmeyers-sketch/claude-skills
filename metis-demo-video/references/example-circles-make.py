"""Lumen POM AI video, version 2: circles, 3D orbs and varied transitions instead of slide-like pages.
One world, eight stations; a 3D Lumen copilot travels; transitions alternate between portals (the camera dives into
an orb), floods (a circle fills the frame) and walks. Same content and numbers as v1 (POM AI Scenario Summary v6).
Writes assets/scenes/journey_v2.html and storyboard_v2.json."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
WX = 2200
TEAL, MINT, TEAL2, OFF = '#0F3133', '#B2FFF6', '#36C6C6', '#F2F0F1'
SRC = 'Source: Metis Strategy Research &amp; Analysis; Metis AI Productivity Assessment (Aug 2025). Modeled potentials, not targets.'
C = 2 * math.pi


def I(n):
    return '<i data-lucide="%s"></i>' % n


def bot(cls, size, x, y, acc='', z=5):
    """A 3D Lumen bot whose CENTRE is at (x, y)."""
    return ('<mascot class="%s" kind="bot" color="#36C6C6" size="%d" acc="%s" style="left:%dpx;top:%dpx;z-index:%d;'
            '--eyec:#B2FFF6;--ant:#B2FFF6;--hat:#B2FFF6;--tie:#0F3133"></mascot>' % (cls, size, acc, x - size // 2, y - int(size * .62), z))


def orb(cls, size, x, y, kind='', inner='', extra=''):
    """A glossy 3D orb centred at (x, y)."""
    return ('<div class="orb %s %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s"><div class="oi">%s</div></div>'
            % (kind, cls, x - size // 2, y - size // 2, size, size, extra, inner))


def donut(cls, x, y, r, sw, arcs, inner=''):
    """SVG ring centred at (x, y); arcs = [(name, colour, start_fraction)] drawn later by style events."""
    box = 2 * r + sw + 8
    c = box / 2
    circ = C * r
    s = ('<div class="dn in-s %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><svg width="%d" height="%d">'
         '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="rgba(128,128,128,.18)" stroke-width="%d"/>'
         % (cls, x - c, y - c, box, box, box, box, c, c, r, sw))
    for name, col, start in arcs:
        s += ('<circle class="%s" cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="%d" stroke-dasharray="%.1f" '
              'stroke-dashoffset="%.1f" transform="rotate(%.1f %.1f %.1f)" style="transition-property:stroke-dashoffset;'
              'transition-timing-function:cubic-bezier(.45,0,.25,1)"/>'
              % (name, c, c, r, col, sw, circ, circ, -90 + 360 * start, c, c))
    return s + '</svg><div class="dni">%s</div></div>' % inner


CSS = '''<style>
.rule{position:absolute;left:0;top:0;width:16px;height:1080px;background:#B2FFF6}
.eb{position:absolute;font-size:32px;font-weight:600;color:#B2FFF6}
.light .eb{color:#0F3133}
.h1{position:absolute;font-size:60px;font-weight:600;line-height:1.12;color:#fff}
.light .h1{color:#000}
.h1 b,.kin b{color:#B2FFF6}.light .h1 b,.light .kin b{color:#0F3133}
.src{position:absolute;left:110px;bottom:30px;font-size:20px;color:#CFD3D9}
.light .src{color:#555}
.wm{position:absolute;right:90px;bottom:60px;height:46px}
.orb{position:absolute;border-radius:50%;
  background:radial-gradient(circle at 34% 28%,#F4FFFD 0%,#B2FFF6 11%,#36C6C6 44%,#17696B 76%,#0A3436 100%);
  box-shadow:inset -18px -26px 50px rgba(0,0,0,.3),0 40px 70px -30px rgba(0,0,0,.55)}
.orb.glass{background:radial-gradient(circle at 34% 28%,#5FB3B1 0%,#25605F 26%,#0F3133 64%,#061A1B 100%)}
.orb.pearl{background:radial-gradient(circle at 34% 28%,#fff 0%,#F2F0F1 38%,#CFD3D9 80%,#A6AEB8 100%);box-shadow:inset -14px -20px 40px rgba(0,0,0,.18),0 30px 60px -28px rgba(0,0,0,.35)}
.orb .oi{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#0F3133}
.orb.glass .oi{color:#fff}
.fo{animation:ofl 6s ease-in-out infinite alternate}
.fo:nth-child(2n){animation-duration:7.5s}.fo:nth-child(3n){animation-duration:5s}
@keyframes ofl{from{translate:0 0}to{translate:0 -22px}}
.ring{position:absolute;width:0;height:0;animation:spin 70s linear infinite}
.ring.rev{animation-duration:110s;animation-direction:reverse}
@keyframes spin{to{rotate:360deg}}
.dot{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:#B2FFF6}
.pc{position:absolute;width:92px;height:92px;margin:-46px 0 0 -46px;border-radius:50%;display:grid;place-items:center;font-size:40px;color:#B2FFF6;
  background:radial-gradient(circle at 34% 28%,#5FB3B1 0%,#25605F 30%,#0F3133 70%,#061A1B 100%);box-shadow:0 18px 30px -16px rgba(0,0,0,.5)}
.pc.sm{width:60px;height:60px;margin:-30px 0 0 -30px;font-size:26px}
.rl{position:absolute;width:240px;margin-left:-120px;text-align:center;font-size:24px;font-weight:600;color:#0F3133}
.cl{position:absolute;width:260px;margin-left:-130px;text-align:center;font-size:22px;font-weight:700;color:#0F3133}
.an{position:absolute;width:260px;margin-left:-130px;text-align:center;color:#fff}
.an b{display:block;font-size:28px}.an span{display:block;font-size:21px;color:#CFD3D9;margin-top:2px}
.dn{position:absolute}
.dn .dni{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.lab{position:absolute;width:420px;margin-left:-210px;text-align:center}
.lab b{display:block;font-size:34px;color:#fff}.lab span{display:block;font-size:26px;color:#CFD3D9}
.lab i.m{display:block;font-style:normal;font-size:26px;color:#B2FFF6;margin-top:10px}
.light .lab b{color:#000}.light .lab span{color:#444}
.stl{position:absolute;color:#fff}.stl b{font-size:72px;color:#B2FFF6;font-weight:600;margin-right:16px}.stl span{font-size:32px}
</style>'''


def station(i, inner, bg=None, light=False):
    st = 'left:%dpx;top:0;width:1920px;height:1080px;' % (i * WX)
    if bg == 'white':
        st += 'background:#fff;'
    elif bg == 'pattern':
        st += 'background:url(assets/pattern.png) center/cover;'
    return '<div class="station st%d%s" style="position:absolute;%s">%s</div>' % (i, ' light' if light else '', st, inner)


WM = '<img class="wm" src="assets/lumen-wordmark-white.png" alt="Lumen">'
S = []

# 0. hook: floating orbs, the question, a portal orb
h = '<div class="rule"></div>'
for k, (sz, x, y, kind) in enumerate([(240, 1560, 170, ''), (130, 260, 170, 'glass'), (90, 1700, 860, ''), (170, 640, 880, 'glass'), (60, 980, 150, '')]):
    h += orb('fo in-s f%d' % k, sz, x, y, kind)
h += orb('fo in-s port', 210, 1380, 800, '')
h += ('<div class="kin split mask k1" style="top:360px;font-size:84px;color:#fff">What happens to the product operating model</div>'
      '<div class="kin split mask k2" style="top:480px;font-size:84px;color:#fff">when every team works with <b>AI</b>?</div>' + WM)
S.append(station(0, h, 'pattern'))

# 1. today: the POM as a 3D core with orbiting value streams and a ring of 213 team dots
cx, cy = 1250, 560
h = ('<div class="rule"></div><div class="eb in-o e1" style="left:110px;top:110px">Today</div>'
     '<div class="h1 split mask k1" style="left:110px;top:160px;width:720px">Lumen\'s product operating model</div>')
h += ('<div class="stl in-o sr" style="left:110px;top:380px"><b>11</b><span>value streams</span></div>'
      '<div class="stl in-o sr" style="left:110px;top:480px"><b>43</b><span>ARTs</span></div>'
      '<div class="stl in-o sr" style="left:110px;top:580px"><b>213</b><span>agile teams</span></div>')
h += '<div class="ring" style="left:%dpx;top:%dpx">' % (cx, cy)
for k in range(11):
    a = -math.pi / 2 + C * k / 11
    h += orb('in-s vs', 84, int(290 * math.cos(a)), int(290 * math.sin(a)), 'glass' if k % 2 else '')
h += '</div><div class="ring rev" style="left:%dpx;top:%dpx">' % (cx, cy)
for k in range(213):
    a = C * k / 213
    rr = 400 + (k * 37 % 5) * 14
    h += '<div class="dot in-s" style="left:%dpx;top:%dpx"></div>' % (int(rr * math.cos(a)), int(rr * math.sin(a)))
h += '</div>' + orb('in-s core', 330, cx, cy, '', '<b class="n0" style="font-size:84px;line-height:1">0</b><span style="font-size:28px">FTE today</span>')
h += ('<div class="kin split mask k2" style="top:830px;left:110px;right:auto;width:640px;text-align:left;font-size:40px;color:#F2F0F1">'
      'Work is done by hand. AI use is individual and ad hoc.</div><div class="src">' + SRC + '</div>')
S.append(station(1, h))

# 2. one agile team as a ring of people; copilots arrive (light)
cx, cy, R = 1150, 560, 300
slots = {0: 'Product owner', 3: 'Tech lead', 7: 'QA', 10: 'DevOps', 12: 'Agile coach'}
copl = {0: 'Backlog copilot', 3: 'Design and review copilot', 5: 'Coding copilot', 7: 'Testing copilot', 12: 'Reporting copilot'}
h = ('<div class="eb morph ebm" style="left:110px;top:96px;height:44px;width:0;justify-content:start"></div>'
     '<div class="h1 split mask k1" style="left:110px;top:150px;width:700px">One agile team</div>')
for k in range(15):
    a = math.radians(-90 + 24 * k)
    x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    nm = slots.get(k)
    small = nm in ('DevOps', 'Agile coach')
    h += '<div class="pc in-s%s" style="left:%dpx;top:%dpx">%s</div>' % (' sm' if small else '', x, y, I('user'))
    if nm or k == 5:
        lab = nm or 'Engineers &times;10'
        lab += ' 1.5' if nm == 'QA' else (' 0.2' if small else '')
        ca = math.cos(a)
        if ca > 0.3:                                   # right side: text starts just right of the circle
            pos = 'left:%dpx;margin-left:0;text-align:left' % (x + 62)
        elif ca < -0.3:                                # left side: text ends just left of the circle
            pos = 'left:%dpx;margin-left:0;text-align:right' % (x - 62 - 260)
        else:                                          # top and bottom: centred above or below
            pos = 'left:%dpx' % (cx + (R + 95) * ca)
        ly = (y - 16) if abs(ca) > 0.3 else (cy + (R + 95) * math.sin(a) - 16)
        h += '<div class="rl in-o" style="%s;top:%dpx;width:260px">%s</div>' % (pos, ly, lab)
        if k in copl:
            h += '<div class="cl in-o cpl" style="%s;top:%dpx;color:#36C6C6;width:260px">+ %s</div>' % (pos, ly + 28, copl[k])
    if k in copl:
        bx, by = cx + 205 * math.cos(a), cy + 205 * math.sin(a)
        h += '<div class="cp c%d">%s</div>' % (k, bot('drop', 72, bx, by))
h += ('<div class="coreW" style="position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:%dpx %dpx;transition-property:scale">' % (cx, cy)
      + orb('in-s core', 230, cx, cy, '', '<div class="morph cnt" style="position:relative;width:0;height:100px;font-size:92px;font-weight:600;color:#0F3133"></div>'
            '<span style="font-size:20px">FTE-equivalent</span>') + '</div>')
h += ('<div class="kin split mask k2" style="top:860px;left:110px;right:auto;width:620px;text-align:left;font-size:38px;color:#000">'
      'Same roles and ceremonies. Copilots draft; <b>people review and decide.</b></div><div class="src">' + SRC + '</div>')
S.append(station(2, h, 'white', True))

# 3. long term: a smaller human circle at the core, five agents in orbit
cx, cy = 1150, 560
h = ('<div class="rule"></div><div class="eb in-o e1" style="left:110px;top:96px">Long term: 4 to 5 years</div>'
     '<div class="h1 split mask k1" style="left:110px;top:150px;width:520px;font-size:56px">Humans and AI agents work together</div>')
h += orb('in-s core', 230, cx, cy, '', '<b style="font-size:96px;line-height:1">~9</b><span style="font-size:20px">FTE-equivalent,<br>from ~14 today</span>')
for k, nm in enumerate(['Tech lead', 'Product owner', 'QA', 'Engineers', 'DevOps']):
    a = -math.pi / 2 + C * k / 5
    x, y = cx + 205 * math.cos(a), cy + 205 * math.sin(a)
    h += '<div class="pc in-s hu" style="left:%dpx;top:%dpx;width:76px;height:76px;margin:-38px 0 0 -38px;font-size:32px">%s</div>' % (x, y, I('user'))
agents = [('glasses', 'Backlog agent', 'Stories, acceptance criteria', -90), ('hardhat', 'Development agent', 'Generates code, proposes fixes', -18),
          ('headset', 'Testing agent', 'Runs tests, analyzes failures', 54), ('tie', 'Release agent', 'Pipelines, release readiness', 126),
          ('glasses tie', 'Planning agent', 'Progress, risks, PI planning', 198)]
for k, (acc, nm, d, deg) in enumerate(agents):
    a = math.radians(deg)
    x, y = cx + 540 * math.cos(a), cy + 330 * math.sin(a)
    h += '<div class="ag g%d">%s<div class="an in-o" style="left:%dpx;top:%dpx"><b>%s</b><span>%s</span></div></div>' % (k, bot('drop', 150, x, y, acc), x, y + 96, nm, d)
h += ('<div class="kin split mask k2" style="top:860px;left:110px;right:auto;width:470px;text-align:left;font-size:34px;color:#F2F0F1">'
      'Agents run defined workflows. <b>People set direction and decide.</b></div><div class="src">' + SRC + '</div>')
S.append(station(3, h))

# 4. across the POM: three capacity rings fill
h = ('<div class="rule"></div><div class="eb in-o e1" style="left:110px;top:96px">Across the whole POM</div>'
     '<div class="h1 split mask k1" style="left:110px;top:150px;width:1500px">AI could unlock <b>~14%</b> of capacity, then <b>~35%</b></div>')
rows = [('Today', 'Manual work, ad hoc AI', 3670, 0, ''), ('2 to 4 years', 'People + copilots', 3160, 14, '~510 FTE-eq. unlocked (~14%)'),
        ('4 to 5 years', 'People + agents', 2390, 35, '~1,280 FTE-eq. unlocked (~35%)')]
for k, (lab, sub, v, p, u) in enumerate(rows):
    x = 480 + k * 520
    h += orb('in-s gl%d' % k, 210, x, 580, 'glass')
    h += donut('d%d' % k, x, 580, 150, 30, [('ka%d' % k, OFF, 0), ('ua%d' % k, MINT, 1 - p / 100.0)],
               '<b class="dv%d" style="font-size:54px;color:#fff;line-height:1">0</b><span style="font-size:22px;color:#CFD3D9">FTE</span>' % k)
    h += '<div class="lab in-o l%d" style="left:%dpx;top:780px"><b>%s</b><span>%s</span>%s</div>' % (k, x, lab, sub, ('<i class="m">%s</i>' % u) if u else '')
h += '<div class="src">' + SRC + ' How freed capacity is used is Lumen\'s decision.</div>'
S.append(station(4, h))

# 5. where the change lands: six layer rings, outer = 2 to 4 years, inner = 4 to 5 years (light)
lays = [('Governance', 10, 32), ('Portfolio', 2, 26), ('Value stream', 4, 17), ('Large solution', 7, 31), ('ART', 7, 31), ('Agile teams', 16, 36)]
h = ('<div class="eb in-o e1" style="left:110px;top:90px">Where the change lands</div>'
     '<div class="h1 split mask k1" style="left:110px;top:140px;width:1560px">Teams get leaner first. Layers above wait for a <b>redesign</b>.</div>'
     '<div class="in-o lg" style="position:absolute;left:110px;top:300px;font-size:26px;color:#333;display:flex;gap:30px;align-items:center">'
     '<span style="display:inline-block;width:22px;height:22px;border-radius:50%;background:#0F3133"></span>2 to 4 years'
     '<span style="display:inline-block;width:22px;height:22px;border-radius:50%;background:#36C6C6;margin-left:20px"></span>4 to 5 years</div>')
for k, (nm, st, lt) in enumerate(lays):
    x, y = 480 + (k % 3) * 480, 500 + (k // 3) * 330
    h += ('<div class="ly ly%d" style="position:absolute;left:0;top:0">' % k
          + donut('lyd', x, y, 132, 24, [('sa%d' % k, TEAL, 0)], '')
          + donut('lyd2', x, y, 100, 20, [('la%d' % k, TEAL2, 0)],
                  '<b style="font-size:26px;color:#000">%s</b><span style="font-size:26px;color:#0F3133;margin-top:4px">-%d%% / -%d%%</span>' % (nm, st, lt))
          + '</div>')
h += '<div class="src">' + SRC + '</div>'
S.append(station(5, h, 'white', True))

# 6. where the gains come from: three big orbs
pans = [('Builders', 8, 22, 'Engineers, architects, SREs, DevOps, network engineers', 'Code generation, up to 15%'),
        ('Enablers', 12, 26, 'QA and test leads, operations leads, product owners, analysts', 'Automated resolution assistant, up to 11%'),
        ('People leaders', 10, 25, 'VSOs and VSTLs, RTEs, ADLs, program managers, tech leads', 'Project plan creation, up to 11%')]
h = ('<div class="rule"></div><div class="eb in-o e1" style="left:110px;top:96px">Where the gains come from</div>'
     '<div class="h1 split mask k1" style="left:110px;top:150px;width:1500px">Five use cases per role type deliver most of the gain</div>')
for k, (nm, a, b, who, uc) in enumerate(pans):
    x = 480 + k * 480
    h += orb('in-s go go%d' % k, 280, x, 480, '', '<b style="font-size:64px;line-height:1"><span class="ra%d">0</span>&ndash;<span class="rb%d">0</span>%%</b>'
             '<span style="font-size:20px;margin-top:6px">near-term gain</span>' % (k, k))
    h += '<div class="lab in-o gn" style="left:%dpx;top:660px"><b>%s</b><span>%s</span><i class="m">Top use case: %s</i></div>' % (x, nm, who, uc)
h += '<div class="src">Near-term productivity gain by role type. ' + SRC + '</div>'
S.append(station(6, h))

# 7. close
h = '<div class="rule"></div>'
for k, (sz, x, y, kind) in enumerate([(200, 1600, 190, ''), (120, 300, 220, 'glass'), (80, 1720, 640, ''), (150, 240, 640, 'glass')]):
    h += orb('fo in-s f%d' % k, sz, x, y, kind)
h += ('<div class="kin split mask k1" style="top:330px;font-size:80px;color:#fff">How freed capacity is used</div>'
      '<div class="kin split mask k2" style="top:440px;font-size:80px;color:#fff">is <b>Lumen\'s decision</b>.</div>'
      '<div class="in-o sub" style="position:absolute;left:0;right:0;top:600px;text-align:center;font-size:40px;color:#CFD3D9">'
      'Redeploy, reinvest or release. These are modeled potentials, not targets.</div>')
for k, (acc, x) in enumerate([('glasses', 530), ('hardhat', 700), ('headset', 1220), ('tie', 1390), ('glasses tie', 1560)]):
    h += bot('fin drop', 120, x, 810, acc)
h += WM + '<div class="src" style="color:#CFD3D9">&copy; 2026 Lumen Technologies. All Rights Reserved.</div>'
S.append(station(7, h, 'pattern'))

# the guide and its bubbles live in the world
GUIDE = [(260, 760), (1780, 120), (1720, 860), (300, 560), (1780, 120), (1760, 330), (1780, 120), (960, 790)]
guide = bot('guide drop', 150, GUIDE[0][0], GUIDE[0][1], '', 8)
bub = ('<div class="bubble in-p gb0" style="left:340px;top:610px;z-index:9;white-space:nowrap;max-width:none">Hi, I am a Lumen copilot. Follow me.</div>'
       '<div class="bubble r in-p gb5" style="left:%dpx;top:%dpx;z-index:9;white-space:nowrap;max-width:none">Teams change first.</div>' % (5 * WX + 1290, 240))
open(os.path.join(HERE, 'assets', 'scenes', 'journey_v2.html'), 'w', encoding='utf-8').write(CSS + ''.join(S) + guide + bub)

# ---------------------------------------------------------------- timeline
ev = []
def E(at, **k):
    k['at'] = int(at); ev.append(k)
def P(i, sel):
    return '.st%d %s' % (i, sel)
def W(i, x):
    return i * WX + x
def cam(at, i, x=960, y=540, s=1, ms=1200, ease='spring-soft', **k):
    E(at, cam=dict(x=W(i, x), y=y, s=s, ms=ms, ease=ease, rx=k.get('rx', 0), ry=k.get('ry', 0), rz=k.get('rz', 0)))
def gpos(i):
    return [W(i, GUIDE[i][0]) - 75, GUIDE[i][1] - 93]

def portal(t, i, sel, colour, nxt, land, start):
    """Dive into an orb of station i, come out in station nxt: flood out toward `land` (station coords)."""
    E(t, cam={"focus": P(i, sel), "s": 13, "ms": 900, "ease": "in"}); E(t, cue='portal')
    E(t + 880, stage_js="floodIn(960,540,'%s',0)" % colour)
    sx, sy, ss = start
    E(t + 920, cam=dict(x=W(nxt, sx), y=sy, s=ss, ms=0, rx=0, ry=0, rz=0))
    E(t + 920, move='.guide', to=gpos(nxt), ms=1)
    lx, ly = 960 + ss * (land[0] - sx), 540 + ss * (land[1] - sy)
    E(t + 960, stage_js="floodOut(%d,%d,700)" % (lx, ly))
    return t + 1000

def flood(t, sx, sy, colour, nxt, land):
    E(t, stage_js="floodIn(%d,%d,'%s',480)" % (sx, sy, colour)); E(t, cue='flood')
    E(t + 520, cam=dict(x=W(nxt, 960), y=540, s=1, ms=0, rx=0, ry=0, rz=0))
    E(t + 520, move='.guide', to=gpos(nxt), ms=1)
    E(t + 560, stage_js="floodOut(%d,%d,650)" % land)
    return t + 600

def walk(t, i, nxt, rz=0):
    E(t, move='.guide', to=gpos(nxt), ms=1800); E(t, cue='travel')
    E(t, cam=dict(x=(W(i, 960) + W(nxt, 960)) / 2, y=580, s=0.78, ms=900, ease='inout', rx=0, ry=0, rz=rz))
    cam(t + 900, nxt, ms=900, ease='spring-soft')
    return t + 1800

t = 0
# 0 hook
E(200, show='.guide'); E(300, stagger=P(0, '.orb'), gap=160)
E(200, words=P(0, '.k1'), gap=130); E(1500, words=P(0, '.k2'), gap=150)
E(600, show='.gb0'); E(600, show='.guide', cls='talk'); E(2400, hide='.guide', cls='talk'); E(2600, show='.guide', cls='happy')
E(200, cam=dict(x=960, y=540, s=1, ms=4800, ease='soft', rx=0, ry=0, rz=0))
E(5000, hide='.gb0'); E(5000, hide='.guide', cls='happy'); E(5000, show='.guide', cls='look-r')
t = portal(5600, 0, '.port', MINT, 1, (1250, 560), (1250, 560, 1.3))
# 1 today
E(t, hide='.guide', cls='look-r')
E(t + 100, show=P(1, '.e1')); E(t + 200, words=P(1, '.k1'), gap=120); E(t + 300, show=P(1, '.core'))
E(t + 500, count=[P(1, '.n0'), 3670], ms=1800, pre='~'); E(t + 1100, stagger=P(1, '.vs'), gap=110)
E(t + 1400, stagger=P(1, '.sr'), gap=350); E(t + 2300, stagger=P(1, '.dot'), gap=5)
cam(t + 2500, 1, ms=1700); E(t + 4600, words=P(1, '.k2'), gap=110); E(t + 3000, show='.guide', cls='happy')
t += 8200
E(t, hide='.guide', cls='happy')
t = flood(t, 1250, 560, '#FFFFFF', 2, (1150, 560))
# 2 team
E(t + 100, morph=P(2, '.ebm'), to={"w": 130, "html": "Today"}, ms=500); E(t + 200, words=P(2, '.k1'), gap=140)
E(t + 300, show=P(2, '.core')); E(t + 500, morph=P(2, '.cnt'), to={"w": 150, "html": "~14"}, ms=700)
E(t + 700, stagger=P(2, '.pc'), gap=80); E(t + 1100, stagger=P(2, '.rl'), gap=110)
E(t, cam=dict(x=W(2, 1150), y=560, s=1.2, ms=0, rx=0, ry=0, rz=0)); cam(t + 2600, 2, ms=1500)
E(t + 4200, morph=P(2, '.ebm'), to={"w": 440, "html": "Short term: 2 to 4 years"}, ms=600)
E(t + 4500, stagger=P(2, '.cp .masc'), gap=280); E(t + 4600, stagger=P(2, '.cpl'), gap=280)
E(t + 6200, style=[P(2, '.coreW'), 'scale', '0.88'], ms=900); E(t + 6300, morph=P(2, '.cnt'), to={"html": "~12"}, ms=700)
E(t + 6500, show=P(2, '.cp .masc'), cls='happy'); E(t + 6700, show=P(2, '.c5 .masc'), cls='waving'); E(t + 6900, words=P(2, '.k2'), gap=120)
E(t + 1200, show='.guide', cls='look-l'); E(t + 4400, hide='.guide', cls='look-l'); E(t + 4500, show='.guide', cls='surprised'); E(t + 5600, hide='.guide', cls='surprised')
t += 9400
t = walk(t, 2, 3, rz=-4)
# 3 agents
E(t + 100, show=P(3, '.e1')); E(t + 200, words=P(3, '.k1'), gap=120); E(t + 300, show=P(3, '.core'))
E(t + 600, stagger=P(3, '.hu'), gap=120); E(t + 1300, stagger=P(3, '.ag .masc'), gap=260); E(t + 1500, stagger=P(3, '.ag .an'), gap=260)
E(t + 2700, cam={"focus": P(3, '.g1 .masc'), "s": 1.55, "ms": 1000, "ease": "spring-soft", "at": [960, 520]})
E(t + 2900, show=P(3, '.g1 .masc'), cls='talk')
E(t + 4000, cam={"focus": P(3, '.g3 .masc'), "s": 1.55, "ms": 1000, "ease": "spring-soft", "at": [960, 520]})
E(t + 4100, hide=P(3, '.g1 .masc'), cls='talk'); E(t + 4200, show=P(3, '.g3 .masc'), cls='waving')
cam(t + 5300, 3, ms=1200); E(t + 5500, show=P(3, '.ag .masc'), cls='happy'); E(t + 5700, words=P(3, '.k2'), gap=110)
t += 8300
t = portal(t, 3, '.core', MINT, 4, (480, 580), (960, 560, 1.05))
# 4 capacity rings
circ = C * 150
E(t + 100, show=P(4, '.e1')); E(t + 200, words=P(4, '.k1'), gap=110)
for k, (lab, sub, v, p, u) in enumerate(rows):
    tk = t + 700 + k * 1500
    E(tk, show=P(4, '.gl%d' % k)); E(tk, show=P(4, '.d%d' % k))
    E(tk + 100, style=[P(4, '.ka%d' % k), 'strokeDashoffset', '%.1f' % (circ * p / 100.0)], ms=1100)
    E(tk + 100, count=[P(4, '.dv%d' % k), v], ms=1100, pre='~')
    if p:
        E(tk + 1100, style=[P(4, '.ua%d' % k), 'strokeDashoffset', '%.1f' % (circ * (1 - p / 100.0))], ms=800)
    E(tk + 700, show=P(4, '.l%d' % k))
E(t + 4400, cam={"focus": P(4, '.d2'), "s": 1.35, "ms": 1100, "ease": "spring-soft", "at": [960, 500]})
cam(t + 6200, 4, ms=1100)
E(t + 1000, show='.guide', cls='look-l'); E(t + 5000, hide='.guide', cls='look-l'); E(t + 5000, show='.guide', cls='happy')
t += 8000
E(t, hide='.guide', cls='happy')
t = flood(t, 1520, 580, '#FFFFFF', 5, (1440, 830))
# 5 layer rings
E(t + 100, show=P(5, '.e1')); E(t + 200, words=P(5, '.k1'), gap=100); E(t + 600, show=P(5, '.lg'))
E(t + 700, stagger=P(5, '.dn'), gap=90)
for k, (nm, st, lt) in enumerate(lays):
    E(t + 1700 + k * 110, style=[P(5, '.sa%d' % k), 'strokeDashoffset', '%.1f' % (C * 132 * (1 - st / 100.0))], ms=900)
    E(t + 3100 + k * 110, style=[P(5, '.la%d' % k), 'strokeDashoffset', '%.1f' % (C * 100 * (1 - lt / 100.0))], ms=900)
E(t + 4300, show='.gb5'); E(t + 4300, show='.guide', cls='talk'); E(t + 5600, hide='.guide', cls='talk')
E(t + 4800, cam={"focus": P(5, '.ly5 .lyd'), "s": 1.45, "ms": 1100, "ease": "spring-soft", "at": [960, 540]})
cam(t + 6800, 5, ms=1100)
t += 8600
E(t, hide='.gb5')
t = walk(t, 5, 6, rz=5)
# 6 gains orbs
E(t + 100, show=P(6, '.e1')); E(t + 200, words=P(6, '.k1'), gap=100); E(t + 700, stagger=P(6, '.go'), gap=300)
for k, (nm, a, b, who, uc) in enumerate(pans):
    E(t + 1100 + k * 300, count=[P(6, '.ra%d' % k), a], ms=900); E(t + 1100 + k * 300, count=[P(6, '.rb%d' % k), b], ms=900)
E(t + 1600, stagger=P(6, '.gn'), gap=250)
for k in range(3):
    E(t + 3400 + k * 1400, cam={"focus": P(6, '.go%d' % k), "x": W(6, 480 + k * 480), "y": 600, "s": 1.3, "ms": 900, "ease": "spring-soft", "at": [960, 540]})
cam(t + 7600, 6, ms=1000); E(t + 3000, show='.guide', cls='happy')
t += 9200
E(t, hide='.guide', cls='happy')
t = portal(t, 6, '.go1', MINT, 7, (960, 540), (960, 540, 1.05))
# 7 close
E(t + 100, stagger=P(7, '.orb'), gap=150); E(t + 200, words=P(7, '.k1'), gap=130); E(t + 1300, words=P(7, '.k2'), gap=150)
E(t + 2300, show=P(7, '.sub')); E(t + 2600, stagger=P(7, '.fin'), gap=180); E(t + 3700, show=P(7, '.fin'), cls='happy')
E(t + 3700, show='.guide', cls='waving'); cam(t + 200, 7, ms=4500, ease='soft')
t += 6200
ev.sort(key=lambda e: e['at'])

base = json.load(open(os.path.join(HERE, 'storyboard.json'), encoding='utf-8'))
sb = {k: v for k, v in base.items() if k != 'scenes'}
sb['output_name'] = 'lumen-pom-ai-v2'
sb['motion_blur'] = 1
sb['scenes'] = [{"type": "motion", "html": "assets/scenes/journey_v2.html", "duration": t,
                 "start": {"x": 960, "y": 540, "s": 1.08}, "events": ev}]
json.dump(sb, open(os.path.join(HERE, 'storyboard_v2.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('v2: %d events, %.0f s' % (len(ev), t / 1000))
