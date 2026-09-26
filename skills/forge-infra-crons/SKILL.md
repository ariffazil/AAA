---
name: forge-infra-crons
description: "Audit root and etc crontab entries without mutating state."
owner: A-FORGE
capability_tier: fed-long-context
ecology_state: WARM
---
> **Case-duplicate collapse (2026-09-20).** This skill was stored twice as two real
> directories differing only in case. The second copy (`/root/.hermes/skills/FORGE-infra-crons`) is now an alias
> symlink here. Its full pre-collapse body is preserved at
> `references/absorbed-FORGE-infra-crons.md` and in `.frozen/2026-09-20-case-dupes/FORGE-infra-crons/`.
# FORGE-infra-crons

Infrastructure cron governance skill. Scans and audits cron entries across the VPS.

## Capabilities
- List all cron jobs from root crontab, /etc/cron.d, and any profile-local cron dirs
- Detect orphaned, duplicate, or dead cron entries
- Verify cron entries against Machine Constitution registry
- Classify by health: `LIVE` / `STALE` / `DEAD` / `DRIFT`

## Floors
- F1 AMANAH: Read-only by default. Mutations require 888_HOLD.
- F11 AUDITABILITY: All cron observations logged.

## Audit procedure (the actual workflow)

Run the following in order. Do not skip steps; each surfaces evidence the next needs.

1. **Inventory.** Enumerate every cron source:
   - `crontab -l` (root crontab)
   - `/etc/cron.d/*` (skip `.placeholder` and `.hermes-cron-ban-*` quarantine dirs)
   - `find /root -maxdepth 4 -type d -name '*cron*'` to surface profile-local cron dirs
   - `/etc/cron.daily`, `/etc/cron.hourly`, `/etc/cron.weekly`, `/etc/cron.monthly`

2. **Map schedule to script.** For each entry, extract the cron schedule and the command
   target. A `jitu-guard <name> && <real-cmd>` wrapper means the *real* command is what
   fires after the gate; the wrapper is the gate, the script is the work.

3. **Probe live evidence.** For each cron, find its log file. The pattern: `/var/log/<name>.log`
   or `/var/log/<name>-cron.log` or a per-app dir. If no log file exists, mark
   `script_missing_or_unlogged` — it may exist but is silent. **Do not declare a cron dead
   just because there is no log file**; check the script path separately.

4. **Classify each cron by log mtime** (use `stat -c '%y' <logfile>`):

   | Bucket | Definition | Action |
   |---|---|---|
   | `LIVE` | log mtime within last 48h | report as firing |
   | `STALE` | log mtime 2–14 days ago | investigate schedule — is it weekly / monthly / has its gate open? |
   | `DEAD` | log mtime >14 days OR log missing AND script missing | flag for removal |

   Two non-bucket flags to attach alongside the bucket:

   - `script_missing` — the command path on disk does not exist. Cron will fire to a 404;
     silence the entry or restore the script.
   - `gate_paused` — the cron is wrapped in `jitu-guard <gate>` and the gate's pause file
     exists. The cron itself is fine; the gate is holding it. Note the pause reason if
     visible in `jitu_events.jsonl`.

5. **Cross-reference declarations.** Federation has two sources of "what jobs *should*
   exist":
   - declared YAML manifest (usually under a profile dir)
   - `jobs.json` (Hermes scheduler source of truth)
   The `cron_failure_autopause` log surface will report drift when these disagree — e.g.
   "DRIFT: <job_id> declared in YAML but missing from jobs.json" repeating every 15 min.
   That is the failure to surface to the sovereign; the cron itself is doing its job
   (reporting drift), but the drift is real and not being resolved.

6. **Output.** The deliverable is a four-bucket table: LIVE / STALE / DEAD / DRIFT, with
   each row carrying name, schedule, script path, last log mtime, last log line snippet.
   **Numbers come from `stat` and `tail`, never from counting grep hits by hand.**

## Pitfalls

- **A "live" log does not mean the cron is doing useful work.** A log that updates
  every 15 minutes with `}` and an empty success message is firing — but firing
  successfully is not the same as firing productively. Cross-reference with the cron
  purpose (declared in the script's docstring or the manifest comment) before claiming
  health.
- **`jitu-guard` wrapped jobs are silent until the gate opens.** Counting these as
  "stale" because their log is unchanged is a false positive. Check the gate's pause
  file before declaring staleness.
- **Scripts in `/usr/local/bin/` are common but may be missing.** The cron still runs
  every interval, the wrapper exits non-zero, and the log shows the failure only if the
  cron pipes stderr to a log. A `MISSING` log entry must be checked against the script
  path before declaring the cron dead — many "missing log" entries are actually
  "script-not-on-path" entries, a different fix.
- **`crontab -l` may include commented-out lines that look active.** Strip `#` lines
  before counting. The banner comments above active entries can fool a naive parser.
- **`/etc/cron.d/` files use `SHELL=` and `PATH=` env-var lines that look like cron
  entries.** A real cron entry starts with five schedule fields (minute hour dom mon
  dow). Anything else is an env-var declaration; do not count it as a job.

## What this skill does NOT do

- **Mutate any cron entry.** That requires F13 / 888_HOLD. The skill is read-only.
- **Resolve `jobs.json` vs YAML drift.** That is the scheduler's job
  (`hermes-cron-zen`). Surface the drift to the sovereign; do not auto-reconcile.
- **Run jobs on demand.** That is `cronjob_manage` (T1 executable).
