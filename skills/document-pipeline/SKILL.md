---
name: document-pipeline
category: document-intel
description: "Use when producing any PDF or document deliverable."
version: 1.0.0
triggers:
  - "make a pdf"
  - "build a report"
  - "generate a briefing pdf"
  - "which pdf tool"
  - "pdf pipeline"
  - "document deliverable"
---

# Document Pipeline — the router

Class-level skill. This is the **entry point** for any document deliverable. It does not replace
the cluster; it routes into it. Load this first, then load only the one or two skills it names.

**Why it exists:** the federation accumulated ~20 document skills with strong individual doctrine and
no map. Every build re-derived the same six steps by hand and forgot a different one each time. The
defects that slipped through were never content defects — they were a skipped gate. On the first run
of the engine below, the path-leak gate caught a real leak that the hand-built pipeline had missed.

## Arif's standing preference — LIGHT, never dark

**Default to a light palette.** White/near-white ground, dark text. He stated this plainly
(2026-09-18): *"I hate black dark background in pdf."* Dark decks are for screen; these artifacts
are for reading. Do not ship a dark-theme document unless he explicitly asks for one.

**This reverses the house style previously recorded in `visual-artifact-delivery` §1**, which
specified a dark base. That file has been corrected. If any older artifact of yours still cites a
dark base as the default, it is stale.

Light palette that works (validated on Edition 001, contrast checked by vision):

| Role | Hex |
|---|---|
| Ground | `#ffffff` |
| Body text | `#1c1c1c` (≈15:1) |
| Heading / table header | `#1a3a5c` navy — white text on it ≈12:1 |
| Accent rule / stamp | `#b02a1f` deep brick |
| Emphasis numbers | `#6b5210` dark bronze — **not** pale gold |
| Zebra row | `#f7f6f4` |
| Muted / footer | `#5f5f5f` |

**Pitfall:** a gold accent that looks right on a dark ground falls to ~3:1 on white — below WCAG AA.
Darken it. Vision inspection caught exactly this on the first light build.

## Layer stack — each layer has an owner

| # | Layer | Owner skill |
|---|---|---|
| 1 | **Audience** — who reads it, what they must retain | `human-facing-artifact-design` |
| 2 | **Content** — sourcing, figures, epistemic tags | `auditable-numeric-artifacts` |
| 3 | **Layout** — pagination, breaks, running furniture | `paged-media-report-layout` |
| 4 | **Render** — the engine | here + `scripts/docbuild.py` |
| 5 | **Audit** — prove content arrived and is legible | `rendered-document-audit` |
| 6 | **Seal** — content hash + artifact hash + chain | `sealed-deliverable-provenance` |
| 7 | **Deliver** | `visual-artifact-delivery` |

Never duplicate an owner's doctrine here. If this file and an owner disagree, the owner wins.

## Engine matrix — pick by shape, not habit

| Artifact | Engine | Why | Watch out |
|---|---|---|---|
| Multi-page HTML report, tables, CSS layout | **chrome** | Highest fidelity; JS runs; **emits a tagged PDF free (Chrome 85+) — the accessibility baseline** | Not built to be a backend service; `--no-pdf-header-footer` is REQUIRED or it burns `file:///` paths into every page |
| Same, no JS, tight on memory | **weasyprint** | Real CSS-paged-media: `@page` running headers/footers via `counter(page)` | No JavaScript; weaker modern-CSS than Chromium |
| Programmatic, canvas control, embedded plots | **reportlab** | Precise coordinates, matplotlib embedding | Needs a Python build script, not HTML |
| Flat poster, single chart, text over a photo | **PIL** | Fastest; no pagination needed | Measure every string — PIL neither wraps nor raises |
| Slides / deck | fixed-size HTML with a matching page box, or `open-slide-integration` | | Fixed-size divs under a non-zero `@page` margin **split each slide into two pages** |

**Do not adopt `wkhtmltopdf`.** Unmaintained; every 2026 comparison advises against new use.

**Contested — carry it honestly:** the Chromium blog states Chrome generates tagged PDFs;
independent accessibility practitioners report headless-browser pipelines produce **weak or absent**
tag trees. Both are published. Verify the tag tree on your own output rather than trusting either.

## The engine

```bash
python3 ~/AAA/skills/document-pipeline/scripts/docbuild.py \
    --src index.html --out EDITION.pdf \
    --edition 001 --ledger edition-ledger.jsonl \
    --engine chrome
```

One pass: render → page count → ink sweep → text layer → path-leak check → content hash →
artifact hash → sidecar → ledger row. **Exits non-zero on any failure.** Put it in the build
script — a gate that depends on remembering to run it is skipped on exactly the rushed edition
that needs it most.

Embed `{{CONTENT_SHA256}}` where the content hash should print. The engine hashes the template
**before** substitution, injects, renders, then hashes the render. Order is load-bearing: hash a
source that already contains its own hash and the digest describes a document that never existed.

## Reading the gate output

- **ink per page** — every page ≥3 %. A page an order of magnitude below its neighbours is a
  stranded fragment, not design. Healthy example (Edition 001):
  `[5.5, 13.7, 5.1, 12.9, 14.0, 7.1, 14.6, 9.9]`.
- **path leak == 0** — an absolute path in the text layer leaks the build machine.
- **content hash inside ≥ 1**; **artifact hash inside == 0** — a file cannot contain the hash of
  its own bytes. That zero asserts the design constraint, not just the bytes.
- **text layer** — a near-empty layer means a scan or a failed render, not a document.

## Pitfalls

- **A forced page break per section header is the top cause of near-empty pages.** Let the engine
  paginate; reserve one forced break for the cover. Documented at length in
  `paged-media-report-layout`, and it recurs because it feels tidy.
- **Patching the PDF instead of the source.** Patched PDFs are unreproducible and hide the diagnosis.
- **Leaving a superseded edition in the chain.** If an error is caught before sealing, rebuild from
  the corrected source and keep the failed build out of the ledger — do not commit it as an ancestor.
- **Adding a generated image that carries text.** Image models render lettering as garbled glyphs;
  ban text in the prompt rather than shipping a corrupted one.
- **Declaring done from a clean exit code.** A generator that writes a failure document still exits 0.
  `%PDF-` header, page count and the ink sweep are the evidence.

## Related

- Engine detail and CSS recipes: `references/engines.md`
- Long-form pagination: `paged-media-report-layout`
- Pre-delivery audit: `rendered-document-audit`
- Seal contract: `sealed-deliverable-provenance`
- Figure discipline: `auditable-numeric-artifacts`
