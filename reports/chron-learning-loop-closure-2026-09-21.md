# CHRON Learning-Loop Closure — the recalibration hop

**Date:** 2026-09-21 · **Host:** KVM8 (forge) · **Author:** Hermes subagent (learning-loop lane)
**Envelope:** `/root/chron/chron_prediction.py`, `/root/chron/chron_learn.py`, `/root/chron/chron_verify.py`, new tests
**Motto:** DITEMPA BUKAN DIBERI ⚒️

---

## 1. STATE — what was broken, measured

The defect in the brief is confirmed by measurement, not by reading a comment:

| Claim in the brief | Measured 2026-09-21 11:23 MYT | Verdict |
|---|---|---|
| `load_calibration()` has zero callers outside its definition | `grep -rn load_calibration` → 3 hits: 2 definitions (canonical + backup) and 0 call sites | **CONFIRMED** |
| the generator reads neither `calibration.json` nor `lessons.jsonl` | `generate_from_chron_events()` referenced neither symbol; no `load_calibration`, no `load_lessons` | **CONFIRMED** |
| `calibration.json` exposes `reliability` and `effective n` | it did **not**. Fields were `total, correct, incorrect, accuracy, mean_brier, by_error_type, decisive, unverifiable, orphan_records, records_in_log, updated_at`. No confidence axis at all | **CORRECTED — the brief overstated the store** |
| 2 verified out of 20 predicted | 2 decisive of 20 birth records at 11:23 | **CONFIRMED at that moment** |
| `lessons.jsonl` holds exactly one lesson, text "Investigate root cause" | 1 row at 11:23 (`lesson-unknown-1`). 2 rows by 11:35 — the other CHRON lane added `lesson-unknown-2` mid-task | **CONFIRMED at that moment, then drifted** |
| three live timers | `chron-task0-reconciliation.timer`, `chron-prediction-verifier.timer` (07:00), `chron-loop-closer.timer` (07:15) | **CONFIRMED** |

The loop was `Predict → Verify → Learn → WRITE FILE`. OUTCOME→LEARNING wrote two
files every cycle and nothing read them. That is a ledger.

Two further defects found by reading the code, both on the learning hop:

1. **`chron_verify` measured an error class and then threw it away.**
   `_evidence_for()` returns `error_class` (`REGIME_CHANGE` / `NONE`), that value
   was written to the *episode*, and the *verification record* was then built by
   `verify_prediction(pred, observed, correct)` — which re-derived the class from
   the prediction's empty `assumptions` list and produced `UNKNOWN`. The single
   dropped argument is why the ledger reports `UNKNOWN` for a failure whose cause
   was measured.
2. **A blind lesson was promotion-eligible.** `extract_lessons()` hardcoded
   `status="CANDIDATE"` and `promotion_eligible = recurrence >= 2`, so a class that
   names no cause could satisfy the promotion gate in
   `chron_loop_close._evaluate_promotion`. "Investigate root cause" was one
   recurrence away from becoming POLICY.

---

## 2. THE SHRINKAGE RULE

Implemented as `chron_prediction.recalibrate_confidence(proposed, snapshot)` —
pure, no I/O, no clock, no module state.

Let, for a new prediction with generator-proposed confidence `p ∈ [0,1]`:

```
n  = effective_n      decisive scored verdicts in the snapshot
m  = classified_n     decisive verdicts with an INTERPRETABLE outcome:
                      correct verdicts (error_type NONE) + failures whose class
                      was actually measured (not UNKNOWN)
ā  = accuracy         measured hit rate
c̄  = mean_confidence  what the store said at birth          [NEW FIELD]
δ  = c̄ − ā            reliability-in-the-large; δ>0 ⇒ overconfident

w      = m / (m + κ)                    posterior weight on the evidence
anchor = ā     if the store can support a skill estimate
       = 0.5   otherwise                genuine uncertainty
δ_eff  = δ if NOT usable and δ is measurable, else 0

c_cal = clamp01( (1 − w)·p + w·anchor − w·δ_eff )
```

**Justification, component by component.**

