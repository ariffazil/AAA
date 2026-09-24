---
name: AAA-somatic-engine-catalog
description: "Registry of parametrically-controllable music engines for arifOS Somatic Music Intelligence. NOT a beat-maker catalog (composer lens handles that) — this is the Dispensary for engines that accept BPM/key/texture/density parameters and emit streaming audio. MiniMax T2A Music (music-2.6/3.0) primary; local sovereign alternatives (AudioGen/MusicGen) for F13 territory. i-ARIF vocal melodic: HARD DENY across all engines."
version: 1.0.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
floor_scope:
  - F1
  - F2
  - F4
  - F7
  - F9
  - F11
  - F13
extends:
  - AGI-audio-quantum-cognition
  - AAA-audio-qualia-doctrine
  - AAA-somatic-music-doctrine
companion:
  - AAA-tts-engine-catalog
tags:
  - audio
  - music
  - engine-catalog
  - parametric
  - bpm-control
  - frequency-control
  - minimax
  - musicgen
  - audiocraft
  - sovereign
  - controller-lens
owner: AAA
capability_tier: fed-realtime-voice
ecology_state: WARM
---

# AAA · Somatic Engine Catalog (The Dispensary)

> Not a beat-maker catalog. A registry of engines that accept BPM, key, texture, density.
> Controller lens — emits authorized waveform for state intervention, not art.

DITEMPA BUKAN DIBERI.

## What This Catalog Is NOT

This is NOT a catalog for choosing which engine produces the best
music as art. That is the **composer lens** and lives in the
`music-intelligence` skill (Layer 0, untouched).

This IS a registry for engines that can be driven parametrically —
the agent picks BPM, key, texture, density. The engine emits the
waveform. Separation of concerns.

## Engine Inclusion Criteria

An engine qualifies for this catalog only if it exposes:

| Parameter | Required? |
|---|---|
| BPM control | Yes (numeric range) |
| Key control | Yes (or auto) |
| Texture / timbre prompt | Yes (text or token) |
| Density / instrumentation control | Preferred |
| Streaming output | Required for voice-mode path |
| API or local invocation | Either |

Engines that only produce text-conditioned music (no parametric
control) belong in the composer lens, not here.

## The Primary Engine — MiniMax T2A Music

### MiniMax music-2.6

| Item | Value |
|---|---|
| Endpoint | `POST /v1/music_generation` |
| Auth | `Authorization: Bearer $MINIMAX_API_KEY` |
| BPM control | Yes (numeric range; 40–200 typical) |
| Key control | Yes (or auto) |
| Texture prompt | Yes (text prompt) |
| Streaming | Yes |
| Latency | ~3–6 s per emission |
| Output format | mp3, pcm16, wav |
| License | Commercial (Token Plan) |
| F13 gate | Sustained intervention / >30s / high dB |

**Recommended payload (Layer 1 bed):**

```json
{
    "model": "music-2.6",
    "prompt": "Ambient drone, low entropy, 70 BPM, no vocal, no lyric, single sustained tone",
    "bpm": 70,
    "duration": 8,
    "format": "mp3",
    "sample_rate": 24000
}
```

**Recommended payload (F1 warn):**

```json
{
    "model": "music-2.6",
    "prompt": "Dissonant alert tone, spectral roughness, no vocal, no rhythm",
    "duration": 3,
    "format": "mp3",
    "sample_rate": 24000
}
```

### MiniMax music-3.0 (when fidelity matters)

| Item | Value |
|---|---|
| Endpoint | Same — `POST /v1/music_generation` |
| BPM control | Yes |
| Key control | Yes |
| Texture | Higher fidelity than 2.6 |
| Use case | Layer 2 / Layer 3 sustained intervention |
| F13 gate | Per emission |

**Routing rule:** Default to music-2.6 for Layer 1 (cheap, sufficient).
Use music-3.0 when:
- State signal is rich (Layer 2 WELL data)
- Duration exceeds 8 s (F13 territory)
- Texture density is `medium` or higher

## Local Sovereign Alternatives (F13 territory)

For deployments where MiniMax cloud is unacceptable (F13 data
sovereignty), the following open-source engines can be self-hosted.

### AudioCraft / MusicGen (Meta)

