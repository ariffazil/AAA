# 2026-09-01 — LiteLLM crash-loop: prisma migrate deploy hangs at boot

**Class:** FED down / crash-loop at boot — NOT upstream, NOT HAProxy, NOT Headscale.

## Symptom signature

- FED `100.64.0.2:4000` returns 503 / times out; HAProxy backend unhealthy.
- `journalctl -u litellm-federation --since today | grep -icE 'prisma|migration'`
  → hundreds of hits (this incident: 264).
- Every restart spends 3–5 min in `Running prisma migrate deploy`, times out,
  systemd `Restart=on-failure` fires → infinite loop + CPU burn.
- Root trigger here: pending migration `20260901030840_baseline_diff` applied
  against the LOCAL postgres (`127.0.0.1:5432/litellm`, docker postgres container)
  while prisma CLI itself was slow/hanging.

## Diagnosis commands (worked, verified)

```bash
ss -tlnp | grep -E ':(4000|4013)\b'           # who holds FED ports
systemctl is-active haproxy litellm-federation
systemctl cat litellm-federation.service      # base unit + drop-ins
journalctl -u litellm-federation --since today --no-pager | grep -iE 'prisma|migration' | head
curl -sS -m 5 http://127.0.0.1:4000/health/liveliness   # "I'm alive!"
```

Topology notes (2026-09-01 state):
- Base unit says port 4000/127.0.0.1 but the ACTIVE drop-in
  (`/etc/systemd/system/litellm-federation.service.d/override.conf`) overrides
  ExecStart → litellm binds **0.0.0.0:4013**; HAProxy :4000 fronts it.
  Always `systemctl cat`, never trust the base unit alone.
- `LITELLM_DATABASE_URL=postgresql://arifos_admin:...@127.0.0.1:5432/litellm`
  lives in `/root/.secrets/kunci-mas.flat.env`; the drop-in `UnsetEnvironment`s it.

## Recovery applied (stateless mode)

1. Comment out `database_url:` in `general_settings` of
   `/root/A-FORGE/litellm-config.yaml` (annotated with date + reason).
2. systemd restart → litellm boots without touching prisma/postgres.
3. Verified end-to-end: local :4000 liveliness, tailnet-IP curl
   (see curl pitfall below), `tailscale status`, HAProxy backend healthy.

**Trade-off:** stateless FED routes fine but loses spend tracking /
virtual-key persistence. It is a bridge, not a fix — re-enable DB after the
proper fix below.

## Correct long-term fix (NOT yet applied — hold decision)

Separate migration from boot:
1. Oneshot systemd unit (or manual step) that runs
   `prisma migrate deploy` against the local DB BEFORE litellm starts.
2. Then re-enable `database_url` (local) in the config.
Reversible, local-only, touches no other node.

## Rejected fix — wrong diagnosis

"Point `LITELLM_DATABASE_URL` at remote Supabase" was proposed as the
permanent fix. REJECTED: root cause is prisma CLI timing out at boot, not
postgres being slow. Coupling LiteLLM state to the vault's Supabase creates
new cross-node failure coupling for a problem that doesn't exist.

## Pitfalls hit during this incident

- **Tailnet curl flake:** first `curl -m 10 http://100.64.0.2:4000/...` timed
  out at 10s; retry with `-m 20` succeeded. On the tailnet, one timeout ≠
  service down — retry once with a longer budget before concluding anything.
- **PrometheusLogger spam:** journal filled with
  `'PrometheusLogger' object has no attribute 'litellm_requests_metric'` on
  every request. Non-blocking, routing unaffected. Do NOT chase it
  mid-incident; fix in a maintenance window.
- **"Recovered by itself" claims:** the recovery report said the system
  self-recovered, but mtimes showed config edit 13:18 + drop-in 13:32 +
  process restart 14:17 — surgery had happened. When verifying another
  agent's recovery claim, diff config/unit mtimes against the timeline and
  read the journal; recoveries are rarely spontaneous.

## Decision taken

HOLD. Let the next wawa pulse confirm stability before any permanent change.
If the pattern recurs, the separated-migration fix above is ready to execute.
