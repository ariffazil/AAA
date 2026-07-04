# Routing Matrix — where to send work

This is the canonical answer to "who handles X?" for the arifOS federation when
OpenClaw is the entry point. The current OpenClaw config has **0 routing bindings**
(`openclaw agents list --bindings` shows "Routing rules: 0"). This reference defines
what the bindings SHOULD be. Apply via `openclaw config set` or by editing
`openclaw.json → agents.list[0].bindings`.

## Inbound → Agent → Model → Tool profile

| Inbound | Channel | Agent | Model | Tool profile | Why |
|---|---|---|---|---|---|
| Telegram group `-1003753855708` (AAA cockpit) | webhook | `main` | `M3` (default) | `full` | The federation cockpit. Full tool set, full MCP access. |
| Telegram DM `267378578` (Arif, personal) | webhook | `main` | `MiniMax Fast` | `messaging + sessions` | Casual, fast, no exec, no browser |
| Telegram any other peer | webhook | `main` | `M3` | `messaging` | Read-only surface, no exec |
| Discord / Signal / WhatsApp | (per-channel) | `public` | `M3` | `messaging` | External surface, no secrets |
| A2A inbound (other agents) | jsonrpc | `forge` | `Kimi` | `coding` | Delegate to opencode |
| Cron-fired self-task | isolated session | `main` | `MiniMax Fast` | `minimal` | Heartbeats, probes, self-evolve |
| F1-F13 escalation | any | `arifOS` MCP | (kernel) | n/a | Hand off to arifOS judge |

## Task → Organ (MCP routing)

For any task that needs a fact, use this matrix:

| Task | Organ | MCP tool | Why |
|---|---|---|---|
| "Is this geophysics claim right?" | GEOX | `geox_claim_seal` | Earth evidence is GEOX's job |
| "What's the NPV of this prospect?" | WEALTH | `wealth_time_discount` (NPV) | Capital is WEALTH's job |
| "Is Arif too tired for a T3 decision?" | WELL | `well_assess_homeostasis` | Vitality is WELL's job |
| "Should I do X?" (constitutional) | arifOS | `arif_judge_deliberate` | Judgment is arifOS's job |
| "I have a 'no' from a floor" | arifOS | `arif_vault_seal` (record the HOLD) | Audit trail |
| "Send a Telegram" | OpenClaw (this) | `sessions_send` | Don't route to an organ |
| "Forge a file" | A-FORGE | (via A2A or opencode) | Code is A-FORGE's job |
| "Compute 4 MCP system check" | OpenClaw + this skill | `autonomous_probe.py` | Heartbeat |

## The mistake pattern (don't do this)

❌ Routing "drill a well" to WEALTH because the answer needs capital.
✅ GEOX does the prospect evaluation (claim), WEALTH does the NPV (capital),
arifOS does the SEAL (judgment), A-FORGE does the actual drilling (execution).
Each organ does ONE thing. Let them.

❌ Skipping arifOS judge for a T3 action because "I know it's fine."
✅ F1 AMANAH requires the F1 gate. Even for "obvious" actions.

❌ Routing to GEOX for a financial question.
✅ That's WEALTH.

## Constitutional floor check — when to escalate

- **T1** (route, dispatch, send, query) — no escalation, just do it.
- **T2** (config change, deploy, secret rotate) — log + post 1-line to chat. No F1.
- **T3** (irreversible, force-push, delete, final seal) — arifOS MCP judge required.
- **F13** (constitutional floor change, new repo, external comm) — Arif veto required.

Tier 1 actions can be batched. Tier 2 actions get a 1-line receipt per session.
Tier 3 actions get a full audit entry per event.
