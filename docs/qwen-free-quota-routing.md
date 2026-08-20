# Qwen Cloud Free Quota — Federation Routing Guide

> **SOT for model routing. Every agent that touches Qwen models loads this.**
> **Forged:** 2026-08-20 · **Authority:** F13 · **Provider:** dashscope-payg (Singapore PAYG)
> **Endpoint:** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
> **API key:** `DASHSCOPE_API_KEY` (PAYG `sk-ws-H.*` — NEVER Token Plan `sk-sp-H.*`)

---

## Free Quota Rules (binding)

| Rule | Detail |
|---|---|
| **Per-model** | 1M tokens (input+output combined), independent per model |
| **Validity** | 90 days from activation or model release (whichever later) |
| **Key rule** | PAYG keys (`sk-ws-H.*`) consume free quota. Token Plan keys (`sk-sp-H.*`) bypass it |
| **Free Quota Only** | ENABLE in console — blocks calls when exhausted, no surprise charges |
| **Non-transferable** | Model A quota ≠ Model B quota. Exhausted = exhausted |
| **Expiry** | Hard expiry. Unused quota = void. No pause, no extension |

---

## Decision Flow

```
USER REQUEST
    │
    ├─ Text / Reasoning / Code ──────────→ TEXT RANKING (§1)
    │   └─ FED routes, FLAME fallbacks, FRAME observes
    │
    ├─ Image Understanding / OCR ────────→ VISION INPUT RANKING (§2)
    │
    ├─ Image Generation ─────────────────→ IMAGE OUTPUT RANKING (§3)
    │
    ├─ Video Generation ─────────────────→ VIDEO RANKING (§4)
    │
    ├─ TTS / Voice Synthesis ────────────→ TTS RANKING (§5)
    │
    ├─ ASR / Transcription ──────────────→ ASR RANKING (§6)
    │
    └─ Voice Clone / Design ─────────────→ VOICE IDENTITY RANKING (§7)
```

**Rule:** Always pick the HIGHEST quality model that has remaining free quota.
If exhausted → fall to next tier. If all free quota gone → PAYG billing.

---

## §1 — Text / Reasoning / Code (Quality Rank)

| Rank | Model | Input $/M | Output $/M | Context | Max Out | Use When |
|---|---|---|---|---|---|---|
| **Q1** | `qwen3.8-max` | $2.00 | $6.00 | 1M | 131K | Frontier reasoning, complex code, BM Penang fidelity, constitutional work |
| **Q2** | `qwen3.7-max` | $1.25 | $3.75 | 1M | 131K | General high-quality, good balance of cost/quality |
| **Q3** | `deepseek-v4-pro` | $0.66 | $1.98 | 1M | 393K | Long output tasks (reports, analysis), best cost/quality |
| **Q4** | `qwen3.7-plus` | $0.32-0.96 | $1.28-3.84 | 1M | 131K | Mid-tier, structured output, tool calling |
| **Q5** | `qwen3.7-flash` | $0.03-0.20 | $0.13-0.80 | 1M | 131K | High-volume, simple tasks, classification, routing |
| **Q6** | `qwen3.6-flash` | $0.25-1.00 | $1.50-4.00 | 1M | 65K | Fallback, longer context needed |

### Federation Role Mapping

| Federation System | Primary Model | Fallback | Why |
|---|---|---|---|
| **FED** (routing/LLM) | `qwen3.8-max` | `qwen3.7-max` → `deepseek-v4-pro` | FED needs frontier for accurate routing |
| **FLAME** (health/fallback) | `qwen3.7-flash` | `qwen3.6-flash` | FLAME does monitoring, not reasoning — speed over quality |
| **FRAME** (observer) | `qwen3.7-plus` | `qwen3.7-flash` | FRAME observes and reports — needs accuracy, not frontier |
| **666 JUDGE** | `qwen3.8-max` | `qwen3.7-max` | Constitutional verdicts demand highest quality |
| **999 SEAL** | `qwen3.8-max` | — | Irreversible — never cheap out |
| **i-ARIF** (persona) | `qwen3.8-max` | `MiniMax-M3` | BM Penang fidelity needs Qwen3.8 |
| **Hermes** (daily ops) | `qwen3.7-plus` | `qwen3.7-flash` | Telegram bot — balance quality vs latency |
| **OpenClaw** (edge) | `qwen3.7-flash` | `glm-5.3` | Edge agent — low latency critical |

### Reasoning / Thinking Models

| Rank | Model | Input $/M | Output $/M | Context | Use When |
|---|---|---|---|---|---|
| **Q1** | `qwq-plus` | $0.80 | $2.40 | 131K | Deep reasoning chains, math, logic |
| **Q2** | `qvq-max` | $1.20 | $4.80 | 131K | Visual reasoning (image + text chains) |

