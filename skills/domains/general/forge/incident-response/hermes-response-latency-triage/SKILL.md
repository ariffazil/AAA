---
name: hermes-response-latency-triage
description: "Use when Hermes or its gateway replies slowly."
version: 1.0.0
license: internal
owner: Hermes (curator-managed)
risk_tier: medium
autonomy_tier: T2
tags: [hermes, latency, gateway, telegram, triage, session-store, cpu, context-bloat]
metadata:
  hermes:
    tags: [hermes, latency, gateway, telegram, triage]
    related_skills: [litellm-proxy-triage, vps-cpu-throttle-triage, telegram-gateway-troubleshooting]
triggers:
  - "Hermes is slow"
  - "replies very slow in Telegram"
  - "agent takes minutes to respond"
  - "gateway laggy"
  - "response time high"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Hermes Response-Latency Triage

End-to-end triage for "the agent is slow": substrate → process attribution → agent context → inference proxy → delivery. **Every layer produces the same symptom. Only measurement says which one is guilty — and the loudest number is usually not the cause.**

## When to Use

- The user says the agent is slow: "Hermes slow", "replies very slow in Telegram", turns taking tens of seconds to tens of minutes.
- Before touching any config, model, or provider — latency complaints almost always have one dominant cause, and it is rarely the model.

Not for: a single organ down or restarting (organ recovery), disambiguating a specific LiteLLM error string (`litellm-proxy-triage`), or Telegram echo/duplicate loops (`telegram-gateway-troubleshooting`).

## Step 0 — Pin the symptom to a number, and a time

```bash
grep "response ready" /root/.hermes/logs/gateway.log | tail -12
```

Each line: `time=NNNN.Ns` = message arrival → response ready. This is the only trustworthy "how slow" figure.

- **Thousands of seconds** = a backlog built while something else was starved. It drains on its own; only the `time=` of freshly-arrived messages answers "is it slow RIGHT NOW".
- **Tens of seconds on fresh arrivals** = live slowness — continue.

Do not quote a stale queue entry to the user as current performance, and do not chase one.

## Step 1 — Substrate

```bash
uptime                      # load vs nproc — load at/above core count = saturation
nproc
vmstat 1 3 | tail -1        # st column = CPU steal
mpstat 1 3                  # per-CPU %steal, finer than vmstat
free -h
```

High `%steal` = the hypervisor is taking your CPU; killing your own processes will not fix it. Low steal + high `us/sy` = your own workload. Low steal + low `us/sy` + slow replies = go to Step 3 — the box is innocent.

## Step 2 — Attribute the CPU load

```bash
ps aux --sort=-%cpu | head -20
ps -eo %cpu,comm | awk '{s[$2]+=$1} END {for(c in s) printf "%6.1f%% %s\n", s[c], c}' | sort -rn | head
ps -o pid,ppid,etime,time,%cpu,cmd -p <PID>
systemctl status <PID>       # which unit owns it
```

`%CPU` in `ps` is a LIFETIME average, not the current rate — a process showing 87% may have spiked once and be idle now. Confirm before accusing: `top -b -n 2` or `vmstat`.

- **PITFALL — a container can BE a systemd unit's `ExecStart`.** Before stopping any CPU-burning container, run `systemctl cat <unit> | grep ExecStart`. If ExecStart is a `docker run`, that "duplicate" worker *is* the service: `docker stop` deactivates the unit and its health checks fail. Restart with `systemctl restart <unit>` — never `docker stop`.
- **PITFALL — an orphan's parent chain decides whether it is safe.** `PPID=1` + long `etime` = orphan from a dead session, usually safe once nothing binds its port (`ss -tlnp | grep <port>`). Attached to `pts/N` under a live sshd with the user in `w` = a human's session; do not kill without asking.

## Step 3 — Agent layer (the usual live culprit)

```bash
grep "conversation turn" /root/.hermes/logs/agent.log | tail
hermes sessions stats
hermes doctor                 # add --live for bounded read-only real-call probes
hermes memory status
```

- `history=NNNN` on a turn = messages loaded into that request. Hundreds there, or one session holding thousands of messages, means every turn re-sends an enormous prompt → slow prefill → upstream timeouts → retries. This survives any CPU fix, and it is the usual reason a healthy box feels slow.
- A memory provider named in config but *unavailable* disables external memory and logs a warning **on every turn**. Systemd units do not inherit `~/.hermes/.env` — set the key in the unit's EnvironmentFile, or switch to built-in memory.

Store maintenance is safe; growing context is not. Recipe and honest expectations: `references/session-store-maintenance.md`.

```bash
cp -a /root/.hermes/state.db /root/.hermes/state.db.bak-<reason>   # ALWAYS first
hermes sessions optimize                     # FTS merge + VACUUM (no data change)
echo y | hermes sessions optimize-storage    # search index -> compact layout (asks y/N, so pipe the y)
```

Reclaiming a few MB is not a failure — it *proves the size is real content*. A large store is rarely the user's problem; per-turn context is.

**Destructive moves are the sovereign's call, not yours:** `sessions prune|delete|archive`, or rotating a bloated conversation. Present the session, its message count, and the trade-off; let them pull the trigger. The store IS their conversation history.

## Step 3b — Voice Governor / output-loop overhead

If the gateway's observed `time=` is healthy on technical probes (Step 4) but humans report
"kekwat / slow / berat" on real replies, the cause is often the human-side output gate, not
the model. The Voice Governor (`bridge-protocol` §STAGE 3) re-drafts replies that fail DITING
6/6 — a first-draft failure can spend 3-5 seconds per re-draft loop, and the loop runs more
than once on strict register. Layered with Voice Governor, `bridge-protocol` §STAGE 4 (the
Presentation Firewall) is a second mechanical gate.

