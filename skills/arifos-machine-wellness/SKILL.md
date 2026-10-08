---
name: arifos-machine-wellness
description: "Stabilize the arifOS host when CPU/load/swap/oil is red — triage zombies (orphaned arifosmcp.runtime workers, runaway ollama runners), free resources, identify the LIVE kernel before killing anything, report steel+silica state tersely, and stop at any irreversible gate. Trigger: 'stabilize the machine', 'stabilize the server', 'steel and silica', load avg > cores × 2, swap >80% full, machine wellness check, 'is the host healthy', orphan python workers, runaway ollama process. Distinct from federation-runtime-forensics (reactive — sibling reported a flood) and federation-infra-verification (proactive — declared-vs-live audit). This is the wellness/triage class."
---

# arifOS Machine Wellness

The federation runs 24/7 on a single host. Workers accumulate, ollama runners go runaway, swap fills, load climbs. This is the **steady-state triage class** — not forensic (no incident to root-cause) and not verification (no claims to audit). It's "is the machine healthy right now, and if not, what can be killed safely."

## 1. The 5-second wellness probe (steel + silica)

> **PREFER THE CANONICAL PROBE — do not hand-roll this.**
> ```bash
> bash /root/scripts/federation-wellness-probe.sh
> ```
> It exists because two false signals occurred in one session (2026-10-07), both of
> which hand-rolled probes keep reproducing:
> 1. **Transient false-DOWN.** A single-shot `curl -sf -m 3` reported the arifOS
>    kernel ❌ while it was a one-off timeout — HTTP 200 in **2ms** on retry. The
>    kernel was never down. Always retry a failed port before believing it.
> 2. **False constitutional alarm.** `/health` returns `status: "degraded"`
>    because **11 of 13 floors are UNMEASURED** (`unmeasured_default:empty_kernel_signal`),
>    each defaulting to score 0.5 → read as "fail". Only **2 are actually measured**
>    (F1, F3). On the last check: **10/13 "pass", genuinely failing: none.**
>    Reporting "3 floors failing" is a false constitutional claim.
>
> The probe prints STEEL / SILICA / measured-vs-defaulted constitution, with layers
> never aggregated. If you hand-roll anyway, apply both rules above.

Run this BEFORE any kill. Live, terse, no prose.

```bash
date '+%Y-%m-%d %H:%M:%S %Z'             # anchor time
uptime                                     # load avg + up time
free -h | head -2                          # mem
swapon --show                              # swap (critical: 100% full = thrashing)
df -h / /var /opt 2>/dev/null | awk 'NR==1 || /\//'   # disk
for p in 8088 7071 7072 7073 3001 8081 18082 18083; do
  curl -sf -m 3 http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ $p" || echo "❌ $p"
done
```

**If a port shows ❌ — RETRY BEFORE BELIEVING IT.** One-shot probes produce false
outages. Confirmed 2026-10-07: the kernel returned ❌ once and HTTP 200 in 2ms on
every subsequent call. Retry 3× at 1s intervals before reporting anything down.

```bash
for i in 1 2 3; do curl -sf -m 5 http://127.0.0.1:$p/health >/dev/null && { echo "✅ on retry $i"; break; } || sleep 1; done
```

**Interpret the result with these thresholds:**

| Signal | Healthy | Warning | Critical |
|---|---|---|---|
| Load avg (1m) | < cores | cores×1.5 | > cores×2 |
| Swap | <50% | 50–80% | >80% (especially >95%) |
| Mem `available` | >20% | 10–20% | <10% (oom imminent) |
| Organ health | all ✅ (after retry) | 1 ❌ after 3 attempts | 2+ ❌ |

**Quotient for "is this normal"**: `earlyoom` is the federation's pressure-relief valve (configured `--avoid (^|/)(caddy|sshd|systemd|...|arifos|docker)` and `--prefer (^|/)([.opencode|chrome|pytest|agy|ollama|node|python3)`). If `earlyoom` is alive and avoided-killing core services, swap is **reclaiming as pages free** — give it 60–120s before any swap reset. Don't fight the valve.

