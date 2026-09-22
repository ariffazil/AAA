---
name: rendered-artifact-verification
description: "Use when verifying a rendered image, PDF or logo artifact."
version: 1.0.0
owner: Hermes
risk_tier: low
tags: [verification, rendering, pdf, image, vision, measurement, qa]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Rendered Artifact Verification

Load this whenever an artifact is produced as **pixels** — a logo or mark, a chart, a figure, an
HTML→PDF report, a contact sheet, a screenshot — and you are about to tell the user it is correct.

A render succeeds silently while being wrong. Nothing raises; the file is produced; the code review
passes. The defect is only visible in the output, and the output is the one thing you cannot read
reliably by asking a model.

## The one rule

Split every claim you are about to make into three classes, and verify each by its own method:

| Claim class | Examples | Verify by |
|---|---|---|
| **Structural** | element present, nothing clipped, nothing blank, page count, aspect | **Pixel measurement** on the render |
| **Content** | what a label says, a number, a unit, a glyph identity, a name | **Source of truth** — the DOM string, the PDF text layer, the input file |
| **Compositional** | looks cluttered, feels off-balance, reads as the right genre | **Vision model**, as a lead only |

Never let a model's reading of *content* stand as evidence, and never let a measurement stand in for a
judgement. The two failure modes are symmetric.

## Procedure

1. **Render at 2x, then downscale.** Screenshot or rasterise at `deviceScaleFactor=2`, then LANCZOS
   down to delivery size. Downscaling from a higher-resolution render is what makes edges and small
   glyphs crisp; rendering at target size directly does not.
2. **Check element presence by pixel count, not by reading the markup.** For each element you believe
   you drew, count pixels matching its colour in the region where it should be. Zero means it is not
   there. Do this before any other check — a missing frame or ring changes the whole composition.
3. **Check placement by centre of mass, not bounding box.** Take the ink colour's centre of mass. An
   asymmetric glyph, a descender or a floating dot pulls the bounding box off-centre while the mass
   sits correctly, and vice versa.
4. **Check content against the source.** Assert the source string; extract the PDF text layer; diff two
   conditional renders. See `references/measurement-recipes.md`.
5. **Check ink coverage per page** on any multi-page PDF. A page an order of magnitude below its
   neighbours is a stranded fragment or a failed render, not a design choice.
6. **Run the small-size gate** on anything destined for a thumbnail or avatar. Render every variant at
   the real consumption sizes (200 / 112 / 64 / 40 / 28 px), circle-crop if the platform will, and
   choose on that sheet — never on the pleasing large render.
7. **Ask vision about composition only**, and treat its answer as a lead to check numerically.
8. **Re-measure after every fix** and quote the numbers. A fix that is not re-measured is a guess.

## What a vision model is and is not good for

**Good:** is anything colliding, clipped, off-frame, blank; is the mark off-centre; is the composition
lopsided; does the colour read at small size; is a requested element absent; how many distinct text
blocks there are; which type sizes compete; what is redundant.

**Diagnosing "this looks chaotic".** When the feedback is a vague complaint about crowding, do not
guess and do not restyle blind — ask the vision model for a census, then verify it numerically: count
the distinct text blocks and the size/style tiers, name which elements repeat (a column header stamped
on every section is pure redundancy), and count how many small metadata lines sit inside the reading
path. Then do the arithmetic on the real markup — `grep -c 'class="<x>"'` per class — and report the
reduction as numbers (block count before/after, rendered height before/after) rather than as an
opinion about tidiness. Prefer **moving** provenance out of the reading path over deleting it:
collected source lines at the foot keep the artifact re-checkable, whereas removing them trades
legibility for unverifiability.

**Not good:** reading text. Given the same image three times, one model returned three different
readings of a single word — one correct, one an entirely different word, one the correct word plus a
fabricated spelling error — and gave no signal marking which to trust. It will also assert the absence
of an element that is present, or the presence of one that is missing, with equal confidence. A model's
report about *what a label says* is noise. A model's report about *where things are* is a useful lead.

Take the geometric observations and check them numerically. Discard the textual ones and check those
against source.

## Silent-failure classes worth knowing

