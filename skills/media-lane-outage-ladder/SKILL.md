---
name: media-lane-outage-ladder
description: "Use when a media lane is quota-gated or blocked."
version: 1.0.0
author: Hermes
license: arifOS
tags: [media, image-generation, tts, video, fallback, provider-outage, delivery-integrity]
metadata:
  hermes:
    category: creative
    tags: [image-gen, tts, provider-outage, delivery-integrity]
    related: [abang-sado-creative-lane, nusantara-voice-stack, lightweight-image-generation, generated-media-delivery]
triggers:
  - a render request fails on quota, balance, policy or endpoint error and a substitute lane is needed
  - the primary TTS or image provider returns a usage/credit limit mid-session
  - a provider rejects a prompt as NSFW / policy-blocked after accepting it earlier
  - deciding whether to wait for a quota reset or ship a different engine
---

# Media Lane Outage Ladder

The procedure for getting a requested artifact out when the lane that normally makes it is
gated — image, voice, or video. Covers error classification, the substitution rule, and what
must be said in the delivery line.

This skill is the DECISION PROCEDURE. Per-register prompt craft lives in the register's own lane
skill; exact call shapes for the alternate lanes are in `references/alternate-media-lanes.md`.

## Step 1 — Classify the error before touching another lane

The expensive failure is not a dead endpoint, it is a LIVE endpoint that refuses the work.
Four classes, four different responses:

| Signature | Meaning | Action |
|---|---|---|
| `402`, `insufficient_balance`, "prepayment credits are depleted" | endpoint alive, needs money | skip the lane; do not retry; a top-up is the user's call, never yours |
| quota/limit code on a still-authenticated key (`2056 Token Plan usage limit reached`, `429 Throttling.AllocationQuota`) | endpoint alive, pool empty for the window/seat | read the reset window from the provider's own quota call, then WAIT — do not burn rungs |
| `400 … contains NSFW content`, `code 8007` | endpoint alive, **provider input filter rejects this register** | reword toward the composition the filter accepts (clothed / from-behind) or route to a lane that does not filter; never re-send the same prompt |
| `404`, conn-refused, 5xx, timeout | endpoint down or moved | fall through the ladder |
| `400 Bad input: Additional or unevaluated properties '/…'` | the lane is fine, your request shape is wrong | drop the unsupported field; do not migrate the lane |

Two rules that follow:

- **One probe decides a quota/limit class — do not cycle models.** A per-account limit hits every
  model, every voice and often several endpoints at once. Probing `model-A`, then `model-B`, then a
  system voice is the same error three times, costing time and quota.
- **A lane that renders is not a lane that renders THIS register.** Test the target register with one
  cheap probe before committing a batch. A policy rejection is a lane property, not a transient
  error, and retrying it is pure waste.

## Step 2 — Ladder on capability, not on recency

Pick the next lane by what it can do, and check the seat/key before probing the endpoint: a key that
401s on one host may be valid on the provider's other region, and an exhausted seat is not an
exhausted provider. Then probe cheaply (smallest size, `n=1`, a few words) rather than launching the
full batch.

**A capability you did not test is not absence.** Before declaring a lane unavailable, read its own
docs and send one smoke call; several "dead" lanes turn out to be a params mistake or the wrong host.

## Step 3 — The substitution rule

When you land on a substitute lane, the artifact is not equivalent to the one requested. Both of
these are required:

1. **Re-measure the substitute on the SAME input.** Do not port a previous lane's verdict or
   settings across: speed, calibration and quality do not transfer. Render the probe, run the same
   gate (for voice: ASR round-trip + f0; for image: the register's vision QC), and read the numbers.
2. **Name the engine in the delivery line, and say what is different.** One clause — engine id plus
   the property that changed (timbre, resolution, whether it is upscaled, cropped, or lower fidelity).
   An unlabelled engine swap is the declare-vs-reality defect: the artifact looks like the one asked
   for and is not.

**Offering to wait is a valid delivery.** When the requested artifact depends on an identity the
substitute cannot carry — a persona's voice, a licensed model, a specific seed family — say so, give
the reset time, and offer the hold. Shipping a different voice as if it were the same one is worse
than returning with the real one later.

## Step 4 — What not to do

- Do not re-send a prompt a policy filter already rejected, on any lane, waiting for a different
  answer.
- Do not present a substitute lane's output in the register's own framing when its defining property
  failed (mangled text, wrong timbre, upscaled from a lower resolution).
- Do not report a lane as "dead" from one error, and do not report a lane as "working" from one
  render — both are single-observation claims.
- Do not narrate the outage in the delivery. The requester gets the artifact, the engine name, and
  the one difference that matters.

## References

- `references/alternate-media-lanes.md` — exact call shapes for the cloud lanes that carry registers
  the paid stack gates (Alibaba DashScope-intl Wan T2I, Cloudflare Workers AI FLUX), plus the measured
  voice-substitute table and the failure mode of each.
