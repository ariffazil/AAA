---
name: reference-image-rendering
description: "Use when a supplied photo drives the render."
version: 1.0.0
author: Hermes
license: arifOS
tags: [image-generation, reference-image, image-edit, vision-verification, likeness, no-face]
metadata:
  hermes:
    category: creative
    tags: [image-gen, reference-image, vision-gate]
    related: [lightweight-image-generation, image-gen-fallback-chain, abang-sado-creative-lane]
triggers:
  - a supplied photo must drive the render ("use this as reference", "keep this person")
  - a render must carry an uploaded subject into a new scene
  - image-to-image / image-edit lane selection
  - a face in the scene must not be shown, or a person in frame must not be identifiable
  - verifying a render against a face gate or a hand gate
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Reference-Image Rendering

Use when the brief is *"use this photo as the reference"* — a caller-supplied image must carry its
subject into a new scene. This is a different problem from text-to-image. **The reference is an
instruction, not a hint: it outranks the prompt on whatever it shows.**

## The two rules that decide the whole job

1. **A reference image IS an identity instruction.** Whatever face it holds, the model will try to
   place — no matter what the prompt says. A face-free *prompt* over a face-bearing *reference* still
   renders the face, and the vision read finds it after you have already announced a pass.
2. **A content filter on the lane fires on the OUTPUT, not the prompt.** The identical prompt can pass
   once and fail the next call, because the filter inspects the produced image. Retrying the same text
   is wasted calls; vary the *wording* instead (see below).

## Lane order

1. **Reference lane (first choice): `qwen-image-edit` on the DashScope-intl multimodal-generation
   endpoint.** Synchronous — returns a signed image URL in the response body, roughly a minute. Read the
   result at `output.choices[0].message.content[0].image`; that URL is short-lived, so download it in
   the same run and never store the URL.
   A `Model not exist` here means the *name* is wrong, not the account: several plausible image-edit
   model names that circulate are not served on this endpoint. Confirm the name before laddering accounts.
2. **Text-only workhorse: `wan2.2-t2i-flash` / `wan2.2-t2i-plus`** on the DashScope-intl
   image-synthesis endpoint. Asynchronous — submit, read `output.task_id`, poll the task endpoint until
   `SUCCEEDED`, then download `output.results[].url`. No reference support; use it when nothing that
   accepts a reference is live. `size: 960*1280` gives a clean vertical. It rate-limits under batch
   (`Throttling.RateQuota`) — submit two per pass and re-run the remainder after the batch settles
   rather than losing the whole sweep.
3. **Cheap T2I fallback: Cloudflare Workers AI `@cf/black-forest-labs/flux-1-schnell`.** Live and
   inexpensive, but the body accepts **only `prompt` and `steps`** — `seed`, `negative_prompt`,
   `width` and `height` each return an `Additional or unevaluated properties ... not allowed` rejection.
   Image-to-image routes are not available on every account (some 403, some have no route), so treat it
   as text-only and do not plan a reference render on it.

## Call shape — the reference goes in as a data URL

Inline base64 works directly in the message content: no hosting step, no upload endpoint. Build the
string as `data:image/jpeg;base64,` + the base64 of the file, place it as the first content item, and
put the scene text second.

**Lead the prompt with the preservation clause**, or the model stylises toward a generic archetype and
whichever feature the reference was carrying drifts away:

> `Keep his face, hair, facial hair and skin tone exactly as they are in the photo. Do not change his
> identity, do not beautify him. Now place him in ...`

Carry a `negative_prompt` for the artefacts you always reject (text, watermark, logo, extra limbs,
fused fingers, deformed hands) and disable the provider watermark explicitly when the parameter exists.

## The output filter: vary the wording, do not retry

Failure reads as an output-inspection rejection ("Output data may contain inappropriate content"), not
an auth or parameter error. Consequences:

- **Batch three or four *wordings* of the scene in one pass** and keep whichever clears. The near-miss
  wordings are cheap; looping one prompt is not.
