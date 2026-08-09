<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# 🏛️ AAA — Protocol Conformance

> **Layer:** L1 ROOT · **Role:** Control Plane / A2A Gateway
> **Protocols:** A2A Server, MCP Consumer, NATS

## Supported Protocols

| Protocol | Status | Detail |
|----------|--------|--------|
| A2A Server | ✅ CONFORMANT | Agent cards, task state, gateway on :3001 |
| MCP Consumer | ✅ CONFORMANT | Reads tools from all federation organs |
| NATS | ✅ CONFORMANT | 888_HOLD alarm routing, event bus |
| OpenTelemetry | ⚠️ PARTIAL | Prometheus + Grafana, no OTel SDK |

## Agent Cards
- 22 agents indexed in AGENT_INDEX.json
- 5 warga: 333-AGI, 555-ASI, 888-APEX, A-AUDIT (collapsed), A-ARCHIVE (collapsed)
- A2A agent card schema compliance: PARTIAL

## Gaps
1. **OpenTelemetry SDK:** Metrics are Prometheus-native, not OTel-compatible
2. **A2A Task Schema:** Task state model incomplete per A2A spec
3. **A2A Leases:** Lease lifecycle not fully A2A-compliant

*DITEMPA BUKAN DIBERI*
