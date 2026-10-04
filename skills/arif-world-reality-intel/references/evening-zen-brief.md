# Evening Zen Brief (evening-zen-brief-v2) — downstream consumer schema

Daily 20:00 MYT wind-down cron. Consumes the day's prediction artifacts and seals the
`unresolved` chain forward. This is the consumer side of
`arif-world-reality-intel`'s `predictions` array.

## Inputs (STEP 0)

Read today's files from `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/`:

```bash
D=$(date +%Y%m%d)
tail -1 pulse_state_${D}.jsonl      # today's readiness (may be ABSENT)
tail -1 world_intel_${D}.jsonl      # today's intel predictions (may be ABSENT)
tail -1 geo_econ_${D}.jsonl         # geo-econ predictions (Mon/Mon-only)
curl -sf http://127.0.0.1:8088/health | head -c 200   # kernel drift check
```

If today's files are absent → **chain gap**. Fall back to yesterday's
`zen_<yesterday>.jsonl` + `geo_econ_<yesterday>.jsonl` to carry the `unresolved`
flags forward. Flag the gap itself as `unresolved` item `chain-gap`.

Predictions carry a `call_hash` id (e.g. `gch-001`, `gch-002`, `gch-003`),
a `claim`, `confidence`, `tag` (OBS/DER/INT), and `falsifiable_by` date.

## Output schema (STEP 2 — seal)

Write one JSONL line to `cron/output/zen_<YYYYMMDD>.jsonl`:

```json
{
  "ts": "<ISO 8601 +08:00>",
  "deltas": {
    "gold":  { "close": "<obs>", "prediction": "<claim>", "status": "on-track|tracking|diverging|diverging-hard", "note": "<OBS-tagged>" },
    "brent": { "close": "<obs>", "prev_close": "<obs>", "prediction": "<claim>", "status": "...", "note": "..." },
    "myr":   { "rate": "<obs>", "trend": "stable|weaken|strengthen", "note": "..." },
    "new_signals": [ "<headline (OBS, source)>", "..." ]
  },
  "unresolved": [
    { "id": "gch-001", "claim": "<claim>", "conflict": "<why diverging>" },
    { "id": "chain-gap", "claim": "<what broke>", "status": "OBS - needs re-arm" }
  ],
  "tomorrow_first": "<1-2 lines: dominant thread + first action>"
}
```

Verify with a one-line inline parse before delivering:

```bash
python3 -c "import json; d=json.loads(open('zen_${D}.jsonl').read()); \
assert all(k in d for k in ('ts','deltas','unresolved','tomorrow_first')); \
assert len(d['unresolved'])>=1; print('JSONL VALID')"
```

This is ad-hoc verification (not suite green) — state that explicitly.

## Delivery (STEP 3)

Final response is auto-delivered by the cron harness to the configured Telegram chat.
Do NOT call send_message. If nothing new, reply exactly `[SILENT]`.

## Tone

Wind-down, reflection, NOT a briefing. No flattery, no "I've got your back."
Every number tagged [OBS] / [DER] / [INT] / [UNKNOWN]. If a metric can't be
fetched (sleep debt, readiness when pulse didn't run), say UNFETCHED — never guess.
