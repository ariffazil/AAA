# Degradation Mode Specification v1 — G5 (Wawa D1)

> **EUREKA P1, G5** — What happens when federation organs are unreachable,
> truth records conflict, or sovereign is unavailable during time-sensitive actions.
>
> **Status:** RATIFIED — governance doctrine
> **Date:** 2026-07-13
> **Author:** Hermes-Prime (on Arif F13 directive, Wawa gap analysis)
> **Floors:** F1 AMANAH, F3 WITNESS, F11 AUDIT, F13 SOVEREIGN
>
> *This spec defines system behaviour under degradation. It does NOT authorise
> self-modification. All degradation paths return through constitutional review.*

---

## 1. Principles

### 1.1 Fail-Closed by Default

When an organ is unreachable, the system must **fail closed** (block the action)
unless a specific degradation path is defined in this document. Silent fallback
to a less-authoritative source is forbidden unless explicitly approved.

### 1.2 Degradation Is Observable

Every degradation event must produce a structured record in VAULT999:
- `event_type: "degradation.event"`
- Severity: `INFO | WARNING | CRITICAL`
- Organ affected, duration, fallback action taken
- Resolution (how normal service was restored)

### 1.3 Sovereignty Is Non-Delegable

When F13 SOVEREIGN (Arif) is unreachable AND a time-sensitive irreversible
action is pending, the system must **wait, not act**. Emergency delegation
requires pre-authorized time-locked escalation (see §4).

### 1.4 Reconciliation After Recovery

After any degradation path activates, a mandatory reconciliation step runs
when all organs are healthy again. Inconsistencies are recorded as COOLING
receipts, not silently resolved.

---

## 2. Degradation Scenarios

### 2.1 Governance Plane Unreachable (arifOS :8088 down)

| Aspect | Definition |
|--------|-----------|
| **Detection** | A-FORGE health check timeout (`/health`) > 5s, 3 consecutive failures |
| **Effect** | All `arif_judge` calls fail. No new verdicts. No new SEALs from governance path. |
| **Degradation path** | **OBSERVE-ONLY.** Read tools continue (forge_shell_dryrun, forge_git_log, etc.). MUTATE/IRREVERSIBLE tools block. Existing leases continue until TTL expiry. |
| **Cached authority** | Last-known-good floor state from `/root/.local/share/arifos/governance_floors.json` (updated on every successful arif_judge call). This cache is used for OBSERVE-only classification, never for MUTATE authorization. |
| **Timeout** | Maximum degradation: 300s (5 min). After that, all non-OBSERVE tools HOLD even with local cache. |
| **Recovery** | On governance restore, all tools that were held during degradation emit COOLING receipts: `cooling_source: "post_verification"`, `severity: "MINOR"`, `drift_dimension: "timing_anomaly"`. |
| **Reconciliation** | Forced re-validation of all lease decisions made during degradation window. Any inconsistency → `violated_floors: ["F3", "F11"]`. |

### 2.2 Truth Plane Has Conflicting Records (VAULT999)

| Aspect | Definition |
|--------|-----------|
| **Detection** | seal_chain.js `verify` returns `ok: false` (prev_hash mismatch at any seq) |
| **Effect** | The seal chain is broken. New SEALs CANNOT be appended until the chain is repaired. |
| **Degradation path** | **APPEND-ONLY SUSPENDED.** Reads continue (getHead, getRecent, summary). The chain is frozen at the last-known-good head. All new seal writes are queued to `/root/VAULT999/deferred_seals.jsonl` with a timestamp. |
| **Conflict resolution** | 1. Identify the broken entry by running `verify` with `broken_at_seq` 2. Examine ledger entries around the break 3. If competing writers detected, the LOWEST `seq` wins (F11 AUDIT principle) 4. Disputed entries are quarantined to `VAULT999/quarantine/` 5. Chain is repaired by removing quarantined entries and writing a `RECONCILIATION` marker 6. Deferred seals are written in order after reconciliation |
| **Which source wins** | The seal_chain.js canonical writer is the sole authority. Any entry NOT produced by seal_chain.js write() is suspect. The `prev_hash` chain defines truth — if two entries have the same seq, the one matching the prev_hash chain wins. |
| **Conflict flagging** | Every conflicting entry is flagged in the output with `_conflict: true`, the reason (prev_hash mismatch, duplicate seq), and the quarantined entry for audit. |
| **Recovery** | Manual (Arif or authorized agent) must review quarantined entries and approve chain repair. Automated repair is FORBIDDEN for conflicts involving REPLACED entries (F1 AMANAH). |

### 2.3 Sovereign Unavailable + Time-Sensitive Action (F13)

