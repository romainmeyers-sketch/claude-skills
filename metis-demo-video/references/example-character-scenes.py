"""Writes the HTML for each motion scene of the Agent Office video into assets/scenes/.
Every name and message here is fictional: never put real client names or emails in this video."""
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'scenes')
os.makedirs(D, exist_ok=True)

NAVY, BLUE, MINT, INK = '#20206e', '#256ba2', '#3bdac0', '#141a3c'
CHIEF = '<mascot class="chief {c}" kind="bot" color="#3bdac0" size="{s}" acc="tie" {n} style="left:{x}px;top:{y}px;--eyec:#b9fff2;--ant:#20206e"></mascot>'
DRAFT = '<mascot class="drafter {c}" kind="bot" color="#4f8ff7" size="{s}" acc="glasses" {n} style="left:{x}px;top:{y}px;--ant:#3bdac0"></mascot>'
BOB = '<mascot class="bob {c}" kind="bot" color="#256ba2" size="{s}" acc="hardhat" {n} style="left:{x}px;top:{y}px;--hat:#3bdac0;--ant:#3bdac0"></mascot>'
MEET = '<mascot class="planner {c}" kind="bot" color="#7b6cf6" size="{s}" acc="headset" {n} style="left:{x}px;top:{y}px;--ant:#3bdac0"></mascot>'


def m(t, x, y, s=240, c='', name=''):
    return t.format(x=x, y=y, s=s, c=c, n=('name="%s"' % name) if name else '')


def save(name, s):
    with open(os.path.join(D, name), 'w', encoding='utf-8') as f:
        f.write(s)


def I(name):
    return '<i data-lucide="%s"></i>' % name


CSS = '''<style>
.msg{position:absolute;display:flex;gap:16px;align-items:center;background:#fff;border-radius:22px;padding:16px 22px 16px 16px;box-shadow:0 26px 50px -26px rgba(20,30,70,.5);
  color:#141a3c;font-size:34px;white-space:nowrap}
.msg .ic{flex:none;width:66px;height:66px;border-radius:16px;display:grid;place-items:center;font-size:34px;color:#fff}
.msg b{display:block;font-size:24px;color:#6b7390;font-weight:600}
.card{position:absolute;background:#fff;border-radius:30px;color:#141a3c;box-shadow:0 50px 90px -40px rgba(20,30,70,.5),0 0 0 1px rgba(20,30,70,.05)}
.btnx{display:inline-flex;align-items:center;gap:12px;padding:16px 30px;border-radius:999px;font-size:28px;font-weight:700}
.btnx.navy{background:#20206e;color:#fff}
.btnx.line{border:2px solid #d5d9e6;color:#141a3c}
.pchip{display:inline-flex;align-items:center;gap:10px;padding:12px 22px;border-radius:999px;border:2px solid #d5d9e6;font-size:26px;font-weight:600;color:#3b4360;margin:0 10px 12px 0}
.pchip.sel{background:#20206e;border-color:#20206e;color:#fff}
.ask{position:absolute;display:flex;align-items:center;gap:16px;background:#fff;border-radius:20px;padding:18px 26px;font-size:34px;font-weight:600;color:#141a3c;box-shadow:0 26px 50px -26px rgba(20,30,70,.5);white-space:nowrap}
.ask .to{font-size:26px;font-weight:700;padding:6px 14px;border-radius:999px;color:#fff}
.stat{position:absolute;width:400px;background:#fff;border-radius:28px;padding:26px 30px;box-shadow:0 40px 70px -36px rgba(20,30,70,.45)}
.stat small{display:flex;gap:10px;align-items:center;font-size:24px;font-weight:600;color:#6b7390}
.stat .n{font-size:84px;font-weight:800;letter-spacing:-.03em;color:#141a3c;line-height:1.05;margin-top:6px}
.night{position:absolute;inset:-200px;background:radial-gradient(1200px 700px at 50% 40%,rgba(32,32,110,.55),rgba(12,12,48,.92));opacity:0;transition:opacity 1.6s}
.night.in{opacity:1}
.zz{position:absolute;font-size:44px;font-weight:800;color:#b9c4ff;opacity:0;transition:opacity .6s}
.zz.in{opacity:1;animation:zz 2.4s ease-in-out infinite}
@keyframes zz{0%{translate:0 0}100%{translate:30px -60px;opacity:0}}
</style>'''

# 1. 7:00 AM, the inbox pours in
msgs = [('message-square', '#4a154b', 'Slack', 'Can you send the deck by Friday?', 160, 330, -4),
        ('mail', '#d93025', 'Email', 'Quick question on the budget', 1220, 300, 3),
        ('notebook-pen', '#256ba2', 'Meeting notes', 'Action: book a sync with Ana', 260, 560, 2),
        ('message-square', '#4a154b', 'Slack', 'Who owns the training plan?', 1180, 560, -3),
        ('mail', '#d93025', 'Email', 'Re: Interview next week', 640, 760, -2),
        ('message-square', '#4a154b', 'Slack', 'Need the Excel by 3pm', 120, 800, 4),
        ('mail', '#d93025', 'Email', 'Can we move Thursday?', 1260, 800, 2)]
