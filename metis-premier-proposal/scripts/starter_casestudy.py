"""
starter_casestudy.py — Starter build script for a single-engagement case study.

Case-study mode: 10–14 pages. One engagement, proof-forward. Prominent
signature visual, outcome metrics, and a closing statement about what good
looks like. No modules overview, no next-steps. The reader is interested
in the engagement, not in buying an engagement.

Expected section shape:
  cover (tagline, no prepared_for)
  → setup / situation (problem_framing with the client's starting context)
  → approach (typically: signature_image or timeline)
  → results (proof_overview with headline dollar figure)
  → supporting evidence (minicase_pair or metric_dense)
  → what good looks like (quote or pillars)
  → closing (contact)

Authoring flow:
  1. Fill in scripts/_brief_template.md first. Case-study mode: thesis is
     "here's what happened; here's why it worked." Credit the team in the
     closing, anonymized per references/content-rules.md.
  2. Copy `starter_casestudy_copy.yaml` to your project folder and rename.
  3. Edit sections. Content pages must declare `intent:`.
  4. Run this script. Verify with `scripts/verify.py --mode all`.
  5. Run the polish pass (see references/polish-pass.md) before shipping.

Run:
  PYTHON="C:/Users/Andrew Krusell/AppData/Local/Programs/Python/Python312/python.exe"
  "$PYTHON" starter_casestudy.py [path/to/copy.yaml]
"""
import os
import sys
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import starter_capabilities as SC


def _validate_casestudy_shape(copy_file):
    with open(copy_file, 'r', encoding='utf-8') as f:
        copy = yaml.safe_load(f)
    sections = copy['sections']
    types = [s.get('type') for s in sections]
    if len(sections) > 16:
        print(f'  WARNING: case study has {len(sections)} sections. '
              f'Target is 10-14. Consider cutting (see references/narrative-planning.md).')
    if 'proof_overview' not in types:
        print('  WARNING: case study should include a proof_overview section '
              'with a headline dollar figure. Consider adding one.')
    if 'next_steps' in types:
        print('  WARNING: case study should not include next_steps. '
              'Use a closing with credit/contact info instead.')
    if 'modules_overview' in types:
        print('  WARNING: case study usually does not need a modules_overview. '
              'The engagement itself is the content, not a sales menu.')


if __name__ == '__main__':
    copy_file = sys.argv[1] if len(sys.argv) > 1 else 'starter_casestudy_copy.yaml'
    _validate_casestudy_shape(copy_file)
    SC.build(copy_file)
