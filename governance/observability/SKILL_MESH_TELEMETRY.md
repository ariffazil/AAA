# SKILL_MESH_TELEMETRY.md — Invocation Counter + Dead Skill Detection

> **Forged:** 2026-08-10 by 333-AGI under 888-APEX observability audit
> **Target:** `/root/AAA/skills/` — 204 skills, zero observability
> **Pattern:** Two-tier registry with automatic pruning signals

## Problem

204 skills in `/root/.agents/skills/`. No agent knows:
- Which skills are loaded (live)
- Which are invoked (hot)
- Which fail (dead)
- Which sit unused for months (cold)

Without this, 204 skills = 204 cognitive tokens wasted on every context load.

## Solution: skill_telemetry.jsonl

Append-only telemetry at `/root/AAA/state/skill_telemetry.jsonl`:

```
{"skill_id":"hermes-gateway-image-routing","event":"load","timestamp":"2026-08-10T03:10:00Z","agent":"333-AGI","session":"SEAL-915ca"}
{"skill_id":"token-plan-image","event":"invoke","timestamp":"2026-08-10T03:12:00Z","agent":"333-AGI","latency_ms":8500,"error":null}
{"skill_id":"token-plan-image","event":"invoke","timestamp":"2026-08-10T03:14:00Z","agent":"333-AGI","latency_ms":12000,"error":"quota_exhausted"}
{"skill_id":"nonexistent-skill","event":"fail","timestamp":"2026-08-10T03:20:00Z","agent":"Hermes","error":"not_found"}
```

## Event Types

| Event | Meaning | Triggers |
|-------|---------|----------|
| `load` | Skill loaded into agent context | Agent init, explicit `skill()` call |
| `invoke` | Skill's workflow executed | Tool call matching skill trigger |
| `fail` | Skill invocation failed | Schema mismatch, error, timeout |
| `prune_signal` | Skill flagged for review | N cycles without invoke |

## Tier Classification (Auto-Computed Weekly)

```
HOT   → invoked ≥ 5 times in last 7 days
WARM  → invoked 1-4 times in last 7 days
COLD  → loaded but 0 invocations in 7 days
DEAD  → 0 invocations in 30 days OR fail_rate > 50%
GHOST → loaded but never invoked (ever)
```

## Auto-Prune Triggers

| Condition | Signal | Action |
|-----------|--------|--------|
| DEAD for 60 days | `prune_signal` | Remove from auto-load, move to cold storage |
| GHOST for 90 days | `prune_signal` | Archive to `/root/AAA/skills/_retired/` |
| fail_rate > 80% | `HOLD` | Flag for 888-APEX review |

## Implementation: Telemetry Shim

```bash
# /root/AAA/scripts/skill-telemetry.sh
# Wraps skill loading. Called by agent boot scripts.
# Usage: skill-telemetry.sh "skill_id" "event" ["error_msg"]

SKILL_ID="$1"
EVENT="$2"
ERROR="${3:-null}"
AGENT="${AAA_AGENT_ID:-unknown}"
SESSION="${ARIF_SESSION_ID:-unknown}"

echo "{\"skill_id\":\"$SKILL_ID\",\"event\":\"$EVENT\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"agent\":\"$AGENT\",\"session\":\"$SESSION\",\"error\":$ERROR}" \
  >> /root/AAA/state/skill_telemetry.jsonl
```

## Query Examples

```sql
-- Hot skills (last 7 days)
SELECT skill_id, COUNT(*) as invocations 
FROM skill_telemetry 
WHERE event='invoke' AND timestamp > datetime('now','-7 days')
GROUP BY skill_id ORDER BY invocations DESC;

-- Ghost skills (never invoked)
SELECT DISTINCT skill_id FROM skill_telemetry WHERE event='load'
EXCEPT
SELECT DISTINCT skill_id FROM skill_telemetry WHERE event='invoke';

-- Dead skills (high failure rate)
SELECT skill_id, 
  COUNT(CASE WHEN event='fail' THEN 1 END) * 1.0 / COUNT(*) as fail_rate
FROM skill_telemetry WHERE event IN ('invoke','fail')
GROUP BY skill_id HAVING fail_rate > 0.5;
```

---

*DITEMPA BUKAN DIBERI — skills earn their place or face metabolism.*
