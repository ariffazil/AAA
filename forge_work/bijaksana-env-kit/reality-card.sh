#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# AAA BIJAKSANA REALITY CARD — metabolizes tersirat → tersurat on demand.
# Generated LIVE from the machine. Never cached, never hand-edited.
# Output expires the moment it prints: older than 10 min = UNKNOWN, re-run.
# v1.1 · 2026-10-05 · absorbed from external audit: scheduled writers, deleted-but-open, journal errors
# ═══════════════════════════════════════════════════════════════
set -u

echo "╔══ AAA REALITY CARD · $(date '+%Y-%m-%d %H:%M:%S %Z') ══"
echo "║ WHO    : $(id -un)@$(hostname) · uid=$(id -u) · BLAST RADIUS = whole machine"
_git=""
_b=$(git -C "$PWD" symbolic-ref --short HEAD 2>/dev/null) && _git="· git $_b"
[ -n "$(git -C "$PWD" status --porcelain 2>/dev/null | head -1)" ] && _git="$_git (dirty)"
echo "║ WHERE  : ${PWD} ${_git}"
_dopen=$(lsof +L1 2>/dev/null | tail -n +2 | wc -l)
echo "║ VITALS : load=$(cut -d' ' -f1-3 /proc/loadavg) · mem=$(free -h | awk '/^Mem:/{print $3"/"$2}') · disk=$(df -h / | awk 'NR==2{print $5" used, "$4" free"}') · del-open=$_dopen"
# Signal only: count UP, list FAILED. Timer-driven oneshots sitting "inactive"
# between fires are NORMAL — they are noise, not alarms. Full depth: run `organs`.
_up=0; _failed=""
while read -r s; do
    [[ "$s" == *@* ]] && continue   # template units are not instances
    _st=$(systemctl is-active "$s" 2>/dev/null || true)
    case "$_st" in
        active) _up=$((_up+1)) ;;
        failed) _failed="$_failed ${s%.service}:failed" ;;
    esac
done < <(systemctl list-unit-files --type=service --no-legend 2>/dev/null \
         | awk '{print $1}' | grep -E '^(arif|geox|wealth|well|hermes|fed|chron|frame|a-?forge|1mcp|aaa|apa|mcp)' || true)
echo "║ ORGANS : ${_up} federation services UP${_failed:+ · ALARM:${_failed}} (detail: organs)"
_t=$(systemctl list-timers --all --no-pager 2>/dev/null | grep -c '\.timer' || true)
_cr=$(crontab -l 2>/dev/null | grep -cvE '^#|^$' || true); _crd=$(ls /etc/cron.d/ 2>/dev/null | wc -l)
echo "║ SCHED  : ${_t} timers · ${_cr} crontab · ${_crd} cron.d — silent writers; re-probe any file after edits"
echo "║ SECRETS: $(find /root/.secrets -maxdepth 1 -type f 2>/dev/null | wc -l) files present (values never shown)"
_c=/root/AAA/registries/AGENTS_UNIFIED.yaml
if [ -r "$_c" ]; then
    echo "║ CANON  : $(sha256sum "$_c" | cut -c1-12) AGENTS_UNIFIED.yaml · AAA branch=$(git -C /root/AAA branch --show-current 2>/dev/null || echo '?') dirty=$(git -C /root/AAA status --porcelain 2>/dev/null | wc -l)"
else
    echo "║ CANON  : registry MISSING — treat all agent identities as UNKNOWN"
fi
_p=$(pgrep -fc '[k]imi-code|[c]laude|[c]odex|[q]wen|[o]pencode' 2>/dev/null); _p=${_p:-0}
_tm=$(tmux ls 2>/dev/null | wc -l); _sc=$(screen -ls 2>/dev/null | grep -c Detached || true)
echo "║ PEERS  : ${_p} agent processes · tmux:${_tm} · screen:${_sc}"
_je=$(journalctl -p err --since '1 hour ago' --no-pager -q -o short-iso 2>/dev/null | grep -cE '^[0-9]{4}-')
_js=$(journalctl --disk-usage 2>/dev/null | grep -oE '[0-9.]+[MG]' | head -1)
echo "║ ERRORS : ${_je} journal error entries (1h) · logs ${_js:-?} on disk"
echo "║ RULES  : money·irreversible·canon·ports·direction = HUMAN ONLY"
echo "╚════════════════════════════════════════════════════════════"
