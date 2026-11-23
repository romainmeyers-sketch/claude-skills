"""Slack notification helper for metis-claude-help.

Sends formatted messages to #claude_help via incoming webhook.
Three message types with distinct titles:
  - NEW SKILL SUBMISSION
  - BUG REPORT
  - NEW TIP
"""

import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

SKILL_CONFIG = Path(__file__).resolve().parent.parent / "config.json"
USER_CONFIG = Path.home() / ".claude" / "metis-skills-config.json"


def load_webhook_url():
    for path in [SKILL_CONFIG, USER_CONFIG]:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                url = json.load(f).get("slack_webhook_url", "")
                if url:
                    return url
    return ""


def send_slack(message: str) -> bool:
    webhook_url = load_webhook_url()
    if not webhook_url:
        print("WARNING: slack_webhook_url not found in config.json or", USER_CONFIG)
        print("Slack notification skipped.")
        return False

    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except urllib.error.URLError as e:
        print(f"WARNING: Slack notification failed: {e}")
        return False


def _md_to_slack(text: str) -> str:
    """Convert markdown to Slack mrkdwn format."""
    lines = text.split("\n")
    result = []
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()
        if re.match(r"^\|[-\s|]+\|$", stripped):
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                in_table = True
                table_rows = [cells]
            else:
                table_rows.append(cells)
            continue
        if in_table:
            if table_rows:
                for row in table_rows[1:]:
                    if len(row) >= 2:
                        result.append(f"• `{row[0].strip('` ')}` {row[1]}")
                table_rows = []
            in_table = False
        if stripped.startswith("###"):
            result.append(f"\n*{stripped.lstrip('# ').strip()}*")
        elif stripped.startswith("##"):
            result.append(f"\n*{stripped.lstrip('# ').strip()}*")
        elif stripped.startswith("#"):
            result.append(f"\n*{stripped.lstrip('# ').strip()}*")
        elif stripped.startswith(">"):
            result.append(f">{stripped.lstrip('> ')}")
        elif "**" in stripped:
            converted = re.sub(r"\*\*(.+?)\*\*", r"*\1*", stripped)
            result.append(converted)
        else:
            result.append(line)

    if in_table and table_rows:
        for row in table_rows[1:]:
            if len(row) >= 2:
                result.append(f"• `{row[0].strip('` ')}` {row[1]}")

    return "\n".join(result)


def format_submission(skill_name: str, version: str, author_name: str,
                      author_email: str, description: str, filepath: str) -> str:
    slack_desc = _md_to_slack(description)
    msg = (
        f"\U0001f195 *NEW SKILL SUBMISSION*\n"
        f"Skill: `{skill_name}` v{version}\n"
        f"Author: {author_name} ({author_email})\n\n"
        f"{slack_desc}\n\n"
        f"Action needed: Review and approve/reject"
    )
    if filepath:
        msg += f"\n\U0001f4c1 Location: `{filepath}`"
    return msg


def format_bug(title: str, reporter_name: str, reporter_email: str,
               os_info: str, python_ver: str, summary: str, filepath: str,
               status: str = "open") -> str:
    status_emoji = "\U0001f534" if status == "open" else "\U0001f7e2"
    slack_summary = _md_to_slack(summary)
    msg = (
        f"\U0001f41b *BUG REPORT: {title}*\n"
        f"Status: {status_emoji} {status.capitalize()}\n"
        f"Reporter: {reporter_name} ({reporter_email})\n"
        f"Environment: {os_info}, Python {python_ver}\n\n"
        f"{slack_summary}"
    )
    if filepath:
        msg += f"\n\n\U0001f4c1 `{filepath}`"
    return msg


def format_tip(title: str, author_name: str, content: str, filepath: str) -> str:
    slack_content = _md_to_slack(content)
    msg = (
        f"\U0001f4a1 *NEW TIP: {title}*\n"
        f"By: {author_name}\n\n"
        f"{slack_content}"
    )
    if filepath:
        msg += f"\n\n\U0001f4c1 `{filepath}`"
    return msg


def format_help_request(author_name: str, author_email: str, question: str,
                        os_info: str = "", python_ver: str = "") -> str:
    env_line = ""
    if os_info or python_ver:
        env_line = f"Environment: {os_info}, Python {python_ver}\n"
    return (
        f"\U0001f64b *HELP REQUEST*\n"
        f"From: {author_name} ({author_email})\n"
        f"{env_line}"
        f"Question:\n{question}"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: notify.py <test>")
        sys.exit(1)
    if sys.argv[1] == "test":
        ok = send_slack("\U0001f9ea *TEST* — metis-claude-help Slack integration working!")
        sys.exit(0 if ok else 1)
