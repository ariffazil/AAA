# Audio Intelligence Knowledge Graph — arifOS Federation

**DITEMPA BUKAN DIBERI** · Forged 2026-08-13 · FI-003 Qwen Code

## Core Thesis

Hermes is the **voice membrane** — the boundary where human state (content + emotion + fatigue + urgency) enters the machine. Like the retina isn't a camera, the voice membrane isn't an "audio agent." It's the translation surface between sovereign human state and machine representation.

> "Teks menyimpan apa yang manusia kata. VoiceState menyimpan keadaan manusia ketika mengatakannya." — F13 SOVEREIGN, 2026-08-13

VoiceState carries sovereign human state — biometric-equivalent trust class. Transcript carries semantic content — standard trust class. These are NOT the same artifact.

## 1. Modality Physics

| Modality | Physics | Collapse State | Agent Role |
|---|---|---|---|
| **Text** | Discrete symbols | Fully collapsed (human observed, encoded) | Classical computation |
| **Image** | Spatial probability distribution | Single eigenstate (frozen frame) | Pattern recognition |
| **Audio** | Temporal wave superposition | Pre-measurement | Quantum observer |
| **Video** | Image sequence + audio entanglement | Partially collapsed | Multi-state tracker |
| **3D/Mesh** | Spatial-temporal manifold | Partially collapsed | Geometric reasoning |

### Audio Quantum Properties

- **Gabor limit** = Heisenberg uncertainty. Cannot simultaneously resolve exact frequency + exact time.
- **Superposition of meaning**: prosody, identity, emotion, intent, language — all entangled in one waveform.
- **Observer-dependent collapse**: same audio, different agents → different interpretations.
- **Temporal non-locality**: coarticulation — phoneme at *t* depends on context at *t+1*.
- **Cocktail party problem** = entangled states requiring measurement projection.

## 2. Hermes Audio Stack — Live Inventory

### 2.1 TTS (Text → Speech — Mouth)

| Provider | Engine | Malay Voice | Status | Config Key |
|---|---|---|---|---|
| **edge-tts** | Microsoft Edge Neural | `ms-MY-OsmanNeural` (M) / `ms-MY-YasminNeural` (F) | ✅ DEFAULT | `tts.provider: edge` |
| **MiniMax 2.8 HD** | MuleRouter proxy | `man` (BM mode) | ✅ Primary (quality) | `mulerouter-tts.py` |
| **Qwen Audio 3.0** | Token Plan TTS-plus | `longxiaochun` (no Malay native) | ✅ Available | `tts.provider: qwen-token-plan` |
| **MiMo V2.5** | Xiaomi TTS | Custom voicedesign/clone (Penang-capable) | ✅ Available | `tts.provider: mimo` |
| **ElevenLabs** | Multilingual v2 | `pNInz6obpgDQGcFmaJgB` (clone target) | ✅ Available | `tts.provider: elevenlabs` |
| **OpenAI** | gpt-4o-mini-tts | `alloy` (English) | ✅ Available | `tts.provider: openai` |
| **Gemini** | gemini-2.5-flash-tts | `Kore` | ✅ Available | `tts.provider: gemini` |
| **xAI** | Grok TTS | `eve` (English) | ✅ Available | `tts.provider: xai` |
| **Mistral** | voxtral-mini | `c69964a6` | ✅ Available | `tts.provider: mistral` |
| **NeuTTS** | Local GGUF | CPU fallback | ⚠️ Standby | `tts.provider: neutts` |
| **Piper** | Local | `en_US-lessac-medium` | ⚠️ Standby | `tts.provider: piper` |

**Decision chain**: mulerouter (quality) → edge-tts (free Malay fallback)
**Voice profile for BM**: OsmanNeural, rate +5% casual / -10% analytical
**Penang path**: MiMo voicedesign with dialect description
**OGG for Telegram**: edge-tts native OGG → voice bubble; MP3/WAV → audio file

### 2.2 STT (Speech → Text — Ears)

Hermes config has a full `stt:` block (line 855+ in config.yaml):

```yaml
stt:
  enabled: true
  provider: openai          # Default: whisper-1
  openai:
    model: whisper-1
  local:
    model: base            # faster-whisper (free, full sovereignty)
  mistral:
    model: voxtral-mini-latest
  elevenlabs:
    model_id: scribe_v2
  mimo:
    model: mimo-v2.5-asr    # Xiaomi MiMo ASR
```

