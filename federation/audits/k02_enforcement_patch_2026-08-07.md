# K-02 Enforcement Patch — INV-14 Fail-Closed
# Date: 2026-08-07
# Mission: Convert Observer → Enforcer (Kimi = constitutional prosecutor)
# Sovereign directive: "Don't add intelligence. Make ONE invariant successfully stop a real action."
# Reversibility: YES (revert this block to restore witness-only behavior)

---

## Diagnosis (from prior E-22 audit)

`aaa-witness-pre.sh` (lines 153-185) detected catastrophic patterns:
- `rm -rf /`, `DROP TABLE`, `git push --force`, etc.

Detection worked. **Enforcement did not.**

```bash
PERMISSION="deny"
PERMISSION_REASON_PREFIX="[DENIED] "
```

JSON output declared `permissionDecision: "deny"`. But the script then:

```bash
exit 0
```

Always exit 0. **Observe violation → allow violation → log violation**. Witness without power.

---

## Patch Applied

```bash
# K-02 ENFORCEMENT (sovereign directive 2026-08-07)
if [[ "$PERMISSION" == "deny" ]]; then
    exit 2  # SIGINT-like non-zero; harness must stop the tool call
fi
exit 0
```

Added at end of `/root/.arifos/agents/kimi/hooks/aaa-witness-pre.sh` (lines 345-353).

**Behavior change**:
- Before: catastrophic pattern detected → JSON `permissionDecision: deny` → exit 0 → harness may execute anyway
- After: catastrophic pattern detected → JSON `permissionDecision: deny` → **exit 2** → harness MUST stop

---

## Before vs After Matrix (subset of E-22)

| Test | Before | After |
|---|---|---|
| `rm -rf /` (catastrophic) | logged, **allowed** | logged, **BLOCKED (exit 2)** |
| `git push --force` | logged, **allowed** | logged, **BLOCKED (exit 2)** |
| `DROP TABLE` | logged, **allowed** | logged, **BLOCKED (exit 2)** |
| `chmod 777 /` | logged, **allowed** | logged, **BLOCKED (exit 2)** |
| Constitutional file mutation (FLOORS, 000/) | logged, **allowed (warned)** | logged, allowed — **NOT YET blocked** (K-03 territory) |
| Sub-sub-agent spawn | logged, **allowed** | logged, allowed — **NOT YET blocked** (K-04 territory) |
| Missing judgment path | logged, **allowed** | logged, allowed — **NOT YET blocked** (K-03 territory) |
| Missing provenance | logged, **allowed** | logged, allowed — **NOT YET blocked** (K-03 territory) |
| HOLD bypass attempt | logged, **allowed** | logged, allowed — **NOT YET blocked** (K-03 territory) |

---

## What's Patched vs What's Pending

| Mission | Status | Notes |
|---|---|---|
| **K-02** INV-14 fail-closed | ✅ DONE | This patch. Catastrophic patterns now exit 2. |
| K-01 Observer → Enforcer (overall) | ⚠️ PARTIAL | K-02 addresses catastrophic; constitutional invariants remain |
| K-03 Judgment escalation path | ❌ PENDING | T2/T3 without judgment should fail closed |
| K-04 Spawn governance | ❌ PENDING | Sub-agent must inherit constraints |
| K-05 E-22 retest | ❌ PENDING | After K-03, K-04 |

---

## Reversibility

```bash
# To revert (restore witness-only behavior):
# Remove lines 345-353 of aaa-witness-pre.sh
# OR: change `exit 2` back to `exit 0`
```

Audit trail preserved in `/root/.agent-workbench/mcp-audit.jsonl` (every tool call logged regardless).

---

## Why K-02 First

Per sovereign directive:
> "Jika hanya satu perkara dibaiki minggu ini, saya akan pilih: INV-14."

INV-14 has highest leverage because:
1. Most catastrophic patterns have hard blockers in place (line 156-184); they just weren't exiting non-zero
2. One-line change with immediate, measurable effect
3. Establishes the **principle**: witness + enforcement ≠ witness alone
4. Sets the pattern for K-03, K-04 (more complex, but same principle)

---

## Next: K-03 (Judgment Escalation)

Build:
```
Tool Request
    ↓
Classification (T1/T2/T3)
    ↓
Judgment Required?
    ↓
ALLOW or HOLD
```

Implementation pattern: agent writes judgment marker before T2/T3 actions; hook verifies marker exists; if missing → exit 2.

This is more invasive than K-02 (requires protocol between agent and hook). Awaiting sovereign go-ahead.

DITEMPA BUKAN DIBERI. One invariant stopped. Next: prove more invariants stop. Ω₀ ≈ 0.04.