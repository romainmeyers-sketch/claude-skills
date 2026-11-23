/* Spacing and rhythm QA.
 *
 * Measures OPTICAL gaps, not declared padding. A large numeral set at
 * line-height 1 does not fill its line box, so the space a reader actually
 * sees between a hairline and the top of a digit is not the padding value.
 * This reads real ink bounds out of the page via canvas TextMetrics.
 *
 * It exists because the Build Note shipped with `padding:22px 26px 22px 0` on
 * its stat cells, which spent the whole gutter on ONE side of each vertical
 * rule: every number after the first sat 2px from the rule on its left and
 * 210px from the one on its right. It read as cramped and nobody could say
 * why, because the declared padding looked generous.
 *
 *   node qa/qa-spacing.mjs <built file> [outPrefix]
 */
import { open, scratchDir, sleep } from "./_harness.mjs";
import { join } from "node:path";

const file = process.argv[2];
if (!file) {
  console.error("usage: node qa/qa-spacing.mjs <built file> [outPrefix]");
  process.exit(1);
}
const outDir = process.argv[3] || scratchDir("spacing");

const FIGS = `(() => {
  const cv = document.createElement("canvas").getContext("2d");
  function ink(el) {
    const cs = getComputedStyle(el);
    cv.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
    const m = cv.measureText(el.textContent.trim() || "0");
    const box = el.getBoundingClientRect();
    const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize);
    const half = (lh - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2;
    const baseline = box.top + half + m.fontBoundingBoxAscent;
    return {
      inkTop: baseline - m.actualBoundingBoxAscent,
      inkBottom: baseline + m.actualBoundingBoxDescent,
      inkLeft: box.left - m.actualBoundingBoxLeft,
      inkRight: box.left + m.actualBoundingBoxRight,
      fontSize: parseFloat(cs.fontSize),
    };
  }
  const out = [];
  document.querySelectorAll(".figs").forEach((figs, si) => {
    const fr = figs.getBoundingClientRect();
    const topRule = parseFloat(getComputedStyle(figs).borderTopWidth) > 0;
    const kids = [...figs.querySelectorAll(".fig")];
    kids.forEach((fig, i) => {
      const cs = getComputedStyle(fig), r = fig.getBoundingClientRect();
      const v = fig.querySelector(".fig-v"), l = fig.querySelector(".fig-l");
      const vi = v ? ink(v) : null;
      const prevR = i > 0 ? kids[i-1].getBoundingClientRect() : null;
      const rnd = n => Math.round(n * 10) / 10;
      out.push({
        strip: si, idx: i, value: v ? v.textContent.trim() : null,
        padT: parseFloat(cs.paddingTop), padR: parseFloat(cs.paddingRight),
        padB: parseFloat(cs.paddingBottom), padL: parseFloat(cs.paddingLeft),
        borderR: parseFloat(cs.borderRightWidth),
        ruleToInkTop: topRule && vi && Math.abs(r.top - fr.top) < 2
          ? rnd(vi.inkTop - fr.top) : null,
        leftRuleToInk: prevR && vi && Math.abs(r.top - prevR.top) < 2
          ? rnd(vi.inkLeft - prevR.right) : null,
        numToLabel: vi && l ? rnd(l.getBoundingClientRect().top - vi.inkBottom) : null,
        fontSize: vi ? vi.fontSize : null,
      });
    });
  });
  return out;
})()`;

const RULES = `(() => {
  const col = document.querySelector(".proj-in, .wrap");
  const colW = col ? Math.round(col.getBoundingClientRect().width) : 0;
  const has = el => {
    const cs = getComputedStyle(el);
    return parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderBottomWidth) > 0;
  };

  /* A stat strip's rule can sit on the .figs container OR on a .fig inside it,
     and a variant that moves it is exactly how the same component ends up
     drawing two different rule widths. So ask each strip how wide its rule
     ACTUALLY is, wherever that rule lives, rather than measuring one selector
     and missing the variant. */
  const strips = [...document.querySelectorAll(".figs")].map(f => {
    const carriers = has(f) ? [f] : [...f.querySelectorAll(".fig")].filter(has);
    const w = carriers.length
      ? Math.round(Math.max(...carriers.map(c => c.getBoundingClientRect().width))) : 0;
    return { variant: f.className.replace(/\\bin\\b/g, "").trim(),
             on: has(f) ? ".figs" : ".fig", w };
  }).filter(s => s.w > 0);

  const seen = new Set(), rows = [];
  document.querySelectorAll(".shot, .note, .next li, .g-row").forEach(el => {
    if (!has(el)) return;
    const r = el.getBoundingClientRect();
    if (!r.width) return;
    const cls = String(el.className).trim().split(/\\s+/).filter(c => c !== "in").slice(0,2).join(".");
    const key = cls + Math.round(r.width);
    if (seen.has(key)) return;
    seen.add(key);
    rows.push({ el: el.tagName.toLowerCase() + "." + cls,
      w: Math.round(r.width), pct: Math.round(r.width / colW * 100) });
  });
  return { colW, strips, rows };
})()`;

