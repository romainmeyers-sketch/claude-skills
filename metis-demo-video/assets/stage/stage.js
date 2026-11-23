/* Stage controls called by render.py. All timers run on the frozen clock (clock.js). */
const $ = s => document.querySelector(s);
const CFG = window.__STAGE__;                    // {aw, ah, ch, fitScale} written by render.py

function scene(id, on){
  const el = $('#' + id); if (!el) return;
  if (on && window.__instant){                     // under a flood: appear at once, the flood is the transition
    window.__instant = false; el.style.transition = 'none'; el.classList.remove('out'); el.classList.add('on'); void el.offsetWidth; el.style.transition = ''; return; }
  if (on){ el.classList.remove('out'); el.classList.add('on'); }
  else { el.classList.add('out'); setTimeout(() => el.classList.remove('on', 'out'), 700); }
}
/* caption: the pill stays solid while one caption replaces another; only the text crossfades,
   so the app never shows through a half-faded pill */
function cap(t){
  const c = $('#cap'); if (!t){ c.classList.remove('on'); return; }
  let s = c.querySelector('.ct');
  if (!s){ c.textContent = ''; s = document.createElement('span'); s.className = 'ct'; c.appendChild(s); }
  if (c.classList.contains('on')){ s.classList.add('swap'); setTimeout(() => { s.textContent = t; s.classList.remove('swap'); }, 220); }
  else { s.textContent = t; c.classList.add('on'); }
}
function note(d){
  const n = $('#note'); if (!d){ n.classList.remove('on'); return; }
  n.querySelector('.av').textContent = d.initials || '';
  n.querySelector('b').textContent = d.title || '';
  n.querySelector('span').textContent = d.body || '';
  n.classList.add('on');
}

/* camera over the app window */
function rig(on){ $('#rig').classList.toggle('on', !!on); }
function dim(on){ $('#rig').classList.toggle('dim', !!on); }
function tilt(rx, ry, rz, ms){ const t = $('#tilt'); t.style.transitionDuration = (ms || 1400) + 'ms';
  t.style.transform = 'perspective(2400px) rotateX(' + (rx || 0) + 'deg) rotateY(' + (ry || 0) + 'deg) rotateZ(' + (rz || 0) + 'deg)'; }
/* put app point (px,py) at stage point (cx,cy), at scale s */
function cam(px, py, s, ms, cx, cy){ const w = $('#win'); w.style.transitionDuration = (ms || 1200) + 'ms';
  cx = cx == null ? 960 : cx; cy = cy == null ? 520 : cy;
  w.style.transform = 'translate(' + (cx - s * px) + 'px,' + (cy - s * (CFG.ch + py)) + 'px) scale(' + s + ')'; }
function fit(ms){ cam(CFG.aw / 2, CFG.ah / 2 - CFG.ch / 2, CFG.fitScale, ms, 960, CFG.fitCy || 500); }

/* hook: words pop in at given times (ms from now); the camera keeps the newest word in view */
function follow(box){ const w = box.querySelector('.txt').offsetWidth || 1;
  const s = 1.2 - Math.min(w, 1800) / 1800 * 0.24, vis = w * s, cx = vis < 1150 ? (1920 - vis) / 2 : 1920 * 0.66 - vis;
  box.style.transform = 'translate(' + cx + 'px,-50%) scale(' + s + ')'; }
function fitBox(box){ const w = box.querySelector('.txt').offsetWidth || 1, s = Math.min(1.05, 1680 / w);
  box.style.transition = 'transform .7s cubic-bezier(.2,.7,.2,1)';
  box.style.transform = 'translate(' + ((1920 - w * s) / 2) + 'px,-50%) scale(' + s + ')'; }
