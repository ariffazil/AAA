# Throttle Incidents 2026-08-30 → 2026-09-01 — Session Transcript

Two back-to-back sustained-CPU incidents on the Hostinger VPS (8 cores, 32GB). Condensed evidence for the vps-cpu-throttle-triage playbook.

## Incident 1 — 2026-08-30 night → 31

Symptom reports: CPU steal 89% → 50-70%; 10+ model providers rate-limited simultaneously; gateway stuck 100% in Telegram retry loop.

Actions taken (all F13-authorized):
- Killed runaway Kimi (PID 236123, 90% CPU) and stuck grep in D-state (PID 225213, 47%).
- Restarted Hermes gateway cleanly; systemd auto-respawned fresh.
- Killed duplicate orphan `hermes serve --port 9120` (PID 306908, PPID=1, 0% CPU idle) after confirming nothing else bound the port. SIGTERM sufficed.
- Verdict on simultaneous rate limits: NOT a chain to hammer — enforce provider cooldown ≥30 min, retry later. Hammering a fallback chain under global rate limits = longer failure path, not reliability.

## Incident 2 — 2026-09-01 early morning

### The stale-report trap
User-relayed report claimed: 74.9% steal, "OpenClaw/LiteLLM/Hermes competing", throttle active. Live re-measurement showed a reboot had ALREADY happened ~10h prior: steal 0-8%, load 2.0-2.5 on 8 cores, 22GB RAM available. The heavy "competing" runtimes were idle (opencode serve 2.7% CPU with zero active clients). Acting on the report would have been wrong.

### Silent drains found
1. **Langfuse exporter retry-storm** — `Failed to export span batch code: 404` ×1,377 in errors.log. Root cause: `LANGFUSE_BASE_URL=http://localhost:4000` in kunci-root.env, but 4000 is HAProxy (LiteLLM front door) — the Langfuse docker stack was never up (3100 was a telegram-miniapp node process; `/api/public/otel/v1/traces` → 404 even with valid Basic auth). Fix: `hermes plugins disable observability/langfuse` (agent cannot write config.yaml directly — write tool refuses security-sensitive files; CLI is the sanctioned path).
2. **Bot spam retry-storm** — 2,255 retry lines in gateway.log, mostly `Forbidden: the bot can't send messages to the bot` to chat 1042200555 and `Reply target deleted`, plus blocked-media floods (user 8195715289 in chat -1004417918825).
3. **Kabarkan NATS backlog** — after worker downtime, stream `kabarkan-ingest` held ~140,793 msgs / 107MiB. Fresh consumer (Deliver Policy: All, Ack Wait 30s, MaxDeliver 3, InactiveThreshold 5s) chewed backlog at ~6,300 msg/min; worker CPU 44-108% during catch-up = EXPECTED, not runaway.

### Tuning applied
- `/etc/systemd/system/kabarkan-worker.service.d/interval.conf`: `KABARKAN_POLL_INTERVAL=5.0→30.0`, `KABARKAN_BATCH_SIZE=20→50` (backup `.bak-20260901` kept). daemon-reload + restart.
- Service had come back DISABLED after reboot → `systemctl enable` + start.

### Post-reboot audit findings
- `arifos-guard.service` failing: ExecStart file `/root/forge_work/2026-07-17/firewall/arifos_guard.nft` missing, AND zero arifos rules in live ruleset pre-reboot → guard long dead. Stubbed ExecStart=/usr/bin/true (original unit backed up as `.bak-20260901`); real perimeter = UFW (active).
- `sct-renew.service` timeout → manual `python3 /root/scripts/sct_renew.py` renewed the federation session envelope (TTL 1h; without it arif_seal/arif_judge fail SCT_EXPIRED). Note: kernel MCP endpoint needs `Accept: application/json` (bare curl gets 406).
- `gov-a007-completion-verifier` failing: script does host-level `pg_dump` but Postgres now runs in Docker. One-line fix pending (`docker exec postgres pg_dump`).
- opencode interactive session (118% CPU, pts/2) belonged to Arif — left alone; exited on its own later.

### Measurement commands that earned their keep
```bash
vmstat 1 3 | tail -1                      # live steal (st column)
ps -eo pid,ppid,etime,time,%cpu,stat,tty,cmd --sort=-%cpu
systemctl status <PID>                    # unit owner of any PID
nats stream info -j kabarkan-ingest | jq .state.messages
nats consumer info kabarkan-ingest kabarkan-worker-fresh
grep -c "Failed to export span batch" errors.log
ss -tlnp | grep -E ":4000|:4318|:3100"    # who ACTUALLY owns the port
```

### Capacity verdict (both incidents)
Single box with 6 agent runtimes + DBs + search is over-consolidated; Hostinger weekly reset already consumed. Recommendation to sovereign: second VPS for workload isolation (control plane vs model/search/batch), designed first, not emergency-migrated. F13 cost decision — agent does not buy.