let problems = 0;
const flag = (m) => { problems++; console.log("     ISSUE  " + m); };

(async () => {
  const page = await open(file, 9343);

  for (const v of [{ n: "desktop", w: 1440, h: 900 },
                   { n: "mobile", w: 390, h: 844, m: true }]) {
    await page.view(v.w, v.h, !!v.m);
    await page.walk();
    console.log(`\n================ ${v.n.toUpperCase()} (${v.w}px) ================`);

    const tops = await page.evaluate(
      `[...document.querySelectorAll(".figs")].map(f =>
         Math.round(f.getBoundingClientRect().top + window.scrollY))`);

    const all = [];
    for (const y of tops) {
      await page.scrollTo(Math.max(0, y - 260));
      const rows = await page.evaluate(FIGS);
      const clip = await page.evaluate(`(() => {
        const f = [...document.querySelectorAll(".figs")].find(f => {
          const r = f.getBoundingClientRect(); return r.top > -50 && r.top < 500; });
        if (!f) return null;
        const r = f.getBoundingClientRect();
        // Page.captureScreenshot clips in ABSOLUTE page coordinates.
        return { x: Math.max(0, r.left - 34), y: Math.max(0, r.top + window.scrollY - 34),
                 width: Math.min(r.width + 68, innerWidth), height: r.height + 68 };
      })()`);
      if (clip) await page.shot(join(outDir, `${v.n}-figs-${y}.png`), clip);
      rows.filter(r => r.ruleToInkTop !== null || r.leftRuleToInk !== null)
          .forEach(r => { if (!all.some(a => a.strip === r.strip && a.idx === r.idx)) all.push(r); });
    }

    if (all.length) {
      console.log("\n  STAT CELLS  (optical gaps, px)");
      console.log("  " + "value".padEnd(8) + "pad T/R/B/L".padEnd(18) +
                  "rule->number".padEnd(14) + "left rule->number".padEnd(19) + "number->label");
      for (const r of all) {
        console.log("  " + String(r.value ?? "?").padEnd(8) +
          `${r.padT}/${r.padR}/${r.padB}/${r.padL}`.padEnd(18) +
          String(r.ruleToInkTop ?? "-").padEnd(14) +
          String(r.leftRuleToInk ?? "-").padEnd(19) +
          String(r.numToLabel ?? "-"));
        // The defect this file exists for: a number crowding the rule beside it.
        if (r.leftRuleToInk !== null && r.leftRuleToInk < 18) {
          flag(`"${r.value}" sits ${r.leftRuleToInk}px from the rule on its left. ` +
               `Spend the gutter on BOTH sides of the rule.`);
        }
        if (r.ruleToInkTop !== null && r.fontSize && r.ruleToInkTop < r.fontSize * 0.6) {
          flag(`"${r.value}" has only ${r.ruleToInkTop}px above it for a ${r.fontSize}px numeral.`);
        }
      }
    }

    await page.scrollTo(0);
    const ru = await page.evaluate(RULES);
    console.log(`\n  RULE WIDTHS  (content column ${ru.colW}px)`);
    ru.strips.forEach(st => console.log("  " + st.variant.padEnd(24) +
      String(st.w).padEnd(8) + `${Math.round(st.w / ru.colW * 100)}% of column   (rule on ${st.on})`));
    ru.rows.forEach(r => console.log("  " + r.el.padEnd(24) +
      String(r.w).padEnd(8) + r.pct + "% of column"));

    // The same component drawing two rule widths reads as an unfinished line.
    const widths = [...new Set(ru.strips.map(s => s.w))];
    if (widths.length > 1) {
      flag(`the stat strip draws ${widths.length} different rule widths ` +
           `(${widths.join(", ")}px) on this page. Cap the content, never the rule. ` +
           ru.strips.map(s => `"${s.variant}" ${s.w}px on ${s.on}`).join("; "));
    }
  }

  await page.close();
  console.log(`\ncaptures: ${outDir}`);
  console.log(problems === 0 ? "\nSPACING QA PASSED\n" : `\n${problems} ISSUE(S) FOUND\n`);
  process.exit(problems === 0 ? 0 : 1);
})().catch((e) => { console.error("HARNESS FAILED:", e.message); process.exit(2); });
