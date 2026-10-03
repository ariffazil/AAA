# HERMES PDF INTELLIGENCE — Doctrine (absorbed from hermes-pdf-intelligence)

**Source:** `/root/.hermes/skills/hermes-pdf-intelligence/SKILL.md` (sha256 `87208163af121d1f2c2a0540a6d76f4a4cc241fbaf561f366335c8fcdd7d140a`, 117 lines)

**Status:** absorbed doctrine. The doctrine, not the skill entry. Source skill deprecated, content preserved.

---

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


---

## Original references (preserved verbatim)


### cognition-doctrine.md

# Cognition Doctrine — Evidence Base (condensed from HERMES PDF Intelligence Report, ch. 2–4)

Load this file when designing document content/layout. Every rule below carries its evidence and
magnitude. A doctrine that cites fabricated numbers forfeits its evidential standard — never quote
a number that cannot be forged from a logged experiment. DITEMPA BUKAN DIBERI: forged, not given.

## 1. The measured attention budget (ch. 2)

| Rule | Evidence | Magnitude |
|---|---|---|
| First-Screen Contract: BLUF block + 3–5 key findings on page 1 | Paragraph-fixation decay 81%→71%→63%→32% (NN/g 2013); ~10 s value verdict (Nielsen 2011, 2B-record dwell data); 57% of viewing time lands on the first screenful (NN/g 2018) | Behavioral shares, not effect sizes |
| Design for scanners, not readers | 79% scan vs 16% read word-by-word (Nielsen 1997); reading depth ceiling ~28% theoretical, ~20% realistic (Weinreich et al. 2008, 45,237 page views) | Behavioral shares |
| Headings as standalone claims (layer-cake by design) | Layer-cake = most effective scan pattern (NN/g 2017); headings causally improve recall of topics and organization (Sanchez, Lorch & Lorch 2001, n=140) | Causal recall gain |
| 4±1 chunk budget per view (bullets, cards, comparison columns) | Working-memory central capacity is 4±1 (Cowan 2001, >10,800 citations); Miller's 7±2 was strategy-assisted, not raw capacity | Visual STM 3–4 |
| Bold numbers, names, decision asks; one idea per paragraph | Spotted-scanning fixations target bold/digits (NN/g 2019); concise+scannable+objective rewrite (Morkes & Nielsen 1997) | +124% measured usability |
| Signal structure; segment dense content | Signaling meta-analysis (Richter & Scheiter 2015, N=2,500); segmentation meta (56 comparisons) | signaling r=.15; segmentation d=.36; replication: signaling retention g+=0.53 (Schneider 2018, 103 studies) |
| Restate BLUF at section boundaries; inverted pyramid per paragraph | Skimming preserves gist but loses inference (Duggan & Payne 2009); a satisficing reader who stops anywhere must still exit with the main point | Experimental |
| Progressive disclosure ≤2 levels | NN/g progressive disclosure (2006): few important items first, detail behind clearly scented cues | Practitioner-standard, evidence-aligned |

## 2. Visual doctrine (ch. 3) — every visual answers a named question or is deleted

