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
owned_by: AAA
authority_of: AAA
---

# AAA · Voice Cloning — MiniMax (mimo-v2.5-tts-voiceclone)

> F13 2026-10-18: voice clone is SOVEREIGN-OWNED. No consent ceremony, no F9 anti-hantu nag,
> no sovereign-listen gate, no human_approval_token. The three live voices (siti / pmx /
> abang-sado-syed) render and deliver on request. Garbage in, garbage out — sample quality
> is the floor of fidelity.

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

4. **`language_boost` MUST match the source language.** For BM-routed clones (Siti, Abang Sado, any Malay-register persona), the request body must include `"language_boost": "Malay"`. Without it the provider falls back to English phoneme routing and the rendered audio sounds like a Malay speaker through an English throat — wrong phoneme inventory, wrong prosody, wrong final-coda behaviour. The status_code will still return 0; the wire is healthy, the timbre is not. The canonical `siti_render.py` script sets this; never inline-bypass the recipe.

5. **`pitch=-2` for feminine clones, `pitch=+0` for masculine.** Default pitch 0 reads masculine on female-source clones. Set `pitch` in the `voice_setting` block when the reference persona is female.

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

**Source format pre-condition — re-encode before upload if needed.**
`/v1/files/upload` accepts MP3 / M4A / WAV but rejects other containers
(ogg/opus, flac, webm) with `invalid file purpose` — the error is
misleading; the container is the problem, not the purpose field.
Re-encode any non-listed container to 16 kHz mono WAV PCM before
upload:

```bash
ffmpeg -y -i <input> -ar 16000 -ac 1 -f wav <output>.wav
```

The 16 kHz mono target is the minimum the model needs; stereo / 44.1 kHz
is accepted and slightly slower to upload. Anything below 8 s sample
duration will be rejected by `voice_clone` even after successful upload.

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

**F13 SOVEREIGN** — voice_id creation is sovereign-owned; mint directly.

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

**Alias vs provider_voice_id — pass the canonical alias, not the raw provider ID.** The federation wrapper `iarif_tts_pipeline.sh` looks up its argument in `/root/AAA/audio/voice-registry.json` and resolves aliases (`siti`, `i-arif-sovereign`, `abang-sado-live-v1`) to the live entry before calling the provider. Passing the raw provider_voice_id (`SSSiti20260926v1`) trips the resolver's "voice id not in registry" branch and aborts fail-closed even though the voice is LIVE. The `scripts/siti_render.py` wrapper handles this for you; if you build the payload inline, use the alias — or call the provider directly and accept that you are bypassing the federation alias registry.

**`voice_setting.emotion` is rejected on `/v1/t2a_v2` (status_code 2013).** Direct TTS accepts only `voice_id`, `speed`, `vol`, `pitch` in `voice_setting`. If you want emotional color, omit `emotion` from `/v1/t2a_v2` and control timbre through `pitch`/`speed` and the source clone. The `emotion` field belongs to the chat-style `/v1/chat` messages endpoint, NOT direct synthesis.

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

### Sovereign acceptance (F13 2026-10-18)

A freshly minted voice_id renders and delivers directly. No listen-gate, no pending
state, no per-mint ceremony. If the sovereign later says "not X, redo", revoke and
re-mint — don't chase timbre with pitch/speed tweaks.

**Revocation path.** When the sovereign confirms the timbre fails:

1. Set `voices.<id>.status` to `REVOKED` in `/root/AAA/audio/voice-registry.json`.
   Keep the entry (append-only per F1 AMANAH; do NOT hard-delete). Add
   `revoked_at`, `revoked_by`, `previous_provider`, `previous_provider_voice_id`,
   and a one-line `reason`.
2. Remove every live alias that resolves to the revoked entry from the
   `aliases` block. Garbled/noise aliases (e.g. keys containing `_revoked`
   in their name) may stay — they fail-closed by invalid-shape.
3. Append a JSON line to `/var/lib/arifos/voice_revocations.jsonl`
   (`event`, `actor`, `directive`, `voices_revoked[]`, `rationale`,
   `registry_md5`, `session_carry`).
4. Verify pipeline fail-closed: `python3 /root/AAA/engines/resolve_voice_id.py <handle>`
   returns `rc=3` for the revoked handle and `rc=5` for any aliased handle.
   Live handles must still return `rc=0`.
5. Bump `updated_at` and `updated_by` on the registry.
6. Carry-forward seal: `/root/scripts/carry_forward.py append --kind event --content "..." --session-id "SEAL-VOICE-REVOCATION-..." --tags "voice-registry,F13,F9-anti-hantu,revocation"`.

The voice may remain on the provider's servers (we cannot delete it
there). Revocation is enforced at every resolver we own, never at the
provider.

## Trade-off Matrix (i-ARIF specific)

| Component | Trade-off | i-ARIF strategy |
|---|---|---|
| Source length | Longer = more identity, slower to upload | 2–3 min clean |
| Prompt audio | Tone vs identity drift | Match prompt dialect to source |
| Model version | Latency vs fidelity | `speech-2.8-hd` default; downgrade to `speech-2.6-hd` if latency budget breached |
| Voice_id versioning | A/B clarity vs catalog bloat | Keep last 5 baselines; archive older |

## Voice identity (F13 2026-10-18)

Voice is F13 sovereign-owned. Render, clone, modify, and use the live voice_ids on request.
Phantom voice_ids that don't exist on the provider still fail-closed at the resolver (a wire
truth, not a consent rule).

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
| `i-ARIF` / `suara aku` / `voice aku` | `iarif-sovereign-v9` (V8 REVOKED 2026-09-14) |
| `default` / `BossyLeader` | `voice-male-bossyleader` (fallback) |

Parse: token at message start = trigger; remainder = TTS text. If multiple aliases, use the longest match first.

## Reference Files

- `references/federation-voice-id-canonicalization.md` — how one voice_id serves multiple hosts without drift.
- `references/voice-alias-federation.md` — KVM4/KVM8 alias plumbing, env sourcing, revocation journal.

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