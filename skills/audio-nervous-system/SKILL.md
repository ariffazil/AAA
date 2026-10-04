---
name: audio-nervous-system
id: audio-nervous-system
risk_tier: low-medium
description: 'Voice state extraction, WELL bridge, and adaptive TTS.'
autonomy_tier: T1-T2
version: "1.0"
author: Hermes Bridge
license: MIT
tags: [audio, voice-state, paralinguistic, well-bridge, tetinga, prosody, tts, stt]
owner: AAA
floor_scope: [F6, F7, F9, F11]
metadata:
  hermes:
    tags: [audio, voice-state, paralinguistic, well-bridge, tetinga, prosody, tts, stt]
    related_skills: [ai-media-generation-ops, hermes-agent]
---

# Audio Nervous System Architecture (TELINGA)

> **DITEMPA BUKAN DIBERI.** Forged 2026-08-13 under F13 sovereign directive.

## When to Use

Use when building or troubleshooting audio voice input → LLM output pipeline for Hermes agent. Specifically:
- Integrate voice notes from Telegram/Discord into agent conversation flow
- Extract prosody/paralinguistic features (fatigue, urgency, stress) from raw audio
- Route TTS output based on detected human emotional state
- Design multi-modal systems understanding modality failure modes
- Debug librosa/Praat segfaults on Python 3.13 + numpy
- Wire VoiceState sensor data through WELL homeostasis
- Configure STT/TTS providers (Edge, MiniMax, Qwen, Whisper, Groq)
- Implement constitutional gates (F9 ANTIHANTU, F7 HUMILITY, F13 SOVEREIGN) on audio operations

## Overview

Transforms raw audio into VoiceState features → WELL homeostasis → LLM context separation. Transcript carries content; VoiceState carries source reality (fatigue, urgency, stress).

### Key Insight
"The gap isn't capability — it's connecting audio to the nervous system."

Hermes had 4500+ TTS lines, 3000+ STT, 2380+ voice mode. Infrastructure existed but treated audio as *file format*, not *state carrier*. Telinga fixes this.

## Layers

### Layer 1: Voice State Extraction (MEMBRANE)
Extracts prosody BEFORE STT. Stored as `event._gateway_voice_state` — invisible to LLM, invisible to transcript.

- **Module:** `/root/hermes-agent-dev/tools/voice_state.py` (237 lines)
- **Features:** pitch mean/std/range, energy RMS, pause density, spectral centroid, voiced fraction
- **Library:** librosa only — NOT parselmouth (Praat crashes on Python 3.13 + numpy 2.4.6 segfault)
- **Governance:** F9 ANTIHANTU — sensor measures, sensor does NOT speak about what it measures
- **Wiring:** `gateway/run.py` line ~22340 via `asyncio.to_thread`, fire-and-forget after STT success
- **Reversibility:** Delete voice_state.py + remove wiring block. Zero state change.

#### Paralinguistic Sidecar Design
Two axes map to WELL fields:
- **Fatigue axis:** pitch_std↓, jitter↑, HNR↓, intensity↓ → `stress_load`, `cognitive_clarity`
- **Arousal axis:** pitch_mean↑, energy↑, speech_rate↑ → `emotional_state`

#### Gap Remaining
`_gateway_voice_state → well_assess_homeostasis()` consumer wire pending. Sensor output exists but no downstream consumer yet.

### Layer 2: Memory Bridge (FORGE)
Persist VoiceState + transcript to Qdrant as `AudioEvent`.

- **Storage:** Qdrant collection `arifos_audio_memory` with 6-dim well-vector
- **Ingest:** `forge_audio_ingest.py` — VoiceState vectorizes features
- **Query:** `"show me all conversations where Arif sounded fatigued"` → cosine similarity
- **Bridge:** `audio_event_bridge.py` — Hermes ↔ A-FORGE connector
- **Watcher:** `audio_watcher.py` — polls cache, auto-ingests new files

#### Bugs Found & Fixed
1. **TemporaryDirectory cleanup:** `_load_mono_stereo()` returned temp WAV path after `with` block exited → deleted before parselmouth read. Fix: keep operations inside same `with` context.
2. **sys.path mismatch:** Added `audio/` but ingest lives in `tools/`. Fix: `parent.parent/"tools"` added to sys.path.
3. **Deployment overwrite:** On-disk edits wiped by A-FORGE deployment pipeline. Commit to git source tree, don't just edit disk.

