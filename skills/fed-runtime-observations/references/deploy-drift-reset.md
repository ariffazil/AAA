# Deployment Drift Reset — arifOS kernel

> Captured 2026-08-12 after a session where `arifOS` kernel reported
> `deployment_drift_status: drift_detected` and blocked a topic-branch push.
> Fix: write the current built_commit to the deploy marker, then restart.

## Symptom

```
[gate] GATE 3: deploy drift check (:8088/health vs git HEAD)
  ❌ deployed=074d32bf42c0 HEAD=c321c21faa9f drift=True runtime_drift=False status=degraded
```

## Root cause

`/opt/arifos/app/.git_commit` was stale (last written by an earlier deploy).
The kernel reads this file on boot and compares to the actual built_commit
in `software_release.built_commit`. If they don't match → drift_detected.

## Fix (5 commands)

```bash
# 1. Inspect the marker
ls -la /opt/arifos/app/.git_commit
cat /opt/arifos/app/.git_commit

# 2. Probe current built_commit from /health
curl -s http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
sw = d.get('software_release', {})
print(f'source:   {sw.get(\"source_commit\")}')
print(f'built:    {sw.get(\"built_commit\")}')
print(f'deployed: {sw.get(\"deployed_commit\")}')
print(f'drift:    {sw.get(\"drift\")}')
"

# 3. Write built_commit to marker
BUILT=$(curl -s http://127.0.0.1:8088/health | python3 -c "import json,sys; print(json.load(sys.stdin)['software_release']['built_commit'])")
echo "$BUILT" > /opt/arifos/app/.git_commit

# 4. Restart the service to pick up the marker
systemctl restart arifos

# 5. Verify alignment (allow ~5s for boot)
sleep 8
curl -s http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
sw = d.get('software_release', {})
ok = sw.get('source_commit') == sw.get('built_commit') == sw.get('deployed_commit')
print('ALIGNED ✅' if ok else 'STILL DRIFTED ❌')
print(f'status={d.get(\"status\")}, drift_status={d.get(\"deployment_drift_status\")}')
"
```

## Pre-push guard then re-attempts

After alignment, the pre-push guard's GATE 3 will pass. Re-attempt:

```bash
GIT_TERMINAL_PROMPT=0 git -c "credential.helper=!gh auth git-credential" \
  push -u origin <branch>
```

GATE 1 (pytest) may still fail with two known vault defects:
- `test_outcomes_jsonl_parseable_majority` — multi-line JSON entries in VAULT999
- `test_no_null_id_entries_on_parseable_lines` — Opus 5 known issue (accepted by guard logic if it's the ONLY failure)

If `test_outcomes_jsonl_parseable_majority` fails too, **the vault has 583/47710
lines unparseable (1.22%)**. This is real F11 AUDITABILITY debt. Surface to F13 —
do NOT silently clean VAULT999 (T3 irreversible).

## Caveat

This recipe is for **clearing GATE 3 (drift)**. It does NOT bypass GATE 1
(test failures). If pytest fails for vault reasons, the push is genuinely blocked
for constitutional reasons, not configuration reasons.