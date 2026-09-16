# Voice Clone Provider Update — 2026-08-25/26

## MiniMax: Quota Exhausted

- Error: `1008-insufficient balance` (MCP tool `mcp__minimax_media__voice_clone`)
- Audio features bill on separate audio-subscription balance, NOT general Token Plan quota
- Base URL confirmed: `https://api.minimax.io/v1` (NOT `api.mxbai.chat` — DNS fail)
- Raw `/v1/voice_clone` API always returns `invalid params` (2013) — MCP tool is the working path
- **Prevention:** Check balance before heavy TTS: `curl -s https://api.minimax.io/v1/user/balance -H "Authorization: Bearer $MINIMAX_API_KEY"`

## Qwen CosyVoice: Enrollment Succeeds, Synthesis Fails

**Enrollment (voice-enrollment model, URL path):**
- Model: `voice-enrollment` (NOT `qwen-voice-enrollment`)
- Input fields: `action: create_voice`, `target_model`, `prefix`, `url`, `language_hints`
- `language_hints` MUST be length 1 (e.g. `[\"ms\"]`) — length 2 returns `InvalidLanguageHints`
- `prefix` must be alphanumeric (no hyphens) — `i-arif-cosy` fails, `iarifcosy` works
- Public URL required: file served from Caddy vhost root (`/var/www/html/geox/`)
- Result: voice_id `cosyvoice-v3-plus-iarifcanon-9b8a9453168b4ffb81f73acee587c31e` created ✅

**Synthesis (SpeechSynthesizer endpoint):**
- `SpeechSynthesizer` HTTP returns `\"current user api does not support http call\"` for DashScope International
- All model variants fail: `cosyvoice-v3-plus`, `qwen-audio-3.0-tts-flash`, `qwen-audio-3.0-tts-plus`
- Error: `Engine error [411]: TTS speak operation failed` — likely Malay content not supported despite docs
- Token Plan endpoint: `Throttling.AllocationQuota` (resets 28 Aug)

**Verdict:** Qwen CosyVoice enrollment is a valid registration path but synthesis is non-functional for Malay content as of 2026-08-25.

## F5-TTS: Proven Canon Voice Path (CPU)

- Install: `pip install f5-tts` in `/root/venv`
- Zero-shot clone from 10s reference audio
- CPU-only (no GPU), ~4 min for 8s output
- **F0 preservation: source 105 Hz → clone 93.8 Hz (-11%, male range preserved)**
- Model auto-downloads from HuggingFace (~2GB first run)

**Working Python API:**
```python
from f5_tts.api import F5TTS
tts = F5TTS(device="cpu")
wav, sr, _ = tts.infer(
    ref_file="/path/to/reference.wav",  # 10-24s clean speech
    ref_text="exact transcription of reference",  # MUST match audio
    gen_text="text to synthesize",
    speed=1.0,
)
```

**Pipeline script:** `/root/AAA/engines/f5tts_pipeline.sh`
**Reference audio:** `/root/AAA/engines/f5tts/reference-10s.wav`

**Pitfalls:**
- `ref_text` must exactly match the reference audio transcription — mismatch causes hallucination
- CPU inference: 4+ minutes for short utterance — use background process
- First run downloads model (~2GB) — expect longer initial latency
- HuggingFace cache: `/root/.cache/huggingface/hub/models--SWivid--F5-TTS/` (~2GB)

## Caddy File Hosting Fix

- Files for Qwen URL enrollment must be in Caddy vhost root: `/var/www/html/geox/`
- Files in `/var/www/html/_shared/` are NOT served (404 HTML page returned)
- Verify: `curl -sLk https://geox.arif-fazil.com/<file> | file -` → should show audio, not HTML

## Provider Status Matrix (2026-08-26)

| Provider | Clone API | Synthesis | BM Support | Status |
|---|---|---|---|---|
| MiniMax | ✅ MCP tool | ✅ t2a_v2 | ✅ verified | ❌ quota exhausted |
| Qwen CosyVoice | ✅ voice-enrollment | ❌ Engine error 411 | ❌ Malay fails | ⚠️ partial |
| Qwen Token Plan | N/A | ❌ quota exhausted | ✅ | ❌ resets 28 Aug |
| F5-TTS (local) | ✅ zero-shot | ✅ CPU slow | ✅ multilingual | ✅ canon voice proven |
| ElevenLabs | — | — | — | ❌ no API key |
| Edge-tts | ❌ no clone | ✅ instant | ✅ YasminNeural | ✅ free fallback |

## Canonical Clone Workflow (when providers exhausted)

1. Get source audio (10-24s, clean speech, no background noise)
2. Transcribe reference text (Groq Whisper, `language=ms`)
3. Run F5-TTS with ref_file + ref_text + gen_text
4. F0-check output (librosa pyin)
5. DSP stabilize if needed (soul_envelope_dsp.py or dsp_stabilizer.py)
6. Convert to OGG for Telegram voice bubble
7. Send to Arif for approval

## Fallback Chain (proven 2026-08-25/26)

```
MiniMax (quota?) → Qwen CosyVoice (BM fail) → F5-TTS CPU (works) → edge-tts (no clone)
```

Check MiniMax balance first. If exhausted, skip directly to F5-TTS for cloning or edge-tts for instant non-clone TTS.
