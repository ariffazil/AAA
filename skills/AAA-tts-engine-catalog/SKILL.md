---
name: AAA-tts-engine-catalog
description: "TTS engine registry for the arifOS federation. ChatTTS (qualitative conversational), F5-TTS / E2-TTS (zero-shot flow matching), Fish Speech (audio language model), MiniMax speech-2.8-hd (HD commercial), Edge / Mulberry (free fallback). Trade-off matrix, F13 governance, and routing rules. Single source of truth for which engine to use when."
version: 1.0.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
floor_scope:
  - F2
  - F4
  - F7
  - F9
  - F11
  - F13
extends:
  - AGI-audio-quantum-cognition
  - AAA-audio-emd-pipeline
tags:
  - audio
  - tts
  - chattts
  - f5-tts
  - e2-tts
  - fish-speech
  - minimax
  - engine-registry
  - qualia
owner: AAA
---

# AAA · TTS Engine Catalog

> Five engines. Five trade-off axes.
> The right engine is a function of acoustic intent, latency budget,
> VRAM budget, and F13 sovereign gate.

DITEMPA BUKAN DIBERI.

## What "Qualia" Means Here

F9 ANTI-HANTU floor — AI has no qualia. In this catalog, **qualitative
fidelity** is defined mechanically as high-fidelity acoustic variance
that mimics human biology:

- Pitch contour (F0 trajectory with micro-variations)
- Micro-pauses (50-300 ms silences inside phrases)
- Breath sounds (inhale, exhale, hesitation)
- Timbre shifts (emotional coloring)
- Tempo variation (WPM jitter, not constant rate)

P(Truth) of any qualitative claim: bounded by the F7 confidence cap
(0.90) — listeners disagree.

## The Five Engines

### 1. ChatTTS — Highest Qualia, Conversational

| Item | Value |
|---|---|
| Mechanism | Token-injected acoustic features |
| Native qualia tokens | `[laugh]`, `[breath]`, `[uv_break]` (gag/hesitation), `[oral]`, `[noise]` |
| Cloning | Difficult — needs fine-tuning, not zero-shot |
| Languages | English, Mandarin (best); limited others |
| Latency | Medium |
| VRAM | ~4 GB |
| License | Open (Apache 2.0) |

**Use when**: agent-to-human voice notes, conversational AI, expressive
narration. The only engine that natively produces laughter and breath.

**Avoid when**: cloning i-ARIF (no good zero-shot path); multilingual
mixing; deterministic output (varies by run).

### 2. F5-TTS / E2-TTS — Zero-Shot, Flow Matching

| Item | Value |
|---|---|
| Mechanism | Flow matching (E2-TTS paper lineage) |
| Native qualia tokens | None — prosody is purely emergent from reference |
| Cloning | Excellent zero-shot from 3–10 s reference |
| Languages | Multilingual (English + zh best) |
| Latency | Fast |
| VRAM | ~4 GB (consumer GPU friendly) |
| License | Open (MIT) |

**Use when**: cloning a voice from a short sample; real-time-ish
narration; low VRAM budget.

**Avoid when**: you need explicit emotional control tokens (no API for
that — prosody is locked to the reference audio).

### 3. Fish Speech — Audio Language Model

| Item | Value |
|---|---|
| Mechanism | Audio LM (text → audio tokens, not spectrogram) |
| Native qualia tokens | None — emotional context from text semantics |
| Cloning | Excellent zero-shot |
| Languages | Multilingual, very strong cross-lingual |
| Latency | Slow (heavier inference) |
| VRAM | ≥ 8 GB, ideal 12+ GB for realtime |
| License | Open (Apache 2.0) |

**Use when**: stable multilingual TTS with code-switching in one
utterance; long-form narration; semantic emotion matters more than
prompt emotion.

**Avoid when**: VRAM constrained (< 8 GB); latency critical
(< 200 ms).

### 4. MiniMax speech-2.8-hd — HD Commercial

| Item | Value |
|---|---|
| Mechanism | Provider proprietary (HD speech synthesis) |
| Native qualia tokens | N/A (commercial API) |
| Cloning | Via `mimo-v2.5-tts-voiceclone` (see companion skill) |
| Languages | Multilingual with voice_id control |
| Latency | Variable; check benchmarks |
| VRAM | N/A (cloud) |
| License | Commercial |

**Use when**: HD narration for media artifact; i-ARIF voice (already
enrolled via companion skill); high-stakes audio where quality wins.

**Avoid when**: budget constrained; local-only operation; F13 concerns
about cloud-only identity storage.

See: `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/SKILL.md`.

### 5. Edge / Mulberry — Free Fallback

| Item | Value |
|---|---|
| Mechanism | Neural TTS (Edge / browser stack) |
| Native qualia tokens | None |
| Cloning | Not supported |
| Languages | 100+ including Malay (`ms-MY-YasminNeural`, `ms-MY-OsmanNeural`) |
| Latency | Lowest (browser-cached) |
| VRAM | N/A (edge runtime) |
| License | Free |

**Use when**: free fallback when MiniMax / Qwen quota exhausted; voice
bubble in chat UI; low-stakes narration.

**Avoid when**: identity continuity matters (no cloning); HD fidelity
needed.

