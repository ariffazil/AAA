# FED — Inference Hypervisor

> FED = **F**ederated **E**xecution **D**irector
> Decouples skill/intent from provider/model.

## Role
- Provider Discovery
- Health Discovery
- Fallback Discovery
- Cost Discovery

## Capability Signature → Provider Mesh
- `fed-reasoning-heavy` → [DeepSeek V4 Pro, Qwen 3.8 Max, Gemini 3.6 Flash]
- `fed-multimodal-vision` → [Qwen VL Max, Gemini 3.6 Flash, Mimo v2.5]
- `fed-long-context` → [MiniMax-M3, Mimo v2.5 Pro, Qwen 3.8 Max]
- `fed-agent-subagent` → [DeepSeek V4 Flash, Qwen 3.6 Flash, Mimo v2.5]
- `fed-realtime-voice` → [Mimo v2.5 TTS, Mimo v2.5 ASR]

## Nothing Above FED References Specific Models
- Skills → `capability_signature: fed-reasoning-heavy`
- AAA → does not know models
- QQQ → does not know models
- A-FORGE → only knows about job execution, not inference
