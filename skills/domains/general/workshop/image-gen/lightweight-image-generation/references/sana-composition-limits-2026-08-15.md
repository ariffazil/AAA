# SANA Free-Tier Composition Limits — 2026-08-15

Session: user asked for a multi-element scene — muscular Malay "alpha abang sado" in an
unbuttoned white shirt, on a throne, pointing an index finger to choose one worshipper
from a waiting/kneeling line.

## What happened lane by lane

| Lane | Result |
|------|--------|
| Qwen Token Plan (wan2.7-image-pro) | `code: Throttling.AllocationQuota` — quota exhausted |
| MuleRouter Wan 2.6 T2I | HTTP 402 `Insufficient balance` (-0.7476 credits) |
| MiniMax image-01 (mmx) | API error HTTP 404 (endpoint down) |
| Pollinations free GET | Survived — always SANA |

Only the last one produced pixels, and it could not hold the full concept.

## Key empirical finding: `model=flux` is ignored on the free GET

Every `image.pollinations.ai/prompt/...?model=flux` call came back as SANA.
Proof via `file`:

```
$ file out.jpg
JPEG image data, Exif standard: [TIFF image data, little-endian, ... manufacturer=sana, ...] baseline, 665x886
```

Requested width/height are ignored too (always 665x886). So on the free tier the
correct expectation is "SANA at 665x886" — not FLUX at the requested size.

## SANA multi-element behavior (7 attempts, varied prompt structure)

Repeated failures to hold 3 simultaneous concept elements (open shirt + pointing
finger + waiting crowd). Typical outcomes:

- s7:  shirt buttoned, no crowd, no pointing (worst)
- s21: shirt OPEN over bare chest + throne correct — but no pointing, no crowd (best)
- s33: partial, crowd missing, pointing off
- s5:  crowd line present, but shirt buttoned again + no pointing
- s11: POV attempt — shirtless (no shirt), pointing wrong
- s3, s77: concept drifted

Prompt-element ORDER had a real effect — moving a desired element earlier made it
more likely to survive — but 1-2 of 3 was the ceiling, never all three.

## Working mitigations

1. **Most important element FIRST** in the prompt.
2. **Swap composite → POV framing** is unreliable for SANA too (POV attempt still lost elements).
3. **5+ seeds + vision_analyze to pick the best partial** — always QC what actually landed before presenting.

## Decision rule

For a concept needing 3+ simultaneous, interacting elements, SANA free is the wrong
engine — route to a paid lane (MiniMax/Wan/GPT) that holds full composition, or be
honest that the deliverable will be degraded.

## Honesty pattern (Arif)

Don't ship a wrong-concept image presented as if it matched. State what each lane
returned, offer: accept best partial / wait for paid-lane recovery / keep iterating.
Arif explicitly values "aku tak nak hantar hang benda separuh-hati" as the ethic here.