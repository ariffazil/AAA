# LOCAL MALAY VOICE STACK — keyless clone + Gödel-lock witness chain
**Date:** 2026-09-29 · **Author:** HERMES (F13 DM lane) · **Trigger:** F13 — *"B still feel not Malay … deep research what resources / open-source repo or code needed to Gödel lock"*
**Status:** RESEARCH (not sealed) · **Scope:** run voice synthesis + cloning + verification with **no external API key**

---

## 0. Measured starting point (this host, today)

| Test | Engine | Wall clock | Audio | Notes |
|---|---|---|---|---|
| A | MiniMax `anwar-bm-20260927` (API key required) | 6.4 s | 17.2 s | pitch 133.9 Hz; intelligible |
| B | F5-TTS v1 Base, local, 12 s reference | **165 s generate / 194 s total** | 5.1 s | pitch **122.8 Hz** (closer to source 127.8 Hz) but **unintelligible**: ASR read *"…bukan soljuat dan isolamana"* |
| C | MMS-TTS-zlm (`facebook/mms-tts-zlm`), local, generic voice, no clone | 16.0 s | 7.5 s | 16 kHz; ASR read *"Saudara Aris"* |

Host: 8 vCPU · 31 GB RAM · **no GPU** · 106 GB free disk.
Measured reference properties (PMX RTM 5 Dec 2022, 29.913 s): f0 127.8 Hz, voiced_ratio 0.359, pause median 418 ms.

**Diagnosis of "B bukan Melayu":** the base checkpoint was trained on **English + Chinese (Emilia)**. Malay is out-of-distribution → phoneme inventory and prosody default to the training languages. Pitch transfers, *phonotactics do not*. Reference quality compounds it: 12 s clip + ASR-derived reference text (two ASR errors in 3 sentences).
→ This is a **model-language problem**, not a prompt problem.

---

## 1. Open-source candidates (ranked for keyless Malay)

| Rank | Project | Repo | Licence | Malay? | Clone from | Notes |
|---|---|---|---|---|---|---|
| 1 | **Chatterbox Multilingual** (Resemble AI) | `ResembleAI/chatterbox` | **MIT** (code + weights) | **Yes — 1 of 23 out-of-box** | zero-shot, few-sec ref | Ships **PerTh watermark** (synthetic provenance embedded in the audio) — directly relevant to the witness chain. CPU-capable, slower than GPU. |
| 2 | **GPT-SoVITS v3/v4** (RVC-Boss) | `RVC-Boss/GPT-SoVITS` | **MIT** | via fine-tune (community MS/ID models exist) | 5 s zero-shot; **~1 min fine-tune** | Most-starred open TTS (~60k). Full toolchain included: audio slicing, ASR labelling, training, WebUI. Cheapest route to a *Malay-native* voice. |
| 3 | **CosyVoice 2 / Fun-CosyVoice3** (Alibaba FunAudioLLM) | `QwenAudio/CosyVoice` | **Apache-2.0** | not official; strong cross-lingual | zero-shot | Same family already used via Qwen Cloud for the PMX trial — local weights exist. |
| 4 | **F5-TTS** (SWivid) | `SWivid/F5-TTS` | code **MIT** but **checkpoints CC-BY-NC-4.0** (Emilia) | via fine-tune | 5–15 s zero-shot | Fine-tune needs 12–24 GB VRAM (LoRA verified at 24 GB); 10–60 min of data. Non-commercial weights — fine for internal, blocking for product. |
| 5 | **XTTS-v2** (Coqui) | `coqui-ai/TTS` | CPML (non-commercial) | 17 langs, no Malay | 6 s | Project dormant. Not recommended. |
| 6 | **MMS-TTS-zlm** (Meta) | `facebook/mms-tts-zlm` | CC-BY-NC-4.0 | **Yes (official)** | ✗ no cloning | Already installed & working (test C). Robotic; keep as the *phonetic ground truth*, not as the product. |
| 7 | **Piper** | `rhasspy/piper` | MIT | no official `ms_MY` voice | ✗ | Fast, tiny, CPU-first. Useful only for non-cloned canned prompts. |