**Swap % alone overstates urgency (2026-08-15).** Gate on PSI before calling swap "critical": `head -2 /proc/pressure/memory`. Observed: swap 100% full for ~2 weeks on a 23-day-uptime host while PSI `full avg10=0.00`, mem available >10%, load 2/8 cores, zero OOM kills in 48h — that is **stale parking** (cold pages parked and never forced to reclaim), not thrashing. Read swap% together with PSI, never alone.

## 2. The orphan-arifosmcp-runtime trap (the recurring class)

This is the #1 pattern on the arifOS box. After every `systemctl restart arifOS`, 1–4 orphaned `python -m arifosmcp.runtime` workers survive. They were children of the OLD kernel, PPID=1, accumulating CPU across hours/days.

### How to identify the LIVE kernel

**Never trust PID age alone.** Use `ss -tlnp` to find who actually LISTENS on :8088:

```bash
ss -tlnp | grep :8088
# Example output:
# 127.0.0.1:8088 users:(("python",pid=474560,fd=13))
```

That PID (e.g. 474560) is the **only one you may not kill**. Everything else with the same cmdline is an orphan.

### The orphan signature

```
PID=1531508 PPID=1 ET=17:01:06 CPU=92.9 RSS_KB=52888 CMD=/opt/arifos/venv/bin/python -m arifosmcp.runtime
```

Five tells:
1. `PPID=1` (orphaned from old systemd unit)
2. `ET` (etime) older than the kernel's `ActiveEnterTimestamp` from `systemctl show arifos.service -p ActiveEnterTimestamp`
3. Same cmdline as the live kernel
4. Does NOT own :8088 in `ss -tlnp`
5. CPU% climbing despite no client load

### The kill sequence (safe, idempotent)

```bash
# 1. Find live kernel
LIVE=$(ss -tlnp | grep ':8088' | grep -oP 'pid=\K[0-9]+' | head -1)
echo "Live kernel PID: $LIVE"

# 2. Find orphans (same cmdline, NOT live)
ps -eo pid,cmd --no-headers | grep '[a]rifosmcp.runtime' | grep -v "from arifosmcp" | awk '{print $1}' | while read pid; do
  [ "$pid" != "$LIVE" ] && echo "ORPHAN: $pid"
done

# 3. Kill them
for pid in $(ps -eo pid,cmd --no-headers | grep '[a]rifosmcp.runtime' | grep -v "from arifosmcp" | awk '{print $1}'); do
  [ "$pid" != "$LIVE" ] && kill -9 "$pid" 2>/dev/null && echo "killed $pid"
done
```

**Verification after kill:**
- Load avg should drop within 10–30s
- Kernel still responsive: `curl -sf -m 3 :8088/health`
- No new orphans in `ps` (if they're re-spawning, there's a service-timer bug — escalate)

### The pattern across the federation

Other workers follow the same orphan signature:
- `arifosmcp.runtime.observability.worker` (1 process, expected)
- `arifosmcp.runtime.l5_search_api` (1 process, expected)
- `arifosmcp.abi.nats_heartbeat_daemon` (1 process, expected)
- `python3 -c from arifosmcp.runtime.__main__ import main; main()` — this is the LIVE one (PPID=1 BUT owns :8088 via systemd `ExecStart`)

**The tell for "live systemd-managed" vs "orphan":**
- LIVE: PPID=1, ET matches `ActiveEnterTimestamp`, owns a port via `ss -tlnp`, cmdline starts with `/opt/arifos/venv/bin/python -c`
- ORPHAN: PPID=1, ET > kernel ET, does NOT own a port, cmdline is `python -m arifosmcp.runtime`

## 3. The runaway ollama runner trap

Symptom: `ollama ps` shows a model with `UNTIL: Stopping...` (stuck shutdown) at 100%+ CPU sustained for minutes/hours.

```bash
ollama ps                                              # identify the stuck model
ps aux | awk '/[o]llama.*runner/ {print $2, $11}'     # find the runner PID
kill -9 <runner_pid>                                   # hard kill
ollama stop <model> 2>/dev/null                        # tell the server to drop it
```

**Why it happens**: the ollama server (PID in systemd) holds a handle to the runner, the runner is unloading the model from GPU/RAM, but something in the unload sequence hangs (cuda driver, shm). Hard kill is safe — the server respawns cleanly on next request.

