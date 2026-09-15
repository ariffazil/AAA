# OBSERVABILITY_GAP_AUDIT

> **Ref:** ARIFOS::OBSERVABILITY_CONVERGENCE::P1 — PHASE 4
> **Authority:** ARIF (Human Sovereign) · **Mode:** GOVERNANCE-FIRST
> **Generated:** 2026-09-15T05:55Z by Hermes ASI (i-arif) on KVM8
> **Schema changes:** none. This is measurement only.

---

## 1. Method

Population: `vault999.observability.observations`, **n = 201,495** (live, growing).
Every figure below is `count(column)/n` measured directly on the table, not
inferred. Layer coverage is the unweighted mean of that layer's declared
required fields — weights are shown so the reader can recompute. No estimation,
no projection.

## 2. Raw field census

| Field | Coverage | Note |
|---|---|---|
| `tool_name` | 100.00% | |
| `actor_id` | 100.00% | |
| `verdict_class` | 100.00% | grammar polluted — see §4 |
| `organ_id` | 100.00% | 100% of rows carry `'arifOS'` |
| `trace_id` | 100.00% | present, but **not shared** — see §3 |
| `span_id` | 100.00% | present |
| `input_hash` | 99.89% | |
| `delta_s` | 99.89% | |
| `latency_ms` | 65.13% | |
| `output_hash` | 65.02% | |
| `next_safe_action` | 63.87% | |
| `reasons` | 55.41% | |
| `session_id` | 21.13% | 3,575 distinct sessions |
| `model_name` | 0.11% | 225 rows |
| `cost_usd` | 0.11% | 225 rows |
| `uncertainty_tag` | 0.11% | |
| `vault_receipt` | 0.04% | |
| `parent_span_id` | **0.00%** | zero rows, all 201,495 |
| `metadata` (JSON object) | 0.11% | 226 rows carry an object; 104,625 NULL; 96,644 JSON `null` |
| `prompt_tokens` | **column does not exist** | |
| `completion_tokens` | **column does not exist** | |
| `cache_tokens` | **column does not exist** | |

## 3. The sharpest single measurement

`distinct(trace_id) ≈ 201,534` against `n = 201,495`.

One trace per row. **Nothing is ever correlated with anything.** The system
records 201,495 events that have never been related to each other — not parent
to child, not request to retry, not agent to subagent. Combined with
`parent_span_id = 0`, Kabarkan is not a distributed trace store with missing
links; it is a flat event log that happens to carry trace-shaped column names.

## 4. Verdict grammar pollution

`verdict_class` is a **constitutional** field (SEAL / HOLD / VOID / SABAR). It is
populated 100% of the time — with, in descending order:

```
OK              136,180    67.6%
HOLD             46,652    23.2%   <- constitutional
PENDING          14,162     7.0%
COMPLETED         1,564     0.8%
SEAL              1,459     0.7%   <- constitutional
VOID                645     0.3%   <- constitutional
SUCCESS             274     0.1%
ERROR               264     0.1%
METRICS_READING     225     0.1%
ALIGNED              24     0.0%
GAPS_FOUND           22     0.0%
CLEAR                16     0.0%
```

Execution status codes have leaked into the field that carries constitutional
verdicts. **Only 23.9% of rows carry a valid verdict-class token**, and the
largest single value (`OK`, 67.6%) is not a verdict at all. Any future query of
the form "how many decisions were HOLD?" is silently contaminated by a field
that is mostly status.

## 5. Layer coverage

| # | Layer | Required evidence | Measured | Score |
|---|---|---|---|---|
| **L1** | Execution & Ingest | tool, actor, latency, in/out hash, session, liveness | 100, 100, 65.13, 99.89, 65.02, 21.13 | **75.2%** |
| **L2** | Causal Trace DAG | parent_span_id, correlated trace_id | 0.00, ≈0 (one trace per row) | **0.0%** |
| **L3** | Token & Cost Economics | prompt/completion/cache tokens, model, cost | columns absent; model 0.11; cost 0.11 | **0.1%** |
| **L4** | Governance Decisions | verdict grammar, delta_s, next_safe_action, reasons, uncertainty | verdict 100 (23.9% valid grammar), delta_s 99.89, next 63.87, reasons 55.41, uncert 0.11, vault 0.04 | **78.3%** (weighted) |
| **L5** | RAG / Retrieval | retrieval span, doc ids, vector latency | no rows of any kind | **0.0%** |
| **L6** | Agentic Metabolism | FQ vector, hold/throttle events, loop limits | vector LIVE at `:7073` but **zero transport edge into Kabarkan** | **0.0%** (in Kabarkan) |
| **L7** | Outcome Reality | task completion, sovereign-goal closure, business KPI | no rows of any kind | **0.0%** |

