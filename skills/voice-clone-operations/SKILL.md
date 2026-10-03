---
name: voice-clone-operations
description: "Use when rendering, verifying or judging a voice clone."
version: 1.0.0
author: Hermes Agent
license: arifOS
tags: [voice, tts, cloning, verification, delivery]
triggers:
  - render this in <person>'s voice / "jawab dalam voice X"
  - is this clone real, fake, good — eureka or biasa
  - voice note / TTS render request in any lane
  - voice with no API key / local offline voice
  - voice-registry cleanup, revoked voice_id, stale voice pointers
capability_tier: fed-realtime-voice
---

# Voice Clone Operations

## When to use

Any request that ends in an audio artifact of a voice: "render in X's voice", "reply in voice Y",
"is this clone real?", "can we do this without an API key?", or any cleanup of voice_ids and the
surfaces that name them. BM realism, provider lane tables and engine ceilings live in the external
`nusantara-voice-stack` skill; this skill is the **operating procedure around it**.

## Procedure

1. **Resolve the handle — never hardcode a provider id.** `/root/AAA/audio/voice-registry.json` is
   the resolver SOT: aliases → canonical key → `provider_voice_id`. Check `status` (a `REVOKED` id
   is never selectable, not even as a fallback) and `distribution` before rendering.
2. **Render through the pipeline, not a raw API call:**
   `bash /root/AAA/engines/iarif_tts_pipeline.sh <text-file> <out-path> "<handle>"`.
   Write the text to a file first. The pipeline resolves the handle, fails closed on revoked/unknown
   ids, strips TTS-poison markdown and bans constitutional clichés. **The output extension picks the
   container** — `.ogg` gives libopus 48 kbps/48 kHz mono, what Telegram renders as a real voice
   bubble (`[[audio_as_voice]]` + `MEDIA:` on their own lines).
3. **Verify before delivering.** For any cloned checkpoint: STT round-trip + `ffprobe` duration
   sanity. Divergence that changes words = re-render; duration near zero or far off the text length
   = silent truncation, re-render. Keyless option when the cloud ASR lane is unreachable: local
   `faster-whisper` (`small`, int8, CPU) — a floor, not a verdict (below).
4. **Deliver:** state engine, voice_id and duration in the message. When a fallback engine fired
   (edge/MiMo/local), say so explicitly — an unlabelled voice swap is a false witness, not a
   fidelity detail.
5. **Close the loop:** record what was rendered, with the artifact hash and the voice_id, where the
   lane keeps its receipts. For a *new clone* (not a re-render of an existing voice_id), a
   audit-grade JSON receipt is required — see the `clone-receipt-protocol` skill for the schema
   and the `/root/.hermes/storage/<owner>/<YYYY-MM-DD>/clone-receipts/` path. Casual re-renders
   of an existing voice_id don't need a new receipt; the original clone's receipt governs.

## Rules (always-on)

- **A `DISTRIBUTION_HOLD` governs publication, not synthesis.** When the registry marks a voice as
  demo-only (unconsented public figure), a direct render request from the principal IS authority to
  synthesise: render it, obey the registry's own `agent_rule` (say it is a demo, never present the
  clip as that person speaking, never publish), and deliver. An earlier audit that declined to render
  on hold grounds is not standing law — the hold blocks the outward path, not the local render.
- **Never mint a new clone without the principal's explicit word; a registered id is reused freely.**
  Per-render approval is not required for a voice that is already registered, and re-cloning an
  existing voice burns quota and adds drift.
- **Identity surfaces are the sovereign's.** The registry and capability docs an agent may repair;
  an identity card or charter that names a voice is F13-word territory — stage the line, state the
  failure class in one sentence, wait. Do not self-authorise an identity mutation.
- **Answer "is this eureka or biasa" with a verdict, not a hedge.** Cloning a voice is a commodity:
  ~10–30 s of clean single-speaker audio, one enrolment call, a render in seconds. Say that plainly.
  The non-obvious findings live in verification and governance, not in synthesis — e.g. a checkpoint
  you rent can emit content your own rules banned, which no input-side sanitizer can catch, so
  verification belongs at the output.
- **Judge with instruments, not adjectives:** measure the reference audio and the render, then
  compare f0 median, voiced ratio, pause distribution and tempo.

## Pitfalls

