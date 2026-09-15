# KABARKAN_WITNESS_RECEIPT

> **Ref:** ARIFOS::OBSERVABILITY_CONVERGENCE::P1 — PHASE 2
> **Authority:** ARIF (Human Sovereign) · **Mode:** GOVERNANCE-FIRST
> **Generated:** 2026-09-15T05:45Z by Hermes ASI (i-arif) on KVM8
> **Mutations:** none (Phase 2 is witness-only)

---

## 1. Objective restated

> FRAME observes the Telemetry Plane. FRAME observes. FRAME does not own.
> FRAME does not mutate.

This receipt is the **pre-integration witness**: it measures what there is to
observe, and records the defect that blocks integration.

---

## 2. The five monitored quantities — current measured state

| Quantity | Required by P1 | Measured | Source |
|---|---|---|---|
| ingestion rate | yes | 193,122 msgs on stream; consumer ack 193,128 | NATS `kabarkan-ingest` |
| worker lag | yes | **pending = 0** (fully drained) | consumer `kabarkan-worker-fresh` |
| last span timestamp | yes | 2026-09-15T05:37:03Z | stream `last_ts` |
| queue depth | yes | 0 pending / 193,128 acked | JetStream consumer state |
| database latency | yes | not exposed — derived proxy: newest row age < 5 min, 448 rows/hr | `observability.observations` |

Additional measured facts:

- `observability.observations`: **201,495 rows** (grew from 201,380 during audit).
- Worker is a batch writer: systemd drop-in `KABARKAN_POLL_INTERVAL=30.0`,
  `KABARKAN_BATCH_SIZE=50`.
- Stream retention: file storage, no `max_age` set on `kabarkan-ingest`.

---

## 3. BLOCKER — Kabarkan has no health surface  ⚠️ SUPERSEDED, see ADDENDUM

> P1 task 3: *Produce health surface.*

**Status at measurement time (13:35 +08): NOT SATISFIED — the surface did not exist.**
**A concurrent session created it at 13:41:48 (+08). See the ADDENDUM at the end of this file.**

The body of this section is preserved as measured at 13:35. Do not act on it without
reading the addendum.

```
curl http://127.0.0.1:18902/health   ->  connection refused (HTTP 000)
ss -ltnp | grep 18902                ->  no listener
```

`18902` is the `KABARKAN_HEALTH_PORT` default declared in
`A-FORGE/kabarkan/worker.py`'s docstring — but that file is **dead code**. The
live worker is `arifosmcp.runtime.observability.worker`, and it exposes no HTTP
surface at all.

Consequence: Kabarkan can fail completely and the only symptom is a stale
`max(start_time)` in Postgres. That is exactly the class of blindness this
convergence is meant to eliminate.

**Minimum viable health surface** (recommendation, not executed):
`service`, `stream_pending`, `last_span_ts`, `rows_total`, `rows_last_hour`,
`ingest_lag_seconds`, `collector_registered` (bool). Provenance-graded: every
field traceable to NATS or Postgres, no derived claims.

---

## 4. How FRAME should observe Kabarkan (design, not executed)

FRAME's current probe contract is `GET <organ>/health` with a 3 s timeout, one
entry per port in `ORGAN_PORTS`. Two options:

**Option A — register a real health endpoint.** FRAME adds `kabarkan: <port>`
to `ORGAN_PORTS`; Kabarkan exposes `/health`. Conforms to the existing probe
contract exactly; the least invasive.

**Option B — FRAME gets a native telemetry witness.** A dedicated chamber
queries NATS `/jsz` and Postgres directly. More powerful and independent of
Kabarkan's own self-report, but it adds an I/O burden to a witness that is
deliberately lightweight — and the observer must not depend on the observed.

**Recommendation: A now, B only if the plane becomes critical infrastructure.**
Prefer Option A because it keeps FRAME's contract uniform and preserves witness
independence: FRAME never reads Kabarkan's data, only Kabarkan's declared
liveness. Reading the data would make the witness a consumer and begin a role
merge.

---

## 5. Separation-of-powers check

| Rule | Status |
|---|---|
| FRAME observes, does not own | PASS — no ownership proposed |
| FRAME does not mutate | PASS — this receipt performed no mutation |
| Kabarkan stays ingestion plane | PASS — see §6 |
| No role collapse | PASS — 0 violations found |

---

## 6. Adversarial note — do not build on an unread ledger

