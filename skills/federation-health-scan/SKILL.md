# Federation Health Scan — OpenClaw P0 Skill

## Purpose
Single-command structured health scan of the entire arifOS federation: all organs, NATS streams, runtime drift, vault staleness. Returns a machine-readable JSON verdict.

## Usage
Invoke via OpenClaw as: run the health scan script.
The skill executes `federation_health_scan.py` and returns structured JSON.

## Output Schema
```json
{
  "organs": {
    "arifOS":    {"status": "OK|WARN|DOWN", "latency_ms": int, "drift": bool, "tools": int},
    "GEOX":      {"status": "OK|WARN|DOWN", "latency_ms": int},
    "WEALTH":    {"status": "OK|WARN|DOWN", "latency_ms": int},
    "WELL":      {"status": "OK|WARN|DOWN", "latency_ms": int},
    "A-FORGE":   {"status": "OK|WARN|DOWN", "latency_ms": int},
    "AAA":       {"status": "OK|WARN|DOWN", "latency_ms": int, "note": str}
  },
  "nats": {
    "server": "OK|DOWN",
    "streams": {
      "arifos-governance": {"messages": int, "last_msg_sec_ago": int},
      "arifos-organs":     {"messages": int, "last_msg_sec_ago": int},
      "agent_memory":      {"messages": int, "last_msg_sec_ago": int}
    }
  },
  "drift": {
    "status": "OK|DRIFTING",
    "build_commit": str,
    "live_commit": str,
    "detail": str
  },
  "vault": {
    "status": "OK|STALE|DOWN",
    "last_seal_sec_ago": int,
    "sealed_count": int
  },
  "summary": "OK|WARN|CRITICAL",
  "recommendation": str,
  "timestamp_utc": str,
  "scan_duration_ms": int
}
```

## Thresholds
- Organ WARN: latency > 2000ms or health endpoint returns non-"healthy"
- Organ DOWN: connection refused or timeout
- NATS WARN: last message > 5 min ago
- Vault STALE: last seal > 24h ago or SEALED_EVENTS.jsonl empty
- Summary WARN: any organ/stream yellow
- Summary CRITICAL: any organ/stream red

## Reversibility
Read-only. No mutations. Safe to run at any time.

## F2 Note
This skill reads from live endpoints at runtime. Results are OBS not INT.