---

## §2 — Vision Input (Image Understanding) — Quality Rank

| Rank | Model | Input $/M | Output $/M | Context | Max Out | Use When |
|---|---|---|---|---|---|---|
| **Q1** | `qwen-vl-max` | $0.80 | $3.20 | 131K | 32K | Complex image analysis, document understanding, charts |
| **Q2** | `qwen3.5-omni-plus` | $1.40 | $8.30 | 262K | 65K | Multi-image + audio + video understanding (omni) |
| **Q3** | `qwen3-vl-plus` | $0.20-0.60 | $1.60-4.80 | 262K | 32K | Good vision, lower cost |
| **Q4** | `qwen-vl-ocr` | $0.07 | $0.16 | 38K | 8K | OCR specialist — documents, tables, receipts |
| **Q5** | `qwen3-vl-flash` | $0.05-0.12 | $0.40-0.96 | 262K | 32K | Fast vision, simple classification |
| **Q6** | `qwen3.5-omni-flash` | $0.43 | $1.66 | 262K | — | Quick omni (image+audio), lower cost |

### Vision Routing

| Task | Primary | Fallback |
|---|---|---|
| Complex image analysis | `qwen-vl-max` | `qwen3-vl-plus` |
| Document/OCR extraction | `qwen-vl-ocr` | `qwen3-omni-flash` |
| Face identification | `deterministic-face-id` (local dlib) | `qwen-vl-max` |
| Multi-modal (image+audio) | `qwen3.5-omni-plus` | `qwen3.5-omni-flash` |
| Quick classification | `qwen3-vl-flash` | `qwen3-vl-plus` |

---

## §3 — Image Generation — Quality Rank

| Rank | Model | Cost/Image | RPM | Use When |
|---|---|---|---|---|
| **Q1** | `qwen-image-3.0-pro` | $0.003-0.075 | 5 | Dense layouts, newspapers, menus, storyboards — highest fidelity |
| **Q2** | `qwen-image-max` | $0.075 | 2 | Flagship realism, photorealistic |
| **Q3** | `qwen-image-3.0` | $0.003-0.075 | 5 | Latest gen, 12-language text render, 4.5K tokens |
| **Q4** | `qwen-image-2.0-pro` | $0.075 | 2 | Full-feature accelerated |
| **Q5** | `z-image-turbo` | $0.015 | 120 | 6B params, 8-step, fastest — #1 on Artificial Analysis |
| **Q6** | `qwen-image-2.0` | $0.035 | 120 | Quick gen, 1000-token prompts |
| **Q7** | `wan2.7-image-pro` | $0.075 | 300 | Image editing via natural language |
| **Q8** | `wan2.6-t2i` | $0.03 | 300 | Older T2I, fast |

### Image Editing

| Rank | Model | Cost/Image | RPM | Use When |
|---|---|---|---|---|
| **Q1** | `qwen-image-edit-max` | $0.075 | 2 | Flagship editing, LoRA support |
| **Q2** | `qwen-image-edit-plus` | $0.03 | 120 | Lighter editing, faster |

### Image Routing

| Task | Primary | Fallback |
|---|---|---|
| High-fidelity generation | `qwen-image-3.0-pro` | `qwen-image-max` |
| Photorealistic | `qwen-image-max` | `qwen-image-3.0-pro` |
| Fast/cheap generation | `z-image-turbo` | `qwen-image-2.0` |
| Image editing | `qwen-image-edit-max` | `wan2.7-image-pro` |
| Text-in-image (multilingual) | `qwen-image-3.0` | `qwen-image-3.0-pro` |

---

## §4 — Video Generation — Quality Rank

| Rank | Model | Cost/Second | RPM | Max Duration | Use When |
|---|---|---|---|---|---|
| **Q1** | `wan3.0-video` | $0.05-0.20 | 50 | ~10s | **NEWEST** — dynamic transitions, best quality |
| **Q2** | `happyhorse-1.1-t2v` | $0.042-0.108 | 300 | ~10s | Realistic dynamic, fast RPM |
| **Q3** | `wan2.7-t2v-2026-06-12` | $0.10-0.15 | 300 | ~10s | Smooth motion, cinematic |
| **Q4** | `wan2.7-i2v-2026-04-25` | $0.10-0.15 | 300 | ~10s | Subject/text preservation from image |
| **Q5** | `wan2.7-r2v-2026-06-12` | $0.10-0.15 | 300 | ~10s | Multi-reference, preserves voice/look |
| **Q6** | `happyhorse-1.1-i2v` | $0.042-0.108 | 300 | ~10s | Fast i2v |

### Video Editing

