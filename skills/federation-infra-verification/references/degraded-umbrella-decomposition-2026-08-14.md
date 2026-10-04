# Degraded Umbrella Decomposition — 2026-08-14

## Context

Arif asked "what's the status of the system." Hermes initially parsed `/health` JSON incorrectly — read `len(d.get("floors", []))` which returned 0 because `floors` is not a key (the integer is `floors_active`). Then in a follow-up, Hermes reported `runtime_drift` as active when the boolean field was actually `False` — the `"runtime_drift"` string in `owner_summary.reasons[]` was confused with the `runtime_drift` boolean field.

Arif corrected both errors in a detailed decomposition, pointing out:
1. "degraded" is an umbrella for 3 separate drift signals
2. The `owner_summary.reasons` string "runtime_drift" doesn't mean the `runtime_drift` field is `True`
3. Infra pressure (swap, load) was being confused with constitutional health

## The 3-source confusion map

| Source field | Value at time of session | Hermes initial report | Reality |
|---|---|---|---|
| `runtime_drift` (bool) | `False` | "runtime drift" ❌ | No drift — code matches |
| `registry_truth` (enum) | `DRIFT_DETECTED` | (correctly reported) | Config bookkeeping mismatch |
| `deployment_drift_status` (enum) | `drift_detected` | (correctly reported) | Marker flag mismatch |
| `owner_summary.reasons` contains `"runtime_drift"` | Yes | (source of confusion) | **Naming collision** — reason label ≠ field name |
| `runtime_matches_build` (bool) | `True` | Not checked | Code is fine |

## The init token stale-cache issue

Separately discovered: `arif_init` response carries `built_commit` from install time (stale), while live `/health` carries current `build_commit`. Agents reading init tokens see drift that doesn't exist in live health. Two different sources, two different values, same field name.

## Resolution — Code Fix Applied (commit `be55fa293`, 2026-08-14)

The `owner_summary.reasons` naming collision was fixed at the code level. Three additive fields were added: `degraded_reasons[]` (structured array), `layer_health{}` (per-layer), and split reason labels (`code_runtime_drift` vs `deployment_attestation_drift`). Full code-level root cause and patch: `references/health-endpoint-clarity-patch-2026-08-14.md`.

**For future probes:** Always decompose `/health` by individual boolean fields, not by the umbrella `status` string. Prefer `degraded_reasons[]` (structured) over `owner_summary.reasons` (string labels). Report each layer independently to Arif.