function typeTimed(id, words, times){        /* words: [[text, bold]] */
  const box = $('#' + id), t = box.querySelector('.txt');
  t.innerHTML = words.map(w => '<span class="wd' + (w[1] ? ' bd' : '') + '"></span>').join('');
  const els = [...t.querySelectorAll('.wd')];
  els.forEach((el, j) => { el.textContent = words[j][0];
    setTimeout(() => { el.classList.add('in'); follow(box); if (j === els.length - 1) setTimeout(() => fitBox(box), 420); }, times[j]); });
}
/* multi-line hook: once the last word lands, bring every line back and show the whole question, stacked and centred */
function hookStack(){
  const rows = [...document.querySelectorAll('#s-hook .row')]; if (rows.length < 2) return;
  const ws = rows.map(r => r.querySelector('.txt').offsetWidth || 1);
  const s = Math.min(0.9, 1680 / Math.max(...ws)), lh = 182 * s;
  rows.forEach((r, k) => {
    const box = r.querySelector('.tw'), c = box.querySelector('.caret');
    r.classList.remove('gone'); r.style.opacity = 1; r.style.filter = 'none';
    r.style.transform = 'translateY(' + ((k - (rows.length - 1) / 2) * lh) + 'px)';
    if (c && k < rows.length - 1) c.style.display = 'none';
    box.style.transition = 'transform .8s cubic-bezier(.2,.7,.2,1)';
    box.style.transform = 'translate(' + ((1920 - ws[k] * s) / 2) + 'px,-50%) scale(' + s + ')';
  });
}
function hookSwitch(ms){ setTimeout(() => { $('#row1').classList.add('gone'); const c = $('#tw1 .caret'); if (c) c.style.display = 'none'; $('#s-hook').classList.add('two'); }, ms); }

/* reveal */
function meet(on){ const m = $('#meet'); m.classList.toggle('on', on === true); m.classList.toggle('off', on === false); }
function logo(on){ $('#s-reveal').classList.toggle('logo-on', !!on); }
function pillTimed(times){ [...document.querySelectorAll('#ptxt .pw')].forEach((p, j) => setTimeout(() => p.classList.add('in'), times[j])); }

/* frames scrolling elements into view must never move the stage */
addEventListener('scroll', () => { if (scrollX || scrollY) scrollTo(0, 0); }, true);

/* prompt: type text one character at a time, then press send */
function promptType(id, text, ms, sendAt){
  const t = $('#' + id + ' .pr-txt .t'), ph = $('#' + id + ' .pr-txt .ph');
  [...text].forEach((ch, i) => setTimeout(() => { if (ph) ph.remove(); t.textContent = text.slice(0, i + 1); }, i * ms));
  setTimeout(() => { $('#' + id + ' .pr-send').classList.add('press'); }, sendAt);
  setTimeout(() => { $('#' + id + ' .pr-send').classList.remove('press'); $('#' + id + ' .pr-box').classList.add('sent'); }, sendAt + 260);
}
/* beats: show word j at times[j], hide the previous one */
function beatsTimed(id, times){
  const els = [...document.querySelectorAll('#' + id + ' .bt')];
  els.forEach((el, j) => setTimeout(() => { if (j) { els[j - 1].classList.remove('in'); els[j - 1].classList.add('gone'); } el.classList.add('in'); }, times[j]));
}

/* environments */
function setBg(v){ $('#bg').className = v ? 'bgv bg-' + v : ''; }
/* chat: show item j at times[j]; then a cursor clicks the last link card and the camera dives into it */
function chatTimed(id, times){ [...document.querySelectorAll('#' + id + ' .ch-body > *')].forEach((e, j) => setTimeout(() => e.classList.add('in'), times[j])); }
function chatClick(id){
  const s = $('#' + id), cards = s.querySelectorAll('.ch-card'), card = cards[cards.length - 1]; if (!card) return;
  const r = card.getBoundingClientRect(), c = s.querySelector('.ccur');
  c.classList.add('on'); c.style.transform = 'translate(' + (r.left + r.width * 0.35) + 'px,' + (r.top + r.height * 0.5) + 'px)';
  setTimeout(() => card.classList.add('press'), 1000);
  setTimeout(() => { card.classList.remove('press'); s.style.transformOrigin = (r.left + r.width / 2) + 'px ' + (r.top + r.height / 2) + 'px'; s.classList.add('dive'); }, 1250);
}
function devPush(id){ $('#' + id + ' .dev').classList.add('push'); }
function arcWipe(){ const w = $('#wipe'); if (!w) return; w.classList.remove('go'); void w.offsetWidth; w.classList.add('go'); }
function phoneTurn(id){ $('#' + id + ' .phone').classList.add('turn'); }
function stripeWipe(){ const w = $('#stripe'); if (!w) return; w.classList.remove('go'); void w.offsetWidth; w.classList.add('go'); }

