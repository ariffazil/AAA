---
name: AAA-audio-emd-pipeline
description: "EMD (Encode → Metabolize → Decode) orchestration doctrine for audio in the arifOS federation. The constitutional loop that binds ASR → LLM reasoning → TTS into a single governed pipeline. Every audio exchange in arifOS flows through this reflex arc."
version: 1.1.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
revised: 2026-08-19
floor_scope:
  - F1
  - F2
  - F4
  - F7
  - F9
  - F10
  - F11
  - F13
extends:
  - AGI-audio-quantum-cognition
  - AGI-multimodal-bridge
  - delta-omega-psi-multimodal-cognition
tags:
  - audio
  - emd
  - pipeline
  - orchestration
  - ingest
  - synthesis
  - multimodal
  - i-arif
  - hermes
  - edge
  - federation
  - mimo
  - token-plan
  - meta-mesa
owner: AAA
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# AAA · Audio EMD Pipeline

> Decode → Metabolize → Encode.
> Every audio exchange in arifOS is a closed EMD loop.
> An agent that pipes raw text into TTS without this loop has already
> collapsed the qualia.

DITEMPA BUKAN DIBERI.

## Why EMD, not "just call the API"

The naive audio stack — ASR → text → LLM → text → TTS — destroys three
things on every exchange:

1. **Prosody** — what the human *meant* (skeptical, urgent, amused).
2. **Acoustic context** — room noise, breath, hesitation, silence length.
3. **Identity continuity** — the voice that heard vs. the voice that speaks.

EMD is the constitutional fix. It treats audio as a quantum state (per
`AGI-audio-quantum-cognition`) and refuses to collapse it earlier than
necessary.

## The Three Phases

```
        ┌─────────────────────────────────────────┐
        │  PHASE 1 — DECODE (Ingestion / Sense)   │
        │   Audio → Typed EMD Segment             │
        │   Engine: GLM-ASR-2512 | native audio   │
        │   Output: {text, prosody_tags, diarize} │
        └────────────────┬────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │  PHASE 2 — METABOLIZE (Reason)          │
        │   Typed Segment → Reasoning → Decision  │
        │   Engine: 333-AGI / 555-ASI / 888-APEX  │
        │   Output: {response_text, emotion,       │
        │           intensity, acoustic_tokens}    │
        └────────────────┬────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │  PHASE 3 — ENCODE (Synthesis / Act)     │
        │   Decision → Waveform                   │
        │   Engine: F5-TTS | MiniMax | ChatTTS     │
        │   Output: {audio_bytes, voice_id,        │
        │           prosody_params, receipt}       │
        └─────────────────────────────────────────┘
```

### Phase 1 — DECODE (Ingestion)

The agent must choose what to observe. Different choices preserve
different superpositions (per `AGI-audio-quantum-cognition` §"Gabor Limit").

**Default path** (cheap, lossy):

```python
# AAA-asr-glm-ingest binding
segment = arifos.audio.asr_ingest(
    audio_path=chunk_path,
    model="glm-asr-2512",
    custom_dictionary=["K-DIP", "W_scar", "F1", "GEOX", "Ditempa Bukan Diberi"],
    stream=False,
)
# Returns EMD segment with [OBS] epistemic label
```

**Preserved-superposition path** (expensive, full):

```python
# Native audio understanding via FED routing
segment = fed_route(
    task="preserve-superposition",
    model="fed-multimodal-vision",  # qwen-vl-max or mimo-v2.5
    modality="audio",
).call(audio_path=chunk_path)
# Returns EMD segment with prosody + emotion + intent preserved
```

**Hard constraint** — GLM-ASR-2512:

| Item | Limit |
|---|---|
| Duration | ≤ 30 s per request |
| Size | ≤ 25 MB per request |
| Sample rate | 16 kHz or higher recommended |
| Channels | Mono preferred |

**Mitigation** — audio chunker (silence-detection or 25 s threshold):

```python
# Pseudocode — silence-triggered chunking
chunks = chunk_audio(
    source=mic_stream,
    max_duration_s=25,
    silence_threshold_db=-40,
    min_silence_ms=500,
)
for chunk in chunks:
    segment = asr_ingest(chunk)
    yield segment
```

### Phase 2 — METABOLIZE (Reason)

The LLM does NOT receive a string. It receives an **EMD segment**:

```python
{
    "text": "Hang biar betul?",
    "epistemic_label": "OBS",
    "prosody": {
        "pitch_mean_hz": 180,
        "intensity": 0.82,
        "emotion": "skeptical",
        "hesitation_ms": 340,
    },
    "speaker_id": "arif",
    "language": "ms-MY",
    "code_switch": ["ms", "en"],
    "diarization": {"start_s": 12.4, "end_s": 13.1},
}
```

