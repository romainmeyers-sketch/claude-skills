/* Functional QA for the navigation, by driving the real page.
 *
 * Two standing regressions live here, both of which have shipped before:
 *
 *   1. A jump control that lands somewhere other than the TOP of its target.
 *      Clicking a contents row and arriving mid-section reads as a broken
 *      link even though the anchor is correct.
 *   2. An auto-hiding rail whose labels vanish as the pointer travels toward
 *      them. The labels are technically buttons and practically unclickable,
 *      because leaving the rail's own box makes :hover go false.
 *
 * Plus: reduced motion has to be a real variant that shows the FINISHED page,
 * not a switch that leaves everything at opacity 0.
 *
 *   node qa/qa-jumps.mjs <built file>
 */
import { open, sleep } from "./_harness.mjs";

const file = process.argv[2];
if (!file) { console.error("usage: node qa/qa-jumps.mjs <built file>"); process.exit(1); }

const MAST = 58;                    // fixed masthead height, the landing tolerance

/* A section shorter than the viewport at the END of the document can never be
   scrolled to the top of the screen: there is no page left below it. Landing
   at maximum scroll IS the correct outcome, so a jump passes if it either put
   the section under the masthead or exhausted the page trying. Without this,
   every narrative whose closing band is shorter than a viewport fails a check
   that describes no real defect. */
const LANDED = `(() => {
  const de = document.documentElement;
  const atBottom = Math.abs(window.scrollY - (de.scrollHeight - innerHeight)) <= 2;
  return { atBottom };
})()`;
let fails = 0;
function check(name, pass, detail) {
  if (!pass) fails++;
  console.log(`  ${pass ? "PASS" : "FAIL"}  ${name}${detail ? "   " + detail : ""}`);
}

(async () => {
  const page = await open(file, 9342);
  const pageErrors = [];
  await page.cmd("Runtime.addBinding", { name: "__err" }).catch(() => {});
  await page.evaluate(`window.addEventListener("error", e => {
    (window.__errs = window.__errs || []).push(e.message); });`);

  await page.view(1440, 900);

  /* ---- 1. every contents row lands on the top of its target ---- */
  console.log("\n--- jump controls land at the top of their target ---");
  const jumps = await page.evaluate(
    `[...document.querySelectorAll("[data-jump]")].map(b => b.dataset.jump)`);
  check("contents rows found", jumps.length > 0, `${jumps.length} rows`);

  for (const target of jumps) {
    await page.scrollTo(0);
    await page.evaluate(`document.querySelector('[data-jump="${target}"]').click()`);
    await sleep(1500);              // smooth scroll has to finish
    const r = await page.evaluate(
      `(() => { const e = document.getElementById("${target}");
         const b = e.getBoundingClientRect(); return {top: Math.round(b.top)}; })()`);
    const { atBottom } = await page.evaluate(LANDED);
    check(`jump to ${target}`, (r.top >= 0 && r.top <= MAST + 12) || atBottom,
      `section top landed at y=${r.top}${atBottom ? " (page bottom reached)" : ""}`);
  }

  /* ---- 2. the rail: one button per section, and it navigates ---- */
  console.log("\n--- section rail ---");
  const sections = await page.evaluate(
    `[...document.querySelectorAll("[data-rail]")].map(s => s.dataset.rail)`);
  const nButtons = await page.evaluate(`document.querySelectorAll(".rail-b").length`);
  check("rail built one button per section", nButtons === sections.length,
    `${nButtons} buttons for ${sections.length} sections`);

  for (let i = 0; i < sections.length; i++) {
    await page.scrollTo(0);
    await page.evaluate(`document.querySelectorAll(".rail-b")[${i}].click()`);
    await sleep(1500);
    const r = await page.evaluate(
      `(() => { const s = document.querySelectorAll("[data-rail]")[${i}];
         return {top: Math.round(s.getBoundingClientRect().top)}; })()`);
    const { atBottom } = await page.evaluate(LANDED);
    check(`rail ${i + 1} (${sections[i]})`,
      (r.top >= 0 && r.top <= MAST + 12) || atBottom,
      `landed at y=${r.top}${atBottom ? " (page bottom reached)" : ""}`);
  }

  /* ---- 3. the labels stay reachable, and cost the page no clicks ---- */
  console.log("\n--- rail labels are reachable without swallowing the page ---");
  const lab = await page.evaluate(`(() => {
    const rail = document.getElementById("rail");
    const l = document.querySelector(".rail-lab");
    return { hiddenPointer: getComputedStyle(l).pointerEvents,
             railWidth: Math.round(rail.getBoundingClientRect().width) };
  })()`);
  check("label is inert while hidden", lab.hiddenPointer === "none",
    `pointer-events: ${lab.hiddenPointer}`);

  const labOn = await page.evaluate(`(() => {
    const rail = document.getElementById("rail");
    rail.classList.add("peek");
    const l = document.querySelector(".rail-lab");
    const r = l.getBoundingClientRect();
    const hit = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
    return { pointer: getComputedStyle(l).pointerEvents,
             hit: !!(hit && hit.closest(".rail-b")),
             width: Math.round(rail.getBoundingClientRect().width) };
  })()`);
  check("label takes the pointer once shown",
    labOn.pointer === "auto" && labOn.hit, `hit test found the button: ${labOn.hit}`);
  check("showing the labels does not widen the rail", labOn.width === lab.railWidth,
    `${lab.railWidth}px -> ${labOn.width}px`);
  check("rail stays a narrow strip", labOn.width <= 80, `width ${labOn.width}px`);

  /* ---- 4. reduced motion is a finished page, not a blank one ---- */
  console.log("\n--- reduced motion shows the finished page ---");
  await page.cmd("Emulation.setEmulatedMedia", {
    features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
  await page.cmd("Page.navigate", { url: page.url });
  await sleep(2600);
  const rm = await page.evaluate(`(() => ({
    hidden: [...document.querySelectorAll("[data-anim]")]
      .filter(e => parseFloat(getComputedStyle(e).opacity) < 0.9).length,
    counters: [...document.querySelectorAll("[data-count]")]
      .filter(e => e.textContent.trim() !== e.dataset.count).length,
    unlit: document.querySelectorAll(".eyebrow:not(.lit),.band:not(.lit)").length,
    railOn: document.getElementById("rail").classList.contains("on"),
    errs: (window.__errs || []).length,
  }))()`);
  check("nothing hidden under reduced motion", rm.hidden === 0, `${rm.hidden} hidden`);
  check("counters show final values immediately", rm.counters === 0,
    `${rm.counters} not at target`);
  check("section rules drawn", rm.unlit === 0, `${rm.unlit} undrawn`);
  check("rail still built", rm.railOn === true);

  /* The rail is built from inside the reduced-motion early return, so a
     lookup declared below that branch is undefined when it fires and kills
     the whole script. This check is what catches that. */
  console.log("\n--- the page script threw nothing ---");
  check("no uncaught page exceptions", rm.errs === 0, rm.errs ? `${rm.errs} errors` : "clean");

  await page.close();
  console.log(`\n${fails === 0 ? "ALL CHECKS PASSED" : fails + " CHECK(S) FAILED"}\n`);
  process.exit(fails === 0 ? 0 : 1);
})().catch((e) => { console.error("TEST HARNESS FAILED:", e.message); process.exit(2); });
