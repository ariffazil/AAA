# SCHEMA_EVOLUTION_PROPOSAL

> **Ref:** ARIFOS::OBSERVABILITY_CONVERGENCE::P1 — PHASE 5
> **Authority:** ARIF (Human Sovereign) · **Mode:** GOVERNANCE-FIRST
> **Generated:** 2026-09-15T05:55Z by Hermes ASI (i-arif) on KVM8
> **Status: PROPOSAL ONLY. No mutation performed. No DDL issued. Awaiting F13.**

---

## 0. Gate check before reading further

Phase 5 is explicitly gated: *"ONLY AFTER PHASES 0-4 COMPLETE."*

Phases 0–4 are complete (4 graphs + 4 receipts produced). Phase 1 and Phase 3
returned **PARTIAL**; Phase 2 returned **PARTIAL** on a missing health surface.
No phase returned VOID and no role collapse was detected, so this proposal is
legitimately admissible.

**But one finding from Phase 4 changes the recommendation.** The gap audit found
that `observability.observations` has **zero consumers** (G-09). This proposal
therefore opens with a recommendation that precedes every schema change in §2.

---

## 1. Proposal 0 (precedes all DDL): establish a consumer before evolving the schema

**Evidence:** only `worker.py` and `postgres_backend.py` reference the table.
Grafana datasources are Prometheus plus an Infinity datasource pointed at
`http://169.254.169.254`. The single dashboard does not query this table.
201,495 rows. Nobody reads them.

**Options**

| Option | Description | Reversibility |
|---|---|---|
| **0-A** | Add a Grafana PostgreSQL datasource + a Kabarkan panel. Reading requires no schema change and no new service. | Trivial (delete datasource) |
| **0-B** | FRAME becomes the consumer (see KABARKAN_WITNESS_RECEIPT §4 option A/B). | Moderate |
| **0-C** | Stop writing; archive the table. | Expensive to undo |

**Recommendation: 0-A, then 0-B.** It is the smallest reversible step that makes
every subsequent schema decision answerable to a real reader. **Do not proceed to
§2 before a consumer exists** — otherwise every change below is verified only
against itself.

---

## 2. Schema evolution candidates

Each evaluated against: reversibility, data-loss risk, whether it can be backfilled,
and whether it can be verified without a consumer.

### E1 — Causal trace DAG (`parent_span_id` propagation)

- **Problem:** 0/201,495 rows populated; `distinct(trace_id) ≈ rows` → one trace per row.
- **Change:** no DDL. The column exists. The change is **producer-side**:
  `arifosmcp/runtime/telemetry.py` must propagate a caller context
  (`trace_id`, `parent_span_id`) instead of minting a fresh trace per emit.
- **Backfill:** impossible. Historical rows can never be correlated.
- **Risk:** low DDL risk, **moderate behavioural risk** — context propagation
  touches every instrumented call path.
- **Verification:** `count(distinct span_id) / count(distinct trace_id) > 1`
  after two hours of traffic.
- **Verdict: highest value, do first among schema work.** No migration, no data
  loss, purely additive at runtime.

### E2 — Token economics (`prompt_tokens`, `completion_tokens`, `cache_tokens`)

- **Problem:** columns do not exist; `model_name` and `cost_usd` cover 0.11%.
- **Change:** `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` × 3 (nullable, no default).
- **Backfill:** impossible — the data was never captured. `model_name`/`cost_usd`
  should be populated prospectively from FED/litellm responses.
- **Risk:** low. Nullable adds are non-blocking in PostgreSQL 11+.
- **Dependency:** FED/litellm currently has `otel_export: false` and
  `callbacks: []` — the upstream source must be enabled first or the columns
  will stay empty and reproduce G-09 one layer down.
- **Verdict: do after E1, and only together with the upstream capture.**

### E3 — Verdict grammar normalisation