### Layer 3: Adaptive TTS Routing (MOUTH)
VoiceState adapts TTS output to detected human state.

- **Module:** `state_aware_tts.py` (A-FORGE)
- **Behavior:** fatigue >0.7 → slower/lower pitch/concise. arousal >0.8 → match energy.
- **Contract (TTS hint JSON):**
```json
{
  "fatigue_score": 0.0-1.0,
  "arousal_score": 0.0-1.0,
  "emotion": "low"|"neutral"|"high",
  "rate_adjust": "-10%" | "+5%",
  "pitch_adjust": "-5Hz" | "+0Hz",
  "response_style": "concise"|"normal"|"detailed",
  "acknowledge_state": True|False
}
```
- **Governance:** F6 EMPATHY — acknowledge state but DO NOT manufacture empathy. Measurement ≠ manufactured feeling.

### Layer 4: Constitutional Gates (F1-F13)

| Floor | Gate | Rule |
|---|---|---|
| F1 AMANAH | Audio immutability | Audio artifacts = biometric vault-class. Not deletable by agents. |
| F7 HUMILITY | Interpretation cap | Prosody→state inference cap 0.70. Cross-speaker: 0.50. |
| F9 ANTIHANTU | No voice-cloned deception | Agent voice = ISYARAT label, never claimed internal feeling. |
| F11 AUDIT | Chain logging | Every audio operation logged with {sha256, duration, transcript, timestamp}. |
| F13 SOVEREIGN | Voice clone consent | Clone requires explicit F13 consent. No silent cloning. |
| W0 WELL | Reflect only | WELL mirrors, never gates. No veto based on audio alone. |

## Modality Triad Doctrine

When building multimodal systems, understand each modality's failure mode:

| Modality | What it sells | Failure mode | Epistemik cost |
|---|---|---|---|
| Image | Reality (rupa) | Ilusi rupa — "aku nampak maka aku faham" | Rendah — no symbolic decomposition |
| Audio/Voice | Presence (kehadiran) | Ilusi kehadiran — emosi rasa betul, konteks boleh salah | Sederhana — partial collapse |
| Text/LLM | Explanation (penjelasan) | Ilusi kefahaman — konsistensi simbol ≠ konsistensi ontologi | Tinggi — full symbolic audit |

**Key principle:** Voice = dual-channel multiplex (symbolic content + source state) free-riding pre-linguistic presence circuits. Text = projection onto symbolic subspace discarding the state manifold. Sidecar = retaining the orthogonal complement so projection loss doesn't become trust loss.

## Provider Matrix

| Provider | Type | Status | Notes |
|---|---|---|---|
| Edge TTS (`ms-MY-OsmanNeural`) | TTS output | ✅ Default free | Standard KL BM. Two voices: Osman (male), Yasmin (female). Use `-10Hz` + `-10% rate` for deeper tone. |
| MiniMax Speech 2.8 HD | TTS output | ✅ MCP :18100 fallback | Best BM quality currently available via cloud API. |
| Qwen Token Plan | TTS output | ✅ Available | `qwen-audio-3.0-tts-plus` ($68/mo Individual Pro). |
| ElevenLabs | TTS + Voice Clone | ⚠️ Configured | Premium tier, voice clone possible. Requires key setup. |
| OpenAI TTS | TTS output | ❌ No key | Natural conversational, improving BM coverage. |
| Whisper (OpenAI) | STT input | ✅ Wired | Primary STT provider, model `whisper-1`. |
| Groq Whisper-v3-turbo | STT input | 🟡 Source wired, config missing | Fast STT — needs config.yaml entry. |
| xAI STT | STT input | 🟡 Source wired, config missing | Needs config.yaml entry. |
| Mesolitica HF models | Local TTS | 📥 Download ready | Malaysian-trained models (Malaysian-TTS-4B-v0.1, F5-TTS). Free open-source. Best native BM but no dialect variants. |
| librosa | Audio analysis | ✅ Installed | Primary feature extraction. Avoid onset_detect() and peak_pick() — numba segfaults on Python 3.13. |

### Penang Presence Strategy

