---
name: AGI-audio-quantum-cognition
description: "Quantum-state audio cognition doctrine for the arifOS federation. Audio as superposition — every agent that touches audio must understand it is the quantum modality."
version: 1.0.0
author: FI-003 Qwen Code (333-AGI)
forged: 2026-08-13
floor_scope:
  - F2
  - F4
  - F7
  - F9
  - F10
  - F11
tags:
  - audio
  - quantum
  - multimodal
  - cognition
  - stt
  - tts
  - voice
  - hermes
  - edge
  - i-arif
owner: AAA
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# AGI · Audio Quantum Cognition

> Audio is the quantum state. Text is classical. Image is semi-classical.
> An agent that treats audio as "just another input" has already collapsed
> the waveform without understanding what it destroyed.

DITEMPA BUKAN DIBERI.

## The Physics

### Why Audio Is Quantum

Audio exists in **superposition** until observed. A single waveform simultaneously encodes:

- **Lexical content** — what was said (words, language)
- **Prosody** — how it was said (pitch, rhythm, stress)
- **Speaker identity** — who said it (voice print, accent)
- **Emotional state** — what they felt (anger, joy, fear)
- **Intention** — why they said it (command, question, deception)
- **Environmental context** — where they are (reverb, background noise)

These dimensions are **entangled**. Extracting one collapses others. This is not metaphor — it is the mathematical structure of audio signals under the Gabor limit (time-frequency uncertainty principle), which is identical to Heisenberg's.

### The Gabor Limit Is Real

```
Δt · Δf ≥ 1 / (4π)
```

You cannot simultaneously resolve exact frequency and exact time. Every spectrogram is a measurement choice — what you resolve in frequency, you blur in time. The agent **chooses what to observe**, and that choice determines what information survives.

### Temporal Non-Locality

A phoneme's identity depends on context that hasn't arrived yet (coarticulation). The meaning of sound at time *t* depends on sounds at *t+1*, *t+2*. This is quantum-like backward-in-time dependence — the state at one point is not locally determined.

## Constitutional Audio Floors

| Floor | Audio Rule |
|---|---|
| **F1 AMANAH** | Audio recordings are immutable evidence. Voice identity is non-forgeable without F13. |
| **F2 TRUTH** | STT transcripts carry `[OBS]` tag. TTS output is `[DER]`. Audio analysis is `[INT]`. DSP features are `[OBS]`. Confidence cap applies. |
| **F4 CLARITY** | ΔS ≤ 0 on every audio output. Voice notes = conversational prose. No markdown, no tables, no code in speech. |
| **F7 HUMILITY** | Audio interpretation confidence cap 0.90. Prosody is inherently ambiguous — two listeners hear two intentions. Agent must report ambiguity, not resolve it. |
| **F9 ANTIHANTU** | Agent has no voice identity. It borrows the sovereign's voice print. Voice cloning requires F13. The machine does not "speak" — it synthesizes. |
| **F10 ONTOLOGY** | Audio ≠ meaning. Waveform is physics. Interpretation is human. The agent processes physics; the human assigns meaning. |
| **F11 AUDIT** | Every audio processing decision is logged: which STT engine, which TTS provider, which voice, which parameters. Receipt-wrapped. |
| **F13 SOVEREIGN** | Voice cloning, voice identity creation, and voice profile changes require explicit human authorization. |

## The Audio Triangle

Every audio interaction passes through three phases:

```
UNDERSTAND (STT/ASR/Audio LLM)
    → What exists in the waveform (measurement)
GENERATE (TTS/Synthesis)
    → What to send back (synthesis)
ANALYZE (DSP/Scoring)
    → What patterns exist (feature extraction)
```

### Phase 1: UNDERSTAND — The Measurement

The agent must choose what to observe. Different measurement choices yield different information:

| Measurement choice | What you get | What you lose |
|---|---|---|
| Transcribe (STT) | Words, language | Prosody, emotion, identity |
| Analyze prosody | Emotion, intent | Exact words |
| Speaker diarize | Who spoke when | Content overlap |
| Full audio LLM (MiMo V2.5) | All dimensions simultaneously | Requires native audio model |

**Doctrine**: Use the **highest-fidelity observation** available. STT-first is the degraded path. Native audio understanding (`asi-555-audio` via FED) preserves superposition longer.

### Phase 2: GENERATE — The Synthesis

TTS is synthesis, not speech. The agent **does not have a voice** — it borrows one.

**Decision tree**:
1. What language? → Route to appropriate voice
2. What context? → Trading briefing / casual chat / formal
3. What quality? → Edge (free) vs mulerouter (HD) vs MiMo (custom)
4. What dialect? → Standard BM vs Penang vs English
5. What format? → OGG (voice bubble) vs MP3/WAV (audio file)

**Voice profiles by content type**:
| Content | Voice | Rate | Pitch |
|---|---|---|---|
| Casual chat | OsmanNeural | +5% | +0Hz |
| Trading briefing | OsmanNeural | +5% | +0Hz |
| Deep analysis | OsmanNeural | -10% | -5Hz |
| Penang dialect | MiMo voicedesign | adaptive | adaptive |
| Formal document | Edge YasminNeural | -5% | +0Hz |

### Phase 3: ANALYZE — The Feature Extraction

DSP analysis treats audio as physics, not meaning. This is the `[OBS]` layer.

**Safe scoring dimensions**:
- Temporal stability (onset envelope autocorrelation)
- Tension/release (spectral flux + energy peaks)
- Paradox/contrast (MFCC clustering over time)
- Embodied coherence (RMS peaks + ZCR stability)
- Timbre (spectral centroid + bandwidth)
- Harmonic content (chroma features)

**Known segfaults** (this system): `beat_track`, `chroma_cqt`, `onset_detect` — use manual workarounds from `audio-analysis` skill.

## When to Load This Skill

- Any agent processes audio input (STT, audio messages, voice notes)
- Any agent generates audio output (TTS, voice notes, music)
- Any agent analyzes audio features (DSP, scoring, music intelligence)
- Deciding which STT/TTS provider to use
- Configuring voice identity or voice preferences
- Audio-related constitutional questions (voice cloning, sovereignty)

## Integration Points

- **Knowledge graph**: `/root/AAA/knowledge-graph/audio-intelligence-map.md`
- **i-ARIF identity**: `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`
- **Hermes TTS config**: `/root/HERMES/config.yaml` (line 851: `tts:`)
- **Hermes SOUL.md**: `/root/HERMES/SOUL.md` (voice delivery section)
- **STT research**: `/root/.openclaw/workspace/memory/research/STT-VOICE-LOOP-RESEARCH.md`
- **Human speech enforcer**: `/root/arifOS/arifosmcp/human_speech/enforcer.py`

## Related Skills

- `hermes-voice-config` — TTS config management
- `tts-edge-fallback` — Free Malay TTS
- `AGI-multimodal-bridge` — Cross-modal reasoning
- `delta-omega-psi-multimodal-cognition` — Δ·Ω·Ψ rules
- `aaa-pdf-voice-protocol` — Federation→human translation
- `audio-analysis` — DSP scoring modules
- `music-intelligence` — Governed music generation

---

*Doctrine sealed 2026-08-13. F2 evidence: live filesystem probe of /root/HERMES, /root/AAA, /root/arifOS.*
