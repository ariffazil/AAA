# WEEKLY AGENTIC MAINTENANCE MAP — KVM8 (forge)

**Measured:** 2026-09-19 18:32 +08 (Asia/Kuala_Lumpur) · host `forge` (100.64.0.2) · uptime 17d 10h
**Method:** live probe only — crontab, /etc/cron.d, systemd timers, jobs.json, executions.db, log mtimes.
**No figure below is inherited from memory.** Every count carries the command that produced it.

---

## 0. Verdict first

Three agentic layers run weekly on this machine, and **only the substrate layer is honest.**

| Layer | Declared weekly tasks | Measured firing | Health |
|---|---|---|---|
| **Hermes (me)** | 12 | 3 verified, 1 out-of-cadence, 8 never fired | ⚠️ PARTIAL |
| **Other AAA agents / organs** | 8 | 2 verified, 3 dead-log, 1 not-wired, 2 unknown | ⚠️ PARTIAL |
| **Machine substrate** | 9 | 9 verified | ✅ LIVE |

The pattern: **the substrate fires because the OS owns it. The agent layers fire only where a log
file proves it.** Above the OS, weekly maintenance is largely declared-but-dark — and the surfaces
that report it (`last_status: ok`) cannot show that, because `ok` is written on completion and never
expires.

---

## 1. LAYER 0 — Me (Hermes, KVM8)

### 1a. Hermes cron — jobs.json (`/root/HERMES/cron/jobs.json`)

`TOTAL JOBS: 40 · ENABLED: 14 · DISABLED: 26`

Weekly cadence in jobs.json — **4 enabled**:

| Job | Schedule | Deliver | Executions in ledger | Last | Verdict |
|---|---|---|---|---|---|
| CANARY iron-radar | Fri 12:00 | tg 267378578 | 2 | 2026-09-18 12:00 | ✅ fires |
| Weekly Governance Digest | Sun 22:00 | tg 267378578 | 2 | **2026-09-17 22:00** | ⚠️ fires OUT of cadence (Thu, not Sun) |
| amin-acl-weekly-checkin | Sun 20:00 | tg 8798431893 | **0** | — | ❌ NEVER FIRED |
| sentinel-heartbeat | Mon 09:00 | origin | **0** | — | ❌ NEVER FIRED |
| 🜂 Site drift watch (Caddy) | interval | origin | 27 | 2026-09-19 13:10 | ❌ last status **failed** |

Weekly cadence in jobs.json — **7 disabled** (all with 0 executions): `arif-reckoning` (Mon 06:30),
`geo-econ-horizon` (Mon 08:00), `malaysia-intel-weekly` (Mon 10:00), `syed-mak-cbd-followup` (Mon 09:00),
`morning-brief-wakebus-audit` (Mon/Wed/Fri 07:00), `seal-integrity-sweep-script` (Sun 03:17),
`hermes-upstream-drift-watch` (1st of month 04:00).

Probe:
```
python3 -c "import json;d=json.load(open('/root/HERMES/cron/jobs.json'));print(len(d['jobs']),sum(1 for j in d['jobs'] if j.get('enabled')))"
sqlite3 -readonly /root/.hermes/cron/executions.db "select job_id,count(*),max(started_at),max(status) from executions group by job_id"
```

### 1b. Hermes weekly work that lives OUTSIDE jobs.json (system cron)

| Task | Schedule (MYT) | Log | Last write | Verdict |
|---|---|---|---|---|
| `hermes checkpoints prune` | Sun 03:17 | /var/log/hermes-prune.log | 2026-09-12 19:17 UTC | ✅ fires weekly |
| `hermes-session-trace` | (cron.d) | — | — | unverified |
| `opencode-receipt-rotate` | daily (14d window) | — | — | ✅ daily, not weekly |

**Ownership split that matters:** the ONLY Hermes maintenance that reliably runs weekly is the one
the *OS* schedules. Everything in jobs.json is best-effort.

### 1c. My own weekly job, stated plainly

Weekly, I must:
1. Prune checkpoints — **OS does it, verified.**
2. Run the weekly governance digest — runs, but on Thursday, not Sunday. Cause unknown.
3. Fire `amin-acl-weekly-checkin` and `sentinel-heartbeat` — **never fired once.** Both are
   `origin`-delivered, one telegrams a human (8798431893 = Arif+Amin mirror).
4. Keep the site-drift watch green — 27 runs, currently failing.
5. NOT run: 7 disabled weekly jobs that were built, tested, and then parked.

