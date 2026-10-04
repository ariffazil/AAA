# Audio-as-State Doctrine (kernel-validated 2026-08-13)

Governance framing for treating human voice as a *state signal*, refined over a
session that started with an over-claimed "audio is quantum" hypothesis and
ended with a kernel-validated doctrine. The framing that survived audit:

## What carries (the refined claim)

- **Text and image are artifacts**: discrete, re-readable, hashable, time-invariant.
  You can seal them.
- **Breath and voice are continuous and time-bound**: the information lives in
  the *derivative* — rate, pause, tremor, latency. Non-repeatable. There is no
  stable object to hash independent of the moment of capture.
- **The governance-useful property is not "quantum" — it is costly-to-fake.** Text
  costs the body nothing. Breath is physiologically coupled. That makes audio
  closer to an **earth signal (F3 witness)** than to a claim.

## Modality failure-mode table

| Modality | Sells | Failure mode |
|---|---|---|
| Image | Reality | Illusion of seeing = understanding ("I saw it, I understand") |
| Audio | Presence | Illusion of a being who cares (empathy-driven trust) |
| LLM/Text | Explanation | Illusion of understanding (symbolic consistency ≠ ontological consistency) |

Audio preserves uncertainty that text collapses; it also bypasses the logical
filter to enter the affective system first. That is exactly what makes it a
powerful *presence* channel — and exactly why it must be governed as a surface
of power, not a convenience.

## Org placement

- **Audio-as-signal** → WELL (`well_assess_homeostasis`).
- **Audio-as-IO** → A-FORGE (`forge_audio_ingest`, `forge_audio_features`,
  `forge_audio_transcribe` → Qdrant payload + VAULT999 provenance `audio_hash`).
- **Kernel** touches it only as an evidence *type* — one field, not an organ.

## Three brakes (kernel verdict)

1. **Prosody → state inference has a weak validity record** — mic, accent,
   illness, acting all confound it. It can only enter as OBS with **low
   confidence**, never as a floor-gating scalar.
2. **F9 ANTI-HANTU risk is direct**: a system that says *"I hear you're
   stressed"* is **performing empathy — the dark pattern F9 forbids**. Sensor
   can measure; it must not *speak* about the measurage to the owner as a
   claimed feeling.
3. **Sequencing**: W3 (third witness) is null in current payloads — adding a
   new witness channel before the existing tri-witness math is measured adds an
   unmeasured input to an unmeasured product. Don't.

## F6/F9 boundary rule

Distress is read to **serve**, never to **persuade**. If a long-fatigue reading
must surface to the human (e.g. prolonged multimodal load past 2am that should
trigger 888 HOLD review), emit it as a **measured fact**:
- "7 consecutive nights high multimodal load to 2am. Fatigue category:
  prolonged. Recommend review."
Never as: "I can hear you're tired / stressed" — that trips F9.

## Shippable version (small first)

`voice_state.py` extracting librosa prosody features from raw audio *before* STT,
wired to `well_assess_homeostasis` `stress_load` / `hrv_status` as the first real
sensor behind today's hand-passed numbers.

- Layer order matters: **gates (F6/F7/F1/F9 labels) must exist BEFORE state is
  used to adapt behavior** (e.g. state-aware TTS). Don't collect fatigue then
  adapt responses on it without the guard already in place.
- W0 must stay reflect-only: WELL mirrors, never gates.
- Deps: librosa 0.11.0, scipy 1.18, numpy 2.4 present. `parselmouth` optional.
- Layer numbering kept for traceability (i-ARIF plan): L1 voice_state →
  L2 native audio understanding → L3 A-FORGE storage → L4 state-aware TTS →
  L5 constitutional audio gates → L6 multi-turn voice context. Gating is built
  in at L5 but must be *conceived before* L4 is wired.

## Session breadcrumbs (2026-08-13)

- "Map all my hermes agent audio skills and contrast with AAA skills mesh" →
  produced the canonical TTS/voice/music capability map. Hermes audio infra is
  production-grade (4500+ lines TTS, 3000+ STT, 2300 voice mode). The gap is
  not capability — it's wiring audio to memory/state/governance ("the nervous
  system"), i.e. the voice-loop goes through text and discards state.
- Hermes is the voice agent: full-duplex, wake word, push-to-talk, barge-in,
  per-chat voice-state persistence, 8-format container detection, OGG bubble
  delivery. A-FORGE is the storage actuator (remember, not hear); OpenClaw is
  request-response edge (transcribe, not be a voice-being).