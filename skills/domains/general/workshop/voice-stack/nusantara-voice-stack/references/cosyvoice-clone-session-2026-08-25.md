# CosyVoice Clone Session — 2026-08-25

## Context
Arif sent a voice note (24.78s, OGG/Opus, 48kHz mono) for voice cloning. Goal: create a canon i-ARIF voice from Arif's actual voice.

## What Worked

### Qwen CosyVoice Voice Enrollment (SUCCESS)
- Model: `voice-enrollment` with `target_model: cosyvoice-v3-plus`
- Prefix: `iarif2026` (alphanumeric only — hyphens rejected)
- Language hints: `["ms"]` (must be exactly 1 — array of 2+ rejected)
- Source: MP3 hosted at `https://aaa.arif-fazil.com/audio/i-arif-clone-source.mp3`
- Result voice_id: `cosyvoice-v3-plus-iarif2026-fc37c2ff31f04ebaa17d5a63a0fdd1b1`
- Enrollment was instant and FREE

### MiMo Token Plan TTS (PROVEN FALLBACK)
- Endpoint: `https://token-plan-sgp.xiaomimimo.com/v1/chat/completions`
- Model: `mimo-v2.5-tts` with `modalities: ["audio"]`
- Voice: `冰糖` (Chinese female, handles BM text)
- Protocol: REST (chat/completions), NOT WebSocket — reliable, no truncation
- Audio returned as base64 in `choices[0].message.audio.data`
- Full sentence synthesis works without truncation

## What Failed

### MiniMax voice_clone — Quota Exhausted
- Error: `status_code: 1008, status_msg: insufficient balance`
- The `general` model pool (shared with image + speech) was depleted
- Voice clone is FREE on Token Plan but requires available quota
- **Lesson**: Check MiniMax quota before attempting clone. `mmx quota show --base-url https://api.minimax.io`

### CosyVoice WebSocket Synthesis — Truncation
- Short text (3-6 words): works, produces complete audio
- Long text (>10 words): **truncates mid-sentence**, only partial audio delivered
- Root cause: WebSocket connection timeout or frame limit
- The `SpeechSynthesizer` SDK requires `/usr/bin/python3` (system), NOT `/root/venv/bin/python3`
- `base_websocket_api_url` must be set at module level, not constructor

### CosyVoice REST Synthesis — Not Available
- `dashscope-intl.aliyuncs.com/compatible-mode/v1/audio/speech` → HTTP 404
- `token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/audio/speech` → HTTP 404
- CosyVoice is WebSocket-only for synthesis

## Audio Hosting Pattern
For Qwen voice enrollment (requires public URL):
```bash
# Copy to Caddy-served web root
cp /tmp/audio.mp3 /var/www/html/aaa/audio/filename.mp3
# Verify accessibility
curl -s -o /dev/null -w "%{http_code}" https://aaa.arif-fazil.com/audio/filename.mp3
# Clean up after enrollment
rm /var/www/html/aaa/audio/filename.mp3
```

## STT Verification Results
- Original Arif recording: BM natural, about fruits/housewife shopping
- CosyVoice output: "Ditempa bukan daivari" (partial, truncation)
- MiMo output: "Assalamualaikum warahmatullahi wabarakatuh" (MiMo added its own greeting)

## Pending
- Arif needs to listen and judge which voice sounds "right"
- If CosyVoice wins: need to solve truncation (chunked synthesis)
- If MiMo wins: wire into pipeline as primary voice
- MiniMax quota needs reset (Sunday) for re-clone attempt
