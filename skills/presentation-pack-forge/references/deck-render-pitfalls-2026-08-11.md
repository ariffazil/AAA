# Deck Render Pitfalls — Live Bug Catalog

**Session:** 2026-08-11 · arifOS 10-slide deck · Hermes ASI
**Path:** `forge_work/arifos-deck/`
**Renderer:** LibreOffice headless → PDF (via `soffice`)

Three artifact classes hit during render. Future decks will reproduce them unless these are encoded as runtime checks. **Read before generating any pptxgenjs deck.**

---

## Pitfall 1 — Mono font letter-spacing at narrow widths

**Symptom:**
`arif_memory` rendered as `arif_m e m ory` (or similar — extra inter-character padding breaking the word into syllable-like chunks).

**Root cause:**
`Consolas` (or any monospace) at font-size 10-11 in a `pptxgenjs` card narrower than ~1.45" rendered through `soffice --headless --convert-to pdf` triggers LibreOffice's monospace justification, which adds tracking between glyphs. Visually reads as "broken word."

**Reproduce:**
- `verbW = 1.45`, fontSize = 10-11, fontFace = "Consolas"
- Card has 11-character string like `arif_memory`

**Fix:**
- Switch short code-style labels to **Arial** (proportional) at the same size. Reserve monospace for body code blocks where card width is generous (≥3").
- If the design requires mono aesthetic, increase card width to ≥2.0".

**Verification:**
After render, `markitdown` extract and `grep -E '[a-z] [a-z] [a-z]'` for orphan single-letter clusters inside known token positions.

---

## Pitfall 2 — Italic Calibri + special characters (glyph loss)

**Symptom:**
String like `Hermes routes · OpenClaw encodes` rendered as `Hem es routes · OpenClaw encodes` — the `r` glyph is dropped, leaving visible space.

**Root cause:**
LibreOffice's italic rendering of Calibri glyphs for certain character combinations (specifically `rm`, `rn`, `re` ligatures) substitutes or drops glyphs at smaller sizes. Verified on body text at fontSize 10 italic Calibri.

**Reproduce:**
- fontFace = "Calibri", italic = true, fontSize = 10
- Text contains "Hermes", "ARIF", "arifOS", or any word with consecutive uppercase + lowercase glyphs

**Fix:**
- **Don't italicize code-style or all-caps strings.** Use bold + spacing instead.
- If italic emphasis is required, switch fontFace to `Arial` (sans-serif italic has fewer glyph-substitution issues in soffice).

**Verification:**
After render, `markitdown` extract and search for known words. If `Hermes` shows as `Hem es` or `Herm es`, the pitfall fired.

---

## Pitfall 3 — LibreOffice → PowerPoint line-break inconsistency

**Symptom:**
A card description that renders on one line through `soffice` wraps to two lines when opened in actual Microsoft PowerPoint (the user's native viewer), breaking the visual rhythm.

**Root cause:**
soffice's word-wrap algorithm differs from MS PowerPoint's, especially with hyphenated tokens (`arif_init`), parentheses, and short words.

**Reproduce:**
- Card width ~1.45-2.0"
- Description is 16-20 characters with hyphenated tokens or short words
- Card layout assumes single-line fit

**Fix:**
- Keep card descriptions to **single short phrases (≤3 words)**, not full sentences.
- If long descriptions are needed, pad card width generously (≥2.5" for 16+ character strings).
- Test with both `soffice` AND actual PowerPoint when shipping to a user who opens in PowerPoint.

**Verification:**
Cannot fully verify from `soffice` render alone. Either: (a) accept the visual QA on soffice render as best-effort, (b) ask user to confirm in their native viewer, or (c) use Chromium headless for preview as a closer approximation.

---

## Bonus — Bullet vertical alignment in panels

**Symptom:**
Bullets in a panel render with a large empty band above them (text floats in middle of panel, not top-aligned).

**Root cause:**
`pptxgenjs` text boxes default to vertical center when `valign` is not set. Multi-bullet lists with `breakLine: true` then have extra leading whitespace calculated as if panel height is content-anchored.

**Fix:**
- Always set `valign: "top"` on text boxes that contain multi-bullet lists.
- Position the text box so its top edge is just below the panel header (use 0.5-0.6" offset, not centered).

---

## Bonus — Panel border consistency

**Symptom:**
Two side-by-side panels where one has a visible border and the other does not — reads as visual imbalance.

**Root cause:**
Forgetting to set `line: { color: ..., width: ... }` on every panel shape, or setting different widths.

**Fix:**
- Define a `PANEL_BORDER` constant at the top of the build script.
- Apply uniformly to all panels of the same class.
- "Both panels have borders" or "neither has borders" — pick one and commit.

---

## Bonus — Connector arrow positioning in flow diagrams

**Symptom:**
Arrows between nodes render INSIDE the source node (visually trapped against the right border) instead of in the gap.

**Root cause:**
Wrong formula for arrow x-coordinate. Centered-on-gap = `startX + nodeW + i * (nodeW + nodeGap) + nodeGap/2`, NOT `startX + i * (nodeW + nodeGap) + nodeGap/2` (which centers on the previous node, not the gap).

**Fix:**
Use the formula above. Test with a 5-node diagram: arrows should sit cleanly in 4 gaps, not overlapping any node.

---

## QA discipline

**Stop after ONE fix-and-verify pass.** Vision models re-flag the same defects across iterations on rendered PNGs as phantom noise. If vision keeps flagging the same defect after fixes, verify against the raw chart PNG as source of truth, then ship. Over-iterating wastes cycles and reads as thrashing.

---

*Forged 2026-08-11 by Hermes ASI. Each pitfall verified live on the arifOS deck. Patch as new classes emerge.*