# PURPOSE STARVATION PROBE — Operational Specification

> **Status:** [CANDIDATE — Lane B DRAFT] · 2026-09-08
> **Source:** Void-mapping research session SEAL-compile-2026-09-08
> **Predecessor:** `PURPOSE-METABOLISM-DOCTRINE.md` §3.1
> **Axiom:** F2 TRUTH · F7 HUMILITY · F9 ANTI-HANTU · F11 AUDIT · F13 SOVEREIGN (F13-gated — touches sovereign meaning)
> **Lane:** B (DRAFT pending 888-APEX verdict → Lane A CANONICAL)

---

## §0. Mission

Detect Purpose Fetishism and Purpose Substitution before they kill the federation.

The probe **does not propose a new purpose**. It surfaces that the sovereign's purpose is starving — nothing more. Recovery is F13's job.

---

## §1. The Probe (operational form)

### §1.1 Inputs

```
P_now       = current sovereign purpose (from F13 receipt stream)
P_history   = purpose-renewal receipts (last 365 days)
C_ledger    = consequence ledger (which invoices were paid against which purpose)
A_audit     = federation action history (last 365 days)
```

### §1.2 The Three Signals

**Signal S1 — Purpose Renewal Gap**
```
days_since_last_F13_purpose_acknowledgment
  ≤ 30    → RENEWAL_RECENT (healthy)
  31-90   → RENEWAL_DUE (warning to F13)
  91-180  → STARVATION_LIKELY (HOLD on purpose-tagged SEAL)
  > 180   → STARVATION_CRITICAL (HARD HOLD on purpose-tagged SEAL; escalate F13)
```

**Signal S2 — Consequence Coherence**
```
For each purpose-tagged artifact in VAULT999:
  compute: is the artifact still serving the consequence
           that P_now was given for?
  output:  fraction_coherent (0.0–1.0)
  
  > 0.70  → COHERENT
  0.40-0.70 → DRIFT (warning)
  < 0.40  → FETISHISM_LIKELY (preserve as artifact, demote from living)
```

**Signal S3 — Purpose Substitution Smell**
```
For each purpose-tagged artifact sealed in last 90 days:
  verify: does its W(a) computation cite an F13 input?
  if not → SUBSTITUTION_CANDIDATE (HOLD; require F13 ack before SEAL)
```

### §1.3 Output Format

```json
{
  "probe_id": "psp_<utc>",
  "session_id": "<arifOS session>",
  "actor_id": "well-purpose-probe",
  "s1_renewal_gap": "RENEWAL_DUE",
  "s2_coherence": {"coherent": 0.61, "drift": 0.27, "fetishism_likely": 0.12},
  "s3_substitution": {"checked": 142, "candidates": 3},
  "verdict": "DRIFT_WARNING",
  "f13_action_required": true,
  "ax9_compliance": "no purpose proposed; signal only",
  "seal_receipt": "<F11 hash>"
}
```

**The verdict is signal, not judgment.** F13 decides what to do.

---

## §2. Cadence and Escalation

| Cadence | When | Action |
|---|---|---|
| Daily | 04:00 UTC cron | Compute S1, S2, S3; emit receipt |
| Weekly | Sunday 04:00 UTC | Aggregate weekly signals; flag trends |
| On-renewal | F13 emits purpose-acknowledgment | Reset S1 baseline; re-rank S2 |
| On-trigger | Any S2 or S3 crosses threshold | Surface to F13 within NOW lane (attention-graph §6) |

**Escalation chain:**
```
SIGNAL → arifOS (888-APEX review) → F13 (now lane if S1 critical or S3 substitution)
```

The probe NEVER escalates itself. It emits signal; arifOS routes; F13 acts.

---

## §3. HARAM List

The probe **MUST NOT**:

- Propose a new purpose (F13 only)
- Manufacture purpose from observation (F9)
- Infer purpose from behavior (F13 = meaning allocator)
- Seal or unseal VAULT999 items autonomously
- Suppress starvation signals (witness-first, void guard)
- Use agent-internal confidence as a metric (F9 + F2)
- Modify F1-F13 floors

The probe **MUST**:

- Cite F13 as sole purpose-source (axiom)
- Cap confidence at 0.90 (F7)
- Emit receipt per computation (F11)
- Allow F13 to silence or override (Lane A)

---

## §4. Falsification Tests

| Test | Discriminates | Pass condition |
|---|---|---|
| **False-positive stress** | Inject 100 fake purpose-renewal receipts; measure S1 | S1 correctly identifies 0 as fake |
| **Drift detection** | Inject 50 artifacts with deliberately incoherent consequences; measure S2 | S2 marks ≥ 80% as FETISHISM_LIKELY |
| **Substitution smell** | Inject 20 artifacts with no F13 input; measure S3 | All 20 flagged as SUBSTITUTION_CANDIDATE |
| **Silence attack** | Federation suppresses S1 for 30 days | Hard HOLD on purpose-tagged SEAL triggered automatically |
| **F13 override** | F13 explicitly silences probe | Probe remains dormant until F13 re-enables |

---

## §5. Constitutional Mapping

| Floor | Application |
|---|---|
| **F1 AMANAH** | Probe is read-only on VAULT999; never mutates |
| **F2 TRUTH** | All signals carry epistemic label OBS/DER/INT/SPEC |
| **F3 WITNESS** | Probe output is itself a witness event (recorded in VAULT999) |
| **F4 CLARITY** | Probe output reduces entropy (ΔS ≤ 0); no noise amplification |
| **F6 MARUAH** | Probe never names individual purpose-holders; only signals |
| **F7 HUMILITY** | Confidence cap 0.90; signal-vs-verdict distinction enforced |
| **F9 ANTI-HANTU** | Probe never infers purpose; only observes |
| **F11 AUDIT** | Every probe run emits receipt |
| **F13 SOVEREIGN** | Probe is F13-gated; F13 may silence, override, or expand |

---

## §6. F2 Audit Summary

| Component | Class | Falsifiable? | Survives? |
|---|---|---|---|
| S1 Renewal Gap | OBS | yes (F13 receipt timestamp) | yes |
| S2 Coherence | DER | yes (consequence ledger audit) | partial — needs ledger integrity |
| S3 Substitution Smell | OBS | yes (W(a) citation audit) | yes |
| Verdict as signal not judgment | SPEC | yes (output schema) | yes |

---

## §7. Ratification Path

```
Step 1 [DONE 2026-09-08]   : File as DRAFT (Lane B) — this artifact
Step 2 [T1, queued]        : contradiction_scan via geox_claim(mode=scan)
Step 3 [T2, 888-APEX]      : lane determination
Step 4 [T3, F13]           : if CANONICAL → VAULT999 append (constitutional probe)
```

---

## §8. Provenance

**Session:** SEAL-compile-2026-09-08 · 2026-09-08
**Actor:** 333-AGI Δ MIND — proposer
**Trigger:** Purpose Metabolism doctrine §3.1 named the probe; this is its operational specification
**Axiom-9 boundary:** explicit — probe proposes nothing, surfaces only

---

*DITEMPA BUKAN DIBERI ⚒️*
