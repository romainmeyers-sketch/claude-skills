#!/usr/bin/env python
"""
append_previous.py — Carry last week's SteerCo slides into the appendix of the
new deck, preserving their original Metis branding.

Uses PowerPoint COM (Slides.InsertFromFile), which keeps the source master on
the inserted slides, so branding, layouts, and images come across cleanly with
no XML rewriting.

Usage:
    PYTHON="C:/Users/<you>/AppData/Local/Programs/Python/Python312/python.exe"
    "$PYTHON" append_previous.py NEW.pptx PREVIOUS.pptx [start] [end]

    start / end : 1-based inclusive slide range from PREVIOUS to bring over.
                  Defaults skip the previous cover (slide 1) and previous
                  closing (last slide): start=2, end=(count-1).

The previous slides are inserted AFTER the new deck's Appendix divider and
BEFORE its closing slide. The new deck is modified in place (a .bak is made).
"""

import sys
import os
import shutil
import subprocess

import win32com.client
from pptx import Presentation


def _slide_titles(path):
    prs = Presentation(path)
    titles = []
    for s in prs.slides:
        t = ""
        for ph in s.placeholders:
            if ph.placeholder_format.idx == 0 and ph.has_text_frame:
                t = ph.text_frame.text
                break
        titles.append(t)
    return titles


def _find_appendix_divider(path):
    """Return 1-based index of the 'Appendix' section divider in the new deck,
    or None if absent."""
    prs = Presentation(path)
    for i, s in enumerate(prs.slides, start=1):
        if s.slide_layout.name == "Section Divider":
            for ph in s.placeholders:
                if (ph.placeholder_format.idx == 0 and ph.has_text_frame
                        and ph.text_frame.text.strip().lower() == "appendix"):
                    return i
    return None


def main():
    if len(sys.argv) < 3:
        print("Usage: append_previous.py NEW.pptx PREVIOUS.pptx [start] [end]")
        sys.exit(1)

    new_path = os.path.abspath(sys.argv[1])
    prev_path = os.path.abspath(sys.argv[2])
    for p in (new_path, prev_path):
        if not os.path.isfile(p):
            raise FileNotFoundError(p)

    prev_count = len(Presentation(prev_path).slides._sldIdLst)
    start = int(sys.argv[3]) if len(sys.argv) > 3 else min(2, prev_count)
    end = int(sys.argv[4]) if len(sys.argv) > 4 else max(1, prev_count - 1)

    new_count = len(Presentation(new_path).slides._sldIdLst)
    # Insert before the closing slide (assumed last), after everything else.
    after_index = new_count - 1
    divider = _find_appendix_divider(new_path)
    if divider is None:
        print("WARNING: no 'Appendix' divider found in the new deck. "
              "Previous slides will still be inserted before the closing slide, "
              "but consider adding an appendix section in the content JSON.")

    shutil.copyfile(new_path, new_path + ".bak")

    was_running = "POWERPNT.EXE" in subprocess.check_output(
        ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/NH"],
        stderr=subprocess.DEVNULL, text=True)

    ppt = win32com.client.DispatchEx("PowerPoint.Application")
    try:
        pres = ppt.Presentations.Open(new_path, WithWindow=False)
        # InsertFromFile(FileName, Index, SlideStart, SlideEnd)
        #   Index = position AFTER which the slides are inserted.
        pres.Slides.InsertFromFile(prev_path, after_index, start, end)
        pres.Save()
        final = pres.Slides.Count
        pres.Close()
    finally:
        if not was_running:
            ppt.Quit()

    print(f"Inserted previous slides {start}-{end} into '{os.path.basename(new_path)}' "
          f"after slide {after_index}. New total: {final} slides.")
    print(f"Backup: {new_path}.bak")


if __name__ == "__main__":
    main()
