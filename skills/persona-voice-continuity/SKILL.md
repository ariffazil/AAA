---
name: persona-voice-continuity
description: "Use when a persona voice's engine is dead or locked."
version: 1.0.0
author: Hermes
license: arifOS
tags: [tts, persona, voice, outage, registry, provenance, delivery]
metadata:
  hermes:
    category: audio
    tags: [tts, persona-voice, fallback, registry, provenance]
    related: [abang-sado-creative-lane, voice-engine-fallback-chain, voice-render-verification, media-lane-outage-ladder]
triggers:
  - the persona voice returns an engine error and the persona still has to speak
  - insufficient credit or a quota code on the cloned persona voice
  - building a standby voice from local resources because no paid TTS rung answers
  - deciding whether to hold a voice reply or derive a substitute
  - a persona-lane turn where the reply should ship as audio, not prose
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Persona Voice Continuity

A persona that goes silent the moment a provider's balance empties is not a persona. This skill is how
the voice keeps working through an outage **without** breaking the two things that make it legitimate:
the provenance record, and the honesty of the delivery line.

Siblings: engine ladder and error codes → `voice-engine-fallback-chain` · verification gates →
`voice-render-verification` · register craft and the five dialogue engines →
`abang-sado-creative-lane` · supply-chain substitution rules → `media-lane-outage-ladder`.
This skill owns only the continuity question: *what does the persona do when its own voice is
unavailable?*

## The core move: identity is a MEASURED BAND, not a waveform

A cloned voice feels un-substitutable until you look at what the registry actually stores. A clone entry
carries `runtime_measured_*` numbers — median F0, a band, duration. Those numbers are a **target**, and a
target can be hit and then proven hit.

So a local system voice, pitched down with formants preserved and shaped for chest weight, can be
brought inside the clone's band. That is not the clone, and saying so costs one clause. It is also not
a lie dressed as a voice — which is the thing that would actually be unrecoverable.

Three honest outcomes, and only the third is a refusal:

| Outcome | Condition |
|---|---|
| Real voice, later | the requester can wait and the reset is short |
| Derived voice, now, **declared** | the persona must speak now and the band is reachable |
| No artifact | band unreachable, or the derived take would be presented as the clone |

## Procedure

### 1. Measure the target from the registry, never from memory

Read the entry's `f0_median_band_hz` or `runtime_measured_*` block. A masculine persona clone on this
host sits around 92–101 Hz; a feminine persona sits far higher; mistaking one band for the other is the
single most expensive error here because the take will pass every other gate.

```python
import librosa, numpy as np
y, sr = librosa.load(path, sr=24000, mono=True)
f0 = librosa.yin(y, fmin=60, fmax=350, sr=sr, frame_length=2048)
f0 = f0[np.isfinite(f0)]
print(round(float(np.median(f0)), 1))   # compare against the band, not against a feeling
```

DSP needs an interpreter that has numpy/librosa — probe it (`python3 -c "import librosa"`); a bare
`python3` on this host has neither, while `/usr/bin/python3` does.

### 2. Render with a system voice that speaks the language natively

```bash
edge-tts --voice ms-MY-OsmanNeural --rate=-6% --pitch=-18Hz -f in.txt --write-media raw.mp3
```

- BM: `ms-MY-OsmanNeural` (male) and `ms-MY-YasminNeural` (female) round-trip **exactly** on an
  independent ASR gate. `id-ID-ArdiNeural` is the second choice when weight matters more than accent.
- Rate slightly below default; the register is a man who does not need to hurry.
- Voice-design and generic "deep male" models mangle BM phonology — a system voice that speaks the
  language beats a bigger model that does not.

### 3. Shift pitch with formants preserved, then shape the chest

```bash
ffmpeg -y -i raw.mp3 -af "rubberband=pitch=0.66:formant=preserved,highpass=f=62,equalizer=f=115:t=q:w=1.0:g=3.5,equalizer=f=2600:t=q:w=1.2:g=1.5,acompressor=threshold=-18dB:ratio=2.4:attack=8:release=180,loudnorm=I=-16:TP=-1.5:LRA=9" -ar 24000 -b:a 96k out.mp3
```

