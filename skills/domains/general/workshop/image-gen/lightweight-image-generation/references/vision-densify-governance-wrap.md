# T2I Governance Wrap (forge-vision-densify)

**Captured:** 2026-08-27 (Hermes ASI vision paradox session)

Every T2I dispatch in this skill MUST route through the densification layer
at `AAA/skills/forge-vision-densify/recipes/dispatch.py`. Naked `{url, status}`
payloads are F2-bad. Every dispatch returns the JSON contract:

```json
{
  "f1_safe": bool,
  "f2_adherence": float (0-1),
  "prompt_density": float (0-1),
  "hallucinated_elements": list[str],
  "anchor_required": bool,
  "anchor_suggestion": str | null
}
```

## Three density bands govern delivery

| `prompt_density` | Delivery mode | Action |
|---|---|---|
| `< 0.20` | `reject` | Hard F2 reject. Forced re-densify loop. Do NOT deliver. |
| `[0.20, 0.50)` | `disclose` | User-facing caption MUST list `hallucinated_elements` from the receipt. |
| `≥ 0.50` | `clean` | Clean delivery, disclosure optional. |

## Hybrid estimator (presence ≠ specification)

The Stage-1 heuristic credits concept SPECIFICATION, not concept presence:

- `full`    = ≥2 keywords in category → credit 1.0
- `partial` = 1 keyword in category    → credit 0.4
- `zero`    = category absent          → credit 0.0

A naive "credit for presence" estimator scores "a man standing in a park"
at ~0.68. That is the SELF-DEFEATING METRIC trap — the heuristic inflates
density for sparse prompts and the gate fails to fire. Always run smoke
tests on the four canonical cases before wiring:

| Prompt | Expected density | Expected mode |
|---|---|---|
| `"a man standing in a park"` | ~0.46 | disclose |
| Dense Caucasian-male-navy-suit prompt | ≥0.70 | clean |
| `"show me a fault dipping 45 degrees NW-SE"` | 0.0 (hard gate fires) | missing_anchor |
| `"label the three horizons: Topaz, Jasper, Onyx"` | 0.0 (hard gate fires) | missing_anchor |

If a sparse prompt lands `clean`, the gate logic is broken. Patch and re-run.

## Hard gate (geometric / structural)

Prompts containing geometric, structural, or numerical constraints
(`45 degrees`, `K-DIP`, `NW-SE strike/dip`, isometric, orthographic, text-in-image,
caption: ..., wellbore, horizon, stratigraph, fault) flip `anchor_required=True`
and refuse to call the diffusion engine until a ControlNet/Depth/Ip-Adapter
reference path is supplied.

Do not bypass from this skill side. If you need an anchor-free render of a
geometric subject, that's a different problem — flag it to the user, don't
silently fall through.

## VLM shadow mode (F1 reversibility)

VLM tri-witness logs `f1_safe`, `f2_adherence`, `prompt_density` WITHOUT
gating payload for the first 7 days. After 7 days of false-positive data,
the curator can promote to hard gate.

If you must promote early, document the threshold in
`density_audit.csv` records and surface a note in the dispatch receipt.

## Wiring smoke tests (run after every change)

End-to-end checks before declaring any densify change shippable:

1. Sparse prompt → assert `delivery_mode == "disclose"` or `"reject"`
2. Dense prompt → assert `delivery_mode == "clean"` and `prompt_density >= 0.50`
3. Hard-gate prompt, no anchor → assert `anchor_required == True`,
   `delivery_mode == "missing_anchor"`
4. Hard-gate prompt with anchor → proceeds past gate
5. Audit log writes one CSV row per dispatch with all fields populated

If the wired pipeline crashes on edge cases (`None` flags treated as falsy,
empty `image_path`, missing sidecar files), the gate logic has bugs. Patch
before declaring SEAL.

## Constitutional anchor

This wrap exists because "the agent should know its limits" is character
attribution (F9 ANTI-HANTU violation). The structural alternative is a
rigid contract the pipe cannot bypass. Falsification is auditable via the
audit log; the gate cannot be silently disabled by a future agent.
