# Intelligence Envelope — what cognition a box can actually buy

Use when the question is not "is it up?" but "what can this machine think with?" — capacity
planning, cross-machine comparison, "can we run another agent here?", or diagnosing why a box with
spare cycles still feels slow. Read-only. Pair with the state probe ladder in SKILL.md; this file
is the layer above it.

## Battery

```bash
# A. IDENTITY FIRST (never from a stamp, config, or memory)
hostname; tailscale ip -4; uname -a; nproc
lscpu | grep -E 'Model name|^CPU\(s\)|Thread|Core|Socket|L3'

# B. RESOURCES + PRESSURE
free -h; swapon --show
cat /proc/pressure/cpu /proc/pressure/memory /proc/pressure/io
vmstat 1 5 | tail -3            # si/so columns: sustained swap-in/out, not just free space
ps -eo rss,pid,comm --sort=-rss | head -15
for f in /proc/*/status; do awk '/^Name:/{n=$2}/^VmSwap:/{if($2>50000) printf "%.0fMB %s\n", $2/1024, n}' "$f" 2>/dev/null; done | sort -rn | head -12
journalctl -u earlyoom --no-pager -n 12   # trend line for avail/swap-free
journalctl --since '24 hours ago' --no-pager | grep -ci 'oom-kill|Killed process'

# C. INFERENCE LANES
curl -s -m 5 http://127.0.0.1:11434/api/ps    # what is resident
curl -s -m 5 http://127.0.0.1:11434/api/tags  # local parameter ceiling
curl -s -m 5 http://127.0.0.1:<fed-port>/health/liveliness
curl -s -m 5 http://127.0.0.1:<fed-port>/v1/models -H "Authorization: Bearer $KEY"

# D. TOOL + CONTEXT TAX
python3 -c "import json;d=json.load(open('/root/.hermes/cache/mcp_schema_cache.json'));s=d.get('mcpServers',d);print(len(s),'servers');[print(' ',len((v or {}).get('tools') or []),k) for k,v in sorted(s.items(), key=lambda x:-len((x[1] or {}).get('tools') or []))]"
du -sh /root/.hermes; ls -la /root/.hermes/state.db
sqlite3 /root/.hermes/state.db "select count(*), sum(length(content))/1048576 from messages;"

# E. REACHABILITY (bound interface says who can reach it)
ss -ltnp    # 127.0.0.1 = local only; tailnet IP = remote-reachable; 0.0.0.0 = public

# F. PEER LATENCY (only meaningful if you also measure model latency)
for t in <peer1> <peer2>; do echo -n "$t "; ping -c 3 -W 2 $t | tail -1; done
```

## Reading it

- **Separate OBSERVED / INFERRED / UNKNOWN explicitly.** Anything you did not read this turn is
  UNKNOWN, even if you are sure. Never let a recalled spec enter the OBSERVED column.
- **Three limits, in this order:** physical (working set, io, thermal), cognitive (context tax,
  tool entropy, decomposition), coordination (which node holds which capability). Name the one that
  actually binds; do not present all three as equal findings.
- **Budget vs policy.** Idle CPU + idle model endpoints + saturated swap is the classic shape: the
  physical budget is *not* exhausted, the allocation policy is. Say it that way — the distinction
  decides whether the fix is a purchase (forbidden here) or a routing change (allowed).
- **Resident weight is a first-class number.** Sum the RSS of idle agent CLIs and daemons. Multi-GB
  of resident-but-idle agent processes is normal on these boxes and is what forces swap pressure,
  which then slows the parts that look fast.
- **Latency hierarchy decides what to optimize.** Inter-node tailnet RTT (~1ms) is a rounding error
  next to model latency (~1s). Do not design around a topology cost that is three orders of
  magnitude smaller than the inference call.

## Pitfalls

- **A stamp is not a witness.** Persona headers (SOUL_STAMP), config values, and memory slots naming
  a host are metadata. `hostname` + `tailscale ip -4` outrank them, and a disagreement is a finding
  to report — not an identity to adopt mid-task.
- **A listener on 127.0.0.1 is not reachable from a peer.** Read `ss -ltnp` addresses before any
  cross-node claim; and dial the *peer's* address, never your own loopback.
- **Do not quote a manifest count from a doubled scan.** Resolve realpaths and dedupe first; if the
  runtime's rendered per-turn size cannot be isolated, report UNKNOWN.
- **Cold vs cached:** one latency sample is not a measurement. Two identical calls, or nothing.
- **A tool or skill count is not a capability claim.** Presence in a catalogue says the surface is
  declared, not that the lane answers; probe the endpoint before reporting it as available.