- **Invalid-in-context markup is dropped without error.** A `<circle>`, `<rect>` or `<line>` written
  directly into an HTML document — with no `<svg>` wrapper — is an unknown element. The browser discards
  it silently: no console warning, no error, and the page still looks plausible because the background
  and text rendered fine. The frame simply is not there. Sample pixels to find it.
- **A near-empty trailing page.** A closing block with a generous top margin gets pushed onto its own
  page. On a light document, measure ink as deviation from the **modal** pixel value, not as non-white —
  on a dark-background document a white-page threshold reports every page as full and hides exactly the
  defect you are hunting.
- **A page count near double the designed block count** means every block is spanning two pages; the
  cause is geometry (container taller than the printable box), not content length.
- **A container that scrolls** silently crops. Measure the rendered height against the intended height
  before screenshotting; a capture that used the viewport will cut the tail.

## Reporting

State the measurement, not the verdict. "The hamza measures present at 63% along the word, 35 px from
the top of the ink box" is evidence. "The model says it looks right" is not, and "it should be fine" is
not. Where you could not verify something — no reference data, no way to measure — say that explicitly
and name it as a gap. A number you could not have measured must never appear; if a correlation or score
has no counterpart in the data loaded, it is not a finding, it is an invention.

## Deliverable shape

Send **one contact sheet or one assembled artifact** plus a named recommendation and the measurements
behind it. Do not send several near-identical full-size files and ask the user which they prefer — the
judgement they need to make is at consumption size, and the sheet is what gives it to them.

## Pitfalls

- Reading the markup to confirm an element rendered. Markup validity is not render presence; count pixels.
- Centring on the bounding box instead of the ink centre of mass — asymmetric glyphs sit wrong and it looks intentional.
- Ranking variants by eye at full size when the artifact is consumed as a 40 px thumbnail.
- Measuring contrast or coverage over the whole canvas. Chrome, borders and neighbours inflate the score; restrict the measurement to the region of interest.
- Trusting a model's transcription of text, numbers or glyphs. Verify against the source string, the PDF text layer, or a conditional-render diff.
- Adding a label or subtitle to a mark without re-running the small-size gate; the label takes vertical space from the primary element and both become unreadable.
- **Diagnosing a layout defect from extracted text.** Text-layer extraction does not preserve reading
  order on a table-heavy or multi-column PDF — it interleaves the columns and splits table cells into
  fragments, so a cleanly typeset document reads as scrambled nonsense. Render the page to PNG and look
  at it before reporting any layout defect. Use extraction for *content presence* only; the text layer
  is not evidence about composition, and a document can be immaculate while its extraction is garbage.
- **A structural/geometric vision finding is still a CLAIM — confirm it against the SOURCE before
  fixing anything.** Measured: a vision audit of an HTML→PNG card reported two columns overlapping in
  one row and a truncated footer seal. Reading the source disproved both — the columns were separate
  `<div>`s inside a `border-right` rule with 18 px padding either side, and the footer string was
  complete. "Geometric observations are a useful lead" is true about *where things are*; it is not a
  licence to edit. For any reported collision, clip or cut-off, grep the CSS/markup for the property
  that would have to be ABSENT for the defect to exist. A fix applied to a defect that does not exist
  is strictly worse than the reported bug: it changes a working artifact and adds a change to review.
- Declaring completion without re-measuring after the fix.
- **A vision QA verdict contradicts itself across passes.** The same model, asked the same way,
  returned `intentional and structural` for one variant and `the biggest issue` for the same tracking
  three passes later. Its **geometric observations** are useful leads (off-centre, clipped, missing),
  its **type verdicts** (this looks elegant, that's typographically forced) are opinion. Verify geometric
  calls with pixel sampling; defer aesthetic calls to the user. Measure the work, do not vote on it.
- **Shipping an oversize page-break-driven PDF.** A `<div class="page-break"></div>` after every section
  looks clean in authoring but creates stragglers — sections that fall mid-page, leaving 1–2 orphan
  lines on otherwise blank pages. Detect by rasterising at 50 dpi and flagging pages under ~3 % ink
  coverage. Strip the page-break markers and let weasyprint flow; insert a break **only** where the page
  must turn (cover, intro, back matter), not on every section.

## Support files

- `references/measurement-recipes.md` — runnable snippets: element presence, ink centre of mass,
  small-size contrast, per-page ink coverage, PDF text-layer assertions, conditional-render diffing.
