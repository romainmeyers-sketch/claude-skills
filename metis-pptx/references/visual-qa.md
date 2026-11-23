# Visual QA (Both Modes)

**Assume there are problems. Your job is to find them.**

## Export Slides as Images

```bash
"$PYTHON" "$SKILL_DIR/scripts/visual_qa.py" output.pptx qa_images/
```

This uses PowerPoint COM automation to render each slide as a high-fidelity PNG.

## Thumbnail Grid

```bash
"$PYTHON" "$SKILL_DIR/scripts/thumbnail.py" output.pptx
```

Creates a grid overview of all slides for quick visual inspection.

## Content QA

```bash
"$PYTHON" -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**Check for leftover placeholder text:**
```bash
"$PYTHON" -m markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert"
```

## Visual QA Checklist

When inspecting slide images, look for:
- Overlapping elements (text through shapes, lines through words)
- Text overflow or cut off at edges/box boundaries
- Elements too close (< 0.3" gaps) or sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (light gray on cream, dark on dark)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content
- **Leftover source content:** Any text, labels, metrics, or brand names from the original deck that weren't updated
- **Hybrid metrics:** Numbers or KPIs that mix source and target data (e.g., a new revenue figure next to a growth multiplier from the original deck)
- **Empty containers:** Shapes, boxes, or pill elements that had content in the source but are now empty or contain generic labels
- **Mismatched structure:** Visual elements (timelines, arrows, connectors) whose spatial arrangement implies a relationship that doesn't exist in the new content
- **Formatting inconsistency:** Slides where bullet style, text color, or font size varies from the rest of the deck (common when some slides are edited and others rebuilt)

## Verification Loop

1. Generate/edit the deck
2. Export slides as images
3. **Inspect every slide** - list issues found
4. Fix issues
5. **Re-export affected slides** - re-inspect
6. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**
