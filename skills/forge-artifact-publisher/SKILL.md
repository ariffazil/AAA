---
name: forge-artifact-publisher
id: forge-artifact-publisher
description: "EMD artifact forge — the OUTPUT direction of AAA document intelligence. Takes structured internal intelligence (GEOX OKF, WEALTH analysis, AAA knowledge graphs, literature reviews) and forges publication-grade visual+text PDF artifacts. SVG diagrams, embedded images, knowledge graphs, reality graphs, tectonic timelines, prospect evaluations — all rendered as geologist-ready slide packs or dossier PDFs. Load when: 'make a PDF', 'visual pack', 'slide deck', 'dossier', 'forge artifact', 'publish to telegram', 'send report'. "
version: 1.1.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
risk_tier: low
floor_scope: [F1, F2, F4, F6, F11]
autonomy_tier: T1
capability_tier: fed-reasoning-heavy
ecology_state: WARM
tags: [artifact-publisher, pdf-forge, visual-intelligence, svg-diagrams, slide-pack, dossier, knowledge-graph, reality-graph, telegram-delivery, emd-output, geological-reports, arifflow, reality-loop, skill-mesh]
dependencies:
  - aaa-pdf-voice-protocol (voice translation layer)
  - forge-document-intelligence (provenance patterns)
  - forge-visual-qa-w3 (visual QA tri-witness)
  - forge-design-intelligence (design tokens, colour palettes)
  - reality-loop-operator (7-stage loop integration)
  - Chrome headless (PDF conversion)
  - Telegram Bot API (delivery)
  - arifFlow (metabolic ledger, FlowReceipt emission)
forged: 2026-09-15
apex-zen: 2026-09-15
session: FI-003 Kinabalu Basin visual pack session
---# FORGE ARTIFACT PUBLISHER — EMD Output Reflex Arc

> **DITEMPA BUKAN DIBERI** — Intelligence is forged into artifacts, not dumped as text.
> **The human reads the artifact. The agent reads the source. Never confuse the two.**

## 0. WHAT THIS SKILL IS

This is the **OUTPUT direction** of AAA document intelligence. While `forge-document-intelligence` handles INPUT (PDF → OCR → structured data), this skill handles OUTPUT (structured intelligence → visual artifacts → PDF → delivery).

The provenance pipeline:

```
forge-document-intelligence:  PDF → OCR → structured data → agents  (INPUT)
forge-artifact-publisher:     agents → structured data → visual → PDF → human  (OUTPUT)
aaa-pdf-voice-protocol:       internal vocabulary → publication prose  (TRANSLATION)
```

**This skill is the forge.** It takes the raw intelligence that agents produce — knowledge graphs, reality graphs, tectonic timelines, prospect evaluations, literature syntheses — and transforms them into artifacts that a geologist can read, understand, and act on.

---

## 1. THE EMD REFLEX ARC FOR ARTIFACT PRODUCTION