**Ollama's role in this federation**: **embedding backend only** (`bge-m3` for Graphiti/Qdrant). Don't add text-gen use-cases. If Graphiti is healthy, ollama can run away freely. If Graphiti is broken, ollama is the prime suspect (see `federation-infra-verification` §3a for the wiring).

## 4. The orphan-`find`/orphan-`grep` trap

Symptom: a `find` or `grep` at 30–80% CPU with no parent shell. Cause: shell crashed (OOM kill or signal), child orphaned, kept indexing.

```bash
ps aux | awk '/[f]ind / && !/grep/ {print $2}'
kill -9 <pid>   # safe — find has no persistent side effects
```

## 5. Drop page cache FIRST — the reversible memory relief (before any swap reset or kill)

When mem `available` is tight but swap isn't yet at 100% and an active session must survive, the FIRST lever is `drop_caches` — not killing anything. It frees clean read-cache pages, costs zero data (kernel re-populates on demand), and often returns 3–5GB of headroom instantly.

```bash
echo "reclaimable cache: $(grep -E '^Cached|^Buffers' /proc/meminfo | awk '{s+=$2}END{print s/1024" MB"}')"
sync; echo 3 > /proc/sys/vm/drop_caches      # 1=page cache 2=dentries+inodes 3=all
sleep 2
free -h | head -2                              # confirm 'free' jumped
```

**When to reach for this:** user says "let it finish what it's doing" / "suruh dia habiskan" about a live session, and mem available <10% but the process is genuinely working (high CPU). Drop cache buys headroom so earlyoom never has to choose a victim.

**Order of levers (least → most disruptive):**
1. `drop_caches` (reversible, zero risk) ← try this first
2. Kill confirmed-idle duplicate instances of the SAME tool (low CPU, `?` TTY)
3. Swap reset (`swapoff && swapon`) — T2, announce
4. Kill orphan/zombie workers (the orphans section below)

## 5a. Protect an ACTIVE session — active vs idle tells

When multiple instances of the same tool run (e.g. several `opencode` processes) and memory is red, you must NOT kill the one doing the real work. Discriminate by **CPU% + TTY**:

```bash
ps aux | awk '/[o]pencode/ && !/awk/{printf "PID %s CPU %s%% RSS %.0fMB TTY %s\n",$2,$3,$6/1024,$7}' | sort -k3 -rn
```

| Signature | Meaning | Action |
|---|---|---|
| **High CPU (>30%) + a real pts/N TTY** | Actively working (has a live interactive session) | **NEVER kill** — protect via drop_caches |
| Low CPU (<10%) + `?` TTY | Idle / daemonized / leftover | Safe to kill if memory is critical |
| `serve`/`--port` mode | A service endpoint other things depend on | Leave alone unless confirmed unused |

**The rule:** high CPU = work in flight. If the user wants it to finish, relieve memory around it (drop_caches, kill idle siblings), never touch the hot one. Confirm zero earlyoom kills after: `journalctl -u earlyoom --since '8 min ago' | grep -icE 'killed|SIGTERM'` → should be `0`.

## 5b. Swap reset recipe (T2, announce before doing)

Only when swap is **>95% full**, with mode determined by PSI (`/proc/pressure/memory`):

- **Stale parking** (PSI `full avg10` ≈ 0, mem available >10%, load < cores): zero-risk reset, do it leisurely. This is the common case on long-uptime hosts — swap% has been red for days but nothing is actually thrashing.
- **Active thrashing** (PSI `full avg10` > 5, load climbing): drop_caches + kill orphans FIRST, wait 60s for earlyoom to drain, then reset.

```bash
head -2 /proc/pressure/memory        # classify BEFORE announcing
echo "Going to swap reset. Why: swap full (<stale|thrashing>), <reason>. Reversible: yes (re-enable same file). Proceeding in 10s."
sleep 10
swapoff /swapfile2 && swapon /swapfile2
free -h | head -2
```

**Why not just `swapoff -a`**: it can take 30–120s on a 4G swap with active pages, during which the kernel keeps allocating. `swapoff /swapfile && swapon /swapfile` is one atomic-ish operation that re-uses the same backing file (no new disk allocation).

