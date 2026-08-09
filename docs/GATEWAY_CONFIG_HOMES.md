<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# GATEWAY_CONFIG_HOMES.md — Canonical Gateway Config Map

> **Purpose:** End the "which config do I edit?" confusion. This box has **multiple Hermes config homes**; only one is read by the live gateway.
> **Last verified:** 2026-08-05 (live probe: PID 417929, `gateway run --replace`)
> **Rule:** If you touch the gateway, read this first. `probe before act` — `ss -tlnp | grep 8444` + `systemctl show hermes-asi-gateway -p Environment` are truth.

## The two homes (do NOT mix them up)

| Path | Status | What reads it |
|---|---|---|
| `/usr/local/lib/hermes-agent/config.yaml` | ✅ **ACTIVE** (HERMES_HOME) | The running gateway — **but has NO telegram block** |
| `/root/.hermes/config.yaml` (40KB, legacy) | ⚠️ **STALE / semi-dead** | Old install; MCP server still runs from here (PID 391426-era). **Telegram block at line 916 is decorative** — the gateway does not read it. Editing it = editing a file nothing reads. |

## Where the Telegram token ACTUALLY comes from

1. **Adapter hardcode** — `plugins/platforms/telegram/adapter.py:9776` reads `TELEGRAM_BOT_TOKEN` env directly; `:9965` requires it. The `bot_token_env:` YAML key is **ignored** by this adapter.
2. **Unit drop-in injection** — `/etc/systemd/system/hermes-asi-gateway.service.d/zzz-webhook-override.conf` injects `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_URL`, `TELEGRAM_WEBHOOK_PORT=8444`, `TELEGRAM_WEBHOOK_SECRET`, `TELEGRAM_ALLOWED_USERS`. **This is the control knob.**
3. **flat.env** — `/root/.secrets/kunci-mas.flat.env` (auto-generated from KUNCI-MAS vault). No generic `TELEGRAM_BOT_TOKEN` since 2026-08-04 sweep. Per-bot vars: `ASI_ARIFOS_BOT_TOKEN`, `AGI_ASI_BOT_TOKEN`, `FORGE_BOT_TOKEN`.

## Identity map (verified live 2026-08-05)

| Bot | ID | Token var | Webhook route → port |
|---|---|---|---|
| @ASI_arifos_bot (Hermes SOUL) | 8410138119 | `ASI_ARIFOS_BOT_TOKEN` / injected `TELEGRAM_BOT_TOKEN` | `/telegram/webhook` → :8444 |
| @AGI_ASI_bot (OpenClaw GUTS) | 8149595687 | `AGI_ASI_BOT_TOKEN` (file: `.secrets/tokens/telegram-agi-asi-bot`) | `/telegram-webhook*` → :8787 (OpenClaw) |
| @arifOS_bot (FORGE) | 8727562763 | `FORGE_BOT_TOKEN` | `/forge/webhook` → :8445 |

**History (why this doc exists):** 2026-08-05 morning — gateway silently spoke as @AGI_ASI_bot because the active config had no telegram block → adapter fell back to generic `TELEGRAM_BOT_TOKEN`, which at that time held OpenClaw's token. Six drift points stacked: 2 config homes, adapter hardcode, generic token name, shared webhook URL, prefilter/allowlist mix-up, Caddy source↔runtime drift. All closed; this doc is the anti-regression.

## Operate (the only 3 commands you need)

```bash
# 1. What the live gateway is injected with
systemctl show hermes-asi-gateway -p Environment

# 2. Who owns :8444 (webhook listener)
ss -tlnp | grep 8444

# 3. Edit the token → edit the drop-in, then restart
nano /etc/systemd/system/hermes-asi-gateway.service.d/zzz-webhook-override.conf   # mode 600!
systemctl daemon-reload && systemctl restart hermes-asi-gateway
```

**Never edit `/root/.hermes/config.yaml` for Telegram changes. Never re-add generic `TELEGRAM_BOT_TOKEN` to the vault.**

*Canon: /root/AAA/docs/GATEWAY_CONFIG_HOMES.md — DITEMPA BUKAN DIBERI*
