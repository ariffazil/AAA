# Hallucination False Positive — Wrong-Path Verification

> PROVEN 2026-08-26. Cron mesh + RSI engine audit.
> Verifier declared 6 artifacts "hallucinated" after checking ONE path.

## The Incident

An agent reported 6 artifacts at canonical locations:
- `cron_graph.json` → `/root/.local/share/arifos/state/`
- `cron_mesh_flow.py` → `/root/HERMES/scripts/zen/`
- `cron_rsi_calibration.json` → `/root/.local/share/arifos/state/`
- `cron_rsi_ledger.jsonl` → `/root/.local/share/arifos/state/`
- `metabolize_cron.py` → `/root/scripts/`
- `validate_jobs_json.py` → `/root/HERMES/scripts/zen/`

The verifier checked ONLY `/root/AAA/cron/` — found nothing — and produced a detailed
table declaring all 6 "MISSING" with status "NOT FOUND." The verdict was presented as
evidence of fabrication.

The user corrected with a path mapping. All 6 files existed at their canonical locations.
All executed clean. All produced verifiable output.

## Why This Is Worse Than No Verdict

A "not found" verdict from a single-path probe carries the authority of verification.
The user trusted the verifier's table. The real work was dismissed. The user had to
do the verifier's job — mapping canonical paths and re-verifying.

This is two errors compounded:
1. Wrong path (pitfall #52 — path confusion)
2. Presenting absence-at-one-path as positive evidence of fabrication

## Detection Protocol

When an agent reports files at specific paths and you need to verify:

```bash
# 1. Check the claimed paths
ls -la /claimed/path/file 2>/dev/null

# 2. If absent, search the full filesystem
find /root -maxdepth 4 -name "filename" 2>/dev/null

# 3. Check for symlinks (files may be symlinked from canonical to convenience paths)
find /root -maxdepth 4 -lname "*filename*" 2>/dev/null

# 4. Check the agent's session log for actual write commands
# (session_search for the agent's tool calls)

# 5. Only declare "not found" after ALL four probes return empty
```

## Rule

**NEVER declare "hallucinated" from a single-path probe.**

A fabrication verdict requires positive evidence (the file was never written, the
function doesn't exist, the commit has no matching diff). Absence at one path is
NOT positive evidence — it's absence at one path.

## Companion Pitfalls

- Pitfall #1: self-claims need live probing (applies to the ORIGINAL report)
- Pitfall #52: path confusion (/root/HERMES/ ≠ /root/.hermes/)
- Pitfall #31: file NAMING a capability ≠ IMPLEMENTING it
- This pitfall: applies to the VERIFICATION of the report — the verifier's own
  methodology was flawed, not just the agent's claim
