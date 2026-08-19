---
name: forge-vss-verifier-suite
id: forge-vss-verifier-suite
version: 1.0.0-2026.08.18
owner: 555-ASI
risk_tier: low
autonomy_tier: T1
floor_scope:
  - F2
  - F4
  - F7
  - F9
  - F11
description: >
  VSS-2 Lightweight Verifier Suite — independent post-generation verifiers for
  Verified Scene Synthesis. Wraps vision_analyze with three focused checks
  (Count/Containment, Perspective/Depth, Shadow/Light Direction) producing
  structured Hard/Soft Violation reports. Pure OBSERVATION — never mutates,
  never judges. 555-ASI gates output before reasoning.
  USE WHEN: "verify this generated image", "check if generation has violations",
  "run VSS verifiers", "post-generation QA", "Hard/Soft Violation report".
tags:
  - vss
  - verifier
  - vss-2
  - 555-asi
  - f2
  - f4
  - f7
  - f9
  - f11
  - proposal-verification-repair
harness: hermes|kimi|opencode|openclaw|claude|codex
domain: meta
capability_tier: fed-multimodal-vision
ecology_state: WARM
required_tools:
  - vision_analyze
  - mcp__arifos__arif_judge
tool_gate: strict
---

# forge-vss-verifier-suite · VSS-2

> **The verifier layer of Verified Scene Synthesis.**
> Pure observation. Never mutates. Never judges. Reports only what the image shows.
> **DITEMPA BUKAN DIBERI ⚒️**

---

## Core Doctrine

The verifier suite is the **independent witness layer** of VSS. It does NOT propose images, does NOT repair them, does NOT seal them. It **observes what exists in the pixels** and reports structured deviations.

> *"The verifier sees what is. The judge decides what to do. The agent acts. The sovereign seals."*

This separation is constitutional:
- **Verifier** = OBSERVE-class. F2 TRUTH (epistemic labels per deviation), F9 ANTIHANTU (no fabricated violations).
- **Output gating** = 555-ASI. F4 CLARITY (structured JSON), F7 HUMILITY (confidence cap 0.85), F11 AUDIT (receipt-wrapped).
- **Decision** = 333-AGI reasons over verifier output.
- **Seal** = W³ sovereign via `arif_judge` → `arif_seal`.

The verifier never sees the prompt (intentionally — to avoid confirmation bias). It only sees the final image + optional auxiliary signals (count assertion, light source intent).

---

## The Three Verifiers (v1)

### Verifier 1: Count / Containment

**Validation target:** Entity count matches prompt assertion. Container relationships respected. No extra/missing entities.

| Input | Type | Required |
|---|---|---|
| `image_path` | string | ✅ |
| `count_assertions` | object | optional (e.g. `{"birds": 5, "people": 2}`) |
| `containment_assertions` | object | optional (e.g. `{"cat": "inside_box"}`) |

**Process:**
1. Qwen-VL-Max (MuleRouter PRMT) extracts every distinct entity with bbox
2. Match count assertions against detected entities (within tolerance ±1 for occlusion)
3. Match containment assertions against spatial layout (bbox center within container bbox)
4. Tag each deviation with severity (HARD = explicit count violation, SOFT = occlusion-induced ambiguity)

**Output schema:**
```json
{
  "verifier": "count_containment",
  "verdict": "PASS|HOLD|FAIL",
  "confidence": 0.0-0.85,
  "epistemic_label": "OBS",
  "hard_violations": [
    {"type": "count_mismatch", "entity": "birds", "expected": 5, "observed": 4, "severity": 0.9, "location_hint": "lower_right_quadrant"}
  ],
  "soft_violations": [
    {"type": "count_ambiguous", "entity": "birds", "reason": "occlusion_overlap", "likely_count": "4-5", "severity": 0.4}
  ],
  "evidence": "qwen-vl-max detected 4 distinct bird-shaped entities in lower half of frame. One additional blur in upper_right may be occluded bird or foliage.",
  "constitutional_floors_applied": ["F2", "F9"]
}
```

**Hard violation examples:**
- Prompt says "5 birds", image shows 4
- Prompt says "cat inside box", cat bbox center outside box bbox
- Prompt says "3 people on stage", image shows 5 people

**Soft violation examples:**
- Possible occlusion making count ambiguous
- Reflection doubling apparent count (mirror visible)
- Partial object visible at frame edge

---

### Verifier 2: Perspective / Depth

**Validation target:** Geometric perspective consistency. Horizon line plausible. Vanishing points converge as expected. No impossible spatial layouts.

