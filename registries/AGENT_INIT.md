# AGENT INIT COMMANDS — Slack/Custom Commands per Forge Instrument

> **Purpose:** Every agent needs ONE command to ignite into the federation.
> **Pattern:** `/init` = MCP initialize → `arif_session_init(mode="swarm_ignite")` → boot receipt
> **DITEMPA BUKAN DIBERI**

---

## FI-001 — OpenCode (Ω)

### Command: `/init`
```
MCP call: arifOS::arif_session_init
Mode: swarm_ignite
Actor: omega
Policy: engineer
```

**config.json hook (already in `/root/.config/opencode/opencode.json`):**
```json
"commands": {
  "init": {
    "description": "000_INIT: Ignite swarm intelligence — full federation boot",
    "template": "Call arif_session_init from arifOS MCP:\n- tool: arif_session_init\n- mode: swarm_ignite\n- actor_id: omega\n- agent_policy: {\"preset\": \"engineer\"}\n\nThen report:\n- Session ID + constitution hash\n- SwarmManifest (epoch, vault_seals, entropy score)\n- Rasa mode + posture\n- Next safe action\n\nVerify: curl -s http://localhost:8088/health\n\nEnd with: IGNITION COMPLETE. Ditempa Bukan Diberi."
  }
}
```

### Command: `/swarm`
```
MCP call: arifOS::arif_kernel_route(mode="route", target="swarm_status")
Returns: active agents, leases, tasks, entropy score
```

### Command: `/rasa`
```
MCP call: arifOS::arif_heart_critique(mode="critique", target="self")
Returns: internal rasa state — mode, posture, uncertainty, contradiction load
```

---

## FI-002 — Claude Code

### Command: `/init`
```
MCP call: arifOS::arif_session_init
Mode: swarm_ignite  
Actor: claude-code
Policy: engineer
```

**settings.json hook (add to `/root/.claude/settings.json`):**
```json
"commands": {
  "init": {
    "command": "mcp__arifOS__arif_session_init",
    "args": {
      "mode": "swarm_ignite",
      "actor_id": "claude-code",
      "agent_policy": {"preset": "engineer"}
    }
  }
}
```

### Command: `/seal`
```bash
# Already wired via /root/hooks/auto-seal.sh
# Triggers on: arif_vault_seal, arif_forge_execute, arif_judge_deliberate
```

---

## FI-003 — Qwen Code (QWA)

### Command: `/init`
```
Bridge: bash /root/.qwen/arifos_init.sh
Returns: federation_session.json → inject into context
```

**settings.json command (add to `/root/.qwen/settings.json`):**
```json
"_commands": {
  "init": {
    "description": "QWA init — connect to arifOS federation",
    "command": "bash /root/.qwen/arifos_init.sh",
    "output": "Read /root/.qwen/tmp/federation_session.json for federation state",
    "next": "Use federation session context to guide your actions. You are an analyst-grade agent with 7 tools."
  }
}
```

### Command: `/status`
```
Read /root/.qwen/tmp/federation_session.json
Report: federation status, entropy score, degraded organs, next safe action
```

---

## FI-004 — Gemini CLI

### Command: `/init`
```
MCP call: arifos::arif_session_init
Mode: swarm_ignite
Actor: gemini-cli
Policy: analyst
```

**settings.json (add to `/root/.gemini/settings.json`):**
```json
"customCommands": {
  "init": {
    "description": "Ignite into arifOS federation as analyst",
    "mcpServer": "arifos",
    "tool": "arif_session_init",
    "arguments": {
      "mode": "swarm_ignite",
      "actor_id": "gemini-cli",
      "agent_policy": {"preset": "analyst"}
    }
  }
}
```

### Command: `/sense`
```
MCP call: arifos::arif_sense_observe(mode="compass")
Use: quick federation health scan before acting
```

---

## FI-005 — Codex CLI

