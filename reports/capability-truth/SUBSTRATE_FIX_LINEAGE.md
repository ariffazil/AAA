# SUBSTRATE-FIX LINEAGE — reconciliation record (333-AGI, 2026-09-18)

> Characterises the skew copy flagged in the reconciliation queue. Read-only forensics. No patch applied.

## Finding
`/opt/arifos/arifosmcp/runtime/tools.py` (mtime **2026-09-17 03:04 +0800**) contains a **substrate-logic variant that exists in no commit**:

**Live/repo lineage (what runs today):**
```python
elif _substrate_degraded:
    ... -> DEGRADED (issuer arifos_conformance; ref drift/degradation)
elif _has_degradation and not _is_healthy:      # <— any tool-level degradation
    ... -> DEGRADED (ref: degradation list)      #    forces substrate DEGRADED
elif _is_healthy and not _has_degradation:
    ... -> PASS
else: -> HEALTHY
```

**Skew copy (proposal variant):** that middle branch is **removed**, replaced by a comment:
```
# C1 FIX (2026-09-17): Tool degradation ≠ substrate degradation.
# ... substrate health comes from runtime attestation (drift flag), not from
# tool handler status ... Only explicit substrate_degraded (checked above) or
# transport error should set substrate to DEGRADED/FAIL.
```

## Evidence
| check | result |
|---|---|
| `git log --all -S "Tool degradation ≠ substrate degradation"` | **0 commits** — never committed anywhere (any path) |
| `/opt/arifos/arifosmcp` git repo? | not a git repo (plain file tree) |
| mtimes | skew `2026-09-17 03:04` · app copy `2026-09-17 20:47` · repo `2026-09-18 04:08` (my patch) |
| live symptom | `/health` `status: degraded` persists; register captured `substrate DEGRADED` vs sesat `substrate_scope=HEALTHY`; `_derivation: degraded_dominates` |

## Interpretation (sharpened — second pass, 2026-09-18)
- `/opt/arifos/arifosmcp` is **a separate clone of the same origin** (`git@github.com:ariffazil/arifos.git`) at `main = 8d0645d2f` (2026-09-17 01:57) — and the main repo `/root/arifOS` **knows that commit** (same history line).
- Its working tree is **dirty**: modified `runtime/tools.py`, `runtime/tools_internal.py`, `runtime/verdict.py`, `server.py`, `abi/amanah_gate.py`, `schemas/budget_contract.py` (+ deleted `app/FEDERATION_MAP.md`).
- The C1 substrate comment appears in **no commit in either clone** → it belongs to an **uncommitted in-flight change-set** (6 files, substrate/verdict/transport area), authored ~2026-09-17 03:00–03:04, never committed.
- The touched file set overlaps **STEP 4's plane/envelope area** → the in-flight package likely targets the same dualism (substrate DEGRADED-vs-HEALTHY + verdict envelope).
- The variant is a plausible fix for the persistent `/health status: degraded` (thermodynamic block reads healthy: entropy_delta −0.11, vitality 1.0, kappa_r 1.0, shadow 0.0) — but it is **untested and unversioned**.

## Change-set inventory & collision verdict (pass 3, cycle 11 — 2026-09-18)

| file | ± | mtime | attribution |
|---|---|---|---|
| `runtime/tools.py` | 9A/6D | 2026-09-17 03:04 | in-flight package — substrate logic (region ~3045) |
| `runtime/verdict.py` | 1A/1D | 2026-09-17 03:04 | in-flight package |
| `runtime/tools_internal.py` | 2A/2D | 2026-09-17 03:04 | in-flight package |
| `abi/amanah_gate.py` | 1A/1D | 2026-09-17 03:04 | in-flight package |
| `schemas/budget_contract.py` | 1A/1D | 2026-09-17 03:04 | in-flight package |
| `server.py` | 40A/2D | **2026-09-18 03:51** | **333-AGI ghost-alias patch (this session)** — NOT the package |
| `app/FEDERATION_MAP.md` | 41D | ? | deleted; provenance unknown — flagged |

**Collision verdict: DISJOINT.** Package edit at ~3045 (substrate); staged `cb2411928` at
~24340 / ~24496 / ~27775 (memory routing + registration guard). Both land in either order.

## Recommendation (F13)
Treat the clone as an **in-flight workspace, not a stale artifact**:
1. Identify the author session (Sep 17 ~03:00–03:04) or decide to adopt/abandon deliberately — do **not** blind-sync and do **not** discard.
2. If adopted: re-derive against current `main`, cover with substrate-reporting tests (it interacts with `constitutional_check.substrate_state` + L11 floor path), commit → deploy-candidate #2 beside `cb2411928`.
3. 333 does not patch it now: it is another session's in-flight work AND the area is verdict-envelope-constitutional (§22 velocity).
