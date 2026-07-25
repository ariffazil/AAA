# Pre-Audit Results — ADVERSARIAL SPEC EXTERNAL

> **Status:** Source-sealed ✅ (commit 93554ad68)
> **Live kernel:** 93554ad68 deployed, drift=false
> **GitHub:** github.com/ariffazil/arifOS @ 93554ad68
> **External mutation:** HOLD — observe/query/dry-run only
> **Next gate:** Action binding, durable nonce, session ownership, evidence resolution

---

## Fix Status

| # | Fix | File | Source-Sealed | Runtime Attested |
|---|---|---|---|---|
| P1 | Ed25519 forge gate (stage_03b) | `forge_preflight.py` | ✅ 93554ad68 | ✅ 16 critical modules |
| P1 | Per-call Ed25519 enforcement | `tools/forge.py` | ✅ 93554ad68 | ✅ tracked |
| P2 | Empty evidence → BLOCK | `kernel/judge.py` | ✅ 93554ad68 | ✅ tracked |
| P3 | F13 FIRST-SEAL-WINS ordering | `kernel/judge.py` + `FLOOR_TABLE.json` | ✅ 93554ad68 | ✅ tracked |
| | Evidence receipt passthrough | `tools/judge.py` | ✅ 93554ad68 | ✅ tracked |

## Remaining Gaps (Before External Mutation)

| Gap | Severity | Status |
|-----|----------|--------|
| Cross-action replay | P0 | NOT FIXED — signature covers action_hash but nonce not durable |
| Spent-seal replay | P0 | NOT FIXED — Python set, not durable ledger |
| Cross-session lift | P0 | NOT FIXED — session ownership not enforced at forge gate |
| Dangling evidence | P1 | NOT FIXED — evidence references not resolved to content_hash |

## Operator Readiness

```
Observe / inspect / query   ✅ READY
Reason / critique           ✅ READY
Dry-run                     ✅ READY
Advisory judgment           ⚠️ LIMITED
Write / generate            ❌ HOLD
Commit                      ❌ VOID
Deploy                      ❌ VOID
Multi-operator execution    ❌ NOT READY
```

## What External Operator Sees

```
tools/list → arif_forge exposes:
  - actor_signature: str | None (ACTIVE — required for mutation)
  - nonce: str | None (ACTIVE — required with signature)
  - mode, manifest, session_id, plan_id, ...
```

## Build Reproducibility

```
git clone https://github.com/ariffazil/arifOS
git checkout 93554ad68
uv sync --frozen
uv run arifos serve
# → /health reports source=93554ad68 built=93554ad68 deployed=93554ad68 drift=false
```
