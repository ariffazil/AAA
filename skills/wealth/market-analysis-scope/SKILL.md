---
name: market-analysis-scope
description: "Use when analysing markets or charting assets."
version: 1.0.0
author: Hermes Agent
tags: [market, analysis, technical-analysis, fundamentals, commodity, equity, collapse, forensics]
---

# Market Analysis Scope

> Trigger: any market question, any chart request, and especially "will this go up / will this survive". Establishes what technical analysis can and cannot evidence **by asset class**, reads the distribution signature, and blocks chart-only claims about company survival.

**Establish the DOMAIN before answering any market question. Chart validity is domain-dependent, not tool-dependent.**

This skill governs reasoning and framing — what you are entitled to claim from a chart. It composes with the chart-generation skills; it does not replace them.

## The domain table — read this first

| Domain | What price encodes | Hidden information present? | What the chart is |
|---|---|---|---|
| Commodity (gold, silver, Brent) | What buyers are paying. No counterparty, no accounts, no management. | No — price is the only information that exists | **The reality** |
| Company equity | What people *believe* about the company | Yes — accounts, audit, related-party deals, insider actions, cash flow | **A shadow of belief** |
| Unlisted / no ticker | Nothing — there is no price | Everything | **Non-existent. Say so.** |

## Rules

1. **For a commodity, more indicators is not more information.** There is nothing hidden for a filter to uncover; extra layers only cut trade frequency and *feel* like discipline. What actually raises signal quality: (a) knowing something others don't, (b) knowing where others' stops sit, (c) a risk process tight enough to survive a small edge. If the user says fundamentals are noise for a commodity, **they are right — do not argue them back toward a heavier stack.**

2. **For a company, the chart cannot see the cause — but it CAN see the effect.** Never claim chart analysis detects fraud. Do claim it records insider exit. Both claims are defensible; only one is honest.

3. **Never answer "will this company survive" with chart-only reasoning.** That question lives in the accounts, the auditor, and the related-party transactions.

4. **Do not answer "the chart is blind here" by adding more chart layers.** That is self-contradiction — you have just conceded the tool cannot see the thing, then prescribed more of it. For a company the corrective is fundamental evidence; for a commodity there is nothing to correct, only discipline.

## The Distribution Signature (support-break cascade)

```
support breaks → rally attempts → rally FAILS at the old support (now resistance)
→ lower high → break again → collapse
```

The failed rally is the informative part: buyers trapped at the old support sell into every bounce just to get out flat, so each rally meets fresh supply and the level flips from floor to ceiling. **Repeated lower highs across successive support breaks = repeated distribution.**

This is the one place fundamentals and technicals agree, and it is worth stating plainly: the cascade does not reveal *why* informed holders are leaving, but the leaving prints on the chart before the reason becomes public. The chart yields a **question** ("why are insiders exiting?"), not an answer — and the question is what keeps the user solvent.

**Cost asymmetry rule:** the chart cannot distinguish "fraudulent" from "ordinary decline". You do not have to distinguish. Exiting a healthy company early costs missed upside; staying in a dead one costs everything. When the cascade prints, exit first, investigate after.

## "It hasn't crashed yet" is not evidence

Companies do not degrade gradually and then die — they die at a **cliff edge**: years of bookkeeping, days of truth. Healthy-looking technicals at the all-time high are the NORM in every corporate collapse, not the exception. Never accept "the chart still looks fine" as a reason a company is safe, and never offer it as one.

## Every analysis artifact carries its own uncertainty

A rule derived from two indicators is a rule, not a judgment. Do not dress it as an authoritative verdict — a letter-graded "setup quality" computed from RSI + EMA is exactly this failure mode. Every published artifact (site panel, PDF, briefing) should carry three blocks:

- what the price is doing,
- what moves it from **outside** the chart (yield, dollar, geopolitics, policy),
- **what we do not know.**

The third block is routinely omitted and is the most valuable to the reader.

## Conceding the domain point gracefully

When the user pushes back on chart-only analysis, **concede the domain point and name the mechanism** rather than defending or piling on analysis. Two speakers are usually both right about different domains; resolve by naming which domain is being asked about.

- Company: price records belief; belief can be falsified; the causal information sits in the accounts and in who is free to audit them.
- Commodity: no counterparty, nothing hidden; price is the only information that exists.
- Same tool, different domain = different result. A tool is not broken because it was applied where no signal exists, nor complete because it returned something.

## Untradeable assets have no chart — and therefore no alarm

An asset without a ticker (e.g. a wholly state-owned company) has no price, no chart, and therefore no early-warning mechanism: nothing can fall, no volume spike can print, no lower high can form. The only available measure is the cash-flow relationship — how much is paid out versus reinvested, year over year. When no market exists, **an observer inside the institution is the only possible witness.** State this plainly rather than forcing the normal chart framework onto it.

## Pitfalls

- **Do not let a chart's apparent health resolve a survival question.** See the cliff-edge rule above.
- **Verify chart layout by reading the render back, not by assuming.** Load the output PNG with `vision_analyze` and ask only about geometry: annotation boxes over the title, labels clipped at the figure edge, summary boxes covering data. The vision model is unreliable on *identity* (it misreads small print, names, logos) and reliable on *occlusion and layout*. Patch the offsets and re-render — a 2000px chart hides collisions until after delivery.
- **Not every chart is a trade chart.** Match the grammar to the request: trade signal (candles + zones + R:R), collapse comparison (stacked panels + dated events, no R:R), long-horizon stock history (price + dividends subplot + raw-vs-adjusted returns), allocation/biometrics (composition + target-band comparison). Adding a BUY ZONE to a forensic chart is noise.
- **Do not attach a market lesson to a named living person or the user's employer.** State the mechanism and stop; the moral is theirs to draw.

## References

- `references/corporate-collapse-forensics.md` — reconstructing delisted price series, the four-phase collapse silhouette, comparison-chart recipe.
