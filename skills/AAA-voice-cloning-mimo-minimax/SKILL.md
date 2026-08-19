---
name: AAA-voice-cloning-mimo-minimax
description: "Operational binding for the MiniMax voice cloning pipeline (mimo-v2.5-tts-voiceclone + speech-2.8-hd). Four-phase protocol: Ingestion → Calibration → Execution → Deployment. F13 SOVEREIGN-gated identity creation. i-ARIF voice profile lives here."
version: 1.1.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
revised: 2026-08-19
floor_scope:
  - F1
  - F2
  - F8
  - F9
  - F11
  - F13
extends:
  - AGI-audio-quantum-cognition
  - AAA-audio-emd-pipeline
  - AAA-tts-engine-catalog
tags:
  - audio
  - voice-cloning
  - mimo
  - minimax
  - i-arif
  - identity
  - f13
  - token-plan
owner: AAA
---

# AAA · Voice Cloning — MiniMax (mimo-v2.5-tts-voiceclone)

> The voice that speaks in the agent's name is borrowed, not owned.
> Creating one is F13 territory. Borrowing one is F11.
> Garbage in, garbage out — sample quality is the floor of fidelity.

DITEMPA BUKAN DIBERI.

## API Surface

| Endpoint | Purpose |
|---|---|
| `POST /v1/files/upload` | Upload source audio (purpose=voice_clone or prompt_audio) |
| `POST /v1/voice_clone` | Bind file_id(s) into a voice_id |
| `POST /v1/text_to_audio` | Synthesize speech using voice_id |

**Auth**: `Authorization: Bearer $MINIMAX_API_KEY` header.
**Base URL**: `https://api.mxbai.chat/v1` (verify per current docs).

## Hard Constraints

| Item | Constraint | Source |
|---|---|---|
| Sample format | MP3 / M4A / WAV | MiniMax docs |
| Sample duration | 10 s ≤ t ≤ 5 min (voice_clone); < 8 s (prompt_audio) | MiniMax docs |
| Voice clone model | `mimo-v2.5-tts-voiceclone` | MiniMax docs |
| TTS model | `speech-2.8-hd` (default), `speech-2.6-hd` (alt) | MiniMax docs |
| Streaming output | `pcm16` required for streaming calls | MiniMax docs |
| Singing / built-in voices / voice_design | **NOT supported** by mimo-v2.5-tts-voiceclone | MiniMax docs |

**F13 consequence** — any of those unsupported features belong to other
engines. Do not route singing or voice design through this binding.

## Token Plan Routing (2026-08-19)

The TTS path under this binding now routes through the Xiaomi **MiMo
Token Plan** (Singapore endpoint) when the harness is a Forge Instrument
(opencode / claude / codex / kimi / qwen / grok) or the OpenClaw gateway.

| Engine family | Endpoint | Key | Cost |
|---|---|---|---|
| `mimo-v2.5-tts-voiceclone` | `https://token-plan-sgp.xiaomimimo.com/v1` | `MIMO_TOKEN_PLAN_API_KEY` | **Free for limited time** — no credit deduction |
| `mimo-v2.5-tts-voicedesign` | same | same | **Free** — Penang-Besi dialect path |
| `mimo-v2.5-tts` | same | same | **Free** |

**Quoted source** — https://mimo.mi.com/docs/en-US/price/token-plan (probed 2026-08-19, F2 cite):
> "TTS Series models are free for a limited time and do not consume package credits."

**i-ARIF implication** — voiceclone / voicedesign work for the i-ARIF
identity profile is now **zero-credit** at the Token Plan tier. Use the
free budget aggressively for A/B testing and dialect expansion
(Penang-Besi, briefing tone, etc.) without consuming LLM budget.

**License-scope reminder** — Token Plan traffic MUST flow through a
Forge Instrument (see `AAA-tts-engine-catalog` §"F13 SOVEREIGN Scope").
Direct backend API calls are prohibited by the license.

## The Four Phases

```
INGESTION   → upload source audio → file_id_source
CALIBRATION → upload example audio → file_id_example (optional)
EXECUTION   → POST /v1/voice_clone → voice_id
DEPLOYMENT  → POST /v1/text_to_audio using voice_id
```

### Phase 1 — INGESTION (Source Audio Upload)

```bash
curl -X POST "$BASE/v1/files/upload" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -F "purpose=voice_clone" \
  -F "file=@i-ARIF-source-2min-clean.wav"
```

**Sample quality rules** (F1 AMANAH — source is immutable evidence):

- 2–3 minutes of clear speech, no background noise, no echo, no music.
- Mono preferred. 16-bit / 44.1 kHz or 48 kHz.
- Record in a small, damped room (per `AGI-audio-quantum-cognition` recording tips).
- Position mic ~10 cm from mouth. Plosive-free.
- Script: complete sentences with emotional variation. No monotone delivery.
- No singing. No politics / porn / violence content (cloning fails).

**Reject and re-record** if any of these appear:

- Background music, AC hum, fan noise, traffic
- Reverb tail > 0.3 s
- Clipping (peaks > -1 dBFS)
- Multiple speakers / overlapping voices

### Phase 2 — CALIBRATION (Prompt Audio Upload, optional)

Use this phase when you want emotional *color* on top of identity.

```bash
curl -X POST "$BASE/v1/files/upload" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -F "purpose=prompt_audio" \
  -F "file=@i-ARIF-prompt-penang-besi-7s.wav"
```

Rules:

