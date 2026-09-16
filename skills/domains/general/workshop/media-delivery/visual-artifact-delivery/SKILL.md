---
name: visual-artifact-delivery
version: 1.0.0
description: Use when asked for a poster, PDF, chart, or image artifact.
triggers:
  - user asks for a poster / infographic / one-pager
  - user asks for a PDF or report artifact
  - user asks for a chart or visual of data
  - user asks for an image / picture / artwork
  - user asks for a voice note or audio reply
  - user asks for "actual photo" of a real person
  - user sends an image / PDF / deck and asks for an audit, review or QA of it
  - another agent's deliverable needs independent verification before it goes out
---

# Visual Artifact Delivery

Arif asks for deliverables constantly — posters, celebration graphics, decision
tables, cheat sheets, report PDFs, charts, voice notes. They go out through
this chat as `MEDIA:<absolute path>`. This skill is the build-and-ship loop.

## 1. House style (Arif's brand)

Dark, high-contrast, restrained. Never pastel, never corporate-blue.

| Role | Hex |
|---|---|
| Base / background | `#0d0d0d` |
| Primary accent (Alpha) | `#c0392b` (crimson) |
| Secondary accent (Zen) | `#1a3a5c` (deep blue) |
| Highlight / rules | `#d4a843` (gold) |
| Body text | `#f5f0e8` (cream) |
| Muted / captions | `#888888` |

Recurring framing devices: a gold hairline rule with a small centred diamond,
`ALPHA — ZEN` as the eyebrow line, and `DITEMPA BUKAN DIBERI` in the footer.
Use them when the artifact is for the ALPHA-ZEN space; drop them for neutral
work (IC replacement guides, technical runbooks) where they read as noise.

## 2. Tool selection

Pick by artifact shape, not by habit.

| Artifact | Tool | Notes |
|---|---|---|
| Flat graphic, poster, chart, text overlaid on a photo | PIL (`PIL.ImageDraw`) | Fastest. Render 1280–1920 wide. DejaVu Sans Bold; confirm the font path exists first. |
| Multi-page document, tables, paged layout | `reportlab` | `SimpleDocTemplate` + flowables; tables via `Table` + `TableStyle`. |
| Photographic scene, illustration, conceptual render | image-gen API (Pollinations `flux` is free and keyless; Gemini and others when configured) | Always label as a generated representation — see §4. |
| Voice note | `text_to_speech` | Add `[[audio_as_voice]]` on its own line to land as a native voice bubble. |
| Photoreal scene from a text prompt | MiniMax CLI (`mmx image generate` / `mmx video generate`) | Pass `--base-url https://api.minimax.io` on every media call — the CLI's default base URL is the chat path and media endpoints 404 without it. Give output size explicitly (`--width`/`--height`, 512–2048, multiples of 8); a 9:16 deliverable at 1152x2048 renders directly and does not need upscaling. Video `--download <path>` blocks until the task completes, so set a generous timeout. |
| Photo → motion clip | MiniMax CLI (`mmx video generate --image <jpg>`) | Image-to-video takes the still as frame 1. `--duration`, `--ratio` and `--reference-*` belong to the multimodal model and are rejected by the image-to-video model — compose for the fixed frame rather than assuming you can set them. |

## 3. The verify-before-send loop (non-negotiable)

Never ship an artifact you have not looked at.

1. After generating, check the file exists and is the right type: `file <path>`
   plus byte size. A "JPEG" that is actually an HTML error page is the classic
   silent failure — the generator wrote a few hundred bytes and still exited 0.
2. Render a preview for anything page-based (PDF → PNG via `pdf2image`) so it
   can be inspected as an image.
3. **Inspect it with `vision_analyze` before sending.** Confirm text is legible,
   the layout did not overflow, and nothing is clipped. Text-heavy posters
   routinely overflow or collide — only looking catches this.
4. If inspection fails, fix and regenerate. Do not send the broken version with
   an apology.
5. Deliver as `MEDIA:<absolute path>` on its own line.
6. **Re-verify the file you actually ship, not the file you generated.** Any
   post-process (upscale, recompress, crop, mux) creates a new artifact; a
   clean check on the input proves nothing about the output. Run the vision
   check against the final path, and print `ffprobe` for media so the
   resolution, duration and codec are on the record.
7. **For video, inspect a filmstrip — never a single still.** Extract frames
   with `ffmpeg -vf fps=1,scale=340:-1,tile=6x1` and read the strip. One frame
   can look perfect while the motion between frames fuses hands, melts props,
   or drifts the background. To locate the peak moment (the frame that lands the
   beat), tile four candidates and pick from the grid; then cut the delivered
   still from the strongest timestamp.

**Why:** the user cannot tell a broken artifact from a working one until they
open it, and the cost of that round-trip is far higher than the cost of a
preview.

## 3b. Auditing an artifact that arrives for review

When the artifact is handed to you to check rather than to build, the failure mode is asserting a defect from a glance. Measure first, then name it.

