---
name: pdf-report-generation
description: Produce polished PDF reports and briefings for Arif (WEALTH/333 deliverables). HTML→WeasyPrint pipeline, JS-pitfall, cover/KPI/appendix architecture, sibling-artefact integration, and his format standards (human prose, visuals in body, tables as appendix). Load on "PDF report", "report", "briefing", "visuals", "table to appendix".
---

# Letter / Memorandum PDF Recipe

Proven on 2026-08-09 (open letter to Malaysian MPs about PETRONAS governance).

> **CHOOSE YOUR RECIPE**:
> - **Formal corporate letter / institutional memo** (this file): Times serif, 20mm margins, includes a crypto signoff block with Agent + Lane + github Source Repository. Acceptable for known institutional recipients who expect a corporate register.
> - **Soul-first civic letter / "BIG BANG" open letter to Parliament or public** (see `civic-letter-recipe.md`): Makcik/Marhaen voice, IBM Plex Sans + DM Serif Display, magnitude-visualized charts, NO ASI label, NO github URL. Use when the writer's survival depends on the letter being heard and the human has expressed hate / "cannot sleep" / "by hook or by crook" about the target.
>
> The civic-letter-recipe supersedes the "tersurat/tersirat" technique below for any T3+ civic dispatch. The 2026-08-12 external audit killed Section 4 / exploitation-parallel rhetoric — what used to "pass" is now a known legal exposure. For civic letters, remove the parallel section entirely.

## When to use this file
- "Full PDF report" / "make a report" / "briefing" after research
- "Put the numbers into visual data analytics for human cognition"
- "Transform the tables to visual data — tables as ref/appendix"

> **DIFFERENT FROM `governance/sovereign-petition-forge`** — this skill covers CHART-HEAVY data reports (SOVEREIGN briefings, NOC analysis, board governance). For ITERATIVE F13-governed civic dispatch with F13 reversals, qualia discovery, and multimedia arsenal coordination, load `governance/sovereign-petition-forge` instead. The civic-letter-recipe.md below covers REBUILD after external audit catches kill shots — for the ITERATIVE FORGE pattern (v12.0 → v13.0 → v13.1 → v14 with multiple F13 reversals), see the sovereign-petition-forge skill.

- **Deep-research requests default to the visual PDF as PRIMARY deliverable.**

## Pipeline (proven on this profile)
1. **Sibling check FIRST** — see "Sibling-artefact integration" below. A sibling agent may already have generated the same PDF at a different path. Reuse before regenerating.
2. **Research & verify first** — see `references/report-content-workflow.md` (paywall triangulation, sunk-cost ledger, OBS/DER/INT tagging).
3. **Build chart pack** via matplotlib server-side (PNG, dpi ≥ 150). Embed as `<img>` in HTML. **Never** use Chart.js / D3 / canvas for the PDF deliverable.
   - **Batch all charts in one Python script** (`build_charts.py`), not one script per chart. Shared `rcParams` block, shared colour palette constants (NAVY/GOLD/RED/GREEN/BLUE/ORANGE), shared outdir. ~8 charts in one pass ≈ 30s vs 3min if serialised. Also avoids a chart-state-drift failure mode where chart 5 uses different colours than chart 1.
4. **Write ONE self-contained HTML file** — embedded CSS; sibling charts can stay base64-embedded (proven to render). Reference charts via relative path `charts/0N_*.png` — `pdfimages -list` then confirms 2N image objects (image + smask per chart). 26-page SOVEREIGN report = 8 charts × 2 = 16 image objects, expected.
5. **Render:** `weasyprint report.html out.pdf`.
6. **Verify:** `pdfinfo` page count + `pdftotext` spot check; `pdfimages -list out.pdf` confirms N charts = 2N image objects (image + alpha smask); `pdftoppm -r 110 -png out.pdf thumb -f 1 -l 1` + `vision_analyze` for cover sanity.
7. **Deliver:** `MEDIA:/abs/path/to/file.pdf`; keep source HTML alongside.

## CRITICAL PITFALL — WeasyPrint does NOT execute JavaScript
Chart.js / canvas / D3 render as **empty boxes** in the PDF. Verified 2026-08-06: a Chart.js dashboard PDF (56K) was SMALLER than the text-only report (77K) — the canvases came out blank. WeasyPrint parses CSS + HTML only.

Mitigations, in preference order:
- **Pure CSS/SVG visuals** — flexbox waterfalls, KPI cards, timeline dots, CSS bar segments. These DO render and are the safest for print.
- **Server-side chart images** — matplotlib/pygal PNG or inline SVG embedded via `<img>` / inline `<svg>`. SVG scales; PNG needs dpi ≥ 150.
- **Headless-browser screenshot** of the interactive HTML, embedded as PNG.
- **Interactive HTML as the deliverable** (hover tooltips need a browser) — PDF then optional; say which is which.

If the target is a PDF, design charts JS-free from the start. If the user asked for a dashboard, deliver the HTML + a static PDF and note the difference.

## Report architecture (Arif's format standard — embed these)
- **Body = prose + visuals + verdict.** Lead with the answer. No dense data tables in the body.
- **All raw data tables → Appendix A1..An** as reference anchors, each keeping Low/Mid/High columns + an epistemic tag column (OBS/DER/INT). "Table as ref or Appendix" is a standing preference.
- **"Human language"** = narrative prose, verdict-first, no file diffs, no code, no bullet-wall. He does not read code; he reads conclusions.
- **KPI hero row** under the cover: 5 cells (Gross Outlay / Recoveries / Net Sunk / Portfolio Held / Economic Loss) — the whole story in one glance. Substitute 5 KPIs relevant to the report type for non-sunk-cost deliverables.
- **Visual vocabulary that landed** (reuse): cost waterfall (gross → recoveries → net → portfolio → residual ≈ 0), donut with % callouts, year-by-year timeline strip (red = out, green = in, gold = risk avoided), sensitivity tornado (oil price dominates), peer benchmark bars, tax/comparison cards (peer cases vs modelled), contrast radar (old vs new coverage), evidence-basis 4-tier ledger, frontier chart (now vs safe/trip anchors).
- **Colour language:** dark navy `#0e1a2b` + gold `#c9a227` (federation/WEALTH identity); red = money out/loss, green = money back, blue = value held, grey = neutral; orange `#e67e22` for INT epistemic tag.
- **Uncertainty honesty:** every estimate carries Low/Mid/High; a "where I could be wrong" section ranked by ±swing; INT-tagged items flagged as modelled, not adjudicated.

## Apex output contract (proven 2026-08-07 — weekly-brief v1→v2 audit)