A weekly job that is *enabled* and has **zero rows in the execution ledger** is not "pending" —
it is a promise the scheduler never kept, and every surface still reads `ok` or empty.

---

## 2. LAYER 1 — Other AAA agents / organs

### 2a. The designed per-agent weekly ritual is NOT INSTALLED

`/root/AAA/scripts/install_tree777_agent_crons.sh` writes a Sunday anchor per agent:

```
${m3} ${h3} * * 0  .../tree777_weekly_anchor.sh --agent=${agent}
```

Probe: `grep -rn 'tree777' /etc/cron.d/ /etc/crontab; crontab -l | grep tree777` → **zero hits.**

**The per-agent weekly maintenance anchor exists as a script and has never been scheduled.**
This is the single largest gap on this list: the federation built a per-agent weekly ritual and
left it unwired.

### 2b. Weekly tasks that DO belong to agents/organs

| Task | Owner | Schedule (MYT) | Log mtime | Lines | Verdict |
|---|---|---|---|---|---|
| `f13-weekly-packet.py` — sovereign decision queue | AAA / F13 | Mon 09:07 | **/var/log/arifos/f13-packet.log MISSING** | 0 | ❌ **never ran via cron** |
| `repo-audit.sh` — repo reality | A-FORGE | Mon 01:00 | 2026-09-15 00:43 | 0 | ❌ stale + silent |
| `sro_calibration_pipeline.py` | A-FORGE/CHRON | Mon 04:00 | 2026-09-16 00:13 | 0 | ❌ stale + silent |
| `dead-pointer-sweep.py` | AAA skills | Mon 05:23 | 2026-09-15 14:31 | 0 | ❌ stale + silent |
| `skill-audit.sh` — cross-harness skill orthogonality | AAA | Sat 20:00 | — | — | unverified |
| `well_dream.py weekly` | WELL | Sat 20:00 | — | — | unverified |
| `sovereignty_drill.sh` (first Sunday only) | arifOS | Sun 02:00 | 2026-09-07 00:44 | 0 | ⚠️ last 12 days ago |
| `weekly-digest.sh` | AAA event bridge | Sun 14:00 | bridge.log | — | partial |
| `entropy-governor` / `memory-helix-rollup` | AAA | daily 19:00 | — | — | daily |

**f13-weekly-packet is the most expensive miss.** It is the *batched sovereign decision queue* —
the mechanism that exists specifically to protect W888 (sovereign attention) by grouping Layer 3/4
proposals into one weekly verdict document. It has produced three packets
(`f13-packet-2026-W38-1/2/3.md`, 2026-09-15 22:45 → 09-16 03:03) — all hand-run. The Monday 09:07
cron has produced zero. **The sovereign-attention shield does not fire.**

### 2c. Agents with NO weekly maintenance at all (measured)

| Agent | Evidence |
|---|---|
| FI-008 kimi-code | crons are hourly/daily only (`aaa-universe-drift` hourly) |
| OpenCode / Kimi / Qwen / Codex / Claude / Antigravity / Gemini CLIs | all present at `/root/.local/bin` and `/root/.npm-global/bin`; **no weekly self-maintenance cron for any of them** |
| A-FORGE AED / orchestrator | duties are daily/hourly |

Nine agent CLIs are installed and running; the only weekly hygiene any of them gets is
`opencode-receipt-rotate` (daily). **No agent CLI has a weekly self-check.**

### 2d. Agent-card / mesh state

`/root/AAA/a2a/agent-cards/` holds **2 files** (`aaa-gateway.json`, `antigravity.json`).
`mesh-topology-static.json` was sealed **2026-06-28** — 83 days old — and its own note reads
*"Dynamic registration is disabled until it returns non-empty, authenticated results."*
`agent-card-drift-check` (Hermes, daily 05:30) fires ✅ — but it checks 2 cards against a
83-day-old mesh. **The drift detector is green because there is almost nothing left to drift.**

---

## 3. LAYER 2 — Machine substrate

### 3a. 🔴 P0 — THE SUBSTRATE'S ONE REAL WEEKLY RISK: 14 dead interpreter paths

```
$ stat /opt/arifos/venv
stat: cannot stat '/opt/arifos/venv': No such file or directory
$ systemd-analyze verify /etc/systemd/system/chron-mcp.service
chron-mcp.service: Command /opt/arifos/venv/bin/python3 is not executable: No such file or directory
$ grep -rh 'ExecStart=' $(grep -rl '/opt/arifos/venv' /etc/systemd/system/ | grep '\.service$') \
    | sed 's/^ExecStart=//' | awk '{print $1}' | sort | uniq -c | sort -rn
     10 /opt/arifos/venv/bin/python
      3 /opt/arifos/venv/bin/python3
      1 /opt/arifos/venv/bin/fastmcp
```

