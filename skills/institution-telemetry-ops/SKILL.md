---
name: institution-telemetry-ops
description: "Publish and read institutional telemetry (MAP·ATLAS·ECHO metrics) through Kabarkan/NATS in the arifOS federation. Covers the nats-CLI publish pattern (worker is async-only), the observability.observations Postgres schema, and the stale-PG-connection pitfall where the Kabarkan worker NAKs every message until restarted. Use when wiring metrics to Kabarkan, debugging 'Store failed: connection is closed', or computing MAP/ATLAS/ECHO readings."
version: 1.0.0
tags: [kabarkan, nats, telemetry, metrics, map, atlas, echo, arifflow, observability]
---

# Institution Telemetry Ops (Kabarkan / NATS)

The federation's telemetry backbone: arifFlow (`:7073`, the pulse/FQ) + Kabarkan (the ear) + MAP·ATLAS·ECHO (the brain). Loop:

```
Reality → Kabarkan (NATS JetStream) → Worker → PG/S3
              ↑                                   ↓
        ATLAS333 hook                    MAP·ATLAS·ECHO (tension weights only)
```

## Roles (confirmed 2026-08-09)

- **Kabarkan** = ear — subscribes `kabarkan.ingest.>` on stream `kabarkan-ingest`
- **MAP·ATLAS·ECHO** = brain — tension weights only, never auto-mutate geometry
- **ATLAS333** = geometry — 35 paradoxes
- **arifFlow** = pulse — FQ verdict

## Publish pattern (sync, via nats CLI)

`nats-py` v2 is async-only, so the kernel telemetry publishes via subprocess `nats` CLI — fire-and-forget:

```bash
nats publish kabarkan.ingest.metrics '{"observation_id":"...","trace_id":"...","span_id":"...","session_id":"...","actor_id":"hermes","tool_name":"institution_metrics","organ_id":"arifflow","verdict_class":"METRICS_READING","metadata":{"metrics":{...}}}'
```

Reusable publisher: `/root/HERMES/scripts/kabarkan-publish.py` — CONSUMES the canonical
state (runs `/root/scripts/map-atlas-echo.py --write` → reads `/root/AAA/state/map_atlas_echo.json`),
never recomputes in parallel. Cron: `institution-metrics-pulse` every 6h.

**CANONICAL COMPUTATION (single source of truth):**
```bash
/root/scripts/map-atlas-echo.py --write   # → /root/AAA/state/map_atlas_echo.json
/root/scripts/map-atlas-echo.py --json    # machine output
map-atlas-echo --write                    # installed at /root/.local/bin
```
Do NOT build a parallel calculator — a duplicate lib adds tool surface and lowers MAP
(thrash law). The session's earlier `institution-metrics.py` + `institution_metrics_lib.py`
were REMOVED as duplicate surface; kabarkan-publish.py reads the canonical JSON instead.

## Worker → Postgres schema

`observability.observations` (DB `vault999`, user `arifos_admin`, docker PG on `127.0.0.1:5432`). Key fields: `id, trace_id, span_id, parent_span_id, session_id, actor_id, tool_name, organ_id, verdict_class, delta_s, reasons(jsonb), uncertainty_tag, input_hash, output_hash, vault_receipt, cost_usd, model_name, latency_ms, start_time, end_time, metadata(jsonb), created_at`. `ON CONFLICT (id) DO NOTHING`.

Verify a reading landed:

```bash
PGPASSWORD="$(grep POSTGRES_PASSWORD /root/.secrets/kunci-mas.flat.env | cut -d= -f2)" \
  psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -c "SELECT session_id, tool_name, metadata->'metrics'->'MAP'->>'score' as map FROM observability.observations WHERE tool_name='institution_metrics' ORDER BY created_at DESC LIMIT 3;"
```

## Pitfalls

- **Stale PG connection = silent data loss.** The worker connects once at startup; if the docker PG restarts or the pool idles out, the worker logs `Store failed: connection is closed` and NAKs EVERY message — stream grows, PG stays stale. Symptoms: `journalctl -u kabarkan-worker.service | grep "Store failed"` + stream message count rising while PG count is flat. Fix: `systemctl restart kabarkan-worker.service` → log shows `Kabarkan Worker v1 connected — NATS=... PG=...`. This is EAR REPAIR (observation infra), not coupling — allowed under the Institutional Zen Freeze.
- **Backlog of invalid-JSON messages.** After a worker restart, a fresh consumer replays old non-JSON messages → `WARNING: Nak msg NNN: invalid JSON`. Harmless noise; it drains and the new consumer starts from the tail. Don't chase it.
- **Publish is fire-and-forget.** The nats CLI subprocess swallows errors — a failed publish returns success with no trace. Verify by querying PG (above), not by trusting the publish exit code.
- **Freeze discipline (2026-08-09 ruling):** observe MAP/ATLAS/ECHO into PG over an observation window (≥4-5 readings / ~24-30h) BEFORE giving telemetry power to alter geometry. Collect noise floor first; coupling before calibration = feedback oscillation. Receipt: `/root/forge_work/2026-08-09/INSTITUTIONAL-ZEN-FREEZE.md`, doctrine `/root/AAA/governance/HERMES_DNA.md`.

## Metric definitions (MAP·ATLAS·ECHO) — canonical formulas

Canonical source: `/root/scripts/map-atlas-echo.py` (reads VAULT999 outcomes.jsonl window,
GATE_FIRE ledger, RSI ledger, failed_trajectories, live organ probes). Bands are DER.

- **MAP** = `reality_contact / (unique_tools_window / holy8)` — reality contact over tool
  thrash. `reality_contact` = healthy organs / 8 core organs (degraded counts as contact).
  **Thrash law:** unique_tools=27 vs holy8=8 → thrash 3.375 → MAP 0.296 (LOW). Raising MAP =
  reducing tool surface back to the Holy 8 verbs — consolidation, not more prompts.
- **ATLAS** = `(tools_exposed * reality_contact) / 13_floors` — governed capability leverage.
  ATLAS metric ≠ ATLAS333 organ (35-paradox geometry).
- **ECHO** = `retained_improvements / honest_observations` — honest observations =
  gate HOLD/VOID/DENY + RSI_DIAGNOSE + failed_trajectories + vault_anomaly_tags (capped)
  + organ_downs. HO==0 → ECHO null (BLIND), never 0/0=perfect.
- **HERMES** = `geometric_mean(MAP, ATLAS, ECHO)` — institution density, NOT agent IQ.
- SCAR = human-strand twin of ECHO (H5 registry, `scar:<id>` gate, sovereign only).

**DARK_MIRROR danger posture:** `MAP_LOW_ATLAS_HIGH` (e.g. MAP 0.296 LOW + ATLAS 0.615 HIGH)
= understanding weak while governance power strong → coherent scale-of-error risk (super-scaled
stupidity). Directive when flagged: **kurangkan thrash / naik MAP sebelum expand ATLAS** — do NOT
add tools/capabilities while MAP is low. State file: `/root/AAA/state/map_atlas_echo.json`
(`danger_posture` field). Note: trust score (who enters / what's allowed) is a DIFFERENT layer
from APEX thermo / MAP·ATLAS·ECHO — keep them separate and honest.

Live reading (2026-08-09 baseline): MAP=0.296 LOW · ATLAS=0.615 HIGH · ECHO=0.247 MID · HERMES=0.356 MID · posture MAP_LOW_ATLAS_HIGH.