| Rank | Model | Cost/Second | RPM | Use When |
|---|---|---|---|---|
| **Q1** | `wan2.7-videoedit` | $0.10-0.15 | 300 | Local/global editing, video reshaping |
| **Q2** | `happyhorse-1.0-video-edit` | $0.112-0.192 | 300 | Natural instruction video editing |
| **Q3** | `wan2.1-vace-plus` | $0.10 | 120 | Unified video editing |

### Video Routing

| Task | Primary | Fallback |
|---|---|---|
| Text-to-video (quality) | `wan3.0-video` | `wan2.7-t2v` |
| Text-to-video (speed) | `happyhorse-1.1-t2v` | `wan2.7-t2v` |
| Image-to-video | `wan2.7-i2v` | `happyhorse-1.1-i2v` |
| Reference-to-video | `wan2.7-r2v` | `happyhorse-1.1-r2v` |
| Video editing | `wan2.7-videoedit` | `happyhorse-1.0-video-edit` |

---

## §5 — TTS (Text-to-Speech) — Quality Rank

| Rank | Model | Cost/10K chars | RPM | Use When |
|---|---|---|---|---|
| **Q1** | `qwen-audio-3.0-realtime-plus` | $0.80/M input, $6.40/M output | — | **BEST** — full-duplex, top global evals, natural prosody |
| **Q2** | `qwen-audio-3.0-tts-flash` | $0.15/10K chars | 180 | Multilingual TTS, free-style instruction, production workhorse |
| **Q3** | `cosyvoice-v3-plus` | $0.26/10K chars | 180 | Generative TTS with text understanding |
| **Q4** | `qwen-audio-3.0-realtime-flash` | $0.45/M input, $4.50/M output | — | Fast realtime, lower quality than plus |
| **Q5** | `qwen3-tts-flash` | $0.10/10K chars | 180 | Budget TTS |

### TTS Routing

| Task | Primary | Fallback |
|---|---|---|
| i-ARIF voice output | `qwen-audio-3.0-realtime-plus` | `qwen-audio-3.0-tts-flash` |
| Telegram voice reply | `qwen-audio-3.0-tts-flash` | `edge ms-MY-OsmanNeural` (free) |
| High-fidelity narration | `qwen-audio-3.0-realtime-plus` | `cosyvoice-v3-plus` |
| Quick read-aloud | `qwen-audio-3.0-tts-flash` | `qwen3-tts-flash` |
| Voice cloning target | `qwen-audio-3.0-realtime-plus` | — |

---

## §6 — ASR (Speech-to-Text) — Quality Rank

| Rank | Model | Cost/Second | RPM | Use When |
|---|---|---|---|---|
| **Q1** | `qwen-audio-3.0-asr-flash-streaming` | $0.00009 | 1200 | Real-time ASR, live meetings, streaming |
| **Q2** | `qwen-audio-3.0-asr-flash` | $0.000035 | 600 | Short audio (<5min), high-quality transcription |
| **Q3** | `qwen-audio-3.0-asr-flash-filetrans` | $0.000035 | 600 | Long audio offline, meetings/calls, batch |
| **Q4** | `fun-asr-flash` | free | 600 | 7 major Chinese dialects, free |

### ASR Routing

| Task | Primary | Fallback |
|---|---|---|
| Live/streaming ASR | `qwen-audio-3.0-asr-flash-streaming` | `qwen-audio-3.0-asr-flash` |
| Short voice note (<5min) | `qwen-audio-3.0-asr-flash` | `fun-asr-flash` |
| Long audio/batch | `qwen-audio-3.0-asr-flash-filetrans` | `qwen-audio-3.0-asr-flash` |
| Chinese dialect audio | `fun-asr-flash` | `qwen-audio-3.0-asr-flash` |

**Note:** ASR models require per-model access enablement in workspace before first invocation.

---

## §7 — Voice Identity — Quality Rank

| Rank | Model | Cost | RPM | Use When |
|---|---|---|---|---|
| **Q1** | `voice-enrollment` | $0.01/voice | 180 | Zero-shot voice cloning from 10-20s sample |
| **Q2** | `qwen-voice-design` | $0.20/voice | 180 | Design voice from text description |

### Voice Identity Routing

| Task | Primary | Gate |
|---|---|---|
| i-ARIF voice clone | `voice-enrollment` | **F13 SOVEREIGN** — never auto-execute |
| New voice design | `qwen-voice-design` | F13 approval required |
| Voice clone + TTS pipeline | `voice-enrollment` → `qwen-audio-3.0-realtime-plus` | F13 |

---

## Free Quota Budget Planner

**Estimated free quota consumption per use case (1M tokens/model):**

