# Complete TTS Landscape — All Token Plans (2026-08-18)

## Summary

Deep research across all available TTS providers on Token Plans owned by Arif. Malay/BM voice is the target language.

## Provider comparison

| Provider | Model | Malay voices | Voice cloning | Cost | Status |
|----------|-------|-------------|---------------|------|--------|
| **MiniMax** | speech-2.8-hd | ✅ 9 Indonesian voices (proven BM) | ✅ FREE (TTV) | Token Plan quota | **PRIMARY** |
| **Qwen** | qwen-audio-3.0-tts-plus | ❌ 597 base = CN/EN only | ✅ FREE (Singapore) | Token Plan quota | Clone only |
| **Qwen** | cosyvoice-v3.5-plus | ⚠️ Indonesian (not Malay) | ✅ FREE | Token Plan quota | Secondary |
| **Qwen** | qwen3-tts-vc | ❌ No Malay | CNY0.01/voice | Beijing region | Not useful |
| **edge-tts** | ms-MY-OsmanNeural | ✅ Native Malay | ❌ | FREE unlimited | Fallback |
| **MuleRouter** | — | — | — | — | DEAD (402) |
| **Runpod** | F5-TTS | ✅ Any language | ✅ Voice clone | GPU top-up | Blocked |

## MiniMax speech-2.8-hd detail

- 334 voices across16 languages
- Indonesian voices handle BM text naturally (no accent bleed)
- Voice cloning: TTV (Text-To-Voice) works on Token Plan, FREE
- Voice ID format: `ttv-voice-{YYYYMMDDHHmmss}-{HASH}`
- Quota: ~52% daily, ~83% weekly (general model bucket)
- Output: 32kHz, ~200KB per13s clip

### BM voice ranking (tested)

1. `Indonesian_BossyLeader` — dominant, commanding, speed0.82 → best for authority/sado
2. `Indonesian_CaringMan` — warm, empathetic, speed0.90 → best for narration
3. `English_ManWithDeepVoice` — deep English, BM text, speed0.85 → accent but heavy
4. `English_MatureBoss` — authoritative, BM text, speed0.85
5. `English_ImposingManner` — commanding, BM text, speed0.85

### Cloned voice (verified 2026-08-18)

- Voice ID: `ttv-voice-2026081809381426-78AFZAgJ`
- Whisper STT transcription:100% accurate on BM text
- Quality:32kHz, stable generation
- Usage: `mmx speech synthesize --voice "ttv-voice-..." --text "..." --output /tmp/out.mp3`
- Requires: `--base-url https://api.minimax.io`

## Qwen TTS detail

### qwen-audio-3.0-tts-plus (Singapore)

- System voices: `longanlufeng` (male), `longanlingxin` (female) — Chinese+English only
- Base voices:597, ALL Chinese or English, ZERO Malay
- Voice list: `https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260723/ulextc/qwen-audio-3.0-tts-plus-base-voices-en.xlsx`
- Voice cloning: FREE, supports Malay input,10-20s reference audio
- Breakthrough path: upload Malay male voice sample → clone → synthesize BM text

### Seat quota

- `QWEN_ARIFOS_API_KEY` — weekly quota exhausted (429, resets08-21)
- `QWEN_TEAM_OWNER_API_KEY` — independent quota, works for TTS and image gen

## edge-tts

- `pip install edge-tts --break-system-packages`
- `ms-MY-OsmanNeural` — native Malay male, engine-capped (one style)
- `ms-MY-YasminNeural` — native Malay female
- Unlimited, zero cost, always available

## Verdict

**Production BM TTS:** MiniMax speech-2.8-hd with Indonesian voices or cloned voice.
**Custom voice creation:** Qwen voice cloning (free, upload Malay sample).
**Zero-cost fallback:** edge-tts ms-MY-OsmanNeural.
