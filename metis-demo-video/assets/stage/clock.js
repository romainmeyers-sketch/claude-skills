/* Injected into every frame (stage, app, page images) before any page script runs.
   A frozen clock: nothing moves until the renderer calls __step(ms). Timers, animation
   frames, Date, performance.now and every CSS animation/transition advance by exactly that
   much, so each captured frame is perfect however slow the machine is. */
(() => {
  if (window.__step) return;
  const FAKE_DATE = window.__FAKE_DATE__ || null;          // set by the renderer, e.g. '2026-11-04T09:30:00'
  const RealDate = Date, base = FAKE_DATE ? new RealDate(FAKE_DATE).getTime() : RealDate.now();
  let now = 0, seq = 1;
  const timers = new Map(), rafs = new Map(), starts = new WeakMap();
  window.setTimeout = (fn, ms, ...a) => { const i = seq++; timers.set(i, {t: now + Math.max(0, +ms || 0), fn, a}); return i; };
  window.setInterval = (fn, ms, ...a) => { const i = seq++, iv = Math.max(1, +ms || 0); timers.set(i, {t: now + iv, fn, a, iv}); return i; };
  window.clearTimeout = window.clearInterval = i => timers.delete(i);
  window.requestAnimationFrame = fn => { const i = seq++; rafs.set(i, fn); return i; };
  window.cancelAnimationFrame = i => rafs.delete(i);
  performance.now = () => now;
  class D extends RealDate { constructor(...a){ a.length ? super(...a) : super(base + now); } static now(){ return base + now; } }
  window.Date = D;
  const run = f => { try { f(); } catch (e) { console.error(e); } };
  window.__step = (dt) => {
    const end = now + dt;
    for (let guard = 0; guard < 500; guard++) {
      let id = null, t = null;
      for (const [i, x] of timers) if (x.t <= end && (!t || x.t < t.t)) { id = i; t = x; }
      if (!t) break;
      now = Math.max(now, t.t);
      if (t.iv) t.t += t.iv; else timers.delete(id);
      run(() => t.fn(...t.a));
    }
    now = end;
    const cbs = [...rafs.values()]; rafs.clear(); cbs.forEach(f => run(() => f(now)));
    for (const a of document.getAnimations()) {
      if (!starts.has(a)) starts.set(a, now - (a.currentTime || 0));
      a.pause(); a.currentTime = now - starts.get(a);
    }
  };

  /* inside the app frame only: a cursor, click ripples, scripted scrolling */
  let fe = null; try { fe = window.frameElement; } catch (e) {}
  if (!fe || fe.id !== 'app') return;
  const css = `#__cur{position:fixed;left:0;top:0;width:26px;height:26px;z-index:2147483647;pointer-events:none;transition:transform .7s cubic-bezier(.22,.8,.3,1);filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))}
    .__ripple{position:fixed;width:52px;height:52px;margin:-26px 0 0 -26px;border-radius:50%;border:3px solid var(--demo-accent,#f49813);z-index:2147483646;pointer-events:none;animation:__rip .6s ease-out forwards}
    @keyframes __rip{from{transform:scale(.3);opacity:1}to{transform:scale(1.5);opacity:0}}`;
  function boot(){
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
    const c = document.createElement('div'); c.id = '__cur';
    c.innerHTML = '<svg viewBox="0 0 24 24" width="26" height="26"><path d="M4 2l15 11-6.5 1.3L16 21l-3 1.4-3.4-6.8L4 19z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    c.style.transform = 'translate(' + (innerWidth * .66) + 'px,' + (innerHeight * .68) + 'px)';
    document.body.appendChild(c);
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', boot) : boot();
  window.__cursor = (x, y, ms) => { const c = document.getElementById('__cur'); if (!c) return; c.style.transitionDuration = ms + 'ms'; c.style.transform = 'translate(' + x + 'px,' + y + 'px)'; };
  window.__ripple = (x, y) => { const r = document.createElement('div'); r.className = '__ripple'; r.style.left = x + 'px'; r.style.top = y + 'px'; document.body.appendChild(r); setTimeout(() => r.remove(), 700); };
  window.__scroll = (dy, ms) => { const y0 = scrollY, t0 = performance.now();
    (function step(t){ const p = Math.min((t - t0) / ms, 1), e = p < .5 ? 2*p*p : 1 - Math.pow(-2*p + 2, 2) / 2; window.scrollTo({top: y0 + dy * e, behavior: 'instant'}); if (p < 1) requestAnimationFrame(step); })(t0); };
})();
