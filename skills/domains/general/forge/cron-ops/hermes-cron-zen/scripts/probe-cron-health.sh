#!/usr/bin/env bash
# probe-cron-health.sh — one-shot T0 probe of the Hermes cron subsystem.
#
# Per hermes-cron-zen SKILL.md, reports the three T0 failure classes:
#   1. BAD JOBS        — jobs.json unparseable, or jobs missing required keys
#   2. BROKEN PATHS    — a job's `script` does not resolve under the resolver base
#                        (/root/HERMES/scripts/); covers the documented failure
#                        modes: bare name missing, relative path stripped,
#                        absolute path blocked
#   3. DELIVER MISMATCH— a job with no deliverable target, or deliver set while
#                        the job is explicitly silent
#
# Silent-on-green is NOT used here (this is a T0 probe run by hand, not a
# watchdog); it prints a compact report and exits non-zero if anything is red.
#
# Usage: bash scripts/probe-cron-health.sh

set -uo pipefail

JOBS_JSON="${JOBS_JSON:-/root/HERMES/cron/jobs.json}"
SCRIPTS_DIR="${SCRIPTS_DIR:-/root/HERMES/scripts}"
VALIDATOR="/root/HERMES/scripts/zen/validate_jobs_json.py"

red=0
note() { printf '  %s\n' "$*"; }
head1() { printf '\n== %s\n' "$*"; }

head1 "jobs.json identity"
if [ ! -f "$JOBS_JSON" ]; then
  echo "FATAL: $JOBS_JSON not found"
  exit 2
fi
sha256sum "$JOBS_JSON" | head -c 16; echo "  (sha256 prefix)"
echo "  bytes: $(wc -c < "$JOBS_JSON")  lines: $(wc -l < "$JOBS_JSON")"

if [ -f "$VALIDATOR" ]; then
  head1 "validator"
  if python3 "$VALIDATOR" "$JOBS_JSON"; then
    note "validator: OK"
  else
    note "validator: FAILED"; red=1
  fi
else
  note "validator not present at $VALIDATOR (skipped)"
fi

head1 "[1] bad jobs / [2] broken script paths / [3] deliver mismatches"
python3 - "$JOBS_JSON" "$SCRIPTS_DIR" <<'PY'
import json, os, sys

jobs_path, scripts_dir = sys.argv[1], sys.argv[2]
try:
    with open(jobs_path) as fh:
        data = json.load(fh)
except Exception as exc:
    print(f"  BAD JOBS: jobs.json unparseable: {exc}")
    raise SystemExit(1)

jobs = data.get("jobs", data if isinstance(data, list) else [])
if isinstance(jobs, dict):
    jobs = [dict(v, id=k) for k, v in jobs.items()]

bad = broken = deliver = 0

for job in jobs:
    jid = job.get("id") or job.get("name") or "<unnamed>"

    # [1] required keys
    missing = [k for k in ("schedule",) if not job.get(k)]
    if missing:
        print(f"  BAD JOB   {jid}: missing {', '.join(missing)}")
        bad += 1

    # [2] script path resolution
    script = job.get("script")
    if script:
        if os.path.isabs(script):
            if not script.startswith(scripts_dir.rstrip("/") + "/"):
                print(f"  BROKEN    {jid}: absolute path blocked by resolver: {script}")
                broken += 1
            elif not os.path.exists(script):
                print(f"  BROKEN    {jid}: file does not exist: {script}")
                broken += 1
        else:
            base = os.path.basename(script)   # relative subdirs are stripped
            target = os.path.join(scripts_dir, base)
            if not os.path.exists(target):
                print(f"  BROKEN    {jid}: not under {scripts_dir}: {script} -> {target}")
                broken += 1

    # [3] deliver mismatch
    deliver = job.get("deliver") or job.get("deliver_to")
    silent = job.get("no_agent") is True or job.get("silent") is True
    if not deliver:
        print(f"  DELIVER   {jid}: no deliver target set")
        deliver += 1
    elif silent and deliver not in ("none", "silent"):
        print(f"  DELIVER   {jid}: silent job still declares deliver={deliver!r}")
        deliver += 1

print(f"\n  totals: bad_jobs={bad} broken_paths={broken} deliver_mismatch={deliver}")
raise SystemExit(1 if (bad or broken) else 0)
PY
rc=$?
[ $rc -ne 0 ] && red=1

head1 "verdict"
if [ $red -eq 0 ]; then echo "  GREEN — no T0 cron defects found"; else echo "  RED — see findings above"; fi
exit $red