Hermes source (`/root/hermes-agent-dev/tools/transcription_tools.py`) also supports **Groq** (whisper-large-v3-turbo) and **xAI** (Grok STT) — these are wired in the source but not yet in the config yaml block.

| Engine | Location | Sovereignty | Latency | Config Status | Source Status |
|---|---|---|---|---|---|
| **OpenAI Whisper-1** | Cloud | LOW | Standard | ✅ `stt.provider: openai` | ✅ |
| **faster-whisper** (base) | Local `/root/venv/` | FULL | ~4× realtime | ✅ `stt.local.model: base` | ✅ |
| **Mistral Voxtral** | Cloud | LOW | Fast | ✅ in config | ✅ |
| **ElevenLabs Scribe v2** | Cloud | LOW | Fast | ✅ in config | ✅ |
| **MiMo ASR v2.5** | Cloud | LOW | Fast | ✅ in config | ✅ |
| **Groq Whisper-v3-turbo** | Cloud | LOW | 216× realtime | ❌ not in config | ✅ in source |
| **xAI Grok STT** | Cloud | LOW | Fast | ❌ not in config | ✅ in source |
| **whisper.cpp** | Local binary | FULL | CPU-native | ❌ | ❌ Not built |

**Loop status**: TTS ✅ working. STT ✅ **fully wired** (config `enabled: true`, 7 engines available).
**Voice loop**: User speaks → Telegram .ogg → STT → LLM → TTS → .ogg reply

### 2.2b OpenClaw Disabled Audio Skills

Several audio skills exist in OpenClaw but are **disabled** (`enabled: false`):
- `sherpa-onnx-tts` — local TTS
- `voice-call` — real-time voice call
- `openai-whisper-api` — cloud STT (superseded by Hermes native STT)
- `songsee` — music analysis
- `spotify-player` — music playback

These are available to enable but intentionally off.

### 2.2c Wake Word Detection

Hermes source includes push-to-talk + **"Hey Hermes" wake word** detection:

| Engine | Type | Status |
|---|---|---|
| **openWakeWord** | ONNX, free | ✅ Default |
| **sherpa-onnx** | Free, open vocabulary | ✅ Available |
| **Porcupine** | Premium | ✅ Available |

Config: `voice.record_key: ctrl+b`, `voice.max_recording_seconds: 120`, `voice.auto_tts: true`

### 2.3 Audio Analysis (DSP — Inner Ear)

| Skill | Library | Capabilities | Status |
|---|---|---|---|
| **audio-analysis** | librosa + numpy | Multi-score modules, onset detection, MFCC, spectral | ✅ Active |
| **audio-feature-analysis** | librosa + scipy | Chroma, motif detection, similarity matrices, segmentation | ✅ Active |
| **music-intelligence** | MiniMax + DSP | Governed generation + somatic scoring pipeline | ✅ Active |

**Known segfaults** (system-specific): `beat_track`, `chroma_cqt`, `onset_detect` — use manual workarounds.
**Safe functions**: `load`, `stft`, `onset_strength`, `rms`, `mfcc`, `spectral_flatness`, `zcr`, `spectral_centroid`, `chroma_stft`.

### 2.4 Music Generation (Creative Audio)

| Skill | Engine | Capabilities | Status |
|---|---|---|---|
| **music-generation** | MiniMax + Suno | Concept → lyrics → cultural research → generation | ✅ Active |
| **music-intelligence** | somatic scoring | Generate → Analyze → Score → Iterate | ✅ Active |
| **ComfyUI ACE-Step 1.5** | Local Stable Audio | Text-to-audio generation | ✅ Blueprint ready |
| **ComfyUI Stable Audio 3** | Local | Audio generation (medium/base) | ✅ Blueprint ready |

### 2.5 Voice Identity & Writing

| Skill | Purpose | Status |
|---|---|---|
| **hermes-voice-config** | Unified voice management, OsmanNeural pinning | ✅ Active |
| **AGI-hermes-system-prompt-voice** | Open-weights voice compliance, stylized witness format | ✅ Active |
| **human-voice-writing** | Arif's personal docs in bahasa kampung voice | ✅ Active |
| **aaa-pdf-voice-protocol** | Federation→geological prose translation | ✅ Active |

### 2.6 Human Speech Enforcer (arifOS Kernel)

| Component | Path | Purpose | Status |
|---|---|---|---|
| **enforcer.py** | `/root/arifOS/arifosmcp/human_speech/` | Strips machine terms from human output | ✅ Wired |
| **test_human_speech** | `/root/arifOS/tests/` | Constitutional test for speech layer refusal | ✅ Active |