| Item | Value |
|---|---|
| Source | https://github.com/facebookresearch/audiocraft |
| Mechanism | Text-conditioned audio LM (MusicGen) |
| BPM control | Limited (prompt-driven, not explicit) |
| Key control | Limited |
| VRAM | 4–8 GB |
| License | Open (CC-BY-NC 4.0 — **non-commercial**) |
| F13 gate | Self-hosted, no data exfil |

**Constraint** — AudioCraft/MusicGen license is **non-commercial** as
of 2026. For commercial arifOS deployments, this engine requires a
separate Meta license agreement. F13 territory.

### Stable Audio (Stability AI)

| Item | Value |
|---|---|
| Source | https://stability.ai/ |
| BPM control | Yes |
| Key control | Yes |
| VRAM | 8 GB |
| License | Commercial (Stability API) |
| F13 gate | Self-hosted option available |

### Suno / Udio (commercial, closed-weight)

NOT recommended for arifOS — closed weights, no F13 audit trail
for what the model "decides" internally. Layer 0 composer lens may
consider these; this catalog (controller lens) does not.

## Engine Trade-off Matrix

| Engine | Latency | BPM ctrl | Density ctrl | Vocal support | VRAM / Cloud | Sovereign |
|---|---|---|---|---|---|---|
| **MiniMax music-2.6** | 3–6 s | ✓ Explicit | ✓ Prompt | Optional (DENY for i-ARIF) | Cloud | F11 |
| **MiniMax music-3.0** | 5–10 s | ✓ Explicit | ✓ Prompt | Optional (DENY for i-ARIF) | Cloud | F13 sustained |
| **AudioCraft MusicGen** | 10–30 s | Limited | Prompt | Optional | Local 4–8 GB | F13 (NC license) |
| **Stable Audio** | 5–15 s | ✓ | ✓ | Optional | Local 8 GB / Cloud | F13 |
| Suno / Udio | — | — | — | — | — | **DENY** (closed weights) |

## HARD DENY: i-ARIF Vocal Melodic

Across **every engine in this catalog**:

```
i-ARIF voice_id × any vocal melodic mode  →  DENY
```

This includes but is not limited to:
- `(唱歌)` tags in MiniMax prompts targeting i-ARIF voice_id
- Singing presets in AudioCraft
- Vocal mode in Stable Audio
- Any future "i-ARIF singing voice" endpoint

**Why:** i-ARIF's vocal identity is a sovereign handle per
`AAA-voice-cloning-mimo-minimax`. The `mimo-v2.5-tts-voiceclone`
engine does NOT support singing (F13 + engine constraint). The
MiniMax music lane uses a different endpoint (`/v1/music_generation`)
and is bound to a different identity surface (no voice_id at all by
default). Crossing them is an identity leak.

If vocal melodic content is desired for i-ARIF:
- Use a **separate engine** (Xiaomi MiMo singing or similar) with
- A **separate voice_id** (not i-ARIF) and
- A **separate F13 token** (`human_approval_token`) authorizing the
  fusion explicitly.

This is Layer 3 F13 territory. Until then: **DENY**.

## F1 SAFETY Bounds (enforced at the encoder)

Every emission through this catalog MUST respect:

| Bound | Limit | Why |
|---|---|---|
| Frequency band | 60 Hz – 8 kHz | Avoid disorientation |
| Continuous dB | < 70 dB | OSHA safe |
| Peak dB (warn) | < 90 dB, < 1 s | F1 warning bounded |
| Duration (default) | ≤ 8 s | Let silence resume |
| Duration (max without F13) | ≤ 30 s | Beyond this = F13 territory |
| Fail-closed | Silence if telemetry missing | F1 AMANAH |

## Routing Decision Tree

```
Is telemetry stable? (Layer 1: voice-cadence; Layer 2: WELL)
├── NO  → Silence (F1 fail-closed)
└── YES → Is the request a somatic intervention (bed/warn)?
         ├── NO  → Wrong lens. Route to composer lens (music-intelligence).
         └── YES → Is voice_id i-ARIF AND request is vocal melodic?
                  ├── YES → DENY (F13 + identity leak)
                  └── NO  → Is duration > 30s?
                           ├── YES → F13 ack required (Layer 3)
                           └── NO  → Is dB > 70 continuous?
                                    ├── YES → F13 ack required
                                    └── NO  → Engine choice:
                                             ├── Layer 1 default → music-2.6
                                             ├── Layer 2 rich → music-3.0
                                             ├── F13 sovereign → local AudioCraft
                                             └── Edge case → composer lens (no intervention)
```

