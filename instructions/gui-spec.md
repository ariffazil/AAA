# GUI_SPEC — Trust Surface Contracts

**Type:** Implementation spec (NOT a canon capsule)
**Scope:** Observatory dashboard + MCP Apps glass layer
**Thesis:** GUI is a **trust surface**, not an action surface. Its only job is to prevent silent divergence between the glass and the ground.
**Status:** v1.0 — apply to code, not to canon.
**Forged:** 2026-08-19

---

## 0. The Inversion

```
Before:  GUI = where the human ACTS
After:   GUI = where the human STAYS ORIENTED while agents act
```

Everything below is an existing constitutional floor applied to glass.

---

## 1. The Four Roles → UI Contracts

| Role | Duty | Floor | UI Contract |
|------|------|-------|-------------|
| **Author** | of intent | F4 CLARITY | **Intent Mirror**: parsed intent shown and confirmed before any T2+ action |
| **Verifier** | of outcome | F2 TRUTH | **Ground Truth**: badges reflect live polled state, never requested/cached |
| **Sovereign** | of veto | F13 SOVEREIGN | **Consent Gate**: T3 actions render HOLD, never auto-execute |
| **Auditor** | of trail | F11 AUDIT | **Provenance**: every value one click from its VAULT999 receipt |

---

## 2. Contract Details

### 2.1 Intent Mirror — Author
- Source: render `arif_think` output directly. Do not paraphrase.
- Gate: T0/T1 may skip. T2+ MUST show mirror.
- Fail mode blocked: **Intent ≠ Interpretation**.

### 2.2 Ground Truth — Verifier
- Poll cadence: ≤30s. Timestamp every badge.
- Stale > 60s → amber ring + "checked Xm ago".
- **Kernel tile is tile #1.** If kernel :8088 DEGRADED → whole board banner: `⚠ SPINE DEGRADED — states below may be unreliable`.
- Fail mode blocked: **Displayed ≠ Actual**.

> A green board on a degraded kernel is a painted wall, not a door.

### 2.3 Consent Gate — Sovereign
- T0–T2: may auto-execute, logged.
- T3: hard pause. Approval requires explicit confirm token.
- Maps to 888_HOLD gate.
- Fail mode blocked: irreversible action indistinguishable from trivial.

### 2.4 Provenance — Auditor
- Every rendered claim carries a receipt link.
- No lineage → render as UNKNOWN, never as fact.
- Fail mode blocked: conclusion with no ancestry.

---

## 3. Uncertainty Tag — Global Rule (F2 + F7)

Every data point carries an epistemic tag. No exceptions.

```
OBS  observed / logged        (highest trust)
DER  derived / computed
INT  interpreted / modeled
SPEC speculative              (lowest trust)
UNK  unknown / no lineage
```

Ω₀ cap applies: SPEC claims may not drive T3 actions.

---

## 4. Three Failure Modes

```
1. Intent    ≠ Interpretation  → blocked by Intent Mirror  (§2.1)
2. Displayed ≠ Actual          → blocked by Ground Truth    (§2.2)
3. Confidence≠ Reality         → blocked by Uncertainty Tag (§3)
```

All three are the same crime: the human's model and reality drifted apart, silently.

---

## 5. Apply-To Checklist (per surface)

- [ ] Kernel health is tile #1; degraded spine → board-wide amber banner
- [ ] Every badge timestamped; stale > 60s visibly flagged
- [ ] T3 actions render HOLD, never auto-fire
- [ ] T2+ actions show Intent Mirror before execute
- [ ] Every data point carries OBS/DER/INT/SPEC/UNK tag
- [ ] Every claim links to a VAULT999 receipt
- [ ] Only HOLDs and failures are loud; noise is silent
- [ ] Badge = live poll = reality (no third surface)

---

## 6. What This Spec Is NOT

- Not a new floor. All floors pre-exist (F1,F2,F4,F7,F11,F13).
- Not a capsule for the canon.
- It is a wiring diagram: existing law → concrete glass contracts.

---

*DITEMPA BUKAN DIBERI. The screen must never let Arif believe something that isn't true.*
