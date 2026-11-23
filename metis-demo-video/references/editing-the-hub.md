# Editing the Video Hub or this skill

Only the two editors (Rohan: rohanintheclouds, Romain: romainmeyers-sketch) do this. Everyone else uses the hub.

- **Repo**: https://github.com/rohanintheclouds/metis-video-hub (private). If it is not cloned yet, clone it to a
  folder outside any scratchpad and tell the person where it is.
- **Live hub**: https://claude.ai/artifact/H6yLztfVoZyzpH5owCaq3N (editors hold Editor access in its Share menu).
- **The workflow is the repo's `CLAUDE.md`. Read it before any edit.** In short:
  1. `git pull --rebase`, then tell the person in plain words what the other editor changed since their last pull.
  2. Edit `hub/index.html` or `skill/metis-demo-video/` in the repo (never `~/.claude/skills/metis-demo-video`).
  3. Skill changed: add a CHANGELOG line, run `python3 _build/package_skill.py --install`.
  4. Page changed: `python3 _build/make_qa_harness.py`, serve the repo root, click through the changed screens.
  5. Commit and push to `main`, THEN publish (a skill change publishes both `skill/metis-demo-video.bundle.json` and
     `skill/version.json`; that is what triggers everyone's update prompt) to the hub URL with the Artifact tool (`url` set, `capabilities`
     omitted, only changed files, under about 10 MB per publish).
  6. Tell the other editor in one line what shipped.
- If a publish is refused because a newer version exists, the other editor shipped: pull, merge, publish again.