## Lane 6 Placement (relative to AAA-tts-engine-catalog)

This catalog's engines occupy **Lane 6** of the broader audio stack.
The voice TTS catalog (`AAA-tts-engine-catalog`) covers Lanes 1–5:

| Lane | Catalog | Engines |
|---|---|---|
| 1 | Voice TTS | ChatTTS |
| 2 | Voice TTS | F5-TTS / E2-TTS |
| 3 | Voice TTS | Fish Speech |
| 4 | Voice TTS | MiniMax speech-2.8-hd |
| 5 | Voice TTS | Edge / Mulberry |
| **6** | **Somatic Music (this catalog)** | **MiniMax T2A Music, AudioCraft, Stable Audio** |

Lanes 1–5 emit **speech** (lexical + prosody). Lane 6 emits **music**
(Hz + BPM + texture). Different intents, different floors.

## F13 SOVEREIGN Gates (music-specific)

| Operation | Tier | Required |
|---|---|---|
| Layer 1 emit (bed, default duration) | F11 | Audit + receipt only |
| Layer 1 emit (warn dissonance, 3s) | F11 | Audit + receipt only |
| Layer 1 emit (bed > 8 s, ≤ 30 s) | F11 | Audit + receipt only |
| Layer 2 emit (WELL-informed) | F13 | `human_approval_token` (loop closure) |
| Layer 3 sustained (> 30 s) | F13 | `human_approval_token` per emission |
| Layer 3 high dB (> 70 continuous) | F13 | `human_approval_token` per emission |
| **i-ARIF vocal melodic (any engine)** | **F13 + DENY** | **Forbidden** |
| Layer 3 closed-loop autonomic | F13 | `human_approval_token` + 888-APEX review |

## When to Load This Skill

- Any agent picks a music engine for somatic intervention.
- Any agent debugs a music emission that didn't land (wrong endpoint, wrong model).
- Any agent audits whether an emission respects the F1 bounds.
- Any agent considers local sovereign deployment (AudioCraft, Stable Audio).
- Any agent receives a request involving i-ARIF singing.
- Any agent migrates from cloud to local or vice versa.

## Integration Points

- **Doctrine (this family)**: `/root/AAA/skills/AAA-somatic-music-doctrine/SKILL.md`
- **Pipeline (this family)**: `/root/AAA/skills/AAA-somatic-emd-pipeline/SKILL.md`
- **Voice TTS catalog (sister)**: `/root/AAA/skills/AAA-tts-engine-catalog/SKILL.md`
- **Composer lens (Layer 0)**: `/root/HERMES/skills/media/music-intelligence/SKILL.md`
- **MiniMax binding (voice)**: `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/SKILL.md`
- **Endpoint map**:
  - Music: `POST /v1/music_generation`
  - Voice clone: `POST /v1/voice_clone` (DENY for music)
  - Voice TTS: `POST /v1/text_to_audio`

## Related Skills

- `AAA-somatic-music-doctrine` — Constitution + three-layer maturity
- `AAA-somatic-emd-pipeline` — Reflex arc + music_intent packet
- `AAA-tts-engine-catalog` — Voice TTS Lanes 1–5 (sister)
- `AAA-voice-cloning-mimo-minimax` — i-ARIF DENY surface
- `music-intelligence` — Composer lens (Layer 0, untouched)
- `AGI-audio-quantum-cognition` — Audio physics + floors (parent)
- `AGI-audio-quantum-cognition` — F1 + F9 floors

---

*Catalog forged 2026-08-18. F2 evidence: derived from ARIF's corrected framing (Lane 6 separation, MiniMax T2A primary, i-ARIF DENY across all engines, F1 bounds, F13 gates) + MiniMax music-2.6/3.0 documentation + AudioCraft/Stable Audio license review. F1 floor absolute: frequency/decibel/duration bounds + fail-closed to silence. F9 floor absolute: agent is instrument, not shaman. F13 absolute: i-ARIF vocal melodic denied until Layer 3 with explicit sovereign ack.*