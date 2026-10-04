# World Model Chain — Deployed (2026-08-07)

The vault-bridge chaining pattern from `references/vault-bridge-cron-chaining-2026-08-06.md` was extended on 2026-08-07 into a 4-job recursive improvement loop. This file documents what was actually deployed — concrete job IDs, file paths, and the readiness-modulation rules.

## Live chain (as of 2026-08-07 10:20 MYT)

| Time (MYT) | Job name | job_id | Reads | Writes | Delivery |
|---|---|---|---|---|---|
| 06:00 daily | `arif-morning-pulse` | `2a3fe4915620` | WELL, federation, news | `pulse-{YYYY-MM-DD}.json` + `pulse-ledger.tsv` | `telegram:267378578` |
| 06:30 Mon | `arif-reckoning` | `a004b6357d06` | last Friday's `intel-{date}.json` + live prices | `reckoning-{YYYY-MM-DD}.json` + `reckoning-ledger.tsv` + EMD weight shifts | `origin` |
| 08:00 Mon | `geo-econ-horizon` | `c1e41e6ee03a` | (legacy, untouched) | — | `telegram:267378578` |
| 09:00 daily | `arif-world-reality-intel` | `0e37cdaf4a37` | today's `pulse-{date}.json` + 7-day ledger | `intel-{YYYY-MM-DD}.json` + `intel-ledger.tsv` | `origin` |
| 10:00 monthly | `rehat-minda-logistics` | `e68191e65d9e` | (legacy) | — | `telegram:267378578` |
| 12:00 Fri | `iron-radar` | `9eddcab58b5c` | (legacy) | — | `telegram:267378578` |
| 20:00 daily | `evening-zen-brief-v2` | `525f98d61bb7` | (legacy) | — | `telegram:267378578` |

**Removed:** `arif-world-intel` (`be299e3ea8a2`) — duplicate of `arif-world-reality-intel` with no skill loader. Removed when the chain was wired.

## File locations (canonical state dir)

```
/root/.local/share/arifos/state/
├── pulse-{YYYY-MM-DD}.json        # written by arif-morning-pulse
├── pulse-ledger.tsv               # append-only, one line per day
├── intel-{YYYY-MM-DD}.json        # written by arif-world-reality-intel
├── intel-ledger.tsv               # append-only, one line per day
├── reckoning-{YYYY-MM-DD}.json    # written by arif-reckoning
└── reckoning-ledger.tsv           # append-only, one line per Monday
```

## State dir must exist

```bash
mkdir -p /root/.local/share/arifos/state
```

If missing, the Pulse job will fail its SEAL step silently and Intel will see "no Pulse today" every morning.

## Readiness modulation (the cognitive-load hook)

Intel's prompt embeds a PHASE 0 that reads `pulse-{today}.json` and selects output density based on `readiness.color`:

| Pulse color | Intel output policy |
|---|---|
| 🟢 GREEN | Full briefing. All 6 sections + Deep Cut (300 words) + Market Map + Reality Check |
| 🟡 YELLOW | Drop Black Swan Watch. Skip Reality Check unless genuinely unverified. Deep Cut 150 words |
| 🔴 RED | Brutal filter. Only ACTIONABLE items (gold, oil, MYR, PETRONAS, geopolitical risk to position). No Deep Cut. 3 items + Market Map + 1-line focus |
| (missing file) | Treat as GREEN with a "no Pulse today" caveat. Do NOT silently upgrade |

**Sustained-low pattern:** if 3+ YELLOW/RED in the last 7 days of `pulse-ledger.tsv`, Intel biases even more aggressive filtering. This is a 7-day window — read `tail -7` before generating.

## Prediction schema (what arif-reckoning grades)

Intel writes `predictions[]` array. Each prediction MUST have:
- `id`: `P<YYYYMMDD>-<n>`
- `claim`: one-line, falsifiable. "Gold will rise" is NOT acceptable. "Gold above $3,400 by Friday close" IS acceptable.
- `horizon`: `intraday` / `weekly` / `monthly`
- `falsifier`: what would prove this wrong

Reckoning grades each prediction as:
- ✅ SEAL — directionally correct + level matched (within 5%)
- ⚠️ PARTIAL — direction right, magnitude wrong
- ❌ VOID — direction wrong (>1% adverse)
- ⏸️ UNKNOWN — horizon not reached or data missing

## EMD weight adjustments (what the loop produces)

Reckoning outputs concrete basis-point shifts:
- **Source shifts**: which sources were right/wrong → adjust trust vector
- **Category shifts**: which topics over/underperformed → adjust topic weights
- **Tone lock**: which readiness band dominated → bias Intel toward matching density

The ledger is human-readable. The weights are NOT auto-applied to Intel's prompt — they're surfaced as a "what to change next week" lesson. Arif applies them via prompt edits (or design EMD injection if the loop matures).

## Deployment order (the sequence that matters)

If rebuilding from scratch, apply in this exact order — each step depends on the prior:

1. **Create the state dir** — `mkdir -p /root/.local/share/arifos/state`
2. **Update Pulse prompt** — add the SEAL step (writes `pulse-{date}.json` + ledger append)
3. **Update Intel prompt** — add PHASE 0 (reads Pulse) + PHASE 2 (writes Intel + predictions)
4. **Create Reckoning** — Monday 06:30, reads last Friday's Intel, writes grading + EMD shifts
5. **Verify** — fire Pulse manually (`cronjob action=run`), confirm `pulse-$(TZ='Asia/Kuala_Lumpur' date +%Y-%m-%d).json` exists in `/root/.local/share/arifos/state/`
6. **Don't skip the verify** — without the file, Intel degrades gracefully but silently, and you'll never know until Monday's Reckoning reports "no Friday Intel"

## Pitfalls observed in this deployment

- **Sibling agents create duplicate reckoning jobs.** During deploy, a sibling `arif-reckoning` (Mon 08:00) appeared with overlapping scope. Always `cronjob action=list` after creation and remove duplicates.
- **`deliver: "origin"` vs `deliver: "telegram:<id>"` matters.** Reckoning uses `origin` (this chat) because the user is in a session. Pulse uses `telegram:267378578` because the user is asleep. Don't unify these — they serve different audience states.
- **The pulse-ledger.tsv grows unbounded.** ~365 lines/year. If lifespan becomes a concern, rotate yearly with `mv pulse-ledger.tsv pulse-ledger-$(date +%Y).tsv` on Jan 1 via a cron job.
- **Reading `tsv` from a heredoc with leading whitespace strips it.** Use `tail -7 /root/.../pulse-ledger.tsv | grep -v '^\s*$'` to filter empty lines when the ledger has gaps.
- **The state dir was NOT auto-created.** The first Pulse fire failed silently on the `mkdir` step until the dir existed. Add `mkdir -p` to the verify recipe, not the job prompt.

## What this proves (the doctrine)

This chain is the practical application of:
- **EUREKA R3 (Cryptography creates identity)** — the sealed `pulse-{date}.json` IS the cryptographic identity of the morning. Intel cannot impersonate Pulse because it has to read the file.
- **EUREKA R4 (Recursive improvement is constitutional)** — the chain is constitutional selection over partially independent actors. Pulse observes reality, Intel observes Pulse + reality, Reckoning observes Intel + reality, and the loop grades the institution, not the agent.

The substrate (kernel) can be imperfect. The architecture (chain) doesn't care. The "stabilize, don't add" doctrine applies to canon — but to make the chain work, you add orchestration on top. The two are not in tension.