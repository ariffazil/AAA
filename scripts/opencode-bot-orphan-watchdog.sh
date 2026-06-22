#!/bin/bash
# /root/.openclaw/workspace/scripts/opencode-bot-orphan-watchdog.sh
# Watchdog: kill any bot.py process NOT inside the opencode-bot.service cgroup.
#
# Why: 2026-06-07 an orphan bot.py (PID 2022663) appeared in the
# openclaw-gateway.service cgroup and fought the legit systemd-managed bot
# for the same Telegram long-poll slot. Result: 409 Conflict spam, bot
# appears to "timeout" to the user. Only the systemd-managed instance is
# allowed to own the @arifOS_bot token.
#
# Rule: legit = cgroup contains "/opencode-bot.service". Anything else dies.
# This is reversible (the legit systemd unit restarts the bot, not us).
# 1-line log per kill, audit-friendly.

set -u
SCRIPT_NAME="opencode-bot-orphan-watchdog"
LOG="/var/log/${SCRIPT_NAME}.log"
mkdir -p "$(dirname "$LOG")"
ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

KILLED=0
# Iterate every python3 process running the opencode-bot entry point.
# Exclude the grep / our own process and the parent shell.
for pid in $(pgrep -f "opencode-bot/bot.py" 2>/dev/null); do
  # Skip our own pid (shouldn't match, but safety)
  [ "$pid" = "$$" ] && continue
  # Skip the parent shell that called us
  ppid=$(awk '{print $4}' "/proc/$pid/stat" 2>/dev/null)
  [ "$ppid" = "$$" ] && continue

  cgroup=$(cat "/proc/$pid/cgroup" 2>/dev/null | head -1)
  cgroup_unit=$(echo "$cgroup" | awk -F'/' '{print $NF}')

  if echo "$cgroup_unit" | grep -q "opencode-bot.service"; then
    # Legit — leave it.
    continue
  fi

  # Orphan: kill it.
  cmd=$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null)
  echo "$(ts) KILL pid=$pid cgroup=$cgroup_unit cmd=${cmd:0:160}" >> "$LOG"
  kill -TERM "$pid" 2>/dev/null
  sleep 1
  # If still alive (stuck like the PTB Conflict state), escalate.
  if kill -0 "$pid" 2>/dev/null; then
    echo "$(ts) KILL_FORCE pid=$pid (TERM ignored)" >> "$LOG"
    kill -KILL "$pid" 2>/dev/null
  fi
  KILLED=$((KILLED + 1))
done

# Quiet success path — no kill = no log noise. Watchdog pattern: silent on
# healthy, loud on action. (See cron registration: every 5 minutes.)
exit 0
