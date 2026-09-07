# MODEL_TO_CAPABILITY_MAP.md
FED Zen v1 — 2026-09-08. Doctrine: expose capabilities, hide implementations.
Model = labour (exchangeable). Capability = constitutional primitive.

| Capability | Organ | Visible lane | Hidden labour (cascade order) |
|---|---|---|---|
| SOVEREIGN | ARIF seat | i-arif | qwen3.8-max → qwen3.7-plus → qwen3.6-plus (+fallbacks: kimi-k3, MiniMax-M3, glm-5.3, mimo-v2.5, gemini-3.6-flash) |
| THINK | 333-AGI | agi-333 | qwen3.8-max, qwen3.7-max, qwen3.7-plus, deepseek-v4-pro, kimi-k3 (5 kept) |
| RESEARCH | Hermes/555 | asi-555 | qwen family + fallbacks |
| COURT | 888-APEX | apex-888 | gemini-2.5-pro (+fallbacks) |
| FORGE | A-FORGE | forge-777 | MiniMax-M3, glm-5.3, deepseek-v4-flash-vision, qwen3.7-plus/max |
| CODE | Dev organ | opencode | 5 proven upstreams kept |
| VISION | Vision organ | fed/vision | gemini/qwen/deepseek vision models |
| IMAGE | Visual forge | fed/image-gen | image gen backends |
| VOICE | Speech organ | fed/audio | fed/audio-tts, fed/audio-asr (+voiceclone-restricted internal) |

## Not model territory (do NOT route via LiteLLM)
- MEMORY → VAULT999 / Qdrant (storage, kernel plane)
- IDENTITY → i-ARIF/i-AZWA personas (meaning plane, decides; never routes)
- WITNESS / JUDGMENT → arifOS kernel :8088 (constitutional plane)

## Legacy aliases now hidden (internal only)
tts, speech, asr, stt, transcribe, vision, gemini-vision, gemini-flash, gemini-pro,
qwen-vision, hermes-asi, hermes-asi-vision, openclaw, qwen3.6-plus, qwen3.8-max,
kimi-k3, glm-5.2, glm-5.3, MiniMax-M3, mimo-v2.5*, deepseek-v4-flash(-vision),
gemini-2.5-*, gemini-3.5-transcribe, gemini-3.6-flash, fed/audio-tts, fed/audio-asr.
