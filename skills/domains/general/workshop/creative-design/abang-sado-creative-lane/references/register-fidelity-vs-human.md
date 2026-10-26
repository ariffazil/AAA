# Register fidelity — measure the clone against the HUMAN, not against itself

## The failure this file exists to prevent

`verify_take.py` compares a take against `--source` (the mint sample). A clone can be
consistently wrong and still pass every take: same voice as itself, wrong voice as the human.
This file records how that went wrong on 2026-10-20 — including one FALSE DIAGNOSIS that had
to be retracted the same night, kept here so it is not repeated.

## Rule 1 — one estimator is not a measurement

`librosa.pyin` inflates loud or shouted speech by an octave. Measured on Syed's clips: pyin
read 1.27× and 1.33× high on two of them while harmonic spacing stayed put.

Use **harmonic spacing** as the primary f0 (median gap between spectral peaks — immune to
which harmonic happens to be loudest) and pyin only as a cross-check. If the two disagree by
more than ~5%, the clip is distorted or pitch-unstable: report that, don't average them.

## Rule 2 — within-utterance range is not cross-clip range

`np.std(f0)` over a CONCATENATION of several clips measures how different the clips are, not
how expressive the speaker is. Real numbers for Syed:

| Measurement | Value |
|---|---|
| one clip, normal register | f0 sd **16.0**, p10–p90 77–121 Hz |
| concatenation of clips from different registers | f0 sd **47–50** |

A clone was labelled "flat — sd 13 vs the human's 65" on the second number. The correct
comparison was 13 vs 16: a match. The diagnosis was wrong and was retracted. Always compute
the human's reference from a SINGLE utterance in the register being judged.

## Rule 3 — find the speaker's register map before judging a clone

Syed's own clips, harmonic-spacing f0:

| Register | f0 | Where it shows up |
|---|---|---|
| normal | **~100 Hz** | ordinary firm delivery (he confirmed: "This normal") |
| raised / exasperated | 145–174 Hz | arguing, irritated questions |
| shout | ~145 Hz | sustained anger |

A clone at 98 Hz is therefore not "wrong" — it is his normal. A clone at 190 Hz is not
"better quality" — it is his raised voice. **Which register to run is a taste decision for the
person, not a correctness finding for the agent.** Measure both, name the map, let them pick
by ear; do not re-litigate it afterwards.

## Rule 4 — clause-split beats any pitch filter

Rendering sentence-by-sentence and joining with 0.32–0.42 s pauses lands closer to a real
speaker than a single long call, with zero timbre cost:

| Path | f0 | f0 sd | centroid | mfcc cos |
|---|---|---|---|---|
| human, normal | 96.9 | 16.0 | 562 | — |
| single-shot render | 97.5 | 15.9 | 480 | 0.9979 |
| clause-split render | 97.5 | 15.9 | 480 | 0.9979 (pauses restored) |

Implemented as `sado say --clause`: splits on `.!?…`, re-merges fragments under 12 chars,
renders each, joins with a silent gap, loudnorms to I=-18 TP=-2.

## Rule 5 — speed does not control pitch

Same clone, same text, five speeds (0.88/0.90/0.92/0.95/0.98) → 202/188/200/191/199 Hz.
Three repeats at 0.95 → 194/189/195. Render pitch is text-dependent, not speed-dependent. Any
note claiming a speed is "the only point inside the source band" is overfitting two renders on
different text.

## What remains once pitch and range match

Brightness. v1 measured centroid 480 against the human's 562 — ~14% dark. A high shelf
`highshelf=f=3000:g=+5` lifted it to 544 with mfcc_cos 0.9974 (identity intact). Keep that as
an **opt-in** post-filter, never a default: it flattens variation across texts.

## Emotion-register clones

A clone minted from a shouted clip does not force shout prosody onto calm text — the mad clone
(`abang-sado-mad-v1`) rendered neutral text at 171 Hz. Keep an emotional register as its own
voice id; never source the general-purpose voice from an angry clip on the theory that "it will
average out". It does not average — it bakes the strain in.

## Build the sample

Concatenate the human's own clips through
`highpass=f=65, afftdn=nr=8, loudnorm=I=-18:TP=-2, aresample=44100`, mono, 0.45 s gap between
clips. 14–20 s is enough for register; 26 s+ gives prosody. **Prefer clips from ONE register**
when building a voice for everyday use — a mixed-register sample measures wider but renders
flatter, because the engine averages the two ends.

## Mint gate

`/root/scripts/voice_clone.py` refuses any id not in `/root/.secrets/voice-mint.allow`.
Adding an id there is an authority act, not a config tweak — only on a directive from the
principal, and record it in the registry entry's `created_by`. Provider slots are finite: an
"insufficient voice slot" error means archive or delete an old clone first, and never spend a
slot re-minting something a measurement says you already have.
