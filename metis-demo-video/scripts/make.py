"""Run the whole pipeline: [voice], render, mix, QA.

  python make.py storyboard.json             full video (voiceover first if the storyboard has one, + scene sheets and a timeline sheet every 1.5 s)
  python make.py storyboard.json --until 2   preview of scenes 0..2 (render + QA only)

Use the Python from the venv that scripts/setup.py created (it prints the exact command).
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(*args):
    r = subprocess.run([sys.executable, os.path.join(HERE, args[0])] + list(args[1:]))
    if r.returncode:
        sys.exit(r.returncode)


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    from common import check_deps
    check_deps()
    board, rest = sys.argv[1], sys.argv[2:]
    with open(board, encoding='utf-8') as f:
        has_voice = bool(json.load(f).get('voiceover'))
    if has_voice:
        run('voice.py', board)
    run('render.py', board, *rest)
    if '--until' not in rest:
        run('mix.py', board)
        import json
        with open(board, encoding='utf-8') as f:
            if json.load(f).get('vertical'):
                run('vertical.py', board)
    run('qa.py', board, *([] if '--until' in rest else ['--every', '1.5']))
