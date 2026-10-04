# Hermes Cron — jobs.json Editing Protocol (long-form)

Operating knowledge for `/root/HERMES/cron/jobs.json` edits, validated through live resolver-source reads (2026-08-05). Read this BEFORE patching any cron `script` path or `provider` field.

## The resolver rule (canonical — verified from source)

```
/usr/local/lib/hermes-agent/cron/scheduler.py  L2037-2063

scripts_dir = _get_hermes_home() / "scripts"        # = /root/HERMES/scripts/
if raw.is_absolute():
    path = raw.resolve()
else:
    path = (scripts_dir / raw).resolve()
# Guard against path traversal / absolute injection / symlink escape
try:
    path.relative_to(scripts_dir_resolved)
except ValueError:
    return False, "Blocked: script path resolves outside the scripts directory"
if not path.exists():
    return False, f"Script not found: {path}"
```

**Rule, plain English:**
- Scripts MUST reside under `HERMES_HOME/scripts/` (= `/root/HERMES/scripts/` in this stack).
- `script` field in jobs.json:
  - **Bare name** (`"eureka-promote.sh"`) → resolves to `/root/HERMES/scripts/eureka-promote.sh`. ✅ works.
  - **Absolute path inside scripts_dir** (`/root/HERMES/scripts/X.sh`) → passes the relative_to guard. ✅ works.
  - **Absolute path OUTSIDE scripts_dir** (`/root/HERMES/cron/scripts/X.sh` or `/tmp/X.sh`) → **Blocked**. ❌ "script path resolves outside the scripts directory".
  - **Path with subdirectory** (`cron/scripts/eureka-promote.sh`) → resolves to `/root/HERMES/scripts/cron/scripts/eureka-promote.sh` (doesn't exist) → "Script not found".
- Working scripts (`morning-brief.sh`, `arif-fazil-sense.sh`, `aaa-dispatch.sh`, etc.) all live in `/root/HERMES/scripts/` with bare names. **Match this convention.**

**Runtime override:** `HERMES_REAL_HOME=/root` is set in the gateway process env. The Python module `get_hermes_home()` returns `/usr/local/lib/hermes-agent/profiles/aaa-hermes` at static import (without a `scripts/` subdir there), but the actual scheduler resolves from `/root/HERMES/`. Don't trust a Python REPL probe — trust the working scripts' location.

## The validator's quirks

`/root/HERMES/scripts/zen/validate_jobs_json.py`:

- **`check` (no file arg):** hardcodes `JOBS = Path('/root/HERMES/cron/jobs.json')`. Passes a file arg → silently ignored. To pre-validate a patch file before apply, replicate `check_jobs()` in Python (see template below).
- **`apply <patch>`:** loads patch JSON, calls `check_jobs(new)` on the in-memory dict, atomic-replaces jobs.json, auto-stamps backup at `/root/forge_work/backups/jobs.json.bak-<YYYYMMDD-HHMMSS>`, writes receipt at `jobs.json.receipt-<stamp>.json`.
- **Patch shape:** FULL replacement of jobs.json (no partial diff). Take the live file, mutate the dict, write back. Backup ensures revert is one `cp`.
- **Live provider set (from `/root/HERMES/model-picker.yaml`):** `[deepseek, minimax, ollama, openrouter, qwen-token-plan, qwen-token-plan-individual]`. Any job with `provider` outside this set → validator error. Common failure: stale `provider: "fed"` from old federation alias (15 jobs in this stack, all dead as of 2026-08-05).
- **`ALLOWED_DELIVER` set:** `local`, `silent_ok`, `telegram:<id>` for known chats, `origin`, comma-separated multi-target. Not in this set → validator error. `Sense` job in this stack has `deliver: "origin"` which IS in the allow-list, but the resolver's tokenizer-strip issue means Telegram delivery still fails — separate token-injection bug.

## Pre-edit protocol (the order that prevents v2→v3 regressions)

1. **Read the resolver rule first** (or this doc). Don't guess absolute paths.
2. **Read live jobs.json immediately before patching:**
   ```bash
   grep -E '"name"|"script"|"provider"|"deliver"|"last_error"' /root/HERMES/cron/jobs.json | head -60
   ```
   Multiple agents (kimi-code, Claude, Hermes, OpenCode) write to this file. Mid-session drift is real and dangerous.
3. **Replicate `check_jobs()` in Python** to validate the patch in isolation:
   ```python
   import json, re
   from pathlib import Path
   PATCH = Path('/path/to/patch.json')
   PICKER = Path('/root/HERMES/model-picker.yaml')
   ALLOWED_DELIVER = {'local','silent_ok','telegram:267378578','telegram:-1003753855708',
       'telegram:-1003815535761','telegram:-1004446358629','telegram:1042200555',
       'telegram:8410138119','origin','telegram:267378578,telegram:-1004446358629'}
   providers = set()
   for m in re.finditer(r'^\s+provider:\s*(\S+)\s*$', PICKER.read_text(), re.MULTILINE):
       providers.add(m.group(1))
   d = json.loads(PATCH.read_text())
   errs = []
   for i, j in enumerate(d.get('jobs', [])):
       pfx = f"job[{i}] {j.get('name','?')[:30]}"
       for f in ('id','name','schedule','enabled'):
           if f not in j: errs.append(f"{pfx}: missing field '{f}'")
       prov = j.get('provider')
       if prov and prov != 'null' and prov not in providers:
           errs.append(f"{pfx}: provider '{prov}' not in live set {sorted(providers)}")
       sched = j.get('schedule', {})
       if sched.get('kind') == 'cron':
           if len(sched.get('expr','').split()) != 5:
               errs.append(f"{pfx}: cron expr must have 5 fields")
       if not isinstance(j.get('enabled'), bool):
           errs.append(f"{pfx}: 'enabled' must be bool")
       dlv = j.get('deliver')
       if dlv and dlv not in ALLOWED_DELIVER:
           errs.append(f"{pfx}: delivery '{dlv[:40]}' not in allow-list")
   print(f"{'✅' if not errs else '❌'} {len(errs)} errors")
   for e in errs: print(f"  {e}")
   ```
4. **Apply via validator:** `validate_jobs_json.py apply <patch>` — auto-stamps backup.
5. **Verify post-apply:** `validate_jobs_json.py check` should print `✅ jobs.json valid (N jobs, M live providers)`.
6. **Manual one-shot** the affected jobs to confirm they actually run before relying on next tick:
   ```bash
   /root/HERMES/scripts/eureka-promote.sh
   /root/HERMES/scripts/syedos-quiet.sh
   ```

## Pitfalls (real ones from 2026-08-05)

- **`eureka-promote` cron every 30m will spam-flag `/root/forge_work/_drafts/`** because every draft created during a chat session is a "high-info delta". With Zen's ≤3 Telegram pings/day budget, this will breach quickly. Consider a `THROUGHPUT_LIMIT` knob or `_drafts` blacklist before letting it run unattended. The `deliver: local` downgrade stops Telegram spam but doesn't stop the script from running and producing output — if you want silence, also add `deliver: silent_ok` or pause the job.
- **`cross-organ-fanout`** in kimi's retrospective referred to an EDIT inside `federation-health.sh`, not a new job. Verify by `stat -c '%y'` on the script, not by `grep jobs.json`.
- **Audit-freshness gap:** kimi wrote a retrospective AFTER the patch that was already stale by 5 minutes (PRN16 already removed from jobs.json before the doc was drafted). Always `grep jobs.json` immediately before drafting a patch — the registry you remember may not be the registry that exists.
- **`last_status` lags live fix.** Right after a patch apply, `last_status: error` still shows the pre-fix error. The next scheduler tick (≤interval minutes) overwrites it. Don't trust `last_status` as live truth post-apply; trust your `validate_jobs_json.py check` + manual run.
- **Tokenizer-strip on `deliver=telegram:*`** when `no_agent=true`: scheduler tries to send without bot token, fails with "You must pass the token you received from https://t.me/Botfather!". Fix: `deliver: "local"` for `no_agent` cron jobs unless you have a verified Telegram chat_id route AND the scheduler's token-injection is wired (separate Hermes gateway bug). Zen-compliant: cron jobs that fire-and-forget shouldn't ping Telegram at all (≤3/day budget per AGENTS.md).
- **Provider migration:** if you migrate 15+ jobs at once, the validator's live-set check catches dead providers (`fed`). Pick a target from the live set. `qwen-token-plan-individual`+`qwen3.7-plus` (default tier) is the safest mass migration. For apex/sovereign jobs, escalate to `glm-5.2` per `model-picker.yaml` apex tier. Do NOT migrate every job to one provider regardless of role — bulk vs default vs heavy vs apex exist for a reason.
- **Multi-agent write contention.** In a single 2026-08-05 session, three different agents (kimi-code, Claude, this one) patched jobs.json. If you're working alongside another agent, communicate who-owns-what or accept that you'll redo work. The `_arifos_lockfile` mechanism (if present) should be checked before write.

## Recovery / rollback

```
# Single-command revert (most recent backup wins)
ls -t /root/forge_work/backups/jobs.json.bak.* | head -1 | xargs -I{} cp {} /root/HERMES/cron/jobs.json

# Script rollback (if you moved .sh files)
mv /root/HERMES/scripts/{eureka-promote,syedos-quiet,quiet-hours-arbiter}.sh /root/HERMES/cron/scripts/

# Validate the revert
/root/HERMES/scripts/zen/validate_jobs_json.py check
```

Receipt trail: `/root/forge_work/backups/jobs.json.receipt-<stamp>.json` (one per apply) and `jobs.json.bak-<stamp>` (pre-apply snapshot). Pattern = `CONFIG_MUTATION_RECEIPT`, schema `arifos.record.v1`, actor=who-applied (often `kimi-code/FI-008` or `hermes-agent`).

## Patch JSON shape (worked example from 2026-08-05)

```json
{
  "_meta": {
    "patch_id": "PATCH-cron-paths-v4",
    "patched_at_utc": "2026-08-05T18:18:00Z",
    "reversible": true,
    "blast_radius": "2 cron jobs, 0 services, 0 humans"
  },
  "jobs": [
    ... full jobs.json dict with mutations ...
  ]
}
```

The validator's `apply` mode loads the patch as a complete jobs.json (it expects the same top-level shape: `_meta` is ignored, but `jobs` is iterated). Take the live file, mutate in-place, write back as the patch.

## What this skill does NOT cover

- The scheduler tick logic itself (interval/cron → next_run_at computation) — covered in `scheduler.py` if needed
- Telegram delivery token injection (separate gateway bug) — covered in `hermes-telegram-gateway-ops`
- Cross-organ health probing — covered in `federation-infra-verification`
- The F13 seal protocol for cron receipts — covered in `arifos-federation-ops` §2