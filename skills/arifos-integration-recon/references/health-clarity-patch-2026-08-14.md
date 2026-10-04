# Health Clarity Patch — K13 Substrate Honesty Fix (2026-08-14)

## Problem
`/health` endpoint reported `status: "degraded"` + `owner_summary.reasons: ["runtime_drift"]` but JSON field `runtime_drift: false`. Root cause: `runtime_drift_val = bool(_drift.get("runtime_drift", False)) or _sr_drift` — boolean OR of two heterogeneous signals (actual code drift + attestation SOT drift).

## Fix (commit `be55fa293`)
Three additive patches to `rest_routes.py` (deployed = source):
1. **`degraded_reasons[]`** — structured list with `layer/field/severity/explanation` per entry
2. **`layer_health{}`** — per-layer independent classification (constitutional, runtime, registry, deployment_attestation, vault, infra)
3. **`owner_summary.reasons` split** — `code_runtime_drift` vs `deployment_attestation_drift`

## Dispatch technique
Kimi Code 429 quota → Qwen Code (`qwen -p "$(cat SPEC.md)" --output-format text`) as fallback. SPEC is CLI-agnostic.

## SPEC: `/root/forge_work/health-clarity-2026-08-14/SPEC.md`
