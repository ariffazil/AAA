# FED HAProxy Migration — 2026-08-09 (port-collision crash-loop postmortem)

> Context: after the 11h Tailscale outage, OpenCode re-architected FED with an HAProxy front
> + escape hatch. The migration was HALF-APPLIED and crashed the fleet a SECOND time.
> This is the full diagnosis + fix recipe so the next migration audit runs in minutes, not hours.

## The intended architecture (design)

```
clients (Hermes/OpenCode/OpenClaw/Codex) → 127.0.0.1:4000 (HAProxy)
                                              ├─ fed_primary  127.0.0.1:4011  (litellm-federation, 5 providers)
                                              └─ escape_backup 127.0.0.1:4012 (litellm-escape, DeepSeek+MiMo, backup flag)
```

- HAProxy: `option httpchk GET /health` with `Authorization: Bearer <LITELLM_MASTER_KEY>` header,
  `fall 2 rise 2`, escape marked `backup` → only used when primary fails health check.
- Escape config: `/root/A-FORGE/escape-config.yaml` — ~30 lines, localhost-only, no Tailscale dep.
- `socat` (litellm-local-forward) killed — no more 127→100.64.0.2 forwarding.

## The crash (what actually happened)

OpenCode pointed the NEW litellm instances at `:4001`/`:4002` — **ports already held by legacy shims**:

| Port | Squatter (old, still needed) | New service that wanted it |
|---|---|---|
| 127.0.0.1:4001 | `fed-clean-proxy.service` (Codex Responses-API stripper, Aug 5) | `litellm-federation` (drop-in) |
| 127.0.0.1:4002 | `mimo_vision_shim.py` (bare process, vision URL→base64 for MiMo, Aug 5) | `litellm-escape` |

Result: `Errno 98: address already in use` → `litellm-federation` crash-looping (`NRestarts=6`),
`litellm-escape` crash-looping, HAProxy `503 Service Unavailable` (no healthy backend) → Hermes dead.

**Worse:** if HAProxy HAD routed to :4001, it would have hit the clean-proxy → which forwards back
to :4000 → **infinite routing loop**. The collision was load-bearing, not cosmetic.

## The diagnosis sequence (reusable)

```bash
# 1. Port map — WHO holds what
ss -tlnp | grep -E ':400[0-9]|:401[0-9]'

# 2. Service states + restart counters (crash-loop signature)
for s in haproxy litellm-federation litellm-escape fed-clean-proxy; do
  echo "$s: $(systemctl is-active $s) restarts=$(systemctl show $s -p NRestarts --value)"
done

# 3. Process ages — old zombie vs new instance
ps -o pid,lstart,cmd -p <pid>

# 4. Crash reason
journalctl -u litellm-federation --no-pager -n 40 | grep -B5 -A5 'Errno\|error\|Traceback'

# 5. The unit file may LIE — check drop-in overrides + mtime
cat /etc/systemd/system/litellm-federation.service.d/override.conf
stat -c '%y' /etc/systemd/system/litellm-federation.service
```

## The fix (reversible-first, applied + committed 4cc5a6a8)

Move the NEW litellm instances to free ports; LEAVE legacy shims untouched (Codex + vision depend on them):

1. `litellm-federation.service.d/override.conf`: `--port 4001` → `--port 4011 --host 0.0.0.0`
2. `litellm-escape.service`: `--port 4002` → `--port 4012`
3. `/etc/haproxy/haproxy.cfg`: `fed_primary 127.0.0.1:4001` → `:4011`; `escape_backup 127.0.0.1:4002` → `:4012`
4. `systemctl daemon-reload` **then** restart (see trap below)
5. Verify: `ss -tlnp` shows `0.0.0.0:4011` + `127.0.0.1:4012` + HAProxy :4000, all `restarts=0`

Snapshots: `/root/forge_work/backups/fed-ha-migration-20260809/{override.conf,litellm-escape.service,haproxy.cfg}.orig`

## Pitfall: editing a .service.d override WITHOUT daemon-reload

The crash-loop restarts kept reusing the OLD cached ExecStart (`--port 4001`) even after the
override.conf on disk said 4011 — because `systemctl daemon-reload` was never run. systemd reads
unit files at daemon-reload, not at every restart. **Always `daemon-reload` after touching any
.service or .service.d file, THEN restart.**

## Failover validation (the full loop, all 200)

| Probe | Path | Result |
|---|---|---|
| Primary | HAProxy :4000 → :4011 `dispatch` | `DISPATCH PRIMARY OK`, 2.6s, 200 |
| Escape direct | :4012 (bypass HAProxy) `dispatch` | `DISPATCH ESCAPE OK`, 0.9s, 200 |
| Failover | `systemctl stop litellm-federation` → HAProxy → escape | `FAILOVER WORKS`, 1.1s, 200 |
| Restore | `systemctl start litellm-federation` → :4011 back | active, restarts=0 |

## Dispatch alias — the TRUE chain (2026-08-09, config-verified)

- **Actual:** `mimo-v2.5-pro` (order 1) → `qwen3.8-max` (order 2). MiniMax M3 **stripped** — it
  appeared in OpenCode's explainer table but is NOT in `litellm-config.yaml` (only 2 dispatch blocks).
- Escape path: `dispatch` → `deepseek-chat` (ultimate fail-safe, no Tailscale).
- dispatch is a thinking model: 40 reasoning tokens vs 6 content tokens on a trivial reply. Small
  `max_tokens` → empty `content` (see reasoning-model pitfall in SKILL.md).

## Wiring audit snapshot (who is on FED, as of 2026-08-09)

| Surface | Endpoint | FED? |
|---|---|---|
| Hermes gateway (Telegram) | wrapper → :4000 hermes-asi | ✅ |
| Hermes CLI default profile | fed provider → :4000 | ✅ |
| OpenCode (all 6 lanes) | `litellm-federation/*` | ✅ |
| OpenClaw | :4000/v1 | ✅ |
| Claude Code | :4000 | ✅ |
| 555-ASI / 888-APEX / dispatch | litellm aliases | ✅ |
| aaa-hermes profile sessions + 16 cron jobs | deepseek DIRECT | ❌ not yet |
| Kimi | kimi-code/k3-256k direct | ❌ not yet |

Kimi + cron staying direct is defensible as escape-hatch independence — Arif decides.
