# Lane Probes & Substitute Call Shapes

Concrete shapes for checking a pool and driving a substitute lane. Keys come from the environment and are
sent as a Bearer token in the `Authorization` header — never inline a key in a command or a file.

## 1. Is the pool actually empty?

Ask the provider's quota surface for the current interval window and the weekly remaining percentage.
Typical shape: a quota subcommand against the media base URL, returning per-model entries with
`current_interval_status`, `current_interval_remaining_percent` and `current_weekly_remaining_percent`,
plus epoch start/end for both windows. Convert the epoch end to local time and quote that to the user as
the return time. Do not probe individual models or voices: on a shared bucket they all fail identically.

## 2. Voice substitutes (measured, one 84-char BM line, male register)

| Lane | BM word round-trip | f0 median | Verdict |
|---|---|---|---|
| Primary provider clone (preferred voice) | clean after alias normalisation | ~96 Hz | the take |
| Free OS TTS, male BM voice | 98.2 % | ~157 Hz | words survive; **timbre is a different man** |
| Second provider, base TTS model | **0 %** — read the system instruction aloud instead of the line | ~203 Hz | unusable |
| Second provider, voice-design variant | **38.5 %** (`Ada`→`Ida`, `tulis`→`gulis`) | ~91 Hz | male register holds, words collapse |

Rules that fall out of the table:

- The second provider's plan is a separate bucket, so it renders while the primary is blocked. Available
  is not equivalent: 38.5 % is far below the 85 % ship floor.
- The fastest free substitute (the OS TTS voice) keeps the words and loses the identity. Ship it only with
  the engine named, and offer to hold for the reset.
- Rate/pitch flags on the OS TTS tool: use the `--pitch=-15Hz` form (a space-separated value errors as a
  missing argument) and step the rate toward positive values if the read drags.
- A second-provider TTS call is not a REST audio endpoint; it goes through the chat-completions surface
  with the audio modality requested and the spoken text placed in the assistant turn, returning base64
  audio. Build the request body as a file rather than inlining it.

## 3. Stills substitutes

**Async submit + poll (text-to-image).** POST to the intl image-synthesis path with an async-enable header
and a body of `{model, input:{prompt}, parameters:{size, n}}`; take `output.task_id`, poll the task path
until `task_status == SUCCEEDED`, then download each `output.results[].url`. This lane accepted a
chest-forward two-figure brief that other lanes refused and returned 960×1280 — the most usable stills
substitute measured. Do not submit a whole batch at once: it rate-limits, so serialise with a sleep.

**Reference-image edit (sync).** POST to the multimodal-generation path with the edit model name; the body
is `input.messages[0].content = [{"image": <data-url>}, {"text": <instruction>}]` — an inline
`data:image/jpeg;base64,…` needs no hosting step. Read the result at
`output.choices[0].message.content[0].image` and download immediately (the URL is signed and expires).
`parameters.watermark:false` and `parameters.negative_prompt` both work. Output size is fixed regardless of
the input aspect ratio — crop afterwards.

**Edit-model names are region-specific.** One host answered a model-not-exist error for three plausible
edit names while a fourth worked. Probe names rather than guessing, and never conclude the lane is down
from a name mismatch.

**Workers-AI / serverless image models.** A fast text-to-image model here is cheap and always up, but
frequently rejects shirtless or subject-contact prompts on the input side and, where it does render, tends
to drop the second figure. The dev-tier image model has no route at all; the SD1.5 img2img model is not
enabled for every account; the SDXL base model expects a binary image part rather than a JSON field. Treat
img2img on this route as account-dependent, not as a general fallback.

**Free public text-to-image.** Single-subject by design (the first-mentioned subject survives a drop),
with an explicit multi-element ceiling, and it stamps a visible watermark. Drafts only.

**Third-party gateways** fail as a payment error on every model on that gateway, not on one — check the
balance before selecting a model there.

## 4. Video

Video pools are usually separate from image/speech, so a blocked stills lane does not imply blocked video
and vice-versa — check the video entry in the same quota response before planning around it. When the video
pool is out, a slow push-in montage over stills plus the audio track is a legitimate deliverable for a
narrative beat; declare it as such rather than presenting it as generated motion.

## 5. Two-figure composition recipe that survives substitutes

1. Compose **from behind or from the side, never from the front** when one figure must stay unidentifiable
   — moving the camera further back is the lever; moving it round to the front leaks profiles.
2. Name the second figure's build, hair and clothing explicitly; an under-specified companion gets
   invented, usually with a visible face and a default sex.
3. Wrap arms so the hands disappear behind a body, or crop the frame above the lower hand.
4. QC in this order: faces and ears, then hands, then subject count, then size relationship, then
   watermark.
5. Crop the passing band and re-verify the crop.
