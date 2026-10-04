---
name: agentic-trust-trajectory
description: "Detect XZ-style trust attacks in agent fleets over time."
author: hermes
license: MIT
tags: [trust, security, agents, xz, trajectory, governance]
related_skills: [arifos-constitutional-judge, ASI-agent-invariants, ASI-drift-watch, fake-governance-detection]
version: 1.0.1
---

# Agentic Trust Trajectory — behavior-over-time trust for agent federations

## When to Use

- User asks whether an agent is trustworthy **over time** (not per-request)
- Auditing the fleet for social-engineering patterns ("Jia Tan scan")
- Discussing or wiring trust decay / trust half-life / fatigue-gated authority grants
- Any probe of "who did what" attribution gaps in federation ledgers
- After incidents where a helpful long-tenured component suddenly requested elevated authority

**Origin:** Veritasium xz-utils backdoor video (aoag03mSuXQ), 2026-08-14. The xz attack was not
technical — it was a TRAJECTORY. No per-request gate can see it; only the longitudinal record can.

## The three orthogonal trust axes (do not merge them)

| Module | Axis | Status |
|---|---|---|
| `arifosmcp/runtime/art/trust_curve.py` | trust per **TOOL** (slope: success/failure/rollback) | exists — keep |
| `arifosmcp/runtime/request_trust.py` | trust per **CONNECTION** (loopback vs proxied) | exists — keep |
| `trust_trajectory.py` | trust per **ACTOR over TIME** | this skill |

## The XZ signature (formalized)

```
Phase 1 QUIET     — presence established, low activity (aging in place)
Phase 2 ACCRETION — sustained helpfulness, observe-heavy, zero violations (LOOKS GOOD)
Phase 3 GRAB      — authority-seeking request shortly after accretion peak,
                    often coinciding with maintainer/sovereign fatigue
```

No single phase is individually suspicious. The **sequence** is the attack. Semantic gates
score each phase as benign; only the trajectory betrays it.

## The tool

`/root/forge_work/2026-08-14-xz-defense/trust_trajectory.py` — Python stdlib ONLY (every
dependency is xz-surface), READ-ONLY (reads ledgers, never writes production state):

```bash
python3 trust_trajectory.py                    # full report (all actors)
python3 trust_trajectory.py --actor hermes     # single actor trajectory
python3 trust_trajectory.py --xz-scan          # XZ signature scan only
python3 trust_trajectory.py --sovereign        # sovereign load (fatigue proxy)
```

Data sources (probed 2026-08-14, do not invent alternates):
- `/root/AAA/ledger/constitutional_guard.jsonl` — 38,800 rows: agent:start/step/end, user_id, session_id, tool_names, observe/mutation classification
- `/root/AAA/data/hold_queue.jsonl` — intent, action_class, proposed_by, violated_floors
- `/root/forge_work/session-receipts.jsonl` — actor, outcome, commits

## Falsifiable detector calibration (the method — reuse for ANY detector)

Calibrate every detector against **externally documented truth** before trusting it.
For sovereign_load(): Arif's marathon pattern (4am/5pm wakes, 14-16h days) is independently
documented. The detector rediscovered it from raw ledgers alone — 11/12 days marathon,
8 predawn wakes, band HIGH — so the gauge is honest. **If a detector fails to rediscover
known truth, the detector is wrong, not the data.** This is the difference between a gauge
and a claim.

## Standing findings (2026-08-14)

1. **Identity-blind logging gap.** The guard ledger records WHAT happened but not WHICH
   agent did it (actor fields absent from agent:step rows). XZ-scan returns empty not
   because the fleet is clean but because trajectories cannot be attributed. Patching
   actor attribution into the ledger is the prerequisite for real coverage. Pending F13.
2. **Trust never decays.** Reputation ratchets up only; no trust half-life exists yet.
   Long-tenured components get implicit passes. Re-verification must be periodic, not
   incident-triggered. (Banda Haram domain #5 already mandates decay params — enforcement
   still missing.)
3. **arif_judge :8088 was drift-flagged** (deployment_attestation.drift) at build time —
   the detector therefore READS receipts instead of calling the judge. Keep that
   separation: a trajectory gauge must not depend on the judgment organ's health.

## The four eurekas (doctrine, falsifiable)

1. **Trust has no half-life yet** — tenure ≠ verification.
2. **Physics catches what semantics miss** — the 500ms login delay caught what every
   scanner passed. For agents: alarm on telemetry DELTA (token burn, latency, entropy
   drift), not semantic intent-reading. Also the honest fix for the W_SCAR semantic-regex
   false-positive flaw.
3. **Attack arrives as relief** — help offered during maintainer fatigue is an attack
   signature, not affection. Temporal rule: verify new helpers twice when sovereign load
   is HIGH. (Lasse Collin handed keys at his most tired.)
4. **Firefighter-arson pattern** — the attacker planted the bug, waited for discovery,
   fixed it heroically; the victim forwarded the bug TO the attacker and felt smart about
   it. In ledgers: fix-follows-own-failure is a FLAG, not a virtue. Trust from "repair"
   outranks trust from "stability" in human minds — and that bias is exploitable.

## Phase 2 (specced, NOT wired — proposal → apex-judge → F13 ratify)

1. Script-bytes hash registry → unknown-hash-at-exec = HOLD (extension of existing floors,
   not a new floor)
2. Fatigue-gated authority grants: sovereign_load HIGH + authority request = extra HOLD
   (**MARUAH** as mechanism, protecting the weakest stakeholder — the tired maintainer)
3. WELL biometric coupling when M-WELL ships (only WELL-STAGING-RECEIPT.md exists today)

## Pitfalls

- **stdlib-only constraint is doctrine, not style** — each pip install in a trust auditor
  is the next xz. json + hashlib + datetime + statistics suffice.
- **Read-only doctrine** — the scanner must never mutate the state it audits (AMANAH:
  the tool itself must be reversible/no-op on production).
- Do not wire detection into enforcement in the same PR as the detector — OBSERVE first,
  calibrate, then propose gates separately.

## Support files

- `scripts/xz_probe.py` — quick read-only probe (sovereign load band + attribution-gap
  census). Run instead of re-typing analysis.
- `references/session-2026-08-14-provenance.md` — origin session, verbatim transcript
  evidence with timestamps, falsifiability record, build artifacts.
