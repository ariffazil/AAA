---
id: nusantara-acoustic-infrastructure
name: nusantara-acoustic-infrastructure
version: 1.0.0
description: "Use when Nusantara voice AI: corpus, TTS, dialect strategy."
triggers:
  - "Malaysian voice AI"
  - "Bahasa Melayu TTS"
  - "dialect voice"
  - "acoustic deficit"
  - "corpus ingestion"
  - "rojak TTS"
  - "sovereign voice"
  - "voice loop data"
  - "Sahabat-AI"
  - "ILMU voice"
  - "F5-TTS"
  - "SEA-LION"
---

# Nusantara Acoustic Infrastructure

Addresses the "Acoustic Deficit"—the structural lack of localized, high-quality voice synthesis (TTS) and speech recognition (STT) for Bahasa Nusantara, despite mature text-layer LLMs (ILMU, MaLLaM, Sahabat-AI).

## The Core Problem
A nation can possess billions in GPU compute (MCMC Sovereign AI Cloud RM2B, YTL AI Cloud) yet remain "acoustically impoverished": compute is commoditized, localized labeled acoustic data is not. The "dapur tanpa beras" (kitchen without rice) paradigm. Text layer is settled; the voice layer is foreign-dependent (Edge-TTS OsmanNeural, Cartesia Sonic selling "Native Malay" voices Faiz/Aisyah back to Malaysia).

## The Infrastructure Pillars

### 1. Corpus Ingestion (Data Moat)
The bottleneck is clean, labeled audio for regional dialects (Penang, Kelantan, Sarawak) and natural code-switching (rojak). HF dialect datasets have <60 downloads — the gap is real.
*   **Vault:** `/root/AAA/corpus/voice/` — `raw/YYYY-MM/` + `meta/YYYY-MM/manifest.json`, sha-keyed entries.
*   **Protocol:** copy (never move — F1 reversible) from Hermes audio cache. Triad = `.ogg` + `transcript` + `meta` (speaker, dialect, consent, intent).
*   **Pitfall:** NEVER ingest agent-synthesized TTS into the human dialect corpus — synthetic feedback loop destroys authenticity. If an A/B sample lands in the cache, mark it `speaker: AGENT-OUTPUT, transcript_status: excluded` in the manifest (done once via post-ingest correction script).
*   **Consent labeling from day one:** `F13-sovereign-self` for Arif's own voice. If the loop ever serves other humans, corpus must be consent-labeled per speaker or it becomes a PDPA/F6 problem.

### 2. The Rojak Preprocessor (`/root/AAA/tools/voice/rojak_tts.py`)
Engine-level TTS cannot handle Malaysian code-switching or SMS shortforms. Five layers:
1.  **Markdown/emoji strip** — engines speak asterisks/backticks.
2.  **Shortform expansion** — "x"→"tak", "dlm"→"dalam".
3.  **Phonetic code-switch** — "deploy"→"deploi", "bug"→"bag" (how Malaysians actually say them).
4.  **Number/currency → BM words** — "RM2.5b"→"dua perpuluhan lima bilion ringgit", "15%"→"lima belas peratus".
5.  **Micro-prosody** — per-sentence rate variation (long sentences slower, questions up), 180ms inter-sentence pauses.

**CRITICAL LIMIT (user-verified 2026-08-14):** this layer changes WHAT the engine says, not HOW the engine sounds. User listened to raw vs rojak and said "still kinda the same" — correct: same OsmanNeural engine, same prosody ceiling. Text preprocessing is polish, not a voice transplant. Selling it as "the fix" overpromises; frame it as a preprocessor for ANY future engine.

### 3. Engine Ladder (TTS)
*   **edge-tts** (free, always alive): ms-MY-OsmanNeural / ms-MY-YasminNeural. Baku, robotic, zero loghat. Baseline only.
*   **MiniMax speech-2.8-hd** (Token Plan audio): voice design via `POST /v1/voice_design` — `prompt` (voice description) + `preview_text` (≤500 chars) + optional `voice_id` → returns custom `voice_id` + hex-encoded trial audio. A "Penang kaki" voice = one API call. Voice clone via `/v1/voice_clone` (needs `voice_id` param — bare file upload 400s). NOTE: audio features bill on a separate audio-subscription balance, NOT the general Token Plan quota — general quota can show 100% while TTS returns `1008 insufficient balance`.
*   **Qwen qwen-audio-3.0-tts-plus** (Token Plan seat, WebSocket `wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`): handles code-switch natively. Can die with `Throttling.AllocationQuota` across ALL seat keys simultaneously — retry next day, do not key-hop (violates sabar-retry).
*   **Cartesia Sonic**: commercial "Native Malay" (voices Faiz/Aisyah), no key on hand.
*   **F5-TTS / Orpheus finetune** (mesolitica Malaysian-F5-TTS v1-v3, Malaysian-orpheus-3b): the sovereign endgame — fine-tune on own dialect corpus; single RTX 3090/4090 class GPU (12-24GB VRAM) is enough. Requires the corpus from pillar 1.

### 4. STT (Ears)
*   **Groq whisper-large-v3-turbo** via curl multipart — proven transcriber for the corpus. Works with `language=ms` + a dialect `prompt` param ("loghat utara, campur English, hang, depa, kambus") which measurably improves Penang transcription.
*   **Pitfall:** Python urllib multipart gets HTTP 403 where identical curl passes — use subprocess curl for Groq audio uploads.

## Key Facts (verified 2026-08-14, HuggingFace API)
- Malaysia text LLMs: ILMU (YTL+UM, self-reported MalayMMLU 87.20 > GPT-4o 84.97 — unverified third-party), MaLLaM 2.5 (mesolitica), Merdeka-LLM (Agmo).
- mesolitica TTS family: Malaysian-TTS-0.6B (12k dl) / 1.7B (290 dl) / 4B, F5-TTS finetunes, Orpheus-3B — heroic, underfunded.
- Singapore benchmark: IMDA National Speech Corpus → MERaLiON-AudioLLM (21k downloads, WER 0.05 local). MNSC partition table sums ~10.6k hours; "260k hours" claims circulating are unverified inflation — do not quote.
- Sarawak SAIC + FLock.io: federated learning for Iban/Bidayuh/Sarawak Malay — raw audio never leaves device.
- Groq free tier hosts Orpheus TTS (English/Arabic only as of 2026-08) — watch for Malay addition.

## Macro strategy (if drafting national policy)
1. National Speech Corpus (100k+ hours, all dialects, gamified gotong-royong collection via existing national apps).
2. Sovereign open TTS on MCMC cloud — fund mesolitica/UM consortium, F5-TTS/Orpheus finetune, 3-5B params.
3. Code-switching as first-class syntax in evaluation benchmarks.

## Micro strategy (i-ARIF loop — proven live)
Every voice note in the Telegram loop = Penang dialect data at zero marginal cost. Ingest + transcribe triads accumulate the corpus nobody else has. 12 months of casual voice notes → proprietary dialect moat → fine-tune when GPU access arrives.

## References
- `references/acoustic-sovereign-strategy.md` — landscape numbers, Singapore/Sarawak patterns, macro/micro blueprint.
- `references/voice-loop-pipeline.md` — vault layout, tool contracts, API schemas, session transcript.