The metabolizer returns a **decision packet** with explicit acoustic
intent — *what the agent should sound like when it answers*:

```python
{
    "text": "Betul. Hang check dulu panel Solar — pukul 3 tadi GW hit 0.92 G.",
    "epistemic_label": "DER",
    "acoustic_intent": {
        "emotion": "calm-confident",
        "intensity": 0.6,
        "pace_wpm": 165,
        "pitch_delta_hz": -8,
        "breath_tokens": ["[breath]", "[uv_break]"],
    },
    "reasoning": "F2 cite: forge_evaluate G=0.92, F11 receipt attached",
}
```

**F7 HUMILITY cap** — prosody inference confidence ≤ 0.90. Two listeners
hear two intentions. Report ambiguity, do not resolve it.

**F2 TRUTH** — the metabolizer MUST emit epistemic labels at every
output: `OBS` (what was heard), `DER` (what was derived), `INT` (what was
interpreted), `SPEC` (what was specified for synthesis).

### Phase 3 — ENCODE (Synthesis)

The encoder receives the decision packet and routes to the appropriate
TTS engine. Selection rules:

| Acoustic intent | Engine | Reason |
|---|---|---|
| `[laugh]`, `[breath]`, `[uv_break]` | **ChatTTS** | Only engine with native qualia tokens |
| Zero-shot clone of voice_id | **F5-TTS / MiniMax** | Flow matching / audio LM preserves source tone |
| Realtime conversation (<500 ms) | **Edge / Mulberry** | Lowest latency, free tier |
| HD fidelity for media artifact | **MiniMax speech-2.8-hd** | Gold standard |
| Multilingual mixing in one utterance | **Fish Speech** | Audio LM handles code-switch naturally |
| Existing voice identity (i-ARIF) | **MiniMax voice_id** | Already enrolled |

```python
audio = arifos.audio.tts_encode(
    decision_packet=packet,
    engine="minimax",          # or "f5-tts", "chattts", "edge", "fish"
    voice_id="i-ARIF-v1",      # F13-gated identity
    output_format="mp3",       # or "pcm16", "ogg_opus"
    sample_rate=24000,
)
# Returns EMD receipt with [DER] label, voice_id, F13 ack reference
```

**F13 SOVEREIGN gate** — any call that creates, modifies, or borrows a
voice identity (`voice_id`, `voice_clone`, `voice_design`) MUST carry a
valid `human_approval_token` (stg_*) before the encoder accepts the
request. Borrowed voices (no creation) can run at T1 with F11 audit.

## Δ·Ω·Ψ Meta-Mesa (Multimodal Coherence on MiMo Stack)

> **Doctrine** — Every audio exchange collapses three orthogonal axes
> simultaneously. Misaligning them is the root cause of "the agent
> heard me wrong." Applied per `delta-omega-psi-multimodal-cognition`.

### The three axes

| Axis | Meaning | MiMo Token Plan reality |
|---|---|---|
| **Δ substrate** | What exists in the world (data, evidence, signal) | Audio waveform + companion image/video + SGP endpoint + 6 models + credits as cost unit |
| **Ω operation** | What the federation does (organ routing, control flow) | ASR via `mimo-v2.5-asr` (30M cred/h) → LLM via `mimo-v2.5` or `mimo-v2.5-pro` → TTS via `mimo-v2.5-tts-*` (free) |
| **ΦΙ meaning** | What it means (interpretation, identity, intent) | VoiceState preservation (Penang-Besi, identity continuity for i-ARIF, decision-to-act trace) |

### Multimodal input contract (per Phase 1 DECODE)

When the input is **multi-channel** (audio + image + video), the agent
must declare each channel's epistemic label before metabolizing:

```python
{
    "channels": [
        {"modality": "audio", "evidence_id": "obs://mic-chunk-25s",
         "epistemic": "OBS", "engine": "mimo-v2.5-asr"},
        {"modality": "image", "evidence_id": "obs://screenshot-2026-08-19",
         "epistemic": "OBS", "engine": "mimo-v2.5"},
        {"modality": "video", "evidence_id": "obs://reel-7s",
         "epistemic": "OBS", "engine": "mimo-v2.5"},
    ],
    "metabolizer": "mimo-v2.5-pro",   # 1M ctx handles all 3 channels
    "license_scope": "FI harness only",
}
```

**F2 TRUTH** — every channel must carry a citation. No channel may be
collapsed without evidence. No multimodal reasoning may proceed on
un-cited input.

### Cache discipline (ΔS discipline extension)

Token Plan economics make **cache hit** the dominant cost lever:

