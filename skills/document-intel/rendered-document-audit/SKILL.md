---
name: rendered-document-audit
description: Use when auditing a rendered PDF or deck before delivery.
category: document-intel
---

# Rendered Document Audit

Class-level skill. Trigger: a rendered artefact exists or is about to be delivered and must be proven intact — "audit the visual", "check this PDF", "is this deck ok", "review this report before I send it", or any handoff of a generated document to a client, colleague, or external party.

**Core axiom:** a file that opens is not evidence it is complete. Thumbnails, file size, and a clean exit code from the render command all lie in the same direction — none of them inspect content.

## The failure this prevents

An HTML slide deck printed to PDF where every slide is clipped to a fraction of its content, with no error at any stage. Thumbnails look plausible, the file opens, and the recipient gets blank paper with headings on it. Worse than a visible failure, because nothing signals it — the author's own render is not independent evidence of its own completeness.

## Audit before you fix

1. **Reconcile page count against source count.** `pdfinfo out.pdf | grep -E '^Pages|^Page size'`. Source count = number of slide/section containers in the source. Any mismatch means content moved or vanished.
2. **Sweep the text layer per page.** `pdftotext -f N -l N -layout out.pdf -` for each page. A page carrying only a title, or no text at all, is a broken half — its body landed on the next page.
3. **Quantify the loss.** Extract text atoms from the source and check each against the PDF text layer; report a percentage. Re-run after any fix — the number must fall. Do not report "some text is missing"; report the percentage.
4. **Locate the clipping in millimetres.** `pdftoppm -r 100 -png` then measure the per-page ink bounding box against the known page box. A page reduced to a ~277 × 17mm box has lost its body.
5. **Interrogate the DOM, not only the pixels.** When the source HTML is available, compare each child's `getBoundingClientRect().bottom` against the slide's padded inner bottom, and compare `scrollHeight` vs `clientHeight`. Under `overflow:hidden` a positive difference is content being thrown away.

`scripts/pdf_content_loss_audit.py` runs steps 1–3 in one deterministic pass and exits non-zero on loss. Use it as the gate; hand-run the per-page commands only to investigate a failure it reported.

### When the source is a drawing script, not HTML

`reportlab` (or any canvas/PDF-library) output has no DOM and no text atoms to diff, so steps 2–3 and 5 do not apply. The source count is still knowable — it is the number of page-break calls in the generator — and reconciling it is still the gate:

```bash
grep -c "showPage()" build_script.py      # canvas page breaks = expected pages
pdfinfo out.pdf | grep -E '^Pages'        # must match
```

Then spot-read the rendered pages (`pdftoppm -r 100 -png`, or the vision tool on a page image) for whichever pages the last edit touched. A generator that exits 0 and writes bytes is the same false green as a file that opens — the count and the read are what make it evidence, and a dossier delivered without either is unaudited.

## Prove figures exist; never read presence from a caption

A caption is the author's claim that a figure rendered. Enumerate the embedded image objects instead:

```bash
pdfimages -list out.pdf     # per page: object id, width, height, colour, x/y-ppi, bytes
```

A page carrying a figure caption with **zero** image rows is a missing figure. A few-hundred-byte object at low pixel dimensions is an icon or a rule, not a plot. Cross-check `pdfinfo`'s page count against the document's own footer (`N / 29`) — disagreement means pages were lost, or the footer was authored separately from the render. Generated documents split figures from their discussion paragraphs across facing pages, so one present with the other absent is half a section, not a layout choice.

## Truth is a separate verdict from arrival

Proving content arrived and is legible says nothing about whether it is *correct*. When the document makes factual claims — numbers, ages, citations, "the test was run" — audit those as their own verdict, and label each finding with which of arrival / legibility / truth it belongs to. Full probe set and checklists: `references/knowledge-artifact-verification.md`.

Short form:

1. **Reconcile the artifact against the machine's own state.** Grep the repo, the resource base, and the code that implements the same subject for the artifact's load-bearing numbers and status constants. Divergence between a document and the code under it is a first-class finding — two subsystems publishing different truths under one name. Check the artifact's internal arithmetic too (durations against the age range cited, per-item counts against the stated total, chronology entries against the events named elsewhere in the same file).
2. **Verify citation metadata, not just citation existence.** A real paper with a fabricated journal or DOI is more dangerous than a fabricated paper: the title search confirms it and the metadata rides along unexamined. Compare journal, year, volume, pages, DOI character-for-character, and give the corrected form. Never summarise a partly-wrong reference list as "citations are broadly correct".
3. **Trace the artifact's own provenance.** Find the build script, the forge run directory, the claim/seal entry, the producing session. Classify full / partial / none and say which — a producing session is not chain of custody. An artifact that grades its every claim by evidence class but has no local build for the version delivered is unevidenced where it matters most.
4. **Probe the headline recommendation for its precondition, not its plausibility.** A step described as free because it reuses existing data is only free if that data exists; the organ's own status constant may read `PENDING` for exactly that reason.
5. **Re-verify any self-audit annex item by item.** A document that confesses its own inconsistencies is making a claim like any other. If it checks out, report that — it is usually the strongest part of the deliverable. If it does not, the annex is a credibility performance, which is a bigger finding than anything it confessed to.

