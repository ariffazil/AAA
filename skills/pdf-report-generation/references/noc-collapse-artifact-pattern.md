# NOC / parent-company collapse-artifact pattern (SOVEREIGN grade)

**Proven 2026-08-06 on PETRONAS (`forge_work/petronas-collapse-2026/`).** 25-page body + appendix, 1.4MB, **15 inline charts**, vision-verified cover and body, all JS-free. Designed for F13 SOVEREIGN-grade "when will X collapse / die / fail / is it titanic" requests — distinct from the Brasil sunk-cost reference (deal-level ledger) and the board-power-node reference (BOD governance).

> **v2 — supersedes the v1 sibling sketch (8-chart / 26-page / Acemoglu-frames-in-chapters).** v2 lesson: Arif corrected mid-build *"No need to mention mouse godel lock etc"* — framework names stay in thinking scaffolding, never in deliverable prose. v2 is what Arif accepted.

## When to use this pattern (not the others)

| Trigger | Use |
|---|---|
| "When will PETRONAS / Aramco / PEMEX / [NOC] collapse? / net debt" | **This pattern** |
| "How much did Petronas lose in Brasil / Iraq / Mexico?" | sunk-cost pattern |
| "Evaluate the governance of [subsidiary BOD]" | board-power-node pattern |
| "Should I buy / sell [bond / share]?" | full WEALTH evaluation, not this |
| "is it titanic / ranges / tripwires / net debt" | This pattern, "titanic" = collapse framing |

The collapse-artifact is a **witness document**, not a decision document. It does not tell Arif what to do. It maps the structural state, gives him tripwires he can monitor, and verifies his stated bias against the data, not confirms it.

## Anti-bias discipline (mandatory)

If the user states a bias ("It's titanic now"), the artifact MUST contain the bull case with equal rigour to the bear case. If the only scenarios confirm the bias, the artifact has failed. The bull case is the falsification test that makes the verdict real.

