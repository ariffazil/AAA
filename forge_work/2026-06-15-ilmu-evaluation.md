# ILMU LLM — Evaluation
**Forged:** 2026-06-15 by FORGE (000Ω)
**Authority:** F13 SOVEREIGN — supplements (does not replace) Arif's F13 judgment
**Status:** DRAFT — substrate evidence + public claims, with explicit epistemic labels

## What the substrate actually says (OBS)

From `/root/.secrets/env/arifOS.env` and `/root/.secrets/env/arifOS-extra.env`:
- ILMU wired as **Tier 2 hosted fallback** for text generation (replaced Ollama for text-gen 2026-06-03)
- Endpoint: `https://api.ilmu.ai/v1` (OpenAI-compatible)
- Model: `ilmu-nemo-nano`
- Key path: `/root/.secrets/tokens/ilmu` (mode 600, F13)
- Per 888_HOLD: "ILMU as Tier 2 hosted fallback"
- **Ollama kept for bge-m3 embeddings only** — text-gen Tier 2 fully migrated to ILMU

From `/root/AAA/registries/model_soul.yaml`:
- id: `ilmu-nemo-nano`
- vendor: YTL ILMU
- role: HELD (not promoted to any production role)
- status: HELD
- soul: "Malaysian language context, 256k context"
- shadow: "Free tier rate limits, less battle-tested for production agentic loops"

**No ILMU soul file or shadow file exists in `/root/AAA/registries/models/`.** This is a gap — the model is in the master registry but has no detailed profile.

## Public claims (PLAUSIBLE → CLAIM ladder)

### Identity
- Full name: Intelek Luhur Malaysia Untukmu (Malaysian Intellect Integrity for You)
- Maker: YTL AI Labs (subsidiary of YTL Power International) + Universiti Malaya partnership
- Launch: Ogos 2025 at ASEAN AI Malaysia Summit 2025, graced by PM Anwar Ibrahim
- Origin story: started early 2023 as UM final-year project (3 students: Lawerence Chieng, Jeraelyn Tan, Jia Xuan) studying hallucination in ChatGPT, taken over by YTL AI Labs late 2023
- Hosted: 100% on YTL AI Cloud (data residency in Malaysia)
- **CLAIM level:** Identity claims are well-documented (multiple Malaysian news outlets, launch event covered). Higher CLAIM confidence than benchmark claims.

### Capabilities (per public launch materials)
- Multimodal: text, voice, vision
- Languages: Bahasa Melayu, Manglish, English, **Kelantanese dialect (Kelate)**
- Passed PT3 and SPM in Bahasa Melayu with A grade
- **MalayMMLU benchmark: 87.2%** — claimed to beat GPT-5, GPT-4o, DeepSeek-V3 on Malay
- Claimed on par with GPT-4o / Llama 3.1 on general global benchmarks
- IFEval: "neck-to-neck with GPT-4o"
- **CLAIM level:** These are **vendor-self-reported** with no independent verification. The MalayMMLU benchmark is one YTL/UM helped define → structural conflict of interest.

### Architecture (largely undisclosed)
- Parameter count: **NOT PUBLICLY DISCLOSED** by YTL as of 2026-06-15
- Base model: **PLAUSIBLE that it's a fine-tune of NVIDIA Nemo** (claim circulating in Malaysian tech community, not confirmed by YTL)
- Training data: composition not disclosed
- **CLAIM level:** Low. Architecture is opaque, which directly conflicts with F11 AUDITABILITY for any sovereign use case.

## What people say (external review)

### Positive
- Real Malay / Manglish / dialect fluency (PT3/SPM A-grade is a credible signal)
- Data residency — Petronas/Maybank/TNB can deploy without cross-border concerns
- Cultural reasoning — adat, maruah, hierarchy (claim, not independently verified)
- "Sovereign IP" — not a license of someone else's model (if true; see shadow)