No TTS provides native Penang dialect. Realistic paths:
1. ElevenLabs voice clone (requires ≥30 second real Penang speaker sample)
2. Mesolitica fine-tuning on Penang audio dataset
3. MiniMax voice_clone via MCP :18100 (verify availability)

"Penang presence" ≠ "Penang accent." It's tempo, rhythm, sentence endings (ka/kah), pause placement, code-switch BM↔English↔Hokkien. Social rhythms, not phonetic transcriptions.

## E2E Test Results

Real BM audio through full stack:

| Input Sample | stress_load | cognitive_clarity | Qdrant rank |
|---|---|---|---|
| "Aku penat sangat hari ni..." (slow, low) | 0.878 | 0.494 | 0.948 (rank 1) |
| "Assalamualaikum Arif, ini ujian" (normal) | 0.761 | 0.734 | 0.757 (rank 2) |

Fatigue query works via cosine similarity in well-vector space, filtered by `stress_load >= 0.6`.

## Implementation Checklist

- [x] Layer 1: `voice_state.py` extraction module
- [x] Layer 1: Wiring in `gateway/run.py` (~line 22340)
- [x] Layer 2: `forge_audio_ingest.py` → Qdrant bridge
- [x] Layer 2: `state_aware_tts.py` adaptive routing
- [x] Layer 2: `audio_watcher.py` cache polling
- [x] Layer 2: `forge_audio_transcribe.py` STT bridge
- [ ] **Gap 1:** `_gateway_voice_state → well_assess_homeostasis()` consumer wire
- [ ] **Gap 2:** Groq/xAI STT entries in config.yaml
- [ ] **Gap 3:** Multi-session temporal fatigue tracking (time-series aggregation in Qdrant)
- [ ] **Gap 4:** i-ARIF identity card with audio profile

## Dependencies & Installation

```bash
pip install librosa soundfile
# A-FORGE deps: pip install parselmouth scipy
```

### Critical Pitfalls
1. **numba segfault:** librosa `onset_detect()` and `peak_pick()` crash via numba on Python 3.13. Use only stable paths: `pyin`, `rms`, `zero_crossing_rate`, `spectral_centroid`.
2. **TemporaryDirectory cleanup:** Don't return file paths after `with` block exits — file deleted. Keep all file ops inside same `with` context.
3. **sys.path ordering:** When cross-importing A-FORGE modules (`audio/` vs `tools/`): `Path(__file__).resolve().parent.parent / "tools"`.
4. **Deployment overwrites:** A-FORGE has automated deployment pipeline. On-disk edits without git commits will be wiped. Always commit first.
5. **STT config drift:** Providers wired in Python source but missing from `config.yaml`. Always sync both layers.
6. **edge-tts CLI pitfalls (verified 2026-08-14):** (a) `--pitch "-5Hz"` — negative values with `--` prefix are parsed as flags by argparse → error. Omit `--pitch` or use positive-only values. (b) For BM text containing apostrophes, quotes, or special chars — **always** write to a temp file and use `-f /tmp/prompt.txt` instead of `-t "inline text"`. Inline Malay text with `!` or `?` or `'` breaks shell escaping even inside single quotes. (c) Only two ms-MY voices exist: `ms-MY-OsmanNeural` (male) and `ms-MY-YasminNeural` (female). For younger male voice: `--rate "+20%"` on Osman. For sultry female: `--rate "+5%"` on Yasmin. (d) `--write-media` required for audio output file; `--write-subtitles` optional for word-level timing.

## Governance Boundaries

- VoiceState = **sensor output**, never LLM-facing text. Lives on `event._gateway_voice_state` attribute. Only accessible to explicitly wired consumers.
- WELL reads VoiceState but returns REFLECT_ONLY. Mirrors state, never gates action.
- All paralinguistic claims labeled `[INT]` with confidence cap 0.70 (F7 HUMILITY). Cross-speaker: 0.50.
- Voice output to third parties = T3 HOLD. Voice output to Arif = T2.

## References
- `references/modality-triad-doctrine.md` — Image/audio/LLM comparison matrix
- `references/provider-audit.md` — Provider latency/cost/quality benchmarks
- `references/well-wiring-template.md` — Template for _gateway_voice_state → well_assess_homeostasis wire
- `references/diagnostic-pipeline.md` — Setup and verification scripts for audio nervous system
