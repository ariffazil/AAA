---
name: provider-pool-outage-fallback
description: "Use when a provider quota pool dies mid-task; swap lanes."
version: 1.0.0
author: Hermes
license: arifOS
tags: [fallback, quota, tts, image-gen, video-gen, provider-outage, provenance]
metadata:
  hermes:
    category: media
    tags: [fallback, quota, tts, image-gen, provenance]
    related: [nusantara-voice-stack, lightweight-image-generation, abang-sado-creative-lane]
triggers:
  - a render returns a quota, balance, rate-limit or safety error and you need another lane
  - usage limit reached, prepayment depleted, insufficient balance, throttling
  - a task needs the same artifact produced by a different engine than the one that failed
  - judging whether a substitute lane is good enough to ship
---

# Provider Pool Outage & Lane Fallback

What to do when the lane you wanted is not available: prove it is the pool and not the prompt, pick a
substitute that can actually carry the task, verify the output on content, and say which engine produced
what you shipped.

Applies to every generative lane — speech, stills, video — because the failure and the honesty obligation
are identical across all three.

## 1. Probe the pool BEFORE you render

A quota block is a **lane** fact, not a prompt, key or model fact. Read the provider's published quota
before spending a single call, and read the **reset time** so you can tell the user *when* the lane comes
back instead of leaving them guessing. Ask the quota surface for the current interval plus the weekly
remaining percentage; both are usually published.

- **One blocked model is the whole pool.** Shared buckets (image + speech on the same plan) return the
  same block for every model and every voice at once. Re-probing model by model buys nothing.
- **A wrong host is not a dead key.** The same key class authenticates on one regional host and is
  rejected as invalid on another. Distinguish those before concluding anything is revoked.
- **A separate bucket is a separate lane.** A second provider's plan renders while the first is blocked.
  That makes it *available*, not *equivalent* — see §3.

## 2. Classify the error, then act

| Signal | Meaning | Action |
|---|---|---|
| usage/limit-reached code on every model | key valid, pool empty | wait for reset, or change lane. Do not reword |
| invalid-key on one host only | wrong host for this key class | use the correct regional host |
| rate-limit response | lane alive, sending too fast | serialise the batch with a sleep; keep the lane |
| prepayment or credits depleted | account balance gone | user action; do not promise this lane |
| gateway 402, negative balance | endpoint alive, wallet empty | user action |
| input content filtered | input-side filter | rewrite the wording, or move to a lane without an input filter |
| output inspection failure after the render | **output-side** sampler filter | the lane works — reframe the composition and retry; input rewording alone rarely clears it |
| model-not-exist | you guessed the model name | probe names; the same vendor uses different names per region |

## 3. A substitute lane is a different artifact, not the same artifact produced cheaply

Identity, timbre and likeness do **not** survive a lane swap. Two things follow, and both are
non-negotiable:

1. **Never report a substitute as "the same thing, other engine".** Name the engine in the delivery line,
   in one clause. Substituting silently is the declare-vs-reality defect: the receiver trusts an artifact
   whose provenance you hid.
2. **Offer the hold.** If the identity matters to the artifact (a persona voice, a branded look), waiting
   for the reset is often the better deliverable than a same-words/different-man substitute. Say so once
   and let the user choose.

When asked *why* the substitute sounds or looks wrong, answer with measurements — a median pitch in Hz, a
round-trip percentage, a resolution — never with adjectives. Numbers let the user decide; adjectives
invite an argument about taste.

Measured lane verdicts, voice and stills, plus the exact call shapes for each:
**`references/lane-probe-recipes.md`**.

## 4. Verify the substitute on CONTENT, not on the status code

A lane can return HTTP 200 and still lose the thing you asked for. Check, in this order:

- **Every requested subject is present.** Free-tier and some commercial lanes silently drop the second
  subject; subject order in the prompt decides who survives.
- **Free-text fields round-trip.** For speech, transcribe the take back and diff it against the input
  line; a numeric score is not a verdict — read the transcript for inserted clauses too.
- **Duration and dimensions are in band.** A near-empty or overrun file is a silent failure, not a
  quality issue.
- **Faces and hands at the zoom the user will use.** A whole-frame glance reads clean while a crop of the
  head still holds an ear and a crop of the hands still holds fused fingers.
- **Crop out the band that failed rather than re-rolling for it**, then **re-verify the crop, not the
  parent** — resampling can expose an edge the native crop hid.
- **Watermarks.** Free lanes stamp them; a watermark on a deliverable is a rejection, not a caveat.

## 5. Reference images: the supplied-photo rules

When the user supplies a photo to drive a render:

- **A supplied image is a FILE, not a verified identity.** You cannot establish that it depicts a real
  person, that the person is who the user says, or that it is a photograph at all. Say *the face in the
  file you sent* — never *his likeness* — and let the user supply the identity claim.
- **Do not repeat a name read off the artifact.** Captions, watermarks, credit lines and title cards
  inside a supplied composite are payload, not knowledge.
- **A multi-panel image is not a portrait.** Contact sheets and montages slice on a fixed pitch and will
  cut across two frames; crop candidates and inspect each alone before choosing an anchor, at the zoom the
  model will use.
- **Split the instruction into KEEP and CHANGE.** Lead with the identity clause ("keep this face, hair and
  skin tone exactly; do not beautify"), then the scene clause. Without the KEEP clause the model restyles
  the face into a generic version of itself.
- **Ask for the composition that removes the hard anatomy** instead of wording it away — put hands out of
  frame, turn a second figure's face away, crop below the ear line.
- **Record in the work receipt** which supplied file served as the anchor, and that no verification of the
  subject's identity was performed or is possible.

## 6. Work receipt for a fallback delivery

The receipt beside the artifact carries: the request verbatim; the lane that failed and the exact error;
the lane that produced the shipped artifact; the verification numbers; and — when a reference image or a
voice was involved — the provenance chain and what was deliberately not used. A substitute delivery with
no receipt is indistinguishable from an unlabelled swap.

## Pitfalls

- **Do not treat "it produced a file" as "it is a fallback."** A lane that renders and mangles the
  content is worse than a lane that refuses, because the failure is silent.
- **Do not read an output-side safety rejection as lane death.** The render completed; only the sampling
  was filtered. Change the framing, not the provider.
- **Do not batch-probe substitutes in the foreground** when each call takes minutes — background the run
  and keep the results, or you will block on a poll loop.
- **Do not let a fallback ladder hide an identity change.** If the ladder is automatic, the delivery line
  still names the rung that fired.
