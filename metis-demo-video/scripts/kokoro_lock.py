"""The Kokoro lock (kokoro.lock.json): what setup.py installs and what voice.py refuses to run without.

Standard library only, so it can run before kokoro or torch exist. Everything Kokoro needs is pinned here with hashes:
the Python packages (every sha256 PyPI publishes for each exact release), the spaCy English model wheel, and the
hexgrad/Kokoro-82M model and voice files at one git commit. voice.py calls ensure() before it imports kokoro; setup.py
calls the same checks after downloading. A mismatch stops the run with a plain message: nothing is patched around.
"""
import hashlib, json, os, pickletools, sys, zipfile
from importlib import metadata

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK_PATH = os.path.join(HERE, 'kokoro.lock.json')


def load():
    with open(LOCK_PATH, encoding='utf-8') as f:
        return json.load(f)


def lock_sha256():
    return sha256_file(LOCK_PATH)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def requirements_text(lock):
    """A pip requirements file in --require-hashes form: one exact version per package, every published hash allowed."""
    lines = []
    for name, p in lock['packages'].items():
        lines.append('%s==%s %s' % (name, p['version'], ' '.join('--hash=sha256:' + h for h in p['sha256'])))
    for name, w in lock.get('extra_wheels', {}).items():
        lines.append('%s @ %s --hash=sha256:%s' % (name, w['url'], w['sha256']))
    return '\n'.join(lines) + '\n'


def _norm(name):
    return name.lower().replace('_', '-')


def package_problems(lock):
    """Installed packages that are missing or not at the locked version, in THIS interpreter."""
    out = []
    wanted = {**{n: p['version'] for n, p in lock['packages'].items()}, **{n: w['version'] for n, w in lock.get('extra_wheels', {}).items()}}
    for name, ver in wanted.items():
        try:
            have = metadata.version(name)
        except metadata.PackageNotFoundError:
            out.append('%s is not installed (lock wants %s)' % (name, ver)); continue
        if have != ver:
            out.append('%s is %s, lock wants %s' % (name, have, ver))
    return out


def hf_cache_dir():
    return os.environ.get('HF_HUB_CACHE') or os.path.join(os.environ.get('HF_HOME') or os.path.join(os.path.expanduser('~'), '.cache', 'huggingface'), 'hub')


def model_file(lock, rel):
    """Where huggingface_hub puts a file of the pinned revision (the standard cache layout)."""
    m = lock['model']
    return os.path.join(hf_cache_dir(), 'models--' + m['repo'].replace('/', '--'), 'snapshots', m['revision'], rel)


def voice_file(lock, voice):
    return model_file(lock, 'voices/%s.pt' % voice)


def pickle_globals(path):
    """Every module.name a pickle inside a torch zip file would import when loaded."""
    found = set()
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not n.endswith('.pkl'):
                continue
            strings = []
            for op, arg, pos in pickletools.genops(z.read(n)):
                if op.name in ('SHORT_BINUNICODE', 'BINUNICODE', 'UNICODE', 'STRING', 'SHORT_BINSTRING', 'BINSTRING'):
                    strings.append(arg)
                if op.name == 'GLOBAL':
                    found.add(arg.replace(' ', '.'))
                elif op.name == 'STACK_GLOBAL':
                    found.add('%s.%s' % (strings[-2], strings[-1]))
    return found


def file_problems(lock, rel, expect, scan=True):
    """Checks one model or voice file against the lock: present, right size, right sha256, pickle imports only allowlisted names."""
    path = model_file(lock, rel)
    if not os.path.exists(path):
        return ['%s is not downloaded' % rel]
    real = os.path.realpath(path)
    if os.path.getsize(real) != expect['size']:
        return ['%s is %d bytes, lock says %d' % (rel, os.path.getsize(real), expect['size'])]
    if sha256_file(real) != expect['sha256']:
        return ['%s does not match its locked sha256' % rel]
    if scan and (rel.endswith('.pt') or rel.endswith('.pth')):
        try:
            bad = pickle_globals(real) - set(lock['pickle_allowlist'])
        except Exception as e:
            return ['%s could not be scanned as a torch file (%s)' % (rel, e)]
        if bad:
            return ['%s would import %s on load, which the lock does not allow' % (rel, ', '.join(sorted(bad)))]
    return []


def model_problems(lock, voices=()):
    out = []
    for rel, expect in lock['model']['files'].items():
        out += file_problems(lock, rel, expect)
    for v in voices:
        if v not in lock['model']['voices']:
            out.append('voice "%s" is not in the lock (not a Kokoro-82M voice at the pinned commit)' % v); continue
        out += file_problems(lock, 'voices/%s.pt' % v, lock['model']['voices'][v])
    return out


_checked = {'packages': None, 'model': None, 'voices': set()}


def ensure(voice):
    """Called by voice.py before kokoro is imported and before each new voice is used. Exits on any problem."""
    lock = load()
    if _checked['packages'] is None:
        _checked['packages'] = package_problems(lock)
    if _checked['model'] is None:
        _checked['model'] = model_problems(lock)
    probs = list(_checked['packages']) + list(_checked['model'])
    if voice not in _checked['voices']:
        probs += model_problems({**lock, 'model': {**lock['model'], 'files': {}}}, [voice])
    if probs:
        sys.exit('Kokoro is not in the verified state the skill expects, so it will not run:\n  ' + '\n  '.join(probs) +
                 '\nRun the setup step, which downloads, verifies and scans everything against scripts/kokoro.lock.json:\n'
                 '  "%s" "%s" --kokoro%s' % (sys.executable, os.path.join(HERE, 'setup.py'), '' if voice in lock['model']['default_voices'] else ' --voice ' + voice))
    _checked['voices'].add(voice)
    return lock


if __name__ == '__main__':
    lk = load()
    print('lock sha256', lock_sha256()[:16], '| %d packages, model %s @ %s, %d voices (%d default)' % (len(lk['packages']), lk['model']['repo'], lk['model']['revision'][:12], len(lk['model']['voices']), len(lk['model']['default_voices'])))
    pp, mp = package_problems(lk), model_problems(lk, lk['model']['default_voices'])
    print('package problems:', pp or 'none'); print('model problems:', mp or 'none')
