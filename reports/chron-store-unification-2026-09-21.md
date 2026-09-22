# CHRON Prediction-Store Unification — Receipt

**Task:** unify two divergent CHRON prediction stores into one canonical store, stop
correlated samples being counted as independent evidence, recompute one calibration.
**Host:** KVM8 (forge) · **Date:** 2026-09-21 · **Migration id:** `chron-store-unify-20260921`
**Policy id:** `chron-correlated-sample-rule-v1`
**Canonical store:** `/root/chron/data/predictions.jsonl`
**Store-scoped calibration artifact:** `/root/chron/data/calibration_store_unified.json`
**Receipt (machine):** `/root/chron_migration/receipts/chron-store-unify-20260921.json`
**Report author scope:** data files under `/root/chron/data/*` and
`/root/.hermes/cron/state/chron_personal/*`, plus new scripts in `/root/chron_migration/`.
No `.py` under `/root/chron/` and nothing under `/root/AAA/scripts/` was modified.

---

## 0. Result in one screen

| | before | after |
|---|---|---|
| live prediction stores | **2** (`predictions.jsonl` 20 rec · `predictions.json` 12 rec) | **1** canonical (29 rec) + 1 retired, marked, with pointers |
| calibration surfaces | 2, claiming **0.24625** and **0.1825** for the same system | 1 canonical surface, correlated-aware, **total n=3 · mean_brier 0.225** |
| decisive samples counted | xau hypothesis pair counted as 2 independent | counted as **1 observation** (raw n shown beside effective n) |
| records destroyed | — | **0** (12/12 S2 records recoverable verbatim) |
| idempotent | — | **yes**, proved by running twice, byte-identical store |

The disputed pair of numbers is resolved and no live surface publishes either of them:
`0.24625 = (0.0025+0.49)/2` and `0.1825 = (0.0625+0.3025)/2` were both **arithmetically
correct on different universes**. Neither was the system's calibration. The unified store
gives raw n=4 / brier 0.214375 and effective n=3 / brier 0.225 — see §5.

---

## 1. Measured pre-state (counted by hand, no count field trusted)

```
S1 /root/chron/data/predictions.jsonl       20 records   sha256 d48d4e2f2e11a3c1…d373582e  (25,962 B)
   status: ACTIVE 16 · CORRECT 1 · VOIDED_SECTION_12 3
S2 /root/.hermes/cron/state/chron_personal/predictions.json  12 records   sha256 c168ec9d0a1deefb…0b0c6aaad2
   count field = 12; hand count = 12  → field agrees with reality here
   state: ACTIVE 10 · VERIFIED 2
S1 calibration.json  before: total 2 · correct 1 · incorrect 1 · accuracy 0.5 · mean_brier 0.24625
S2 calibration_report.json before: total_predictions 5 · verified 2 · mean_brier 0.1825 · OVERCONFIDENT
```

### Brief corrections (my measurement outranks the brief)

1. **"20 records. status: 16 ACTIVE, 1 CORRECT, 3 VOIDED_SECTION_12" — CONFIRMED exactly.**
2. **"count field says 12, actual 12" — CONFIRMED.** The count field is not a defect here.
3. **`mean_brier 0.246` — CONFIRMED but incomplete: it is `0.24624999999999997`.**
   It is not a store statistic: `compute_calibration()` joins `predictions.jsonl` with
   `verification_log.jsonl`, and the two decisive verdicts there are
   `pred-chron-loop-test-0bc4ce80` (brier 0.0025) and `pred-d54455f9b039` (brier 0.49).
   Neither xau row was in S1 at all.
4. **"S2's two 'verified' predictions are BOTH about the same asset on the same date … one
   hit, one miss" — CONFIRMED, with a detail the brief omits:** the two records disagree with
   themselves about the date. Claim text says *"by 2026-09-18"*; `expected_outcome` and
   `verify_at` both say **2026-09-17 23:59 MYT**. The resolving observation is a single
   XAUUSD print (`price_observed 4399.7`, `price_source yfinance:GC=F`,
   `price_observed_at 2026-09-17T00:00:00Z`). Same observation, confirmed by the data.
