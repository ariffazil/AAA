# Cron — Script Location vs jobs.json Path Mismatch (2026-08-06)

## The bug class

A recurring failure mode in the HERMES cron subsystem: scripts live in one directory, but `jobs.json` paths reference a different directory. The cron runner reports `last_status: error, last_error: "Script not found: <path>"` — but the script DOES exist, just at a different path.

## Worked example (2026-08-06)

| Job | jobs.json path | Actual script location | State |
|---|---|---|---|
| `eureka-promote` | `/root/HERMES/scripts/eureka-promote.sh` | `/root/HERMES/cron/scripts/eureka-promote.sh` | ❌ broken |
| `quiet-hours-arbiter` | (no entry in jobs.json) | `/root/HERMES/cron/scripts/quiet-hours-arbiter.sh` | ❌ orphan (script exists, no job) |
| `cross-organ-fanout` | (script not found anywhere) | — | ❌ never created |
| `daily-news-briefing` | `script: None` (cron schedule `0 8 * * *`, `last_status: ok`) | — | ⚠️ LLM-prompt-driven? Or ghost? |

## Diagnostic procedure

### Step 1: List actual scripts

```bash
find /root/HERMES/cron/scripts/ -name "*.sh" -ls 2>/dev/null
ls -la /root/HERMES/cron/scripts/ 2>/dev/null
```

Expected output: every `.sh` file with size + mtime + perms.

### Step 2: List jobs.json script references

```python
import json
with open('/root/HERMES/cron/jobs.json') as f:
    jobs = json.load(f)
for j in jobs.get('jobs', []):
    print(f"{j['name']}: script={j.get('script')!r}  enabled={j.get('enabled')}  status={j.get('last_status','-')}")
```

Expected output: every job with its `script` field (which may be `None`, an absolute path, or a relative name).

### Step 3: Diff the two lists

For each script in step 1, is it referenced by any job in step 2?
For each non-`None` script in step 2, does the file actually exist at that path?

```bash
# For each script in jobs.json, check existence
python -c "
import json, os
jobs = json.load(open('/root/HERMES/cron/jobs.json'))['jobs']
for j in jobs:
    s = j.get('script')
    if s:
        full = s if s.startswith('/') else f'/root/HERMES/cron/scripts/{s}'
        print(f\"{j['name']:30s} {s!r:60s} exists={os.path.exists(full)}\")
"
```

### Step 4: Distinguish 3 failure modes

