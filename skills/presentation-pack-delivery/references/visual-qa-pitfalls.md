# Visual QA Pitfalls — Session Reference

> **Session reference, distilled from 2026-08-11 arifOS Constitutional Kernel deck (11 slides, 3 QA rounds, vision-loop trap closed).**
> Read alongside `presentation-pack-delivery` SKILL.md.

## The 5 visual defects that always bite first render

After 1+ rounds of vision_analyze on rendered slide PNGs, these are the consistent defects:

### 1. **Vertical imbalance — top-heavy with empty bottom half**

Cover/closing slides tend to have a huge title block at top + dead cream/space at bottom. Standard fix:

```javascript
// Cover slide — pull title down to y=2.0 (not 1.5)
// Add ornament in lower third to absorb dead space:
s.addShape(pres.shapes.RECTANGLE, {
  x: W / 2 - 2.5, y: 5.85, w: 5.0, h: 0.03,  // longer hairline
  fill: { color: amber }, line: { color: amber, width: 0 }
});
s.addText("DITEMPA BUKAN DIBERI", {
  x: 0.6, y: 5.95, w: W - 1.2, h: 0.45,
  fontSize: 14, color: amber, bold: true,
  charSpacing: 8, align: "center"
});
```

The ornament (longer hairline + centered motto caption) gives the lower half visual weight without crowding the title.

### 2. **Subtitle overlap with title period (anchor collision)**

A subtitle placed at y=2.95 with motto at y=1.5+1.3=2.8 ends up overlapping the period. Fix:

```javascript
// Subtitle must clear title baseline by at least 0.35 inches
// Title at y=1.4, h=1.4 → bottom at 2.8
// Subtitle at y=3.25 (gap=0.45) — clear separation
s.addText("Forged, not given.", {
  x: 0.6, y: 3.25, w: W - 1.2, h: 0.5,
  fontSize: 24, color: amber, italic: true, align: "center"
});
```

### 3. **Bottom hairline + footer cramping**

Hairline at y=6.85 with footer text immediately below = no breathing room. Move the rule UP, push the footer DOWN:

```javascript
// Bottom rule at y=6.55 (not 6.85)
// Footer at y=6.85 (0.30 gap from rule)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.55, w: W, h: 0.04, fill: { color: amber }
});
s.addText("footer text here", {
  x: 0.6, y: 6.85, w: W - 1.2, h: 0.4, fontSize: 13
});
```

### 4. **Inconsistent card title baselines (wrapped vs single-line)**

When some pillar/card titles wrap to 2 lines and others don't, the body text starts at different y across the row. Fix: pin the title block to a fixed height that accommodates the longest possible wrap:

```javascript
// All titles share same h=0.7 block (room for 2 lines)
s.addText(card.title, {
  x: cx + 0.2, y: cy + 0.2, w: cellW - 0.4, h: 0.7,  // pinned height
  valign: "top"
});
```

Or shorten titles to single-line consistently: "PROBE BEFORE ACT" (wraps) → "PROBE FIRST" (one line).

### 5. **Stranded last-row element in a 5-col grid (13 floors in 5x3 = 5+5+3)**

13 items in a 5-column grid leaves last row with 3 items, with the most-important item (e.g. F13 SOVEREIGN) stranded at column 3, with empty cells 4 and 5 to its right. Fix: center the last 3 by starting at column 1 (or 2) instead of column 0:

```javascript
// Positions array — last row centered
const positions = [];
for (let c = 0; c < 5; c++) positions.push({ row: 0, col: c });
for (let c = 0; c < 5; c++) positions.push({ row: 1, col: c });
positions.push({ row: 2, col: 1 });  // centered, not stranded at col 3
positions.push({ row: 2, col: 2 });
positions.push({ row: 2, col: 3 });
```

## The vision-loop trap (full reproduction recipe)

```python
# Round 1: vision_analyze on rendered PNGs
# Result: "X overlaps" on slide 1, "title too big" on slide 5, etc.

# Round 2: fix issues, re-render, vision_analyze again
# Result: "X is fine but now Y has an issue" — different complaint, same vicinity

# Round 3: fix Y, re-render, vision_analyze
# Result: "Y is fine but I notice Z has..."  ← THIS IS THE TRAP

# Rule: STOP at round 3. Vision is hallucinating new complaints on edge zones.
# Use raw PNG inspection (PIL, coordinate math) for any further verification.
```

## F2 epistemic labels in slide notes (proposed — not yet implemented)

Slide notes (`<p:sp>` with `<p:nvSp>` containing `<p:nvPr>`) can carry per-slide epistemic tags. Pattern for future implementation:

```javascript
slide.addNotes(
  "OBS: data verified live at <url>\n" +
  "DER: derived from OBS items\n" +
  "INT: interpretive claim — needs sovereign review"
);
```

Notes are exported by markitdown but not shown to the audience. This gives an audit trail for slide claims without polluting visual design.

## Federation design system — interim palette mapping

Until `FORGE-visual-design-system` exists as a separate umbrella, fork the Trinity palette and apply per-organ:

| Organ | Primary | Accent | Use case |
|---|---|---|---|
| arifOS | midnight `1A1F36` | amber `D4A574` | Constitutional decks, governance briefings |
| A-FORGE | red `B85042` | midnight | Execution briefings, engineering decks |
| GEOX | midnight | teal `2C7B7B` | Earth intelligence reports |
| WEALTH | navy `0E1A2B` | gold `C9A227` | Capital reports, financial briefings |
| WELL | midnight | violet `8B5CF6` | Human readiness briefings |
| AAA | midnightLift `2D3454` | gold `C9A227` | Control plane documentation |

Generic default (when organ is unclear): midnight + amber + cream (`1A1F36` / `D4A574` / `F5F1E8`) — same as arifOS but works cross-organ.

## What I tried that didn't work

- **Reduced title fontSize 140 → 130, moved title down 0.3, added 5" ornament in lower half** — only the ornament move helped. Title size change was cosmetic.
- **Tightening eyebrow-to-title gap from 1.05" → 0.27"** — still read loose. The fundamental issue was title positioning, not gap.
- **Adding bottom hairline below motto** — created visual weight but didn't fix vertical balance.

## What worked

- **Pull title down to y=2.0+** (the biggest single fix for vertical balance)
- **Ornament in lower-third** (hairline + 14pt motto caption in mid-deck color)
- **Move bottom rule up to y=6.55, push footer to y=6.85** (consistent clearance)
- **Shorten title strings** to keep single-line ("PROBE BEFORE ACT" → "PROBE FIRST")
- **Use consistent emoji glyphs** across all 8 organ cards (consistency matters more than typography)

---

*DITEMPA BUKAN DIBERI — patterns forged 2026-08-11 by Hermes-Prime on arifOS Constitutional Kernel deck.*