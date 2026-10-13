# CHRON verify cycle — cron proposal

**Date:** 2026-10-06
**Author:** 333-AGI (FI-008) — refinement within Pintu B
**Type:** F13 binary required (per `base.md` line 15: "no new cron without explicit F13 approval")

## What

`/root/AAA/scripts/chron_verify_cycle.py` exists and works. It:
1. Reads `/root/chron/data/predictions.jsonl`
2. Filters ACTIVE predictions whose `verify_at <= today`
3. Probes market state via WEALTH MCP (cached 6h)
4. Probes filesystem state via `verifier_method` (ExecStart grep etc.)
5. Computes brier score and verdict (CORRECT / INCORRECT / UNKNOWN)
6. Updates prediction status, appends to `verification_log.jsonl`, emits lesson to `lessons.jsonl`

This closes T3 → T4: every cycle produces fresh calibration data.

## How to fire (no new infrastructure)

Option A — wire as a cron (F13 binary needed):
```json
{
  "id": "chron-verify-daily",
  "name": "CHRON verify cycle (06:00 MYT daily)",
  "prompt": "python3 /root/AAA/scripts/chron_verify_cycle.py",
  "schedule": {"kind":"cron","expr":"0 6 * * *","display":"0 6 * * *"},
  "deliver": null,
  "lane": "machine",
  "no_agent": true,
  "script": null
}
```

Option B — wire as a cron (later in day, after A-Z pulse):
```json
{
  "schedule": {"kind":"cron","expr":"30 6 * * *","display":"30 6 * * *"}
}
```

Option C — wire as a hook on `chron_briefing` (event-driven, no polling):
Trigger: `chron_briefing.last_write_utc` changes → run verify_cycle.
This is the **APEX-compliant** way: per `base.md` "new capability fires on a trigger, not a polling timer".

## What this proposal does NOT do

- Does NOT auto-publish verdicts to Telegram
- Does NOT modify prediction confidence based on brier
- Does NOT add new prediction classes
- Does NOT touch the TREE777 anchor (still absent)
- Does NOT mutate any constitutional state

## Live evidence (this morning's run, 2026-10-06 08:57 MYT)

```
4 ACTIVE → VERIFIED
  pred-a1210fe9e53c  INCORRECT  brier=0.4225  conf=0.65  (Brent 100.54 vs range 65-75)
  pred-d54455f9b039  INCORRECT  brier=0.4900  conf=0.70  (systemd count=0, claim said 14)
  pred-oil-001-up75  CORRECT    brier=0.1225  conf=0.65  (Brent 100.54 > 70)
  pred-usmyr-001-down CORRECT    brier=0.0784  conf=0.72  (USDMYR 4.087 < 4.40)

19 ACTIVE → gaps/errors/UNOBSERVABLE (RON95, NG, KLCI = NO_LIVE_DATA;
rest = EVENT_PREDICTION = need manual review)

Counts moved:
  predictions.jsonl: ACTIVE 59→55, VERIFIED 4→6, INCORRECT 0→2
  lessons.jsonl: 8→12 (4 cycle-derived, each with prediction_id + brier + evidence)
  verification_log.jsonl: 30→53 entries
```

## What F13 decides

- **A)** Add daily 06:00 cron (simple, polling). Easy to reason about.
- **B)** Add daily 06:30 cron (after A-Z morning pulse writes to chron_briefing).
- **C)** Wire as event-driven hook (APEX-compliant, no new poll, harder to reason about).
- **D)** Hold — keep running manually, F13 triggers when needed.
- **E)** Defer — accumulate more cycle evidence first (next 7 days), then decide.

DITEMPA BUKAN DIBERI ⚒️