5. **NEW defect the brief did not name: `calibration_report.json` was stale, not merely
   divergent.** Generated `2026-09-18T13:50:10Z`; the store it claims to describe was last
   written `2026-09-20T11:35:47Z` (two days later), and `total_predictions: 5` describes an
   earlier 5-record epoch of that store. It was never re-derived after the price predictions
   were added. A reader was being shown a 5-row snapshot of a 12-row store.
6. **NEW defect the brief did not name: the same claim was asserted with two different
   confidences.** Three claims exist in both stores, worded differently, at *different*
   confidence: BNM OPR 0.8 vs 0.5 · CPI 0.75 vs 0.5 · GDP 0.7 vs 0.5. Two pipelines were
   asserting the same proposition with materially different conviction and nothing reconciled
   them. (§3, merge policy: both kept, divergence recorded, no averaging.)
7. **The brief's framing "both are seeded from the same chron_events.json (8 dated events)" —
   CONFIRMED (8 events), but the seeding is not symmetric:** S1 takes the per-event
   `predictions[]` array; S2 takes an event-level fallback that only fires for events inside a
   90-day window. That difference is why the two stores never converged — they were not
   describing the same slice of the same source.

---

## 2. Schema mapping S2 → S1

S2 is `chron_predictions_v0` (whole-file JSON, in-place mutation on verify).
S1 is JSONL, immutable birth record + append-only verification log.

| S2 field | S1 field | note |
|---|---|---|
| `state` | `status` | `ACTIVE`→`ACTIVE`; `VERIFIED`→ birth record stays `ACTIVE`, verdict moves to the verification log (see below) |
| `prediction_id` | `prediction_id` | **preserved verbatim** — no re-minting, so ids stay resolvable |
| `horizon_sessions` | `horizon` | `1` → `"1s"`, `5` → `"5s"`; S2 counts sessions, S1 uses a duration string |
| `price_source` | `probe_id` | the evidence act that resolves a price claim; also read directly for grouping |
| `instrument`, `direction`, `threshold`, `baseline_price`, `baseline_date`, `regime_context`, `macro_context`, `price_data_quality`, `price_observed`, `price_observed_at`, `check_window_max`, `schema_version` | same names | carried through unchanged |
| `outcome` (HIT/MISS), `brier_score`, `error`, `error_type`, `observed_outcome`, `verified_at` | **verification log**, not the birth record | S1's invariant: verification is a separate append-only record keyed by `prediction_id` |
| `claim`, `expected_outcome`, `confidence`, `verify_at`, `assumptions`, `source`, `source_id`, `principal`, `created_at`, `supersedes` | same names | unchanged |
| *(absent in S2)* | `falsifier`, `verifier_method`, `success_rule`, `world_state_hash` | written as **`null`**, not invented. Absence is recorded as absence. |
| *(absent in S2)* | `machine_unverifiable` | set `true` for migrated rows (S2 claims had no machine probe binding beyond price_source) |
| — | `migration{…}` | provenance block on every inserted row |
| — | `merged_from[…]` | provenance block on every merged row |

**Losslessness:** each inserted row embeds `migration.original_record` (the S2 record
verbatim) and each merged row embeds `merged_from[i].original_record`. All 12 S2 records are
recoverable byte-for-byte from the canonical store — verified in §7.1.

### Why S1 is canonical (evidence, not preference)

1. **Schema surface:** 20 records carry 47 distinct fields including `falsifier`,
   `verifier_method`, `success_rule`, `threshold`, `brier_score`, `error_type`, `surprise`,
   `void_reason_class`. S2 carries 33, with no falsifier at all.
2. **Architecture:** S1 implements the immutable-birth-record invariant with a separate
   append-only verification log (`verification_log.jsonl`, last-write-wins, VOID to retract).
   S2 mutates the prediction dict in place on verification
   (`prediction_store.verify_prediction`), so S2 cannot prove what it believed at birth.
   A store that rewrites its own beliefs cannot be calibrated.
3. **Live machinery:** S1's store is read/written by live, enabled, firing timers —
   `chron-prediction-verifier.timer` (07:00), `chron-loop-closer.timer` (07:15) — plus the
   crontab `verify_due.py` (23:30 MYT) and `chron-mcp.service`. S2's only writer is
   `chron-task0-reconciliation.service` (06:50), which regenerates it from `chron_events.json`
   with a `source_id`-only dedupe and no verification log at all.