| Input | Type | Required |
|---|---|---|
| `image_path` | string | ✅ |
| `scene_type` | string | optional ("indoor" | "outdoor" | "architectural" | "portrait") |

**Process:**
1. Qwen-VL-Max detects horizon line + dominant vanishing points
2. Check vanishing point convergence within tolerance
3. Check objects near horizon follow atmospheric perspective (if outdoor)
4. Flag impossible geometries (e.g., two vanishing points that should converge but don't)

**Output schema:**
```json
{
  "verifier": "perspective_depth",
  "verdict": "PASS|HOLD|FAIL",
  "confidence": 0.0-0.85,
  "epistemic_label": "OBS",
  "hard_violations": [
    {"type": "vanishing_point_conflict", "vp1_location": "left_third", "vp2_location": "right_third", "expected_convergence": "single_vanishing_point", "severity": 0.8}
  ],
  "soft_violations": [
    {"type": "horizon_ambiguous", "reason": "low_contrast_or_partial_occlusion", "severity": 0.3}
  ],
  "evidence": "Two vanishing points detected at opposite sides of frame, neither consistent with single-point perspective. Horizon line unclear due to foliage. Likely multiple-light or non-photorealistic composition.",
  "constitutional_floors_applied": ["F2", "F7"]
}
```

**Hard violation examples:**
- Vanishing points that should converge but don't
- Objects defying gravity (floating without support)
- Impossible camera angle (e.g., 180° tilt)

**Soft violation examples:**
- Horizon line obscured by foreground
- Mixed focal lengths (wide-angle + telephoto in same frame)
- Stylized perspective (intentional, but flagged for awareness)

---

### Verifier 3: Shadow / Light Direction

**Validation target:** Shadow direction consistency. Single dominant light source unless multiple explicitly stated. Shadow length proportional to light angle.

| Input | Type | Required |
|---|---|---|
| `image_path` | string | ✅ |
| `light_source_count` | int | optional (default 1) |

**Process:**
1. Qwen-VL-Max detects shadows on ground plane + objects
2. Trace shadow direction vectors (radial from object base outward)
3. Check all shadows converge toward consistent light source
4. If multiple lights specified, allow multiple consistent directions

**Output schema:**
```json
{
  "verifier": "shadow_light",
  "verdict": "PASS|HOLD|FAIL",
  "confidence": 0.0-0.85,
  "epistemic_label": "OBS",
  "hard_violations": [
    {"type": "shadow_direction_conflict", "shadows": ["shadow_A_180deg", "shadow_B_45deg"], "expected_single_light": true, "severity": 0.85}
  ],
  "soft_violations": [
    {"type": "shadow_length_inconsistent", "objects": ["tree", "person"], "expected_similar_length": true, "reason": "may_indicate_mixed_lights_or_different_ground_plane", "severity": 0.4}
  ],
  "evidence": "Shadows from left-side objects point east (45°), shadows from right-side objects point west (180°). Inconsistent single-light-source geometry. Likely multiple generators or stylized composition.",
  "constitutional_floors_applied": ["F2", "F7", "F9"]
}
```

**Hard violation examples:**
- Two shadows from same object pointing opposite directions
- Shadow length inconsistent with light position
- Shadow falling upward (impossible without bounce light)

**Soft violation examples:**
- Ambient occlusion vs hard shadow ambiguity
- Multiple plausible light sources
- Subsurface scattering effects (skin, wax, leaves)

---

## Composition API

Each verifier is callable independently. The suite composes them.

### Single verifier call

```python
from forge_vss_verifier_suite import verify_count_containment

result = verify_count_containment(
    image_path="/path/to/generated.png",
    count_assertions={"birds": 5, "people": 2},
    containment_assertions={"cat": "inside_box"}
)

# result is structured dict per schema above
```

### Full suite call (3 verifiers in parallel)

```python
from forge_vss_verifier_suite import verify_suite

result = verify_suite(
    image_path="/path/to/generated.png",
    count_assertions={"birds": 5},
    scene_type="outdoor",
    light_source_count=1
)

# result is aggregated:
# {
#   "image_path": "...",
#   "overall_verdict": "PASS|HOLD|FAIL",
#   "overall_confidence": 0.0-0.85,
#   "verifier_results": {
#     "count_containment": {...},
#     "perspective_depth": {...},
#     "shadow_light": {...}
#   },
#   "aggregated_hard_count": int,
#   "aggregated_soft_count": int,
#   "total_severity_score": float,  # 0.0 - 3.0
#   "epistemic_labels": ["OBS", "OBS", "OBS"],
#   "constitutional_floors_applied": ["F2", "F4", "F7", "F9", "F11"],
#   "audit_receipt_id": "vss_verify_<sha256>"
# }
```

### Aggregation rules

| Condition | Overall Verdict |
|---|---|
| All verifiers PASS, no violations | `PASS` |
| 1+ HARD violations OR 3+ SOFT violations | `FAIL` |
| 1-2 SOFT violations, no HARD | `HOLD` |
| Any verifier returns HOLD | `HOLD` (highest seen) |

Total severity score = sum of all violation severities (capped at 3.0).

### VSS-1 ledger ingest (no VLM)

`vss_ledger_adapter.project_ledger(assertion_ledger)` validates the VSS-1 contract, then projects counts / containments / lighting into a **work order**. `raw_prompt` is stripped (F9). `verifier: none` stays unrouted.

`run_verifier_suite(..., assertions=ledger)` fail-closes with `ERROR` if the ledger is not a valid VSS-1 object. Pixel checks still require a VLM; ingest does not.

Verified 2026-08-19: `ledgers_projected=50/50` via `test_vss_ledger_adapter.py`.

---

## Model Selection

**Default:** `qwen-vl-max` via MuleRouter (single failure domain — same key as chat).

**Why not MiniMax?**
- `minimax-mcp` server frequently crashes (parked after 3 attempts)
- `MINIMAX_BASE_URL` historically sops-encrypted (Invalid IPv6 URL bug)
- MuleRouter has shared key with chat = no split failure domain

**Fallback ladder:**
1. `qwen-vl-max` (MuleRouter) — preferred
2. `qwen3-vl-plus` (MuleRouter) — faster, slightly lower quality
3. `qwen3-vl-flash` (MuleRouter) — fastest, basic
4. `qwen/qwen2.5-vl-72b-instruct` (OpenRouter) — legacy fallback, separate key

**Do NOT use for verifiers:**
- Text-only models (no vision)
- Generation models (MiniMax image-01) — conflict of interest, may bias toward "looks fine"

---

## Constitutional Compliance

| Floor | How Verifier Honors It |
|---|---|
| **F2 TRUTH** | Every deviation tagged `epistemic_label: "OBS"`. Confidence capped at 0.85. Verifier NEVER fabricates — if it can't see the violation, it returns HOLD not FAIL. |
| **F4 CLARITY** | Output is structured JSON. No prose deviation reports. Schema-validated before return. |
| **F7 HUMILITY** | Confidence cap 0.85 (vision model is imperfect). Verifier never claims "no violations exist" — only "no violations observed." |
| **F9 ANTIHANTU** | Verifier sees pixels only. Doesn't see prompt (avoid confirmation bias). Doesn't hallucinate violations — must be visible in image. |
| **F11 AUDIT** | Every verifier call writes receipt to VAULT999. Receipt contains: image_path hash, verifier_results, model used, timestamp. |

**Constitutional test before deploying:**
```python
# F2: Epistemic label present
assert result["epistemic_label"] == "OBS"

# F7: Confidence capped
assert 0.0 <= result["confidence"] <= 0.85

# F9: No prompt leakage
# (verifier function signature does not accept prompt — only image + assertions)

# F11: Receipt written
assert result["audit_receipt_id"].startswith("vss_verify_")
```

---

## Integration with Federation

### With `aaa-image-editing`

After NB family edit completes, run verifier suite to check structural integrity:
```python
edit_result = aaa_image_editing(
    prompt="Add woman on left",
    reference_image=original_path,
    semantic_mask="man's face, physique, pose"
)

verification = verify_suite(
    image_path=edit_result.output_path,
    count_assertions={"people": 2},
    containment_assertions={},
    scene_type="portrait"
)

if verification["overall_verdict"] == "FAIL":
    # Targeted repair (VSS-3) — when built
    # For now: log + present to user with realism rating
    log_verification_failure(verification)
```

### With `forge_visual_qa-w3`

Verifiers compose with W³ tri-witness as the W₁ layer (vision validation):
- W₁ = Verifier Suite (independent OBSERVATION)
- W₂ = DOM lint (structural validation)
- W₃ = Human sovereign (governance)
- Composite hash → VAULT999

This means **Verifier Suite IS the W₁ implementation** for VSS-aligned visual QA.

### With `forge_chart`

Chart eureka discovery (already in `forge_chart`) outputs deviations. Verifier Suite complements with image-based checks. Composable for chart+image composite outputs.

### With Hermes PRMT

When Arif sends an image to Telegram, PRMT produces [IMAGE TRANSCRIPT]. Verifier Suite is the structural check that can run on the same image BEFORE reasoning — ensures transcript is structurally consistent with pixels.

---

## Failure Modes & Recovery

### Verifier returns HOLD due to model latency

- Retry once with `qwen3-vl-flash` (faster)
- If still HOLD after retry, log + proceed with HOLD verdict
- Never silently upgrade HOLD to PASS

### Verifier returns FAIL on subjective composition

- Verifier reports violation + evidence
- 555-ASI gates: "is this a real violation or aesthetic choice?"
- 333-AGI reasons: "does prompt imply intentional multi-light source?"
- W₃ sovereign decides (e.g., "this is a stage photo, multi-light is intentional")

### Verifier model crashes mid-suite

- One verifier failure does NOT abort suite
- Mark missing verifier as `unavailable`
- Aggregate on available results only
- Log model failure to ARA (auto-recovery agent)

### Image path not accessible

- Return `verdict: "ERROR"`, `reason: "image_unreadable"`
- Never guess at contents

---

## Out of Scope (v1)

The following are NOT in v1 — deferred to future versions or other VSS layers:

- **Temporal consistency** (video) — VSS-4+
- **Material reflectance validation** (BSDF) — VSS-5+
- **Biomechanical joint limits** — VSS-5+
- **Fluid dynamics** (Navier-Stokes) — VSS-6+
- **Text legibility** (legible-font check) — VSS-7
- **Color constancy** (lighting white balance) — VSS-8
- **Style consistency** (across multi-image generations) — VSS-9

Add verifier to suite only when there's measurable demand. Each new verifier costs latency + cognitive load. Stay minimal.

---

## Test Criteria

```
□ Single verifier call returns schema-valid JSON
□ Suite call aggregates 3 verifiers in parallel (< 10s total)
□ Confidence never exceeds 0.85 (F7)
□ Every deviation tagged epistemic_label "OBS" (F2)
□ Receipt written to VAULT999 for every call (F11)
□ HOLD verdict returned when verifier model returns ambiguous
□ FAIL verdict returned when hard violation confirmed
□ PASS verdict returned when no violations observed
□ No prompt input in verifier function signature (F9 anti-bias)
□ Constitutional test suite passes (5 floors)
```

---

## Telemetry (for ARA monitoring)

```
- verifier_calls_per_session
- verifier_verdict_distribution (PASS / HOLD / FAIL)
- verifier_avg_latency_ms
- verifier_hard_violation_types (top 5)
- verifier_soft_violation_types (top 5)
- verifier_model_fallback_rate
- constitutional_floor_compliance_rate (target 100%)
```

---

## Known Limitations (F7 honesty)

- **Verifiers see pixels only.** Cannot verify claims about events, emotions, narrative (those are semantic, not structural).
- **Vision models imperfect.** Confidence cap 0.85 reflects this. A "PASS" never means "perfect" — only "no violations observed."
- **No ground truth.** Verifiers check geometric/physical consistency, not factual accuracy. "Image of Eiffel Tower" could be visually correct but the wrong city.
- **Latency budget.** 3 verifiers in parallel ≈ 3-9s. Not for real-time interactive use. Use for SEAL-grade generation only.
- **English-centric prompts.** Count/containment assertions work best in English. Other languages: parse with locale-aware VLM, may need additional prompting.

---

## Path Forward (Sequence)

**Now (VSS-2):** Lightweight Verifier Suite — this skill. Wraps vision_analyze. No GPU. ~1-3 day build.

**Next (VSS-1):** Causal Scene Graph Parser — L2 skill. Extracts structured entities + relations from prompt. Provides assertions to verifiers and bbox hints to repair (VSS-3). Medium build.

**Then (VSS-3):** Bounded Local Repair Controller — wires VSS-1 (bbox) + VSS-2 (FAIL signal) into a forge_scar-gated inpainting loop. Max 3 retries. Edit-damage cost function J. Higher build complexity.

**Later (VSS-4+):** Hybrid 3D Scene Representation, Staged Differentiable Rendering, Biomechanical/Ophthalmic/Fluid Verifiers. GPU required.

---

*Forged 2026-08-18 by 333-AGI / Hermes-prime under F13 SOVEREIGN ratification of Verified Scene Synthesis doctrine.*
*Mirror of W³ tri-witness pattern from `/root/.kimi-code/skills/FORGE-visual-qa-w3/`.*
*DITEMPA BUKAN DIBERI ⚒️ — The verifier sees what is. The judge decides what to do.*