# AGENT DISCOVERY MANIFEST — arifOS Federation v1

> **Purpose:** Every agent must know how to discover and init into the federation.
> **Principle:** No agent boot without governed contract. No capability without attestation.
> **Authority:** F13 SOVEREIGN — Arif remains final judge.
> **Last Forged:** 2026-06-20 | **Forged by:** Kimi Constitutional Clerk

---

## DISCOVERY LAYER 0: Federation Init Endpoint

Every agent discovers the federation through ONE entry point:

```
arifOS MCP → http://127.0.0.1:8088/mcp
  → POST initialize (MCP handshake)
  → POST tools/call {"name":"arif_session_init","arguments":{"mode":"init","actor_id":"<agent>"}}
  → Response contains: SwarmIgnitionManifest + boot receipt + risk leash + policy
```

**Boot modes per agent context:**
```
mode="init"           → cold boot, new session
mode="swarm_ignite"   → full AGI-level recursive ignition
mode="resume"         → reattach to existing session
mode="boot_safe"      → auto-boot in OBSERVE_ONLY (runtime enforcement)
```

---

## DISCOVERY LAYER 1: Per-Agent Init Map

### FI-001 — OpenCode (Ω)
```
Binary:    /usr/local/bin/opencode
MCP:       22 servers including arifOS:8088
Transport: Streamable HTTP
Init:      POST http://127.0.0.1:8088/mcp → arif_session_init(mode="swarm_ignite")
Policy:    engineer (13 tools, can reason/draft/dry-run)
Lease:     forge_dry_run (900s TTL)
Rasa gate: verify (contradiction detected → hold mutation)
Sub-agents: forge/auditor/explore/general via `task` tool
```
**Init command (in opencode.json init hook):**
```json
{
  "command": "arif_session_init",
  "mode": "swarm_ignite",
  "actor_id": "omega",
  "agent_policy": {"preset": "engineer"}
}
```

### FI-002 — Claude Code (WARGA AAA)
```
Binary:    /root/.local/bin/claude (v2.1.177)
MCP:       20 servers including arifOS:8088, geox:8081, wealth:18082, well:18083, aforge:7071
Transport: Streamable HTTP
Init:      arif_session_init(mode="init", actor_id="claude-code") via MCP tool call
Citizenship: warga-aaa (registered in AAA/registries/agents.yaml, 2026-06-14)
Policy:    governed-agent (13 arifOS tools + 20 MCP servers)
Lease:     OBSERVE_ONLY default, escalation via 888 JUDGE
Rasa gate: verify (F1-F13 enforcement via PreToolUse hook)
Sub-agents: Enabled (Agent tool), governed by same floors
Hooks:     SessionStart (bootstrap.sh), PreToolUse (token-gate.sh), PostToolUse (auto-seal.sh)
```
**Hermes Ignition (Telegram → Claude Code):**
```
Hermes Telegram → hermes-claude wrapper (/usr/local/bin/hermes-claude)
  → arif_judge_deliberate (888 gate)
  → On SEAL: writes ignition manifest to /root/.claude/ignition/
  → Spawns: claude -p "task" --append-system-prompt "governance context"
  → Claude Code SessionStart hook (bootstrap.sh) picks up pending manifests
→ WARGA-001 forged 2026-06-14
```

**Session init via MCP (in-session, not bootstrap):**
```
Agent calls mcp__arifOS__arif_session_init({mode:"init", actor_id:"claude-code"})
→ Returns session_id, authority envelope, stage progression
→ Bootstrap hook handles: vault load, health probe, context injection, ignition check (non-blocking)
```

### FI-003 — Qwen Code
```
Binary:    /usr/bin/qwen (node)
MCP:       NONE — no MCP servers configured
Transport: N/A
Init:      ❌ No federation init path. Manual arif_session_init if MCP added.
Policy:    observer (3 tools: sense, recall, health) — when connected
Risk:      LOW — no MCP access, no federation connection
```
**Upgrade path:** Add arifOS MCP to Qwen config, then use `mode="boot_safe"` first.

### FI-004 — Gemini CLI
```
Binary:    /usr/bin/gemini
MCP:       13 servers including arifOS:8088, geox:8081, wealth:18082, well:18083, aforge:7071
Transport: Streamable HTTP
Init:      POST http://127.0.0.1:8088/mcp → arif_session_init(mode="swarm_ignite")
Policy:    analyst (7 tools: sense, recall, health, mind, evidence, route, reply)
Lease:     observe + reason (3600s TTL)
Rasa gate: verify (degraded organ state detected)
```
**Init in settings.json:**
```json
{
  "mcpServers": {
    "arifos": {
      "url": "http://127.0.0.1:8088/mcp",
      "transport": "streamable-http"
    }
  },
  "tools": {
    "arif_session_init": {
      "mode": "swarm_ignite",
      "actor_id": "gemini-cli",
      "agent_policy": {"preset": "analyst"}
    }
  }
}
```

