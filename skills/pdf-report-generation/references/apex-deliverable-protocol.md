# Apex Deliverable Protocol (claim-graphed, counter-tested, scenario-branched)

Proven 2026-08-07: Arif weekly brief v1 (13 pp, flat narrative) → external audit → v2 (15 pp) rebuilt to this contract. The audit verdict on v1: "strong strategic brief, not yet Apex audit-grade" — gap = evidence traceability, visual grammar consistency, decision operability. v2 closed all five findings.

## The 8-element contract

`Claim → Evidence → Derivation → Countercase → Trigger → Action → Falsifier → Confidence`

Applied to every nontrivial deliverable. If any element is missing for a load-bearing claim, the artifact is not yet Apex.

## Page anatomy (v2 proven)

1. **Cover** — badges (F13 SOVEREIGN / APEX v2 / CLAIM-GRAPHED·COUNTER-TESTED), contract line, seal line with ΔS.
2. **KPI hero row** — same as v1 (5 cells, FY-now + delta).
3. **Verdict box** — binding constraint + falsification test in 2–3 sentences.
4. **Claim blocks (C-01..)** — the workhorse. Each:
   - ID chip `C-0N` (monospace, navy bg / gold text) + epistemic chip (OBS/DER/INT/UNC colour map)
   - claim text
   - Evidence block: source IDs (S-0N) with one-line "used for"
   - `Falsify:` one sentence, threshold + date where possible
   - `Confidence: 0.xx [OBS/DER/INT]` — split band when mixed (e.g. "0.78 [OBS levels] · 0.55 [DER fan weights]")
5. **Countercase boxes** (orange) — steelman + disconfirming datapoint + what-shifts-view. One per main thesis; 3 in the 15-pp brief (gold, subsidy paradox, Hormuz deal).
6. **Scenario fans** (charts) — Base/Upside/Failure lines + shaded fan + weights in legend + falsifier thresholds in title.
7. **Decision packet grid** — signal × trigger × horizon × confidence × action × expected reaction; ≥60% green/act, <60% orange/wait.
8. **Source index appendix** — S-01..S-N grouped by domain (Markets, Hormuz, Fed, Malaysia, Petronas, AI, China/Crypto, Agent) with URL + used-for + tag.

## Chart grammar (matplotlib, proven)

- Semantic-role palette: NAVY observed, GOLD derived/median, RED risk/invalidation, GREEN upside, ORANGE adverse, BLUE forecast. Same colour never means two roles across charts.
- **Falsifier-in-title**: title ends `· Falsify: <threshold> by <date> = <interpretation>`. Keep ≤ ~90 chars or the title runs into the legend (vision check flagged this on the Brent fan).
- Fan charts: `fill_between` for the band, solid line = base, dashed = upside/failure, vertical "NOW" marker at x=0, weighted legend entries ("Base (40%) — Hormuz reopens by Q3").
- Decision packet as matplotlib grid: header row gold, alternating row shading, per-cell colour (signal navy bold, horizon blue, confidence green/orange by ≥60%, action red bold, expected grey italic).

## HTML/CSS for WeasyPrint (proven)

- `.claim-block`: white box, 1px #ddd border, radius 4px, `page-break-inside: avoid`. `.claim-id` monospace navy chip gold text; `.claim-tag` chips (obs green / der purple / int orange / unc red); `.claim-text` 10.5pt; `.claim-evidence` dashed-top grey 8.5pt; `.claim-falsifier` red; `.claim-confidence` green bold.
- `.countercase`: `#fef3e2` bg, 1px `#e67e22`, 5px orange left border; `.cc-head` uppercase orange letter-spaced.
- `.lane-block` (three-lane: headline signal / evidence / operator implication): 3 flex columns, gold / navy / red left borders.
- `.source-idx` tables: 7.5pt, grouped by domain, `th` navy bg gold text.
- Footer left: `SEAL ::APEX::v2::<date>` via `@bottom-left`.

## v1 → v2 before/after (the audit's 5 findings)

| Gap | v1 | v2 |
|---|---|---|
| Claim graphing | epistemic tags at paragraph end | C-IDs + source blocks + falsifier + confidence per claim |
| Adversarial balance | none | 3 countercase boxes |
| Scenario engine | single-path directional language | 3-scenario fans with weights + triggers + falsifiers |
| Visual unification | mixed per-chart palettes | semantic-role palette + falsifier-in-title |
| Decision packet | watchlist table | operator grid (signal/trigger/horizon/conf/action/expected) |

## Pitfalls

- Long falsifier-in-title collides with legend → keep titles short; move long falsifier to the caption or claim block.
- Don't put epistemic chips inside flowing prose (v1 style). Either use structured claim blocks or omit from prose entirely — rendering doctrine: tags belong in tables, captions, and structured blocks, not paragraph text.
- Weights must sum to 100 and each scenario needs a falsifier; a scenario without a falsifier is decoration.
- **When Arif pastes an external audit of your artifact, treat it as a spec upgrade**: rebuild the artifact to it, then codify the protocol into the skill library so the next brief starts at the new floor (v2 ΔS = 0.42 vs v1).
- Verify rendered v2 as usual: `pdfinfo` pages, `pdfimages -list` (N charts = 2N image objects), `pdftoppm` + `vision_analyze` on cover AND one chart page (title/legend overlap is the common defect).
