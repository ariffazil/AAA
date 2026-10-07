---
name: html-pdf-reporting
description: Build polished HTML reports with embedded visuals and render to PDF using weasyprint (or pandoc/wkhtmltopdf fallback) for arifOS federation deliverables. Use when asked for "PDF report", "human-language report", "visual data analytics", "dashboard PDF", or "WEALTH/AAA briefing" with charts and tables. Covers chart library choice, page-break rules, federated dark theme, and the critical weasyprint JS pitfall.
---

# html-pdf-reporting

Federation reports must look engineered, not generated. This skill encodes the patterns that worked on the Petronas-Brazil sunk-cost report (Aug 2026).

## The one pitfall that bites every first attempt

**weasyprint does NOT execute JavaScript.** Chart.js, D3, Plotly, ECharts — none render. Your dashboard shows empty white boxes in the PDF even though the HTML looks perfect in a browser.

**Two viable paths:**

| Path | Use when | Trade-off |
|---|---|---|
| **A. Static PNG charts** generated via matplotlib → base64 data URI → embed in HTML → WeasyPrint (proven 2026-08-06, 12-chart Gentari deep-research PDF) | You need a pixel-perfect print artifact with real data charts | More setup, two pipelines (matplotlib script + HTML template), but fully offline-portable |
| **B. CSS-only visuals** (waterfall bars, donut bars, timelines, KPI cards) drawn with HTML+CSS as inline boxes | You're willing to skip interactive Chart.js styling for the PDF | Single pipeline, but you lose tooltips |

The Petronas-Brazil report used **path B with CSS-rendered bars** (`.wf-bar` absolute-positioned divs, percentages hard-coded, no canvas). The HTML version still ships Chart.js for interactive viewers, but the PDF render is pure CSS. This is the recommended pattern for simple KPI/tornado/waterfall charts.

If you need real data charts (capacity growth, geographic mix, financial time series, radar, BOD network diagrams), use **path A**. The proven 2026-08-06 sequence: (1) `gen_charts.py` produces matplotlib PNGs at 180 dpi → `/path/to/charts/01_chartname.png` etc; (2) Python script reads each PNG as bytes → base64-encode → replaces `__CHn__` placeholders in the HTML template; (3) WeasyPrint renders the HTML with embedded data URIs. The HTML file ends up ~1-1.3 MB but is fully self-contained — no external image fetches, no CDN dependencies. Verified on Gentari Deep Research v2: 18 pages, 811 KB PDF, 12 charts embedded as image+smask pairs, all rendered correctly. If you must have chart visuals in the PDF, generate them server-side before render — see `references/weasyprint-js-pitfall.md`.

### Path A — matplotlib base64-embed pipeline (proven 2026-08-06)

```python
# gen_charts.py — produces /charts/01_*.png ... 12_*.png at 180 dpi
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
NAVY="#0e1a2b"; GOLD="#c9a227"; RED="#c0392b"; GREEN="#27ae60"; BLUE="#2c7be5"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":"#cccccc",
                     "axes.titlecolor":NAVY,"text.color":NAVY,"figure.facecolor":"white",
                     "savefig.facecolor":"white","savefig.bbox":"tight"})
# fig, ax = plt.subplots(figsize=(9.5, 4.5)); ... plt.savefig(f"/charts/{i:02d}_name.png", dpi=180)

# build_report.py — embeds PNGs as base64 data URIs
import base64, os
CH = "/path/to/charts"
def b64(fname):
    with open(os.path.join(CH, fname), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()
IMGS = {f"CH{i+1}": b64(f"{i+1:02d}_name.png") for i, name in enumerate([...])}
html = open("report_template.html").read()
for k, v in IMGS.items(): html = html.replace(f"__{k}__", v)
open("report.html","w").write(html)

# render
weasyprint report.html "Report_2026-08-06.pdf"
```

Verification after render: `pdfimages -list report.pdf | grep -c image` should equal 2× the chart count (each PNG = image + smask alpha channel). For 12 charts = 24 image objects. Verified 2026-08-06 Gentari v2: 12 charts → 24 image objects rendered.

