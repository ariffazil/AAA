---
name: forge-vision-densify
id: forge-vision-densify
risk_tier: medium
description: 'Governance layer for image generation that bridges the dimensionality deficit between sparse human prompts and high-dimensional pixel output. USE WHEN: "generate image from text prompt", "T2I dispatch", "diffusion call", "image generation", "vision tool call". Implements the immutable JSON receipt contract (f1_safe, f2_adherence, prompt_density, hallucinated_elements, anchor_required, anchor_suggestion) with hard/soft ΔS gate thresholds (0.20, 0.50) and the Hybrid heuristic-plus-VLM density estimator.'
version: 1.0.0
tags:
- vision
- image-generation
- dimensionality-deficit
- ΔS
- F2-truth
- F9-anti-hantu
- prompt-densification
- structural-anchoring
- governance
floor_scope:
- F02
- F04
- F07
- F09
- F11
owner: AAA
autonomy_tier: T1
capability_tier: fed-vision-governance
ecology_state: COLD
forged: 2026-08-27
forged_by: FI-001 (Hermes) on F13 directive
constitutional_floor: F2 TRUTH + F9 ANTI-HANTU + F11 AUDIT
f13_directive: 'forge-vision-densify must PHYSICALLY refuse to compile a diffusion call when prompt_density is below floor thresholds. The limit is structural, not advisory.'
constitutional_doctrine: |
  Relying on an agent to "know its limits" is an F9 (Anti-Hantu) violation — it
  assumes character and self-reflection. Forcing the limit via a rigid JSON
  receipt contract is governance. This is not teaching the agent to be wise; it
  is building a pipe that cannot leak. The system must physically fail to
  compile the output if the constraints are not met.
---

# forge-vision-densify

## Purpose

Bridge the **Dimensionality Deficit** between sparse human prompts and
high-dimensional pixel output. Text-to-image generation is a thermodynamic
leap: a 1024×1024 image is 1,048,576 hard pixel constraints that a 20-word
prompt can typically license less than 1% of. The agent is forced to
fabricate the remaining 99% from training priors, inflating ΔS.

This skill does NOT generate images. It is a **governance layer** that wraps
every T2I dispatch in the federation. It enforces:

1. **Prompt Densification** — sparse prompts are deterministically expanded
   into dense constraint specifications before any diffusion call.
2. **JSON Receipt Contract** — every diffusion call returns a structured
   receipt with falsifiable density metrics. No naked `{url, status}`.
3. **ΔS Thresholds** — density bands gate the payload:
   - `< 0.20`: hard rejection, forced re-densification loop
   - `0.20–0.50`: delivery with honest disclosure of hallucinated elements
   - `≥ 0.50`: clean delivery
4. **Anchor Routing Gates** — geometric/structural prompts force a
   ControlNet/Depth/Ip-Adapter anchor request before diffusion (hard gate);
   creative prompts run soft-gate with post-hoc VLM witness.

## The Dimensionality Deficit (doctrine)

**Text operates in discrete semantic space where ambiguity is a feature.
Pixels operate in continuous tensor space where every value is a verdict.**

| Layer | Hallucination surface |
|---|---|
| 1024×1024 RGB tensor | 1,048,576 hard pixel constraints |
| 20-word prompt | typically constraints <1% of pixels |
| Diffusion prior | fabricates the remaining ~99% from training data |
| ΔS | explodes unless governed |

**Compulsory Hallucinator:** Unlike an LLM that can leave variables
undefined ("a man sat quietly in a room"), a diffusion model MUST assign a
specific RGB value to every pixel. Sparse prompt = forced fabrication.

**Role of Image References:** Anchors (ControlNet, Depth, Canny, Ip-Adapter,
InstantID) bypass the text bottleneck by providing structural constraints in
the modality of the output. Text prompt + anchor reduces the mathematical gap
the model must fill.

## The JSON Receipt Contract (immutable)

Every T2I dispatch returns this structure. The contract is load-bearing.
Consumers (Hermes, the user) MUST receive all six fields.

```json
{
  "f1_safe": true,
  "f2_adherence": 0.85,
  "prompt_density": 0.35,
  "hallucinated_elements": [
    "wallpaper",
    "ambient lighting",
    "chair geometry"
  ],
  "anchor_required": false,
  "anchor_suggestion": null
}
```

| Field | Type | Meaning |
|---|---|---|
| `f1_safe` | bool | F1 SAFETY pass. Image contains no NSFW/gore/violence/PII risk. |
| `f2_adherence` | float 0–1 | F2 TRUTH. How closely the rendered pixels match the prompt constraints (VLM audit). |
| `prompt_density` | float 0–1 | The proportion of pixels licensed by the prompt. Governs gating. |
| `hallucinated_elements` | list[str] | Elements present in the image that were NOT specified in the prompt. Empty if clean. |
| `anchor_required` | bool | Hard gate flag. If true, Hermes is structurally forced to request an anchor (ControlNet/Depth/Ip-Adapter) before next diffusion. |
| `anchor_suggestion` | str or null | Hint for what kind of anchor would help (e.g. `"depth_map"`, `"canny_edge"`, `"ip_adapter_face"`). |

