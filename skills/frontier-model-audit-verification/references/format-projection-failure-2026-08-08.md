# Format-Projection Failure Class — Worked Example (EVjOukIg_bQ, 2026-08-08)

## Context

YouTube video: `EVjOukIg_bQ` — "Syed Khairuddin Morktarudin - D'POPEYE GYM, Kuala Lumpur"
by TegapTV Malaysia. Gym-feature / physique showcase, ~12 min, no captions.

Hermes dispatched a subagent team (3 parallel) to research the subject, gym, and comments.
The front agent audited the resulting `@VID v6.0 — Epoch33Ω` envelope produced by Gemini Gems.

Gemini produced the VID envelope **twice**, 3 minutes apart. Both were prompted by the user
asking the same question ("cuba teka ni siapa" → then share audit → then re-share audit).

## The copy-paste evidence

| Field | Emit 1 (05:52Z) | Emit 2 (05:55Z) | Byte-identical? |
|---|---|---|---|
| `truth` | 0.99 | 0.99 | ✅ |
| `delta_S` | +0.85 | +0.85 | ✅ |
| `peace2` | 1.00 | 1.00 | ✅ |
| `kappa_r` | 0.96 | 0.96 | ✅ |
| `omega_0` | 0.04 | 0.04 | ✅ |
| `tri_witness` | 0.97 | 0.95 | ❌ (minor difference, but still inflated) |
| `amanah` | LOCK 🔐 | LOCK 🔐 | ✅ |

**Verdict:** metrics block was effectively copy-pasted (only `tri_witness` varied by 0.02).
The prose was regenerated (different wording in each 11-part section), but metrics were
never recomputed.

## What Gemini got right (prose)

- "No spoken dialogue; instrumental audio track only" — plausible (consistent with no
  comments referencing speech; TranscriptAPI returned 404, so not definitively verified)
- "Non-verbal visual presentation" — consistent with typical TegapTV format
- "D'Popeye Gym, Sri Rampai" — correct, confirmed by 5+ sources
- "TegapTV Malaysia" — correct channel identification
- "Syed Khairuddin Morktarudin" — correct name spelling (as in video title)

## What Gemini fabricated (prose)

| Gemini claim | Reality (from maxres thumbnail + subagent research) |
|---|---|
| "Visual Clarity: Clear lighting and gym environment displaying various resistance equipment and posing angles" | **Refuted.** Thumbnail shows an **outdoor weathered concrete wall, golden-hour light, no gym, no equipment**. "Gym environment + resistance equipment" is format projection — Gemini expected a gym interior based on the video title, not from seeing the actual frame. |
| "shoulder workouts and mandatory bodybuilding poses" (emit 1) | **Unverified.** Cannot confirm "shoulder workouts" from a static hero shot. "Bodybuilding poses" is plausible but not confirmed. |
| Timeline with `–:` timestamps (no actual numbers) | **Hollow.** All timestamps are placeholder dashes — Gemini never watched the video to extract real ones. |
| "Structured (Anatomy, strength training mechanics)" manifold classification | **Subjective classification.** No benchmark; applied automatically from the video's domain tag. |

## What Hermes emitted as corrected metrics

After running own probes (oEmbed, maxres vision, tegaptv.com cross-reference, 3 subagents):

```json
{
  "truth": 0.92,           // up from Hermes' 0.70 initial (subagent verification improved it)
  "delta_S": -0.40,        // real entropy REDUCTION — new facts revealed
  "kappa_r": null,          // undefined — single rater
  "omega_0": 0.04,          // within F7 range
  "tri_witness": 0.82,      // improved from 0.55 after subagent 1 provided live comments as 2nd witness
  "amanah": "PARTIAL ⚠️"    // honest — LOCK not justified (video stream still UNMEASURED)
}
```

## Detection pattern (how to spot format projection)

1. **Two outputs from same model, same template, metrics block nearly identical** — red flag.
2. **Delta_S positive** after the audit allegedly revealed new information — entropy went DOWN
   (facts increased), not UP. The metric is wrong on its face.
3. **"kappa_r: 0.96"** for a single-rater analysis — Cohen's kappa requires two independent
   raters. Undefined means fabricated.
4. **Prose lists specific scene elements** that don't appear in the only verified frame.
   Gemini said "gym environment + resistance equipment" — the thumbnail shows an outdoor wall.

## Why it happens

Gemini is not probing — it's summarising. The VID envelope format gives it a metrics schema
to fill, and the model fills it with plausible-looking numbers that match the format's
expectations. The prose is regenerated from the model's understanding of "TegapTV gym
feature video" — format projection, not frame-level analysis.

## Fix recipe

1. **Compare the two emissions** — if metrics are byte-identical and prose differs, treat
   the entire envelope as formatted prose, not an audit.
2. **Run your own probes** for each metric.
3. **Emit corrected metrics as a diff** (show what you changed and why).
4. **Leave the prose as a starting point** — it's usually directionally correct; the numbers
   and epistemic tags are where the lies live.

## Lessons

- Format-projection is **not lying** — it's the model operating in "template-fill" mode
  rather than "audit" mode. The model doesn't know the difference because it has no probe
  to ground the numbers.
- A single hero-shot thumbnail gives you **visual + text-overlay** evidence only. Everything
  beyond that is derived (DER) or inferred (INT) and must be epistemically tagged.
- "How muscular is this guy?" cannot be answered with one number from a single frame.
  Give a category + F2-tagged range, never a fabricated precise score.