```
┌─────────────────────────────────────────────────────────────────┐
│  ENCODE (Gather + Structure)                                     │
│  ────────────────────────────────────────────────────           │
│  Input: Internal intelligence (OKF, YAML, claims, literature)   │
│  Agent: Reads all source files, compiles structured content      │
│  Output: Section-by-section content manifest                     │
│  Floor: F2 TRUTH — every claim tagged OBS/DER/INT/SPEC          │
│  Gate: Content completeness check — no section empty             │
└─────────────────────┬───────────────────────────────────────────┘
                      │  Content manifest
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  METABOLIZE (Design + Visualize)                                 │
│  ────────────────────────────────────────────────────           │
│  Input: Content manifest + existing images                       │
│  Agent: Generates SVG diagrams, selects images, designs layout   │
│  Output: HTML slides/pages with embedded SVG + base64 images     │
│  Floor: F4 CLARITY — visual hierarchy serves understanding       │
│  Gate: Voice protocol applied (no raw code/function names)       │
└─────────────────────┬───────────────────────────────────────────┘
                      │  HTML artifact
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  DECODE (Render + Deliver)                                       │
│  ────────────────────────────────────────────────────           │
│  Input: HTML artifact                                             │
│  Agent: Chrome headless → PDF, then delivers via channel         │
│  Output: PDF file + delivery receipt                              │
│  Floor: F1 AMANAH — artifact hash computed, delivery confirmed   │
│  Gate: PDF page count + file size sanity check                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. ARTIFACT TYPES

| Type | Format | When | Example |
|------|--------|------|---------|
| **Dossier** | A4 portrait PDF | Comprehensive single-topic report | Basin evaluation, prospect review |
| **Slide Pack** | A4 landscape PDF | Presentation-ready visual brief | Tectonic storyline, board pack |
| **Knowledge Graph** | PDF + SVG | Entity-relationship compilation | Basin intelligence graph |
| **Reality Graph** | PDF + SVG | Evidence + epistemic map | Claim audit, evidence inventory |
| **Visual Brief** | A4 landscape PDF | Image-heavy quick-see | Cross-section compilation, well data |
| **Executive Summary** | A4 portrait PDF | 1–2 page decision brief | Drilling recommendation |

---

## 3. SVG DIAGRAM PATTERNS

### 3.1 Tectonic Timeline

```svg
<!-- Pattern: Horizontal timeline with colour-coded event boxes -->
<svg viewBox="0 0 1000 400">
  <!-- Time axis -->
  <line x1="60" y1="350" x2="960" y2="350" stroke="#333" stroke-width="3"/>
  <!-- Age ticks -->
  <!-- Event boxes — colour by tectonic regime -->
  <!-- Evidence badges as coloured pills (green=measured, blue=derived, amber=interpreted, red=hypothesised) -->
  <!-- Source citations below badges -->
  <!-- Vertical connector lines from boxes to axis -->
</svg>
```

**Colours by regime:**
- Subduction/extension: `#2c3e50` (dark blue-grey)
- Collision: `#922B21` (deep red)
- Post-collisional: `#884ea0` (purple)
- Thermal/intrusive: `#e67e22` (amber)
- Ongoing/active: `#1b4332` (dark green)

### 3.2 Cross-Section Schematic

```svg
<!-- Pattern: Layered geological cross-section with labels -->
<svg viewBox="0 0 800 380">
  <!-- Sky (light blue) -->
  <!-- Sea (blue) -->
  <!-- Seafloor surface (path) -->
  <!-- Geological units as filled paths with distinct colours -->
  <!-- Structural features (faults as dashed lines, folds as curves) -->
  <!-- Labels positioned inside or adjacent to units -->
  <!-- Prospect symbols (circles with risk colours) -->
  <!-- Mass flow arrows -->
</svg>
```

### 3.3 Phase/Wedge Architecture

```svg
<!-- Pattern: Stacked rectangles showing evolution phases -->
<svg viewBox="0 0 600 400">
  <!-- Phase bars — height proportional to activity, colour by type -->
  <!-- Unconformity lines as dashed horizontal rules -->
  <!-- Thickness/wedge profile as a bold line -->
  <!-- Time axis at bottom -->
</svg>
```

### 3.4 Cooling Path / Time-Temperature

```svg
<!-- Pattern: X-Y plot with data points and connecting line -->
<svg viewBox="0 0 600 380">
  <!-- Axes with labelled ticks -->
  <!-- Data points as coloured circles -->
  <!-- Connecting path (bold red/orange) -->
  <!-- Reference lines (e.g., erosional rate as dashed grey) -->
  <!-- Annotation box for key metric (e.g., cooling rate) -->
</svg>
```

### 3.5 Knowledge Graph

```svg
<!-- Pattern: Node-edge graph with colour-coded node classes -->
<!-- Nodes: circles or rounded rects with class colours -->
<!-- Edges: lines with arrow markers and edge-type labels -->
<!-- Legend: node class colour key -->
```

### 3.6 Issue Cards