function gpClick(id){
  const s = $('#' + id), p = s.querySelector('.gpill'), h = s.querySelector('.gp-hand'), r = p.getBoundingClientRect();
  h.classList.add('on'); h.style.transform = 'translate(' + (r.left + r.width * 0.62) + 'px,' + (r.top + r.height * 0.42) + 'px) rotate(-8deg)';
  setTimeout(() => p.classList.add('press'), 1000);
  setTimeout(() => { p.classList.remove('press'); s.style.transformOrigin = (r.left + r.width / 2) + 'px ' + (r.top + r.height / 2) + 'px'; s.classList.add('dive'); }, 1220);
}

/* ---------- motion scenes (v1.2): a world under its own camera, driven by timed events from render.py ---------- */
const EASE = {inout: 'cubic-bezier(.65,0,.35,1)', out: 'cubic-bezier(.2,.8,.2,1)', in: 'cubic-bezier(.6,0,.8,.4)', linear: 'linear', soft: 'cubic-bezier(.45,0,.25,1)'};
/* world position of an element (sum of offsets up to the world), so camera and cursor ignore any transforms */
function wpos(el, world){ let x = 0, y = 0, e = el;
  while (e && e !== world){ x += e.offsetLeft; y += e.offsetTop; e = e.offsetParent; }
  return [x + el.offsetWidth / 2, y + el.offsetHeight / 2, el.offsetWidth, el.offsetHeight]; }
