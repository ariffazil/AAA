---
id: sovereign-tts-lanes
name: sovereign-tts-lanes
description: "Use when TTS must run offline without a cloud provider."
version: 1.0.0
author: hermes
license: arifOS
tags: [tts, sovereign, offline, malay, piper, mms, onnx, cpu]
metadata:
  hermes:
    tags: [audio, tts, sovereign, offline]
    related: [nusantara-voice-stack, hermes-voice-config, audio-roundtrip-diagnostics]
    forged: 2026-09-18
    provenance: "All rows measured live on KVM8 (forge) 2026-09-18. Each engine rendered the identical test line; round-trip via Groq Whisper language=ms; f0 via librosa yin."
triggers:
  - cloud TTS quota exhausted and a voice is still needed
  - TTS must work offline / without a provider
  - MiniMax 2056 / balance error blocks delivery
  - Malay or BM text needs speech on CPU only
  - evaluating Piper, MMS-TTS, F5-TTS for Malay
---

# Sovereign TTS Lanes

## 0b. WHY THIS LANE EXISTS — the cap it covers (measured 2026-09-18)

Do not read a MiniMax `2056` as "weekly quota gone". The Token Plan caps `general` TWICE:

```bash
mmx quota show --base-url https://api.minimax.io
# general: current_interval_status 2 = EXHAUSTED  ← 4-HOUR window
#          current_weekly_status   1 = open, current_weekly_remaining_percent N
# video  : separate bucket (3 / 24 h, 21 / week)
```

Measured live: interval 0 %, **weekly 36 % with 3 days left**. The lane went quiet on a
4-hour cap while a third of the week sat unused. That is the failure this skill covers.

**`general` serves BOTH `image_generation` and `t2a_v2`** — both endpoints returned the same
2056 at the same instant. Images spend the voice allowance. `video` is the only separate
bucket. Model choice is irrelevant: `speech-2.8-hd`, `-turbo`, `2.6-*`, `02-*` and
`2.5-hd-preview` all return 2056 identically, so the cap is account-level.

**Allocation rule:** *draft sovereign, seal rented.* Iterate wording and pacing on Piper — it
costs nothing and never runs out. Make every metered render the final take.

**Probe the lane before spending it:**
```bash
bash /root/AAA/engines/tts_lane_status.sh          # human; exit 3 = Tier 1 shut, use Piper
bash /root/AAA/engines/tts_lane_status.sh --json
```

### Wired into the live pipeline

`/root/AAA/engines/iarif_tts_pipeline.sh` failover chain (repaired 2026-09-18):

```
MiniMax (Tier 1, rented) → PIPER (sovereign, offline, zero-quota) → edge-tts → MiMo (last resort)
```

The rung below MiniMax used to be MiMo, which is falsified for BM — so the first fallback
silently shipped mangled speech in a different voice. Every rung now writes `IARIF_ENGINE=` to
stderr so the delivery message can name what actually spoke.

Override points: `IARIF_PIPER_BIN` (default `/usr/local/bin/piper`),
`IARIF_PIPER_MODEL` (default `/root/forge_work/piper-sovereign/id_voice.onnx`).

## When to Use

Load when a voice note is needed but the cloud lane is dead (quota, balance, network), or when the requirement is "this must not depend on a rented voice".

## 0. INVENTORY FIRST — the phantom-absence trap

**Two complete offline TTS stacks were already installed and were declared missing** because the probe checked `/usr/bin/python3` and `/root/venv` only, found no `torch`, and concluded "not available".

The workspace sweeps that matter:

```bash
# find EVERY venv, do not stop at the first
for p in /opt/arifos/venv/bin/python3 /root/GEOX/.venv/bin/python /usr/bin/python3; do
  [ -x "$p" ] && echo "--- $p" && $p -c "
import importlib
for m in ['torch','transformers','onnxruntime','piper','soundfile','librosa']:
    try: importlib.import_module(m); print('  ',m,'OK')
    except Exception: print('  ',m,'MISSING')" 2>/dev/null
done
# and binaries
which piper edge-tts
ls /usr/local/bin/piper 2>/dev/null
```

