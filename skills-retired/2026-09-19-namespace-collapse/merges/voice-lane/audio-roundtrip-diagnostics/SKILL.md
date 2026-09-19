---
id: audio-roundtrip-diagnostics
name: audio-roundtrip-diagnostics
description: "Use when a TTS take needs round-trip verification."
version: 1.0.0
author: hermes
license: arifOS
tags: [tts, audio, round-trip, whisper, asr, verification, desync, timestamp]
metadata:
  hermes:
    tags: [audio, verification, whisper, tts]
    related: [nusantara-voice-stack, sovereign-tts-lanes, abang-sado-creative-lane]
    forged: 2026-09-18
    provenance: "Measured across a full persona-voice session: 16 takes, 9 alias classes, one transcriber hallucination past EOF, one false-positive INSERTED from token-count desync."
triggers:
  - TTS round-trip match percentage looks wrong
  - INSERTED words flagged but the text contains them
  - transcript has words after the file duration
  - about to re-render a take on a low match score
  - building an alias table for a voice
---

# Audio Round-Trip Diagnostics

## When to Use

Load after rendering a TTS take and **before** declaring it clean or re-rendering it. The core
discovery: a raw ~20% match on dense regional speech can be **100% after aliasing** — the take was
clean the whole time, and re-rolling would have burned a clean render.

## 1. Score the round-trip correctly, THEN judge

A raw match percentage is not a quality signal until the known substitution classes are normalised.
Six classes inflate the mismatch; two of them create **entirely false verdicts**.

| Class | Example (heard → written) | Why it matters / handling |
|---|---|---|
| **Token-count desync** | `tak ada` → `takde` (one written token heard as two) | Every downstream token shifts by one and the aligner reports the whole remainder as INSERTED. A clean take collapses to ~20%. Alias the *expanded* form back to one token: `--alias "tak ada=takde"`. Multi-word alias keys work when the matcher word-bounds them |
| **Alias direction reversed** | the flag is `HEARD=WRITTEN` | Reversing it rewrites a correct heard token into one the source lacks, manufacturing a phantom INSERTED. Read the transcript before touching the line |
| English loanword | `syut` → `shoot`, `kamera` → `camera`, `fotografer` → `photographer` | alias; never rewrite the line |
| Digit ↔ word | `11` → `sebelas`, `20` → `dua puluh`, `3` → `tiga` | the transcriber normalises digits while the source spells them; alias both directions |
| Slang standardisation | `tahu` → `tau`, `pernah` → `penah`, `itu` → `tu`, `tidur` → `tidoq` | alias; the dialect is the point, do not flatten it out of the source |
| **Engine inconsistency** | the SAME English word mangled two different ways inside ONE take (`somebody` → `sambodi` then `sambadi`) | one alias per instance — a single alias will not cover both, and this is an engine property, not an ASR error |

### The alias protocol (do this before re-rolling)

1. **Zero-alias pass.** Run the verifier with no aliases. Read the raw match, the INSERTED list, and
   the full transcript line.
2. **Diagnostic diff pass.** Print every divergent token pair in order. Do not guess.
3. **Build the table from the diff.** One alias per class. The table IS the deliverable — it
   captures what this voice does to this text, and it is reusable across every later take.
4. **Re-score with the full table.**
5. **Judge:** ≥95% + zero INSERTED → ship · 85–95% with every divergence a known alias class → ship
   · <85%, or any INSERTED that is NOT a confirmed false positive → re-render.

**A long INSERTED list with an empty MISSING list is the signature of token-count desync, not
contamination.** Fix the desync first and re-read; only then decide.

## 2. The timestamp gate — the verifier is not the sole witness for a tail

A transcriber can fabricate a whole sentence after the last spoken word, and a text-vs-transcript
diff may still report `INSERTED: none` because the aligner matched the invented tokens loosely
against real ones inside one block. **The two checks are not substitutes.**

The decisive discriminator is the **timestamp**, not the text:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 take.mp3
# then re-transcribe with word timestamps:
#   -F response_format=verbose_json  -F 'timestamp_granularities[]=word'
# compare the LAST word's end against the duration above
```

| Evidence | Reading |
|---|---|
| invented words' timestamps run **past the file duration** (measured: one ending at **117.24 s on an 87.62 s file**) | **Transcriber invention over silence.** The audio contains no such line. Do NOT cut it, do NOT report contamination |
| timestamps end at or before EOF, right where the script stopped, with real separated stamps | spent audio — hard-cut at the gap and state in the delivery line that the take is cut |
| audio energy agrees (speech ends ~0.05 s before EOF) | independent confirmation of the invention reading |

Never retract a take, and never report a checkpoint contamination, on a whole-file transcript alone.

## 3. Verify with an engine that cannot invent

Two Whisper engines share a training prior, so their agreement is **not independent confirmation** —
on non-speech both return the same fictitious sentence. Whisper is the right tool for *"the engine
mangled this"* (gross damage, both see it) but not for *"the engine did/did not say X"*.

For absence and attribution claims use an architecture-independent witness: a **CTC** model cannot
autoregressively invent fluent speech over non-speech. Look for one already staged on disk before
concluding a second witness is unavailable — the expensive part may already be done.

## 4. Speed carries emotion; F0 does not (measured)

On a cloned voice the F0 median stayed **flat (~96 Hz) across speeds 0.85–0.90** — emotion lived in
**pacing and pause**, not pitch. Practical mapping on a persona register:

| Speed | Register |
|---|---|
| ~0.90 | neutral, confident (default) |
| ~0.88 | deliberate, weighty |
| ~0.85 | most vulnerable — the mask is thinnest here |

**Never speed UP for intensity.** Escalation is slower, quieter, narrower permission — not louder.

**Slow-speed articulation drift is real:** at 0.85 final consonants degrade (`abang` → `abah`,
`cakap` → `kakak`, `mintak` → `minta`). If the mangled word is load-bearing, re-render at 0.88
rather than shipping it. If it is incidental, alias it and note it — it is a voice property, not a defect.

## 5. Pitfalls

- **Delivery is not measured by the round-trip.** STT confirms words; it cannot assess warmth,
  authority, or persona fit. Ship on the text gate, judge on the ear.
- **Never narrate the QC to the recipient.** Seed counts, retries, which take failed what — the
  requester experiences the artifact, not the search.
- **A take at 100% can still be wrong.** Match percentage says the words are right; it says nothing
  about whether the speed, register, or emotion matched the brief.
- **Alias tables are per-voice, not per-language.** Rebuild at least the desync and loanword rows for
  a new `voice_id`; carry over the rest as a starting point.

## Related

- `nusantara-voice-stack` §12 — the engine-selection and provider-lane map; load that first to choose
  a lane, this to verify what it produced.
- `sovereign-tts-lanes` — offline/owned lanes (Piper, F5-TTS) and their measured round-trip scores.

DITEMPA BUKAN DIBERI — a clean take rejected by a broken scoring pass is a render you paid for twice.