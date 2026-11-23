"""Shared helpers for the demo-video pipeline: storyboard loading, paths, ffmpeg, audio."""
import json, os, re, subprocess, sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


REQUIRED = {'playwright': 'playwright', 'imageio_ffmpeg': 'imageio-ffmpeg', 'numpy': 'numpy', 'PIL': 'pillow'}


def check_deps():
    """Name every missing package in one go, with the one pip line that installs them."""
    import importlib.util
    missing = [pkg for mod, pkg in REQUIRED.items() if importlib.util.find_spec(mod) is None]
    if missing:
        sys.exit('Missing Python packages: %s\nInstall them with:\n  "%s" -m pip install %s'
                 % (', '.join(missing), sys.executable, ' '.join(missing)))


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit('Missing dependency: pip install imageio-ffmpeg')


class Board:
    """A storyboard file plus the paths derived from it."""
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.dir = os.path.dirname(self.path)
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)
        self.out = os.path.join(self.dir, self.data.get('out_dir', 'out'))
        os.makedirs(self.out, exist_ok=True)

    def rel(self, p):
        """Resolve a path written in the storyboard (relative to the storyboard file, ~ allowed)."""
        if not p:
            return p
        p = os.path.expanduser(p)
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(self.dir, p))

    def json_out(self, name, obj):
        with open(os.path.join(self.out, name), 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=1)

    def json_in(self, name):
        p = os.path.join(self.out, name)
        if not os.path.exists(p):
            return None
        with open(p, encoding='utf-8') as f:
            return json.load(f)


def pcm(path, rate=16000):
    """Mono float32 samples of any audio file."""
    import numpy as np
    raw = subprocess.run([ffmpeg(), '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(rate), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype('float32') / 32768


def norm(word):
    return re.sub(r'[^a-z0-9]', '', word.lower())
