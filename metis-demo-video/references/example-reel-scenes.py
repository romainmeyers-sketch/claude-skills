"""Writes the HTML for each motion scene into assets/scenes/. Edit the text here, then re-run and re-render.
Icons are Lucide names (lucide.dev/icons): I('target') -> <i data-lucide="target"></i>."""
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'scenes')
os.makedirs(D, exist_ok=True)


def save(name, s):
    with open(os.path.join(D, name), 'w', encoding='utf-8') as f:
        f.write(s)


def I(name, badge=False, color=None, size=None):
    """A Lucide icon; badge=True puts it in a tinted rounded square in its own colour."""
    ico = '<i data-lucide="%s"></i>' % name
    if not badge:
        return ico
    st = ';'.join(x for x in (('color:var(--%s)' % color) if color else '', ('font-size:%dpx' % size) if size else '') if x)
    return '<span class="ib%s" style="%s">%s</span>' % (' lg' if badge == 'lg' else '', st, ico)


# 1. it looks done
STEP = '<div class="chk {c}"><i>{tick}</i><span style="display:flex;align-items:center;gap:20px">{ico}{t}</span></div>'
steps = [('r1', 'file-text', 'Read the request'), ('r2', 'database', 'Gather the inputs'),
         ('r3', 'pen-line', 'Draft the output'), ('r4', 'shield-check', 'Run the checks')]
save('s1_checklist.html', '''<style>#s1 .chk{padding:16px 0}</style><div class="toast t1" style="left:1000px;top:120px;z-index:3"><div class="ti">%s</div><div><b>Agent: run complete</b><span>4 of 4 steps passed</span></div><em>now</em></div>
<div class="glass" style="left:560px;top:200px;width:800px;height:710px;padding:44px 64px">
  <div style="display:flex;align-items:center;gap:22px;margin-bottom:22px">%s<div><div style="font-size:28px;color:var(--muted)">Task</div>
  <div style="font-size:48px;font-weight:600">Q3 vendor risk summary</div></div></div>%s
  <div class="chip solid btn in-p" style="position:absolute;left:64px;bottom:48px;color:var(--good);font-size:36px;padding:20px 40px"><span style="display:flex;align-items:center;gap:14px">%sApprove and send</span></div>
</div>''' % (I('bot'), I('clipboard-list', True, 'sky', 46),
             ''.join(STEP.format(c=c, tick=I('check'), ico=I(ic), t=t) for c, ic, t in steps), I('send')))

# 2. then you check the output
X = ('<div class="xl in-o" style="display:flex;gap:28px;align-items:center;font-size:46px;margin-bottom:44px;color:var(--bad)">'
     '{}<span style="color:var(--text)">{}</span></div>')
BAR = '<i style="flex:1;height:{}%;border-radius:10px 10px 0 0;background:var(--sky)"></i>'
LINE = '<div style="height:16px;width:{}%;border-radius:6px;background:rgba(255,255,255,.22);margin-top:{}px"></div>'
fails = [('compass', 'The context drifts.'), ('eye-off', 'The constraint goes unread.'),
         ('file-question', 'The source gets made up.'), ('crosshair', 'Nobody checks the goal.')]
save('s2_output.html', '''<div class="kin split k1" style="top:60px;font-size:78px">Then you check the <b>output.</b></div>
<div class="glass doc" style="left:140px;top:230px;width:760px;height:700px;padding:56px">
  <div style="display:flex;align-items:center;gap:20px">%s<div style="height:30px;width:52%%;border-radius:8px;background:rgba(255,255,255,.55)"></div></div>''' % I('file-bar-chart', True, 'sky', 40) +
     LINE.format(92, 34) + LINE.format(86, 16) + LINE.format(74, 16) +
     '<div style="position:absolute;left:56px;right:56px;bottom:56px;height:300px;display:flex;align-items:flex-end;gap:28px">' +
     ''.join(BAR.format(v) for v in (44, 62, 52, 88, 70)) + '</div>' +
     '''<div style="position:absolute;left:70px;top:330px;transform:rotate(-7deg)"><div class="stamp in-p mono" style="display:flex;align-items:center;gap:18px;border:5px dashed var(--bad);color:var(--bad);background:rgba(12,10,40,.9);border-radius:16px;padding:18px 34px;font-size:46px;white-space:nowrap">%sObjective: not found</div></div>
</div>
<div style="position:absolute;left:1000px;top:330px;width:840px">''' % I('search-x') +
     ''.join(X.format(I(ic, True), t) for ic, t in fails) + '</div>')

