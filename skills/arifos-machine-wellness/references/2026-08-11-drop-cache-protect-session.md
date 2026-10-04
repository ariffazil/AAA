# 2026-08-11 — Drop-cache protect-active-session

## Scenario

User had 8 concurrent `opencode` instances running (~6GB RSS total), FED (:4000)
and FLAME (:18901) both healthy, one session mid-task. Two red signals:

- RAM free dropped to ~555MB (reclaimable cache ~6.7GB)
- Swap at 99.4% full (8146/8191 MB)

`earlyoom` (configured `--prefer .opencode`) was sitting at its trigger point
(mem <10% AND swap >5%). User instruction: "Let it finish what it's doing"
(suruh dia habiskan) — so the hot session must NOT be killed.

## Decisions made

1. **Do NOT kill the hot opencode** — it was at 58–73% CPU (live work), pointed
   at a real `pts/N` TTY. High CPU = work in flight.
2. **First lever = `drop_caches`** — reversible, zero data loss, kernel
   re-populates on demand.
3. **Left alone (essential):** LiteLLM :4011 (1.28GB), OpenClaw gateway (3GB),
   Hermes gateway (1.33GB), arifOS kernel.

## The fix (exact commands)

```bash
# Before
free -m | tail -2
# Mem: 32092 total, 26782 used, 664 free, 1353 buffers, 6642 cached
# Swap: 8191 total, 8146 used, 45 free

# Reclaim cache
sync; echo 3 > /proc/sys/vm/drop_caches
sleep 2

# After
free -m | tail -2
# Mem: 32092 total, 26819 used, 4318 free, 1353 buffers, 2950 cached
# Swap: 8191 total, 8146 used, 45 free
```

Result: RAM free 664MB → **4,318MB** (reclaimable cache 4.5GB → 2.5GB).
Earlyoom now has headroom; **0 kill events**.

## Active vs idle discrimination (opencode)

```
PID 3188984  CPU 60%  RSS 876MB  TTY pts/0   ← ACTIVE (protect)
PID 331600   CPU 56%  RSS 625MB  TTY ?       ← ACTIVE (protect)
PID 3211300  CPU 19%  RSS 719MB  TTY pts/7   ← working
PID 3572314  CPU 8%   RSS 622MB  TTY ?       ← idle / could kill if needed
PID 3472385  CPU 10%  RSS 739MB  TTY ?       ← idle / could kill if needed
```

Rule: high CPU + real pts TTY = never touch. Low CPU + `?` TTY = safe to kill
only if memory is still critical after drop_caches.

## Key learning

- **drop_caches is the under-used first lever.** Before any kill, before any
  swap reset, check reclaimable cache (`grep -E '^Cached|^Buffers' /proc/meminfo`).
  It routinely frees multi-GB without touching a single active process.
- **Swap being 99% full is NOT itself a kill trigger** if RAM has clear headroom
  after cache drop — swap only gets used when RAM fills. The danger is combo
  (swap full + RAM near-zero), which is what earlyoom watches.
- **"Let it finish" (F1 reversibility) maps to drop_caches, not kill.** The
  user's instinct to preserve in-flight work is the correct AMANAH-first call.