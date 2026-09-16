# WAWA PULSE False Alarm — Tailscale Route Flap + Heavy Health Endpoint (2026-09-03)

## Incident

00:00:28 MYT — wawa-pulse (cron on azwaos/100.64.0.4, script `/usr/local/bin/wawa-pulse.sh`, */30) alerted:

```
⚠️ WAWA PULSE: FED UNREACHABLE dari wawa node
100.64.0.2:4000 tak jawab.
```

## Ground truth (verified during the "outage")

| Vantage | Endpoint | Result |
|---|---|---|
| KVM8 localhost | :4000/health/liveliness | 200, 2-90ms |
| KVM8 → wawa (reverse) | :4000 | 200 |
| wawa → KVM8 by IP (100.64.0.2) | /health/liveliness | 200, 4-25ms (3/3) |
| wawa → KVM8 by IP | /health (full, ~13KB) | timeout 10s, 0 bytes |
| wawa → KVM8 by hostname `af-forge` | :4000 | 000 (7ms — resolve failure) |

Pulse log on wawa: `16:00:27 ISSUE / 16:00:28 ALERT-SENT / 16:30:09 HEALTHY` — one-cycle transient, self-resolved before any intervention.

## Root causes (stacked, all benign)

1. **Route flip direct ↔ DERP.** `tailscale netcheck` from KVM8 showed `UDP: false`, `IPv4: no addr found`; peer path flapped between IPv6 direct (5ms) and DERP relay (83ms). Tailscale re-holes NAT periodically; during the flip, fresh short connections can time out while existing ESTABLISHED ones keep flowing (tcpdump showed ~13KB trickling at ~4KB/s on an old session while five fresh curls got 0 bytes).
2. **Heavy endpoint on a degraded path.** `/health` returns the full ~13KB model list; `/health/liveliness` returns 12 bytes. Same degraded path answers the small payload in ms and times out on the big one. WAWA PULSE already used liveliness (line 29) — correct.
3. **Hostname resolution drift.** `getent hosts af-forge` empty on wawa (MagicDNS not propagating the short name); SSH config still worked because it keys on `Host af-forge` with port 22888 + dedicated key. A `/etc/hosts` entry `100.64.0.2 af-forge` was added — harmless, but NOT the fix (pulse used IP anyway).

## What NOT to do (all done or proposed during the session, none correct)

- `ip link set tailscale0 mtu 1200` on KVM8 — applied, non-persistent, proved nothing: big responses still timed out. MTU probing (DF ping) showed 1200B pass / 1300B+ fail both directions, but ICMP passes at full size while TCP large transfers fail → asymmetric PMTU blackhole territory, NOT fixable from the node side.
- A relayed session claimed "MTU 9000 jumbo frames fix applied" — **fabricated**. Tailscale caps at 1280 (WireGuard overhead); jumbo frames over WireGuard are invalid. Lesson: never forward a fix claim you didn't verify; verify state yourself before reporting.
- `tailscale set --derp-only=true` — proposed, correctly REJECTED: topology-wide change (adds 30-50ms to ALL mesh traffic) to fix a transient that had already self-resolved. Also flag syntax was unverified for the installed version.
- Restarting tailscaled / FED / haproxy — nothing was wrong with any of them.

## Durable lessons

1. **A remote monitor alert is a hypothesis.** Re-probe from the target node and at least one other vantage before declaring an outage. One failing probe (or one failing endpoint size) ≠ node down.
2. **Lightweight endpoints for cross-tailnet monitoring.** `/health/liveliness` (12B) is the contract; `/health` (13KB) is for humans on localhost. Point every mesh pulse/watchdog at liveliness.
3. **One-cycle transient = log, don't page.** Suppress single-cycle failures (require 2-3 consecutive failures over N minutes) before alerting. Route flaps self-heal.
4. **Persistent-connection-passes / fresh-connection-fails is a Tailscale route-flip signature**, not a service backlog or conntrack issue (conntrack was 175/262144). Check `tailscale ping` path type and `tailscale netcheck` before touching iptables.
5. **Verify before reporting fixes.** Claiming "MTU 9000 applied" without verification poisoned the diagnostic thread for several turns.
