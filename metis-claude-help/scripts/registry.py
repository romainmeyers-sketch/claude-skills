"""Skill registry — list, search, detail, install skills from G Drive.

Reads skills-versions.json manifest and individual tile.json files
to build a registry of available skills with install status.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".claude" / "metis-skills-config.json"
LOCAL_SKILLS = Path.home() / ".claude" / "skills"


def load_config():
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config not found at {CONFIG_PATH}")
        print("Create it with at minimum: {\"root_dir\": \"G:/Shared drives/...\"}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_root_dir(config):
    root = Path(config.get("root_dir", ""))
    if not root.exists():
        print(f"ERROR: Skills root not found: {root}")
        print("Is Google Drive mounted? Check root_dir in config.")
        sys.exit(1)
    return root


def load_manifest(root: Path):
    manifest_path = root / "skills-versions.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def read_tile_json(skill_dir: Path):
    tile_path = skill_dir / "tile.json"
    if tile_path.exists():
        with open(tile_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def is_installed(skill_name: str) -> bool:
    return (LOCAL_SKILLS / skill_name).exists()


def get_installed_version(skill_name: str):
    version_file = LOCAL_SKILLS / skill_name / ".metis-version"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    tile = read_tile_json(LOCAL_SKILLS / skill_name)
    if tile:
        return tile.get("version", "?")
    return "?"


def discover_skills(root: Path, manifest):
    """Build list of skills from manifest or directory scan."""
    skills = []

    if manifest and "skills" in manifest:
        for name, info in manifest["skills"].items():
            default_ver = info.get("default", "latest")
            available = info.get("available", [default_ver])

            skill_dir = root / name
            if not skill_dir.exists():
                for ver in [default_ver] + available:
                    candidate = root / name / ver / name
                    if candidate.exists():
                        skill_dir = candidate
                        break

            tile = read_tile_json(skill_dir) if skill_dir.exists() else None
            summary = tile.get("summary", "") if tile else ""
            version = tile.get("version", default_ver) if tile else default_ver

            installed = is_installed(name)
            local_ver = get_installed_version(name) if installed else None

            skills.append({
                "name": name,
                "version": version,
                "summary": summary,
                "installed": installed,
                "local_version": local_ver,
                "available_versions": available,
                "path": str(skill_dir),
            })
    else:
        for d in sorted(root.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                tile = read_tile_json(d)
                skill_md = d / "SKILL.md"
                if not tile and not skill_md.exists():
                    continue
                name = d.name
                version = tile.get("version", "?") if tile else "?"
                summary = tile.get("summary", "") if tile else ""
                installed = is_installed(name)
                local_ver = get_installed_version(name) if installed else None
                skills.append({
                    "name": name,
                    "version": version,
                    "summary": summary,
                    "installed": installed,
                    "local_version": local_ver,
                    "path": str(d),
                })

    return skills


def list_skills(skills):
    print(f"\n📦 Metis Skills Registry ({len(skills)} skills)\n")
    for s in skills:
        status = "✅ installed" if s["installed"] else "⬇ available"
        ver = f"v{s['version']}"
        print(f"  {s['name']:<25} {ver:<10} {status:<14} {s['summary']}")
    print(f"\nSearch: run with --action search --query \"<keyword>\" to filter")


def search_skills(skills, query: str):
    query_lower = query.lower()
    matches = [
        s for s in skills
        if query_lower in s["name"].lower() or query_lower in s["summary"].lower()
    ]
    if not matches:
        print(f"No skills matching \"{query}\". Try a different keyword.")
        return
    print(f"\n🔍 Search results for \"{query}\" ({len(matches)} matches)\n")
    for s in matches:
        status = "✅ installed" if s["installed"] else "⬇ available"
        ver = f"v{s['version']}"
        print(f"  {s['name']:<25} {ver:<10} {status:<14} {s['summary']}")


def skill_detail(skills, name: str):
    match = next((s for s in skills if s["name"] == name), None)
    if not match:
        close = [s for s in skills if name.lower() in s["name"].lower()]
        if close:
            print(f"Skill \"{name}\" not found. Did you mean?")
            for s in close:
                print(f"  - {s['name']}")
        else:
            print(f"Skill \"{name}\" not found in registry.")
        return

    skill_dir = Path(match["path"])
    print(f"\n📦 {match['name']} v{match['version']}")
    print(f"   Status: {'✅ Installed' if match['installed'] else '⬇ Available'}")
    if match.get("local_version"):
        print(f"   Local version: v{match['local_version']}")
    print(f"   Summary: {match['summary']}")
    print(f"   Source: {match['path']}")

    if match.get("available_versions"):
        print(f"   Versions: {', '.join(match['available_versions'])}")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8")
        in_frontmatter = False
        body_lines = []
        for line in content.split("\n"):
            if line.strip() == "---":
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter:
                body_lines.append(line)
        body = "\n".join(body_lines[:30]).strip()
        if body:
            print(f"\n--- Description ---\n{body}")
            if len(body_lines) > 30:
                print(f"\n   ... ({len(body_lines) - 30} more lines)")


def install_skill(skills, name: str):
    match = next((s for s in skills if s["name"] == name), None)
    if not match:
        print(f"ERROR: Skill \"{name}\" not found in registry.")
        sys.exit(1)

    if match["installed"]:
        print(f"Skill \"{name}\" already installed (v{match.get('local_version', '?')}).")
        print("To update, the skill will be overwritten.")

    source = Path(match["path"])
    dest = LOCAL_SKILLS / name

    if not source.exists():
        print(f"ERROR: Source directory not found: {source}")
        sys.exit(1)

    print(f"Installing {name} v{match['version']}...")
    print(f"  From: {source}")
    print(f"  To:   {dest}")

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

    version_marker = dest / ".metis-version"
    version_marker.write_text(match["version"], encoding="utf-8")

    print(f"\n✅ {name} v{match['version']} installed successfully.")
    print("Restart Claude Code to activate the skill.")


def main():
    parser = argparse.ArgumentParser(description="Metis Skills Registry")
    parser.add_argument("--action", required=True,
                        choices=["list", "search", "detail", "install"])
    parser.add_argument("--query", default="")
    parser.add_argument("--name", default="")
    args = parser.parse_args()

    config = load_config()
    root = get_root_dir(config)
    manifest = load_manifest(root)
    skills = discover_skills(root, manifest)

    if args.action == "list":
        list_skills(skills)
    elif args.action == "search":
        if not args.query:
            print("ERROR: --query required for search action")
            sys.exit(1)
        search_skills(skills, args.query)
    elif args.action == "detail":
        if not args.name:
            print("ERROR: --name required for detail action")
            sys.exit(1)
        skill_detail(skills, args.name)
    elif args.action == "install":
        if not args.name:
            print("ERROR: --name required for install action")
            sys.exit(1)
        install_skill(skills, args.name)

    output = {
        "action": args.action,
        "skill_count": len(skills),
        "skills": [{"name": s["name"], "version": s["version"],
                     "installed": s["installed"], "summary": s["summary"]}
                    for s in skills]
    }
    json_path = Path(__file__).parent / "last_result.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()