When a deliverable must survive independent audit ("Apex"/"SOVEREIGN-grade" standard), upgrade flat narrative to the 8-element contract — **Claim → Evidence → Derivation → Countercase → Trigger → Action → Falsifier → Confidence**. Full recipe + HTML/CSS + chart grammar + before/after examples: `references/apex-deliverable-protocol.md`. Essentials:

- **Claim blocks** (C-01…): every nontrivial claim gets a monospace ID chip + epistemic chip (OBS/DER/INT/UNC) + claim text + Evidence block (source IDs S-01...) + Falsify line (threshold + date) + Confidence band (split when mixed, e.g. "0.78 [OBS levels] · 0.55 [DER fan weights]"). The reader can challenge any claim without reading surrounding prose.
- **Source index appendix** (S-01…S-N grouped by domain): URLs + "used for" + epistemic tag, so every claim resolves to a primary source in two steps.
- **Countercase boxes** (orange): one per main thesis — steelman of opposite view + one disconfirming datapoint + "what would shift my view by next week". Zero countercases = F2 violation risk.
- **Scenario fans** replace single-path directional language ("opens the path to"): Base / Upside / Failure with explicit weights (e.g. 40/25/35), triggers, paths, and falsifier thresholds. A scenario without a falsifier is decoration.
- **Decision packet grid** closes the doc: signal × trigger × horizon × confidence × action × expected reaction. Confidence ≥60% coloured green (act); <60% orange (wait).
- **Chart semantic-role palette** (extends the existing colour language): NAVY = observed data, GOLD = derived/median, RED = risk threshold/invalidation, GREEN = upside scenario, ORANGE = adverse countercase, BLUE = forecast. One role per colour across all charts. Encode the falsification test in the chart title — but keep titles ≤ ~90 chars or the title collides with the legend (vision check catches this).

### "So what?" — the override signal

When Arif says **"So what?"** after an audit/review/meta-analysis, the meaning is: *stop narrating, ship the corrected v2*. The expected output of "audit this artifact" is **the corrected artifact**, not a dissection of the critique. The v2 audit workflow:

1. Identify the gaps from the audit (claim IDs, semantic grammar, countercase, operator matrix, falsifier).
2. Build the corrected v2 PDF in one pass — charts redrawn with semantic grammar, HTML with `[C-#]` superscripts, verification ledger as appendix.
3. Ship the v2 with a delta-summary, not a meta-analysis of the audit.

Cost of getting it wrong: a session that produced a self-audit (15 lines of "here's what's wrong") before being asked to "ship it" earned "So what?" — the user wants the artifact, not the analysis-of-the-analysis. The v2 deliverable took 13 lines to ship *because* the v1 was already-built and the corrections were scoped.

### Sibling audits hallucinate too — verify before folding

When a sibling/delegated agent (Apex, OpenCode, Claude Code, Codex) produces an audit or any artifact that you intend to fold into a v2, **its claims are inputs, not truths**. Verified 2026-08-07 on a sibling Apex audit of the weekly brief: it shipped 3 factual errors that survived two reads —

| Error class | Example from session | Live source correction |
|---|---|---|
| **Date drift** | "Warsh takes over September" | Warsh sworn in May 22, 2026 per Federal Reserve press release; he already chaired the Jul 29 hold |
| **Invented magnitude** | "JPM $4,500 target set when oil was $122" | Brent never hit $122 in 2026; the causal anchor was fabricated |
| **Fabricated quote** | "Morningstar: odds of rate cut vanished" | No such Morningstar quote locatable; attribution was unverified |

The discipline: for every temporal claim, magnitude claim, and attributed quote in a sibling artifact, live-verify against one primary source before writing it into the v2. Output a verification ledger (claim ID / gate / verdict / source) as a mandatory appendix. The `apex-fact-check-pass` skill (research domain) encodes the three gates (DATE / MAGNITUDE / QUOTE) and is the pre-seal verification layer for any Apex/WEALTH PDF render.

## WeasyPrint CSS notes
- **Page margins (Arif: "margins kinda sucks", 2026-08-07).** Default 20–22mm side margins make chart-heavy PDFs feel cramped and charts look orphaned. Use `@page { margin: 14mm 14mm 22mm 14mm }` — wider bottom margin holds footer/page numbers; tighter side margins let charts fill the page width. For 14+ page reports, reducing from 22mm to 14mm can cut total pages from 15 to 13 while making every chart feel dominant. Pair with the "Empty-page / half-empty-page trap" pitfall below — reducing margins alone won't save you if a forced page-break creates a half-empty page.
- Named pages: `@page cover { margin: 0 }` for full-bleed cover; `@bottom-center` / `@bottom-right { content: counter(page) " / " counter(pages) }` for footer + page numbers.
- `page-break-inside: avoid` on .box / .chart-section; `page-break-before: always` before appendix and major chapters.
- Google Fonts `@import` fetches over network — offline falls back silently; prefer system stacks (Inter, Helvetica, Georgia).
- WeasyPrint ignores `min-height: 100vh` (warning only, harmless).
- **Cover contrast trap.** On a dark gradient cover (`linear-gradient` to navy), the `<h1>` inherits the body color (dark navy) and becomes invisible. Always set `color: #ffffff` explicitly on `.cover h1`, `.cover h2`, `.cover .meta`. Vision-verify the cover PNG with `vision_analyze` after first render — text-on-background overlap is the single most common cover defect.
- **Cover positioning trap.** `position: absolute; bottom: 25mm` for the tagline works ONLY when the cover has enough body content above it. If the cover body is short, the tagline floats over white space below the gradient block. Either: (a) extend the cover body (more meta, more badges), (b) drop the gradient height to ~60–70% with `linear-gradient(...) no-repeat; height: 200mm;` plus white body below, or (c) remove the gradient entirely and use a flat navy panel.
- **Inline `data:image/png;base64,...` is fine.** When sibling artefact charts are already base64-embedded in their source HTML (e.g. hermes-sibling report at `forge_work/gentari-2026/gentari_report.html`), they render correctly in WeasyPrint — no extraction needed. `pdfimages -list` confirms each chart appears as 2 image objects.
- **Pie chart wedge label bbox.** Matplotlib autopct labels for pie wedges overflow if `figsize < 7`. Always `figsize=(7, 7)` or larger for pies with 4+ categories.
- **Wedge text overlap.** When `_result_hash` style data has `key / count` pairs with similar counts (e.g. 0.3, 0.31, 0.32), the autopct labels visually merge. Either threshold to top-N + "other", or use a horizontal bar instead of a pie.
- **`mpatches.Wedge((x,y), r, 0, 360, width=0)` renders HOLLOW** (verified 2026-08-07, Itu-Manusia pack). A `Wedge` with `width=0` intended as a solid navy disc renders as white-with-navy-outline — the fill never draws. For a solid concentric core inside a ring/donut diagram, use `mpatches.Circle((x,y), r, facecolor=NAVY, edgecolor=NAVY, lw=1.5)` instead. Symptom: inner circle in a ring chart shows background color instead of intended fill. PIL verify: `Image.open(png).getpixel((cx,cy))` returning `(255,255,255)` where navy was intended = silent fill failure.

