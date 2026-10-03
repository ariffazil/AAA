---
name: hermes-pdf-intelligence
description: Probe-first, cognition-aligned, verified, trust-anchored PDF doctrine for HERMES agents. Covers probe-first PDF capability mapping (presence is a fact, fitness is a verdict), cognition-aligned PDF design (attention budget, 4±1 working-memory chunks, visual doctrine), PDF generation routing across pandoc/xelatex, typst, reportlab+matplotlib, weasyprint, chromium headless, and libreoffice, Render-Rasterize-Read verification gates (qpdf, pdftoppm, pdftotext sentinels), and trust-anchoring outside the file (SHA-256, Merkle DAG in VAULT999, RFC 3161 timestamp). Use when creating a PDF, auditing PDF capability on a node, extracting text or tables from a PDF, verifying a generated PDF before delivery, redacting sensitive PDF content, or designing a document for a time-poor expert reader.
---

# HERMES PDF Intelligence

PDF work is governed by four standing orders: probe the environment, route the task, design for the
reader's cognition, verify and anchor the artifact. Capability claims without probe output are VOID.
DITEMPA BUKAN DIBERI — forged, not given: the forge is the probe, the proof is the gate.

## Step 0 — ALWAYS probe first

Run the probe at the start of every PDF session, on every node. The capability map is probe OUTPUT,
never assumption or inherited audit.

```bash
bash scripts/probe_manifest.sh | tee probe_manifest.txt   # saved next to the deliverable
```

- Save the RAW probe output to `probe_manifest.txt` next to the deliverable — probe output is
  evidence; a prose claim of probing is fabricable.
- Treat every `MISSING` as VOID: route to a probed fallback, never to hope.
- Treat `wkhtmltopdf` as FORBIDDEN even when PRESENT: archived upstream Jan 2023, Qt WebKit engine
  frozen circa 2012–2015, unpatched CVE-2022-35583 (CVSS 9.8 SSRF). Presence is a fact; fitness is
  a verdict. A capability map without a fitness column is an attack-surface inventory.
- Record versions. The same federation node differs per machine; yesterday's probe is a claim.

## Step 1 — Route with the decision matrix

X → Y → Z → W reads: if you want X, use Y, because Z, and prove it with W. Condensed from report
Table 6.5; full pipeline and reading-stack matrices live in `references/toolchain-matrix.md`.

| Task | Pipeline | Why | Verify with |
|---|---|---|---|
| Fast text dossier (≤2 pp. glanceable) | `pandoc --pdf-engine=xelatex` (typst where probed) | ~5 s/24 pp., TOC + refs; typst ≈27× faster, tags by default | G1 + G3; dark theme legal at ≤2 pp. |
| Long report (>2 pp.) or print | pandoc/typst, LIGHT theme | Polarity rule: dark-on-light reads better; print beats screen | G1 + G2 + G3; contrast ≥7:1 |
| Full-control/chart dossier, live data | reportlab + matplotlib (PNG ≥150 dpi if not vector) | Single script, coordinate-exact layout | G1 + G2 (chart vs source data) + G3 |
| HTML/CSS you tweak in a browser | weasyprint (only if probe shows it) | CSS variables, paged media; MISSING → chromium fallback | G1 + G2; backgrounds need print CSS |
| JS-heavy / modern Grid HTML | chromium `--headless --print-to-pdf` | Only real-browser engine; weasyprint Grid is partial | G2 mandatory (blank/tofu/clipping are silent) |
| Existing DOCX/PPTX → PDF | `soffice --headless --convert-to pdf` | Installed, reliable; one document per instance | G1 + G2 (fonts substitute silently) |
| Read back / extract text | PyMuPDF (pdftotext as backup) | Instant, no models; sentinel assertion | G3; empty output → OCR ladder, never ship |
| Scanned PDF / evidentiary seal | tesseract → VLM / SHA-256 → Merkle → RFC 3161 | 98–99% clean print @300 dpi; in-file signatures broke 16/29 viewers | G3 + sampled human check / G4 + veraPDF |

FORBIDDEN: wkhtmltopdf on every row, no matter what the probe finds. For Markdown input, use
`scripts/md_to_pdf.sh` — it routes by probe in the order xelatex → weasyprint → chromium → soffice.

## Step 2 — Design per cognition doctrine

Five binding rules (evidence and effect sizes in `references/cognition-doctrine.md`):

