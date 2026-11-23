# Native Template Layout Catalog (Metis 2025 template)

The 2025 Metis template (`master.pptx`, derived from
`Metis_Intro Slides and Template_2025.potx`) ships **32 named slide layouts**.
These are the **primary build path** (Path 1, see SKILL.md §0.5.1): they are
human-designed, on-brand, varied, and far less brittle than hand-drawn shapes.
Reach for a native layout first; hand-build (patterns.md / Timesaver) only when
no layout fits.

## How to use a layout

```python
def get_layout(prs, name):
    for m in prs.slide_masters:
        for lay in m.slide_layouts:
            if lay.name == name:
                return lay
    raise ValueError(f"layout '{name}' not found")

slide = prs.slides.add_slide(get_layout(prs, "Three Content w/ Heading"))

# Fill placeholders by idx (see maps below). Title is always idx 0.
ph = {p.placeholder_format.idx: p for p in slide.placeholders}
ph[0].text = "Evolving the AI operating model from ad hoc to hub-and-spoke"
ph[1].text = "Ad hoc domain delivery"          # heading 1
ph[17].text_frame.text = "..."                  # content under heading 1
```

**Rules**
- Title is **idx 0** on every layout.
- The optional subhead/subtitle is **idx 14** on most content layouts. Use it
  only when the title cannot carry the so-what (SKILL.md §0.5). Do not fill it
  by reflex, and when you skip it, delete the placeholder rather than leaving
  it empty (see the deletion rule below): an unfilled placeholder still shows
  "Click to add subtitle" when the deck is opened in PowerPoint, even though
  it is invisible in Slide Show and does not export.
- `DATE`/`FOOTER`/`SLIDE_NUMBER` placeholders are the brand frame; leave them
  to the layout, do not overwrite.
- `PICTURE` placeholders take images via `placeholder.insert_picture(path)`.
- `OBJECT`/`CHART` placeholders accept text frames, tables, or charts.
- If a layout has more item-slots than you have content, or you are skipping
  the optional subhead (idx 14), **delete the unused placeholders** rather
  than leaving them empty:
  ```python
  sp = ph._element
  sp.getparent().remove(sp)
  ```

## Selection guide (content → layout)

| Content | Layout |
|---|---|
| One chart, one table, or a single large visual | **One Chart or Table** |
| Three charts side by side | **Three Chart** |
| Two-way comparison (current vs future, A vs B, pros/cons) | **Comparison** |
| Three points, each with a heading | **Three Content w/ Heading** |
| Four points, each with a heading | **Four Content w/ Heading** |
| Four-step process, each step with sub-bullets | **Four Content Process** |
| Four icon-led points | **Icon box Four Content** |
| Six icon-led points | **Icon box Six Content** |
| A big visual with an explanatory caption beside it | **Content with Caption** |
| 2-3 people (headshot + name + bio) | **Two / Three Content Speaker Image** |
| Four items each with its own photo | **Four Content - 4 Photo** |
| Four quotes in columns | **Four Content Quote** |
| Up to three stacked quote rows | **Quote Rows** |
| Free-form / hand-built slide needing only a framed canvas | **1_Title Only** or **Title Only** |
| Section break | **Section Divider** (in-deck) or **Closing Slide** |
| Title / cover | **Cover Page**, **Alt Cover Page 1/2/3**, **Title Slide** |
| Bibliography / references | **Reference** |

> **Anti-monotony:** do not route every "list of points" slide to the same
> layout. Across a section, mix `Comparison`, `Content with Caption`, an icon
> box, a chart/table slide, and a quote slide. Reserve even-column grids
> (`Three/Four Content w/ Heading`) for genuinely parallel content (§0.7).

## Placeholder maps: content layouts

Positions are inches `@(left, top) width x height` on the 13.33 x 7.50 canvas.
Frame placeholders (date/footer/slide-number) are omitted; do not touch them.

### One Chart or Table
- idx0 TITLE `@(0.3,0.2) 12.7x0.4`
- idx14 BODY subhead `@(0.3,0.6) 12.5x0.3` *(optional)*
- idx16 OBJECT content `@(0.3,1.2) 12.5x5.3`, chart, table, or one big visual

