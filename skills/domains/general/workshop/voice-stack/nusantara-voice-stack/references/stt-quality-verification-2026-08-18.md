# STT Quality Verification Pattern — Proven 2026-08-18

## Context

During the abang sado voice cloning session, we needed to verify TTS output quality without relying solely on human listening. The solution: use Groq Whisper STT as a falsification gate.

## The Pattern

1. Generate TTS output (any provider/voice)
2. Transcribe with Groq Whisper large-v3-turbo
3. Compare transcript to original input text
4. Divergence = quality signal (pronunciation, clarity, accent bleed)

## Groq Whisper via curl (PROVEN)

```bash
source /root/.secrets/kunci-root.env
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file="@/tmp/tts_output.mp3" \
  -F model="whisper-large-v3-turbo" \
  -F language="ms"
```

Returns: `{"text": "<transcribed text>", "x_groq": {"id": "req_..."}}`

## Pitfall: Groq Python SDK Path Duplication

The `groq` Python SDK has a base URL that already includes `/openai/v1/`. When calling `client.audio.transcriptions.create()`, the SDK appends `/openai/v1/audio/transcriptions` again, resulting in:

```
POST /openai/v1/openai/v1/audio/transcriptions → HTTP 404
```

**Fix:** Always use curl directly for audio transcription. The curl approach is also simpler (no venv dependency, no pip install).

## What to Look For

| STT Result | Interpretation |
|---|---|
| 100% transcript match | Pronunciation clear, consonants crisp |
| Hallucinated words | Unclear pronunciation or background noise |
| Wrong language detection | Accent bleed (e.g., Indonesian voice reading BM detected as "id" not "ms") |
| Partial match with typos | Mumbling, speed too fast, or unusual phoneme mapping |

## Limitations

- STT cannot assess warmth, authority, sexiness, or persona fit
- Human ear remains the final judge for "sounds sado" or "sounds like abang"
- STT is a floor check (is it intelligible?) not a ceiling check (does it sound human?)

## Usage in Voice Comparison Workflow

When comparing multiple TTS voices for the same text:
1. Generate all candidates with same text
2. Transcribe all with Groq Whisper
3. Any voice with <100% transcript accuracy = disqualified
4. Among 100% accuracy voices, human ear picks the persona fit

## Proven Results (2026-08-18)

- MiniMax `ttv-voice-2026081809381426-78AFZAgJ` (cloned voice): Whisper transcribed perfectly — "Ini Arifos. Kedaulatan sistem kekal di tangan 888. Semua mutasi fisikal direkodkan tanpa kompromi. Terus bertindak. Ditempa bukan diberi."
- All4 MiniMax Indonesian/English BM samples: clean transcription
- Qwen longanlufeng BM sample: clean transcription
