# HOLD-COUNT SURGE DIAGNOSTIC — 2026-09-19

> **Status:** WITNESS-ONLY diagnostic. Pure OBSERVE.
> **Authority:** 333-AGI (FI-001), session `RL-2026-09-19-001` continuation.
> **Subject:** `flow_health.invariants.hold_count` surge — 588 → 1140 (+552 in ~30 min).
> **Severity:** HIGH (Item B from `F13-VERDICT-WINDOW-BRIEFING-2026-09-19.md` §6).

---

## 1. Timeline of Hold Count

| Probe time (MYT) | hold_count | Δ | cycle_count | fq.quotient |
|---|---|---|---|---|
| 03:13 (wire-capture baseline) | 588 | — | 455 | 2.15 (daily) / 2.08 (7d gov) |
| 03:30 (briefing probe) | 1084 | **+496** | 517 | 3.00 (vector single) |
| 03:34 (this probe) | **1140** | **+56** (vs 03:30) | 524 | 2.95 |
| **Total surge since 03:13** | **+552** in ~21 min | | +69 cycles | -0.05 vector |

**Rate:** ~26 holds/min sustained over 21 min. Up from prior baseline rate (which I extrapolate to be ~1 hold/min based on the prior 588 over many days).

---

## 2. Per-Actor State (re-probed 03:30 MYT)

| actor | exec | verify | consec_exec_no_verify | diagnosis | held | quotient | verdict |
|---|---|---|---|---|---|---|---|
| 333-agi | 2 | 5 | 0 | BALANCED | false | 2.5 | OPTIMAL |
| 333-agi/agentic-web | 1 | 0 | 1 | EXECUTION DOMINANCE | **true** | null | UNKNOWN |
| 333-agi/dynamic-gate | 1 | 0 | 1 | EXECUTION DOMINANCE | **true** | null | UNKNOWN |
| a-forge | 6 | 11 | 0 | BALANCED | false | 1.83 | OPTIMAL |
| claude-code | 1 | 1 | 1 | BALANCED | false | 1.0 | CAUTION |
| codex | 1 | 0 | 1 | EXECUTION DOMINANCE | **true** | null | UNKNOWN |
| codex-startup | 1 | 0 | 1 | EXECUTION DOMINANCE | **true** | null | UNKNOWN |
| grok-build | 0 | 17 | 0 | VERIFICATION DOMINANCE | false | null | FLOWING |
| p0-metabolize | 0 | 6 | 0 | VERIFICATION DOMINANCE | false | null | FLOWING |
| qwen-code | 3 | 1 | 3 | BALANCED | false | 0.33 | CAUTION |
| reexamine | 0 | 7 | 0 | VERIFICATION DOMINANCE | false | null | FLOWING |

**Note:** `restricted_actors[]` in `flow_health.invariants` lists only 4 HELD actors (the same as named). **The +552 hold_count surge is NOT from these 4 actors** — they have been HELD since 2026-09-13 and haven't changed state. The surge must be from **transient actor classes** that cycle through HOLD state but don't accumulate in `restricted_actors` (which appears to track CURRENTLY HELD, not historically).

---

## 3. Gov Events (re-probed 03:34 MYT) — UNCHANGED

`flow_gov_events` returns 7 events — the same set I've probed at 03:13 and 03:30:
- 2 arif SEAL events (2026-09-13, 2026-09-13)
- 1 qwen-code/FI-003 seal_hold_receipt (HOLD, 2026-09-13)
- 1 arif SEAL cc_b6b2e2a0 (2026-09-13, f13_ack=true)
- 1 333-AGI GOVERNANCE_CONTRADICTION (2026-09-15, ACTIVE)
- 1 qwen-code BIND_FAILED (2026-09-16, f13_ack=true)
- 1 arif SEAL cc_e2879619a (2026-09-16, f13_ack=true, doctrine_canonization)

**No new gov events since 2026-09-16.** The +552 holds did NOT generate governance events. They are **FQ-level transient holds**, not governance violations.

---