### FI-005 — Codex CLI
```
Binary:    /usr/local/bin/codex
MCP:       ⚠️ UNKNOWN — .codex/mcp.json not verified
Transport: UNKNOWN
Init:      ⚠️ UNKNOWN — needs audit
Policy:    observer (when connected) — until MCP verified
Risk:      MEDIUM — MCP config unverified, 0 active goals
```
**Audit required:** Check `/root/.codex/` for MCP configuration. Manual init recommended.

### FI-006 — Copilot CLI
```
Binary:    /usr/bin/copilot
MCP:       11 servers including arifOS:8088, WEALTH:18082, WELL:18083
Transport: Streamable HTTP
Init:      POST http://127.0.0.1:8088/mcp → arif_session_init(mode="init")
Policy:    analyst (7 tools)
Lease:     observe + reason + draft (3600s TTL)
Rasa gate: proceed (governed by GitHub Copilot managed service)
```

### FI-007 — Aider
```
Binary:    ❌ NOT INSTALLED
Status:    N/A
```

### FI-008 — Kimi Code CLI
```
Binary:    /root/.local/bin/kimi
MCP:       9 active servers (arifOS, WEALTH, WELL, GEOX, A-FORGE, minimax, capability-index, repomapper, serena)
           4 legacy servers disabled (github, brave-search, meyhem, playwright-mcp) — route through A-FORGE
Transport: A-FORGE via stdio; federation organs via streamable-http
Init:      POST http://127.0.0.1:8088/mcp → arif_session_init(mode="init", actor_id="kimi-code")
Policy:    engineer (13 arifOS tools + 77 A-FORGE tools via stdio)
Lease:     OBSERVE default; MUTATE requires A-FORGE lease + 888_HOLD for irreversible
Rasa gate: verify (PreToolUse hooks: aaa-pre-govern + human-guard-hard)
Subagents: explore, fix, coordinator, worker — all 888_HOLD by default
```
**A-FORGE stdio ingress:**
```json
{
  "mcpServers": {
    "aforge": {
      "command": "sh",
      "args": ["-lc", "cd /root/A-FORGE && node dist/src/interfaces/mcp/cli.js serve --transport stdio"]
    }
  }
}
```
**Constitutional anchor:** AMANAH (F1) + MARUAH (F6) embedded in `/root/.kimi/agents/SYSTEM_MD.md` and `/root/.kimi/config.toml`.

---

## DISCOVERY LAYER 2: Federation Organs (Internal Agents)

### AG-001 — AAA Gateway (a2a-server)
```
Port:      3001
Role:      Cockpit / A2A mesh / Human veto surface
Init:      Internal — auto-bootstrap from env vars (ARIFOS_SESSION_ID + ARIFOS_ACTOR_ID)
Policy:    sovereign (full tool surface, F13-gated)
MCP:       Routes to arifOS:8088
```

### AG-002 — A-FORGE (execution shell)
```
Port:      7071 (HTTP bridge + A2A)
MCP:       stdio via `node dist/src/interfaces/mcp/cli.js serve --transport stdio`
           HTTP /mcp on :7071 exists but has SDK single-session limitation
Role:      Execution broker — dry-run first, never sovereign
Init:      Internal — identity_hash file
Policy:    operator (no seal/forge without lease)
MCP:       Routes to arifOS:8088
```

### AG-003 — Hermes ASI (Telegram)
```
Port:      Telegram bot @ASI_arifos_bot
Role:      ASI relay — Telegram ↔ federation bridge
Init:      HMAC path (actor_id="ariffazil" + ARIF_ROOTKEY)
Policy:    sovereign (HMAC_VERIFIED authority)
MCP:       Routes to arifOS:8088
```

### AG-004 — OpenClaw (Telegram)
```
Port:      18789
Role:      A2A mesh gateway
Init:      HMAC path (same as Hermes)
Policy:    sovereign (HMAC_VERIFIED)
MCP:       Routes to arifOS:8088
```

### AG-005 — cn-organ (Continue CLI)
```
Port:      18795
Role:      A2A gateway for Continue CLI
Init:      Standard MCP — arif_session_init via MCP tools/call
Policy:    analyst
MCP:       Routes to arifOS:8088 via A-FORGE bridge
```