| Mode | Symptom | Fix |
|---|---|---|
| **Path mismatch** | script exists at `/cron/scripts/`, jobs.json says `/scripts/` | `validate_jobs_json.py apply <patch>` with corrected path — F1 AMANAH (reversible, validator does STAMPED backup) |
| **Orphan script** | script exists, no jobs.json entry | either add job entry (if intended) or move script to `_drafts/` (don't delete — 7-day quarantine per Zen doctrine) |
| **Script-None with status=ok** | schedule fires, no script, last_status=ok | investigate whether job is LLM-prompt-driven (jobs.json's `prompt` field, not `script`) — `daily-news-briefing` may be a prompt-driven cron, not a bash script. Verify by reading the job entry's full `prompt` field. |

## Diagnostic commands (re-runnable)

```bash
# 1. Live cron health per job
python -c "
import json
with open('/root/HERMES/cron/jobs.json') as f: jobs = json.load(f)['jobs']
for j in jobs:
    err = j.get('last_error')
    err_str = (err or '-')[:80]
    print(f\"{j['name']:30s} enabled={j.get('enabled')}  status={j.get('last_status','-')}  err={err_str}\")
"

# 2. Script files vs jobs.json paths
diff <(find /root/HERMES/cron/scripts/ -name "*.sh" -printf "%f\n" | sort) \
     <(python -c "import json; [print(j['script']) for j in json.load(open('/root/HERMES/cron/jobs.json'))['jobs'] if j.get('script')]" | sort)
```

## The fix workflow (F1 AMANAH)

For path mismatches ONLY — do not bypass `validate_jobs_json.py`:

```bash
# 1. Probe (already done above)
# 2. STAMPED backup via validator
python /root/HERMES/scripts/zen/validate_jobs_json.py apply <patch.json>
# 3. Restart the cron service (if needed)
systemctl restart hermes-cron
# 4. Verify
hermes cron list
tail -F /root/HERMES/cron/output/<job-name>.log
```

**Iron Rule:** do NOT edit `jobs.json` directly — must go through the validator (atomic, STAMPED backup, receipt). The Zen doctrine on agent peace forbids direct edits.

## Why this bug recurs

Two causes:

1. **Scripts moved when the cron subsystem was restructured.** Original layout: `/root/HERMES/scripts/<name>.sh`. Restructured: `/root/HERMES/cron/scripts/<name>.sh`. Some jobs were updated, some weren't. The path mismatch is the residue.

2. **New scripts added without registering them in jobs.json.** `quiet-hours-arbiter.sh` lives in `cron/scripts/` but has no jobs.json entry. Either (a) it was meant to be registered but wasn't, or (b) it's leftover from a previous design that was retired.

The pattern: **script-creation and job-registration are two separate operations** that can drift apart. Same class of bug as code-without-test, secret-without-vault-entry, skill-without-profile. The fix: enforce registration-as-part-of-creation at the tooling layer (e.g., `forge_ephemeral` lifecycle for cron jobs).

## Cross-references

- `references/cron-model-ref-fix-2026-08-05.md` — different cron failure class: allowlisted model id not exposed by provider. Different symptom (last_error mentions model name), different fix (dual-write SQLite).
- §4.4 of SKILL.md — the audit-of-meaning class — captures the related "is this verification or performance?" discipline that applies when reading the cron status.

## Update 2026-08-15 — TWO registries; the live one is profile-level

The 2026-08-06 table above assumed `/root/HERMES/cron/jobs.json` is the registry. As of 2026-08-15 there are **two** jobs.json files:

| Registry | Path | Status |
|---|---|---|
| Profile (LIVE) | `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json` | This is what the Hermes cron daemon actually runs (verify via `cronjob list` — job_ids here match `executions.db` in the same dir) |
| Legacy | `/root/HERMES/cron/jobs.json` | Stale mirror — grepping it for a job returns NOTHING even though the job fires daily. Do not diagnose from it. |

**Resolution rule discovered live:** in the profile registry, a bare `script:` name (e.g. `federation-health-probe.sh`) resolves against the **profile scripts dir** `/usr/local/lib/hermes-agent/profiles/aaa-hermes/scripts/` — NOT against `/root/HERMES/scripts/` where the file actually lives. Symptom: `last_status: error` every tick with `Script not found: <profile-scripts-path>` (read it from `cron/output/<job_id>/<ts>.md`, which contains the exact failed path).

**On the no-symlink pitfall above:** it still holds for same-registry layout confusion. But when the script's canonical home is another subsystem (`/root/HERMES/scripts/`, referenced by other tooling) and the cron registry only accepts its own scripts dir, a symlink `profile/scripts/<name>.sh -> /root/HERMES/scripts/<name>.sh` is the minimal reversible fix — applied and verified 2026-08-15 (`federation-health-probe`, next tick passes). Record the symlink in the commit message so the layout stays explainable (F11), and prefer a real move only when nothing else references the old path.

**Diagnosis order for `script not found` cron errors (2026-08-15 revision):**
1. `cronjob list` → get the real job_id + confirm which registry is live.
2. `cat cron/output/<job_id>/<latest>.md` → the error line contains the EXACT path the runner tried. That path tells you the resolution base — no guessing.
3. Place/symlink the script at that path, `bash <path>` once to verify exit 0, done.

## Pitfalls

- Don't `ln -s` the missing path. The script will run, but the next person reading the layout will be confused about which directory is canonical. F4 CLARITY says entropy should go DOWN, not sideways. Either move the script or move the jobs.json path — pick one and apply F1 reversibility.
- Don't assume `last_status: ok` means the script ran. `daily-news-briefing` has `last_status: ok` with `script: None`. Either (a) it's a prompt-driven cron (run by LLM, not bash) or (b) the status field is stale from before the script was removed. Read the job's `prompt` field to distinguish.
- Don't delete orphan scripts. Zen doctrine: quarantine 7-day grace in `_drafts/`, then archive. Reversible > irreversible.
- The cron subsystem's `output/` directory accumulates per-job logs. They're useful for post-mortem but not for catching this class of bug — the error happens before any output is generated.