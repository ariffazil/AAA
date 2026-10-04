---
name: multimodal-audio-pipeline
description: "Use for multi-provider audio generation/testing/selection."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [audio, tts, stt, music, gemini, minimax, edge, qwen, mulerouter]
metadata:
  hermes:
    tags: [audio, multimodal, provider-discovery, testing]
---

# Multimodal Audio Pipeline — Federation-Grade

## When to Use

Use when generating/transcribing/analyzing audio **across all available providers** and picking the best one. Not just "use X" — discover what works NOW, test live, deliver.

## When to Load

- User asks for speech/audio/song with specific style (dialect, gender, mood).
- Audio generation seems silent/broken — diagnose first.
- Any audio task where quality matters more than speed ("buat suara yang sedap").
- Building or debugging voice pipelines (voice-state, paralinguistic analysis).

## Providers Inventory

| Provider | How | Live status rule |
|---|---|---|
| **edge-tts** (default) | `edge-tts --voice ms-MY-OsmanNeural --text ...` | Free, stable. Only 2 Malay voices: Osman (male), Yasmin (female, sounds like "makcik"). KL-standard, no dialect. |
| **Gemini TTS** | `gemini-2.5-flash-preview-tts`, `responseModalities:["AUDIO"]`, voice via `prebuiltVoiceConfig` (Aoede, Leda, Charon, Achernar...). | Best for STYLE CONTROL — accepts natural-language instruction for tone/dialect/persona. Output = raw L16 PCM → FFmpeg to MP3. |
| **MiniMax (MuleRouter)** | `mulerouter-tts.py` / `mulerouter-music.py` | Best Malay quality. Check balance FIRST — negative balance = 402. Music via `music-2.5`. |
| **Qwen TTS** | DashScope WebSocket SDK `SpeechSynthesizer`, model `qwen-audio-3.0-tts-plus` | Token-plan key may be quota-exhausted; DashScope websocket may be firewalled. Confirm before use. |
| **MiMo** | `MIMO_PLATFORM_BASE_URL` + key, `/audio/speech` | Endpoint may 404 (openresty) if base URL wrong. Verify first. |
| **OpenAI gpt-4o-mini-tts** | `/v1/audio/speech` | Vault key may be a placeholder string — check before use. |
| **ElevenLabs** | — | No key in vault. Most natural + voice cloning. Cloning = F13 HOLD. |
| **Mesolitica** | HuggingFace Malaysian-TTS | Best MY identity. Needs GPU (RunPod), not local. |

## Testing Protocol — NEVER GUESS, PROBE LIVE

1. **edge smoke** (<5s): generate to `/tmp/test.mp3`, check file size.
2. **Gemini probe**: POST `generateContent?key=...` with audio modality, then FFmpeg-convert the PCM.
3. **Quota/balance check** before paid providers. A failed probe costs nothing; a bad assumption costs the session.

Minimal Gemini TTS script (proven working):

```python
payload = {
    "contents": [{"parts": [{"text": instruction + "\n\n" + text}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
    }
}
r = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=" + API_KEY, json=payload, timeout=120)
# audio = base64.b64decode(r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
# raw L16 PCM → ffmpeg -f s16le -ar 24000 -ac 1 -i in.raw out.mp3
```

## Style Instruction Pattern (Gemini TTS)

The key to custom tones is the natural-language instruction BEFORE the spoken text:

```
Deep masculine voice, confident cocky alpha male. Tone like a dominant
bodybuilder speaking with an arrogant smirk. Slow, deliberate, commanding.
Not shouting — quiet confidence.

<text to speak>
```

Valid voice names (from API error list): achernar, achird, algenib, algieba, alnilam, aoede, autonoe, callirrhoe, charon, despina, enceladus, erinome... Always write the instruction explicitly — never rely on default voice personality.

## Pitfalls

- **No native Penang-dialect TTS exists.** All dialect effects are Gemini instruction-driven approximations. Authentic Penang presence needs ElevenLabs voice cloning with real samples (F13 consent). TTS can copy phonetics, not social rhythm (tempo, "ka?", pause placement, code-switch).
- **Yasmin (edge) reads as an older woman** — user rejected it as "macam makcik". For casual/young female, use Gemini with youth instruction instead.
- **Gemini audio output is raw L16 PCM** (mime `audio/L16;codec=pcm;rate=24000`) — always FFmpeg-convert before delivering. Parse rate from the mimeType string.
- **Vision-analyzing video frames**: batch ≤3 frames per Gemini call with 2s delay, or hit 401/rate limits. vision_analyze tool can 504 under load — fall back to direct Gemini API with base64 inline_data.
- **Audio/DSP in gateway context**: wrap librosa extraction in `asyncio.to_thread()` to avoid blocking the event loop.
- **Video + generated audio**: if audio is longer than video, slow the video (`setpts=PTS*ratio`) rather than cutting the voice — preserves the full line.

## Related

- TELINGA doctrine: voice-as-state extraction (voice_state.py) lives in hermes-agent-dev; see references for the architecture summary.
- **Winning voice recipes + video-mux:** `references/voice-gen-field-notes.md` — the Charon cocky voice (user-approved), edge/gemini candidate table, the proven Charon instruction string, and the slow-video-to-fit-audio FFmpeg technique.