4. **Recency/consistency:** S1 was 25,962 B / 20 records; S2's 12 records include price
   hypotheses with no falsifier and no verifier method, and its companion report was provably
   stale (§1.5).

---

## 3. Migration receipt

```
S1 records before                     : 20
S2 records actual (count field = 12)  : 12
inserted                              : 9
merged                                : 3
accounted                             : 12 / 12   (abort condition if not equal — it was equal)
S1 records after                      : 29
S1 sha256 before                      : d48d4e2f2e11a3c1e2c56f8a5485b45b8f95463ad893ee71ff3f47bad373582e
S1 sha256 after (this migration)      : 9ea02b6858c40a36cd7a82da83ecfa28bfc581c44dd1208060f3166143e241c1
S2 sha256 before                      : c168ec9d0a1deefb608334cd9803069768560e224fbb7ef82318000b0c6aaad2
S2 sha256 after (retired)             : e1853d1f7c773496c11526333b33f0c0dbbbad9bb373daf2439fde5201367848
verification_log.jsonl before/after   : 55440d2485f1e07e6ef1c049e4944b905fc1da3db747af7ebfd4e6a0cd77c241 / 817ef5e9dff723486d985853d5af01503f2464946398661466954a2fde011451 (+2 outcome records)
```

### Inserted (9) — canonical id preserved from the original

| original id | original state | claim |
|---|---|---|
| `pred-ecceaf3f7ee4` | ACTIVE | Budget event: Belanjawan 2027 dibentang di Parlimen |
| `pred-73c28f73377f` | ACTIVE | Market event: Harga minyak kuat kuasa 17-23 Sept tamat |
| `pred-xau-001-up4250` | VERIFIED | XAUUSD closes > 4250 by 2026-09-18 (1 session horizon) |
| `pred-xau-002-down4000` | VERIFIED | XAUUSD closes < 4000 by 2026-09-18 — short hypothesis |
| `pred-xau-003-up4500` | ACTIVE | XAUUSD closes > 4500 within 5 sessions |
| `pred-oil-001-up75` | ACTIVE | OIL (WTI) holds > 70.0 by 2026-09-25 |
| `pred-gas-001-down30` | ACTIVE | GAS (NG) holds < 3.20 by 2026-09-25 |
| `pred-klci-001-up1640` | ACTIVE | KLCI holds > 1630 by 2026-09-25 |
| `pred-usmyr-001-down440` | ACTIVE | USMYR holds < 4.40 by 2026-09-25 |

The two S2 `VERIFIED` rows arrived as birth records **plus** two verification records
(`verif-mig-*`) carrying `verdict VERIFIED_CORRECT / VERIFIED_INCORRECT`,
`brier_score 0.0625 / 0.3025`, the observed price, and a `correlation_key` field. Both
outcomes therefore survive in the canonical home for verdicts — nothing was flattened into
the birth record.

### Merged (3) — same claim, two stores, two ids, two confidences

| S2 id | merged into (S1) | S2 conf | canonical conf | merge test |
|---|---|---|---|---|
| `pred-3ce8ccbd78f9` | `pred-c57a554045e7` | 0.5 | 0.8 | same resolving event + numeric content `{2.75}` |
| `pred-c44bc4fb5561` | `pred-7d905b858479` | 0.5 | 0.75 | same resolving event + numeric content `{1.7, 2.1}` |
| `pred-ddea17587bfb` | `pred-b225ca03d268` | 0.5 | 0.7 | same resolving event + numeric content `{5.0}` |

Both ids are kept: the surviving record carries `merged_from[]` with the original record
verbatim, the original confidence, and the confidence divergence, plus
`supersedes: "pred-…"`. **No averaging.** The 0.5-vs-0.8 divergence on an identical claim is
preserved as evidence and reported as a defect (§1.6).

### Left as correlated, not merged (disclosed, not silently collapsed)

`pred-ecceaf3f7ee4` (budget-2027) and `pred-73c28f73377f` (fuel-price-window) share a
resolving event with existing S1 rows but are *different claims*; the duplicate predicate
deliberately refuses to merge claims with no numeric anchor. They arrived as separate records
and are counted as correlated. Every such judgement is listed in the receipt under
`same_event_not_duplicate`, each with the reason (e.g. `numeric content differs ['2.05'] vs
['17']`, `no numeric anchor — not mechanically adjudicable`).