In the PETRONAS Aug 2026 v2 (this skill's reference): Soft landing 45%, Structural squeeze 30%, Full squeeze 15%. Arif said "Titanic" but the base case was the most likely outcome. **Do not collapse to the user's stated certainty. Test it. Show your work.**

## RENDERING DOCTRINE — frameworks invisible in the deliverable

The 7 layers, Acemoglu, Calhoun, Gödel/Hofstadter, "strange loops", principal-agent voids — all **thinking scaffolding**. The deliverable contains:
- ✅ Plain human language, verdict-first
- ✅ Epistemic tags (OBS/DER/INT/UNK) in table cells and chart captions
- ✅ "7-Layer Intelligence" badge on cover if you want
- ❌ NO framework names in chapter headings or body prose
- ❌ NO layer labels in narrative
- ❌ NO mention of "structural capture" / "gradient constructor" / "critical juncture" unless Arif asked for those terms

If Arif says "no need to mention X" mid-build, drop X completely and never re-introduce. He means it.

## Report skeleton (25 pages, 11 chapters)

```
Page 1     Cover — dark navy gradient + gold accent + F13 SOVEREIGN badge + tagline
Page 2     KPI Hero (5 cells) — the headline numbers at a glance
Page 3-4   Chapter 1 — The Question (reframe, scope, what is and isn't being asked)
Page 5-6   Chapter 2 — What Happened (FY25 facts: revenue, PAT, segment mix, capex)
Page 7     Chapter 3 — The Dividend Problem (timeline chart + cash flow gauntlet)
Page 8-9   Chapter 4 — The Balance Sheet (gearing/ROACE twin chart + assets/equity)
Page 10    Chapter 5 — The Breakeven Question (Brent regimes + breakeven range table)
Page 11-13 Chapter 6 — What Nobody Is Talking About (5 sub-sections, one each)
Page 14    Chapter 7 — What the Models Say (sensitivity tornado + Monte Carlo)
Page 15-16 Chapter 8 — The Three Scenarios (Soft/Structural/Full, with probabilities)
Page 17    Chapter 9 — Tripwires (dashboard chart + table, severity-coded)
Page 18-19 Chapter 10 — What I'm Sure Of / Deriving / Interpreting / Where I'm Wrong
Page 20    Chapter 11 — The Omega Question (one box, italic, gold accent)
Page 21-23 Appendix A — Source table (every number traceable, OBS/DER/INT tagged)
Page 24-25 Appendix B — NOC peer comparison + methodology
```

## Chart pack (15 charts, batch in one Python script)

| # | Chart | Why |
|---|---|---|
| 01 | KPI Hero strip | Five headline numbers in one glance |
| 02 | Revenue & PAT 5yr + dividend line | Trajectory + dividend line overlay |
| 03 | Segment PAT FY25 | Where the profit actually comes from |
| 04 | OCF vs Capex vs Dividend + post-FCF residual | The cash flow gauntlet |
| 05 | Dividend timeline 2016-2026E | The cliff in historical context |
| 06 | Gearing vs ROACE (twin axis) | Twin drift — direction matters |
| 07 | Sensitivity tornado | Brent dominates everything |
| 08 | Monte Carlo on FY26 PAT (5,000 runs) | Distribution, not point |
| 09 | Gentari (or subsidiary) capacity vs plan | Subsidiary gap analysis |
| 10 | Subsidiary losses (PCG or equivalent) | One chapter, one chart |
| 11 | Brent price regimes history | Context for guidance |
| 12 | Total assets & equity | The balance sheet erosion |
| 13 | Political/dispute timeline | The Sarawak-style regulator case |
| 14 | Tripwire dashboard | Single page, all 7 tripwires |
| 15 | "Where I'm wrong" ranked by swing | Self-attack visual |

**Always batch all 15 in one `build_charts.py` script** with shared `rcParams`, shared palette constants (NAVY/GOLD/RED/GREEN/BLUE/ORANGE/GREY), shared outdir. ~30s total, single state, no drift.

## Mandatory HTML patterns

- `<span class="tag tag-obs">OBS</span>` / `.tag-der` / `.tag-int` / `.tag-unk` in tables and captions only — not in prose
- `<div class="box navy">` / `.box red` / `.box orange` — interpretive boxes, distinct colour for each severity
- `<blockquote>` with gold left-border for the Omega Question
- `<table>` ALWAYS in appendix — body has prose + charts + verdict only
- `<img src="charts/0N_*.png">` — relative paths so `pdfimages -list` finds them all

## The "no certainty" doctrine

The artifact MUST contain:
- **3 scenarios with explicit probability bands** (Soft landing / Structural squeeze / Full squeeze — 45/30/15% proven; or 4 if a clear renewal case exists)
- **7 tripwires** the user can monitor — read these numbers, that's the test
- **A "Where I'm wrong" section** ranked by magnitude of swing, upside AND downside
- **An Omega Question** — one uncomfortable question that survives all numbers

Missing any of these = the artifact has collapsed into a forecast, which violates F2 (P(truth) ≥ 0.99) and F7 (Ω₀ ∈ [0.03, 0.05]).

## Binding constraint discipline

Every collapse-artifact needs ONE load-bearing variable stated explicitly. For PETRONAS Aug 2026 v2 it was **Brent at $50/bbl → upstream breakeven** (the line where upstream stops being self-funding). The binding constraint must:
1. Be observable in published data (not internal memos)
2. Lead the financial signals by 6-18 months
3. Be specific enough to be a single number, not a category

If you can't name the binding constraint in one sentence, the artifact isn't finished.

## Pitfalls

- **Don't name frameworks in the deliverable.** Even if you used them to think. They are scaffolding, not content.
- **Don't put the user-named bias in the conclusion.** Test it. Show your work. If your analysis contradicts his bias, lead with the analysis — don't suppress it to be polite.
- **Don't cite sibling reports verbatim.** Sibling reports are inputs. Your synthesis is the output.
- **Don't lead with the data.** Lead with the verdict. Arif already knows the data. He wants the synthesis.
- **Don't pad to 26 pages.** 25 + appendix is the proven minimum. More pages of repeated data is entropy accumulation.
- **KPI hero must be 5 cells, all YoY deltas visible.** This is the one-glance summary that matters.
- **The Monte Carlo MUST include the median line AND P10/P90 lines** — a single mean is not enough; the floor is what matters.
- **The tripwire dashboard MUST have status colour-coding** (SEVERE red, ELEVATED orange, WATCH grey, GREEN ok) or it's just a list.
- **The "where I'm wrong" MUST be ranked by swing magnitude** — biggest upside error, biggest downside error, separately.

## What "human language" means in this pattern

Bad: "The trajectory exhibits a structural deterioration pattern consistent with extractive-institution closure, with RRR migration from 0.3 to 1.0+ indicating reserve quality degradation across the upstream portfolio."

Good: "Production is falling 28,000 boed per year. Reserve replacement is below 1.0×. The fields are getting older, and the new ones aren't being found fast enough. This is the wall the upstream business is walking toward."

Same analysis. First one is for an academic paper. Second one is for Arif.

## v1 → v2 evolution log

- **v1 (sibling, 2026-08-06):** 26-page skeleton with Acemoglu/Calhoun/Gödel frames embedded in chapter titles. 8-chart pack.
- **v2 (this skill, 2026-08-06 same day):** Arif's mid-build correction "no need to mention mouse godel lock etc" → dropped all framework names from prose. Expanded to 15 charts because each chapter needed its own visual. Reduced to 25 body pages because the v1 chapters 4 and 5 (Acemoglu frames, incentives) collapsed into "Chapter 6 — What Nobody Is Talking About" which uses plain prose instead of framework labels. v2 is the canonical pattern.