---
name: machine-read-verification
description: "Use when relaying an ASR/OCR/vision read to a human."
version: 1.0.0
owner: AAA
category: verification-discipline
tags: [asr, whisper, vision, ocr, hallucination, evidence, verification, media]
floor_scope: [F2, F4, F7, F9]
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Machine-read verification — falsify the model before you relay it

Applies to any generated *reading* of real-world media: speech-to-text, OCR, a vision or
contact-sheet read, a screenshot, a poster, a scanned table. The transport (which lane, which
provider, which credits) is a separate concern; this skill is only about whether the text you
are about to hand a human is actually a reading of the source.

## Rule 0 — a model's output is a CLAIM, not an observation

ASR and vision models do not fail loudly on content they cannot read. They **invent** it.
Whisper transcribes music and silence into plausible sentences; a vision model answers a
tiled contact sheet with confident, wrong strings. A fabricated read is worse than an empty
one because it looks like content and poisons every downstream reader. So: an unverified read
is ABSENT-with-a-reason, never content.

## Procedure

### Step 1 — can this channel carry the content at all?

Speech channel, cheapest probe first:

```bash
# digitally silent track?  mean == max == -91.0 dB  ->  there is no speech
ffmpeg -hide_banner -i media.mp4 -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"

# not silent (music bed) but still suspicious: pin the language, request segments,
# then read it segment by segment
ffmpeg -v error -y -ss 0 -t 150 -i media.mp4 -vn -ac 1 -ar 16000 -b:a 48k /tmp/slice.mp3
curl -sS https://api.groq.com/openai/v1/audio/transcriptions -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@/tmp/slice.mp3" -F "model=whisper-large-v3" -F "language=ms" -F "response_format=verbose_json"
```

- **One sentence repeated in every segment is a hallucination template, not speech.** Real
  speech varies across segments. (Measured: the same sentence on all five segments of a
  music-only montage.)
- **A music bed defeats the silence probe** — real audio at ~−20 dB mean — so the second
  probe is the one that works in the general case. Run it whenever the words do not look
  like the source's language.
- **Pin `language=` on any non-English source.** Auto-detect drifts into an arbitrary script
  (it wrote Khmer over Malay audio); a pinned re-run is what separates "wrong script" from
  "genuinely foreign soundtrack". `verbose_json` returns the detected `language` — read it.
- Never run STT to find out what silence says. If there is no speech, the honest answer is
  the pixels, not a transcript.

### Step 2 — resolve every quoted string from ONE full-size frame

A tiled contact sheet is a **layout summary**, not an OCR source. Before a quoted word, name,
number or watermark reaches a human, re-read it from a single full-resolution frame.

- One sheet read transcribed the same watermark two different ways inside one answer. **Two
  reads that disagree mean the read FAILED** — it is not a menu to choose from.
- **Identity never comes from a sampled grid.** Take a person's name from the source's own
  title or on-screen caption and say that is where it came from; never infer it from a body, a
  scene, or a prior photo.