**When the complaint comes from a third party, not the principal** ("Arif, abang sado Syed
complain Hermes kekwat sekarang"), do NOT take the lay pipeline apart — the human is reporting
the symptom, not asking for surgery. Identify the cause, propose bounded action, surface the
F13 binary the user owns. Don't restart the gateway; don't re-rate-limit; don't switch models.

**Diagnostic recipe** — proves the gate is the suspect, not the model:

```bash
# Compare fresh-arrival time= across the day, per chat
grep "response ready" /root/HERMES/logs/gateway.log | tail -50
# Look for chat_ids with rising time= on simple/casual exchanges
# A DM reply to a one-line technical question that takes 30s+ is the signal.

# Check memory pressure — cache hit rate falls as memory fills
hermes memory status
# 98%+ memory budget = context cache misses, every turn pays full prefill.
```

**Two bounded actions the agent owns (no F13 needed):**

- Trim memory if >95% full — release cache pressure, lifts the cache-miss cost.
- Add per-step timing log to the agent loop so the gate-cost is visible next time.

**One F13 binary the user owns:** branch Voice Governor into strict/casual lanes (casual DM
≤15s strict, technical/full-DITING), or keep strict everywhere. The technical-vs-casual split
is a register policy, not an agent decision — propose it as ONE binary choice, never a menu.

**Mechanism.** Voice Governor's "re-draft, never fallback" rule (`references/voice-governor.md`
§1) is correct on register — it prevents AI-speak leaks — but the loop has a real cost. A casual
BM reply that scores 4/5 DITING on first draft takes ~12s to re-draft to 6/6. Stack three drafts
plus the Presentation Firewall pass plus prefill, and a "30-second reply" is what the human sees.
The cost is real; the trade-off is real; the user decides the cut.

## Step 4 — Inference path

Find the port the gateway actually uses — read the unit's drop-ins, do not assume:

```bash
systemctl cat <gateway-unit> | grep -iE "OPENAI_BASE_URL|Environment"
curl -sf -m 8 http://127.0.0.1:<port>/health/liveliness
```

Then time one real completion through that exact path — not through a sibling port:

```bash
curl -s -m 90 http://127.0.0.1:<port>/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  -d '{"model":"<lane>","messages":[{"role":"user","content":"reply OK only"}],"max_tokens":5}' \
  -o /dev/null -w "http=%{http_code} total=%{time_total}s\n"
```

Compare that against the gateway's observed `time=` to see whether the proxy or the agent layer is eating the seconds.

A proxy carrying accumulated rate-limit cooldowns answers health checks fine while being slow — a unit restart clears it. Restart discipline and error disambiguation: `litellm-proxy-triage`.

## Step 5 — Delivery

```bash
grep -cE "Failed to send Telegram|Send failed" /root/.hermes/logs/gateway.log
grep -E "Failed to send Telegram|Send failed|Blocked unauthorized" /root/.hermes/logs/gateway.log | tail -40
```

Classify before fixing — the classes have different owners: bot-to-bot posts in a group, DMs to a user who never started the bot, replies to deleted messages, unsanctioned users posting in an allowed group. Each failure retries with backoff and occupies the sender.

Fix at the lane/allow-list layer, or by removing the bot from the group — **not** by killing the gateway. Silencing a chat or blocking a user is a sovereign decision: propose it, do not apply it.

## Step 6 — Fix, then prove it

Order the fixes by leverage: free the substrate → shrink per-turn context → restart the stale proxy → quiet the retry storm.

Re-measure after each and report before/after. The proof is a fresh `response ready: ... time=` on a newly-arrived message, not a service reporting `active`.

**Never restart the gateway from inside a turn it is delivering — you kill your own reply.** If a restart is genuinely needed, hand it to the user, or detach it so it runs after the current turn has been delivered.

## Reporting to this user

- **Lead with the finding and the human consequence**, not the probe transcript. "Punca utama: CPU kena throttle 90%" beats a wall of command output.
- **Before/after numbers are the proof.** State them as pairs: load 12.34 → 1.42, steal 90% → 0%, replies 1973s → 14s.
- **Disclose risky actions immediately and unprompted.** If you stopped something that turned out to be a live service, say so in the same breath as the fix, not buried at the end.
- **Collapse the noise.** No analysis-of-analysis, no raw log dumps, no `[OBS]`/`[DER]` label blocks. If it fits in one or two direct sentences, write that.
- **Close with at most 2–3 plain decisions**, each one a yes/no with what it buys. No menus, no essays.
- Casual BM with English technical terms, mixed, untranslated. Short, direct sentences.

## Pitfalls

- Quoting a stale backlog `time=` as current performance.
- Reading lifetime-average `%CPU` as an instantaneous spike.
- Stopping a container that is actually a unit's ExecStart.
- Promising a large reclaim from VACUUM without checking `freelist_count` — the size is usually real content.
- Blaming the model before measuring context size.
- Fixing delivery retries by restarting the gateway.
- Rotating the user's conversation history without asking.
- Restarting the gateway mid-turn and losing the reply.
- Declaring victory from `systemctl is-active` instead of a fresh response-time sample.
- Treating a third-party "Hermes kekwat" complaint as a request to dismantle the inference stack — the human reported a symptom; find the cause, propose bounded action, surface the F13 binary.
- Diagnosing Voice Governor overhead as "the model is slow" — the model is fine; the re-draft loop on a 4/5 DITING first draft is the cost. Confirm via Step 3b before opening the inference path.

## References

- `references/session-store-maintenance.md` — measuring and compacting the Hermes session store (`state.db`): the `hermes sessions` subcommands, sqlite queries for finding bloated sessions, and realistic reclaim expectations.
