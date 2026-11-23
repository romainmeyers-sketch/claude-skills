"""Check for, and install, a newer version of this skill from the Video Hub.

  python3 self_update.py --check <version.json>     prints {"installed", "latest", "behind", "notes"}
  python3 self_update.py --install <bundle.json>    backs up the installed skill, installs the bundle, prints the result

Fetch the two files from the hub with the Artifact tool (action "read", url = the Video Hub, path =
"skill/version.json" or "skill/metis-demo-video.bundle.json"). Only Rohan and Romain can publish to the hub, so
the bundle comes from the skill's editors. Backups go to ~/.metis/demo-video/skill-backups/<version>-<time>/.
"""
import base64, datetime, json, os, re, shutil, sys

SKILL = os.path.join(os.path.expanduser('~'), '.claude', 'skills', 'metis-demo-video')
BACKUPS = os.path.join(os.path.expanduser('~'), '.metis', 'demo-video', 'skill-backups')


def installed_version():
    try:
        with open(os.path.join(SKILL, 'CHANGELOG.md'), encoding='utf-8') as f:
            m = re.search(r'v(\d+(?:\.\d+)+)', f.readline())
            return m.group(1) if m else '0'
    except OSError:
        return '0'


def vt(v):
    return tuple(int(x) for x in re.findall(r'\d+', str(v))) or (0,)


def check(path):
    with open(path, encoding='utf-8') as f:
        latest = json.load(f)
    have = installed_version()
    print(json.dumps({'installed': have, 'latest': latest.get('version'), 'behind': vt(have) < vt(latest.get('version')),
                      'notes': latest.get('notes', [])}, indent=2))


def install(path):
    with open(path, encoding='utf-8') as f:
        bundle = json.load(f)
    files = bundle.get('files') or {}
    if 'SKILL.md' not in files:
        sys.exit('That file is not a metis-demo-video bundle (no SKILL.md inside). Nothing was changed.')
    have, new = installed_version(), bundle.get('version', '?')
    staging = SKILL + '.updating'
    shutil.rmtree(staging, ignore_errors=True)
    for rel, data in files.items():
        if rel.startswith('/') or '..' in rel.split('/'):
            sys.exit('Unsafe path in bundle: %s. Nothing was changed.' % rel)
        dst = os.path.join(staging, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'wb') as out:
            out.write(base64.b64decode(data))
    backup = None
    if os.path.isdir(SKILL):
        os.makedirs(BACKUPS, exist_ok=True)
        backup = os.path.join(BACKUPS, '%s-%s' % (have, datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
        shutil.move(SKILL, backup)
    shutil.move(staging, SKILL)
    print(json.dumps({'updated_from': have, 'updated_to': new, 'files': len(files), 'backup': backup, 'skill': SKILL}, indent=2))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--check':
        check(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == '--install':
        install(sys.argv[2])
    else:
        sys.exit(__doc__)