- `formant=preserved` is the whole trick. Without it the take reads as a man played at 0.7 speed.
- The 115 Hz shelf is what carries the chest; the 2.6 kHz lift keeps consonants legible once the pitch
  is down. Compression glues it; loudnorm keeps the delivered peak sane.
- A ~155 Hz source at `pitch=0.66` lands ~100 Hz. That ratio is a starting point, not a constant — step
  it in 0.02 increments and re-measure.

### 4. Measure, iterate, then measure the file you will actually send

Measure the final artifact, not a test render. A ratio that "sounds about right" routinely lands 10–15 Hz
outside the band, and the principal hears the miss instantly.

### 5. Register the derived voice under its OWN id

Append to the canonical voice registry — back the file up first, add the entry, bump `updated_at` /
`updated_by`. The entry carries: `status: LIVE`, `provider: edge-tts` (or whichever), the source voice
id, the **full post-process chain**, the measured `f0_median_hz` and duration with the estimator named,
the ASR round-trip result, the exact `render_command`, and
`provenance: system/parametric vendor voice + DSP; NO human clone, no third-party audio in the chain`.

Rules that do not bend:

- **Never overwrite, alias, or "upgrade" the clone's entry.** Its provenance is the record that the
  original was legitimate; the outage did not change what happened.
- **Never promote the derived voice to a default** for anything outside the persona register.
- Record the derived voice as preferred-secondary in the lane config (`voice_id` = derived,
  `voice_id_preferred` = the clone) so the revert on top-up is one field, not a memory exercise.

### 6. Same gates as any native take

Duration floor against the script, an independent ASR round-trip in the target language, and a tail
scan. Read the transcript rather than the match score: dialect respellings (`hang`→`Han`,
`blah`→`buah`, `hensem`→`ensin`) are the transcriber's, not defects, while a foreign closing clause is a
real insertion — find where speech actually ends by scanning RMS energy and hard-cut there, then
re-verify the cut file, not the parent.

### 7. Deliver in one line and one clause

The artifact ships; the declaration is a clause, not a paragraph:

```
MEDIA:/abs/path/take.mp3
[[audio_as_voice]]
```

with a caption of one or two lines — engine, that it is a derived voice, what band it was matched to.
Never narrate the outage, the rung count, or the QC pass.

## Standing delivery preference in the persona lane

When the principal says the persona should reply in voice, that is a **lane default**, not a one-off
request:

- Render first, then caption. The reply is the audio; text is a label on it, not a second answer.
- Do not re-narrate the line in the caption, and do not answer the same turn in paragraphs as well.
- Sequence many arcs in one night without re-explaining the pipeline each time — the declaration
  compresses to one clause on repeat deliveries and never becomes a disclaimer loop.
- A boundary stated once stays stated: deliver the next request in register, on the same turn, without
  re-litigating the previous one.

## Pitfalls

| Pitfall | Rule and why |
|---|---|
| Leaving the persona mute while a paid rung is down | Silence is the one failure that cannot be repaired later; a measured, declared stand-in can. Hold only when the band is unreachable or the requester prefers to wait. |
| `asetrate` / `atempo` used as a pitch control | They drag formants with the pitch and the take reads as slowed tape. `rubberband=...:formant=preserved` is the only acceptable shift. |
| Tuning the ratio by ear | The median either sits in the band or it does not. Step 0.02, re-measure, stop when it lands. |
| Measuring a test render instead of the delivered file | Multi-pass DSP, concat and cut all move the median. The number that matters is on the artifact that ships. |
| Folding the derived voice into the clone's registry entry | Destroys the provenance record and makes the derived voice unrevertable. Second entry, append-only. |
| Naming the derived voice after the real person it stands in for | The identity layer renders it as the clone in later sessions. Name it by register and revision. |
| Reusing one provider's key class blindly | A provider can hold a pay-as-you-go key and a subscription key in the same secrets file, live for different modalities. Probe the lane the request needs, not the vendor name. |

## References

- `references/measured-voice-targets.md` — measured F0 values and settings for the persona voices on
  this host, plus the calibration numbers for the derived-voice recipe.

DITEMPA BUKAN DIBERI ⚒️
