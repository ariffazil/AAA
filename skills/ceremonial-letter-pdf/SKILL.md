---
name: ceremonial-letter-pdf
description: "Use when a letter for a person ships as a designed PDF."
tags: [pdf, letter, keepsake, typst, svg, design, artifact]
metadata:
  hermes:
    tags: [pdf, letter, keepsake, typst, svg, artifact-delivery]
    related_skills: [typst-pdf-report, third-party-advisory-doc, human-facing-artifact-design]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Ceremonial Letter PDF (warkah)

Trigger: 'buat warkah', 'surat untuk <person> as PDF', 'letter from the future', a keepsake page with colours/motif for a named family member or friend.

A **report** argues; a **letter** lands. When the artifact is one page written to a person — a warkah from a future self, a note to a sibling, a keepsake — the deliverable is a designed page with a frame, a motif, one pull-quote, and a signature. Plain prose in chat is the draft; the PDF is the artifact.

For general reports, dossiers and evidence packs use `typst-pdf-report`. Use this skill when the page itself has to feel like an object.

## Procedure

1. **Draft the body as short lines first**, in the person's own register (for Arif's family: BM dapur, `hang`/`aku`, no psychology vocabulary, no system jargon). Assert a word budget — a letter is 250-400 words. One idea per line; the pull-quote is chosen from the body, not written beside it.
2. **Draw the frame as SVG** at A4 @ 72 dpi: `width="595" height="842"` + `viewBox="0 0 595 842"`. Layer order: opaque page tint, outer stroke, inner hairline, `<pattern>` motif tiles, corner roundels. Start from `templates/nusantara-border.svg` (pink + gold songket lattice) and recolour the four hex values in its header comment.
3. **Draw the floral flourish separately** (`templates/floral-ornament.svg`) and place it inline above the title. Bake it into the border and it can no longer centre against a variable-length title.
4. Write the `.typ`:
   ```
   #set page(paper: "a4", margin: (x: 66pt, top: 64pt, bottom: 60pt),
     background: image("border.svg", width: 100%, height: 100%))
   #set text(font: "DejaVu Serif", size: 10.8pt, fill: rgb("#402A31"))
   #set par(leading: 0.78em)
   ```
   Serif + loose leading reads as a letter; sans reads as a report. The page background is **not** clipped to the margin box — a full-bleed frame works, and the margin alone keeps the body off the border.
5. Title block: `#align(center)[#image("ornament.svg", width: 44%) #v(4pt) #text(size: 19pt, weight: "bold", fill: rgb("#C2185B"))[...] #v(3pt) #text(size: 9.5pt, style: "italic", ...)[subtitle]]`.
6. The line that must land, boxed: `#block(fill: rgb("#FDE7EF"), inset: 12pt, radius: 6pt, width: 100%)[#align(center)[#text(size: 12.5pt, weight: "bold")[one sentence] #v(2pt) #text(size: 10pt)[its echo]]]`.
7. Close right-aligned: `#align(right)[#text(style: "italic", fill: rgb("#C2185B"))[— Name, masa hadapan]]`.
8. Compile, then **verify both layers** — `pdftotext warkah.pdf -` for wording/names (this is the only text truth; a vision pass paraphrases and will rename people while calling the page clean), and `pdftoppm -png -r 60` + `vision_analyze` for layout only (overlap, clipping, stranded second page). A letter must be exactly one page.
9. Deliver with `MEDIA:/abs/path/warkah.pdf`. Never cite the scratch path in prose.

## Person visual identities (standing)

When the user names a person and a colour, that pairing is durable — reuse it next time instead of re-asking:

- **Azwa** — pink, nusantara/songket: `#C2185B` outer, `#E91E63` accent, `#C9A227` gold motif, `#FDE7EF` pull-quote fill, `#FFF6F9` page tint. Gentle sister register.

Add a row when a new person/colour pair is set by the user; never invent one.

## Voice-note companion

A letter to a family member is often followed by "and now in <persona> voice". Render the spoken version as a **shorter** script (60-75 s) that carries the same three beats — never read the letter verbatim; the ear rejects written syntax. Use that persona's registry voice and its canonical render recipe, then send as a voice bubble.

## Pitfalls

- **`_` starts emphasis — one stray underscore fails the whole document.** `*Azwa,_` raises "unclosed delimiter" and the caret blames the `*`. For an opening or signature line use `#text(weight: "bold")[Azwa,]`; sweep the source for bare `_` before compiling.
- **`$`, `@`, `#` are markup too.** Escape as `\$`, `\@`, `\#` in one pass before the first compile.
- **A filled `#block(...)` needs `width: 100%`** or it shrinks to its contents and the pull-quote stops reading as a banner.
- **Image paths are relative to the `.typ` file**, so keep border, ornament and source in one directory.
- **A second, near-empty page is the classic failure.** Trim the body rather than shrinking the font — a letter that spills has one paragraph too many.
- **Never sign a letter the principal did not write, and never attribute the words to the subject.** Leave it unsigned unless the user asked for a signature line.
