# 🔬 MiMo — Xiaomi's Reasoning LLM Family

> **Research Date:** 2026-07-11
> **Researcher:** Hermes (SOUL layer)
> **Sovereign:** ARIF (F13)
> **Epistemic Tags:** OBS (observed from sources), DER (derived/interpreted), SPEC (speculated)

---

## 1. Identity

| Field | Value |
|-------|-------|
| **Developer** | Xiaomi Corp. (LLM-Core Team) |
| **Team Lead** | Luo Fuli (ex-DeepSeek, joined Xiaomi late 2025) |
| **First Release** | April 30, 2025 (MiMo-7B) |
| **Latest Release** | April 22, 2026 (MiMo-V2.5 + MiMo-V2.5-Pro) |
| **Website** | mimo.xiaomi.com / mimo.mi.com |
| **GitHub** | github.com/XiaomiMiMo |
| **HuggingFace** | huggingface.co/XiaomiMiMo |
| **Investment** | $8.7B committed to AI over 3 years (Lei Jun, March 2026) |
| **ArXiv Papers** | 2505.07608 (MiMo-7B), 2601.02780 (V2-Flash), 2506.03569 (VL) |

---

## 2. Model Family — Complete Lineup

| Model | Released | Params (Total) | Params (Active) | Context | License | Architecture |
|-------|----------|----------------|-----------------|---------|---------|-------------|
| **MiMo-7B** | Apr 2025 | 7B | 7B (dense) | 32K | MIT | Dense Transformer |
| **MiMo-V2-Flash** | Dec 2025 | 309B | 15B | 256K | MIT | MoE + Hybrid SWA |
| **MiMo-V2-Pro** | Mar 2026 | 1T | 42B | 1M | Proprietary | MoE |
| **MiMo-V2-Omni** | Mar 2026 | Unknown | Unknown | 1M | Proprietary | Multimodal MoE |
| **MiMo-V2-TTS** | Mar 2026 | Unknown | — | — | Proprietary | Speech synthesis |
| **MiMo-V2.5** | Apr 2026 | 310B | ~15B | 1M | MIT | MoE + Hybrid SWA + Omni |
| **MiMo-V2.5-Pro** | Apr 2026 | 1.02T | 42B | 1M | MIT | MoE + Hybrid SWA |
| **MiMo-VL-7B** | 2025 | 7B | 7B | — | MIT | ViT + MiMo-7B backbone |
| **MiMo-Audio-7B** | 2025 | 7B | 7B | — | MIT | 25Hz Transformer + RVQ |
| **MiMo-Embodied** | 2025 | Unknown | Unknown | — | Unknown | Cross-embodied (driving + robotics) |

---

## 3. Architecture Deep Dive (OBS)

### 3.1 MiMo-7B — The Foundation
- **Pre-training:** ~25 trillion tokens (web, papers, books, synthetic reasoning data)
- **Data emphasis:** Math + code data increased to ~70% in final pre-training phase
- **Post-training:** SFT on 500K→6M instances, RL on 130K math+code problems
- **RL window:** Expanded from 32K to 48K tokens
- **Key innovation:** Proves small models can match larger ones with targeted training

### 3.2 MiMo-V2-Flash — The Efficiency Breakthrough (OBS from arXiv 2601.02780)
- **Architecture:** MoE — 309B total, 15B active per token
- **Experts:** 256 total, 8 activated per token, no shared experts
- **Attention:** Hybrid SWA + Global Attention at **5:1 ratio**
  - 39 SWA layers + 9 GA layers (48 total)
  - Sliding window: **128 tokens** (aggressive!)
  - ~6× reduction in KV-cache and attention compute for long contexts
  - Learnable attention sink bias enables aggressive windowing
- **MTP (Multi-Token Prediction):** 0.33B params per MTP block, dense FFN + SWA
  - Used for speculative decoding → **2.6× speedup**, 3.6 acceptance length
  - 3 MTP layers included in open-source release
- **Pre-training:** 27T tokens, FP8 mixed precision, native 32K → extended to 256K
- **Post-training:** Multi-Teacher On-Policy Distillation (MOPD)
  - 3-stage: (1) General SFT, (2) Domain-specialized RL/SFT teachers, (3) Student learns from teachers + verifiable rewards
- **Head dims:** Q/K=192, V=128; SWA: 64Q/8KV heads, GA: 64Q/4KV heads

### 3.3 MiMo-V2.5-Pro — The Flagship (OBS from multiple sources)
- **Architecture:** MoE — 1.02T total, 42B active, hybrid attention
- **Context:** 1M tokens
- **Pricing:** ~$0.43/1M input, ~$0.87/1M output (8× cheaper than Claude Opus 4.6)
- **Key capabilities:**
  - Built a complete compiler in 4.3 hours (672 tool calls, 4 phases)
  - Produced ~8,000-line desktop video editor from brief prompts
  - 40-60% fewer tokens than Claude Opus 4.6 / Gemini 3.1 Pro