```svg
<!-- Pattern: Grid of coloured cards for issues/priorities -->
<!-- Each card: number circle + title + bullet points -->
<!-- Colour coding: red=critical, amber=warning, green=opportunity, blue=info -->
<!-- Bottom section: action items or questions -->
```

---

## 4. HTML TEMPLATE STANDARDS

### 4.1 Slide Template (Landscape A4)

```html
<div class="slide">
  <h1>Title — Subtitle Context</h1>
  <div class="subtitle">One-line description of what this slide shows</div>
  <div class="row">
    <div class="col-main">  <!-- SVG or image, flex:2-3 -->
      <svg>...</svg> or <img src="data:image/png;base64,..."/>
    </div>
    <div class="col-side">  <!-- Text panels, flex:1 -->
      <div class="box box-blue"><h3>Key Numbers</h3>...</div>
      <div class="box box-amber"><h3>Warning</h3>...</div>
    </div>
  </div>
  <div class="footer"><span>Organ name</span><span>Slide context</span></div>
</div>
```

### 4.2 Dossier Template (Portrait A4)

```html
<h2>Section Title</h2>
<p>Narrative text in publication voice (per aaa-pdf-voice-protocol)</p>
<div class="pullquote">Key insight in italic with blue left border</div>
<div class="issue-box"><strong>THE REAL ISSUE:</strong> Description</div>
<table><!-- Data tables with alternating row colours --></table>
```

### 4.3 CSS Constants

```css
/* Colours */
--basin-green: #1b4332;
--accent-green: #2d6a4f;
--text-dark: #0d1b2a;
--evidence-obs: #28a745;
--evidence-der: #007bff;
--evidence-int: #ffc107;
--evidence-spec: #dc3545;
--box-blue: #2980b9;
--box-amber: #e67e22;
--box-red: #c0392b;
--box-green: #27ae60;

/* Typography */
body: 'Segoe UI', Arial, sans-serif; 10.5pt;
h1: 22-28pt, #0d1b2a, border-bottom: 4px solid #1b4332;
h2: 14-16pt, #1b4332;
h3: 12-13pt, #2d6a4f;

/* Page */
@page { size: A4 landscape; margin: 1cm; }  /* slides */
@page { size: A4 portrait; margin: 2cm; }   /* dossiers */
```

---

## 5. IMAGE EMBEDDING

### 5.1 Real Images (Cross-Sections, Well Data, Maps)

```python
import base64
def b64img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Embed in HTML:
img_html = f'<img src="data:image/png;base64,{b64img(path)}"/>'
```

**Convention:** Images > 500KB should be resized before embedding. Target: < 300KB per image for PDF < 5MB total.

### 5.2 Image Discovery

```bash
# Standard image locations in federation
/root/GEOX/outputs/*/           # Generated GEOX charts, maps, cross-sections
/root/.hermes/*xsection*.png    # Cross-sections from Hermes sessions
/root/arif-fazil.com/sites/*/   # Published visuals
/root/GEOX/data/geox_las/*.las  # Well data (convert to chart first)
/root/WEALTH/outputs/*/         # WEALTH analysis charts, capital visualisations
/root/WELL/state/*.png          # WELL organ telemetry visualisations
/root/forge_work/artifacts/     # Previously forged artifacts (reuse/reference)
```

---

## 6. PDF CONVERSION PIPELINE

### 6.1 Method: Chrome Headless (Proven)

```bash
# Individual slide HTML → PDF
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=output.pdf \
  --print-to-pdf-no-header \
  input.html
```

### 6.2 Multi-Slide Assembly

```python
# 1. Generate individual slide HTML files
# 2. Extract <div class="slide">...</div> from each
# 3. Combine into single HTML with CSS page-break-after: always
# 4. Convert combined HTML → single PDF via Chrome headless
# 5. Verify: pdfinfo output.pdf (check page count, file size)
```

**Key lesson (2026-09-15):** Chrome headless renders SVG + base64 images correctly when each slide is a complete HTML document extracted properly. Direct f-string embedding of large base64 in combined HTML can fail — use the extraction approach.