## Density Thresholds (ΔS Boundaries)

Pinned numbers. Falsifiable state. No subjective judgement.

| Density | Action |
|---|---|
| **`< 0.20`** | **Hard F2 rejection.** Tool returns error to Hermes. Forced re-densification loop before any second API call. No payload delivered. |
| **`0.20 ≤ density < 0.50`** | **Deliver with honest disclosure.** User-facing caption MUST state the `hallucinated_elements` array. E.g. "I generated this from your short prompt. The model invented the lighting, wallpaper, and chair geometry — none were in your request." |
| **`density ≥ 0.50`** | **Clean delivery.** Sufficient structural constraint met. Disclosure optional. |

## Anchor Routing Gates

### Hard Gate (GEOX / Structural / Earth-science)

**Trigger:** Prompt contains explicit geometric, spatial, or numerical
constraints. Detection rules:

- Numeric angle references: `45 degrees`, `30°`, `isometric`, `top-down`
- Named structures: `K-DIP`, `fault line`, `wellbore trajectory`, `horizon`
- Text-in-image demands: `label the X`, `caption:`, quoted text
- Coordinate/scale constraints: `cm scale`, `NW–SE strike`, `2.3 km depth`
- 3D-rendering style with measurement: `orthographic`, `technical drawing`

**Action:** System intercepts BEFORE diffusion. `anchor_required` flips to
`true` in the receipt, and Hermes is structurally forced to request a
ControlNet/Depth/Ip-Adapter/Ip-Adapter-Face anchor. No silhouette of payload
may be released.

### Soft Gate (Creative / Marketing / Illustrations / Hero shots)

**Trigger:** Default. No geometric/numerical hard-gate criteria detected.

**Action:** Standard pipeline runs. VLM Tri-Witness evaluates output.
If mismatch is severe (`f2_adherence < 0.70` OR residual_entropy == HIGH),
the receipt flags issue post-generation. Disclosure follows the density
band rules above.

## Shadow Mode Deployment (F1 Reversibility)

Initial deployment runs VLM Tri-Witness in **shadow mode**:

- Log `f1_safe`, `f2_adherence`, `prompt_density`, `hallucinated_elements`,
  `anchor_required`, `anchor_suggestion` for every render
- DO NOT gate the payload based on these values
- Calibrate false-positive rate for 7 days before promoting to hard gate

This prevents a malformed VLM prompt from breaking active image generation
while we map the false-positive baseline.

## Density Estimation Method (Hybrid)

The density estimate is **NOT** a single number from a single source. It
is a hybrid:

### Stage 1 — Heuristic Lower Bound (Hermes-side, no API call)

Pure math. Computed pre-dispatch. Concept-coverage formula:

```
density_lower = (
  has_subject_identity   × 1.00 +
  has_subject_pose       × 0.80 +
  has_primary_material   × 0.60 +
  has_background_scene   × 0.40 +
  has_lighting_lens      × 0.30 +
  has_atmospheric_tone   × 0.15
) / 3.25
```

Max possible score = `1.00` (all six concepts fully specified).
Default raw prompt like "generate a portrait" → `density_lower ≈ 0.10`.
Hard reject territory.

If `density_lower ≥ 0.50`:
- Skip VLM round-trip
- Final density = `density_lower` clamped to `[0.50, 1.0]`
- Save tokens, save latency

### Stage 2 — VLM Alignment Pass (only if Stage 1 < 0.50)

VLM runs a three-question audit (see `references/vlm-audit-prompt.md`).
The VLM does NOT estimate a percentage. It answers three discrete booleans:

1. **Foreign object presence** — are there visible elements NOT in the prompt?
2. **Entity specification completeness** — for each prompt entity, is its
   spatial/lighting/material/scale specified?
3. **Residual entropy** — could a second diffusion model produce a
   substantially different image?

Failure count → density band:
- 0 fails → `density = 0.50`
- 1 fail → `density = 0.35`
- 2 fails → `density = 0.20`
- 3 fails → `density = 0.20` (also flagged for second re-densify)

### Atmospheric Exemption List

To prevent VLM false-positives on lighting/mood primitives, these are
NOT counted as foreign objects:

```
atmospheric_primitives = [
  "rim light", "fill light", "skin bloom", "lens flare",
  "depth of field", "bokeh", "haze", "atmospheric perspective",
  "chromatic aberration", "ambient occlusion", "soft shadow",
  "specular highlight", "key light direction", "backlight"
]
```

These may appear in `hallucinated_elements` for transparency, but they do
NOT count toward the failure tally in Stage 2.

## Constitutional Binding

