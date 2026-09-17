# Qwen Voice Cloning for Malay TTS — discovered 2026-08-18

## Discovery

Qwen-Audio-TTS voice cloning is **FREE** on the Singapore Token Plan. This is the first zero-cost path to a custom Malay male voice without GPU. Upload a 10-20s sample of a deep Malay male voice → clone → synthesize BM text with that voice.

## Why this matters for "abang sado"

Indonesian voices (MiniMax) handle BM text but have subtle accent differences. Qwen voice cloning preserves the exact timbre, accent, and emotional quality of the reference speaker. A Malay male reference = native BM pronunciation, no Indonesian accent bleed.

## API endpoint (Singapore region)

```
POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization
Authorization: Bearer $QWEN_TEAM_OWNER_API_KEY
```

Replace `{WorkspaceId}` with actual workspace ID. Use Singapore-region API key.

## Step 1 — Create voice

```bash
curl -X POST "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization" \
  -H "Authorization: Bearer $QWEN_TEAM_OWNER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voice-enrollment",
    "input": {
      "action": "create_voice",
      "target_model": "qwen-audio-3.0-tts-flash",
      "prefix": "abangsado",
      "url": "https://your-audio-url.wav"
    }
  }'
```

Returns `voice_id` for use in synthesis.

## Step 2 — Synthesize with cloned voice

```python
import dashscope, os
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat

dashscope.api_key = os.environ["QWEN_TEAM_OWNER_API_KEY"]
dashscope.base_websocket_api_url = "wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference"

# voice_cloning and synthesis MUST use the same model
model = "qwen-audio-3.0-tts-flash"
voice = "YOUR_VOICE_ID"  # from step 1

synthesizer = SpeechSynthesizer(model=model, voice=voice, format=AudioFormat.MP3_22050HZ_MONO_256KBPS)
audio = synthesizer.call("Sini. Dekat sikit. Kau pandang aku.")
with open("out.mp3", "wb") as f:
    f.write(audio)
```

## Billing

- Voice creation: **FREE** (no charge for cloning itself)
- Speech synthesis with cloned voice: normal Token Plan quota
- Up to 1,000 custom voices per account
- Auto-deleted after 1 year of no synthesis usage
- MiniMax cloning (Beijing only): CNY 9.9 unlock fee per voice — NOT free

## Audio requirements

| Item | Requirement |
|---|---|
| Formats | WAV (16-bit), MP3, M4A |
| Duration | 10-20s recommended, 60s max |
| File size | ≤ 10 MB |
| Sample rate | ≥ 16 kHz |
| Channels | Mono (stereo → first channel only) |
| Content | ≥ 5s continuous clear speech, no background noise/music, pauses ≤ 2s |
| Languages | Chinese (20+ dialects), English, Japanese, Korean, Russian, French, German, Portuguese, Thai, Indonesian, Vietnamese, Spanish, Italian, **Malaysian**, Filipino, Arabic |

## Critical pitfall: target_model must match

The `target_model` specified during voice creation MUST exactly match the model used for speech synthesis. Create with `qwen-audio-3.0-tts-flash` → synthesize with `qwen-audio-3.0-tts-flash`. Mismatch = synthesis failure.

## Pitfall: audio must be URL-accessible

The `url` parameter requires an accessible HTTP(S) URL, NOT a local file path. Options:
- Temporary HTTP server on VPS: `python3 -m http.server 8888 --directory /path/to/audio`
- Upload to object storage (S3, OSS, etc.)
- Use any public file hosting

## Seat quota ladder

| Key | Env var | Status (2026-08-18) |
|---|---|---|
| ArifOS seat | `QWEN_ARIFOS_API_KEY` / `BAILIAN_TOKEN_PLAN_API_KEY` | EXHAUSTED (HTTP 44) |
| Team Owner seat | `QWEN_TEAM_OWNER_API_KEY` | WORKING |

Always try QWEN_TEAM_OWNER_API_KEY first when QWEN_ARIFOS_API_KEY returns 44.

## Qwen system voices (for reference, NOT Malay)

| Voice | Param | Gender | Age | Characteristic | Language |
|---|---|---|---|---|---|
| Long An Ling Xin | longanlingxin | F | 25 | Warm empathetic | Chinese, English |
| Long An Lu Feng | longanlufeng | M | 25 | Bright cheerful | Chinese, English |

Base voices: 597 total, ALL Chinese or English. ZERO Malay/Indonesian.

## CosyVoice v3.5-plus (alternative cloning model)

Supports Indonesian, Vietnamese, Thai — but NOT Malay explicitly. Voice cloning is also free. Less relevant for BM than Qwen-Audio-TTS which explicitly lists Malaysian.

## Related

- SKILL.md §5 — Qwen Voice Cloning section
- SKILL.md §4 — Indonesian Voice Breakthrough (MiniMax alternative)
- `references/tts-lane-updates-2026-08-18.md` — seat quota flavours