### 6.3 Quality Gates

| Gate | Check | Action |
|------|-------|--------|
| Page count | `pdfinfo` → Pages matches expected | Fail if mismatch |
| File size | < 5MB for slides, < 10MB for dossiers | Warn if > threshold |
| Image presence | Visual spot-check or pixel count | Fail if blank slides |
| Text readability | `pdftotext` → non-empty output | Fail if no extractable text |

### 6.4 Chrome Fallback Chain

The `build_slides.py` script searches for Chrome in this order:
1. `google-chrome` (primary)
2. `google-chrome-stable`
3. `chromium`
4. `chromium-browser`

If none found → `ERR_CHROME_MISSING` with remediation hint. Install with:
```bash
apt-get install -y chromium-browser
```

### 6.5 Error Taxonomy

All errors emit structured codes for diagnostics:

| Code | Meaning | Remediation |
|------|---------|-------------|
| `NO_SLIDES` | No slide divs extracted from HTML | Check HTML has `<div class="slide">` blocks |
| `NO_HTML` | No `.html` files in slides directory | Ensure slides_dir is correct |
| `CHROME_MISSING` | No Chrome/Chromium binary in PATH | `apt install chromium-browser` |
| `PDF_EMPTY` | PDF output is 0 bytes or Chrome failed | Check Chrome stderr, HTML validity |
| `PAGE_MISMATCH` | PDF page count ≠ expected slide count | Check for blank/missing slides |
| `SIZE_EXCEEDED` | PDF exceeds size threshold | Resize images, reduce embedded data |
| `PDFINFO_MISSING` | `pdfinfo` not available for verification | `apt install poppler-utils` |
| `FILE_NOT_FOUND` | Delivery script: PDF file missing | Check file path |
| `ENV_MISSING` | Delivery script: `.hermes/.env` not found | Ensure Hermes is configured |
| `ENV_VAR_MISSING` | Delivery script: required env var empty | Check `.hermes/.env` contents |
| `TELEGRAM_API` | Telegram Bot API returned error | Check bot token, chat ID, file size |

---

## 7. DELIVERY CHANNELS

### 7.1 Telegram (Primary for Arif)

```bash
source /root/.hermes/.env
curl -s -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendDocument" \
  -F "chat_id=${HERMES_SESSION_CHAT_ID}" \
  -F "document=@/path/to/output.pdf" \
  -F "caption=<description with emoji and bullet points>"
```

### 7.2 File System (Archive)

```bash
/root/forge_work/artifacts/     # Canonical artifact archive
/root/.qwen/tmp/                # Session-scoped temporary artifacts
```

### 7.3 Web (Public — if authorized)

```bash
/root/arif-fazil.com/sites/arif-fazil.com/public/   # Published artifacts
```

---

## 8. CONSTITUTIONAL BINDING

| Floor | Application |
|-------|-------------|
| **F1 AMANAH** | Artifact hash computed before delivery. Original source files never modified. |
| **F2 TRUTH** | Every claim in the artifact carries its OBS/DER/INT/SPEC rank from the source. Voice protocol translates tags to publication language. |
| **F4 CLARITY** | Visual hierarchy serves understanding. No raw code, function names, or governance plumbing visible. |
| **F6 MARUAH** | Personal/sensitive data handled with dignity. No unnecessary exposure. |
| **F11 AUDIT** | Delivery receipt logged. Source file SHA-256s referenced. |

**Voice Protocol binding:** ALL text in the artifact MUST pass through `aaa-pdf-voice-protocol` translation. Internal vocabulary (`[OBS]`, `F1`, `Kill Matrix`, `PASS/FAIL`) NEVER appears in the rendered artifact. See: `/root/AAA/skills/aaa-pdf-voice-protocol/SKILL.md`.

---

## 9. ANTI-PATTERNS

