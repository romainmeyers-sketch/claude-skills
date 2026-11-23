"""Bug report creation for metis-claude-help.

Collects user description, auto-captures environment details,
writes report to G Drive, and sends Slack notification.
"""

import argparse
import json
import platform
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

CONFIG_PATH = Path.home() / ".claude" / "metis-skills-config.json"
LOCAL_SKILLS = Path.home() / ".claude" / "skills"
SYNC_LOG = Path.home() / ".claude" / "last-sync.log"


def load_config():
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config not found at {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    return text.strip("-")


def capture_environment():
    os_info = f"{platform.system()} {platform.release()}"
    try:
        os_version = platform.version()
        os_info += f" ({os_version})"
    except Exception:
        pass

    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    installed_skills = []
    if LOCAL_SKILLS.exists():
        for d in sorted(LOCAL_SKILLS.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                ver_file = d / ".metis-version"
                ver = ver_file.read_text(encoding="utf-8").strip() if ver_file.exists() else "?"
                installed_skills.append(f"{d.name} (v{ver})")

    sync_log_excerpt = ""
    if SYNC_LOG.exists():
        try:
            lines = SYNC_LOG.read_text(encoding="utf-8", errors="replace").strip().split("\n")
            sync_log_excerpt = "\n".join(lines[-10:])
        except Exception:
            sync_log_excerpt = "(could not read sync log)"

    return {
        "os": os_info,
        "python": python_ver,
        "installed_skills": installed_skills,
        "sync_log": sync_log_excerpt,
    }


def create_report(bugs_dir: Path, title: str, description: str,
                  author_name: str, author_email: str):
    today = date.today().isoformat()
    env = capture_environment()

    author_slug = slugify(author_name.split()[0]) if author_name else "anon"
    title_slug = slugify(title)[:50]
    filename = f"{today}-{title_slug}-{author_slug}.md"

    skills_list = "\n".join(f"  - {s}" for s in env["installed_skills"]) or "  (none found)"

    report = f"""---
status: open
reporter: {author_name}
date: {today}
---

# Bug Report: {title}

**Reporter:** {author_name} ({author_email})
**Date:** {today}
**Status:** Open
**Environment:** {env['os']}, Python {env['python']}

## Description

{description}

## Environment Details

- **OS:** {env['os']}
- **Python:** {env['python']}
- **Installed Skills:**
{skills_list}

## Last Sync Log (last 10 lines)

```
{env['sync_log']}
```
"""

    filepath = bugs_dir / filename
    file_saved = False
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(report, encoding="utf-8")
        file_saved = True
        print("\nBug report created!")
        print(f"   File: {filepath}")
    except OSError as e:
        print(f"\n   WARNING: Could not save bug report file: {e}")
        print("   Continuing with Slack notification only.")

    # Send Slack notification (independent of file save)
    try:
        from notify import send_slack, format_bug
        summary = description[:200].replace("\n", " ")
        saved_path = str(filepath) if file_saved else ""
        msg = format_bug(title, author_name, author_email,
                         env["os"], env["python"], summary, saved_path)
        if send_slack(msg):
            print("   Slack notification sent to #metis-ai-help")
    except Exception as e:
        print(f"   WARNING: Slack notification failed: {e}")

    return {"filename": filename, "path": str(filepath) if file_saved else ""}


def main():
    parser = argparse.ArgumentParser(description="Bug Report Creator")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--author-name", default="Unknown")
    parser.add_argument("--author-email", default="")
    args = parser.parse_args()

    config = load_config()
    bugs_dir = Path(config.get("bugs_dir", ""))

    if not bugs_dir.exists():
        bugs_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created Bug-Reports directory: {bugs_dir}")

    create_report(bugs_dir, args.title, args.description,
                  args.author_name, args.author_email)


if __name__ == "__main__":
    main()