### Three Chart
- idx0 TITLE; idx14 subhead *(optional)*
- idx15 CHART `@(0.3,1.5) 4.0x5.0`
- idx16 CHART `@(4.6,1.5) 4.0x5.0`
- idx17 CHART `@(8.8,1.5) 4.0x5.0`

### Comparison
- idx0 TITLE; idx14 subhead *(optional)*
- idx1 BODY heading-L `@(0.3,1.2) 6.2x0.3`  |  idx15 OBJECT body-L `@(0.3,1.6) 6.2x4.5`
- idx3 BODY heading-R `@(6.8,1.2) 6.2x0.3`  |  idx16 OBJECT body-R `@(6.8,1.6) 6.2x4.5`

### Three Content w/ Heading
- idx0 TITLE; idx14 subhead *(optional)*
- headings: idx1 `@(0.3,1.2)`, idx3 `@(4.6,1.2)`, idx15 `@(8.9,1.2)` (each 4.1x0.3)
- bodies: idx17 `@(0.3,1.6)`, idx18 `@(4.6,1.6)`, idx19 `@(8.9,1.6)` (each 4.1x4.5)

### Four Content w/ Heading
- idx0 TITLE; idx14 subhead *(optional)*
- headings: idx1 `@(0.3,1.2)`, idx3 `@(3.6,1.2)`, idx15 `@(6.8,1.2)`, idx17 `@(10.0,1.2)` (each 3.0x0.3)
- bodies: idx19 `@(0.3,1.6)`, idx20 `@(3.6,1.6)`, idx21 `@(6.8,1.6)`, idx22 `@(10.0,1.6)` (each 3.0x4.5)

### Four Content Process
- idx0 TITLE; idx14 subhead *(optional)*
- step headings: idx24 `@(0.4,1.4) 3.2x0.6`, idx23 `@(2.9,1.4)`, idx22 `@(6.2,1.4)`, idx17 `@(9.2,1.4)` (3.8x0.6)
- step bodies (objects): idx19 `@(0.4,2.1)`, idx29 `@(3.7,2.1)`, idx30 `@(6.9,2.1)`, idx31 `@(10.1,2.1)` (each 2.8x3.2)
- small bullets w/ heading row: idx25 `@(0.4,5.5)`, idx26 `@(3.6,5.5)`, idx27 `@(6.9,5.5)`, idx28 `@(10.1,5.5)` (each 2.8x0.9)

### Icon box Four Content
- idx0 TITLE; idx14 subhead *(optional)*
- icon slots (OBJECT, ~0.9x0.9): idx18 `@(0.3,1.2)`, idx19 `@(0.3,2.6)`, idx22 `@(0.3,3.9)`, idx20 `@(0.3,5.2)`
- text rows (BODY, 11.8x1.0): idx24 `@(1.2,1.2)`, idx25 `@(1.2,2.6)`, idx26 `@(1.2,3.9)`, idx27 `@(1.2,5.2)`

### Icon box Six Content
- idx0 TITLE; idx14 subhead *(optional)*
- icon slots (OBJECT, 0.9x0.9): idx18 `@(0.3,1.2)`, idx22 `@(4.6,1.2)`, idx23 `@(8.9,1.2)`, idx19 `@(0.3,3.8)`, idx20 `@(4.6,3.8)`, idx21 `@(8.9,3.8)`
- text boxes (BODY, 3.2x1.9): idx24 `@(1.2,1.2)`, idx30 `@(5.5,1.2)`, idx31 `@(9.8,1.2)`, idx32 `@(1.2,3.8)`, idx33 `@(5.5,3.8)`, idx34 `@(9.8,3.8)`

### Content with Caption
- idx0 TITLE; idx14 subhead *(optional)*
- idx1 BODY caption heading `@(0.3,1.2) 3.4x0.3`
- idx2 OBJECT caption body `@(0.3,1.6) 3.4x4.2`
- idx13 PICTURE main visual `@(3.9,1.3) 9.0x5.3`