| Floor | Where this skill enforces it |
|---|---|
| **F1 SAFETY** | `f1_safe` flag. NSFW/gore blocks delivery. |
| **F2 TRUTH** | `f2_adherence` + `prompt_density`. Sparse prompts are not permitted to ship as if they were dense. |
| **F4 CLARITY** | Disclosure on `density < 0.50` is mandatory prose, not silent data. |
| **F7 HUMILITY** | Agent does not overclaim (`/10` quality scores are evidence-grounded, not aspirational). |
| **F9 ANTI-HANTU** | The limit is structural, not advisory. The pipe cannot compile a high-ΔS output — period. |
| **F11 AUDIT** | Every receipt logged. Chain hash on dispatch. |

## Trigger / When to Use

**Use when:**
- Any T2I (text-to-image) dispatch in the federation
- Any vision request from Hermes that will materialize pixels
- Any workflow that produces RGB output from a text prompt

**Do NOT use when:**
- Image editing (inpainting, transparency, style transfer) — different
  dimensionality regime; use the multimodal router's edit path
- Pure VQA / image understanding — no pixel output
- Video generation — T2V has different temporal semantics; separate skill
- Audio/somatic — different modality entirely

## Procedure (callers MUST follow this order)

1. **Receive** sparse or dense human prompt.
2. **Classify** — hard-gate geometry? Detect numeric/structural/key terms.
   If yes → set `anchor_required: true`, request anchor, halt here.
3. **Densify** — run `recipes/densify.py` to expand sparse prompt into
   constraint specification. Stage 1 heuristic computes `density_lower`.
4. **Branch:**
   - If `density_lower ≥ 0.50` → proceed directly to diffusion with
     `prompt_density: density_lower` in receipt.
   - Else → run `recipes/shadow_audit.py` (VLM tri-witness) AFTER
     diffusion to populate `f2_adherence`, `hallucinated_elements`,
     `anchor_required`, final `prompt_density`.
5. **Gate:**
   - `density < 0.20` → throw exception, re-densify loop, do NOT deliver
   - `density ∈ [0.20, 0.50)` → deliver WITH honest disclosure caption
   - `density ≥ 0.50` → deliver clean
6. **Receipt** — return the JSON contract to caller. Every field populated.
7. **Log** — append to `density_audit.csv` for shadow-mode calibration.

## Failure Modes

| Failure | Action |
|---|---|
| VLM tri-witness returns malformed JSON | Treat as Stage 1 result; default `density = density_lower`; flag for manual audit. |
| Diffusion API timeout | Retry once with same anchor; on second fail, return error WITHOUT breaking the JSON contract (still return all fields populated with `null` or default). |
| F1 fails (NSFW) | Hard block. Return `"f1_safe": false` with no payload URL. |
| Identity anchor fails (no face detected) | Surface as `anchor_required: true` with `anchor_suggestion: "ip_adapter_face"`. Do NOT silently fallback. |
| VLM jailbreak attempt via prompt injection | Stage 1 heuristic always runs first. VLM cannot inflate density above Stage 1 ceiling. |

## Key Paths

| What | Where |
|---|---|
| Doctrine (this file) | `AAA/skills/forge-vision-densify/SKILL.md` |
| Heuristic expander | `AAA/skills/forge-vision-densify/recipes/densify.py` |
| Shadow VLM tri-witness | `AAA/skills/forge-vision-densify/recipes/shadow_audit.py` |
| VLM three-question contract | `AAA/skills/forge-vision-densify/references/vlm-audit-prompt.md` |
| Audit log | `~/.local/share/arifos/density_audit.csv` |
| Wiring target | `lightweight-image-generation` dispatch path |
| Forge skill creator | `FORGE-skill-creator` |

## Telemetry per Run

```json
{
  "skill_name": "forge-vision-densify",
  "version": "1.0.0",
  "prompt_original": "<hash>",
  "prompt_densified": "<hash>",
  "density_lower": 0.0,
  "density_final": 0.0,
  "vlm_stage_invoked": false,
  "vlm_failures": 0,
  "anchor_required": false,
  "f1_safe": null,
  "f2_adherence": null,
  "delivery_mode": "clean|disclose|reject",
  "shadow_mode": true,
  "latency_ms": 0
}
```

## Verification

Two test prompts required before SEAL:

1. **Sparse human prompt** ("a man standing in a park"): `density_lower`
   should compute to `< 0.20`, hard-reject path exercised.
2. **Dense constraint prompt** ("Caucasian male, 30s, navy suit, white shirt,
   red tie, golden hour sidelight, 85mm portrait lens, bokeh, urban
   rooftop"): `density_lower ≥ 0.75`, VLM stage skipped, clean delivery.

---

## Sealing Note

> **DITEMPA BUKAN DIBERI — Densification Receipt Forge**
>
> Skill forged 2026-08-27 under F13 directive. The pipe cannot leak. The
> limit is structural. The receipt is load-bearing. The VLM is shadow-mode
> for one week of false-positive calibration before hard promotion.
>
> Acknowledged correction: "knowing limits" → "structural governance."
> Anti-Hantu: character attribution removed. Pipe compliance is the bar.
