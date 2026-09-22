# FED — Inference Hypervisor

> FED = **F**ederated **E**xecution **D**irector
> Decouples skill/intent from provider/model.

## Role
- Provider Discovery
- Health Discovery
- Fallback Discovery
- Cost Discovery

## Capability Signature → Provider Mesh

_Patched 2026-09-22 (kimi-code/FI-008, F13 directive audit-and-close): MiMo-V2.6 series registered in SOT — `mimo-v2.6-pro` prepended on `fed-reasoning-heavy`, `fed-multimodal-vision`, `fed-long-context`; `mimo-v2.6-flash` on `fed-multimodal-vision` and `fed-agent-subagent`; `mimo-v2.6-pro-ultraspeed` available via mimo-platform (PAYG-only). AA Index 46 vs MiniMax-M3's 29 — V2.6-Pro wins intelligence tier, M3 wins latency tier (168.9 vs 134.3 tok/s, 0.92s vs 2.15s TTFT). V2.5 demoted to fallback (Stage 3 SABAR)._

- `fed-reasoning-heavy` → [MiMo v2.6 Pro, DeepSeek V4 Pro, Qwen 3.8 Max, Gemini 3.6 Flash, Mimo v2.5 Pro]
- `fed-multimodal-vision` → [MiMo v2.6 Pro, MiMo v2.6 Flash, Qwen VL Max, Gemini 3.6 Flash, Mimo v2.5]
- `fed-long-context` → [MiMo v2.6 Pro, MiniMax-M3, Mimo v2.5 Pro, Qwen 3.8 Max]
- `fed-agent-subagent` → [MiMo v2.6 Flash, DeepSeek V4 Flash, Qwen 3.6 Flash, Mimo v2.5]
- `fed-realtime-voice` → [Mimo v2.5 TTS, Mimo v2.5 ASR]

## Nothing Above FED References Specific Models
- Skills → `capability_signature: fed-reasoning-heavy`
- AAA → does not know models
- QQQ → does not know models
- A-FORGE → only knows about job execution, not inference
