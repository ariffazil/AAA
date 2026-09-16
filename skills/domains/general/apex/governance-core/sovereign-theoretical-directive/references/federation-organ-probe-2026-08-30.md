# Federation Organ Probe Reference

Collected: 2026-08-30 during 4-Phase Hardening Protocol.

## Port-to-Service Map (af-forge VPS)

Verified via `ss -tlnp` and health endpoint responses.

| Port | Service | Process | Expected latency |
|------|---------|---------|-----------------|
| :8088 | arifOS Kernel | python | <5ms |
| :4000 | FED/LiteLLM | haproxy->litellm :4011 | <5ms |
| :18085 | FRAME (observer) | python | <5ms |
| :7071 | Hermes Gateway | node (pid=1252) | <110ms |
| :7072 | A-FORGE MCP | node | <400ms |
| :18082 | WEALTH | python3 | <120ms |
| :18083 | WELL | python3 | <600ms (data-dep) |
| :8081 | GEOX | python3 | 2-4s (cross-service) |
| :18100 | MiniMax Media | python3 | <200ms |
| :9120 | Hermes Serve | hermes | <10ms |

## Diagnosis Patterns

### WELL "degraded" (2026-08-30)

- Service is UP (systemd active, 200 OK in logs)
- Root cause: state.json is a MOCK/TEST fixture from April 2026
- Freshness calculation: age_hours=2921 > 72h threshold -> STALE
- truth_status: INSUFFICIENT_DATA (correctly refusing to fabricate)
- Fix: inject real biometric data (requires human action)
- DO NOT restart service to fix degraded status

### GEOX slow /health (2026-08-30)

- Latency: 2.0-4.4s (vs <100ms for other organs)
- Root cause: health handler does cascading HTTP calls to arifOS for
  apex scalars, deployment drift, federation geometry
- Each health check triggers 3+ cross-service HTTP calls
- Fix requires GEOX code change: split lightweight /health from heavy /diagnostics
- Service itself is healthy; the health check is expensive

### A-FORGE latency (corrected from SWOT)

- Original SWOT claimed 1.5s — INCORRECT
- Actual: 96-398ms on port 7072 (A-FORGE MCP)
- Port 8081 (GEOX) was misidentified as A-FORGE in the SWOT
- A-FORGE is NOT the bottleneck

### carry_forward.json seal bridge gap

- recent_seals was empty despite vault999 at seq 45
- Fix: sync last 5 entries from seal_chain.jsonl to recent_seals[]
- Backup before modifying: carry_forward_backup_YYYYMMDD_HHMMSS.json

### MCP config pruning

- 6 disabled MCPs (social-mcp, gemini-media, osm, firecrawl, mage, minimax)
- Archived to /root/.hermes/mcp_archive.yaml
- Active MCPs retained: aforge, arifos, fed, geox, mapbox, composio,
  minimax-media, wealth, well (9 total)
- Config YAML validated after pruning

## Probe Command

```bash
for port in 8088 4000 18085 7071 7072 18082 18083 8081 18100 9120; do
  t=$(curl -sf --max-time 3 -o /dev/null -w "%{time_total}" \
    "http://localhost:$port/health" 2>/dev/null || echo "timeout")
  echo "  :$port = ${t}s"
done
```

## Heartbeat Daemon

The organ_heartbeat_daemon.py runs as arifos user and probes each organ.
It determines degraded status from the health response JSON, not from
HTTP status code. HTTP 200 with "degraded" in JSON = organ is running
but reporting data quality issues.