| Anti-Pattern | Why Wrong | Remedy |
|-------------|-----------|--------|
| ❌ Dump tables without narrative | Machine-readable ≠ human-readable | Wrap tables in storyline text |
| ❌ Raw function names in captions | Breaks immersion, confuses non-technical readers | Voice protocol translation |
| ❌ Images without alt text or context | Image alone doesn't explain what it shows | Always include caption + context |
| ❌ SVG without viewBox | Breaks on different page sizes | Always set viewBox explicitly |
| ❌ Single massive HTML file | Chrome can choke on >2MB HTML | Split into individual slides, combine with page breaks |
| ❌ Base64 images > 1MB each | PDF becomes unwieldy | Resize images before embedding |
| ❌ No page count verification | Blank pages or missing slides go unnoticed | Always `pdfinfo` after conversion |
| ❌ Skip delivery confirmation | Artifact may fail to send | Check Telegram API response |

---

## 10. QUICK REFERENCE — DECISION TREE

```
ARTIFACT REQUEST ARRIVES
    │
    ├── What type?
    │   ├── Dossier (narrative report) → portrait A4, prose-heavy
    │   ├── Slide Pack (visual brief) → landscape A4, SVG + images
    │   ├── Knowledge Graph → SVG nodes/edges + narrative
    │   ├── Reality Graph → evidence table + epistemic map
    │   └── Executive Summary → 1-2 pages, decision-focused
    │
    ├── What content sources?
    │   ├── GEOX OKF → basin data, stratigraphy, prospects
    │   ├── WEALTH → capital analysis, falsification framework
    │   ├── Literature review → papers, DOIs, citations
    │   ├── Well data → LAS files, checkshots, velocity models
    │   └── Cross-sections → SRTM, seismic interpretations
    │
    ├── What visuals needed?
    │   ├── Tectonic timeline → SVG pattern §3.1
    │   ├── Cross-section schematic → SVG pattern §3.2
    │   ├── Phase architecture → SVG pattern §3.3
    │   ├── Cooling/trajectory path → SVG pattern §3.4
    │   ├── Entity relationship → SVG pattern §3.5
    │   └── Issue/priority cards → SVG pattern §3.6
    │
    └── Delivery?
        ├── Telegram (Arif) → §7.1
        ├── File archive → §7.2
        └── Web publish → §7.3 (requires F13 authorization)
```

---

## 11. PROVEN PIPELINE (2026-09-15 Session)

This skill was forged during the Kinabalu Basin visual pack session:

1. **144+ internal artifacts** across 6 organs (GEOX, WEALTH, AAA, arifOS, VAULT999, Hermes) compiled
2. **45+ peer-reviewed papers** cross-validated against internal intelligence
3. **12 SVG diagrams** generated inline (tectonic timeline, two-oceanics schematic, NSPW architecture, cooling path, stratigraphic column, issue cards, priority ladder)
4. **3 real images** embedded as base64 (cross-sections, well data chart)
5. **12 landscape A4 slides** assembled as individual HTML → combined with page breaks → Chrome headless → PDF
6. **3 PDFs delivered** to Arif via Telegram Bot API (dossier, geologist briefing, visual pack)

**Key eureka:** Individual slide HTML files with proper extraction + page-break assembly renders correctly. Direct f-string embedding of large base64 in combined HTML can fail silently.

---

## 12. SKILL RELATIONSHIPS

```
aaa-pdf-voice-protocol          ← THIS SKILL READS (translation rules)
forge-document-intelligence      ← PARALLEL (INPUT direction, not dependency)
forge-visual-qa-w3              ← THIS SKILL CALLS (visual QA before delivery)
forge-design-intelligence       ← THIS SKILL READS (design tokens, colour palettes)
forge-tailwind-tokens           ← OPTIONAL (if web-publishing)
aaa-ocr-optical-compression    ← NOT DEPENDENT (that's input, this is output)
reality-loop-operator           ← THIS SKILL USES (7-stage loop for complex artifacts)
arifFlow                        ← THIS SKILL EMITS TO (FlowReceipt per forge step)
geox_claim                      ← THIS SKILL PULLS FROM (Reality Graph data)
forge-repo-intelligence         ← THIS SKILL READS (repo metadata for dossier context)
```