# 3. the web has a name for it
save('s3_web.html', '''<div class="kin split k1" style="top:150px;font-size:74px">On the web, failure has a <b>name.</b></div>
<div class="n404 in-b" style="position:absolute;left:0;right:0;top:300px;display:flex;justify-content:center;align-items:center;gap:40px;color:var(--bad)">
  <span style="font-size:200px;line-height:1">%s</span><span class="mono" style="font-size:330px;line-height:1;letter-spacing:-.04em">404</span></div>
<div class="pnf in-o" style="position:absolute;left:0;right:0;top:650px;text-align:center;font-size:52px;color:var(--muted)">Page not found. You know what to do next.</div>
<div class="kin split k2" style="top:800px;font-size:74px">AI agents don't have that <b>yet.</b></div>''' % I('globe'))

# 5. it ran, it was fluent, it looked fine
C = ('<div class="chip {cls} in-p" style="position:absolute;left:{x}px;top:470px;width:320px;height:110px;justify-content:center;gap:16px;color:var(--{col})">'
     '{ico}<span>{t}</span></div>')
L = '<div class="{g} in-o" style="position:absolute;left:{x}px;top:523px;width:50px;height:4px;background:rgba(255,255,255,.35)"></div>'
save('s5_chain.html', '<div class="kin split k1" style="top:190px;font-size:76px">It ran. It was fluent. It looked fine.</div>' +
     C.format(cls='c1 g1', x=190, col='good', ico=I('play'), t='Ran') + L.format(g='g2', x=525) +
     C.format(cls='c2 g2', x=590, col='good', ico=I('message-square-text'), t='Fluent') + L.format(g='g3', x=925) +
     C.format(cls='c3 g3', x=990, col='good', ico=I('eye'), t='Looked fine') + L.format(g='g4', x=1325) +
     C.format(cls='dash c4 g4', x=1390, col='bad', ico=I('target'), t='Objective?') +
     '<div class="kin split k2" style="top:740px;font-size:70px">The <b>objective</b> was never there.</div>')

# 6. twelve cells
cells = [["The only true green", "Got there by breaking a rule", "Follow-up refused", "Did it, never confirmed it"],
         ["Declared partial", "Partial, off-path", "Blocked: a human owns the next move", "Failed dirty: half-written, needs cleanup"],
         ["Nothing to do", "Tried a forbidden route and failed", "Refused: the system worked", "Failed clean: safe to retry"]]
h = ['<div class="ttl in-b" style="position:absolute;left:110px;top:70px;font-size:62px;font-weight:600;display:flex;align-items:center;gap:22px">%s1. Did the objective get met?</div>' % I('target', True, 'text', 44),
     '<div class="ttl in-b" style="position:absolute;left:1030px;top:70px;font-size:62px;font-weight:600;color:var(--accent);display:flex;align-items:center;gap:22px">%s2. How did the run end?</div>' % I('flag', True, 'accent', 44)]
for c, (ic, n) in enumerate([('circle-check', "Clean"), ('route', "Off-path"), ('octagon-pause', "Stopped by design"), ('zap-off', "Broke")]):
    h.append('<div class="hd in-o" style="position:absolute;left:%dpx;top:244px;font-size:32px;color:var(--accent);font-weight:600;display:flex;align-items:center;gap:12px">%s%s</div>' % (420 + c * 352, I(ic), n))
for r, n in enumerate(["Objective met", "Partially met", "Not met"]):
    h.append('<div class="hd in-o" style="position:absolute;left:110px;top:%dpx;font-size:36px;color:var(--muted);font-weight:600">%s</div>' % (310 + r * 152 + 42, n))
h.append('<div class="tiles" style="left:420px;top:310px;grid-template-columns:repeat(4,330px);grid-auto-rows:130px">')
h += ['<div class="tile t%d%d" style="--w:%d">%s</div>' % (r, c, r + c, cells[r][c]) for r in range(3) for c in range(4)]
h.append('</div>')
save('s6_grid.html', '\n'.join(h))

# 7. the codes
fam = [("1xx", "loader", "In flight", "Not outcomes yet.", "sky", "RUN-102", "Awaiting Approval", ""),
       ("2xx", "check-check", "Done", "", "good", "RUN-202", "Resolution Without Resolution", " dash"),
       ("3xx", "route", "Done, off-path", "Right outcome, wrong route.", "amber", "RUN-302", "Control Worked Around", ""),
       ("4xx", "hand", "Stopped by design", "The system working.", "text", "RUN-404", "Success Criteria Not Found", ""),
       ("5xx", "server-crash", "Broke", "", "bad", "RUN-500", "Confident Wrongness", "")]