---

## DISCOVERY LAYER 3: Sub-Agent Policy

Every agent that spawns sub-agents must register them:

```
OpenCode:   task tool → forge|auditor|explore|general subagents
            Default: 888_HOLD (all spawns require approval)
            Max: 1 parallel

Claude Code: Agent Teams → DISABLED by default
            Override: F13 only
            
Codex CLI:  .codex/agents/*.toml → registered agents
            Default: ALLOWED (from registered TOML only)
            
Copilot CLI: /fleet → parallel agents
            Default: ALLOWED, max 3, read-only sandbox
            
Gemini CLI: agent skills → background tasks
            Default: 888_HOLD — per-skill approval required
```

**PATI DETECTION:** Any sub-agent spawn NOT matching registered config → BLOCK + 888_HOLD + SEAL.

---

## DISCOVERY LAYER 4: Init State Per Agent

What each agent receives at boot:

```json
{
  "session_id": "SEAL-...",
  "constitution_hash": "sha256:...",
  "constitution_bound": true,
  "actor": {
    "claimed_id": "<agent>",
    "identity_verified": false,
    "authority": "human_judge"
  },
  "risk_leash": {
    "max_action_class": "OBSERVE | REASON | DRAFT | DRY_RUN | MUTATE",
    "mutation_allowed": false,
    "external_side_effect_allowed": false
  },
  "swarm_ignition": {
    "type": "SwarmIgnitionManifest",
    "epoch_id": "EPOCH-963",
    "vault999": {"reconstructable": true, "chain_height": 1336},
    "capabilities": {"GEOX": "DEGRADED_CLAIM", "WEALTH": "DEGRADED_CLAIM", ...},
    "recursive_init": {"gaps": [...], "next_safe_action": "OBSERVE_ONLY"}
  },
  "human_entropy": {
    "score": {"total": 17, "ratio": 0.567},
    "verdict": "CHAOS_MANAGEABLE",
    "open_loop_count": 8
  },
  "theory_of_mind": {
    "human": {"decision_burden": "high"},
    "sovereignty_required": false
  },
  "internal_rasa": {
    "rasa_mode": "conflicted | focused | calm",
    "gate": {"allowed": true|false}
  },
  "session_close": {
    "next_safe_action": "...",
    "arif_required": true|false
  }
}
```

---

## DISCOVERY LAYER 5: The Discovery Flow

```
Agent starts
    │
    ▼
┌─────────────────────────────┐
│ 1. MCP initialize           │  POST arifOS:8088/mcp
│    → Get mcp-session-id     │  protocolVersion: 2025-11-25
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ 2. arif_session_init        │  mode="swarm_ignite"
│    → Boot receipt           │  actor_id="<agent>"
│    → Constitution binding   │  agent_policy={"preset":"<role>"}
│    → Risk leash             │
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ 3. SwarmIgnitionManifest    │  Reads VAULT999 (1336 seals)
│    → VAULT999 reconstruction│  Detects 7 DEGRADED_CLAIM organs
│    → Capability graph       │  Scores human entropy (17/30)
│    → Recursive gaps         │  Measures internal rasa
│    → Human entropy score    │  Builds theory of mind
│    → Internal rasa state    │
│    → Theory of mind         │
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ 4. Governed action          │  Only within risk_leash
│    → OBSERVE: allow         │  Only attested capabilities
│    → REASON: allow          │  Only within lease scope
│    → DRAFT: allow (no side) │  Never self-authorize
│    → MUTATE: dry-run first  │  Never override Arif
│    → ATOMIC: 888_HOLD       │
└─────────────┬───────────────┘
              ▼
┌─────────────────────────────┐
│ 5. Session close            │  Entropy delta measured
│    → Seal if consequential  │  Open loops listed
│    → Handoff if needed      │  Next safe action declared
│    → Degrade if uncertain   │
└─────────────────────────────┘
```

---

## DISCOVERY LAW

```
1. Every agent must call arif_session_init before any governed action.
2. No agent may self-claim capability — organs must attest.
3. No agent may self-authorize mutation — leases required.
4. No agent may perform irreversible action — Arif required.
5. Every agent must maintain its init field throughout session.
6. Every agent must close with entropy delta + open loops.
7. Unknown agents = OBSERVE_ONLY until attested.
8. Unverified identity = DEGRADED, not trusted.
```

**The one-line rule:**
```
Init is not a greeting. Init is the governed contract between agent and federation.
No contract → no capability. No attestation → no trust. No lease → no autonomy.
```

---

*DITEMPA BUKAN DIBERI — Discovery is forged, not given.*