/* k = {x, y, s, rx, ry, rz, ms, ease, at: [sx, sy] (screen point to put x,y on), focus: selector} */
function mcam(id, k){
  const sc = $('#' + id), mt = sc.querySelector('.mt'), mc = sc.querySelector('.mc');
  const st = sc.__cam || (sc.__cam = {x: 960, y: 540, s: 1, rx: 0, ry: 0, rz: 0});
  if (k.focus){ const el = sc.querySelector(k.focus); if (el){ const p = wpos(el, mc); st.x = p[0]; st.y = p[1]; } }
  ['x', 'y', 's', 'rx', 'ry', 'rz'].forEach(n => { if (k[n] != null) st[n] = k[n]; });
  const ms = k.ms == null ? 1400 : k.ms, ez = EASE[k.ease || 'inout'] || k.ease, at = k.at || [960, 540];
  [mt, mc].forEach(e => { e.style.transitionDuration = ms + 'ms'; e.style.transitionTimingFunction = ez; });
  mt.style.transform = 'perspective(' + (k.persp || 2200) + 'px) rotateX(' + st.rx + 'deg) rotateY(' + st.ry + 'deg) rotateZ(' + st.rz + 'deg)';
  mc.style.transform = 'translate(' + (at[0] - st.s * st.x) + 'px,' + (at[1] - st.s * st.y) + 'px) scale(' + st.s + ')';
}
function mcls(id, sel, cls, on){ document.querySelectorAll('#' + id + ' ' + sel).forEach(e => e.classList.toggle(cls || 'in', on !== false)); }
function mstagger(id, sel, gap, cls){ [...document.querySelectorAll('#' + id + ' ' + sel)].forEach((e, j) => setTimeout(() => e.classList.add(cls || 'in'), j * gap)); }
/* the world cursor glides to an element, presses it and leaves a ripple */
function mclick(id, sel, ms){
  const sc = $('#' + id), mc = sc.querySelector('.mc'), el = sc.querySelector(sel), c = sc.querySelector('.mcur'); if (!el || !c) return;
  const p = wpos(el, mc); ms = ms || 700;
  c.style.transition = 'opacity .3s, transform ' + ms + 'ms cubic-bezier(.3,0,.2,1)';
  if (!c.classList.contains('on')){ c.style.transition = 'none'; c.style.transform = 'translate(' + (p[0] + 260) + 'px,' + (p[1] + 220) + 'px)'; void c.offsetWidth;
    c.style.transition = 'opacity .3s, transform ' + ms + 'ms cubic-bezier(.3,0,.2,1)'; c.classList.add('on'); }
  c.style.transform = 'translate(' + (p[0] - 6) + 'px,' + (p[1] - 4) + 'px)';
  setTimeout(() => { el.classList.add('press-me', 'pressed'); const r = document.createElement('div'); r.className = 'mrip';
    r.style.left = p[0] + 'px'; r.style.top = p[1] + 'px'; mc.appendChild(r); setTimeout(() => r.remove(), 800); }, ms);
  setTimeout(() => el.classList.remove('pressed'), ms + 180);
}
/* count a number up inside an element: "78%" */
function mcount(id, sel, to, ms, pre, suf, dec){
  const el = $('#' + id + ' ' + sel); if (!el) return; const t0 = performance.now();
  (function k(t){ const p = Math.min((t - t0) / ms, 1), e = 1 - Math.pow(1 - p, 3);
    el.textContent = (pre || '') + (to * e).toLocaleString('en-US', {minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0}) + (suf || ''); if (p < 1) requestAnimationFrame(k); })(t0);
}
/* set a CSS property with a transition (bars that fill, lines that draw) */
function mstyle(id, sel, prop, val, ms){ document.querySelectorAll('#' + id + ' ' + sel).forEach(e => { e.style.transitionDuration = (ms || 1200) + 'ms'; e.style[prop] = val; }); }
/* words blur in one by one */
function mwords(id, sel, gap){ [...document.querySelectorAll('#' + id + ' ' + sel + ' .kw')].forEach((w, j) => setTimeout(() => w.classList.add('in'), j * (gap || 140))); }
/* class "split" on any element: wrap each word in a .kw span so mwords() can blur them in one by one */
function splitWords(root){ [...root.childNodes].forEach(n => {
  if (n.nodeType === 3){ const f = document.createDocumentFragment();
    n.textContent.split(/(\s+)/).forEach(p => { if (!p) return;
      if (/^\s+$/.test(p)) f.appendChild(document.createTextNode(p));
      else { const s = document.createElement('span'); s.className = 'kw'; s.textContent = p; f.appendChild(s); } });
    n.replaceWith(f); }
  else if (n.nodeType === 1 && !n.classList.contains('kw')) splitWords(n); }); }
document.querySelectorAll('.split').forEach(splitWords);
/* class "splitc": one .kw per letter (for titles that drop in letter by letter) */
document.querySelectorAll('.splitc').forEach(el => { const t = el.textContent; el.textContent = '';
  [...t].forEach(ch => { const s = document.createElement('span'); s.className = 'kw'; s.textContent = ch === ' ' ? ' ' : ch; el.appendChild(s); }); });

/* ---------- v1.4: springs, flood transition, mask-line text, morphing shape ---------- */
/* springs as CSS easing: a closed-form damped spring sampled into linear(); "spring" has a small overshoot,
   "spring-soft" none. Use as ease: "spring" in camera moves, or var(--spring) in CSS transitions. */
function springEase(zeta, w){ const pts = [];
  for (let i = 0; i <= 40; i++){ const t = i / 40, T = t * w;
    const v = zeta < 1 ? 1 - Math.exp(-zeta * T) * (Math.cos(Math.sqrt(1 - zeta * zeta) * T) + zeta / Math.sqrt(1 - zeta * zeta) * Math.sin(Math.sqrt(1 - zeta * zeta) * T))
                       : 1 - Math.exp(-T) * (1 + T);
    pts.push((i === 40 ? 1 : v).toFixed(4)); }
  return 'linear(' + pts.join(',') + ')'; }
