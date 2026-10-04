#!/bin/bash
# hermes-config-effective.sh — probe which config.yaml / SOUL.md the live Hermes
# gateway ACTUALLY loads, and simulate the effective agent.{clarify_timeout,
# task_completion_guidance, ...} values via load_config() deep-merge.
#
# Usage: bash hermes-config-effective.sh [unit-name]
#   default unit-name: hermes-asi-gateway.service
#
# Returns:
#   - Resolved HERMES_HOME (unit-declared + proc/environ injection)
#   - Effective values from load_config_readonly() simulation
#   - Code DEFAULT_CONFIG values for comparison
#
# Verification target: any sibling claim of the form "I flipped <key> X→Y in
# <file>" must be checked here before accepting as live.

set -u

UNIT="${1:-hermes-asi-gateway.service}"
HERMES_PY="/usr/local/lib/hermes-agent/venv/bin/python3"

if ! command -v systemctl >/dev/null 2>&1; then
  echo "❌ systemctl not found — run on the host with systemd, not in a container." >&2
  exit 2
fi

if ! systemctl cat "$UNIT" >/dev/null 2>&1; then
  echo "❌ unit '$UNIT' not found. systemctl status '$UNIT' to debug." >&2
  exit 2
fi

PID="$(systemctl show "$UNIT" -p MainPID --value 2>/dev/null)"
if [[ -z "$PID" || "$PID" == "0" ]]; then
  echo "❌ $UNIT has no MainPID — service not running." >&2
  exit 2
fi

echo "════════════════════════════════════════════════════════════"
echo " UNIT         : $UNIT"
echo " MainPID      : $PID"
echo "════════════════════════════════════════════════════════════"
echo

# 1. HERMES_HOME declared by the unit
echo "─── HERMES_HOME declared by unit ─────────────────────────────"
unit_home="$(systemctl cat "$UNIT" 2>/dev/null | awk -F= '/^Environment=HERMES_HOME=/{print $2; exit}')"
echo "  unit-declared : ${unit_home:-<not set in unit>}"
echo

# 2. HERMES_HOME injected into the live process
echo "─── HERMES_HOME in /proc/$PID/environ ───────────────────────"
proc_home="$(tr '\0' '\n' < "/proc/$PID/environ" 2>/dev/null | awk -F= '/^HERMES_HOME=/{print $2; exit}')"
echo "  proc-injected  : ${proc_home:-<not set in env>}"
echo

# 3. Resolved home — prefer proc (what the process actually sees)
RESOLVED="${proc_home:-${unit_home:-/root/.hermes}}"
echo "═══ RESOLVED HERMES_HOME = $RESOLVED"
echo

if [[ ! -d "$RESOLVED" ]]; then
  echo "❌ resolved home does not exist: $RESOLVED" >&2
  exit 3
fi

# 4. config.yaml + SOUL.md at the resolved home
echo "─── Files at \$HERMES_HOME ─────────────────────────────────────"
for f in config.yaml SOUL.md profiles/active_profile; do
  if [[ -e "$RESOLVED/$f" ]]; then
    stat -c '  %y  %s bytes  %n' "$RESOLVED/$f"
  else
    echo "  <missing>  $RESOLVED/$f"
  fi
done
echo

# 5. Effective agent.* values via load_config() simulation
echo "─── Effective agent.* values (load_config_readonly) ─────────"
if [[ ! -x "$HERMES_PY" ]]; then
  echo "  ⚠️  python venv missing — falling back to raw grep"
  if [[ -f "$RESOLVED/config.yaml" ]]; then
    grep -E "^[[:space:]]+(clarify_timeout|task_completion_guidance):" "$RESOLVED/config.yaml" | sed 's/^/  /'
  fi
else
  HERMES_HOME="$RESOLVED" "$HERMES_PY" -c "
import os, sys
os.environ['HERMES_HOME'] = os.environ.get('HERMES_HOME', '$RESOLVED')
try:
    from hermes_cli import config
    cfg = config.load_config_readonly()
except Exception as e:
    print(f'  ⚠️  load_config failed: {e}')
    sys.exit(0)
agent = cfg.get('agent') or {}
for k in ('clarify_timeout', 'task_completion_guidance'):
    v = agent.get(k)
    print(f'  {k:<24} = {v!r}')
"
fi
echo

# 6. Code DEFAULT_CONFIG values for comparison (the "before" baseline)
echo "─── Code DEFAULT_CONFIG baseline ────────────────────────────"
DEFAULT_PY='
import sys
sys.path.insert(0, "/usr/local/lib/hermes-agent")
try:
    from hermes_cli.config import DEFAULT_CONFIG
    a = (DEFAULT_CONFIG or {}).get("agent") or {}
    for k in ("clarify_timeout", "task_completion_guidance"):
        print(f"  {k:<24} = {a.get(k)!r}  # code default")
except Exception as e:
    print(f"  ⚠️  could not read DEFAULT_CONFIG: {e}")
'
if [[ -x "$HERMES_PY" ]]; then
  HERMES_HOME="$RESOLVED" "$HERMES_PY" -c "$DEFAULT_PY"
fi
echo
echo "════════════════════════════════════════════════════════════"
echo " Verdict: if effective == default, sibling claims of"
echo " 'flipped from X' with X != default are wrong on the BEFORE"
echo " side too. If effective == default but file at \$HERMES_HOME"
echo " shows the flip, the edit lives but is not loaded."
echo "════════════════════════════════════════════════════════════"