| Rule | Evidence | Magnitude |
|---|---|---|
| Functional visuals help | Mayer & Fiorella 2014 program medians: coherence (remove extraneous) 23/23 tests; spatial contiguity 22/22; temporal contiguity 9/9; redundancy 16/16; signaling 24/28 | d = 0.86 (coherence); 1.10 (spatial contiguity); 1.22 (temporal); 0.86 (redundancy); 0.41 (signaling) |
| Honest replication discount | Cromley et al. 2025 meta of Mayer corpus (181 studies, 591 effects): overall g = 0.37; text+diagrams g = 0.39 (Guo 2020, 39 studies, independently identical) | ~half the originator program's sizes |
| Decorative imagery is a measured harm, not neutral | Seductive details meta (Rey 2012): overall g = −0.48; images g = −0.95 vs text g = −0.27; Sundararajan & Adesope 2020 (68 effects): paper-based g ≈ −0.61 vs video ≈ −0.05; end-of-document placement g = −0.70 | An irrelevant image costs ~2× an irrelevant paragraph; harm is LARGER on paper — the PDF condition |
| Pictures must represent, organize, interpret, or transform | Levin, Anglin & Carney (87 studies): every function positive EXCEPT decoration (null) | Classification meta-analysis |
| Direct labels over legends; figure at point of first citation | Split-attention / spatial-contiguity cost of separation | d = 0.72 (Ginns 2006, 37 studies); g = 0.63 (Schroeder & Cenkci 2018) |
| Encoding accuracy: position first, color last | Cleveland & McGill 1984 hierarchy, replicated crowdsourced (Heer & Bostock 2010); area worse than angle | Replicated |
| Tables for exact values, charts for patterns | Cognitive fit (Vessey 1991); tables win "retrieve value" on speed+accuracy+preference (Saket 2019); DeSanctis review: 12 pro-table, 7 pro-graph, 10 tie | Chart-with-data-labels = best of both for non-interactive PDF |
| Zero-baseline bars; no 3D; no dual axes | Truncated bars cause major misinterpretation that survives warnings (Pandey 2015; ACM 2024); 3D depth cues lower accuracy (Talbot 2014); dual axes manufacture correlation (UK ONS) | Measured cost per sin |
| Risk quantities as icon arrays with natural frequencies ("7 in 100") | Bayesian task success 4% → 24% (McDowell & Jacobs 2017 meta) | 6× success |

## 3. Typography, polarity, layout spec (ch. 4)

