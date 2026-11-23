---
name: metis-claude-help
description: >
  Metis Claude Help, the skill management utility for Claude Code at Metis
  Strategy. Discover and install skills, publish new skills, search FAQs and
  tips, share knowledge, and report bugs. Invoke with "metis-claude-help,"
  "claude help," "what skills are available," "browse skills," "install a
  skill," "publish a skill," "search FAQ," "share a tip," "report a bug,"
  "need help with claude," or "skill registry." This is a utility skill for
  skill management, not for creating documents or deliverables.
metadata:
  author: Metis Strategy
  version: 0.1.1
---

# Metis Claude Help

Your one-stop skill for everything Claude Code at Metis Strategy.

## What This Skill Does

Metis Claude Help is a terminal-native command center that connects every Metis
consultant to the shared skill ecosystem. Instead of browsing folders on G Drive
or asking colleagues on Slack, invoke this skill and get guided through whatever
you need.

## When to Use It

- **"What skills exist?"** — Browse or search the full registry of Metis skills
- **"I want to install a skill"** — One-click install from G Drive to your machine
- **"I built something useful"** — Publish a new skill for team review
- **"How do I do X?"** — Search FAQs and tips from other consultants
- **"Here's a trick I found"** — Share a tip so others can benefit
- **"Something is broken"** — Report a bug with auto-captured diagnostics

## Key Capabilities

| Capability | What It Does |
|---|---|
| **Skill Registry** | Browse, search, and view details for all available Metis skills with version and install status |
| **One-Click Install** | Copy any skill from G Drive to your local `~/.claude/skills/` with version tracking |
| **Skill Publishing** | Guided wizard that collects name, description, example, and author — auto-generates SKILL.md, tile.json, SUBMISSION.md |
| **FAQ Search** | Full-text search across all shared tips and FAQs on G Drive |
| **Tip Sharing** | Write and publish tips with title, content, links, and tags — dated and attributed |
| **Bug Reporting** | Describe the problem in plain language — OS, Python version, installed skills, and sync log captured automatically |
| **Slack Notifications** | Every action posts to `#claude_help` with clear emoji-prefixed titles |

## Guided Menu

When invoked, present this menu to the user:

```
Metis Claude Help — What would you like to do?

  SKILLS
     1. Search skills          — Find a skill by name or keyword
     2. Browse all skills      — See everything available
     3. Know more about a skill — Deep dive into a specific skill
     4. Install a skill        — Add a skill to your Claude Code
     5. Publish a skill        — Submit a new skill for review

  HELP & KNOWLEDGE
     6. Search FAQ             — Find answers to common questions
     7. Need help              — Get assistance with Claude Code or skills
     8. Share a tip            — Contribute a tip or trick

  REPORT
     9. Report a bug           — Something not working? Let us know

Type a number or describe what you need.
```

If the user picks a number, route to that action. If they describe a need in natural
language, match it to the closest action and proceed.

## Actions

### 1–4: Skills Browse, Search, Detail, Install

Run `scripts/registry.py` with the appropriate action:

```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe"
"$PYTHON" "<skill-dir>/scripts/registry.py" --action list
"$PYTHON" "<skill-dir>/scripts/registry.py" --action search --query "<query>"
"$PYTHON" "<skill-dir>/scripts/registry.py" --action detail --name "<skill-name>"
"$PYTHON" "<skill-dir>/scripts/registry.py" --action install --name "<skill-name>"
```

Display results formatted in conversation. For install, confirm with user before copying.

**Error handling:** If the script exits non-zero, check: (1) Python path exists, (2) G Drive is mounted, (3) `metis-skills-config.json` exists at `~/.claude/`. Report the specific error to the user and suggest running the health check.

### 5: Publish a Skill

Interactive conversation flow — collect these fields from the user:

1. **Skill name** (required) — lowercase, hyphenated
2. **Description** (required) — what it does, when to trigger
3. **Working example** (required) — a prompt + expected output demonstrating the skill
4. **Category** (optional) — generation, reference, automation, integration
5. **Version** (default: 0.1.0)

Pre-fill author name and email from `~/.claude/about-me.md` if available.

Show a summary of all collected details and ask for confirmation before proceeding.

On confirmation, run:
```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe"
"$PYTHON" "<skill-dir>/scripts/publish.py" \
  --name "<name>" \
  --description "<desc>" \
  --example "<example>" \
  --author-name "<name>" \
  --author-email "<email>" \
  --version "<version>"
```

This will:
- Create the submission folder on G Drive
- Generate SKILL.md, tile.json, and SUBMISSION.md
- Send a Slack notification to #claude_help

### 6: Search FAQ / Tips

Search-only. Run `scripts/faq.py` with `--action search`:

```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe"
"$PYTHON" "<skill-dir>/scripts/faq.py" --action search --query "<query>"
```