**Multi-swapfile layout (2026-08-15):** `swapon --show` on this host lists `/swapfile` (prio -2) and `/swapfile2` (prio -3). Higher priority fills first, so the **lowest-priority file holds the coldest, most stale pages**. Reset THAT one first: (a) coldest pages = cheapest to force back into page cache, (b) the other swapfile keeps absorbing during the swapoff window, so nothing stalls. Verified: reset of `/swapfile2` alone took <30s, swap went 8.0G full → 4.0G used, held after settle (SwapFree 4.2G). Note the reset temporarily shifts swapped pages back into page cache (mem used jumped 14→19G during the operation) — expected, drains on its own.

## 6. The "DON'T kill" list (F1 reversibility, sanity check)

Before any `kill -9`, confirm the target is NOT on this list:

| Process | Why |
|---|---|
| `python -c from arifosmcp.runtime.__main__ import main; main()` (the live kernel) | Owns :8088, F13 sovereign surface |
| `arifOS-NATS-heartbeat` | F11 auditability substrate |
| `earlyoom` | The pressure valve — killing it = free-for-all oom kills |
| `caddy`, `sshd`, `systemd`, `systemd-journal`, `systemd-logind`, `cron` | earlyoom `--avoid` list — verify they're matched |
| `postgres`, `redis-server`, `qdrant`, `nats-server`, `arifos` | earlyoom `--avoid` list |
| `docker` | Container host for substrate services |
| Any process whose PID matches `MainPID` from `systemctl show <unit> -p MainPID` for a running service | That's the live systemd-managed instance |

**Fastest sanity check**: `systemctl show arifos.service -p MainPID` returns the kernel PID. Any kill list MUST NOT contain that PID.

## 7. Reply shape (Arif's preference)

Lead with the table, follow with what was killed, end with carry-forward. No preamble.

```
## 🩺 State of the Machine — <time>
**Steel:** load X/Y/Z cores=N mem=X/G avail=X% swap=X% 
**Silica:** 8/12 organs ✅ (or list ❌)

**Killed (T1):**
- 4× orphaned arifosmcp.runtime workers (PIDs ...)
- 1× ollama bge-m3 runner (PID ...)

**Left for sovereign:**
- DRIFT_7 / DRIFT_8 carry-forward items
- Swap pressure (draining or stuck)

ΔS of session: -X (negative = improvement)
```

**No "Should I...?"** — Arif's working style: announce + execute within authority. The wellness class lives in T1 (kill orphans, reset stuck processes). T2 only for swap reset and service restart. T3 888_HOLD for anything that touches VAULT999, secrets, or external comms.

## 8. Infra pressure ≠ constitutional health — never aggregate layers (2026-08-14)

When reporting system status to Arif, **four layers of health are INDEPENDENT** and must be reported separately. An agent that says "constitutional collapse" when swap is full and load is high is lying — the constitution can be 13/13 pass while the machine is pressured.

| Layer | Source | Red when |
|---|---|---|
| **Constitutional** | `/health` → `floors_active` (int), `runtime_floors_status` | Floor failures > 0 |
| **Runtime** | `/health` → `runtime_drift` (bool), `runtime_matches_build` (bool) | `runtime_drift=True` or `matches_build=False` |
| **Registry** | `/health` → `registry_truth` (enum), `deployment_drift_status` (enum) | `DRIFT_DETECTED` — bookkeeping mismatch, not functional failure |
| **Infra** | `uptime`, `free -h`, swap probes (NOT in `/health`) | Load > cores×2, swap > 80%, mem available < 10% |

Arif's exact teaching (2026-08-14): *"Infra pressure keliru dengan constitutional health."* Agents that merge these produce false alarms. The `/health` `status: "degraded"` umbrella aggregates registry + deployment drift into one word — **do not read `status` as the verdict.** Read the individual boolean fields.

Also: `owner_summary.reasons[]` can contain the string `"runtime_drift"` even when the `runtime_drift` **boolean field** is `False`. This is a naming collision. Trust the boolean, not the reason label.

### 8a. UNMEASURED ≠ FAILING — the constitutional false-alarm (2026-10-07)

`status: "degraded"` is an **aggregate**, and on this host it is triggered almost
entirely by floors that were never measured. `floors_provenance` distinguishes them:

| Field | Meaning |
|---|---|
| `floors_measured` | floors with a real probe behind them |
| `floors_defaulted` | `unmeasured_default:*` — placeholder score 0.5, reads as "fail" |
| `floors_failing` | reported failures — **subtract `floors_defaulted` before calling any of these a violation** |

