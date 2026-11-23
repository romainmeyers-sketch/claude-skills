"""Rebuild scripts/kokoro.lock.json from PyPI and the Hugging Face API. A deliberate step, never automatic.

  <venv python> kokoro_relock.py                          re-pin to today's two-week-old releases, same model commit
  <venv python> kokoro_relock.py --revision <commit>      ... and move the model to that hexgrad/Kokoro-82M commit
  <venv python> kokoro_relock.py --days 30 --out x.json   older releases only; write somewhere else to compare first

What it does, in order: resolves kokoro + soundfile in an empty throwaway venv with pip --dry-run (no package code
runs), capping every package to releases at least --days old, not yanked, not pre-release; takes every sha256 PyPI
publishes for those releases; keeps the spaCy model wheel pinned by hash (warns if the spaCy minor version moved, since
the model must match it); reads the model repository's file list at the chosen commit, downloads the model, config and
the locked voices at that commit, verifies each against the API's hash, and reads their pickles to rebuild the import
allowlist. Then it writes the lock and prints what moved. After that: run setup.py --kokoro and re-render one storyboard.
Run it with the skill's venv Python (it needs packaging and huggingface_hub).
"""
import argparse, datetime, hashlib, json, os, subprocess, sys, tempfile, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kokoro_lock as KL
from packaging.version import Version
from packaging.utils import canonicalize_name

ROOTS = ['kokoro==0.9.4', 'soundfile==0.14.0']
SOURCE_ONLY = ['docopt']
UTC = datetime.timezone.utc
_rel = {}


def releases(name):
    name = canonicalize_name(name)
    if name not in _rel:
        with urllib.request.urlopen('https://pypi.org/pypi/%s/json' % name, timeout=60) as r:
            _rel[name] = json.load(r)['releases']
    return _rel[name]


def newest_upload(files):
    return max(datetime.datetime.fromisoformat(f['upload_time_iso_8601'].replace('Z', '+00:00')) for f in files)


def usable(files, cutoff):
    return bool(files) and not any(f.get('yanked') for f in files) and newest_upload(files) <= cutoff


def cap_below(name, current, cutoff):
    c = [(Version(v), v) for v, files in releases(name).items() if _ver(v) and not Version(v).is_prerelease and Version(v) < Version(current) and usable(files, cutoff)]
    if not c:
        sys.exit('No release of %s older than the cutoff below %s' % (name, current))
    return max(c)[1]


def _ver(v):
    try:
        Version(v); return True
    except Exception:
        return False


