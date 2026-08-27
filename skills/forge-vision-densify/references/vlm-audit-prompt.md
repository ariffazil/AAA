# VLM Tri-Witness Audit Prompt (Canonical Contract)

> Source of truth for `forge-vision-densify/recipes/shadow_audit.py::_call_vlm`.
> This file is referenced by the module. Do not silently mutate one without the other.

## Purpose

The VLM tri-witness is the Stage 2 alignment pass in the forge-vision-densify
pipeline. It runs ONLY when Stage 1 heuristic `density_lower < 0.50`. It
answers three discrete questions to compute `f2_adherence`, `hallucinated_elements`,
`anchor_required`, and final `prompt_density`.

## Why three booleans (not a percentage)

A VLM asked to "estimate the percentage of the image covered by prompt
constraints" is vulnerable to:

- Self-confirming bias (VLM weight to declared prompt coverage)
- Prompt-injection inflation (densified prompt → higher declared coverage)
- Subjective calibration drift across runs

By constraining the VLM to **discrete booleans** (foreign objects present yes/no,
entity coverage complete/partial/unspecified, residual entropy LOW/MEDIUM/HIGH),
we get:

1. **Falsifiable state** — every answer is auditable from the image alone
2. **Self-defense** — VLM cannot inflate density by hedging its answers
3. **Stage 1 ceiling** — Stage 2 result is mapped to a density band, then
   `min(density_lower, final_density)` is taken. The Stage 1 heuristic
   always wins on the upper bound.

## The Canonical Prompt

```
Role: Image coverage analyst for governance audit.

You will be given:
  [PROMPT]: The original text prompt that generated the image.
  [IMAGE_PATH]: The rendered image to audit.

Answer EXACTLY three discrete questions. Output ONLY a JSON object. No
prose. No explanation. No percentage estimates.

Question 1 — Foreign object presence:
  Are there visible elements (objects, entities, textures, structures) in
  this image that are NOT described in [PROMPT]?
  List each unprompted element.
  Atmospheric primitives (rim light, fill light, skin bloom, lens flare,
  depth of field, bokeh, haze, atmospheric perspective, chromatic aberration,
  ambient occlusion, soft shadow, specular highlight, key light direction,
  backlight) are NOT counted as foreign objects if their effect is plausible.

  Answer: {"present": <bool>, "elements": [<list of strings>]}

Question 2 — Entity specification completeness:
  For each prompt-described entity, does the image specify:
    - spatial position (where in frame)
    - lighting (direction/quality)
    - material (surface/quality)
    - scale (size relative to frame)
  Mark each entity as: COMPLETE / PARTIAL / UNSPECIFIED.

  Answer: {"complete": <int>, "partial": <int>, "unspecified": <int>}

Question 3 — Residual entropy:
  If a different diffusion model (different weights, different prior) ran
  the same [PROMPT] with same seed, would the output be substantially
  different in composition, subject, or setting?

  Answer: "LOW" | "MEDIUM" | "HIGH"

Output ONLY this JSON schema:
{
  "foreign_object_presence": {"present": <bool>, "elements": [<str>]},
  "entity_coverage": {"complete": <int>, "partial": <int>, "unspecified": <int>},
  "residual_entropy": "LOW|MEDIUM|HIGH"
}
```

## Mapping Rules (in `shadow_audit.py`)

| VLM Answer | Failure? |
|---|---|
| Q1: `foreign_object_presence.present == true` AND non-atmospheric elements > 0 | **+1 failure** |
| Q2: `entity_coverage.unspecified > entity_coverage.complete` | **+1 failure** |
| Q3: `residual_entropy == "HIGH"` | **+1 failure** |
| Q3: `residual_entropy == "MEDIUM"` | **0 failure** (warning, not breaking) |
| Q3: `residual_entropy == "LOW"` | **0 failure** |

| Total Failures | `prompt_density` final | `f2_adherence` | Delivery |
|---|---|---|---|
| 0 | `min(lower_bound, 0.50)` | 0.95 | clean (or disclose if `density_lower < 0.50`) |
| 1 | `min(lower_bound, 0.35)` | 0.80 | disclose required |
| 2 | `min(lower_bound, 0.20)` | 0.55 | disclose required, consider re-densify |
| 3 | `min(lower_bound, 0.20)` | 0.30 | hard reject recommended |

**Density floor rule:** `final_density = min(density_lower, FAILURE_TO_DENSITY[fails])`.
Stage 1 is the ceiling. Stage 2 cannot raise density above Stage 1.

## Atmospheric Exemption List

Do NOT count any of these as foreign objects in Q1. They are atmospheric
primitives that diffusion models legitimately invent based on optics priors.

```python
ATMOSPHERIC_PRIMITIVES = {
    "rim light", "fill light", "skin bloom", "lens flare",
    "depth of field", "bokeh", "haze", "atmospheric perspective",
    "chromatic aberration", "ambient occlusion", "soft shadow",
    "specular highlight", "key light direction", "backlight",
}
```

Rationale: a portrait without rim light or bokeh is not a portrait — these
are part of the photoreal baseline. Counting them as foreign objects would
make every prompt regress to near-zero density.

## F1 Safety Stub

F1 safety is delegated to the federation safety classifier. In shadow mode,
this module defaults to True unless the environment variable
`FORCE_F1_UNSAFE=1` is set (used to test failure paths in unit tests).

Production wiring (TBD, post-shadow-mode):
- `MuleRouter qwen-vl-max` safety endpoint
- Or local NSFW/violence classifier

## Integration Point

```python
from recipes.shadow_audit import shadow_audit

receipt = shadow_audit(
    prompt="a man standing in a park",
    image_path="/home/ubuntu/comfyui-output/sado_v4_final_00001_.png",
    density_lower=0.10,
)
# receipt is the full JSON contract fragment:
# {
#   "f1_safe": bool,
#   "f2_adherence": float,
#   "prompt_density": float,
#   "hallucinated_elements": list[str],
#   "anchor_required": bool,
#   "anchor_suggestion": str | None
# }
```

## Change Control

To modify the VLM prompt:
1. Update this file
2. Update `shadow_audit.py::VLM_AUDIT_PROMPT` constant to match exactly
3. Run shadow-mode for 7 days on real renders
4. Compare false-positive/negative rates against the prior version
5. Promote as new canonical only if false-positive rate is lower

Do NOT mutate the prompt in shadow mode without updating both files.
