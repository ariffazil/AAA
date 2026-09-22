---
name: blind-prediction-testing
version: 1.0.0
description: Use when a claim of predictive skill needs testing.
triggers:
  - "can X predict Y"
  - "technical analysis can tell when a company dies"
  - "our model gives high signal quality"
  - "I can see the market"
  - "I saw it coming"
  - any claim of forecast skill from a person, a chart, a signal, an organ or a model
  - a calibration, accuracy or hit-rate figure quoted without its baseline
  - whenever you are about to agree that a signal works
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Blind Prediction Testing

Never debate whether a signal predicts. Measure it.

An argument about predictive power is unwinnable as an argument, because the person who already
knows the outcome will find their pattern every single time. Hindsight guarantees the pattern. So
"I can see the signal" and "the signal is not there" are both defensible in conversation, and only
one of them is true. Counting is what separates them.

## 1. The three failures this prevents

**Hindsight bias.** A chart of a collapsed company, drawn after the collapse, will always show the
technical pattern that "should" have warned. The pattern is real and worthless at the same time —
you cannot tell which without counting the false positives the same rule produced on the survivors.

**Accuracy without a baseline.** "I got 6 of 8" is not a finding. If always answering the majority
class also scores 6 of 8, skill is exactly zero. Report no hit rate without the trivial baseline
beside it, and compute the baseline in code rather than in your head.

**Rare-event base rate.** A collapse signal that is right 30% of the time is strong when the base
rate is 4% and unremarkable when it is 25%. Report the base rate or the number means nothing.

## 2. The protocol

1. **Fix the outcome and the horizon before looking.** Make it binary and pre-declared ("did the
   price fall at least X% within N months") so the target cannot drift after the fact.
2. **Use at least four items.** Three items can be won one-in-three by guessing. Four binary items
   give 16 combinations. More is better; when the ask is a demonstration, say plainly that it is a
   demonstration and not a test of the signal.
3. **Anonymise.** Strip names, tickers, dates and absolute prices. Normalise each series to 100 at
   the decision point. Label them A/B/C/D.
4. **Assign labels by a SEEDED shuffle.** A hand-ordered label list leaks the answer through its
   ordering, and the leak is invisible to whoever wrote it.
5. **Cut each series at the decision point and show only the visible window.** The entire test is
   whether the visible half constrains the hidden half.
6. **Seal the answer to a separate file and say that it is sealed.** The predictor commits in
   writing before anything is revealed. A test whose answer is reachable is not a test.
7. **Take the prediction. Then reveal.** Score it.
8. **Publish both the score and the baseline.** Including the all-one-class baseline explicitly —
   that is the number which tells the reader whether the exercise did anything at all.
9. **Report the result against your own hypothesis first.** If you bet the signal would work and it
   did not, that leads the message. You are the party most likely to be flattered by a positive
   result, so state your own prediction before you score anyone else's.

## 3. Scoring a signal (not a quiz)

For a rule applied across many observations, report all five — accuracy alone is not one of them:

| Metric | Meaning |
|---|---|
| base rate | share of all cases that had the outcome |
| PPV | outcome share *given* the signal fired |
| lift | PPV / base rate |
| sensitivity | share of the actual outcomes the signal caught |
| specificity | share of non-outcomes the signal correctly cleared |

Lift on its own misleads. A rule with 5x lift and 28% sensitivity misses 72% of the events it exists
to catch. State both, and translate the PPV into plain words — "two of three times the signal
fires, nothing happens" — because a percentage does not carry the consequence.

Before any of this, sanity-check the inputs: a rule that flags a whole quadrant of the data as the
most dangerous class, and flags nothing there, has a sign or units error in its own definition.

## 4. Known limitations belong on the artifact, with the direction of the bias

Backtests are usually built from data that exists only for the survivors. When the dead cases are
missing from the panel, that limitation goes ON THE RESULT, not in your head:

> LIMITATION: the source serves no history for delisted tickers. This panel is survivors only, so
every case that actually died is absent — the test is biased AGAINST the signal, not for it.

State the direction. A limitation note that does not say which way it pushes is decoration, and a
reader will reasonably assume it pushes your way.

## 5. Pitfalls

- **Do not let the predictor see the answer and do not drop hints.** No "close", no warm/cold, no
  "you got most of them". The whole value is in the commitment being made before the reveal.
- **Do not let a quiz become a finding.** A handful of charts demonstrates a mechanism. A signal
  needs hundreds of observations. Say which one you are delivering.
- **A degenerate output is your bug, not a discovery.** A derived score that returns infinity, zero,
  or assigns one class to an entire slice of the data is almost always a sign or units error in your
  own derivation. You will be strongly tempted to write up the degenerate result as an insight.
  Check the formula first, and if you shipped the bad version, say so in the same message.
- **Report the falsification that killed your own idea in the same breath as the idea.** If a
  classification you designed to catch the most dangerous cases catches nothing, the failure is the
  deliverable. Lead with it rather than quietly dropping the hypothesis.
- **A survivor of the test is still weak evidence.** Report the numbers and stop. Do not upgrade
  "modest lift on a survivors-only panel" into "reliable" on the way out.
- **Do not confuse the absence of a signal with the absence of a mechanism.** A rule can be real and
  still not separate the outcomes; say which of the two you actually measured.

## 6. Reusable scaffold

`scripts/blind_test_scaffold.py` builds the harness: seeded label assignment, a sealed truth file,
and a scorer that prints the trivial baseline beside the score and names when no skill was
shown. Adapt the loader; keep the seal.