EASE.spring = springEase(0.62, 11); EASE['spring-soft'] = springEase(1, 9);
document.documentElement.style.setProperty('--spring', EASE.spring);
document.documentElement.style.setProperty('--spring-soft', EASE['spring-soft']);

/* flood: a shape grows from a point until it covers the frame (overscaled past the corners), the scene changes
   under it, then it contracts toward a point in the next scene. */
function floodIn(x, y, color, ms){
  const f = $('#flood'); if (!f) return; const d = Math.hypot(Math.max(x, 1920 - x), Math.max(y, 1080 - y)) * 2.3;
  f.style.transition = 'none'; f.style.background = color; f.style.left = x + 'px'; f.style.top = y + 'px';
  f.style.width = f.style.height = d + 'px'; f.style.transform = 'translate(-50%,-50%) scale(0)'; f.style.opacity = 1; void f.offsetWidth;
  f.style.transition = 'transform ' + ms + 'ms cubic-bezier(.7,0,.2,1)'; f.style.transform = 'translate(-50%,-50%) scale(1)'; }
function floodOut(x, y, ms){
  const f = $('#flood'); if (!f) return; const d = Math.hypot(Math.max(x, 1920 - x), Math.max(y, 1080 - y)) * 2.3;
  f.style.transition = 'none'; f.style.left = x + 'px'; f.style.top = y + 'px'; f.style.width = f.style.height = d + 'px'; void f.offsetWidth;
  f.style.transition = 'transform ' + ms + 'ms cubic-bezier(.6,0,.3,1)'; f.style.transform = 'translate(-50%,-50%) scale(0)'; }

/* class "mask" on a .split element: each word rises out of its own mask line instead of blurring in */
document.querySelectorAll('.mask').forEach(el => el.querySelectorAll('.kw').forEach(w => {
  const m = document.createElement('span'); m.className = 'mw'; w.replaceWith(m); m.appendChild(w); }));

/* morph: one shape that changes size, radius and colour on a spring while its content swaps with its own mask.
   to = {w, h, r, bg, color, html} (any subset) */
function morph(id, sel, to, ms){
  const el = $('#' + id + ' ' + sel); if (!el) return; ms = ms || 700;
  el.style.transition = ['width', 'height', 'border-radius', 'background-color', 'color', 'left', 'top']
    .map(p => p + ' ' + ms + 'ms ' + EASE.spring).join(',');
  if (to.w != null) el.style.width = to.w + 'px'; if (to.h != null) el.style.height = to.h + 'px';
  if (to.r != null) el.style.borderRadius = to.r + 'px'; if (to.bg) el.style.backgroundColor = to.bg; if (to.color) el.style.color = to.color;
  if (to.x != null) el.style.left = to.x + 'px'; if (to.y != null) el.style.top = to.y + 'px';
  if (to.html != null){
    const old = el.querySelector('.mo-c'), nu = document.createElement('div'); nu.className = 'mo-c enter'; nu.innerHTML = to.html;
    if (window.lucide) lucide.createIcons({icons: lucide.icons, root: nu});
    el.appendChild(nu); void nu.offsetWidth; nu.classList.remove('enter');
    if (old){ old.classList.add('leave'); setTimeout(() => old.remove(), 450); } }
}

/* move: a character (or any element) travels across the world to (x, y) in ms; it walks while moving
   and looks the way it is going. Pair it with a "cam" of the same ms so the camera travels with it. */
function mmove(id, sel, x, y, ms){
  const el = $('#' + id + ' ' + sel); if (!el) return; ms = ms || 1600;
  const x0 = el.offsetLeft, dir = x > x0 ? 'look-r' : x < x0 ? 'look-l' : '';
  el.style.transition = 'left ' + ms + 'ms cubic-bezier(.45,0,.3,1), top ' + ms + 'ms cubic-bezier(.45,0,.3,1)';
  el.classList.add('walk'); if (dir) el.classList.add(dir);
  el.style.left = x + 'px'; el.style.top = y + 'px';
  setTimeout(() => { el.classList.remove('walk'); if (dir) el.classList.remove(dir); }, ms);
}