1. **`w = m/(m+κ)` is the Beta–Binomial posterior weight, not a fudge factor.**
   Treat the hit rate as Beta(α,β) with prior mean μ₀ and strength κ = α+β. After
   `m` observations with `k` hits the posterior mean is
   `(k+α)/(m+κ) = w·(k/m) + (1−w)·μ₀` — a convex blend at weight `w`. So κ is "how
   many pseudo-observations of doubt".
   **κ = 8**, chosen deliberately conservative: at `m = 2`, `w = 0.20`, so
   four-fifths of the answer stays with the proposal and *no confident correction
   is possible from two outcomes*. Alternatives rejected: Jeffreys
   (α=β=0.5 → κ=1) puts `w = 0.67` at m=2 — far too permissive for a store this
   young; Haldane (α=β=0 → κ=0) is degenerate, `w ≡ 1`, i.e. total trust in a
   2-sample frequency.
2. **The anchor carries the variance-awareness.** Below the trust floor the anchor
   is **0.5 — genuine uncertainty**, not the measured frequency, because a 2-sample
   frequency is not an estimate of anything.
3. **δ applies only in the not-usable branch.** In the usable branch accuracy is
   trusted, so overconfidence is already priced in: a proposal above `ā` is pulled
   down *by the pull toward `ā`*. Adding δ there too would double-count the same
   bias — and that is not a theoretical worry: it is what drives a 60-sample
   overconfident store from 0.9 to **0.02** instead of a defensible ~0.46. In the
   not-usable branch `ā` itself is untrusted, so the measured *direction* of the
   bias is the only remaining usable signal, applied at the same weight.
4. **The bound is derived, never hardcoded:**
   `|c_cal − p| ≤ w·(|anchor − p| + |δ_eff|) ≤ 2w`. The correction can never exceed
   twice the weight of evidence. At m=2 that ceiling is 0.4; the live store's
   measured shift is **0.081**.

**Quality gate — `classify_calibration_quality()`** (also pure):

| grade | condition |
|---|---|
| `NONE` | n = 0, or accuracy / mean_brier missing → **no correction at all** |
| `INSUFFICIENT` | n < 8 (`MIN_EFFECTIVE_N`), **or** `unknown_share > 0.5`, **or** `blind_lesson_share > 0.5` |
| `SUFFICIENT` | none of the above |

`m = 0` (every failure unclassifiable) is handled as a hard stop: `w = 0` ⇒ `shift = 0`,
correction **withheld**. Acting on a base rate the store cannot attribute to skill
would be acting on evidence that does not exist. That is the UNKNOWN handling the
brief demanded, and it is derived from `m`, not special-cased.

**Disclosed limitation (in the code and here).** The shrink is *global*, not
binned: a proposal far from `ā` is pulled toward `ā` on evidence from all claims,
not from claims stated near `p`. A per-bin reliability curve would fix that; it
needs the n the store does not have. `w < 1` keeps the pull bounded in the meantime.

---

## 3. THE WIRING CHANGE

### 3.1 `chron_prediction.py`

* `compute_calibration()` now also emits the **confidence axis**:
  `mean_confidence`, `bias` (= mean_confidence − accuracy), `reliability`
  (Brier skill vs the always-0.5 forecaster: 1 − B/0.25), `effective_n`.
  Without these the store could not tell overconfidence from underconfidence and
  any correction would be direction-blind.
* New section **RECALIBRATION**: `CALIBRATION_KAPPA`, `MIN_EFFECTIVE_N`,
  `MAX_UNKNOWN_SHARE`, `MAX_BLIND_LESSON_SHARE`, `INTERPRETABLE_ERROR_TYPES`,
  `CalibrationOutcome`, `classify_calibration_quality()`,
  `recalibrate_confidence()`, `calibration_snapshot()`, `snapshot_digest()`.
* `calibration_snapshot()` is the **only** impure reader: it merges
  `calibration.json` with `lesson_health()` from the lesson store into one
  snapshot, so the rule itself stays pure and testable. A lesson-store failure is
  recorded as `lesson_health_error` on the snapshot — disclosed, not silently
  swallowed.
