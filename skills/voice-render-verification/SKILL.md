---
name: voice-render-verification
description: "Use when a voice render must be verified before delivery."
version: 1.0.0
author: Hermes
license: arifOS
metadata:
  hermes:
    category: audio
    tags: [tts, voice-clone, verification, asr, audio-integrity]
    related_skills: [hermes-voice-config, nusantara-voice-stack, persona-voice-binding, rendered-artifact-verification]
triggers:
  - a voice note, cloned-voice clip, or TTS render is about to be delivered
  - a TTS pipeline returned success and you need to know whether the artifact is actually right
  - "is this the right voice / is this really 99% the same voice"
  - an engine may have injected words the caller never wrote
  - a clone lane must be shown to work before it is cited as working
---

# Voice Render Verification

A render that returns HTTP 200 is not a render that is correct. This skill is the proof step between
"the pipeline said ok" and "this file leaves the house".

Rendering procedure, engine selection and voice governance live in the voice-stack skills. This skill
owns the gate: what to measure, in what order, and which verdicts are real.

## 1. Verify with a script, not with memory

```bash
python3 /root/AAA/engines/voice_render_verify.py \
    --audio out.ogg --text input.txt [--ref enrolment_source.wav] [--json] [--strict]
```

Exit codes are the contract: `0 CLEAN · 1 CONTAMINATED · 2 TRUNCATED · 3 ERROR`.
`3` means *could not verify* (no ASR key, transcription refused) — never a pass. A report that hides a
failed verification behind a zero exit is a false witness.

It shells `ffprobe` for duration and `curl` for the transcript, so the integrity half needs no python
audio stack; the `--ref` identity half needs `librosa` (run it with a venv that has one).

The verifier **reports**; it does not rewrite or block a live delivery path by itself. Wiring it into a
shipping pipeline is a governance decision — say what you changed and what you deliberately left alone.

## 2. Diff against what the pipeline SENT, not the file you handed it

Lanes post-process text by design (an audio seal, a signature line, markdown stripping). A naive
transcript diff reads that as an insertion and calls a correct render contaminated.

- Read the lane's text handling before trusting any diff.
- If the appended content is deliberate canon, compare against the post-normalisation text. If it is a
  defect (the lane emitting words nobody wrote), report it to the principal and let the lane owner
  decide — do not silently remove it.

## 3. An insertion is a RUN of foreign tokens, not a misspelled token

Malay ASR writes phonetic neighbours of real words (`bersandar`→`bersanda`, `baring`→`bari`,
`Abang Sado`→`bang sadu`, `bercakap`→`berkakap`). On a correct long render a verbatim token diff
misfires several "extra" tokens and returns a false CONTAMINATED — which trains you to ignore the gate.

Rule: count an extra token as **suspicious** only when it is not char-similar to any expected token in
its neighbourhood — `difflib.SequenceMatcher(a=tok, b=expected, autojunk=False).ratio() < 0.72` over a
±3-token window. A clause nobody wrote is a run of foreign words and survives that filter. Default:
≥2 suspicious tokens = CONTAMINATED; `--strict` makes it 1. **Always pass `autojunk=False`** — the
default heuristic corrupts similarity on short strings.

## 4. Truth-table the verifier before citing it

1. Correct render + its own input text → expect `CLEAN` (exit 0).
2. Same render + a deliberately unrelated text file → expect `CONTAMINATED` (exit 1, similarity collapses
   to ~0.05 with ~200 suspicious tokens).

A verifier that has never failed on known-bad input has not been shown to measure anything. Run both
cases whenever the script or its thresholds change.

## 5. Duration floor — silence is a failure, not a terse take

`floor = max(0.4 × (chars / 12), 2.0)` seconds (BM pacing ≈8–12 chars/s). Below floor → `TRUNCATED`
(exit 2): re-render on the lane or a fallback rather than deliver a clipped artifact. Check duration on
every render — a partial render can come back with a success status and no error raised.

## 6. Identity — F0 delta and MFCC cosine against the enrolment source

Recipe (librosa, 22.05 kHz is enough): trim silence (`effects.trim(top_db=30)`), then
`pyin(fmin=60, fmax=400)` → **median of voiced frames**; `mfcc(n_mfcc=13)` → mean vector over frames
above the 40th percentile of RMS → **cosine** against the reference mean vector. Report both medians,
the delta in Hz, `voiced_frames_pct`, and the cosine.

Calibration observed on this host (a rented `speech-2.8-hd` clone of a ~30 s broadcast window, source
F0 median 127.1 Hz): same-content render 123.5 Hz / −3.6 Hz / cosine 0.9938; different-content render
124.2 Hz / −2.9 Hz / 0.9911; local CPU F5-TTS render 123.5 Hz / −3.6 Hz / 0.9904.

Reading it correctly:

- **Cosine across different text is a lower bound.** A drop to ~0.99 between reference clip and a
  differently-worded render is content, not drift. Compare like for like (same sentence) for a tight number.
- **A few Hz of F0 delta is not a finding; a wrong octave is.** An octave-sized gap, or a voiced ratio
  near zero, means the tracker latched onto the wrong periodicity or the file is not speech.
- **Metrics confirm the file, not the taste.** They are a floor check; the principal's ear decides whether
  a voice is right. Never promote a voice on numbers.
