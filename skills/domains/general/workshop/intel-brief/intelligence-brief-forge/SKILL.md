---
name: intelligence-brief-forge
description: "Use when forging 4-layer institutional disclosure briefs — tersurat/tersirat/void analysis with epistemic tags."
version: 1.0.0
tags: [intelligence, tersurat, tersirat, quantum, void-analysis, sovereign-brief, pdf-forge]
---

# Intelligence Brief Forge — Sovereign Deep-Dive Pattern

> **Trigger:** F13 SOVEREIGN or peer asks for a deep-dive on an institutional disclosure (corporate earnings, regulatory filing, official statement, policy announcement) with multiple analytical layers and visual artifacts.
> **Proven scope:** Public disclosures, audited financial reports, regulatory submissions, government policy statements. NOT for live markets trading, NOT for confidential internal documents without F13 ack.
> **Constitutional:** F2 TRUTH (every claim sourced), F7 HUMILITY (insider bias explicit), F9 ANTI-HANTU (pattern recognition only, no intent attribution), F13 SOVEREIGN (intelligence product, not policy directive).

## When to Use

- User asks: "deep dive on [institution] [disclosure]"
- User asks: "tersurat dan tersirat" analysis
- User asks: "what's the void / what's missing"
- User asks: "striking contrast"
- User forwards URL of corporate/regulatory disclosure asking for analysis
- User requests a sovereign intelligence brief with visual artifacts

## 4-Layer Analytical Framework