---

*Forged: 2026-09-15 by FI-003 (Qwen Code) for F13 SOVEREIGN*
*Session: Kinabalu Basin tectonic intelligence compilation*
*Gap filled: Missing OUTPUT direction of AAA document intelligence*
*Apex-zen: 2026-09-15 by FI-008 (Kimi Code) — reality graph, arifFlow, skill mesh wired*
*DITEMPA BUKAN DIBERI — The artifact is the forge's proof.*

---

## 13. REALITY GRAPH PIPELINE — GEOX Claim Engine Integration

Reality Graphs are the **evidence + epistemic map** artifact type. They visualise the state of knowledge — what's measured, derived, interpreted, and hypothesised — using the GEOX claim engine as the data source.

### 13.1 Data Source: GEOX Claims

```python
# Pull all claims for a basin/topic from GEOX
claims = mcp__geox__geox_claim(mode="scan", query="Malay Basin prospectivity")

# Each claim has:
#   claim_id, claim_text, claim_type, truth_class (OBS/DER/INT/SPEC),
#   uncertainty_p10/p50/p90, evidence_ids, provenance, alternatives
```

### 13.2 Reality Graph SVG Pattern

```svg
<!-- Pattern: Epistemic map with layered confidence rings -->
<svg viewBox="0 0 1000 600">
  <!-- Central claim node (rounded rect) -->
  <!-- Evidence nodes radiating outward, colour-coded by truth class -->
  <!--   green = Measured Ground Truth (OBS) -->
  <!--   blue  = Derived Geometry (DER) -->
  <!--   amber = Geological Interpretation (INT) -->
  <!--   red   = Hypothesised Extent (SPEC) -->
  <!-- Confidence rings as dashed circles (P10/P50/P90) -->
  <!-- Challenge/alternative links as dashed red lines -->
  <!-- Source citation badges on each evidence node -->
</svg>
```

### 13.3 Claim Table Rendering

```html
<!-- Each claim renders as a row with epistemic badge + uncertainty bar -->
<tr>
  <td><span class="badge badge-obs">Measured</span></td>
  <td>Seismic reflection at 3.2s TWT confirms top Jurassic</td>
  <td>
    <div class="uncertainty-bar">
      <span class="p10" style="width:30%">2.8s</span>
      <span class="p50" style="width:40%">3.2s</span>
      <span class="p90" style="width:30%">3.6s</span>
    </div>
  </td>
  <td>Madon (2021)</td>
</tr>
```

### 13.4 Reality Graph Decision Tree

```
REALITY GRAPH REQUEST
    │
    ├── What scope?
    │   ├── Single basin → geox_claim(mode="scan", query="<basin>")
    │   ├── Single prospect → geox_claim(mode="validate", claim_id="<id>")
    │   └── Cross-basin → geox_claim(mode="scan", scope="all")
    │
    ├── What epistemic depth?
    │   ├── OBS only → measured data map (high confidence)
    │   ├── OBS+DER → computed surfaces + data
    │   ├── OBS+DER+INT → full interpretation map
    │   └── All classes → epistemic risk map (includes SPEC)
    │
    └── Render?
        ├── SVG diagram → §3.5 Knowledge Graph pattern
        ├── Claim table → §13.3 above
        └── Combined → Dossier with narrative + SVG + table
```

---

## 14. ARIFLOW METABOLIC INTEGRATION

Every artifact forge MUST emit a `FlowReceipt` to the arifFlow metabolic ledger. This is how the Flow Quotient (FQ = verify/execute ratio) tracks whether the federation is producing artifacts without verification.

### 14.1 When to Emit

