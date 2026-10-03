# PDF_OPERATIONS — the one appendix (composer · verifier · cognition · styles · trust)

Single operational reference for pdf-federation. Everything here is evidence-backed; sources were
the 2026-10-02 HERMES PDF Intelligence research corpus (10 dimensions, cross-verified) plus the
absorbed forge-artifact-publisher / scientific-pdf-generation / civic-intelligence-pdf /
empirical-audit-pdf skills. Full evidence tables preserved in
`.archive/pdf-federation-consolidation-20261002/`.

## 0. The one rule

Every capability claim cites raw probe output from THIS node and THIS session, or it is VOID.
Run `bash scripts/probe_manifest.sh` first, every session, every node; save output next to the
deliverable. A prose claim of probing is fabricable.

Flag definitions: **PRESENT** = binary/lib found on node · **EXECUTABLE** = compiles + dry-runs
clean · **PROVEN** = executed end-to-end here with passing gates. Presence is a fact; fitness is a
verdict — wkhtmltopdf is PRESENT-class on many nodes yet FORBIDDEN (repo archived Jan 2023,
Qt WebKit frozen ~2012–2015, unpatched CVE-2022-35583 CVSS 9.8 SSRF; wrappers inherit the risk).

## 1. Engine routing (probed 2026-10-02 on forge)

| Task | Pipeline | Why | Verify |
|---|---|---|---|
| Text dossier ≤2 pp | `pandoc --pdf-engine=xelatex` (typst where probed) | ~5s/24pp; typst ≈27× faster, tags by default | G1+G3; dark legal at ≤2pp only |
| Report >2 pp or print | pandoc/typst, LIGHT theme | polarity rule: dark-on-light reads better; print beats screen | G1–G3; contrast ≥7:1 |
| Full-control / chart dossier, live data | reportlab + matplotlib (PNG ≥150 dpi) | coordinate-exact, single script | G1–G3 + charts vs source data |
| HTML/CSS tweaked in browser | weasyprint (no JS; Grid partial) | CSS paged media, 50–80% smaller files | G2 mandatory |
| JS-heavy / modern Grid HTML | `google-chrome --headless --print-to-pdf` (chromium MISSING here) | only real-browser engine | G2 mandatory — blank/tofu silent |
| DOCX/PPTX → PDF | `soffice --headless --convert-to pdf` | reliable; NOT thread-safe — one doc per instance | G1+G2 (fonts substitute silently) |
| Read text | PyMuPDF → pdftotext backup | instant; OCR ladder only if layer empty | G3; empty → OCR, never ship |
| Scanned / evidentiary | tesseract (98–99% clean print @300dpi) → VLM; SHA-256 → Merkle → RFC 3161 | in-file signatures broke 16/29 viewers | G3 + sampled human check |

Gotchas: weasyprint needs `printBackground: true` equivalents + base64-inlined images (local
`file://` src silently renders blank pages <5KB); Plotly/Kaleido needs a real browser binary;
PDF→DOCX fails ~6.2% vs DOCX→PDF ~1.1% — never promise symmetric conversion; `pandoc` cannot read
PDFs as input.

## 2. Compose

### 2.1 Manifest path (the governed default)

`python3 scripts/compose_artifact.py references/build-manifest.v1.yaml`

One machine-readable manifest drives one governed PDF. Producers (WEALTH, GEOX, HERMES, CHRON)
supply typed CONTRACTS (FigureAsset / ClaimEnvelope), never PDFs. Composition =
`compile(manifest) → one PDF + one envelope.json`. Authority state stays OBSERVE_ONLY — producers
may not self-seal; arifOS seals. EMD reflex arc: ENCODE (gather + tag every claim OBS/DER/INT/SPEC)
→ METABOLIZE (verify claims live, charts from fetched data, never stale) → DECODE (render +
Gate + envelope + FlowReceipt to arifFlow: Execute on render, Verify on gates, Seal on tri-witness QA).

### 2.2 Quick path

`bash scripts/md_to_pdf.sh input.md out.pdf` — routes xelatex → weasyprint → chromium → soffice by
probe. One source of truth in markdown; pipe-tables only (spaces/hand-rolled HTML get eaten).

### 2.3 SVG diagram patterns (from forge-artifact-publisher)

Tectonic timeline · cross-section schematic · phase/wedge architecture · cooling
path/time-temperature · knowledge graph · issue cards. CSS constants: `--basin-green #1b4332`,
`--accent-green #2d6a4f`, `--text-dark #0d1b2a`; evidence colors **OBS #28a745 · DER #007bff ·
INT #ffc107 · SPEC #dc3545**; body 'Segoe UI'/Arial 10.5pt; @page A4 landscape margin 1cm (slides)
/ portrait 2cm (dossiers).

### 2.4 Style presets

