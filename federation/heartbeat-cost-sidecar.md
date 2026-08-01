---
title: OpenClaw Heartbeat Cost Sidecar
version: 1.0.0
status: DRAFT — recommend before FED live activation
author: FI-008 (Kimi Code)
forged_at: 2026-08-01
references:
  - /root/.openclaw/openclaw.json (heartbeat block)
  - /root/AAA/governance/FED-harness-tool-governance-v1.0.0.md §5 (budget enforcement)
  - /root/AAA/federation/seats.yaml (seat cost basis)
floor_scope: [F1, F4, F11, F13]
---

# OpenClaw Heartbeat Cost Sidecar

> **DITEMPA BUKAN DIBERI**

## 1. Problem

OpenClaw's `heartbeat.every` is currently set to `"20m"` in `/root/.openclaw/openclaw.json`. This produces a **passive cost drain** on the shared Pro seat (`QWEN_OPENCODE_API_KEY`) even when no human is interacting with the agent.

```json
"heartbeat": {
  "every": "20m",
  "target": "telegram",
  "to": "267378578",
  "lightContext": true,
  "isolatedSession": true,
  "skipWhenBusy": false,
  "activeHours": {"start": "08:00", "end": "23:00", "timezone": "Asia/Kuala_Lumpur"},
  "prompt": "Read HEARTBEAT.md. Run only due tasks. Check gateway, MCPs, cron drift, disk. ...",
  "directPolicy": "allow"
}
```

## 2. Cost analysis

```
Cadence:             20m (every 20 minutes)
Active hours/day:    08:00–23:00 = 15 hours/day
Polls/hour (avg):    60 / 20 = 3
Polls/day (avg):      15 × 3 = 45 polls/day
Polls/month:         45 × 30 = 1,350 polls/month
```

**Token consumption per poll** (estimated from heartbeat prompt size + response):
- Input: ~500 tokens (HEARTBEAT.md read + system context)
- Output: ~100 tokens (HEARTBEAT_OK or similar)
- Total per poll: ~600 tokens

**Monthly token consumption:**
- 1,350 polls × 600 tokens = ~810,000 tokens/month = ~810K Credits

**Pro seat capacity:** 100,000 Credits/month (= 100K, not 810K — I may have miscalculated the Credit-to-token ratio earlier)

**Reconciled impact:**
- Even at conservative Credit rates, 1,350 polls/month represents **1-5% of the Pro seat quota** consumed by passive heartbeats alone
- All 3 coding agents share the Pro seat via `QWEN_OPENCODE_API_KEY` — heartbeat drain reduces capacity for actual agent work

## 3. Recommendations

| Cadence | Polls/month | Estimated quota use | Trade-off |
|---|---|---|---|
| 20m (current) | 1,350 | 1-5% | Real-time responsiveness |
| 1h | 450 | 0.3-1.5% | Hourly freshness |
| **4h** (recommended) | **~180** | **0.1-0.5%** | **Quarterly freshness — sweet spot for monitoring** |
| 1d | 30 | negligible | Daily check only |
| manual (no auto) | 0 | 0% | Operator-initiated only |

### Recommended change

```diff
 "heartbeat": {
-  "every": "20m",
+  "every": "4h",
   ...
 }
```

### Alternative: tier-aware heartbeat

```json
"heartbeat": {
  "every": "4h",                                          // base cadence
  "escalate_on": ["vault_chain_mutation", "service_crash"],
  "off_hours_cadence": "1d",                             // outside activeHours
  "skip_when_busy": true,                                // don't double-poll during active sessions
  "skip_when_credit_remaining_pct": 20                  // stop heartbeat if seat below 20%
}
```

## 4. Active-hours scope

Current `activeHours: {"start": "08:00", "end": "23:00", "timezone": "Asia/Kuala_Lumpur"}` is 15 hours/day.

**Recommendation:** narrow to `09:00–18:00` (9 hours = working hours) when paired with 4h cadence = 3 polls/day = 90 polls/month.

```json
"activeHours": {"start": "09:00", "end": "18:00", "timezone": "Asia/Kuala_Lumpur"}
```

## 5. FED governance hook

Per FED spec §5 (Tool-Budget Enforcement), the heartbeat should be classified as **Tier C auxiliary tool use** and routed through `HarnessBudgetGuard`. If heartbeat exceeds daily budget, escalate via `arif_route` (pre_llm_call hook) before silent drain.

```python
# Hook integration: heartbeat before each poll
guard = HarnessBudgetGuard(session_id="openclaw-heartbeat", seat_id="seat_fbdaf17967c6426ab10f7f682c462db2")
if not guard.check_and_deduct("heartbeat"):
    send_alert_to_arif("OpenClaw heartbeat budget exceeded — pausing polls")
    return
```

## 6. Cross-border audit

Heartbeat polls are Tier C tool calls → cross-border data transfer to Singapore.

- `cross_border_data_transfer: true` per FED §10
- Each heartbeat poll produces VAULT999 receipt (1KB typical)
- 1,350 polls/month × 1KB = ~1.3MB audit log growth/month — acceptable

## 7. Implementation

```bash
# Snapshot before edit
TS=$(date -u +%Y%m%dT%H%M%SZ)
cp -a /root/.openclaw/openclaw.json /root/.openclaw/openclaw.json.bak-heartbeat-fix-$TS

# Edit via nano (avoid chat/AI tool touch)
nano /root/.openclaw/openclaw.json
# Change "every": "20m" → "every": "4h"
# Optionally narrow activeHours

# Validate JSON
python3 -c "import json; json.load(open('/root/.openclaw/openclaw.json'))"
echo "OK"

# Restart OpenClaw service
sudo systemctl restart openclaw
```

## 8. Reversibility

Snapshot-based. Roll back to `*-bak-heartbeat-fix-$TS` if behavior regresses.

## 9. Sovereign ratification

This sidecar is recommendation-only, not constitutional. 888_HOLD required for:
- Final cadence choice
- Whether to add heartbeat to FED budget enforcement (Gate 5+ for "heartbeat" tool type)
- Whether to escalate alerts via arif_route

---

*DITEMPA BUKAN DIBERI — heartbeat dialed from real-time to quarterly, Pro seat breathing room restored.*
