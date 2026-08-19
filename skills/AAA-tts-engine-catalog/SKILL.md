---
name: AAA-tts-engine-catalog
description: "TTS engine registry for the arifOS federation. ChatTTS (qualitative conversational), F5-TTS / E2-TTS (zero-shot flow matching), Fish Speech (audio language model), MiniMax speech-2.8-hd (HD commercial), Edge / Mulberry (free fallback), MiMo Token Plan (Xiaomi multimodal subscription). Trade-off matrix, F13 governance, and routing rules. Single source of truth for which engine to use when."
version: 1.1.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
revised: 2026-08-19
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
  - AAA-voice-cloning-mimo-minimax
tags:
  - audio
  - tts
  - chattts
  - f5-tts
  - e2-tts
  - fish-speech
  - minimax
  - mimo
  - token-plan
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

## 6. MiMo Token Plan — Credit Economics & F13 Scope

> The Xiaomi MiMo V2.5 family is the federation's primary subscription-backed
> multimodal surface (text + image + audio). Quoted from the official
> Token Plan pricing page — https://mimo.mi.com/docs/en-US/price/token-plan
> (probed 2026-08-19, F2 cite).

### Catalog (6 active models)

| Model | Modality (in / out) | Role |
|---|---|---|
| `mimo-v2.5-pro` | text / text | Flagship reasoning (1M ctx, ~10× cheaper than v3 at output) |
| `mimo-v2.5` | text+image / text | Multimodal LLM (1M ctx, native image understanding) |
| `mimo-v2.5-asr` | audio / text | Speech-to-text (billed per audio-hour, not per token) |
| `mimo-v2.5-tts` | text / audio | Base TTS |
| `mimo-v2.5-tts-voiceclone` | text+audio / audio | Zero-shot voice clone (F13-gated identity) |
| `mimo-v2.5-tts-voicedesign` | text / audio | Prompt-driven voice design (Penang path) |

**Deprecated 2026-06-30**: `mimo-v2-pro`, `mimo-v2-omni`, `mimo-v2-tts` (V2 family sunset).

### Credit Deduction (per Token — language models)

| Model | Cache hit | Cache miss | Output |
|---|---|---|---|
| `mimo-v2.5-pro` | 2.5 | 300 | 600 |
| `mimo-v2.5` | 2 | 100 | 200 |

### ASR pricing

`mimo-v2.5-asr` is billed by audio duration: **30 M credits / hour** (seconds-precision, rounded up to hours).

### TTS pricing

All TTS series (`mimo-v2.5-tts`, `...-voiceclone`, `...-voicedesign`) are
**free for a limited time** — do not deduct package credits. Use them aggressively.

### Plan tiers (monthly credits)

| Tier | Monthly Credits | USD/mo | CNY/mo | mimo-v2.5 rounds (medium-complex) |
|---|---|---|---|---|
| Lite | 4.1 B | $6 | ¥39 | ~200 |
| Standard | 11 B | $16 | ¥99 | ~1,600 |
| Pro | 38 B | $50 | ¥329 | ~5,600 |
| Max | 82 B | $100 | ¥659 | ~12,800 |

Annual tiers: ~12× monthly volume at **88% off** (Lite $63.36/yr).
First-purchase discount: **12% off** (one-time per account, not on annual).
Off-peak discount: **0.8× consumption** during BJT 00:00–08:00 (UTC 16:00–24:00).

### Endpoints

| Region | URL | Use |
|---|---|---|
| Singapore (default) | `https://token-plan-sgp.xiaomimimo.com/v1` | OpenAI-compat |
| Singapore (Anthropic) | `https://token-plan-sgp.xiaomimimo.com/anthropic` | Claude Code / Hermes Anthropic-compat |

### F13 SOVEREIGN Scope (license-binding)

Verbatim from the Token Plan page:

> "The Token Plan package quota can only be used in programming tools
> (such as OpenClaw, OpenCode, etc.), and is prohibited from being
> used in the form of API calls for request behaviors in clearly
> non-Coding scenarios such as automated scripts and custom
> application backends."

**Consequence for arifOS**: All production Token Plan traffic MUST
flow through a Forge Instrument harness (`opencode`, `claude`,
`codex`, `kimi`, `qwen`, `grok`) or the OpenClaw gateway. Direct
`curl`/SDK calls from custom backends or batch scripts are
PROHIBITED under the license. Connectivity probes for testing are
permitted (F2) but MUST be tagged `[PROBE-NON-PRODUCTION]` and
not exercised in CI/cron loops.

### Δ·Ω·Ψ meta-mesa (multimodal coherence)

| Axis | MiMo Token Plan reality |
|---|---|
| **Δ substrate** | 6 models × {text, image, audio} modalities; credits as cost unit; SGP endpoint |
| **Ω operation** | ASR (30M/h), TTS (free), LLM (per-token w/ cache hit), routing via `fed_route` |
| **ΦΙ meaning** | VoiceState preservation, dialect capability (Penang-Besi path), identity continuity for i-ARIF, cost discipline via cache hit |

## Trade-off Matrix (canonical)

| Engine | Latency | Zero-shot clone | Qualia tokens | VRAM cost | Sovereign |
|---|---|---|---|---|---|
| **ChatTTS** | Medium | Hard (fine-tune) | **Highest** | ~4 GB | Open |
| **F5-TTS** | Fast | Excellent (3–10 s) | High (from ref) | ~4 GB | Open |
| **Fish Speech** | Slow | Excellent | High (semantic) | ≥ 8 GB | Open |
| **MiniMax 2.8-hd** | Variable | Via mimo-v2.5 | High | N/A cloud | F13 |
| **Edge** | Lowest | None | Low | N/A edge | Open |
| **MiMo Token Plan** | Variable (SGP) | Excellent (voiceclone) | High (voicedesign) | N/A cloud | F13 + license-scope |

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