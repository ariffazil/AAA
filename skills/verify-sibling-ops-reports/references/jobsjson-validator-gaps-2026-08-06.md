# jobs.json Mutation — Validator Gaps, Provider Drift, Tier Mapping (2026-08-06)

Three concrete techniques captured from the eureka-promote Tier-3.8 patch cycle. Distinct from `cron-script-location-vs-jobsjson-2026-08-06.md` (which covers path mismatch); this file covers the deeper validation-and-provider classes of bug.

---

## 1. The validator's hidden gap — `check` reads jobs.json, not the patch

**The trap** (Aug 2026, kimi-code Tier 3.8 patch + Hermes follow-up):

```bash
$ /root/HERMES/scripts/zen/validate_jobs_json.py check /root/forge_work/_drafts/PATCH-cron-paths-v2.json
❌ 15 validation errors: provider 'fed' not in live set ...
```

The `check` command **appears to validate the patch file**, but it actually:
- Reads `/root/HERMES/scripts/zen/validate_jobs_json.py` line 23: `JOBS = Path('/root/HERMES/cron/jobs.json')`
- `check_jobs()` reads from `JOBS`, ignoring any CLI argument
- The patch file argument is **silently ignored** in `check` mode

So `check <patch>` reports errors against the *live* jobs.json, not the patched version. This means:

1. If the live jobs.json has 15 stale `provider=fed` entries, `check` fails even when your patch is clean
2. Pre-applying validation of a patch in isolation is **not possible with `check`** — you must replicate `check_jobs()` logic in your own script
3. The `apply` command (line 88) DOES validate the patch correctly before installing — but you've got no pre-flight signal

**The discipline:**

```python
# Replicate validator's check_jobs() to validate a patch file in isolation
import json, re
from pathlib import Path

PATCH_PATH = Path('/root/forge_work/_drafts/PATCH-cron-paths-v3.json')
PICKER = Path('/root/HERMES/model-picker.yaml')

text = PICKER.read_text()
providers = set()
for m in re.finditer(r'^\s+provider:\s*(\S+)\s*$', text, re.MULTILINE):
    providers.add(m.group(1))

ALLOWED_DELIVER = {'local', 'silent_ok', 'telegram:267378578', 'telegram:-1003753855708',
                   'telegram:-1003815535761', 'telegram:-1004446358629', 'telegram:1042200555',
                   'telegram:8410138119', 'origin', 'telegram:267378578,telegram:-1004446358629'}

d = json.loads(PATCH_PATH.read_text())
errs = []
for i, j in enumerate(d.get('jobs', [])):
    prov = j.get('provider')
    if prov and prov != 'null' and prov not in providers:
        errs.append(f"job[{i}] {j.get('name')[:30]}: provider '{prov}' not in live set")
    dlv = j.get('deliver')
    if dlv and dlv not in ALLOWED_DELIVER:
        errs.append(f"job[{i}] {j.get('name')[:30]}: delivery '{dlv[:40]}' not in allow-list")

if errs:
    print(f"❌ {len(errs)} errors in PATCH")
    for e in errs: print(f"  {e}")
else:
    print(f"✅ PATCH valid: {len(d['jobs'])} jobs")
```

After this passes, run `validate_jobs_json.py apply <patch>` which validates the patch content again *correctly* (the in-memory check uses `check_jobs(new)` on the new data — see line 97).

**Why this matters:** if you skip the in-isolation check and apply directly, the validator's apply path will fail with the **live-state errors** (the 15 stale fed ones) — and your patch will be rejected, even though your patch is clean. You'll think your patch is wrong when actually the live state is wrong.

---

## 2. Provider drift — the silent failure mode for cron jobs

**The bug class:** A cron job has `provider: "fed"` and `model: "hermes-asi"` — both legacy aliases from when `litellm:4000` was the federation gateway. When `litellm` was decommissioned and `hermes-asi` aliasing moved to the model-picker.yaml tiers (`default`/`bulk`/`heavy`/`apex`), the alias kept resolving at the SOT level but at the cron-runner level, `provider: "fed"` was no longer in the live set the validator checks.

**Symptoms:**

