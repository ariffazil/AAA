# Coverage Census — measuring whether a telemetry store is a plane or a ledger

Use for any "is the observability complete / do we have full observability?" question.
Liveness checks (worker active, consumer drained) answer a different, easier question.

Substitute your own schema/table names; the queries below assume
`observability.observations` in a Postgres database.

## 0. Load secrets / connection

```bash
set -a && source /root/.secrets/kunci-root.env && set +a
# POSTGRES_URL is set by this file. Note that a worker may use explicit PG* vars
# instead of the URL — check the unit's EnvironmentFile before assuming.
```

## 1. Column census — one query, every field

```sql
SELECT count(*) AS n,
  round(100.0*count(trace_id)/count(*),2)        trace_id,
  round(100.0*count(span_id)/count(*),2)         span_id,
  round(100.0*count(parent_span_id)/count(*),2)  parent,
  round(100.0*count(session_id)/count(*),2)      session,
  round(100.0*count(latency_ms)/count(*),2)      latency,
  round(100.0*count(model_name)/count(*),2)      model,
  round(100.0*count(cost_usd)/count(*),2)        cost,
  round(100.0*count(verdict_class)/count(*),2)   verdict,
  round(100.0*count(organ_id)/count(*),2)        organ,
  round(100.0*count(uncertainty_tag)/count(*),2) uncert,
  round(100.0*count(vault_receipt)/count(*),2)   receipt,
  count(DISTINCT trace_id)   distinct_traces,
  count(DISTINCT session_id) distinct_sessions
FROM observability.observations;
```

Read it as a shape, not a score. Fields at 100% can still be meaningless — see §3 and §4.

## 2. Correlation test

`distinct_traces ≈ n`  =>  one trace per row; nothing is correlated with anything.
Pair with the `parent` percentage. If `parent = 0.00`, no hierarchical root-cause
query is possible for any historical row and no backfill will create one.

## 3. Constant-field check

```sql
SELECT organ_id, count(*) FROM observability.observations GROUP BY 1 ORDER BY 2 DESC;
```

A single value at 100% means the field is a constant. The column exists, the
attribution does not.

## 4. Vocabulary / grammar check

```sql
SELECT verdict_class, count(*) FROM observability.observations GROUP BY 1 ORDER BY 2 DESC;
```

Declare the valid vocabulary up front (for a constitutional ledger: `SEAL`, `HOLD`,
`VOID`, `SABAR`). Anything else (`OK`, `COMPLETED`, `SUCCESS`, `ERROR`, `PENDING`,
`METRICS_READING`, `ALIGNED`, `GAPS_FOUND`, `CLEAR`) is an execution status that has
leaked in. Compute the valid share before quoting any statistic over this field — a
field that is mostly status will silently corrupt "how many HOLDs?" questions.

## 5. JSON column state-split

```sql
SELECT jsonb_typeof(metadata), count(*) FROM observability.observations GROUP BY 1;
```

`null` (JSON null) and an empty result (SQL NULL) are different states. Report them
separately; lumping them misreports coverage. A column that is mostly NULL or JSON
`null` with a handful of objects is effectively inert.

## 6. Liveness of the store (different question, still worth checking)

```bash
systemctl is-active <worker> <collector>
curl -s http://127.0.0.1:8222/jsz?streams=1&consumers=1   # msgs, last_ts, consumer pending
psql "$POSTGRES_URL" -tAc "select now()-max(start_time) as age,
  count(*) filter (where start_time > now()-interval '10 min') as last_10m
  from observability.observations;"
curl -s http://127.0.0.1:8888/metrics | grep -E '^otelcol_(receiver_accepted|exporter_sent)'
```

The last one matters for an OTLP collector specifically: **absent
`otelcol_receiver_accepted_*` and `otelcol_exporter_sent_*` families mean the
collector has carried zero traffic since boot**, whatever the process is doing. A
collector exposing only `otelcol_exporter_queue_*` for a single exporter is
decorative. Confirm the real ingest path separately by grepping for the producer —
a patch module, an in-process publisher, a direct stream write — and do not assume
OTLP is the entry point just because the port is open.

## 7. The gate — who reads it

```bash
grep -rl "observability\.observations" /root --include="*.py" --include="*.sql" --include="*.yaml"
```

If only the writer appears, it is a **write-only ledger**. That finding outranks any
coverage gap: adding schema to an unread table is not progress.

Also inspect the visualiser's datasources before claiming the data is "visible":
metrics-endpoint and generic HTTP datasources do not read a relational table. A
single unrelated dashboard does not make the ledger consumed.

## 8. Report shape that worked

Per layer, with the fields you held it to and the weights:

```
L1 Execution & Ingest    tool, actor, latency, in/out hash, session   ~75%
L2 Causal Trace DAG      parent_span_id, correlated trace_id            0%
L3 Token & Cost Econ.    prompt/completion/cache tokens, model, cost  ~0%
L4 Governance Decisions  verdict grammar, delta_s, next_safe_action   ~78% (weighted)
L5 Retrieval / RAG       retrieval span, doc ids, vector latency        0%
L6 Agentic Metabolism    FQ vector, hold/throttle events                0%
L7 Outcome Reality       task completion, goal closure                  0%
```

Then: state the weighting method inline, name the layers carrying the system, name
the empty ones, and order remediation as consumer -> no-DDL producer fix ->
view-based vocabulary split -> new columns last.

## Pitfalls

- **Do not diagnose from a stale twin.** Check the unit's `ExecStart` and
  `readlink -f` the deployed path before reading any worker source.
- **A declared port is not a deployment.** Verify with `ss -ltnp` or `curl` before
  reporting a surface as present or broken.
- **Do not quote a row count from any document, including this file.** Re-measure.
- **Check for a scheduled caller before diagnosing a dead writer.** If the only code
  path that advances a series is an HTTP handler, look for a timer. An irregular
  series (clustered then gappy) means manual invocation, not failure.
- **Keep the audit read-only.** Graphs and receipts are the deliverable; schema
  changes need separate authorisation.