## 3. FED FLAME FRAME Audio Routing

```
asi-555-audio → MiMo V2.5 — AUDIO (native audio understanding)
hermes-asi-vision → MiMo V2.5 / Qwen 3.7 Plus — IMAGE
supports_audio: true  (Hermes config model block)
```

Hermes routes audio through FED LiteLLM :4000 → `asi-555-audio` model → MiMo V2.5 for native audio understanding (not transcription first, but direct audio-in).

## 4. AAA Skills Mesh — Audio Surface

### Federated Skills (cross-agent)

| Skill | Owner | Available To | Audio Role |
|---|---|---|---|
| `AGI-hermes-system-prompt-voice` | AAA | All warga | Voice compliance |
| `AGI-multimodal-bridge` | AAA | All warga | Text+image+audio+geospatial fusion |
| `delta-omega-psi-multimodal-cognition` | AAA | All warga | Δ·Ω·Ψ multimodal cognition rules |
| `aaa-pdf-voice-protocol` | AAA | All warga | Internal→human translation |
| `AAA-OCR-optical-compression` | AAA | All warga | Image→text (sensory compression) |
| `forge-document-intelligence` | AAA | All warga | VLM perception pipeline |

### Hermes-Local Skills (EDGE layer)

| Skill | Audio Function |
|---|---|
| `hermes-voice-config` | TTS config, unified voice, provider management |
| `text-to-speech` | Qwen Token Plan TTS via DashScope |
| `tts-edge-fallback` | edge-tts free Malay TTS, OGG delivery |
| `audio-analysis` | DSP scoring (temporal, tension, paradox, coherence) |
| `audio-feature-analysis` | Chroma, motif, similarity, structural segmentation |
| `music-generation` | Full pipeline: concept→lyrics→cultural→generation |
| `music-intelligence` | Governed generation + somatic scoring |
| `human-voice-writing` | Arif's personal voice for docs |

## 5. i-ARIF Audio Identity

### Arif's Voice Preferences (observed, session-confirmed)

| Preference | Evidence | Date |
|---|---|---|
| **Primary voice**: OsmanNeural (ms-MY) | Multiple sessions, trading briefings | 2026-07 |
| **"Nusantara mode" trigger** | Strong preference signal → switch to edge-tts | 2026-07-13 |
| **Penang dialect interest** | Requested Penang voice experiments | 2026-07-08 |
| **Quality override**: edge-tts over mimo for BM | Rejected mimo quality, accepted edge | 2026-07-11 |
| **Language**: BM-English code-switch (Penang style) | SOUL.md canonical | Ongoing |
| **Trading voice format**: 90s template, spell numbers | SADO daily briefing | 2026-07-18 |

### i-ARIF Audio State (LIVE — forged 2026-08-14, updated 2026-08-14 post-musyawarah)

Identity card exists at `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`.

**Converged audio architecture** (post-musyawarah 2026-08-14):
- **Layer 1 (Hermes EDGE, CANONICAL):** `voice_state.py` — librosa, 14 features, wired into gateway hot path. F7: confidence 0.70. F9: emotional_state always "neutral".
- **Layer 2 (WELL DIAGNOSIS):** `voice_state_to_well_features()` — maps raw → stress_load, cognitive_clarity. WELL reflects, never gates.
- **Layer 3 (A-FORGE PERSISTENCE):** `forge_audio_ingest.py` — imports voice_state.py (librosa), NOT forge_audio_features.py. Qdrant `arifos_audio_memory`, 6-dim well-vector, sidecar at `/tmp/aforge_voice_state.json`.
- **Layer 4 (A-FORGE TTS ACK):** `state_aware_tts.py` — REWRITTEN to F9-compliant diagnostic-only. Outputs `{acknowledge, message, response_style, factual_metrics}`. `speed: None`, `instructions: None`. NEVER modifies how agent speaks.
- **E2E verified:** BM speech → Qdrant → "fatigued conversations" cosine query (score 0.948)

**RETIRED (dead code, ARA-protected in git):**
- `forge_audio_features.py` — parselmouth+scipy, crashes on every file (PraatError). Has F9 violations (`emotion` field), F7 overclaim (0.90 on 5-proxy composite), nominal fallacy (`fatigue_score`). ARA (Kimi Code FI-008) auto-restores when deleted. Accepted as dead weight pending F13 decision.
- `audio_event_bridge.py` — imports from forge_audio_features.py (broken import). Dead code — bridge is broken and points to dead extractor.

