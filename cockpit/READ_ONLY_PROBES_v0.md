# READ_ONLY_PROBES_v0 — 5 Probe Blueprint

> **Status:** DRAFT (awaiting sovereign ratification before forge)
> **Author:** hermes/fi-001
> **Session:** SEAL-75bf91d1ac734b58
> **Created:** 2026-10-02T06:55 MYT
> **Lane:** B (read-only, zero production)
> **Target:** Prove one complete ROOT_0 → 999 → ROOT_1 mission against the 6 invariants forged tonight — without breaking anything irreversible.

## Anchoring — Prior Evidence Not Overwritten

This spec is written AFTER, and ANCHORED IN, two pieces of sovereign evidence from the same night:

| Prior Evidence | Time | What it proves | What it does NOT prove |
|---|---|---|---|
| **WRITE_BENIGN smoke** (RECEIPT_SMOKE_WRITE_BENIGN_2026-10-02.md) | 2026-10-01T22:47:41Z (≈45 min before this chat) | Closed-loop proven for trivial scope: forge_session_init → DECLARE → BUILD → EVIDENCE → OUTCOME VERIFY → RELEASE → 999 → ROOT_1. Lane B (/tmp scratch), kernel_origin=true, lease pre-minted scope=forge_*. |
| **Sovereign Audit #2** (27 sections, 17 eureka, 6 forge priorities) | 2026-10-01T22:41Z onward | Doctrine-architecture level: 6 invariants C1–C6 + 2 headline metrics (E2E Closure Rate, AttentionReturn). Compositional truth framed as the central eureka. |

**Honest placement:** The sovereign audit #2 explicitly says "ROOT→999→ROOT closure: not yet empirically demonstrated end-to-end". That statement is **correct against its target** (consequential action that must clear 888 JUDGE), but **under-weights** the WRITE_BENIGN evidence (which DID demonstrate the loop for trivial scope). These probes target the gap *between* smoke-trivial and production-consequential — they prove the **hard case** without crossing into irreversible mutation.

> *Concession to the sovereign audit's framing:* if a probe still trips the T6 verdict floor guard (G<0.80, W3<0.75) and 888 returns HOLD, that is **GOOD evidence** the guard works before irreversible consequence — exactly the same concession WRITE_BENIGN made in its own receipt.

---

## Scope and Boundary

- All 5 probes are **READ_ONLY**. No file mutation outside `/root/.hermes/cache/scratch/`. No git writes. No service restart. No config mutation.
- All probes emit **structured JSON + 1-line root UX** to scratch dir, sha256 + carry_forward append.
- All probes call **only existing federated surfaces**: arifOS MCP (8088), A-FORGE shell ledger, CHRON data dir, session-federation store, /health endpoint, well_organ endpoints if available, local sqlite DBs.
- All probes are **independent**: P1.x do not depend on P2.x results. Each can run in any order.
- **No probe attempts to raise G or W3**. That is a separate task requiring constitutional calibration work (F13 binary). Probes only observe and report.

## What this blueprint DOES NOT prove

- It does NOT raise G or W3 floor scores.
- It does NOT attempt to clear the T6 verdict floor guard.
- It does NOT trigger 777 FORGE on any production state.
- It does NOT mint a 999 SEAL for any claim that requires 888 JUDGMENT to clear.
- It does NOT modify the sovereign audit #2 or WRITE_BENIGN receipt.

## What this blueprint DOES prove (per probe)