| Use Case | Model | Est. Tokens/Use | Uses Before Exhaustion |
|---|---|---|---|
| LLM chat turn (complex) | `qwen3.8-max` | ~2K in + 1K out = 3K | ~333 turns |
| LLM chat turn (simple) | `qwen3.7-flash` | ~500 in + 200 out = 700 | ~1,428 turns |
| Image understanding | `qwen-vl-max` | ~1K in + 500 out = 1.5K | ~666 analyses |
| OCR extraction | `qwen-vl-ocr` | ~1K in + 1K out = 2K | ~500 extractions |
| Image generation | `qwen-image-3.0-pro` | ~4.5K tokens | ~222 images |
| TTS (1000 chars) | `qwen-audio-3.0-tts-flash` | $0.15/10K chars | ~6,666 pages |
| ASR (1 min audio) | `qwen-audio-3.0-asr-flash` | 60s × $0.000035 | ~476 minutes |

**Priority allocation for free quota:**
1. **qwen3.8-max** — highest value, consume first (constitutional work, i-ARIF)
2. **qwen-vl-max** — vision understanding, second priority
3. **qwen-image-3.0-pro** — image generation, third
4. **qwen-audio-3.0-tts-flash** — TTS, moderate use
5. **qwen-audio-3.0-asr-flash** — ASR, moderate use
6. **qwen3.7-flash** — high volume, low cost, stretch the quota

---

## Quick Reference Card (print this)

```
┌─────────────────────────────────────────────────────────────┐
│  QWEN FREE QUOTA ROUTING — AGENT QUICK REFERENCE           │
├──────────────────┬──────────────────────────────────────────┤
│ TEXT (best)      │ qwen3.8-max     → FED, JUDGE, SEAL     │
│ TEXT (mid)       │ qwen3.7-plus    → FRAME, Hermes         │
│ TEXT (cheap)     │ qwen3.7-flash   → FLAME, OpenClaw       │
│ TEXT (long out)  │ deepseek-v4-pro → reports, analysis     │
├──────────────────┼──────────────────────────────────────────┤
│ VISION (best)    │ qwen-vl-max     → complex analysis      │
│ VISION (omni)    │ qwen3.5-omni-plus → image+audio+video  │
│ OCR              │ qwen-vl-ocr     → documents, tables     │
│ VISION (fast)    │ qwen3-vl-flash  → classification        │
├──────────────────┼──────────────────────────────────────────┤
│ IMAGE GEN (best) │ qwen-image-3.0-pro → dense layouts     │
│ IMAGE GEN (photo)│ qwen-image-max  → photorealistic        │
│ IMAGE GEN (fast) │ z-image-turbo   → 8-step, 120 RPM      │
│ IMAGE EDIT       │ qwen-image-edit-max → LoRA, flagship   │
├──────────────────┼──────────────────────────────────────────┤
│ VIDEO (best)     │ wan3.0-video    → dynamic transitions   │
│ VIDEO (fast)     │ happyhorse-1.1-t2v → 300 RPM           │
│ VIDEO (i2v)      │ wan2.7-i2v      → subject preservation  │
│ VIDEO EDIT       │ wan2.7-videoedit → local/global edit    │
├──────────────────┼──────────────────────────────────────────┤
│ TTS (best)       │ qwen-audio-3.0-realtime-plus → natural │
│ TTS (workhorse)  │ qwen-audio-3.0-tts-flash → multilingual│
│ TTS (free)       │ edge ms-MY-OsmanNeural → Telegram      │
├──────────────────┼──────────────────────────────────────────┤
│ ASR (live)       │ qwen-audio-3.0-asr-flash-streaming     │
│ ASR (short)      │ qwen-audio-3.0-asr-flash               │
│ ASR (long)       │ qwen-audio-3.0-asr-flash-filetrans     │
├──────────────────┼──────────────────────────────────────────┤
│ VOICE CLONE      │ voice-enrollment (F13 SOVEREIGN gate)   │
│ VOICE DESIGN     │ qwen-voice-design (F13 gate)            │
└──────────────────┴──────────────────────────────────────────┘
```

---

## Constitutional Gates

| Modality | Gate | Rule |
|---|---|---|
| Text (constitutional) | 666 JUDGE | `qwen3.8-max` only — no downgrade |
| Text (seal) | 999 SEAL | `qwen3.8-max` only — irreversible |
| Voice clone creation | F13 SOVEREIGN | Manual approval required |
| Video generation (public) | F13 | Review before publish |
| Image generation (public) | F2 TRUTH | No fabrication, no deepfake |

---

*Forged: 2026-08-20 · F13 directive: "optimize it for the FED FLAME FRAME, rank by output quality"*
*Source pricing: Qwen Cloud pricing page (2026-08-20)*
*DITEMPA BUKAN DIBERI*
