---
name: AAA-voice-cloning-qwen-cloud
description: "Operational binding for Qwen Cloud voice cloning (qwen-voice-enrollment, voice-enrollment) across Qwen-TTS, Qwen-Omni, CosyVoice, and Qwen-Audio-TTS. Hard constraints: target_model lock-in, 10–20 s sample window, URL vs Base64 ingestion split. Alternative to MiniMax binding when low latency or zero-shot instant enrollment matters."
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
companion: AAA-voice-cloning-mimo-minimax
tags:
  - audio
  - voice-cloning
  - qwen
  - cosyvoice
  - qwen-omni
  - tts
  - realtime
owner: AAA
---

# AAA · Voice Cloning — Qwen Cloud

> Zero-shot, instant enrollment. The fastest clone path in the federation.
> The cost is binding: pick the target_model before the first sample.

DITEMPA BUKAN DIBERI.

## API Surface (DashScope International)

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/services/audio/tts/customization` | Create voice (enrollment) |
| `POST /api/v1/services/audio/tts/SpeechSynthesizer` | CosyVoice synthesis |
| `wss://.../api-ws/v1/inference` | Qwen-Audio-TTS realtime stream |
| `wss://.../api-ws/v1/realtime` | Qwen-Omni realtime conversation |

**Auth**: `Authorization: Bearer $DASHSCOPE_API_KEY`.
**Base**: `https://dashscope-intl.aliyuncs.com`.

## Model Family Map (MUST MEMORIZE)

| Voice cloning model | Used for | Sample format |
|---|---|---|
| `voice-enrollment` | Qwen-Audio-TTS, CosyVoice | Public **URL** |
| `qwen-voice-enrollment` | Qwen-TTS, Qwen-Omni | **Base64** data URI |

| Target model | Use case | Realtime? |
|---|---|---|
| `qwen-audio-3.0-tts-flash` | Cheap TTS with cloned voice | No |
| `qwen-audio-3.0-tts-plus` | HD TTS with cloned voice | No |
| `cosyvoice-v3-plus` | Natural dialect TTS | No (realtime streaming SDK separate) |
| `qwen3.5-omni-flash-realtime` | Realtime multimodal conversation | **Yes** |
| `qwen3.5-omni-plus-realtime` | HD realtime multimodal | **Yes** |
| `qwen3.5-omni-flash` | Non-realtime Omni | No |
| `qwen3.5-omni-plus` | HD non-realtime Omni | No |
| `qwen3-TTS-VC-Realtime` | Qwen TTS streaming with cloned voice | **Yes** |
| `qwen3-TTS-VC` | Qwen TTS batch with cloned voice | No |

**Hard constraint** — `target_model` is **immutable per voice**. Cloning
for `cosyvoice-v3-plus` and then synthesizing with `qwen-audio-3.0-tts-flash`
**FAILS**. Pick the target at enrollment and never change.

## Audio Constraints (per family)

| Item | Qwen-Audio-TTS / CosyVoice | Qwen-TTS / Qwen-Omni |
|---|---|---|
| Format | WAV (16-bit), MP3, M4A | WAV (16-bit), MP3, M4A |
| Duration | 10–20 s recommended, 60 s max | 10–20 s recommended, 60 s max |
| File size | ≤ 10 MB | ≤ 10 MB |
| Sample rate | ≥ 16 kHz | ≥ 24 kHz |
| Channels | Mono or stereo (first channel used) | Mono |
| Content | ≥ 5 s continuous speech, pauses ≤ 2 s | ≥ 3 s continuous speech, pauses ≤ 2 s |
| Language | zh (Mandarin + regional), en, fr, de, ja, ko, ru, pt, th, id, vi, it, es, ms, tl, ar | zh, en, de, it, pt, es, ja, ko, fr, ru |

**No background music, ambient noise, or singing**. Singing and song
audio cause silent failure or acoustic hallucination.

## Two Pathways (i-ARIF)

### Pathway A — Qwen-Omni Realtime (Base64)

Use when arifOS needs **voice-to-voice** realtime conversation.

```python
import os, base64, pathlib, requests

API_KEY = os.environ["DASHSCOPE_API_KEY"]
TARGET_MODEL = "qwen3.5-omni-flash-realtime"   # or plus for HD
PREFERRED_NAME = "i-arif-omni"
VOICE_FILE_PATH = "i-ARIF-sample-15s-clean.wav"

def create_voice(file_path: str, target_model: str, preferred_name: str) -> str:
    p = pathlib.Path(file_path)
    data_uri = f"data:audio/wav;base64,{base64.b64encode(p.read_bytes()).decode()}"
    resp = requests.post(
        "https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "qwen-voice-enrollment",
            "input": {
                "action": "create",
                "target_model": target_model,
                "preferred_name": preferred_name,
                "audio": {"data": data_uri},
            },
        },
    )
    resp.raise_for_status()
    return resp.json()["output"]["voice"]

voice_id = create_voice(VOICE_FILE_PATH, TARGET_MODEL, PREFERRED_NAME)
# voice_id = "i-arif-omni-<hash>"
```

Then for realtime conversation, wire through `OmniRealtimeConversation`:

