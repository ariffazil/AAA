---
name: aaa-audio-mms-ctc-witness
description: "Use when an ASR witness must not hallucinate (MMS-1b CTC)."
version: 1.0.0
forged: 2026-09-15
owner: AAA
floor_scope: [F1, F2, F10]
capability_tier: fed-long-context
ecology_state: WARM
tags: [audio, asr, mms-1b, ctc, tri-witness, falsification, hallucination-proof, penang-bm]
---

# MMS-1b — CTC Sovereign Witness (Tri-Witness Validation, third seat)

> "One witness wearing two hats" — autoregressive ASR (Whisper, GLM) hallucinates
the SAME sentence from any noise. A CTC witness physically cannot. Architecture,
not vendor, is the independence guarantee.

DITEMPA BUKAN DIBERI.

## The problem this witness solves

Whisper and GLM are both seq2seq autoregressive decoders. Under noise they
share a failure mode: they FABRICATE a fluent utterance from nothing.
Two autoregressive witnesses are not independent — they are two hats on one
head. A falsification test must use a witness whose architecture blocks the
lie, not one that merely sizes/vendors differently.

## Verified benchmark (2026-09-15, onnx-community/mms-1b-all-ONNX int8)

| Test | MMS-1b (CTC) | Whisper (autoregressive) |
|---|---|---|
| 6 noise controls (silence/white/sine/brown/pink/burst) | 0/6 sentence (4 empty, 2 garbage <=2 chars) | 6/6 hallucinated the SAME "Terima kasih kerana menonton!" |
| 2 clean BM samples | WER 0.000 | correct words (+ punctuation/caps only) |
| Resource | ~2.3GB RAM, 3s load, ~1-2s/clip | heavier |

Artifacts: `/root/audio-lane-2026-09-15/mms1b_benchmark.json`,
`/root/audio-lane-2026-09-15/mms_witness.py`.

## Hardcode (the gate)

```python
from mms_witness import MMSWitness
w = MMSWitness()
if not w.has_speech(audio):
    return "NO_SPEECH"   # CTC witness refuses — treat as falsification signal
```

Tri-Witness rule: Whisper (fast, autoregressive) + GLM-ASR (dict/code-switch)
+ MMS-1b (CTC, hallucination-proof). If MMS-1b returns empty while the
autoregressive witnesses return text, the audio is noise — HOLD.

## Iron rules

- CTC empty on clean speech = audio too short/degraded — re-feed, do NOT lower threshold.
- Never use MMS-1b as the ONLY witness — it is the falsification seat, not the transcriber.
- Keep int8 model local (RM0). Do NOT route MMS through a paid API.

## Environment pitfall (hit 2026-09-15)

`importlib.metadata.version('numpy'|'scipy')` returned None and blocked
transformers import — caused by leftover broken `*.dist-info` dirs (no METADATA)
from interrupted installs. Fix: delete the broken `numpy-2.5.0.dist-info` /
`scipy-1.17.1.dist-info` (and any dist-info without METADATA), keep only one valid.
Then `pip install --break-system-packages --ignore-installed --no-deps packaging`
if packaging itself is broken.