| Layer | Symptom |
|---|---|
| jobs.json validator | `provider 'fed' not in live set (['deepseek', 'minimax', 'ollama', 'openrouter', 'qwen-token-plan', 'qwen-token-plan-individual'])` |
| jobs.json in editor | `provider: "fed"` (looks fine, no syntax error) |
| cron run | `last_status: ok` or `error` — depends on whether `hermes-asi` fallback chain caught it |
| model-picker.yaml | `provider: fed` is NOT listed anywhere — alias is **orphan** |

**Why it recurs:** The validator exists since 2026-08-01, but no CI runs `validate_jobs_json.py check` against jobs.json. So drift accumulates silently. The kimi retrospective (Aug 2026) caught it: *"the validator isn't actually catching these errors in CI either — separate gap."*

**The diagnostic:**

```bash
# 1. Run validator manually
/root/HERMES/scripts/zen/validate_jobs_json.py check
# Should print ✅ jobs.json valid. If it prints ❌ N errors, drift has accumulated.

# 2. Find jobs with stale providers
python -c "
import json
live = {'deepseek', 'minimax', 'ollama', 'openrouter', 'qwen-token-plan', 'qwen-token-plan-individual'}
jobs = json.load(open('/root/HERMES/cron/jobs.json'))['jobs']
for j in jobs:
    p = j.get('provider')
    if p and p not in live and p != 'null':
        print(f'{j[\"name\"]:40} provider={p} enabled={j[\"enabled\"]} status={j.get(\"last_status\")}')
"
```

**The fix:** for each stale entry, migrate to a live provider+model. See §3 for the tier-mapping heuristic.

**Why it bit Aug 2026:** 15 jobs had `provider: "fed"`. 11 enabled, 4 disabled. None were returning clean `last_status: ok` — all had either `error` or stale `ok` from before the drift. The cumulative effect: 11 enabled cron jobs running on a dead alias, with the validator's CI gap hiding it.

---

## 3. Tier-mapping heuristic — picking the right live provider+model

When migrating a job from a dead provider to a live one, **the target matters**. Each job's intent determines which tier from `model-picker.yaml` is correct:

| Tier | Provider | Model | Use case | When to pick |
|---|---|---|---|---|
| `bulk` | `qwen-token-plan-individual` | `qwen3.6-flash` | cron jobs, background scans, high-volume summaries | When job is fire-and-forget; speed > quality; cost-free |
| `default` | `qwen-token-plan-individual` | `qwen3.7-plus` | Telegram chat, daily work, casual code | When job generates content for Arif's review; needs reasonable quality |
| `heavy` | `qwen-token-plan-individual` | `deepseek-v4-pro` | code generation, audits, long-context reasoning | When job does analytical work (entailment, scoring, deep analysis) |
| `apex` | `qwen-token-plan-individual` | `glm-5.2` | rare governed judgments, constitutional reasoning | ONLY when job does F13-adjacent constitutional work — and `apex` is "rare," so the job must be infrequent |

**The 7-entry fallback chain** lives in the `default` tier's `fallback_chain` (in model-picker.yaml): Qwen→DS direct→MiniMax→OpenRouter→Qwen Team→Ollama. Picking `default` for unknown jobs is the **conservative choice** because it inherits the thickest fallback chain. Picking `apex` for everything wastes apex-tier capacity on work that doesn't need it.

**Mapping for the 15 stale `fed` jobs (Aug 2026):**