If no results found, suggest the user pick action 7 (Need help) to ask the team
directly on Slack, or action 8 (Share a tip) if they have one to contribute.

### 7: Need Help

Collect a free-form question from the user — what they're stuck on, what they've
already tried, anything an answerer needs to know. Pre-fill author from
`~/.claude/about-me.md` if available.

On confirmation, run:

```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe"
"$PYTHON" "<skill-dir>/scripts/help.py" \
  --question "<user-question>" \
  --author-name "<name>" \
  --author-email "<email>"
```

This posts a `🙋 HELP REQUEST` message to `#claude_help` with the question,
author, and auto-captured environment (OS, Python version). No file is
written — Slack is the inbox.

### 8: Share a Tip

Collect from user:
1. **Title** (required)
2. **Content** (required) — markdown text
3. **Links** (optional) — relevant URLs
4. **Tags** (optional) — keywords for searchability

Pre-fill contributor from `~/.claude/about-me.md`.

On confirmation, run:
```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe"
"$PYTHON" "<skill-dir>/scripts/faq.py" --action create-tip \
  --title "<title>" \
  --content "<content>" \
  --links "<links>" \
  --tags "<tags>" \
  --author-name "<name>" \
  --author-email "<email>"
```

### 9: Report a Bug

Ask user to describe the bug in their own words. No rigid form — just a natural description.

On confirmation, run:
```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe"
"$PYTHON" "<skill-dir>/scripts/bugs.py" \
  --title "<auto-generated-title>" \
  --description "<user-description>" \
  --author-name "<name>" \
  --author-email "<email>"
```

The script auto-captures environment details (OS, Python version, installed skills, last sync log).

**Error handling for all script actions:** If any script fails, check these in order:
1. Python path: `C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe` (do not use `python` or `python3` directly)
2. G Drive mounted: `G:\Shared drives\Knowledge Management\Claude Code\` must be accessible
3. Config file: `~/.claude/metis-skills-config.json` must exist with valid paths
4. Slack webhook: `config.json` in the skill directory must contain a valid webhook URL
5. Network: corporate VPN may block outbound webhook calls

If the error is unclear, suggest the user run the health check:
```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/pythonw.exe"
"$PYTHON" "$HOME/.metis/health-check.py"
```

## Configuration

Slack webhook URL is in `config.json` (ships with the skill, no per-user setup needed).

G Drive paths read from `~/.claude/metis-skills-config.json`:

```json
{
  "root_dir": "G:/Shared drives/Knowledge Management/Claude Code/Metis-Skills",
  "incoming_dir": "G:/Shared drives/Knowledge Management/Claude Code/Incoming-Skills",
  "faq_dir": "G:/Shared drives/Knowledge Management/Claude Code/FAQ-Tips",
  "bugs_dir": "G:/Shared drives/Knowledge Management/Claude Code/Bug-Reports"
}
```

## Slack Notifications

All notifications go to `#claude_help`. Titles clearly distinguish type:

- `🆕 NEW SKILL SUBMISSION` — someone published a skill for review
- `🐛 BUG REPORT` — someone reported an issue
- `🙋 HELP REQUEST` — someone needs help with Claude Code or a skill
- `💡 NEW TIP` — someone shared a tip or trick

---

## Troubleshooting

### "Drive not found" or skill sync fails
- **Cause:** Google Drive for Desktop not running, or shared drive not mounted.
- **Fix:** Verify `G:\Shared drives\Knowledge Management\Claude Code\` is accessible. Start Google Drive for Desktop if needed. Check that the shared drive "Knowledge Management" is visible in File Explorer.

### Python script errors (ModuleNotFoundError, FileNotFoundError)
- **Cause:** Wrong Python path or missing dependencies.
- **Fix:** Use full Python path: `C:/Users/navan/AppData/Local/Programs/Python/Python312/python.exe`. Do not attempt `python`, `python3`, or `py` directly. If a module is missing, install it: `"<python-path>" -m pip install <module>`.

### Slack webhook not sending
- **Cause:** Invalid webhook URL or network restriction.
- **Fix:** Check that `config.json` in the skill directory contains a valid `SLACK_WEBHOOK_URL`. Verify network connectivity (corporate VPN may block outbound webhooks to `hooks.slack.com`).

### Skills not appearing after install
- **Cause:** Claude Code only discovers skills at session start.
- **Fix:** Start a new Claude Code session. Verify the skill folder exists at `~/.claude/skills/<skill-name>/SKILL.md`. Check that `SKILL.md` has valid YAML frontmatter with `name` and `description`.

### Config file missing or invalid
- **Cause:** `~/.claude/metis-skills-config.json` not created during setup.
- **Fix:** Run the health check with `--fix` flag to auto-create. See `references/config-guide.md` for the expected file structure.
