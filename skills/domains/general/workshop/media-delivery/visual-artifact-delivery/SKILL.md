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

**Default to LIGHT for anything read on paper or scrolled as text** — PDFs, reports, briefs, dossiers,
letters. White ground, dark text, restrained accents.

> **Corrected 2026-09-18.** This section previously specified a dark base (`#0d0d0d`) as the house
default. Arif stated the opposite plainly: *"I hate black dark background in pdf."* The dark palette
survives only as an **opt-in for screen-native artifacts** — a poster, a social graphic, a deck
shown on a projector — and never as the default for a document he reads.

**Light palette (use this):**

| Role | Hex |
|---|---|
| Ground | `#ffffff` |
| Body text | `#1c1c1c` |
| Heading / table header | `#1a3a5c` (navy) — white text on it |
| Accent rule / stamp | `#b02a1f` (deep brick) |
| Emphasis numbers | `#6b5210` (dark bronze) |
| Zebra row | `#f7f6f4` |
| Muted / caption | `#5f5f5f` |

**Dark palette — opt-in only, for screen-native work:**

| Role | Hex |
|---|---|
| Base / background | `#0d0d0d` |
| Primary accent (Alpha) | `#c0392b` (crimson) |
| Secondary accent (Zen) | `#1a3a5c` (deep blue) |
| Highlight / rules | `#d4a843` (gold) |
| Body text | `#f5f0e8` (cream) |
| Muted / captions | `#888888` |

**Contrast trap when you move a design from dark to light:** an accent that sits comfortably on a
dark ground can fall to ~3:1 on white — below WCAG AA. Gold `#d4a843` is the usual casualty; take it
to `#6b5210`. Vision inspection caught exactly this on the first light build, so check the accent
rather than assuming the palette transferred.

Recurring framing devices: a gold hairline rule with a small centred diamond, `ALPHA — ZEN` as the
eyebrow line, and `DITEMPA BUKAN DIBERI` in the footer. Use them when the artifact is for the
ALPHA-ZEN space; drop them for neutral work (IC replacement guides, technical runbooks) where they
read as noise.

For the full document pipeline — engine choice, gates, seal, and the layer stack with each layer's
owning skill — load `document-pipeline` first.

## 2. Tool selection

Pick by artifact shape, not by habit.

| Artifact | Tool | Notes |
|---|---|---|
| Flat graphic, poster, chart, text overlaid on a photo | PIL (`PIL.ImageDraw`) | Fastest. Render 1280–1920 wide. DejaVu Sans Bold; confirm the font path exists first. Long strings never wrap and never raise — measure every one against its column width at build time (`references/pil-text-poster.md`). |
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
   *Before* the vision check, catch overflow mechanically: measure each string with
   `draw.textlength(text, font=font)` against its column width and print every failure
   as the build runs. PIL neither wraps nor raises, so an overlong line silently runs
   off the canvas edge and the vision pass degrades from confirmation into detection.
   A build that printed an overflow is a failed build — fix and rebuild, never ship it.
   Recipe: `references/pil-text-poster.md`.
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

## 3c. Mechanical gates at build time, not at audit time

A page-based artifact must be measured by the build that produced it. Anything you can check with a
number, check automatically — reserve the vision pass for what only looking can catch.

Run these the moment the file is rendered, and fail the build on any of them:

- **Page count.** `pdfinfo <pdf> | grep ^Pages`. An unexpected count means the content did not fit
  where you thought it did — most often one section spilled onto an extra page.
- **Text layer size.** An empty or tiny text layer means a scan or a failed render, not a document.
- **Per-page ink coverage.** Render to PNG and measure the non-white share of each page. A page far
  below its neighbours is a **stranded fragment** — a trailing section with nothing to sit beside.
  Fix it by moving real content into that page (the seal block, the verification table), never by
  padding. Compare coverage before and after to prove the fix.
- **Leaked internals.** Grep the text layer for `file://` and for absolute source paths. Headless
  `--print-to-pdf` stamps browser chrome unless `--no-pdf-header-footer` is passed, and a document
  that prints its own build path on its face exposes the machine it was built on.

A **recurring** artifact needs a second gate class that runs on its CONTENT, because the checks above
only prove it rendered. For any card that carries claims, prices, deadlines or a countdown:

- **Freshness — a source can be real and the number still stale.** Presence of a citation proves the
  citation exists; it says nothing about whether the figure is current. Require a DATE inside the
  source on every price/rate/market line, set an explicit staleness limit, and refuse past it. A
  confidently-sourced stale figure is *more* dangerous than an unsourced one because it reads as
  verified. Scope the rule to price-bearing lines or legitimate monthly series will false-fail every
  run.
