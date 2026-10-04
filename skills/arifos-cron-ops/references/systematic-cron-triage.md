# Systematic Cron Error Triage

> **Canonical since:** 2026-08-10
> **Source:** 11/19 erroring jobs triage session
> **Read this when:** ≥3 cron jobs show last_status=error simultaneously

## The Three Error Categories

| Category | Signal | Diagnosis | Fix |
|----------|--------|-----------|-----|
| **Script-based** (`no_agent=true`) | Script missing, permission denied, exit non-zero | Check script exists + executable + deps | Fix script path or install deps |
| **Agent-based** (`no_agent=false`) | Prompt references dead files, tool access denied, model timeout | Check prompt validity + tool access | Fix prompt or update toolsets |
| **Delivery** | `Forbidden: bot can't send to bot`, token error | Check `deliver` field target | Change deliver to explicit user_id |

## Triage Protocol (5 steps)

### Step 1: Categorize all erroring jobs

```bash
python3 -c "
import json
jobs = json.load(open('/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json'))['jobs']
errors = [j for j in jobs if j.get('last_status') == 'error']
for j in errors:
    typ = 'script' if j.get('no_agent') else 'agent'
    deliver = j.get('deliver', 'unknown')
    print(f'{j[\"name\"]:40s} {typ:8s} deliver={deliver}')
"
```

### Step 2: Check for systemic patterns

**≥3 jobs fail with identical error within 30 min = infrastructure issue.**

Common systemic patterns:
- `RuntimeError: Connection error` — model provider down
- `Forbidden: bot can't send messages to bot` — delivery target is bot itself
- All jobs from same provider fail — API key rotated/exhausted

### Step 3: Diagnose by category

**Script-based:** check existence + executability + stderr
**Agent-based:** check prompt references + toolsets + workdir
**Delivery:** grep deliver field for bot self-messaging

### Step 4: Fix or remove

- Fixable → fix and re-fire
- Obsolete → `cronjob(action='remove')`
- Blocked on infra → pause until fixed

### Step 5: Verify

Re-fire one job from each fixed category.

## The "Majority Erroring" Pattern

When >50% of jobs are erroring, check in order:
1. **Infrastructure** (provider down, gateway restarted) — FIRST
2. **Delivery** (bot self-messaging) — SECOND
3. **Stale prompts** (files moved, tools changed) — THIRD
4. **Individual defects** — LAST (rare when majority fail)

Don't diagnose jobs one-by-one when the majority are broken.
