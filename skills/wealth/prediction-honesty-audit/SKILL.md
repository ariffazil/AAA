---
name: prediction-honesty-audit
description: Use when asked to predict a price or outcome.
capability_tier: fed-long-context
ecology_state: WARM
---

# Prediction Honesty Audit

Use when a human asks for a forecast, or when a human or agent claims that a method (an indicator, a signal engine, a model) can predict. Applies to markets, but the test is generic.

## Stance

Never emit a directional forecast. When asked "up or down", the honest answer has two parts:

1. a **volatility envelope** — where the price may plausibly sit, expressed as percentiles;
2. the **position-size consequence** of each level in that envelope.

Say plainly that direction is not knowable from here, then give the range and what each end of it does to the position. The human is not asking for a number because the number is knowable; they are asking because the decision is uncomfortable. Answer the decision, not the question.

## Procedure

**Step 1 — check the engine's calibration before quoting it.**

Hit the organ/service health endpoint and read the calibration block (`verified`, `accuracy`, `brier`). If `verified == 0` or accuracy is ~0, the engine has no demonstrated skill: label it `HYPOTHESIS_ONLY` and say so in the reply. A signal tool answering `verdict: SABAR` with RR < 1.5 and confluence ~0 is telling you there is no setup — report that as the answer, not as something to reason past.

**Step 2 — convert an argument into a test.**

Any prediction claim (from a human, an indicator, or yourself) is settled by arithmetic, not debate. For a signal S and outcome O over a historical panel:

- base rate `P(O)`;
- conditional hit rate `P(O | S)`;
- sensitivity, specificity, and `lift = P(O|S) / P(O)`;
- and the false-negative count printed explicitly.

Sample-size the panel in thousands of observations, not a handful of charts. The rule that decides usefulness: **a signal with low sensitivity catches almost none of the real events even when specificity looks impressive** — "everything is fine" also scores high specificity. State both dials or the number misleads.

**Step 3 — blind test whatever still stands.** See `references/blind-test-protocol.md` for the mechanics. Hide the answer, commit the guess, then reveal. Include a null baseline.

**Step 4 — publish your own miss.**

If you run the test on yourself and score at chance, say so with the number in the reply, in the same message as the conclusion. An honest zero is what makes the negative finding credible, and it is the only version of the claim the human can actually use.

## Deliverable shape (this principal)

- **Draw it.** Present the falsification as a chart, not a table of numbers. Labels like specificity and lift do not land; two colours and a cut line do.
- Split each panel at the cut: one colour for the half that was visible, a second colour for the half that was hidden, dashed vertical cut line, verdict printed inside the panel (`valid actual 5.2x` / `cross actual 1.1x`).
- The blind-test image must carry no answer, ticker, date, or price. If the label leaks the identity, the test is void.
- Vision-check the render before sending; fix collisions first.
- Keep prose short. One idea per paragraph, and land on the consequence rather than the method.
- For a principal who says the numbers are the problem: a drawn chart is the deliverable, a numeric table is not. Never answer a "why is this so" with a table alone.

## Domain rules

See `references/market-domain-rules.md`. In one line: fundamentals are the **floor**, technicals are **what others will pay**; gold has a durable floor and no cash flow, a company can compound but its floor can be painted over a hole.

## Pitfalls

- **Hindsight contamination.** Any chart cut *after* a known collapse shows "the signal" — the annotation is written by someone who already knows. Cut the test at the moment of the decision, never at a point chosen from the outcome.
- **Chance-rate illusion.** With binary calls an unbalanced set lets one constant answer score high. Balance the classes so a trivial baseline is not already right two-thirds of the time, and print the majority-class score beside the model score. If they are equal, the method added nothing — say that sentence out loud.
- **Fame bias.** The cases every article illustrates are the contaminated ones. Prefer cuts where the outcome was genuinely contested at the time.
- **Forecast creep.** When a tool returns no setup, do not manufacture a view by layering more indicators. Telling the human charts are blind and then recommending another chart layer is self-contradiction; if it happens, name it and withdraw the recommendation.
- **Delisted tickers have no price feed.** A data API returns empty history for dead symbols, which are exactly the cases that matter. Rebuild the series from a documented month-end close table and say where it came from, rather than inventing values or silently dropping the case.
- **Label collisions at the cut line.** When horizontal position/stop labels, a vertical cut line and a fan edge converge, the annotations overlap. Offset repeated levels by a multiple of the label height, give each label an opaque background box, and re-verify with a vision pass before delivery.