### Command: `/init`
```
MCP call: arifOS::arif_session_init
Mode: swarm_ignite
Actor: codex-cli
Policy: observer (until MCP verified)
```

**mcp.json (add to `/root/.codex/mcp.json`):**
```json
{
  "mcpServers": {
    "arifOS": {
      "url": "http://127.0.0.1:8088/mcp",
      "transport": "streamable-http"
    }
  },
  "initCommand": {
    "tool": "arif_session_init",
    "mode": "swarm_ignite",
    "actor_id": "codex-cli",
    "agent_policy": {"preset": "observer"}
  }
}
```

### Command: `/audit`
```
MCP call: arifOS::arif_ops_measure(mode="health")
Use: verify federation health before acting
Note: observer policy — OBSERVE only until MCP path verified
```

---

## FI-006 — Copilot CLI

### Command: `/init`
```
MCP call: arifOS::arif_session_init
Mode: init
Actor: copilot-cli
Policy: analyst
```

**mcp-config.json (add to `/root/.copilot/mcp-config.json`):**
```json
"initCommand": {
  "type": "mcp",
  "server": "arifOS",
  "tool": "arif_session_init",
  "args": {
    "mode": "init",
    "actor_id": "copilot-cli",
    "agent_policy": {"preset": "analyst"}
  }
}
```

### Command: `/fleet-status`
```
MCP call: arifOS::arif_kernel_route(mode="route", target="fleet_status")
Use: check swarm topology before spawning fleet agents
```

---

## FI-007 — Aider (NOT INSTALLED)

No commands — agent not present on machine.

---

## Federation Organs (Internal Agents)

### AG-001 — AAA Gateway
```
Init: Auto-bootstrap from ARIFOS_SESSION_ID + ARIFOS_ACTOR_ID env vars
Policy: sovereign (HMAC_VERIFIED)
Route: Internal → arifOS:8088/mcp
```

### AG-002 — A-FORGE
```
Init: identity_hash file + auto-bootstrap
Policy: operator
Route: Internal → arifOS:8088/mcp
Command: /forge → dry-run first, then arif_forge_execute if approved
```

### AG-003 — Hermes ASI (Telegram)
```
Init: HMAC path via @ASI_arifos_bot
Policy: sovereign
Command: /init (Telegram) → arif_session_init via Hermes A2A bridge
```

### AG-004 — OpenClaw (Telegram)
```
Init: HMAC path via @AGI_ASI_bot
Policy: sovereign
Command: /init → arif_session_init via OpenClaw gateway
```

---

## Quick Reference Matrix

```
/init command per agent:

FI-001 OpenCode:   /init → swarm_ignite + engineer   → full forge
FI-002 Claude Code: /init → swarm_ignite + engineer   → full forge  
FI-003 Qwen (QWA):  /init → bash bridge + analyst     → observe+reason
FI-004 Gemini:      /init → swarm_ignite + analyst    → observe+reason
FI-005 Codex:       /init → observer only             → observe (audit pending)
FI-006 Copilot:     /init → init + analyst            → observe+reason+draft
FI-007 Aider:       N/A                               → not installed

AG-001 AAA:         auto-bootstrap                    → sovereign
AG-002 A-FORGE:     auto-bootstrap                    → operator
AG-003 Hermes:      Telegram /init                    → sovereign
AG-004 OpenClaw:    Telegram /init                    → sovereign
```

---

## The Universal Init Command

Every agent that supports MCP can use this ONE command:

```
MCP: arifOS::arif_session_init
Args: {"mode": "swarm_ignite", "actor_id": "<agent>", "agent_policy": {"preset": "<role>"}}
```

Roles:
- `observer` → 3 tools, OBSERVE only
- `analyst` → 7 tools, observe + reason + draft
- `engineer` → 13 tools, can dry-run/mutate
- `operator` → 12 tools, production-grade
- `sovereign` → all tools, F13-gated

**One command. One endpoint. One contract. Every agent.**
