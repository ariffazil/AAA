# Cron Model-Ref Fix — Weekly Governance (2026-08-05)

Session evidence chain for the recurring OpenClaw cron allowlist failure and its fix.

## Symptom

`FORGE ⟁ Weekly Governance Roll-up (Sun 03:00 MYT)` — job `a4301644-2f6a-4365-965a-a6c908953a8f` in
`~/.openclaw/state/openclaw.sqlite` — fails at preflight:

```
cron payload.model 'deepseek-v4-flash' rejected by agents.defaults.models
allowlist: minimax/deepseek-v4-flash is not in [bailian-token-plan/deepseek-v4-flash, ...]
```

## Root cause mechanics

1. The job's model is stored in TWO places in `cron_jobs`: the `payload_model` column AND `job_json.payload.model`. A fix that touches only one is not a fix — the scheduler reads both.
2. A bare name (`deepseek-v4-flash`) gets provider-prefixed during resolution to `minimax/deepseek-v4-flash`, which the allowlist (`openclaw.json → agents.defaults.models`) rejects.
3. `last_run_status`/`last_error` columns are STALE: the error persisted after an allowlist edit because the job had not re-run. Read the CURRENT allowlist keys before trusting the error.
4. **Allowlist membership ≠ provider model existence.** `minimax/deepseek-v4-flash` can be allowlisted (alias-only entry) while the `minimax` provider exposes only `MiniMax-M2.7/MiniMax-M2.7-highspeed/MiniMax-M3` — the allowlist gate passes, then the runtime dies "model not found". The correct target must be BOTH allowlisted AND in the provider's real model list.

## The fix (dual write, backup first)

```bash
DB=/root/.openclaw/state/openclaw.sqlite
JOB=a4301644-2f6a-4365-965a-a6c908953a8f
cp "$DB" "$DB.bak-weekly-gov-$(date +%Y%m%d-%H%M%S)"

python3 << 'EOF'
import json, sqlite3
db = "/root/.openclaw/state/openclaw.sqlite"
job = "a4301644-2f6a-4365-965a-a6c908953a8f"
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("UPDATE cron_jobs SET payload_model=? WHERE job_id=?", ("deepseek/deepseek-v4-flash", job))
row = cur.execute("SELECT job_json FROM cron_jobs WHERE job_id=?", (job,)).fetchone()
j = json.loads(row[0])
j.setdefault("payload", {})["model"] = "deepseek/deepseek-v4-flash"
cur.execute("UPDATE cron_jobs SET job_json=? WHERE job_id=?", (json.dumps(j), job))
con.commit()
con.close()
EOF
```

Verify: `payload_model` AND `job_json.payload.model` both set; model is in allowlist keys
(`deepseek/deepseek-v4-flash` → True); next run timestamp sane.

## Why `deepseek/deepseek-v4-flash` and not `minimax/...`

`openclaw.json → models.providers`:
- `deepseek` → `['deepseek-v4-flash', 'deepseek-v4-pro']` — target EXISTS ✅
- `minimax` → `['MiniMax-M2.7', 'MiniMax-M2.7-highspeed', 'MiniMax-M3']` — no v4-flash ❌
- `bailian-token-plan` → has `deepseek-v4-flash` too (also valid target)

## Prior art

This is a RECURRING failure: fixed 2026-08-01 (documented in
`/root/HERMES/skills/devops/openclaw-cron-operations/references/forge-weekly-allowlist-fix-2026-08-01.md`),
found broken again 2026-08-05 with `payload_model` empty. After any gateway restart / config
churn / DB restore, re-verify the job's model ref before the next Sunday run. `openclaw cron list`
CLI can be broken by unrelated config invalidity — sqlite3 is the reliable path.
