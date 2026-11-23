# Which skill builds which request

**The request's `skill` leads.** The Studio routes every request to one skill: the person picked it
(`picked_by: "person"`, always honour it) or the Studio chose the best fit for the kind and formats
(`picked_by: "studio"`, override only if it plainly cannot make a requested format, and say so in `worker.note`).
Then make each requested format with the skill in the table, keeping one storyline across all of them.

## By kind of work

| `kind.id` | What good looks like | Lead skill | Usual formats |
|---|---|---|---|
| `training` | One module per journey stage, labs that fit the function, the client's AI tool by name, a knowledge check | `metis-learning-module` (course, lab), `metis-pptx` (deck), `duolingo-style-learning` when asked for daily practice | pptx, course, lab, preread, video |
| `prd` | The firm PRD template (start from `rok-prd-tpl` in `sources`): summary, context and problem, objectives, users and flows, functional and non-functional requirements, data and integrations, risks, success metrics, rollout | Word via the `docx` skill, structured like the template; the PRD Builder artifact is the reference | doc |
| `product` | PM role and interactions, lifecycle, habits and artifacts, how to apply them | `metis-pptx`, or `metis-learning-module` if they asked for a course | pptx, course |
| `opmodel` | Design principles, taxonomy, capability map, roles, intake-to-value governance, transition plan | `metis-capability-map` for the map (pptx, xlsx or html), `metis-pptx` for the rest | pptx, xlsx |
| `strategy` | Where value is, maturity, use-case portfolio, phased roadmap, operating model, the asks | `executive-slide-builder` for the storyline, then `metis-pptx` | pptx |
| `steerco` | The SteerCo playbook: same three-column anchor every week, risks needing support, decisions table, appendix | `metis-steerco` | pptx |
| `proposal` | Understanding, perspective, approach and phases, options, case studies, team, next steps | `metis-premier-proposal` (PDF) or `metis-pptx` if they asked for a deck | pdf, pptx |
| `casestudy` | Challenge, approach by phase, results with numbers, what made it work | `metis-premier-proposal` | pdf |
| `thought` | Thesis, evidence, what leaders should do, how to start | `metis-whitepaper` | pdf |

## By format

| Format id | Build it with | Notes |
|---|---|---|
| `pptx` | `metis-pptx` (or `metis-steerco` for SteerCos) | Generation mode from the draft. If a source is a client .pptx template (Lumen and others), use template-preserving mode on a copy of it. Facilitator or presenter notes go in the speaker notes. |
| `slides` | `metis-html-slides` | Same storyline as the PowerPoint when both are asked for. |
| `doc` | `docx` (Word) | PRDs, playbooks, memos. Use the firm template from `sources` when there is one. |
| `pdf` | `metis-premier-proposal`, `metis-whitepaper` or `metis-pdf-creator`, by kind | |
| `xlsx` | `metis-capability-map` (maps) or `xlsx` | Capability maps, use-case inventories, business cases. |
| `course`, `lab` | `metis-learning-module` | One module per journey stage, lessons from the draft's slides, the check from `draft.check`. Films only if asked: they take long. |
| `preread` | `metis-narrative-scroll` | Why it matters, the agenda with timings, what to install and bring. |
| `video` | The **Video Hub** (`metis-demo-video`) | Don't render here. Create a Video Hub project (below), then tell the person to open it to approve the script. |

## Look and feel (every deck, course and document)

Romain's rule: our slides must not look AI-made.
- No kicker line plus accent bar plus title opener. No " · " separators anywhere. No bullet dots: every point gets an
  icon (Lucide style, the draft names one per module, slide and point).
- Vary the layout slide to slide (icon cards, three columns, a step track, before/after compare, one big statement).
  Never two slides in a row with the same layout.
- Title and section slides are colour fields with one playful element (an icon mosaic, a big section number, one
  large icon), not a wall of text. Speaker or facilitator notes go in the notes, never on the slide face.
- Short points (under 14 words). Real numbers, client words, the client's tool by name.

Design system first, skill second: whichever skill builds the file, colours, fonts and logo come from the request's
`design_system` (README rules for built-in systems, tokens for custom ones). A Metis deliverable also follows
`metis-brand-identity`. Run `metis-humanizer` over client-facing prose before QA.

## Design system requests become Claude Design systems

A request with `kind.id: "designsystem"` asks for a full design system for a client, built in Claude Design (the
Design System artifact type). Its `design_system_brief` carries the name, website, what it's for, the brand feel,
the tokens the person approved, a fuller palette, the brand voice, and the colours and fonts read from their
PowerPoint theme. `attachments` carries the brand files: logos (SVG, PNG), guidelines PDF, deck text, fonts,
screenshots, and logo images pulled from their deck's media. Originals with an `asset_id` are in the Studio's asset
store (`Artifact` read on the Studio url with `path` = the asset id).

1. Fetch every attachment original into `<project folder>/brand/`. Read the guidelines PDF and deck text in full.
2. Create the system: ONE `Artifact` publish with `type_url` = `design_system_brief.type_url`
   (https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd), `title` = "<client> Design System", no files. Follow the
   instructions that result carries exactly (files under `project/`, `tokens.json` as lists, README brand book,
   logos uploaded as assets and recorded in the index, the cover written last).
3. Build FROM the brand's real files: exact hex values and font names from the guidelines and the deck theme beat
   the approved tokens, which beat guesses. Copy logos as files, never redraw a mark. No logo in the files: plain
   type and a note in the README. Keep it small if the sources are thin (6 to 10 colours, 5 to 7 text styles) and
   say so.
4. Report: `outputs` gets `{format: "designsystem", title, url: "<the new system's link>", notes}`. Then make it
   usable from the Studio: `ArtifactData` `get` then `update` the Studio's `designSystems` doc
   `design_system_brief.studio_doc_id` (on the Studio url, with `if_version`) with `url` set to the new link,
   `status: "live"`, and any corrected `p`, `a`, `s`, `i`, `font`, `fontName`. If there is no `studio_doc_id`,
   skip that write.
5. The new system is private to the person until they share it. Say in the report: "Share it with the organization
   from its Share menu so the team can build with it." Never change sharing yourself.

## Video requests become Video Hub projects

The Video Hub (https://claude.ai/artifact/H6yLztfVoZyzpH5owCaq3N) keeps each person's projects as documents in its
own `data/users/me` collection, schema `metis-video-project/1`. If `metis-demo-video` is installed, read its
`references/hub-mode.md` for the full contract first. Create one project with `ArtifactData` `set` on the **Video
Hub's** url (`collection: "data/users/me"`, a new doc id), holding only what the Video Hub's own brief would hold:

```json
{"schema": "metis-video-project/1", "title": "<request title> video",
 "brief": {"fork": "informational", "variant": "slide-narrative",
           "purpose": "<what the video is for, from the request>", "audience": "<audience>",
           "branding": "metis or client", "client": {"name": "<client>", "palette": ["<primary>", "<accent>"], "font": "<font>"},
           "length_s": 75, "formats": ["16:9"], "key_points": ["<the draft's outcomes or key messages>"], "cta": "<the next step>",
           "names_policy": "fictional", "voiceover": false},
 "created_from": "metis-build-studio"}
```

Leave `script`, `music` and `render_request` empty: the person writes and approves the script in the Video Hub, and
their Claude renders it with "check the Video Hub". Put the Video Hub link in `outputs[].url` with
`notes: "Open the Video Hub to approve the script"`. If the write is refused, put the brief in `worker.note`
instead and tell the person to start the video in the Video Hub themselves.
