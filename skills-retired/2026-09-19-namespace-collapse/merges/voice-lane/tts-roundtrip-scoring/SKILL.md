---
name: tts-roundtrip-scoring
description: "Use when scoring a TTS take against its script."
version: 1.0.0
owner: AAA
category: voice-stack
tags: [tts, asr, roundtrip, scoring, dialect, verification]
floor_scope: [F2, F4, F7]
autonomy_tier: T1
---

# Scoring a TTS round-trip

Load when a synthesised voice artifact is verified by rendering → transcribing → diffing the
transcript against the input script. This is the SCORING discipline. For deciding whether a
suspicious phrase is really in the audio (slice-and-re-read, duration budget, witness
independence), use `machine-read-verification` — that skill owns insertion adjudication and is
not duplicated here.

## The metric law

**The gate is INSERTED = 0, not the raw match percentage.**

A low raw score with zero insertions is a CLEAN take. A high raw score carrying one inserted
clause is a REJECTED take — an insertion means the audio says something the script never did,
which is the one failure that cannot be explained by transcription surface.

Score in this order:

1. Apply the alias table (below) → recompute the normalised match.
2. Read the transcript for INSERTED clauses specifically. Zero insertions = pass the hard gate.
3. Only then consider the normalised percentage: ≥95% ship · 85–95% ship if divergences are
   non-lexical · <85% block and re-render on another lane.

## The five false-FAIL classes

On real colloquial/dialect text the raw score collapses for purely surface reasons. Every row
below is a false FAIL. Build the alias table BEFORE concluding anything about the engine.

| Class | Script | Heard | Cause |
|---|---|---|---|
| English loanword spelled in target-language letters | `alpha` | `Alfa` | ASR respells to its own orthography |
| Colloquial normalised to standard | `mintak`, `takde`, `pastu`, `datang la` | `minta`, `tak ada`, `pas tu`, `datanglah` | transcriber corrects the dialect |
| Particle / slang respell | `je`, `hang`, `tau` | `yeh`/`ja`, `Hank`, `tahu` | genuine phoneme ambiguity |
| Transcriber adds a syllable | `Bahu` | `Bahawa` | pronunciation, not content |
| Spelled digit normalised | `tiga`, `sepuluh` | `3`, `10` | number formatting |

Measured on real colloquial Malay: a long take scored **66.6% raw → 99.8% normalised** with
zero insertions, and a short line scored **24.7% raw → 99.4% normalised** and was likewise
clean. Raw percentage is not evidence of engine quality on dialect text.

## Do not rewrite the script to raise the raw score

Pre-normalising dialect into standard language destroys the register the take exists to carry,
and it optimises the wrong quantity. Write the colloquial form, alias it, and report the
normalised figure. If a native-speaker register matters, the dialect stays in the script.

## An alias table is a claim about the transcriber — keep it falsifiable

Only alias a substitution you have already seen recur across independent passes. Aliasing a
real divergence away hides the exact defect the gate exists to find.

**A normalised score LOWER than the raw score is the signal that the alias table itself is
wrong**, not the take. Measured: 24.7% raw → 15.8% with one bad alias entry → 99.4% once
corrected. Treat that inversion as a diagnostic, not a rounding error.

For every alias, record the classes applied alongside the number, so a reader can re-derive it.
A bare normalised percentage is not auditable.

## Substitution vs respell

Respells normalise away (the table above). A word the script did not contain is a different
event and must be isolated before it is called an insertion — slice the suspect window and
re-read the slice. See `machine-read-verification` for that procedure and the duration-budget
cross-check.

## Check the channel's resolution before promising prosody control

The free edge-tts lane emits **`SentenceBoundary` only** for its `ms-MY` voices — no
`WordBoundary` events — while an English voice on the same client emits them. (Verified across
two Malay voices.) Any prosody feedback loop built on that lane therefore has sentence
resolution at best, never word-level. Probe the event stream before designing against it.

## Pitfalls

- **A single pass of one model family is not a witness.** Re-running the same request, or
  stepping within a family (turbo → non-turbo), reproduces the same artifact.
- **A low score is not a verdict on the engine** until the alias table has been applied and the
  transcript read for insertions. Reverse that order and you will re-render clean takes.
- **Never report a normalised score without the alias classes**, and never report a raw score as
  if it were the quality of the audio.