- **Never store a countdown — compute it at render.** A day-count written into prose or a field is
  frozen at authoring time: it does not error, it just keeps saying the old number. Store the target
  DATE, compute the delta at draw time, let prose cite dates, and expire passed events out of the
  pool. Guard the false positive — a historical or deep-time figure is a fact, not a clock.
- **Prove the gate can refuse before you trust it.** A gate that only ever says PASS is
  indistinguishable from no gate. Keep a companion suite of deliberately-broken inputs that MUST be
  rejected *plus* at least one legitimate input that must still pass — the passing case is the
  false-positive guard. On a HOLD, fix the content; never lower a threshold to pass. The pressure to
  relax a gate peaks exactly when it is doing its job.

Full ladder, the freshness and countdown rules, and the negative-control suite pattern:
`references/content-gates.md`.

**Why the order matters:** a gate that runs inside the build fails loudly and cheaply; the same check
performed later by eye costs a round-trip and is easy to talk yourself out of.

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

## 4c. Internal-audience artifacts — keep the vocabulary, stamp the status

When the reader is the sovereign himself and the subject *is* his own system, the
"no internal vocabulary" rule inverts. Organ names, floor IDs, canonical verb names and
drift findings are the entire payload; stripping them out destroys the artifact. Diagram
the architecture in its own terms — the reader is the person who named those terms.

What such an artifact owes instead is its **epistemic status, rendered on its face** —
not only in the chat message that carries it:

- **Stamp non-ratified assessments in the frame.** An artifact built from an assessment
  the kernel did not authorize carries that status where it will be read next to the
  content — `NOT F13-RATIFIED`, `OBSERVE_ONLY`. An unstamped architecture diagram gets
  forwarded and cited as though it were the decided architecture.
- **Source external figures as rendered text, with version and date** (`v0.20.1`,
  `v0.21.3 (14 Sep 2026)`). A diagram is the easiest place for a remembered number to
  become a permanent one, and the hardest place for a reader to check it.
- **The frame and the message must agree.** A hedge that lives only in the chat text does
  not travel with the image. Frame the claim once, then state it in the artifact.

## 4d. Artifacts read by more than one person — select on private context, never disclose it

When an artifact goes to a shared surface — a group, a partner, a family member — the privacy
question is not whether you may *use* what you know. It is whether the reader can infer *why* an item
was chosen.

**Memory informs SELECTION; it must never create EXPOSURE.** Use what you know to decide what is
relevant. Never reprint the evidence, and never write a causal clause that explains the choice
(``because you told me...``, ``after what happened with...``). The artifact is a product of the
knowledge; it is not a report about it.

- **Only what is already public, or stated on the shared surface itself.** Nothing a third party said
  in confidence; no health, money, family or private-deadline detail — even if the user would not
  personally mind.
- **The safety test, applied per line:** could the OTHER reader see this without learning something
  they were not meant to know? If no — rewrite it generally, substitute a public signal, or drop it.
- **Enforce the boundary in CODE, not in the prompt.** Give each item an audience field and have the
  renderer filter it. A rule that lives only in an instruction is skipped exactly on the busy day it
  matters. Measured: a shared card was about to print a personal departure date that only ONE of the
  two readers had been told; the renderer's audience filter caught it and the writer's prompt had not.
- **Never let the machine be the first to disclose.** A detail the user has not told the co-reader is
  his to reveal, on his timing. Surfacing it inside a pleasant digest does not make it less of a
  disclosure.
- **Do not model the bond.** Witness the shared surface and stop there; inferring what the
  relationship means, or ranking one person's importance from activity counts, is a claim the
  evidence does not carry.

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
- **When he names a count, it is a CEILING, not a target.** "Max 2 PNG" means two,
  not two plus a chart plus a source table plus a spare variant. Ship inside the
  budget; if the content genuinely cannot fit, say so and let him raise it.
- **Chrome `--screenshot` captures exactly the window height** — too short clips
  the bottom, too tall ships a dead band. Render well above any realistic content
  height and auto-crop the trailing background rows, so one height is correct for
  both a short and a long layout. Helper: `references/balance-card.md`.
- **A structural element drawn in the same colour as what it sits on is
  invisible.** Dots, badges, dividers and counters placed on a filled shape must
  contrast with THAT shape, not with the page. Derive the colour from its
  container in code so it cannot be got wrong by hand.

## 6. Delivery conventions

- `MEDIA:/absolute/path` alone on its line; the platform decides photo vs file.
- Voice: append `[[audio_as_voice]]` on its own line.
- Multiple artifacts: one `MEDIA:` line each, and name them in the body so the
  user knows what arrived.
- Save into the workspace directory so it can be re-sent later without
  regenerating.