- **Problem:** 76.1% of `verdict_class` values are not verdict tokens
  (OK 136,180 / PENDING 14,162 / COMPLETED 1,564 / SUCCESS 274 / ERROR 264 /
  METRICS_READING 225 / ALIGNED 24 / GAPS_FOUND 22 / CLEAR 16).
- **Change:** introduce `exec_status` (text, nullable) and **stop writing status
  into `verdict_class`**. Do **not** rewrite history in place.
- **Migration posture:** keep existing rows untouched; add a view
  `observability.verdict_clean` that maps legacy values to
  `(verdict_class, exec_status)`. Zero destructive operations.
- **Verification:** `count(*) where verdict_class not in
  ('SEAL','HOLD','VOID','SABAR')` trends to 0 for rows newer than the cutover.
- **Verdict: safe, and it repairs a governance-truth defect rather than a
  cosmetic one. High priority.**

### E4 — Organ attribution (`organ_id`)

- **Problem:** 100% of rows carry `'arifOS'`, including calls originating in
  A-FORGE, subagents, and external CLIs.
- **Change:** no DDL — derive `organ_id` from producer identity at emit time.
- **Caveat:** the correct derivation depends on the topology in the Phase 0
  capability graph; mis-derivation would silently mislabel federation-wide
  traffic. Requires a mapping table ratified by F13.
- **Verdict: defer until the producer identity model is agreed.**

### E5 — `metadata` hygiene

- **Problem:** 104,625 NULL + 96,644 JSON `null` + only 226 with an object.
  The column is effectively inert and its type is inconsistent at read time.
- **Change:** none recommended yet. Fixing it is premature while no consumer
  reads it.
- **Verdict: defer.**

---

## 3. Recommended sequence

```
Step 0   consumer exists (Proposal 0-A)              — no DDL, reversible
Step 1   E1 trace context propagation                — no DDL, additive runtime
Step 2   E3 verdict / exec_status split              — additive + view, non-destructive
Step 3   E2 token columns + upstream FED capture     — additive DDL, gated on upstream
Step 4   E4 organ attribution                        — needs ratified mapping
Step 5   E5 metadata hygiene                         — only if a consumer demands it
```

Rationale for the order: **observability of the change first, then the change.**
Steps 0–1 make every later step verifiable. Doing E2 first would produce three
more empty columns in an unread table.

---

## 4. Constraint compliance

| Constraint | Status |
|---|---|
| Graph Before Mutation | PASS — 4 graphs in Phase 0 |
| Witness Before Mutation | PASS — 4 receipts in Phases 1–4 |
| Reversible First | PASS — every step either adds nullable columns, adds a view, or is runtime-only |
| No Schema Breakage | PASS — no destructive DDL proposed; no column dropped, retyped, or renamed |
| No Data Loss | PASS — no backfill that overwrites; history preserved verbatim |
| No Service Interruption | PASS — no DDL requiring an exclusive lock on `observations` |
| Mutation performed | **NONE** |

---

## 5. Open questions requiring F13

1. **E4 organ taxonomy** — what is the ratified mapping from producer identity
   to `organ_id`? Cannot be derived safely from code alone.
2. **Step 0 choice** — Grafana PostgreSQL datasource (0-A), FRAME-as-consumer
   (0-B), or write-stop (0-C)? This determines whether the following schema work
   has an audience.
3. **E1 blast radius** — trace context propagation touches every instrumented
   call path. Confirm the scope of the change window.
4. **F-011** (from the failure graph) — retire the otelcol collector, or promote
   it to the real OTLP entry point for all organs? The decision changes whether
   E2 is captured at the collector or in-process.

---

## VERDICT

**PARTIAL** — proposal complete and admissible under the Phase 5 gate.

No schema mutation performed, as required. The proposal's substantive position is
that the most valuable evolution is **not in the schema**: it is establishing a
consumer, then propagating trace context — neither of which requires DDL. The
three genuinely new columns (E2) should wait until the upstream capture exists
and a reader is looking at the table.

*DITEMPA BUKAN DIBERI*
