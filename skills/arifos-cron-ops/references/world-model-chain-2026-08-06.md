# World-Model Cron Chain — Vault-Bridge Spec (deployed 2026-08-06)

Arif's directive: link all cron jobs so they stop being stateless reporters — "ini betul-betul practical application of Eureka R3 (Cryptography Creates Identity) and R4 (Recursive Improvement is Constitutional)." The chain was built in one session: Pulse → Intel → Reckoning, all live.

## Chain topology

```
arif-morning-pulse (06:00 daily)
   │  writes pulse-{date}.json + pulse-ledger.tsv (SEAL phase)
   ▼
arif-world-reality-intel (09:00 daily, skills: deep-research-plus-wealth, wealth-four-layer-intelligence)
   │  PHASE 0 reads pulse state → modulates output shape
   │  writes intel-{date}.json + intel-ledger.tsv (predictions with falsifiers)
   ▼
arif-reckoning (Mon 06:30)
   │  grades last Friday's predictions vs live prices → SEAL/PARTIAL/VOID/UNKNOWN
   │  writes reckoning-{date}.json + reckoning-ledger.tsv + EMD weight shifts
   ▼
(next week's Intel reads reckoning-ledger → adjusted weights)
```

State dir: `/root/.local/share/arifos/state/`. Created via `mkdir -p`; seed with the existing `config-mutation-*.jsonl` file present.

## State file schemas

### pulse-{YYYY-MM-DD}.json (written by morning-pulse)
```json
{
  "ts_myt": "<ISO 8601 +08:00>",
  "day": "Friday", "date": "2026-08-07",
  "readiness": {"color": "GREEN|YELLOW|RED", "vitality_index": 0.0,
                "sleep_hours": null, "hrv_ms": null, "fatigue_flag": true},
  "federation": {"organs_alive": 7, "organs_total": 7, "ollama_up": true,
                 "aaa_dirty_files": 0, "last_seal_id": "RECEIPT-..."},
  "macro_top3": [{"headline": "...", "why_it_matters": "..."}],
  "focus_today": "<one-line directive>"
}
```
Ledger line: `<date>|<color>|<focus>` → `pulse-ledger.tsv` (append).

### intel-{YYYY-MM-DD}.json (written by world-reality-intel)
```json
{
  "ts_myt": "...", "date": "...",
  "readiness_consumed": "GREEN|YELLOW|RED|UNKNOWN",
  "tone_calibrated": "full|filtered|brutal",
  "key_levels": {"xauusd_spot": 0.0, "xauusd_resistance": 0.0, "xauusd_support": 0.0,
                 "brent": 0.0, "dxy": 0.0, "us10y": 0.0},
  "predictions": [
    {"id": "P20260807-1", "claim": "<one-line, specific — 'gold above $3,400 by Friday close' NOT 'gold will rise'>",
     "horizon": "intraday|weekly|monthly",
     "falsifier": "<what would prove this wrong — REQUIRED field>"}
  ],
  "watch": ["<event-1>"], "sources": ["<source-1>"]
}
```
Ledger line: `<date>|<n_predictions>|<top_claim>` → `intel-ledger.tsv`.

### reckoning-{YYYY-MM-DD}.json (written by arif-reckoning Monday)
```json
{
  "ts_myt": "...", "monday": "...", "graded_friday": "...", "intel_file": "<abs path>",
  "predictions_total": 3, "predictions_sealed": 1, "predictions_partial": 1,
  "predictions_voided": 1, "predictions_unknown": 0,
  "score": 0.5,
  "emd_adjustments": {
    "source_shifts_bp": [{"source": "<name>", "delta_bp": -20}],
    "category_shifts_bp": [{"category": "geopolitics", "delta_bp": 20}],
    "tone_lock_week": "full|filtered|brutal"
  },
  "lesson": "<one-sentence: what intel should do DIFFERENTLY next week>"
}
```
Ledger line: `<monday>|<friday>|<score>|<n_voided>|<lesson[:60]>` → `reckoning-ledger.tsv`.

## Cognitive modulation table (Intel reads Pulse)

| Pulse color | Intel output policy |
|---|---|
| 🟢 GREEN | Full briefing. All 6 sections + Deep Cut (300w) + Market Map + Reality Check. |
| 🟡 YELLOW | Drop Black Swan Watch unless major. Skip Reality Check unless genuinely unverified. Deep Cut shorter (150w). |
| 🔴 RED | Brutal filter. ONLY actionable items affecting today's decisions (gold, oil, MYR, PETRONAS, geopolitical risk to position). No Deep Cut. 3 items + Market Map + 1-line focus. |
| (missing file) | Default GREEN but note "no Pulse today" — do NOT silently upgrade if the file genuinely doesn't exist. |

Also: `tail -7 pulse-ledger.tsv`; 3+ YEL/RED in 7 days → flag "sustained low-readiness pattern" and bias more aggressive filtering.

## Grading verdicts (Reckoning on Intel predictions)

| Outcome | Verdict |
|---|---|
| Direction correct + level within 5% or stated target hit | ✅ SEAL |
| Direction right, magnitude wrong (e.g. "above $3,400" landed $3,380) | ⚠️ PARTIAL — tighten level |
| Direction wrong (>1% opposite move) | ❌ VOID — retract, learn why |
| Cannot verify / horizon not reached | ⏸️ UNKNOWN — defer |

## EMD weight adjustments (basis points; 1bp = 0.01 weight unit)

1. **Source reliability shift** — Reuters/Bloomberg-class >80% right → no shift. Speculative/social >50% wrong → −15 to −30bp per source. Official data (FRED/BNM) wrong → −50bp.
2. **Category bias shift** — geopolitics predictions voided → +20bp to Macro/Commodity (over-weighted on geopolitics). Macro data voided → +20bp to Commodities (trust the tape over the words). AI/Tech voided → −10bp (lower signal for trading life).
3. **Tone lock** — Pulse RED/YELLOW >60% of last 4 weeks → lock Intel to brutal for the week. GREEN >80% → restore full.

## Prompt skeleton conventions (copy for any new chain job)

- Open with `PHASE 0 — READ UPSTREAM STATE` (non-negotiable read before composing).
- Close with `PHASE N — SEAL: WRITE TODAY'S STATE` (JSON + ledger append).
- Human Telegram output carries a header line `⚙️ READ: pulse-{date} ({color}, {tone}) | {n} items` and footer `🔗 SEALED → .../state/intel-{date}.json ({n} predictions)`.
- Zero-touch invariants: never ask Arif a question; never request auth; if a source is unreachable report the gap; if nothing changed say so in one line — never manufacture signal.
- Reckoning must have a no-op exit: if no Friday intel file exists → output "⚖️ NO RECKONING — Friday Intel missing. Skipping grade." and exit.

## Duplicate-job hazard

Before ANY `cronjob(action='create')`: `cronjob(action='list')` and grep names. Sibling agents create jobs concurrently — this session found `arif-world-intel` duplicating `arif-world-reality-intel` (killed the bare, skill-less one) and a sibling's `arif-reckoning` at Mon 08:00 (killed via remove; verify it actually still exists before assuming the remove failed — a stale list entry can show a job already gone). Delivery: chain jobs to `telegram:267378578` (Arif's user_id) or `origin` for chat-context delivery.