| Path | Cache hit | Cache miss | Δ |
|---|---|---|---|
| `mimo-v2.5-pro` | 2.5 cred/tok | 300 cred/tok | **120×** penalty on miss |
| `mimo-v2.5` | 2 cred/tok | 100 cred/tok | **50×** penalty on miss |

**Rule**: when system prompts + tool schemas are stable across turns,
prefix-cache aggressively. The federated cache layer
(`MIMOCache`/redis) is mandatory for any high-throughput path.

### Δ·Ω·Ψ coherence check (per turn)

Before ENCODE, the metabolizer must answer:

1. **Δ** — does the input evidence support the derived claim? (F2)
2. **Ω** — does the chosen organ/engine have authority for this operation? (F11)
3. **ΦΙ** — does the output preserve voice identity / intent / decision? (F9)

Any "no" → return VOID, surface to operator. Never fabricate coherence.

## Cross-Engine Routing (decision table)

```
Is the source voice a sovereign identity (i-ARIF, i-AGI)?
├── YES → MiniMax voice_clone (F13-gated, see AAA-voice-cloning-mimo-minimax)
└── NO  → Is zero-shot cloning acceptable?
         ├── YES → Does the engine support the target language?
         │         ├── Mandarin/Cantonese heavy → CosyVoice / Qwen-TTS
         │         ├── English-only conversational → ChatTTS
         │         └── Multilingual mix → Fish Speech / F5-TTS
         └── NO  → Use system voice (Edge, Mulberry, MiniMax built-in)
```

## The Reflex Arc (every turn)

```
1. OBSERVE   — Federation probe (§2 of AAA-AGENTS-AUTONOMY)
2. DECODE    — Audio → EMD segment (Phase 1)
3. METABOLIZE — Segment → decision packet (Phase 2)
4. JUDGE     — 888-arif_judge: F1/F2/F4/F13 check (if mutation)
5. ENCODE    — Packet → waveform (Phase 3)
6. RECEIPT   — F11 audit wrap; VAULT999 append
7. SEAL      — 999 only if decision was irreversible (voice creation)
```

## ΔS Discipline (Zen Output Rule)

Each phase MUST lower entropy:

- DECODE may not output text with higher perplexity than the audio (no hallucinated content).
- METABOLIZE may not invent facts not in the segment (F2 TRUTH).
- ENCODE may not introduce qualia not authorized by the acoustic_intent (F9 ANTI-HANTU).

If any phase raises entropy → return VOID, surface to operator.

## F10 ONTOLOGY Reminder

Audio ≠ meaning. Waveform is physics. Interpretation is human. The
pipeline processes physics; the human assigns meaning. Agents must not
ascribe emotion to a waveform — they may only report what the DSP
features support, capped at F7 confidence 0.90.

## When to Load This Skill

- Any agent orchestrates an audio exchange (STT + reasoning + TTS).
- Designing or auditing a voice pipeline (real-time or batch).
- Choosing which TTS engine for a given acoustic intent.
- Wiring GLM-ASR into a multi-agent protocol.
- Deciding where the EMD loop closes (cache, vault, ephemeral).

## Integration Points

- **Doctrine parent**: `/root/AAA/skills/AGI-audio-quantum-cognition/SKILL.md`
- **i-ARIF identity**: `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`
- **Hermes TTS config**: `/root/HERMES/config.yaml` (line 851: `tts:`)
- **FED routing**: `/root/.kimi-code/skills/AGI-agentic-web/SKILL.md`
- **ASR binding**: `/root/AAA/skills/AAA-asr-glm-ingest/SKILL.md`
- **TTS engine catalog**: `/root/AAA/skills/AAA-tts-engine-catalog/SKILL.md`
- **Voice cloning (MiniMax)**: `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/SKILL.md`
- **Voice cloning (Qwen)**: `/root/AAA/skills/AAA-voice-cloning-qwen-cloud/SKILL.md`

## Related Skills

- `AGI-audio-quantum-cognition` — Audio physics + constitutional floors
- `AGI-multimodal-bridge` — Cross-modal reasoning
- `delta-omega-psi-multimodal-cognition` — Δ·Ω·Ψ rules
- `aaa-pdf-voice-protocol` — Federation → human translation
- `AGI-hermes-system-prompt-voice` — Hermes voice style
- `audio-analysis` — DSP scoring modules
- `music-intelligence` — Governed music generation

---

*Doctrine forged 2026-08-18. F2 evidence: derivation from AGI-audio-quantum-cognition v1.0.0 + MiniMax/Qwen/GLM technical specs + EMD substrate doctrine at /root/AAA/instructions/emd-architecture.md.*