- **Discard a read that leaks reasoning scaffolding** ("starting with the first image…", "now
  the second image…"). That is a failed read, not a verbose one — re-ask.

### Step 3 — class the claims, and abstain where the channel is empty

Every statement gets a class: OBS (seen in the source), DER (entailed by what was seen), INT
(inference). Abstention is a valid, reportable outcome — "not visible" beats confabulation.
A channel that returned nothing cannot support claims of that modality, no matter how much
the other channel returned.

### Step 4 — relay the receipts with the content

State which halves were actually read and which channel was refused, alongside the content:
`truth_state` (OBSERVED / PARTIAL / BLOCKED), `content_read` (which modalities), and
`transcript_state` (`OK` / `ABSENT` / `SUSPECT_DEGENERATE:<why>`). Keep the refused text on
disk for audit. "The audio had no usable speech; this read is from the frames" is a complete,
honest answer — and it is the one a downstream reader needs.

## Hallucination signature table

| signature | what it means |
|---|---|
| repetition loop (≤3 unique words over >12 words) | non-speech audio; the classic `"you you you …"` |
| unique-word ratio < 0.2 over >25 words | degenerate loop (real speech ≈ 0.7) |
| script mismatch (non-Latin output for a Latin-script target) | the model is guessing at noise |
| boilerplate ratio ≥ 0.35 | "thank you / subscribe" filler filling silence |
| a closing boilerplate line ("terima kasih kerana menonton", "subscribe") on a file whose every lexical word round-trips | transcriber TAIL ARTIFACT, not content — the whole-file pass creates it; slice the last seconds and re-read |
| one sentence in every segment | hallucination template |
| <15 words across >2 min | too sparse to be speech |

## Localising a suspected insertion — never convict from a whole-file pass

A full-file transcript cannot separate a source defect from a transcriber artifact, and the
transcriber is the likelier author. When you are about to report an insertion — or retract a
take, reject a render, or escalate a contamination finding — narrow the window first.

1. **Slice the suspect window and re-read the SLICE.** Cut it out losslessly and run the same
   STT on the cut: `ffmpeg -v error -y -ss <start> -to <end> -i take.mp3 -c:a copy slice.mp3`.
   A phrase that survives isolation with real, separated timestamps is in the audio; a phrase
   that vanishes inside the window was written by the model. Re-verify the CUT, not the parent —
   clearing the artifact you already cleared proves nothing about the one you are about to send.
2. **Cross-check the DURATION BUDGET.** If the source's own words already fill the file, and a
   sibling of comparable word count runs the same length, there is no room for an insertion —
   a claimed extra clause needs seconds that do not exist. Arithmetic is a witness the
   transcriber cannot argue with.
3. **Two passes of the same model family are not independent witnesses.** Re-running the same
   request, or stepping within one family (turbo → non-turbo), reproduces the same artifact
   because it is the same decoder. Agreement counts only across genuinely different models or
   methods — and even then, position and duration outrank a second opinion.
4. **Do not destroy content to satisfy a gate.** Hard-cutting a tail is legitimate only after
   step 1 proves the tail is not speech; a cut past a real word is a worse defect than the one
   being hunted. And if you do cut, say so — a silently trimmed take is a claim about the source.

## The measurement must itself be testable

A probe whose output you cannot observe is not a probe. `ffmpeg -v quiet` SUPPRESSES the
`silence_start` lines a silence-counting probe was reading — it returned 0 every time and
reported "continuous audio" for a digitally silent file. Never add `-v quiet` to a command
whose output you intend to parse, and sanity-check a detector against a case where it MUST
fire before trusting a pass.

## Pitfalls

- **A gate that destroys real information is worse than the hallucination it prevents.** An
  acoustic gate ("speech has pauses") withheld a valid transcript from a clip containing clear
  speech. Trigger on the most reliable signal, keep weaker signals in the artifact as evidence
  a human can inspect, and never let an untested heuristic overrule the text itself.
- **A health check sampled on one item is a false green.** A capability probed against a
  single (heavily cached) item reported OK while three real items failed in the same minute.
  Probe several samples and report a RATE.
- **Transient ≠ broken.** A media fetch denial can be a temporary host block; retry with
  backoff before reporting a capability dead, and never relay a single transient denial as a
  hard BLOCKED.
- **Never promote absence to success.** An empty transcript next to real frames is not a
  partial read of the content — it is success of the visual channel and absence of the speech
  channel, and it must be reported as both.

## Relationship to other skills

| This skill | Other skills |
|---|---|
| Is the read real? | `claim-level-verification`, `synthesis-verification-gate` — system-state claims |
| Media transport / lane ladder / provider economics | `media-ingest-lane`, `youtube-extraction-datacenter-ip` |
| Video evidence ledger + claim classes | `AAA-video-emd-pipeline` |

Support file: `references/vision-endpoint-quirks.md` — driving the OCR/vision endpoints
ourselves (argv limits, empty-`content` reasoning models, scratchpad stripping, 402/429
handling, the two-model-agreement rule for anatomy/injury/identity).