---

## 4. Correlated-sample rule

### Statement

> Two prediction records are **CORRELATED** — one independent observation, not two — when
> they share all three of:
> **(1) subject** — the entity/asset/event the claim is about (`instrument`, else
> `source_id`, else claim slug);
> **(2) window** — the resolution appointment (the `verify_at` date);
> **(3) resolving event** — the evidence act that produces the outcome (`probe_id`, else
> `price_source`, else `instrument|baseline_date`, else `source_id`).
>
> Records sharing all three form a **sample group**. A group of size *k* contributes
> **exactly one** unit to *effective n*. Group score = unweighted mean of member scores;
> group hit-rate = hits ÷ k. Singletons are groups of size 1 and are untouched.
>
> **Raw n and effective n are both printed, always**, with the difference named
> (`correlation_inflation.samples_removed`) and each multi-member group disclosed with its
> member ids. A number that hides its denominator is not reported here.

**Two distinct deduplications, deliberately not conflated:**
* **DUPLICATE** — same claim asserted twice → **merge**, record both ids → contributes 1 to raw *and* effective n.
* **CORRELATED** — different claims over one resolving event (the XAU pair) → **keep both records**, count the group once.

### Why this rule and not "same instrument = same sample"

The rule is the store's own event ontology made explicit. S1 already groups predictions by
`source_id` (the event that generated them); S2 groups them by the event record too. What was
missing was the *consequence*: sharing a resolving event means sharing the resolving
observation, so those rows are not independent evidence. The rule is stated on the fields the
store already carries, so it is checkable by a reader who trusts nothing but the data.

### The measured instance

```
group k=2  ['pred-xau-001-up4250', 'pred-xau-002-down4000']
   subject=(instrument,XAUUSD) window=2026-09-17 resolving_event=yfinance:GC=F
   hits=1 misses=1 hit_rate=0.5 group_brier=0.1825
```

`0.1825` — the number S2's report published as CHRON's calibration — is *exactly* the mean
Brier of these two correlated members. It was never wrong arithmetic; it was a one-observation
sample wearing a denominator of two.

### Groups disclosed before they can inflate (currently unresolved)

| k | subject/event | window | members |
|---|---|---|---|
| 4 | weekly-agentic-maintenance | 2026-09-28 | `pred-4b67c1dad6b0`, `pred-1be85d3c7117`, `pred-a19cbc2dfd9b`, `pred-d54455f9b039` (1 already resolved) |
| 3 | budget-2027 | 2026-10-09 | `pred-fdb40342252b`, `pred-e3808eff19ee`, `pred-ecceaf3f7ee4` |
| 3 | fuel-price-window | 2026-09-23 | `pred-5004749ee139`, `pred-a1210fe9e53c`, `pred-73c28f73377f` |
| 2 | einv-svdp | 2027-12-31 | `pred-b08104a9ed9f`, `pred-ee1b02e2897d` |
| 2 | od1 | 2027-03-01 | `pred-283d3e08da11`, `pred-aaafe3e432cf` |

### Negative control (required, and it is a real test)

`python3 /root/chron_migration/test_correlated_rule.py` → **ALL PASS**

```
A) CORRELATED PAIR (one resolving event, two claims) -> effective n=1
   [PASS] raw n=2   [PASS] effective n=1   [PASS] samples removed=1
   [PASS] raw mean_brier=0.1825   [PASS] effective mean_brier=0.1825
   [PASS] group size=2   [PASS] group hit_rate=0.5
B) UNCORRELATED PAIR (different subject+event) -> effective n=2      <-- negative control
   [PASS] raw n=2   [PASS] effective n=2   [PASS] samples removed=0
   [PASS] effective mean_brier equals raw (nothing collapsed)
C) SAME SUBJECT+EVENT, DIFFERENT WINDOW -> effective n=2             <-- window clause
D) SAME SUBJECT+WINDOW, DIFFERENT RESOLVING EVENT -> effective n=2   <-- event clause
E) ONE CORRELATED PAIR + ONE SINGLETON -> raw 3, effective 2
F) DUPLICATE vs CORRELATED are different predicates
   [PASS] xau pair is CORRELATED, not a duplicate (reason: numeric content differs ['4250'] vs ['4000'])
   [PASS] same claim across stores -> duplicate (reason: same resolving event, content ['2.75'])
   [PASS] two no-numeric claims are NOT auto-merged (no numeric anchor — not mechanically adjudicable)
   [PASS] same event, different asserted value -> NOT duplicate
G) NUMERIC TOKENISER hygiene (range dash ≠ minus; ISO dates, times, Q-labels stripped)
H) LIVE CANONICAL STORE invariants — every group of k>1 contributes 1
```

