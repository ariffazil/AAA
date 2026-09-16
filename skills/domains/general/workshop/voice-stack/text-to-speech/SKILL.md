---
name: token-plan-tts
description: "Generate speech audio via QwenCloud Token Plan TTS. Activates when user asks to speak text, generate audio, or convert text to voice."
---

# Token Plan Text-to-Speech

Call the Token Plan speech synthesis API via DashScope WebSocket SDK.

## Supported model

| Model | Description |
|-------|-------------|
| `qwen-audio-3.0-tts-plus` | High-quality TTS, multiple languages, voice cloning |

## Prerequisites

```bash
pip install dashscope
```

## Usage

```python
import os
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
from datetime import datetime

dashscope.api_key = os.environ.get("QWEN_API_KEY")
dashscope.base_websocket_api_url = "wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference"

synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-plus",
  voice="longxiaochun",  # default voice
  format=AudioFormat.MP3_22050HZ_MONO_256KBPS,
)

audio = synthesizer.call("<text>")
filename = f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
with open(filename, "wb") as f:
  f.write(audio)
print(f"Audio saved: {filename}")
```

## Available voices (qwen-audio-3.0-tts-plus, verified 2026-08-18)

Voice params are LOWERCASE, no underscores between syllables. Old CosyVoice names (longxiaochun, longshu, longlaotie) and Qwen3-TTS names (Cherry, Ethan) FAIL with `[cosyvoice:]Engine error [411]` on this model.

Working: `longanlufeng` (male, bright cheerful, flagship), `longanlingxin` (female, warm empathetic, flagship). Full catalog: https://docs.qwencloud.com/api-reference/speech-synthesis/qwen-audio-tts/voice-list — v3.6-suffixed voices (longchuanshu_v3.6, loongjohn) also 411 on plus (flash-only).

## Seat quota notes (2026-08-18)

BAILIAN_TOKEN_PLAN_API_KEY and QWEN_ARIFOS_API_KEY (same key) hit weekly quota 429 `Throttling.AllocationQuota` (resets 08-21). QWEN_TEAM_OWNER_API_KEY (Seat 3) has independent quota and works for both image gen and TTS.

## Notes

- Billed in Credits from Token Plan quota
- Uses WebSocket protocol (not HTTP REST)
- Supports voice cloning from audio samples (see below)

## Voice Cloning (FREE, 2026-08-18)

Both MiniMax and Qwen offer FREE voice cloning on existing Token Plans. This is the breakthrough path for custom Malay male voices.

### MiniMax TTV (recommended — simplest workflow)

Voice created on MiniMax platform → voice ID → `mmx speech synthesize`:

```bash
mmx speech synthesize --base-url https://api.minimax.io \
  --model speech-2.8-hd \
  --voice "ttv-voice-YYYYMMDDHHMMSS-*" \
  --speed 0.85 \
  --text "Sini. Dekat sikit." \
  --output /tmp/clone_output.mp3
```

Voice ID persists server-side. Creation via MiniMax UI (API not reverse-engineered). Quota: shared with `general` model pool.

### Qwen Voice Cloning (Singapore)

Clone from 10-20s audio sample. Supports Malaysian input language.

```python
import dashscope, os
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
dashscope.api_key = os.environ["QWEN_TEAM_OWNER_API_KEY"]
dashscope.base_websocket_api_url = "wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference"
s = SpeechSynthesizer(model="qwen-audio-3.0-tts-flash", voice="YOUR_VOICE_ID", format=AudioFormat.MP3_22050HZ_MONO_256KBPS)
audio = s.call("Sini. Dekat sikit.")
with open("out.mp3", "wb") as f: f.write(audio)
```

**Pitfall:** reference audio must be accessible via URL (not file://). Host on temporary HTTP server first.
**Seat quota:** QWEN_ARIFOS_API_KEY exhausted (449), QWEN_TEAM_OWNER_API_KEY works. Always ladder seats.
**Zero Malay base voices:** Qwen has 597 base voices, all Chinese/English. Voice cloning is the ONLY path for Malay on Qwen.