Close with consequences, not with the inventory: numbered impacts and one concrete next action each. Name what you did **not** modify, and when a source is sealed or otherwise authority-gated, present the reconciliation as a proposal to ratify rather than as a fix.

## Three measurement traps

- **Horizontal run length cannot tell a RULE from a FILL.** A 2px navy border under a table header and a 26px navy filled block produce the *identical* longest dark run — both span the full width. An audit that measures run length alone reports a false "dark band" failure on a page of ordinary rules, and a developer who then "fixes" it damages a document that was fine. Measure **thickness** (at 110dpi, 1px = 0.231mm; a rule is 1–3px, a fill is 20px+) and measure **`dark_frac`** — the fraction of dark pixels — as the primary signal: a light page sits ~0.03–0.10, a genuinely dark page ~0.5–0.9. Prove the separation with a control image containing one of each before trusting either number.

- **Sparse sampling misreads a full-bleed page as empty.** A dark cover page sampled at intervals yields a near-zero ink average while being completely full. Measure a bounding box or a row profile before declaring any page blank.
- **SVG-only content is invisible to a text-layer check.** A slide whose content is inline `<svg><text>` renders correctly but contributes **zero** characters to the text layer. Any text-layer audit scores it as 100% lost. Strip `<svg>` blocks before the atom diff, confirm those slides visually instead, and report the retrieval limitation rather than treating it as a defect.
- **A blank-page threshold is renderer-specific and must be calibrated, not inherited.** Measured at 110dpi on A4: blank = 0.00–0.01 % ink, heading-only = 0.06 %, a real short page = 0.17 %, a dense page = 4–25 %. A floor borrowed from "reports are dense" guidance (3 %, or even 0.2 %) refuses legitimate short documents and sparse decks — the gate then reports a defect that does not exist and gets switched off. Set the floor below every measured real page, then add a relative test for the orphan case (page under ~25 % of the document's median ink, and only when the median itself is dense). State the limitation plainly: ink alone cannot separate a heading-only page from a two-line page — pair it with the text-layer check, which is a different signal, rather than tuning one number until it appears to cover both.

## Fix the source, never the artefact

Patched PDFs are unreproducible and hide the diagnosis. Patch the HTML, re-render, re-measure.

```css
@page { size: 297mm 210mm; margin: 0; }
.slide { width: 297mm !important; height: 210mm !important;
         page-break-after: always !important; overflow: hidden !important; }
* { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
```

```bash
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --no-pdf-header-footer --run-all-compositor-stages-before-draw \
  --virtual-time-budget=15000 --print-to-pdf=out.pdf "file://$PWD/fixed.html"
```

Done when page count == source count, the missing-atom count has fallen, no `file:///` path appears on any page, and no page falls below the blank floor — which you measured for this renderer, never inherited. Keep the patched HTML beside the PDF so the deliverable regenerates without repeating the diagnosis, and **leave the original untouched** — it is the only record of what was actually rendered.

## The silent-clip mechanism

Fixed-size HTML slides (`width:297mm; height:210mm`) inside a print stylesheet that sets `@page { size: A4 landscape; margin: 1cm }`. The printable area is smaller than the slide, so the renderer scales it down, it no longer fits the page box, each slide breaks across two pages — and `overflow:hidden` discards the overflow with no error.

Signature to recognise it instantly:

- Total pages ≈ **2×** the slide count
- Odd pages carry only a title; even pages carry a 15–20mm strip of body and are otherwise blank
- The renderer's timestamp and the `file:///…` source path burned into every page
- Diagrams absent entirely — an SVG-only slide reduces to a bare heading

## Legibility is a separate verdict

A render audit proves content *arrived*; it does not prove it can be *read*. Report these as their own findings, never folded into "looks fine":

- **Dark backgrounds are a defect for this principal, not a style choice.** A filled dark table header, a navy callout block or a dark code panel draws the complaint "I hate black dark background in pdf". Treat it as a delivery-blocking finding: a filled dark block also eats toner and bands on paper. The remedy is a light tint plus a structural rule (bold bottom border on a header, coloured left border on a callout, coloured top rule on a stat), never a saturated fill. Confirm with the fill-vs-rule measurement above rather than by eye.

- Body text at ~9–10pt — legible on screen, marginal when projected or printed as a handout.
- Low-contrast text — dark red on pale pink, grey italic on grey. Contrast, not point size, is what actually degrades.
- Load-bearing numbers buried in the densest slide.

## Reporting

Lead with the severity and the cause, then the fix, then what remains. Name the single root cause in one line (e.g. the page-box mismatch) rather than listing symptoms. Quantify the damage — a percentage or a page count, not "some". Deliver the fixed artefact with a real path, and say plainly that the original was left untouched so the fix can be verified.

Do not soften a broken artefact into "minor formatting issues". If it would have reached a third party empty, say so.