### Audience order — his DM before any group

When an artifact is destined for a shared group, render it, deliver it **to his own DM first**, and
wait for his read before publishing it anywhere else.

The failure is not that the group saw it — it is that he lost the chance to reject it. A shared
group cannot un-see an artifact, and his correction then arrives after the fact instead of before.
Preview and publish are different acts; the cheap order is **preview → his verdict → publish**.

### Pushing to Telegram from a scheduled job

- **`hermes send -t <target>` requires the `telegram:` prefix.** A bare numeric chat id returns
  `Unknown or unregistered plugin platform: <id>` and exits 0 — a false success. Use
  `telegram:<chat_id>`, and read the JSON result for `"success": true` plus a `message_id` rather
  than trusting the exit code.
- **`deliver: origin` can silently resolve to the BOT's own chat, not the human's DM.** A job created
  from an agent context may capture the bot's chat_id as its origin, so it *looks* configured while
  every delivery goes somewhere the user never reads — with no error surfaced. Set an EXPLICIT
  target on any human-facing job and re-read the stored job to confirm it persisted.
- **Verify the destination against the identity lock, not a hardcoded list.** `/root/.hermes/IDENTITY_LOCK.json`
  already declares which ids are humans, groups and bots; a literal allow-list goes stale the moment
  a human's id changes. Refuse (fail closed) when the lock cannot be read — "I could not check" is
  not "it is fine". This also catches the mirror bug of a correctly-formed id aimed at the WRONG
  person.
- **Enumerate EVERY scheduler surface before adding a recurring artifact — or declaring one
  redundant.** This host runs several cron stores for different agent runtimes, plus systemd timers,
  `/etc/cron.d` files and a user crontab. Each is invisible from inside the others, so "there is only
  one briefing job" is a claim about the surface you happened to read. List them all before
  scheduling, and again before declaring a duplicate removed. Note especially the trap of a job whose
  schedule has long passed but whose `enabled` flag is still true: it is dormant, not dead, and it
  wakes the moment its runtime restarts — adding deliveries nobody planned. Probe for a job that has
  actually FIRED, not for a job that is merely marked enabled.

### Sealing a deliverable — two hashes, two homes

When an artifact carries a claim of integrity, split the digest in two, because a file cannot contain
the hash of its own bytes:

- **Content hash — printed inside the document.** Taken over the template *before* placeholder
  substitution, so it proves the words were fixed at build time.
- **Artifact hash — written to a sidecar beside the file** (`<name>.sha256`, verifiable with
  `sha256sum -c`). This is the one that proves the delivered bytes are the built bytes.

State in the document which hash is which, and give the reader the exact verification command.
A bare digest pasted into the chat message is not a seal — it is a number in a conversation that
nothing can be checked against.

**Chain successive editions.** Record `{edition, content_sha256, artifact_sha256, chain_prev}` in an
append-only ledger, where `chain_prev` is the previous edition's `artifact_sha256`. Edition *n+1*
cannot then be substituted without breaking the chain, and the ledger turns a pile of artifacts into
an ordered record. Verify the linkage by rendering twice into a scratch ledger and asserting
`rows[1].chain_prev == rows[0].artifact_sha256` — do not assume the plumbing works.

**Label the authority truthfully.** Lane-level integrity is not constitutional ratification. If the
kernel did not grant a SEAL, the artifact says so on its face (`NOT F13-RATIFIED`) rather than
inheriting the stronger word from habit.

## 7. Support files

- `references/pil-text-poster.md` — building a text-dominant single-page graphic:
  geometry constants, the build-time overflow check that catches what the vision pass
  would only discover, tracked/right-aligned text, grid furniture, and the
  build → measure → look → fix order of operations.
- `references/generated-scene-recipe.md` — prompt skeleton for generated human
  scenes, the composition rules that stop fused anatomy, and the vision-based
  verification harness (author ground truth → read back on a different lane →
  per-lane WORKS / PARTIAL / BLIND / FABRICATES verdict).
- `references/pdf-artifact-audit.md` — auditing a delivered PDF: page fragmentation
  from a slide/page box mismatch, browser-chrome leakage, ink-coverage triage,
  squashed rasters, orientation / scale / legend consistency, citation verification.
- `references/balance-card.md` — presenting TWO subjects as EQUALS: why not to chart
  them to scale, taijitu SVG geometry, the dot-contrast trap, the render-tall-then-crop
  helper, and the label-ambiguity guard.
- `references/content-gates.md` — gating a recurring artifact's CONTENT: the gate ladder,
  freshness (a real source can carry a stale number), why never to store a countdown,
  ranking by consequence, and the negative-control suite that proves a gate can refuse.
  Read before building or auditing any card that repeats.
