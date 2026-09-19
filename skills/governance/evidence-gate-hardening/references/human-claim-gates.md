# Claims About People Are Gates Too

The invariant in this skill — *shape is not witness; make the anchor resolve against reality* — applies
unchanged when the artifact under audit is a claim about a person rather than a code path. A
person-map is a set of assertions, each of which needs an anchor that resolves in the source before it
may be stated.

> Authority for the conduct layer lives in the human-facing doctrine
> (`hermes-rasa`, `hermes-shadow`, `governed-uncertainty`, `shadow-mapping`). This file covers only the
> **measurement**, which is the part that fails silently.

## The failure that survives review: misattributed lexicon

The most damaging defect in a person-map is not dramatic prose. It is the analyst's own organising
vocabulary read back onto the subject with the subject's name on the cover. Every individual sentence
then looks sourced, which is exactly why it passes review.

**Test.** Take the load-bearing nouns and verbs the analysis is built on, and count them in the raw
corpus, split by speaker:

```
parse the export -> split records by sender -> regex-count each key term per sender -> print both counts
```

If the map's organising words appear overwhelmingly in one party's lines and near-zero in the
subject's, the map is a portrait of that party's lexicon. Measured instance: across a two-party export
of ~4,300 messages one term the map treated as the subject's organising axis appeared **19× from the
other party and 1× from the subject** — and the subject's single occurrence was him *quoting* the
other. A second term the map called load-bearing appeared **0 times in either party's lines**.

## Rules that follow

- **A term the subject never uses is not the subject's term.** Print the count beside any claim built
  on it, or drop the claim.
- **A single hit may be an echo.** Check whether the subject's one occurrence is a quotation before
  reading it as his own.
- **Absence is a finding about the record, not about the person.** "This word appears zero times across
  three years" is true and useful. "This thing is absent from him" is a different claim and is not
  supported by the same count.
- **Measure expression, then stop.** A zero count for an affect word describes *expression*. It does
  not license "cannot receive affection" — that is a claim about an interior the record cannot reach.
  Name the rung actually evidenced and leave the capacity `UNKNOWN-HUMAN-PRIVATE`.
- **Re-run per speaker and per channel.** A corpus that pools two speakers, or two channels, hides the
  exact asymmetry the test exists to find. Channel is part of the metadata, not a detail.
- **Two instances name a shape, never a trait.** Counts support "this happened repeatedly in the
  available history". They never support "he always does this".
- **Timestamp before interpreting.** The same words mean different things depending on what preceded
  them in the same ten minutes. Reconstruct the interleaved order across every channel before drawing
  a conclusion from any single message.

## The runtime check

> *What observation would make this reading less likely?*

If the answer is "none", the vocabulary test was never run and the reading is not inference — it is a
portrait of the analyst. The gate is the same one as in §4: the anchor must resolve, and the anchor for
a claim about a person is **that person's own lines**, not the analyst's conviction.

## Reporting

When a measurement falsifies a map the principal is attached to, state the falsification plainly with
its counts, correct the artifact in place, and record the correction rather than deleting the earlier
version. A map that was wrong and is now marked wrong is more useful than one that silently changed.
