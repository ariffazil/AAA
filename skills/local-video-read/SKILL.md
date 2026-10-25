---
name: local-video-read
description: Use when a local video or audio file must be read.
version: 1.0.0
author: hermes
license: sovereign-internal
tags: [media, video, asr, vision, local-file]
metadata:
  hermes:
    tags: [media, video, asr, vision]
    related_skills: [media-ingest-lane, paste-router]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Local Video Read — frames plus speech, in that order

## When to Use

Load when a video or voice attachment lands as a local path (`/root/.hermes/cache/videos/…`,
`/root/.hermes/cache/audio/…`) and the question depends on what is IN it: a clip pasted with no
caption, a screen recording, media nobody transcribed.

`media-ingest-lane` and `paste-router` own the routing contract and the truth-state ladder; this
skill is only the execution recipe for a local file.

## Pipeline

**0. Check for an existing digest first (added 2026-10-25).** The Telegram gateway now pre-computes
frames + speech at inbound for every video and inlines the result as a `[VIDEO DIGEST — measured
locally, not described]` block. If that block is in your message, the frames are already on disk and
the speech already transcribed — go straight to step 4 with those paths. Do not re-run ffmpeg; do not
claim you cannot read the clip. Fall through to step 1 only when no digest block is present (CLI,
other platforms, or a digest that reported failure).

1. **Identity only, never the answer.**
   ```bash
   ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height \
     -of default=noprint_wrappers=1 "$P"
   ```
   Duration and codec confirm the file decodes. They say nothing about content — quoting them as a
   description of the clip is the metadata-for-content substitution the truth ladder forbids.
2. **Frames.** Six is enough for a one-minute clip; scale the rate, not the count.
   ```bash
   mkdir -p "$D" && ffmpeg -v error -y -i "$P" -vf fps=1/10 -frames:v 6 "$D/f%02d.jpg"
   ```
   Shorter than ~30s, use `fps=1/2` so six frames still span the whole clip.
3. **Speech.** Downmix to 16 kHz mono first — Whisper on the raw stream wastes minutes.
   ```bash
   ffmpeg -v error -y -i "$P" -vn -ac 1 -ar 16000 "$D/audio.wav"
   cd "$D" && whisper audio.wav --model base --language ms --output_format txt --output_dir .
   ```
   `--language ms` matters: Malay clips auto-detected as Indonesian lose the register that carries
   meaning. Malay/English code-switching transcribes acceptably on `base`.
4. **Vision read, three frames per call.** `mcp__media_ingest__media_vision_read(images=[…])` —
   batch three paths and steer with `question` (signage verbatim, uniforms, room, on-screen text).
   More than three per call degrades attention per frame.
5. **Synthesize.** What the frames show plus what the audio says, then the one thing neither gives.

## Report shape

Whatever the ladder reached — frames observed, audio observed, both — and nothing above it. For a
clip pasted with no caption: one line of what it is, one or two lines of what it argues, then why it
matters to him. No scene-by-scene narration.

## Pitfalls

- **"I cannot read video" is almost never the truth on Telegram anymore.** Since the digest landed in
  the inbound path (2026-10-25), a video turn arrives with frames and a transcript already computed.
  Replying that the clip is unreadable wastes the human's turn and, measured that morning, led to a
  wrong-intent answer when he was actually asking about a cooking defect. Read the digest block first.
- **A digest speech line marked SUSPECT is not speech.** Whisper-family models emit "Terima kasih
  kerana menonton" over silence, music and outro stings. On a short silent clip that phrase means the
  decoder filled a gap — report no speech and let the frames carry the answer.
- **Identical ASR segments separated by silence are loop, not speech.** A clip whose audio repeats
  the same line at 0:00, 0:30 and 1:00 is a music bed or a hallucinating decoder; quote the first
  occurrence, say the rest repeats or is unclear, and never present the repetition as three separate
  statements.
- **Music or ambience with no speaker yields confident garbage.** If no frame shows a mouth or a
  stage, treat the transcript as unverified and say the speech could not be read cleanly.
- **Whisper on CPU warns `FP16 is not supported`.** A notice, not a failure — the run continues in
  FP32. Do not re-run it or switch models because of that line.
- **One frame per ten seconds lands mid-blink.** Text overlays persist; faces do not. When a person
  matters, sample more frames rather than reasoning from a single blurred one.
- **Reading frames is not identifying people.** Names, schools and relationships are hypothesis from
  the pixels unless the audio or an overlay states them; attribute by what the clip says, not by who
  it looks like.
- **A link's metadata is not a clip's content.** A resolved URL, redirect chain or video title tells
  you what page it is, not what is said in it.
