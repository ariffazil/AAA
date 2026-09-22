---
name: generated-media-delivery
description: "Use when generating an image or video for delivery."
version: 1.0.0
tags: [image-generation, video-generation, qc, delivery, lane-selection, minimax, mmx]
metadata:
  hermes:
    category: creative
    requires: [mmx-cli]
    related: [lightweight-image-generation, image-gen-fallback-chain, photorealistic-human-image-gen]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Generated Media Delivery

Lane selection, flag/key gating, frame QC, and honest reporting for any image or video generation
task. Generation is the cheap part; verification and truthful reporting are the deliverable.

Depth:

- [`references/video-lane-selection.md`](references/video-lane-selection.md) — video model lanes,
  flag compatibility, key-class gating, ffmpeg verify/QC/upscale commands.
- [`references/pov-composition.md`](references/pov-composition.md) — peek/doorway framing, crowd
  scenes with one payoff beat, SEA phenotype phrasing, synthetic-subject boundaries.
- [`references/symbolic-life-portrait.md`](references/symbolic-life-portrait.md) — "portray my life"
  requests: element ledger, positional prompt shape, element-level QC checklist.

## Order of operations

1. **Pick the lane before writing the prompt.** Cheapest lane that satisfies the ask wins; reach for
   the top-fidelity lane only when the request genuinely needs its capabilities *and* the credential
   class is entitled to it. Lane table: `references/video-lane-selection.md`.
2. **Write the prompt around one focal beat.** For video, one camera behaviour per clip. For stills of
   crowds, one payoff action stated last. Place the most important element first.
3. **Generate with an explicit absolute `--download` path.** These waits exceed the foreground command
   cap: launch as a tracked background process (`terminal(background=true, notify=true)`) and wait on
   that same session. A missing final path while the session is alive is not a failure.
4. **Verify the artifact** (dimensions, duration, frame count) before treating the run as done.
5. **Read the frames back** with `vision_analyze` and check the invariants the request named.
6. **Deliver** the file plus one line stating which lane rendered and what is synthetic about it.

## Two hard stops you will meet

- **Flag rejection is a usage error, not a content error.** Flags that belong to a newer model
  (`--duration`, `--ratio`, multimodal `--reference-*`) fail instantly on the default legacy model.
  Drop the flags or move lanes — and when you move lanes, re-check the key requirement, because it
  moves too.
- **A model series can be gated by credential class.** A subscription / Token-Plan credential can be
  refused for a pay-as-you-go-only series. Nothing was submitted, so no retry is owed: report the
  gate, fall through to the lane that credential can drive, and return to the top lane only with a
  key of the right class already injected as an environment variable. Never ask the user to paste a
  key into chat and never put a key in a command transcript.

## Reproducible takes: seeds, geometry, exact paths

Generate the still half of the work as a small set of *comparable* takes, not one lucky roll.

- **Pin an output path per take** (`mmx image generate --out /abs/path/take_501.jpg`). Distinct
  absolute `--out` paths in the same directory all land correctly, which keeps the QC loop and any
  re-run auditable. The CLI's `--output` flag is ignored, and an unflagged call overwrites
  `image_001.jpg` in the working directory — so an unflagged batch silently destroys its own earlier
  takes.
- **Vary one variable per take.** Hold the prompt fixed and change only the seed (`--seed <n>`), with
  geometry pinned (`--width/--height`, 512–2048, multiple of 8). Change one thing at a time or the
  comparison means nothing.
- **Read every take back** with `vision_analyze` and keep the one where the *named* invariants
  survived — the requested framing, the single payoff beat, the intended phenotype. Animate that
  take; do not animate an unread frame.

## Frame QC before delivery

```bash
ffmpeg -y -v error -i out.mp4 -vf "select='eq(n\,0)+eq(n\,70)+eq(n\,143)'" -vsync 0 qc/f_%02d.png
ffmpeg -y -v error -sseof -0.08 -i out.mp4 -frames:v 1 qc/f_last.png
```

Run `vision_analyze` on first / middle / last and confirm: the requested framing survived, the focal
beat is present, the intended phenotype/props landed, and there is no garbled text, melted hands or
impossible mirror geometry. If a requested beat is absent, regenerate — never narrate an image that is
not in the file.

## Better quality: upscale, do not overclaim

