# arif-morning-pulse — WELL MOCK-signal & freshness trap (2026-08-07)

Reference for the 06:00 daily cognitive-ignition job `arif-morning-pulse`. Captures
the real signal-reading rules for the WELL organ that the prompt's naive
`vitality_index` lookup misses. Future pulse sessions must read this first.

## The trap

The deployed prompt says:

```
curl -sf http://127.0.0.1:18083/health | python3 -c "...print(d.get('thermodynamic',{}).get('vitality_index',0))"
  → vitality_index ≥ 0.7 → GREEN | 0.4-0.69 → YELLOW | <0.4 → RED
```

**This returns `0` 100% of the time when WELL is not actively measuring** because
`thermodynamic.vitality_index` is a stub path that resolves to `None` → default
`0`. Reporting this as `RED` is a false alarm (a healthy body mis-labeled
collapsed because the sensor wire is disconnected).

The full `:18083/health` payload carries the real signals in different keys:

| Key | Real signal | Interpretation |
|-----|-------------|----------------|
| `owner_summary.color` | `GREEN` / `YELLOW` / `RED` | Kernel-computed readiness band — use THIS, not vitality_index |
| `well_signal` | `WELL_HOLD` / `WELL_OK` | Domain-level hold/ok (floor-checked verdict) |
| `freshness.status` | `fresh` / `aged` / `stale` | Time since last measurement (`max_fresh_age_seconds=3600`, `stale_after=14400`, `expired_after=86400`) |
| `state_age_hours` | float | 30.7 → no fresh sensor reading in 30h (clearly stale) |
| `honesty.code` | `MOCK` / `SENSOR_VERIFIED` / `SELF_REPORT` | **`MOCK` = "test data, not live biometrics — do not treat as body truth"** |
| `honesty_banner` | "MOCK / TEST -- not live biometrics..." | Same warning in plain English |
| `metrics.cognitive.clarity` | 0-10 | Self-reported clarity (use with caution — see `honesty.code`) |
| `metrics.cognitive.decision_fatigue` | 0-10 | Self-reported fatigue (higher = more fatigued) |
| `apex_scalars.*` | `value: null, status: UNMEASURED` | All apex scalars unmeasured → F8 GENIUS_UNCOMPUTED by design |
| `domain_data_readiness` | `INSUFFICIENT_DATA` / `READY` | Tells you whether downstream tools can run |

## Correct read protocol (replaces the prompt's broken lookup)

```bash
curl -sf http://127.0.0.1:18083/health > /tmp/well.json && python3 -c "
import json
d = json.load(open('/tmp/well.json'))
o = d.get('owner_summary', {})
print('color:', o.get('color'))          # GREEN/YELLOW/RED — THE field
print('well_signal:', d.get('well_signal'))
print('freshness:', d.get('freshness',{}).get('status'))
print('state_age_h:', d.get('state_age_hours'))
print('honesty.code:', d.get('honesty',{}).get('code'))   # MOCK = not live
print('data_readiness:', d.get('domain_data_readiness'))
"
```

Then map to readiness band:

- `owner_summary.color == GREEN` AND `honesty.code != MOCK` AND `freshness.status == fresh` → 🟢 GREEN
- `owner_summary.color == YELLOW` OR `freshness.status in (aged, stale)` OR `honesty.code == MOCK` → 🟡 YELLOW + ⚠️ FATIGUE banner
- `owner_summary.color == RED` OR (`state_age_hours > 24` AND `honesty.code == MOCK`) → 🔴 RED

When `honesty.code == MOCK`, the report MUST prepend `⚠️ FATIGUE` even if `color == GREEN`,
because MOCK = "not live biometrics" — the system is honest about not knowing.
Arif's owner_summary reason in this case will typically be `human_injection_required`.

## Xiaomi Smart Band bridge: where data lives

The prompt says:
```
cat /root/HERMES/scripts/health-bridge/last-night.json
```

This file is the **correct location** when present, but its absence is normal —
the Xiaomi Smart Band bridge is not always running. When missing, report
`Sleep: — | HRV: —` with the ⚠️ FATIGUE banner and do NOT synthesize numbers.