| Step | step_type | epistemic_label | Why |
|------|-----------|-----------------|-----|
| Start encoding content manifest | `Execute` | `Derivation` | Beginning of forge work |
| SVG diagram generated | `Execute` | `Interpretation` | Visual intelligence produced |
| Voice protocol applied | `Verify` | `Specification` | Translation layer verified |
| PDF converted | `Execute` | `Derivation` | Artifact rendered |
| PDF verified (page count, size) | `Verify` | `Observation` | Quality gate passed |
| Visual QA tri-witness | `Verify` | `Seal` | Independent review complete |
| Delivered to human | `Seal` | `Seal` | Artifact reaches human |

### 14.2 FlowReceipt Pattern

```python
from mcp__arifFlow__flow_ingest import flow_ingest

# After PDF verification passes:
flow_ingest(
    actor_id="fi-008",  # or whichever agent forged
    session_id="<current_session>",
    step_type="Verify",
    step_number=5,
    epistemic_label="Observation",
    floor_verdict="Pass",
    cost_ns=elapsed_ns,
    witness_organs=["aforge", "geox"],
    payload={
        "artifact_type": "slide_pack",
        "pdf_path": output_pdf,
        "page_count": page_count,
        "size_bytes": file_size,
        "delivery_channel": "telegram"
    }
)
```

### 14.3 FQ Impact

- **Execute steps** (encoding, rendering, delivery) increase the execute counter
- **Verify steps** (QA, page count, voice protocol check) increase the verify counter
- **Target FQ**: ≥0.5 (every execute has at least half a verify)
- **Red flag**: FQ < 0.3 = forging without verifying = quality risk

---

## 15. SKILL MESH WIRING MAP

This skill is wired across the federation mesh. Every surface is a discovery path for any agent.

### 15.1 Cross-References

| This Skill | Direction | Related Skill | Wire Type |
|---|---|---|---|
| forge-artifact-publisher | ← reads | `aaa-pdf-voice-protocol` | Voice translation rules |
| forge-artifact-publisher | ← reads | `forge-design-intelligence` | Design tokens, colour palettes |
| forge-artifact-publisher | ← reads | `forge-tailwind-tokens` | CSS design system (web publish) |
| forge-artifact-publisher | → calls | `forge-visual-qa-w3` | Visual QA tri-witness before delivery |
| forge-artifact-publisher | → calls | `arifFlow` (flow_ingest) | FlowReceipt emission per step |
| forge-artifact-publisher | → pulls | `geox_claim` | Reality Graph data from GEOX claims |
| forge-artifact-publisher | → pulls | `forge-repo-intelligence` | Repo metadata for dossier context |
| forge-artifact-publisher | → uses | `reality-loop-operator` | 7-stage loop for complex multi-slide artifacts |
| forge-artifact-publisher | → parallel | `forge-document-intelligence` | INPUT direction (not dependency) |
| forge-artifact-publisher | → writes | VAULT999 (via receipt) | Delivery receipt logged |

### 15.2 Registration Surfaces

| Surface | Registry | ID/Key | Status |
|---|---|---|---|
| AAA filesystem | `/root/AAA/skills/forge-artifact-publisher/` | directory | ✅ Present |
| AAA federated registry | `FEDERATED_SKILLS_REGISTRY_V3.yaml` | `forge-artifact-publisher` | ✅ Registered |
| AAA alias table | `SKILL_ALIAS_TABLE.json` | `forge-artifact-publisher` | ✅ Registered |
| Hermes registry | `/root/.hermes/registry/skills.yaml` | `governance-audit.execute.forge-artifact-publisher` | ✅ Active |
| Kimi Code | Session cache | transient | ⚠️ No persistent user-scope copy |
| arifFlow | `flow_ingest` receipts | per-artifact | ✅ Wired (this session) |

### 15.3 Trigger Routing

Any agent in the federation should load this skill when:
- User says: "make a PDF", "visual pack", "slide deck", "dossier", "forge artifact", "publish to telegram", "send report"
- Task involves: rendering structured intelligence into human-readable visual format
- Reality loop reaches SEAL stage with visual output needed
- GEOX claim scan produces results that need epistemic mapping
