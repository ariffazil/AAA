#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# AAA FILE PROBE v1 — honest tersirat for ONE file. Read-only.
# Usage: fileprobe <path> [--no-content]
# safety is NEVER "safe": UNKNOWN | CLEAR | HOLD. Stale the moment it prints.
# Cost note: runs a full open-file scan (~1s) — intended for canon/R2-grade files.
# v1 · 2026-10-05 · FI-008 · referee-sealed semantics (Gemini header, Copilot fixes)
# ═══════════════════════════════════════════════════════════════
set -u
p="${1:?usage: fileprobe <path> [--no-content]}"
content=1; [ "${2:-}" = "--no-content" ] && content=0
[ -e "$p" ] || [ -L "$p" ] || { echo "FILE_PROBE: no such path: $p"; exit 1; }
p="$(readlink -f "$p")"
ts=$(date '+%Y-%m-%dT%H:%M:%S%z')
if [ -L "$p" ]; then typ="symlink -> $(readlink "$p")"; [ -e "$p" ] || typ="$typ (BROKEN)"
else typ=$(stat -c %F "$p"); fi
inode=$(stat -c %i "$p"); hl=$(stat -c %h "$p"); mod=$(stat -c %y "$p" | cut -d. -f1)
sha=$(sha256sum "$p" 2>/dev/null | cut -c1-12); sha="${sha:-n/a}"
open_by=$(lsof "$p" 2>/dev/null | tail -n +2 | awk '{print $1"(pid "$2","$4")"}' | sort -u | tr '\n' ' '); open_by="${open_by:-none}"
locks=$(lslocks 2>/dev/null | grep -F "$p" | awk '{print $2":"$6}' | tr '\n' ' '); locks="${locks:-none}"
if lsof +L1 2>/dev/null | grep -qF "$p"; then dopen="yes"; else dopen="no"; fi
imm=$(lsattr -d "$p" 2>/dev/null | awk '{print $1}')
attrs=""
echo "$imm" | grep -q "i" && attrs="$attrs immutable"
echo "$imm" | grep -q "a" && attrs="$attrs append-only"
attrs="${attrs:- none}"
writers=$( { crontab -l 2>/dev/null; cat /etc/cron.d/* 2>/dev/null; } | grep -cF "$p" || true)
units=$(grep -rlF "$p" /etc/systemd/system/ 2>/dev/null | xargs -r -n1 basename 2>/dev/null | tr '\n' ' '); units="${units:-none}"
wmounts="none"
if command -v docker >/dev/null 2>&1 && [ -n "$(docker ps -q 2>/dev/null | head -1)" ]; then
    wmounts=$(docker ps -q 2>/dev/null | xargs -r docker inspect -f '{{.Name}} {{range .Mounts}}{{.Source}} {{end}}' 2>/dev/null | grep -F "$p" | head -2 | tr '\n' ' '); wmounts="${wmounts:-none}"
fi
# Safety: HOLD on kernel locks · CLEAR only when every check passes · else UNKNOWN
if [ "$attrs" != " none" ]; then
    s="HOLD (kernel-locked:$attrs — removal is a human-only F13 decision)"
elif [ "$dopen" = "yes" ]; then
    s="UNKNOWN (deleted-but-open — a dead handle still owns this path)"
elif [ "$open_by" = "none" ] && [ "$locks" = "none" ] && [ "$writers" = "0" ] && [ "$units" = "none" ] && [ "$wmounts" = "none" ]; then
    s="CLEAR (as of print · re-probe after any edit · never 'safe')"
else
    s="UNKNOWN (writer/holder present — see fields above)"
fi
cat <<EOF
[FILE_REALITY_STATE @ $ts]
path: $p
type: $typ · inode: $inode · hardlinks: $hl
sha256: $sha · modified: $mod
open_by: $open_by
locks: $locks
deleted_but_open: $dopen
kernel_flags:$attrs
scheduled_writers: $writers cron refs · units: $units
container_mounts: $wmounts
safety: $s
EOF
if [ "$content" = 1 ]; then echo "---"; echo "[CONTENT]"; cat "$p" 2>/dev/null; fi
