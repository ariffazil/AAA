# Prediction Test — designing an experiment that can fail

Use when a capacity to forecast is claimed — by an agent, an indicator, an organ, a person, or your
own analysis — and belief is not good enough. The deliverable is a scored experiment with a stated
baseline, not an explanation of why the claim is plausible.

## The build

1. **Pick real cases, then hide the outcome.** The stimulus is a genuine series truncated at a cut,
   with everything after the cut withheld. Anonymise: no names, no tickers, no dates, no price
   units. Normalise to 100 at the cut so the reader sees shape and nothing else.
2. **Label by seeded shuffle** — `random.seed(N); random.shuffle(items)` — and record the seed in the
   artifact footer. Unshuffled labels leak ordering information.
3. **Keep the visible windows comparable.** Panels cut from the same data at very different lengths
   cannot be compared; a short window is harder to read, not harder to predict.
4. **Seal the answer to its own file.** Write `{mapping, truth, seed, windows}` to a separate path and
   state in the rendered artifact that the answer is not in the image. Never print the answer from
   the same script, or into the same output, the human is reading.
5. **Commit the guess in writing BEFORE the reveal.** This is the step that separates a test from a
   story — take the human's calls and the agent's calls first, then open the seal.

## The scoring

| Term | Meaning |
|---|---|
| score | items answered correctly |
| constant baseline | correct count from answering the single majority outcome every time |
| chance | `1 / 2**n` for `n` binary items |

Report all three. **The finding is the gap between score and baseline.** Zero gap means the analysis
was decoration — that is a complete, publishable result, and it is the outcome to lead with.

## Balance check — run this before trusting the test

If the majority outcome exceeds roughly 70% of items, the constant baseline is nearly optimal and the
test **cannot separate skill from habit**. Either balance the set across both outcomes, or report the
imbalance and label the result inconclusive.

This is the most common way a prediction test fails to falsify: an unbalanced set flatters whoever
guesses the majority — including a model, and including a coin with a bias.

## Failure modes of the test itself

- **Outcome imbalance** — see above.
- **Label leakage** — panel ordering, unequal series lengths, a footer naming the window.
- **Seal leakage** — the answer rendered by the same script that produced the artifact.
- **Post-hoc storytelling** — explaining why a missed item "was actually ambiguous" after the
  reveal. Score it as a miss and stop.
- **Claim drift** — a test of *direction over one horizon* reported as a test of *skill*. Restate the
  exact question asked when reporting the score.
- **Too few items** — three binary items give 8 possibilities; four or more before any claim of skill
  survives.

## What a refutation owes the reader

1. Score, baseline and chance level, side by side.
2. The mechanism the failures exposed — not "I was wrong", but *what property of the data made the
   guess impossible* (e.g. the visible half carried no information about the hidden half; the
   strongest first half produced the weakest second half).
3. What the claim is reduced to afterwards: usually **a trigger, not a verdict** — a signal can be
   legitimate as a reason to act while remaining worthless as a prediction.
4. The consequence for the decision at hand, in one line, without re-litigating the test.

## Reuse: falsifying a gate

The same harness falsifies any threshold, rule or gate. Hold out the outcome, commit the pass/fail
prediction, score against the constant baseline. A control that has only ever been observed to pass
is indistinguishable from no control, and this is the cheapest way to show it. Pair it with a
negative-control set of deliberately-broken inputs that MUST be rejected — see
`visual-artifact-delivery` `references/content-gates.md`.