Sleep < 6h or HRV < 30ms from a sensor-verified (non-MOCK) reading → FATIGUE flag = true.
MOCK readings → do not trust the numbers; report the MOCK banner instead.

## Fatigued-but-healthy reporting discipline

A YELLOW state with `honesty.code == MOCK` and `state_age_hours=30` is the
honest answer when WELL is wired up but no biometric source is feeding it.
Reporting that as RED ("vitality 0 → RED") is a false alarm. Reporting it as
GREEN ("vitality OK") is dishonest. YELLOW + ⚠️ FATIGUE banner is the
SOVEREIGN_VERIFY-correct output.

## Federation organ list (verified live 2026-08-07)

```
for p in 8088 7071 3001 8081 18082 18083 7073; do curl -sf --max-time 2 http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ :$p" || echo "❌ :$p"; done
```

arifOS:8088, A-FORGE:7071, arifFlow:3001, :8081, WEALTH:18082, WELL:18083, plus :7073.
Verify on each run — ports can drift.

## Ollama :11434 fail-closed warning

If `curl -sf http://127.0.0.1:11434/api/tags` fails, report `❌ DOWN` and prepend
a ⚠️ note: Graphiti (memory layer) depends on local embedding model — without
Ollama, downstream memory writes degrade. This is the only organ where DOWN
matters specifically for the morning pulse.

## Macro/news: signal-density filter

The prompt says "max 3 items" — held to that. Filter rule (proven 2026-08-07):

1. **Energy markets first** — Brent price + OPEC/PETRONAS relevance (Malaysia).
   Don't quote Brent without naming the % move and the conflict driver.
2. **ASEAN geopolitics second** — only if a Malaysia-relevant item exists.
   Skip this slot if the news cycle has nothing in it; don't fabricate to hit 3.
3. **AI/tech with capital-market consequences third** — model releases with $
   attached, big funding rounds, IPO filings. Skip if none in last 24h.

If only 1-2 items clear the filter, report 1-2 items. Do NOT pad with low-signal
items to fill the slot.

## Ledger sealing — load-bearing

The state file `/root/.local/share/arifos/state/pulse-YYYY-MM-DD.json` is read
by `arif-world-reality-intel` (09:00) and downstream jobs. The ledger line
(`/root/.local/share/arifos/state/pulse-ledger.tsv`) is the canonical operating
context for the day's other jobs.

Schema reminder:
```json
{
  "ts_myt": "<ISO 8601 with +08:00>",
  "day": "<Friday>",
  "date": "<2026-08-07>",
  "readiness": {"color": "YELLOW", "vitality_index": 0.0, "sleep_hours": null, "hrv_ms": null, "fatigue_flag": true},
  "federation": {"organs_alive": 7, "organs_total": 7, "ollama_up": true, "aaa_dirty_files": 0, "last_seal_id": "..."},
  "macro_top3": [{"headline": "...", "why_it_matters": "..."}],
  "focus_today": "1-line directive"
}
```

`focus_today` is the cognitive-load setter for downstream jobs. RED → "3 lines
only". YELLOW → "focused subset". GREEN → full format. (See `arifos-cron-ops` →
vault-bridge chaining pattern.)

## Ad-hoc verification script (post-write check)

After writing the state file, run a schema verification:
```bash
python3 /tmp/hermes-verify-pulse-state.py
```
Expected: `PASS: <date> | <color> | vitality=<v> | organs=<a>/<t> | macro=<n> items | ledger OK`

Script is ephemeral at `/tmp/hermes-verify-pulse-state.py`, recreated per
session. Not committed (state files are dated per-day, ephemeral too).

## Lessons from 2026-08-07 run

1. `vitality_index` lookup in the prompt is dead code — kernel doesn't populate
   `thermodynamic.vitality_index`. The real key is `owner_summary.color`. Prompt
   should be patched; until then, use this recipe.
2. Xiaomi bridge file absent is NORMAL, not an outage — report `Sleep: —` cleanly,
   don't pretend.
3. YELLOW + ⚠️ FATIGUE banner is the honest answer for MOCK/stale biometrics —
   never RED, never silent GREEN.
4. MOCK banner ("MOCK / TEST -- not live biometrics. Do not treat as body truth.")
   is the kernel's own honesty signal — respect it verbatim in the report.