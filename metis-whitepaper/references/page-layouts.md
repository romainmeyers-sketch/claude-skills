# Whitepaper Page Layouts — HTML/CSS Templates

Every whitepaper is a **single HTML file** (`whitepaper.html`) made of `.page` divs rendered to PDF by Playwright. Each `.page` is exactly one page: landscape 1280×720px or portrait 816×1056px. **Portrait (816×1056px) is the default orientation** for text-heavy whitepapers — it produces a denser, Word-document feel with `12.5px` body text and two-column layouts. Use these templates as copy-paste starting points, then fill in real content.

**Important — every page must include:**
- The **Metis Strategy logo** in the top-right corner (`.metis-m` class): Black-Mint variant on light pages, White-Mint variant on dark pages
- A **page footer** (`Page X | [Short Title]`) in the bottom-right

---

## Table of Contents

1. [Base CSS (include once)](#1-base-css-include-once)
2. [Cover Page](#2-cover-page)
3. [Abstract / Introduction Page](#3-abstract--introduction-page)
4. [Section Divider Page](#4-section-divider-page)
5. [Standard Content Page — Light Background](#5-standard-content-page--light-background)
6. [Standard Content Page — Dark Navy](#6-standard-content-page--dark-navy)
7. [Photo Left + Text Right Page](#7-photo-left--text-right-page)
8. [Photo Banner + Two-Column Text](#8-photo-banner--two-column-text)
9. [Full-Width Diagram Page](#9-full-width-diagram-page)
10. [Credits Page](#10-credits-page)
11. [Resources Page](#11-resources-page)
12. [Playwright Rendering Reference](#12-playwright-rendering-reference)

---

## 1. Base CSS (include once)

Place this in the `<head>` of `whitepaper.html`. Every page template below assumes these classes exist.

```html
<head>
  <meta charset="UTF-8" />
  <link
    href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap"
    rel="stylesheet"
  />
  <style>
    /* ── Brand tokens ── */
    :root {
      --dark-blue:  #20216f;
      --green:      #3cdbc0;
      --med-blue:   #256ba2;
      --gray:       #7b8692;
      --white:      #ffffff;
      --light-bg:   #f4f6fa;
      --teal-light: #e8f8f5;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Open Sans', sans-serif;
      background: #fff;
    }

    /* ── Page container ── */
    .page {
      position: relative;
      overflow: hidden;
      page-break-after: always;
    }

    /* Landscape: 1280 × 720 */
    .page.landscape { width: 1280px; height: 720px; }
    /* Portrait: 816 × 1056 */
    .page.portrait  { width: 816px;  height: 1056px; }

    /* ── Full-bleed photo utilities ── */
    .photo-fill {
      position: absolute;
      inset: 0;
      width: 100%; height: 100%;
      object-fit: cover;
      object-position: center;
    }

    /* When no photo is available, use a dark navy gradient placeholder */
    .photo-placeholder {
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, #20216f 0%, #1a3a6b 60%, #102040 100%);
    }

    /* Dark overlay on top of photo for text legibility */
    .photo-overlay {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.45);
    }

    /* ── Typography ── */
    .eyebrow {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--green);
    }

    .snglarrow {
      color: var(--green);
      margin-right: 4px;
      font-size: 11px;
    }

    .display-title {
      font-size: 42px;
      font-weight: 700;
      line-height: 1.1;
      color: var(--white);
    }

    .section-headline {
      font-size: 26px;
      font-weight: 700;
      line-height: 1.2;
      color: var(--dark-blue);
    }

    .section-headline.on-dark { color: var(--white); }

    .body-text {
      font-size: 12.5px;
      font-weight: 400;
      line-height: 1.7;
      color: #333;
    }

    .body-text.on-dark { color: rgba(255,255,255,0.88); }

    .pull-quote {
      font-size: 14px;
      font-weight: 600;
      font-style: italic;
      line-height: 1.45;
      color: var(--dark-blue);
      border-left: 3px solid var(--green);
      padding-left: 14px;
      margin: 18px 0;
    }

    .pull-quote.on-dark {
      color: var(--white);
      border-color: var(--green);
    }

    /* ── Divider rule + eyebrow combo ── */
    .section-rule {
      width: 48px;
      height: 2px;
      background: var(--green);
      margin-bottom: 8px;
    }

    /* ── Two-column layout ── */
    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 32px;
    }

    /* ── Callout box ── */
    .callout {
      background: var(--teal-light);
      border-left: 4px solid var(--dark-blue);
      padding: 12px 16px;
      margin: 12px 0;
      font-size: 10.5px;
      line-height: 1.5;
      color: var(--dark-blue);
    }

    .callout .callout-label {
      font-weight: 700;
      font-size: 9px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--green);
      margin-bottom: 4px;
    }

    /* ── Page furniture: footer + M icon ── */
    .page-footer {
      position: absolute;
      bottom: 20px;
      right: 28px;
      font-size: 9px;
      color: var(--gray);
      text-align: right;
    }

    .metis-m {
      position: absolute;
      top: 22px;
      right: 28px;
      height: 22px;
      width: auto;
    }

    /* ── Section divider title (white text on gradient, no pill background) ── */
    .divider-pill {
      display: inline-block;
      background: transparent;
      color: var(--white);
      font-size: 22px;
      font-weight: 700;
      padding: 10px 32px;
      border-radius: 0;
      letter-spacing: 0.04em;
    }

    /* ── Endnote citation superscripts ── */
    sup.fn {
      font-size: 8px;
      font-weight: 700;
      color: var(--green);
      vertical-align: super;
      line-height: 0;
      margin-left: 1px;
    }
    sup.fn.on-dark { color: var(--green); }

    /* ── Step list (dark navy pages) ── */
    .step-list { list-style: none; }
    .step-list li {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 16px;
    }
    .step-number {
      flex-shrink: 0;
      width: 28px; height: 28px;
      border-radius: 50%;
      background: var(--green);
      color: var(--dark-blue);
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .step-text { font-size: 11px; line-height: 1.55; color: rgba(255,255,255,0.88); }
    .step-text strong { color: var(--white); font-weight: 700; }
  </style>
</head>
```

---

## 2. Cover Page

Teal-to-navy gradient background with B&W photo at 25% opacity, trajectory device overlay at 35%, large title, eyebrow, subtitle, and Metis logo.

```html
<!-- COVER PAGE -->
<div class="page portrait" style="background:linear-gradient(135deg, #20216f 0%, #256ba2 35%, #1a8a7a 60%, #3cdbc0 100%);">
  <!-- Background photo at reduced opacity on gradient -->
  <img class="photo-fill" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/PPT%20Assets/Metis%20PPT%20Images/pexels-divinetechygirl-1181311-bw.jpg" alt="" style="opacity:0.25;" />

  <!-- Trajectory device — full-page overlay on gradient background -->
  <img
    src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Graphic%20Devices/Metis%20Trajectory%20Device%20RGB.png"
    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.35;pointer-events:none;"
    alt=""
  />

  <!-- Content overlay -->
  <div style="position:absolute;top:0;left:0;right:0;bottom:0;display:flex;flex-direction:column;justify-content:center;padding:80px 64px;">
    <p class="eyebrow" style="margin-bottom:20px;">A METIS STRATEGY PERSPECTIVE FOR TECHNOLOGY LEADERS</p>
    <h1 class="display-title" style="max-width:600px;margin-bottom:24px;">
      AI Smart: Maximizing AI Value<br/>with a Balanced Strategy
    </h1>
    <p style="font-size:15px;font-weight:400;color:rgba(255,255,255,0.80);max-width:500px;line-height:1.6;">
      The Metis Strategy framework to guide technology executives through the ambiguity of AI
    </p>
  </div>

  <!-- Metis logo bottom-left -->
  <div style="position:absolute;bottom:40px;left:64px;">
    <img src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20White%20RGB%20logo.png" height="28" alt="Metis Strategy" onerror="this.style.display='none';this.nextElementSibling.style.display='inline';" />
    <span style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);letter-spacing:0.06em;display:none;">METIS STRATEGY</span>
  </div>

  <!-- Year bottom-right -->
  <div style="position:absolute;bottom:40px;right:64px;font-size:11px;color:rgba(255,255,255,0.5);">2025</div>
</div>
```

---

## 3. Abstract / Introduction Page

Photo banner at top (~25% height for portrait), then rule + eyebrow, hook headline, and two-column body text below. **Do NOT place the trajectory device on this page** — keep it clean.

```html
<!-- ABSTRACT / INTRODUCTION PAGE -->
<div class="page portrait" style="background:var(--light-bg);">
  <!-- Metis logo top-right (Black-Mint for light pages) -->
  <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20Black-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

  <!-- NO trajectory device on this page -->

  <!-- Top photo banner (~220px height for portrait) -->
  <div style="position:relative;height:220px;overflow:hidden;">
    <img style="width:100%;height:100%;object-fit:cover;object-position:center top;" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/PPT%20Assets/Metis%20PPT%20Images/pexels-pixabay-63320-bw.jpg" alt="" />
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.30);"></div>
  </div>

  <!-- Content area -->
  <div style="padding:32px 56px 0;">
    <div class="section-rule"></div>
    <p class="eyebrow" style="margin-bottom:12px;"><span class="snglarrow">&#9654;</span>Introduction</p>

    <h2 style="font-size:21px;font-weight:700;color:var(--dark-blue);line-height:1.25;margin-bottom:18px;">
      [Hook headline — bold, declarative, not a question]
    </h2>

    <div class="two-col body-text">
      <div>
        <p>[Opening body — problem statement in 2–3 short paragraphs]</p>
      </div>
      <div>
        <p><strong style="color:var(--dark-blue);">[Metis POV paragraph — bold lead-in sentence stating position]</strong> [Explanation and paper overview]</p>
      </div>
    </div>
  </div>

  <div class="page-footer">Page 2 | [Short Title]</div>
</div>
```

---

## 4. Section Divider Page

Full-page teal-to-navy gradient with trajectory device overlay at 30% opacity. White section title text (no pill background). Bold centered pull statement below.

```html
<!-- SECTION DIVIDER PAGE -->
<div class="page portrait" style="background:linear-gradient(135deg, #20216f 0%, #256ba2 35%, #1a8a7a 60%, #3cdbc0 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">

  <!-- Trajectory device — full-page overlay on gradient -->
  <img
    src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Graphic%20Devices/Metis%20Trajectory%20Device%20RGB.png"
    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.3;pointer-events:none;"
    alt=""
  />

  <!-- Section title — white text, no pill/background -->
  <div class="divider-pill" style="margin-bottom:32px;position:relative;z-index:1;">II. AI Funding</div>

  <!-- Pull statement -->
  <p style="font-size:16px;font-weight:400;color:rgba(255,255,255,0.90);max-width:560px;line-height:1.7;position:relative;z-index:1;">
    Companies spent 2.7% of their IT budgets on Generative AI in 2024.
    In 2025, that figure is anticipated to reach 4.3%. This doubling will
    inevitably attract CFO scrutiny and demand a more rigorous investment thesis.
  </p>

  <div class="page-footer" style="color:rgba(255,255,255,0.40);position:relative;z-index:1;">Page 5 | [Short Title]</div>
</div>
```

---

## 5. Standard Content Page — Light Background

The workhorse layout. Rule + eyebrow + headline at top, two-column body text, optional pull quote, optional diagram or callout.

```html
<!-- STANDARD CONTENT PAGE — LIGHT -->
<div class="page landscape" style="background:var(--light-bg);padding:44px 64px 44px;">

  <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20Black-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

  <!-- Header -->
  <div style="margin-bottom:20px;">
    <div class="section-rule"></div>
    <p class="eyebrow"><span class="snglarrow">▶</span>AI Strategy</p>
    <h2 class="section-headline" style="margin-top:8px;">Why Most AI Investments Fail to Scale</h2>
  </div>

  <!-- Two-column body -->
  <div class="two-col" style="margin-bottom:20px;">
    <div>
      <p class="body-text">The gap between AI ambition and AI outcomes is not a technology problem — it is a strategy problem. Organizations invest heavily in models and tooling but underinvest in the operating conditions that allow AI to deliver at scale: clear ownership, reliable data, and a funding model tied to business outcomes.</p>
      <p class="body-text" style="margin-top:10px;">In our work with more than 40 technology organizations over the past three years, the pattern is consistent: teams that move fast without foundational clarity accumulate technical debt and organizational friction faster than they accumulate value.</p>
      <div class="pull-quote" style="margin-top:18px;">
        "The companies that win with AI are not the fastest adopters. They are the most disciplined builders."
      </div>
    </div>
    <div>
      <p class="body-text">Three root causes account for the majority of stalled AI programs:</p>
      <ul style="margin:10px 0 0 16px;" class="body-text">
        <li style="margin-bottom:8px;"><strong>Fragmented ownership.</strong> AI initiatives sit in technology without business co-sponsorship, limiting adoption and ROI clarity.</li>
        <li style="margin-bottom:8px;"><strong>Underdeveloped data foundations.</strong> Models are only as good as the data they ingest — and most enterprises have not made the foundational investments required.</li>
        <li style="margin-bottom:8px;"><strong>Misaligned funding models.</strong> Project-style funding cycles are incompatible with the iterative, long-horizon nature of AI capability building.</li>
      </ul>
      <div class="callout" style="margin-top:14px;">
        <div class="callout-label">Client Example</div>
        A global financial services firm, for example, consolidated 14 siloed AI pilots under a single platform team. Within 18 months, time-to-production halved and deployment costs dropped by 60%.
      </div>
    </div>
  </div>

  <!-- Diagram placeholder — replace with inline SVG from diagram-builders.md -->
  <!--
  <div style="border:1px solid #dde2ea;border-radius:4px;padding:20px;text-align:center;background:#fff;">
    [INSERT DIAGRAM SVG HERE]
    <p style="font-size:9px;color:var(--gray);margin-top:8px;">Source: Metis Strategy</p>
  </div>
  -->

  <div class="page-footer">Page 4 | Short Title</div>
</div>
```

---

## 6. Standard Content Page — Dark Navy

Used for multi-step frameworks, phase descriptions, and numbered lists that benefit from a bold visual break.

```html
<!-- STANDARD CONTENT PAGE — DARK NAVY -->
<div class="page landscape" style="background:var(--dark-blue);padding:44px 64px 44px;">

  <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20White-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

  <div style="margin-bottom:28px;">
    <div class="section-rule"></div>
    <p class="eyebrow"><span class="snglarrow">▶</span><span style="color:rgba(255,255,255,0.7);">AI Operating Model</span></p>
    <h2 class="section-headline on-dark" style="margin-top:8px;">Five Moves That Separate Scalers from Starters</h2>
  </div>

  <div class="two-col">
    <ul class="step-list">
      <li>
        <span class="step-number">1</span>
        <div class="step-text"><strong>Establish a Platform Team</strong><br/>Consolidate AI infrastructure, model management, and developer tooling under a central platform team — not in individual product lines. This creates reuse, reduces duplication, and builds institutional capability.</div>
      </li>
      <li>
        <span class="step-number">2</span>
        <div class="step-text"><strong>Define a Tiered Funding Model</strong><br/>Separate exploratory investments (sandbox budgets, time-boxed experiments) from scaling investments (platform builds, productionization). Each tier requires different governance and success metrics.</div>
      </li>
      <li>
        <span class="step-number">3</span>
        <div class="step-text"><strong>Instrument Every Initiative</strong><br/>Every AI initiative must ship with a measurement plan. Define leading and lagging indicators before launch — not after. Teams that measure from day one course-correct faster and build the evidence base for continued investment.</div>
      </li>
    </ul>
    <ul class="step-list">
      <li>
        <span class="step-number">4</span>
        <div class="step-text"><strong>Build a Data Readiness Baseline</strong><br/>Before scaling any AI capability, assess data quality, accessibility, and governance across the domains it will touch. A global retailer, for example, ran a 6-week data readiness sprint before deploying its demand-forecasting model — cutting rework by over 40%.</div>
      </li>
      <li>
        <span class="step-number">5</span>
        <div class="step-text"><strong>Create an AI Governance Council</strong><br/>Assign accountable senior sponsors for AI risk, ethics, and compliance. This is not a compliance checkbox — it is a prerequisite for operating in regulated industries and for earning the organizational trust AI needs to scale.</div>
      </li>
    </ul>
  </div>

  <div class="page-footer" style="color:rgba(255,255,255,0.40);">Page 7 | Short Title</div>
</div>
```

---

## 7. Photo Left + Text Right Page

Left half is a full-bleed photo; right half is section header and body content. Strong visual contrast.

```html
<!-- PHOTO LEFT + TEXT RIGHT PAGE -->
<div class="page landscape" style="display:flex;">

  <!-- Left: full-bleed photo (50% width) -->
  <div style="position:relative;width:50%;flex-shrink:0;overflow:hidden;">
    <img style="width:100%;height:100%;object-fit:cover;" src="assets/photos/section-photo.jpg" alt="" />
    <!-- Fallback: <div style="width:100%;height:100%;background:linear-gradient(160deg,#20216f,#102040);"></div> -->
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.25);"></div>
  </div>

  <!-- Right: text content -->
  <div style="flex:1;background:var(--light-bg);padding:52px 48px 52px 52px;display:flex;flex-direction:column;justify-content:center;position:relative;">
    <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20Black-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

    <div class="section-rule"></div>
    <p class="eyebrow" style="margin-bottom:10px;"><span class="snglarrow">▶</span>Governance Framework</p>
    <h2 class="section-headline" style="margin-bottom:18px;">Governance Is Not a Brake — It Is an Accelerator</h2>

    <p class="body-text" style="margin-bottom:12px;">The organizations that scale AI fastest are, paradoxically, the ones that govern it most deliberately. Governance defines the guardrails that allow teams to move quickly without triggering the organizational immune response that kills most AI programs.</p>

    <p class="body-text" style="margin-bottom:12px;">An effective AI governance framework addresses three dimensions: <strong>risk</strong> (what are we allowed to do?), <strong>accountability</strong> (who decides?), and <strong>quality</strong> (how do we know it is working?).</p>

    <div class="pull-quote">
      "Governance done right is not about saying no. It is about creating the conditions that make 'yes' sustainable."
    </div>

    <div class="page-footer">Page 8 | Short Title</div>
  </div>

</div>
```

---

## 8. Photo Banner + Two-Column Text

Top third is a full-bleed photo banner with the section headline floated over it; the lower two-thirds has two-column body text.

```html
<!-- PHOTO BANNER + TWO-COLUMN TEXT PAGE -->
<div class="page landscape">

  <!-- Top photo banner (35% height ≈ 252px landscape) -->
  <div style="height:252px;position:relative;overflow:hidden;">
    <img style="width:100%;height:100%;object-fit:cover;object-position:center 30%;" src="assets/photos/banner.jpg" alt="" />
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.35);"></div>

    <!-- Headline floated over photo -->
    <div style="position:absolute;bottom:24px;left:64px;right:64px;">
      <div class="section-rule" style="background:var(--white);margin-bottom:8px;"></div>
      <p class="eyebrow" style="color:rgba(255,255,255,0.75);margin-bottom:6px;"><span class="snglarrow">▶</span>AI Talent</p>
      <h2 style="font-size:24px;font-weight:700;color:var(--white);line-height:1.2;max-width:720px;">
        The Talent Equation: Build, Buy, Borrow, or Bot
      </h2>
    </div>
  </div>

  <!-- Bottom text area -->
  <div style="padding:28px 64px 0;position:relative;">
    <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20Black-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

    <div class="two-col">
      <p class="body-text">The AI talent market is tight and shows no signs of easing. Technology leaders who wait for the "right" hires before launching AI initiatives will still be waiting in three years. The winning approach is a portfolio strategy: build internal capability in the domains that matter most, buy specialized talent for critical gaps, borrow capability through partners and vendors, and use AI tooling to multiply the productivity of the team you already have.</p>
      <div>
        <p class="body-text">In our experience, organizations that adopt this portfolio approach staff AI programs 40% faster than those pursuing pure hire-and-build strategies — and retain talent at higher rates because the work is more varied and the learning curve steeper.</p>
        <div class="callout" style="margin-top:14px;">
          <div class="callout-label">Key Insight</div>
          The build-vs-buy decision should be made at the <em>capability</em> level, not the headcount level. Define which AI skills are core to your competitive differentiation — then build those. Everything else is a candidate for a partner model.
        </div>
      </div>
    </div>
  </div>

  <div class="page-footer">Page 10 | Short Title</div>
</div>
```

---

## 9. Full-Width Diagram Page

Dedicated page for a large framework diagram. Header at top, diagram fills the lower portion, Source caption below.

```html
<!-- FULL-WIDTH DIAGRAM PAGE -->
<div class="page landscape" style="background:#fff;padding:40px 64px 40px;">

  <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20Black-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

  <div style="margin-bottom:20px;">
    <div class="section-rule"></div>
    <p class="eyebrow"><span class="snglarrow">▶</span>AI Maturity</p>
    <h2 class="section-headline" style="margin-top:6px;">The AI Maturity Model: Where Are You on the Journey?</h2>
  </div>

  <!-- Paste inline SVG from diagram-builders.md here -->
  <div style="display:flex;flex-direction:column;align-items:center;">
    <!-- REPLACE with generated SVG -->
    <svg width="1100" height="340" viewBox="0 0 1100 340">
      <rect width="1100" height="340" fill="#f4f6fa" rx="6"/>
      <text x="550" y="175" text-anchor="middle" font-family="Open Sans,sans-serif" font-size="16" fill="#7b8692">[Insert framework diagram SVG — see diagram-builders.md]</text>
    </svg>
    <p style="font-size:9px;color:var(--gray);margin-top:10px;text-align:center;">Source: Metis Strategy</p>
  </div>

  <div class="page-footer">Page 6 | Short Title</div>
</div>
```

---

## 10. Credits / Closing Page

Clean branded closing page. Centered Metis Strategy logo and contact email on dark navy background. No author cards, no headshots, no "AI Working Group."

```html
<!-- CREDITS / CLOSING PAGE -->
<div class="page portrait" style="background:var(--dark-blue);padding:56px 64px;display:flex;flex-direction:column;justify-content:space-between;">

  <!-- Energy device background texture -->
  <img src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Graphic%20Devices/Metis%20Energy%20Device%20RGB.png"
    style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:0.08;pointer-events:none;" alt="" />

  <!-- Top-right logo -->
  <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20White-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

  <!-- Spacer -->
  <div></div>

  <!-- Centered logo + email -->
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;">
    <img src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20White-Mint%20RGB%20Logo.png" height="52" alt="Metis Strategy" style="margin-bottom:8px;" onerror="this.style.display='none';this.nextElementSibling.style.display='block';" />
    <span style="font-size:22px;font-weight:700;color:var(--white);letter-spacing:0.06em;display:none;">METIS STRATEGY</span>
    <p style="font-size:14px;color:var(--green);font-weight:600;letter-spacing:0.02em;">info@metisstrategy.com</p>
  </div>

  <!-- Copyright -->
  <div style="text-align:center;">
    <p style="font-size:10px;color:rgba(255,255,255,0.40);">Proprietary &amp; Confidential, Metis Strategy LLC [YEAR]</p>
  </div>

  <div class="page-footer" style="color:rgba(255,255,255,0.30);">Page N | [Short Title]</div>
</div>
```

---

## 11. References / Endnotes Page

Light background. Numbered endnote entries corresponding to in-text `<sup class="fn">N</sup>` citations. Two-column layout to fit more entries. Every in-text citation number must have a matching entry here.

```html
<!-- REFERENCES / ENDNOTES PAGE -->
<div class="page portrait" style="background:#fff;padding:48px 56px;">

  <img class="metis-m" src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Metis%20Strategy%20Logo/Metis%20Strategy%20Black-Mint%20RGB%20Logo.png" alt="Metis Strategy" />

  <div style="margin-bottom:20px;">
    <div class="section-rule"></div>
    <p class="eyebrow"><span class="snglarrow">&#9654;</span>References</p>
    <h2 class="section-headline" style="margin-top:8px;">Endnotes</h2>
  </div>

  <div class="two-col" style="font-size:9.5px;line-height:1.7;color:#444;">
    <div>
      <p style="margin-bottom:6px;"><strong>1.</strong> Stack Overflow. <em>2025 Developer Survey.</em> 2025. https://survey.stackoverflow.co/2025/</p>
      <p style="margin-bottom:6px;"><strong>2.</strong> GitHub. <em>Octoverse 2024.</em> 2024. https://octoverse.github.com/2024</p>
      <p style="margin-bottom:6px;"><strong>3.</strong> [Continue numbering...]</p>
    </div>
    <div>
      <p style="margin-bottom:6px;"><strong>N.</strong> [Continue numbering...]</p>
    </div>
  </div>

  <div class="page-footer">Page N+1 | [Short Title]</div>
</div>
```

**Important:** Every `<sup class="fn">N</sup>` in the whitepaper body must have a corresponding numbered entry on this page. Numbers must match exactly.

---

## 12. Playwright Rendering Reference

The full render script lives at `scripts/render-whitepaper.js`. Key configuration:

```javascript
await page.pdf({
  path:            outPath,
  landscape:       isLandscape,        // true for 1280×720, false for 816×1056
  width:           isLandscape ? '1280px' : '816px',
  height:          isLandscape ? '720px'  : '1056px',
  printBackground: true,               // REQUIRED — dark navies and photo fills need this
  margin:          { top: '0', right: '0', bottom: '0', left: '0' },  // full-bleed
});
```

Critical flags:
- **`printBackground: true`** — without this, all dark navy backgrounds and photo fills render white
- **`margin: 0`** — pages are full-bleed; any margin will shift content
- **`waitUntil: 'networkidle'`** on `page.goto()` — ensures Google Fonts CDN loads before capture

Run it: `node scripts/render-whitepaper.js whitepaper.html output.pdf landscape`