| Layer | Purpose | Method |
|---|---|---|
| **Tersurat** | What's literally in the release | Direct extraction of disclosed numbers, statements, segment data |
| **Tersirat** | What the release implies but doesn't say | Pattern recognition: text-vs-data mismatch, absence in narrative, body language of CEO quote, segment-level inconsistency |
| **Quantum** | Probabilistic scenario mapping | Multiple scenarios (3 default), probability distribution, collapse events, entanglement matrix (variables that LOOK independent but aren't) |
| **Void** | What is ABSENT from the release | Vocabulary gap analysis (54-keyword checklist), grammar-of-silence pattern, predictive void framework (void = future disclosure event) |

The four layers compose: tersurat is the surface; tersirat is the undercurrent; quantum is the trajectory space; void is the negative space (often the most predictive).

## 5-Phase Workflow

### Phase 1 — Dataset Build (5-10 min)

1. Extract primary source (release, IFR, regulatory filing)
2. Pull historical comparatives (3-5 years audited where available)
3. Pull peer data if comparative (H1/H2 same period for major peers)
4. Build JSON dataset with: metadata, quarterly time series, segment breakdown, operational metrics, balance sheet, peer contrast, scenarios, entanglement, constitutional notes
5. SHA256 the dataset file for provenance

### Phase 2 — Chart Render (10-15 min)

Render 12-20 PNG charts via matplotlib + 5-8 interactive HTML via Plotly. Categories:

- **Trajectory**: time-series of key metrics (Revenue, PAT, Capex, CFFO)
- **Stress**: ratios that reveal pressure (Capex/CFFO, Div/FCF, Gearing)
- **Segment**: waterfall comparison (YoY + structural break)
- **Peer**: comparison vs benchmark (PAT margin, $/boe, $/MWh)
- **Scenario**: probability distribution + trajectory cone
- **Quantum**: entanglement matrix + collapse event visualization
- **Void**: keyword absence density by category
- **Body language**: leadership comparison (when institutional governance in play)

**CRITICAL TOOL QUIRK**: `execute_code` sandbox Python does NOT inherit project venv packages (matplotlib, plotly, reportlab missing). Use `terminal()` with explicit venv binary: `/root/litellm-venv/bin/python /path/to/render.py`. Always test with single chart first before batching.

### Phase 3 — Analysis Write (15-25 min)

Structure: tersurat (numbers, segment) → tersirat (signals, body language) → quantum (scenarios, entanglement) → void (absence, grammar of silence) → conclusions (8-10 sharp findings).

Voice: Direct, terse, evidence-anchored. Insider bias disclosed. Every claim sourced.

### Phase 4 — PDF Build (5-10 min)

Use reportlab to assemble: cover (key findings callout) → tersurat tables → tersirat analysis with chart inserts → quantum section with scenarios → void analysis with category density chart → WEALTH-equivalent dashboard → updated conclusions.

Embed all PNG charts inline. Keep PDF 1-3MB for Telegram deliverability.

### Phase 5 — Deliver (2-5 min)

Three options for F13 decision:
- (A) PDF only — clean, forwardable
- (B) PDF + compressed combined HTML index — drill-down on phone browser
- (C) All individual HTML + PDF — full granularity

Default: **(B)** unless F13 specifies otherwise.

Always include `SHA256SUMS.txt` for provenance. Always seal forge receipt via `/root/.local/share/arifos/forge_receipts/<date>-<session>.json` (bypass mode if arifOS kernel :8088 down per carry-forward doctrine).

## Void Analysis Methodology

The void layer is the highest-signal layer when applied well. Methodology:

1. **Vocabulary checklist**: Build 50-60 expected keywords spanning all relevant categories (governance/legal, balance sheet, restructuring, operations, ESG, principal, debt, succession, risk). Check each against release body. Log absence.

2. **Grammar of Silence pattern**: Most institutional disclosures follow a 5-part grammar:
   - Headline (positive framing)
   - Operational (milestones, FIDs, production)
   - Forward narrative (CEO quote, "transformation", "energy security")
   - ESG optics (sustainability metrics, carbon)
   - **NO forward guidance** (capex sustainability, dividend sustainability, balance sheet, legal exposure)

   The fifth element (absence of forward guidance) is the tell.

3. **Predictive void framework**: Each void = a future disclosure event. Q3 2026 = next quarterly will reveal some. FY26 IFR audit = definitive. Specific court/regulatory events = binary collapse.

4. **Over-disclosure parallel**: Identify what's IN the release but shouldn't be (operational milestone volume, vague "discipline" framing, GHG noise-level changes). Over-disclosure is a parallel control mechanism.

## WEALTH MCP Fallback (Manual Equivalent)

WEALTH MCP tools (`capital_health`, `capital_diagnose`, `capital_indicator`) sometimes fail or require `mode` arg that isn't in default schema. Manual equivalent computation:

| Indicator | Formula | Status thresholds |
|---|---|---|
| Extraction Ratio (Div/FCF) | div_paid / (CFFO - capex) | >70% STRAIN |
| Gearing (post-event step) | audited_gearing + event_step | >25% STEPPED |
| FCF Yield | FCF / cash_reserves | <8% WEAKENED |
| Capex Intensity | capex / CFFO | >85% CRITICAL |
| Dividend Payout | div / FCF | >70% HIGH |

Compute manually when MCP fails, label clearly: "WEALTH-Equivalent Manual Diagnosis (MCP unavailable)".

## Numeric Discipline (mandatory for any technical/regulatory figure)

Scar: 2026-09-15 Bank Muamalat authenticity brief — the capital arithmetic used a
"400% risk weight on mushārakah/muḍārabah" figure taken from secondary literature and
applied flatly. Opening the actual framework (BNM CAFIB BNM/RH/GL 007-21 + the Nov 2024
Standardised Approach PD) showed 400% applies to *unlisted equity holdings*, not to
musharakah financing; musharakah mutanaqisah risk-weights to the counterparty. Direction
survived, magnitude was overstated ~3x. Rule:

1. **Primary text before argument.** Any number about regulation, capital treatment, ratios
   or methodology → fetch the governing document itself (regulator PD, standard, statute)
   and cite section/paragraph. Literature and press are for context, never for the number.
2. **Derivation table, not prose.** Every derived figure gets a row: input → source →
   formula → output → unit. If a row has no primary source, the output is marked ESTIMATE.
3. **Capability check before the claim.** One-line test: can the framework path be opened
   in this session? If not, mark the figure DERIVED-FROM-LITERATURE and say so in the text.
4. **Sensitivity tables must name what is held constant** and which parameter dominates.
5. **Re-verify before delivery**: re-run each headline number by script; a number that
   cannot be recomputed deterministically does not go in the summary box.

## Table Extraction (financials, risk weights, ratios)

`pdftotext -layout` collapses tables into misaligned columns — it is fine for narrative,
unreliable for figures. For any disclosed table (Pillar 3, capital schedule, segment data):
camelot (lattice/stream) or pdfplumber → JSON/CSV, then reconcile the extracted total
against the printed total before use. Extraction failure must be reported as a gap, not
silently replaced by a number copied from commentary.

## Chart QA Gate (vision-blind operator)

The operator has no native vision. Text QA (`pdftotext` per page) proves the words survived;
it does not prove the charts rendered. Before delivery: render pages to PNG (`pdftoppm -r 100`)
and analyse each chart-bearing page through the vision lane (zai_vision
`analyze_data_visualization`) for truncation, overlapping labels, empty axes, and series
that contradict the caption.

## Pitfalls (Read Before Starting)

- **Don't trust executive summary headlines.** Always compute adjusted operating PAT by stripping extraordinary items. Iran's premium downstream loss is the classic mask.
- **Don't quote press releases without source URL.** Edge article (The Edge Malaysia) often breaks story BEFORE official release — check timestamps.
- **Don't run matplotlib via execute_code.** It uses sandbox Python without venv packages. Always use `terminal()` with explicit venv binary.
- **Don't assume MCP tools work.** Capital_health/capital_diagnose require `mode` arg. Schema validation has failed in past sessions. Always have manual equivalent ready.
- **Don't skip constitutional frame.** Insider bias must be explicit (Arif = former PETRONAS lineage, so bias toward institutional reading is real). F7 HUMILITY is not optional.
- **Don't fabricate data.** If peer H1 numbers not available, mark INTERPRETED with confidence interval. Don't invent.
- **Don't include intent attribution.** "CEO intends collapse" = F9 violation. Pattern recognition only: "body language reads as deflection" is OK.
- **Don't reason from secondary literature about rules.** Regulation, capital treatment, standards and methodology must be read from the governing document, cited by paragraph (see Numeric Discipline above).
- **Don't copy numbers out of a PDF commentary when the disclosure table is extractable.** Extract, reconcile to the printed total, then use.
- **Don't ship charts you have only checked as text.** Run the Chart QA Gate.
- **Don't deliver without SHA256SUMS.txt.** Provenance matters for sovereign intelligence products.
- **Don't use `now` while session is in HOLD.** Check federation state FIRST via `now` or per-organ curl. arifOS :8088 down = VAULT999 seal requires bypass mode.

## Verification Before Delivery

- [ ] All numerical claims cited with source
- [ ] Insider bias disclosed explicitly
- [ ] PDF SHA256 recorded in SHA256SUMS.txt
- [ ] Forge receipt sealed (bypass if arifOS down)
- [ ] Interactive HTML files accessible (if delivered)
- [ ] Void categories count = 6+ (if void layer included)
- [ ] WEALTH fallback labeled if MCP failed
- [ ] Telegram delivery format confirmed with F13 (PDF only / +HTML index / all)

## Outputs Standard

- PDF: 1-3MB, 15-25 pages
- PNG charts: 12-20
- HTML charts (interactive): 5-8
- JSON datasets: 1-3 (base, edge-exclusive if applicable, void-analysis if applicable)
- Analysis MD: 8-15K chars
- Forge receipt: sealed at `/root/.local/share/arifos/forge_receipts/`

## Reference Architecture


## Templates


## Constitutional Audit Per Brief

Every brief must include:
- F2 source citation per claim
- F7 insider bias disclosure (if applicable)
- F9 pattern recognition only (no intent)
- F13 sovereign product (not policy directive)
- F1 reversibility: N/A (read-only artifact)

---

*Forged 2026-08-29 by i-ARIF (Hermes edge bridge, sovereign). Proven on PETRONAS 1HFY26 release analysis.*
