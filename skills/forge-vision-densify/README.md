# forge-vision-densify

Governance layer for T2I image generation in the arifOS federation.
Implements the immutable JSON receipt contract and ΔS gating rules.

## Day-0 Posture (F13 SEAL 2026-08-27)

| Flag | Value | Meaning |
|---|---|---|
| `ENFORCE_PIPELINE` | `true` | Every T2I dispatch MUST go through this wrapper. Bypass raises RuntimeError. |
| `HARD_REJECT` | `false` | Density < 0.20 returns disclose warning, does not block. |
| `DISCLOSE` | `true` | Density < 0.50 delivers image with honest disclosure caption. |
| `AUDIT` | `true` | Every dispatch writes to density_audit.csv. |

All four flags are environment-overridable for testing:
```bash
DENSIFY_ENFORCE_PIPELINE=false python3 recipes/fuse.py --prompt "..."
DENSIFY_HARD_REJECT=true python3 recipes/fuse.py --prompt "..."
DENSIFY_FORCE=1 python3 recipes/fuse.py --prompt "..."  # bypass ENFORCE check
```

## Day-7 Calibration Gate

Day-7 is **criteria-driven, not calendar-driven**. Promotion criteria live in
`/root/HERMES/scripts/forge-vision-densify-summary.py`:

```python
MIN_DISPATCHES = 7
FPR_THRESHOLD = 0.05        # >5% suspected FP → stay disclose
FNR_THRESHOLD = 0.10        # >10% suspected FN → stay disclose
MISSING_ANCHOR_RATIO = 0.30 # >30% missing-anchor → stay disclose
```

Operator must mark suspect events in `~/.local/share/arifos/density_overrides.jsonl`
*before* `HARD_REJECT_CANDIDATE` verdict can fire. Zero overrides = `INSUFFICIENT_REVIEW`,
NOT pass. (F7 HUMILITY binding: absence of evidence is not evidence of absence.)

The summary script reads the audit log + overrides, computes the seven metrics, and
appends a chain-hashed Markdown line to `~/.local/share/arifos/density_audit_summary.md`.
The file IS the receipt (F11 AUDIT). There is no automatic gate flip — sovereign
reviews the chain, then decides.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Doctrine + JSON contract + thresholds |
| `recipes/densify.py` | Stage 1 heuristic (no API call) |
| `recipes/shadow_audit.py` | Stage 2 VLM tri-witness (shadow mode by default) |
| `recipes/dispatch.py` | Wrapper + posture flags + audit log + disclosure caption |
| `recipes/fuse.py` | CLI entry point — single canonical access |
| `references/vlm-audit-prompt.md` | The three-question VLM contract |

## Wiring into the Federation

Any dispatcher that wants to call a T2I engine MUST:

```python
from forge_vision_densify import dispatch_image, to_json_contract, render_caption

receipt = dispatch_image(
    prompt=user_prompt,
    call_diffusion=lambda p, anchor: my_engine_call(p, anchor, ...),
    engine="MiniMax",   # or "Pollinations", "Wan", etc.
    reference_image_path=user_provided_anchor,  # may be None
)

# User-facing layer:
contract = to_json_contract(receipt)  # the six fields
caption = render_caption(receipt)     # the disclosure text (or "")

# NEVER return naked {url, status} to the user.
# Always return: contract + caption + url.
```

The pipe cannot leak. There is no naked T2I call path that bypasses
this wrapper. Hermes governance is structural, not advisory.

## Constitutional Binding

| Floor | Enforcement point |
|---|---|
| F1 SAFETY | `f1_safe` flag in receipt; "reject_f1_unsafe" delivery mode |
| F2 TRUTH | density bands + mandatory `hallucinated_elements` disclosure |
| F4 CLARITY | disclosure caption is human prose, not silent data |
| F7 HUMILITY | hard reject is data-driven, not assumption-driven (Day-7+) |
| F9 ANTI-HANTU | ENFORCE_PIPELINE=true; wrapper is the only entry point |
| F11 AUDIT | density_audit.csv on every dispatch, prompt-hashed |

## DITEMPA BUKAN DIBERI ⚒️