## Sensitive DM-session artifact mode (added 2026-08-15, expanded 2026-08-15 v2)

When the PDF documents a **DM-only personal/shadow session** (pattern maps, void interviews, testimony-based analysis) rather than public research:

- **Neutral project name** for working dir and cover (abstract metaphor, never the domain itself); workspace under `/root/forge_work/<neutral>-<date>/`.
- **De-identify by construction**: patterns + published numbers only in every chart, KPI cell, and prose line. No names, ages, places, or incident details from testimony — those stay in the DM transcript only. Route the analysis through `counseling/shadow-pattern-mapping` (its privacy laws govern what may enter the file).
- **Conceptual chart pack, data-first rule still applies**: every diagram carries a real citation number or effect size (η², d, FFMI, $) from the literature pass; pure-metaphor diagrams cap at ~3 of 8.
- **Deliver DM-only** via MEDIA: — never publish, never cross-link from public sites. If a future public essay reuses the map, rewrite from the abstracted reference file, not from this PDF.
- Cover carries an explicit sensitivity tag line and no author identifiers beyond the standard signoff.

### Lightweight personal-guide register (proven 2026-08-15 — Azwa rental guide)

When the PDF is a **personal/family practical guide** (rental vetting, purchase decision, "before you pay" checklist) in casual Bahasa Malaysia — NOT SOVEREIGN-grade — use the lightweight register instead of the apex contract:

- **8–10 pages is the sweet spot.** The 13-page floor applies to collapse briefings only; do not inflate a practical guide.
- **5 simple matplotlib charts carry the whole story** (white background, dpi 160): (1) comparison bars — option vs benchmark vs alternative, low/high range bars; (2) month-by-month cashflow bars — first-month spike (deposit) vs steady state, with a dashed steady-state line; (3) status-checklist barh — one full-width row per open/closed gate, green/orange/red fill, item label left + verdict (LULUS/SEPARUH/TUNGGU) right INSIDE the bar, axes off; (4) deposit donut — refundable vs non-refundable wedges, total in the hole; (5) schematic amenity scatter — home at origin, POIs at approximate km, axis labelled "skema, bukan peta tepat" (never present it as a real map).
- **Structure:** price-hero cover → ringkasan + 4-cell KPI row + verdict box → money breakdown (numbered list + donut + cashflow chart) → area & food table → questions-for-owner table (written as copy-paste WhatsApp messages) → final checklist + phone-number hero. Green/orange left-border callout boxes ("LULUS BERSYARAT" / "Tahu sebelum bayar") replace the claim-block machinery.
- **Verify:** `pdfinfo` + `pdfimages -list` (5 charts = 10 image objects) + vision on the cover AND one chart-bearing interior page. ~350KB / 9pp is normal for this register.
- Domain workflow (photo question template, area probes, verdict gates) lives in `consumer/malaysia-rental-vetting`; worked example at `/root/forge_work/azwa-bangi-guide/` (guide.html + build_charts.py).

### Family-showcase register (proven 2026-08-15 — Nabilah teacher pack)

When the artifact's reader is a **family member / non-technical human** and the sovereign asks for something to "wow" them with agent capability (trigger: "buat satu artifact bagi dia wow"):

