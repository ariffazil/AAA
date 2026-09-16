# Nusantara AI / Bahasa Melayu LLM & Voice Landscape

Knowledge bank from 2026-08-14 deep research (Arif: "Malaysia tak ada AI LLM sendiri, suara fake — how to solve"). Merged from two same-day research passes. All items verified against live sources (HF API, mesolitica.com, sea-lion.ai, ytlailabs.com, ilmu.ai, GoTo press release, Bernama via Bing News RSS). Re-verify staleness beyond ~6 months.

## The Real Gap (falsified premise)

The premise "Malaysia has no own LLM" is FALSE — three exist (ILMU, MaLLaM, Merdeka-LLM). What's missing is precise:
- **Voice layer**: all deployed ms-MY TTS (OsmanNeural-class) = formal baku, single studio speaker, no fillers, no code-switch. Sounds like a Jakarta newsreader, not a person. The "fake voice" complaint in one line.
- **Dialect layer**: ZERO dialect TTS (Penang/Kelantan/Sarawak). Dialect audio datasets are scraps: malaysia-ai/malaysian-dialects-audio (55 dl), Xiaoyangishere/sarawak-malay-speech-corpus (~16 dl). Kelantan: not found on HF.
- **Code-switch layer**: no shipped rojak BM-English synthesizer. Research exists (AsyncSwitch arXiv 2506.14190 — code-switched ASR; MDPI Malay-English CS studies) but no product.
- **Funding asymmetry**: RM2b sovereign AI budget (MCMC, Budget 2026) → infrastructure (GPU/datacenter), ~nothing → language/dialect layer. Singapore built corpus-FIRST (IMDA National Speech Corpus → MERaLiON, 21,685 dl), then models. Malaysia bought the oven, no rice.
- **Sovereignty irony**: Cartesia (US) launched "Native Malay" TTS (voices Faiz/Aisyah, cartesia.ai/languages/malay) before Malaysia has one. And Malaysia consumes Singapore's open Malay-capable SEA-LION models.

## Grassroots (the hidden champions) — Mesolitica