- **Benchmark: MiMo Coding Bench:** 73.7 (vs Claude Opus 4.6: 77.1, Gemini 3.1 Pro: 67.8)

### 3.4 MiMo-V2.5 — The Omnimodal (OBS from HuggingFace)
- Built on V2-Flash backbone + vision/audio encoders
- 729M-param ViT with hybrid window attention
- Audio encoder initialized from MiMo-Audio weights
- Supports text, image, video, audio understanding
- 1M context, open-weight (MIT license)

---

## 4. Benchmark Performance (OBS)

### MiMo-V2-Flash vs Frontier Models
| Benchmark | MiMo-V2-Flash | DeepSeek-V3.2 | K2-Thinking | Claude Sonnet 4.5 | GPT-5 (High) | Gemini 3.0 Pro |
|-----------|---------------|---------------|-------------|-------------------|--------------|----------------|
| SWE-Bench Verified | **73.4%** | 73.1% | 71.3% | 77.2% | 76.2% | 85.4% |
| SWE-Bench Multilingual | **71.7%** | 70.2% | 61.1% | 68.0% | 85.4% | 76.2% |
| AIME 2025 | **80.3%** | 80.3% | 74.3% | 84.7% | 85.0% | 95.0% |
| GPQA-Diamond | **94.1%** | 93.1% | 94.5% | 87.0% | 91.9% | — |
| HLE (w/o Tool) | **84.3%** | 82.4% | 84.5% | 83.4% | 37.5% | — |
| Arena-Hard | **22.1%** | 25.1% | 23.9% | 13.7% | 26.3% | 37.5% |

### MiMo-7B-RL Performance (OBS)
| Benchmark | MiMo-7B-RL | MiMo-7B-RL-0530 | Notes |
|-----------|------------|-----------------|-------|
| MATH-500 | 95.8% | — | Pass@1 |
| AIME 2024 | 68.2 | 80.1 | Surpasses DeepSeek R1 (79.8) |
| LiveCodeBench v5 | 57.8% | — | Pass@1 |

### MiMo-V2.5-Pro Coding (OBS)
| Benchmark | MiMo-V2.5-Pro | Claude Opus 4.6 | GPT-5.4 | Gemini 3.1 Pro |
|-----------|---------------|-----------------|---------|----------------|
| MiMo Coding Bench | 73.7 | 77.1 | — | 67.8 |
| SWE-Bench Verified | ~78.6 (Thinking) | — | — | — |

---

## 5. Key Innovations (DER)

### Innovation 1: Pre-training for Reasoning Potential
MiMo's thesis: RL effectiveness depends on the **inherent reasoning potential of the base model**. By saturating pre-training with 70% math+code data and 25T tokens, the base model already has strong reasoning priors before any RL begins. This is why a 7B model can beat 32B models on math.

### Innovation 2: Aggressive Hybrid Attention
The 128-token sliding window with 5:1 SWA:GA ratio is the most aggressive hybrid attention in any frontier model. Learnable attention sink bias makes this viable — it's the key architectural enabler for cost-efficient long-context processing.

### Innovation 3: MTP as Speculative Decoding
Repurposing Multi-Token Prediction modules as draft models for speculative decoding is elegant — training signal becomes inference speedup. 2.6× decode speed with 3 MTP layers.

### Innovation 4: Multi-Teacher On-Policy Distillation (MOPD)
Instead of one massive RL run, MiMo trains domain-specialized teachers (math, code, agentic) then distills into a single student. This scales RL compute efficiently and avoids the capability imbalance problem.

### Innovation 5: Context Management (Unix-inspired)
Tools, docs, and databases exposed as "files" — model retrieves via Bash commands. Aggressive memory compression when context >30% utilization → 5-10% accuracy gains on deep research tasks.

---

## 6. The "Hunter Alpha" Story (OBS)

Before MiMo-V2-Pro's official release, it appeared anonymously on OpenRouter under codename **"Hunter Alpha"**. It:
- Topped daily usage charts for several days
- Processed over **1 trillion tokens** in total usage
- Was mistaken by some users for a DeepSeek model
- Reuters confirmed Xiaomi's origin after speculation

This is a significant credibility signal — the model performed well enough in blind testing to gain organic adoption before anyone knew what it was.

---

## 7. Licensing Strategy (DER)