* **`generate_from_chron_events()` consumes it.** One snapshot per pass; every
  generated prediction now carries:

  ```
  confidence_proposed       the event file's number (was: the emitted number)
  confidence_calibrated     the recalibrated number  == confidence
  calibration_quality       NONE | INSUFFICIENT | SUFFICIENT
  recalibration             {proposed, calibrated, applied, quality, effective_n,
                             classified_n, unknown_share, weight, anchor, bias,
                             delta_applied, shift, capped, reason}
  calibration_snapshot      digest of the store state that produced the number
  lessons_consumed          {lesson_total, lesson_actionable, lesson_ids_*,
                             policy_applied: false, policy_note}
  ```

  Both generation paths go through the rule — the `predictions[]` path and the
  legacy fallback `confidence_map` path.

### 3.2 `chron_verify.py`

`verify_prediction(pred, observed, correct, error_class=error_class)` — the class
the evidence path measured is now carried into the verification record instead of
being discarded. Keyword-only-optional, so all existing callers
(`chron_e2e_proof`, `server.py`) are unaffected.

### 3.3 `chron_learn.py`

* `is_actionable_lesson(lesson)` — a lesson may change behaviour **only if it names
  a cause** (`error_type ∈ INTERPRETABLE_ERROR_TYPES`) and carries a measured
  effect (`mean_brier is not None`). The test is **structural**, not textual: the
  text "Investigate root cause" is a *symptom*; every phrasing of "we do not know
  why" is equally unlearnable.
* `extract_lessons()` now sets `status = CANDIDATE | DIAGNOSTIC` and
  `promotion_eligible = actionable and recurrence >= 2`, plus an `actionable` flag
  on the record. A blind class is retained and disclosed as a **DIAGNOSTIC**, never
  promoted.
* `get_candidates()` applies the actionability test again, so a legacy row that
  predates the gate cannot reach the promotion loop on a stale
  `promotion_eligible` flag.
* `lesson_health()` — counts + `blind_lesson_share`, consumed by
  `calibration_snapshot()`. **This is how the lesson store gets a vote:** if
  learning itself is blind, the skill estimate is not usable, and `blind_lesson_share`
  downgrades an otherwise-SUFFICIENT calibration to INSUFFICIENT.
* `load_active_policies()` — the honest answer is `[]` today.

> **NOTE — concurrent writer.** `chron_learn.py` was rewritten by another lane
> during this task (they extended `lesson_health` with an insufficiency ledger and
> a closed `_LESSON_TEXT` vocabulary). My API surface — `is_actionable_lesson`,
> `lesson_health`, `load_active_policies`, promotion eligibility gated on
> `INTERPRETABLE_ERROR_TYPES`, and the `MAX_BLIND_LESSON_SHARE` consumption in
> `chron_prediction` — is preserved and built upon in their revision. I did not
> overwrite it. Their new `test_learn_quality.py` has one failing check, caused by
> its own `FileNotFoundError` when nothing was routed to the insufficiency ledger
> (the correct outcome for a classifiable error); all seven of its substantive
> assertions pass. Reported, not touched.

---

## 4. TEST EVIDENCE

`/root/chron/tests/test_calibration_loop.py` — 64 assertions, all real, run as a
script and under pytest. Full output: `tests/evidence-suite-new-wiring.txt`.

