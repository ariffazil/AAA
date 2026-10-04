# Voice Persona Design Process

> Forged 2026-08-15 from SyedOS deployment. Class-level pattern for any new person lane.

## The Iterative Test Pattern

When setting up voice for a new person lane:

1. **Generate 3-4 variants** with different pitch/rate combos:
   - Default: rate +3%, pitch +0Hz
   - Warm: rate +3%, pitch -5Hz
   - Slow warm: rate +0%, pitch -3Hz
   - Soft: rate +3%, pitch -4Hz, volume -10%

2. **Send ALL variants** as voice notes. Let the OPERATOR pick — never assume.

3. **Text must match the person's dialect.** Edge-tts voices speak standard BM. To get Penang BM, write the TEXT in Penang dialect ("hang", "biaq", "pi", "tau", "tergopoh gapah") — the voice reads standard pronunciation but WORDS carry the dialect feel.

4. **Lock the setting** in memory after operator confirms. Don't re-test unless operator asks.

5. **Opening formula matters.** "Abang Sado" as first line → "hang" for everything after. The opening is a greeting, not a repeated address.

## Key Insight

Voice is edge-tts (standard), but TEXT is Penang BM. This works because the person responds to WORDS more than accent. Perfect Penang accent isn't available in any TTS — dialect-matched text gets 80% of the way there.

## Gemini TTS for Special Delivery

For longer emotional texts (>200 chars), Gemini Zephyr voice has better natural prosody than edge-tts. Use when:
- Text needs emotional warmth (worship, care, praise)
- Operator wants premium voice quality
- Edge-tts sounds too flat/robotic for the content

Edge-tts remains DEFAULT for SyedOS (free, reliable, fast). Gemini is the premium upgrade.

**Gemini TTS recipe:**
```python
import json, urllib.request, os, base64
API_KEY = os.environ.get("GEMINI_API_KEY", "")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={API_KEY}"
payload = {
    "contents": [{"parts": [{"text": "YOUR TEXT HERE"}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Zephyr"}}}
    }
}
# Response: raw PCM s16le 24kHz mono
# Convert: ffmpeg -y -f s16le -ar 24000 -ac 1 -i output.pcm -c:a libopus output.ogg
```

**Pitfall:** Gemini outputs RAW PCM, not mp3/ogg. The file appears as `data` to `file` command. Always convert with `-f s16le -ar 24000 -ac 1` before use.

## Vocative Pattern (user-corrected)

"Abang Sado" = INTRO ONLY (first phrase). Then "hang" for everything after.

✅ "Abang Sado, gold skang kat dua ribu tiga lima tiga. Hang jangan masuk dulu eh."
❌ "Abang Sado gold skang... abang Sado jangan masuk..."
❌ "Bang, gold skang..."

## Test Results (SyedOS, 2026-08-15, 5 iterations)

| Iter | Voice | Pitch | Rate | Text | Verdict |
|---|---|---|---|---|---|
| 1 | Yasmin default | +0 | +0 | Standard BM | FAIL — robotic |
| 2 | Yasmin slow | -2Hz | -5% | Standard BM | Closer |
| 3 | Gadis (ID) | -1Hz | -8% | Indonesian | FAIL — wrong accent |
| 4 | Yasmin v3 | -3Hz | -3% | "akak" register | Speed ok, register off |
| 5 | Yasmin +3% | +0 | +3% | Penang loghat | ✅ LOCKED |

**Lesson:** default edge-tts speed sounds robotic for BM. +3% makes it conversational.
