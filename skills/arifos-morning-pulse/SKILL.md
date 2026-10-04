---
name: arifos-morning-pulse
description: Execute the daily 06:00 MYT arif-morning-pulse cron job — WELL human-readiness probe, federation health scan, macro/news scan, VAULT999-adjacent state seal. Use when running as arif-morning-pulse, producing today's pulse, or reading/writing /root/.local/share/arifos/state/pulse-<date>.json.
---

# arifOS Morning Pulse (arif-morning-pulse)

Daily 06:00 MYT cognitive ignition for Arif. ONE Telegram ping, BM casual, terse.
Downstream dependency: `arif-world-reality-intel` (09:00) reads today's pulse JSON to
calibrate cognitive load — **without the seal, downstream jobs suffer amnesia.** The seal
is load-bearing, not cosmetic. See that skill for the consumer-side pipeline, tone policy,
and prediction-seal schema.

## Pipeline (4 stages)

### A. Human Readiness (do this FIRST — it gates everything)
1. `curl -sf http://127.0.0.1:18083/health -o /tmp/well-health.json && python3 -c ...`
2. Sleep bridge: `cat /root/HERMES/scripts/health-bridge/last-night.json 2>/dev/null || echo 'no data'`
3. MYT timestamp: `TZ='Asia/Kuala_Lumpur' date '+%A %d %b %Y %H:%M'`

Color logic:
- vitality_index ≥ 0.7 → 🟢 GREEN | 0.4–0.69 → 🟡 YELLOW | <0.4 → 🔴 RED
- **vitality_index absent/null → do NOT default to 0/GREEN.** Fail closed (see pitfalls).

### B. Federation Reality (one line each)
- Organs: `for p in 8088 7071 3001 8081 18082 18083 7073; do curl -sf --max-time 2 http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ :$p" || echo "❌ :$p"; done`
- Ollama :11434 (Graphiti dependency) — warn if DOWN
- AAA dirty: `cd /root/AAA && git status --porcelain | wc -l`
- Last VAULT999 seal: `tail -1 /root/.local/share/arifos/vault999/outcomes.jsonl | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('record_id', d.get('type','?'))[:30])"`

### C. Macro/News (max 3, no fluff)
`web_search('global macro news today energy markets ASEAN geopolitics AI tech')` then
targeted follow-ups (e.g. `Brent crude oil price OPEC <month> <year>`, `Malaysia PETRONAS
news <year>`, `AI model release funding <year>`). Filters, in priority order:
1. Energy (Brent, OPEC, PETRONAS) — Malaysia revenue exposure
2. ASEAN geopolitics / Malaysia-relevant items
3. AI/tech with capital-market consequences
Each item: `headline` + 1-line `why_it_matters`. Include concrete numbers (price, %, $).

If the configured search/extract backend is unavailable (e.g. HTTP 432 bot-block, Tavily
quota, Jina timeout), do not silently omit macro context. Fall back to three parallel
`browser_navigate` calls on Bing News with narrow queries:
  - `https://www.bing.com/news/search?q=oil+OPEC+Brent&FORM=HDRSC6`
  - `https://www.bing.com/news/search?q=Malaysia+ASEAN+geopolitics&FORM=HDRSC6`
  - `https://www.bing.com/news/search?q=AI+funding+model+release+capital+markets&FORM=HDRSC6`
Pick the 3 highest-signal items across those three result sets. Prefer headlines with
named outlets (Reuters, The Star, Bloomberg) and named dates. Disclose the fallback
explicitly in the pulse output (e.g. "Macro scan via Bing News fallback — primary backend unavailable").
Treat snippets as provisional [OBS]; do not add numbers the snippet itself does not carry.

### D. Seal (write machine-readable state + ledger)
1. Write `/root/.local/share/arifos/state/pulse-<YYYY-MM-DD>.json` — schema:
   `ts_myt` (ISO 8601 +08:00), `day`, `date`, `readiness{color, vitality_index, sleep_hours,
   hrv_ms, fatigue_flag}`, `federation{organs_alive, organs_total, ollama_up,
   aaa_dirty_files, last_seal_id}`, `macro_top3[{headline, why_it_matters}]`, `focus_today`.
   Extra diagnostic fields are welcome (well_signal, state_age_hours, decision_fatigue,
   clarity, note) — they help the 09:00 consumer.
