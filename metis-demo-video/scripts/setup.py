"""One-time setup: makes a private Python environment and checks everything the pipeline needs.

  python3 setup.py
  python3 setup.py --kokoro                 also installs Kokoro, for narration with no account and no key (about 1 GB with PyTorch)
  python3 setup.py --kokoro --voice bm_lewis  ... plus one more Kokoro voice (repeat --voice as needed)

The Kokoro step installs ONLY what scripts/kokoro.lock.json pins: exact package versions with their PyPI hashes
(pip --require-hashes), the spaCy English model wheel by hash, and the Kokoro-82M model and voice files at one git
commit, each checked by sha256 and scanned so its pickle imports nothing outside the lock's allowlist. Any mismatch
stops the step with a plain message; nothing is patched around. voice.py runs the same checks before it speaks.

Creates ~/.metis/demo-video/.venv (so nothing is installed into your system Python), installs playwright,
imageio-ffmpeg, numpy and pillow, checks for a browser, and tells you the exact command to run next.
Works on macOS, Linux and Windows (Python 3.10 or newer).
"""
import json, os, shutil, subprocess, sys, tempfile, zipfile

ROOT = os.path.join(os.path.expanduser('~'), '.metis', 'demo-video')
VENV = os.path.join(ROOT, '.venv')
PY = os.path.join(VENV, 'Scripts' if os.name == 'nt' else 'bin', 'python' + ('.exe' if os.name == 'nt' else ''))
HERE = os.path.dirname(os.path.abspath(__file__))


