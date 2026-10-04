# Vault-Bridge Cron Chaining — 2026-08-06

Cron jobs reading each other's output through shared filesystem state. Produces a continuous institutional memory chain without requiring vault999 seal or MCP tool access.

## Architecture

```
06:00  pulse → pulse_state_YYYYMMDD.jsonl
09:00  world-intel → world_intel_YYYYMMDD.jsonl (+ predictions)
08:00  geo-econ (Mon) → geo_econ_YYYYMMDD.jsonl (+ predictions)
20:00  zen → zen_YYYYMMDD.jsonl (reads ALL day's files)
06:30  reckoning (Mon) → reckoning_YYYYMMDD.jsonl (reads WEEK of predictions)
```

All files in: `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/`

## Read Protocol

Each job's prompt includes a STEP 0 that reads prior outputs before generating:

```bash
# Read today's pulse (for world-intel at 09:00)
cat /usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/pulse_state_$(date +%Y%m%d).jsonl 2>/dev/null | tail -1

# Read yesterday's world-intel (for zen at 20:00)
cat /usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/world_intel_$(date -d yesterday +%Y%m%d).jsonl 2>/dev/null | tail -1

# Read week of predictions (for reckoning on Monday)
for i in $(seq 0 6); do
  d=$(date -d "$i days ago" +%Y%m%d)
  for prefix in world_intel geo_econ; do
    f="/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/${prefix}_${d}.jsonl"
    [ -f "$f" ] && cat "$f"
  done
done
```

If the file doesn't exist, set the variable to "UNKNOWN" / "NONE" and proceed in default mode.

## Write Protocol

Each job appends a single JSON line to its output file:

```jsonl
{"ts": "2026-08-08T09:00:15+08:00", "readiness_band": "RED", "predictions": [...], "summary": "..."}
```

Prediction format (for jobs that make them):
```jsonl
{"ts": "...", "prediction": "NFP <100K → XAUUSD breaks $4,300", "falsification": "actual NFP value at 20:00 MYT", "expected_window": "24h"}
```

## Cognitive-Load Modulation

When a downstream job reads the upstream job's readiness state, it adjusts output complexity:

| Pulse readiness | World-intel output |
|---|---|
| `RED` | 3 lines only: NFP event + ringgit + "what NOT to read" |
| `YELLOW` | Macro + gold + Malaysia only. Drop AI + geopolitics. |
| `GREEN` / `UNKNOWN` | Full 6-section format |

Implementation: the world-intel prompt includes the modulation rules in its STEP 0b section. The pulse output includes a `readiness_band` field: `"readiness_band": "RED"`.

## The Reckoning Loop

Monday 06:30: `arif-reckoning` reads the week's prediction files, fetches actual outcomes via web search, and emits weight adjustments.

```
Weight adjustment = {
  "component": "gold|geopolitics|macro|tech|malaysia|energy",
  "direction": "over-weighted" or "under-weighted",
  "magnitude": 0.0-1.0,
  "evidence": "NFP was 32K → gold thesis over-optimistic"
}
```

The reckoning output is read by the next Monday's `geo-econ-horizon` (which applies the weight adjustments — e.g., "lean less on speculative geopolitical narratives").

## Dependencies (no external services required)

- No vault999 seal needed (jsonl files are the state bridge)
- No arifOS MCP tool needed (agents read via terminal `cat`)
- No `context_from` parameter needed (reads are in-prompt via STEP 0)
- Files survive gateway restarts (stored on disk, not in session state)

## Failure Mode

If the chain breaks (a job doesn't fire), the downstream job reads "UNKNOWN" and proceeds in default mode. The chain degrades gracefully — no silent failure. The Monday reckoning will surface: "NO PREDICTIONS TO JUDGE — the institution has no memory."

## Schema

| File | Writer | Contains |
|---|---|---|
| `pulse_state_YYYYMMDD.jsonl` | morning-pulse | readiness_band, sleep, organs, inherited flags |
| `world_intel_YYYYMMDD.jsonl` | world-reality-intel | market prices, predictions, deep cut |
| `geo_econ_YYYYMMDD.jsonl` | geo-econ-horizon | PETRONAS thesis, energy signals, predictions |
| `zen_YYYYMMDD.jsonl` | evening-zen | deltas, unresolved flags, tomorrow intent |
| `reckoning_YYYYMMDD.jsonl` | arif-reckoning | scorecard, weight adjustments, summary |