| Aspect | Definition |
|--------|-----------|
| **Detection** | No response from Arif within expected window (configurable per action class, default: IRREVERSIBLE=immediate HOLD, EXECUTE_HIGH_IMPACT=300s escalation wait) |
| **Effect** | IRREVERSIBLE actions block immediately. EXECUTE_HIGH_IMPACT actions enter a 300s grace period. |
| **Emergency delegation** | NOT AVAILABLE in v1. Timeline for v2: pre-authorized time-locked escalation contracts where Arif pre-signs specific emergency delegation rules (e.g., "If I'm unreachable for 24h AND the system detects a security breach, A-FORGE may rollback the last 3 commits without further judgment"). |
| **What happens** | The action is pended to `/root/VAULT999/f13_pending/` with full envelope. A NOTICE_BOARD entry is created. All organs continue at OBSERVE-ONLY until sovereign returns. |
| **Escalation cadence** | After 300s: NOTICE_BOARD warning. After 1h: AAA cockpit alert. After 24h: system-wide HOLD on all non-OBSERVE tools. |
| **Recovery** | Arif reviews pending actions on return. Each is individually approved, rejected, or deferred via `arif_judge` with `F13_SOVEREIGN` authority. |

### 2.4 Execution Plane Reports Success But Continuity Shows Inconsistency

| Aspect | Definition |
|--------|-----------|
| **Detection** | A-FORGE returns `{verdict: "SEAL", ...}` but post-execution verification (via `forge_runtime_verify` or seal_chain.js verify) shows divergence from expected state |
| **Effect** | The seal was written but the system state is uncertain. |
| **Degradation path** | **QUARANTINE.** The action is flagged in VAULT999 with `verification_status: "INCONSISTENT"`. All actions that depend on this execution are held pending verification. |
| **Rollback** | Not automatic. A COOLING_RECEIPT is emitted with `drift_dimension: "runtime_commit"` and routed to governance. arif_judge decides SEAL (accept divergence), HOLD (defer), or VOID (reject). |
| **Recovery** | Once governance decides: if SEAL, the divergence becomes the new expected state. If HOLD, the action is re-executed with verification. If VOID, the divergence is rolled back (manual). |

---

## 3. Degradation State Machine

```
                    ┌──────────────┐
                    │   NORMAL     │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
      ┌────────────┐ ┌──────────┐ ┌──────────┐
      │ GOVERNANCE │ │  TRUTH   │ │SOVEREIGN │
      │ DEGRADED   │ │ BROKEN   │ │ UNAVAIL  │
      └──────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             ▼            ▼            ▼
      OBSERVE-ONLY   APPEND-FROZEN   PENDING
      MUTATE→HOLD    READS-ONLY      OBSERVE-ONLY
             │            │            │
             └─────┬──────┴──────┬─────┘
                   ▼             ▼
           ┌────────────┐ ┌────────────┐
           │ QUARANTINE │ │ESCALATION  │
           │ (multi)    │ │(escalated) │
           └────────────┘ └────────────┘
                   │
                   ▼
          RECONCILIATION
          ┌──────────────┐
          │  COOLING     │
          │  receipts    │
          └──────┬───────┘
                 │
                 ▼
           ┌──────────┐
           │  NORMAL  │
           └──────────┘
```

---

## 4. Pre-Authorized Time-Locked Escalation (v2 Design)

In v1, all sovereign-unavailability cases block. For v2:

1. **Pre-sign contracts:** Arif signs a contract offline (Ed25519) specifying:
   - Trigger conditions (e.g., "Sovereign unreachable > 24h AND security breach detected")
   - Authorized actions (e.g., "rollback last 3 git commits")
   - Expiry (e.g., "valid for 48h after signing")
   - Boundary (e.g., "no database changes, no VAULT999 seal deletion")

2. **Storage:** The signed contract is stored encrypted in VAULT999 as `event_type: "emergency.contract"`.

3. **Execution:** When trigger conditions are met AND sovereign is unreachable, A-FORGE (after 24h) decrypts the contract, verifies the signature, and executes the bounded actions.

4. **Audit:** Every action under emergency delegation produces a full audit trail with `authority: "emergency_delegation"` and the contract hash.

---

## 5. Monitoring

### 5.1 Degradation Probe

Every 60s, the federation health check probes all organs:
```json
{
  "degradation_active": false,
  "organs": {
    "arifOS": {"healthy": true, "latency_ms": 12},
    "A-FORGE": {"healthy": true, "latency_ms": 8},
    "AAA": {"healthy": true, "latency_ms": 15},
    "GEOX": {"healthy": true, "latency_ms": 42},
    "WEALTH": {"healthy": true, "latency_ms": 23},
    "WELL": {"healthy": true, "latency_ms": 18}
  }
}
```

### 5.2 Degradation Recording

Every degradation event is recorded:
```json
{
  "event_type": "degradation.event",
  "timestamp": "2026-07-13T01:00:00Z",
  "organ": "arifOS",
  "severity": "WARNING",
  "duration_seconds": 45,
  "fallback": "OBSERVE_ONLY",
  "resolution": "AUTO_RECOVERED",
  "affected_actions": 3
}
```

---

## 6. Summary

| Scenario | Fallback | Blocks | Records To |
|----------|----------|--------|------------|
| Governance unreachable | OBSERVE-ONLY | MUTATE/IRREVERSIBLE | COOLING receipt |
| Truth chain broken | APPEND-FROZEN | New SEALs | Quarantine + F13 notification |
| Sovereign unavailable | PENDING | IRREVERSIBLE after grace | F13 pending queue |
| Inconsistent execution | QUARANTINE | Dependent actions | COOLING receipt |

*DITEMPA BUKAN DIBERI — Degradation is observed, not improvised.*