### Negative / concerns
- **Vendor lock-in to YTL AI Cloud** — if you want sovereign AI but the only host is YTL, you have sovereign-AI-shaped-vendor-lock-in, not sovereign AI. This concern is in tension with the framing.
- **Opaque rate limits** — "free tier" framing but no public quota matrix
- **No published reasoning benchmarks** — MalayMMLU is the only public number; no GSM8K, MMLU, MATH, GPQA, SWE-Bench, τ-bench, IFBench numbers
- **Possible thin wrapper on Nemo/NVIDIA base** — if true, ILMU is a LoRA adapter on top of someone else's weights, which means the "sovereign IP" claim is partially hollow
- **"Harness macam anjing babi ada akta hasutan bagai"** (your phrasing) — the alignment/safety harness may be over-tuned for Malaysian political sensitivities, making it useless for legitimate research on those topics
- **No independent third-party evaluation** — no entry on Artificial Analysis, no HuggingFace OpenLLM leaderboard, no LMSYS arena presence (as of 2026-06-15)
- **Architecture not published** — F11 auditability is structurally blocked

## Honest evaluation (my read)

**ILMU has a real deployment niche but is oversold as a general-purpose Malaysian LLM.**

The real value proposition:
1. Malay/Manglish/Kelate dialect fluency (real, demonstrated)
2. Data residency (real, YTL AI Cloud)
3. Cultural reasoning for Malaysian context (claim, partially demonstrated)
4. Sovereign IP story (claim, depends on whether it's a fine-tune or built-from-scratch — undisclosed)

The real limitations:
1. Architecture is opaque → F11 auditability blocked → cannot be used for sovereign-critical paths where audit matters
2. No published reasoning benchmarks → cannot claim "good at math/coding/reasoning"
3. Vendor lock-in to YTL infrastructure → "sovereign" is conditional
4. Tight alignment harness → likely evades on sensitive topics in both directions (over-censors legitimate queries, possibly under-censors government-favored narratives)
5. No independent third-party evaluation → all claims are vendor-self-reported

## For arifOS specifically

The substrate treats ILMU as **Tier 2 fallback for text generation** — not as a primary. That's the right call given:
- Constitutional work needs F11 auditability (blocked)
- Agent loops need benchmark evidence (missing)
- Coding work needs SWE-bench numbers (missing)
- Primary paths are already covered (MiMo-V2.5-Pro for text, Kimi K2 for reasoning, Claude Sonnet for architecture)

**Where ILMU is genuinely useful in arifOS:**
- BM/Manglish text where the harness works (low-stakes comms, draft generation)
- Code-mixed queries where MiMo's BM is thin
- Workloads that need to stay in Malaysia for compliance
- Backup Tier 2 when MiMo token-plan-sgp has issues

**Where ILMU is NOT safe to use:**
- Any F1-F13 constitutional path (no F11 audit)
- Code generation requiring reliability (no SWE-Bench)
- Long-horizon agent work (no agentic benchmarks)
- Sovereign-critical decisions (architecture undisclosed → no audit)

## What I recommend

1. **Keep ILMU at HELD + Tier 2 fallback** — the substrate role is appropriate, no promotion
2. **Create the missing `/root/AAA/registries/models/ilmu_soul.yaml` and `ilmu_shadow.yaml`** — fill the registry gap with the substrate facts we have
3. **Don't add to the A/B test** — the promotion gate (Bar 4 = F11 audit) is structurally blocked; no point running the test
4. **Document the "sovereign IP vs vendor lock-in" tension** — it's the honest frame; pretending it's not there is the kind of F2 violation the trinity reports were guilty of

## On your "ILMU is scammer" framing

Too strong, but the concern is real. The right framing:
- **Not a scam** (real team, real product, real launch, real Malaysian-language capability)
- **Oversold** (sovereign IP claim is conditional; "beats GPT-5 on Malay" needs independent verification; architecture not disclosed)
- **Real deployment niche** (Tier 2 BM/Manglish fallback is a legitimate role)
- **Wrong for primary** (F11 audit, benchmark evidence, agentic track record all missing)

The "scammer" framing is rhetorically satisfying but loses the nuance. The "structurally constrained, oversold by launch PR, useful in narrow Tier 2 role" framing is closer to substrate truth.

---

*Forged by FORGE (000Ω) — DITEMPA BUKAN DIBERI*
