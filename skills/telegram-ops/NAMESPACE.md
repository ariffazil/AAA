# NAMESPACE: telegram-ops

> **Updated 2026-09-20 (F13 skill-merge) — this directory is now the UMBRELLA, not a namespace.**
> The skill `telegram-ops` lives here: `SKILL.md` + `references/`.
> Previous marker (2026-09-19) declared this a namespace holding `outbound-message-delivery`;
> that skill is now `references/outbound-message-delivery.md`, archived at
> `/root/AAA/skills/.archive/merge-20260920/telegram/outbound-message-delivery/`.

## What lives here

- `SKILL.md` — the umbrella. Its `## FLOW` section is the routing table: **situation / observable →
  reference file**. Read it first.
- `references/` — the twelve merged member bodies, byte-identical to the originals, each under a
  four-line provenance header carrying the source sha256.

Merged members (12 → 1): forge-telegram-audit · hermes-lane-switch-routing ·
hermes-telegram-gateway-authorization · hermes-telegram-stack-zen · outbound-message-delivery ·
relay-echo-loop-handling · telegram-bot-identity-and-group-routing · telegram-bot-routing-doctrine ·
telegram-conversation-history-extraction · telegram-group-bot-rollout ·
telegram-group-sender-identity · telegram-userbot-telethon

Archive: `/root/AAA/skills/.archive/merge-20260920/telegram/`
Receipt: `/root/forge_work/merge-2026-09-20/telegram-receipt.json`
Alias fragment: `/root/forge_work/merge-2026-09-20/alias-telegram.json`

## Owner

**Owner:** `AAA/telegram-ops`

## Conventions

- The umbrella holds rules and routing; a reference holds the procedure. Do not summarise a
  reference into `SKILL.md`.
- Do not edit a reference body except to re-sync it with a changed original — and if you do,
  update its provenance `sha256-body` line.
- `references/` is a loader support dir: a `SKILL.md` inside it would not be discovered, so it is
  safe for bodies to keep quoting paths like `references/foo.md` from their original skill.