**Measured state (KVM8, 2026-09-18):** `/opt/arifos/venv` carries `torch 2.14.0+cu130`, `transformers`, `onnxruntime 1.28.0`, `soundfile`. `/usr/local/bin/piper` is `piper_tts-1.8.0`, installed 2026-09-09 — nine days unseen.

**Rule:** a capability may only be declared down after the inventory sweep AND an alternate-lane test. A venv you did not open is not absence.

## 1. The three lanes — MEASURED, identical test line

Test text: `"Aku tak tahu nak cakap apa. Tapi aku masih sini."`

| Lane | Engine | Voice | Round-trip | f0 | Latency | Size | License |
|---|---|---|---|---|---|---|---|
| **Piper** | ONNX VITS | `id_ID-news_tts-medium` | 91% (`nak`→`na`) | 260.5 Hz | **1.3–1.8 s** | 63 MB | **MIT** |
| **F5-TTS** | PyTorch | any reference | not run | — | ~5 min | — | MIT |
| ~~MMS-TTS-zlm~~ | ~~PyTorch VITS~~ | ~~native Malay~~ | *removed* | — | — | — | *CC-BY-NC* |

### MMS-TTS-zlm — EVALUATED AND REMOVED (2026-09-18)

**Do not re-propose this lane without an F13 decision.** It was built, measured, and then removed.

What it was: `facebook/mms-tts-zlm`, VITS, 36.3M params, 145 MB, 16 kHz. `zlm` = Malay specifically
(not Indonesian). Measured **100% round-trip** on the short line — the best pronunciation of any
sovereign lane tested.

**Why it was removed:**

1. **License `cc-by-nc-4.0` — NON-COMMERCIAL.** Load-bearing. The fleet does employer work; a
   lane that cannot touch commercial output is a footgun, not a capability. Piper is MIT and
   renders in 1.3 s — the marginal pronunciation gain did not justify carrying a licence risk
   that has to be re-evaluated at every render.
2. **f0 222–225 Hz** — female register. Unusable for the persona lane regardless.
3. **No emotion contour.** It reads flat. Where MiniMax carries `penat` / `lembut` through pacing,
   MMS states the words evenly. For a line like "Abang penat" it loses.
4. **16 kHz** — half of MiniMax's 32 kHz, audibly thinner.

**Teardown receipt:** `/root/forge_work/piper-sovereign/mms_teardown.py` — removed the demo pack,
probe scripts, 4 sample files, the stray `mms-tts` work dir, and the 139 MB HF model cache.
Verified clean: no `*mms-tts-zlm*` path remains under `/root` or `/opt`.

**Rejected-lane rule:** a capability that was measured and then deliberately removed is *knowledge*,
not a gap. Record WHY it was removed so a later session does not spend a cycle rediscovering it.
Keep the finding; delete the artifact.

### Piper — fastest, MIT, no native Malay voice

Piper's library has **54 languages and NO `ms`**. Verified live:
```
HTTP 404  .../rhasspy/piper-voices/resolve/main/ms/ms_MY/
{"error":"ms does not exist on \"main\""}
```
SEA languages present: `id`, `ja`, `ko`, `th`, `vi`, `zh`.

Use **Indonesian** — it reads BM natively (same phoneme-overlap principle as the MiniMax Indonesian voices).

```bash
D=/root/forge_work/piper-sovereign
B="https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium"
curl -sL "$B/id_ID-news_tts-medium.onnx"      -o $D/id_voice.onnx
curl -sL "$B/id_ID-news_tts-medium.onnx.json" -o $D/id_voice.onnx.json
echo "Aku tak tahu nak cakap apa." | /usr/local/bin/piper -m $D/id_voice.onnx -f out.wav
```
Tuning: `--length-scale` (pace, >1 slower), `--noise-scale`, `--noise-w-scale`, `--sentence-silence`.

**Known defect: `nak` → `na`.** One phoneme. Not yet fixed; consider pre-normalising the token or a different Indonesian voice.

