"""Help request → Slack post for metis-claude-help.

The user describes what they need help with in their own words; this script
posts a #claude_help message tagged HELP REQUEST so a teammate can pick it up.
Environment details (OS, Python version) are captured automatically.
"""

import argparse
import platform
import sys
from pathlib import Path

# notify.py sits in the same directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from notify import send_slack, format_help_request  # noqa: E402


def collect_environment():
    return {
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
    }


def main():
    parser = argparse.ArgumentParser(description="Post a help request to Slack")
    parser.add_argument("--question", required=True,
                        help="What the user is asking for help with")
    parser.add_argument("--author-name", default="")
    parser.add_argument("--author-email", default="")
    args = parser.parse_args()

    env = collect_environment()
    msg = format_help_request(
        author_name=args.author_name or "Unknown",
        author_email=args.author_email or "unknown@metisstrategy.com",
        question=args.question,
        os_info=env["os"],
        python_ver=env["python"],
    )

    if send_slack(msg):
        print("Help request posted to #claude_help.")
    else:
        print("ERROR: Help request not delivered (Slack webhook unreachable).")
        sys.exit(1)


if __name__ == "__main__":
    main()