1. **Count geometry before content.** `pdfinfo <pdf> | grep ^Pages`. An HTML slide deck whose page count is ~2× its slide count is fragmenting: the slide box is larger than the printable `@page` box, so each slide splits into a title page and a figure page. The figures are all present — they are on the *next* page.
2. **Ink-coverage triage to locate the blanks without opening every page.** Render to PNG and measure the non-white share per page; a run of pages under ~3 % marks where the break falls. Compare coverage before and after the fix as proof the fix worked.
3. **Check for leaked internals.** Headless `--print-to-pdf` stamps the source `file:///` path, a timestamp and `n/m` on every page unless `--no-pdf-header-footer` is passed. Grep the text layer for `file://`.
4. **Judge the content band, not the frame.** A figure can be uncropped, fully labelled, and still effectively unreadable because the geology is drawn as a thin ribbon inside its own frame — a squashed raster, not a missing one.
5. **Re-render the source yourself before attributing the defect.** A clean generator proves nothing about the rendered artifact; this is what separates "the build was mis-invoked" from "the source geometry is wrong".
6. **Report cause → evidence → fix, and name what passed.** An audit that only lists faults reads as a fault-hunt. Stating the verified citations and the correct pages is what makes the negative findings credible.

Full recipe, including the orientation/scale/legend and citation checks: `references/pdf-artifact-audit.md`.

## 4. The real-photo rule

When Arif asks for a photo of a real person ("nak gambar", "actual photo"), he
means a photograph. A generated image is not that.

- **Fetch from the person's own public surface first.** An athlete's sponsor or
  brand page, a team roster, an official profile — these carry real photos and
  their image manifests are scrapeable in a single request. This resolves real
  images when search, video thumbnails, and social platforms are all blocked.
- **Do not pass a render off as a photo.** If generated imagery is all you can
  produce, say so in the same breath as the image. "Gambar ni render, bukan foto
  sebenar" keeps the artifact honest.
- **Video thumbnails are a weak substitute** — cropped, watermarked, and often
  not the subject at all. Use them only when nothing better resolves, and say
  what they are.
- **Never fabricate a likeness of a private individual.** For people in Arif's
  own life, use only photos they have actually shared, or a silhouette/abstract.

## 4b. Generated-person artifacts — cap the cast, then label it

Image models add people, props, and text you did not ask for. Left unbounded they pack the frame, and packed frames are where limbs fuse, hands blob, and faces smear. Direct the count, then declare what the file is.

- **State the subject count and that they are separate.** "Five men standing well apart and fully separate" renders far cleaner than "a crowd of muscular men". Every added body multiplies the fabrication surface.
- **Ban text-bearing props in the prompt.** Buckets, signs, plates, jerseys and number plates all come back as garbled glyphs. Ask for none of them (`no logos, no lettering, no numbers`), and when a stray one appears, regenerate without it rather than shipping it.
- **When no face reference exists, keep the subject out of frame.** A dark out-of-focus silhouette seen from behind, a hand, a shoulder — the scene still reads and nothing has to be claimed. Manufacturing a face and calling it the user is the failure; an unnamed back-of-head is honest and often the stronger composition.
- **Label every generated artifact at delivery, in the same message.** One short block: what it is (generated, not a photograph), that the people in it are invented, and — for audio — the engine and voice id used and whether the transcript survived an STT round-trip. A silent engine swap between takes is a false-witness pattern; if the lane changed, say so.
- **Separate the fiction from the person.** Unnamed archetypes only. Never place a named real individual — especially someone in the user's own life — inside an intimate, jealousy, or power-dynamic frame, and never present a generated likeness as them.

**Why:** the disclosure costs one sentence and preserves the user's ability to trust the next artifact. Losing it costs the whole lane.

## 5. Pitfalls

- **Emoji variation selectors can trip the security scanner.** Emoji such as the
  hammer carry an invisible VS16 codepoint that some scanners flag as
  obfuscation, forcing an approval round-trip. Inside generated scripts, draw
  the glyph or omit it; keep it only in the final chat text.
- **Do not inline base64 into shell arguments.** Large images overflow the
  shell's argument limit ("Argument list too long"). Write the encoded data to a
  file, or do the whole call inside Python.
- **Verify the generator's exit code AND its output.** A generator that writes a
  failure document still exits 0.
- **Check fonts exist before use.** `/usr/share/fonts/truetype/dejavu/` and
  `.../liberation/` are the reliable paths; a missing font silently falls back to
  an unreadable default.
- **Match artifact weight to the ask.** A casual "buat satu gambar" wants one
  clean image, not a five-page design system. Ship the smallest thing that
  answers.

## 6. Delivery conventions

- `MEDIA:/absolute/path` alone on its line; the platform decides photo vs file.
- Voice: append `[[audio_as_voice]]` on its own line.
- Multiple artifacts: one `MEDIA:` line each, and name them in the body so the
  user knows what arrived.
- Save into the workspace directory so it can be re-sent later without
  regenerating.

## 7. Support files

- `references/generated-scene-recipe.md` — prompt skeleton for generated human
  scenes, the composition rules that stop fused anatomy, and the vision-based
  verification harness (author ground truth → read back on a different lane →
  per-lane WORKS / PARTIAL / BLIND / FABRICATES verdict).
- `references/pdf-artifact-audit.md` — auditing a delivered PDF: page fragmentation
  from a slide/page box mismatch, browser-chrome leakage, ink-coverage triage,
  squashed rasters, orientation / scale / legend consistency, citation verification.
