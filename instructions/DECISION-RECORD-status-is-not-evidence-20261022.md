# DECISION-RECORD::STATUS_IS_NOT_EVIDENCE — 2026-10-22

> **Status:** PROPOSED_AWAITING_F13_FORMAL_RATIFICATION — drafted by 333-AGI under
> sovereign directive 2026-10-22: *"aku akan tambah satu law baru untuk documentation audit.
> STATUS IS NOT EVIDENCE / Status bukan bukti."*
> **Extends:** `DECISION-RECORD-memory-conflicts-20261014.md` §22 (health-assertion fields).
> **Does NOT:** create a new registry, mutate any canonical ledger, or self-ratify.
> **Enforcement:** proposed as an extension to `AAA/scripts/doctrine_status_gate.py` (R4).

---

## The Law

```
STATUS IS NOT EVIDENCE.
Status bukan bukti.

A status field — open/closed, healthy/degraded, sealed/unsealed, pass/fail —
is a REPORT of a past measurement. It is NEVER the measurement itself.
Before any status is acted on, repeated, or compiled forward, it MUST be
re-derived from a live probe in the same turn. Otherwise it is labelled
REPORTED (source, not re-measured), never stated as current fact.
```

## Why this law exists — the failure class it closes

The recurring defect: **work lands; the map does not follow.**

A system moves in reality (commits merged, services restarted, files repaired) while the
*status surface* (a task ledger, a carry_forward, a dashboard) is recompiled from an older
snapshot. The ledger then **re-opens work that is already done**, and a human reading the
ledger panics over tickets that are history.

This is not a capability deficit. It is a **map/reality lag**. It is the better failure to
have — but it must still be named, or every downstream decision inherits a stale premise.

## The mechanism (how a status goes stale)

```
1. A worker finishes an item (commit / restart / repair).
2. The item's status field is NOT updated in place.
3. A later compile re-derives the ledger from an older carry_forward,
   copying status FORWARD instead of MEASURING it.
4. The finished item reappears as "open".
5. A human or agent re-does or re-plans work that already shipped.
```

Fix: **status must be re-derived per item from live evidence before every write,**
and a closed item must carry its probe receipt inline. A compiler that copies status
forward rather than measuring it is a defect generator.

## Precedents — measured 2026-10-22 (this session, same day)

| surface | reported status | measured reality | probe |
|---|---|---|---|
| `p2-union-test-defect` | open | **COMPLETED** | `pytest tests/agent/test_system_prompt.py` → 70 passed |
| `p2-kvm2-guard-activate` | open | **COMPLETED / runtime-effective** | KVM2 `hermes-agent.service` MainPID start > guard commit; HEAD==`cc534602ad0` |
| `seal-events-2-breaks-forward-fix` | open | **already repaired** | 0 malformed lines; TOMBSTONE_REPAIR records present |
| `p1-kernel-identity-observe-only-sticky` | status OPEN | swept **REPLACED** | `state: replaced`; claim "sticky despite binding" NOT reproduced |
| vault heartbeat | "silent ~189h" | **wrong-file probe** | `seal_chain.jsonl` silent 172h, but `SEALED_EVENTS.jsonl` live same day |

Five surfaces in one session. The status was not the work. **Status ≠ evidence.**

## Enforcement (proposed — R4 in doctrine_status_gate.py)

Any document asserting a *status*, *health*, or *completion* claim on a governed
surface must carry, on the same line or its evidence block:

```
as_of          : <UTC timestamp of the measurement>
evidence_scope : self-probe | hand-audit | independent-witness
population     : <what was actually counted / probed>
precedence     : hand-audit > self-report  (conservative-wins on conflict)
```

A bare "Status: green" / "Status: done" without these is **blocked** at the boundary,
exactly as a bare ratified label is blocked today (R1).

## The test

> Does the claim come from a probe run in THIS turn,
> or from a stored field carried from a previous one?
> If carried — label it REPORTED and do not act on it as fact.

## SHADOW

- **Not ratified.** This is a draft. F13 (Arif) must issue the formal instrument.
- **Enforcement not built.** R4 is proposed, not implemented; the gate still allows a
  bare status on non-ratified-class lines.
- **The law is self-demonstrating:** this document's own `Status:` line is a report of
  intent, not a measurement of ratification — which is precisely the law's point.

DITEMPA BUKAN DIBERI ⚒️