**Overall (unweighted mean of layers): ≈ 21.9%**

Weighting for L4: verdict 40 / delta_s 20 / next_safe 20 / reasons 10 /
uncertainty 5 / vault 5.

## 6. Gap catalogue

| id | Layer | Gap | Severity | Upgrade candidate |
|---|---|---|---|---|
| G-01 | L2 | No span DAG; one trace per row | **P0** | propagate `trace_id` + `parent_span_id` from the caller context in `telemetry.py` |
| G-02 | L3 | No token or cost columns at all | **P0** | add `prompt_tokens`, `completion_tokens`, `cache_tokens`; capture from FED/litellm responses |
| G-03 | L4 | Verdict grammar polluted by status codes | **P1** | split `verdict_class` (SEAL/HOLD/VOID/SABAR) from a new `exec_status` |
| G-04 | all | `organ_id = 'arifOS'` on 100% of rows | **P1** | derive `organ_id` from producer identity, not a constant |
| G-05 | L6 | arifFlow vector never reaches Kabarkan | **P1** | Kafka-style transport of the vector snapshot per enforcement cycle |
| G-06 | L5 | No retrieval instrumentation | **P2** | instrument Qdrant/FalkorDB calls |
| G-07 | L7 | No outcome instrumentation | **P2** | emit a terminal span per task with a declared success predicate |
| G-08 | L1 | `session_id` 21%, `output_hash` 65% | **P2** | require session propagation at ingest |
| G-09 | — | **201,495 rows, zero consumers** | **P0** | a reader, or a decision to stop writing |
| G-10 | — | No collector/worker health surface | **P1** | see KABARKAN_WITNESS_RECEIPT §3 |

## 7. Adversarial finding — G-09 outranks the schema gaps

> **ADDENDUM 13:44 (+08):** G-09 and G-10 are **partially superseded.** A concurrent
> session started `kabarkan-health.service` at 13:41:48, which reads
> `observability.observations` (aggregate counts and latency) and is registered in
> FRAME as `kabarkan: 18902`. The table now has **one reader**, and the telemetry
> plane now has **a health surface**.
>
> The argument below is **weakened but not refuted**: the new consumer reads
> *counts and latency*, never row content. Nothing reads a verdict, a tool name,
> a trace, or a cost. "Nobody reads this table" becomes "one process counts this
> table." Content consumption remains zero. The recommendation to build a reader
> before evolving the schema stands; what changes is that a liveness consumer now
> exists, so the schema work is no longer strictly premature.

Every gap in §6 except L1 is a schema problem, and schema work is the most
expensive, least reversible kind of change available. G-09 is not a schema
problem: **nothing reads this table.** Only `worker.py` and `postgres_backend.py`
reference `observability.observations`; Grafana's datasources are Prometheus plus
an Infinity datasource aimed at `http://169.254.169.254`; the one dashboard does
not query it.

Upgrading L2/L3 first would mean adding token economics and causal tracing to a
ledger nobody opens. **A complete schema for an unread table is still a table
nobody reads.** Recommended order: G-09 → G-10 → G-01/G-02.

## VERDICT

**PARTIAL** — audit complete, gaps catalogued, no schema mutation performed.

Coverage: **≈21.9%**, concentrated in L1 (ingest) and L4 (governance decisions).
Kabarkan is a competent **constitutional verdict ledger** and a non-existent
**AI observability engine** — it records what the federation *decided*, and is
blind to what it *cost*, what it *retrieved*, what it *spawned*, and what it
*achieved*. The gap is not evenly distributed: two layers carry the system and
five are empty.

*DITEMPA BUKAN DIBERI*