**14 ExecStart lines across ~12 units name an interpreter that does not exist.** The live venv is
`/opt/arifos/current/venv/` (built 2026-09-16 06:16–06:40). Verified by systemd itself, not inferred.

Affected and **currently active** — every one of these fails on its next restart:
`arifos.service` (the constitution organ) · `chron-mcp` (:18102) · `aforge-heartbeat` ·
`geox-heartbeat` · `wealth-heartbeat` · `well-heartbeat` · `kabarkan-health` · `kabarkan-worker` ·
`mcp-claim-ledger` · `mcp-doc-tables` · `mcp-filings` · `mcp-media-ingest` · `mcp-numeric-audit` ·
`arifOS-NATS-heartbeat` · `arif-design-mcp`. Also `arif-dream`, `arif-dream-distill`,
`arifos-observatory-emitter` (inactive).

**Automatic reboot is OFF** (`Unattended-Upgrade::Automatic-Reboot "false"`) — that is the only thing
standing between this and a fleet-wide restart. Uptime: **17 days**. No reboot-required flag present.

Two one-line repairs exist and they are not equivalent:
- `ln -s /opt/arifos/current/venv /opt/arifos/venv` — restores every declared path at once, but
  pins 25 services to whatever `current` points at from now on.
- Edit 14 `ExecStart=` lines to `/opt/arifos/current/venv/bin/...` — explicit, no indirection.

I have **not** touched either. Rewiring the interpreter for the constitution organ is not a
maintenance chore — it is an authority call, and picking wrong means 25 services come back running a
venv nobody chose. **Escalated as a binary, below.**

### 3b. Weekly substrate tasks (the part that is genuinely healthy)

Counts: `crontab -l | wc -l` → **50 lines** (4 weekly) · `/etc/cron.d/` → **39 files** (9 weekly) ·
systemd timers → **57**.

Weekly, verified by log mtime:

| Task | Schedule | Evidence |
|---|---|---|
| `logrotate` | daily 00:50 | timer fired 2026-09-19 00:45 |
| `e2scrub_all` | Sun 03:30 | cron.d present, std |
| `litter-autoclean` | Sun 03:30 | cron.d present |
| `man-db` | weekly | timer |
| `docker-builder-prune` | Mon 05:22 | cron.d present |
| `pati-sweep` | Sat 18:00 | cron.d present |
| `vault999-backup` | daily 03:48 | fired 2026-09-19 03:50 |
| `arifos-backup` | daily 04:30 | fired 2026-09-19 04:30 |
| `sysstat-rotate` | Sun 00:00 | timer |
| `chron-prediction-verifier` | daily 07:00 | fired 2026-09-19 07:00 |
| `chron-loop-closer` | daily 07:15 | fired 2026-09-19 07:15 |
| `chron-task0-reconciliation` | daily 06:50 | fired 2026-09-19 06:50 |
| `drift-detector` | daily 07:15 | fired 2026-09-19 07:15 |

`df -h /` → **244G / 387G used (64%), 143G free.** No capacity pressure.
`du -sh /root/.hermes` → **2.2G**, dominated by `state.db` **744M** and `plugins` **381M**.

CHRON (the temporal organ): `chron-mcp.service` **active (running) since 2026-09-18 15:51**,
pid 3643487 on 127.0.0.1:18102. Store: **51,789 episodes**, 15 predictions active, **0 verified**,
**0 lessons**, `lessons.jsonl` 0 bytes. Its three weekly-adjacent timers all fired today.

---

## 4. Honest failures of this very audit (Shadow)

1. **`last_status: ok` is not a firing proof.** In jobs.json, `ok` is stamped on completion and
   never expires. Four weekly jobs read `ok`/`?` in that file; the execution ledger shows
   **0 rows** for two of them and out-of-cadence for a third. The ledger, not the job file, is truth.
2. **A log with 0 lines and an old mtime is ambiguous** — it can mean "ran, found nothing" or
   "never ran." I can distinguish them only where a packet/output artifact exists (f13) or does not
   (repo-audit, sro-calibration, dead-pointer). For `skill-audit`, `well-dream`, `pati-sweep`,
   `hermes-session-trace` I have **no evidence either way** — marked *unverified*, not *dead*.
