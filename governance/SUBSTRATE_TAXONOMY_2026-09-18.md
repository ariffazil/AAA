# SUBSTRATE TAXONOMY 2026-09-18 (F13 SEAL · Anti-False-Green)

> **Status:** F13_RATIFIED_CHAT 2026-09-18 — "Anti-False-Green substrate taxonomy"
> Canonical: this file supersedes the binary FAIL/PASS verdict vocabulary
> for Observatory emission semantics. State-transition vocabulary is mandatory;
> a single word without a named state is a transition lie.

---

## 0. Provenance

| Field | Value |
|---|---|
| **Ratified** | 2026-09-18 (UTC 18:14 / MYT 02:14) |
| **Trigger** | Observatory snapshot obs_20260917_180016 — substrate_state reported FAIL while 11/11 federation edges reachable, 8/8 organs UP, Ed25519 valid, P1-1..P1-6 SEALED |
| **Verdict (audit)** | PARTIAL — Infrastructure ALIVE, Capability DEGRADED, Constitutional OBSERVE_ONLY |
| **Classification** | Epistemic collapse in emission vocabulary, NOT infrastructure outage |
| **F13 Class** | D1 (Doktrin / doctrine patch) — non-mutating; only vocabulary canon |
| **Authority** | ARIF GO (choice 1 of 3) |
| **Status** | SEALED — `/root/AAA/governance/` chattr +i after write |
| **Iron rule** | Emission wording change at runtime is F13 binary scope; this file SEALs the *canon* only |

---

## 1. Why a 5-state taxonomy (not binary)

The single word `FAIL` collapses two structurally different conditions:

1. **Defect / Outage** — physical failure requiring repair (port dead, daemon crashed, process missing).
2. **Restraint / Boundary** — machine alive but mutation authority gated (F13 SOVEREIGN holds, witness insufficient, observer session did not authorize).

Operators reading a `FAIL` label will, by training, assume (1) and may page an on-call engineer at 02:00 for a system that is in condition (2) — sleeping under its own doctrine, not failing.

This is an **Epistemic Collapse**: one label carries two semantics; the wrong one triggers attention leaks and false alarms.

The doctrine reference is `state-transition-discipline.md`:

> "Single-word verdicts hide entire state machines... saying 'done', 'sent', 'true', or 'fail' without naming which state you actually achieved is a transition lie."

---

## 2. The Five Canonical Substrate States

```
┌────────────────────────────────────────────────────────────────────────┐
│                    ARIFOS SUBSTRATE TAXONOMY (5)                       │
├──────────────────┬─────────────────────────────────────────────────────┤
│ 1. OUTAGE        │ Port dead, daemon crash, process missing (Physical) │
│ 2. DEGRADED      │ Port alive, but latency high / telemetry drift      │
│ 3. IDLE_RESTING  │ Substrate alive, no active workload, no session     │
│ 4. FAIL_CLOSED   │ Alive & vigilant, but mutation authority LOCKED      │
│ 5. ACTIVE_SEALED │ All measured floors attested within mutation session │
└──────────────────┴─────────────────────────────────────────────────────┘
```

### 2.1 OUTAGE
- **Physical reality:** service unreachable or process absent.
- **Operator action:** page on-call, diagnose, repair.
- **Constitutional posture:** F13 is not gating anything because F13 has nothing to gate. The system cannot evaluate floors in this state.

### 2.2 DEGRADED
- **Physical reality:** service reachable but behaving below SLO (latency, drift, partial failure).
- **Operator action:** investigate, decide whether to escalate.
- **Constitutional posture:** floors may be evaluated but at least one is below threshold for non-doctrinal reasons.

### 2.3 IDLE_RESTING
- **Physical reality:** substrate alive, no observer session, no work scheduled.
- **Operator action:** none expected. This is the normal sleeping state.
- **Constitutional posture:** floors are not "failed"; they are simply not under test. The watchdog is awake; the work is not.

