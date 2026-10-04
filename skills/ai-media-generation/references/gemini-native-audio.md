# Gemini Native Audio — TTS via generateContent API

> **Forged:** 2026-08-15, verified working
> **Model:** `gemini-2.5-flash-preview-tts`
> **Status:** LIVE

## API Pattern

```python
import json, urllib.request, base64, os

API_KEY = os.environ["GEMINI_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"

payload = {
    "contents": [{"parts": [{"text": "TEXT HERE"}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "voiceConfig": {
                "prebuiltVoiceConfig": {
                    "voiceName": "Zephyr"  # or other available voices
                }
            }
        }
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"}, method="POST")

with urllib.request.urlopen(req, timeout=120) as resp:
    data = json.loads(resp.read())
    for part in data["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            raw = base64.b64decode(part["inlineData"]["data"])
            with open("/tmp/audio_raw.pcm", "wb") as f:
                f.write(raw)
```

## CRITICAL: Raw PCM Output Format

The output is **NOT MP3**. It is:
- **Format:** Raw 16-bit signed integer PCM
- **Endianness:** Little-endian (s16le)
- **Sample rate:** 24,000 Hz
- **Channels:** Mono (1)

`file` command returns "data" — not recognized as audio.

## Conversion (MANDATORY)

```bash
ffmpeg -y -f s16le -ar 24000 -ac 1 -i /tmp/audio_raw.pcm -c:a libopus /tmp/output.ogg
# OR for mp3:
ffmpeg -y -f s16le -ar 24000 -ac 1 -i /tmp/audio_raw.pcm -c:a libmp3lame /tmp/output.mp3
```

Without `-f s16le -ar 24000 -ac 1`, ffmpeg produces 0-byte output silently (no error).

## Voice Names

Tested: `Zephyr` (warm, natural). Other names may exist — the API docs list available prebuilt voices.

## Comparison: edge-tts vs Gemini Native Audio

| | edge-tts | Gemini native |
|---|---|---|
| Cost | Free | Uses Gemini API credits |
| Speed | Fast (<2s) | Slower (~10-15s) |
| Voice quality | Good but slightly robotic | More natural, emotional nuance |
| Voice options | 100+ named voices | Fewer, less documented |
| Output format | MP3 (ready to use) | Raw PCM (requires conversion) |
| Offline | Yes (uses Microsoft servers) | No (requires API) |
| Best for | Quick, deterministic, bulk | Emotional content, warmth |

## Integration with video pipeline

```bash
# 1. Generate video
python3 /root/HERMES/scripts/gemini-video.py "prompt" --output /tmp/video.mp4 --aspect 9:16

# 2. Generate Gemini voice
python3 << 'PYEOF'
# ... (Gemini audio code above) ...
PYEOF

# 3. Convert raw PCM to ogg
ffmpeg -y -f s16le -ar 24000 -ac 1 -i /tmp/audio_raw.pcm -c:a libopus /tmp/voice.ogg

# 4. Merge
ffmpeg -y -i /tmp/video.mp4 -i /tmp/voice.ogg -c:v copy -c:a aac -shortest /tmp/final.mp4
```