def venv_package_problems():
    """Which locked packages the venv is missing or has at another version (checked inside the venv's own Python)."""
    code = 'import sys, json; sys.path.insert(0, %r); import kokoro_lock as K; print(json.dumps(K.package_problems(K.load())))' % HERE
    r = subprocess.run([PY, '-c', code], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else ['could not check the environment: ' + r.stderr.strip()[-300:]]


def kokoro_step(extra_voices):
    """Install Kokoro from scripts/kokoro.lock.json and nothing else: pinned versions with hash-checked downloads,
    every wheel inspected before install, model and voice files verified against the lock and pickle-scanned."""
    sys.path.insert(0, HERE)
    import kokoro_lock as KL                               # standard library only
    lock = KL.load()
    model = lock['model']
    print('\nKokoro (narration with no key), from scripts/kokoro.lock.json (lock sha256 %s...)' % KL.lock_sha256()[:12])
    for v in extra_voices:
        if v not in model['voices']:
            sys.exit('"%s" is not a Kokoro-82M voice at the pinned commit. Voices in the lock: %s' % (v, ', '.join(sorted(model['voices']))))
    # 1. packages: only if something is missing or at another version
    probs = venv_package_problems()
    if not probs:
        print('  packages: all %d already at the locked versions' % len(lock['packages']))
    else:
        print('  packages: %d to install or change (%s%s)' % (len(probs), '; '.join(probs[:3]), '; ...' if len(probs) > 3 else ''))
        with tempfile.TemporaryDirectory(prefix='kokoro-wheels-') as tmp:
            req = os.path.join(tmp, 'requirements.txt')
            with open(req, 'w', encoding='utf-8') as f:
                f.write(KL.requirements_text(lock))
            print('  downloading %d pinned packages, every file checked against its locked sha256 (about 300 MB)...' % len(lock['packages']))
            subprocess.run([PY, '-m', 'pip', 'download', '-q', '--require-hashes', '--no-deps', '--only-binary=:all:',
                            '--no-binary', ','.join(lock.get('source_only', [])), '-r', req, '-d', tmp], check=True)
            files = sorted(f for f in os.listdir(tmp) if f != 'requirements.txt')
            bad, outside = [], []
            for fn in files:                                   # look inside every wheel before anything is installed
                if not fn.endswith('.whl'):
                    continue
                with zipfile.ZipFile(os.path.join(tmp, fn)) as z:
                    for n in z.namelist():
                        if n.endswith('.pth') and not (fn.startswith('setuptools-') and n.endswith('distutils-precedence.pth')):
                            bad.append('%s carries a startup file that Python would run at every launch: %s' % (fn, n))
                        if '.data/' in n and '/purelib/' not in n and '/platlib/' not in n:
                            outside.append('%s: %s' % (fn.split('-')[0], n.split('.data/')[1]))
            if bad:
                sys.exit('Stopped before installing anything:\n  ' + '\n  '.join(bad))
            print('  inspected %d files: no startup .pth files%s' % (len(files), ('; outside site-packages only: ' + ', '.join(outside)) if outside else ''))
            subprocess.run([PY, '-m', 'pip', 'install', '-q', '--require-hashes', '--no-index', '--find-links', tmp, '--no-deps', '-r', req], check=True)
        probs = venv_package_problems()
        if probs:
            sys.exit('After installing, the environment still does not match the lock:\n  ' + '\n  '.join(probs))
        print('  installed: every package now matches the lock')
    # 2. model and voices: download what is missing at the pinned commit, then verify and scan everything we will load
    voices = list(dict.fromkeys(model['default_voices'] + extra_voices))
    need = list(model['files']) + ['voices/%s.pt' % v for v in voices]
    missing = [rel for rel in need if not os.path.exists(KL.model_file(lock, rel))]
    if missing:
        print('  downloading %d model files from %s at commit %s...' % (len(missing), model['repo'], model['revision'][:12]))
        code = 'from huggingface_hub import hf_hub_download\nimport sys\nfor f in sys.argv[1:]: hf_hub_download(%r, f, revision=%r)' % (model['repo'], model['revision'])
        subprocess.run([PY, '-c', code] + missing, check=True, env={**os.environ, 'HF_HUB_DISABLE_PROGRESS_BARS': '1'})
    probs = KL.model_problems(lock, voices)
    if probs:
        sys.exit('Model files do not match the lock, so Kokoro will not be used:\n  ' + '\n  '.join(probs))
    print('  %-20s %11s  %-18s %s' % ('file', 'bytes', 'sha256', 'check'))
    for rel in need:
        exp = model['files'].get(rel) or model['voices'][rel.split('/')[1][:-3]]
        print('  %-20s %11d  %s...  size, sha256 and pickle imports OK' % (rel, exp['size'], exp['sha256'][:16]))
    with open(os.path.join(ROOT, 'kokoro.verified.json'), 'w', encoding='utf-8') as f:
        json.dump({'lock_sha256': KL.lock_sha256(), 'voices': voices, 'python': PY}, f, indent=1)
    print('  Kokoro ready: %d voices verified (%s). Add one with: setup.py --kokoro --voice <id>' % (len(voices), ', '.join(voices)))


def main():
    if sys.version_info < (3, 10):
        sys.exit('Python 3.10 or newer is required (this is %d.%d).' % sys.version_info[:2])
    os.makedirs(ROOT, exist_ok=True)
    if not os.path.exists(PY):
        print('Creating environment at', VENV)
        subprocess.run([sys.executable, '-m', 'venv', VENV], check=True)
    print('Installing packages (about a minute the first time)...')
    subprocess.run([PY, '-m', 'pip', 'install', '-q', '--upgrade', 'pip'], check=True)
    subprocess.run([PY, '-m', 'pip', 'install', '-q', 'playwright', 'imageio-ffmpeg', 'numpy', 'pillow'], check=True)
    if '--kokoro' in sys.argv:
        kokoro_step([sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--voice' and i + 1 < len(sys.argv)])
    browsers = {'darwin': ['/Applications/Google Chrome.app', '/Applications/Microsoft Edge.app'],
                'win32': [r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe']}.get(sys.platform, [])
    found = [b for b in browsers if os.path.exists(b)] or [b for b in ('google-chrome', 'chromium', 'chromium-browser', 'microsoft-edge') if shutil.which(b)]
    if found:
        print('Browser found:', found[0])
    else:
        print('No Chrome or Edge found. Installing a private Chromium (about 150 MB)...')
        subprocess.run([PY, '-m', 'playwright', 'install', 'chromium'], check=True)
    key = os.environ.get('ELEVENLABS_API_KEY') or os.path.exists(os.path.join(ROOT, 'elevenlabs.key'))
    print('ElevenLabs key:', 'found' if key else 'not set (only needed for voiceover; see references/voiceover.md)')
    if '--kokoro' not in sys.argv:
        kok = subprocess.run([PY, '-c', 'import kokoro'], capture_output=True).returncode == 0
        print('Kokoro voices:', 'installed' if kok else 'not installed (optional: narration with no key, in stock voices; python3 setup.py --kokoro)')
    print('\nReady. Try the example (about 3 minutes):')
    print('  "%s" "%s" "%s"' % (PY, os.path.join(HERE, 'make.py'), os.path.join(HERE, '..', 'examples', 'storyboard.json')))


if __name__ == '__main__':
    main()
