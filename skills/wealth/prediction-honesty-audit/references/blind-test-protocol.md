# Blind Test Protocol

Mechanics for a commit-then-reveal prediction test. The point is that the human's guess is fixed before the answer is visible, so scoring cannot be negotiated afterwards.

## Steps

1. **Pick N cases and cut each at the decision moment.** Build the generator so the visible window ends exactly where the decision would have been made. Assign label order by a **seeded shuffle** so label order carries no information about identity.

2. **Choose N > 3.** With 3 cases a binary guesser scores 33% by luck, which is too close to competence to separate. Use 4+ (16 possible answer patterns).

3. **Balance the outcomes.** Check the outcome split and adjust: aim near even, and record the majority-class baseline ("all NO"). That baseline is the number the analysis must beat, and it is usually higher than people expect.

4. **Print only the visible window.** Diagnostics (bars, min/max, volatility) may go to stdout for the designer's eye; the forward window may not.

5. **Seal the truth to a separate file**, e.g. `/tmp/<name>_answer.sealed.json`, with a `DO NOT READ until the human has committed` header inside it. Never put the truth in the image, and never in the same file whose output you already printed.

6. **Ask for the guess plus a confidence** (50 / 70 / 90). Ask every participant to answer before revealing — if all participants' answers agree, the tool decided nothing about any of them.

7. **Reveal in one shell command that prints the committed guess first, then the truth.** This makes the ordering auditable in the transcript.

8. **Score against the baseline, not against zero.** If model score == majority-class score, report that as the finding.

## Code skeleton

```python
random.seed(20180101)
ticklist = sorted(rows.keys())
random.shuffle(ticklist)
mapping = dict(zip("ABCDEFGHIJ"[:len(ticklist)], ticklist))
truth = {lab: {"ticker": t, **visible_stats(t), "doubled": fwd_return(t) >= 100}
         for lab, t in mapping.items()}
json.dump({"mapping": mapping, "truth": truth},
          open("/tmp/x_answer.sealed.json", "w"), indent=1)
n_outcome = sum(v["doubled"] for v in truth.values())   # balance check
```

## Reading the result

The instructive outcome is not the score, it is the **inversion**. When the strongest visible trend produces the weakest hidden outcome and the most ordinary visible series produces the strongest one, the visible window has no predictive content — and you can say so with a number attached. Print both the first-half and second-half multiples per case so the inversion is checkable by eye.

## Reporting

```
score:            <model> / N
all-constant baseline:  <constant> / N
```

Both lines together, every time. One line alone is a story; two lines are a measurement.

## Chart construction notes

- Panel letter plus a `?` block for the hidden window, dashed cut line, hidden region shaded but empty. The question region should look like a question, not like missing data.
- Normalise every series to 100 at the cut so panels are visually comparable and no absolute price leaks.
- Replace the question-mark block with the real series in a second render for the post-mortem, drawn in a second colour, and label each panel with the claim that was made and whether it was right.