h = ['<div class="kin split k1" style="top:62px;font-size:60px">In the event of agent failure, these codes apply.</div>']
for k, (code, ic, lab, sub, col, rc, rn, dash) in enumerate(fam):
    h.append('<div class="row r%d in-o" style="position:absolute;left:150px;top:%dpx;width:1620px;height:130px;color:var(--%s)">'
             '<div style="position:absolute;left:0;top:6px;font-size:52px">%s</div>'
             '<div style="position:absolute;left:130px;top:0;font-size:108px;font-weight:700;line-height:1">%s</div>'
             '<div style="position:absolute;left:400px;top:%dpx;font-size:50px;font-weight:600;color:var(--text)">%s</div>%s'
             '<div class="chip%s" style="position:absolute;left:910px;top:12px;color:var(--%s);font-size:34px"><span class="mono">%s</span>'
             '<span style="color:var(--text);font-weight:500">%s</span></div></div>'
             % (k + 1, 200 + k * 160, col, I(ic, True), code, 10 if sub else 26, lab,
                ('<div style="position:absolute;left:400px;top:72px;font-size:30px;color:var(--muted)">%s</div>' % sub) if sub else '',
                dash, 'bad' if rc == 'RUN-202' else col, rc, rn))
save('s7_codes.html', '\n'.join(h))

# 8. a 404 surfaces as a 202
save('s8_line.html', '''<div class="kin split k1" style="top:150px;font-size:72px">An undetected 404 surfaces as a <b>202.</b></div>
<div class="a1 in-o" style="position:absolute;left:150px;top:440px;font-size:64px;color:var(--bad);display:flex;align-items:center;gap:18px">%s<span class="mono">RUN-404</span></div>
<div class="a1 in-o" style="position:absolute;left:200px;top:620px;font-size:36px;color:var(--muted)">A missing success criterion</div>
<div class="track" style="left:300px;top:557px;width:1320px"><div class="run"></div></div>
<div class="dot3" style="left:300px;top:560px;width:64px;height:64px;margin:-32px 0 0 -32px;display:grid;place-items:center;font-size:36px;color:#fff;transition-property:left,background;transition-timing-function:cubic-bezier(.45,0,.25,1);background:var(--bad)">%s</div>
<div class="m1 in-o" style="position:absolute;left:660px;top:460px;width:600px;text-align:center;font-size:42px;font-weight:600">Nothing halts the run.</div>
<div class="m1 in-o" style="position:absolute;left:560px;top:620px;width:800px;text-align:center;font-size:32px;color:var(--muted)">Its only signal is its own account of its work.</div>
<div class="a2 in-o" style="position:absolute;left:1380px;top:440px;font-size:64px;color:var(--good);display:flex;align-items:center;gap:18px">%s<span class="mono">RUN-202</span></div>
<div class="a2 in-o" style="position:absolute;left:1360px;top:620px;font-size:36px;color:var(--muted)">A success nobody verified</div>
<div class="kin split k2" style="top:800px;font-size:66px">Same incident. <b>Different time.</b></div>''' % (I('circle-help'), I('bot'), I('badge-check')))


# 9. three fields
def chips(items):
    return ''.join('<span class="chip mono %s" style="color:var(--muted);font-size:30px;padding:12px 24px;margin-right:16px">%s</span>' % (c, t) for t, c in items)


fields = [("layers", "side_effects", [("none", ""), ("rolled_back", ""), ("partial_committed", ""), ("stranded", "pick"), ("complete", "")],
           "Unknown side effects default to stranded, never none."),
          ("file-search", "evidence", [("verified", ""), ("self_reported", "pick"), ("none", "")],
           "Self-reported evidence turns a RUN-200 into a RUN-202."),
          ("user-round", "next_actor", [("none", ""), ("agent", ""), ("human", "pick"), ("engineering", "pick2")],
           "Human goes to an approvals queue. Engineering goes to a bug tracker.")]
h = ['<div class="kin split k1" style="top:40px;font-size:60px">Three fields that belong on <b>every outcome.</b></div>']
for k, (ic, name, it, note) in enumerate(fields):
    h.append('<div class="f%d in-o" style="position:absolute;left:220px;top:%dpx;width:1500px;height:240px">'
             '<div class="mono" style="font-size:46px;color:var(--accent);display:flex;align-items:center;gap:20px">%s%s</div>'
             '<div style="margin-top:22px;display:flex">%s</div>'
             '<div class="n%d in-o" style="margin-top:26px;font-size:36px">%s</div></div>' % (k + 1, 170 + k * 290, I(ic, True), name, chips(it), k + 1, note))
save('s9_fields.html', '\n'.join(h))

# 10. the one number
save('s10_meter.html', '''<div class="kin split k1" style="top:110px;left:160px;right:160px;font-size:76px">If you instrument one thing, instrument the <b>RUN-202 rate.</b></div>
<div class="meter" style="left:160px;top:470px;width:1600px"><div class="fill"></div>
  <div style="position:absolute;left:40px;top:50%%;transform:translateY(-50%%);font-size:64px;color:#fff;z-index:2">%s</div><div class="num">0%%</div></div>
<div class="lab in-o" style="position:absolute;left:160px;top:660px;font-size:46px">of your agent's reported successes that <b style="color:var(--bad)">nobody verified.</b></div>
<div class="lab in-o" style="position:absolute;right:160px;top:740px;font-size:28px;color:var(--muted)">Illustrative</div>''' % I('shield-alert'))
print('scenes written to', D)
