# 04 — Cron & Monitors Audit: the Scheduled / Autonomous Layer

> **Report:** `acah-audit-2026-09-19` · surface 04 of the ACAH audit
> **Authority:** delegated subagent, read-only inspection
> **Host:** KVM8 (truth node) · cross-probed KVM4 (100.64.0.5) read-only over SSH
> **Session time:** 2026-09-19 ~10:45–11:05 MYT
> **Mode:** STRICTLY READ-ONLY. `jobs.json` not edited. No job triggered. No service restarted. All DB access via `mode=ro` URI.

**Definitions used** (from the task's definitional test):
`THEATRE` = the control cannot withhold or deliver what it claims · `DISABLED` = could act but is switched off · `BROKEN` = crashes or never fires · `REAL` = does what it says · `UNPROVEN` = no evidence either way.
For jobs the binding test is: **does the output reach a human, or is it produced and swallowed?**

---

## 0. Headline

The scheduled layer is **not governed, it is abandoned**. 26 of 40 jobs are `enabled:false`. Every single one of those 26 cites a successor — and **three of the three successor mechanisms are phantoms**:

| Successor claim | Jobs relying on it | Verified reality |
|---|---|---|
| "converted to `/etc/cron.d/hermes-legacy-scripts`" | 14 | **The file does not exist on KVM8 or KVM4.** `find` across `/` returns nothing. |
| "superseded by canary `canary-<name>`" | 6 | The canaries ran **once** in a 20-minute window on 2026-09-17 and were then **deleted from `jobs.json`**. The live copies sit on KVM4 — whose Hermes cron ticker **has been dead since 2026-09-12 17:03**. |
| "MIGRATED to KVM4 gateway book" | 3 | On KVM4 the target jobs are either **absent** (`reddit-daily-monitor`) or **disabled with `paused_reason: null`** (`arif-morning-pulse`, `arif-world-reality-intel`). Dead on both hosts. |

Net effect: **~20 human-facing and governance lanes were switched off in a deliberate cleanup that was never completed on the far end.** The system looks governed; a large part of it is silent.

---

## 1. `jobs.json` census — the 40 jobs

**Command**
```
python3 -c "import json;d=json.load(open('/root/.hermes/cron/jobs.json'));print(d['updated_at'],len(d['jobs']))"
```

**Observed:** `updated_at = 2026-09-19T08:02:13.140998+08:00`, `jobs = 40`
**Measured split:** `TOTAL 40 | enabled 14 | disabled 26` — matches the briefing's 40/26 exactly.

### 1.1 All 26 disabled jobs, verbatim fields

| # | name | schedule | paused_at | paused_reason (actual value) | last_run_at | last_status |
|---|---|---|---|---|---|---|
| 1 | arif-morning-pulse | `0 6 * * *` | 2026-09-04T00:17:32Z | `MIGRATED to KVM4 gateway book 2026-09-04 FI-008 — do not re-enable here (double-fire risk)` | 2026-09-03T06:02:30+08 | ok |
| 2 | arif-world-reality-intel | `0 9 * * *` | 2026-09-04T00:17:32Z | `MIGRATED to KVM4 gateway book 2026-09-04 FI-008 — do not re-enable here (double-fire risk)` | 2026-09-03T09:04:39+08 | ok |
| 3 | reddit-daily-monitor | `0 9 * * *` | 2026-09-04T00:35:25Z | `MIGRATED to KVM4 2026-09-04 FI-008 tail` | 2026-09-03T09:07:22+08 | ok |
| 4 | output-attestation-check | `every 120m` | 2026-09-04T00:33:43Z | `converted to /etc/cron.d/hermes-legacy-scripts 2026-09-04 — do not re-enable (double-fire)` | 2026-09-03T10:56:22+08 | ok |
| 5 | institution-metrics-pulse | `every 360m` | 2026-09-04T00:33:43Z | *(same legacy-scripts string)* | 2026-09-03T06:21:53+08 | ok |
| 6 | Forge→Vault Auto-Ingest | `every 60m` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T12:01:46+08 | ok |
| 7 | hermes-upstream-drift-watch | `0 4 1 * *` | 2026-09-04T00:33:43Z | *(same)* | **None** | **None** |
| 8 | trajectory-harvest | `every 360m` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T11:40:41+08 | ok |
| 9 | seal-integrity-sweep-script | `17 3 * * 0` | 2026-09-04T00:33:43Z | *(same)* | 2026-08-30T03:17:48+08 | ok |
| 10 | artifact-drift-audit-script | `53 1 * * *` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T01:53:34+08 | ok |
| 11 | evening-zen-brief | `0 20 * * *` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-02T20:51:19+08 | ok |
| 12 | syed-mak-dressing | `0 8 * * *` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T08:00:20+08 | ok |
| 13 | syed-gerd-log | `0 8 * * *` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T08:00:21+08 | ok |
| 14 | syed-sambal-preorder | `30 6 * * *` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T06:30:50+08 | ok |
| 15 | stale-group-session-cleaner | `every 360m` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T11:25:31+08 | ok |
| 16 | forge-vision-densify-summary | `55 23 * * *` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-02T23:55:08+08 | ok |
| 17 | federation-state-backup | `0 3 * * *` | 2026-09-04T00:33:43Z | *(same)* | 2026-09-03T03:01:48+08 | ok |
| 18 | geo-econ-horizon | `0 8 * * 1` | 2026-09-16T16:56:36Z | `superseded by canary canary-geo-econ-horizon (APEX-ZEN 777 swap 2026-09-17); tombstones.jsonl` | 2026-08-31T08:04:56+08 | ok |
| 19 | iron-radar | `0 12 * * 5` | 2026-09-16T16:56:36Z | `superseded by canary canary-iron-radar (APEX-ZEN 777 swap 2026-09-17); tombstones.jsonl` | 2026-08-28T12:02:44+08 | ok |
| 20 | arif-reckoning | `30 6 * * 1` | 2026-09-16T16:56:36Z | `superseded by canary canary-arif-reckoning (…)` | 2026-08-24T06:33:30+08 | ok |
| 21 | arifflow-daily-governance-digest | `0 22 * * *` | 2026-09-16T16:56:36Z | `superseded by canary canary-arifflow-governance-digest (…)` | 2026-09-16T22:02:02+08 | ok |
| 22 | morning-brief-wakebus-audit | `0 7 * * 1,3,5` | 2026-09-16T16:56:36Z | `superseded by canary canary-morning-brief-wakebus (…)` | 2026-09-16T07:03:15+08 | ok |
| 23 | malaysia-intel-weekly | `0 10 * * 1` | 2026-09-16T16:56:36Z | `superseded by canary canary-malaysia-intel-weekly (…)` | 2026-08-31T10:01:42+08 | ok |
| 24 | syed-mak-cbd-followup | `0 9 * * 1` | 2026-09-17T09:31:35+08 | `F13 chat directive 2026-09-17: pull-model — Syed replies on his own if he needs it; machine must not initiate. Lane silently unfired since 2026-08-31. Resurrect only on Syed's explicit request.` | 2026-08-31T09:02:21+08 | ok |
| 25 | **organ-health-sentinel** | `every 15m` | **2026-08-30T13:22:00+08** | **`None`** | 2026-08-30T13:10:13+08 | ok |
| 26 | **Executive Briefing — Daily Edition** | `0 9 * * *` | **2026-09-18T09:39:36+08** | **`None`** | **None** | **None** |

### 1.2 Classification of the 26

| Class | Count | Which |
|---|---|---|
| **Deliberate — documented reason** | **24** | #1–#24 |
| · of which: superseded by canary | 6 | #18–#23 |
| · of which: "converted to legacy-scripts" | 14 | #4–#17 |
| · of which: "MIGRATED to KVM4" | 3 | #1–#3 |
| · of which: F13 chat directive | 1 | #24 |
| **Forgotten / silently stopped — `paused_reason: null`** | **2** | #25 `organ-health-sentinel`, #26 `Executive Briefing — Daily Edition` |
| Unknown | 0 | — |

**Measured answer:** **24 deliberate, 2 silently stopped.**

But "deliberate" ≠ "successful". Of the 24 deliberate pauses, **20 name a successor that does not exist on this host** (14 + 6), and 3 name a host whose scheduler is dead. Only #24 (Syed CBD follow-up) is a genuinely complete, correctly-reasoned shutdown.

Note #7 (`hermes-upstream-drift-watch`) is disabled with a "converted" reason but recorded **`last_run_at: None` / `last_status: None`** — it is the monthly `0 4 1 * *` job; it was paused 2026-09-04 and never produced a single execution record. Its "conversion" has no original to convert.

### 1.3 The `lane-routing.json` contradicts its own stated source

`/root/.hermes/cron/lane-routing.json` line 3 declares:
```json
"source": "/root/.hermes/cron/jobs.json (live, not a story)",
```
Measured (`python3` set-difference of all 20 routed names against `jobs.json`):
```
lane-routing routes: 20  | names present in jobs.json: 0 | DANGLING: 20
```
**0 of 20** named routes match a job that exists. (`arif-executive-briefing` is the one entry with a plausible rename successor, `Executive Briefing — Daily Edition` — which is itself disabled.) The file asserts it is "not a story"; it is a routing table for twenty jobs that no longer exist. **Classified THEATRE.**

---

## 2. The three successor claims, verified independently

### 2.1 `hermes-legacy-scripts` does not exist (14 jobs)

**Commands**
```
cat /etc/cron.d/hermes-legacy-scripts
find / -maxdepth 6 -name '*legacy-scripts*' 2>/dev/null
grep -rn 'hermes-legacy-scripts' /etc/cron.d /etc/crontab
```
**Observed**
```
cat: /etc/cron.d/hermes-legacy-scripts: No such file or directory (os error 2)
(done)          <-- find returned nothing
                <-- grep returned nothing
```
Same check on KVM4:
```
ls: cannot access '/etc/cron.d/hermes-legacy-scripts': No such file or directory
```
**What *does* exist** is an unrelated, earlier ban directory `/etc/cron.d/.hermes-cron-ban-20260904/` (created Sep 4 12:13) containing 6 `*.disabled` files — `arif-verify-attestation`, `arifos-dreamer`, `arifos-site-audit-pipeline`, `arifos-vault-tail`, `status-federation`, `zai-federation-watchdog`. **None of them corresponds to the 14 jobs**, except loosely `arif-verify-attestation` ↔ `output-attestation-check`, which are different scripts.

⇒ The stated conversion target was never created. The 14 jobs are **not migrated; they are gone.** Classified: **14 × DISABLED-with-false-reason** (the pause note is a claim the filesystem does not support).

### 2.2 The canary swap — canaries ran once, then were deleted

Execution records for the six canary job-ids (`executions.db`):
```
canary-arif-reckoning                1 exec  completed  2026-09-17T00:46
canary-arifflow-governance-digest    2 exec  completed  2026-09-17T00:45 → 2026-09-17T22:00
canary-geo-econ-horizon              1 exec  completed  2026-09-17T00:36
canary-iron-radar                    2 exec  completed  2026-09-17T00:40 → 2026-09-18T12:00
canary-malaysia-intel-weekly         1 exec  completed  2026-09-17T00:43
canary-morning-brief-wakebus         2 exec  completed  2026-09-17T00:35 → 2026-09-18T07:00
```
They ran, proved the lane, and were then removed from `jobs.json`. Name-matching against today's 40 jobs:
```
canary-geo-econ-horizon:            *** NOT PRESENT IN jobs.json ***
canary-iron-radar:                  *** NOT PRESENT IN jobs.json ***   (only "CANARY iron-radar", a different id)
canary-arif-reckoning:              *** NOT PRESENT IN jobs.json ***
canary-arifflow-governance-digest:  *** NOT PRESENT IN jobs.json ***
canary-morning-brief-wakebus:       *** NOT PRESENT IN jobs.json ***
canary-malaysia-intel-weekly:       *** NOT PRESENT IN jobs.json ***
```
Only `CANARY iron-radar` survives (enabled, `0 12 * * 5`, last delivered 2026-09-18). **The other five were swapped in, tested once, and then swapped out to nothing.** The disable note says "superseded by canary X"; in five of six cases there is no X left.

### 2.3 KVM4 is the claimed successor host — and its scheduler has been dead for 7 days

The 2026-09-04 pauses all cite KVM4. i, Read-only over SSH:

```
ssh root@100.64.0.5  →  hostname = srv1946043
```
KVM4 `jobs.json`: `total 13 enabled 10 disabled 3`, `updated_at 2026-09-13T00:04:49`

| KVM4 enabled job | schedule | KVM4 last_run_at |
|---|---|---|
| arif-reckoning | `30 6 * * 1` | 2026-09-12T23:33:31 |
| arifflow-daily-governance-digest | `0 22 * * *` | 2026-09-12T23:29:15 |
| geo-econ-horizon | `0 8 * * 1` | 2026-09-12T23:30:08 |
| iron-radar | `0 12 * * 5` | 2026-09-12T23:29:44 |
| malaysia-intel-weekly | `0 10 * * 1` | 2026-09-12T23:31:10 |
| morning-brief-wakebus-audit (+`-rest`) | `0 7 * * 1,3,5` / `0 7 * * 0,2,4,6` | 2026-09-12T23:37:49 |
| syed-mak-cbd-followup | `0 9 * * 1` | 2026-09-12T23:30:04 |
| vps-gdrive-daily-backup | `0 2 * * *` | 2026-09-12T23:29:36 |
| Dream Engine — 72h Reasoning Distillation | `0 */72 * * *` | 2026-09-13T00:00:38 |
| **arif-morning-pulse** | `0 6 * * *` | **disabled, `paused_reason: None`** |
| **arif-world-reality-intel** | `0 9 * * *` | **disabled, `paused_reason: None`** |
| dream-engine-distillation | — | disabled, `duplicate of working cron-based Dream Engine — retired` |

**Is KVM4 actually running them? No:**
```
/root/.hermes/cron/executions.db      mtime Sep 12 16:00 · 17 rows · max(claimed_at) = 2026-09-13T00:00:31
/root/.hermes/cron/ticker_heartbeat   -rw------- 18 bytes  Sep 12 17:03  → 1789232611.6006005
/root/.hermes/cron/ticker_last_success                     Sep 12 17:03
pgrep -af "hermes|gateway"   →  2573762 openclaw-gateway      (no Hermes process)
systemctl is-active hermes-gateway.service hermes-health.service  →  inactive / inactive
systemctl list-unit-files "*hermes*"  →  0 unit files listed
```
⇒ **KVM4's Hermes cron ticker last beat 2026-09-12 17:03.** Its ten `enabled:true` jobs are **DISABLED in effect** — the scheduler is not running at all. `arif-morning-pulse` (the 06:00 daily ignition) and `arif-world-reality-intel` are additionally switched off *with no reason recorded*.

⇒ **Combined result:** the six canary-swapped governance lanes are off on KVM8 and dead-on-arrival on KVM4. Nothing has produced them since **2026-09-16** (KVM8) / **2026-09-12** (KVM4).

---

## 3. `executions.db` / `deliveries.db` — measured

**Command (read-only URI, never opened read-write)**
```
sqlite3 -readonly "file:/root/.hermes/cron/executions.db?mode=ro" '<query>'
```

### 3.1 Totals

```
executions                = 560 rows
status:   completed 506 · failed 52 · unknown 2
source:   builtin 509 · direct 51
delivery_outcome:  suppressed 359 · NULL 132 · delivered 66 · failed 3
max(claimed_at)   = 2026-09-19T08:00:10.881077+08:00        (live, ticking)

deliveries.db:  deliveries = 31   (status: delivered 31 — all 31 terminal-delivered)
                delivery_tombstones = 0
```
**Measured ratio: 66 delivery outcomes recorded as `delivered` against 359 `suppressed` and 132 unrecorded.** Four-fifths of all execution output never left the box.

### 3.2 Per-job delivery breakdown (aggregated by NAME, because IDs were migrated)

`jobs.json` job IDs were migrated from 12-hex to name-slugs (e.g. `agent-card-drift-check` exists both as `8b2ccdb9bce5` in the output tree and as its own slug in `jobs.json`). Aggregating by **name** across both id-spaces (`_idmap.json`, `_agg.json` written alongside this report):

| job | en | exec | ok | fail | **delivered** | suppressed | del-failed | last claim |
|---|---|---|---|---|---|---|---|---|
| cron-receipt-bridge | GONE | **143** | 143 | 0 | **0** | 107 | 0 | 2026-09-09 |
| session-auto-trace | GONE | **94** | 64 | 30 | **0** | 94 | 0 | 2026-09-10 |
| pull-openclaw-traces | GONE | **93** | 92 | 1 | **0** | 90 | 0 | 2026-09-10 |
| 🜂 Site drift watch | **Y** | 52 | 32 | 20 | **20** | 32 | 0 | 2026-09-18 |
| experience-surface-regen | GONE | 15 | 15 | 0 | **0** | 7 | 0 | 2026-09-08 |
| arif-executive-briefing | GONE | 12 | 12 | 0 | **0** | 5 | 0 | 2026-09-08 |
| arif-eod-wrap | GONE | 10 | 8 | 2 | 2 | 0 | 0 | 2026-09-04 |
| syed-evening-wrap | GONE | 10 | 9 | 1 | 2 | 0 | 0 | 2026-09-04 |
| arif-market-brief | GONE | 9 | 8 | 1 | 2 | 0 | 0 | 2026-09-04 |
| arif-midday-alert | GONE | 8 | 8 | 0 | 2 | 0 | 0 | 2026-09-04 |
| capability-fitness-cycle | GONE | 8 | 8 | 0 | **0** | 8 | 0 | 2026-09-10 |
| syed-afternoon-chk | GONE | 8 | 8 | 0 | 1 | 1 | 0 | 2026-09-04 |
| **agent-card-drift-check** | **Y** | 8 | 8 | 0 | **0** | 8 | 0 | 2026-09-16 |
| arif-morning-readiness | GONE | 7 | 7 | 0 | 5 | 0 | 0 | 2026-09-08 |
| snapshot-morning / -afternoon | GONE | 6 / 6 | 6 / 6 | 0 | **0 / 0** | 3 / 3 | 0 | 2026-09-07 |
| arif-brief-deliver | GONE | 6 | 6 | 0 | **0** | 5 | 0 | 2026-09-09 |
| arif-morning-pulse | n | 0 | 0 | 0 | 0 | 0 | 0 | — |
| maintenance-health-loop | GONE | 5 | 5 | 0 | 1 | 4 | 0 | 2026-09-10 |
| snap-evening-03 | GONE | 7 | 6 | 1 | **0** | 2 | 0 | 2026-09-04 |
| **Malaysia Weekly Reality Probe** | **GONE** | 4 | 4 | 0 | **0** | 1 | **3** | 2026-09-12 |
| **gate-integrity-check** | **Y** | 2 | 2 | 0 | **0** | 2 | 0 | 2026-09-19 |
| VPS Backup | **Y** | 4 | 4 | 0 | **4** | 0 | 0 | 2026-09-16 |
| sentinel-tripwire | **Y** | 4 | 4 | 0 | **4** | 0 | 0 | 2026-09-18 |
| docforge-edition-daily | **Y** | 4 | 4 | 0 | **4** | 0 | 0 | 2026-09-18 |
| attention-closure | **Y** | 8 | 8 | 0 | 6 | 2 | 0 | 2026-09-16 |
| ALPHA-ZEN 1 / 2 / 3 | **Y** | 2 / 2 / 2 | 2 | 0 | **2 / 2 / 2** | 0 | 0 | 2026-09-19 |
| CANARY iron-radar | **Y** | 4 | 4 | 0 | 2 | 2 | 0 | 2026-09-17 |
| Weekly Governance Digest | **Y** | 2 | 2 | 0 | 1 | 1 | 0 | 2026-09-17 |
| warga-lifecycle-sweep | GONE | 1 | 1 | 0 | **0** | 1 | 0 | 2026-09-14 |
| organic-rebuild-watch — seal/HOLD only | GONE | 1 | 0 | **1** | 1 | 0 | 0 | 2026-09-13 |

### 3.3 Jobs that ran and NEVER delivered

**Criterion:** ≥3 completed executions, **0** `delivered` outcomes, ever.

```
Malaysia Weekly Reality Probe   exec=4    suppr=1   DEL-FAILED=3   last=2026-09-12
arif-brief-deliver              exec=6    suppr=5                  last=2026-09-09
capability-fitness-cycle        exec=8    suppr=8                  last=2026-09-10
arif-executive-briefing         exec=12   suppr=5                  last=2026-09-08
cron-receipt-bridge             exec=143  suppr=107                last=2026-09-09
experience-surface-regen        exec=15   suppr=7                  last=2026-09-08
pull-openclaw-traces            exec=93   suppr=90                 last=2026-09-10
session-auto-trace              exec=94   suppr=94                 last=2026-09-10
snapshot-morning                exec=6    suppr=3                  last=2026-09-07
snapshot-afternoon              exec=6    suppr=3                  last=2026-09-07
snapshot-evening                exec=7    suppr=2                  last=2026-09-04
agent-card-drift-check          exec=8    suppr=8                  last=2026-09-16   <-- ENABLED today
```

**The single sharpest finding here is `cron-receipt-bridge`.** 143 executions, zero deliveries, 107 suppressions — and its own output payload carries:

```json
{"ts":"2026-09-14T15:13:02+08:00","ingested":2,"ingest_fail":0,"escalated":[],
 "skipped":0,"job_verifies":1,"telegram_delivery_failures":24,"vitals_written":true}
```
*(source: `/root/.hermes/cron/output/25c2e9ff80d2/2026-09-14_15-13-02.md`)*

**The bridge that counts Telegram delivery failures itself never delivers, and its `escalated` list — the field that would tell a human — is empty while `telegram_delivery_failures` reads 24.** The failure counter increments and nothing is escalated. **THEATRE.**

**Second sharpest: `Malaysia Weekly Reality Probe`.** 4 executions, 4 completed, **3 delivery failures**, 1 suppressed, 0 delivered. It is named in `lane-routing.json` under `A2A → telegram:-1003753855708`. **A monitor whose whole job was to probe reality to a group and whose delivery failed 3 of 4 times, now deleted from `jobs.json` entirely. It could not have alerted anyone.** **BROKEN.**

---

## 4. The delivery gate — exact suppression conditions

The decision lives in `/usr/local/lib/hermes-agent/cron/scheduler.py`.

### 4.1 The taxonomy function (line 2562)

```python
def _classify_delivery_outcome(*, delivery_error, should_deliver, unresolved_origin,
                               normalized_deliver, incident_acked, success, delivery_queued=None) -> str:
    if delivery_error:                                    return "failed"
    if should_deliver and delivery_queued:                return "queued"
    if should_deliver and unresolved_origin:              return "not_configured"
    if should_deliver and normalized_deliver != "local":  return "delivered"
    if incident_acked and not success:                    return "suppressed_acked"
    return "suppressed"                                   # <-- the default sink
```
**`suppressed` is the fall-through.** Anything not positively delivered lands there.

### 4.2 The five ways output is swallowed (line 2663–2725)

| # | Condition | Code / line | Effect |
|---|---|---|---|
| 1 | **Empty/whitespace-only output** | `d.should_deliver = bool(deliver_content.strip()) and not _silent_alert` (L2700) | silent; `no_agent` script jobs → "**Status:** silent (empty output)" (L1310-1312) |
| 2 | **Agent chose silence** | `_is_cron_silence_response` (L2713) | suppressed if the whole response, or its **first/last line**, is exactly `[SILENT]` / `SILENT` / `NO_REPLY` / `NO REPLY` |
| 3 | **Model unreachable + auto-retry pending** | L2701-2708 → `unreachable_retry.will_retry` | failure notice held back |
| 4 | **Fire-claim ownership lost** | L2720-2722 | suppressed |
| 5 | **`deliver: local`** | L2573 `normalized_deliver != "local"` | *even when `should_deliver` is True*, classified `suppressed` — the output stays on disk by design |

Token set, defined at `/usr/local/lib/hermes-agent/gateway/response_filters.py:15`:
```python
LIVE_GATEWAY_SILENT_MARKERS = frozenset({"[SILENT]", "SILENT", "NO_REPLY", "NO REPLY"})
```

### 4.3 The monitor gate — a sixth, structural suppression (line 1317)

```python
def _apply_monitor_gate(...):
    """Monitor gate (hash-suppressed change detection). Must run BEFORE any agent machinery so an
    unchanged tick costs no LLM/delivery."""
    if not _mon.changed:
        logger.info("Job '%s': monitor output unchanged — suppressing agent run", job_id)
        return (True, f"{header}**Status:** no_change (agent run suppressed)\n", SILENT_MARKER, None), extra_prompt
```
Only **one** job today carries monitor state: `sentinel-tripwire` (`monitor_script: sentinel-tripwires.py`, `monitor_state.last_output_hash: b8bd5973…`). It **does** deliver (4/4), because a change was detected each time.

### 4.4 Verdict on the gate itself

The gate is **not** broken and not inherently theatrical: it correctly distinguishes empty output, agent-chosen silence, local-only lanes, and monitor no-change ticks, and it alerts on failure paths (`Blocked-config` alerts once; monitor *source* failure is an error, never a change — L1331-1342 is explicitly written to stop a broken monitor going quiet). The **suppression machinery is sound**. The theatre is in **which jobs sit behind it and whether their "local" / "silent" configuration is honest.**

**The one genuinely damning configuration:** `cron-receipt-bridge` is listed in `lane-routing.json` under `A2M_local` and so is `deliver: local` — i.e. permanently unable to deliver — while carrying a `telegram_delivery_failures` counter and an `escalated[]` field. It is instrumented to report a delivery problem it structurally cannot report.

### 4.5 Two silent-by-design monitors — assessed fairly

`agent-card-drift-check` (`agent-card-drift-check.py`) and `gate-integrity-check` (`gate-integrity-verify.py`) are `no_agent` script jobs whose 8/8 and 2/2 "suppressed" outcomes are **"silent (empty output)"** (verified in `/root/.hermes/cron/output/8b2ccdb9bce5/2026-09-19_05-30-56.md` and `/root/.hermes/cron/output/5d11524f35a5/2026-09-19_06-15-59.md`). Reading both scripts: this is the documented **alert-on-change** watchdog pattern (`Contract: EMPTY STDOUT = SILENT`), and both print a `⚠` warning on the *cannot-witness* path (detector missing, timeout, unparseable manifest). So their silence is **consistent with design, not proof of deadness**.

**Classified `UNPROVEN`, not THEATRE** — the alerting path has never fired in 10 combined executions, so we have no evidence it can. That is the honest reading.

Two enabled jobs show **zero** execution rows — `sentinel-heartbeat` (created 2026-09-18T08:58, next Mon 2026-09-21 09:00) and `amin-acl-weekly-checkin` (created 2026-09-18T22:38, next Sun 2026-09-20 20:00). **Neither has missed a slot yet.** Not defects. `sentinel-heartbeat` is in fact an anti-theatre control ("Weekly proof-of-life for the three sentinel tripwires… Deliberately unconditional — the absence of th[is] report is itself the alarm").

---

## 5. systemd layer

**Commands**
```
systemctl list-timers --all --no-pager --plain
systemctl list-units --all --state=failed --no-pager --plain
systemctl list-unit-files --all --no-pager --type=timer
```

**Failed units:**
```
UNIT LOAD ACTIVE SUB DESCRIPTION
0 loaded units listed.
```
**Clean. Zero failed units.** (Note: `list-unit-files` does show `arif-agent-worker.service`, `hermes-agent-mcp.service`, `hermes-mcp.service` as **masked** — masked is intentional, not failed.)

**Timer census:**
```
enabled 55 · disabled 32 · masked 8 · static 2      (97 timer unit files known to systemd)
systemctl list-timers (no --all) = 52 active/scheduled; with --all = 55
```
**Dangling timers** (a `.timer` whose `Unit=`/`Requires=` target `.service` does not exist on disk anywhere in the unit search path — scan over `/etc/systemd/system`, `/lib/systemd/system`, `/usr/lib/systemd/system`, `/run/systemd/system`):

| timer | requires | state | classification |
|---|---|---|---|
| **dream-engine** | dream-engine.service | loaded / **inactive** / disabled | DANGLING-DORMANT |
| **dream-engine-weekly** | dream-engine-weekly.service | loaded / **inactive** / disabled | DANGLING-DORMANT |
| **dream-engine-monthly** | dream-engine-monthly.service | loaded / **inactive** / disabled | DANGLING-DORMANT |
| **apex-health** | apex-health.service | `unit file: disabled` | DANGLING-DORMANT |
| **arifosmcp-network-heal** | arifosmcp-network-heal.service | loaded / **inactive** / disabled | DANGLING-DORMANT |

```
$ for t in arifosmcp-network-heal dream-engine dream-engine-weekly dream-engine-monthly; do ... done
arifosmcp-network-heal     loaded inactive disabled
dream-engine               loaded inactive disabled
dream-engine-weekly        loaded inactive disabled
dream-engine-monthly       loaded inactive disabled

$ systemctl list-unit-files --all | grep -E '^apex'
apex-health.timer     disabled    enabled
```
**5 dangling timers, all dormant.** None is currently causing a failure — which is *why* nothing flagged them: a disabled dangling timer is invisible to `--state=failed` and silent in `list-timers --all` output once it has no `NEXT`. Dead controls produce no alert.

**Negative finding worth stating:** the 40+ live federation timers (`federation-state`, `fed-sync`, `arifos-drift-check`, `frame-probe`, `vault999-backup`, `arifos-backup`, `gov-a008-arifflow-sync`, `gov-a009-git-to-vault`, `hermes-liveness`, `sct-renew`, `fq-probe`, …) all show recent `LAST` timestamps in the same minute-to-hours range. **The systemd half of the autonomous layer is REAL and healthy.** The rot is concentrated in the Hermes cron half and in the vision/care/digest lanes.

---

## 6. Independent check of `dream-federation-2026-09-12` claims

Report audited: `/root/AAA/reports/dream-federation-2026-09-12/04-G3A-RECONCILIATION.md` (58 lines, 2026-09-12).

| Claim in the report | Independently verified today (2026-09-19) | Status |
|---|---|---|
| `dream-engine.timer` · `-weekly` · `-monthly`: "**disabled + inactive**; each `Requires=` a service file that **DOES NOT EXIST** → dangling, dormant (never fired)" | Re-probed. All three: `loaded inactive disabled`; `dream-engine*.service` absent from every unit path. | **CONFIRMED — still true today** |
| "`Documentation=` links dead (`/root/.hermes/skills/dream-engine/SKILL.md`)" | All 3 timers still carry `Documentation=file:/root/.hermes/skills/dream-engine/SKILL.md`; that path does not exist (engine now lives at `/root/AAA/dream_engine/`). | **CONFIRMED** |
| "`dreams/` = ONLY `consolidate.py` (+ bak). **Absent:** defuse.py · housekeeping.py · rehearse.py · recombine.py · scheduler/ · state/manifest.yaml · state/evidence/ · state/queue.json" | `ls /root/AAA/dream_engine/dreams` → `consolidate.py`, `consolidate.py.bak-20260909T0932Z`. `find /root -maxdepth 5` for `defuse.py|rehearse.py|recombine.py|housekeeping.py` → **nothing**. `state/` holds only `last_dream.json`. | **CONFIRMED — still true today** |
| "four **phantom passes**" (nightly defuse+housekeep; weekly rehearse+recombine) | Stronger evidence than the report had: `last_dream.json` contains **13 entries / 10 distinct dates** and the only `pass` value ever recorded is `consolidate`. | **CONFIRMED, and the report's "9 runs" figure is now stale (13 entries)** |
| "one working nightly battery … `state/last_dream.json` fresh … 9 runs recorded, 2026-08-21 → 2026-09-09" | `arif-dream.timer` enabled+active, last fired **2026-09-18 22:52:40**, `arif-dream.service` exited `status=0/SUCCESS`. `last_dream.json` 13 entries, **2026-08-21 → 2026-09-18**. | **CONFIRMED — and it is still alive 7 days later** |
| "`~80% map, 20% territory`" | Not a measurable claim; directionally supported (1 of 5 designed stages exists). | *Not falsifiable — no verdict* |
| "`liveness.json` claims `\"liveness_status\":\"ALIVE\"`; `last_invoked:null`, `invocation_count:0` → liveness claim without territory" | **Partial.** No `liveness.json` exists under `/root/AAA/dream_engine` today — the report's instance is gone from that path. But the pattern is alive and **worse** elsewhere: e.g. `/root/AAA/skills-deprecated/FLAME-operator/liveness.json` and `/root/AAA/skills-retired-20260826/FORGE-mcp-smoke-test/liveness.json` both read `{"liveness_status":"ALIVE","last_invoked":null,"invocation_count":0,…}` — **retired/deprecated skills still self-reporting ALIVE with zero invocations.** | **CLAIM MOSTLY CONFIRMED (pattern), exact instance NOT LOCATED** |
| "Live DB schema: `to_regclass` `arifosmcp_memory_records` = EXISTS" | Not re-probed (out of this surface's scope). | **NOT CHECKED** |

**Verdict on the report:** it is **honest and accurate**. Every claim I could re-run still holds, seven days later, and one (`phantom passes`) is now *better* evidenced. It also correctly withdrew its own P1 — a rare, credible move. The one claim I could not reproduce exactly is the `liveness.json` at the dream-engine path.

**But its bottom line understates the problem.** The 2026-09-12 report scoped itself to the dream engine. The same defect class — *"absence without detection"* — is present at 10× the scale in the cron layer: `hermes-legacy-scripts` (14 jobs), the deleted canaries (5 jobs), and the dead KVM4 ticker. **The report said "pipeline mostly unbuilt, undetected". Today the accurate sentence is: "pipeline mostly unbuilt, undetected, and the detector that was supposed to notice has itself been switched off."**

---

## 7. Extract from the HOLD-surge canon (monitors / alerts)

Read: `/root/AAA/canon/HOLD-COUNT-SURGE-DIAGNOSTIC-2026-09-19.md` (113 lines) and `/root/AAA/canon/HOLD-SURGE-RCA-2026-09-19.md` (128 lines).

**Neither document contains any finding about a monitor or alert firing spuriously.** Both are single-subject diagnostics of `flow_health.invariants.hold_count`. What they *do* give us is negative evidence about the alerting surface:

| Extract | Line | Significance |
|---|---|---|
| `{"status": "SEAL", "total_alerts": 0, "alerts": []}` — A-FORGE `forge_shell_alert_history` | RCA §2.2 (L31-37) | The alert subsystem reports **zero alerts, ever**. Cited as proof of calm; equally readable as proof that the alert path has never been exercised. `UNPROVEN` either way — the document does not distinguish. |
| "`flow_gov_events` returns 7 events — the same set I've probed at 03:13 and 03:30" · "**No new gov events since 2026-09-16.**" | DIAGNOSTIC §3 (L43-53), restated RCA §2 | The governance event feed has been **static for 3 days** while +552 holds accumulated. A live governance feed that does not move during a 552-event surge is indistinguishable from a feed that has stopped. **The docs assert "no governance events triggered"; they do not test whether the event feed can still fire.** `UNPROVEN → leans THEATRE (unexercised)` |
| `restricted_actors[]` "appears to track CURRENTLY HELD, not historically" | DIAGNOSTIC §2 (L39) | The docs themselves flag that the accounting surface is miscounting 552 events. The author notices the instrument is broken and files it as a caveat rather than a defect. |
| "the real silent surface is **absence without detection** (no designed-vs-live coverage watch…)" | `04-G3A-RECONCILIATION.md` §4 (L43) | Named on 2026-09-12. Seven days later, exactly that: 20 lanes absent, nothing detected. |

**The consistent pattern across all three documents: every alerting surface is reported as "0 alerts", "unchanged", or "no data" — and each is interpreted as calm.** Per the workspace's own Void Guard ("'No data' ≠ 'All clear'. 'No data' = 'Cannot witness'"), that interpretation is inverted.

---

## 8. Findings table

| # | job / unit | claims | actual | evidence | class |
|---|---|---|---|---|---|
| 1 | 14 jobs × `hermes-legacy-scripts` | "converted to /etc/cron.d/hermes-legacy-scripts 2026-09-04" | File absent on KVM8 **and** KVM4; `find /` empty | `cat`/`find`/`grep` → not found | **THEATRE** (false migration claim; lanes dead) |
| 2 | 6 jobs × canary swap | "superseded by canary canary-X" | 5 of 6 canaries **deleted** from `jobs.json`; ran once 2026-09-17 | 6 canary ids in `executions.db`; name-match → NOT PRESENT ×6 | **THEATRE** |
| 3 | KVM4 (claimed successor host) | "MIGRATED to KVM4 gateway book" | KVM4 ticker dead since **2026-09-12 17:03**; no hermes unit; 0 hermes processes | `ticker_heartbeat` mtime + epoch; `systemctl is-active` → inactive; `pgrep` | **BROKEN** |
| 4 | arif-morning-pulse | migrated to KVM4 | KVM8 disabled; **KVM4 disabled with `paused_reason: null`**; KVM4 scheduler dead | KVM4 `jobs.json` disabled list | **DISABLED** (dead both ends) |
| 5 | arif-world-reality-intel | migrated to KVM4 | same as #4 | same | **DISABLED** (dead both ends) |
| 6 | reddit-daily-monitor | "MIGRATED to KVM4 2026-09-04 FI-008 tail" | **Not present in KVM4 `jobs.json` at all** | KVM4 enabled+disabled name list | **THEATRE** |
| 7 | cron-receipt-bridge | bridge that carries cron receipts; tracks `telegram_delivery_failures` | **143 exec, 0 delivered, 107 suppressed**; own payload shows `telegram_delivery_failures: 24`, `escalated: []` | `executions.db` agg; `output/25c2e9ff80d2/2026-09-14_15-13-02.md` | **THEATRE** |
| 8 | Malaysia Weekly Reality Probe | `A2A → telegram:-1003753855708` | 4 exec, **3 delivery-FAILED**, 1 suppressed, 0 delivered; then deleted | `executions.db`; `lane-routing.json` | **BROKEN** |
| 9 | session-auto-trace | session tracing lane | 94 exec (30 failed), **0 delivered** | `executions.db` | **THEATRE** |
| 10 | pull-openclaw-traces | openclaw trace ingest | 93 exec, **0 delivered**, 90 suppressed | `executions.db` | **THEATRE** |
| 11 | capability-fitness-cycle | fitness measurement | 8 exec, **0 delivered**, 8 suppressed | `executions.db` | **THEATRE** |
| 12 | arif-executive-briefing | executive briefing | 12 exec, **0 delivered** | `executions.db` | **THEATRE** |
| 13 | agent-card-drift-check | alerts Arif on new agent-card drift | **enabled, runs daily, 8/8 silent-by-design, 0 delivered ever** | `output/8b2ccdb9bce5/…` "silent (empty output)"; script docstring | **UNPROVEN** |
| 14 | gate-integrity-check | makes W_SCAR gate edits VISIBLE | enabled, 2/2 silent-by-design, 0 delivered ever | `output/5d11524f35a5/…`; script docstring | **UNPROVEN** |
| 15 | `lane-routing.json` | `"source": "jobs.json (live, not a story)"` | **0 of 20 routed names exist** | python set-difference | **THEATRE** |
| 16 | dream-engine ×3 timers | cadence for a design that exists | dangling, dormant, dead `Documentation=` | `systemctl show`; `systemctl cat` | **DANGLING/DISABLED** |
| 17 | apex-health.timer · arifosmcp-network-heal.timer | 5-min / heal probes | dangling (service absent), disabled | unit scan | **DANGLING/DISABLED** |
| 18 | dream-engine nights | "one working nightly battery" | **REAL** — fires, exit 0, 13 entries 2026-08-21→09-18 | timer + `last_dream.json` + `systemctl status` | **REAL** |
| 19 | VPS Backup, attention-closure, docforge-edition-daily, ALPHA-ZEN 1-3, sentinel-tripwire, Site drift watch, Weekly Governance Digest, CANARY iron-radar | deliver | **all delivered** | `executions.db` | **REAL** |
| 20 | 40+ federation systemd timers | scheduled | all firing, **0 failed units** | `list-timers --all`, `list-units --state=failed` | **REAL** |
| 21 | `organ-health-sentinel` | health sentinel, every 15m | disabled 2026-08-30 with **`paused_reason: null`**, last run 2026-08-30 13:10 | `jobs.json` | **DISABLED/SILENT-STOP** |
| 22 | `Executive Briefing — Daily Edition` | daily executive briefing | disabled 2026-09-18, **`paused_reason: null`**, `last_run_at: None` | `jobs.json` | **DISABLED/SILENT-STOP** |
| 23 | A-FORGE / flow alerting | "0 alerts", "no new gov events since 2026-09-16" | alert paths asserted calm on zero evidence | HOLD docs §2.2, §3 | **UNPROVEN → leans THEATRE** |

---

## 9. The two measured numbers

### 9.1 Of the 40 cron jobs, how many are doing real delivered work?

**10.**

**Method:** 14 are `enabled:true`; of those, count only jobs with ≥1 `delivery_outcome='delivered'` row in `executions.db` (aggregated by name across the migrated ID spaces).

**The 10:** `VPS Backup` · `attention-closure` · `docforge-edition-daily` · `ALPHA-ZEN 1 — Alpha Signal` · `ALPHA-ZEN 2 — Body Check` · `ALPHA-ZEN 3 — Zen Signal` · `sentinel-tripwire` · `🜂 Site drift watch` · `Weekly Governance Digest` · `CANARY iron-radar`

**The other 30:**
- **26 disabled** — could act, switched off, 20 of them behind a successor that does not exist
- **2 enabled monitors that run and have never delivered** (`agent-card-drift-check` 0/8, `gate-integrity-check` 0/2) — **UNPROVEN**, silent-by-design
- **2 enabled, not yet due for their first run** (`sentinel-heartbeat`, `amin-acl-weekly-checkin`) — **REAL-pending**

**10 / 40 = 25%.** And of the 10, one (`CANARY iron-radar`) is the *only* survivor of a six-job successor program; the five governance lanes it was meant to replace are dark.

**Counter-measurement — the shutdown was not confined to dead lanes.** Querying the same way for *any* name with delivered history, then subtracting the currently-enabled set:
```
DELIVERED-HISTORY names not currently enabled (18 total, incl. renames/duplicates):
  syed-morning-brief · syed-afternoon-chk · syed-evening-wrap · syed-daily-presence ·
  arif-morning-readiness · arif-evening-anchor · arif-market-brief · arif-midday-alert ·
  arif-eod-wrap · daily-life-learning-video · alpha-zen-morning-intel · maintenance-health-loop ·
  skill-drift-watch · arifflow-daily-governance-digest · morning-brief-wakebus-audit ·
  vps-gdrive-daily-backup · organic-rebuild-watch · CANARY arifflow-daily-governance-digest
```
After removing obvious renames (`vps-gdrive-daily-backup`→`VPS Backup`; `alpha-zen-morning-intel`→ALPHA-ZEN family) and the canary, **~15 lanes with a proven record of reaching a human were switched off.** This is not a cleanup of things that never worked — it is a cleanup that removed working human-facing lanes and did not replace them.

### 9.2 How many monitors could not have alerted anyone?

**13.** (monitor/alert-intent jobs **within the 40-job set** that cannot deliver an alert to a human, today)

| monitor | why it cannot alert |
|---|---|
| `iron-radar` | disabled; canary successor deleted; KVM4 copy on a host whose ticker died 2026-09-12 |
| `geo-econ-horizon` | same |
| `arifflow-daily-governance-digest` | same |
| `arif-reckoning` | same |
| `malaysia-intel-weekly` | same |
| `morning-brief-wakebus-audit` | same |
| `output-attestation-check` | disabled; `hermes-legacy-scripts` does not exist |
| `hermes-upstream-drift-watch` | disabled; target does not exist; **never ran once** (`last_run_at: None`) |
| `seal-integrity-sweep-script` | disabled; target does not exist |
| `artifact-drift-audit-script` | disabled; target does not exist |
| `organ-health-sentinel` | disabled 2026-08-30, `paused_reason: null` — silently stopped |
| `reddit-daily-monitor` | disabled; "migrated to KVM4"; **absent from KVM4** |
| `institution-metrics-pulse` | disabled; target does not exist |

**Excluded, and why** (12 further monitors that *can* alert or are not yet tested): `sentinel-tripwire` (delivers 4/4), `🜂 Site drift watch` (delivers 20), `agent-card-drift-check` + `gate-integrity-check` (running, silent-by-design — **UNPROVEN**, not proven dead), `sentinel-heartbeat` (not yet due, and is itself an anti-theatre proof-of-life control).

**Beyond the 40**, four further monitor-class jobs are deleted-but-recent and had **0 deliveries** in their entire final history — `cron-receipt-bridge` (0/143), `session-auto-trace` (0/94), `pull-openclaw-traces` (0/93), `Malaysia Weekly Reality Probe` (0/4, 3 delivery failures), plus `capability-fitness-cycle` (0/8). Counting those, the honest figure is **18 monitor-class lanes that could not have alerted a human.**

---

## 10. What is actually wrong (one paragraph)

The delivery gate is competently built; the **jobs sitting behind it are not maintained**. Twenty-six of forty jobs are off, and twenty of those were switched off in favour of a successor that was never created on this host: fourteen point at a cron file that does not exist, five point at canaries that were deleted after one test run, one points at a KVM4 that was never told. KVM4 — the host the migration notes call "the gateway book" — has had no Hermes cron ticker since 2026-09-12 17:03 and no Hermes unit file at all. On KVM8, `cron-receipt-bridge` ran 143 times without ever delivering, while faithfully counting 24 Telegram delivery failures into an `escalated: []` field nobody reads. `lane-routing.json` routes twenty jobs that do not exist while asserting `"not a story"`. Five systemd timers require service files that are not on disk — invisible because they are disabled, so they raise no failure. And across three separate diagnostic documents this week, every alerting surface was reported as `0 alerts` / `no new events` / `no data`, and each was read as calm.

**The scheduled layer is not protecting anything. It is a set of tripwires whose wires were cut in a cleanup that recorded the cut but never recorded that the replacement never arrived.**

---

## Appendix — raw artifacts written by this audit

| file | contents |
|---|---|
| `/root/AAA/reports/acah-audit-2026-09-19/_raw-jobs.tsv` | all 40 jobs, full field dump |
| `/root/AAA/reports/acah-audit-2026-09-19/_idmap.json` | output-dir id → job name map (46 entries) |
| `/root/AAA/reports/acah-audit-2026-09-19/_agg.json` | name → [ids] + per-id execution aggregates |

**No cron configuration, `jobs.json`, service, or database was modified. Every DB read used `mode=ro`; every remote KVM4 command was read-only (`ls`, `cat`, `sqlite3 -readonly`, `systemctl show/is-active`, `pgrep`).**