Small Malaysian lab (huseinzol05), no state funding. HuggingFace org: `mesolitica`.
- **MaLLaM** 🌙 — BM LLM family 1.1B–5B (`mesolitica/mallam-5b-20k-instructions-v2`), Mistral-template. MaLLaM 2.5 Small scored 71.53 on Malay MMLU (per ILMU's own comparison table).
- **Malaysian-Emilia** — 15,631h Malaysian voice dataset (`mesolitica/Malaysian-Emilia`, +v2, +annotated). THE corpus asset nobody funded.
- **Malaysian-F5-TTS-v3** (`mesolitica/Malaysian-F5-TTS-v3`) — full-param finetune of SWivid/F5-TTS on Emilia. THE key artifact: generates fillers ("erm","uhm"), transfers emotion from reference speaker, code-switches Malay/local English/Mandarin even from mono-speaker reference. License **CC-BY-NC-4.0** (non-commercial!). ~0 downloads at research time = unknown gem. Gradio infer via SWivid/F5-TTS repo + `hf://mesolitica/Malaysian-F5-TTS-v3/checkpoints/model_220000.pt`.
- **Malaysian-TTS-0.6B-v1** (12,001 dl — their most-adopted TTS), 1.7B-v1 (290 dl), 4B-v0.1 — LLM-style TTS (DistilCodec detokenizer, 24kHz, ms/en context switching). Also malay-parler-tts-mini/tiny, MeloTTS-MS, Malaysian-orpheus-3b-0.1-ft.
- **STT**: `mesolitica/wav2vec2-xls-r-300m-mixed` (760,931 dl — most-used artifact), Malaysian-whisper-large-v3-turbo-v3 (4,727 dl).
- **Dialect data**: `malaysia-ai/malaysian-dialects-youtube`, `malaysian-youtube`, `malaysian-cartoons-youtube`, `Multilingual-TTS`, `malaysia-ai/Qwen3-1.7B-Multilingual-TTS`, Podcast-Dia-1.6B.

## Corporate — ILMU (YTL AI Labs + NVIDIA)

- Aug 2025: ILMU ("Intelek Luhur Malaysia Untukmu") launched — first MY multimodal LLM, built with Universiti Malaya. Hosted 100% in Malaysia on YTL AI Cloud, PDPA-governed. ILMUchat: free + RM50/mo Pro (ilmu.ai), web/iOS/Android.
- Mar 2026: Ilmu-Nemo-30B with NVIDIA (sovereign AI). API for agent frameworks ("ILMU Claw Plan" — Nemo-Super / ILMU-Nemo-Nano, OpenClaw-compatible).
- Claims #1 Malay MMLU 87.20 vs GPT-4o 84.97, GPT-5 79.53, DeepSeek-V3 80.56, SahabatAI 78.31, SEA-LION 78.03, MaLLaM 2.5 71.53, Merdeka-LLM (Agmo) 57.28. **SELF-REPORTED on their own benchmark (github.com/UMxYTL-AI-Labs/MalayMMLU) — treat as marketing until independently reproduced.**
- Closed/proprietary. NOT open weights, NOT a voice layer.

## Government

- May 2025: Strategic AI Infrastructure launched (first in region, full-stack sovereign claim).
- Oct 2025 (Budget 2026): **RM2 billion Sovereign AI Cloud** — infra only.
- JPA circular (Oct 2025): all government-run programs must use BM fully — policy tailwind for BM-native AI.
- Sarawak: separate track — SAIC (Sarawak AI Centre), FLock.io sovereign AI partnership, SAINS + INFINITIX MOU (Jul 2026), AI blueprint targeted 2H2026.
- Compute: YTL AI Cloud = NVIDIA GPU datacentre in Johor (green-powered, ~$2.36B programme).

## Regional context (the benchmark Malaysia is judged against)

- **Sahabat-AI** (Indonesia, Indosat Ooredoo Hutchison + GoTo, launched 14 Nov 2024 at Indonesia AI Day): open-source 8B/9B on NVIDIA NeMo; Erick Thohir AND Jensen Huang on stage, VP Gibran endorsement, Golden Indonesia 2045 vision; universities (UI, UGM, ITB, IPB) + media (Kompas, Republika) contributing data; AI Singapore + Tech Mahindra support. gemma2-9b-cpt (117k dl) + Llama-Sahabat-AI-v2-70B. **Full national mobilization — the model Malaysia didn't build.**
- **SEA-LION v4.5** (AI Singapore): 1T SEA tokens, 11+ languages incl. Malay, agentic-ready, free API, GGUF/Ollama, SEA-Guard safety models, SEA-BED embedding benchmark, Project ATLAS data platform. Families: Qwen-SEA-LION-v4.5-27B-IT, Gemma-SEA-LION-v4.5-E2B, Llama-SEA-LION-v3.5-70B-R.
- **IMDA National Speech Corpus** (Singapore): MERaLiON/Multitask-National-Speech-Corpus-v1, 21,685 dl — seeded a national speech model. Malaysia has no equivalent.
- **Sailor2** (Alibaba SAIL): 1B–20B SEA models.
- Pattern: Indonesia and Singapore both built **corpus-first, compute-second**. Malaysia did compute-first, corpus-never.

## Solution shape (delivered to Arif)

No new base model needed. Missing = (1) **curated dialect corpus** (Penang/Kelantan/Sarawak + real rojak code-switch, ~100K hours nationally; gotong-royong collection) and (2) **product layer** (open national TTS = fine-tune F5/Orpheus-class 3B on corpus, hosted on MCMC sovereign cloud) and (3) **code-switch as first-class training signal**. This maps directly to Arif's data-moat thesis (I-ARIF: F1-F13 pairs, BM + Penang loghat, failure grammar).

**Fast experiment (sub-week, hundreds of RM not millions):** Runpod GPU → pull Malaysian-F5-TTS-v3 → 10s Penang voice sample as reference → gradio infer → listen. If pass → path open for I-ARIF voice layer that doesn't sound synthetic.

**Slow moat (i-ARIF voice loop):** every session (.ogg + transcript + intent, Penang loghat) = labeled dialect corpus the nation doesn't have. Structure collection now → 12-month head start. (Pending F13 GO as of session end.)

## Research transports that worked this session

web_search tool empty + SearXNG engines all suspended (DDG timeout / google CSE rate-limited / startpage CAPTCHA):
1. **Diagnose via SearXNG itself** — `curl "http://localhost:8080/search?q=test&format=json"` exposes `unresponsive_engines` with the reason per engine.
2. **Jina Reader wrapping DDG HTML** — `https://r.jina.ai/https://duckduckgo.com/html/?q=<urlencoded>` returns titles + `uddg=` links; works because the request originates from Jina's infra.
3. **Bing News RSS** — `https://www.bing.com/news/search?q=<query>&format=rss` returns clean XML (title/description/pubDate), immune to the CAPTCHA walls that block HTML SERPs. Best for news-shaped queries.
4. **HuggingFace API direct from VPS** — `https://huggingface.co/api/models?author=<org>&sort=downloads&direction=-1`, `?search=<term>`, datasets same pattern; READMEs at `https://huggingface.co/<repo>/raw/main/README.md`. Downloads count separates "exists" from "matters". Note: r.jina.ai proxy is domain-blocked for huggingface.co (403 AbuseAlleviation) but direct API works.
5. **Jina Reader** (`https://r.jina.ai/<url>`) for everything else (mesolitica.com, sea-lion.ai, ytlailabs.com, ilmu.ai, gotocompany.com all worked).