- **Stale pointers to a REVOKED voice_id outlive the revocation.** Grep the estate for the dead id
  and repair only the lines that declare *current state* (trigger tables, config examples, expected
  values, pipeline stage prose). Leave dated incident/scar records and archived reports untouched —
  retro-editing them destroys the provenance that makes the revocation auditable.
- **Clone fidelity is asymmetric: identity transfers, performance does not.** Measured source vs
  rented clone on the same text: f0 127.8 → 133.9 Hz (close) while voiced ratio went 0.359 → 0.736
  and pause median 418 → 255 ms. Pitch is copied; breath, hesitation and dynamics are not — that
  asymmetry is why a clone sounds like someone and still reads as synthetic.
- **`voiced_ratio` alone is not a synthetic-speech detector.** TTS lanes on the same pipeline span
  0.379–0.854, and source-vs-render comparisons on different text or register are suggestive only.
  Never present a one-sample DSP delta as a detector.
- **The measurement organ is interpreter-sensitive and fails closed.** `rasa_somatic_dsp.py` under an
  interpreter without numpy returns `ok: false` + `reason: "numpy unavailable"` with every field
  `NOT_MEASURED` — it reads like a broken file. Run it as
  `/usr/bin/python3 /root/scripts/rasa_somatic_dsp.py AUDIO > out.json` and parse stdout's JSON.
- **A small ASR model is a floor, not a verdict.** `faster-whisper small` mis-hears proper nouns
  (`Arif` → `Aris`), so name-level divergence from a small model is not evidence the lane is bad.
  Condemn a lane only when the reference lane also scores below threshold under the same model.
- **Do not declare a lane dead before inventory + alternate test.** Cached model weights and an
  installed package are independent facts — check both (`ls ~/.cache/huggingface/hub` *and* the
  interpreter's import list) before saying a capability is absent.

## Keyless / offline lane (no API key)

Use when the paid lane is dark (quota, missing key, network) or the principal asks for keyless work.
**Local is a fallback lane, never a replacement** — it is ~30× slower and rougher.

Installed vs cached are independent facts: `piper` is installed (fixed voices only, no BM, no
cloning), while `facebook/mms-tts-zlm` (generic offline Malay VITS) and `Systran/faster-whisper-*`
(verify gate) are cached weights, and `SWivid/F5-TTS` + `charactr/vocos-mel-24khz` give zero-shot
cloning with the package absent. Probe both surfaces before calling a lane dead.

Generic Malay (no clone), run with the torch-bearing system interpreter:

```python
import torch, soundfile as sf
from transformers import AutoTokenizer, VitsModel
torch.set_num_threads(8)
tok = AutoTokenizer.from_pretrained("facebook/mms-tts-zlm")
model = VitsModel.from_pretrained("facebook/mms-tts-zlm").eval()
with torch.no_grad():
    wav = model(**tok(TEXT, return_tensors="pt")).waveform[0].numpy()
sf.write(OUT_WAV, wav, model.config.sampling_rate)   # 16 kHz, CC-BY-NC-4.0
```

Local zero-shot clone — isolate the install, never into the interpreter the estate shares:

```bash
python3 -m venv --system-site-packages .venv && .venv/bin/pip install f5-tts
ffmpeg -i SOURCE -t 12 -ar 24000 -ac 1 ref.wav      # 10–15 s, one clean speaker
export HF_HUB_OFFLINE=1                             # use cached weights, no mid-run download
.venv/bin/f5-tts_infer-cli -m F5TTS_v1_Base \
  -r ref.wav -s "$(cat ref.txt)" -t "GEN TEXT" \
  -o out -w clone.wav --device cpu --nfe_step 16
```

The CLI needs a transcript of the reference clip — generate it with the local ASR rather than
hand-typing. `--nfe_step` is the speed/quality dial (16 ≈ fast and rough, 32 ≈ default).

Measured baselines (8 vCPU, no GPU — re-measure, do not quote): rented `t2a_v2` 6.4 s wall for
17.2 s of audio (0.37× realtime) · MMS-zlm 16.0 s for 7.5 s (2.1×) · F5-TTS 194 s wall (165 s
generate) for 5.1 s at `nfe_step 16` (~38×) · faster-whisper verify ~3 s. In the same A/B the local
clone's pitch was *closer* to the source than the rented clone's (122.8 vs 127.8 Hz source; rented
133.9 Hz) while intelligibility was poor — local wins on cost alone. Decision rule: rented lane
reachable → use it and do not "improve" a working lane; rented lane dark → local render **declared
as a fallback**; never present the generic local voice as a person's voice, it clones nobody.
