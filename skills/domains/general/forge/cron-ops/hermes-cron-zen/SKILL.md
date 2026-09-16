---
id: hermes-cron-zen
name: hermes-cron-zen
version: 1.1.0
description: 'Audit, modify, and heal the Hermes cron subsystem — jobs.json, /root/HERMES/scripts/*, the validator at /root/HERMES/scripts/zen/validate_jobs_json.py. Probe-first, validator-writes-only, review-before-apply. USE WHEN: "cron audit", "jobs.json", "fix broken cron job", "validate jobs.json", "patch cron job", "expand cron patch", "PRN16 / eureka-promote / watchdog-of-watchdogs / syedos-quiet bug", "Telegram token failure in cron", "silent Telegram token failure in cron", "missing script for cron", "convert LLM cron to script", "cron zen", "cron optimization", "kill cron job", "wasteful cron", "cron token savings".'
risk_tier: low
floor_scope: [F1, F2, F11, F13]
autonomy_tier: T1
tags: [hermes, cron, jobs.json, validator, audit, federation-ops]
---

# Hermes-Cron-Zen

> **DITEMPA BUKAN DIBERI — patch the geometry, not the symptom.**
> The cron subsystem writes receipts; the substrate accumulates tribal knowledge; the sovereign reviews diffs.

## Why this skill exists

The Hermes cron subsystem (`jobs.json` + `/root/HERMES/scripts/*` + the validator) is the canonical
keystone for daily federation operations. Three forces collide here:

1. **Stale-context failure**: An agent asked to audit cron in Aug 2026 cited jobs (PRN16 Compare
   Auto-Sync) that had been removed 9 minutes earlier by a separate agent (kimi-code/FI-008). The agent
   produced a 4-tier patch proposal that was already done. The audit cost ~20 minutes of sovereign
   attention; the value was zero. **The lesson: never audit cron from cached memory. Always probe live.**

2. **Path resolver rules**: Hermes cron runner only finds scripts under `/root/HERMES/scripts/`.
   - Bare names work (`morning-brief.sh`, `steel.sh`, `git_to_vault.py`).
   - Relative paths with subdirs (`cron/scripts/foo.sh`) are silently stripped or rejected.
   - Absolute paths outside `/root/HERMES/scripts/` come back as "Blocked: script path resolves
     outside the scripts directory".
   - **Substrate choice**: Park development scripts at `/root/HERMES/cron/scripts/` and either
     symlink into `/root/HERMES/scripts/` or run the full move before scheduling.

3. **Review-before-apply pattern**: Any change to `jobs.json` (deletes, edits, mass migrations) should
   go through the validator with a JSON patch envelope. The validator gives you a diff-and-confirm
   cycle, atomic write, and an automatic receipt. **Direct edits to jobs.json are forbidden by
   substrate convention** — the validator is the only sanctioned writer.

## The four rules (binding)

### Rule 1 — Probe state first. Never audit from cached memory.

Before any audit statement about jobs.json contents, run:

```bash
# 1. SHA + line count + job count
sha256sum /root/HERMES/cron/jobs.json | head -c 16
wc -l /root/HERMES/cron/jobs.json
python3 -c "import json; d=json.load(open('/root/HERMES/cron/jobs.json')); print(len(d['jobs']))"

# 2. List all jobs by id + name + last_status + last_error
python3 -c "
import json
from collections import Counter
d = json.load(open('/root/HERMES/cron/jobs.json'))
for j in sorted(d['jobs'], key=lambda x: x.get('last_run_at') or ''):
    err = (j.get('last_error') or j.get('last_delivery_error') or '')[:60]
    print(f'{j[\"id\"][:12]:12s} | {j[\"name\"][:40]:40s} | {j.get(\"last_status\",\"?\"):8s} | {err}')
"
```

**If any of these contradict your training data, your data is stale. Trust the probe.** This is the
single hardest discipline — agents want to pattern-match "I remember this layout" instead of reading.

### Rule 2 — Hermes cron resolver base is `/root/HERMES/scripts/`

