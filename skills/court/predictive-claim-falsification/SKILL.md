---
name: predictive-claim-falsification
description: "Use when someone claims X predicts Y. Test it blind."
version: "1.0"
author: "hermes-curator"
metadata:
  hermes:
    tags: [falsification, prediction, blind-test, base-rate, trading, verification]
    related_skills: [infographic-generation, hermes-response-format-fit]
triggers:
  - "can you predict"
  - "boleh tak ramal"
  - "this signal predicts"
  - "my model forecasts"
  - "does TA work"
  - "backtest proves"
  - "prove this technique works"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Predictive-Claim Falsification

> **Trigger:** Anyone — you, another agent, a model card, a human expert — asserts that something *predicts* an outcome. Also load when a human asks "can you predict X?" and you are tempted to answer with an opinion.

## The rule

**A prediction claim is a measurable claim. Measure it or say UNKNOWN — never answer from plausibility.**

The two failure modes this kills:

| Failure | What it looks like | Fix |
|---|---|---|
| **Anecdote dressed as method** | One famous case where the signal fired before the event | Population test |
| **Analysis scoring at baseline** | You predict, feel skilful, never compare to a dumb rule | Committed blind test |

## Test 1 — Population lift test (does the signal carry information?)

Never judge a signal on selected cases. Compute across the whole panel:

```
base rate          = P(outcome)                  # how often it happens at all
P(outcome | signal)                              # the signal firing
P(outcome | no signal)                           # the control row
sensitivity = TP/(TP+FN)   specificity = TN/(TN+FP)
PPV = TP/(TP+FP)           lift = P(outcome|signal) / base_rate
```

Data source: `yfinance` monthly closes (`period="max"`) for equities — include survivors AND decliners.

Run `scripts/signal_lift_test.py` — computes all of the above and prints the control row beside the signal row.

**Interpretation floor:** lift near 1.0 = the signal carries nothing. Lift 1.5–2× with high specificity but low sensitivity is a *weak filter*, not a predictor. Specificity is worthless without the denominator — always print `n` beside every rate.

## Test 2 — Committed blind test (does the judge beat a coin?)

1. Choose N cases by a **rule**, not by memory of the outcome.
2. **Cut each series at the decision point.** Show only the visible half. Hide the rest — no ticker, no dates, no prices, no axis labels.
3. **Assign labels by seeded shuffle**, never alphabetically and never in ticker order. Label order must carry zero information.
4. **Commit the predictions and a confidence level BEFORE reading the answer.**
5. **Seal the answer to a separate file** (`*.sealed.json`) — never the same stdout the renderer reads. Confirm the rendered artifact leaks nothing.
6. Reveal, then score against the **trivial baseline**: the always-most-common-class answer.

Run `scripts/blind_prediction_test.py` — cuts, seeds, prints the visible profile only, writes the sealed answer file, and carries the scoring snippet in its footer.

**The number that matters is the delta against baseline, not the score.** A 6/8 score looks like skill; 6/8 from saying "no" eight times without looking is the actual finding. Report both in the same breath.

## Hindsight checks before accepting any chart or case as evidence

- **Date the artifact.** A chart drawn after the event shows the signal because the author already knew. Compare the timestamp printed on the chart against the event date; if it postdates, the chart is a *lesson*, not a forecast.
- **Count the false positives the same signal would have produced.** A rule that fires on every healthy company during its long rise tells you nothing when it fires before the collapse.
- **Outcome-based selection is the default failure.** If the cases were picked because they died, the test measures nothing.

## Scope guard — what falsification does NOT prove

Passing Tests 1–2 does not license the reverse claim:

- **Do not convert the finding into the opposite product.** "This cannot predict, but it can prevent ruin" is a different claim with its own evidence burden. A gate is not an oracle — asserting both in one breath is the contradiction the human will catch.
- **Stay precise about the domain.** "Cannot be predicted from price alone" is safe. "This asset has no fundamentals" is false for any quoted pair — a commodity inherits the macro of its quote currency (policy rate, CPI, employment, the currency). Over-broad negatives get corrected by the domain expert in the room.

## Pitfalls

- **Answer file in the same output as the artifact** → the renderer prints the answer and the test is void. Separate files, always.
- **Alphabetical or ticker-order labels** → the label leaks identity and the "blind" test becomes a memory test.
- **Reporting a score without its baseline** → the reader cannot separate skill from guessing. Print both.
- **Printing rates without denominators** → 7.5% on n=332 reads like a finding; the same rate on n=8 does not.
- **Letting the predicting agent see population results first** → it anchors on the answer. Commit before revealing.
- **Treating "no successful practitioner does this" as proof** → a strong prior, not a measurement. Pair it with the test.
- **Sampling only survivors or only decliners** → include both classes in every panel test.

## Reporting to a human

The human wants the consequence, not the statistic:

1. The two tests in one line each, with the baseline comparison explicit.
2. What survives — the *process* that limits loss, if any.
3. What the claimant got right, by name. A falsified prediction claim is not a verdict on a person; the domain expert is often right about a different question than the one you tested.

## Scripts

- `scripts/signal_lift_test.py` — base rate vs conditional rates, sensitivity/specificity/PPV/lift across a ticker panel.
- `scripts/blind_prediction_test.py` — cut series, seeded-shuffle labels, sealed answer file, baseline scoring snippet.