h = [CSS, '<div class="kin split mask k1" style="top:120px;font-size:96px;color:#141a3c">7:00 AM. <b>43 new messages.</b></div>']
for k, (ic, col, src, txt, x, y, r) in enumerate(msgs):
    h.append('<div style="position:absolute;left:%dpx;top:%dpx;transform:rotate(%ddeg)"><div class="msg in-p m%d floaty" style="position:relative;animation-delay:-%dms">'
             '<span class="ic" style="background:%s">%s</span><div><b>%s</b>%s</div></div></div>' % (x, y, r, k, k * 600, col, I(ic), src, txt))
h.append('<div class="kin split mask k2" style="top:440px;font-size:84px;color:#141a3c">Who answers all of this?</div>')
save('s1_inbox.html', '\n'.join(h))

# 2. meet the Chief of Staff
asks = [('Deck for Thursday', 'Bob De Builder', BLUE), ('Reply to Tom', 'Reply Drafter', '#4f8ff7'), ('Book a sync with Ana', 'Meeting Planner', '#7b6cf6')]
h = [CSS, m(CHIEF, 740, 300, 400, 'drop'),
     '<div class="bubble in-p b1" style="left:1180px;top:200px">Hi, I\'m your Chief of Staff.</div>',
     '<div class="bubble in-p b2" style="left:1180px;top:200px">Every message becomes an ask, with an owner.</div>']
for k, (t, who, col) in enumerate(asks):
    h.append('<div class="ask in-o a%d" style="left:%dpx;top:%dpx">%s%s<span class="to" style="background:%s">%s</span></div>'
             % (k, 1220, 520 + k * 130, I('arrow-right'), t, col, who))
for k, (ic, col, src, txt, x, y, r) in enumerate(msgs[:3]):
    h.append('<div class="msg in-o q%d" style="left:%dpx;top:%dpx">%s<div><b>%s</b>%s</div></div>'
             % (k, 60, 520 + k * 130, '<span class="ic" style="background:%s">%s</span>' % (col, I(ic)), src, txt))
save('s2_chief.html', '\n'.join(h))

# 3. Reply Drafter: the draft is ready, you send
draft = ('Hi Tom, here is the budget view you asked for. The two open lines are travel and tooling; '
         'I have flagged both. Happy to walk you through it on Thursday.')
save('s3_replies.html', CSS + m(DRAFT, 70, 430, 330, 'drop') + '''
<div class="bubble in-p b1" style="left:60px;top:250px">Drafted for you.</div>
<div class="card c1 in-o" style="left:560px;top:130px;width:1260px;height:800px;padding:40px 46px">
  <div style="display:flex;align-items:center;gap:16px;font-size:24px;color:#6b7390;font-weight:600"><span class="ib" style="color:#4f8ff7;font-size:30px">%s</span>Replies &middot; To answer (4)</div>
  <div style="font-size:40px;font-weight:700;margin:18px 0 6px">Reply to Tom Becker</div>
  <div style="font-size:24px;color:#6b7390">Slack &middot; asked about the budget view</div>
  <div class="split dr" style="margin-top:26px;padding:26px 30px;border:2px solid #20206e;border-radius:20px;font-size:35px;line-height:1.45;height:270px">%s</div>
  <div style="display:flex;align-items:center;gap:14px;margin-top:22px;padding:14px 18px;background:#f2f4f9;border-radius:18px;font-size:26px;color:#3b4360">
    %s<span class="rw" style="flex:1">shorter, warmer</span><span class="btnx line" style="padding:10px 22px;font-size:24px">Rewrite</span></div>
  <div style="position:absolute;right:46px;bottom:40px;display:flex;gap:16px"><span class="btnx line">Save draft</span><span class="btnx navy send">%sReview and send</span></div>
</div>''' % (I('reply'), draft, I('sparkles'), I('send')))

# 4. Bob De Builder: send work, it gets built
fmts = [('presentation', 'Deck', 'sel'), ('sheet', 'Excel', ''), ('code', 'HTML page', ''), ('file-text', 'PDF', ''), ('file-type', 'Word', ''), ('clapperboard', 'Video', '')]
save('s4_bob.html', CSS + m(BOB, 1420, 360, 340, 'drop') + '''
<div class="bubble r in-p b1" style="left:1150px;top:150px">Building: Champion role card</div>
<div class="card c1 in-o" style="left:90px;top:250px;width:1160px;height:680px;padding:42px 46px">
  <div style="display:flex;align-items:center;gap:16px;font-size:24px;color:#6b7390;font-weight:600"><span class="ib" style="color:#256ba2;font-size:30px">%s</span>Send work</div>
  <div style="margin-top:22px;padding:22px 26px;border:2px solid #d5d9e6;border-radius:18px;font-size:40px;font-weight:600;height:96px"><span class="split ty">Champion role card, one slide</span></div>
  <div style="margin-top:28px;font-size:22px;color:#6b7390;font-weight:600">Format</div>
  <div style="margin-top:12px">%s</div>
  <div style="margin-top:14px;font-size:22px;color:#6b7390;font-weight:600">Design</div>
  <div style="margin-top:12px"><span class="pchip sel">Metis</span><span class="pchip">Client</span><span class="pchip">Let it decide</span></div>
  <div style="position:absolute;right:46px;bottom:40px"><span class="btnx navy start">%sStart</span></div>
</div>
<div class="morph st" style="left:150px;top:840px;width:0;height:76px;border-radius:38px;background:#20206e;color:#fff;font-size:30px;font-weight:700"></div>
<div class="ccard in-p out1" style="left:1330px;top:770px;--cc:#256ba2">
  <div class="cc-h"><span class="cc-av">%s</span><div><b>Champion role card</b><span>Deck &middot; Metis</span></div></div>
  <div class="cc-b"><small>%sReady in Outputs</small>1 slide, with notes</div><span class="ok-badge">%s</span></div>
''' % (I('send'), ''.join('<span class="pchip %s">%s%s</span>' % (c, I(ic), t) for ic, t, c in fmts), I('play'), I('presentation'), I('folder-check'), I('check')))