- Bare names resolve against `/root/HERMES/scripts/`. Example: `script: "morning-brief.sh"` → runs
  `/root/HERMES/scripts/morning-brief.sh`.
- Absolute paths outside `/root/HERMES/scripts/` are **blocked** by the resolver with `error: Blocked:
  script path resolves outside the scripts directory`.
- Path prefix `cron/scripts/foo.sh` (relative) is silently stripped to `foo.sh` and looked up under
  `/root/HERMES/scripts/`. If the file is only in `cron/scripts/`, the error is `Script not found`.

#### The fix when scripts are in a sub-directory

Either:
- **Move** the scripts: `mv /root/HERMES/cron/scripts/foo.sh /root/HERMES/scripts/`.
- **Symlink**: `ln -s /root/HERMES/cron/scripts/foo.sh /root/HERMES/scripts/foo.sh`.
- **Revert jobs.json**: set `script: "foo.sh"` (bare name) instead of the absolute path.

**Don't try to "fix" this by setting absolute paths in jobs.json.** The resolver rejects them. The
correct fix is moving the file, not the config.

### Rule 3 — Validator is the only writer of jobs.json

`/root/HERMES/scripts/zen/validate_jobs_json.py` is the canonical writer. It:

1. Validates the patch JSON (provider in live set, cron expr 5-field, enabled bool, delivery in allow-list).
2. Backups current jobs.json to `/root/forge_work/backups/jobs.json.bak-<timestamp>`.
3. **MERGES** each `updates[]` entry into the live store by `search_field`, validates the merged result, atomic-replaces jobs.json.
4. Writes a receipt to `/root/forge_work/backups/jobs.json.receipt-<timestamp>.json`.

**F-005 (fixed 2026-08-14):** the pre-fix `apply` wrote the PATCH FILE itself as jobs.json (never merged) — corrupted 18 jobs to a 770-byte patch payload. Hermes restored from the validator's own backup and patched the store surgically; the validator was then rewritten to merge. Self-test passed (1 update applied, 18 jobs intact). If you ever see jobs.json containing `_meta`/`updates` keys, it is a patch payload, not the store — restore from the newest `jobs.json.bak-*` in /root/forge_work/backups/ immediately.

**Direct edits to jobs.json bypass the validator and break the receipt chain.** If you must edit
directly (e.g. emergency kill), immediately run `validate_jobs_json.py check` afterwards.

Validator apply form:

```bash
python3 /root/HERMES/scripts/zen/validate_jobs_json.py apply /path/to/PATCH.json
```

Patch JSON shape (see `templates/PATCH-minimal.json` for a one-edit example):

```json
{
  "_meta": {"patch_id": "...", "reversible": true, "patched_at_utc": "..."},
  "updates": [
    {"id": "abc123", "name": "...", "search_field": "id", "fields": {"deliver": "local"}}
  ],
  "explicitly_not_patched": [...]
}
```

### Rule 4 — Every patch has a receipt + a rollback

Every `apply` writes:
- `jobs.json.bak-<ts>` in `/root/forge_work/backups/`
- `jobs.json.receipt-<ts>.json` in the same dir

To roll back:

```bash
cp /root/forge_work/backups/jobs.json.bak-<timestamp> /root/HERMES/cron/jobs.json
```

**The receipt is the proof-of-work. Without it, no patch is sovereign-reviewable.**

## The review-before-apply sequence (binding for any T2+ change)

```
1. PROBE   — run Rule 1 verification, find the target jobs
2. DRAFT   — write a patch JSON next to the live state at /root/forge_work/_drafts/<slug>/
3. SHOW    — display the diff in chat (script: foo.sh → /abs/path, deliver: x → y, etc.)
4. WAIT    — explicit "go" / "apply" from human. No drive-by applies.
5. APPLY   — validate_jobs_json.py apply
6. VERIFY  — re-probe per Rule 1; confirm `last_error` and `last_status` shift
7. RECEIPT — point to /root/forge_work/backups/jobs.json.receipt-<ts>.json
```