| Job | Function | Target tier |
|---|---|---|
| `evening-digest` | daily summary for Arif | `default` (qwen3.7-plus) |
| `weekly-deep-brief` | weekly summary | `default` |
| `weekly-reflection` | weekly reflection | `default` (DISABLED — field updated but won't run) |
| `ASI World Sensorium — Daily Briefing` | daily intelligence | `heavy` if analysis-heavy; `default` for casual summary |
| `Model Drift Watchdog` | metadata probe, no LLM | None — `provider=None` (script-only or empty `prompt`) |
| `🌙 SyedOS Ringkasan Harian` | Malay daily brief for Syed | `default` (DISABLED) |
| `nightly-seal` | seal metadata | `default` (cheap operation) |
| `Weekend Bodybuilding Event — SADO` | schedule notification | `default` (DISABLED) |
| `AI Events — SADO` | calendar digest | `default` (DISABLED) |
| `Mingguan — Seal Chain + Federation SOT` | weekly audit | `heavy` (audits warrant deep reasoning) |
| `🌙 Rehat Minda — Personal Audit` | weekly reflection | `default` |
| `Human Readiness Pulse` | WELL-organ reflection | `heavy` (F6 empathy+maruah warrants care) |
| `arifos-entropy-audit` | ΔS sweep | `default` (mechanical computation) |
| `🜂 Verify — arif-fazil.com Drift Audit` | drift check | `default` (descriptive not analytical) |
| `🜂 Heal — arif-fazil.com Self-Repair` | repair actions | `heavy` (will execute on result; reasoning matters) |

**Conservative single-target mapping (what I shipped):** all 15 → `default`. This is safe (every job works, thick fallback chain covers all 5 providers) but **suboptimal** (apex-tier work doesn't get apex-tier models; bulk work wastes tokens).

**The follow-up patch discipline:** when migrating providers, don't blast all to `default`. Read each job's `prompt` field and pick the tier that matches the work. The conservative move (`all→default`) is a placeholder, not a destination.

---

## Pitfalls

- **Don't trust `validate_jobs_json.py check <patch>`** to validate the patch — it ignores the argument and validates live jobs.json. Replicate `check_jobs()` in your own script for in-isolation validation.
- **Don't pick `apex` for cron jobs** unless the work is genuinely constitutional. Apex tier is "rare" per model-picker.yaml — using it for daily summaries wastes capacity and creates a congestion point when apex work actually fires.
- **Don't pick `bulk` for content Arif reads** — qwen3.6-flash is fine for fire-and-forget, but daily briefings deserve qwen3.7-plus for quality.
- **Don't assume `provider: null` means "dead job"** — script-only jobs (no LLM) have `provider: null` because they don't need a model. The validator's `check_jobs` skips None providers (line 65: `if prov and prov != 'null'`), so None is fine.
- **CI integration is missing** — there's no scheduled `validate_jobs_json.py check` running anywhere. Drift accumulates silently until someone manually runs it. Add to the audit-freshness watchdog (suggested pattern below).

---

## Suggested follow-up: the audit-freshness watchdog

A self-policing cron that catches this class of bug without human intervention:

```bash
#!/bin/bash
# /root/HERMES/cron/scripts/jobs-json-path-check.sh
# Hourly: walk jobs.json, verify every script exists, check provider is in live set.
# Silent when GREEN; single-line FAIL message + last_good_ts on first drift.
set -uo pipefail

JOBS=/root/HERMES/cron/jobs.json
STATE=/tmp/jobs_audit_last_good

# Run validator check
if /root/HERMES/scripts/zen/validate_jobs_json.py check >/dev/null 2>&1; then
    echo "$(date -u +%FT%TZ)" > "$STATE"
    exit 0  # silent on GREEN
fi

# Drift detected — print first failure
ERRORS=$(/root/HERMES/scripts/zen/validate_jobs_json.py check 2>&1 | grep -c "❌")
LAST_GOOD=$(cat "$STATE" 2>/dev/null || echo "never")
echo "⚠️ jobs.json drift: $ERRORS validation errors. Last clean: $LAST_GOOD"
exit 0
```

Register as a new cron job: `script: /root/HERMES/cron/scripts/jobs-json-path-check.sh`, `schedule: { kind: interval, minutes: 60 }`, `deliver: local`, `no_agent: true`. The job self-policing the registry is itself an example of F11 AUDITABILITY closing the void.

---

## Cross-references

- `references/cron-script-location-vs-jobsjson-2026-08-06.md` — the path-mismatch class (related but distinct: paths vs providers).
- `references/cron-model-ref-fix-2026-08-05.md` — the SQLite `payload_model` column case (different storage, same drift symptom).
- §4.2b of SKILL.md — governance enforcement audit: ENFORCED vs PARTIAL vs ABSENT, same discipline applies to "validator in CI" — currently ABSENT.
- The Pitfalls section in SKILL.md — the "cron path-mismatch + token-strip double-failure (2026-08-06, kimi-code Tier 3.8)" entry already captures the surface symptom; this reference covers the **validator-side** reasons it slipped past CI.