2. Update the ledger idempotently: remove any existing line beginning with `<date>|`, then
   append exactly one `<date>|<color>|<focus>` line to
   `/root/.local/share/arifos/state/pulse-ledger.tsv`. Cron reruns (e.g. manual re-trigger)
   must not create duplicate entries. Implement in Python (read existing, filter by date prefix,
   rewrite) rather than `echo >>` alone. **Color MUST match JSON `readiness.color`.**
3. Verify with `scripts/verify_pulse.py <YYYY-MM-DD>` (ad-hoc schema + ledger cross-check;
   no canonical suite exists for this file).

## Output format (BM casual, terse — one Telegram ping)

```
☀️ ARIF MORNING PULSE — {day}, {date} — {time} MYT

🫀 READINESS
  WELL: {color} vitality={v:.2f}
  Sleep: {hrs}h | HRV: {ms}ms ⚠️ if fatigued

⚙️  FEDERATION
  Organs: {alive}/{total} alive
  Ollama: ✅ UP / ❌ DOWN
  AAA dirty: {n} files
  Last seal: {seq}

📰 MACRO (3 items max)
  1. {headline} — {1-line why-it-matters}
  ...

🎯 FOCUS TODAY
  {1-line derived from macro + readiness: what should Arif protect or push?}

🔗 SEALED → /root/.local/share/arifos/state/pulse-{date}.json
```

## Pitfalls (learned 2026-08-08)

- **WELL /health has NO `thermodynamic` key.** The spec's
  `d.get('thermodynamic',{}).get('vitality_index',0)` silently returns 0 on every real
  payload. Real readiness signals: `well_signal` (WELL_HOLD = no readiness), `well_score`
  (null), `state_age_hours`, `freshness_band` (STALE), `truth_status`
  (INSUFFICIENT_DATA), `metrics.cognitive.{clarity, decision_fatigue}`. Full observed
  payload: `references/well-health-schema.md`.
- **Fail closed on human readiness.** No live telemetry (vitality absent, state_age_hours
  ≫ 48, decision_fatigue = 10.0, WELL_HOLD) → 🔴 RED + HOLD, never GREEN. The 09:00
  reality-intel calibrates Arif's cognitive load off this file; a false GREEN loads him
  when he's blind. Focus directive becomes: defer irreversible moves (sizing, allocation,
  F13 commits) until WELL re-pings.
- **Missing sleep bridge file → nulls, not zeros.** `sleep_hours: null`, `hrv_ms: null`,
  `fatigue_flag: false`. Never fabricate sleep data to fill the schema.
- **Color consistency:** ledger line and JSON color must agree — the ledger IS the
  operating context for downstream jobs. Verify both after writing.
- Saturday + RED → "sovereign-only mode": light F13 review + cognitive recovery, protect
  the substrate, don't push.
- **`owner_summary.color` is the direct readiness signal.** When present, use it directly
  (GREEN/YELLOW/RED) with the `reasons` array for context. Don't recompute from
  `well_signal` + `freshness_band` + `state_age_hours` when the organ already decided.
  Fallback to the manual decode only when `owner_summary` is absent.
- **`honesty.is_mock_or_test` = biometrics are synthetic.** If true, note it in the pulse
  output (e.g. "MOCK/TEST mode — no live biometrics"). A YELLOW from mock data is less
  alarming than YELLOW from real sensors, but Arif must know the difference.
- **Use `scripts/verify_pulse.py`, don't recreate inline.** The skill ships a reusable
  verification script. Running `python3 <skill_dir>/scripts/verify_pulse.py <date>` is
  sufficient; creating ad-hoc `/tmp/hermes-verify-*` scripts is redundant.
- Quiet-hours doctrine: 06:00 MYT is inside the 23:00–07:00 window but the pulse is the
  one sanctioned morning ping (it is the job itself).

## Support files
- `references/well-health-schema.md` — real WELL /health payload anatomy (degraded state)
- `scripts/verify_pulse.py` — ad-hoc schema + ledger cross-check for a pulse date
