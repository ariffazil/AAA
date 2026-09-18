---
name: model-score-disclosure
description: "Use when presenting a model or score to a human."
version: 1.0.0
author: Hermes
license: arifOS
tags: [model, backtest, score, disclosure, falsification, risk]
metadata:
  hermes:
    category: governance
    tags: [model-score, backtest, disclosure, prediction, risk]
    related: [market-prediction-falsification, prediction-honesty-audit, trading-risk-review, auditable-numeric-artifacts]
triggers:
  - delivering a derived model, index, score, or formula to a human
  - a backtest or hit-rate result is about to be quoted as evidence of skill
  - a chart, percentile cone, or barrier distance is presented as a forecast
  - scoring your own predictions against a revealed answer key
  - a predictive claim needs to be stated, ranked, or priced
---

# Model Score Disclosure

Handing a derived number — an index, a barrier distance, a backtest hit rate, a percentile
cone — to a human who is about to make a real decision with it. The artifact is usually right
and the DISCLOSURE is what fails: a correct number presented at the wrong scope becomes a
false authority, and the human acts on a claim the model never made.

Applies to any model output with a person on the other end: financial risk scores, credit or
failure scores, health or fitness metrics, capacity or runway estimates, ranking models.

## The rules

1. **State what the number IS and what it is NOT, in the same breath, before the number is used.**
   A score that measures one thing will be read as measuring the thing the human cares about unless
   you say otherwise. Name the scope positively ("this is a filter") and negatively ("this is not a
   signal"), then the mechanism in one clause. A model that ranks candidates must say it does not
   time outcomes; a model that measures capacity must say it does not measure demand.

2. **A score is a filter, never a forecaster.** Percentile cones, distance-to-barrier figures and
   confidence bands describe the WIDTH of normal movement, not its direction. Say the width and
   explicitly refuse the direction — refusing is the deliverable, not a hedge. If the human asks for
   a direction, the honest answer is that the model does not produce one, plus what would.

3. **Separate the model's threshold from the human's decision.** The model may fire at a level
   ("closes at X"); that is a modelling choice, not a verdict on the person's situation. When the
   observed reality sits far from the model's threshold, say plainly that you cannot distinguish
   "my threshold is wrong" from "the input is being driven by something else" on the available data.
   Do not defend the threshold, and do not silently move it.

4. **A hit rate alone makes no money, and a small-sample hit rate is not a hit rate.**
   - Quote the rate as a rate times its payoff: `edge = p x RR x size` minus cost. A high win rate
     with a poor reward-to-risk ratio is a losing system, and saying so is the useful part.
   - Put a confidence interval on any count under ~30. Three trials at 2 of 3 correct spans roughly
     21%-94%; the sample is consistent with near-zero skill. State the trial count needed to
     distinguish the two (order of ~85 for a 2-in-3 claim) rather than reporting the point estimate
     as a skill level.
   - Separate the sample you CHOSE from the skill of the person who answered. If you selected the
     evaluation cases, the result measures your selection as much as their ability — say which.

5. **Never let a score imply survival.** A low score on a distance/runway metric does not mean the
   subject dies soon; it means the margin is thin. The correct phrasing carries the action, not the
   event: the low value means there is no time left to wait, not that the failure is near. Humans
   reliably read the dramatic version, so write the non-dramatic one.

6. **Score yourself BEFORE the answer key is opened, or score yourself zero and say why.**
   If you are measuring your own predictive skill, commit your prediction to a file (or the
   transcript) before revealing the answers. A guess stated after seeing the outcome is hindsight,
   not prediction, and presenting it as a guess is the same defect as a chart annotated after a
   collapse. When you have already seen the answer, the honest report is "no score — I did not seal a
   guess" plus what the sealed-answer machinery is for next time.

7. **Verify your own answer key before you open it.** A key assembled earlier can be wrong (wrong
   instrument, wrong window, wrong normalization). Re-derive it against the source before it decides
   anyone's score, and when you correct a key, say the key was corrected — do not quietly reissue it.

8. **Report the gate's raw verdict, including when it is unflattering.** When an automated check
   returns a non-passing verdict and your read is that the artifact is actually fine, deliver BOTH:
   the raw verdict and the reason you cleared it manually. A gate that is only ever cited when it
   passes is not a gate, and a human who discovers the suppressed verdict later discounts every
   number that came before it.

9. **Declare the untested layers with their falsification criteria, and mark them.** An artifact
   that mixes validated and unvalidated components must label which is which IN the artifact, with a
   status field a later reader cannot mistake. A correctly labelled untested layer is science; an
   unlabelled one is an overclaim, and a status line is what stops the next session treating it as
   validated.

10. **Give the human the decision, not a recommendation dressed as a number.** Present the structure
    (options, thresholds, what each implies), then stop. The model supplies the arithmetic; the
    human supplies the commitment. Where the model genuinely cannot answer the question being asked,
    say so and name what data would be required — and note when that data exists only inside an
    institution the human can access and you cannot.

## Pitfalls

| Pitfall | Why it bites | Fix |
|---|---|---|
| Quoting a score without its scope clause | The human supplies the most dramatic available reading | Lead with `this is X, not Y` before the digits |
| Moving the model's threshold to fit observed reality | You lose the ability to ever falsify the model | Report the gap as an open question and name the two candidate explanations |
| Reporting a hit rate as skill | n is small and the cases were your selection | Rate x payoff, CI on the count, name who chose the cases |
| Stating a prediction after the reveal | Hindsight presented as foresight — the exact defect you would flag in someone else's annotated chart | Seal before reveal, or score zero and say why |
| Silently normalising a gate verdict | A gate only cited when it passes is decoration | Ship the raw verdict plus your reasoning |
| Blending validated and unvalidated layers in one number | Downstream readers inherit the weakest layer's authority | Per-layer status labels inside the artifact |
| Answering "will it / won't it" because that is what was asked | Manufactures a forecast the model cannot make | Say the model produces no direction, then offer the nearest measurable proxy |

## Delivery shape

Plain language, no dashboard framing: what the number measures, what it does not, what it implies for
the decision, and where the uncertainty sits. The scope clause comes before the figure, and the
refusal of forecast comes before any interpretation. If the human's question is bigger than the
model, say which part the model answers and which part is theirs.

DITEMPA BUKAN DIBERI
