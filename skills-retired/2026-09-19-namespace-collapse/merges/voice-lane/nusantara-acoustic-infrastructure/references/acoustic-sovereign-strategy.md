# Acoustic Sovereign Strategy — Malaysia Voice AI Landscape

Research synthesis 2026-08-14. Sources: HuggingFace API (live), ytlailabs.com, ilmu.ai, gotocompany.com press, sea-lion.ai, lowyat.net, theborneopost.com, mesolitica.com, Cartesia language pages, user-supplied 10-page strategy PDF (audited).

## The parallax

Malaysia's text layer is mature; the acoustic layer is bankrupt (foreign-dependent):
- **Compute:** MCMC Sovereign AI Cloud RM2B (Budget 2026); YTL-Nvidia Johor campus (500MW, GB200s — press figures conflict RM10B-RM20B, don't quote without primary source).
- **Text LLMs:** ILMU (YTL AI Labs + UM, Aug 2025, MalayMMLU 87.20 self-reported > GPT-4o 84.97 — EMNLP benchmark acceptance unverified, closed API, no third-party audit); MaLLaM 2.5 (mesolitica, open); Merdeka-LLM (Agmo, 57.28).
- **Voice:** everyone daily-hears Microsoft Edge-TTS OsmanNeural (baku, robotic). Cartesia (US) sells "Native Malay" voices (Faiz/Aisyah) before any sovereign alternative exists. mesolitica TTS family (0.6B→4B, F5 finetunes, Orpheus-3B) — 1.7B model has 290 downloads; dialect datasets 16-55 downloads. Kelantan phonetic data: zero.

## Verified numbers (HF API, 2026-08-14)

| Asset | Downloads | Meaning |
|---|---|---|
| mesolitica/Malaysian-TTS-0.6B-v1 | 12,001 | only adopted MY TTS |
| mesolitica/Malaysian-TTS-1.7B-v1 | 290 | flagship neglect |
| malaysia-ai/malaysian-dialects-audio | 55 | dialect data gap |
| Sarawak Malay speech corpus | 16 | near-zero |
| MERaLiON MNSC (SG) | 21,685 | what national funding does |
| mesolitica/Malaysian-Emilia-v2, whisper finetunes | — | active lab, no scale |

## Singapore benchmark (the blueprint)

IMDA National Speech Corpus → MERaLiON-AudioLLM (A*STAR + IMDA + AI Singapore): localized Whisper-large-v2 encoder + SEA-LION V3 decoder. WER 0.05 on local conversation (beats Qwen2-Audio, WavLLM). Deployed: scam-call interception, empathetic elderly check-ins. MNSC partitions: prompted readings (6k h), organic conversation (900 h), explicit code-switch (900 h), thematic/emotion (1.5k h), simulated sector phone calls (1.3k h) — table sums ~10.6k hours. The "260,000 hours" figure circulating in AI-generated reports is inflation; do not quote.

## Sarawak pattern (decentralized)

SAIC + FLock.io (UK): federated learning — model ships to edge devices, only weight updates return. Targets Iban, Bidayuh, Sarawak Malay + 40 hyper-local languages. Raw voice never leaves jurisdiction. Privacy-safe template for indigenous dialects.

## Falsification notes (from PDF audit)

The 10-page strategy PDF built on this session's research was 90% verifiable but contained: (1) 260k-hour NSC claim contradicting its own 10.6k partition table; (2) RM20B/1,640-acre/500MW YTL figures conflicting with press ($2.36B≈RM10B, phased USD5B); (3) unverified MalayMMLU EMNLP acceptance. Also flagged: PDF framed the micro-loop as "covert data harvester" — for Arif's own voice this is consent-clean (F13-sovereign-self), but any multi-user loop MUST be consent-labeled per speaker from day one (PDPA/F6).

## Macro blueprint (national, if drafting for MCMC/Ministry of Digital)

1. National Speech Corpus — 100k+ hours, all dialects (Northern/East Coast/Southern/Bornean), intentionally solicit code-switching, gamified gotong-royong via existing national app infrastructure.
2. Sovereign open-source TTS on the RM2B cloud — fund mesolitica/UM consortium; fine-tune F5-TTS/Orpheus; 3-5B params for low-latency inference; API for public+private.
3. Code-switching as first-class syntax — evaluation benchmarks penalize models that fail mid-sentence rojak transitions.

## Micro blueprint (i-ARIF loop — LIVE since 2026-08-14)

Voice-first Telegram loop where every interaction archives triads (.ogg + transcript + intent) = passive Penang dialect corpus at zero marginal cost. Captures prosody, failure grammar, hyper-local lexicon ("kambus"). 12 months → unassailable moat → fine-tune F5-TTS (single RTX 3090/4090, 12-24GB VRAM) when GPU access arrives. Corpus vault: /root/AAA/corpus/voice/. This is the thesis "data = moat, BM + Penang loghat, failure grammar" made operational.

## Watch list

- Groq free tier hosting Orpheus TTS (EN/AR only 2026-08) — Malay addition = free lane.
- Cartesia Sonic Malay (Faiz/Aisyah) — no key yet; naturalness benchmark to beat.
- mesolitica Malaysian-F5-TTS v3 — closest open sovereign baseline.
- Qwen qwen-audio-3.0-tts-plus — code-switch native.
