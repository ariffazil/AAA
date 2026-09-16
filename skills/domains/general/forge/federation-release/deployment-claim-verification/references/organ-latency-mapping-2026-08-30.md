# Organ Latency Mapping & Health Diagnostic Patterns
# Proven 2026-08-30 during APEX SWOT audit

## Organ Latency Baseline (verified 2026-08-30)

Establish expected latency for each organ to detect anomalies:

| Port | Service | Expected Latency | Notes |
|------|---------|-----------------|-------|
| 8088 | arifOS kernel | <10ms | Fastest organ — constitutional core |
| 4000 | FED/LiteLLM | <5ms | Proxy layer, no computation |
| 18085 | FRAME | <5ms | Independent observer, lightweight |
| 7071 | Hermes Gateway | <150ms | Node.js, session management |
| 7072 | A-FORGE MCP | <400ms | Node.js, 118 tools registered |
| 18082 | WEALTH | <150ms | Python, financial computation |
| 18083 | WELL | <200ms | Python, state classification |
| 8081 | GEOX | **2-4s** ❌ | Cascading HTTP calls in /health |

### Technique: Parallel Latency Probe
```bash
for port in 8088 7071 7072 4000 8081 18082 18083 18085; do
  t=$(curl -sf --max-time 3 -o /dev/null -w "%{time_total}" "http://localhost:$port/health" 2>/dev/null || echo "timeout")
  echo "  :$port = ${t}s"
done
```

### Interpreting Results
- **<100ms**: Healthy, no investigation needed
- **100-500ms**: Acceptable for compute-heavy organs
- **500ms-2s**: Investigate — may indicate expensive health checks or resource pressure
- **>2s**: Definite bottleneck — find root cause before it affects tool calls
- **timeout/conn-refused**: Service DOWN — auto-restart candidate

## GEOX Health Handler Cascading HTTP Calls (PROVEN 2026-08-30)

**Symptom**: GEOX /health endpoint takes 2-4s despite being a simple health check.

**Root cause**: GEOX /health does cascading HTTP calls to arifOS (:8088) for:
1. Apex scalars (G, C_dark, W3, h, QDF)
2. Deployment drift verification (source_commit vs built_commit vs deployed_commit)
3. Federation geometry (subjects, ledger_events, witness_oracle)

Each cross-service call adds ~500ms-1s latency. The health response is also massive (2KB+ JSON).

**Fix**: Split GEOX /health into:
- `/health` — lightweight: status, version, tools_loaded, git_commit only (<100ms target)
- `/diagnostics` — heavy: apex scalars, drift, geometry (for on-demand audit)

**Current status**: Requires GEOX source code change. Not yet implemented.

## DEGRADED vs DOWN Decision Matrix (PROVEN 2026-08-30)

When a health sentinel detects a non-healthy organ, classify BEFORE restarting:

| HTTP Response | Health Status | Classification | Action |
|--------------|---------------|----------------|--------|
| 200 + "healthy"/"ok" | HEALTHY | No action | Log only |
| 200 + "degraded" | DEGRADED | Data freshness issue | DO NOT restart — fix data |
| 200 + "stale"/"expired" | DEGRADED | State too old | Inject fresh data |
| Connection refused | DOWN | Service crashed | Auto-restart |
| Timeout (>5s) | UNREACHABLE | Service hung | Auto-restart, then investigate |
| HTTP 401/403 | HEALTHY (auth-gated) | Service up, auth required | No action |

### Key Insight
"degraded" means the SERVICE is running correctly but its INPUT DATA is stale or insufficient. Restarting a degraded organ wastes resources and doesn't fix the root cause. The organ is telling the truth — listen to it.

### WELL-Specific Pattern
WELL (18083) reports "degraded" when:
- state.json contains mock/test data (environment: "TEST")
- state.json is older than 12h (freshness band: AGED or STALE)
- No biometric data has been injected

This is CORRECT behavior per F9 anti-hantu. The organ refuses to fabricate body readiness.

## Carry-Forward Seal Bridge Pattern (PROVEN 2026-08-30)

**Problem**: carry_forward.json had empty recent_seals[] despite vault999 seal_chain_head at seq 45.

**Root cause**: The seal chain writes to vault999/seal_chain.jsonl but carry_forward.json (the inter-session memory bridge) doesn't automatically sync recent seals.

**Fix**: On session end or periodically, sync last 5 entries from seal_chain.jsonl into carry_forward.json recent_seals[]:

```python
import json
from datetime import datetime

with open("/root/.local/share/arifos/carry_forward.json") as f:
    cf = json.load(f)

seals = []
with open("/root/.local/share/arifos/vault999/seal_chain.jsonl") as f:
    for line in f.readlines()[-5:]:
        entry = json.loads(line.strip())
        seals.append({
            "seq": entry.get("seq", entry.get("sequence", "?")),
            "actor": entry.get("actor", "unknown"),
            "verdict": entry.get("verdict", "?"),
            "timestamp": entry.get("timestamp", entry.get("ts", "?")),
            "source": "seal_chain.jsonl"
        })

cf["recent_seals"] = seals
cf["recent_seals_synced_at"] = datetime.utcnow().isoformat() + "Z"

with open("/root/.local/share/arifos/carry_forward.json", "w") as f:
    json.dump(cf, f, indent=2, default=str)
```

## MCP Config Pruning Pattern (PROVEN 2026-08-30)

**Problem**: 6 disabled MCP servers cluttering config.yaml (42.9% of MCP entries were dead weight).

**Fix**: Archive disabled MCPs to cold storage, keep only active ones in config:

```python
import yaml

with open("/root/.hermes/config.yaml") as f:
    config = yaml.safe_load(f)

disabled = {k: v for k, v in config.get("mcp_servers", {}).items() if v.get("enabled") is False}
active = {k: v for k, v in config.get("mcp_servers", {}).items() if v.get("enabled") is not False}

# Archive disabled
with open("/root/.hermes/mcp_archive.yaml", "w") as f:
    yaml.dump(disabled, f, default_flow_style=False)

# Update config
config["mcp_servers"] = active
with open("/root/.hermes/config.yaml", "w") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

**Result**: 15 → 9 active MCPs. Config validated as correct YAML.