The kimi-code/FI-008 Aug 5 patch violated step 4 (applied without explicit F13 review). The
retrospective acknowledged the process hit and committed to drafts-first. Same rule applies to all
federation cron changes.

## Common failure modes and their fixes

### "Script not found: /root/HERMES/scripts/<name>.sh"

The script lives somewhere else. Either:
- Move it to `/root/HERMES/scripts/`.
- Symlink it.
- Update jobs.json to the absolute path (only if the path is **inside** `/root/HERMES/scripts/`).

### "Blocked: script path resolves outside the scripts directory"

The jobs.json script field is an absolute path outside `/root/HERMES/scripts/`. **Fix the jobs.json
field, not the script location.** Set the field to a bare name and move the script into place.

### "delivery error: Telegram send failed: You must pass the token"

Hermes cron runner strips provider/bot secrets from cron-script subprocess env (defense in depth).
If a job uses `no_agent=true` + `deliver=telegram:*`, the scheduler can't deliver because it has no
bot token. Two options:
- **Local-first**: change `deliver` to `local`. Job output saved to `/root/.hermes/cron/output/<id>/`.
- **Agent mode**: change `no_agent` to false. The agent loop inherits the full env. (Cost: each
  scheduled run costs tokens.)

### "Provider 'X' not in live set"

The validator at apply-time rejects patches that reference providers not in the live set. Check
`/root/HERMES/config.yaml` provider definitions and the live set. Migrations: server → server
name (e.g. `fed` → `qwen-token-plan-individual`), model version → model version
(`hermes-asi` → `qwen3.7-plus`).

### "Skipped to prevent unintended spend: global inference config drifted" (2026-08-14)

When the global default provider/model changes (e.g. `openai-api/hermes-asi` → `custom/i-arif`),
agent jobs are skipped by the scheduler's drift guard (#44585) — it refuses to spend
on a config the job never consented to.

**Pinning alone is NOT sufficient (2026-08-14 evening cluster).** Six jobs (three Syed caregiver
jobs + arif-world-reality-intel + artifact-drift-audit + seal-integrity-sweep) were skipped at the
20:48 catch-up burst even though their jobs.json `provider`/`model` fields were ALREADY
`qwen-token-plan-individual` / `qwen3.7-plus`. The guard checks the job's consent stamp (last write
time) against the config change, not just field values — jobs saved before the config change fail
until re-saved; jobs re-saved after it sail through the same burst. The fix that worked:
`cronjob action=update job_id=<id>` per affected job, re-asserting the FULL prompt + provider +
model. Overdue jobs then fire immediately as catch-up (two of the six re-ran OK at 21:07 same
evening).

Two verification rules from that cluster:
- `provider_snapshot`/`model_snapshot` in jobs.json still read `openai-api`/`hermes-asi` after a
  successful re-save AND a successful run — they lag cosmetically. Verify healing by
  `last_status: ok` + cleared `last_error`, never by the snapshot fields.
- **Never test-fire caregiver/citizen-facing jobs (they DM a human) to verify a fix.** Let them
  ride their natural schedule; a one-cycle delay beats a 21:00 spam ping. Only self-facing jobs
  (`deliver: local`, or your own sovereign DM) are safe catch-up probes.

`cronjob action=update` REPLACES the prompt wholesale — paste the FULL recovered/as-run prompt,
never a summary. If a job's stored prompt has already been stubbed, recover the as-run text from
its last output file (`/root/.hermes/cron/output/<job_id>/<ts>.md`, `## Prompt` section, slice
from the `You are <job-name>` marker) — those files are the only canonical prompt backup.

New agent jobs MUST be created with an explicit
model+provider pin, never left to inherit the global default. Also: after a gateway restart, the
scheduler catch-up fires all due jobs at once — expect a burst of runs; that is normal, not a bug.

Full evidence trail (job IDs, prompt-recovery recipe, false-unreachable digest):
`references/cron-healing-2026-08-14.md`.