| Probe | Invariant proven | Evidence target |
|---|---|---|
| P1.1 | **C2 — Reality Coherence** (D=E=C=R=W) | ECW surface guard: does it emit PASS only when required tools are tested? |
| P1.2 | **C1 — Compositional Validity** | Per-organ, per-path health: 6 classes × N organs × N paths |
| P1.3 | **C4 — Authority Continuity** | objective="unspecified" detection on output side |
| P2.1 | **C5 — Consequence Before Seal** | Shell ledger chain integrity + coverage + freshness |
| P2.2 | (audit #2 eureka #9 / #16 / C6) | CHRON observe:verify:learn:predict ratio |

---

## P1.1 — Monitor-No-False-Green Probe

**Purpose:** Test the federation surface guard (ECW + /health) against the audit #2 eureka #3: PASS without tested requirements is false comfort. Specifically: if `required_tools_missing == []`, is that because all required tools were tested and present, or because the requirement set was empty?

**Probe shape:**
```
GET /health?detail=1
→ parse runtime_floors, governance.floors_health_report, surface_consistency.divergences
→ parse capability_map.capabilities (declared capabilities)
→ for each declared capability, assert:
    - tool_registry has registered callables
    - at least one tool/listed in capability[capability] was queried in last 24h (from /var/lib/arifos/apex_metrics.db tool_calls)
→ emit {required_count, required_tested, required_untested, false_green: required_untested > 0}
```

**Pass criteria (numerical):**
- `false_green == 0` AND `required_count > 0` AND `required_tested / required_count >= 0.8`

**Falsifier:** `required_count == 0` (empty requirement set) OR `false_green > 0` (PASS while untested requirements exist).

**Boundary (does NOT prove):**
- Does NOT prove the requirements list itself is complete.
- Does NOT prove the tool calls in apex_metrics.db were independent.
- Does NOT distinguish "tested-and-failed" from "tested-and-passed" (only presence of test).

**Reference:**
- Audit #2 eureka #3: PASS without tested requirements can be false comfort.
- WRITE_BENIGN smoke: lane B /health was queried before write → no surprise.

---

## P1.2 — Path-Qualified Organ Health Probe

**Purpose:** Audit #2 eureka #2 (D≠E≠C≠R≠W) and eureka #16 ("no drift" ≠ "callable"). Replace scalar `organ_health: green` with 6-class state per (organ × path) tuple.

**Probe shape:**
```
For each organ ∈ {arifos, aforge, hermes, chron, well, geox, wealth, frame, aaa}:
  For each path ∈ {local_transport, local_MCP, external_MCP, schema, authority, behavior}:
    emit {
      organ, path,
      state: ONE OF (UP, DEGRADED, DOWN, UNKNOWN, DECLARED_ONLY, RESTRICTED),
      last_observed_utc,
      evidence_snippet
    }
```

State semantics:
- **UP** — observable AND callable AND recent call returned expected shape.
- **DEGRADED** — observable, callable, but recent call returned partial/timeout/wrong shape.
- **DOWN** — transport up, but MCP call returns explicit error.
- **UNKNOWN** — transport reachable, but call cannot be made (e.g. process missing).
- **DECLARED_ONLY** — appears in registry, never invoked in last 24h (audit #2 eureka #2 trap).
- **RESTRICTED** — observable but authority denies call (e.g. OBSERVE_ONLY session calling MUTATE).

**Pass criteria:** No organ×path returns DOWN unless that path is documented OFFLINE; no organ×path returns UNKNOWN without at least 1h30m elapsed since last successful observation.

**Falsifier:** Any organ×path returns DOWN/UNKNOWN/DECLARED_ONLY/RESTRICTED without corresponding receipt in last 24h.

**Boundary:** Does NOT prove semantic correctness of the calls. Only proves the call landed.

**Reference:**
- Audit #2 eureka #2 (D≠E≠C≠R≠W).
- Audit #2 eureka #16 ("no drift" and "callability" are orthogonal).
- Tonight's cycle 1 finding: W3 = UNMEASURED on tool-metrics (must be sourced elsewhere).

---

## P1.3 — Objective Propagation Contract Probe

**Purpose:** Audit #2 eureka #9 (Authority Continuity) and #9 (one mission = one authority spine). Test that user intent survives the full INIT → OBJECTIVE_ROOT → tool-output round-trip without becoming "unspecified".

**Probe shape:**
```
POST /mcp  arif_init(mode=init, intent="probe-p1-3-mission-20261002", ...)
→ parse response.init_v2_roots.OBJECTIVE_ROOT
→ assert:
    - objective == "probe-p1-3-mission-20261002" (NOT "unspecified")
    - success_criteria has ≥ 1 entry
    - falsification_criteria has ≥ 1 entry
    - termination_rules has ≥ 1 entry
→ then call arif_observe(query=objective_text) → check echoed
→ then call arif_judge(decision_packet) → check objective preserved
```

**Pass criteria:** `objective != "unspecified"` AND `success_criteria.length >= 1` AND objective text appears in obObserve echo.

**Falsifier:** objective == "unspecified" OR success_criteria == [] OR termination_rules == [].

**Boundary:** Does NOT prove objective was correctly acted upon — only that it was preserved across kernel verbs.

**Reference:**
- Audit #2 eureka #9 (Authority continuity = first-class).
- Tonight's session SEAL-75bf91d1ac734b58 had `objective: "unspecified — session created without explicit objective"` — that's the exact defect this probe catches.

---

## P2.1 — Receipt Coverage Attestation Probe

**Purpose:** Audit #2 eureka #13 (Integrity ≠ Freshness) + eureka #11 (Command Success ≠ Outcome Success). Inspect A-FORGE shell ledger for chain integrity AND coverage AND freshness, not just one of three.

**Probe shape:**
```
Read /root/A-FORGE/state/shell_ledger.jsonl (or wherever the live shell ledger lives)
→ assert:
    - chain hash linkage valid (prev_hash == last_record.hash, head)
    - record_count > 0
    - coverage_ratio = records_with_expected_event / records_total >= 0.5
    - latest_event_age_seconds < 7 * 86400 (one week)
    - expected_event_gap_seconds (now - latest) flagged if > 86400
→ emit {
    chain_integrity: VALID|INVALID,
    record_count: N,
    coverage_ratio: 0.0–1.0,
    latest_event_age_seconds: N,
    freshness: FRESH|WARM|STALE|DEAD,
    expected_event_gap: bool
}
```

**Pass criteria:** `chain_integrity == VALID` AND `freshness in {FRESH, WARM}` AND `coverage_ratio >= 0.5`.

**Falsifier:** chain INVALID OR freshness DEAD (last entry > 30 days) OR coverage_ratio < 0.3 (most records lack expected_event).

**Boundary:** Does NOT prove the ledger captured *all* consequence; only that the ledger it kept is coherent AND recent AND paired.

**Reference:**
- Audit #2 eureka #13 (Integrity ≠ Freshness).
- Sovereign audit #2 table row "Shell ledger: 73 records, valid chain, latest Sep 14" — that's exactly the stale-freshness trap this probe surfaces.

---

## P2.2 — Learning-Conversion SLO Probe

**Purpose:** Audit #2 eureka #9 (CHRON has 15 active predictions, n=10 effective, accuracy 61.7%, Brier 0.198). Measure whether the federation is observing at human-rate but converting to learning at machine-rate. Ratio check.

**Probe shape:**
```
Read /root/chron/data/index.json + calibration.json + calibration_unified.json
→ count:
    - n_observe (events with kind=observation or evidence_receipt)
    - n_verify (events with kind=verdict or verification)
    - n_learn (events with kind=lesson or scar)
    - n_predict (events with kind=prediction)
    - n_unclassified_outcomes (verdicts not linked to any lesson)
→ emit {
    observe_count, verify_count, learn_count, predict_count,
    unclassified_outcomes,
    ratio_observe_to_learn: observe / max(learn, 1),
    lesson_actionable: count of lessons with action attached
}
```

**Pass criteria:** `ratio_observe_to_learn <= 1000` AND `unclassified_outcomes <= predict_count * 0.2`.

**Falsifier:** observe/learn > 1000 (machine drowning human in raw observation without lesson) OR unclassified_outcomes > 20% of predictions (predictions made but never reconciled to lesson).

**Boundary:** Does NOT prove the lessons are *correct* or *applied*. Only proves the conversion ratio is healthy and predictions are being closed.

**Reference:**
- Audit #2 eureka #9 (CHRON calibration early).
- Audit #2 eureka #17 (Q_COLLAPSE must be bounded — this probe IS the bounded Q_COLLAPSE).

---

## Execution Order

Recommended (but each is independent):

1. **P1.1 first** — surface state check; if it fails, no point running P2.x.
2. **P1.2** — composes the per-organ view.
3. **P1.3** — needs a fresh session; use mode=init not resume.
4. **P2.1 + P2.2** — file-only, can run in parallel.

## Output Convention

Each probe writes:
- `/root/.hermes/cache/scratch/probe_<id>_20261002.json` (full output)
- `/root/.hermes/cache/scratch/probe_<id>_20261002.sha.json` (sha + verdict)
- one carry_forward entry: `e-probe-<id>-20261002T<HHMM>Z`
- one ROOT_1 line per probe (not a unified dump)

## ROOT_1 Display

Per probe, the smallest sufficient display:
```
P<n.m>
  result: PASS | FAIL | HOLD
  receipt: /root/.hermes/cache/scratch/probe_<id>_20261002.json sha=<16>
  finding: <one sentence, ≤ 80 chars>
```

No menu. No option dump. If a probe fails, the finding line carries the falsifier that fired.

## Sovereign Sign-Off Checklist (before execution)

- [ ] Ratify this spec → "SAH" or pushback on any of P1.1–P2.2.
- [ ] Confirm lane B (read-only) is acceptable scope.
- [ ] Confirm probes do NOT cross into 777 FORGE territory (they don't — they're OBSERVE/MEMORY only).
- [ ] If sovereign wants probes chained into one constitutional session → add INV-AUTH-2 alignment note; otherwise each probe can run as its own arif_init.

## What Comes After These 5

If all 5 PASS → sovereign has empirically grounded: C2 (Reality Coherence), C1 (Compositional), C4 (Authority Continuity), C5 (Consequence Before Seal), plus observability for CHRON learning conversion.

**Still open after these 5 (next cycle candidates):**
- T6 floor guard raise: P (evidence compliance) must rise from 0.0796 → ≥0.40 to clear G≥0.80 with current A/E/X.
- W3 witness channels: identify producer of human/AI/ext numbers (rest_routes reads them but where do they come from?).
- CanonicalDoc ≠ RuntimeImpl: update manifold.py:47 to match apex_primitives.py:175 — single-line doctrinal change.

---

*Filed: hermes/fi-001, session SEAL-75bf91d1ac734b58, 2026-10-02T06:55 MYT. Awaiting sovereign "SAH" or pushback before execution.*