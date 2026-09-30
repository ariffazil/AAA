# F5-TTS offline clone lane — KVM8, no API key

**Status:** RUNNABLE (2026-09-29). Verified by rendering, not by reading.

## ⚠️ WIP — Malaysian finetune NOT sealed (F13, 2026-09-29)

**Do not use the Malaysian-Emilia finetune for the sovereign's voice.** Tested A/B against base, same reference and same
text (`ab_finetune_test.sh`; artifacts in `ab_test/`):

| | base `F5TTS_v1_Base` | `mesolitica/Malaysian-F5-TTS-v3` |
|---|---|---|
| BM intelligibility (ASR round-trip) | mangled: "pasal"→"pazal" ×3, lost "sembang"/"masih"/"ada" | 14/14 tokens, 2 spell-slips |
| MFCC cosine vs reference | 0.954 | 0.979 |
| **F0 (dominant spectral peak)** | **118 Hz** | **237 Hz** — reference is ~100 Hz |

The finetune renders roughly **an octave above the reference** (85 % of its voiced frames sit >180 Hz), so it does **not**
preserve speaker identity. It improves BM intelligibility *and* spectral envelope while destroying the voice.
**Verdict: WIP, not sealed.**

**Gate defect found (fix this regardless):** `voice_render_verify.py` scores MFCC cosine, which measures spectral-envelope
shape and is **blind to F0** — so it *passes* this finetune (0.979 > 0.954). Any TTS verification gate must compare F0
against the reference, not MFCC alone.

**Open question — CLOSED: it is the finetune, not the weights.** Non-EMA weights (`checkpoints/bm_v3_infer_noema.pt`,
rendered to `ab_test/v3_noema.wav`) are **worse**, not better:

| | raw-spectrum peak | pyin median | frames >180 Hz |
|---|---|---|---|
| reference | 99.6 Hz | 105.1 | 0 % |
| base | 118.4 Hz | 116.6 | 0 % |
| v3 EMA | 236.9 Hz | 252.8 | 85 % |
| v3 non-EMA | 253.0 Hz | 305.9 | 90 % |

Both weight sets sit roughly an octave above the reference. There is no flag that fixes this — the finetune does not
preserve speaker identity under this base config. **Parked as WIP.** Do not re-open without a new hypothesis (e.g. a
different base-config/vocab pairing), and do not spend a GPU budget on it before that.

## Checkpoints on disk

| File | Size | What |
|---|---|---|
| `checkpoints/bm_v3_220000.pt` | 5.39 GB | original HF training checkpoint (model + ema + optimizer + scheduler); sha256 verified against HF LFS oid `d4774d75…` |
| `checkpoints/bm_v3_infer_ema.pt` | 1.35 GB | EMA weights only — what the renders above used |
| `checkpoints/bm_v3_infer_noema.pt` | 1.35 GB | non-EMA weights, wrapped so f5-tts' ema path consumes them |

## Why this file exists
The lane was declared on 2026-08-26 (`/root/AAA/engines/f5tts_pipeline.sh`) but could not run:
the venv it sourced (`/root/venv`) does not exist, and `f5_tts` was installed in no interpreter
on this host. The 1.3 GB model weights were cached in `~/.cache/huggingface`. That is a ghost
capability — script present, capability absent.

## What runs now
```bash
cd /root/AAA/engines/f5tts
./venv/bin/python f5_local_render.py <ref.wav> "<ref transcript>" "<text to say>" <out.wav> [nfe_steps]
```
Env: `venv/` = python 3.14 + torch 2.11.0+cpu + torchaudio 2.11.0+cpu + f5-tts 1.1.22.
No network, no API key, no quota. 8 CPU, no GPU.

## Measured on KVM8 (2026-09-29)
| | MiniMax `speech-2.8-hd` (rented) | F5-TTS local (CPU) |
|---|---|---|
| time for ~8–9 s of speech | 5.7 s (24 s audio) | ~5.5 min (8.7 s audio) |
| realtime factor | ~4× faster than realtime | **~42× slower than realtime** |
| F0 median vs source | 123.5 Hz (−3.6 Hz) | 123.5 Hz (−3.6 Hz) |
| MFCC cosine vs source | 0.9938 | 0.9904 |
| ASR round-trip | clean, verbatim | clean; one slip (`bercakap`→`berkakap`) |
| needs API key / quota | yes | **no** |

Use: short offline clips, backstage, air-gapped work. Do NOT use for long letters — a 103 s
letter is ~70 min of CPU here.

## Two traps this lane hit (do not rediscover them)
1. **torchaudio ↔ TorchCodec ABI.** torchaudio ≥ 2.9 delegates decoding to TorchCodec, which is
   built against ONE exact torch build. Mixing torch 2.14 with torchaudio 2.11 (or removing
   torchcodec) makes `torchaudio.load()` raise at call time. Resolved by shimming
   `torchaudio.load` to soundfile inside `f5_local_render.py` — f5-tts only loads a local wav
   reference, so the shim is complete and version-proof.
2. **`f5tts_pipeline.sh` appends `"Ditempa bukan diberi."`** to every text it renders if absent.
   That is silent content injection into the artifact — the same failure class that got voice id
   `i-ARIF-V8` revoked (checkpoint inserted an unrequested clause). NOT changed here: it is the
   sovereign's own voice lane and the seal may be intentional. Flagged for F13.

## Verification
`/root/AAA/engines/voice_render_verify.py --audio X.ogg --text input.txt [--ref src.wav] --json`
Exit: 0 CLEAN · 1 CONTAMINATED · 2 TRUNCATED · 3 ERROR.
Truth-table tested both directions 2026-09-29: correct text → CLEAN; a deliberately wrong text
file → CONTAMINATED (219 suspicious tokens). ASR misspellings of Malay are filtered
(char similarity ≥ 0.72) so they do not read as injection.