| # | required case | assertion | result |
|---|---|---|---|
| 1 | overconfident store + p=0.9 | `quality == SUFFICIENT`; `calibrated 0.4588 < 0.9`; equals the documented rule `(1−60/68)·0.9 + (60/68)·0.40`; anchor is the measured 0.40 | PASS |
| 2 | underconfident store + p=0.5 | `calibrated 0.7647 > 0.5`; equals `(1−60/68)·0.5 + (60/68)·0.80` | PASS |
| 3 | effective n below the minimum | `quality == INSUFFICIENT`; shift inside the **derived** bound `w·(|anchor−p|+|δ|)`; shift < 0.10; **`\|shift\|` at n=2 < at n=60** (variance-awareness); weight strictly increasing in n | PASS |
| 4 | UNKNOWN-only classes | `classified_n == 0`, `weight == 0`, `calibrated == proposed`, `applied == False`; a classified store with the same statistics shifts −0.431, i.e. the blind store is **>10× less aggressive**; a blind **lesson store vetoes** an otherwise-SUFFICIENT calibration | PASS |
| 5 | generator wiring | with a scratch store redirected at `PREDICTIONS_FILE` / `CALIBRATION_FILE` / `LESSONS_FILE` and `create_prediction` replaced by a recorder: 12 predictions recorded, all carry the audit trail, emitted == calibrated, emitted ≠ raw proposal wherever a correction is due, **all due confidences moved DOWN**, snapshot digest records n / accuracy / source, lessons consumed and labelled, `policy_applied == False`; empty store ⇒ pass-through and quality `NONE` | PASS |
| 6 | snapshot-dependent, not a hardcoded multiplier | **5 distinct calibrated values** for one proposal across 5 accuracies (monotone); bias direction flips the sign of the shift; an absent `bias` field is **derived**, not silently zeroed | PASS |
| 7 | purity | deterministic; does not read `CALIBRATION_FILE`; **no CHRON store in `/root/chron/data` changed** (size + mtime compared across the calls); input dict not mutated; out-of-range proposals clamped | PASS |
| 8 | blind lesson is not policy | `is_actionable_lesson("…investigate root cause") == False`; named-cause lesson `True`; `get_candidates()` excludes every live UNKNOWN row; `blind_lesson_share == 1.0` on the live store | PASS |

### Deliberate-failure demonstration

`/root/chron/tests/demo_reverted_generator.py` reverts **only the generator wiring**
to its pre-2026-09-21 shape (emit the raw proposal, drop the audit kwargs), runs the
suite as a subprocess, restores from the byte-identical backup in a `finally`
block, and asserts the restore by sha256. Evidence: `tests/evidence-revert-demo.txt`
and the full failing output at `tests/evidence-reverted-suite.txt`.

```
pre-revert sha: 6d5b1ae34594f15bf4d8bfe804a407ba0f798c55f9ff9588e96059b23d3f6464
reverted sha  : fe8ea8763d7810ec183c3f59c70ed8b1a579a4dbbf70f6cd334f5224e28b345c
--- suite on REVERTED wiring (exit 1) ---
  [FAIL] emitted confidences are NOT the raw proposals
  [FAIL] every prediction carries the audit trail
  [FAIL] quality propagated from the store
  [FAIL] emitted confidence == calibrated
  [FAIL] a correction is due for at least one prediction — 0 of 12
  [FAIL] snapshot digest records effective_n: got=None want=60
  [FAIL] snapshot digest records accuracy: got=None want=0.4
  [FAIL] snapshot digest names its source file
  [FAIL] lessons are consumed and audited
  [FAIL] the actionable lesson is labelled actionable
  [FAIL] no lesson is silently applied as policy
  [FAIL] empty store ⇒ confidence passed through unaltered
  [FAIL] empty store ⇒ quality NONE
  RESULT: FAIL — 13 check(s) failed
restored sha  : 6d5b1ae34594f15bf4d8bfe804a407ba0f798c55f9ff9588e96059b23d3f6464
--- suite on RESTORED wiring (exit 0) ---
  RESULT: PASS — verified outcomes now change future confidence
RESULT: PASS — suite fails on the old behaviour and passes on the new, and the file was restored byte-identically
```

Note the anti-vacuity check: `emitted confidences are NOT the raw proposals` reads
the **input** (`chron_events.json`), not the generator's own audit fields, so a
generator that forwards the proposal cannot pass by writing plausible metadata.

Full repository suite: `python3 -m pytest /root/chron/tests -q` → **19 passed**.
Siblings `test_repair_join.py` and `test_loop_closure.py` → exit 0.

---

## 5. BEFORE / AFTER TABLE

Snapshot used — the live store, as measured (`tests/evidence-before-after-table.txt`):