## Tools available on this host (verified 2026-08-06)

- `weasyprint 64.x` — primary renderer. Honors @page, CSS print, page-break-*.
- `pandoc` — markdown→PDF/HTML. Limited CSS control.
- `wkhtmltopdf` — Qt-based, handles limited JS.
- `xelatex` — TeX path, but slow and unforgiving.

## Render pipeline

```bash
weasyprint report.html "Report_Name_Date.pdf" 2>&1 | tail -20
ls -lh *.pdf
```

Then deliver via Telegram: `MEDIA:/absolute/path/to/file.pdf` in your reply.

## Federated report style (from arif-fazil.com house style)

- **Cover page** with dark theme (linear-gradient navy `#0e1a2b`), gold accent `#c9a227`, kicker line in uppercase letterspaced caps.
- **KPI hero row** at the top — 5 cards in a flex row, big numbers, gold/green/red/blue color-coding.
- **Section headings**: 16pt Helvetica bold, gold underline (border-bottom 2px solid #c9a227).
- **Box callouts**: `.box` (blue), `.box.gold`, `.box.red` — left-border accent, 4mm padding.
- **Tables → appendix only**. Per Arif (Aug 2026 explicit feedback: "Update the pdf and tranform the Table to visual data. Table Put AS ref or Appendix"). Body text + visuals; tables in Appendix A1/A2/etc.
- **Epistemic tags**: `.tag.obs` green, `.tag.der` blue, `.tag.int` gold — inline after numbers, never as footnotes.
- **Footer**: page X/Y, document confidentiality line.

See `templates/report-cover.html` and `templates/report-body.html` for starters.
See `references/surat-terbuka-template-2026-08-09.md` for the open-letter/civic-intelligence pattern (cover page, pull quotes, KPI cards, callout boxes — different from data reports).

## Visual patterns that work (CSS-only, no JS)

1. **Waterfall chart** — labelled rows, div bars positioned by percent width, gradient backgrounds.
2. **Donut chart** — use `<canvas>` ONLY for interactive HTML; for PDF, use a stack of CSS arcs (rarely worth it) OR render server-side with matplotlib + base64 embed.
3. **Timeline** — flex-row of dots + dates + descriptions, a 2px horizontal line as the connector. Works in print.
4. **Tornado chart** — indexAxis:'y' Chart.js for HTML; CSS bars for PDF.
5. **KPI cards** — flex row, equal width, big numbers.
6. **Comparison cards** — 3 cards in flex row with colored top borders.

## Arif's explicit report style (2026-08-06)

> "Give me full PDF report Here. Human language"

- No corporate buzzwords. Write like a senior analyst talking to the F13 SOVEREIGN.
- Lead each section with the verdict, not the methodology.
- Every claim needs `[OBS]` / `[DER]` / `[INT]` tag — no naked numbers.
- "But", "However", "The honest headline is…" — direct language, not hedged.
- Tables in appendix; visuals in body. Tables show low/mid/high ranges + epistemic tag column.
- Always include a sensitivity tornado.
- Always include an "Where I might be wrong" section.
- Always end with a "one-line ledger for the sovereign" paragraph.

## Minimum visual quality — no plain text dumps (2026-08-09)

Every PDF must meet a minimum visual bar — **including open letters (surat terbuka) and civic intelligence documents.** A plain WeasyPrint HTML→PDF with Liberation Serif, no branding, no visual hierarchy, and no colored sections is NOT acceptable. At minimum:
- Header/masthead with document title + date (use the dark theme cover pattern)
- Section headings with accent color (gold underline)
- Key data in visual format (KPI cards, colored boxes) — not raw tables in body
- Pull quotes for strong lines (styled blockquotes with accent border)
- Page numbers + footer
- Professional font stack (not just Liberation Serif)

Arif explicitly rejected a plain Surat Terbuka PDF (2026-08-09): "Kenapa pdf ni buruk sangat" — the content was strong but the presentation looked like a Notepad dump. Content strength does not excuse poor visual design. **Civic intelligence documents (open letters, public briefs) are the federation's public face — they MUST look engineered.**

**Formal letters to officials = different standard (2026-08-09 correction).** When Arif sent the Surat Terbuka to MPs, he corrected the suggestion to add branding/colors: "Wei ni surat nak hantar kat ahli parlimen lanwei." Formal correspondence to government officials should maintain appropriate formality — clean typography, numbered paragraphs, proper spacing, but NOT infographic-style design. The minimum visual bar applies to BRIEFINGS and REPORTS; formal LETTERS should look like formal letters. **Don't over-design what should be dignified.**

## matplotlib execution environment (2026-08-09)

**CRITICAL:** `matplotlib` is NOT available in `execute_code` sandbox. Always use `terminal()` for chart generation:

```python
# WRONG — will fail with ModuleNotFoundError
from execute_code import matplotlib  # ❌

# CORRECT — run via terminal()
terminal(command='python3 << "PYEOF"\nimport matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n# ... chart code ...\nplt.savefig("/tmp/charts/01-name.png", dpi=150, bbox_inches="tight")\nPYEOF')
```

Then embed charts in HTML using `file://` URIs (simpler than base64):

```html
<img src="file:///tmp/charts/01-revenue-trend.png" />
```

**Verified 2026-08-09:** `file://` URIs work in WeasyPrint for local files. No base64 encoding needed. Charts render correctly in PDF.

## Path C — Markdown → WeasyPrint PDF (no HTML template, no JS)

When the source is a `.md` file (audit, classification table, doctrine artifact, sovereign spec) and the deliverable is a PDF the sovereign reads in Telegram, this is the lightest path. The current `html-pdf-reporting` skill describes paths A and B (HTML+matplotlib or HTML+CSS charts). Path C is the markdown-direct path proven tonight.

**When to use path C:**
- Source is markdown, not raw data
- No charts needed; tables and prose carry the content
- The sovereign reads in Telegram via `MEDIA:` (PDF file viewer, not a browser)
- One-shot document, not a recurring report
- A single Python script does MD→HTML→PDF in one call

**Why path C:**
- The HTML-template-and-CSS skill covers data reports. Audit/classification PDFs are mostly tables, source quotes, and the `[OBS] / [REPORTED] / [DECLARED]` truth-ladder tags. Charts are noise.
- Building a CSS template per document inflates context (10+ KB of CSS for a 50-row table).
- The output is structurally identical to a markdown viewer rendered to print: head, body, tables.

**Recipe (proven 2026-10-06, multi-document: math inventory, narrative classification, items-1-3 exec):**

```python
import markdown as md_lib
from weasyprint import HTML, CSS

src = Path('/abs/path/source.md')
dst = Path('/abs/path/out.pdf')
md_text = src.read_text()

# Convert MD → HTML (extensions matter: tables, fenced_code, toc)
html_body = md_lib.markdown(md_text, extensions=['tables', 'fenced_code', 'toc', 'attr_list', 'def_list'])

# Inline CSS — no external file, no @import, no CDN
css = """
@page { size: A4; margin: 18mm 16mm; @bottom-right { content: counter(page) " / " counter(pages); font-family: 'DejaVu Sans', sans-serif; font-size: 9pt; color: #666; } }
@page :first { @bottom-right { content: ''; } }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 10pt; line-height: 1.42; color: #1a1a1a; }
h1 { font-size: 18pt; font-weight: 700; color: #5a1a1a; margin: 0 0 4pt; padding-bottom: 6pt; border-bottom: 2pt solid #5a1a1a; }
h2 { font-size: 14pt; font-weight: 700; color: #5a1a1a; margin: 14pt 0 6pt; padding-bottom: 3pt; border-bottom: 1pt solid #c0a0a0; page-break-after: avoid; }
h3 { font-size: 11.5pt; font-weight: 700; color: #7a3a3a; margin: 10pt 0 4pt; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 8.5pt; page-break-inside: avoid; }
th { background: #5a1a1a; color: white; padding: 4pt 6pt; text-align: left; font-weight: 700; }
td { padding: 3pt 6pt; border: 0.5pt solid #d0c0c0; vertical-align: top; }
tr:nth-child(even) td { background: #faf5f5; }
code, pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.5pt; background: #f0e8e8; padding: 1pt 3pt; }
blockquote { border-left: 2.5pt solid #7a3a3a; padding: 4pt 8pt; margin: 6pt 0; background: #faf5f5; font-style: italic; }
"""

HTML(string=f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{html_body}</body></html>").write_pdf(
    target=str(dst), stylesheets=[CSS(string=css)]
)
```

**Two pitfalls specific to path C:**

1. **`pip install --break-system-packages` is required for `markdown`** in the same way as weasyprint (PEP 668 externally-managed-environment). The base hermes venv does not have `markdown`. Install once, or fall back to a hand-rolled minimal MD→HTML (just regex on `^#+ ` for headers, `|` for tables). Verified 2026-10-06: `python3 -c 'import markdown; print(markdown.__version__)'` returned 3.11 after install.
2. **`write_file` refuses to overwrite a recently-read script.** Re-using the path of a script you already created in the same session will be rejected as a stale-write guard. Either delete the old script first, or write to a new path with `_run.py` suffix. Verified 2026-10-06: `compile_horizon_seal.py` was accepted on first write; re-writing it as `exec_items_1_3_run.py` required the new path.

**When NOT to use path C:**
- Document needs data charts (use path A)
- Document is for a civic / public surface where brand matters (use path A or B with the cover/body templates in `templates/`)
- Document is a surat terbuka / formal letter (use the formal-letter pattern noted below in this skill)

**The path is so light it can be re-run per artifact.** When the source markdown changes, re-rendering takes one second and 50-100 KB PDF. Treat the script as ephemeral; keep the source MD as the durable artifact.

## Cross-cutting pitfalls (paths A/B/C)

- **doctype/head encoding**: include `<meta charset="utf-8">` or WeasyPrint mangles non-ASCII.
- **Google Fonts**: WeasyPrint downloads them; if offline, fall back to system fonts (Helvetica, Arial).
- **page-break-inside: avoid** on box callouts and tables; they break ugly.
- **Long URLs**: in tables, use display:none on mobile but allow line-wrap in print.
- **External CDN scripts**: Chart.js CDN works in interactive HTML; PDF must not depend on it.
- **Image rendering**: external `<img src="https://...">` may fail offline; for portability, base64-embed or copy locally.
- **Matplotlib `Circle`/`FancyBboxPatch` import bug**: import via `matplotlib.patches`, NOT `matplotlib.pyplot`. Always `from matplotlib.patches import Circle, FancyBboxPatch`.
- **`weasyprint` not installed by default** on this host — install with `pip install --break-system-packages weasyprint` (PEP 668). Same flag needed for `markdown` package (path C).
- **Filename pattern discipline**: matplotlib chart files must be named `##_name.png` (zero-padded) and embedded via base64 data URI. Don't reference local paths in `<img src>`.
- **Filename builder `.png` extension bug**: include the extension in filename builders — `f"{i+1:02d}_{name}.png"` not `f"{i:02d}_{name}"`.
- **Two-image-object chart verification**: each PNG renders as TWO PDF image objects (`image` + `smask` alpha). For 12 charts, `pdfimages -list | grep -c image` = 24 (or 20 with aliasing). The 2×-ish ratio is the success signal.
- **`write_file` stale-write guard**: re-using the path of a script you already created in the same session will be rejected. Either delete the old script first, or write to a new path with `_run.py` suffix. (Path C specific; covered above.)

## Support files

- `templates/report-cover.html` — cover page template (dark theme, gold accent, verdict box).
- `templates/report-body.html` — body template with KPI row, section, waterfall, donut, timeline, tornado.
- `references/weasyprint-js-pitfall.md` — full diagnosis + fallback patterns.
- `references/federated-style.md` — house-style details (colors, fonts, KPI cards).
- `references/light-theme-protocol-pdf.md` — light-theme protocol/educational PDF pattern (clean white, step flows, checklists, AI-generated instructional images). For non-federation deliverables: health protocols, reference guides, equipment checklists.
