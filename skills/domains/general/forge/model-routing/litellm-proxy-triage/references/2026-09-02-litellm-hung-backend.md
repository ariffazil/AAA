# 2026-09-02 — LiteLLM Backend Hung (port bound, no HTTP) → haproxy 503 Cascade

## Symptom chain (as seen from OTHER nodes — the confusing part)

A remote node (KVM4/azwaos) probing `100.64.0.2:4000` reported:
- `curl -m 6` → `http_code=000`, timeout, "TCP connect ok but 0 bytes back"
- Network-level reachability fine (tailscale `active; direct`)

**Misdiagnoses this produced before the truth was found:** "haproxy deadlock",
"service-level hang on both nodes", "KVM8 ASI gateway FAILED + state.db corrupt"
(the last one from a parallel agent session — gateway was actually active since
10:57, DB healthy, `quick_check: ok`).

## Actual root cause

litellm backend on KVM8 (`:4013`, backend of haproxy `:4000`) was **hung**:
- Process alive (36+ min uptime), port :4013 still LISTEN
- But HTTP probes to `127.0.0.1:4013/health/liveliness` never answered
- Load average climbing to 14–20 (litellm burning CPU in a stuck loop)

haproxy (health check `fall 5 inter 5s`) correctly marked the backend down →
`:4000` returned `503 Service Unavailable — No server is available` with an
empty-ish HTML body. From a remote curl with short timeout that reads as
`000 / 0 bytes / timeout` — looks like a network hang, is NOT.

## Diagnosis recipe (order matters)

```bash
# 1. Is :4000 a proxy? Who owns it?
ss -tlnp | grep :4000        # haproxy pid ≠ litellm pid → proxy in front

# 2. What does haproxy forward to?
grep -A8 "backend llm_nodes" /etc/haproxy/haproxy.cfg
#   → server fed_primary 127.0.0.1:4013 check inter 5s fall 5 rise 2

# 3. Probe the BACKEND directly — listener ≠ healthy
ss -tlnp | grep :4013        # LISTEN present…
curl -m 8 http://127.0.0.1:4013/health/liveliness   # …but hangs = hung process

# 4. Corroborate: load + process CPU
uptime; ps -o pid,etime,pcpu,cmd -p <litellm_pid>
#   etime high + pcpu 50-60% + no HTTP = stuck loop, not booting
```

**Distinguish from Python-3.13 import hang** (`references/2026-08-28-litellm-python313-hang.md`):
import hang never binds the port; this mode HAS the port bound and still won't answer.

## Fix (verified working)

```bash
kill -TERM <hung_pid>; sleep 4
kill -9 <hung_pid> 2>/dev/null          # it ignored TERM — SIGKILL needed
# fed-watchdog restarts it (systemd unit litellm does NOT exist on KVM8 —
# the watchdog owns recovery). Verify single replacement process:
ss -tlnp | grep :4013                   # new pid, owned by watchdog tree
```

Then **wait for haproxy rise**: `rise 2 × inter 5s` ≈ 10–15 s before :4000
serves 200 again. Do not declare failure at t+2s.

Verified recovery: KVM8 `:4000` → `"I'm alive!"`; KVM4 → `100.64.0.2:4000`
→ `http_code=200 time=0.38s`; load 20 → 7 falling.

## Pitfalls proven this incident

1. **LISTEN ≠ healthy.** A bound port proves nothing about HTTP liveness.
   Always curl the backend, never trust `ss` alone.
2. **Don't manually spawn litellm when fed-watchdog owns it.** Killing the
   hung process and spawning your own creates a duplicate race (both bind
   attempts collide; watchdog also restarts its own). Kill → let watchdog
   win → kill YOUR duplicate if you already spawned one.
3. **Cross-agent state reports are evidence, not truth.** A parallel session
   claimed "gateway FAILED + state.db corrupt"; direct probe showed gateway
   active 6h and DB healthy. VERIFY with `systemctl status` + `sqlite3
   quick_check` before acting on another agent's report — the federation
   runs multiple agent sessions that can hold stale views.
4. **Mask tokens when reading unit env.** `systemctl show -p Environment` /
   `/proc/PID/environ` emit FULL bot tokens. Pipe through
   `sed "s/=.\{6\}/=***MASKED/"` before echoing into chat/logs.
5. **Terminal tool rejects `nohup … &`** in foreground commands — use
   `terminal(background=true)` instead. (Hermes tool guard, by design.)

## Related open item (unresolved — awaiting F13 decision, do NOT act alone)

Dual Telegram polling: KVM4 `hermes-asi-gateway` and KVM8
`hermes-asi-gateway` both hold `TELEGRAM_BOT_TOKEN=8410138119…` → 409 polling
conflicts. Discovery method: on each node, `systemctl show
hermes-asi-gateway.service -p Environment` + `/proc/$(systemctl show -p
MainPID --value hermes-asi-gateway.service)/environ | grep TOKEN`.
Status 2026-09-02: documented, HOLD per Arif. (Separately,
`hermes-real-bridge.service` on KVM8 — same token — was stopped AND
disabled same day; that one is done.)