Case B is the control that matters: a rule that collapsed everything would score 100% on
case A and destroy the evidence. Case C and D prove the rule is a conjunction, not
"same asset ⇒ same sample".

---

## 5. One calibration, recomputed from the unified store

```
python3 /root/chron_migration/chron_store_unify.py --calibrate-only
```
```
canonical store : /root/chron/data/predictions.jsonl
store sha256    : 71f8983a5bf132f636240cc538cc43e380db88c47c173077480f068ab998b0f3
records         : 29
RAW        n=4  correct=2 incorrect=2  accuracy=0.5  mean_brier=0.214375
EFFECTIVE  n=3  correct=1 incorrect=1 mixed=1  accuracy=0.5  mean_brier=0.225
correlation inflation: 4 -> 3 (1 correlated sample removed)  brier 0.214375 -> 0.225
resolved group k=2 hits=1 misses=1 [xau-001, xau-002] hit_rate=0.5 brier=0.1825
```

Decisive set after unification (raw n = 4):
`pred-chron-loop-test-0bc4ce80` CORRECT 0.0025 · `pred-d54455f9b039` INCORRECT 0.49 ·
`pred-xau-001-up4250` CORRECT 0.0625 · `pred-xau-002-down4000` INCORRECT 0.3025.
Groups: 3 → **effective n = 3**.

Both numbers are in the artifact, side by side, with the inflation named. The headline
(`total`, `accuracy`, `mean_brier`) is the **effective** figure, because accuracy over
non-independent samples is not accuracy; `raw` carries the naive figure for audit.

`mixed: 1` is deliberate — the xau group is one observation that contains one hit and one
miss, and reporting it as either a hit or a miss would be the same defect in a new costume.

### Retirement of the other calibration artifact

`/root/.hermes/cron/state/chron_personal/calibration_report.json` — **left in place, in the
same path, marked `_SUPERSEDED` with pointers** to the canonical artifact, the durable copy
and this receipt. Its original content is preserved under `_original_report`, and a frozen
byte-identical copy sits beside it at
`calibration_report.superseded-chron-store-unify-20260921.json`
(sha256 `9320f907b60bd71dba4bcf5b09fe47aad836ba5b60c18752a88786c5c12bbd9a`).
**Nothing deleted.**

Also retired in place: the S2 store itself (`predictions.json`), every record marked
`state: SUPERSEDED` with `state_original` preserved and a per-record `superseded_by` pointer
to its canonical id; plus a frozen copy
(`predictions.superseded-chron-store-unify-20260921.json`,
sha `c168ec9d0a1deefb608334cd9803069768560e224fbb7ef82318000b0c6aaad2`) and a top-level
`_SUPERSEDED` banner. All 12 `source_id` values are deliberately retained so that the 06:50
`task0_reconciliation` job, which rewrites that file only when it finds a NEW `source_id`,
does not regenerate the store behind our back. Each record's `state` is set so that
`task0_reconciliation.load_prediction_status()` stops publishing a competing accuracy.

---

## 6. Idempotence — proved by running it twice

### On the live stores
```
run 2:  inserted 0 · merged 0 · store sha256 before = after = 9ea02b6858c4…43e241c1
        IDEMPOTENCE: unchanged since last run = True
        retired store already marked — left byte-identical
        retired calibration report already marked — left byte-identical
```
S2's retired file is byte-identical before and after the second run
(`e1853d1f7c77…01367848`).

### End-to-end, clean, on real data copies
`bash /root/chron_migration/reproduce_in_sandbox.sh` — seeds a sandbox from the
pre-migration backups and runs the whole migration twice:
```
SEED           data/predictions.jsonl        d48d4e2f…d373582e   (20 records, the original)
               chron_personal/predictions.json c168ec9d…0b0c6aaad2 (12 records, the original)
RUN 1          inserted 9 · merged 3 · accounted 12 · sha d48d4e2f… → 62d3978849c0…b406eac7
RUN 2          inserted 0 · merged 0 · IDEMPOTENCE unchanged since last run = True
               sha 62d3978849c0…b406eac7 → 62d3978849c0…b406eac7   (byte-identical)
SANDBOX: ALL PASS  (14/14 assertions)
```
Idempotence mechanism: already-migrated ids are detected from the store itself
(`migration.original_id`, `merged_from[].original_id`); every timestamp is read back from the
existing receipt rather than regenerated; retirement markers are detected and re-asserted, not
rewritten; backups are content-addressed and re-used instead of re-created.

---

## 7. Verification battery (independent of the migration's own report)

`python3 /root/chron_migration/verify_unification.py` → **ALL PASS (43 checks)**

1. **Losslessness** — all 12 S2 records recoverable from the canonical store, each compared
   by canonical-JSON sha256 against the pre-migration backup: 12/12 match. Frozen copy ==
   pre-migration S2.
2. **Line integrity** — of the 20 original S1 lines, **17 are byte-identical** and the 3
   changed are exactly the 3 merge targets. Appended lines are exactly the 9 migrated ids.
2b. **Live divergence, measured** — the live store was rewritten at 11:31:59 MYT by a
   concurrent repair which ADDED `ledger_id` and `superseded_*` to rows. Verified: record
   count still 29, ids unchanged, **no migration field removed**, `migration` provenance
   present on all 9 appended rows, `merged_from` present on all 3 merge targets. The other
   writer built on this migration rather than reverting it.
3. **Outcomes** — `verif-mig-*` records present exactly once each; verdicts
   `VERIFIED_CORRECT` (0.0625) / `VERIFIED_INCORRECT` (0.3025); correlation disclosed.
4. **Retirement** — banner present and naming the canonical store; 12 records kept; all
   `SUPERSEDED`; all 12 `superseded_by` pointers resolve to real canonical ids; original
   calibration report preserved (`mean_brier 0.1825` still readable inside `_original_report`).
5. **Surfaces do not disagree** — `calibration.json` and the store-scoped artifact agree on
   `total=3`, `accuracy=0.5`, `mean_brier=0.225`, `effective_n=3`. Neither publishes 0.24625
   or 0.1825.
6. **Legacy path, measured not predicted** — calling the unmodified
   `chron.chron_prediction.compute_calibration()` on the unified store returns
   `total=4, mean_brier=0.214375` — i.e. the **raw** count, and it does **not** apply the
   correlated rule. Our artifact reports that same figure in its `raw` block, so the two never
   contradict; but see §8.

### sha256 of the store before and after (required deliverable)

```
BEFORE  /root/chron/data/predictions.jsonl   d48d4e2f2e11a3c1e2c56f8a5485b45b8f95463ad893ee71ff3f47bad373582e  (20 records, 25,962 B)
AFTER   (this migration)                     9ea02b6858c40a36cd7a82da83ecfa28bfc581c44dd1208060f3166143e241c1  (29 records)
AFTER   (live now, + concurrent writer)      71f8983a5bf132f636240cc538cc43e380db88c47c173077480f068ab998b0f3  (29 records + ledger_id/superseded_*)
SANDBOX reproduction of the AFTER           62d3978849c0947a21c0f0dcbdc970bd3a757376f9d466b9381b8bf4b406eac7
```
The sandbox hash differs from the live one because `migrated_at` is embedded in every
migrated row; that is the only intended source of variation.

---

## 8. WHAT I COULD NOT DO

