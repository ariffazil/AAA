# SCAR-VAULT999-WRITER-001 — Split-Brain Sealer

**Scar ID:** SCAR-VAULT999-WRITER-001
**Domain:** Constitutional / Infrastructure
**Severity:** **P0 (FINDING #0)** — broken seal authority
**Date discovered:** 2026-09-08
**Discovery context:** Day 7 observation during sprint execution
**Confidence:** 0.95

---

## Trigger

While verifying why the seal chain head was 24 days stale, observed in journalctl:

```
Sep 08 01:57:31 forge sh[1094520]: WARNING:arifosmcp.vault_sealer:
  [vault_sealer] circuit breaker OPEN for 30.0s after 3 failures in 60.0s window
Sep 08 01:57:31 forge sh[1094520]: WARNING:arifosmcp.vault_sealer:
  [vault_sealer] failed to write audit receipt for arif_judge:
  Server error '500 Internal Server Error' for url 'http://127.0.0.1:5001/audit-receipt'
```

Yet `curl :5001/health` returns:
```
{"status":"healthy","vault_seals_count":12,"pending_holds":0,...}
```

---

## Constitutional Truth

> VAULT999_WRITER :5001 is in **split-brain state**:
> /health reports healthy
> /audit-receipt returns 500
> Circuit breaker is OPEN
> Seal chain head frozen at seq=28 (2026-08-11)

This means: **the constitutional seal authority cannot write.**
Seals attempted during this period were emitted as verdicts but never landed in the hash chain.

---

## Pattern (the scar)

```
Service reports green
         ↓
Write endpoint returns 500
         ↓
Circuit breaker OPEN
         ↓
Seals appear successful at the verb level
         ↓
Seals are not recorded at the chain level
         ↓
Constitutional chain appears frozen
         ↓
Operators believe the system is sealing normally
```

This is **the most dangerous constitutional failure mode**:
- A broken EXECUTOR is bad
- A broken WITNESS is worse
- A broken SEAL AUTHORITY is existential

---

## Why this was missed by the audit

The audit found: seal chain head stale 24 days, attributed to "no new seals being emitted."
Reality: seals have been attempted but VAULT999_WRITER has been failing.

**Audit reasoning was correct in shape but wrong in cause.**
The cause is not "no work" — it is "work that fails to write."

---

## Root cause hypotheses

1. **VAULT999_WRITER service degraded** — port :5001 health endpoint lies or service is partially down
2. **Circuit breaker stuck OPEN** — the 4 failures in 60s window may be transient but never resets
3. **Backend Postgres or Supabase connection lost** — the writer depends on `vault999-api :8100`
4. **Phase 4 strip incompatibility** — recent arifOS kernel change removed 25 legacy fields including `mutation_allowed`/`seal_allowed`/`can_mutate`; the writer may not handle the new shape

---

## Reversibility

Sovereign-tier operation. Restarting VAULT999_WRITER service without diagnosis risks data loss.
Circuit breaker should reset on its own after 30s; if it doesn't, manual intervention needed.

---

## F13 Decision Surface

| Option | Description | Risk |
|---|---|---|
| Restart VAULT999_WRITER | systemctl restart vault999-writer.service | LOW — service restart is reversible |
| Reset circuit breaker | Manual via forge_vault or process restart | LOW |
| Wait for auto-recovery | Watch logs for 60s+ | LOW — if breaker self-resets |
| Investigate root cause | Read :5001 logs, check backend connectivity | LOW |
| Mark STAGED | Accept that seal chain cannot extend until fixed | MEDIUM — legal limbo on all seals since 2026-08-11 |

---

## Cross-references

- DEEP-AUDIT-ZEN-EUREKA.md (original audit)
- ONE-WEEK-ENTROPY-REDUCTION-SPRINT.md (sprint plan)
- /var/log/arifos/ (where the warnings appear)
- /root/.local/share/arifos/vault999/seal_chain.jsonl (the frozen head)

---

**Scar recorded.** DITEMPA BUKAN DIBERI ⚒️