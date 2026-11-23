/* Render QA for a narrative scroll, in real time at three viewports.
 *
 * Catches the failures that only appear once the page is actually painted:
 * horizontal overflow, an image that did not decode, an icon <use> pointing at
 * a sprite id that is not there, a webfont that never loaded, an entrance that
 * strands an element invisible, and a counter that never reaches its target.
 *
 *   node qa/qa-render.mjs <built file> [outPrefix]
 */
import { open, scratchDir, VIEWS, sleep } from "./_harness.mjs";
import { join } from "node:path";

const file = process.argv[2];
if (!file) {
  console.error("usage: node qa/qa-render.mjs <built file> [outPrefix]");
  process.exit(1);
}
const outDir = process.argv[3] || scratchDir("render");

const PROBE = `(() => {
  const de = document.documentElement, cw = de.clientWidth;

  const over = [];
  document.querySelectorAll("body *").forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) return;
    if (r.right + window.scrollX > cw + 1) {
      over.push({ over: Math.round(r.right + window.scrollX - cw),
        tag: el.tagName.toLowerCase() + (typeof el.className === "string" && el.className
          ? "." + el.className.trim().split(/\\s+/).slice(0,2).join(".") : "") });
    }
  });
  over.sort((a,b) => b.over - a.over);

  const counters = [...document.querySelectorAll("[data-count]")].map(el => ({
    shown: el.textContent, target: el.dataset.count,
    onScreen: (() => { const r = el.getBoundingClientRect();
      return r.top < innerHeight && r.bottom > 0; })(),
  }));

  // An entrance that armed but never resolved leaves the element invisible
  // while it sits in the middle of the viewport. That is the one failure a
  // reader definitely notices.
  const strandedHidden = [...document.querySelectorAll("[data-anim]")].filter(el => {
    const r = el.getBoundingClientRect();
    const inView = r.top < innerHeight * 0.9 && r.bottom > innerHeight * 0.1;
    return inView && parseFloat(getComputedStyle(el).opacity) < 0.9;
  }).map(el => el.tagName.toLowerCase() + "." +
      String(el.className).trim().split(/\\s+/).filter(c => c !== "in")[0]);

  const images = [...document.querySelectorAll("img")].map(im => {
    const r = im.getBoundingClientRect();
    return {
      alt: (im.alt || "(NO ALT)").slice(0, 40),
      natural: im.naturalWidth + "x" + im.naturalHeight,
      drawn: Math.round(r.width) + "x" + Math.round(r.height),
      ok: im.complete && im.naturalWidth > 0 && r.width > 1,
      noAlt: !im.alt,
    };
  });

  const uses = [...document.querySelectorAll("svg use")];
  const badUses = uses.filter(u => {
    const href = u.getAttribute("href") || "";
    return !href.startsWith("#") || !document.querySelector(href);
  }).map(u => u.getAttribute("href"));

  const icon = document.querySelector(".icn");
  const ics = icon ? getComputedStyle(icon) : null;

  return {
    clientWidth: cw, scrollWidth: de.scrollWidth, docHeight: de.scrollHeight,
    scrollY: Math.round(window.scrollY),
    overflow: de.scrollWidth > cw, overflowing: over.slice(0, 8),
    counters, strandedHidden, images, badUses, uses: uses.length,
    icons: document.querySelectorAll(".icn").length,
    iconFill: ics && ics.fill, iconStroke: ics && ics.stroke,
    fontLoaded: document.fonts ? document.fonts.check("700 16px 'Open Sans'") : null,
    lit: document.querySelectorAll(".eyebrow.lit,.band.lit").length,
    litTotal: document.querySelectorAll(".eyebrow,.band").length,
    mastOn: document.getElementById("mast")?.classList.contains("on") || false,
  };
})()`;

let problems = 0;
const flag = (msg) => { problems++; console.log("     ISSUE  " + msg); };

(async () => {
  const page = await open(file, 9341);
  console.log("\n================ RENDER QA ================");

  for (const v of VIEWS) {
    await page.view(v.w, v.h, !!v.mobile);

    const steps = [];
    steps.push({ at: "top", data: await page.evaluate(PROBE) });
    await page.shot(join(outDir, `${v.name}-1-top.png`));

    const H = await page.evaluate("document.documentElement.scrollHeight");
    const stops = [0.22, 0.42, 0.62, 0.82, 0.97];
    let i = 2;
    for (const f of stops) {
      await page.scrollTo(H * f);
      await sleep(600);
      steps.push({ at: f, data: await page.evaluate(PROBE) });
      await page.shot(join(outDir, `${v.name}-${i++}-at${String(f).replace("0.", "")}.png`));
    }
    // Back to the top: where a bidirectional reveal strands elements.
    await page.scrollTo(0);
    await sleep(700);
    steps.push({ at: "back-to-top", data: await page.evaluate(PROBE) });
    await page.shot(join(outDir, `${v.name}-${i++}-backtotop.png`));

    const first = steps[0].data;
    console.log(`\n--- ${v.name}  (${v.w}px viewport, doc ${first.docHeight}px) ---`);
    console.log("  horizontal overflow : " + (first.overflow ? "YES" : "no"));
    if (first.overflow) {
      first.overflowing.forEach(o => flag(`${o.tag} overflows by ${o.over}px`));
    }
    console.log(`  icons               : ${first.icons} in page, fill=${first.iconFill}, stroke=${first.iconStroke}`);
    console.log(`  <use> refs          : ${first.uses} total, ${first.badUses.length} unresolved`);
    first.badUses.forEach(h => flag(`icon reference ${h} resolves to nothing`));
    console.log("  Open Sans loaded    : " + first.fontLoaded);
    if (first.fontLoaded === false) flag("Open Sans did not load");

    first.images.forEach(im => {
      console.log(`     ${im.ok ? "ok " : "BAD"}  natural=${im.natural.padEnd(12)} drawn=${im.drawn.padEnd(12)} ${im.alt}`);
      if (!im.ok) flag(`image did not render: ${im.alt}`);
      if (im.noAlt) flag("image has no alt text");
    });

    for (const s of steps) {
      const d = s.data;
      const cs = d.counters.filter(c => c.onScreen)
        .map(c => `${c.shown}/${c.target}`).join(" ") || "(none on screen)";
      const reveals = d.strandedHidden.length
        ? "STRANDED: " + d.strandedHidden.join(", ") : "reveals ok";
      console.log(`  at ${String(s.at).padEnd(13)} y=${String(d.scrollY).padStart(5)}  mast=${d.mastOn ? "on " : "off"}  rules=${d.lit}/${d.litTotal}  counters=${cs}  ${reveals}`);
      if (d.strandedHidden.length) {
        flag(`${d.strandedHidden.length} element(s) stranded invisible at ${s.at} (${v.name})`);
      }
      d.counters.filter(c => c.onScreen && c.shown !== c.target).forEach(c => {
        // Mid-count is fine at a stop we just arrived at; only a settled
        // mismatch matters, and the 600ms settle above covers the run.
        flag(`counter shows ${c.shown} but targets ${c.target} at ${s.at} (${v.name})`);
      });
    }
  }

  await page.close();
  console.log(`\ncaptures: ${outDir}`);
  console.log(problems === 0
    ? "\nRENDER QA PASSED\n"
    : `\n${problems} ISSUE(S) FOUND\n`);
  process.exit(problems === 0 ? 0 : 1);
})().catch((e) => { console.error("HARNESS FAILED:", e.message); process.exit(2); });