The strongest finding against rushing Phase 2: **`observability.observations`
has no consumer.** Only `worker.py` and `postgres_backend.py` reference the
table; Grafana's datasources are Prometheus plus an Infinity datasource aimed at
`http://169.254.169.254` (a cloud metadata address, not a federation source);
the single dashboard does not query this table.

Therefore registering Kabarkan in FRAME produces a witness over a plane whose
output nothing reads. That is still strictly better than today (we would at
least detect ingestion death), but it should be stated plainly in the graph:
**Phase 2 gives us liveness, not usefulness.**

Second adversarial note: two distinct capabilities are named *kabarkan*.
`SIGNAL :18084 POST /kabarkan/broadcast` is a priority-classified alert
dispatcher (returns 422 without a body). `frame_organ/alert.py` lines 59 and 89
route drift escalation **there**, not to the telemetry plane. Any future
"wire FRAME into Kabarkan" change must disambiguate the name first, or it will
attach to the notifier silently.

---

## VERDICT

**PARTIAL** — evidence complete, integration blocked on a missing surface.

- Ingestion, worker lag, last span, queue depth: **measured and healthy.**
- Database latency: **not exposed**; proxy only.
- Health surface: **MISSING** — the single blocker for Phase 2 completion.
- FRAME integration: **designed, not executed** (witness-only phase).
- Role collapse: **0**.

---

# ADDENDUM — concurrent mutation discovered at 13:44 (+08)

This receipt was invalidated on its central claim within nine minutes of being
written. Recording it rather than quietly rewriting, because the *sequence* is
itself the finding.

## What happened

| Time (+08) | Event |
|---|---|
| 13:35 | Audit probes `:18902/health` → connection refused. No listener. Blocker recorded. |
| 13:41:48 | A **different session** creates `/root/scripts/kabarkan_health_server.py`, installs and starts `kabarkan-health.service`, and adds `kabarkan: 18902` to FRAME's live `ORGAN_PORTS`. |
| 13:42:13 | FRAME's next probe cycle reports `organs_up: 10, organs_total: 10` |
| 13:44 | This audit re-probes and finds the surface live |

**No lock, no claim, no announcement.** Two sessions wrote the same
observability plane inside a nine-minute window. Both believed they were acting
on current state. One of them was already stale.

## The surface, as built (measured 05:44Z)

`GET http://127.0.0.1:18902/health` → `status: healthy`

```json
{"organ":"kabarkan","role":"telemetry_plane","healthy":true,
 "postgres_healthy":true,"nats_healthy":true,
 "database_latency_ms":6.96,"ingestion_rate_1h":584,
 "worker_lag_messages":0,"queue_depth":0,
 "last_span_timestamp":"2026-09-15T05:42:28Z","last_span_age_seconds":94.3,
 "total_observations":201554,"nats_stream_messages":193198,
 "collector_status":"STANDBY","authority":"INGEST_AND_PERSIST_ONLY"}
```

**This satisfies every quantity Phase 2 asked for**, and exceeds it: database
latency, which this audit had marked "not exposed — proxy only", is now a direct
measurement. Phase 2's blocker is **RESOLVED — by another session, not by this one.**

## Independent corroboration that matters

The surface self-declares `collector_status: "STANDBY"`. That is a second,
independently-authored source confirming this audit's F-011 finding: the
otelcol collector is **not** in the ingest path. Two sessions, two different
methods, same conclusion.

`authority: "INGEST_AND_PERSIST_ONLY"` also declares the separation-of-powers
boundary explicitly — Kabarkan states it will not judge or govern.

## Corrected Phase 2 status

| P1 requirement | Before 13:41 | After 13:41 |
|---|---|---|
| ingestion rate | measured via NATS | **exposed** `ingestion_rate_1h` |
| worker lag | measured via JetStream | **exposed** `worker_lag_messages` |
| last span timestamp | measured via PG | **exposed** |
| queue depth | measured via JetStream | **exposed** |
| database latency | **proxy only** | **exposed** `database_latency_ms` |
| FRAME integration | not registered | **registered**, 10/10 organs up |

**Amended verdict: SEAL on the deliverable, PARTIAL on process.** The
convergence objective for Phase 2 is met. The method by which it was met —
concurrent unlogged mutation of shared infrastructure — is flagged in the
failure graph as F-013.

*DITEMPA BUKAN DIBERI*