### MMS-TTS-zlm — REMOVED. See §1 for the teardown record.

Do not re-propose. The finding is retained; the artifact is deleted.

### F5-TTS — the clone path

Reference audio staged at `/root/AAA/engines/f5tts/reference.wav` (24.8 s) and `reference-10s.wav`.
Module **not installed in any venv**. ~4–5 min per utterance on CPU.

**The only offline path that clones a specific voice.** Too slow for production; correct for sovereignty-critical work.

## 2. Why this matters more than wiring a DSP pipeline

Wiring DSP (soul-envelope, WORLD stabilizer) across a cloud voice polishes a rented asset. Piper renders Malay-adjacent speech in **1.3 s on CPU, MIT, zero network, zero quota**.

| Failure | Rented voice | Sovereign lane |
|---|---|---|
| Provider quota exhausted | silence | lane switch |
| Provider changes terms | silence | unaffected |
| Network down | silence | unaffected |
| Cost per render | non-zero | zero |

**Do not propose pipeline improvements around a provider without first asking why the provider is needed at all.**

## 3. Tier restructure (proposed)

| Tier | Voice | Engine | Sovereignty |
|---|---|---|---|
| 1 | Siti Nurhaliza (i-ARIF) | MiniMax `iarif-sovereign-v9` | rented |
| 2 | Abang Sado persona | MiniMax `abang-sado-live-v1` | rented (own voice) |
| 3 | Indonesian BM | MiniMax `Indonesian_*` | rented |
| **4** | **Sovereign-fast** | **Piper `id_ID-news_tts`** | **OWNED · MIT** |
| 5 | Clone | F5-TTS | OWNED |

MMS-TTS-zlm was proposed as Tier 5 and **removed 2026-09-18** (non-commercial licence). Tier 4 is the
only offline lane currently in service.

## 4. The CTC second witness — check for it before claiming it is missing

Two Whisper engines share a training prior, so their agreement is **not independent confirmation** — on pure noise both return the same fictitious Malay sentence. Absence and attribution claims need an architecture-independent witness; a **CTC** model cannot autoregressively invent fluent speech over non-speech.

**One was already on disk**, staged 2026-09-15, unused for three days:

```
/root/audio-lane-2026-09-15/mms-1b-all/
├── onnx/model_int8.onnx     970 MB
├── vocab.json  ├── tokenizer.json  ├── config.json
└── preprocessor_config.json
```

Probed live — `inputs: ['input_values']`, `outputs: [(1, 221, 154)]`, **GRAPH INVOCABLE** via `onnxruntime` CPUExecutionProvider. The language-adapter decode step is not yet wired; the checkpoint loads and runs.

**Run this probe before any absence claim on audio.**

## 5. Pitfalls

- **`/opt/arifos/venv` has a cffi version mismatch** (2.1.1 API vs 2.1.0 `_cffi_backend`), which breaks `librosa` import there. Use system `python3` for librosa, `/opt/arifos/venv/bin/python3` for torch/transformers.
- **MiniMax `status 2056`** = Token Plan weekly quota, NOT an auth failure. The key is valid. Resets weekly.
- **`--base-url https://api.minimax.io` is required** for all `mmx` media commands; the default points at `/anthropic` and 404s.
- **Piper needs its `.onnx.json` beside the `.onnx`** — the model alone fails.
- **MiMo `mimo-v2.5-tts-voiceclone` captures MALE REGISTER (f0 182.9 Hz from a male reference) but mangles BM pronunciation** — measured transcript `"Hawekaku tatoa nō kakaapa, taipi akumasi sini."` for source `"Aku tak tahu nak cakap apa. Tapi aku masih sini."` The base `mimo_default` is also female-register (230.6 Hz) and merges words (`nak cakap`→`nakakap`). **MiMo is not a BM lane at any variant.** The turbo Whisper engine returns the non-speech boilerplate on the clone output — the §12 signature.

DITEMPA BUKAN DIBERI — a voice you rent is a voice you can lose.