**Training data (open, for a Malay-native base):**
- **Malaya-Speech** (`huseinzol05/malaya-speech`) — Malaysian speech toolkit + corpora, **CC-BY 4.0** for research; includes GlowTTS/VITS recipes.
- **Common Voice `ms`** (Mozilla) — CC0.
- **FLEURS `ms`** (Google) — CC-BY-4.0, ~10 h read speech.
- **ASR-MalCSC** (MagicHub) — 5 h conversational Malay, transcripts included.
- Mesolitica Malaysian Whisper fine-tunes — for **forced alignment / labelling** of any new corpus (needed before training).

---

## 2. Hardware & cost

| Task | Requirement | This host | Cost |
|---|---|---|---|
| Local **inference** (Chatterbox / F5) | CPU ok, 8 GB+ RAM | ✅ works, ~30–40× realtime | $0 |
| **Fine-tune** Malay (GPT-SoVITS 1–10 min data) | 8–12 GB VRAM | ❌ no GPU | Runpod RTX 3090 ≈ **$0.19/hr** → 2–4 h |
| **Fine-tune** F5-TTS LoRA (10–60 min data) | 16–24 GB VRAM | ❌ | A6000 ≈ $0.82/hr → 3–6 h |
| Malay base from scratch (5–20 h data) | 24 GB+, days | ❌ | not recommended for now |

---

## 3. Gödel lock — what it actually means here

Canon: `/root/AAA/canon/GODEL_LOCK.md` — *"a constitutional agent reasoning about its own constitutional compliance will always encounter at least one judgment it cannot fully verify from inside itself. Self-audit is structurally incomplete."* Enforcement stub: `/root/AAA/contracts/godel_lock_enforcement.py`, `/root/AAA/contracts/APEX_GODEL_LOCK.yaml`.

Translated to voice: **a render may not certify a render.** The generator is inside the loop; the verdict must come from outside it.

| # | Witness in the chain | Independent of generator? | Status today |
|---|---|---|---|
| 1 | Voice registry + fail-closed resolver (`AAA/audio/voice-registry.json`, `iarif_tts_pipeline.sh`) | ✅ | **LIVE** — proven to refuse the revoked V8 checkpoint |
| 2 | Content witness — ASR diff (no INSERTED words) | ✅ | LIVE but **key-dependent** (Groq). Keyless replacement: `faster-whisper` (MIT, cached locally, measured 3.0 s / 7.5 s audio) |
| 3 | **Speaker witness** — is the output really the claimed speaker? | ✅ | **MISSING.** Today: ad-hoc f0 / MFCC cosine. Repo needed: `speechbrain` ECAPA-TDNN (`speechbrain/spkrec-ecapa-voxceleb`, Apache-2.0) or `3D-Speaker` (Apache-2.0) → cosine score + calibrated threshold |
| 4 | **Provenance watermark** — mark + verify synthetic audio | ✅ | **MISSING.** Repo: PerTh (inside Chatterbox, MIT) or **AudioSeal** (Meta, MIT) → embed + detect |
| 5 | Hash receipt → VAULT999 | ✅ | LIVE (CHC / blake3) |
| 6 | Enforcement at runtime (not a document) | — | **PARTIAL.** Pipeline gate = runtime. `distribution: DISTRIBUTION_HOLD` = document with **0 consumers** (measured) |

**The two things actually worth coding:** (3) speaker witness and (4) watermark verify — then bind (2)+(3)+(4)+(5) into one fail-closed script that runs **before** any delivery. Home for it: `AAA/skills/voice-render-verification/` (created 2026-09-29).

---

## 4. Recommended sequence (non-breaking)

1. **Clean-reference re-test** (30 min, CPU-only): correct reference transcript + `nfe_step 32` → quantify whether the fault is the reference or the model. Cheap falsification.
2. **Chatterbox Multilingual trial** in a **separate venv** (`/root/forge_work/local-voice/.venv-chatterbox`) → same BM sentence, measure WER + f0 + wall clock. MIT + Malay + watermark makes it the best keyless candidate.
3. If quality still short: **GPT-SoVITS few-shot fine-tune** on 1–10 min of Malay (Runpod GPU, few hours). Cheapest path to a genuinely Malay-native voice.
4. **Gödel witness chain**: ECAPA speaker-verify + local ASR diff + per-file hash → single pass/fail gate on the render-verification skill.

**Nothing in the existing MiniMax lane is modified by any step above.** Local lanes stay fallback-only until a local render beats 6.4 s + intelligible.

---

*Sources: local measurements (this host, 2026-09-29); project repos & model cards cited inline; licence claims taken from upstream repo/README/HF model cards and marked as vendor-declared. Not independently verified against licence text.*
