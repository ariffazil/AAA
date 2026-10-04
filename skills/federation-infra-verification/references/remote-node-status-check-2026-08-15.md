# Remote Federation Node Status Check — wawa / azwaos (2026-08-15)

Session: Arif (DM) asked "How's wawabot status". WAWA = Azwa's Hermes instance, TG user 8324190535, on remote node `srv1642546` ("azwaos" / "flow-edge", Hostinger VPS, Tailscale IP `100.64.0.4`). Not on the main federation box.

## Access pattern

- SSH alias already in `~/.ssh/config`: `Host srv1642546 → 100.64.0.4`, key-based, BatchMode works. Public fallback alias `srv1642546-public` (72.61.126.65).
- Verify mesh first if SSH fails: `tailscale status | grep azwaos` → must show `active; direct`.
- Unit name on that node: `hermes-agent.service` ("Hermes ASI Gateway for Azwa") — naming differs from main-node gateway units (`forge-gateway` etc.), don't assume.

## The 3-probe status check (all three, every time)

```bash
# P1 — alive NOW (a snapshot; hides history)
ssh srv1642546 "systemctl status hermes-agent.service --no-pager | head -8"

# P2 — stability HISTORY (where crash loops hide)
ssh srv1642546 "journalctl -u hermes-agent.service --since '2 hours ago' --no-pager | tail -30"

# P3 — gateway layer agreement
ssh srv1642546 "timeout 8 /usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main gateway status"
```

## Findings this session

1. **"active (running) since <recent>" hid a 20× crash loop.** Journal showed `status=127/n/a` exit loop with `restart counter is at 20` around 13:31 MYT, then a manual stop/start at 13:32, stable since 14:26 (uptime ~54min, RAM ~160MB). Self-recovered via Restart= policy + manual restart — "healthy now" was true but incomplete. Reported the scar alongside the present state because the human asked *status* while suspecting something.
2. **App stdout didn't reach journald.** `journalctl -o cat` showed only systemd lifecycle lines (Started/Stopping/exited) — no app logs. That is NOT "no logs exist"; the exit codes ARE the diagnostic story. App-level logs live in the node's HERMES_HOME logs dir; check the unit's `StandardOutput=` before concluding journald is empty.
3. **`gateway status` said "Running manually, not as a system service"** for a process systemd started (PID matched unit MainPID). The label is unreliable — cross-check `systemctl show <unit> -p MainPID` vs the PID gateway reports before believing either.

## Lane discipline

A remote-node bot serves another human (wawa → Azwa). Read-only SSH diagnosis from Arif's session = fine. Root-cause digging or restarts on that node = surface findings to the sovereign and let him decide — it's someone else's lane.

## Generalization

For ANY "how's bot X status" question: first establish WHERE the bot lives (grep `/root/HERMES/memories/MEMORY.md` + `~/.ssh/config`), then run the 3 probes against that node. Never answer from memory of last known state.