See: `/root/.kimi-code/skills/tts-edge-fallback/SKILL.md`.

## Trade-off Matrix (canonical)

| Engine | Latency | Zero-shot clone | Qualia tokens | VRAM cost | Sovereign |
|---|---|---|---|---|---|
| **ChatTTS** | Medium | Hard (fine-tune) | **Highest** | ~4 GB | Open |
| **F5-TTS** | Fast | Excellent (3–10 s) | High (from ref) | ~4 GB | Open |
| **Fish Speech** | Slow | Excellent | High (semantic) | ≥ 8 GB | Open |
| **MiniMax 2.8-hd** | Variable | Via mimo-v2.5 | High | N/A cloud | F13 |
| **Edge** | Lowest | None | Low | N/A edge | Open |

## Routing Decision Tree (AAA-audio-emd-pipeline Phase 3)

```
Is the acoustic_intent a qualia token like [laugh] or [breath]?
├── YES → ChatTTS
└── NO  → Is there a sovereign voice_id to use?
         ├── YES → MiniMax (F13-gated identity)
         └── NO  → Is the deployment latency-critical realtime?
                  ├── YES (< 500 ms) → Edge / Mulberry
                  └── NO  → Is the sample short (3–10 s)?
                           ├── YES → F5-TTS
                           └── NO  → Multilingual mixing?
                                    ├── YES → Fish Speech
                                    └── NO  → F5-TTS (default)
```

## EMD Integration (Phase 3 ENCODE)

Per `AAA-audio-emd-pipeline`:

```python
audio = arifos.audio.tts_encode(
    decision_packet=packet,
    engine="chattts",          # or "f5-tts", "fish", "minimax", "edge"
    qualia_tokens=packet.acoustic_intent.breath_tokens,  # ChatTTS only
    voice_id="i-ARIF-2026-08-18",  # MiniMax only
    reference_audio="path/to/i-ARIF-15s.wav",  # F5-TTS, Fish
    output_format="mp3",
    sample_rate=24000,
)
```

## Engine Selection by Use Case

| Use case | Recommended engine | Rationale |
|---|---|---|
| i-ARIF identity narration | MiniMax speech-2.8-hd | Voice_id continuity |
| Voice-to-voice realtime | Qwen-Omni / MiniMax realtime | Latency + cloned voice |
| Voice notes to Arif | ChatTTS | Qualia tokens feel like real voice |
| Bulk document narration | Edge | Free, fast, good enough |
| Multilingual code-switch | Fish Speech | Audio LM handles mixing |
| Quick zero-shot clone (no i-ARIF) | F5-TTS | Fastest path to a voice |
| Sensitive / sovereign content | MiniMax or local F5-TTS | F11 audit + receipt |

## ΔS Discipline

Per `AAA-audio-emd-pipeline` Phase 3:

- The encoder may not introduce qualia not authorized by `acoustic_intent`.
- `[laugh]` token in `acoustic_intent` MUST be matched by an engine that
  honors the token (ChatTTS). Routing to F5-TTS silently drops the
  token — return VOID and surface.

## F13 SOVEREIGN Gates

| Operation | Tier | Required |
|---|---|---|
| Mint new voice_id | F13 | `human_approval_token` |
| Modify existing voice_id | F13 | `human_approval_token` |
| Borrow existing voice_id | F11 | Audit receipt only |
| Engine switch for same voice_id | F2 | Document the change |
| Adding `[laugh]` token to i-ARIF synthesis | F13 | Review by Arif |
| Switching to Edge fallback (identity lost) | F11 | Log + receipt |

## When to Load This Skill

- Choosing a TTS engine for a new pipeline.
- Auditing engine selection in an existing pipeline.
- Switching engines after quota / latency issue.
- Wiring qualia tokens (`[laugh]`, `[breath]`) into agent output.
- Deciding local vs cloud for VRAM / sovereignty reasons.

## Integration Points

- **Doctrine parent**: `/root/AAA/skills/AGI-audio-quantum-cognition/SKILL.md`
- **EMD pipeline (Phase 3)**: `/root/AAA/skills/AAA-audio-emd-pipeline/SKILL.md`
- **MiniMax binding**: `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/SKILL.md`
- **Qwen binding**: `/root/AAA/skills/AAA-voice-cloning-qwen-cloud/SKILL.md`
- **ASR binding**: `/root/AAA/skills/AAA-asr-glm-ingest/SKILL.md`
- **Edge fallback**: `/root/.kimi-code/skills/tts-edge-fallback/SKILL.md`
- **Audio analysis**: `/root/.agents/skills/audio-analysis/SKILL.md`

## Related Skills

- `AGI-audio-quantum-cognition` — Physics + floors
- `AAA-audio-emd-pipeline` — Phase 3 orchestration
- `AGI-multimodal-bridge` — Cross-modal evidence
- `music-intelligence` — Governed music generation (sibling domain)
- `aaa-pdf-voice-protocol` — Federation → human translation

---

*Catalog forged 2026-08-18. F2 evidence: derived from open-source papers (ChatTTS, F5-TTS, E2-TTS, Fish Speech) + MiniMax technical spec + Edge TTS documentation. F7 confidence cap applies to all qualitative claims.*