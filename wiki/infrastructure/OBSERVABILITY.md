# Observability Stack

> **CLAIM** | Source: `observability/` directory + `docker-compose.yml` | **Confidence:** 0.95 | **Epoch:** 2026-04-23

## Summary

arifOS's observability stack uses Prometheus (metrics) + Grafana (visualization) + Nine-Signal alerting rules. All monitoring ports bound to `127.0.0.1` only — no public exposure.

---

## Components

### Prometheus (`:9090`)
- Scrapes 4 targets every 15–30s
- Hot-reload enabled via `prometheus.yml`
- 14 alerting rules from `nine_signal_alerts.yml`

### Grafana (`:3000`)
- Dashboard: `nine_signal_overview.json`
- UID: `arifOS-nine-signal`
- Auto-refresh: 15s
- Timezone: Asia/Kuala_Lumpur

### Alertmanager
- Routes alerts via Nine-Signal rules
- Labels: `observability_layer: prometheus-observability-only`

---

## Scrape Targets

| Target | Endpoint | Interval | Labels |
|--------|----------|----------|--------|
| arifOS-MCP | `http://localhost:8080/metrics/json` | 15s | `observability_layer: prometheus-observability-only` |
| arifOS-API | `http://localhost:8000/api/status` | 30s | `observability_layer: prometheus-observability-only` |
| GEOX | `http://localhost:8081/metrics` | 30s | `observability_layer: prometheus-observability-only` |
| OpenClaw | `localhost:18789/metrics` | 30s | `observability_layer: prometheus-observability-only` |

---

## Nine-Signal Alert Rules (14 total)

From `observability/prometheus/nine_signal_alerts.yml`:

1. **NineSignalDelta** — entropy change out of range
2. **NineSignalOmegaHigh** — overconfidence (Ω > 0.97)
3. **NineSignalOmegaLow** — false certainty (Ω < 0.10) ⚠️ F9 Anti-Hantu
4. **NineSignalFalseCertainty** — omega suspiciously low
5. **NineSignalPsi** — grounding below threshold
6. **NineSignalKappaR** — resilience below threshold
7. **NineSignalFloorDrift** — floor deviation > 2
8. **NineSignalPlaneDrift** — spatial/geo deviation
9. **NineSignalF3Consensus** — tri-witness consensus < 0.50
10. **NineSignalF9AntiHantu** — manipulation potential > 0.80
11. **NineSignalPrometheusPipeline** — Prometheus scraping failing
12. **NineSignalArifOSAPIDown** — API target down
13. **NineSignalGEOXDown** — GEOX target down
14. **NineSignalOpenClawDown** — OpenClaw target down

---

## Deployment

```bash
docker-compose up -d prometheus grafana
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000 (admin/admin)
```

---

## Cross-References

- [[nine-signal/OVERVIEW]] — Nine-Signal metric definitions
- [[nine-signal/WATCHDOG]] — watchdog heartbeat cron

---

## Status

**Stable** — Prometheus + Grafana stack deployed and scraping.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE