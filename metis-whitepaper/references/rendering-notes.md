# Rendering Notes

## Visual Density Rules

These rules prevent the most common failure mode: text-only pages with large empty areas
that look unfinished compared to published Metis whitepapers.

### Every content page needs a visual anchor

A page with only two-column body text and a headline will look empty at 1280x720. Every
content page must include **at least one** of the following in addition to body text:

- A half-page or banner photo (B&W stock, with dark overlay for legibility)
- An inline SVG framework diagram
- A styled callout box (case study, key concept, or data highlight)
- A pull quote (bold italic, green left border)
- Metric highlight cards (large teal numbers + small label text)

Most published pages include **two or more** of these elements. When in doubt, add more
visual material rather than less. Empty white space reads as unfinished draft.

### Layout variety is mandatory

Do not use the same two-column text layout for every content page. A published whitepaper
alternates across at least four layout types:

| Layout | When to use |
|---|---|
| **Photo left (40%) + text right (60%)** | Opening page of a new section, or when the topic shifts |
| **Photo banner top (35%) + two-column text below** | Abstract/intro pages, conclusion pages |
| **Two-column text + pull quote + callout box** | Core argument pages with supporting evidence |
| **Full-width diagram page** | Framework introductions, maturity models |
| **Dark navy with step list or metric cards** | Data-heavy pages, phase descriptions, key lists |

Plan layout variety during the outline step (Step 2). Annotate each page with its intended
layout type so the HTML build step does not default to uniform text-only pages.

### Photos

**Use real photos, not just gradient placeholders.** Gradient-only pages look visibly sparse
and unpolished compared to published Metis whitepapers. Use the firm's B&W stock photo
library:

**Stock photo path:** `G:\Shared drives\Knowledge Management\New Brand Assets\PPT Assets\Metis PPT Images\`

Available photos (B&W, ready to use as `file://` URIs):
- `pexels-divinetechygirl-1181311-bw.jpg` - woman at computer (covers, tech topics)
- `pexels-thecoachspace-2977547-bw.jpg` - coaching/collaboration (people, team topics)
- `chris-linnett-Rl8gOeq0xNM-unsplash-bw.jpg` - abstract/atmospheric
- `pexels-pixabay-276299-bw.jpg` - architecture/building (structure topics)
- `Metis_flatiron_bw2.jpg` - Flatiron building (conclusion, NYC brand identity)
- `pexels-pixabay-63320-bw.jpg` - office environment (intro, workplace topics)
- `Metis_leap_bw_2.jpg` - action/movement (transformation topics)
- `curated-lifestyle-tRkGpRU1K90-unsplash-bw.jpg` - lifestyle/professional
- `pexels-pixabay-358530-bw.jpg` - additional atmospheric

**Photo rules:**
- Always add a dark overlay (`rgba(0,0,0,0.40)` to `rgba(0,0,0,0.50)`) on photos used behind text for legibility
- Cover: teal-to-navy gradient background, B&W photo at 25% opacity, trajectory device overlay at 35% opacity
- Photo banners: ~35% page height for landscape, ~25% for portrait
- Photo+text splits: photo side is 40%, text side is 60%

If the user provides their own photos, use those. Only fall back to gradients when no
photos are available at all, and note this in the output as a limitation.

### Energy device as background texture

On dark navy pages, overlay the Energy device PNG at 7-10% opacity as a full-width
background texture. This adds visual depth without competing with content:

```html
<img src="file:///G:/Shared%20drives/Knowledge%20Management/New%20Brand%20Assets/Graphic%20Devices/Metis%20Energy%20Device%20RGB.png"
     style="position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;opacity:0.08;pointer-events:none;" alt="" />
```

### Callout boxes for case studies

Named company examples that span 2+ sentences should be styled as callout boxes, not
left as inline body text:

```html
<div class="callout">
  <div class="callout-label">DBS Bank</div>
  CEO Piyush Gupta mandated the bank operate as a technology startup. The GANDALF
  framework and Agile operating model now deliver 45 million hyper-personalized
  nudges monthly.
</div>
```

### Metric highlight cards

For data-heavy sections, present key statistics as large-number cards rather than inline
text. Pattern: large teal number (36-42px) + small gray label (9-10px) below:

```html
<div style="display:flex;gap:32px;margin:20px 0;">
  <div style="text-align:center;">
    <div style="font-size:38px;font-weight:700;color:var(--green);">+154%</div>
    <div style="font-size:9px;color:var(--gray);margin-top:4px;">Pull Request Size</div>
  </div>
</div>
```

---

## Endnote Citation System

All whitepapers use numbered endnote citations. Do NOT use inline parenthetical citations or footnotes at the bottom of individual pages.

**In-text citation markup:**
```html
<!-- On light-background pages -->
<sup class="fn">1</sup>

<!-- On dark-background pages -->
<sup class="fn on-dark">1</sup>
```

**Required CSS (include in base styles):**
```css
sup.fn {
  font-size: 8px; font-weight: 700; color: var(--green);
  vertical-align: super; line-height: 0; margin-left: 1px;
}
sup.fn.on-dark { color: var(--green); }
```

**References/Endnotes page:** The final page of every whitepaper must be a dedicated References page listing all cited sources as numbered entries (1-N). Each entry includes: author/publisher, title (italicized), year, and URL. Use the two-column layout on this page to fit more entries.

**Example endnote entry:**
```
1. Stack Overflow. 2025 Developer Survey: AI Tools & Developer Experience. 2025.
   https://survey.stackoverflow.co/2025/
```

---

## Playwright Rendering Notes

**Landscape orientation bug:** When using the `render-whitepaper.js` script with explicit
`width: '1280px'` and `height: '720px'` (already landscape dimensions), do NOT also set
`landscape: true` in the `page.pdf()` call. Playwright interprets `landscape: true` as
"swap width and height," which produces a 720x1280 portrait page. The render script has
been patched to avoid this, but if writing a custom renderer, omit the `landscape` flag
when providing explicit landscape dimensions.

**Expected file sizes:** A whitepaper with embedded B&W photos will be 8-12 MB. A
text-only draft without photos will be ~0.5 MB. The large size is normal and expected.
