# EMD Lane Table — Live Federation State

> **Last verified:** 2026-08-08 (F2 evidence: live probes + curl to QwenCloud dashboard)
> **Re-probe before any SEAL-grade claim.** Live state shifts faster than this table.
> **Canonical source:** `/root/A-FORGE/litellm-config.yaml` + FED :7074 status

## Master Table

| Model | Lane | Max Input | Max Output | Multimodal | Cost In $/M | Cost Out $/M | Provider | Constitutional Tier | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **deepseek-v4-pro** | ACT | 1,048,576 (1M) | **384,000** | text | 0.435 | 0.87 | direct deepseek | ✅ 666/999 | Workhorse. 384k output = ACT stability floor. |
| **deepseek-v4-flash** | ACT (lite) | 1,048,576 | 131,072 | text | 0.14 | 0.28 | direct deepseek | 333 only | Cheap ACT for high-volume iterations. |
| **deepseek-v4-flash-0731** | ACT (lite) | 1,048,576 | 131,072 | text | 0.20 | 0.80 | mulerouter gateway | 333 only | Older snapshot. Avoid unless newer flash is down. |
| **MiniMax-M3** | **SENSE** | 1,048,576 | 131,072 | text+image | ~1.80 | ~2.40 | direct MiniMax | ✅ 666/999 | 1M context champion. Wrong tool for ACT coding loops. |
| **qwen3.8-max** | **SENSE + ACT lite** | 1,000,000 | 131,072 | text+image | 0.50 | 2.00 | qwen-individual / token-plan | ✅ 666/999 | The compromise. Mid-size multimodal + medium code. |
| **qwen3.7-max** | SENSE | 262,144 | 131,072 | text | 0.50 | 2.00 | qwen-individual / token-plan | 555 only | Older 3.7 — smaller context. |
| **qwen3.7-plus** | ACT (lite) | 262,144 | 131,072 | text | 0.15 | 0.60 | qwen-individual | 333 only | Cheap Qwen ACT. |
| **qwen3.6-flash** | ACT (recovery) | 1,000,000 | 131,072 | text | 0.15 | 0.60 | qwen-individual / mulerouter | 333 only | High-volume flash. |
| **glm-5.2** | ACT (free) | varies | varies | text | **0.00** | **0.00** | tokenrouter (free) | ✅ 666/999 | Free reasoning — budget ACT when quota threatened. |
| **kimi-k3** | ACT (free) | 1,000,000 | 131,072 | text+image | **0.00** | **0.00** | tokenrouter (free) | 333 only | Free ACT, smaller output. |
| **kimi-k2.7-code** | ACT (coding) | varies | varies | text | 0.20 | 0.80 | qwen-individual | 333 only | Kimi coding specialist. |
| **mimo-v2.5-pro** | ACT (lite) | 1,048,576 | 131,072 | text+image | 0.14 | 0.28 | Xiaomi token plan | 333 only | Hermes-asi default — strong tool calling. |
| **mimo-v2.5** | ACT (lite) | 1,048,576 | 131,072 | text | 0.14 | 0.28 | Xiaomi token plan | 333 only | Hermes-asi primary fallback. |
| **qwen-vl-max** | SENSE (vision) | 32,768 | 8,192 | text+image | 0.80 | 2.00 | mulerouter | 333 only | Vision specialist. |
| **wan2.7-image-pro** | SENSE (image-gen) | varies | varies | image-in | TBD | TBD | qwen-individual | n/a | Image generation, not chat. |
| **qwen-audio-3.0-tts-plus** | METABOLIZE (audio) | varies | varies | text→audio | TBD | TBD | qwen-individual | n/a | TTS — bridge modality. |

## Constitutional Allowlist (per `federation-models.json _meta.constitutional_rule`)

**Only these 4 may serve 666_JUDGE / 999_SEAL:**

1. `deepseek-v4-pro` — primary
2. `glm-5.2` — free fallback
3. `qwen3.8-max` — multimodal fallback
4. `MiniMax-M3` — 1M-context fallback

**Mapping by lane:**

