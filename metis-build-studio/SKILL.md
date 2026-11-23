---
name: metis-build-studio
description: Build the files people request in Metis Build Studio (https://claude.ai/artifact/9zvDDHBE8Zs1QaQxZHNWPq) on this computer, and report progress back to the Studio. The Studio is where a consultant picks what to build (a training, a PRD, product management material, operating model work, AI strategy, a SteerCo, a proposal, a case study), the past Metis work to start from, the client, design system, formats and skill with Claude; this skill turns each queued request into the real files (PowerPoint, Word, PDF, Excel, course hub, HTML deck, pre-read, lab guide, a Video Hub project, a client design system in Claude Design) with the skill the request names, then posts the result and picks up revisions. Use it whenever someone says "check the Build Studio", "build my requests", "build what's in the queue", "check my Build Studio builds", pastes the Build Studio link with a request to build, or hands over a build-request.json from the Studio. Do NOT use it for building a deck or course that was never requested in the Studio (use metis-pptx, metis-learning-module and the rest directly).
---

# Metis Build Studio worker

The Build Studio is a Claude artifact. It interviews the consultant, picks the past Metis work to build from and the
skill to build with, and drafts the storyline in the browser. A browser cannot make an editable .pptx, a course hub with films, or a video, so the
Studio queues those as **requests**, and **you build them here**, on the requester's computer, with their Claude and
their usage. This is the same model as the Video Hub.

Read `references/hub-mode.md` before the first build: it is the data contract (paths, fields, who writes what) and
the loop. `references/formats.md` says which skill builds which format and what "good" looks like.

## The loop in one screen

1. **Check for a newer skill.** `Artifact` read the Studio with `path: "skill/version.json"`. If its `version` is
   higher than the first line of this skill's `CHANGELOG.md`, tell the person what's new (its `notes`) and offer to
   update before building (see "Updating" below). Never update without a yes.
2. **Find waiting requests.** `ArtifactData` `list` the collection `data/users/me` on the Studio's url. Requests are
   the documents with `schema: "metis-build-request/1"`. Waiting = `build_request.version` higher than
   `worker.built_version` (missing counts as 0), or `revisions` with ids not in `worker.applied_revisions`.
   Write the presence document (`data/users/me` / `worker`). Nothing waiting: say so in one line and offer to keep
   watching.
3. **Per request:** connect (status `connected`), gather the sources (SharePoint and Drive, see hub-mode.md),
   read the design system, build each requested format led by the request's `skill` (see `formats.md`) (status `building`),
   QA it (status `qa`), save it, and report (status `done`, `outputs`, `built_version`).
4. **Need a decision?** Write `worker.question` with 2 to 4 options and status `needs_input`. The person answers in
   the Studio. Ask once, batched.
5. **Revisions** arrive as new `revisions` entries or a higher `build_request.version`. Apply, rebuild, report as
   the next version with `notes` saying what changed.
6. **Offer to keep watching** (once): `/loop 5m check the Build Studio` while the chat is open, a scheduled task while
   the computer is on, or "no thanks". Say plainly that each check uses a little of their Claude usage.

## Rules that never bend

- **Nothing leaves the person's computer except what the Studio already holds.** Never send, share, post or email a
  file, never write to a client SharePoint, never publish an artifact for a request. Saving to the person's own
  OneDrive is allowed only after they say yes in this chat.
- **Other clients stay out of learner-facing text.** Sources come from Rockwell, Workday, DocuSign, Intuitive and
  others. Reuse structure and ideas, never names, logos, numbers or screenshots from another client.
- **Write only the `worker` field** of a request (merge `update` with `if_version`), plus the presence document.
  `brief`, `spec`, `draft`, `sources`, `revisions`, `answers` and `build_request` belong to the Studio.
- **Every file you make is a draft for a person to review.** Say so in the report.
- An `error` status always carries a plain-English `note` saying what the person can do.

## Updating

`Artifact` read `path: "skill/metis-build-studio.bundle.json"`. It is `{name, version, files: {relpath: base64}}`.
Write every file under `~/.claude/skills/metis-build-studio/` (decode base64, keep the relative paths, overwrite),
then re-read this SKILL.md and carry on.

## Without the Studio

If `ArtifactData` or `Artifact` is not available in this Claude app, ask the person to click **Download request** on
the build in the Studio and hand you the `build-request.json`. Work from the file and report in chat.
