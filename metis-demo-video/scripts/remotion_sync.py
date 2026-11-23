"""Refresh the vendored Remotion agent skills in references/remotion/.

  python remotion_sync.py            pull the latest remotion-dev/skills from GitHub
  python remotion_sync.py --check    only print the vendored and the latest version

Remotion publishes its own agent skills (github.com/remotion-dev/skills). We keep one
copy of the "remotion-best-practices" bundle inside this skill so a video request has
the Remotion knowledge without installing a dozen extra skills. The bundle's SKILL.md
is kept as ROUTER.md so Claude Code does not register it as a separate skill.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(os.path.dirname(HERE), 'references', 'remotion')
REPO = 'https://github.com/remotion-dev/skills'


def version(path):
    try:
        m = re.search(r'^version:\s*(\S+)', open(path, encoding='utf-8').read(), re.M)
        return m.group(1) if m else '?'
    except OSError:
        return 'none'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'skills')
        subprocess.run(['git', 'clone', '--depth', '1', '-q', REPO, src], check=True)
        bundle = os.path.join(src, 'skills', 'remotion-best-practices')
        old, new = version(os.path.join(DEST, 'ROUTER.md')), version(os.path.join(bundle, 'SKILL.md'))
        print('vendored: %s   latest: %s' % (old, new))
        if a.check or old == new:
            return
        staged = DEST + '.new'
        if os.path.exists(staged):
            shutil.rmtree(staged)
        shutil.copytree(bundle, staged, ignore=shutil.ignore_patterns('agents', 'remotion-icon.svg', '.git'))
        os.replace(os.path.join(staged, 'SKILL.md'), os.path.join(staged, 'ROUTER.md'))
        for root, dirs, files in os.walk(staged, topdown=False):      # drop folders left empty by the ignore
            if not os.listdir(root):
                os.rmdir(root)
        if os.path.exists(DEST):
            shutil.rmtree(DEST)
        os.replace(staged, DEST)
        print('updated references/remotion to %s' % new)


if __name__ == '__main__':
    sys.exit(main())
