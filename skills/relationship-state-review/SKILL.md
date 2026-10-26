---
name: relationship-state-review
version: 1.0.0
description: "Use when asked for the state of a relationship with X."
tags: [relationship, corpus, human, receipts, falsification, f5]
triggers:
  - "what is the state of me and X"
  - "does he want me / does he love me / why did he do that"
  - "reality loop on <person>"
  - a chat export is pasted or attached for analysis
  - a long narrative run about one person accumulates without any measurement
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Relationship State Review

The recurring ask is **"tell me the state of me and X"** about a real, named human. It arrives after
hours of narrative — what he said, what he did, what it meant — and the temptation is to answer inside
that narrative, because the narrative is fluent and the person asking is in pain.

**The measurement doctrine is owned elsewhere:** `corpus-claim-discipline` (external, AAA) owns the
dedupe funnel, attribution, two-sided test, era-check, tiers and storage rules. Read it. This skill owns
the **delivery workflow** around it: the order of operations, what a state report contains, and the
habits that make these sessions useful instead of expensive.

## 1. Order of operations

1. **Check for a corpus before you interpret.** Exports live on disk far more often than the principal
   volunteers them (`WhatsApp Chat with <Name>.txt`/`.zip` in the lane, `state.db`, a pasted transcript).
   Search first. If none exists, every sentence is `REPORTED`-tier and you say so.
2. **Parse, then count, then read.** Header regex → per-speaker volume → initiation (first-of-day and
   after a long gap) → reply latency → question counts → topic share → **affection bids and their
   returns**. Print the figures you will quote.
3. **Write the model only after step 2.** A reading formed before the count survives the count by
   absorbing it.
4. **Report: what the corpus says → what the told-story claimed → the gap.** The gap is the finding.
5. **One testable next step, with a falsifier.** Not advice. A window, a behaviour to stop, and the
   number that would prove you wrong.

## 2. The metrics that actually separate cases

| Metric | How | What it decides |
|---|---|---|
| Volume ratio | messages per speaker, and per week | a weekly ratio that stays flat is a **structure**, not a phase — a phase has a curve |
| Initiation | first message of each day; first after a >3h gap | who sustains the contact. The single most decisive number |
| Reply latency | median gap to the next message by the other party | separates *uninterested* from *busy* — a 1-minute median kills "he doesn't care enough to reply" |
| Questions | count per speaker; then read them for subject | separates *engaged* from *responsive*. Fifteen replies where none asks about the principal's inner state is a finding no narrative reaches |
| Affection bids | count warmth expressions from A; count B's returns in kind vs deflections | the cleanest available read of reciprocity |
| Topic share | count the principal's own project/work words vs the subject's | where the other person refuses to go |

**Presence and reciprocity are separate axes.** A subject can reply in one minute, remember concrete
details, drive across the city, and still never initiate and never ask a personal question. Report both
numbers; do not let the warm one stand in for the cold one.

## 3. Habits that decide whether the session helps

- **Never price the person.** No rule of the form "he gives only what costs him nothing", no score for
  who cares more, no scalar for the relationship. Every such rule is unfalsifiable by the person it
  describes and gets built to explain a contradiction rather than to resolve one.
- **Counter-evidence is a falsification instance.** When the principal answers with a concrete
  contradicting event — a cheap gift, a trip the subject turned up for, a night in the same room — say
  what it withdraws from the model. Do not fold it in as "consistent with what I said". Three in a row
  means the model is wrong, not nuanced. Say so in the same turn.
- **Never assert the subject's interior.** "He is envious", "he is afraid you'll outgrow him", "he thinks
  you will fail" are readings. Offer a small enumerated set, mark which are unfalsifiable here, name the
  one observation that would separate them, and leave motive `UNKNOWN-HUMAN-PRIVATE`.
- **Refuse the frame the principal pre-empts.** *"Don't say it's getting expensive"*, *"don't tell me he's
  busy"* — that is a red line on the explanation class, not on the wording. Give a different mechanism
  or say you have none.
- **Name the loop when it appears.** If the same question returns in five forms in one session (does he
  want me → does he like women → who will get him → why can't I have his body), the repetition is the
  finding, and saying it once plainly beats a sixth answer.
- **Distinguish "not yet measured" from "cannot be measured".** The first is a task; the second is a
  boundary. Label them differently.

## 4. Report shape

```
1. Numbers (with the denominator and the window)
2. What the numbers support — the rung reached, named
3. What the told-story claimed that the numbers don't
4. The gap, stated plainly
5. One test: window + behaviour + the number that would falsify the model
6. What is left unknown, and why no instrument reaches it
```

Lead with the number that contradicts the principal's hope or fear, not the one that flatters. Then the
next step is a *behaviour with a deadline*, never a reframe.

## 5. Seal the receipt

Write the counted figures to a JSON receipt beside the artifact — source file, sha256, window, per-metric
values, verdict line, falsifier. A later session re-runs the numbers instead of re-arguing the story.
Never write derived relationship analysis into persistent memory: memory holds the environment and the
method's home, not a profile of a person.

## Siblings

- `corpus-claim-discipline` (external) — the measurement doctrine this workflow calls.
- `governed-uncertainty`, `hermes-rasa` (external) — claim-object and interior rules.
- `persona-boundary-conduct` (external) — when the same person also appears as a fiction.
- `intimate-anthropology` (external) — subculture analysis; it stops being the owner the moment the
  question names a real man.

DITEMPA BUKAN DIBERI
