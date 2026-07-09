# arifOS Federation — Canonical Agent Architecture
> Forged: 2026-06-05 | Hermes ASI + Kimi Code
> Status: LIVE | Verdict: SEAL

## The Truth

**Hermes is the ASI ingress.** All human conversation flows through Hermes.
**arifOS is the law layer.** All dangerous actions are gated through arifOS 888_JUDGE.
**External agents are direct workers.** Kimi, Claude, Copilot edit files and run code directly.
**OpenClaw is a chat router.** Telegram routing + model inference. Not an execution gate.
**Capability Index is the discovery layer.** Any agent discovers tools via local Qdrant.
**Shared memory is the learning layer.** NATS JetStream carries cross-agent outcomes.

## What Changed (2026-06-05)

### Before (Copilot Proposal)
- "Route all execution through OpenClaw" — WRONG
- OpenClaw as "execution commons" — WRONG
- Agent shims for every CLI — over-engineering

### After (Kimi Correction)
- OpenClaw stays in its lane: Telegram routing + model inference
- Dangerous actions go through arifOS 888_JUDGE (direct, fast, zero errors)
- Coding actions are direct (no middleman, no token penalty)
- Capability Index is a local lookup (zero LLM cost)
- Shared memory is a NATS publish (zero LLM cost)

## Cost Reality

| Action | Extra Token Cost | Why |
|--------|-----------------|-----|
| Read file / edit code / run test | Zero | Direct execution |
| Discover tools via Capability Index | Zero | Local Qdrant vector search |
| Dangerous action (git push --force, deploy) | ~1 small arifOS call | Only when needed |
| Publish to shared memory | Zero | NATS message, no LLM |

## Agent Roles

| Agent | Role | Lane |
|-------|------|------|
| Hermes 💃 | ASI human-facing ingress | Telegram, coordination, cron |
| OpenClaw 🦞 | AGI chat router + model inference | Telegram routing, model failover |
| arifOS ⚖️ | Constitutional law layer | F1-F13, 888_JUDGE, VAULT999 |
| A-FORGE 🔨 | Execution substrate | Build, deploy, sandbox |
| Kimi Code ⚡ | Speed executor | Terminal-native coding |
| Claude Code 🧠 | Reasoning specialist | Architecture, code review |
| Copilot ✏️ | IDE operator | Inline code suggestions |

## Dangerous Action Path

```
Agent wants to: git push --force / deploy / delete / rotate secrets
  → arif_judge_deliberate (arifOS 888_JUDGE, localhost:8088)
  → SEAL → execute
  → HOLD → ask Arif
  → VOID → blocked
```

NOT: Agent → OpenClaw → arifOS → back → back → back. That's three extra hops for nothing.

## Capability Discovery Path

```
Agent: "What tools handle zakat calculation?"
  → Capability Index (Qdrant vector search, localhost:6333)
  → Returns: wealth_personal_finance (zakat mode)
  → Zero tokens. 50ms.
```

## Shared Memory Path

```
Claude: fixes a bug, learns a pattern
  → Publish to NATS agent.memory stream
  → Kimi encounters similar bug
  → Queries shared memory
  → Finds Claude's solution
  → Zero tokens. Cross-agent learning.
```

## What We Have NOW (2026-06-05)

✅ Capability Index: 106 tools, 8 servers (Kimi-forged at /root/AAA/registries/CAPABILITY_INDEX.json)
✅ arifOS law layer: F1-F13 active, 888_JUDGE live, VAULT999 sealed
✅ Hermes ASI ingress: Telegram, cron, A2A coordination
✅ OpenClaw AGI router: Model inference with deepseek primary, ilmu fallback
✅ Cross-agent memory: NATS JetStream agent.memory stream
✅ Agent cards: Hermes, OpenClaw, Claude Code, Kimi Code
✅ Telemetry schema: Cross-agent event envelope
✅ Direct execution: Kimi, Claude edit files directly
✅ Selective governance: Dangerous actions only through arifOS

🔜 Agent Router (month 2+): Smart task dispatch
🔜 Memory promotion discipline: Ephemeral → Session → Reusable → Sealed

## The Invariant

**The system may recursively improve execution, but may not recursively rewrite sovereignty.**
arifOS remains the law layer. Arif remains F13 SOVEREIGN. No agent self-authorizes.
