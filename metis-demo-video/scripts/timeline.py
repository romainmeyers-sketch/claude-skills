"""Alignment report: every spoken phrase next to the clicks, camera moves and scene changes around it.

  python timeline.py storyboard.json [from_seconds]

Read it after a render with voiceover. A CLICK that happens before the SAY that describes it, or a long run
of lines with no SAY, is what to fix in the storyboard (see references/voiceover.md, "Sync").
"""
import sys
from common import Board

board = Board(sys.argv[1])
c, m = board.json_in('cues.json'), board.json_in('voice_manifest.json') or {}
lo = float(sys.argv[2]) if len(sys.argv) > 2 else 0
ev = []
for t, k in c['cues']:
    if k.startswith('click:'): ev.append((t, '   CLICK ' + k[6:]))
    elif k == 'zoom': ev.append((t, '   zoom'))
    elif k == 'notify': ev.append((t, '   TOAST'))
    elif k == 'app_in': ev.append((t, '   APP IN'))
for t, lid in c.get('vos', []):
    for sg in m.get(lid, {}).get('segs', []):
        ev.append((round(t + sg['start'], 2), 'SAY  ' + sg['text']))
for n, t in c['marks']:
    ev.append((t, '--- scene ' + n))
for t, l in sorted(ev, key=lambda x: x[0]):
    if t >= lo:
        print('%6.1f %s' % (t, l))