1. **I could not make `calibration.json` durably mine, and I did not pretend to.** That file
   has **seven** unowned writers. Verified by grep: `chron_cron_verify.py:67-68` (timer 07:00
   MYT), `chron_loop_close.py:64-66` (timer 07:15), `chron_learn.py:243-244`,
   `chron_verify.py:343-344`, `__main__.py:119`, `chron_mcp.py:101` — plus a concurrent
   agent's ledger repair. During this task it was rewritten at least **five** times under me
   (11:29:34, 11:31:59, 11:33:42, 11:34:57, and once more at 11:35:13 MYT). Two of those were
   the legacy raw writer publishing `total=4 / mean_brier=0.214375`; snapshots of the
   clobbered states are preserved at
   `/root/chron_migration/evidence-calibration-json-clobber-033155Z.json` and
   `/root/chron_migration/evidence-calibration-json-legacy-clobber-033513Z.json`.
   At the moment of delivery the surface is correct — the drift check returns
   `DRIFT: none — headlines agree` (`total=3`, `mean_brier=0.225`) — but that is a *current
   reading*, not a guarantee, and the next 07:00/07:15 fire can change it. Repairing the code
   path is a change
   under `/root/chron/` which the brief forbids me to make. **What I did instead:**
   (a) wrote the correlated-aware result to that file (it is correct at the time of writing
   — `total=3`, `mean_brier=0.225`);
   (b) put the durable artifact at a non-contested path
   (`/root/chron/data/calibration_store_unified.json`) that nothing else writes;
   (c) added `chron_store_unify.py --check-drift`, which compares the headline figures and
   **exits 1 on disagreement** — so the next clobber is loud, not silent;
   (d) made `--calibrate-only` refuse to overwrite a `calibration.json` that already declares
   an effective-n policy (it repairs only a legacy-shaped one), so it stops fighting the
   owner while still repairing regressions.
   **Code change required (not made):** point the scheduled producers at the correlated rule —
   `chron_prediction.compute_calibration()` must count observations, not hypotheses. Either
   route `chron_cron_verify`/`chron_loop_close` through
   `chron.chron_ledger_integrity.compute_calibration_unified()`, or have
   `compute_calibration()` import this rule. Measured urgency: today the legacy path publishes
   `total=4 / 0.214375` while the correct figure is `total=3 / 0.225`.