When the ask is "better quality" and the higher lane is unreachable, upscale and say so:

```bash
ffmpeg -y -v error -i out.mp4 \
  -vf "scale=1920:1080:flags=lanczos,unsharp=5:5:0.45:5:5:0.0" \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart -an out_1080p.mp4
```

Name the lane that rendered and offer the re-render once the right key exists. Presenting an upscale
as native model output is an F2 truth failure, not a delivery detail.

## Synthetic subject boundaries

- Say plainly what is generated: the bodies, faces and observer in a synthetic frame are not real
  people. That sentence belongs in the delivery, not in a footnote.
- Do not place a real named person — or the user's own likeness — into a generated frame without a
  user-supplied reference image. A collective noun for a type of person ("abang sado", "the fans") is
  not one person: ask which referent is meant instead of defaulting to one.

## When the ask is the subject's own life

"How would you portray my life?" is a DISCOVERY request, not a spec, and its failure mode is a
flattering composite assembled from generic symbolism. Three rules keep it honest:

- **Element ledger before pixels.** Every object in the frame must trace to something the subject
  actually said, wrote, or built. Write the mapping first; any element with no source gets cut. A
  symbol the subject never disclosed is a fabrication that happens to be pretty.
- **Mark the blanks instead of filling them.** Say in the delivery what you deliberately left out of
  frame, and why. Undisclosed territory stays undisclosed — an invented detail reads as knowledge and
  cannot be un-read.
- **Still life, not portrait.** Zero people, zero faces, zero hands; the working surface is the stage
  and one key light carries the frame. State the negatives explicitly or the render drifts back into an
  anonymous figure.

Because there is no likeness to verify, QC runs on the *elements*: ask the enumerated checklist
("which of these landed: …; any people, faces, or text?") rather than "describe the image", and keep
the take where the named objects survived. A take that renders mood beautifully while dropping two
named elements is a reject, not a runner-up — low-key night frames in particular lose the key light
source and still look good. Recipe and checklist: `references/symbolic-life-portrait.md`.

## When the ask is a real likeness

A request for a *specific real person's* image cannot be met by generation, and a render offered as
a substitute is rejected on sight ("I want the actual photo"). Fetch instead — two routes work
without a session, API key, or scraping infrastructure:

- **YouTube thumbnails by video ID** — `https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg`
  (fall back to `hqdefault.jpg` when `maxresdefault` 404s). One still per video, stable URL.
- **Sponsor / brand / federation pages** — a sponsored or ranked athlete has a profile page on the
  sponsor's or federation's site. Scrape that page for image URLs, take the largest, and convert
  WebP→JPEG with PIL before delivering.

State what each image actually is (thumbnail, press photo) and where it came from. If neither route
surfaces the right person, name which real-photograph route failed and stop — do not close the gap
with a render.

## Pitfalls

- Do not re-run the identical failing command. Read the error class first (usage / key-class gate /
  balance / rate limit) — each one has a different move.
- In a parallel batch (`&` + `wait`), verify each lane's output separately with `file` and read its own
  log line — a lane that never launched (helper script absent, wrong binary, missing source) leaves no
  trace in the aggregate result. Report the lost lane in one clause and ship the surviving takes; never
  re-fire the whole set for one dead lane.
- Do not submit a second paid task because waiting or downloading was interrupted.
- Do not add the newer model's flag set to "fix" a legacy-lane usage error; that silently changes the
  key requirement.
- Do not present a fallback-lane output as the requested lane, and do not report a model name you did
  not verify.
- Do not scale a still and a video from different aspect ratios when the still is meant to be a
  video's first or last frame.
- Do not deliver a render that contradicts the brief while captioning it as if it matched. Name what
  came back instead, in one line, and offer the honest alternate route (a real photograph, or the
  subject's own camera). Re-rolling the identical prompt reproduces the same prior — change the brief
  or stop.
- Do not name a relationship in emotional terms and expect a neutral composition. "A hug", "close
  friends" — any two-person frame carries an intimacy prior and will render as romantic or sexual
  content. Specify clothing, pose, framing, camera distance and what is *not* in frame, then read the
  render back before delivery.
- Do not treat a deterministic layout (reportlab / PIL / ffmpeg text) as pre-verified. It will not
  garble words the way a model render does, but it can still overflow, collide or run off-canvas —
  rasterise a page and read it back like any other output.
