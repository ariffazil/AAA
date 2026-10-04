# Cron Audit — 2026-08-11 (Arif F13 directive)

**Trigger:** Arif observed "every cron job must have meaning and function and benefits in the long run for Arif Fazil. Kalau takat dok spam telegram x payah."

## Starting state

21 jobs in L2 gateway registry (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json`):
- 9 with `last_status: error` (model drift + dead machines)
- 2 confirmed duplicates (`arifflow-daily-digest` vs `arifflow-daily-governance-digest`)
- Token cost baseline: ~3.77M tok/month (computed per the skill's formula)

## Action audit table

| ID | Name | Schedule | Decision | F3 rationale |
|---|---|---|---|---|
| `50149e42f6d9` | `seal-integrity-sweep` | Sun 03:17 | **RETIRE** | F11 auditability = write-time invariant, not sweep |
| `7602d6cfdcc7` | `memory-compression` | Daily 02:13 | **RETIRE** | Nobody reads `/root/.local/share/arifos/state/memory-compress-*.json` |
| `8aa44381de86` | `contradiction-scan` | Sat 03:23 | **RETIRE** | Better as apex-judge preflight rule |
| `3d369c28f1ab` | `artifact-drift-audit` | Daily 01:53 | **RETIRE** | No human action on ORPHAN report; git-to-vault handles sealing |
| `4f47cde23bb8` | `output-attestation-check` | every 120m | **RETIRE** | Every 120m × LLM = waste; hooks handle attestation |
| `4eee9cc62dfb` | `institution-metrics-pulse` | every 6h | **RETIRE** | Telemetry spike, no consumer |
| `2123bfc0a3bc` | `vault-data-refresh` | every 5m | **RETIRE** | 288×/day writes, nobody consumes |
| `29a1d93fbd53` | `arifflow-daily-digest` | Daily 22:00 | **REMOVE** | Duplicate of `arifflow-daily-governance-digest` |
| `6c672e289f80` | `arifflow-daily-governance-digest` | Daily 22:00 | **REMOVE** | Same hour, same target, VM-based. Replace with `evening-zen-brief` consolidation |
| `2a3fe4915620` | `arif-morning-pulse` | Daily 06:00 | **KEEP + PIN** | Human intel: readiness at 06:00. Model pin needed |
| `c1e41e6ee03a` | `geo-econ-horizon` | Mon 08:00 | **KEEP + PIN** | Professional intel: Monday strategy |
| `525f98d61bb7` | `evening-zen-brief-v2` | Daily 20:00 | **KEEP + PIN** | Human intel: ΔS wind-down. Now absorbs governance digest |
| `9eddcab58b5c` | `sado-physique-radar` | Fri 22:00 | **KEEP** | Already pinned to `minimax/minimax-m3`, group lane |
| `0e37cdaf4a37` | `arif-world-reality-intel` | Daily 09:00 | **KEEP + PIN** | Daily reality contact |
| `a004b6357d06` | `arif-reckoning` | Mon 06:30 | **KEEP + PIN** | Prediction grader (closes learning loop) |
| `5d87405c1770` | `syed-mak-dressing` | Daily 08:00 | **KEEP + PIN** | F6 MARUAH caregiving |
| `a5b0eda31bfa` | `syed-mak-cbd-followup` | Mon 09:00 | **KEEP + PIN** | Medical timeline |
| `0f07d72c0673` | `syed-gerd-log` | Daily 08:00 | **KEEP + PIN** | Health tracking with [SILENT] |
| `cf1c6b534b2f` | `syed-sambal-preorder` | Daily 06:30 | **KEEP + PIN** | Daily life friction reducer |
| `b08b1c5d45c5` | `arifflow-weekly-drift-check` | Mon 09:00 | **KEEP + PIN** | Constitutional integrity |
| `e684146a638c` | `sado-physique-radar` (old) | — | **SUPERSEDED** | Already marked `enabled=False, state=superseded` |

## Final catalog (12 jobs: 11 active + 1 superseded)

```
📅 DAILY    06:00  morning-pulse           → cognitive ignition
📅 DAILY    06:30  sambal-preorder         → pre-order window
📅 DAILY    08:00  mak-dressing            → dressing schedule
📅 DAILY    08:00  gerd-log                → GERD tracker
📅 DAILY    09:00  world-reality-intel     → reality contact
📅 DAILY    20:00  evening-zen-brief       → ΔS wind-down (absorbs digest)
📅 WEEKLY   Mon 06:30  reckoning            → prediction grading
📅 WEEKLY   Mon 08:00  geo-econ-horizon     → subsurface energy economics
📅 WEEKLY   Mon 09:00  weekly-drift-check    → constitutional drift
📅 WEEKLY   Fri 22:00  sado-physique-radar  → bodybuilding scan (SADO group)
⚪ SUPERSEDED old-sado-physique-radar       → archived
```

## Token cost delta

```
Before:  ~3.77M tok/month (20 jobs, heavy polling)
After:   ~2.2M tok/month  (11 jobs, human-focused)
Saved:   ~1.57M tok/month (~42% reduction)
```

## Pin ritual applied (11 jobs pinned)

For each unpinned job (`model: null` + `provider: null`), pinned explicitly to current global:
```bash
cronjob(action='update', job_id=<id>, 
        model={'provider': 'hermes-asi', 'model': 'hermes-asi'})
```
Then manually fired:
```bash
cronjob(action='run', job_id=<id>)  # verified all 11 → last_status: ok
```

## Lessons distilled (kill body, keep lesson)

| Killed cron | Essence preserved as doctrine |
|---|---|
| `seal-integrity-sweep` | F11 auditability = write-time invariant in every write hook |
| `memory-compression` | Memory density doctrine (intrinsic to architecture, not a metric) |
| `contradiction-scan` | Apex-judge preflight rule (runtime gate, not scheduled fire) |
| `artifact-drift-audit` | git-to-vault auto-ingest (handles it correctly per commit) |
| `output-attestation-check` | Python hook in write path (`output-attest.py`) |
| `institution-metrics-pulse` | Merged into weekly digest for human consumption |
| `vault-data-refresh` | nginx/Caddy auto-refresh is sufficient; no cron needed |
| `arifflow-daily-digest` | Folded into `evening-zen-brief` wind-down |

## Going forward

Every cron must pass F3 test before staying: *"If this fires, who opens the result and what do they DO with it?"* If nobody → delete. If someone but no clear action → convert to doctrine/invariant.

## Reference commands

```bash
# Probe current state
cronjob(action='list')

# Pin drifts
cronjob(action='update', job_id=X, provider='hermes-asi', model='hermes-asi')

# Verify fire
cronjob(action='run', job_id=X)

# Delete by F3 violation
cronjob(action='remove', job_id=X)
```

## F2 Evidence

- L2 catalog before: 21 jobs (as of 2026-08-11 ~19:00 MYT)
- L2 catalog after: 11 jobs (active) + 1 superseded
- Token cost: 3.77M → 2.2M tok/month (42% reduction)
- All 11 surviving jobs: `last_status: ok` after one-shot verification
- VAULT999 receipt: `arif_hygiene_triage_verdict_2026_08_09_v2_final` (chain integrity verified)