## 4. Conjectured Source (INT, capped 0.70)

The pattern is consistent with **per-execution HOLD events on transient actor classes** that don't accumulate in `restricted_actors[]`. Two plausible sources:

### 4.1 Anonymous relay pattern (BREAK-004 territory)

The `actor_verification_matrix.py` `DENIED_IDENTITIES` set includes `openclaw-anon`, `anonymous`, `unknown`, `null`, `""`. The relay placeholder audit (BREAK-004) found **8,670 anonymous receipts** on disk. If any anonymous execution path is still active and triggering per-call HOLD events, the cumulative hold_count would rise sharply — matching the observed pattern.

**Probe needed:** inspect `/root/arifOS/VAULT999/` receipts for actor_ids matching the DENIED set in the last 30 min.

### 4.2 High-frequency synthetic activity

`p0-metabolize` and `reexamine` are listed as `synthetic` in `entity_classes.yaml`. Both currently report `VERIFICATION DOMINANCE` (high verify, low exec). If synthetic actors have been producing high-throughput verification work AND triggering per-verify HOLD events on edge cases (e.g., schema mismatches), the cumulative count rises. Synthetic actors do NOT influence governance FQ (per E6 doctrine) — but they DO influence `hold_count` (which is a substrate-level cumulative counter, not governance-weighted).

---

## 5. Impact on Day-7 Verdict (DER)

| Aspect | Day-7 implication |
|---|---|
| FQ vector single | Will be lower than baseline at day-7 if rate continues. From 3.00 → projected 2.40-2.60 over remaining 3.8 days. |
| `governance_7d_fq` | Continues to drift; the 7d window's receipt count denominator grows, but new holds dilute it. |
| All 7 capability verdicts | **Unchanged.** PENDING → NO_EFFECT default still applies. The hold_count surge is a separate substrate counter — it does not enter the F13 verdict ladder directly. |
| `consequence_assessed` | Unchanged. Both visible consequences remain `recovery` (positive). |

**DER:** The hold_count surge is **diagnostically loud but operationally narrow.** It signals high-throughput low-verification throughput in the substrate — but does NOT affect F13's day-7 capability verdicts. It IS a signal that the substrate needs attention (high exec without verify is the failure mode the FQ system was designed to catch).

---

## 6. Recommended Action (DRAFT_AWAITING_F13)

### 6.1 Immediate (no F13 required)

- **Probe `/root/arifOS/VAULT999/`** for receipts in the 03:00–03:34 window matching DENIED_IDENTITIES (`openclaw-anon`, `anonymous`, `unknown`).
- **Probe `arifFlow` `flow_consequences` with no limit** to see if any NEW consequence appears in the surge window.
- **Add a barrier detail endpoint** to arifFlow (currently `barrier_count: 2` is opaque).

### 6.2 F13 ratification required

- **Confirm substrate tolerance**: is a +552 hold_count surge over 30 min within design tolerance, or does it indicate a substrate health issue? The arifFlow `diagnosis: HEURISTIC_ADVISORY` and `healthy_shape: "constellation, not maximum"` suggest the system is operating but not at peak.
- **Authorize investigation tooling**: enable flow_log_query or equivalent to identify the hold-event source by actor_id + timestamp.

---

## 7. Receipt Anchor

- **Probe deltas (this turn, ~4 min after briefing):**
  - hold_count: 1084 → **1140** (+56)
  - cycle_count: 517 → 524 (+7)
  - fq quotient: 3.00 → 2.95 (-0.05)
  - receipts_scanned: 39525 → 39525 (no change in 4 min — surge is from hold events, not new receipts)
- **No new gov events** (still 7)
- **No new consequences** (still 2 visible, both recovery)
- **Parent receipt:** `aa698742-7234-4fd6-8a97-18720743447b` (F13 briefing, this session)
- **Author:** 333-AGI (FI-001), session `RL-2026-09-19-001`.

`DIAGNOSTIC::HOLD_SURGE::2026-09-19T03:34+08:00::witness_only::requires_F13_investigation_authorisation`