# 5. Meeting Planner: books the easy ones, asks for the rest
save('s5_meet.html', CSS + m(MEET, 140, 400, 340, 'drop') + '''
<div class="bubble in-p b1" style="left:110px;top:200px">Internal ones I book myself.</div>
<div class="bubble in-p b2" style="left:110px;top:200px">Client ones wait for you.</div>
<div class="ccard in-p k1" style="left:800px;top:200px;width:460px;--cc:#3bdac0">
  <div class="cc-h"><span class="cc-av">%s</span><div><b>Team sync</b><span>Internal &middot; Zoom</span></div></div>
  <div class="cc-b"><small>%sThursday</small><span class="big">10:00 AM</span></div><span class="ok-badge ok1 in-p">%s</span></div>
<div class="ccard in-p k2" style="left:1320px;top:330px;width:460px;--cc:#20206e">
  <div class="cc-h"><span class="cc-av">%s</span><div><b>Client check-in</b><span>External &middot; Teams</span></div></div>
  <div class="cc-b"><small>%sWaiting on you</small><span class="big">Fri 2:00 PM</span>
  <div style="margin-top:16px"><span class="btnx navy appr" style="font-size:24px;padding:12px 26px">%sApprove</span></div></div><span class="ok-badge ok2 in-p">%s</span></div>
''' % (I('users'), I('calendar'), I('check'), I('briefcase'), I('hourglass'), I('check'), I('check')))

# 6. the whole office
stats = [('loader', 'Working right now', '2', BLUE), ('hand', 'Waiting on you', '3', NAVY), ('check-check', 'Done today', '12', '#1fa898')]
h = [CSS, '<div class="kin split mask k1" style="top:820px;font-size:76px;color:#141a3c">They do the work. <b>You make the calls.</b></div>']
for k, (ic, lab, n, col) in enumerate(stats):
    h.append('<div class="stat in-o s%d" style="left:%dpx;top:90px"><small style="color:%s">%s%s</small><div class="n c%d">0</div></div>' % (k, 260 + k * 480, col, I(ic), lab, k))
for k, (t, nm) in enumerate([(CHIEF, 'Chief of Staff'), (DRAFT, 'Reply Drafter'), (BOB, 'Bob De Builder'), (MEET, 'Meeting Planner')]):
    h.append(m(t, 210 + k * 400, 370, 250, 'drop t%d' % k, nm))
save('s6_office.html', '\n'.join(h))

# 7. Friday: close for the weekend
h = [CSS, '<div class="night nt"></div>']
for k, t in enumerate([CHIEF, DRAFT, BOB, MEET]):
    h.append(m(t, 210 + k * 400, 400, 250, 'z%d' % k))
    h.append('<div class="zz zs" style="left:%dpx;top:420px">z</div>' % (210 + k * 400 + 220))
h.append('<div style="position:absolute;left:0;right:0;top:170px;text-align:center"><span class="btnx navy cl" style="font-size:44px;padding:26px 54px;box-shadow:0 30px 60px -26px rgba(20,30,70,.6)">%sClose for the weekend</span></div>' % I('lock'))
h.append('<div class="kin split k1" style="top:860px;font-size:66px;color:#fff">Back on Monday, 7:00.</div>')
save('s7_weekend.html', '\n'.join(h))

# 8. end: the name in 3D
h = [CSS, '<div class="x3d splitc k1" style="position:absolute;left:0;right:0;top:250px;text-align:center;font-size:210px;color:#20206e">Agent Office</div>',
     '<div class="in-o sub" style="position:absolute;left:0;right:0;top:540px;text-align:center;font-size:40px;color:#3b4360;font-weight:600">My AI staff, built with Claude Code &middot; Metis Strategy</div>']
for k, t in enumerate([CHIEF, DRAFT, BOB, MEET]):
    h.append(m(t, 470 + k * 270, 660, 150, 'drop e%d' % k))
save('s8_end.html', '\n'.join(h))
print('scenes written to', D)