| Rule | Evidence | Magnitude / spec |
|---|---|---|
| Positive polarity (dark-on-light) for sustained reading; halation penalizes light-on-dark | Buchner & Baumgartner 2007; Piepenbrock 2013/14 (pupil-constriction mechanism); halation amplified by astigmatism | 5–15% reading-speed advantage at body sizes even at identical contrast |
| Print beats screen for comprehension | Delgado 2018 meta, 54 studies, >170k participants; corroborated Clinton 2019 | g ≈ −0.21 for screen vs paper |
| Dark-Dossier Compromise | Synthesis of polarity + halation + screen-inferiority | Light default >2 pages or print; dark ONLY ≤2-page glanceables; contrast ≥7:1 either way (dark variant: surface #121212, text ~#E0E0E0, weight +1 step; #B0B0B0 on #121212 ≈ 8:1) |
| Font size is the lever; typeface is not | Rello, Pielot & Marcos 2016 (CHI, N=104): readability improves monotonically, comprehension better at 18–26 pt, plateau ~22 pt | Print body 10.5–11.5 pt; screen ≥18 pt-equivalent; never below 10 pt |
| Line length | Dyson & Haselgrove 2001 (~55 CPL comprehension); Shaikh 2005 (speed peaks ~95 CPL); failure zone past 80–100 CPL | 60–75 CPL for comprehension-first documents; 25 mm margins at 10.5–11.5 pt achieves this naturally |
| Line spacing tolerant mid-band | Rello 2016: only 0.8× and 1.8× extremes harm | 1.4–1.5×; never <1.2 or >1.8 (1.5× is a WCAG floor, not an experimental optimum) |
| Margins / contrast / alignment | WCAG 2.2 SC 1.4.3/1.4.6/1.4.8/1.4.11 | 25 mm all sides; contrast ≥7:1 target, 4.5:1 floor; left-aligned ragged right, no full justification; bold not italics (italics impair reading speed) |
| Serif vs sans | Ho Sang & Petraca 2025 PRISMA review, 42 studies; Arditi & Cho RSVP null | NULL — choose typeface for tone, not readability |
| Tags = machine interface | PDF/UA (ISO 14289-1/-2); untagged PDF has no logical order for screen reader AND extractor alike | Structure tree in reading order, H1–H6 no skips, alt text, embedded Unicode-mapped fonts, language+title, validate with veraPDF/PAC |
| Type scale | Practitioner convention (marked as convention) | 1.25–1.4× per level (e.g. 11/14/18/22/28 pt), ≤4 levels |

## 4. Debunked myths — never cite in HERMES output

| Myth | Verdict | Trace |
|---|---|---|
| "Attention span of a goldfish (8 s)" | Fabricated | Unsourced 2015 Microsoft Canada deck; BBC debunk 2017. Real measures: ~47 s avg / 40 s median screen attention (Mark 2023) |
| "Brain processes images 60,000× faster than text" (and "90% of information is visual") | Fabricated | Traced to a 1982 Business Week advertisement; no scientific source exists |
| "Serif is more readable in print / sans on screen" | Busted (null) | 42-study systematic review 2025; Arditi & Cho 2005 RSVP null |
| "Dyslexia fonts (OpenDyslexic, Dyslexie) help" | Busted | Consistent nulls (Wery & Diliberto 2017; Kuster 2018); the Dyslexie effect traced to its spacing (Marinus 2016). Real lever: extra-large letter+word spacing (Zorzi 2012 PNAS, contested stats) |
| "45–75 CPL, 66 optimal" | Part-folklore | Bringhurst convention; experiments support ~55 CPL comprehension, ~95 speed |
| "Whitespace improves comprehension ~20%" | Direction supported, number inflated | Lin 2004, small single lab study, blog-amplified |
| "1.5× line spacing is optimal" | Part-supported | Codified WCAG floor; experiments show only extremes harm |


---


### toolchain-matrix.md

# Toolchain Matrix — Generation Pipelines and Reading Stacks (condensed from report ch. 5)

Load this file when routing a PDF task after `scripts/probe_manifest.sh` has run. Every capability
claim must cite probe output from THIS environment and THIS session, or it is VOID. A MISS at probe
time routes to the named fallback, never to hope.

## 1. Generation pipeline matrix (2026 status)

| Pipeline | Layout control | Speed (typical) | CSS fidelity | i18n/fonts | Tagged-PDF / a11y | Status |
|---|---|---|---|---|---|---|
| Pandoc + XeLaTeX | Highest (decades of packages) | Slow: 9.65 s / 4-page doc, multi-pass | n/a | Excellent (XeCJK, bidi, unicode-math) | PDF/UA-2 only via LuaLaTeX + TeX Live 2025 `\DocumentMetadata` | Active; multi-GB install |
| Typst 0.14+ | Very high (typesetting language) | Fastest class: 356 ms / 4-page doc, ~27x XeLaTeX | n/a | Good Latin; CJK gaps; RTL needs `auto-bidi` | Tagged BY DEFAULT; PDF/UA-1 enforced at compile time | Active, rising; single ~13 MB binary |
| ReportLab 4.x | Very high (programmatic, coordinate-exact) | ~0.08 s/page | n/a | TTF/OTF embed; RTL needs reshaper hacks | Limited tagging (UNTAGGED PDF 1.4 by default); PDF/A in paid PLUS tier | Active (BSD core); mature |
| WeasyPrint 67–70 | High (CSS Paged Media) | ~227 ms cold page; ~100 s / 52 pages | Very good; Grid partial; NO JavaScript | Pango shaping; good CJK/RTL | PDF/UA-1 since v57; UA-2 + PDF/A-4e/f in v67 | Very active |
| Headless Chromium / Playwright | High (full web platform) | 42–119 ms cold; 3–13 ms warm pool | Reference (full CSS/JS) | Full browser stack; best i18n | Tagged since Chrome 85/106; quality rated "mediocre" | Very active |
| LibreOffice headless (`soffice --convert-to pdf`) | Medium (Office layout) | Seconds per document | n/a | Excellent Office i18n | Tagged export supported; PDF/A config-driven | Active; NOT thread-safe — one document per instance |
| ~~wkhtmltopdf~~ | Medium | 0.5–1 s | BROKEN (2012-era Qt WebKit: no Grid, no Flexbox, no CSS variables, JS ~ES5.1) | Frozen ICU | None | FORBIDDEN — repo archived read-only Jan 2023, last release 0.12.6 (Jun 2020), unpatched CVE-2022-35583 CVSS 9.8 SSRF. Wrappers (PDFKit-python, python-wkhtmltopdf, DinkToPdf, Rotativa, NReco) inherit the risk. Pandoc itself dropped it as default engine in 2024. |

Routing notes:
- HTML→PDF fork: no JS + paged CSS → WeasyPrint (50–80% smaller files, better tags); JS charts or modern Grid → Chromium (only real-browser engine; WeasyPrint cannot execute JS-rendered D3/Chart.js/Plotly).
- Markdown reports: Pandoc with Typst engine is the 2026 default where probed; XeLaTeX where Typst absent.
- Charts: vector-first. matplotlib → PDF for LaTeX/Typst includes, SVG for HTML pipelines; PNG only at ≥150 dpi when the pipeline rejects vector. Plotly static export (Kaleido ≥1.0) requires a SEPARATELY installed Chrome/Chromium — a probe with Plotly but no browser is a render-time failure.
- Conversion direction is asymmetric: PDF→DOCX fails ~6.2% vs DOCX→PDF ~1.1% (single-vendor corpus). Never promise it symmetrically.

## 2. Reading-stack ladder (extraction)

| Tier | Stack | Throughput | Accuracy class | Cost / 1k pages | When to use |
|---|---|---|---|---|---|
| 1. Text layer | PyMuPDF / pdfplumber / pypdf / pdfminer.six | ms-scale; PyMuPDF 8.01 s / 7,031 pages (10–50x faster than PyPDF2/PDFMiner) | Perfect text fidelity on born-digital; structurally blind (reading order, tables, scans) | ~$0 (compute) | Born-digital PDFs with a text layer. PyMuPDF for speed, pdfplumber for borderless tables, pypdf for merge/split |
| 2. Layout pipelines | Docling / Marker / MinerU | 0.21–3.1 s/page GPU; Docling 3.1 s/page CPU | Layout-aware; Marker 2 balanced 76.0 olmOCR-bench @ 2.9 pg/s; MinerU 86.47 OmniDocBench v1.6 | Compute only; GPU break-even vs API in low 100k pages/month | Scanned or complex layouts at volume; structure reconstruction on owned hardware |
| 3. Specialist VLMs | PaddleOCR-VL (0.9B), MinerU2.5-Pro (1.2B), GLM-OCR (0.9B) | 1.4–2.1 pg/s datacenter GPU | SOTA 95.2–96.3 OmniDocBench v1.6 (model-card self-reports); ~20-pt drop on photographed/warped pages | Compute only; single consumer GPU | Accuracy-critical parsing of degraded scans. Beats 235B general models at ~1% of compute |
| 4. Hosted APIs | Mistral OCR, Textract, Azure DI, Google DAI | Service-side | Commodity-strong; 25-pt table spread (RD-TableBench, vendor-run) | $1.50 raw OCR; $2 Mistral OCR 3; $10–30 layout; $65 Textract forms+tables | Burst volume without GPU; NEVER for sovereign-sensitive documents |
| 5. Frontier VLM page-reading | Claude, Gemini | 1,500–3,000 tokens/page; ≤100 pages visual (Claude) | Strong reasoning, WEAKER parsing than specialists; hallucinated page ranges observed | Token-priced, order-of-magnitude costlier | Reasoning over extracted content; visual QA of rendered pages (G2); never bulk extraction |

Routing doctrine: extraction and reasoning are different workloads. Route per page by type — born-digital
text to tier 1, structured layouts to tier 2, degraded scans to tier 3 — and reserve frontier VLMs for
reasoning over extracted content, never for re-deriving glyphs a text layer already encodes. Extra
reasoning tokens actively degrade parse quality (GPT-5.2 thinking-level test: accuracy flat ~0.79,
cost/latency +5–8x).

Known extraction failure modes: CID-keyed fonts without ToUnicode → garbage `/31 /8 /18` extraction
(detect with pdffonts `uni=no`; fix only via OCR fallback); multi-column reading-order bleed (0.564 →
0.816 with column-region detection; PyMuPDF4LLM ceiling 0.860); empty text layer on scans.

## 3. Benchmark-drift rule (CZ3 resolution)

Never quote a benchmark without harness, version, date, and runner. OmniDocBench spans v1.0 (981 pp),
v1.5 (1,355), v1.6 (1,651) — v1.6's corrected matching MOVED existing models' scores (MinerU2.5:
90.67 in its own paper, 92.98 as a v1.6 baseline). Docling table accuracy is 97.9% under IBM's metric
and 50.3 on olmOCR-bench — different harnesses, both "true". Vendor-run numbers are self-reports;
flag them. Before trusting any extraction component, score it on a stratified sample of the
federation's own documents with human ground truth: a 50-page local probe beats leaderboard shopping.


---


### trust-and-verification.md

# Trust and Verification — Threat Model, Verification Ladder, Honest Gaps (condensed from report ch. 5–6, dim09, dim10)

Load this file before sealing, redacting, or adjudicating any PDF. Core doctrine (I5): trust is
anchored OUTSIDE the artifact. The file is evidence; the ledger is proof.

## 1. Threat model — why in-file trust is insufficient

| Attack / failure | Evidence | Doctrine consequence |
|---|---|---|
| Shadow attacks on signed PDFs | Mainka, Mladenov & Rohlmann (NDSS 2021, CVE-2020-9592/9596): standard-compliant content hide/replace defeated signature validation in 16 of 29 tested viewers | A viewer's signature checkmark is a claim, not evidence. Never conclude integrity from it |
| Redaction by overlay | Failure record: Manafort (Jan 2019), Kentucky AG v. TikTok (Oct 2024), DOJ Epstein files (Dec 2025) — black rectangles over live text layers | Redaction = content REMOVAL + rasterize-verified re-extraction. Never cosmetics |
| Metadata leakage | ~39–40k PDFs from 75 security agencies / 47 countries mostly leaked hidden data; 1,237 files "sanitized" with exiftool still yielded full metadata — the tool removes the reference, not the object (arXiv:2103.02707) | Metadata sanitization requires object-level removal; treat all internal metadata as claims |
| Internal dates | PDF internal dates are rewritable | Dates inside the file are claims, never evidence. Time comes from RFC 3161 |
| Hallucinated success (agent-side) | Premature termination + skipped verification >14% of observed multi-agent failures (directional, secondary); agents hallucinate tool invocations (Google ADK issue #4173) | Decouple the success signal from the agent that did the work (F9 Anti-Hantu) |

## 2. The anchor protocol (D5)

```
content bytes -> SHA-256 digest -> Merkle leaf -> append to hash-chained DAG (VAULT999)
              -> RFC 3161 qualified timestamp where evidentiary grade is required
```

Reference logic (per report snippet S8):

```python
import hashlib
h = hashlib.sha256(open(path, "rb").read()).hexdigest()
leaf = hashlib.sha256(bytes.fromhex(h)).hexdigest()  # Merkle leaf over file digest
anchor = {"artifact": path, "sha256": h, "merkle_leaf": leaf,
          "ledger": "VAULT999", "status": "SEALED"}  # append to hash-chained DAG
# VOID on any mismatch. RFC 3161 qualified timestamp added where evidentiary
# grade is required; internal PDF dates are claims, never evidence.
```

- Evidentiary grade: PDF/A-4 (ISO 19005-4, on PDF 2.0) for permanence + PAdES-B-LTA with a
  qualified RFC 3161 timestamp. eIDAS Article 41(2) gives qualified timestamps a presumption of
  accurate time and data integrity that reverses the burden of proof — no in-file mechanism does this.
- veraPDF (pinned installer) gates any PDF/A or PDF/UA conformance claim. qpdf does not.
- Redaction events are the one sanctioned irreversibility: content is destroyed, but the EVENT is
  recorded as a new hash-chained VAULT999 entry — provability of what/when without retaining content (F1 Amanah).

## 3. The four-gate verification ladder (D7) — deterministic first, model last

Mismatch at any gate is a hard fail, never "log and continue."

| Gate | Method | Pass criteria | Failure response |
|---|---|---|---|
| G1 Structural integrity | `qpdf --check`; `pdfinfo`; `pdffonts`; veraPDF for PDF/A/UA profiles | qpdf exit 0; page count = expected; every font `emb=yes`; no `uni=no` CID fonts; veraPDF "PASSED" for declared profile | Regenerate from source; rebuild ToUnicode maps; embed fonts; do not ship |
| G2 Rasterized visual QA | `pdftoppm -png` per page; deterministic checks first (blank-page size/luminance heuristic, bbox non-empty); vision model second | Zero blank pages; no clipping; no tofu glyphs; every claimed chart present on its expected page | Re-render with explicit waits (`networkidle0`, `waitForSelector`); `printBackground: true`; provision fonts; regenerate figures |
| G3 Text round-trip | `pdftotext` / PyMuPDF on the RENDERED artifact; sentinel assertions; word-count tolerance vs source | Extraction non-empty; all sentinels found; no CID-garbage sequences | OCR fallback on corrupted layers; regenerate with proper subsetting/ToUnicode |
| G4 Adjudication (model-last) | LLM judge against rubric, only after G1–G3 pass; judge pre-validated | Judge reports chance-corrected kappa; position-swap consistency; 3 runs at temperature 0 | Reject or re-baseline the judge; an unvalidated judge verdict is void |

G4-data (data accuracy): every number printed in the PDF is recomputed from the source data by the
generator script — never hand-typed — and any derived statistic (ratios, projections) must disclose
its computation basis in the artifact or its sidecar; a hand-typed narrative number is FABRIKASI.

G4 discipline: the largest LLM-judge study (21 judges, ~541k judgments) found raw agreement
overstates quality by 33–41 percentage points of kappa deflation; self-family preference reaches
67–82% in high-risk contexts. An unvalidated judge is a NEGATIVE verifier — it manufactures
confidence. `scripts/pdf_verify.sh` implements G1–G3; G4 is human/judge protocol, not a script.

Tool-OK != page-correct: blank pages, missing backgrounds, and tofu all return exit status 0 from
the generator. A zero exit status is evidence that a process completed, not that a page rendered.

## 4. FABRIKASI — the negative capability list (claims VOID until probed)

- Live re-rendering of data inside an opened PDF — render happens at build time; "live" means a
  pre-render snapshot frozen into the artifact.
- Audio embedded in PDF — possible via reportlab, but no verified federation pattern exists.
- Pixel-perfect modern CSS Grid via WeasyPrint — partial support; Chromium headless is the probed
  path for JS-heavy layouts.
- Better-than-95% OCR on heterogeneous real-world scans or handwriting — clean print at 300 DPI is
  98–99%; hand-filled forms stay below 95% document-level; degraded documents fall to 72.7% (wet);
  handwriting belongs to frontier VLMs (1.2–1.5% CER on IAM, capped near 85% on hard medical forms).
- Voice-to-PDF in one step — unbuilt; the chain is speech-to-text -> Markdown -> pandoc, and it is
  doctrine only once probe-verified end-to-end.
- Trustworthy redaction of third-party PDFs without content destruction + rasterize-verified
  re-extraction.
- Any integrity conclusion from a viewer's signature checkmark (shadow attacks, 16/29 viewers).
- Tagged PDF from raw reportlab — output is UNTAGGED PDF 1.4. Closing paths (unprobed): pandoc +
  LuaLaTeX `-V pdfstandard=ua-2` (TeX Live 2025), or Typst >=0.14 (tags by default).
- Symmetric conversion promises: PDF->DOCX fails ~6.2% vs DOCX->PDF ~1.1%.

Any assertion of the above without fresh probe output is FABRIKASI — fabricated until probed — and
VOID under F4 Clarity. Say what the federation cannot do, in writing; that registry is doctrine.


---

