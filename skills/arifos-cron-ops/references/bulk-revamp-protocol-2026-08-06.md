# Bulk Cron Revamp — Human-Cognitive Catalog Rebuild (2026-08-06)

Verified playbook for the "the cron catalog serves the system, not the human" failure mode. Tested with 31 → 20 jobs.

## Symptom

- User asks "why no daily brief?" but the cron log shows the brief did fire.
- Operator feels the cron noise without signal.
- `last_status: ok` on most jobs but operator receives 0-2 Telegram pings/day.
- `last_delivery_error` field is full of "Telegram send failed: You must pass the token..."
- ≥30% of jobs are machine telemetry (sense, verify, heal, drift, entropy, watchdog, snapshot, reality).

## Root cause

The cron catalog grew over time without triage. New jobs got added for federation internals (heartbeats, backups, snapshots) that don't need to fire on the human-facing scheduler. Meanwhile, the human-facing jobs (morning brief, evening digest, weekly reflection) broke silently on provider 401 or Telegram token injection — and no one noticed because the operator stopped reading them.

## Triage framework

For every job, ask three questions:

1. **Audience**: machine / federation / human-intel / human-body / joy?
2. **Delivery**: telegram (working?) / local (silent) / silent_ok?
3. **Liveness**: enabled? provider live? script exists? delivery path working?

If audience=machine AND delivery=local AND it's a federation internal → candidate for systemd timer, not cron.
If audience=human AND delivery=telegram AND last_delivery_error != null → re-pin, don't delete.
If audience=human AND provider=401 → re-pin to live provider.
If last_status=error and the script doesn't exist → orphan chain (e.g. quiet-hours-arbiter.sh execs syedos-receipt-watcher.sh which never existed).

## Bulk revamp procedure (verified 2026-08-06)

```python
import json, time
from pathlib import Path

p = Path("/root/HERMES/cron/jobs.json")
data = json.loads(p.read_text())
jobs = data["jobs"]

# 1. Define TO_REMOVE (machine noise / zen-pruned / zombie)
TO_REMOVE = [
    "SyedOS Receipt Watcher",         # zombie chain, 2483 errors
    "Sense — arif-fazil.com Health Probe",  # machine, not human-facing
    "Verify — arif-fazil.com Drift Audit",  # machine
    "Heal — arif-fazil.com Self-Repair",    # machine (rsync mutator)
    "Reality Snapshot Compiler",            # machine
    "Watchdog of Watchdogs",                # machine
    "Forge→Vault Auto-Ingest",              # machine
    "eureka-promote",                       # machine
    "drift-alert",                          # machine
    "federation-health",                    # machine
    "entropy-watch",                        # machine
    "hermes-hybrid-backup",                 # machine
    "federation-daily-backup",              # machine
    "Temporal Anomaly Detector",            # machine
    "arifos-entropy-audit",                 # machine + 401 dead
    "STEEL · Machine Steel Pulse",          # machine
    "Model Drift Watchdog",                 # machine
    "weekly-deep-brief",                    # 401 dead
    "weekly-reflection",                    # 401 dead
    "Mingguan — Seal Chain + Federation SOT",  # 401 dead + overlap
    "Weekend Bodybuilding Event — SADO",    # zen-pruned, SADO-only (will re-add human-centered)
    "AI Events — SADO",                     # zen-pruned, SADO-only
    "SyedOS Ringkasan Harian",              # zen-pruned, SADO-only
]

# 2. Filter
before = len(jobs)
jobs = [j for j in jobs if j["name"] not in TO_REMOVE]
print(f"Removed {before - len(jobs)}")

# 3. Bulk re-pin dead providers
for j in jobs:
    if j.get("model") == "qwen3.7-plus":
        j["model"] = "mimo-v2.5"
        j["provider"] = "minimax"

# 4. Define new jobs (human-cognitive, around daily rhythm)
def new_job(name, prompt, schedule, deliver="telegram:267378578", model=None, provider=None, skills=None):
    return {
        "id": "".join(c for c in name.lower()[:8] if c.isalnum() or c=="-") + format(int(time.time()) % 10000, "04x"),
        "name": name, "prompt": prompt or "",
        "skills": skills or [], "skill": (skills or [None])[0],
        "model": model, "provider": provider,
        "provider_snapshot": None, "model_snapshot": None, "base_url": None,
        "script": None, "no_agent": model is None,
        "context_from": None, "schedule": schedule,
        "schedule_display": schedule.get("display", ""),
        "repeat": {"times": None, "completed": 0},
        "enabled": True, "state": "scheduled",
        "paused_at": None, "paused_reason": None,
        "created_at": "2026-08-06T11:30:00+08:00",
        "next_run_at": None, "last_run_at": None, "last_status": None,
        "last_error": None, "last_delivery_error": None,
        "deliver": deliver, "origin": None, "enabled_toolsets": None,
        "workdir": None, "fire_claim": None,
    }

new_jobs = [
    new_job("🫀 Body Check-In (06:00 weekdays)",
            "[body check-in prompt with 5 questions: sleep, water, workout, food, stress]",
            {"kind": "cron", "expr": "0 6 * * 1-5", "display": "0 6 * * 1-5"},
            model="mimo-v2.5", provider="minimax"),
    # ... (12 more jobs around daily rhythm)
]

jobs.extend(new_jobs)

# 5. Save
data["jobs"] = jobs
data["updated_at"] = "2026-08-06T11:30:00+08:00"

backup = Path("/root/HERMES/cron/jobs.json.bak-2026-08-06-revamp")
backup.write_text(json.dumps(json.loads(p.read_text()), indent=2))

p.write_text(json.dumps(data, indent=2))

# 6. Validate
import subprocess
r = subprocess.run(["python3", "/root/HERMES/scripts/zen/validate_jobs_json.py", "check"],
                   capture_output=True, text=True, timeout=30)
assert "valid" in r.stdout, r.stdout
```

## Job templates that worked

### Body check-in (06:00 weekdays)
- One question, 5 sub-questions, integer replies
- Emoji prefix, BM casual
- "Jangan lecture. Tanya, dengar, pandang."

### Joy (10:00 Thursday — nearby events)
- web_search 4-6 queries in parallel
- Format: title, location, date, link, SADO energy
- "Kalau tak jumpa event, jangan fabricate. Diam okay."

### F13 Sovereign Question (Sunday 20:00)
- 4 deep questions about the week's decisions
- Don't answer FOR the human. Don't add moral.
- Format: question only, no template reply.

### Weekly Energy Audit (Sunday 14:00)
- 4 dimensions × 1-10 score: body, mind, money, social
- WIN / LOSS / Adjust next week
- "Bukan metrics. Self-awareness."

### Midday Reset (12:30 daily)
- 3 checkboxes: solat / water / walk
- "Pilih satu. Buat." Not lecture.

### ONE Thing (09:00 weekdays)
- Single input: one task that wins the day
- "Buka. Jangan touch apa-apa lain sampai first 25 minit."

## Output

After revamp: validator prints `✅ jobs.json valid (20 jobs, 6 live providers)`.
Catalog composition shifts from 73% machine → 75% human-centered.

## Files

- `/root/HERMES/cron/jobs.json` — live registry
- `/root/HERMES/cron/jobs.json.bak-2026-08-06-revamp` — pre-revamp snapshot (rollback)

## Anti-patterns to avoid

- Don't keep machine telemetry as cron jobs "just in case" — move to systemd.
- Don't keep broken (401/token-error) jobs and pray they'll recover — re-pin or remove.
- Don't add more jobs without first triaging what's there.
- Don't use `qwen-token-plan-individual` if it's been failing for days — switch provider en bloc.