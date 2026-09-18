---
name: corpus-evidence-discipline
description: "Use when verifying claims against a message corpus."
version: 1.0.0
triggers:
  - "count how often X appears in the chat"
  - "does this person ever / never do Y"
  - "verify this claim against the export"
  - a negative finding ("zero instances") is about to be published
  - numbers from a previous analysis are being reused instead of recomputed
  - a third-party review of an analysis needs checking before it is relayed
floors: [F1, F2, F4, F5, F9]
tags: [audit, evidence, corpus, verification, epistemic]
---

# Corpus Evidence Discipline

Rules for turning a messy personal corpus (chat export, gateway log, message archive) into claims that
survive re-checking. Applies to any analysis built on these sources; the relationship-specific audit
procedure lives separately in `relationship-evidence-audit`.

**Governing law: the archive is a sensor, not the relationship.** A sensor has coverage, blind spots,
distortion and sampling bias. Missing evidence is **bidirectional** — it may raise, lower, or leave
unchanged any hypothesis. Never use absence to rescue a preferred story.

**Parsing recipe:** `references/corpus-parsing-and-metrics.md` — export/log formats, metric
definitions, ladder rungs, epistemic tags, amendment discipline.

---

## The four rules that decide whether the analysis can be trusted

Each has already produced a retraction on a live corpus. They are always-on, not situational.

### 1. A zero-count from ONE pattern is not a zero

A single regex produced the headline "never once used this word across 4,300 messages" — while the true
form was a **misspelling of the same word**. The false zero propagated into two downstream audits and an
external review before anyone caught it. A misspelt variant silently converts presence into absence, and
a negative claim is the easiest thing to publish and the hardest to retract.

Before publishing ANY zero:

1. List the spellings, elisions, abbreviations and code-switch forms you tested — and put that list in
   the output, not just the count.
2. Run the pattern against a **known positive** occurrence to prove it matches at all.
3. Loosen to a stem (`wor[ks]*hip`) and re-count.
4. Report the number with its method: "0 hits for `<pattern>`".

If you cannot name the pattern behind a zero, you have an untested search, not a zero.

### 2. Never inherit a figure — recompute from source, and state the definition

Numbers handed down from a previous pass are the most plausible-looking wrong thing in the file.
Recomputing from source overturned four inherited figures at once: the day-opener count, the active-day
denominator, an affection-token total, and a body-message total. Two consequences:

- **Define the metric before counting it.** An "active day" is a day with N messages — say which N, and
  say what the count becomes under the neighbouring definitions (≥1, ≥2, ≥5). A denominator nobody
  defined is the source of most count disputes.
- **Write the drift down.** When a figure moves: old value, new value, the definition, and the effect on
  any confidence built on it — as a dated amendment. Audit files are append-only; never overwrite the
  earlier text, because a later session needs to see the drift in order to trust the file at all.

### 3. "Spontaneous" is a claim about CONTEXT, not about the keyword

A callback ("remember when…", "lama tak…") counts as self-generated evidence only if the topic was not
raised in the immediately preceding turns. Counts cannot show this; the surrounding thread can.
Classify every hit **SPONTANEOUS / PROMPTED / AMBIGUOUS** by reading ±10 lines, quote the thread in the
deliverable, and never upgrade a prompted hit by dropping that fact. The keyword returns the line; only
the context returns the meaning.

### 4. A review of your own analysis inherits your errors

An external reviewer's *method* may be sound while its *inputs* are yours — expect it to repeat your
wrong counts verbatim and to miss the very error it is reviewing. Before relaying any review: re-run its
specific claims against source, endorse the method, correct the arithmetic, and say plainly which is
which. A review is a second pass over the same sensor with the same blind spots, not an independent
witness.

## Ladders instead of verdicts

For any contested behaviour, define the rungs *before* looking, then report the highest rung the evidence
reaches and name the higher rung that is NOT reached.

```
0 no evidence  ·  1 tolerated  ·  2 responded positively  ·  3 independently created another occasion
4 independently initiated or requested  ·  5 noticed absence and attempted to restore
```

Acceptance is not longing. Adjacent-but-different categories (insecurity, logistics, self-criticism,
ordinary chat about the topic) stay OUT of the ladder unless the interaction itself establishes a
request. Acceptance at rung 1 does not license a sentence about rung 5.

## Voids

Separate and name them: **visual** (media stripped) · **vocal** (tone) · **physical** (offline life) ·
**temporal** (gaps, channel switches) · **internal-state** (motive). For every hypothesis, state whether
the missing channel could RAISE **or** LOWER confidence — always both directions. One-directional
"the missing media probably shows more" is the failure this section exists to catch.

**Prove a void is structural before calling it unrecoverable.** Open the archive container itself
(`zipfile.ZipFile(p).namelist()`) and report what it holds. If it contains only the `.txt`, the media
are permanently absent — that is a finding, and every hypothesis depending on them is closed. "I could
not find it" and "it is not in the artifact" are different statements.

## Inflections: dates, not causes

A behaviour channel that stops is a locatable fact; the reason is not in the corpus. Record the last
instance (date + verbatim), the counts by year and by side, whether both sides stopped together or one
side stopped first, and the events within ±10 days — explicitly marked **sequence, not cause**. Give any
causal story low confidence and label it a hypothesis. A channel that stopped being co-produced is a
different finding from one side being refused.

## Counterfactuals

Never manufacture a test. Hunt for periods that already occurred: a behaviour that stopped unannounced,
long silences. Silence-based claims need a who-spoke-first-after-each-gap computation — quote the return
line and report the exceptions ("7 of 9, plus the two that went the other way"), never a clean n/n. If
no natural counterfactual exists, write **NO NATURAL COUNTERFACTUAL AVAILABLE**; that is a result, not a
gap to fill.

## Privacy

Move any personal export out of `/tmp` into the working directory with `chmod 600` (dir `700`) before
parsing. Keep the analysis at the same classification as its source, and never widen a private detail
into an output another room can read.

## Output discipline

- Tag every claim: OBSERVED · SELF-REPORTED · STRONG INFERENCE (state the causal bridge) · WEAK
  INFERENCE · UNKNOWN. Use UNKNOWN aggressively; do not repair missing information with narrative.
- Keep the two sides' columns physically separate. Never let one party's desire migrate into the other
  party's signal column without independent evidence.
- Frequency is not meaning: high initiation ≠ attachment, low affection vocabulary ≠ low care, silence ≠
  rejection. Count first, interpret second, challenge the interpretation third.
- Where a rung needs a comparison baseline that the corpus does not contain, the honest verdict is
  **not testable in either direction** — not "unsupported".
