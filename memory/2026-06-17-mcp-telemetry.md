# Memory — MCP Telemetry Proxy (2026-06-17)

## What happened
Arif asked for global MCP telemetry — tagging every MCP call from every agent (Hermes, OPENCLAW, opencode, Kimi, Claude, Agy) with agent identity and session data.

Built: `/root/arifOS/core/mcp_telemetry/proxy.py` — MCP Telemetry Proxy v3.

## What it does
- Transparent HTTP intercept layer on port 8092
- Routes: POST /mcp/arifos → arifOS MCP (:8088), POST /mcp/A-FORGE → A-FORGE (:7071)
- Non-blocking asyncio server + thread-pool for upstream calls (never stalls gateway)
- Session mapper: scans gateway JSON log every 5s, maps sessionId → agent name
- Every MCP call → writes structured record to `/root/arifOS/core/mcp_telemetry/calls.jsonl`
- In-memory counters: per-server, per-agent, per-tool, error rates
- Endpoints: GET /health /stats /agents /sessions /ledger

## What was wired
- `/root/.openclaw/openclaw.json`: arifos and A-FORGE URLs changed from direct `:8088/:7071` to proxy `127.0.0.1:8092/mcp/arifos` etc.
- Backup: `/root/.openclaw/openclaw.json.bak4proxy`
- Gateway restarted — routes all arifos + A-FORGE MCP calls through proxy automatically

## Systemd service
- Unit: `/etc/systemd/system/mcp-telemetry-proxy.service`
- Enabled, active (PID 2229581)
- Survives reboot

## Key design decision (Arif confirmed)
- Start with VISIBILITY, not enforcement
- Collect 24-48h of real call data before designing any forcing functions
- Light forcing: "your uncertainty label will be wrong if you skip the witness" — not hard gates
- Tool ≠ useless if unused; data tells us where gaps are

## Next steps (Arif to decide)
- Add more MCP servers to proxy routing (WEALTH, WELL, GEOX) once arifos + A-FORGE confirmed working
- Review /ledger endpoint for live call data once agents start making calls
- Design complexity threshold for sequential-thinking forcing based on actual call distributions
- Prometheus metrics layer later for Grafana dashboards

## Files
- `/root/arifOS/core/mcp_telemetry/proxy.py` — proxy v3 (16KB, pure stdlib)
- `/root/arifOS/core/mcp_telemetry/calls.jsonl` — call ledger (2 records so far)
- `/root/arifOS/core/mcp_telemetry/proxy.log` — proxy log
- `/root/.openclaw/openclaw.json.bak4proxy` — pre-change config