| Tier | Models | License | Implication |
|------|--------|---------|-------------|
| Open-weight | MiMo-7B, V2-Flash, V2.5, V2.5-Pro | **MIT** | Fully open, F11 audit-friendly |
| Proprietary | V2-Pro, V2-Omni, V2-TTS | Proprietary | API-only, no weight access |

**Notable:** V2.5-Pro (1T params) is MIT-licensed while V2-Pro (1T params) was proprietary. Xiaomi opened up the flagship. This is a strategic choice — MIT licensing on the best model maximizes ecosystem adoption.

---

## 8. Weaknesses & Gaps (INT/SPEC)

### Known Issues
- **SWE-Bench reward hacking:** MiMo team discovered ground truth commits weren't properly deleted in SWE-Bench images. They fixed it in their own training/eval but this is an industry-wide issue.
- **Arena-Hard scores lag:** MiMo-V2-Flash scores 22.1% vs Gemini 3.0 Pro's 37.5% — creative writing and general conversation not the strength.
- **Chinese-first bias (SPEC):** English-first optimization evident. Chinese language performance not well-documented in English-facing papers.
- **Proprietary V2-Pro/V2-Omni (OBS):** These variants lack weight access — less auditability for the multimodal frontier tier.
- **Migration chaos (OBS):** Silent legacy→V2.5 pricing reroute, ASR TPM asymmetry, model ID naming drift (dash vs dot).

### What It Doesn't Give You
- No documented safety/alignment research beyond standard RLHF
- No explicit constitutional AI or governance framework
- No red-teaming disclosure or responsible scaling policy
- MoE architecture means full model replication requires massive infrastructure (309B-1T weights)
- Benchmark performance vs real-world reliability gap unknown

---

## 9. Strategic Position (INT)

MiMo occupies a unique position: **Chinese company, MIT-licensed frontier model, reasoning-first design**. 

- vs **DeepSeek:** Similar open-weight Chinese origin but MiMo focuses on smaller models punching up (7B beating 32B) rather than raw scale
- vs **Qwen (Alibaba):** MiMo has stronger reasoning benchmarks; Qwen has broader ecosystem integration
- vs **Western frontier (Claude/GPT/Gemini):** 40-60% fewer tokens for comparable coding performance at 1/8th the price
- vs **Kimi (Moonshot):** Direct competitor in Chinese reasoning models; MiMo-V2-Flash rivals K2-Thinking

**The arifOS angle (INT):** MiMo is already wired into the federation as `ACTIVE_FALLBACK`. V2.5-Pro's MIT license + strong coding performance + cost efficiency makes it a viable PRIMARY candidate for OpenCode workloads. The agentic capabilities (1000+ tool calls, 4.3-hour compiler builds) align with A-FORGE's execution model.

---

## 10. Model Registry Update Notes

### What Changed Since Last Registry Entry (2026-06-15)
1. **V2.5 family fully released** (April 22, 2026) — V2.5 and V2.5-Pro both MIT-licensed
2. **V2.5-Pro specs confirmed:** 1.02T total, 42B active, 1M context, MIT license
3. **V2.5 multimodal:** ViT 729M, audio encoder from MiMo-Audio, omni modal
4. **Benchmarks updated:** SWE-Bench, AIME, MiMo Coding Bench scores
5. **Hunter Alpha story confirmed** by Reuters
6. **UltraSpeed variant announced:** mimo-v2.5-pro-ultraspeed (early access)
7. **MiMo-VL 2508 update:** Enhanced vision+video benchmarks (70.6 MMMU, 70.8 VideoMME)

### Registry Recommendations
- Status should remain `ACTIVE_FALLBACK` pending F11 cooling ledger completion
- Architecture field should be updated with V2.5-Pro specs (1.02T MoE, 42B active, hybrid SWA)
- Benchmark scores should be added to capability profile
- MIT license is a major F11 auditability upgrade over previous proprietary V2-Pro

---

## Sources

| Source | Type | Epistemic |
|--------|------|-----------|
| Wikipedia: Xiaomi MiMo | Encyclopedia | OBS |
| arXiv 2505.07608 (MiMo-7B paper) | Technical paper | OBS |
| arXiv 2601.02780 (V2-Flash report) | Technical paper | OBS |
| arXiv 2506.03569 (VL report) | Technical paper | OBS |
| mimo.xiaomi.com (official) | Vendor | OBS |
| HuggingFace: XiaomiMiMo/MiMo-V2.5 | Model card | OBS |
| GitHub: XiaomiMiMo/MiMo-V2-Flash | Code/weights | OBS |
| The Decoder, Neura Market, Reuters | News | OBS |
| LLMReference comparison | Third-party | OBS |
| AAA model_soul.yaml (registry) | Internal | OBS |

---

*Sealed by research protocol. DITEMPA BUKAN DIBERI.*