**Civic briefing — Scheme A Vibrant (default, proven Jul 2026):** Red #e74c3c/bg #fdf2f2 (critical)
· Green #22c55e/#f0fdf4 (positive) · Amber #f59e0b/#fffbeb (watch) · Purple #8b5cf6/#faf5ff (human
cost) · Blue #3b82f6/#eff6ff (context) · Dark #1e293b/#f8fafc (bottom line) · body #2d2d2d (never
pure black). Scheme B Gold/Amber (archival): gold #f0a500 H1, amber #ffa657 H2, panel #161b22,
page #0d1117, body #e6edf3. Civic typography: Helvetica 10pt body JUSTIFY, H1 18pt gold
bottom-border, tables 9pt alternating rows, footer 8pt centered.

**Scientific/analyst (Mode C):** white bg; navy #003366 (headers, table header rows, banner);
gold #C5A572 (BUY/SELL accent, key takeaways); teal #2A9D8F (bullish); red #C73E1D (bearish);
rows white/#F3F4F6; body Helvetica 8.8pt justify leading 11.5pt; captions 7.8pt centered.
Recommendation banner = 4-column table: navy/white top row, rating-coded bottom (BUY teal /
HOLD gold / SELL red + target price). Mode B intelligence dossier: dark palette
(#0d1117 page, #e6edf3 text), reportlab BaseDocTemplate, per-page char-count verification
(designed pages ≥800 chars, spill <300). Mode A academic: pandoc→xelatex with cross-refs.

Every analytical PDF carries an explicit **Caveats line IN the artifact** — sidecar notes are not enough.

### 2.5 B2B invoice composition (vendor → client)

Recurring pattern from catering / supply / service contracts. Composition rules that protect both sides at audit:

**Pre-render math verification.** When the user provides both line items AND a stated grand total,
recompute sum-of-line-items in Python first. If they match, proceed. If they mismatch, STOP and
ask the human — the mismatch is a real-world arithmetic error that belongs in their hands, not
silently "fixed" by editing one side.

**Daily or batch subtotals stay inside the main table.** Use `<tr class="day-total">` after each
batch — repeating header + grouped rows + subtotal line. These belong inside `<tbody>` and repeat
naturally as the page breaks.

**Grand total lives OUTSIDE `<tfoot>`.** weasyprint repeats `<tfoot>` on every page break, so a
grand total placed there will print on every page of a multi-page invoice. Move it to a separate
table block placed AFTER the closing `</table>` of the main table. Use a heavier top+bottom border
so it visually reads as the closing figure. Verify with `pdfinfo out.pdf | grep Pages` then visually
check first vs last page — same grand total on every page = bug, fix and re-render.

**Complimentary items: itemise at RM0.00 with a `(Complimentary)` suffix.** Never omit them —
the audit trail (delivery receipt, kitchen record) needs every line that left the kitchen. Suffix
the description: `Creampuff (Complimentary)`. Unit price and line amount both `RM0.00`.

**MOQ vs actual consumption: declare both.** When a supply contract bills at a Minimum Order
Quantity (e.g. hot coffee MOQ 400 pax/month at RM3.90) but actual consumption is lower (e.g.
387 pax), append a transparency note in the description: `(Actual consumption 387 pax; MOQ 400
pax billed — 13 pax unused)`. This prevents the client asking the same thing and getting a
suspicious-looking zero-difference.

**Instalment schedule as a separate sub-table.** When invoice carries payment milestones, render
them as a table AFTER the totals row with columns `Milestone / Percentage / Amount / Due Period`
plus a `tfoot` Total row. The grand total table lives BEFORE the schedule; the schedule lives
BEFORE the payment info box. Never inline milestone amounts into the main line-item table.

**Date format.** Spell out dates for invoices (`1 September 2026`), not `1.09.2026` or `1/9/2026`.
Account payable systems parse both but humans do not — invoices live at the human edge.

**Number convention.** `YYYYMMDD-NNN` (e.g. `20260930-001`) is the working format for sequential
monthly invoicing — sortable, dedup-able, audit-friendly. Use `-001`, `-002` for the same day's
second invoice.

## 3. Verify — no PDF ships without gates

`bash scripts/pdf_verify.sh out.pdf "headline claim" "key sentinel"`

- **G1 structural**: `pdfinfo` exit 0 + page count; `qpdf --check` exit 0 (syntax only — PDF/A-UA
  claims need veraPDF).
- **G2 rasterize**: first AND last page at 60 dpi; PNG <5KB trips the blank-page heuristic — inspect.
- **G3 round-trip**: `pdftotext` finds every sentinel; empty layer → OCR ladder, never ship.
  Pick sentinels that cannot hyphenate.
- **G4-data**: every printed number recomputed from source by the generator script, never
  hand-typed (this gate caught a real ~4x claim that was ~6x). Derived stats disclose their basis.
- **G4-hash**: sha256 printed on pass — feed to VAULT999 ledger; embed first 16 hex chars in the
  footer for print-visible anchoring.

Anti-patterns (each one bit a real build): skipping page-count check (blank slides ship) ·
local file paths in weasyprint `<img src>` (silently blank, <5KB PDF) · vision-checking page 1
only (cover-pass ≠ artifact-pass — check a random body page) · dark-theme ink-coverage sweeps
(useless on dark pages — use per-page char count) · exit-0 celebration (blank/tofu/clipping all
exit 0). LLM judges only AFTER G1–G3 and only pre-validated (chance-corrected kappa, position
swap, 3 runs temp 0): raw agreement overstates 33–41pp; self-family preference 67–82%; an
unvalidated judge is a NEGATIVE verifier.

## 4. Empirical rule (audit/capability PDFs)

Every claim in an audit PDF backs to a probe or live API response captured in the SAME run —
`subprocess` every binary+lib version, fetch live data once and derive all charts from it, never
screenshot prior sessions, never recite catalogs. Evidence density is credibility. Structure:
cover (4-line table: title/date/mode/source/goal) → live numbers + 1 chart → inventory + heatmap
→ copy-paste snippets + 2-min decision matrix. 4 pages, single script end-to-end.
Benchmark rule: never quote a benchmark without harness+version+date (OmniDocBench v1.5→v1.6 moved
existing models' scores; same model reads 97.9% on one harness, 50.3 on another).

## 5. Cognition essentials (evidence-magnitudes in archive doctrine)

1. **First-Screen Contract**: BLUF + ≤4 chunks on page 1 — 79% scan vs 16% word-by-word, ~20–28%
   of words read, verdict in ~10s, 57% of viewing time on first screenful. Working memory = 4±1
   chunks (a panel/table/chart/callout each counts).
2. **Headings are standalone claims** (layer-cake): a scanner who stops anywhere still exits with
   the argument. Inverted pyramid per paragraph; restate BLUF at section boundaries.
3. **Every visual answers a named question or is deleted**: functional d=0.86–1.22; decorative
   imagery g=−0.95, harm LARGER on paper (g≈−0.61). Tables for exact values, position-encoded
   charts for trends; no 3D, no dual axes, zero-baseline bars, direct labels over legends;
   figure at first citation (split-attention g=0.63).
4. **Polarity**: dark ONLY ≤2-page on-screen glanceables; light default >2min/print; contrast ≥7:1
   (floor 4.5:1); body 10.5–11.5pt print, 60–75 CPL, 1.4–1.5× leading, bold not italics,
   left-aligned ragged right. Serif-vs-sans = NULL — choose for tone.
5. **Tags = machine interface**: structure tree in reading order, no skipped heading levels, alt
   text, embedded Unicode fonts (untagged PDF has no logical order for readers OR extractors).

## 6. Trust — anchored OUTSIDE the artifact

`content → SHA-256 → Merkle leaf → VAULT999 hash-chained DAG → RFC 3161 timestamp (evidentiary)`.
Viewer signature checkmarks are claims (shadow attacks defeated 16/29 viewers, NDSS 2021);
internal PDF dates are rewritable claims — time comes from RFC 3161; exiftool-style sanitization
removes references, not objects (1,237 "sanitized" files still leaked full metadata). Redaction =
content REMOVAL + rasterize-verified re-extraction, never overlay (Manafort 2019, TikTok/Kentucky
2024, DOJ 2025). Redaction events are recorded as new ledger entries WITHOUT retaining content.

## 7. Delivery

Telegram: `MEDIA:/absolute/durable/path.pdf` (forge_work, never /tmp) — Hermes auto-attaches.
**Never claim an attachment you did not build and verify** — "[PDF Attachment]" without a real
file is fabrication; users call it out ("Tepek sini"). Own misses in one plain line, rebuild,
deliver, move on. Confirm the Telegram API response; delivery is not done until the send is real.

## 8. Never cite (debunked)

Goldfish 8s attention (fabricated 2015 marketing deck) · "images 60,000× faster" / "90% visual"
(1982 ad, no source) · "maximize germane load" (retracted by Sweller 2019) · dyslexia fonts
(consistent nulls; letter SPACING is the lever) · "66-char optimal line" (folklore; ~55 CPL
comprehension, ~95 speed) · "whitespace +20% comprehension" (inflated blog number).

## 9. Reading / extraction (routed, not re-implemented here)

Born-digital → PyMuPDF (10–50× faster than PyPDF2/pdfminer); borderless tables → pdfplumber;
scans/degraded → `ocr-and-documents` + tesseract ladder; evidence-grade claims from untrusted
PDFs → `forge-document-intelligence`. CID-keyed fonts without ToUnicode extract as `/31 /8 /18`
garbage — detect with `pdffonts uni=no`, fix only via OCR fallback.
