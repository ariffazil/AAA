# D3 DECISION — otelcol ELEVATED as single OTLP gateway
> Status: DRAFT_2026-09-15 — lane work, awaiting F13 review (housekeeping consolidation)

**Date:** 2026-09-15
**Decided by:** Trinity consensus (333-AGI + 555-ASI + 888-APEX) under standing F13 delegation from Arif Fazil ("decide agentically agi asi apex", 2026-09-15)
**Supersedes:** open_loop e-d56ce74f (carry_forward gen-1789411108-1f7dff)

## Decision

**ELEVATE** — otelcol-contrib becomes the federation's single OTLP gateway. Organs export to the collector; the collector is the one trusted pipe into storage.

## Grounding (probed 2026-09-15)

- `otelcol-contrib` live at PID 1150953, config `/root/forge_work/kabarkan/kabarkan-collector.yaml`
- Listening: `*:4318` (OTLP HTTP) — UP
- Note: a second listener on `127.0.0.1:4317` (OTLP gRPC) is held by `otel-plugin` PID 2218081 (Netdata's plugin) — NOT the Kabarkan collector. Two processes touch the OTLP ports; consolidation should account for this.

## Rationale (plain)

One trusted pipe is easier to watch than nine separate pipes. The collector has already proven itself — it delivered the 202k-row telemetry treasure now visible in Grafana. In-process capture per organ would mean 9 copies of the same failure surface, 9 configs to audit, 9 things to restart. Elevate = fewer moving parts, single audit point, consistent enrichment. Reversible: any organ can re-enable in-process export if the collector misbehaves.

## Conditions

1. Per the F6 rule (same day): the collector is OBSERVE+TRANSPORT infrastructure. If it ever triggers a state-changing alert, that alert routes through `arif_judge` like any other.
2. Port 4317 conflict (Netdata otel-plugin vs collector) to be resolved in a follow-up — one owner per port.
3. Rollback: revert per-organ exporters to in-process; no data loss (storage side unaffected).

## Residual work (queued, not blocking)

- [ ] Resolve 4317 dual-owner (Netdata otel-plugin vs kabarkan collector)
- [ ] Confirm all organs actually point at :4318 (inventoried per-organ exporter config)
- [ ] Collector health surfaced on the Grafana observability dashboard
