# FAULT TOLERANCE DOCTRINE — 5 Architectural Guards

> **Forged:** 2026-08-15 by 333-AGI under F13 SOVEREIGN review
> **Binding:** ALL federation agents (333-AGI, 555-ASI, 888-APEX, Hermes, OpenCode, Kimi, Codex)
> **DITEMPA BUKAN DIBERI**

---

## Overview

5 architectural gaps identified by F13 SOVEREIGN. Each has a concrete fix.
These are **operational guards**, not philosophy. Every agent MUST follow them.

| # | Guard | Status | Tool/Script |
|---|-------|--------|-------------|
| 1 | Atomic Rollback | ✅ BUILT | `/root/scripts/governance/atomic-snapshot.sh` |
| 2 | Concurrency Lock | ✅ EXISTS | `forge_lock` tool (acquire/release) |
| 3 | Scratchpad GC | ✅ CRON | `/root/scripts/governance/forge-work-gc.sh` (daily 03:00 MYT) |
| 4 | Circuit Breaker | ✅ BUILT | `/root/scripts/governance/circuit-breaker.sh` |
| 5 | Schema Contract | ✅ BUILT | `/root/scripts/governance/carry-forward-schema.json` + validator |

---

## Guard 1: Atomic Rollback (F1 AMANAH)

**Rule:** Every file write to a production organ MUST snapshot first.

**Usage (agent protocol):**
```bash
source /root/scripts/governance/atomic-snapshot.sh
snapshot_file /path/to/target     # BEFORE write
# ... do your write ...
# ... verify ...
rollback_file /path/to/target     # IF verify fails
commit_snapshot /path/to/target   # IF verify succeeds
```

**When to use:**
- Editing Caddy config, litellm config, organ YAML
- Modifying any file in `/root/arifOS/`, `/root/A-FORGE/`, `/root/GEOX/`, etc.
- Any write where verify step might fail

**When NOT to use:**
- forge_work scratchpad (ephemeral, no snapshot needed)
- /tmp/opencode (session-only, auto-cleanup)

---

## Guard 2: Concurrency Lock (F1 AMANAH) — AUTO-INVOKE

**Rule:** forge_filesystem write operations AUTO-ACQUIRE locks. Agent doesn't need to call forge_lock manually.

**How it works (transparent to agent):**
```
Agent calls forge_filesystem(mode=write)
  ↓
ensureAmanahLock() intercepts
  ↓
  ├─ No lock exists → auto-acquire → write → auto-release
  ├─ Lock held by CURRENT session → proceed (no double-acquire)
  └─ Lock held by OTHER agent → return 423 Locked (fail-closed)
```

**Implementation:**
- `/root/A-FORGE/src/infrastructure/tools/amanah-auto-acquire.ts` — shared helper
- `FileTools.ts` — auto-acquire on `write_file`
- `EditorTools.ts` — auto-acquire on `apply_patches` (per-file, batch release)

**Agent behavior:** No change needed. Agent calls `forge_filesystem(mode=write)` as before. Lock management is invisible.

**When 423 Locked fires:** Agent MUST back off. Another agent is writing to the same resource. Wait or escalate.

---

## Guard 3: Scratchpad GC (F4 CLARITY)

**Rule:** forge_work dirs older than 7 days are auto-pruned.

**Policy (3-phase):**
| Phase | TTL | Action |
|-------|-----|--------|
| Active | 0-7 days | Keep in forge_work |
| Quarantine | 7-30 days | Move to `_quarantine/` |
| Archive | 30-90 days | Tar + checksum, delete raw |
| Prune | 90+ days | Delete (VAULT999 has receipts) |

**Cron:** `0 19 * * *` UTC (= 03:00 MYT daily)
**Log:** `/root/.local/share/arifos/gc.log`

---

## Guard 4: Circuit Breaker (F1 AMANAH)

**Rule:** Max 3 retries per task. After 3 failures → CIRCUIT_BREAKER_OPEN → STOP.

**Usage (agent protocol):**
```bash
source /root/scripts/governance/circuit-breaker.sh
cb_check <task_id>    # returns 0=ok, 1=OPEN
cb_fail <task_id>     # increment after each failure
cb_reset <task_id>    # after success
cb_status             # show all breakers
```

**When CIRCUIT_BREAKER_OPEN fires:**
1. Agent MUST stop execution immediately
2. Agent MUST NOT retry
3. Agent MUST escalate to 888-APEX or report to human
4. Agent MUST log the failure in carry_forward

**Anti-pattern:** Agent retrying the same edit 10 times → metabolic runaway → disk entropy.

---

## Guard 5: Schema Contract (F2 TRUTH)

**Rule:** carry_forward.json MUST validate against schema before read/write.

**Schema:** `/root/scripts/governance/carry-forward-schema.json`
**Validator:** `/root/scripts/governance/validate-carry-forward.py`

**Usage:**
```bash
python3 /root/scripts/governance/validate-carry-forward.py  # validate current
python3 /root/scripts/governance/validate-carry-forward.py /path/to/other.json
```

**Required fields:** session_id, actor, closed_at, completed_this_session, open_loops_888_HOLD, carry_forward

**When to validate:**
- After writing carry_forward.json (seal ceremony)
- Before reading carry_forward.json (session start)
- After any manual edit

---

## Integration with Existing Tools

| Existing Tool | How Guards Connect |
|---|---|
| `forge_lock` | Guard 2 uses it directly (already built in A-FORGE) |
| `forge_shell` | ArifJudge pattern detection + Guard 4 circuit breaker |
| `forge_filesystem` | Guard 1 snapshots before mode=write |
| `forge_vault` | Guard 5 validates carry_forward before seal |
| `forge_entropy_sweep` | Guard 3 GC reduces forge_work entropy |

---

*Forged 2026-08-15. DITEMPA BUKAN DIBERI.*