2. **A concurrent agent solved the same problem at the same time, in the same tree.** At
   11:24–11:32 MYT, while this migration was running, `/root/chron/chron_prediction.py` and
   `/root/chron/chron_learn.py` were modified and a new
   `/root/chron/chron_ledger_integrity.py` appeared (sha256
   `657b8f5c90fbb1fb11b73d95d693b80e2468ca55d79488fdfdd834781c4a617c` at the time of
   measurement; it is a moving target). It implements observation-level de-duplication (its
   "R2") over **both** stores rather than unifying them. **I did not modify any of it.** The
   two implementations were cross-checked against each other and agree:
   * their `duplicate_guard` fires on observation
     `price|XAUUSD|yfinance:GC=F|4399.7|2026-09-17T00:00:00Z`, `n_before 4 → n_after 1`;
   * their `observations` count = **3** = my effective n;
   * their unified calibration = `total=3, correct=1, incorrect=1, mean_brier=0.225` = my
     effective figures, to the last digit;
   * both later adopted my merged ids and added `ledger_id` to all rows.
   Residual difference, disclosed rather than smoothed: **raw_n scope** — mine counts rows in
   the canonical store (4); theirs counts rows across both files (6, then 4 once the retired
   file's copies are excluded), because the retired file's 12 records still exist by design
   ("never delete"). Both collapse to effective n=3.
3. **I did not touch the S2 writer's code.** `/root/scripts/chron_personal/prediction_store.py`
   and `task0_reconciliation.py` are outside my declared ownership. Residual risk, stated
   plainly: if a NEW event lands in `/root/chron/chron_events.json` inside its 90-day window,
   the 06:50 job will find a new `source_id`, rewrite the retired file and drop my banner —
   regenerating a second store with a fresh id-space. I mitigated by keeping all 12
   `source_id` values present (so `added == 0` and no write occurs) and by making re-running
   the migration re-assert the banner. **This is a fragile mitigation, not a fix.** The fix is
   a one-line change in another lane's file: delete the "regenerate predictions" step (7) from
   `task0_reconciliation.py`, or point `prediction_store.PREDICTIONS_FILE` at the canonical
   store.
4. **The retired store's 12 records are still physically present** — deliberately, per the
   brief ("never delete"), and now duplicated by id in the canonical store. Verified: all 12
   retired ids exist in the canonical store, so **no claim lives only in the retired file**.
   But any reader that counts raw rows across both files without deduping will see 41 rows for
   29 claims. Both implementations dedupe this (mine by `prediction_id` + correlation key,
   theirs by observation key), and the live surfaces report 29/3 correctly — but the
   double-file layout is a standing trap for the next reader.
5. **Not done: no new cron, timer, or service.** Per AGENTS.md, a polling job needs F13
   approval. `--check-drift` is a command, not a schedule; wiring it to a timer would be a
   new background process and I did not add one.
6. **Not done: the `CORRECT`/`VOIDED_SECTION_12` statuses already inside S1's rows were left
   untouched.** S1 mixes the birth-record invariant (status `ACTIVE` + separate verdict) with
   legacy inline verdicts (`status: CORRECT` on `pred-chron-loop-test-0bc4ce80`,
   `VOIDED_SECTION_12` on three rows). Both are read correctly by my resolver and by the
   concurrent ledger, so this is not a live defect — but the store carries two conventions and
   a future writer can still mistake one for the other.
7. **Not done: the pre-verification `UNBOUND` status.** Current code can create rows with
   `status: UNBOUND`; no migrated row uses it, and the 3 `machine_unverifiable` flags on
   migrated rows are my inference from the absence of a machine probe, disclosed as such.

---

## 9. Files — created, modified, backed up

**Created**
```
/root/chron_migration/correlation_rule.py          the rule (pure functions, no I/O)
/root/chron_migration/chron_store_unify.py         idempotent migration + calibration + retirement + --check-drift
/root/chron_migration/test_correlated_rule.py      negative-control suite (ALL PASS)
/root/chron_migration/verify_unification.py        independent verification battery (43 checks, ALL PASS)
/root/chron_migration/reproduce_in_sandbox.sh      end-to-end repro on real data copies (14/14 PASS)
/root/chron_migration/final_evidence.py            evidence capture (every number in this report)
/root/chron_migration/crosscheck_parallel_impl.py  cross-check vs the concurrent implementation
/root/chron_migration/measure_store_change.py      diff of the store across the concurrent writer
/root/chron_migration/receipts/chron-store-unify-20260921.json          cumulative receipt
/root/chron_migration/receipts/…run-<timestamp>.json                    per-run receipts
/root/chron_migration/backups/chron-store-unify-20260921/…              17 timestamped backups
/root/chron_migration/evidence-calibration-json-clobber-033155Z.json    snapshot of a clobbered surface
/root/chron/data/calibration_store_unified.json    durable correlated-aware calibration
/root/.hermes/cron/state/chron_personal/predictions.superseded-chron-store-unify-20260921.json
/root/.hermes/cron/state/chron_personal/calibration_report.superseded-chron-store-unify-20260921.json
/root/AAA/reports/chron-store-unification-2026-09-21.md   (this report)
```

**Modified (all backed up first, timestamped, none deleted)**
```
/root/chron/data/predictions.jsonl                 20 → 29 records
/root/chron/data/verification_log.jsonl            +2 outcome records (append-only)
/root/chron/data/calibration.json                  rewritten correlated-aware (see §8.1)
/root/.hermes/cron/state/chron_personal/predictions.json            records marked SUPERSEDED + banner
/root/.hermes/cron/state/chron_personal/calibration_report.json     marked _SUPERSEDED + pointer
/root/.hermes/cron/state/chron_personal/task0_latest.json           _SUPERSEDED_NOTE added
```
**Not touched:** every `.py` under `/root/chron/`, everything under `/root/AAA/scripts/`,
every other file in the two data directories, and any backup ever written.

---

## 10. Reproduce

```bash
python3 /root/chron_migration/test_correlated_rule.py        # rule + negative control
python3 /root/chron_migration/chron_store_unify.py --dry-run  # what a migration would do
python3 /root/chron_migration/chron_store_unify.py           # migrate (idempotent)
python3 /root/chron_migration/chron_store_unify.py --calibrate-only
python3 /root/chron_migration/chron_store_unify.py --check-drift   # exit 1 on surface disagreement
python3 /root/chron_migration/verify_unification.py
bash    /root/chron_migration/reproduce_in_sandbox.sh
```

DITEMPA BUKAN DIBERI ⚒️
