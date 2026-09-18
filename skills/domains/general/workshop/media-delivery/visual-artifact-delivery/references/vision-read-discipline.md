# Vision-read discipline — resolving text off images and video frames

When the artifact's payload **is** the text in the pixels (a poster, a badge, a garment print, a
signboard, a frame grabbed from video), the vision read is the deliverable, and getting it wrong is
worse than returning nothing. This file is the gate to run before a quoted string reaches a human.

## The three failure classes

| Class | What it looks like | How to catch it |
|---|---|---|
| **Memory fill-in** | The read is plausible, on-theme, and never came from the image | Call the vision tool, quote what it returned, and say so explicitly — never let priors complete a partial read |
| **Overlay misattribution** | A real string in the frame, read off the wrong surface | Name the surface in the question, or crop the overlay band out |
| **Resolution hallucination** | A confident word that changes on every call | Do the pixel arithmetic first; abstain when the glyph is too small |

### Overlay misattribution is the nastiest of the three

A video's own title graphic, a poster's caption, a lower-third, a watermark — all sit inside the
frame, often directly over the subject. Asked to "read every line of text", the model returns one of
them and it lands in your report as text **on the object**.

What makes this worse than invention: the string is genuinely present, so the natural verification
step — *does that text appear in the image?* — **confirms it**. The model is not fabricating; it is
answering a question you asked too broadly.

- Scope the ask to the surface: *"teks yang tercetak pada [object], bukan caption atau overlay."*
- Or crop the overlay band away before asking — cheaper than a disambiguation pass.
- Treat any result that echoes the media's own title or channel name as contaminated by default.

### Resolution hallucination — the tell is variance

**A readable target reproduces; an unreadable one produces a fresh confident guess every time.**

Measured: four consecutive calls on identical pixels returned four different words, each delivered
without hedging — and a fifth returned a string that was not a word at all. That is not model
instability to be outvoted. It is the channel telling you it cannot carry this content.

- **Two disagreeing reads = a FAILED read**, not a menu. Do not choose.
- **Do not pick the most frequent answer**, and do not re-ask with a firmer prompt. The limit is
  resolution, not persuasion; pressure buys more confident fabrication.
- **Do the arithmetic before spending the call.** Estimate the target's height in source pixels. A
  chest print on a 640×360 frame is roughly ten pixels tall — nothing resolves that, and ×3 LANCZOS
  on the crop leaves a 30-pixel blur. Upscaling adds no information the source never carried.
- **UNREADABLE is a complete output.** Say it and stop.
- **The fix is a bigger source, not a better question.** Ask for a higher-resolution image of the same
  object (the requester's own photograph, the original file) and read that.

## Video frames specifically

- **A whole-timeline contact sheet is a layout summary, never an OCR source.** Right for "what happens
  in this video"; wrong for a badge or a logo. For a specific string, extract a short high-scale
  window and crop tight:
  `ffmpeg -v error -y -ss <t> -i media.mp4 -t 8 -vf "fps=2,scale=1920:-2" out_%02d.jpg`
- **Sample the sheet for coverage, the crop for glyphs.** They are two different tools and swapping
  them is how a ten-pixel string becomes a confident wrong word.
- **The overlay sits in the middle of the frame**, so the trap is worse here than on a poster.
- **Re-check the frame you actually read.** Paths get copied between scratch and artifact
  directories; a `missing files` error from a read tool means the path did not resolve, not that the
  vision lane is down — copy the frame where the tool expects it and retry before concluding
  anything.

## Relaying the read

State which surface it came from and mark the class of every claim: **OBS** (seen in the source),
**DER** (entailed), **INT** (inferred). "Not visible at this resolution" beats a confident string,
and a refused read reported honestly is a valid delivery — a fabricated one poisons every reader
downstream of you.
