# 2026-06-13 ~04:47-04:57Z — Hermes Emergency Switch to Kimi

## What happened

Arif flagged DeepSeek API key habis kredit, asked for fallback to minimax,
make sure no looping chaos. Three-agent triage:

- **ASI💃 (Hermes itself)**: reported machine OK, 18G disk recoverable, 3 systemd
  services in crash loop (separate), load 26 driven by 3 opencode + 1 stuck clamscan.
- **AGI🦞 (me, brief context)**: confirmed DeepSeek 402, MiniMax 503/429, kimi live.
- **OPENCLAW (me, this session, config layer)**: found structural bug —
  `fallback_model` set to same dead primary, causing "Fallback skip" infinite
  retry loop. Also caught secondary issue: `KIMI_API_KEY` only in
  `/root/HERMES/.env` which systemd doesn't source — auth.json status=ok was
  a phantom registration.

## Root cause (3 layers)

1. **Primary**: `deepseek/deepseek-v4-pro` → 402 Insufficient Balance
2. **Fallback chain**: `fallback_providers: [minimax, ilmu]`
3. **fallback_model block** (the bug): `provider: deepseek, model: deepseek-v4-pro`
   → "chain entry matches current provider/model" skip → retry dead primary
   → 402 → skip → ... flooded journal, no progress for 10+ hours
4. **Hidden env gap**: KIMI_API_KEY present in `/root/HERMES/.env` but NOT in
   `/root/.secrets/env/providers.env` (the actual systemd-sourced file). So even
   if I had switched primary to kimi, it would have failed at key load.

## Fix applied (5 edits across 2 files + 1 process)

| # | File | Change |
|---|---|---|
| 1 | `/root/.secrets/env/providers.env` | Append `KIMI_API_KEY` + `KIMI_BASE_URL` |
| 2 | `/root/HERMES/config.yaml` model block | `default: kimi-coding/kimi-for-coding, provider: kimi-coding, switched_at: 2026-06-13` |
| 3 | `/root/HERMES/config.yaml` providers block | Add `kimi-coding:` entry between deepseek and ilmu |
| 4 | `/root/HERMES/config.yaml` fallback_providers | `[minimax, kimi-coding, ilmu]` (kimi moved up since now primary) |
| 5 | `/root/HERMES/config.yaml` fallback_model | `provider: minimax, model: MiniMax-M3` (was pointing to dead deepseek) |
| 6 | process | `kill -9 2176908` (clamscan zombie, 65% CPU, state T) |
| 7 | process | `systemctl restart hermes-asi-gateway` (had to `kill -9` old PID 1016613 after SIGTERM timeout — busy event loop from 10h of API retries) |

## Backups

- `/root/HERMES/config.yaml.bak.20260613-0452-pre-kimi-switch` (15180 bytes)
- `/root/.secrets/env/providers.env.bak.20260613-0452-pre-kimi-add` (4479 bytes)

## Verification

- New process PID 2401450, fresh start, 47.6M RSS
- Telegram platform: `state: connected` at 04:55:18Z
- journalctl last 2 min: **0 error/warning lines** (was flooding every ~1s)
- kimi-coding credential status: `ok`
- deepseek credential: still `exhausted 402` (expected, key dead)
- minimax credential: still `exhausted 429` (stale, may have reset)

## F2 confessions

1. Initial diagnosis almost missed the env-load gap. Auth.json said
   `kimi-coding status=ok` which I almost took at face value. Process env
   check (`/proc/<pid>/environ`) caught it. **Lesson: credential pool
   status='ok' only means "registered, not yet tested" — not "live".**
2. The 888 ask was clean (3 options + recommendation). Arif picked 🅐.
3. The old process needed SIGKILL not SIGTERM (busy event loop). Should
   probably add `KillMode=mixed` or `TimeoutStopSec=60` to the systemd unit
   in a future cleanup pass — currently 210s is way too long.

## Reversibility

All edits backed up. To revert: `cp` the .bak files back + restart.
Provider list includes deepseek so re-activating is one model.default
flip away.

## Carry-forward (not done, surfaced for Arif)

1. **MiniMax** may have reset by now — verify with a test query, watch for
   `minimax status` to flip from `exhausted` to `ok`. If reset, fallback
   chain becomes: kimi (primary) → minimax (live) → ilmu.
2. **DeepSeek** key is dead until Arif tops up.
3. **Disk cleanup** (ASI flagged): 18G recoverable — 2 stale backups
   (12G + 5.5G), hermes state.db vacuum (~600M reclaimable), 4 venvs
   consolidation. Not urgent.
4. **3 systemd crash loops** (geox-static, nats-prometheus, +1): cosmetic,
   not blocking federation.
5. **systemd unit cleanup**: TimeoutStopSec=210 is too long. Suggest 60s.
   Add a note to arifos-hygiene backlog.
6. **Auth pool phantom-status issue**: hermes-agent credential pool sets
   `status=ok` on registration but doesn't actually test until first call.
   Misleading for diagnosis. Consider a "ping on boot" feature.

## Receipts

- Telegram DM conversation #74704-#74718
- journalctl: "Consumed 59min 15.612s CPU time, 8G memory peak" before kill
- gateway_state.json: `state: running, pid: 2401450`
- Time spent: ~10 min wall clock (04:47-04:57Z)
