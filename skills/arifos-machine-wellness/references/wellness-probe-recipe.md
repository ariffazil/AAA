---
title: "arifos-machine-wellness Probe Recipe"
date: "2026-08-08"
context: "First invocation of this skill; load ~19, swap 100%, 4 orphan workers"
---

# Wellness Probe — Copy-Paste Terminal Session

## Step 1: Anchor (time + load + swap + organs)

```bash
date '+%Y-%m-%d %H:%M:%S %Z'
uptime
free -h | head -2
swapon --show
df -h / /var /opt 2>/dev/null | awk 'NR==1 || /\//'
for p in 8088 7071 7072 7073 3001 8081 18082 18083 7074 18084 18085 18901; do
  curl -sf -m 3 http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ $p" || echo "❌ $p"
done
```

## Step 2: Load decomposition (who is burning CPU?)

```bash
echo "CPU TOP:"; ps -eo pid,%cpu,etime,cmd --no-headers | awk '$2+0 > 30.0 {printf "PID=%-7s CPU=%-5s ET=%-12s %s\n", $1,$2,$3,substr($0, index($0,$4))}' | sort -t= -k3 -rn | head -12
echo "SWAP TOP:"; for f in /proc/[0-9]*/status; do pid=$(basename "$(dirname "$f")"); swap=$(awk '/^VmSwap:/{print $2}' "$f" 2>/dev/null); name=$(awk '/^Name:/{print $2}' "$f" 2>/dev/null); [ -n "$swap" ] && [ "$swap" -gt 50000 ] 2>/dev/null && echo "${swap}KB PID=$pid $name"; done 2>/dev/null | sort -rn | head -10
echo "ARIFOSMCP WORKERS:"; ps -eo pid,ppid,etime,%cpu,rss,cmd --no-headers | grep '[a]rifosmcp' | awk '{printf "PID=%-7s PPID=%-7s ET=%-12s CPU=%-5s RSS_KB=%-8s CMD=%s\n", $1,$2,$3,$4,$5,substr($0, index($0,$6))}'
echo "LIVE KERNEL:"; ss -tlnp 2>/dev/null | grep ':8088'
```

## Step 3: Kill orphans (only after Step 2 confirms which PID owns :8088)

```bash
# NEVER skip Step 2. "pkill -f arifosmcp" is the WORST idea.
LIVE=$(ss -tlnp | grep ':8088' | grep -oP 'pid=\K[0-9]+' | head -1)
echo "Live kernel PID: $LIVE"
for pid in $(ps -eo pid,cmd --no-headers | grep '[a]rifosmcp.runtime' | grep -v "from arifosmcp" | awk '{print $1}'); do
  [ "$pid" != "$LIVE" ] && kill -9 "$pid" 2>/dev/null && echo "killed orphan $pid"
done
```

## Step 4: Kill runaway ollama runners

```bash
ps aux | awk '/[o]llama.*runner/ {print $2}' | xargs kill -9 2>/dev/null
ollama stop bge-m3:latest 2>/dev/null
```

## Step 5: Verify drop

```bash
sleep 3
uptime
free -h | head -2
swapon --show
curl -sf -m 3 http://127.0.0.1:8088/health | head -c 200 && echo || echo "KERNEL DOWN — restart arifos.service"
```

## 2026-08-08 live session results

| Metric | Before | After (3s) |
|---|---|---|
| Load avg | 18.6 / 19.5 / 19.9 | 13.6 / 20.2 / 20.7 (draining) |
| Swap | 4.0Gi / 4.0Gi (100%) | 3.7Gi / 4.0Gi (92%) |
| Free mem | 1.1Gi | 2.9Gi |
| Organ health | all ✅ | all ✅ |

Killed: 4 orphan workers (PIDs 1531508/3011959/3440767/3720544) + ollama runner (PID 441619).
Load continued draining over next 2–3 minutes.