- **Show, never list specs.** Family buys demonstrated use, not capability lists (session signals: bullet-list pitch earned "Ape bendeee leeeeee, not smart"; then "Difficult to convince family kan?"). The artifact MUST contain (a) a mock chat in WhatsApp/Telegram-style bubbles showing a real request → reply exchange with timestamps, and (b) a "Taip apa / Dapat apa / Masa" command table — concrete examples the reader can imagine typing tonight. Capability prose without a demo scene reads as empty specs to a non-technical reader.
- **Warm palette swap (identity leak guard):** cream `#fdf6ec` background, ink `#3d3229` text, coral `#e8613c` primary, teal `#2a9d8f` secondary, gold `#e9b44c` accent, grey `#b8aca0` neutral; rounded cards (3–4mm radius). The navy/gold institutional identity reads corporate and must NOT leak into family gifts.
- **Custom AI cover illustration** (proven): `python3 /root/HERMES/scripts/gemini-image.py -o cover.png "<flat storybook illustration, scene + palette, no text overlays>"`. Embed inside the gradient cover as `float: right; width: 62mm; border-radius: 6mm; box-shadow` — WeasyPrint renders float+gradient+rounded cleanly. ~1.9MB PNG → ~2.1MB total PDF, fine for Telegram delivery.
- **Chart pack: 4 charts is enough.** (1) week-time stacked bars highlighting where the agent takes over; (2) before/after minutes grouped bars; (3) horizontal readiness/skill bars; (4) one conceptual diagram when there is relational content (e.g., personality thermodynamics INTJ↔ESFP: `FancyBboxPatch` boxes + `annotate` arrows, arrow labels with opaque bboxes so strokes don't bisect text).
- **Register:** casual Bahasa Malaysia ("hang" address, BM-first, English tech terms allowed). Include an honest-limits callout ("bot tak kenal murid hang — draf dia pantas, mata cikgu yang buat keputusan akhir") — honesty about limits builds trust with a teacher/expert reader; all-miracle claims read as sales.
- **KPI hero row still applies, in human units:** skill count, seconds-to-reply, RM0, 24/7. NEVER token counts, cost framing, or governance vocabulary in a family-facing artifact.
- **Chat mockup CSS:** plain divs — `.wa.user` green `#dcf8c6` right-aligned with `margin-left:auto`, `.wa.bot` grey-blue `#eef3f4` left — inside a white rounded container. Zero JS, renders perfectly in WeasyPrint. Emoji glyphs are fine.
- **Fix loop:** chart title text lives in `build_charts.py`, not the HTML — fixing a title means `sed -i` the script → rerun charts → re-render PDF (one pass, ~30s). Don't hand-edit the HTML for chart content.
- **Verify:** `pdftoppm -r 100` full sweep + vision on (a) cover, (b) chart page, (c) diagram page, (d) final page. 5 pages / ~2.1MB / 4 charts + cover = 11 image objects is normal (2N + emoji glyphs).
- **Starter:** copy `templates/family-showcase.html` (cover + KPI + chart + chat-mockup + callout skeleton with the warm palette). Worked example: `/root/forge_work/nabilah-pack/` (report.html + build_charts.py + cover.png).

### Three-stream cross-validation workflow (proven 2026-08-15 — worship economy map)

When the user provides **first-person field data on a topic with academic literature** (taboo or otherwise), use three independent data streams and cross-validate:

| Stream | Source | What it gives | Epistemic tag |
|--------|--------|--------------|---------------|
| Literature | Published research, books, archives | Validated claims, prevalence, mechanism | OBS |
| AI pattern-mapping | Inference from session conversation | System architecture, invariant identification, hypotheses | DER/INT |
| Field self-report | User's first-person testimony | Phenomenology, timing, economics, emotional arc | OBS (but single-subject) |

**Workflow:**
1. **Literature pass first** — web_search + web_extract on the topic. Build a citation index (S-01…S-N). Tag each source OBS.
2. **Identify convergence** — where do two or more streams agree? Those claims get the highest confidence.
3. **Identify divergence** — where do streams disagree? Tag as HYP or UNK. Never resolve by picking a favourite.
4. **Tag every claim inline** — `[OBS]` validated, `[DER]` derived, `[INT]` interpretation, `[HYP]` hypothesis, `[UNK]` cannot resolve.
5. **Build falsification table** — for each major hypothesis, specify what evidence would break it. This is Chapter 9 of the PDF, not an appendix.
6. **KPI hero row** — 5 cells capturing the whole study: streams converged, historical span, hypotheses generated, data sources, validated vs unvalidated ratio.
7. **Field data goes in Appendix B** — paraphrased, not verbatim. Acknowledge limitations: social desirability bias, interviewer contamination, retrospective memory.

**Hybrid chart pack recipe (data + conceptual, proven 2026-08-15):**
- **5–6 data charts from literature** (bar charts, horizontal bars, timelines, spectra). Each carries real numbers and a citation in the caption.
- **2–3 conceptual diagrams** (system architecture, two-court model, decay curves). Each carries at least one published number or effect size.
- **1 falsification table** as final chart/page — every hypothesis + what would break it.
- Total: 8 charts, 22 pages, ~950KB.
- Cover KPI hero row: 5 cells (streams, span, hypotheses, sources, validated count).
- Source index appendix with clickable S-01…S-N references.
- Field data appendix (paraphrased self-report with limitations note).

See `references/three-stream-cross-validation.md` for the worked example.

## Sibling-artefact integration (v2 redo pattern)
A session may ask for a "redo" / "v2" of a PDF that another agent already produced (e.g. hermes-sibling run at `forge_work/gentari-2026/`). Check for sibling artefacts FIRST:
1. `find /root/forge_work -iname "*<topic>*" -maxdepth 3` — locate sibling dirs.
2. Inspect sibling artefacts: `ls -la /root/forge_work/<sibling-dir>/` for PDFs, HTML sources, chart dirs.
3. Inspect shared tool fixtures: `ls /root/wealth/tests/fixtures/baseline/ | grep <topic>` for the WEALTH eval receipts the audit should reference.
4. **Re-use sibling charts**: `cp /root/forge_work/<sibling-dir>/charts/0*.png /root/<new>/charts/` rather than re-render. Adds ~30s vs minutes and avoids divergent visuals between the two versions.
5. **Add only the v2-specific charts** (eval matrix, Brent headroom, contrast radar, evidence-basis ledger, frontier chart) — typically 4–6 new PNGs.
6. The v2 HTML is a **layered composition**: cover meta carries the live-update overlay line + reference to the v1 sibling path + pointer to the audit fixture dir. The narrative spine is sibling verbatim; the audit layer is original.
7. **Do NOT delete or overwrite the sibling artefacts.** They are a sibling's working output. Your v2 sits alongside.
8. Build a **contrast section** (radar chart or table) showing what v1 covered vs v2 covered. This makes the redo legible in the body, not just in the cover.
9. Append a **source-file appendix** with clickable `file://` links to: v1 PDF + sibling PDF + every WEALTH eval fixture + the IFR PDF + the live dashboards. Future agents loading this PDF can trace every claim back to its source in one click.

Proven on Gentari v2 (06 Aug 2026): 20-page v2 PDF = 9 sibling charts + 6 new charts + sibling HTML spine + original audit integration. Render time: ~5 min for new charts, ~30s for HTML→PDF.

## WEALTH evaluation integration (when the audit layer is requested)
If the v2 redo is triggered by a WEALTH evaluation (12+ tool runs against `wealth_institutional_power_loop` or similar):
1. **Lead with the eval results matrix** as Chart #1 of the audit layer — a 12-row matrix with `tool / mode / score / verdict / key signal` columns. Use a colour-coded verdict dot per row (GREEN=passive, ORANGE=partial, GOLD=hold, RED=negative/absent, GREY=diffused).
2. **Diagnostic-level box**: ABSENT (Beautiful Mouse 0.0) / EMERGING (most scans show healthy friction + structural capture) / DOMINANT (institutional decay). Map scanner verdicts vs structural evidence in a side-by-side table.
3. **Frontier chart**: 4 binding metrics on one chart with safe / trip / now markers. Visualises where the constraint actually binds.
4. **Brent / FX headroom** chart for any energy / commodity subject: residual FCF (CFFO − capex − dividend) vs price scenarios, mark the "turns-negative" point. This is the financial binding constraint per session.
5. **Evidence-basis ledger**: 4-tier (OBS / DER / INT / UNCERTAIN). UNCERTAIN = tool returned HOLD/EMPTY/W0-conflict — these do NOT score and must be flagged separately.
6. **Power geometry map**: when evaluating subsidiary governance, render the board as a node-graph with chair + CFO dual-hatted seats coloured RED, operator BLUE, unverified ORANGE. Annotate `veto_concentration` and `independence` numbers from the eval.
7. **NOC / sector peer comparator** (see `references/noc-control-set-fy2025.md`): build the 7-row table BEFORE writing the verdict. Single-NOC verdicts are the W-007 defect.

## Verifying a rendered PDF (cover check is NOT full QA)
**Never SEAL on cover sanity alone.** Verified 2026-08-07 (Itu Manusia PDF): cover passed vision, but Arif caught "Do u know that ur visual in the pdf is incomplete" — interior defects (hollow wedge fill, ring-label collisions, caption-number mismatch) only showed on chart pages.

1. `pdfinfo out.pdf | grep -E "Pages|File size"` — page count, size in expected range (1 chart ≈ 70-150 KB).
2. `pdftotext out.pdf -` — first 30 lines match the cover narrative.
3. `pdfimages -list out.pdf | head` — confirm N chart images = 2N image objects (image + alpha smask per chart).
4. `pdftoppm -r 110 -png out.pdf thumb -f 1 -l 1 && vision_analyze thumb-01.png "cover OK? text legible? gold accent visible? any overlap?"` — cover sanity ONLY.
5. **FULL-PAGE SWEEP before SEAL.** Render every page: `for p in $(seq 1 $(pdfinfo out.pdf | awk '/Pages/{print $2}')); do pdftoppm -r 110 -png out.pdf pg -f $p -l $p; done`, then vision-sample every chart-bearing page (not text-only pages). Check: charts render fully (no hollow fills, no missing wedges), no text/ring collisions, caption numbering matches chart-title numbering, paired charts have symmetric value labels, inner-circle text readable at print size.
6. **Vision-model loop trap.** vision_analyze on PDF page renders can hallucinate overlap/ghosting that does NOT exist on the raw chart. If vision keeps flagging the same defect after fixes, verify against the RAW chart PNG as source of truth (or PIL pixel-sample: `Image.open(png).getpixel((cx,cy))` — `(255,255,255)` at a center that should be navy = fill silently failed). Fix → verify once on the raw artifact → ship. Over-iterating on vision feedback wastes cycles and reads as thrashing to the user.

## Files
- `references/letter-format-pdf-recipe.md` — formal letter/memorandum PDF format (text-first, 20mm/22mm margins, Times serif, corporate crypto signoff with ASI label and source repository). Use for corporate letters, formal memos, institutional submissions to known recipients.
- `references/civic-letter-recipe.md` — **soul-first civic letter recipe (2026-08-12)** for "surat terbuka", "BIG BANG" civic dispatches, F13 SOVEREIGN letters to Parliament or public. Marhaen/Makcik voice, 5-visualization magnitude pack, fixed crypto signoff (NO ASI label, NO github URL), self-referential hash handling (Kleene's fixed-point), apex-judge isolation step, the 5 external-audit kill shots to defend against. Use when the writer's SURVIVAL depends on the letter being HEARD and the user has expressed hate / "cannot sleep" / "by hook or by crook" about the target.
- `references/report-content-workflow.md` — research → model → report method (paywall triangulation, bottom-up sunk-cost ledger, WI-share discipline, peer-precedent tax modelling, sensitivity conventions).
- `references/petronas-brasil-sunk-cost-2026.md` — worked-example data bank: Petronas Brasil 2003–2026 (deal values, wells, tax cases, sources) so future Brazil/Petronas questions start ahead of zero.
- `references/board-power-node-analysis.md` — recipe + worked example for the "shadow of the chairman" governance chapter; triggers whenever Arif asks to evaluate a BOD or its parent-subsidiary power structure.
- `references/noc-control-set-fy2025.md` — NOC peer panel for energy / oil & gas briefings (Aramco, Equinor, PTT, Ecopetrol, Petrobras, ADNOC Gas, PETRONAS) so single-NOC verdicts always read against a base rate.
- `references/noc-collapse-artifact-pattern.md` — SOVEREIGN-grade collapse/witness artifact skeleton, 8-chart pack, mandatory sections (verdict, scenarios, tripwires, Omega, falsification), and anti-bias discipline. Proven Aug 2026 on PETRONAS (26-page PDF).
- `references/jcorp-financial-databank-2026.md` — JCorp FY2025 metrics, divisional breakdown, growth trajectory, and PETRONAS comparison data. For comparison reports (diversification, growth, resilience).
- `references/petronas-subsidy-paradox-2026.md` — Malaysia fuel-subsidy numbers bank (RON95/diesel mechanics, monthly bill surge Jan→Apr 2026, SERC/Bloomberg/Anwar estimates) + the fiscal-paradox rule. Load before any PETRONAS scenario fan.
- `references/subsidy-paradox-chart-pack.md` — matplotlib chart-recipe for the 4 paradox charts (inversion curve, regime history, cap-floor collision, hidden-tax ratio). Use when building a subsidy-paradox section for a PDF or live-site sovereign-organ coupling. Proven Aug 2026.
- `references/semantic-chart-grammar-v2.md` — binding colour-by-role palette (observed=grey, derived=navy, forecast=gold, risk=red, opp=green) for unified chart grammar across all charts. Proven 2026-08-07 on Arif weekly brief v2; replaces the old decorative navy/gold use.

### The audit-of-the-audit pattern (2026-08-07)

When the user asks "audit this artifact" and the artifact is a sibling's SEAL report or
Apex output, the deliverable is **a verification ledger of the audited artifact, not a
meta-analysis of the critique**. Two failure modes to avoid:

- **Confident agreement** — endorsing the audit's claims without re-probing. Live
  verification on 333-AGI SEAL-9e3e38d3adb3459b (Aug 7) showed the report's "no unexpected
  exposure" claim was wrong: `ss -tlnp` revealed `hermes pid=3015207` listening on
  `0.0.0.0:8444` with no UFW rule. Endorsing that line would have left a public listener
  unreported.
- **Confident dismissal** — rejecting the audit wholesale because some claims look
  suspicious. The same report's *architecture* (DID registration, DISPLAY_ONLY ceiling,
  OpenClaw as EDGE warga) was correct; the *fact layer* was wrong. Reject the bad claims,
  keep the good ones.

Required output: a server-rendered table with columns (Claim / Live evidence / Verdict) —
each row pointing at the exact live command that proved or disproved the claim. Ship the
corrected v2 if real gaps exist; otherwise verify the existing v1 stands. Bullet items
must reference live commands (`ls -la /root/AAA/auth/keys/...`, `find /root/.openclaw -name
...`, `wc -l /root/arifOS/VAULT999/outcomes.jsonl`), not prose claims about them.

### Conceptual chart pack for reflective / essay PDFs (proven 2026-08-07 — "Itulah Manusia")

When the PDF carries a personal-reflection/essay arc (triggered by `deep-research-plus-wealth` → "reflective-essay variant"), the chart pack is NOT data charts — it's **conceptual diagrams**: persona/shadow schemas, two-policy bodies, complementarity matrices, timelines of feeling, projection rings, omega questions. Recipe:

- **Tool: matplotlib with `patches`, NOT data APIs.** Use `FancyBboxPatch` for boxes, `Circle` (imported from `matplotlib.patches`, NOT `plt.Circle` — see pitfall below), `Wedge` for ring effects. Each chart is `ax.axis("off")` — diagrams, not plots.
- **Shared rcParams + shared palette.** NAVY bg (`#0e1a2b`), CREAM text (`#f4ecd8`), GOLD highlights (`#c9a227`), RED suppression, GREEN recognition/integration, ORANGE countercase/gap, BLUE hidden/held. One batch script, one outdir — same discipline as the data-chart pack.
- **Dark background, dpi 180, bbox_inches="tight".** Conceptual diagrams read cleaner on dark — same navy as institutional charts, same federation identity.
- **Caption grammar**: each chart gets a one-line caption with figure number + a non-obvious observation, NOT a restatement of the title.
- **Chart count target**: 6–8 conceptual diagrams per essay PDF. Fewer feels thin, more feels decorative.
- **Escalate verification**: the `pdfimages -list` count and `pdftoppm` + `vision_analyze` for cover are still required. Conceptual diagrams have text labels — vision-analyse a chart page, not just the cover.

#### CRITICAL override — data-first even for reflective essays (Arif, 2026-08-07, "still none and your margins kinda sucks")

**Default rule for the conceptual pack: NOT only conceptual diagrams. Every chart must carry a real number, a verifiable observation, or a published citation — or it does not belong in the pack.** The "Itu Manusia" session shipped v1 as 8 pure-concept diagrams (circles + arrows + boxes, zero numbers) and Arif rejected with "Do u know that ur visual in the pdf is incomplete" — visual decoration is not visual analytics, even on a reflective essay. Even a four-line reflection has a real-data spine available: heritability percentages, latency numbers (12 ms amygdala, 50 ms body, 300 ms conscious feeling), study sample sizes, effect-size CIs, replication evidence. Find the numbers first; build the diagrams around them.

**Concrete recipe for reflective-essay chart packs:**
1. **Pull 6–10 published numbers from research BEFORE drawing.** Latencies, percentages, study sample sizes, effect sizes with CIs, replication counts. Tag each [OBS] / [DER] / [INT]. Sources: `web_search` + verify against a primary source. No fabrication.
2. **Data charts are the spine (5–6 of 8).** Bar charts of percentages (e.g. 10–30% heritable vs 60% chance), forest plots of effect sizes (Wedekind MHC vs 2017 meta), log-scale latency timelines, comparison bars across studies/cultures. These carry the weight.
3. **Conceptual diagrams are accent (2–3 of 8).** Persona/shadow schema, two-policy body, the Omega. Each one labels elements with the data points it explains ("−40% serotonin", "12 ms amygdala fast route") — never as decoration alone.
4. **KPI hero row is mandatory.** 5 cells, real numbers from the same research, under the cover. The hero row alone proves the report has data; users stop scrolling after seeing it.
5. **Charts MUST be tagged inline.** Every chart caption starts with `<span class="tagline">[OBS/DER/INT]</span>` so the reader sees evidence-type before the chart.

**Margin discipline (the second half of "margins kinda sucks"):** Force page breaks before major chapters and the appendix ONLY. Otherwise let content flow — never insert a forced break that creates a half-empty page. Empty dark space after a chart is the most-criticized defect in this class. Rules: no `page-break-before: always` mid-chapter; if a chart would land alone at the top of the next page with empty space below, prepend one or two paragraphs of body text; if a chapter is short, fold it into the previous page instead of forcing a new one.

## Pitfalls quick list
- **Emoji glyphs render as IMAGE objects in WeasyPrint — don't confuse them with charts in `pdfimages -list`** (verified 2026-08-08, FORGE constitutional-sync PDF). A 🟡 in the cover stamp produced 2 small image objects (136×128, ~3KB, image+smask) — exactly the signature of a chart, but it's just the emoji font glyph rasterized. When the 2N-chart count looks off by a small margin, check object dimensions: emoji glyphs are tiny (≈100–200px); real charts are ≥800px. Same for `ΔS`, `≤` etc. if they appear as replaced glyphs. Don't chase a phantom missing chart — verify object size first.
- **Don't run `python3 -c "<subprocess_with_multiline_string>"` via `execute_code`.** The execution environment blocks `subprocess` inside `execute_code` because it bypasses shell-string approval. Write the script to disk with `write_file`, then run via `terminal`. Costs one extra tool call but unblocks the whole batch.
- **Vision_analyze loop trap — STOP after one fix-and-verify pass (2026-08-07, Itu Manusia).** User flagged the chart, I re-rendered + re-vision-checked 5 times. Each pass said "X is overlapping" or "now Y is overlapping" — but the raw chart PNG was clean from the first fix. Vision models re-flag the same edge-zone defect across iterations on rendered PNGs as phantom noise. Rule: fix the flagged defect → re-render → ONE confirming vision pass on the RAW chart PNG, not a PDF page render (page renders add caption/footer text that vision mis-reads as chart overlap). After one confirming pass, ship. Continued iteration is thrashing the user can see in their attention.
- **Page break restraint — let content flow (2026-08-07, "margins kinda sucks").** Default instinct: insert `page-break-before: always` between chapters. Result: half-empty pages with one chart and a paragraph, looks "semak" (Arif's word for cluttered). Rule: forced page breaks ONLY before cover, major chapter openings, and appendix. Mid-chapter content flows naturally. CSS `page-break-inside: avoid` on `.chart` and `.verdict` is sufficient. A page with <60% content fill = violation; fold backward or merge.
- **`mpatches.Wedge((x,y), r, 0, 360, width=0)` renders HOLLOW** (verified 2026-08-07). Want solid concentric core inside ring/donut? Use `mpatches.Circle((x,y), r, ...)` instead. PIL pixel-sample to confirm: `(255,255,255)` at a center that should be navy = silent fill failure.
- **Caption numbering must match chart-title numbering.** Two parallel sequences read as editorial confusion. One sequence per document.
- **Symmetric value labels across paired charts.** If chart A shows per-bar values, chart B beside it must too. User reads asymmetry as broken.
- **Default margins 22mm → 14mm for chart-dense PDFs.** Wider side margins make charts look orphaned.
- **SOVEREIGN-grade collapse / "when will X die" requests** need ≥13 pages (Arif's stated minimum, 2026-08-06), 8+ charts, 7 tripwires, 4+ scenarios with explicit probability bands, an Omega Question box, and a Falsification Protocol section. Proven Aug 2026 on PETRONAS: v1 ran 26 pages (994K) but was REJECTED for named-philosophy framing; v2 at 17 pages of pure human-language PETRONAS was accepted. The page count is a floor, not a target — frame first, length second. See `references/noc-collapse-artifact-pattern.md`.
- **JS charts → blank in PDF (top item).**
- **Live site interactive engine ≠ PDF deliverable.** When the user asks to update a LIVE site page (not a PDF), **static PNG charts are vestigial** — Arif's words: *"why u do so many static graph?? Baked that into the model slider."* Pattern: pure-Python model in `models/v3/model.py` (unit-tested, 53+ tests) → port to JS as IIFE module → Node cross-validation script (assert Python == JS within 0.05 for ~6 sample param sets) → embed inline `<script>` in `public/<path>/index.html` → static charts are removed, replaced by canvas chart that redraws on slider tick. PDFs use the chart-pack recipe; live sites use the engine. See `arif-fazil-site-ops` skill for the site-edit flow.
- Never fabricate paywalled article detail — triangulate secondary sources, tag OBS/DER/INT.
- Always check whether a headline deal actually CLOSED — rescinded deals cost only fees; count the avoided amount as an outcome.
- Minority stakes: count only the working-interest share of capex, not the operator's full project cost.
- **WeasyPrint may not be installed by default.** On Debian-derivative hosts, `pip install` requires `--break-system-packages` because PEP 668 blocks the system python; use `pip install --break-system-packages weasyprint`. Verify with `python3 -c "import weasyprint"`.
- **`which python3` may NOT be the python that has weasyprint.** Verified 2026-08-06 on af-forge: default `python3` was the WEALTH venv (`/root/WEALTH/.venv/bin/python3`, Python 3.12) which had no `pip` and no `weasyprint`. The system `pip install --break-system-packages` installed to `/usr/local/lib/python3.13/dist-packages/`. The fix: render via `/usr/bin/python3.13` (system Python 3.13 with weasyprint 69.0). One-liner that always works: `PY=/usr/bin/python3.13; $PY -c "import weasyprint; weasyprint.HTML('report.html').write_pdf('out/report.pdf')"`. Always verify with `$PY -c "import weasyprint; print(weasyprint.__version__)"` before committing the render command. The host has multiple pythons; default `python3` does not imply the one you want.
- **User may supply live intelligence mid-build** (dividend cuts, court rulings, governance corrections). Treat as [OBS] with an explicit "live-update overlay" callout in the cover meta + relevant chapter. Do not re-render twice — fold into the next render cycle, not the current one.
- **"Lorem ipsum" placeholder bios** on the public leadership page are an [OBS] site defect, not your problem. Flag as [UNK] on the person's status; never invent a bio to fill the gap.
- **Arif's PDF standard for SOVEREIGN-grade briefings** (WEALTH/333 deliverables): 9-12 inline charts covering trajectory, geographic mix, financials, capex split, policy map and timeline; KPI hero row under cover; tables in appendix only; epistemic tags on every number; named "shadow of the chairman" / governance chapter for any subsidiary board being evaluated. See `references/board-power-node-analysis.md`.

- **Empty-page / half-empty-page trap (2026-08-07, "margins kinda sucks").** Arif rejects PDFs with large empty dark blocks or pages that are less than ~60% filled. This usually happens when: (a) a forced `page-break-before: always` pushes a short chapter to a new page leaving a full page empty above; (b) a tall chart is followed by a forced page break, leaving a blank space below the chart. Rules: (1) no `page-break-before: always` except before the cover, appendix, or the Appendix section — mid-chapter content always flows naturally; (2) before rendering, ask: "does this page have ≥60% content fill?" — if a text page is nearly empty, fold it backward; if a chart page is nearly empty, prepend body text or merge the caption; (3) if the HTML body has a `<div class="break"></div>` that creates a sparse page, remove it and let WeasyPrint paginate naturally — the CSS `page-break-inside: avoid` on `.chart` and `.verdict` is sufficient; (4) verify with `pdftoppm` full sweep — any page where dark/chart background dominates >40% of the page height without a caption or text below it is a "semak" violation. This is the same "one signal per cell" rule from the Redundancy Tax, extended to page fills.
- **Memory cross-check before patching WEALTH organ state.** If your memory says "PCM fixed in commit X, 18/18 differential green" but a sibling eval just reproduced the original crash, treat memory as stale — verify against `git -C /root/WEALTH log` + the live `wealth_mcp/middleware/evidence_middleware.py` before trusting either. The crash repro at the eval receipt IS evidence; memory IS a hint.
- **Memory write discipline.** Do not write session-task progress, "fixed bug X", PR numbers, or sealed receipts to memory. Memory captures stable user preferences + environment quirks. The Gentari v1→v2 lesson (governance_capacity 0.2883/3.0) belongs in the skill, not memory.
- **Arif's PETRONAS/NOC deliverable format: plain human language, NO named theory in the body.** Arif (2026-08-06, verbatim): "I want full human language and focus on PETRONAS. No need to mention mouse godel lock etc" — he is *obsessed* with Acemoglu/Calhoun/Gödel as THINKING frames, but they must NOT appear by name as sections/labels in the sovereign-facing artifact. Use them silently to shape chapters (extraction, hollowing, self-audit) and write PETRONAS-only narrative: the numbers nobody reads together → reserves → debt/dividend → what the world is doing to oil → scenarios → what everyone pretends not to see → timeline → tripwires. v1 surfaced the frames and got rejected; v2 hid them and passed. Frames are the scaffold, never the facade.
- **KPI hero grid: `white-space: nowrap` on `.kpi-value`.** Without it, "RM" wraps alone above "266bn" in narrow cells while "RM 45bn" stays on one line — a ragged 5-column strip that vision_analyze flags. Fix in CSS, not per-cell.
- **The subsidy paradox (Malaysia fiscal lens) — mandatory for ANY PETRONAS scenario work.** High oil price is NOT a bull case for the nation: Brent $90 → PETRONAS dividend +RM10B vs government subsidy bill +RM30–40B → net nation −RM20–30B. In 2026 the fuel-subsidy bill (~RM40B/yr run-rate) ≈ 2× the PETRONAS dividend (RM20B). A scenario fan built only on PETRONAS cash flow inverts the real verdict — reframe scenarios as nation-fiscal outcomes (dividend + petroleum revenue − subsidies). Numbers bank: `references/petronas-subsidy-paradox-2026.md`.
- **v1 → v2 contrast analysis — separate document, not a re-render.** When the user points out a load-bearing omission (e.g. "u are missing the subsidy paradox"), don't try to fix it silently into the original PDF. Build a separate contrast document that: (1) lists every specific omission in v1 with magnitude, (2) renders a v1-vs-v2 radar showing what each version covered, (3) shows the new chart pack (subsidy paradox curves, cap-floor collision, hidden-tax ratio), (4) lays out the new binding-constraint geometry, (5) restates the "where I'm wrong" vector list with FY26 fiscal-capacity swing magnitudes, (6) names the new tripwire proposal explicitly. Render at ~16 pages, single self-contained HTML → WeasyPrint. Proven on PETRONAS Aug 2026: 16 pages / 850KB / 4 contrast charts + 3 paradox charts. The contrast document is the FALSIFICATION of v1, not a correction of v1 — both stay on disk and the user gets the meta-record.
- **Bias-test discipline when user states a position.** If the user opens with "Actually it's not good for the entire nation" or "It's titanic now" or any stated bias, the FIRST step is to render the bull case with equal rigour. The artifact MUST contain "where I'm wrong" ranked by ±swing on the FY26 fiscal outcome. If the only scenarios confirm the user's stated certainty, the artifact has failed F2 (P(truth) ≥ 0.99). Lead the analysis even when it contradicts the bias — Arif wants the analysis, not the agreement.
- **Subsidy paradox chart-pack recipe (proven Aug 2026 on /propa/ + /malaysia/ site revamp):**
  - S01: Brent (x) → dividend + subsidy bill + net-to-budget (y), fill regions where net < 0 in red, mark crossover explicitly.
  - S02: Subsidy regime history — annual Brent avg vs subsidy bill (RM B), colour-coded by severity band.
  - S03: Cap-floor-subsidy collision — PAT (x) → AMEND cap × MoF floor × subsidy cost, mark the PAT=33.3B crossover.
  - S04: Hidden-tax ratio — Brent (x) → subsidy/dividend ratio (y), draw parity line at 1.0, label bands.
  All four live in `site-charts/` for site use OR `charts/` for PDF use — copy to whichever is the deliverable.
- **Live site edit contrast with PDF redo.** PDF redoes use the sibling-artefact integration pattern (cp sibling charts, layered composition). Live site edits on coupled sovereign organs use the cross-organ coupling pattern (shared anchor id, bidirectional cross-links, distinct accent colours per page). The two patterns look similar but the verification differs: PDFs verify via `pdfimages -list`; live sites verify via `curl -sf` per page + chart endpoint. Don't apply PDF redo patterns to live site edits — they have different verification surfaces.
- **Redundancy tax — semak before ship (Arif, 2026-08-06).** Arif verbatim: *"the pages so semak. No clarity suggest lower entropy reduction. No redundants."* Every element must carry ONE signal. Common redundancies: state shown as badge + card + label (pick ONE), readout derivable from other readouts (e.g. CFFO = PAT × 1.88 → drop CFFO readout), prose callout restating what the canvas already shows (delete the prose), probe lines that repeat all cards verbatim (delete). Fix: before shipping any panel, list each element and ask "what does this add that no other element already carries?" If the answer is "nothing", delete it. A panel with 3 readouts + 1 state badge + 1 canvas + 1 contrast strip is complete. A panel with 5 readouts + 3 state indicators + 1 canvas + 1 prose block is noise. Contrast by construction (low-oil vs high-oil side-by-side strips) not by accumulation. Same rule applies to PDF panels — one signal per cell.
- **Cover meta crop on full-bleed covers (2026-08-07).** Long meta lines (author lists, omega sentences) crop at the right edge of 210mm covers — verified: "Brehm 1956" rendered as "Brehm 195". Keep cover meta lines ≤ ~90 chars or break with `<br>`. Vision-verify the cover after every re-render.
- **`pdftoppm` single-page filename is `prefix-0N.png`** (e.g. `thumb-03.png`), not `prefix-0N-01.png`. `ls prefix*.png` before passing to `vision_analyze` — a guessed wrong path wastes a call.
- **`plt.Circle` is not exported from `matplotlib.pyplot`.** When building conceptual diagrams (persona/shadow, projection rings, gap schemas) with matplotlib patches, `plt.Circle((x, y), r, ...)` raises `reportPrivateImportUsage` / `AttributeError`. Import `Circle` (and `FancyBboxPatch`, `Wedge`, `FancyArrowPatch`) directly: `from matplotlib.patches import Circle, FancyBboxPatch, Wedge`. Then `Circle((x, y), r, color=..., alpha=..., ec=..., lw=...)` and `ax.add_patch(...)`. Verified 2026-08-07 on the "Itulah Manusia" conceptual chart pack — caught at lint, fixed with a single import line.

- **`letter_spacing` is NOT a valid matplotlib `Text` property (verified 2026-08-12 PETRONAS APEX LETTER II v14).** `ax.text(x, y, "...", letter_spacing=2)` raises `AttributeError: 'Text' object has no property 'letter_spacing'`. matplotlib has no CSS-letter-spacing analog for `Text`. If you need character-spacing (e.g. for "OPERATION OPERATION" with wide tracking), use multiple `text()` calls with hand-tuned `x` offsets, OR use a Pillow-rendered bitmap, OR simply drop the tracking. Common pitfall when porting CSS-styled HTML labels (e.g. `letter-spacing: 2px`) to matplotlib patches.
- **Arrow labels crossing arrow strokes (conceptual diagrams).** A curved `annotate` arrow passes through its own text label → text visually bisected (the arrow stroke cuts the letterforms). Fix: give the label an opaque `bbox=dict(boxstyle="round,pad=0.3", fc=NAVY, ec=ORANGE, lw=1)` so the label masks the stroke behind it. Verified 2026-08-07: 3 chart rebuild iterations on the "suppression arrow" pill before this stuck.
- **Gap/channel labels spilling into adjacent colored shapes.** Text centered in the navy channel between two boxes bleeds onto a box edge at font sizes ≥ 12. Fix: size the label for the channel (fontsize 9–11), stack lines vertically, place the connecting arrow BELOW the text block not through it, and verify with vision_analyze ("the model reliably catches 'left edge of THE touches gold box'"). Verified 2026-08-07.
- **Text truncation inside small markers.** A short word inside a small scatter marker reads as truncated ("same" → "ame") when marker s ≈ 200 AND font color is the marker fill. Fix: marker s ≥ 350 AND flip text color to NAVY on GOLD fill (low-contrast text on a matching-hue marker reads as missing at render scale). Verified 2026-08-07 on the complementarity matrix.
- **Edge clipping at plot extremes.** Markers at the corners of a scatter matrix get cut by the axes. Fix: `clip_on=False` on both scatter and text, AND give the axes extra headroom (`set_xlim(-0.3, 5.8)` not `(-0.5, 5.5)`). Verified 2026-08-07.
- **Copy-paste title numbering drift.** Chart N titled with the wrong figure number ("04 — …" rendered as "06 — …") — a duplicate-title copy error that survived the lint pass but was caught by vision_analyze. Always re-check chart numbers against the figure list before render.
- **Vision-noise on small text (after first fix).** The vision model re-flags the same small-text defect across iterations even after a successful fix — perception at the resolution edge of the rendered PNG. Don't chase every flag: after fixing a flagged defect, re-render and do ONE confirming pass; treat repeated flags on the same element as noise unless the rendered PNG actually shows the defect. Otherwise you loop forever on phantom issues.
- **Verify EVERY conceptual chart with vision_analyze before embedding.** Arif inspects chart quality and will call out incomplete visuals (verified 2026-08-07: "Do u know that ur visual in the pdf is incomplete" — drove a 3-iteration rebuild). Batch 4 vision calls per round on the rendered PNGs (cheap, parallel). Conceptual diagrams have text labels — vision-analyse each chart page, not just the cover.
