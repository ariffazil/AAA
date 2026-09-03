# VAULT999 List Response Parsing

**Problem:** `arif_vault_seal(mode=list)` returns a nested JSON structure that requires double-deserialization.

**Pattern:**
```python
import json

# Raw response is a JSON string containing another JSON string
outer = json.loads(raw_response)
result_str = outer["result"]          # This is a JSON STRING, not a dict
inner = json.loads(result_str)        # Parse it again to get the actual payload
entries = inner["result"]["entries"] # Now access the data
```

**Why:** The MCP tool wraps its JSON payload inside another JSON envelope, and the inner payload is serialized as a string field (not a nested object). This is a known pattern in FastMCP response serialization.

**Fields in vault list entries:**
| Field | Notes |
|-------|-------|
| `ts` | ISO timestamp — most entries have this |
| `timestamp` | Some entry types use this instead (heartbeats) |
| `actor` | Who wrote the entry — `hermes-shell-hook`, `hermes-agent`, `hermes-asi`, `Kimi`, etc. |
| `action` | What tool/action — `terminal`, `read_file`, `patch`, `write_file`, `web_search`, etc. |
| `outcome` | `unknown`, `pending`, `failure` — 98%+ are `unknown` |
| `session_id` | Session identifier — can be `"unknown"` for rogue/misconfigured runs |
| `params_sha256` | Hash of parameters — not reversible |

**Entry types:**
- **Shell entries** (`actor: hermes-shell-hook`) — every terminal() call logged. High volume.
- **Agent entries** (`actor: hermes-agent` or `hermes-asi`) — direct tool calls
- **LGR decision entries** — `decision_id: LGR-...` format, calibration test artifacts, NOT real verdicts
- **Heartbeats** — `type: heartbeat`, use `timestamp` not `ts`

**Common analysis patterns:**
```python
# Filter by actor
actor_counts = Counter(e.get("actor","?") for e in entries)

# Filter by action
action_counts = Counter(e.get("action","?") for e in entries)

# Filter by outcome
failures = [e for e in entries if e.get("outcome") == "failure"]

# Date range from entries with ts
ts_entries = [e for e in entries if e.get("ts")]
date_range = (min(e['ts'] for e in ts_entries), max(e['ts'] for e in ts_entries))

# Monthly breakdown
monthly = defaultdict(int)
for e in entries:
    ts = e.get("ts") or e.get("timestamp","")
    if ts:
        monthly[ts[:7]] += 1
```

**Known quirks:**
- 409 entries show `actor: "?"` — these are LGR test entries (no actor field) + mixed edge cases
- Latest entry may be days old — check if recent events are being flushed or if there's a write gap
- 98% outcome="unknown" means the vault logs actions but not results — audit use is limited without outcome tracking