```python
from dashscope.audio.qwen_omni import OmniRealtimeConversation, MultiModality, OmniRealtimeCallback

conv = OmniRealtimeConversation(
    model=TARGET_MODEL,
    callback=my_callback,
    url="wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime",
)
conv.connect()
conv.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice=voice_id,
)
```

**Pros**: no public file exposure; fastest realtime voice-to-voice in
federation. **Cons**: 15 s sample must be flawless — no margin for noise.

### Pathway B — CosyVoice High-Fidelity TTS (Public URL)

Use when arifOS only needs **Text-to-Speech** (no realtime).

```bash
# Step 1: host sample publicly (Caddy / Cloudflare Tunnel)
#   https://geox.arif-fazil.com/audio/i-ARIF-sample-15s.wav

# Step 2: enroll
curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voice-enrollment",
    "input": {
      "action": "create_voice",
      "target_model": "cosyvoice-v3-plus",
      "prefix": "i-arif-cosy",
      "url": "https://geox.arif-fazil.com/audio/i-ARIF-sample-15s.wav",
      "language_hints": ["ms", "en"]
    }
  }'
```

Then synthesize:

```bash
curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cosyvoice-v3-plus",
    "input": {
      "text": "Salam. Hang nak checker Solar pukul 3 tadi?",
      "voice": "i-arif-cosy-<hash>",
      "format": "wav",
      "sample_rate": 24000
    }
  }'
```

**Pros**: CosyVoice is among the most natural for dialect / multilingual.
**Cons**: requires public URL hosting; sample must be reachable from
DashScope servers (no localhost).

## Recording Checklist (15 s Window)

Per `AGI-audio-quantum-cognition` recording tips + Qwen-specific:

1. Close windows and doors.
2. Off fans, AC, fluorescent ballasts.
3. Small enclosed room (≤ 10 m²), acoustic foam / curtains / carpet.
4. Mic ~10 cm from mouth.
5. Script: complete sentences, ≥ 3 s continuous speech, semantic continuity.
6. Add appropriate emotional expression (warmth / seriousness). Monotone fails.
7. Avoid sensitive content (politics / porn / violence) — recording fails.

## Trade-off Matrix (i-ARIF specific)

| Pathway | Latency | Sample prep | Cost | Best for |
|---|---|---|---|---|
| Qwen-Omni Realtime | < 500 ms | 15 s clean Base64 | Per minute | Voice-to-voice conversational AI |
| CosyVoice HD | 2–4 s synthesis | 15 s clean URL | Per character | High-fidelity batch TTS |
| Qwen-Audio-TTS Flash | 1–2 s | 15 s clean URL | Cheapest | Background / bulk narration |
| MiniMax (companion skill) | Variable, HD | 2–3 min clean | Per character | Identity-rich narrative |

## F13 SOVEREIGN Gate

Voice enrollment is **identity creation**. Even though Qwen returns the
`voice` instantly with no training, the resulting handle is a sovereign
identity. Required:

- `human_approval_token` (stg_*) on the enrollment call.
- VAULT999 append with `category=identity`, `tier=sovereign`.
- Cross-reference the chosen `target_model` and document why.

Borrowing an existing voice for synthesis → F11 audit + receipt only,
no F13.

## F9 ANTI-HANTU

Synthetic voice handles that don't exist on DashScope → DENY at
L1_IDENTITY. The provider rejects, but agent must not paper over the
denial by retrying with a fabricated hash.

## F2 TRUTH Labels

- Voice creation response → `[OBS]` (provider-asserted).
- Sample selection → `[DER]` (derived from user's source audio).
- Target model choice → `[SPEC]` (specification, with rationale).

## When to Load This Skill

- Picking between MiniMax and Qwen for i-ARIF cloning.
- Configuring CosyVoice or Qwen-Omni realtime.
- Hosting source audio via Caddy / Cloudflare Tunnel for URL ingestion.
- Auditing target_model lock-in across federated voice handles.
- Debugging clone failures (silent synthesis, missing voice, drift).

## Integration Points

- **Companion (MiniMax)**: `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/SKILL.md`
- **Doctrine parent**: `/root/AAA/skills/AGI-audio-quantum-cognition/SKILL.md`
- **EMD pipeline**: `/root/AAA/skills/AAA-audio-emd-pipeline/SKILL.md`
- **Public audio hosting**: `/root/AAA/skills/forge-caddy-cloudflare/SKILL.md`
- **VAULT999 identity**: `/root/VAULT999/identity/`
- **DashScope docs**: https://dashscope-intl.aliyuncs.com

## Related Skills

- `AAA-voice-cloning-mimo-minimax` — Alternative provider (longer sample, more control)
- `AAA-audio-emd-pipeline` — Phase 3 ENCODE routing
- `AGI-audio-quantum-cognition` — Physics + floors
- `hermes-voice-config` — Hermes TTS config
- `tts-edge-fallback` — Free fallback

---

*Operational binding forged 2026-08-18. F2 evidence: DashScope International API documentation derived from provider docs. F13 gate: every enrollment call requires stg_* approval token before request.*