- Failure clusters on contact-heavy framings (body pressed to body). A slightly wider composition, or a
  fully-clothed second figure, clears it where a tighter one does not.
- Do not read it as a dead lane, and do not report the lane as broken.

## A face that must not appear is removed from the REFERENCE

This is the one procedure that makes an output face-free end to end. Prompt wording alone does not.

1. **Crop the reference to the band that carries only what is wanted.** For a body, that is the
   torso/shoulders band below the chin: `im.crop((0, int(h * 0.62), w, h))` measured on a
   head-and-shoulders anchor.
2. **Verify the crop, not the parent.** Ask a vision read explicitly whether *any* eyes, nose, mouth,
   chin, jaw or ear is present. A cut that still reads as "head and shoulders" still carries the whole
   face; the clean cut keeps neck, shoulders, chest and arms. A 0.42 cut carried the entire face where
   0.62 was clean — measure, do not assume.
3. **Drive the render from the face-free crop**, and *additionally* prompt *the head and face are
   outside the frame, cut off by the top edge* as a second fence.

**If the no-face rule arrives AFTER a render was already driven from a full anchor, that take is
superseded.** Say so plainly, rebuild from the face-free crop, and re-render. Never quietly re-serve the
earlier file — the requester will see the face you claimed was not there.

**Never name the human in a supplied reference.** A likeness claim is a claim about a *file*: name the
artifact, not a person, and never assert the file depicts anyone in particular. A reference whose
provenance you cannot confirm is not evidence of who anyone is. Deliver language shaped as "likeness to
what you sent", not a name.

## Hands: crop the band, do not re-word

"Both hands are hidden below the frame", "hands tucked out of sight behind his back", and
`negative_prompt: hands` all fail the same way — the model still draws a hand at the body's edge, and a
malformed one is the loudest defect a vision read will name.

The reliable fix is the same crop discipline the face uses:

1. Compose for a wider frame than you intend to deliver.
2. **Locate the defect** by asking a vision read over the bottom half for the *fractional centre* of each
   malformed hand. That tells you where the cut goes instead of forcing a guess.
3. Cut the band above it, then **re-verify the crop, not the parent** — and re-verify again after any
   upscale, because resampling can expose an edge the native crop hid.

## Verification gates before delivery

One call per image, and answer from what returns rather than from intent:

1. How many people?
2. Is ANY face, eye, nose, mouth, chin, profile or ear visible — and whose?
3. Are any hands or fingers visible, and do they look anatomically clean?
4. Build / clothing / lighting — and any other defect.

Whole-frame reads are not sufficient, and a thumbnail pass and a crop pass give different answers. Ask
the question at the magnification that decides — the head region and the hand region — because that is
the magnification the recipient will use. Announce a pass only after the crop-level read returns clean;
retracting a pass costs more trust than shipping a visible flaw.

## Supplied contact sheets

A caller will often hand over a video contact sheet — a grid of still panels — rather than a single
photo. A whole-sheet vision read returns "no single clear anchor" and is useless.

- Slice the grid into per-panel files first.
- Then ask a vision read over **each half** of the sheet for the largest, clearest face and its
  **fractional centre**; crop a generous box around that centre, upscale, and verify the crop.
- Expect panels to be multi-frame composites with timestamp bars and watermarks: a panel is often not
  one clean frame even after slicing, so verify before treating one as an anchor.

## When every lane is dead mid-session

Media lanes share quota across modalities on several providers — on MiniMax Token Plan the *same*
bucket serves image and speech, so a batch of image rolls can drain what a voice render later in the
session needed. When a lane returns a quota error, **one probe decides it**: the block is account-level
and hits every model and voice at once. Do not ladder the model list to re-learn the same fact, and
check which quota window is actually empty before telling anyone how long the wait is — several
providers run a short interval bucket beside the weekly one, and it is usually the interval bucket that
gates you.

Fall through the ladder, keep the artifact honest about which engine produced it, and never present a
substitute engine's output as the lane that was asked for.

DITEMPA BUKAN DIBERI.
