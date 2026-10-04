# Provider Audit — TTS/STT Benchmarks & Selection Guide

> Forged 2026-08-13 by Hermes Bridge. Live benchmarks against real infrastructure.

## TTS Output Providers Tested

### Edge TTS (`ms-MY-OsmanNeural`)
- **Status:** ✅ Default free. Unlimited. No cost.
- **Quality:** Good neural BM. Two voices: Osman (male, standard KL), Yasmin (female)
- **Latency:** <2 seconds generation time
- **Dialect support:** Standard BM only. No Penang/Perak/Sabah variants.
- **Tuning knobs:** 
  - `-10Hz pitch` = deeper/more mature tone (what Arif preferred over "makcik")
  - `-15% rate` = slower pacing, more deliberate delivery
  - Combined: authoritative, calm, not robotic announcer-like
- **Known issues:** Very deep pitches can sometimes produce artifacts on short texts. Test each parameter combo.
- **Best use case:** Default Malaysian TTS for all internal agent communication. Free → no budget concerns.
- **Voice note test:** `"Woi hang dengar ni sikit nak tengok siapa suara paling real"` — produced clear, natural BM speech in ~9.7s duration, 72KB OGG.

### MiniMax Speech 2.8 HD (via MCP :18100)
- **Status:** ✅ Working via FastMCP streamable-HTTP on port 18100
- **Quality:** Best BM currently available via cloud API
- **Cost:** Token plan charges per request ($68/mo Individual Pro seat via Qwen)
- **Features:** Voice clone capability available through same MCP
- **Limitations:** MCP server is unstable under sustained use — SIGKILL'd (likely OOM) after 2-3 tool calls. Must check port before calling, auto-restart if dead.
- **Best use case:** Fallback when Edge TTS doesn't meet quality requirements, or when voice cloning needed.

