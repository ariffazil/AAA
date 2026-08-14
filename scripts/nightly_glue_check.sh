#!/usr/bin/env bash
# nightly_glue_check.sh — glue-surface verify for the nightly duty slot.
# Exit 0 = clean. Exit 2 = HOLD signal (drifted/unknown bytes) — judge material,
# and per triage rule (EUREKA_COMPILATION §2.2) the flag must NOT be routed
# solely to the flagged file's last author.
#
# PROPOSED CRON LINE (word-gated per infra-crons doctrine — do not self-install):
#   15 2 * * * /root/AAA/scripts/nightly_glue_check.sh >> /var/log/arifos/cron.log 2>&1
set -uo pipefail
LOG=/root/.arifos/registries/glue-verify.log
OUT=$(/root/AAA/scripts/glue_sweep.py verify 2>&1); RC=$?
printf '%s rc=%d\n%s\n' "$(date -u +%FT%TZ)" "$RC" "$OUT" >> "$LOG"
if [ "$RC" -ne 0 ]; then
  echo "GLUE_DRIFT_HOLD: rc=$RC — see $LOG" >&2
fi
exit "$RC"
