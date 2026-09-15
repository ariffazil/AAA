# Kabarkan / FRAME — Capability & Dependency Map (Phase 2)
> **Author:** Hermes ASI (i-arif) · 2026-09-15 · read-only audit, no mutation
> **Method:** live probes on KVM8 with primary evidence. Every edge below is
> measured, not read from doctrine. Stale-copy traps explicitly flagged.
> **Scope:** what ACTUALLY flows into the Kabarkan observability plane, and what does not.

---

## 0. Reality Reconciliation — stale copies found

Three artifacts in the federation have a live twin elsewhere. Debugging the stale
copy produces false bug reports (this happened twice in one session).

| Declared path | Actually live | Status |
|---|---|---|
| `/root/FRAME/src/frame_organ/` | `/root/AAA/federation/frame/src/frame_organ/` (symlinked at `/opt/frame/app`) | **stale sibling** — still lists retired `flame:18901`; live code removed it with a dated comment |
| `/root/A-FORGE/kabarkan/worker.py` (17,084 B, 24 Jul) | `/root/arifOS/arifosmcp/runtime/observability/worker.py` (9,895 B, 12 Sep) | **dead code** — service ExecStart runs the arifOS module |
| `/root/A-FORGE/kabarkan/patch_telemetry.py` (12 Sep) | never applied | **dead patch** — no `_publish_to_nats` in any A-FORGE `telemetry.py` |

---

## 1. Verified data path (the only live ingest)

```
arifOS MCP runtime  (arifosmcp/runtime/telemetry.py)
        │  _get_nats() → publishes via `nats` CLI subprocess (sync bridge;
        │  nats-py v2 is async-only). Subject: kabarkan.ingest.<type>
        ▼
NATS JetStream  stream=kabarkan-ingest  subject=kabarkan.ingest.>
    193,122 msgs · last_ts 2026-09-15T05:37:03Z  (LIVE)
        ▼
consumer kabarkan-worker-fresh
    pending=0 · delivered=193,128 · ack=193,128   (HEALTHY, fully drained)
        ▼
kabarkan-worker.service
    ExecStart = /opt/arifos/venv/bin/python -m arifosmcp.runtime.observability.worker
    EnvironmentFile = /root/.secrets/vault.flat.env
        ▼
Postgres vault999 → schema observability.observations
    201,380 rows · 448/hr · 7,772/24h · newest span age < 5 min  (LIVE)
```

**Producers observed in the ledger** (`actor_id`): 333-AGI, f006-edge-probe,
openclaw-anon, ariffazil, opencode-e2e-probe, qwen-code, kimi-code/FI-008,
wealth-mcp, conformance-spine, selftest, grok-build, + others.
All 201,380 rows carry `organ_id = 'arifOS'` — **single-organ taxonomy**, no
per-organ attribution despite the platform being federation-wide.

---

## 2. Broken / dead edges

| Edge | Evidence | Verdict |
|---|---|---|
| A-FORGE → NATS | `_publish_to_nats` count = 0 in all A-FORGE `telemetry.py` | **never wired** — patch written, never applied |
| arifFlow → Kabarkan | `src/governance/kabarkan.rs` (`KabarkanTracer`) referenced only in `scheduler.rs`; scheduler is compiled-but-not-invoked from the daemon (per arifFlow AGENTS.md). No `arifflow` actor in `observations`. | **dead code** |
| FRAME → Kabarkan | `frame_organ/alert.py` posts drift to `SIGNAL_URL/kabarkan/broadcast` | **WRONG TARGET — name collision** (see §4) |
| otelcol → Kabarkan | `otelcol_process_uptime` = 13.2 d; zero `receiver_accepted`/`exporter_sent`; sole registered exporter `otlphttp/langfuse` | **decorative** — carried 0 traffic since boot |
| worker → MinIO cold storage | `_archive_to_s3()` docstring: *"Not yet implemented — requires aioboto3 or minio-py"* | **stub** — 90-day archive does not exist |
| `observations` → any reader | only `worker.py` + `postgres_backend.py` reference the table; Grafana datasources = Prometheus (:8088/metrics) + an Infinity datasource pointing at `http://169.254.169.254` (cloud metadata address, not a federation source); single dashboard = "arifOS Nine-Signal Overview" | **write-only ledger — nobody reads it** |