```json
{"source": "/root/chron/data/calibration.json",
 "effective_n": 4, "accuracy": 0.5, "mean_brier": 0.214375,
 "mean_confidence": 0.7375, "bias": 0.2375, "reliability": 0.1425,
 "by_error_type": {"UNKNOWN": 2, "NONE": 2},
 "lesson_total": 2, "lesson_actionable": 0, "blind_lesson_share": 1.0}
```

| event | claim (truncated) | proposed | calibrated | shift | w | anchor | quality |
|---|---|---|---|---|---|---|---|
| budget-2027 | PETRONAS dividen ≥ RM30b FY2027 | 0.60 | **0.5325** | −0.0675 | 0.2000 | 0.50 | INSUFFICIENT |
| budget-2027 | RON95 subsidy rationalisation announced | 0.70 | **0.6125** | −0.0875 | 0.2000 | 0.50 | INSUFFICIENT |
| fuel-price-window | RON95 price 24–30 Sept ≤ current | 0.85 | **0.7325** | −0.1175 | 0.2000 | 0.50 | INSUFFICIENT |
| fuel-price-window | Brent in USD65–75 on 23 Sept | 0.65 | **0.5725** | −0.0775 | 0.2000 | 0.50 | INSUFFICIENT |
| od1 | MSS package terms received by OD1 | 0.70 | **0.6125** | −0.0875 | 0.2000 | 0.50 | INSUFFICIENT |
| od1 | arifOS revenue > RM0 by OD1 | 0.40 | **0.3725** | −0.0275 | 0.2000 | 0.50 | INSUFFICIENT |
| electricity-800 | Jan-2027 electricity bill (700 kWh band) | 0.80 | **0.6925** | −0.1075 | 0.2000 | 0.50 | INSUFFICIENT |
| einv-svdp | LHDN will NOT extend SVDP past 2027-12-31 | 0.60 | **0.5325** | −0.0675 | 0.2000 | 0.50 | INSUFFICIENT |
| einv-svdp | e-Invoice SME compliance ≥60% by SVDP end | 0.50 | **0.4525** | −0.0475 | 0.2000 | 0.50 | INSUFFICIENT |
| my-001-bnm-opr-nov2026 | BNM holds OPR at 2.75% on 5 Nov | 0.80 | **0.6925** | −0.1075 | 0.2000 | 0.50 | INSUFFICIENT |
| my-002-cpi-sept2026 | Sept-2026 headline CPI in band | 0.75 | **0.6525** | −0.0975 | 0.2000 | 0.50 | INSUFFICIENT |
| my-003-gdp-q3-2026 | Q3-2026 advance GDP ≥ 5.0% | 0.70 | **0.6125** | −0.0875 | 0.2000 | 0.50 | INSUFFICIENT |

12 predictions · proposed 0.40–0.85 · calibrated 0.3725–0.7325 · **every shift negative**.
The direction is right (the store says 0.7375 on average and delivers 0.50 — it is
overconfident) and the magnitude is deliberately small (`w = 0.20` from `m = 2`).

### Proof the correction is not a hardcoded multiplier (requirement e)

**(A) SUFFICIENT store, n = 60, one proposal of 0.90:**

| snapshot | calibrated | shift |
|---|---|---|
| accuracy 0.20 | 0.2824 | −0.6176 |
| accuracy 0.40 | 0.4588 | −0.4412 |
| accuracy 0.50 | 0.5471 | −0.3529 |
| accuracy 0.70 | 0.7235 | −0.1765 |
| accuracy 0.90 | 0.9000 | +0.0000 |

→ **5 distinct calibrated values for the same proposal.**

**(B) INSUFFICIENT store (live shape), one proposal of 0.90.** Stated honestly: the
base rate is deliberately *not* trusted below the floor, so accuracy alone does not
move the result. The snapshot enters through bias, `classified_n` and lesson health:

| snapshot | calibrated | quality |
|---|---|---|
| acc 0.30 / bias +0.10 | 0.8000 | INSUFFICIENT |
| acc 0.50 / bias +0.2375 **[live]** | 0.7725 | INSUFFICIENT |
| acc 0.50 / bias −0.3000 (underconfident) | 0.8800 | INSUFFICIENT |
| acc 0.50 / bias +0.2375, failures classified | 0.6875 | INSUFFICIENT |

