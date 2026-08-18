---
name: "token-plan-speech"
id: "token-plan-speech"
version: 1.0.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: "Call Qwen Token Plan speech models on the Personal allowlist (TTS, ASR, realtime). Activate for text-to-speech, speech-to-text, or live voice on Token Plan."
autonomy_tier: T1
capability_tier: fed-multimodal-audio
ecology_state: WARM
---

Speech on **Qwen Token Plan** only. Capability SOT: `CAPABILITIES.json` (`audio_in` / `audio_out`).

User request: $ARGUMENTS

## Allowlist (exact IDs)

| Model | Job |
|---|---|
| `qwen-audio-3.0-tts-plus` | **Default TTS** + clone/instruct |
| `qwen-audio-3.0-asr-flash` | Speech-to-text |
| `qwen-audio-3.0-realtime-plus` | Realtime conversation |

Pay-as-you-go CosyVoice / `qwen3-tts-vd-*` / Omni S2S are **not** on Token Plan Personal. Do not call them on this key.

S2S vs pipeline (from docs): S2S for live talk; pipeline (ASR + LLM + TTS) when you need voice design/clone control.

## Notes

- Use `QWEN_API_KEY` + Token Plan Singapore host.
- Malay is listed on Omni/Livetranslate tables, not on this Token Plan TTS trio. Do not claim Malay S2S on these three IDs.
- MiniMax `voice_design` / `text_to_audio` is a different hand (`minimax-media`).
- Docs: https://docs.qwencloud.com/developer-guides/speech/tts-models
  S2S: https://docs.qwencloud.com/developer-guides/speech/s2s-models