---

## 3. Stream saturation — silent data loss

```
stream arifos-organs   subjects=arifos.organ.>   Retention=Limits  Discard=Old
    messages = 29,327        bytes = 134,205,613   ← max_bytes = 134,217,728 (128 MiB)
    first_ts = 2026-09-11T01:41:19Z    last_ts = 2026-09-15T05:37:13Z
    consumers:
      probe          pending=29,327  delivered=0    ack=0     ← DEAD, never acked once
      verifier       pending=29,327  delivered=0    ack=0     ← DEAD, never acked once
      verifier-api   pending=29,327  delivered=900  ack=900
      verifier-probe pending=29,327  delivered=155  ack=155
```

- Stream is **at its byte ceiling** (99.99% of 128 MiB) with `discard_policy=old`:
  organ heartbeat/distress history is being **silently discarded**, oldest-first.
- No systemd unit matches `verifier` → the two zero-ack consumers are orphans.
- Publisher: `arifOS/scripts/organ_heartbeat_daemon.py` and
  `arifosmcp/abi/nats_heartbeat_daemon.py`.

---

## 4. Name collision: two different "kabarkan"

| Name | Location | Function |
|---|---|---|
| **Kabarkan** (observability plane) | NATS `kabarkan-ingest` → worker → `observability.observations` | telemetry ingest |
| **kabarkan** (notification broadcast) | SIGNAL :18084 `POST /kabarkan/broadcast` (returns 422 = exists, needs body) | priority-classified alert dispatch |

FRAME's drift escalation targets the SIGNAL endpoint, **not** the observability
plane. Any future "wire FRAME → Kabarkan" work must first disambiguate the name,
or it will silently wire into the notifier.

---

## 5. HTTP surface — CONTESTED claim, now settled by primary measurement

Probe: `curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:<port>/health`

| Port | Canonical organ | Measured |
|---|---|---|
| 8088 | arifOS kernel | 200 |
| 7071 | A-FORGE | 200 |
| 7072 | A-FORGE (secondary) | 200 |
| 8081 | GEOX | 200 |
| 7073 | arifFlow | 200 |
| 7074 | FED | 200 |
| 18082 | WEALTH | 200 |
| 18083 | WELL | 200 (status: degraded) |
| 18084 | SIGNAL | 200 |
| 18085 | FRAME | 200 |
| 3001 | AAA | 200 |
| **18081** | *(none)* | **no listener has ever existed** |

`18081` is the only "refused" in the contest, and it is a **phantom port** — the
FRAME claim attached to it was a port-map error. The "whole HTTP surface is down"
claim is **FALSIFIED**.

---

## 6. Phase 1 — completed (receipts)

| Item | Action | Receipt |
|---|---|---|
| Collector config | reconstructed from runtime observation + `otelcol validate` exit 0 | `/root/forge_work/kabarkan/kabarkan-collector.yaml` (1,575 B) |
| Credential hygiene | `BASE64_AUTH` moved out of world-readable unit file | `/root/.secrets/kabarkan-collector.env` (0600, 161 B); unit grep = 0 |
| FRAME heartbeat | `frame-probe.timer` installed (15 min) — `/frame/probe` is the only trend writer | trend 22 → 24 lines and growing |
| Triage delivery | `digest_inbox/` created, today's digest re-delivered | `.../digest_inbox/triage_latest.md` (3,326 B) |

All three services active: `kabarkan-collector`, `kabarkan-worker`, `frame-probe.timer`.

---

## 7. Phase 3 — NOT STARTED (mutation, awaiting F13)

Deferred by design: `parent_span_id` (0/201,380 populated), token/cost columns
(225/201,380), `organ_id` taxonomy normalisation, `verdict_class` grammar cleanup
(OK/COMPLETED/SUCCESS/METRICS_READING leak into a field meant for SEAL/HOLD/VOID).

*DITEMPA BUKAN DIBERI*
