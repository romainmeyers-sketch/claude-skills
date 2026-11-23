"""Skill publishing workflow for metis-claude-help.

Creates a properly structured skill submission in the G Drive incoming folder,
generates SKILL.md, tile.json, and SUBMISSION.md, then sends a Slack notification.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

CONFIG_PATH = Path.home() / ".claude" / "metis-skills-config.json"


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


def generate_skill_md(name: str, description: str, example: str,
                      author_name: str, author_email: str) -> str:
    return f"""---
name: {name}
description: >
  {description}
---

# {name.replace('-', ' ').title()}

{description}

## Usage

{example}

## Author

{author_name} — {author_email}
"""


def generate_tile_json(name: str, version: str, summary: str) -> dict:
    return {
        "name": f"metis-strategy/{name}",
        "version": version,
        "scope": "firm",
        "private": False,
        "summary": summary,
        "skills": {
            name: {
                "path": "SKILL.md"
            }
        }
    }


def generate_submission_md(name: str, version: str, description: str,
                           example: str, author_name: str,
                           author_email: str) -> str:
    today = date.today().isoformat()
    return f"""# Skill Submission

**Skill:** {name}
**Author:** {author_name} ({author_email})
**Version:** {version}
**Submitted:** {today}

## Description

{description}

## Working Example

{example}

## Status

Pending review
"""


def main():
    parser = argparse.ArgumentParser(description="Publish a new skill")
    parser.add_argument("--name", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--example", required=True)
    parser.add_argument("--author-name", required=True)
    parser.add_argument("--author-email", required=True)
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--category", default="")
    args = parser.parse_args()

    config = load_config()
    incoming_dir = Path(config.get("incoming_dir", ""))

    skill_slug = slugify(args.name)
    author_slug = slugify(args.author_name.split()[0]) if args.author_name else "unknown"
    today = date.today().isoformat()
    folder_name = f"{today}-{skill_slug}-{author_slug}"
    submission_dir = incoming_dir / folder_name

    file_saved = False
    try:
        submission_dir.mkdir(parents=True, exist_ok=True)

        skill_md = generate_skill_md(
            skill_slug, args.description, args.example,
            args.author_name, args.author_email
        )
        (submission_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

        tile = generate_tile_json(skill_slug, args.version, args.description[:100])
        (submission_dir / "tile.json").write_text(
            json.dumps(tile, indent=2), encoding="utf-8"
        )

        submission_md = generate_submission_md(
            skill_slug, args.version, args.description, args.example,
            args.author_name, args.author_email
        )
        (submission_dir / "SUBMISSION.md").write_text(submission_md, encoding="utf-8")

        file_saved = True
        print("\nSkill submission created!")
        print(f"   Folder: {submission_dir}")
        print(f"   Files: SKILL.md, tile.json, SUBMISSION.md")
    except OSError as e:
        print(f"\n   WARNING: Could not save submission files: {e}")
        print("   Continuing with Slack notification only.")

    # Send Slack notification (independent of file save)
    try:
        from notify import send_slack, format_submission
        saved_path = str(submission_dir) if file_saved else ""
        msg = format_submission(
            skill_slug, args.version, args.author_name,
            args.author_email, args.description[:200], saved_path
        )
        if send_slack(msg):
            print("   Slack notification sent to #metis-ai-help")
        else:
            print("   Slack notification skipped (webhook not configured)")
    except Exception as e:
        print(f"   WARNING: Slack notification failed: {e}")

    output = {
        "status": "submitted" if file_saved else "slack_only",
        "folder": folder_name,
        "path": str(submission_dir) if file_saved else "",
        "skill_name": skill_slug,
        "version": args.version,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
