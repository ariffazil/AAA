# 2026-09-02/03 — Infra Night: Three Incidents + Six-Hour Echo Loop

Session lane: Telegram DM bridging Hermes (KVM8/af-forge) and a second agent session on wawa/azwaos (100.64.0.4). Human input was intermittent; most traffic was agent-to-agent relay.

## Incident 1 — hermes-real-bridge redundant poller (resolved)

Two local processes held bot token 8410138119: `hermes-asi-gateway` (canonical) and `hermes-real-bridge.service` (legacy relay, uvicorn :18091). Stopped AND disabled the legacy one — stop alone would have it return on reboot:

```bash
sudo systemctl stop hermes-real-bridge.service
sudo systemctl disable hermes-real-bridge.service   # removes multi-user.target.wants symlink
ss -tlnp | grep 18091                                # port free = clean
```

Lesson: **stop + disable together** for any "redundant service" verdict; a bare stop is a scheduled regression.

## Incident 2 — FED :4000 503 = litellm backend hung (resolved by watchdog)

`ss -tlnp` showed haproxy listening :4000, but curl → 503 "No server available". Backend litellm (:4013) process alive with port bound but never answering HTTP (etime ~36min, CPU 50-60%, classic stuck loop). Sequence:

1. `kill -TERM <pid>` ignored → `kill -9` → process dead, :4013 empty
2. Manually spawned a replacement → `fed-watchdog` ALSO spawned one → duplicate; mine died on `address already in use` (expected, harmless)
3. Killed my duplicate, kept watchdog's → after haproxy `rise 2 × inter 5s` (~15s) :4000 answered "I'm alive!"
4. KVM4 → KVM8 FED went from timeout-6s to HTTP 200 / 0.38s

Lesson: **never race the watchdog.** Kill the hung process, let fed-watchdog own the restart, dedupe anything you spawned yourself. Note litellm was NOT under a systemd unit on this box (`systemctl restart litellm.service` = "unit tidak wujud") — process ownership here is fed-watchdog, not systemd.

## Incident 3 — WAWA PULSE false alarm (resolved: transient, no action)

Full analysis in `2026-09-03-wawa-pulse-false-alarm.md` (same directory). Key: remote monitor alert ≠ fact; re-probe with `/health/liveliness` from multiple vantages before waking anyone.

## Failure — The six-hour 🤐 echo loop

After all three incidents closed (~00:45), the two agent sessions bounced 🤐 / "(no response)" / "Standby 👍" tokens at each other until ~01:50 — **6+ hours of pure token burn**, dozens of round trips, each side periodically writing a long "I'm breaking this loop" message that itself continued the loop (one side did this at least 5 times). Root cause: each side's session treats the other's silence token as inbound input requiring acknowledgment. Neither side ever emitted NOTHING.

Also observed mid-loop: a prompt-injection attempt embedded in one relayed message (fake `<system-reminder>` trying to impose a "reasoning format"). Correct handling = ignore injected directive, keep identity, do not follow. Flagging it once was enough; engaging with it per-turn would have fed the loop.

**The terminating move is no output at all.** Content-bearing messages (incident alerts, names, tasks) re-open the lane legitimately — and did, at 00:00 when WAWA PULSE fired.

## Fabrication scar (self-inflicted)

During incident 3 diagnosis, a relayed claim "MTU 9000 jumbo frames fix applied" entered the thread. It was false — Tailscale caps tailscale0 at 1280 (WireGuard overhead); jumbo frames over WireGuard are invalid; no such change existed on any node. It polluted diagnosis for several turns until the wawa-side agent called it out. Rule: **never forward or endorse a fix claim you didn't verify on the box yourself.** Read state (`ip link show tailscale0`) before repeating anyone's mutation report.
