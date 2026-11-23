# Configuration Guide

## metis-skills-config.json

Location: `~/.claude/metis-skills-config.json`

This file tells all Metis skills where to find shared resources on Google Drive.

### Required fields

```json
{
  "root_dir": "G:/Shared drives/Knowledge Management/Claude Code/Metis-Skills",
  "incoming_dir": "G:/Shared drives/Knowledge Management/Claude Code/Incoming-Skills",
  "faq_dir": "G:/Shared drives/Knowledge Management/Claude Code/FAQ-Tips",
  "bugs_dir": "G:/Shared drives/Knowledge Management/Claude Code/Bug-Reports"
}
```

| Field | Purpose |
|---|---|
| `root_dir` | Published skills directory (source for registry and install) |
| `incoming_dir` | Submission inbox for new skills awaiting review |
| `faq_dir` | FAQ and tips shared by all consultants |
| `bugs_dir` | Bug report storage |

### How it gets created

The first-time setup script (`team-setup/scripts/first-time-setup.sh`) creates this file automatically. If it is missing, run the health check with `--fix`:

```bash
PYTHON="C:/Users/navan/AppData/Local/Programs/Python/Python312/pythonw.exe"
"$PYTHON" "$HOME/.metis/health-check.py" --fix
```

### config.json (skill-local)

Location: `<skill-dir>/config.json`

Contains the Slack webhook URL for notifications. Ships with the skill; no per-user setup needed.

```json
{
  "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/..."
}
```

This URL is shared across all consultants. Do not change it unless migrating to a new Slack channel.
