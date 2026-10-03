---
name: civic-intelligence-pdf
description: "Generate colour-coded civic intelligence briefing PDFs. Two"
triggers:
  - "civic briefing pdf"
  - "intelligence dossier pdf"
  - "civic intelligence"
  - "briefing pdf with colors"
  - "dark themed pdf"
  - "intelligence briefing"
capability_tier: fed-long-context
ecology_state: WARM
---

# Civic Intelligence PDF Generation

## When to Use

When producing civic intelligence briefings, synthesis documents, or analysis outputs that need to be read fast, scanned for signals, and understood at a glance. NOT for academic papers or print-first archival docs (use `scientific-pdf-generation` skill for those).

**Trigger:** User asks for a briefing, dossier, or synthesis PDF with visual emphasis, color coding, or intelligence aesthetic.

## Design Philosophy

Design is governance, not aesthetics. Color forces attention to what matters. The goal is 60-second scannability — a reader must extract the top 3 signals without reading full paragraphs.

## Two Modes

| Mode | Use Case | Background | Status |
|------|----------|------------|--------|
| **Light-clean (RECOMMENDED — DEFAULT)** | Contrast clarity, executive review, readable docs | White/off-white, sharp contrast | LIVE |
| **Dark** | Screen reading, intelligence briefings, Telegram delivery | #0d1117 (GitHub dark) | Legacy / opt-in only |

### Light-Clean Design Spec

```
Background:    #ffffff (white)
Page bg:       #fafbfc (subtle off-white when needed)
Body text:     #1a1a1a (near-black, not pure #000 for screen comfort)
Accent gold:   #c49500 (warmer, visible on white)
Signal green:  #16a34a (green calls positive)
Signal amber:  #d97706 (warning attention)
Signal red:    #dc2626 (critical/threat)
Signal blue:   #2563eb (info/data)
Dim text:      #64748b (captions, footer)
Table header:  #f1f5f9 + #334155 border-bottom (no filled cells)
Box bg:        #fefce8 (amber), #f0fdf4 (green), #fef2f2 (red), #eff6ff (blue)
Border radius: 6px everywhere (consistent, not aggressive)
Font:          Helvetica Neue / Arial, 10pt body, 1.6 line-height
H1 underline:  none — use accent color + top border only
Shadow:        none (flat design = no rendering variance)
Emphasis:      Bold for structure, color for status ONLY. No italic blocks.
```

Key principle: **Less noise, more signal**. White space > box density. One accent per element max. No gradient cards, no overlapping layers.

## Stack

**Option A: Chrome headless** (preferred — no extra install, handles modern CSS better):
```bash
google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="output.pdf" --print-to-pdf-no-header "input.html"
```

**Option B: WeasyPrint** (fallback):
```bash
weasyprint input.html output.pdf
```

Single HTML file with inline CSS. No external dependencies.

## Colour Palette — Two Schemes

### Scheme A: Vibrant (v2 — proven Jul 2026, brighter, better for screen scanning)

| Colour | Hex | Meaning |
|---|---|---|
| Red | `#e74c3c` / bg `#fdf2f2` | Structural problems, critical warnings |
| Green | `#22c55e` / bg `#f0fdf4` | Forged discipline, positive signals |
| Amber | `#f59e0b` / bg `#fffbeb` | Attention failures, watch items |
| Purple | `#8b5cf6` / bg `#faf5ff` | Human cost, tragedy, dignity |
| Blue | `#3b82f6` / bg `#eff6ff` | Context, data, economic backdrop |
| Dark | `#1e293b` / bg `#f8fafc` | Executive summary, bottom line |
| Body text | `#2d2d2d` | All body text (NOT pure black) |
| Cover gradient | `#1a1a2e` → `#16213e` → `#0f3460` | Dark intelligence aesthetic |

### Scheme B: Gold/Amber (original — warmer, more archival)

| Colour | Hex | Meaning |
|---|---|---|
| Gold | `#f0a500` | Primary accent, H1, executive callout borders |
| Amber | `#ffa657` | Secondary accent, H2, warnings |
| Green | `#3fb950` | Positive / Forged / metabolized |
| Red | `#f85149` | Critical / Threat / active scars |
| Blue | `#58a6ff` | Info / Data |
| Body text | `#e6edf3` | Near-white on dark bg |
| Dim | `#8b949e` | Captions, footer, metadata |
| Panel bg | `#161b22` | Callout boxes, alt rows |
| Page bg | `#0d1117` | GitHub dark |

