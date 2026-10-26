---
name: narrative-technical-artifact
description: Use when a technical subject ships as a story PDF.
tags: [typst, pdf, narrative, artifact, colophon, geoscience, artbook]
---

# Narrative Technical Artifact

Use when the ask is a **story** about a technical subject rather than a report on it: a "hikayat" of a field or block, a portrait of an asset, a place-based historical piece, a designed booklet where the reader should feel the fact before they audit it. Deliverable: PDF in chat (`MEDIA:/abs/path.pdf`), built in Typst, in the sovereign's Malay register.

Two obligations run in parallel and neither may be dropped: the form is narrative, the evidence is still first-party.

## 1. Procedure

1. **Recover before building.** If the ask is "redo this for <other subject>", find the existing source — `.typ` file plus its ornament/figure generator — in the scratch tree (`~/.hermes/cache/scratch/`). Rebuild from source, never from the delivered PDF: a re-typed copy drifts in every margin and loses the thing the reader asked you to keep. Search session history for the artifact name too; the build path and its verified numbers are usually recorded there.
2. **Re-source the new subject from scratch.** Discovery dates, first production, ownership, capacity, schedules are re-verified per subject. A re-cut is not a licence to carry the old subject's numbers into new sentences.
3. **Fix the spine before writing.** Durable order for an asset or place: discovery → what happened after it → who named it → what changed hands → what it cost → what remains. Narrative order is not report order; the consequence lands fifth or sixth, never first, or there is no reason to read the evidence.
4. **Generate ornaments deterministically.** Matplotlib → transparent SVG (`fig.savefig(..., format="svg", transparent=True, bbox_inches="tight", pad_inches=0)`), one function per ornament (cloud curl, wave band, wayang mountain, songket meander, schematic map, seal). Re-run unchanged on a re-cut; redraw only the figures whose subject changed — map, seal, labels.
5. **Assemble in Typst**, compile, and **verify before delivery** (§4).
6. **Deliver** with one line of prose naming what changed against the previous version — no build narrative, no source path in the chat text.

## 2. Page furniture that reads as a book

- A4, cream ground, generous side margins; body DejaVu Serif, display Playfair Display (`font: "Playfair Display"` resolves from the system font set), justified, leading ~0.78em.
- **Cover**: full-bleed ground via `#page(fill: rgb("#16283d"), margin: …)[…]` with `#set text(fill: cream)` inside that page scope; ornament, small tracked kicker, two-line title (one cream, one gold), subtitle, second ornament, one factual footer line (block, location, key dates).
- **Chapters**: roman numeral + Malay noun (`I · Alkisah`, `II · Resak`), tracked kicker beneath, drop-cap opening paragraph, one chapter per page via `#pagebreak()`.
- **Fact bands**: `#block(fill: rgb("#efe6d2"), inset: …, radius: 2pt)[…]` for a pulled fact set, `#block(fill: rgb("#e8ece4"), …)` for a second and different one. Two band styles maximum.
- **Pull quotes** in display italic, centred, indigo.
- **Closing page**: the consequence in one boxed paragraph, small ornament, one line of verse, a generated seal.
- **Colophon page** (`Keterangan · Sumber dan Batas`) — mandatory, §3.

## 3. Evidence rules for a story-first document

- **The prose may carry meaning; the numbers stay exact.** No rounding for rhythm, no figure included because it sounds large. Every number is sourced on the artifact.
- **The colophon is the honesty mechanism.** One paragraph per claim group: what was used, what could not be verified, what was deliberately left unresolved. It is what stops a poetic document borrowing story authority for unverified numbers. Write the limits plainly in first person ("aku tidak menjumpai rekod awam yang menyebut…").
- **Schematics are labelled on the page and in the caption** — `Peta ini skematik · bukan untuk navigasi` — and say what the figure is for. An unlabelled schematic inside a beautiful page is the most convincing wrong thing you can ship.
- **Conflicting first-party figures are printed, not resolved.** Different discovery years in two records, or GIIP that disagrees with the recovery-factor arithmetic in the same report, are named as a disagreement in the colophon. Picking the tidier number is the defect a checking reader finds first.
- **Testimony stays testimony.** If the naming of a well, the intent behind a decision, or the human cost of a delay comes from the principal rather than a document, write it as testimony in the body and list it in the colophon.
- **Every narrative line rests on a physical fact** — a recovery factor, a count of strings still producing, the gap between discovery and first gas. Emotion without a datum reads as marketing; a datum without a consequence reads as a report.
- **No system vocabulary in rendered text** — no agent, tool, organ, pipeline or process words. The reader is a human reading about rock and time.
- **No signature attributed to the principal.** An agent-authored artifact carries no "— <name>" unless he wrote it.

## 4. Verify before shipping

```bash
typst compile doc.typ doc.pdf          # silent on success
pdfinfo doc.pdf | grep -E "Pages|Page size"
rm -f p-*.png                          # MANDATORY when the page count changed
pdftoppm -png -r 70 doc.pdf p
```

- **Cheap text probe first, per page**: `pdftotext -f N -l N doc.pdf - | head -6` and `| tail -4`. Overflow and stranded fragments show up as a heading with no body, or a body starting mid-sentence.
- **Then look at pages with `vision_analyze`** — cover, table page, map page, colophon page at minimum. Ask specifically about legibility, clipping, overlap, and whether a fact band ran past the bottom margin.
- **Stale rasters are the trap.** Inserting or removing one page renumbers every page after it, and the previous build's PNGs survive with the old numbering — a QA pass then reviews the page that *used to be there* and passes content the current build does not contain. Delete the render set before every rasterisation and confirm `pdfinfo` page count matches what you are reviewing.
- Typst silent failures: `$` opens math mode (`\$`), `@` opens a label reference (`\@`), `#` opens a function call (`\#`); image paths resolve relative to the `.typ` source, so keep assets in a sibling directory (`hikayat/peta.svg`).

## 5. Sourcing field-level facts (upstream / asset subjects)

- **The richest public source for a producing field is the Competent Person's Report (CPR) inside a listed acquirer's circular or prospectus** — GIIP, TRR low/best/high, recovery factor, project listing with dates, production history, facility design life, pipeline size and length. Download the prospectus and read it locally; a 400-page prospectus is one ~12 MB fetch.
- **Discovery years and play context** come from Geological Society of Malaysia bulletins (`gsm.org.my` PDFs). They disagree with CPRs — that is the disagreement you print, not resolve.
- **Operator narrative and framing** (what a find "means") from the operator's activity outlook and media releases; **facility detail** (platform count, water depth, bridge-link configuration) from industry award or inspection profiles.
- Work the PDF with `pdftotext -layout file.pdf out.txt`, then `grep -n` the field name for line offsets and `sed -n 'A,Bp'` to read just that section. Never paste a whole prospectus into context.

## Pitfalls

- Rebuilding from the delivered PDF instead of the source produces invisible drift in margins, ornaments and furniture.
- Regenerating the whole design on a re-cut wastes the recognisability the reader asked for; regenerate only subject-specific figures.
- Reviewing stale page PNGs after a page-count change — §4.
- Resolving a two-record discrepancy "for tidiness". The unresolved discrepancy is content.
- Writing the consequence in section one; the reader then skips the evidence and the artifact becomes an opinion with decoration.
- Padding a chapter that no longer has a subject. Replace it; do not fill it with the nearest available fact.