**(C) The lesson store votes.** Same SUFFICIENT calibration, but the lesson store
reports its own blindness:

| lesson store | calibrated | quality |
|---|---|---|
| blind share 0.0 | 0.4588 | SUFFICIENT |
| blind share 1.0 | 0.1059 | INSUFFICIENT |

---

## 6. PRODUCTION PROOF

`systemctl start` on both 07:00/07:15 units after a manual run:

```
chron-prediction-verifier ExecMainStatus = 0
chron-loop-closer         ExecMainStatus = 0
```

`chron-loop-closer` journal, final run:

```
  Status: ACTIVE
    episodes_created: 0        predictions_new: 0
    predictions_verified: 0    lessons_extracted: 0
    policies_promoted: 0
  State:
    predictions_total: 29      predictions_active: 22     predictions_decisive: 4
    lessons_total: 2           lesson_candidates: 0
CHRON Briefing … ✅ Injected to carry_forward.json
chron-loop-closer.service: Deactivated successfully.
```

Fresh `load_calibration()` callers (proof a, `tests/evidence-load-calibration-callers.txt`):

```
/root/chron/chron_prediction.py:535:def load_calibration() -> Optional[dict]:
/root/chron/chron_prediction.py:828:    stored = load_calibration()          ← NEW: inside calibration_snapshot()
...
820:def calibration_snapshot() -> dict:
895:    snapshot = calibration_snapshot()    ← inside generate_from_chron_events()
976:                outcome = recalibrate_confidence(proposed, snapshot)
1026:        outcome = recalibrate_confidence(proposed, snapshot)
```

Call chain: **generator → `calibration_snapshot()` → `load_calibration()` → `recalibrate_confidence()` → emitted confidence.**

---

## 7. INCIDENT — canonical file clobbered by a concurrent writer

At **11:26 MYT** the tree-consolidation lane replaced the stale copy at
`/root/AAA/scripts/chron_prediction.py` with a **symlink** to
`/root/chron/chron_prediction.py` (correct work), and then wrote its deprecation
shim **through that symlink** — overwriting the canonical module with 2069 bytes of
shim. All in-flight changes to `chron_prediction.py` were destroyed.

* **Detected by:** `ImportError: cannot import name 'get_verified'`, then
  `grep -c "^def "` returning 0 on a 1050-line module.
* **Repaired from:** `git show HEAD:chron_prediction.py` (23753 B, commit 68a2403 —
  byte-identical to the file that was patched), then all edits re-applied.
* **Preserved evidence (never deleted):**
  `/root/chron/.backup-learning-loop-20260921T032325Z/CLOBBERED-by-tree-agent-20260921T0326Z-chron_prediction.py`