**Default: Scheme A (vibrant)** for briefings. **Scheme B (gold/amber)** for more formal/archival tone.

## Typography

```
Body:        Helvetica, 10pt, #e6edf3, JUSTIFY
H1:          Helvetica-Bold, 18pt, #f0a500, gold bottom border
H2:          Helvetica-Bold, 14pt, #ffa657
H3:          Helvetica-Bold, 11pt, #3fb950
H4:          Helvetica-Bold, 10pt, #58a6ff
Tables:      9pt, alternating row backgrounds (#161b22 / #0d1117)
Blockquotes: Helvetica-Oblique, 10pt, #ffa657, gold left border
Footer:      8pt, #8b949e, center-aligned
```

## Page Template

```css
@page {
  size: A4;
  margin: 2cm 2.2cm;
  @top-left { content: "Document Title — Date"; font-size: 7pt; color: #8b949e; }
  @top-right { content: "arifOS Federation"; font-size: 7pt; color: #f0a500; font-weight: bold; }
  @bottom-center { content: "Page " counter(page) " of " counter(pages); font-size: 7pt; color: #8b949e; }
}
@page :first { @top-left { content: ""; } @top-right { content: ""; } }
```

## Document Structure

### 1. Cover Page
- Title (28pt, #f0a500, centered)
- Gold divider line (200px, 2px, #f0a500)
- Subtitle (16pt, #ffa657)
- One-line summary / headline quote (11pt, #ffa657, italic)
- Meta block: preparer, mode, epistemic band, confidence, classification
- `page-break-after: always`

### 2. Contents (Optional)
- Summary strip (dark panel, key-value pairs)
- Only for documents >8 pages

### 3. Body Sections
- H1 with section number in gold (e.g., `I`, `II`, `III`)
- H2 for subsections
- H3 for specific items
- Callout boxes between sections for key findings

### 4. Appendices (When Applicable)
- Epistemic discipline table (OBS/DER/INT/SPEC tags)
- Source matrix
- Glossary

### 5. Footer Philosophy
- Centered, 8pt, dim
- "DITEMPA BUKAN DIBERI" + epistemic disclaimer + preparer + date

## Component Library

### Stat Cards (v2 — Key Numbers Dashboard)

3-5 gradient cards in a flex row. White text on dark gradient. For headline numbers only.

```html
<div class="stats">
  <div class="stat-card stat-red">
    <div class="num">~49</div>
    <div class="label">BN Seats<br>of 56</div>
  </div>
  <div class="stat-card stat-green">
    <div class="num">⅔</div>
    <div class="label">Chose restraint<br>over cash</div>
  </div>
</div>
```

```css
.stats { display: flex; justify-content: space-around; gap: 10px; flex-wrap: wrap; }
.stat-card { text-align: center; padding: 18px 15px; border-radius: 10px; flex: 1; min-width: 120px; color: white; }
.stat-card .num { font-size: 28pt; font-weight: 800; line-height: 1; }
.stat-card .label { font-size: 8.5pt; margin-top: 6px; opacity: 0.9; text-transform: uppercase; }
.stat-red { background: linear-gradient(135deg, #e74c3c, #c0392b); }
.stat-green { background: linear-gradient(135deg, #27ae60, #1e8449); }
.stat-blue { background: linear-gradient(135deg, #2980b9, #1a5276); }
.stat-purple { background: linear-gradient(135deg, #8e44ad, #6c3483); }
.stat-orange { background: linear-gradient(135deg, #e67e22, #d35400); }
.stat-dark { background: linear-gradient(135deg, #2c3e50, #1a252f); }
```

Rule: Max 5 stat cards. More than 5 = eyes glaze.

### Numbered Pills (v2)

For ranked lists (surprises, findings):
```css
.pill { display: inline-block; background: #e74c3c; color: white; padding: 2px 8px; border-radius: 12px; font-size: 9pt; font-weight: 700; }
.pill-green { background: #22c55e; }
.pill-purple { background: #8b5cf6; }
.pill-blue { background: #3b82f6; }
.pill-orange { background: #f59e0b; }
```

### Section Header (v2 — coloured banner)

```css
h2 { padding: 10px 15px; border-radius: 6px; color: white; }
.s-politics { background: #e74c3c; }
.s-human { background: #8e44ad; }
.s-capital { background: #27ae60; }
.s-attention { background: #e67e22; }
.s-entertainment { background: #3498db; }
.s-watch { background: #2c3e50; }
```

### Signal Box (General Accent)
```css
.signal-box {
  background: #161b22;
  border-left: 4px solid #f0a500;
  padding: 12px 16px;
  margin: 14px 0;
  border-radius: 0 6px 6px 0;
}
.signal-box.red { border-left-color: #f85149; }
.signal-box.green { border-left-color: #3fb950; }
.signal-box.amber { border-left-color: #ffa657; }
.signal-box.blue { border-left-color: #58a6ff; }
```
Use for: inline signal annotations, structural diagnoses, sharp takes.

### Executive Callout (Big Finding)
```css
.exec-callout {
  background: #1a1f28;
  border: 2px solid #f0a500;
  padding: 20px 24px;
  margin: 20px 0;
  border-radius: 8px;
}
.exec-callout .headline {
  font-size: 14pt; color: #f0a500; font-weight: bold; margin-bottom: 10px;
}
```
Use for: top-level findings, election results blocks, major announcements.

### Key Insight Box (Positive Signal)
```css
.key-insight {
  background: #0d1f0d;
  border: 1px solid #3fb950;
  padding: 16px 20px;
  margin: 16px 0;
  border-radius: 6px;
}
.key-insight .label {
  color: #3fb950; font-size: 8pt; font-weight: bold;
  text-transform: uppercase; letter-spacing: 1px;
}
```
Use for: hidden headlines, standout positive signals, "the real story."

### Warning Box (Threat / Casualty)
```css
.warning-box {
  background: #1f0d0d;
  border: 1px solid #f85149;
  padding: 16px 20px;
  margin: 16px 0;
  border-radius: 6px;
}
.warning-box .label {
  color: #f85149; font-size: 8pt; font-weight: bold;
  text-transform: uppercase; letter-spacing: 1px;
}
```
Use for: mass casualty events, structural compromises, existential threats.

### Civic Thermometer Table
Standard table with color-coded "Reading" column:
```html
<td class="reading-critical">CRITICAL</td>  <!-- #f85149 -->
<td class="reading-warning">WARNING</td>      <!-- #ffa657 -->
<td class="reading-good">POSITIVE</td>        <!-- #3fb950 -->
<td class="reading-info">INFO</td>            <!-- #58a6ff -->
```

### Summary Strip (Key-Value Dashboard)
```css
.summary-strip {
  background: #161b22; padding: 14px 18px; margin: 16px 0;
  border-radius: 6px; border: 1px solid #30363d;
}
.summary-strip .item {
  display: flex; justify-content: space-between;
  padding: 4px 0; border-bottom: 1px solid #21262d;
}
```
Use for: quick-read dashboards, fact summaries, "Feeling-Fact-Law" blocks.

### Epistemic Tags
```css
.tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 8pt; font-weight: bold; }
.tag-obs { background: #0d2818; color: #3fb950; }   <!-- Observed -->
.tag-der { background: #1a1a0d; color: #ffa657; }   <!-- Derived -->
.tag-int { background: #1a0d1a; color: #bc8cff; }   <!-- Interpreted -->
.tag-spec { background: #1a0d0d; color: #f85149; }  <!-- Speculative -->
```

## Forge Process (3 Steps)

1. **Content kernel locked** — All analysis, data, and synthesis finalized before any HTML is written.
2. **Visual encoding applied** — Every status, severity, or signal gets explicit color treatment. Callout boxes for key findings. Tables with color-coded readings.
3. **Epistemic provenance + footer** — Appendices (source matrix, glossary, epistemic tags), "DITEMPA BUKAN DIBERI" footer, confidence score.

## Scoping Protocol (from open-slide eureka)

Before writing ANY briefing code, lock 4 decisions via `clarify`:

1. **Color scheme** — vibrant (v2, brighter, screen scanning) / gold-amber (warmer, archival). Mark one "(Recommended)" based on audience.
2. **Signal density** — sparse (3-5 signals) / moderate (6-10) / dense (11+). Drives callout box count.
3. **Epistemic strictness** — relaxed (narrative-driven) / standard (tagged claims) / strict (every claim sourced, F2 discipline).
4. **Audience** — screen (dark theme, 10pt body) / print (light theme, 11pt body).

Skip only when already answered. Restate assumption if skipping.

## Budget Discipline (from open-slide eureka)

Fixed page size = forced prioritization. Before rendering, calculate:

```
Usable area = A4 - 2cm margins
Text budget = ~2000 characters per page (10pt, 1.5 line-height)
Signal budget = 1 callout box per 2 pages max
```

**Rules:** one signal per callout. Max ~2000 chars per page. Near budget = split page, never shrink font below 9pt. No overflow escape hatches.

## Design Tokens (from open-slide eureka)

Expose tweakable values as CSS variables in the HTML template:

```css
:root {
  --civic-bg: #0d1117;
  --civic-accent: #f0a500;
  --civic-text: #e6edf3;
  --civic-signal: #3fb950;
}
```

User adjusts via browser devtools or Jinja2 template vars, agent reads back, persists to template. Two surfaces: CSS vars for live tweaking, Python constants for arithmetic.

## Task Markers (from open-slide eureka)

Leave `@agent-task` markers in HTML source for async follow-up:

```html
<!-- @agent-task id="t-xxx" text="base64url(JSON{task, priority, context})" -->
```

Agent scans, finds, executes, deletes. Apply in reverse line order so line numbers stay valid.

## Pitfalls

- **Dark theme doesn't print well.** For print, use light variant (planned, not yet implemented). Tell user to read on screen.
- **WeasyPrint ignores box-shadow.** Don't use it. Use border instead.
- **vh/vw units may be rejected.** Use px or cm for padding/margins.
- **Emoji don't render in PDF fonts.** Replace with text labels (CRITICAL, WARNING, POSITIVE) or colored CSS classes.
- **Wide tables overflow.** Keep tables under 6 columns for A4. If more needed, restructure as lists.
- **WeasyPrint is slower than pandoc for text-only.** Use pandoc→xelatex for plain reports. Use weasyprint only when design matters.
- **File size.** Dark-themed PDFs are ~60-80KB for 10-14 pages. No image overhead since everything is CSS.

## Verification

After generating:
1. Check file size (50KB–100KB typical for 10-15 pages)
2. Open in PDF viewer — dark background, gold headings, color-coded tables
3. Verify text is selectable (weasyprint outputs real text, not images)
4. Check page count matches expectations
5. Verify callout boxes render with correct border colors

## Official Document Ingest — the number comes from the source document

Before any figure enters a briefing, ingest it from the document that PUBLISHES it, not from an
article about that document. The briefing's credibility is the provenance of its numbers; a
beautiful layout over a summarised figure is decoration on a defect.

| Figure class | Ingest from | Notes |
|---|---|---|
| Budget revenue / expenditure / subsidy / debt-service lines | **Buku Anggaran Hasil dan Perbelanjaan Persekutuan** (MOF) + Economic Report / Finance Bill | Line-item level — the aggregate headline is not the programme figure |
| GDP, CPI, labour, trade, mining & gas output | **DOSM** release PDFs (`open.dosm.gov.my`, `storage.dosm.gov.my`) | Match the metric label exactly — volume vs value, production vs exports |
| Monetary, OPR, financial stability, household debt | **BNM** Annual Report · Economic & Monetary Review · Financial Stability Review (`bnm.gov.my/publications`) | AR and FSR publish the same metric on different bases — quote both with their labels |
| Election results / seat counts | **SPR** result pages | Not outlet live-blogs |
| Corporate financials | Issuer report / Bursa announcement | Not the analyst note |

**Extraction discipline.** `pdftotext -layout` is fine for narrative and unreliable for tables —
it collapses columns. For any disclosed table use camelot (lattice/stream) or pdfplumber, then
**reconcile the extracted total against the printed total before use**. An unreconciled table is
not ingested. If extraction fails, report the gap and leave the figure out — never fill it from
commentary. (Same rule as `intelligence-brief-forge` → Table Extraction.)

**The pairing trap (scar 2026-09-18).** Two figures brought into relation inside a briefing —
debt-service charges beside tax receipts, a wage level beside a productivity figure — form an
**argument**. If the pairing came from an article rather than from each document, the argument is
the article's and the provenance does not transfer. Cite each figure to its own document, and
state the relationship as *your* inference with its basis. A briefing that borrows a juxtaposition
inherits the summariser's error and then signs it in the sovereign's name.

**A level is not a base.** When a source publishes a growth rate, a back-solved level is a derived
figure: label it as yours and show the derivation, or leave it out. Attributing a computed level to
the body that published only the rate is the defect an auditor finds first, because the arithmetic
looks impeccable while the citation is false.

**Ingest receipt.** Per document: source body · document title · period · page or table reference ·
content hash. The briefing appendix carries that table, so a reader can open the same document and
land on the same line.

## Data Analytics Layer (charts, maps, diagrams)

Every briefing MUST include embedded visual analytics when data supports it. Use these tools:

### Available on this VPS

| Tool | Purpose | Install |
|------|---------|---------|
| matplotlib 3.11 | Bar charts, line charts, donut/pie, heatmaps | `pip install matplotlib` |
| cartopy 0.25 | Static geospatial maps (coastlines, markers, zones) | `pip install cartopy` |
| graphviz 0.21 | Flow diagrams, decision trees, impact chains | `pip install graphviz` + `apt install graphviz` |
| folium 0.20 | Interactive HTML maps (for web delivery, not PDF) | `pip install folium` |
| PIL/Pillow 12.3 | Image compositing, resizing | `pip install Pillow` |

### Chart Types — When to Use

| Data Shape | Chart Type | Library |
|-----------|------------|---------|
| Comparison across categories | Horizontal/vertical bar chart | matplotlib |
| Trend over time | Line chart (single or dual-axis) | matplotlib |
| Part-of-whole / severity distribution | Donut chart (not pie — cleaner) | matplotlib |
| Geographic distribution / risk zones | Static map with markers + zones | cartopy |
| Decision flow / impact chain | Directed graph (flow diagram) | graphviz |
| Multi-variable comparison | Grouped bar or small multiples | matplotlib |

### Analytics Pipeline (3-step)

1. **Generate chart images** — Python scripts output PNG at 200 DPI to `/tmp/civic_analytics/`
2. **Embed as base64** — HTML template uses `data:image/png;base64,...` inline (no external files)
3. **Render PDF** — WeasyPrint processes the single HTML file with all images embedded

### Chart Design Rules

- White background (`facecolor='white'`) — matches light-clean theme
- No gridlines on maps (causes cartopy/shapely bugs)
- Font: Arial/Helvetica, 9pt labels, 11pt titles
- Color palette matches signal colors: `#16a34a` (good), `#d97706` (warning), `#dc2626` (critical), `#2563eb` (info)
- Max 2 charts side-by-side (`.two-col` flex layout)
- Every chart needs a caption (`.chart-caption`, 8pt, italic, grey)
- `page-break-inside: avoid` on all chart containers

### Map Rules (cartopy)

- Use `CartoDB positron` style equivalent: `LAND=#f8fafc`, `OCEAN=#e0f2fe`
- No gridlines (shapely LinearRing bug with small extents)
- Markers: `marker='o'`, `markersize=10`, `markeredgecolor='white'`
- Zone circles: `plt.Circle()` with `alpha=0.15-0.2`
- Legend: `loc='lower left'`, `frameon=True`, `facecolor='white'`

### Flow Diagram Rules (graphviz)

- `shape='box'`, `style='filled,rounded'`
- Risk nodes: red fill (`#fef2f2`), observe: blue (`#eff6ff`), mitigate: green (`#f0fdf4`)
- Edge labels: 9pt, describe the relationship
- `bgcolor='white'`, `dpi='200'`

## Automated Pipeline (Jinja2 — Content-in → PDF-out)

```bash
python3 scripts/generate_briefing.py content.json output.pdf
```

Content JSON structure: `title`, `subtitle`, `date`, `confidence`, `headline_quote`, `executive_summary`, `sections[]` (with `subsections[]` containing `tables[]`, `callouts[]`, `lists[]`, `blockquote`), `thermometer[]`, `scar_map[]`, `reflection{}`, `appendices[]`, `glossary[]`.

Full template: `scripts/generate_briefing.py` — Jinja2 template with all CSS components inline.

Sample content: `references/sample_content.json` — the Malaysia briefing in JSON format. Copy and modify.

To generate manually from HTML: `weasyprint input.html output.pdf`

## Template Reference

Full working HTML template: `references/proven-template.html` — the Malaysia Civic Intelligence Briefing (2026-07-11). Copy and modify. All CSS components (signal boxes, callouts, key insights, warning boxes, summary strips, epistemic tags, civic thermometer) are included inline.

## Proven

- 2026-07-11: Malaysia Civic Intelligence Briefing — 14 pages, 61KB, dark theme with gold/amber/green/red semantic coding. WeasyPrint HTML→PDF. Delivered via Telegram.
