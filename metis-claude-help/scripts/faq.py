"""FAQ and tips management for metis-claude-help.

Search existing tips/FAQ files and create new tips.
Files stored as flat dated markdown in G Drive FAQ-Tips folder.
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


def get_faq_dir(config):
    faq_dir = Path(config.get("faq_dir", ""))
    if not faq_dir.exists():
        faq_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created FAQ-Tips directory: {faq_dir}")
    return faq_dir


def search_faq(faq_dir: Path, query: str):
    query_lower = query.lower()
    results = []

    md_files = sorted(faq_dir.glob("*.md"), reverse=True)
    if not md_files:
        print("No FAQ/tips found yet. Be the first to share a tip!")
        return

    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        if query_lower in content.lower() or query_lower in f.name.lower():
            title = f.stem
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            contributor = ""
            for line in content.split("\n"):
                if "**Contributor:**" in line:
                    contributor = line.split("**Contributor:**")[1].strip()
                    break

            preview = ""
            in_content = False
            for line in content.split("\n"):
                if line.startswith("## Tip") or line.startswith("## Content"):
                    in_content = True
                    continue
                if in_content and line.strip():
                    preview = line.strip()[:150]
                    break

            results.append({
                "filename": f.name,
                "title": title,
                "contributor": contributor,
                "preview": preview,
            })

    if not results:
        print(f"No results for \"{query}\". Try different keywords.")
        print("Or share a tip with: metis-claude-help → Share a tip")
        return

    print(f"\n\U0001f50d FAQ/Tips matching \"{query}\" ({len(results)} results)\n")
    for r in results:
        print(f"  \U0001f4c4 {r['title']}")
        if r["contributor"]:
            print(f"     By: {r['contributor']}")
        if r["preview"]:
            print(f"     {r['preview']}")
        print(f"     File: {r['filename']}")
        print()


def list_recent(faq_dir: Path, count: int = 10):
    md_files = sorted(faq_dir.glob("*.md"), reverse=True)[:count]
    if not md_files:
        print("No FAQ/tips found yet. Be the first to share a tip!")
        return

    print(f"\n\U0001f4cb Recent Tips ({min(count, len(md_files))} shown)\n")
    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="replace")
        title = f.stem
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break
        date_prefix = f.name[:10] if len(f.name) > 10 else ""
        print(f"  {date_prefix}  {title}")


def create_tip(faq_dir: Path, title: str, content: str, links: str,
               tags: str, author_name: str, author_email: str):
    today = date.today().isoformat()
    author_slug = slugify(author_name.split()[0]) if author_name else "anon"
    title_slug = slugify(title)[:50]
    filename = f"{today}-{title_slug}-{author_slug}.md"

    links_section = ""
    if links:
        link_lines = "\n".join(f"- {l.strip()}" for l in links.split(",") if l.strip())
        links_section = f"\n## Links\n\n{link_lines}\n"

    tags_line = tags if tags else "general"

    tip_content = f"""# {title}

**Contributor:** {author_name} ({author_email})
**Date:** {today}
**Tags:** {tags_line}

## Tip

{content}
{links_section}"""

    filepath = faq_dir / filename
    file_saved = False
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(tip_content, encoding="utf-8")
        file_saved = True
        print("\nTip created!")
        print(f"   File: {filepath}")
    except OSError as e:
        print(f"\n   WARNING: Could not save tip file: {e}")
        print("   Continuing with Slack notification only.")

    # Send Slack notification (independent of file save)
    try:
        from notify import send_slack, format_tip
        saved_path = str(filepath) if file_saved else ""
        msg = format_tip(title, author_name, content, saved_path)
        if send_slack(msg):
            print("   Slack notification sent to #metis-ai-help")
    except Exception as e:
        print(f"   WARNING: Slack notification failed: {e}")

    return {"filename": filename, "path": str(filepath) if file_saved else "", "slack_sent": True}


def main():
    parser = argparse.ArgumentParser(description="FAQ & Tips Manager")
    parser.add_argument("--action", required=True,
                        choices=["search", "recent", "create-tip"])
    parser.add_argument("--query", default="")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--title", default="")
    parser.add_argument("--content", default="")
    parser.add_argument("--links", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--author-name", default="")
    parser.add_argument("--author-email", default="")
    args = parser.parse_args()

    config = load_config()
    faq_dir = get_faq_dir(config)

    if args.action == "search":
        if not args.query:
            print("ERROR: --query required for search")
            sys.exit(1)
        search_faq(faq_dir, args.query)
    elif args.action == "recent":
        list_recent(faq_dir, args.count)
    elif args.action == "create-tip":
        if not args.title or not args.content:
            print("ERROR: --title and --content required")
            sys.exit(1)
        create_tip(faq_dir, args.title, args.content, args.links,
                   args.tags, args.author_name, args.author_email)


if __name__ == "__main__":
    main()