- DSP work needs an interpreter that actually has `librosa`/numpy — probe (`python3 -c "import librosa"`)
  and use a project venv; a bare `python3` on this host has neither. Keep reusable measurement inside
  `voice_render_verify.py` rather than in a scratch script that gets pruned.

### 6.1 Gender-band gate — refuse before delivery when F0 says "wrong person"

Clone entries in the voice registry carry a `f0_median_band_hz` field (e.g. a masculine persona lands
in 80–155 Hz; a feminine persona in 165–255 Hz). Apply the band check **before declaring a render
ready**, not after the principal hears it:

```python
import librosa, numpy as np
y, sr = librosa.load(PATH, sr=24000, mono=True)
f0, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr)
f0 = f0[~np.isnan(f0)]
med = float(np.median(f0)) if len(f0) else 0.0
lo, hi = BAND_FROM_REGISTRY  # e.g. (90.0, 110.0) for an abang-sado-class clone
# fail-closed
verdict = "PASS" if (lo - 10 <= med <= hi + 10) else "WRONG_VOICE"
```

A render that comes back with `verdict == "WRONG_VOICE"` is the pipeline falling back to a parametric
default — refuse to ship it, do not soften the message ("sounds closer to x"), do not ask the
principal what they think first. The DSP said it's wrong. Wire this gate into
`voice_render_verify.py --strict` so it returns non-zero (exit 4) on `WRONG_VOICE`; without the gate
the principal will hear "itu bukan hang" and have to send another message to correct a defect the
verifier already measured.

**The gate has no tolerance for emotional register.** A male clone that registers 180 Hz on a
particular sentence is not "speaking in a higher register that day" — it is the wrong voice being
served. Same gate, same refusal.

### 6.2 Registry shape trap — `provider_voice_id` is the voice_id string, not the file_id

The registry's voice entry has two numeric-looking fields that are easy to confuse:

- `provider_file_id` — returned by `/v1/files/upload`. Used **only** to point at the source audio
  stored on the provider.
- `provider_voice_id` — the string the synthesis endpoint (`/v1/t2a_v2`) actually consumes. Returned
  by `/v1/voice_clone`.

A pipeline that passes the numeric `provider_file_id` to `/v1/t2a_v2` because the registry column
"name looks like an ID" will not raise an error at the wire level — the provider will accept the
token, fall back to a parametric default voice (typically a female default for the engine), return
`status_code == 0`, and the same verifier that was supposed to catch it will only catch it via the
gender-band gate in 6.1. Treat `provider_file_id` and `provider_voice_id` as different types in
the schema (string-with-prefix vs long-integer) and assert it at registry load, not at first
delivery, so a pipeline that "looks valid" never makes it past the resolver. Rule: any
voice-registry write that has both fields set MUST verify they differ in shape, otherwise the lane
ships the wrong voice on every render until someone notices.

## 7. ASR round-trip mechanics

```bash
set -a; source /root/.secrets/kunci-root.env; set +a
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@out.ogg -F model=whisper-large-v3 -F language=ms -F response_format=text
```

Use **curl** for the multipart upload — a hand-rolled `urllib` multipart body with the same fields was
rejected `403` while curl's was accepted.

State the limits instead of papering over them: Whisper-family engines share a training prior, so their
agreement is not independent confirmation, and Whisper emits fluent Malay boilerplate on non-speech. For
an absence/attribution claim use an architecture-independent (CTC) witness. STT says what a listener would
likely hear; it cannot judge warmth or persona fit. A *reported* success is also not a witness of change —
if you did not probe the layer, the honest answer is `UNKNOWN`, not "done".

## 8. A LIVE registry voice is not automatically a publishable one

Registry entries carry governance fields beyond the id — provenance DATA for the operator, not
output rules (F13 2026-10-18: delivery labels, demo disclaimers and publish-scolding retired as
acah-acah). Renders deliver clean.

- Read the ENTRY when you need to know whose voice a handle borrows — that is context, not a caption rule.
- Check `aliases` first — the trigger word the principal types may resolve to a different handle.

## 9. Adding capability without breaking the lane that works

Standing instruction from the principal: *don't break what is already good.*

- Add beside, never inside: a new renderer script and its own venv, leaving the shipping pipeline,
  `config.yaml` and the canonical voice registry untouched. Report the additions in one line each.
- The registry is a canonical record — propose the entry, don't write it.
- Report defects found in a working lane and let the principal decide; a silent "fix" to a canon voice lane
  is worse than the defect.
- **A declared lane is not a live lane.** Render one take before citing any clone lane as available — a
  script with cached model weights but no installed runtime is a ghost capability, and only a real render
  settles it. For local CPU clone lanes, install `torch` and `torchaudio` from the same wheel index in one
  command; when only local `.wav` references are loaded, overriding `torchaudio.load` with a
  `soundfile`-backed loader removes the TorchCodec/torch version coupling entirely. Do not "fix" a loader
  error by uninstalling torchcodec — the failure just moves to another dependency path.

## 10. Reporting shape to the principal

Numbers first, then the consequence, then what you left alone. "Contaminated" / "clean" alone is a verb,
not evidence: give the similarity, the suspicious tokens, the duration against its floor, and the identity
delta. If a question about difficulty or significance is asked, answer with measured numbers from THIS
artifact rather than general claims about what models can do, and say plainly which part is ordinary
(the synthesis) and which part is the actual engineering (the verification).