| Lane | Constitutional-eligible | Why |
|---|---|---|
| ACT | deepseek-v4-pro, glm-5.2 | Both sustain long autoregressive chains |
| SENSE | qwen3.8-max, MiniMax-M3 | Wide context + multimodal |
| Mixed | (qwen3.8-max bridges both) | The compromise choice for tier 666/999 |

## Live Provider State (FED :7074, 2026-08-08)

| Pool | Track | Balance | Confidence | Health | Notes |
|---|---|---|---|---|---|
| deepseek | A | $12.54 | 1.0 | LIVE | API-probed 2026-08-05 |
| flame | A | $0.00 | 1.0 | LIVE | FREE — FLAME :18901 (Groq + Gemini) |
| qwen-token-plan-individual | A | $0.00 | 1.0 | LIVE | QwenCloud Individual Pro, 94.5% 7-day quota, 5hr removed |
| qwen-token-plan-team | A | $0.00 | 1.0 | LIVE (limited) | Team plan EXHAUSTED 0/150K credits. qwen-native 429. |
| bailian-token-plan | B | $25.00 | 1.0 | n/a | Track B estimate |
| mimo-platform | B | $10.00 | 1.0 | n/a | Track B estimate |
| minimax | B | $0.00 | 0.95 | LIVE | Monthly token plan (not zero balance = dead) |
| mulerouter | B | $49.93 | 0.99 | ARCHIVED | Orphaned 2026-08-04 |
| tokenrouter | B | $59.94 | 0.98 | PARKED | Drained, no top-ups |
| openrouter | B | $0.50 | 0.60 | ARCHIVED | Near-empty |

## Cost Ratios at ACT Scale (live 2026-08-08)

Computing cost for a typical 100k-token-out, 5k-token-in coding task:

| Model | Cost (5k in + 100k out) | Output stability (subjective) |
|---|---|---|
| deepseek-v4-pro | $0.0022 + $0.087 = **$0.089** | ⭐⭐⭐⭐⭐ |
| deepseek-v4-flash | $0.0007 + $0.028 = **$0.029** | ⭐⭐⭐⭐ |
| MiniMax-M3 | $0.0090 + $0.240 = **$0.249** | ⭐⭐⭐ (output drift > 50k tokens) |
| qwen3.8-max | $0.0025 + $0.200 = **$0.203** | ⭐⭐⭐⭐ |
| glm-5.2 (free) | **$0.00** | ⭐⭐⭐ |
| kimi-k3 (free) | **$0.00** | ⭐⭐⭐ |

**Inference:** Using MiniMax-M3 for ACT cost 2.8× more than deepseek-v4-pro AND produces less stable long output. Pure SENSE-on-ACT loss.

## Quick Lookup — "I need to do X, which model?"

| I need to... | Lane | First pick | Why |
|---|---|---|---|
| Write 50k+ tokens of code that compiles | ACT | deepseek-v4-pro | 384k output, stability floor |
| Generate 5-10k tokens of reasoning | ACT | deepseek-v4-flash | Cheap, fast, sufficient |
| Ingest a 500k-token repo for analysis | SENSE | MiniMax-M3 | 1M context window |
| Process images + text | SENSE | qwen3.8-max | Multimodal, constitutional |
| Hold a long conversation in Bahasa | ACT lite | mimo-v2.5 | Hermes default, tool-calling strong |
| Hit a 666/999 verdict | ACT or SENSE (per task) | deepseek-v4-pro (ACT) or MiniMax-M3 (SENSE) | Constitutional allowlist |
| Fall back when DeepSeek is down | ACT or SENSE | qwen3.8-max (SENSE) or glm-5.2 (ACT free) | Different lanes, different cascades |
| Test a sub-task inside OpenClaw | varies | subtask.allowedModels override | Subtask is the unit of split |

## Drift Watch

| Symptom | Likely cause | Action |
|---|---|---|
| Cost per task rising, quality flat | SENSE model on ACT task | Switch to deepseek-v4-pro |
| Hallucinations on >100k generation | ACT model past its stability window | Reduce generation length or chain multiple short ACT loops |
| Quota exhausted on MiniMax | Over-routed to SENSE when ACT would work | Switch small SENSE tasks to qwen3.8-max |
| Inference latency >5s sustained | Wrong lane + cascading retries | Re-pick by lane; don't let cascade continue >3 retries |