* **A second, quieter loss:** one patch reported success but was absent from disk
  (the tool's "modified since last read" warning fired). Caught by grepping for the
  new comment after every patch. **Lesson: on this tree, verify each write on disk;
  a successful tool result is a claim, not a measurement.**

Guard taken: `chron_prediction.py.MINE`, `chron_learn.py.MINE`,
`chron_verify.py.MINE` sit in the backup dir, and the revert demo asserts a sha256
restore.

---

## 8. WHAT I COULD NOT DO

1. **The 29 records already in the live store still hold their original, uncalibrated
   birth confidence.** Verified: `preds with calibration audit: 0`. Predictions are
   *immutable at birth* (F2/F11 invariant, witness-flagged 2026-09-18) and there is
   a named stub, `_save_all_predictions`, that refuses to rewrite them. So the table
   in §5 is what the generator emits **when each claim is next generated**, not a
   rewrite of history. Closing the gap on existing rows would require a new record
   with a `supersedes` link — a store decision, and the stores are under another
   lane's migration. **Reported, not done.**
2. **`load_lessons` is consumed but no lesson yet *changes* a number.** Lessons are
   read, labelled actionable/non-actionable, carried on every prediction, and given
   a **veto** over calibration quality — but `policy_applied` is honestly `false`,
   because no lesson has passed the promotion gate and criterion 3 (external
   validation) is not implemented. Treating a lesson as policy without a measured
   effect is exactly the failure this task exists to remove, so I did not fake one.
3. **The UNKNOWN class will keep appearing.** I removed one cause (the dropped
   `error_class`) but not all: `chron_verify._evidence_for()` *deliberately*
   declines every magnitude/threshold claim, and only a SearXNG-confirmed event
   produces `REGIME_CHANGE`/`NONE`. Until a unit-aware extractor over a named data
   source exists, most verified outcomes will remain unclassifiable and the store
   will stay `INSUFFICIENT`. That is correct behaviour, not a remaining bug.
4. **`MIN_EFFECTIVE_N = 8` is not reachable soon from the current store.** It sits
   at n = 4. Earliest active `verify_at` is **2026-09-23**, with 11 of 22 active
   predictions dated 2026-09, so the floor should be approached within weeks — but
   only if the verifier can gather evidence, which for threshold claims it cannot
   (see 3). **Falsifiable prediction, logged here:** the store will still report
   `INSUFFICIENT` on 2026-10-09 unless at least 4 more *classifiable* decisive
   verdicts land.
5. **`chron_loop_close.py` is outside my envelope**, so the promotion gate there
   was not edited. The actionability requirement is instead enforced upstream in
   `chron_learn.get_candidates()`, which is that gate's only input. A future editor
   adding a second path into `_evaluate_promotion` would bypass it.
6. **The reliability curve (per-bin calibration) is not implemented.** The shrink is
   global toward `ā`. Disclosed in the code (`Known limitation`) and in §2.
7. **`test_learn_quality.py` (another lane's new file) has one failing check** —
   `FileNotFoundError` reading the insufficiency ledger that correctly does not
   exist. Not mine, not touched. Every substantive assertion in it passes.

---

## 9. FILES

**Changed** (backups: `/root/chron/.backup-learning-loop-20260921T032325Z/`)

| file | sha256 |
|---|---|
| `/root/chron/chron_prediction.py` | `6d5b1ae34594f15bf4d8bfe804a407ba0f798c55f9ff9588e96059b23d3f6464` |
| `/root/chron/chron_learn.py` | `d8396109fd2962b76899f9b99f62edd5bf8bf3bbc93707508c4f4b1501f05b8f` (also revised by another lane) |
| `/root/chron/chron_verify.py` | `4cc9526bd61da141ff68fa3a1849e2aac4bb10a5b2daa71818d35ca2596956ed` |

**Added**

* `/root/chron/tests/test_calibration_loop.py` — the falsifiable suite (64 checks)
* `/root/chron/tests/demo_reverted_generator.py` — the deliberate-failure proof
* `/root/chron/tests/evidence-suite-new-wiring.txt`
* `/root/chron/tests/evidence-reverted-suite.txt`
* `/root/chron/tests/evidence-revert-demo.txt`
* `/root/chron/tests/evidence-before-after-table.txt`
* `/root/chron/tests/evidence-load-calibration-callers.txt`
* `/root/AAA/reports/chron-learning-loop-closure-2026-09-21.md` (this report)

**Not touched:** anything under `/root/chron/data/`, anything under
`/root/AAA/scripts/`, `/root/chron/chron_loop_close.py`, `chron_loop_close.py`'s
promotion gate, and the other lane's `test_learn_quality.py` /
`chron_ledger_integrity.py`.

---

## 10. FUTURE-CONTEXT BENEFIT

Tomorrow's session can now ask a falsifiable question that was unaskable
yesterday: *"did the last verified outcome move any future confidence?"* The answer
is readable straight off a prediction record — `confidence_proposed`,
`confidence_calibrated`, `calibration_quality`, `calibration_snapshot`,
`lessons_consumed` — and the direction is derivable from the store rather than
asserted by the generator. When the store finally crosses `n ≥ 8`, the same code
path starts trusting the measured base rate with no further surgery: the anchor
switches from 0.5 to `ā`, `w` rises, and the correction grows with the evidence.

DITEMPA BUKAN DIBERI ⚒️