### Two Content Speaker Image
- idx0 TITLE; idx14 subhead *(optional)*
- left: idx18 PICTURE headshot `@(0.4,1.6) 1.6x1.6`, idx16 BODY name `@(0.3,1.2) 6.1x0.3`, idx1 OBJECT bio `@(0.3,3.2) 6.1x2.6`
- right: idx19 PICTURE headshot `@(7.0,1.6) 1.6x1.6`, idx17 BODY name `@(6.9,1.2) 6.1x0.3`, idx21 OBJECT bio `@(6.9,3.2) 6.1x2.6`
- idx20 BODY caption strip `@(0.3,6.3) 12.7x0.3`

### Three Content Speaker Image
- idx0 TITLE; idx14 subhead *(optional)*
- names: idx16 `@(0.3,1.2)`, idx17 `@(4.6,1.2)`, idx22 `@(8.9,1.2)` (4.1x0.3)
- headshots (PICTURE 1.6x1.6): idx18 `@(0.4,1.6)`, idx19 `@(4.7,1.6)`, idx23 `@(9.0,1.6)`
- bios (OBJECT 4.1x2.6): idx27 `@(0.3,3.2)`, idx28 `@(4.6,3.2)`, idx29 `@(8.9,3.2)`

### Four Content - 4 Photo
- idx0 TITLE; idx14 subhead *(optional)*
- captions/headings (BODY 2.8x0.6): idx18 `@(0.4,1.4)`, idx19 `@(3.6,1.4)`, idx20 `@(6.9,1.4)`, idx21 `@(10.1,1.4)`
- photos (PICTURE 2.8x2.2): idx22 `@(0.4,2.0)`, idx23 `@(3.6,2.0)`, idx24 `@(6.9,2.0)`, idx25 `@(10.1,2.0)`
- descriptions (BODY 2.8x2.2): idx26 `@(0.4,4.4)`, idx27 `@(3.6,4.4)`, idx28 `@(6.9,4.4)`, idx29 `@(10.1,4.4)`

### Four Content Quote
- idx0 TITLE; idx14 subhead *(optional)*
- quote columns (BODY 2.4x3.8): idx18 `@(0.3,1.6)`, idx19 `@(2.9,1.6)`, idx20 `@(5.5,1.6)`, idx21 `@(8.1,1.6)`, idx22 `@(10.7,1.6)`  *(five slots; delete extras)*

### Quote Rows
- idx0 TITLE; idx14 subhead *(optional)*
- rows (BODY 12.7x1.4): idx18 `@(0.3,1.5)`, idx19 `@(0.3,3.1)`, idx20 `@(0.3,4.6)`

## Title / cover / divider layouts

| Layout | Key placeholders |
|---|---|
| **Cover Page** | idx0 TITLE `@(1.2,2.0)`, idx1 BODY `@(1.2,3.4)`, idx13 BODY `@(1.2,4.8)`, idx14 PICTURE |
| **Alt Cover Page 1** | idx0 CENTER_TITLE, idx1 SUBTITLE, idx10 BODY (eyebrow) |
| **Alt Cover Page 2** | idx0 TITLE `@(2.0,1.9) 9.0x1.7`, idx1 BODY, idx13 BODY |
| **Alt Cover Page 3** | idx0 TITLE, idx1 BODY, idx14 PICTURE `@(11.1,2.8)` |
| **Title Slide** | idx0 CENTER_TITLE, idx1 SUBTITLE, idx10 BODY (eyebrow) |
| **Section Divider** | idx0 CENTER_TITLE `@(1.2,0.9) 9.0x1.1` (navy background built in) |
| **Closing Slide** | idx0 TITLE `@(0.4,2.9) 8.0x1.1` |
| **Title Only** / **1_Title Only** | idx0 TITLE, idx14 subhead, clean framed canvas for hand-built slides |
| **Blank** | frame placeholders only, avoid for content |

> Layout names and placeholder indices were extracted directly from the 2025
> template. If a future template revision renames or re-indexes layouts,
> re-extract with python-pptx (`for lay in master.slide_layouts: lay.name`,
> then iterate `lay.placeholders`) and update this file.
