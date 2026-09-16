# Voice Clone Provider Audit — 2026-08-19

External verification of voice cloning capability for the four token-plan providers wired into the arifOS FED (MiniMax, Xiaomi MiMo, Alibaba Qwen, Z.ai/GLM). Source: official docs + Artificial Analysis TTS Arena data. Use when choosing a clone engine for a new sovereign voice identity or evaluating whether to migrate from MiniMax.

## Verdict at a Glance

For Bahasa Melayu (Penang) sovereign voice identity:

| Provider | Clone API | Malay support | Open benchmark | Sovereignty | Verdict |
|---|---|---|---|---|---|
| MiniMax | ✅ speech-2.8-hd voice_clone (10s sample, official `language_boost: "Malay"`) | ✅ verified in docs | ✅ ELO #12 (1173) on Artificial Analysis | ❌ SaaS only | 🥇 Primary — only BM-verified clone |
| Qwen/CosyVoice | ✅ DashScope voice-enrollment | ⚠️ enrollment OK, synthesis fails for BM | ✅ 0.81% CER (CosyVoice3-RL) | ✅ 0.5B model 4-6GB VRAM | 🥈 Champion for non-BM workloads |
| MiMo | ✅ mimo-v2.5-tts-voiceclone (FREE window) | ❌ Chinese + English only | ❌ no public benchmark | ✅ 8B model ~24GB VRAM | 🥉 Wildcard; R&D only |
| Z.ai (Zhipu) | ✅ GLM-TTS-Clone (¥1.50/1K calls, 3s sample) | ❌ Mandarin-centric | ❌ zero clone benchmarks | ✅ 9B GLM-4-Voice OSS | 4th — out of race |
| F5-TTS | ✅ zero-shot (10s ref, CPU) | ✅ multilingual | ✅ MIT open-source | ✅ CPU-only, ~4GB | 🥈 Sovereign fallback |

## Sources

- MiniMax voice_clone docs: https://platform.minimaxi.com/document/voice_clone — `language_boost` enum includes `Malay`, `Indonesian`, `Thai`, `Vietnamese`, `Filipino`. Min sample 10s, max 5min, max 20MB.
- MiniMax benchmark: Artificial Analysis TTS arena, speech-2.8-hd ELO 1173.2 (rank #12).
- Qwen-TTS docs: https://www.alibabacloud.com/help/en/model-studio/qwen-tts — supports voice cloning and voice design via DashScope API. Language list (Qwen3-TTS repo): Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian. NO Malay. CosyVoice3-RL paper: 0.81% CER zh.
- MiMo docs: https://platform.xiaomimimo.com/docs — MiMo-V2.5-TTS offers "Voice Design & Cloning: Create a new voice from a single sentence, or clone any voice with just a few audio samples." Languages: Chinese + English only per MiMo-V2.5-ASR documentation. FREE limited-time window. Token Plan REST TTS path returns 404 (verified 2026-08-19).
- Z.ai docs: https://docs.z.ai/ — only audio offering is GLM-ASR-2512 (STT only). GLM-TTS-Clone exists but no public voice clone benchmarks, no BM support. ZAI Coding Plan has no voice/TTS inclusion.
- Speaker similarity data: CosyVoice2 78.0% zh / 71.8% en; CosyVoice3-RL 77.4% zh. MiniMax claims SOTA without published numbers (F2 red flag).
- CER/WER: CosyVoice3-RL 0.81% zh CER beats human 1.26%. MiniMax 0.83% zh CER but no public benchmark methodology.

## Provider Recommendation per Use Case

### i-ARIF sovereign voice (BM Penang, female, 239Hz envelope)

Primary: **MiniMax speech-2.8-hd** via `voice_clone` (synthetic Penang sample, NOT clone of real person). DSP-locked to 239 Hz. ONLY provider with verified BM `language_boost`.

Why not the others:
- Qwen: Malay not in supported list. Dialect support exists for Chinese only. Will produce BM phonemes with accent drift toward Mandarin or English baselines.
- MiMo: Chinese + English only. Token Plan TTS REST path 404 (verified). Few-shot ICL not true zero-shot.
- Z.ai: STT only, no TTS in documented API surface. GLM-TTS-Clone is Mandarin-centric, no benchmark.

### Sovereignty path (when Arif releases GPU GO)

**CosyVoice3-0.5B or CosyVoice2-0.5B** open-source (Apache 2.0), 4-6GB VRAM. Path: train on sealed i-ARIF corpus to produce a sovereign on-premise clone. Eliminates MiniMax SaaS dependency for BM Penang — but only viable after GPU hardware arrives.

### Budget / free clone probe

MiMo Token Plan has a FREE window for `mimo-v2.5-tts-voiceclone`. Probe value: clone a 3-5 second sample and check whether MiMo's acoustic fingerprint matches the i-ARIF envelope. If yes — promote to P2 fallback. If no — archive.

## Decision Matrix

| Priority | If you need... | Use... |
|---|---|---|
| BM Penang production voice, zero latency criticality | MiniMax speech-2.8-hd voice_clone (via MCP tool) |
| Mandarin, Cantonese, or other Asian language | Qwen CosyVoice via DashScope |
| Open-source on-premise sovereign clone (4-6GB VRAM) | CosyVoice3-0.5B / CosyVoice2-0.5B |
| Cheap bulk clone API for Mandarin content | Z.ai GLM-TTS-Clone (¥1.50/1K calls) |
| Experimental probe (free window) | MiMo Token Plan (REST currently 404 — verify before relying) |
| Sovereign fallback when all cloud exhausted | F5-TTS (CPU, ~4 min/8s, zero-shot from 10s ref) |

## Scar: 2026-08-19 — MiniMax remains primary despite marketing claim

Arif initially flagged that MiniMax "claims TTS Arena #1 — but publishes zero benchmark numbers." This is an F2 red flag. Yet for BM Penang specifically, no competitor offers Malay support. Verifiable > complete. MiniMax wins on verifiable BM capability, not on raw quality claims.

Lesson: choose provider by verified feature support for the specific task, not by leaderboard rank.

## Update: 2026-08-25 — F5-TTS added as sovereign fallback

F5-TTS (open-source, MIT) proven viable for zero-shot voice cloning on CPU. No GPU needed. Performance: 4 min 23s for 8.3s output on VPS CPU. F0 preservation: source 105 Hz → clone 113.6 Hz (+8%).

**Status update:**
- MiniMax: quota exhausted (1008-insufficient balance), MCP tool is the working clone path (raw API returns invalid params)
- Qwen CosyVoice: enrollment succeeds but synthesis fails for Malay content (Engine error 411)
- F5-TTS: ✅ working sovereign fallback, CPU-only

Full session details: see `references/voice-clone-provider-update-2026-08-25.md`.