Measured 2026-10-07 20:14 MYT:

```
constitutional : 10/13 pass · 2 MEASURED · 11 UNMEASURED
  unmeasured (NOT violations): F2,F4,F5,F6,F7,F8,F9,L10,L11,L12,L13
  ✓ F1 ← arifflow_fq_probe:fq=1.02
  ✓ F3 ← witness_producers:human+ai+earth
  genuinely failing: none
```

So "3 floors failing (F2/F5/F6)" — the reading reported earlier tonight — was a
**false constitutional claim**. Those three are unmeasured defaults, not violated
floors. `rest_routes.py:3438-3459` already documents this; the provenance was
published precisely so consumers would stop conflating the two.

**Rule: never report a constitutional violation without checking `floors_provenance`
first.** Report measured and unmeasured separately.

Report shape for Arif: one emoji per layer, one line each. Never aggregate. See `federation-infra-verification` §14 for the full decompose-before-report recipe.

## Pitfalls

- **PPID=1 doesn't mean orphan.** The live systemd-managed kernel also has PPID=1 because systemd is its parent. Use `ss -tlnp | grep :PORT` as ground truth for "who owns the listener," then back-derive the PID.
- **Process ETIME can lie** during a tz boundary or NTP step. Cross-check with `systemctl show <unit> -p ActiveEnterTimestamp` for the canonical "service started at".
- **`kill -9` on a live kernel will surface** as :8088 connection refused on the next probe. If you see that after a kill, you killed the live one — `systemctl restart arifOS` and re-derive the orphan list.
- **Ollama runner can refuse to die** with `kill -9` if the ollama server reaps it first. Watch for "no such process" on second `kill` — that's success, not failure.
- **`pkill -f arifosmcp`** is the WORST idea. It kills the live kernel too. Always enumerate, always check `ss -tlnp`.
- **Don't trust `top`/`htop`** for CPU attribution under high load — both lag 1–3s and will misattribute swap-thrashing CPU to whichever task happens to wake up. Use `ps -eo pid,etime,%cpu,rss,cmd --no-headers` with grep filters instead.
- **`earlyoom` math**: it triggers when mem < 10% AND swap > 5% (configurable via `-m`). If swap is 100% AND mem is at 8%, earlyoom is ABOUT to kill something — but `drop_caches` can often prevent this entirely. Always try cache drop first (reversible, zero risk) before earlyoom needs to make a victim choice. Check `dmesg | grep -i oom` for the last kill before you kill anything else.
- **`ollama stop <model>` may hang** if the runner is already stuck — the stop call joins the runner's unload thread. If `ollama stop` blocks >10s, Ctrl-C it and `kill -9` the runner PID directly.
- **The A-FORGE `types.ts.append` pattern** is cosmetic, not harmful — drafts that were applied but the apply-script left the draft file behind. `rm` is safe, but check the git diff first (`git -C /root/A-FORGE log -S <field>` to confirm the field already exists in HEAD).

## Support files

- `references/wellness-probe-recipe.md` — copy-paste terminal session for the 5-second wellness probe, the orphan-arifosmcp kill sequence, and the ollama-runner kill. Run from `/root` with `bash` and the kill lists resolve to live PIDs.
- `references/2026-08-08-machine-wellness-session.md` — the session transcript that produced this skill: live machine had load ~19, swap 100%, 4 orphan workers, stuck ollama runner, killed all safely, load dropped to ~13 and continued draining.
- `references/2026-08-11-drop-cache-protect-session.md` — session where 8 concurrent opencode instances (~6GB RSS) pushed swap to 99.4% with an active session mid-task; the fix was `drop_caches` (664MB→4.3GB ram free, 0 earlyoom kills) rather than killing the hot process. Includes the exact probe + active/idle discrimination.
- `references/2026-08-15-node-institution-map-session.md` — full live institution map (77 services + 7 containers, top-RAM consumers), the stale-swap-vs-thrashing discrimination case, zram observation (proposed, not yet implemented), dead-weight /root/comfy finding, and the ROI-ordered next-level resource list. Load this before answering any "map the machine / what does X service do / resource allocation" question.