**Three sealed brakes:**
1. **Prosody ≠ Truth** — never infer intent from prosody
2. **F9 Anti-Hantu** — sensor measures, never speaks about what it measures
3. **W³ Measurement** — don't add witness dimensions before tri-witness math is stable

## 6. Quantum Audio Architecture — Design Doctrine

### The Audio Triangle

```
                    ┌─────────────┐
                    │  UNDERSTAND  │
                    │  (STT/ASR)   │
                    │  Groq/Whisper│
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   REASON     │   │   GENERATE  │   │   ANALYZE   │
│  Audio LLM   │   │   (TTS)     │   │   (DSP)     │
│  MiMo V2.5   │   │  Edge/MiniMax│  │  librosa    │
│  asi-555     │   │  Qwen TTS   │   │  scoring    │
└─────────────┘   └─────────────┘   └─────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼──────┐
                    │   DELIVER   │
                    │  Telegram   │
                    │  .ogg voice │
                    └─────────────┘
```

### Constitutional Audio Floors

| Floor | Audio Application |
|---|---|
| F1 AMANAH | Audio recordings immutable. Voice identity non-forgeable without F13. VoiceState = biometric-equivalent — same access control. |
| F2 TRUTH | STT transcripts carry `[OBS]`. TTS output is `[DER]`. DSP features are `[OBS]`. VoiceState is `[OBS]` (measured sovereign state). |
| F4 CLARITY | Voice notes = conversational prose only. No markdown, no tables, no code in speech. |
| F7 HUMILITY | Canonical extractor (voice_state.py) confidence cap 0.70 (3-proxy composite). Retired extractor (forge_audio_features.py) used 0.90 on 5-proxy composite — overclaim. Prosody is inherently ambiguous. |
| F9 ANTIHANTU | Agent has no voice identity — borrows sovereign's. VoiceState is **diagnostic**, not expressive. **TTS emotional adaptation = F9 violation.** State-aware TTS = acknowledgment only. |
| F10 ONTOLOGY | Audio ≠ meaning. Waveform is physics. Interpretation is human. |
| F11 AUDIT | Every audio processing decision logged. Receipt-wrapped. |
| F13 SOVEREIGN | Voice cloning = explicit F13. VoiceState access = F13 explicit. VoiceState deletion = F1 AMANAH (irreversible). |

## 7. Gap Analysis

| Gap | Severity | Action |
|---|---|---|
| **Groq/xAI STT not in config yaml** | P2 | Add `groq:` and `xai:` blocks to `stt:` in config.yaml (already wired in source) |
| **i-ARIF identity card created** | ✅ DONE | Created with audio profile, language prefs, voice sample ref |
| **No AAA-level audio cognition skill** | ✅ DONE | Created `AGI-audio-quantum-cognition` skill (v2.0.0 — unified mesh) |
| **SOUL.md audio section added** | ✅ DONE | Added §Audio Identity — Suara & Pendengaran |
| **Audio memory persistence** | ✅ DONE (2026-08-14) | Layer 3 live: `forge_audio_ingest.py` → Qdrant `arifos_audio_memory` |
| **Fatigue query** | ✅ DONE (2026-08-14) | `--query-fatigued` cosine search on well-vector, E2E verified |
| **State-aware TTS** | ✅ DONE (2026-08-14) | `state_aware_tts.py` REWRITTEN to F9-compliant diagnostic-only. No rate/pitch/instructions. Acknowledgment only. |
| **forge_audio_features.py retired** | ⚠️ ARA-protected | Dead code (PraatError). ARA auto-restores when deleted. Accepted pending F13 decision. |
| **ComfyUI audio not federated** | P3 | No bridge from ComfyUI→Hermes audio pipeline |
| **OpenClaw audio skills disabled** | P3 | sherpa-onnx-tts, voice-call, songsee, spotify available but off |

---

*Graph sealed 2026-08-13 by FI-003 Qwen Code. Updated 2026-08-14 post-musyawarah.*
*Post-correction: STT was already wired in config (stt.enabled: true, 7 engines). Previous version incorrectly stated STT not in config.*
*Post-musyawarah: forge_audio_features.py marked RETIRED. state_aware_tts.py rewritten F9-clean. Architecture converged to single extractor (voice_state.py).*
