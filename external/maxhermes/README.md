# MaxHermes — External Third-Party Service

**Status:** Documentation entry. NOT under AAA Federation control.

## What it actually is (verified 2026-06-22)

MaxHermes is **Minimax's managed cloud deployment of the Hermes Agent framework** by Nous Research.

- **Vendor:** MiniMax (HKEX: 00100)
- **URL:** https://agent.minimaxi.com/max-hermes
- **Launched:** April 16, 2026
- **Default model:** MiniMax M2.7 (230B MoE, 10B active per token)
- **Pricing:** $0.30/M input tokens, $1.20/M output tokens (pay-as-you-go token plans)
- **Distinctive feature:** "Learning loop" — autonomously extracts reusable skills from completed tasks
- **Native integrations:** Feishu (Lark), DingTalk, WeCom (Chinese enterprise messaging platforms)
- **Western platform support:** None as of April 2026 (no Slack, Discord, Telegram, Teams)
- **License:** Proprietary (MiniMax ToS)

## Source of truth

- **Blog post (third-party):** https://lushbinary.com/blog/maxhermes-minimax-cloud-sandbox-self-evolving-ai-guide/
- **Official MiniMax platform:** https://agent.minimaxi.com/max-hermes

## Critical distinction from Hermes-ASI

| Property | Hermes-ASI (our bot) | MaxHermes (external) |
|---|---|---|
| **Owner** | Arif (F13 Sovereign) | MiniMax |
| **Hosted** | VPS af-forge (72.62.71.199) | MiniMax cloud |
| **Runtime** | Nous Research `hermes-agent` v3.0.0 | Hermes Agent framework + MiniMax M2.7 |
| **Data sovereignty** | Full (we own the data) | MiniMax cloud (data flows to vendor) |
| **Constitutional binding** | F1-F13 enforced at arifOS kernel | None |
| **Model** | Multiple providers (configurable) | M2.7 only |
| **Messaging** | Telegram + A2A | Feishu, DingTalk, WeCom |
| **License** | MIT (Nous Research) | Proprietary |

**Bottom line:** The naming overlap is unfortunate but the two are completely separate. Hermes-ASI is "Arif's bot". MaxHermes is "MiniMax's cloud product".

## Why was there a `agents/maxhermes/` in AAA previously?

Historical: someone in the federation configured a "local OpenClaw MaxHermes" agent entry
(`agents/maxhermes/`, `registries/openclaw/maxhermes-agent.yaml`) that was meant to be a
self-hosted version of MaxHermes using our local MCP servers (geox-mcp, arifos-mcp).

That local instance **never actually existed** — no service, no process, no open port. The
registry entries were aspirational.

This cleanup:
1. Removed the fictional local config (`agents/maxhermes/`, registry entries, schema enums)
2. Archived them to `_archive/maxhermes-2026-06-22/` for audit trail
3. Created this external/ entry documenting what MaxHermes ACTUALLY is
4. Updated internal docs to remove the misleading "Geology → maxhermes" routing

## Reversibility

If you want to integrate MaxHermes externally (call `agent.minimaxi.com/max-hermes` from
arifOS), the path is:
1. Register MiniMax API key in `/root/.secrets/vault.env`
2. Add a gateway route in `aaa-gateway` config (NOT a local agent entry)
3. F13 ack required for any data flowing to external (data sovereignty)
4. Witness via arifOS MCP

The archived `_archive/maxhermes-2026-06-22/` contains the old config for reference.

## DITEMPA BUKAN DIBERI

External services are honest, not fabricated. We don't claim ownership of things we don't own.