### Qwen Token Plan TTS (`qwen-audio-3.0-tts-plus`)
- **Status:** ✅ Configured in config.yaml. Requires BAILIAN_TOKEN_PLAN_API_KEY ($68/mo)
- **Quality:** Comparable to MiniMax for BM
- **Model ID:** `longxiaochun` voice
- **Base URL:** `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **Best use case:** Alternative fallback with separate billing from MiniMax.

### ElevenLabs (Configured but Not Active)
- **Status:** ⚠️ In config.yaml but API key needs setup
- **Quality:** Premium tier. Best voice cloning available
- **Cost:** Paid subscription required
- **Voice clone requirement:** ≥30 second reference audio sample from native speaker
- **Best use case:** Achieving "Penang presence" via cloning from real Penang speaker samples. Most realistic path to dialect-specific output.

### Gemini Native TTS (`gemini-2.5-flash-preview-tts`)
- **Status:** ✅ Working (verified 2026-08-15)
- **Quality:** Natural female voice ("Zephyr"). Good BM pronunciation, slightly formal register.
- **Cost:** Uses Gemini API key (same as image gen). No separate billing.
- **API:** `POST /v1beta/models/gemini-2.5-flash-preview-tts:generateContent` with `responseModalities: ["AUDIO"]` + `speechConfig.voiceConfig.prebuiltVoiceConfig.voiceName: "Zephyr"`
- **Output format:** RAW PCM s16le 24kHz mono — NOT mp3, NOT ogg, NOT wav. File appears as `data` to `file` command. Must convert before use.
- **Conversion recipe:**
  ```bash
  # Raw PCM → OGG (for Telegram voice bubbles)
  ffmpeg -y -f s16le -ar 24000 -ac 1 -i input.pcm -c:a libopus output.ogg
  # Raw PCM → MP3 (for general playback)
  ffmpeg -y -f s16le -ar 24000 -ac 1 -i input.pcm -c:a libmp3lame output.mp3
  ```
- **Pitfall:** The generated file saved as `.mp3` is NOT actually mp3 — it's raw PCM. `ffprobe` shows "Audio: mp3 (mp3float), 0 channels" which is garbage. Always check with `xxd | head -5` — valid PCM shows repeating 16-bit LE samples. Fix: re-encode from raw PCM, don't assume the extension matches the format.
- **Character limit:** Very long texts (>500 chars) produce 50+ second audio. Edge-tts is better for short quick responses.
- **Voice note playback:** PCM-converted ogg files play fine on Telegram. PCM-converted mp3 may not play on some mobile players if the PCM→mp3 conversion didn't set proper headers.
- **Best use case:** When edge-tts sounds too robotic/announcer-like. Gemini Zephyr has more natural prosody for longer emotional texts. Good for worship/care/voice persona delivery.

## OpenAI TTS
- **Status:** ❌ No API key configured
- **Quality:** Natural conversational style, improving BM coverage
- **Best use case:** Future option when key becomes available. Better than Edge for natural flow in dialogue-heavy scenarios.

## STT Input Providers

### Whisper (OpenAI) — Primary
- **Status:** ✅ Wired in config.yaml as default STT provider, model `whisper-1`
- **Cost:** Per-minute transcription costs (varies by usage)
- **Accuracy:** Production-grade for English and decent BM
- **Reliability:** Stable, well-tested in production pipeline

### Groq Whisper-v3-turbo — Secondary
- **Status:** 🟡 Source code wired in `/root/hermes-agent-dev/tools/transcription_tools.py` but NOT in config.yaml
- **Feature:** Extremely fast inference (<100ms for short clips)
- **Gap:** Needs one sed command to add STT entry to `~/.hermes/config.yaml`
- **Best use case:** Low-latency STT when response time matters most.

### xAI STT — Secondary  
- **Status:** 🟡 Source code wired but missing from config.yaml
- **Gap:** Same as Groq — needs config.yaml entry to activate
- **Best use case:** Redundant fast STT backup alongside Groq.

## Mesolitica HF Models (Local TTS) — Download Ready
- **Models:** Malaysian-TTS-4B-v0.1 (4B params), Malaysian-F5-TTS-v3 (full parameter fine-tuning)
- **Source:** https://huggingface.co/collections/mesolitica/malaysian-text-to-speech
- **License:** Open-source download ready
- **Quality:** Malaysian-trained dataset. Best native BM authenticity available
- **Limitation:** No Penang dialect variant yet. All models trained on standard Malaysian corpus
- **Installation:** `hf download --local-dir './ckpt' 'Mesolitica/Malaysian-TTS-4B-v0.1'`
- **Requirements:** GPU recommended (16GB+ VRAM comfortable). Can run CPU but expect 30-60 min per song.

## librosa vs parselmouth Decision Matrix

| Feature | librosa (✅) | parselmouth/Praat (❌) |
|---|---|---|
| F0 estimation (pitch) | ✅ pyin works | ✅ praat pitch |
| Jitter/shimmer analysis | ❌ Not directly available | ✅ Native |
| HNR estimation | Via spectral features approximation | ✅ Native Praat metrics |
| onset_detect() | ❌ SEGFAULTS on Python 3.13 | N/A |
| peak_pick() | ❌ SEGFAULTS on Python 3.13 | N/A |
| RMS energy | ✅ stable | ✅ stable |
| Zero-crossing rate | ✅ stable | ✅ stable |
| Spectral centroid | ✅ stable | ✅ stable |
| chroma_cqt | ❌ SEGFAULTS | N/A |
| beat_track | ❌ SEGFAULTS | N/A |

**Conclusion:** Use librosa only for stable paths (pyin, rms, zcr, spectral_centroid). Avoid onset_detect(), peak_pick(), chroma_cqt, beat_track entirely on Python 3.13 + numpy 2.4.6. These crash via numba extension modules with segfault (core dumped).

## Recommendation Stack

| Scenario | Best Provider | Reason |
|---|---|---|
| Default AGI output | Edge TTS OsmanNeural (-10Hz pitch) | Free, reliable, good enough |
| Voice clone needed | ElevenLabs | Realistic penang presence achievable |
| Premium fallback | MiniMax 2.8 HD via MCP | Quality > Edge for complex BM text |
| Local/offline mode | Mesolitica HF models | Malaysian-native training data |
| Ultra-fast STT | Groq whisper-v3-turbo (once configured) | Sub-100ms latency crucial for real-time |
| Balanced STT | OpenAI whisper-1 | Production-tested reliability |