1. **First-Screen Contract**: page 1 carries a BLUF block + ≤4 chunks (79% of readers scan; the value
   verdict lands in ~10 s). Restate the BLUF at section boundaries.
2. **Headings as standalone claims** (layer-cake): a reader scanning only headings must still receive
   the argument. Inverted pyramid per paragraph.
3. **Every visual answers a named question or is deleted**: functional visuals gain d=0.86–1.22;
   decorative imagery costs g=−0.95 and the harm is larger on paper. Exact values → tables; trends →
   position-encoded charts; no 3D, no dual axes, zero-baseline bars, direct labels over legends.
4. **Polarity rule**: light theme for anything >2 pages or destined for print; dark ONLY for ≤2-page
   on-screen glanceables; contrast ≥7:1 either way; print body 10.5–11.5 pt, 25 mm margins,
   60–75 CPL, bold not italics.
5. **4±1 chunk budget**: a chunk = one visual or verbal unit the reader must hold in working memory
   (a panel, table, chart, or callout); budget ≤4±1 chunks per first screen, ≤4 bullets or
   comparison columns; a stat-strip of N tiles counts as N chunks unless grouped under one header;
   progressive disclosure ≤2 levels.
6. **Caveats in the artifact**: every analytical PDF carries an explicit "Caveats" line IN the PDF
   itself — sidecar notes are not enough.

Never cite the debunked myths (goldfish attention span, "60,000× faster", serif superiority, dyslexia
fonts) — the full bust list is in `references/cognition-doctrine.md` §4.

## Step 3 — Verify before shipping

No PDF ships without G1–G3. Tool-OK ≠ page-correct: blank pages, tofu, and clipping all return
exit 0 from the generator.

```bash
bash scripts/pdf_verify.sh out.pdf "headline claim" "key sentinel"
```

- **G1 structural**: `pdfinfo` exit 0 + page count; `qpdf --check` exit 0 when present (qpdf
  certifies syntax only — PDF/A or PDF/UA claims require veraPDF).
- **G2 rasterize**: first and last page rendered at 60 dpi; any PNG < 5 KB trips the blank-page
  heuristic — inspect the raster. For chart dossiers, rasterize EVERY page and check charts against
  source data.
- **G3 round-trip**: `pdftotext` must return every sentinel string written at generation time;
  empty extraction routes to the OCR ladder, never to shipment. Note: line-wrapped hyphens break
  exact sentinel matches — pick sentinels that cannot hyphenate.
- **G4-data accuracy**: every number printed in the PDF is recomputed from the source data by the
  generator script — never hand-typed — and any derived statistic (ratios, projections) discloses
  its computation basis in the artifact or its sidecar. (This gate caught the "~4x range" slip
  where the true ratio was ~6x.)
- **G4 adjudication** (evidentiary work only): LLM judge runs last, only after G1–G3, only
  pre-validated (chance-corrected kappa, position swap, 3 runs at temp 0).

## Step 4 — Anchor trust outside the file

Every delivered PDF is a SEAL capsule: content + provenance hash + verification verdict as one unit.
Threat model, anchor protocol, and gate detail: `references/trust-and-verification.md`.

1. SHA-256 over the final bytes. Embed the first 16 hex chars in the PDF footer itself (visible
   anchor on every printed page), in addition to the ledger entry.
2. Compute the Merkle leaf; append the anchor record to the VAULT999 hash-chained DAG.
3. Add an RFC 3161 qualified timestamp where evidentiary grade is required (PDF/A-4 + PAdES path).
4. VOID on any mismatch at re-verification. Internal PDF dates and viewer signature checkmarks are
   claims, never evidence.
5. Redaction = content REMOVAL + rasterize-verified re-extraction, never overlay; record the
   redaction EVENT as a new ledger entry without retaining the content.

## References (load only when needed)

- `references/cognition-doctrine.md` — evidence tables: scanning stats, 4±1, effect sizes,
  polarity/halation, typography spec, debunked myths.
- `references/toolchain-matrix.md` — full generation-pipeline matrix (7 rows incl. struck
  wkhtmltopdf), reading-stack ladder with cost/throughput, benchmark-drift rule.
- `references/trust-and-verification.md` — threat model (shadow attacks, redaction failures),
  anchor protocol detail, four-gate ladder, FABRIKASI negative-capability list.
