---
name: voice-register-fidelity
description: "Use when a voice clone may not sound like its person."
version: 1.0.0
author: Hermes
license: arifOS
tags: [voice, tts, clone, measurement, f0, register]
metadata:
  hermes:
    category: audio
    tags: [voice-clone, f0, measurement, prosody]
    related_skills: [voice-render-verification, voice-clone-operations, nusantara-voice-stack, abang-sado-creative-lane]
triggers:
  - this clone does not sound like the person
  - that is not my voice
  - judging whether a voice clone is faithful
  - a clone reads flat, dull, rushed, or wrong-register
  - deciding whether to re-mint a voice or fix the render
  - a person supplies their own voice note as the reference
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Voice Register Fidelity

A render can pass every take-gate and still not sound like the person. The take gate asks "is this the
same voice as the sample I cloned" — it cannot catch a clone minted from a narrow slice of a speaker,
and it cannot catch a judge who measured the speaker wrong. This skill owns the second comparison:
**render vs HUMAN**.

Rendering procedure lives in the voice-stack skills; the delivery gate lives in
`voice-render-verification`. This skill answers "is this the right person, in the right register, at
the right pace — and if not, which one of those is actually wrong."

## Procedure

1. **Get the human reference first — one utterance, in the register being judged.** Do not judge a
   voice against a concatenation of clips from different moods. If the person only supplied a mixed
   bag, ask for (or cut) a single continuous clip.
2. **Measure the reference, then the render, then compare.** Run
   `/root/scripts/voice_contrast.py <human_ref> <take...>`. Report: f0 (two estimators), f0 spread
   WITHIN the utterance, spectral centroid, pause fraction, MFCC cosine.
3. **Build the register map before calling anything wrong.** Measure several of the person's own
   clips, one at a time, and write the map down. Only then can a reading be judged "outside his
   span" rather than "higher than the one clip I happened to start with".
4. **Diagnose the ONE defect that is actually present**, in this order: wrong register (outside the
   map) → rushing (pause fraction) → dark/dull (centroid) → unstable pitch (estimators disagree). One
   diagnosis, one remedy.
5. **Apply the cheapest remedy that addresses it.** Rushing → `--clause` segmentation. Dark → opt-in
   high shelf. Outside the map → re-mint from that register. Never EQ your way out of a register
   problem and never re-mint your way out of a segmentation problem.
6. **Record the outcome in the voice registry entry**, including any claim you had to retract.

## Rules (always-on)

- **One estimator is not a measurement.** pyin inflates loud or shouted speech by an octave — measured
  1.27x and 1.33x high on clips where harmonic spacing (median gap between spectral peaks) held
  steady. Use harmonic spacing as primary, pyin/autocorrelation as cross-check, require agreement
  within ~5%, report both. Disagreement means instability; report it, never average it.
- **Within-utterance spread is not cross-clip spread.** `std(f0)` across a concatenation measures how
  different the clips are, not how expressive the speaker is: the same person measured spread 16
  within one utterance and 47-50 across a mixed concatenation. Comparing a clone against the wrong
  number manufactures a defect that does not exist.
- **Register is a taste axis, not a correctness axis.** A speaker spans 70+ Hz across moods. A clone
  matching one point of that span is faithful, not broken. Measure the map, state it in one line,
  render the option the principal picks by ear, and do not re-litigate it afterwards with a fresh
  metric — including by calling the one he liked "better quality" when it was only pitched higher.
- **Segmentation beats any pitch filter.** Sentence-by-sentence render joined with 0.32-0.45 s of
  silence restores breath and contour at zero timbre cost; a pitch filter trades pitch for flattened
  variation. Use the filter only as a safety net, and say so when you do.
- **A blended sample renders narrower, not wider.** Mixing two registers widens the measured
  reference range while the clone renders flatter than either end (spread 30 blended vs 45-50 from one
  register), because the engine averages across them. One register per voice id.
- **Never re-mint what a measurement says you already have.** Provider clone slots are finite
  (`insufficient voice slot`); when an existing id matches the reference within a few Hz, the work
  left is segmentation or brightness.
- **Correct a retracted measurement in the REGISTRY, not the reply.** The next session reads the
  entry, not the transcript. Overwrite the field that carries the wrong number and record the
  retraction in the same entry.

## Pitfalls

- **A take-gate PASS on fourteen renders proves consistency, not identity.** Tuning a clone against
  the sample it was built from is circular. The only non-circular test is against a clip of the human
  the clone never saw.
- **"It sounds flat" is a measurement problem before it is a synthesis problem.** Check the spread
  reference first; a mixed concatenation will make any faithful clone look monotone.
- **A clone minted from a continuous shout rushes every calm sentence afterwards.** The source has no
  breath in it, so the clone has none to give — pause fraction ~0.6x the human's. Fix with `--clause`,
  and if a new sample is ever taken, ask for one that contains natural pauses.
- **Speed is not a pitch control.** One clone, one text, five speeds (0.88-0.98) gave
  202/188/200/191/199 Hz, and three repeats at one speed gave 194/189/195. Render pitch is
  text-dependent. Any note claiming a speed is "the only point inside the source band" was fitted to
  two renders on different text.
- **Emotion transfers less than identity.** A clone from an angry clip renders neutral text at a normal
  pitch, so an emotional register is safe as its own voice id — but it does not give you the emotion on
  demand. Do not promise anger, tenderness or menace from a single mood-built clone.
- **An instrument that has never failed on known-bad input has not been shown to measure anything.**
  Before trusting a threshold, run the contrast tool on two obviously different voices and confirm it
  says so.

## Reference

`references/register-fidelity-measurement.md` — worked numbers: register map across four clips, spread
within vs across clips, pause-fraction bands, centroid and MFCC targets, the estimator disagreement that
caused a false diagnosis, and the sample-build chain.