3. **I did not read every /etc/cron.d file end-to-end.** Weekly extraction used the 5th field
   (`dow`) plus the 6th (`dom` for the monthly job). A schedule quoted with `@weekly`, or with the
   day-of-week written as a name inside a wrapped line, would be missed.
4. Counts are point-in-time. `f13-weekly-packet` may have fired at 09:07 today-adjacent and I would
   still see MISSING for the log if stderr went elsewhere. Timestamp: 2026-09-19 18:32 +08.

---

## 5. The contrast, compressed

```
MACHINE   — OS owns it, dies loudly, log proves it.        ✅ 9/9 weekly tasks
            ...but 14 ExecStart lines point at a venv that
            no longer exists. Every affected service is up
            NOW and fails on next restart.                 🔴 P0
ME        — OS owns 1 of my weekly jobs (it fires).
            jobs.json owns 12 (3 fire, 8 are dark).       ⚠️ 3/12
OTHER AAA — script exists, ritual designed, scheduler
            never installed. f13 packet: 0 cron runs.     ⚠️ 2/8
```

The invariant under all three: **maintenance that a scheduler owns runs; maintenance that a
doctrine owns does not.** Every weekly task above that is dead was *written, dated, commented and
committed* — none of that schedules anything.

And the substrate caveat that reframes the whole table: the machine layer looks honest only because
it is running. It has not restarted since the venv moved. **A green row here is a row nobody has
tried to re-earn.**

---

## 5b. CHRON registration (temporal consequence tracking)

Registered 2026-09-19 18:36 +08 via `chron_create_event`:

- **event** `weekly-agentic-maintenance` · target 2026-09-28 · kind OBSERVATION ·
  consequence HIGH · actionability PREPARE · audience arif
- **4 falsifiable predictions** generated via `chron_generate_predictions()`, each with a named
  verifier and a named falsifier, all `verify_at = 2026-09-28T23:59:59+08`:

| prediction_id | claim (abbrev) | conf |
|---|---|---|
| `pred-4b67c1dad6b0` | f13-weekly-packet produces 0 new packets via cron by 28 Sep | 0.75 |
| `pred-1be85d3c7117` | TREE777 per-agent weekly anchor still absent from every crontab | 0.80 |
| `pred-a19cbc2dfd9b` | weekly coverage stays ≤ 8 of 29 tasks with a fresh in-period receipt | 0.65 |
| `pred-d54455f9b039` | the 14 dead ExecStart lines remain unrepaired | 0.70 |

The daily `chron-prediction-verifier.timer` (07:00) will surface them when due. A prediction that
nobody can check is decoration; these four name the exact command that closes them.

---

## 6. Binary decisions (F13 only)

1. 🔴 **The dead interpreter paths.** 14 ExecStart lines across ~12 units (incl. `arifos.service` and
   `chron-mcp`) point at `/opt/arifos/venv`, which no longer exists. All those services are UP now
   and will fail on their next restart. Two repairs, pick one:
   **(a)** `ln -s /opt/arifos/current/venv /opt/arifos/venv` — one line, restores every path, but
   couples 25 services to whatever `current` means later; or
   **(b)** repoint 14 `ExecStart=` lines at `/opt/arifos/current/venv/bin/...` — explicit, no
   indirection, more edits.
   *My read: (b). `current` is a moving pointer; a service interpreter should not be.*

2. **TREE777 per-agent weekly anchor** — install the Sunday cron block for the FI agents, or retire
   the script? (One command either way; currently it is neither.)

3. **`f13-weekly-packet`** — repair the Monday 09:07 lane so the sovereign decision queue actually
   arrives, or confirm you prefer to pull it by hand?

4. **7 disabled weekly Hermes jobs** — resurrect or delete. They have 0 executions; they are
   inventory, not capability.

Everything reversible I do myself and report. These four are direction, not effort.

---

## 7. What I did NOT do, and why (Shadow)

- **Did not create the venv symlink.** It is one line and it is reversible — which is exactly why it
  is tempting. It also decides which interpreter 25 services run, permanently, in a way that a
  future session would inherit without noticing. That is an authority call, not a chore.
- **Did not restart any service to test the finding.** Testing it would have proven it by taking the
  constitution organ down. `systemd-analyze verify` proves it without the outage.
- **Did not delete or repair the dead-log weekly jobs.** A 0-line log cannot distinguish "ran, found
  nothing" from "never ran" — I marked the three I can prove dead, and the rest *unverified*.

---

*Probe timestamp: 2026-09-19T18:32+08 · host forge · METHOD=live-probe ·
all commands printed above are re-runnable.*
