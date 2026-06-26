# opencode-bot (000Ω)

**arifOS-gated Telegram code-specialist translator for Arif.**

A read-only Telegram bot that turns federation code, audit data, and system
state into plain human language. Every request is pre-flighted through the
arifOS 888_JUDGE gate via the `hermes-opencode` wrapper.

## What it does

When Arif sends a message, the bot:

1. Verifies sender is Arif (F13 SOVEREIGN, user_id=267378578). Refuses everyone else silently.
2. Builds a persona-locked prompt: "translate to plain human language, no code, no jargon."
3. Calls `hermes-opencode run "..."` (the GATED wrapper).
4. The wrapper calls `arif_judge_deliberate` on the proposed delegation.
5. If verdict is SEAL/SABAR/QUALIFY, opencode runs and returns the answer.
6. If verdict is HOLD/VOID/888_HOLD, the wrapper blocks and the bot explains in plain words.
7. Bot sends the reply to the same Telegram thread.
8. The judge's verdict is sealed to VAULT999 by the wrapper automatically.

## Architecture (the constitutional part)

```
Arif on Telegram
       │
       ▼
opencode-bot (this service, 127.0.0.1 polling, no public ingress)
       │
       ▼
hermes-opencode wrapper  ←── GATE — no opencode call without judge approval
       │
       ├──▶ arifOS MCP 8088 → arif_judge_deliberate → verdict → VAULT999 seal
       │       │
       │       └─ SEAL/SABAR/QUALIFY ──▶ proceed
       │       └─ HOLD/VOID/888_HOLD ──▶ block (exit 77)
       │       └─ MCP down ──▶ block (exit 78)
       │
       └──▶ opencode CLI  (the actual model, MiniMax-M3 with full MCP tools)
                  │
                  ▼
              reply (plain human language, by persona)
                  │
                  ▼
              back to Telegram
```

## Files

| File | Purpose |
|---|---|
| `bot.py` | The bot. ~210 lines. Token from vault, Telegram polling, calls hermes-opencode. |
| `/etc/systemd/system/opencode-bot.service` | systemd unit. Hardened. Sets `ARIFOS_MCP_URL=http://127.0.0.1:8088/mcp` so the wrapper talks to arifOS (port 8088), not Caddy (port 8080). |
| `/root/.secrets/tokens/telegram-opencode-bot` | Bot token (mode 600). |
| `/usr/local/bin/hermes-opencode` | The GATED wrapper (134 lines of Python). We invoke this, not raw `opencode`. |

## Why hermes-opencode, not raw opencode?

Raw `opencode` would let the bot call the model without any governance check.
That's a constitutional violation: any code-writing or irreversible delegation
must have JUDGE_SEAL_AUTHORIZATION first (per the federation's authority
chain). `hermes-opencode` enforces that on every call. The bot stays
"read-only and explainable" precisely because the gate blocks anything that
would cross that line.

## Run

```bash
systemctl daemon-reload
systemctl enable --now opencode-bot
journalctl -u opencode-bot -f
```

## Scope (F13 / constitutional)

- **Read-only** — no forge, no seal, no mutation
- **Gated** — every call passes through 888_JUDGE
- **Single user** — only Arif's Telegram user_id is allowed
- **No public ingress** — outbound to `api.telegram.org` and `127.0.0.1:8088` only
- **No memory writes** — does not write to L1-L5. Systemd journal only.
- **Reversible** — `systemctl stop opencode-bot` and it's gone
- **Hardened** — `NoNewPrivileges`, `ProtectSystem=strict`, `PrivateTmp`,
  memory cap 512M, CPU 50%

## Exit codes from hermes-opencode (for debugging)

| Code | Meaning | Bot reply to Arif |
|------|---------|-------------------|
| 0 | success | the model answer (in plain human language) |
| 77 | governance blocked (HOLD/VOID) | "the gate blocked this — try a more read-only question" |
| 78 | judge unavailable (arifOS MCP down) | "the brain is offline — try again in a minute" |
| other | opencode internal error | "my brain hiccup" |

## Why a new bot, not extend Hermes?

Hermes is the public-facing chat surface (MiniMax-M3, friendly persona).
000Ω is the dev-tool surface (gated, terse persona, code-specialist, read-only).
Different jobs, different voices, different governance posture.

## DITEMPA BUKAN DIBERI
