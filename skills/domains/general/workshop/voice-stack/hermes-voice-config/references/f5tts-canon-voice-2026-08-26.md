# F5-TTS Canon Voice Session — 2026-08-26

## Context

Arif sent a voice note (24.8s, OGG, F0 105.3 Hz — male register) and said "clone this and make this as canon voice." This was a direct F13 sovereign authorization — Arif's own voice, explicit consent.

## What happened

1. **Source audio analyzed:** 24.8s, F0 105.3 Hz (male), SNR 7.9 dB (low noise), 18% voiced frames
2. **Transcription:** Groq Whisper-large-v3-turbo — Malay (Penang dialect)
3. **MiniMax attempt:** `mcp__minimax_media__voice_clone` → `1008-insufficient balance` (quota exhausted)
4. **Qwen CosyVoice attempt:** Voice enrollment succeeded (`cosyvoice-v3-plus-iarifcanon-9b8a9453168b4ffb81f73acee587c31e`), but synthesis failed for all models (`Engine error [411]: TTS speak operation failed`)
5. **F5-TTS success:** Zero-shot clone from 10s reference clip, CPU inference, 4min50s for 7.6s audio

## Files created

| File | Purpose |
|---|---|
| `/root/AAA/engines/f5tts_pipeline.sh` | Hermes command-provider pipeline script |
| `/root/AAA/engines/f5tts/reference.wav` | Full source audio (24.8s, 792KB) |
| `/root/AAA/engines/f5tts/reference-10s.wav` | 10s clip for faster inference (480KB) |

## Performance

| Metric | Value |
|---|---|
| Inference time | 4 min 50s (CPU, single thread) |
| Output duration | 7.6s |
| F0 source | 105.3 Hz |
| F0 clone | 93.8 Hz (-11%) |
| Voiced frames | 91% |
| Spectral centroid | ~1900 Hz |

## Provider status (2026-08-25/26)

| Provider | Status | Notes |
|---|---|---|
| MiniMax | ❌ Quota exhausted | `1008-insufficient balance` |
| Qwen CosyVoice | ⚠️ Voice created, synthesis fails | BM not fully supported |
| Qwen Token Plan | ❌ Quota exhausted | Resets 2026-08-28 |
| F5-TTS | ✅ Working | CPU only, ~4 min per utterance |
| ElevenLabs | ❌ No API key | Not configured |
| Edge-tts | ✅ Working | No cloning, free fallback |

## Key learnings

1. **F5-TTS preserves male register** — source 105 Hz → clone 93 Hz. No feminine drift.
2. **CPU inference is viable** — 4+ min is acceptable for testing/development, not production.
3. **10s reference clip works** — don't need full 24.8s source. Shorter = faster inference.
4. **Reference text matters** — the ref_text must match the reference audio content exactly.
5. **HuggingFace cache** — F5-TTS models auto-download on first run (~2GB). Cache at `/root/.cache/huggingface/hub/models--SWivid--F5-TTS/`.

## Not yet wired into Hermes config

The pipeline script exists but hasn't been wired into `~/.hermes/config.yaml` as a command provider. Arif needs to decide:
- Keep V8 (i-arif-sovereign) as production
- Add F5-TTS canon as alternative provider
- Or replace V8 entirely

Gateway restart required after any config change.

## Quota exhaustion pattern

This session proved the fallback chain:
```
MiniMax (quota) → Qwen CosyVoice (BM fail) → F5-TTS CPU (works) → edge-tts (no clone)
```

The chain is now documented in the main skill. Future sessions should check MiniMax balance before attempting voice operations.
