# Malaysia AI Landscape — August 2026

Research snapshot from deep research session 2026-08-14. Sources: HF API direct, Jina Reader, Bing News RSS, HuggingFace models API.

## 1. Mesolitica (Malaysia, independent, community)

Founder: Husein Zolkepli (GitHub: huseinzol05). One person. No visible institutional backing.

### Models on HuggingFace (top downloads)
| Model | Downloads | Type |
|---|---|---|
| wav2vec2-xls-r-300m-mixed | 760,931 | ASR (multilingual) |
| llama2-embedding-1b-8k | 195,210 | Embedding |
| Qwen2.5-72B-Instruct-FP8 | 143,733 | LLM (quantized) |
| sentiment-analysis-nanot5-small-malaysian | 20,660 | Sentiment |
| Malaysian-TTS-0.6B-v1 | 12,001 | TTS (DistilCodec) |
| Malaysian-whisper-large-v3-turbo-v3 | 4,727 | ASR |
| MaLLaM-5B | 129-233 | LLM (Mistral-based) |

### Key assets
- **Malaysian-Emilia** (9,152 downloads): 15,631 hrs Malaysian speech + 600 hrs Mandarin. THE dataset for Malaysian voice AI.
- **Malaysian-Emilia-annotated** (2,104): Emotion-annotated subset.
- **Malaysian-Voice-Conversion**: Post-filtered from Emilia for F5-TTS training.
- **Malaysian-dialects-youtube** (5,079): Dialect-specific YouTube speech corpus.
- **MaLLaM** (1.1B-5B): Mistral-based LLM, fine-tuned on Malaysian instructions.

### F5-TTS Malaysian (CRITICAL for I-ARIF voice layer)
- **Malaysian-F5-TTS-v3**: Full-parameter finetune of SWivid/F5-TTS on Malaysian-Emilia.
- **Checkpoint:** `hf://mesolitica/Malaysian-F5-TTS-v3/checkpoints/model_220000.pt`
- **Source code:** github.com/mesolitica/malaya-speech session/f5-tts
- **Claims (unverified):** fillers, emotion transfer, code-switch MS/EN/ZH from mono-speaker reference
- **License:** CC-BY-NC-4.0 (non-commercial)
- **Downloads:** 0 as of 2026-08-14 — very new, no community validation yet
- **Malaysian-TTS-1.7B-v1**: Alternative TTS, DistilCodec-based, 290 downloads

## 2. YTL AI Labs — ILMU (Malaysia, corporate, government-backed)

- **ILMU**: Malaysia's first multimodal LLM, launched Aug 2025 by PM Anwar at ASEAN AI Summit
- Partnership with Universiti Malaya
- **ILMU-Nemo-30B**: Collaboration with NVIDIA (Mar 2026) — sovereign AI model
- **ILMU Claw**: Agentic platform (Apr 2026), works with OpenClaw. "Build autonomous AI agents through simple prompts"
- **Not open-source.** Hosted in Malaysia only.
- **HF presence:** nil (no model published on HuggingFace under ytl/ilmu)

## 3. SEA-LION (Singapore, AISG)

- **Full name:** Southeast Asian Language Intelligence for Nations
- Latest: SEA-LION v4.5 (2026)
- Base architectures: Gemma, Llama, Qwen (all fine-tuned for SEA)
- Sizes: 2B, 4B, 8B, 27B, 32B, 70B
- 11+ SEA languages including Bahasa Melayu
- Agentic-ready (v4.5+)
- SEA-Guard: safety-tuned for SEA cultural norms
- SEA-HELM: leaderboard for SEA language performance
- Free API + playground: https://playground.sea-lion.ai
- **1 trillion tokens trained on SEA languages**
- **Not Malaysian-owned** — Singapore, but closest regional ally for BM.

## 4. Sahabat-AI (Indonesia)

- Backed by GoTo (Gojek) and Indosat
- Models: 70B Llama, Gemma2-9B variants
- 116,950 downloads (Gemma2-9B-cpt-sahabatai-v1-instruct)
- Indonesian-first but supports BM as related language

## 5. Sailor2 (SAIL, Alibaba-affiliated)

- 1B, 8B, 20B sizes
- Multilingual SEA focus
- Lower community adoption (669 downloads max)

## 6. Malaysia Government Investment

- **RM2 billion** Sovereign AI Cloud (Budget 2026)
- **SAINS + INFINITIX MOU** (Jul 2026): Sarawak sovereign AI infrastructure
- **Strategic AI Infrastructure launch** (May 2025): "first in region to activate sovereign full-stack AI"
- Minister Gobind Singh Deo: "vigilant over DeepSeek, potential data security"
- **Gap:** investment is infrastructure (GPUs, data centers). Almost nothing into language layers (TTS, datasets, loghat).
- **NAIO** (National AI Office): Wikipedia article does not exist yet — institutional maturity still forming.

## 7. Gap Analysis for I-ARIF

| What exists | What's missing |
|---|---|
| Malaysian-Emilia dataset (15K hrs) | Voice cloning pipeline for Arif's own voice |
| ILMU multimodal LLM (closed) | Open-source Malaysian LLM with loghat understanding |
| SEA-LION v4.5 (open, free API) | Penang loghat in any model's training data |
| F5-TTS-v3 Malaysian | Voice design layer for non-standard registers |
| RM2b sovereign cloud | Zero allocation into language/voice sovereignty |
| Edge-TTS ms-MY (2 voices) | Any voice that sounds like a real Penang person |

The moat for I-ARIF remains: **data** (BM + Penang loghat + failure grammar as F1-F13 pairs), not compute.