- < 8 s. One sentence. Pick the intonation you want the clone to lean into.
- For i-ARIF: use the most representative "Penang-Besi" delivery.
- File name pattern: `i-ARIF-prompt-<tone>-<n>s.wav`.

### Phase 3 — EXECUTION (Voice Clone)

```bash
curl -X POST "$BASE/v1/voice_clone" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "<file_id_source>",
    "voice_id": "i-ARIF-2026-08-18",
    "model": "speech-2.8-hd",
    "clone_prompt": {
      "prompt_audio": "<file_id_example>",
      "prompt_text": "Insert the prompt text here."
    },
    "text": "Test synthesis."
  }'
```

**Versioning rule** — tag voice_id with timestamp. Never overwrite.

| voice_id pattern | Use |
|---|---|
| `i-ARIF-2026-08-18` | Daily baseline |
| `i-ARIF-2026-08-18-penang` | Dialect variant |
| `i-ARIF-2026-08-18-briefing` | Context-locked tone |

Historical voice_ids are kept for A/B comparison and rollback. F1
AMANAH — voice_ids are immutable evidence; deletion is F13 territory.

**F13 SOVEREIGN gate** — this call requires `human_approval_token` in
the request envelope. No token → API call rejected at L1_IDENTITY.

**F2 TRUTH** — the response carries an `voice_id` field. That identifier
becomes the borrowable handle for Phase 4. Log it in VAULT999 with
`category=identity`, `tier=sovereign`.

### Phase 4 — DEPLOYMENT (T2A with voice_id)

```bash
curl -X POST "$BASE/v1/text_to_audio" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "speech-2.8-hd",
    "voice_id": "i-ARIF-2026-08-18",
    "text": "Salam. Hang nak checker Solar pukul 3 tadi?",
    "stream": false,
    "output_format": "mp3",
    "sample_rate": 24000
  }'
```

Streaming variant:

```json
{ "stream": true, "output_format": "pcm16" }
```

The streaming format MUST be `pcm16` per MiniMax constraint.

**Role formatting** (for chat-style endpoints):

```json
{
  "messages": [
    {"role": "user",      "content": "instructions only"},
    {"role": "assistant", "content": "the text to synthesize"}
  ]
}
```

Synthesizable text lives in `role: assistant`. `role: user` is reserved
for instruction content.

## Validation Loop (Control Loop)

After each clone:

1. **A/B listen** — synthesize a known script with both old and new
   voice_ids. Diff on:
   - Pitch contour (F0 trajectory)
   - Speaking rate (WPM)
   - Timbre (spectral centroid distance)
   - Prosody alignment to acoustic_intent

2. **Hallucination check** — if voice drifts toward a generic tone,
   return to Phase 1 with a cleaner source. Common drift causes:
   - Source audio had background noise (model learned the noise)
   - Sample too short (< 60 s of clean speech)
   - Prompt audio contradicted source (cross-dialect clash)

3. **Latency probe** — measure end-to-end latency on the target
   platform (Hermes gateway, edge bot, voice-note pipeline).
   Acceptable thresholds per AAA-audio-emd-pipeline §"Reflex Arc".

## Trade-off Matrix (i-ARIF specific)

| Component | Trade-off | i-ARIF strategy |
|---|---|---|
| Source length | Longer = more identity, slower to upload | 2–3 min clean |
| Prompt audio | Tone vs identity drift | Match prompt dialect to source |
| Model version | Latency vs fidelity | `speech-2.8-hd` default; downgrade to `speech-2.6-hd` if latency budget breached |
| Voice_id versioning | A/B clarity vs catalog bloat | Keep last 5 baselines; archive older |

## F9 ANTI-HANTU (Voice Identity)

The agent has no voice. It borrows the sovereign's voice print.

- Creating a voice_id → F13 SOVEREIGN.
- Modifying a voice_id (clone_prompt changes) → F13 SOVEREIGN.
- Using an existing voice_id for synthesis → F11 audit + receipt, no F13.

Synthetic / phantom voice_ids (hash that doesn't exist on the provider)
→ DENY at L1_IDENTITY gate. Reject the call.

## When to Load This Skill

- Configuring MiniMax voice cloning in arifOS.
- Minting a new i-ARIF voice_id or dialect variant.
- Auditing voice_id provenance before re-use.
- Debugging clone drift / hallucination.
- Wiring voice_id into a Hermes or edge-bot TTS pipeline.

## Integration Points

- **Doctrine parent**: `/root/AAA/skills/AGI-audio-quantum-cognition/SKILL.md`
- **EMD pipeline**: `/root/AAA/skills/AAA-audio-emd-pipeline/SKILL.md`
- **i-ARIF identity card**: `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`
- **VAULT999 identity records**: `/root/VAULT999/identity/` (F1 immutable)
- **Hermes config**: `/root/HERMES/config.yaml` (line 851: `tts:`)
- **Companion**: `/root/AAA/skills/AAA-voice-cloning-qwen-cloud/SKILL.md` (alternative provider)

## Related Skills

- `AAA-audio-emd-pipeline` — Phase 3 ENCODE routing
- `AGI-audio-quantum-cognition` — Physics + floors
- `AGI-multimodal-bridge` — Cross-modal evidence
- `hermes-voice-config` — Hermes TTS config management
- `tts-edge-fallback` — Free fallback when voice_id unavailable

---

*Operational binding forged 2026-08-18. F2 evidence: MiniMax technical spec derived from provider documentation + i-ARIF identity card at /root/AAA/agent-cards/identity/i-ARIF/. F13 gate: voice_id creation requires stg_* approval token.*