### Inference-path failures that LOOK like cron failures (2026-08-14)

- **`HTTP 504 — HTML error page` after ~50s** = haproxy :4000 (fronting litellm :4011) had
  `timeout client/server 50000`; long reasoning calls get cut mid-flight, Hermes retries 3×,
  job dies. Raised to 600000 on 2026-08-14 (backup: /root/forge_work/backups/haproxy.cfg.bak-20260814);
  reload `kill -HUP $(pgrep -x haproxy)`. Rule: long prompt 504s while short probes 200 → check
  haproxy timeouts FIRST, not the model.
- **`HTTP 503 — HTML error page`** = upstream quota death (MiniMax 429 code 2056 "Token Plan
  usage limit reached") surfaced after retries. Probe the upstream DIRECTLY with the key before
  debugging FED routes. As of 2026-08-14 all 14 agent jobs pinned to `qwen3.7-plus` /
  `qwen-token-plan-individual`.
- **`delivery platform 'telegram' has no gateway credentials configured`** = cron PREFLIGHT
  checking gateway platform health, not the job. The telegram adapter resolves
  `TELEGRAM_BOT_TOKEN` via `get_secret()` which reads `/root/HERMES/.env` as an AUTHORITATIVE
  secret-scope overlay — process env alone is NOT enough. If `.env` was rewritten and lost the
  key, every telegram job blocks with zero tokens spent. Fix: restore the raw-named token into
  `.env` (chmod 600), restart gateway. Beware interpolated values
  (`HERMES_TELEGRAM_BOT_TOKEN=${ASI_BOT_TOKEN}`) — resolve the referenced var; never copy a
  `${...}` literal into `.env`.

### Watchdog jobs must classify honestly (2026-08-14)

Cron watchdogs (seal-integrity-sweep, artifact-drift-audit) screamed "BROKEN 97.9%" / "DRIFT"
for states that were actually UNLINKED_HISTORICAL (old writer never fully linked a FROZEN
ledger) and UNSEALED (artifacts never sealed — no vault entry by name or hash). Watchdog
prompt-design rules:
- Distinguish **broken** (changed after seal / live chain broken) from **never-full** (gaps by
  old writer) from **never-sealed** (backlog). Report all three; only "broken" is an alarm.
- NEVER recommend rewriting/rehashing an append-only ledger — T3, F13 only; say so in the prompt.
- Skip non-seal telemetry rows (FED_HEALTH_PROBE, tool_call) when walking seal chains.
- Health verdict = LIVE ledger tail continuity (last ~50 seal rows), not frozen-ledger fragmentation.
- Never auto-seal batches of artifacts; list the backlog, do not act on it.

### "Kill on error" without investigating root cause (2026-08-15)

When multiple jobs show `last_status: error`, the instinct is to delete them all. **Don't.**
Three Syed caregiver jobs were ERROR — turned out the bot COULD reach the chat (`getChat`
returns `ok: true`). The error was the LLM agent failing, not delivery. Converting to
`no_agent=True` script-only fixed it while preserving the function.

**Diagnostic sequence before any kill:**
1. `curl getChat` — can the bot reach the target chat?
2. Check if an existing script does the same thing
3. Check if the task is deterministic (→ convert to script-only)
4. ONLY kill if: function is truly wasteful (spam, duplicate) OR no script path exists

**What gets lost when you kill without investigating:** caregiving reminders, health
trackers, business notifications. These have human cost beyond token savings.

### Validator rejects a job that was working before

Possibilities:
- Provider was retired (see above).
- Cron expression dropped to 4 fields.
- Delivery target not in allow-list.
- `enabled` is something other than `true`/`false`.

Run `validate_jobs_json.py check <jobs.json>` to see the full list.

## Zen Optimization — LLM to Script Conversion

**Core lesson (2026-08-15):** Many cron jobs use LLM agents (qwen3.7-plus) for deterministic
tasks that a bash/python script handles identically at zero token cost. Audit every LLM job
and ask: "Does this need reasoning, or just execution?"

### When to convert (ALL must be true)
- Task is deterministic: same input → same output every time
- No reasoning/decision-making needed (reminders, status probes, health checks, file scans)
- Script already exists or is trivial to write
- Output is plain text (not analysis requiring judgment)

### Conversion pattern
1. **Investigate before kill.** Don't delete erroring jobs — check WHY they error.
   - Test delivery: `curl -s "https://api.telegram.org/bot${HERMES_TELEGRAM_BOT_TOKEN}/getChat?chat_id=<ID>"`
   - If `ok: true` → delivery works, error is elsewhere (agent failure, prompt issue)
   - If `ok: false` → chat unreachable, fix delivery target or redirect

2. **Check for existing scripts.** Look in `/root/HERMES/scripts/` and `/root/.hermes/scripts/`
   before writing new ones. Many tasks already have bash scripts from earlier iterations.

3. **Write output-only scripts.** With `no_agent=True`, stdout = delivered message.
   Script just outputs text. No curl needed — the cron system handles delivery.

4. **Create with `no_agent=True`.** Set `script` field to bare filename. Set `deliver` to target.
   Model/provider fields become irrelevant.

### Anti-pattern: kill on error without investigating
❌ Job errors → delete it → function lost
✅ Job errors → check `getChat` → check script exists → convert or fix → preserve function

### Token savings example (2026-08-15 audit)
- 6 LLM jobs converted to script-only (seal-integrity-sweep, artifact-drift-audit,
  syed-mak-dressing, syed-gerd-log, syed-sambal-preorder, evening-zen-brief)
- Net: LLM jobs cut from 12 → 7 (42% reduction)
- Functions preserved: all caregiving reminders, health trackers, status probes

### The `no_agent=True` + `deliver` interaction
When `no_agent=True`:
- Script stdout IS the delivered message
- Script should output plain text, NOT use curl (double delivery risk)
- `deliver` field controls where stdout goes (e.g. `telegram:1042200555`)
- If script also curls, user gets TWO messages — avoid this

## Probe vs patch — when to escalate

| Action | Tier | Reversibility |
|---|---|---|
| Read jobs.json, run health probe | T0 | n/a |
| Pause/resume a job | T1 | reversible |
| Edit a single job's fields | T1 | validator receipt |
| Add a new job (cronjob create) | T1 | reversible until removed |
| Remove a disabled/zero-run job | T2 | reversible (jobs.json restored from backup) |
| Bulk migration (provider swap for 15 jobs) | T2 | reversible per-job |
| Edit the script itself (NOT jobs.json) | T2 | git revert + script restart |
| Schedule a new cron primitive | T3 | depends on backend |
| Change Hermes cron runner source | T3 + F13 | requires diagnostic + F13 sign-off |

## Three-system awareness (2026-08-15)

Hermes cron is NOT the only cron system. Three run in parallel:

```
HERMES CRON (hermes cronjob) — 18 jobs, LLM + script-only
/etc/cron.d/ (system crontab) — 25+ raw entries, all infra, no governance
OPENCLAW CRON (migrated) — mostly dead, jobs.json.migrated has 11 entries
```

**Audit must check all three.** Duplicates between Hermes cron and /etc/cron.d/ waste
compute. Example: `institution-mae-pulse` (system cron) and `institution-metrics-pulse`
(Hermes cron) both publish metrics.

### Hermes role boundary

**Hermes = human edge bridge ONLY.** The SOUL.md contract: translate reality for the human.
If a cron job is doing infrastructure work (seal sweeps, drift checks, vault ingestion,
metric publishing) with `deliver: local`, it belongs in OpenClaw, not Hermes.

Filter: `deliver: local` + `no_agent: True` + task is infra → candidate for OpenClaw migration.
Filter: `deliver: telegram:*` + task is human-facing → keep in Hermes.

### False governance signal (NEW failure mode)

forge-weekly.sh ran every Sunday, produced a governance report showing "0/7 days"
for every metric. Looked clean. Was actually dead — upstream daily producers (steel.sh,
silica.sh, intel.sh) were never scheduled. The aggregator counted nothing and reported
it as "all clean".

**Rule: if a rollup/aggregator shows zero across ALL metrics for extended periods, check
whether the upstream producers are actually running. Zero can mean clean OR dead.**

Diagnostic: check `ls cron-receipts/steel-*.json | wc -l` (or equivalent). If zero
receipts exist for the window, the pipeline is broken, not clean.

### Absence of review is not evidence of calibration (companion failure mode, 2026-08-27)

The companion case to "false positive clean" is "false positive calibrated":

```
Zero operator-marked overrides
       ↓
"Zero false positives"
       ↓
Verdict: HARD_REJECT_CANDIDATE
```

Looks calibrated. Was actually unreviewed. **The reviewer hadn't looked yet** —
the dataset is unproven, not proven safe.

**Rule: zero overrides ≠ zero false positives.** A dataset with no operator marks
must produce `INSUFFICIENT_REVIEW`, NOT a promotion-ready verdict. Absence of
evidence is not evidence of absence (F7 HUMILITY).

Diagnostic: compare `manual_override_count` in the summary file against total
dispatches in the underlying audit log. If overrides = 0 AND dispatches > 0,
verdict logic is suspect — confirm the verdict field rejects `HARD_REJECT_CANDIDATE`
when overrides is zero.

### Local-first evidence, Telegram-as-pointer (companion pattern, 2026-08-27)

A daily governance / calibration summary is **evidence**, not a notification.
When the operator reads it, they need to see:

- the audit log row by row
- the operator override marks
- the verdict code with the data that produced it
- the chain hash that ties this run to the prior runs

That is what a file on disk gives them. Telegram gives them a one-line ping
that they glance at. After three days of glances, they stop reading the
underlying ledger and audit discipline weakens silently.

**Rule: evidence lives on disk; notification is at most a pointer, never
the artifact.** Schedule the script with `deliver: local` first, audit the
file regularly, only then add Telegram with **pointer-only** format
("Daily density summary available at <path>") — never the verdict.

Diagnostic: if any governance/calibration watchdog script has
`deliver: telegram:*` without first proving operator file-review discipline,
swap to `deliver: local`. Telegram comes later, after behavior is verified.

---

## Cross-references

- `claim-receipt-discipline` — the discipline for backing any [OBS] claim with a receipt. The
  probe-first rule is its operational expression.
- `deployment-claim-verification` — verify reported counts against live state. Same family of
  check-the-numbers-before-trusting.
- `agentic-infrastructure-ops` — broader systemd + Docker ops, this skill covers only the
  Hermes-cron slice.
- `openclaw-cron-operations` — same shape but for OpenClaw/AGI cron. **Different SQLite store, different
  cron-edit workflow.** Don't conflate.

## Companion references (under this skill)

- `references/jobs-json-shape-2026-08-05.md` — schema fields, deliver allow-list, provider live-set.
- `references/validator-quirks.md` — what the validator does/doesn't catch, runtime-only errors.
- `references/cron-healing-2026-08-14.md` — drift-guard cluster healing, prompt-stub recovery recipe, false "daemon unreachable" digest (versioned status strings need prefix match, not `== "ok"`).
- `references/cron-audit-2026-08-15.md` — full audit trail: LLM→script conversions, Syed delivery diagnosis, token savings breakdown.
- `templates/PATCH-minimal.json` — bare-minimum patch JSON for one edit.
- `templates/PATCH-multi-updates.json` — multi-job migration shape (provider swaps, mass renames).
- `scripts/probe-cron-health.sh` — one-shot T0 probe: bad jobs, broken paths, deliver mismatches.

---

*Forged 2026-08-05 under F13 SOVEREIGN — three live patch cycles (Hermes cron + kimi-code cross-pollination)
yielded the four rules and the review-before-apply sequence.*
*DITEMPA BUKAN DIBERI — probe first, draft second, sovereign gate third.*
