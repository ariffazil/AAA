---
name: AAA-voice-cloning-mimo-minimax
description: "Clone and deploy sovereign voice profiles on MiniMax engine."
version: 1.0.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
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
tags:
  - audio
  - voice-cloning
  - mimo
  - minimax
  - i-arif
  - identity
  - f13
owner: AAA
capability_tier: fed-realtime-voice
ecology_state: WARM
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
| `POST /v1/t2a_v2` | Synthesize speech using voice_id |

**Auth**: `Authorization: Bearer $MINIMAX_API_KEY` header.
**Base URL**: `https://api.minimax.io/v1` (verified live KVM4 + KVM8).
**Env hint**: `MINIMAX_API_HOST` may override the base URL on each host.

**Endpoint paths** (use exactly these):
- TTS: `POST /v1/t2a_v2` — NOT `/v1/text_to_audio` (older doc path; current API path is `/v1/t2a_v2`)
- Voice clone: `POST /v1/voice_clone`
- Source upload: `POST /v1/files/upload`

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

**Canonical pitfalls — read before any TTS call:**

1. **MiMo Token Plan is NOT the engine.** `token-plan-sgp.xiaomimimo.com` (`tp-…` key) returns 429 quota exhausted and exposes no `/t2a_v2`, `/voice_clone`, or `/files/upload` route. Always use `https://api.minimax.io/v1` with the `sk-cp-…` key. If you see a `tp-` prefixed key in env, swap to `MINIMAX_API_KEY` before calling.

2. **`data.audio` is HEX, not base64.** Decode with `bytes.fromhex(...)`. Base64 decoding produces garbage. Success indicator: `base_resp.status_code == 0`.

3. **Before minting a new voice_id, scan the federation.** Check `/root/.openclaw/workspace/voice/` (KVM4) and `/root/.hermes/voice/` (KVM8) for an existing canonical alias matching the request. If a sealed voice_id already exists (e.g. `SSSiti20260926v1` for "SS" trigger), reuse it — never mint a parallel ID. Duplicate voice_ids across hosts = drift.

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

### Phase 4 — DEPLOYMENT (TTS with voice_id)

```bash
curl -X POST "$BASE/v1/t2a_v2" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "speech-2.8-hd",
    "voice_id": "i-ARIF-2026-08-18",
    "text": "Salam. Hang nak checker Solar pukul 3 tadi?",
    "stream": false,
    "voice_setting": {"voice_id": "i-ARIF-2026-08-18", "speed": 1.0},
    "audio_setting": {"sample_rate": 24000, "format": "mp3"}
  }'
```

**Response shape** (verify before writing):
```json
{"base_resp": {"status_code": 0, "status_msg": "success"}, "data": {"audio": "<hex-string>", ...}}
```

**Decode pitfall (always-on):** `data.audio` is HEX, NOT base64. Use `bytes.fromhex(...)`. Base64 decoding produces garbage. Success indicator: `base_resp.status_code == 0`.

**Conversion for Telegram voice bubble:**
```bash
ffmpeg -y -i out.mp3 -c:a libopus -b:a 48k -ar 16000 -ac 1 out.ogg
```

Opus `.ogg`, 16 kHz mono, 48 kbps. This is the format Telegram accepts as a native voice bubble.

Streaming variant: `{"stream": true, "output_format": "pcm16"}`. Streaming format MUST be `pcm16` per MiniMax constraint.

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
- Trigger phrase detected: `SS` / `suara SS` / `voice SS` / `suara Siti` (or any other voice-alias trigger in `signal_triggers` of an existing canonical card).
- Federation canonical audit: "is this voice_id already sealed somewhere?" — check `/root/.openclaw/workspace/voice/` and `/root/.hermes/voice/` first.

## Trigger Phrase Convention

Voice aliases are surface-triggered by short phrases in user chat. Pattern:

| Phrase | Voice |
|---|---|
| `SS` / `suara SS` / `voice SS` / `suara Siti` | `SSSiti20260926v1` |
| `i-ARIF` / `suara aku` / `voice aku` | `i-ARIF-20260819T084602` |
| `default` / `BossyLeader` | `voice-male-bossyleader` (fallback) |

Parse: token at message start = trigger; remainder = TTS text. If multiple aliases, use the longest match first.

## Reference Files

- `references/federation-voice-id-canonicalization.md` — how one voice_id serves multiple hosts without drift.

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