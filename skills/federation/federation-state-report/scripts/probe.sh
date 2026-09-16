#!/usr/bin/env bash
# Read-only federation state probe — four layers.
# Run from the truth node (KVM8). Writes nothing, mutates nothing.
set -uo pipefail

BAR="========================================================"
echo "$BAR"
echo "[1/4] MACHINE"
echo "$BAR"
hostname
date -u '+%Y-%m-%dT%H:%M:%SZ'
date '+%Y-%m-%d %H:%M:%S %Z'
uptime
free -h
df -h / | tail -1
echo "cores: $(nproc)"
cat /proc/pressure/cpu /proc/pressure/memory /proc/pressure/io 2>/dev/null

echo
echo "$BAR"
echo "[2/4] SYSTEM"
echo "$BAR"
echo "-- failed units (authoritative) --"
systemctl --failed --no-pager --plain
echo "-- running units (enumerated, never guessed) --"
systemctl list-units --type=service --state=running --no-pager --plain \
  | grep -iE 'arif|forge|geox|wealth|well|frame|fed|hermes|mcp|flow|nats|headscale'
echo "-- containers --"
docker ps --format '{{.Names}}\t{{.Status}}' 2>/dev/null
echo "-- listening sockets --"
ss -tlnp 2>/dev/null

echo
echo "$BAR"
echo "[3/4] AGENT"
echo "$BAR"
ps -eo pid,etime,pcpu,rss,args --sort=-pcpu \
  | grep -iE 'hermes|opencode|qwen|kimi|codex|claude' | grep -v grep | head -15
echo "-- FED liveness (no-auth) --"
curl -s -m 5 http://127.0.0.1:4000/health/liveliness 2>/dev/null; echo

echo
echo "$BAR"
echo "[4/4] INTELLIGENCE"
echo "$BAR"
python3 -c "import json;d=json.load(open('/root/.hermes/cron/jobs.json'));j=d if isinstance(d,list) else d.get('jobs',[]);print(len(j),'jobs,',sum(1 for x in j if x.get('enabled')),'enabled')" 2>/dev/null
echo "-- latest eurekas --"
tail -5 /root/AAA/canon/eureka-entries.jsonl 2>/dev/null

echo
echo "Reminder: probe /ready as well as /health before reporting a box healthy."
