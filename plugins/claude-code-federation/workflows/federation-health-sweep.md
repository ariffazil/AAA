#!/usr/bin/env python3
"""
DYNAMIC WORKFLOW — Federation Health Sweep
===========================================
Claude Code Workflow: probes all 7 organs + kernel, reports health,
flags degradation, computes FQ pulse, and returns a structured report.

Use Claude Code's Workflow tool to execute:
  "Run the federation-health-sweep workflow"

This script is a Claude Code Workflow definition. Claude Code will
execute it as a JS orchestration script, spawning up to 7 parallel
subagents for organ probing and synthesizing results.

Part of the arifos-federation Claude Code plugin.
DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

# This is a REFERENCE DOCUMENT — the actual workflow is invoked
# through Claude Code's Workflow tool. It describes the probe
# pattern and expected output schema.

WORKFLOW_DESCRIPTION = """
## Federation Health Sweep

Probes all arifOS federation organs and returns a structured health report.

### Organs to probe
| Organ | Port | URL |
|-------|------|-----|
| arifOS | 8088 | http://127.0.0.1:8088/health |
| A-FORGE | 7071 | http://127.0.0.1:7071/health |
| arifFlow | 7073 | http://127.0.0.1:7073/health |
| AAA | 3001 | http://127.0.0.1:3001/health |
| GEOX | 8081 | http://127.0.0.1:8081/health |
| WEALTH | 18082 | http://127.0.0.1:18082/health |
| WELL | 18083 | http://127.0.0.1:18083/health |

### Output Schema
```json
{
  "timestamp": "ISO8601",
  "fq": {"quotient": float, "verdict": "string"},
  "organs": {
    "organ_name": {
      "status": "alive" | "degraded" | "DOWN",
      "latency_ms": int,
      "details": {}
    }
  },
  "kernel": {
    "verdict": "SEAL|HOLD|...",
    "floors_active": int,
    "drift": bool,
    "vault999_health": "string"
  },
  "summary": {
    "total": int,
    "alive": int,
    "degraded": int,
    "down": int,
    "verdict": "HEALTHY|DEGRADED|CRITICAL"
  },
  "recommendations": ["string"]
}
```

### Execution
Launch up to 7 parallel subagents (one per organ) using curl probes.
Collect results. Synthesize into report. Return structured JSON.

### Thresholds
- ≥6 alive + FQ ≥ 0.5 → HEALTHY
- 4-5 alive or FQ < 0.5 → DEGRADED (agents limit mutation)
- <4 alive or FQ < 0.3 → CRITICAL (888_HOLD all non-essential work)
"""
