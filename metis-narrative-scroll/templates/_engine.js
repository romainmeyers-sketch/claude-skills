/* =========================================================================
   Motion. This is the Onboarding Hub's About Metis engine, ported: a single
   sweep over everything animated, in both directions, driven off the scroll
   frame rather than an observer.

   Bidirectional on purpose. A one shot reveal leaves a second pass down the
   page showing a wall of already revealed content, and shows nothing at all
   on the way back up, so leaving the band returns an element to its start
   state and the entrance runs in reverse.
   ========================================================================= */
(function(){
  "use strict";

  var FROM = {
    up:     "translateY(26px)",
    left:   "translateX(-30px)",
    right:  "translateX(30px)",
    scale:  "scale(1.055)",
    pop:    "scale(.9)",
    tilt:   "perspective(900px) rotateX(9deg) translateY(24px)",
    blur:   "translateY(14px)",
    wipe:   "scaleX(0)"
  };

  var still = window.matchMedia &&
              window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Every element this script touches, resolved before any branch can use it.
     buildRail() runs inside the reduced-motion early return below, so a lookup
     declared after that branch would be undefined when it fires. */
  var railEl  = document.getElementById("rail");
  var mast    = document.getElementById("mast");
  var mastBar = document.getElementById("mastBar");
  var stops   = [];

  var anims  = [].slice.call(document.querySelectorAll("[data-anim]"));
  var counts = [].slice.call(document.querySelectorAll("[data-count]"));
  var lits   = [].slice.call(document.querySelectorAll(".eyebrow, .band"));

  /* Reduced motion gets the finished page, counters included. */
  if(still){
    anims.forEach(function(el){ el.classList.add("in"); });
    counts.forEach(function(el){ el.textContent = fmt(+el.dataset.count); });
    lits.forEach(function(el){ el.classList.add("lit"); });
    buildRail(true);
    return;
  }

  /* A stagger on the parent orders its children; a delay on the element
     itself always wins, because the page uses both together. */
  document.querySelectorAll("[data-stagger]").forEach(function(p){
    var step = +p.dataset.stagger || 0;
    [].slice.call(p.children).forEach(function(c, i){
      var t = c.hasAttribute("data-anim") ? c : c.querySelector("[data-anim]");
      if(t && !t.hasAttribute("data-delay")) t.dataset.delay = i * step;
    });
  });

  anims.forEach(function(el){
    var kind = el.dataset.anim;
    el.style.opacity = "0";
    if(kind === "clip")        el.style.clipPath = "inset(0 100% 0 0)";
    else if(kind === "clipup") el.style.clipPath = "inset(100% 0 0 0)";
    else if(kind === "blur"){  el.style.filter = "blur(9px)";
                               el.style.transform = FROM.blur; }
    else if(kind === "wipe"){  el.style.transformOrigin = "left center";
                               el.style.transform = FROM.wipe; }
    else if(FROM[kind])        el.style.transform = FROM[kind];
  });
  requestAnimationFrame(function(){ document.body.classList.add("live"); });

  /* Arming happens BELOW the fold, not at it. An entrance is a stagger on top
     of an 850ms transition, so triggering it as the element crosses the
     viewport edge means a reader scrolling at any speed watches it arrive
     late. Starting 12% of a viewport early means the motion is already under
     way by the time the element is on screen, and the stagger is capped for
     the same reason.

     The release edge sits well outside the arming edge, or an element parked
     between the two flips state on every sub pixel scroll. */
  var ARM = 1.12, ARM_PX = 90, DELAY_CAP = 260;

  function gone(r, vh){
    return r.bottom < -(ARM_PX + 90) || r.top > vh * ARM + ARM_PX;
  }
  function fmt(n){ return String(n); }

  function sweep(){
    var vh = window.innerHeight;

    anims.forEach(function(el){
      var r = el.getBoundingClientRect();
      var shown = el.classList.contains("in");
      if(!shown && r.top < vh * ARM && r.bottom > -ARM_PX){
        clearTimeout(el._t);
        el._t = setTimeout(function(){ el.classList.add("in"); },
                           Math.min(+el.dataset.delay || 0, DELAY_CAP));
      } else if(shown && gone(r, vh)){
        /* Cancel a stagger still waiting to fire, or it lands after the
           element was sent back and strands it visible. */
        clearTimeout(el._t);
        el.classList.remove("in");
      }
    });

    /* The rule under a section label, and the closing band's wipe. One shot
       each: re-drawing a hairline on every pass is noise, not information. */
    lits.forEach(function(el){
      if(el.classList.contains("lit")) return;
      var r = el.getBoundingClientRect();
      if(r.top < vh * 1.02) el.classList.add("lit");
    });

    counts.forEach(function(el){
      var r = el.getBoundingClientRect();
      var counted = el.dataset.counted === "1";
      if(!counted && r.top < vh * 1.02 && r.bottom > -ARM_PX){
        el.dataset.counted = "1";
        run(el);
      } else if(counted && gone(r, vh)){
        el.dataset.counted = "";
        el._seq = (el._seq || 0) + 1;   /* strands any run still in flight */
        el.textContent = "0";
      }
    });

    railSync();
    mastSync();
  }

  /* Count up on an ease out, so it decelerates into the real number instead
     of ticking at a constant rate. */
  function run(el){
    var target = +el.dataset.count || 0;
    var seq = el._seq = (el._seq || 0) + 1;
    var dur = 1000 + Math.min(target, 120) * 5;
    var t0 = null;
    function frame(t){
      if(el._seq !== seq) return;
      if(t0 === null) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(target * e));
      if(p < 1) requestAnimationFrame(frame);
      else el.textContent = fmt(target);
    }
    requestAnimationFrame(frame);
  }

  /* ---- masthead: appears once the hero is behind you, and carries the read
          progress on its lower edge. ---- */
  function mastSync(){
    var hero = document.getElementById("top");
    var past = hero ? hero.getBoundingClientRect().bottom < 40 : false;
    mast.classList.toggle("on", past);
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(Math.max(window.scrollY / max, 0), 1) : 0;
    mastBar.style.transform = "scaleX(" + p + ")";
  }

  /* ---- the rail, built from the sections that declare a name ---- */
  function buildRail(reducedMotion){
    var secs = [].slice.call(document.querySelectorAll("[data-rail]"));
    if(!secs.length || !railEl) return;
    var prog = document.createElement("span");
    prog.className = "rail-prog";
    prog.innerHTML = "<i></i>";
    var list = document.createElement("div");
    list.className = "rail-list";

    secs.forEach(function(s, i){
      var b = document.createElement("button");
      b.className = "rail-b";
      b.style.setProperty("--i", i);
      b.type = "button";
      b.setAttribute("aria-label", "Jump to " + s.dataset.rail);
      b.innerHTML =
        '<span class="rail-lab"><span class="rail-n">' +
        String(i + 1).padStart(2, "0") +
        '</span><span class="rail-t"></span></span><span class="rail-tick"></span>';
      b.querySelector(".rail-t").textContent = s.dataset.rail;
      b.addEventListener("click", function(){
        b.classList.add("going");
        setTimeout(function(){ b.classList.remove("going"); }, 520);
        s.scrollIntoView({behavior: reducedMotion ? "auto" : "smooth", block: "start"});
      });
      list.appendChild(b);
      stops.push({sec: s, btn: b});
    });

    railEl.appendChild(prog);
    railEl.appendChild(list);
    railEl._fill = prog.querySelector("i");

    requestAnimationFrame(function(){
      railEl.classList.add("on", "ready");
      if(reducedMotion) return;
      /* One authored moment: the rail introduces itself once, then gets out
         of the way. Without it a reader has no reason to know the ticks are
         navigation at all. */
      setTimeout(function(){ railEl.classList.add("peek"); }, 900);
      setTimeout(function(){ railEl.classList.remove("peek"); }, 3100);
    });
  }

  function railSync(){
    if(!stops.length) return;
    var mid = window.innerHeight * 0.42, cur = -1;
    stops.forEach(function(st, i){
      var r = st.sec.getBoundingClientRect();
      if(r.top <= mid && r.bottom > mid) cur = i;
    });
    if(cur < 0){
      var first = stops[0].sec.getBoundingClientRect();
      if(first.top > mid) cur = -1;
      else cur = stops.length - 1;
    }
    stops.forEach(function(st, i){
      if(i === cur) st.btn.setAttribute("aria-current", "true");
      else st.btn.removeAttribute("aria-current");
    });
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(Math.max(window.scrollY / max, 0), 1) : 0;
    if(railEl._fill) railEl._fill.style.height = (p * 100) + "%";
  }

  buildRail(false);

  /* ---- the jump rows in "Inside this note" ---- */
  document.querySelectorAll("[data-jump]").forEach(function(b){
    b.addEventListener("click", function(){
      var t = document.getElementById(b.dataset.jump);
      /* Land at the top of the target section and nowhere else. */
      if(t) t.scrollIntoView({behavior: "smooth", block: "start"});
    });
  });

  /* One rAF coalesced sweep per frame, shared by the entrances, the counters,
     the rail and the masthead, so they all read one set of rects. */
  var queued = false;
  function onScroll(){
    if(queued) return;
    queued = true;
    requestAnimationFrame(function(){ queued = false; sweep(); });
  }
  window.addEventListener("scroll", onScroll, {passive: true});
  window.addEventListener("resize", onScroll);
  sweep();
  /* Images settle after first paint and move everything below them, so the
     rects measured at load are wrong within a second. */
  window.addEventListener("load", function(){ sweep(); setTimeout(sweep, 300); });
})();
