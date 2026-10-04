# Health Endpoint Clarity Patch — 2026-08-14

## The Problem

The arifOS `/health` endpoint reported `status: "degraded"` with `owner_summary.reasons: ["runtime_drift"]`, but the JSON field `runtime_drift: false`. Every agent that read the health payload got contradictory signals — leading to false "constitutional collapse" diagnoses.

## Root Cause (code-level)

File: `/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py`

### The contamination line (~3173-3187)

```python
runtime_drift_val = bool(_drift.get("runtime_drift", False))  # → False (actual code drift)
# ...
_sr_drift = bool(_attest.get("drift"))                        # → True (source_commit ≠ built_commit)
runtime_drift_val = runtime_drift_val or _sr_drift             # → True (CONTAMINATED)
```

### How it propagated

```python
_degraded = runtime_drift_val or contract_drift_val             # → True (line 3234)
"status": "degraded" if _degraded else "healthy"               # → "degraded" (line 3236)

# BUT the JSON field emitted is the ORIGINAL uncontaminated value:
"runtime_drift": bool(_drift.get("runtime_drift", False))      # → False (line ~3480)

# AND the owner reason used the CONTAMINATED variable:
+ (["runtime_drift"] if runtime_drift_val else [])              # → ["runtime_drift"] (line ~3428)
```

Result: `status=degraded`, `runtime_drift=false`, `owner_summary.reasons=["runtime_drift"]` — all from the SAME response, all contradicting each other.

## The Source ≠ Deployed Gap

The source repo (`/root/arifOS/`) `horizon_health()` at line 2465 returns a clean 3-signal design. The deployed version (`/opt/arifos/app/`) has enriched middleware that adds 80+ keys including `registry_truth`, `deployment_drift_status`, and the contaminated `runtime_drift_val`. Both files are 370KB/8629 lines and identical — the "enriched" code IS in source too, just harder to find because the health handler is buried inside a massive `register_rest_routes()` function spanning hundreds of lines.

## The Fix (commit `be55fa293`)

Three additive patches, no existing fields changed or removed:

### Patch 1: `degraded_reasons[]`

```python
degraded_reasons: list[dict[str, str]] = []
if _sr_drift:
    degraded_reasons.append({
        "layer": "deployment_attestation",
        "field": "software_release.drift",
        "value": "true",
        "severity": "warning",
        "explanation": "source_commit != built_commit in runtime attestation (SOT drift, not code drift)"
    })
if _code_runtime_drift:  # uses ORIGINAL uncontaminated value
    degraded_reasons.append({
        "layer": "runtime",
        "field": "runtime_drift",
        "value": "true",
        "severity": "critical",
        "explanation": "Live running code does not match deployed commit"
    })
```

### Patch 2: `layer_health{}`

```python
_layer_health = {
    "constitutional": "healthy" if _floors_pass_count == _floors_total else "degraded",
    "runtime": "healthy" if not _code_runtime_drift else "degraded",
    "registry": "degraded" if contract_drift_val else "healthy",
    "deployment_attestation": "drift" if _sr_drift else "aligned",
    "vault": _vault_health,
    "infra": "normal",
}
```

### Patch 3: owner_summary.reasons split

```python
# BEFORE:
+ (["runtime_drift"] if runtime_drift_val else [])

# AFTER:
+ (["code_runtime_drift"] if _code_runtime_drift else [])
+ (["deployment_attestation_drift"] if _sr_drift else [])
```

## Post-fix Live Output (verified)

```json
{
  "status": "healthy",
  "degraded_reasons": [],
  "layer_health": {
    "constitutional": "healthy",
    "runtime": "healthy",
    "registry": "healthy",
    "deployment_attestation": "aligned",
    "vault": "healthy",
    "infra": "normal"
  },
  "runtime_drift": false,
  "owner_summary": {
    "color": "GREEN",
    "reasons": ["vault_healthy"]
  }
}
```

## How to Verify the Fix is Present

```bash
curl -s http://localhost:8088/health?nocache=1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('degraded_reasons:', d.get('degraded_reasons', 'MISSING'))
print('layer_health:', d.get('layer_health', 'MISSING'))
reasons = d.get('owner_summary', {}).get('reasons', [])
has_old = 'runtime_drift' in reasons
has_new = 'deployment_attestation_drift' in reasons or 'code_runtime_drift' in reasons
print(f'reasons: {reasons}')
print(f'old label present: {has_old}  new labels present: {has_new}')
"
```

If `degraded_reasons` key is `MISSING` → endpoint is running pre-be55fa293 code.

## Dispatch Pattern

This patch was executed via **Qwen Code** (GLM-5.2) after Kimi Code returned 429 quota exhaustion. The SPEC file was CLI-agnostic (`/root/forge_work/health-clarity-2026-08-14/SPEC.md`) — write once, dispatch to whichever CLI has quota. Verification done independently by Hermes: syntax check, file sync check, live endpoint probe, git diff review.
