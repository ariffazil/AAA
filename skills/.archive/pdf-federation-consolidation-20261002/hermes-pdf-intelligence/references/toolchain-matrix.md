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