### 2.4 FAIL_CLOSED
- **Physical reality:** substrate alive, observer session active, but F13 SOVEREIGN or one of gates F2/F3/F5/F6 refuses to grant mutation authority.
- **Operator action:** review gate floor, do not interpret as outage.
- **Constitutional posture:** principled restraint. The machine is awake AND being asked something, but the doctrine says no — sabr, not failure.

### 2.5 ACTIVE_SEALED
- **Physical reality:** substrate alive, mutation session active, all required floors attested.
- **Operator action:** mutation is in progress; observe the receipt chain.
- **Constitutional posture:** the only state where green light is honest. Obtained through `arif_judge`, not by default.

---

## 3. Disambiguating IDLE_RESTING vs FAIL_CLOSED

Both states emit "no mutation happening," but the upstream provenance differs:

- **IDLE_RESTING** is the *default state*. No session was opened. The cage is locked because there is nothing to put in it.
- **FAIL_CLOSED** is *active restraint under load*. A session exists, evidence arrived, but F13 — or one of F2/F3/F5/F6 — declined the verdict that would open gates.

A substrate in IDLE_RESTING cannot transition to OUTAGE silently: the watchdog wakes it. A substrate in FAIL_CLOSED requires an ARIF GO to clear, not a restart.

This distinction lives *upstream* of emission — in how `arif_judge` tags the session. Runtime emission in this canon may use the same surface token (e.g. `HOLD`) but the upstream tag MUST distinguish them when persistence matters (VAULT999 receipts, audit replays).

---

## 4. Mapping old vocabulary → new taxonomy

| Old emission            | New emission                | Why |
|-------------------------|-----------------------------|-----|
| `UNKNOWN` (no probe)    | `UNKNOWN` (kept)            | honest absence of data |
| `FAIL` (port dead)      | `OUTAGE`                    | explicit physical fault |
| `DEGRADED` (latency)    | `DEGRADED` (kept)           | already correct |
| `FAIL` (idle, healthy)  | `IDLE_RESTING`              | doctrine not defect |
| `FAIL` (gate hold)      | `FAIL_CLOSED`               | restraint not defect |
| `PASS` / green by default | `ACTIVE_SEALED` (only when attested) | anti-false-green |

The substring `FAIL` MUST NOT appear in any emission where the substrate is alive at the transport layer. If the watchdog sees a port, it is not in `OUTAGE`. If it is in `OUTAGE`, the port is gone — use that word.

---

## 5. What this SEAL does, and what it does not

### Does
- Records the 5-state taxonomy as canonical doctrine.
- Names `Epistemic Collapse` as the failure mode being prevented.
- Anchors the disambiguation IDLE_RESTING vs FAIL_CLOSED upstream of emission.
- Provides a contract any future Observatory iteration must speak.

### Does NOT
- Touch runtime emission in `observatory_routes.py`.
- Modify the watchdog math (`floors_passing < floors_loaded → ...`).
- Auto-relabel past snapshots. Past `FAIL` readings are preserved verbatim
  in VAULT999 with their original semantics; re-tagging them would be
  retroactive fraud.
- Replace `UNKNOWN`. `UNKNOWN` remains the honest verdict when no probe
  has returned.

---

## 6. Forward decisions (F13 HOLD — not auto)

The following are *open* and await ARIF GO before any execution:

- Run emission rewrite in `observatory_routes.py` to surface the 5 labels.
- Compose gotong-royong for F-002 / F-004 / F-005 / F-006 / F-008.
- Adopt this taxonomy in the cockpit (`arifos-board`) footer.
- Publish externally (arif-fazil.com). Currently internal-only.

The SEAL above is the doctrinelock for these future moves; it does not
authorize them.

---

## 7. Receipt

- File: `/root/AAA/governance/SUBSTRATE_TAXONOMY_2026-09-18.md`
- Ceremony: chattr -i → write → chattr +i
- Time: 2026-09-18 UTC 18:14 (MYT 02:14)
- Authority: ARIF GO (choice 1 of 3: HOLD + SEAL)
- Mode: OBSERVE_ONLY → HOLD (no runtime mutation)
- Audit log: appended beside the 2026-09-18 chattr ceremony receipts
