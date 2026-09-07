---
name: mimo-audio
description: "FEDERATED Xiaomi MiMo v2.5 audio intelligence — TTS (0-credit free window), ASR (en/zh), voice design, voice clone (F13-gated). Available to ALL AAA agents via this canonical skill. Use when generating speech/voice notes, designing voices, or transcribing wav/mp3 (en/zh). BM/dialect stays on GLM/dashscope lanes. TRANSPORT: direct lane (litellm cannot carry audio bodies)."
---

# MiMo Audio — federated organ (AAA canonical, 2026-09-07)

**Status:** LIVE, E2E-verified. TTS = 0 credits while free window lasts.
**Env (every FI home + Hermes):** `MIMO_TOKEN_PLAN_API_KEY` + `MIMO_BASE_URL` (https://token-plan-sgp.xiaomimimo.com/v1); alias `MIMO_API_KEY`.
**Contracts SOT:** `/root/.config/federation-models.json` → `mimo/mimo-v2.5-*` (`api_contract`) + signatures `fed-realtime-voice` (WIRED_DIRECT_LANE) / `fed-audio-understanding`.

## ⚠️ TRANSPORT WARNING (E2E-tested 2026-09-07)
- **FED front door `:4000`** lists all 6 mimo models (discovery GREEN) — but **litellm's translator CANNOT carry audio bodies**: TTS response crashes `convert_dict_to_response.py` (`message.audio` unknown); ASR `input_audio` content part gets mangled → provider "Param Incorrect".
- **Audio bodies MUST ride the DIRECT lane** (agent → `$MIMO_BASE_URL/chat/completions`). ToS-clean agent-tool usage, E2E-proven below. Text-lane MiMo traffic may use :4000 normally.
- Filed for FED owner (FI-008): litellm audio-body support + classifier audio lexicon (v1 has no audio class).

## The three TTS models — ALL ride POST {BASE}/chat/completions (NOT /audio/speech)
| model | voice source | singing | clone | design |
|---|---|---|---|---|
| mimo-v2.5-tts | builtin | yes ((唱歌)/(sing) prefix, CN lyrics best) | no | no |
| mimo-v2.5-tts-voicedesign | text description (user msg) | no | no | yes |
| mimo-v2.5-tts-voiceclone | audio sample data-URI <=10MB mp3/wav | no | yes | no |

**Wire:** assistant message = text to speak; user message = style instructions (not spoken); `audio: {format: "wav"|"pcm16"(stream), voice: "<id>"}`; response `choices[0].message.audio.data` = base64 wav; stream = `delta.audio.data` 24kHz PCM16LE mono.
**Voices:** EN Mia / Chloe / Milo / Dean — CN 冰糖 / 茉莉 / 苏打 / 白桦 (+ mimo_default).
**Style control:** natural language (user msg) + inline audio tags `[pause] [sighs] [sternly] [trembling]` (bilingual, mixable) + screenplay layers Instruct/Text/Character/Scene/Direction.
**Gotchas:** `audio.voice` is model-specific — voicedesign MUST omit it (HTTP 400); clone needs data-URI; TTS output is random — regenerate a few times to pick the best take.

## ASR — mimo-v2.5-asr (chat/completions, NOT /audio/transcriptions)
Content part: `{"type":"input_audio","input_audio":{"data":"data:audio/wav;base64,..."}}`; wav/mp3 ONLY; b64 <= 10MB; `asr_options.language` in auto|zh|en — **no `ms`**; BM/dialect rides `auto` (Penang-Besi UNTESTED → prefer dashscope/GLM for BM fidelity). ~30M credits/audio-hour (~$0.074/h).

## Governance
- voiceclone/voicedesign new voice_id = **F13 SOVEREIGN gate**; reuse = F11 audit (see AAA-voice-cloning-mimo-minimax).
- i-ARIF voice_id stays MiniMax speech-2.8-hd — do NOT move.
- ToS: token-plan key for agent/harness use only — never cron/backend.

## Fallback ladder
mimo-audio (0 credits, free window) → edge-tts (free floor, ms-MY voices) → QwenCloud token-plan TTS.

## E2E receipts (2026-09-07)
- Direct TTS (Hermes KVM4, Mia): 307,244B wav / 24kHz mono / 6.4s / 223 tokens / 0 credits
- Direct TTS (FI-003 KVM8): 133,180 b64 chars / 173 tokens / 0 credits
- Vision understanding: 128x128 red PNG → "Red." (img_tokens=16, cached=192)
- litellm :4000 TTS/ASR bodies: RED (translator) — warning above

## Quick recipe (direct lane)
    curl -sS "$MIMO_BASE_URL/chat/completions" \
      -H "Authorization: Bearer $MIMO_TOKEN_PLAN_API_KEY" \
      -H 'Content-Type: application/json' -d '{
      "model":"mimo-v2.5-tts",
      "messages":[{"role":"user","content":"Warm, friendly Malaysian English."},{"role":"assistant","content":"Good morning, the federation is healthy."}],
      "audio":{"format":"wav","voice":"Mia"}}' \
      | jq -r '.choices[0].message.audio.data' | base64 -d > out.wav

## Federation map
Canonical: `/root/AAA/skills/mimo-audio` (this file) · Hermes original: KVM4 `~/.hermes/skills/media/mimo-audio` · visible to: qwen/claude/codex/grok (whole-dir AAA links) + kimi-code/opencode-config/gemini/.agents (per-skill links) — 9 homes total · official vendor reference: `references/official/` (MIT, XiaomiMiMo/MiMo-Skills).
