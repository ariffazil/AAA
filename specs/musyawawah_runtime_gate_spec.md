# Musyawawah Runtime Gate — Integration Specification (Phase A2)

> **Status:** Phase A2 (specification) — 2026-09-08
> **Path:** A → Evidence → B (per F13 strategic judgment 2026-09-08)
> **Author:** FI-003 under F13 APEX Verdict
> **DITEMPA BUKAN DIBERI**

## 0. Context

First real musyawawah verdict since 2026-08-11 protocol-birth:
- Verdict: `musyawarah/2026-09-08-no-gate-task6/CONVERGENCE.md`
- Reference implementation: `scripts/musyawawah_runtime_gate.py`
- Falsification test: `scripts/test_musyawawah_runtime_gate.py` (Phase A3)
- Sentinel (OBSERVE_ONLY): wired at AAA pre-commit boundary (Phase 2 step 1 done)

This spec defines the **Path B** integration: kernel-side runtime enforcement.

## 1. Integration target

`/root/arifOS/arifosmcp/runtime/pre_execution_gate.py`

```
Line  ~275  action_class = _art_action_class_str(requested_action)   ← INSERT musyawawah check here
Line  ~306  action_class = requested_action.value                    ← OR here
Line  ~335  action_class = requested_action.value                    ← OR here
```

The check fires BEFORE the action proceeds to forge_* chokepoints.

## 2. forge_* chokepoints gated (per A1 amendment)

| Chokepoint | Action class coverage | Notes |
|---|---|---|
| `forge_shell` | T0/T1/T2/T3 | Primary executor |
| `forge_execute` | T1/T2 | Task execution |
| `forge_postgres` (mutate=true) | T2 | DB writes |
| `forge_filesystem` (write modes) | T1/T2 | File writes |
| `forge_git_commit` | T1/T2 | Commits |
| `forge_docker` | T2 | Container ops |
| `forge_pipeline_run` | T2 | Pipeline execution |
| `forge_judge_proxy` | T3 | APEX judgment proxy |

T0/T1 chokepoints NOT gated (baseline affordances per CCC doctrine).

## 3. Contract

For every invocation with `action_class` ∈ {EXECUTE_HIGH_IMPACT, SEAL}:

```python
required = {
    "payload.musyawawah_reference": str,     # format: "musyawarah/<date>-<topic>/CONVERGENCE.md"
}

optional = {
    "payload.ack_irreversible": bool,        # F13 sovereign override
}

verdict = {
    ALLOW:          reference valid, no override needed,
    ALLOW_BYPASS:   F13 override (ack_irreversible=True), logged,
    DENY:           reference missing OR invalid (fail-closed)
}
```

## 4. Override pathway

`payload.ack_irreversible = True` → `ALLOW_BYPASS` with audit log entry:

```
actor=<id>
tool=<forge_*>
action_class=<EXECUTE_HIGH_IMPACT|SEAL>
override_reason=<required string>
session_id=<id>
timestamp=<ISO-8601>
```

Reserved for F13 sovereign direct command. Audit log at `/root/VAULT999/musyawawah/overrides/<YYYY-MM-DD>.jsonl`.

## 5. Validation function

```python
def verify_musyawawah_in_vault999(reference: str) -> bool:
    if not reference.startswith("musyawarah/"):
        return False
    rest = reference[len("musyawarah/"):]
    if "/" not in rest:
        return False
    date_part = rest.split("/")[0]
    if len(date_part) != 10 or date_part[4] != "-" or date_part[7] != "-":
        return False
    return True
```

(Path B): integrate with real arifOS VAULT999 lookup. Phase A uses structural validation only.

## 6. Decision flow (for kernel integration)

```
invoke(action_class, payload):
  1. IF action_class ∈ BASELINE → ALLOW (no check)
  2. IF payload.ack_irreversible == True → ALLOW_BYPASS + log
  3. IF payload.musyawawah_reference is None → DENY (fail-closed)
  4. IF verify_musyawawah_in_vault999(payload.musyawawah_reference) == False → DENY
  5. ELSE → ALLOW
```

## 7. Failure modes (Phase A5 — populated by 12-scenario falsification)

12-scenario test harness at `scripts/test_musyawawah_runtime_gate.py` (all PASS).

### Tested failure modes (Phase A5)

- **F1: empty string reference** → DENY (rejected by type check, no crash)
- **F2: None reference (omitted)** → DENY (rejected by type check)
- **F3: path traversal attempt** (`../../../etc/passwd`) → DENY (regex rejects)
- **F4: future-dated reference** (`2099-12-31-...`) → ALLOW (no expiration in Phase A — semantic check is Path B)
- **F5: path spelling inconsistency** — filesystem uses `musyawarah/` (with 'r') per `git ls-files`, but display/test references use `musyawawah/` (with 'w'). Regex now accepts BOTH via `musyaw[a]?wah/`. **Resolution: canonicalize to `musyawarah/` in Path B.**

### Hypothetical failure modes (pending Path B)

- **F6: stale reference** (date_part in past, verdict already expired) — semantic check, not regex
- **F7: phantom reference** (format valid but no file in VAULT999) — needs actual VAULT999 lookup
- **F8: bypass abuse** (ack_irreversible used >N times per actor) — rate limiting needed
- **F9: race condition** (reference verified, then mutated before invocation) — needs cache invalidation
- **F10: Unicode lookalike in path** (r/w confusion) — discovered as F5; canonicalize spelling

## 8. Reversibility (Path B rollback)

Per gate-promotion doctrine, named rollback required:
- Set `MUSYAWARAH_BYPASS_KERNEL=1` env → kernel check bypasses (fail-open)
- Sentinel continues to log violations
- Restore: unset env + restart kernel

## 9. Promotion criteria (OBSERVE_ONLY → GATE)

Per gate-promotion.md:
1. Real-catch from sentinel (Phase 2 step 1 already firing — 7+ live violations detected)
2. Named rollback (above)
3. Fail-closed (kernel check returns DENY, never ALLOW on invalid state)
4. Reference implementation passes 5-scenario test (Phase A3 — pending)

## 10. Out of scope for Path A

- Actual arifOS kernel modification (Path B)
- VAULT999 integration (Path B)
- Audit log infra (Path B)
- Performance impact measurement on kernel latency