def resolve(cutoff):
    """pip --dry-run in an empty venv, re-run with <= caps until every package is old enough."""
    with tempfile.TemporaryDirectory(prefix='kokoro-relock-') as tmp:
        subprocess.run([sys.executable, '-m', 'venv', os.path.join(tmp, 'venv')], check=True)
        py = os.path.join(tmp, 'venv', 'Scripts' if os.name == 'nt' else 'bin', 'python' + ('.exe' if os.name == 'nt' else ''))
        caps, cfile, rep = {}, os.path.join(tmp, 'constraints.txt'), os.path.join(tmp, 'report.json')
        for rnd in range(12):
            with open(cfile, 'w') as f:
                f.write(''.join('%s<=%s\n' % kv for kv in caps.items()))
            r = subprocess.run([py, '-m', 'pip', 'install', '--dry-run', '--ignore-installed', '--quiet', '--only-binary=:all:', '--no-binary', ','.join(SOURCE_ONLY),
                                '-c', cfile, '--report', rep] + ROOTS, capture_output=True, text=True)
            if r.returncode:
                sys.exit('pip could not resolve:\n' + r.stderr[-2000:])
            resolved = {canonicalize_name(i['metadata']['name']): i['metadata']['version'] for i in json.load(open(rep))['install']}
            young = sorted(n for n, v in resolved.items() if not usable(releases(n).get(v) or [], cutoff))
            print('  resolve round %d: %d packages, %d too new%s' % (rnd, len(resolved), len(young), ': ' + ', '.join(young) if young else ''))
            if not young:
                return resolved
            for n in young:
                caps[n] = cap_below(n, resolved[n], cutoff)
    sys.exit('resolution did not converge')


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=14); ap.add_argument('--revision'); ap.add_argument('--out', default=KL.LOCK_PATH)
    a = ap.parse_args()
    old = KL.load()
    today = datetime.datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    cutoff = today - datetime.timedelta(days=a.days)
    print('Re-pinning: releases on or before %s' % cutoff.date())
    resolved = resolve(cutoff)
    packages = {}
    for name, ver in sorted(resolved.items()):
        files = releases(name)[ver]
        packages[name] = {'version': ver, 'newest_upload': newest_upload(files).date().isoformat(), 'sha256': sorted({f['digests']['sha256'] for f in files}),
                          'wheels': sum(f['packagetype'] == 'bdist_wheel' for f in files), 'sdists': sum(f['packagetype'] == 'sdist' for f in files)}
    extra = old['extra_wheels']
    if resolved.get('spacy', '').rsplit('.', 1)[0] != old['packages']['spacy']['version'].rsplit('.', 1)[0]:
        print('  WARNING: spaCy moved to %s; the pinned en_core_web_sm %s matches spaCy %s. Update extra_wheels by hand after checking the new model release.'
              % (resolved['spacy'], extra['en_core_web_sm']['version'], old['packages']['spacy']['version']))
    for name, w in extra.items():
        data = urllib.request.urlopen(w['url'], timeout=120).read()
        got = sha256_bytes(data)
        print('  %s wheel: %d bytes, sha256 %s (%s)' % (name, len(data), got[:16], 'unchanged' if got == w['sha256'] else 'CHANGED, was ' + w['sha256'][:16]))
        if got != w['sha256']:
            sys.exit('The %s wheel at %s no longer matches the lock. GitHub publishes no hash for it; verify the release by hand before accepting it.' % (name, w['url']))
    # model files at the chosen commit
    from huggingface_hub import hf_hub_download
    repo, rev = old['model']['repo'], a.revision or old['model']['revision']
    tree = {e['path']: e for e in json.load(urllib.request.urlopen('https://huggingface.co/api/models/%s/tree/%s?recursive=true' % (repo, rev), timeout=60)) if e['type'] == 'file'}
    head = json.load(urllib.request.urlopen('https://huggingface.co/api/models/%s/commits/%s' % (repo, rev), timeout=60))[0]
    if head['id'] != rev:
        sys.exit('revision %s is not a full commit id (the API resolved it to %s); pin the full id' % (rev, head['id']))
    print('  model: %s @ %s (%s, "%s"), %d files, %d voices' % (repo, rev[:12], head['date'][:10], head['title'][:40], len(tree), sum(p.startswith('voices/') for p in tree)))
    want = list(old['model']['files']) + ['voices/%s.pt' % v for v in old['model']['default_voices']]
    files, allow = {}, set()
    for rel in want:
        e = tree[rel]
        local = os.path.realpath(hf_hub_download(repo, rel, revision=rev))
        data = open(local, 'rb').read()
        exp = e['lfs']['oid'] if e.get('lfs') else hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
        got = sha256_bytes(data) if e.get('lfs') else hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
        if got != exp or len(data) != e['size']:
            sys.exit('%s at %s does not match the Hugging Face API metadata' % (rel, rev[:12]))
        files[rel] = {'size': len(data), 'sha256': sha256_bytes(data)}
        if rel.endswith(('.pt', '.pth')):
            allow |= KL.pickle_globals(local)
        print('  %-22s %11d  verified' % (rel, len(data)))
    voices = {p.split('/')[1][:-3]: {'size': e['size'], 'sha256': e['lfs']['oid']} for p, e in sorted(tree.items()) if p.startswith('voices/') and e.get('lfs')}
    new = dict(old)
    new.update({'generated': today.date().isoformat(), 'packages': packages, 'pickle_allowlist': sorted(allow),
                'rule': old['rule'].replace(old['generated'], today.date().isoformat()),
                'model': {**old['model'], 'revision': rev, 'commit_date': head['date'][:10], 'files': {k: v for k, v in files.items() if not k.startswith('voices/')}, 'voices': voices}})
    moved = [(n, old['packages'].get(n, {}).get('version'), p['version']) for n, p in packages.items() if old['packages'].get(n, {}).get('version') != p['version']]
    gone = [n for n in old['packages'] if n not in packages]
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(new, f, indent=1)
    print('\nwrote %s' % a.out)
    print('packages that moved: %s' % (', '.join('%s %s -> %s' % m for m in moved) or 'none')); print('packages dropped: %s' % (', '.join(gone) or 'none'))
    print('pickle allowlist: %s' % ', '.join(sorted(allow)))
    print('model commit: %s -> %s' % (old['model']['revision'][:12], rev[:12]))
    print('\nNext: run setup.py --kokoro, then re-render one Kokoro storyboard before trusting the new pins.')


if __name__ == '__main__':
    main()
