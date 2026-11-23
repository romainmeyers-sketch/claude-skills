# External Slide Templates — Visual Pattern Library

`assets/external_slide_templates_master.pptx` is a 217-slide, 16:9 library of
pre-built visual patterns (Metis "External Slide Templates_Master"). Use it
when a SteerCo slide (usually an appendix visual) needs a real diagram rather
than a title + bullets: timelines, process flows, comparison layouts,
maturity pyramids, circular step diagrams, etc.

## How to use a template slide

Never rebuild these visuals from scratch in python-pptx. Pull the slide in,
then replace its placeholder text:

1. Generate the base deck with `scripts/build_steerco.py` as usual.
2. Insert the chosen template slide(s) into the deck at the right position
   with PowerPoint COM (same InsertFromFile mechanism as
   `scripts/append_previous.py`):

```python
# Windows only, requires desktop PowerPoint
import win32com.client
app = win32com.client.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(r"<deck>.pptx", WithWindow=False)
# insert template slide N after deck position P (keep source formatting)
pres.Slides.InsertFromFile(r"<skill>/assets/external_slide_templates_master.pptx", P, N, N)
pres.Save(); pres.Close(); app.Quit()
```

3. Edit the inserted slide's text via python-pptx (find shapes by their
   placeholder text such as "YOUR TEXT HERE" / "Lorem ipsum ..." and replace).
4. Re-apply house style: no shadows, Calibri, Metis colors (Navy #20216F,
   Blue #256BA2, Mint #3CDBC0). Many library slides use off-brand palettes;
   recolor fills/lines on the shapes you keep.
5. Run visual QA as always.

## Index (slide numbers in the master)

| Slides | Section / pattern | Good for |
|---|---|---|
| 3–20 | Personal Favorites: circle/step diagrams, workplans, competitive analysis, funnels, agile boards | First place to look |
| 21–31 | Arrow diagrams: 3D arrows, comparisons, 5-stage timelines, briefing layouts | Roadmaps, before/after, sequencing |
| 32–72 | Circle infographics: cycles, orbit/step wheels of many sizes | Operating cadences, loops, lifecycles |
| 73–74, 103–119, 197–198, 208–212 | Project management infographics: status boards, Gantt-ish views, milestone charts | Workplans, milestone tracking |
| 75–80, 149–171 | Process diagrams: linear flows, curved arrows, swimlane-ish steps | Intake flows, SDLC, hand-off maps |
| 81–92, 199–203, 213–215 | Business strategies & frameworks: six-box, PESTEL, step models, risk/comms matrices | Frameworks, gap analyses |
| 93 | Agile infographic (backlog/sprint board) | Agile/SAFe explainers |
| 94–102 | Groupings of 4 + empathy maps | Stakeholder views, quadrants |
| 120–148 | Product lifecycle infographics: intro/growth/maturity/decline in many forms | Maturity stories, phase narratives |
| 172–177 | Venn diagrams (triple) | Overlapping ownership/scope |
| 178–196 | Pyramid infographics: DIKW, 3–5 level pyramids, productivity pyramids | Hierarchies, capability ladders |
| 204–217 | Other designs: funnels, quadrants, KPI/percentage tiles | Metrics tiles, misc |

Slides 1–2 are the cover and a slide-type overview; skip them.

## Cautions

- The library contains third-party filler text ("Slidesgo", planets copy).
  Replace ALL placeholder text before delivering; never ship a slide with
  Lorem ipsum or planet facts left in.
- Library slides carry their own masters when inserted with
  `WithSourceFormatting`. Prefer inserting WITHOUT source formatting where the
  Metis master should apply, and keep source formatting only when the visual
  breaks otherwise.
- House style still wins (see SKILL.md §3): strip shadows and off-brand
  accent colors on anything you keep.
