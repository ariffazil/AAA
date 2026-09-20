#!/usr/bin/env bash
# probe-bypass.sh — enforcement-coverage probe for a command claimed to be gated.
#
# READ-ONLY. Runs the intercepted command NORMALLY (not through its guard) and resolves
# its identity on every PATH entry. If step 5 succeeds, the bypass is open no matter what
# the guard's own acceptance suite reports.
#
# Usage:  probe-bypass.sh <cmd> [args...]
# Example: probe-bypass.sh gws gmail users labels list --params '{"userId":"me"}'
#
# Interpreting the result:
#   step 5 exit 0    -> CONVENTION_GATE at best. Bypass reachable from a normal shell.
#   step 5 denied    -> then check steps 3/4 for an alternate path the shim missed.
#   step 5 not found -> re-check step 1; you may be probing the wrong name.
set -uo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 <cmd> [args...]" >&2
  exit 2
fi

CMD="$1"; shift

printf '=== 1. command identity on PATH ===\n'
type -a "$CMD" 2>&1 || echo "NOT ON PATH"

printf '\n=== 2. resolved target of each PATH hit ===\n'
which -a "$CMD" 2>/dev/null | while read -r p; do
  printf '%-42s -> %s\n' "$p" "$(readlink -f "$p" 2>/dev/null)"
done

printf '\n=== 3. shim locations (a shim OFF the PATH enforces nothing) ===\n'
FOUND_SHIM=0
for d in /usr/local/bin /usr/bin /bin "$HOME/.local/bin"; do
  if [ -e "$d/$CMD" ]; then
    ls -la "$d/$CMD"
    FOUND_SHIM=1
  fi
done
[ "$FOUND_SHIM" -eq 0 ] && echo "(no binary named '$CMD' in the common PATH dirs)"

printf '\n=== 4. shell rc / profile shims ===\n'
grep -n "$CMD" "$HOME/.bashrc" "$HOME/.profile" "$HOME/.bash_profile" /etc/profile 2>/dev/null \
  || echo "(no alias or wrapper in shell rc)"

printf '\n=== 5. DIRECT INVOCATION — the actual test ===\n'
"$CMD" "$@"
exit_code=$?
echo "exit=$exit_code"

printf '\n=== verdict input ===\n'
if [ "$exit_code" -eq 0 ]; then
  echo "EXIT 0: the intercepted command succeeded from a normal shell."
  echo "Verdict may be CONVENTION_GATE. Do NOT report CHOKEPOINT."
else
  echo "EXIT $exit_code: refused on the normal path."
  echo "Now re-check steps 3 and 4 for an alternate path before claiming full coverage."
fi
