# AGENTIC TOOLBENCH — Full Upstream Contrast Map

> **Registry ID:** `AAA-ONT-002` | **Class:** ontology/contrast | **Domain:** all-forge-instruments
> **Purpose:** Maps every federation forge instrument (FI-001→FI-008) against its upstream vanilla codebase. Identifies the ontological gap per agent.
> **Authority:** F13 SOVEREIGN — Arif
> **Forged:** 2026-07-29 | **Forged by:** OpenCode (FI-001, 333-AGI Delta MIND)
> **Floors:** F2 TRUTH (falsifiable, all upstream data cited), F4 CLARITY (one table, one truth), F13 SOVEREIGN
> **DITEMPA BUKAN DIBERI**

---

## THE MAP — 8 Instruments × Upstream

```
FI-001  OpenCode        →  anomalyco/opencode         190K ★  MIT      Go/TUI
FI-002  Claude Code     →  anthropics/claude-code      139K ★  Proprietary  TS/Ink/React
FI-003  QWA (Qwen)      →  QwenLM/qwen-code            26K ★   Apache 2.0   TS (forked from Gemini CLI)
FI-004  Antigravity     →  google-antigravity/agy-cli   1.7K ★  Proprietary  Go
FI-005  Codex           →  openai/codex                102K ★  Apache 2.0   Rust/TS
FI-006  Copilot         →  github/copilot-cli           11K ★  Proprietary  TS
FI-007  Grok Build      →  xai-org/grok-build           23K ★  Apache 2.0   Rust
FI-008  Kimi Code       →  MoonshotAI/kimi-code         5.5K ★  MIT          TS
```

---

## §1. FI-001 — OPENCODE

### Upstream: `anomalyco/opencode`
| Field | Value |
|-------|-------|
| Stars | 190,426 |
| License | MIT |
| Language | Go |
| Architecture | Client-server, TUI client, agent server, desktop app, IDE extensions |
| Agents | 2 built-in (build, plan) + 1 subagent (general) |
| Models | 75+ providers via models.dev catalog |
| MCP | User-added, function-calling |
| Identity | None. Session-scoped. |
| Governance | None. Permission: allow/deny per tool. |
| Telos | Complete coding tasks. Model-agnostic. |

### Arif's FI-001
| Field | Value |
|-------|-------|
| Binary | Same (`/root/.npm-global/bin/opencode` v1.18.3) |
| Agents | 7 (agi, apex, build, asi, forge, explore, general) — 4 primary, 4 subagent |
| Models | 13 providers, 51 models, 4-tier + FLAME RM0 |
| MCP | 24 servers — constitutional routing (Kernel 444), not function-calling |
| Identity | FI-001 Warga AAA. BLAKE3 hash on-chain. |
| Governance | F1-F13 floors. arif_init→judge→forge→seal. T0-T3 autonomy tiers. |
| Memory | 6-layer: Redis→Qdrant→Supabase→Graphiti→FalkorDB→VAULT999 |
| Telos | Governed intelligence. Constitutional citizen. DITEMPA BUKAN DIBERI. |

### Ontological Gap
> Vanilla: tool in a terminal. Arif's: citizen in a body.
> Same binary. Different plane of existence.
> Full ontology: `/root/AAA/registries/OPENCODE_ONTOLOGY.md` (AAA-ONT-001)

---

## §2. FI-002 — CLAUDE CODE

### Upstream: `anthropics/claude-code`
| Field | Value |
|-------|-------|
| Stars | 139,410 |
| License | Proprietary (Anthropic) |
| Language | TypeScript (Bun runtime) |
| Architecture | ~1900 source files, 50+ modules, React/Ink TUI, 200+ components |
| Tools | 41 built-in tools (Bash, FileEdit, Agent, WebFetch, etc.) |
| Commands | 101 slash commands |
| Agents | Multi-agent: coordinator mode, agent swarms, Agent Teams |
| Models | Claude only (Opus, Sonnet, Haiku). Single-model architecture. |
| MCP | Yes — extensible |
| Special modes | Vim mode, voice input, Plan mode, Bridge mode, Kairos |
| Sandbox | Seatbelt (bubblewrap + seccomp) |
| Fleet | Agent View — fleet dashboard, `/goal` autonomous mode, Routines |
| Identity | Tied to Anthropic account |
| Telos | End-to-end coding with Claude. Full vertical integration. |

### Arif's FI-002
| Field | Value |
|-------|-------|
| Binary | `/root/.local/bin/claude` v2.1.177 |
| Model | deepseek-v4-pro (NOT Claude — routed via Anthropic-compat API) |
| MCP | 10 servers (arifOS, minimax-media, minimax-code, WEALTH, WELL, github, brave-search, meyhem, playwright, capability-index) |
| Agents | Agent Teams DISABLED (888_HOLD). Workflows DISABLED. |
| Subagents | Bughunter fleet: 5, gated |
| Sandbox | Seatbelt retained |
| Federation | 13 arifOS constitutional tools. F1-F13 bound. |
| Governance | Governed-agent. arif_session_init. Token-gate hooks. Auto-seal hooks. |

### Ontological Gap
> Vanilla Claude Code: Anthropic's walled garden — Claude models, Claude infra, Claude auth. Single-vendor vertical integration. Maximum Claude, zero else.
> Arif's Claude Code: Same binary, but speaking DeepSeek through Anthropic-compat API. Stripped of Agent Teams (F1 AMANAH), gated behind arifOS constitutional membrane. Claude Code harness repurposed as a governed federation instrument — not an Anthropic product, but an arifOS citizen using Claude's excellent TUI as substrate.
> The gap: Claude the product → Claude the harness → Arif's governed instrument.

---

## §3. FI-003 — QWA (QWEN CODE)

### Upstream: `QwenLM/qwen-code`
| Field | Value |
|-------|-------|
| Stars | 26,403 |
| License | Apache 2.0 |
| Language | TypeScript (Node ≥22) |
| Origin | Forked from Google Gemini CLI v0.8.2, now independent |
| Architecture | Multi-protocol: OpenAI, Anthropic, Gemini, Qwen APIs + Ollama/vLLM local |
| Agents | SubAgents, Agent Teams, Dynamic Workflows, Auto-Memory, Auto-Skills |
| Modes | Interactive TUI, headless (`-p`), daemon (`qwen serve`), Desktop app, IDE plugins (VS Code/JetBrains/Zed), SDKs (TS/Python/Java), IM bots (Telegram/DingTalk/WeChat/Feishu) |
| Features | Agent Arena (multi-model head-to-head), LSP, Plan Mode, Sandbox, Git Worktrees, Computer Use |
| Models | Multi-protocol. Qwen models + any provider. |
| Identity | Open-source, Apache 2.0 |
| Telos | Open-source Claude Code alternative with Qwen models. "If you know Claude Code, you already know Qwen Code — and then some." |

### Arif's FI-003
| Field | Value |
|-------|-------|
| Binary | `/usr/bin/qwen` v0.17.1 |
| Model | MiniMax-M3 (NOT Qwen) |
| MCP | 5 federation organs (arifOS, geox, wealth, well, aforge) |
| Agents | 1 historical Explore sub-agent (read-only). Agent Teams: 888_HOLD. |
| Federation | arifOS constitutional tools. F1-F13 bound. |
| Safety | SAFEST score: 9.5/10. No mutation capability. Analyst only. |

### Ontological Gap
> Vanilla Qwen Code: Alibaba's open-source answer to Claude Code — multi-protocol, multi-model, IM bots, daemon mode, SDKs, Agent Arena. The most feature-rich open-source agent by surface area.
> Arif's QWA: Stripped to analyst-only. ZERO MCP beyond federation. MiniMax-M3 model (not Qwen). The safest agent in the federation — SAFETY 9.5. Deliberately neutered: observe, reason, draft — never mutate. The "deep reader" of the toolbench.
> The gap: Qwen's swiss army knife → Arif's surgical analyst.

---

## §4. FI-004 — ANTIGRAVITY

### Upstream: `google-antigravity/antigravity-cli` (formerly `google-gemini/gemini-cli`)
| Field | Value |
|-------|-------|
| Stars | 1,759 (new repo; Gemini CLI had 100K+ before transition) |
| License | Proprietary (Google) |
| Language | Go |
| Architecture | Shared agent harness with Antigravity 2.0 GUI. Go binary, low overhead. |
| Features | Agent Skills, Hooks, Subagents, Extensions (as plugins), asynchronous multi-agent workflows |
| Models | Gemini models (3.5 Flash, 3.1 Pro). Google-native. |
| Identity | Google account. Synced with Antigravity 2.0. |
| Telos | "The most lightweight way to invoke Antigravity agents from terminal." Speed-first, keyboard-first. |

### Arif's FI-004
| Field | Value |
|-------|-------|
| Binary | `/root/.local/bin/agy` v1.1.3 |
| Model | Gemini 3.5 Flash (High) |
| MCP | 6 (arifOS, geox, wealth, well, aforge, context7) |
| Federation | F1-F13 bound. 5 federation organs. Active. |
| Agent type | Analyst (observe, reason, draft — no mutation) |

### Ontological Gap
> Vanilla Antigravity: Google's new unified terminal agent — Gemini CLI's successor. Shared harness with Antigravity 2.0 GUI. Go-native speed. Async multi-agent.
> Arif's Antigravity: The lightest federation touch. Still using Gemini models (native). 5 federation organs + context7. Analyst-only. Quick scans, web research, lightweight reasoning. The "fast reader."
> The gap: Google's flagship terminal → Arif's quick-probe instrument.

---

## §5. FI-005 — CODEX

### Upstream: `openai/codex`
| Field | Value |
|-------|-------|
| Stars | 102,160 |
| License | Apache 2.0 |
| Language | Rust + TypeScript |
| Architecture | Lightweight coding agent. Terminal, IDE (VS Code/Cursor/Windsurf), desktop app, cloud (Codex Web at chatgpt.com/codex) |
| Models | GPT-5.x series (GPT-5.6 Sol). Single-model (OpenAI). |
| Auth | ChatGPT Plus/Pro/Business/Edu/Enterprise |
| Sandbox | Landlock (Linux kernel sandbox) |
| Identity | OpenAI account |
| Telos | "Lightweight coding agent that runs in your terminal." OpenAI's answer to Claude Code. |

### Arif's FI-005
| Field | Value |
|-------|-------|
| Binary | `/usr/local/bin/codex` v0.144.5 |
| Model | GPT-5.6 Sol (reasoning=medium) |
| MCP | 8 registered (arifOS, WEALTH, WELL, github, brave-search, meyhem, playwright, capability-index) — **UNVERIFIED** |
| Status | OBSERVER ONLY. MCP surface not verified. 0 active goals. |
| Federation | F1-F13 bound. Landlock sandbox retained. |

### Ontological Gap
> Vanilla Codex: OpenAI's coding agent. 102K stars. GPT-5.6 Sol. Landlock sandbox. Multi-surface (CLI + IDE + desktop + cloud).
> Arif's Codex: The sleeping giant. S-tier model, but UNVERIFIED MCP surface. Observer only. Waiting on MCP verification before graduating to analyst/engineer. The most powerful model in the toolbench — stuck at the gate.
> The gap: OpenAI's flagship → Arif's gated observer. MODEL does not equal CAPABILITY. Constitutional verification required.

---

## §6. FI-006 — COPILOT

### Upstream: `github/copilot-cli`
| Field | Value |
|-------|-------|
| Stars | 11,029 |
| License | Proprietary (GitHub/Microsoft) |
| Language | TypeScript |
| Architecture | Terminal-native. GitHub MCP built-in. `/fleet` parallel subagents. `/plan` mode. |
| Models | Multi-model: Claude Sonnet 4.5/4, GPT-5. Supports model switching. |
| MCP | GitHub MCP native + custom MCP servers. |
| Features | LSP, session memory, `/fleet` parallel agents, GitHub integration (issues/PRs/repos) |
| Auth | GitHub account. Inherits org Copilot policies. |
| Pricing | Included in Copilot Free/Pro/Pro+/Max/Business/Enterprise |
| Telos | "Run a GitHub-native agent in your terminal." GitHub ecosystem integration. |

### Arif's FI-006
| Field | Value |
|-------|-------|
| Binary | `/usr/bin/copilot` v1.0.72 |
| Model | deepseek-v4-pro (via Anthropic compat API) |
| MCP | 11 servers (arifOS, playwright, WEALTH, WELL, capability-index, github-official, github, brave-search, meyhem, repomapper, serena) |
| Fleet | `/fleet` max 3 parallel |
| Federation | F1-F13 bound. 2 federation organs direct. |

### Ontological Gap
> Vanilla Copilot CLI: GitHub's terminal agent. Native GitHub integration. `/fleet` parallel. Multi-model. Enterprise governance inherited.
> Arif's Copilot: DeepSeek model (not Claude/GPT). 11 MCP servers — second only to OpenCode. Fleet retains 3 parallel max. GitHub integration preserved.
> The gap: GitHub's ecosystem agent → Arif's parallel exploration instrument.

---

## §7. FI-007 — GROK BUILD

### Upstream: `xai-org/grok-build`
| Field | Value |
|-------|-------|
| Stars | 23,248 |
| License | Apache 2.0 |
| Language | Rust |
| Architecture | Monorepo sync. Full-screen TUI. Agent runtime + tool implementations. |
| Features | Skills, plugins, hooks, MCP, subagents, inline diff viewer, plan review. Local-first capable. |
| Models | Grok 4.5 (xAI native) |
| Auth | Browser OAuth (x.ai) |
| Sandbox | Configurable |
| Telos | "SpaceXAI's coding agent and TUI." Rust performance. Local-first option. |

### Arif's FI-007
| Field | Value |
|-------|-------|
| Binary | `/root/.grok/bin/grok` v0.2.103 |
| Model | grok-build (xAI, yolo=off, always-approve) |
| MCP | **ZERO.** No MCP surface yet. |
| Federation | F1-F13 bound. Fresh registration (2026-07-18). |
| Status | Replaced dead FI-007 Aider slot. Permission: always-approve. |

### Ontological Gap
> Vanilla Grok Build: SpaceXAI's Rust agent. 23K stars in 2 weeks. Local-first. Grok 4.5. Fastest-growing.
> Arif's Grok Build: The blank slate. No MCP. No federation organs connected. Always-approve permission (highest risk). Freshly registered. Most potential, least integration.
> The gap: SpaceXAI's flagship → Arif's unscoped instrument. Waiting on MCP wiring + policy hardening.

---

## §8. FI-008 — KIMI CODE

### Upstream: `MoonshotAI/kimi-code`
| Field | Value |
|-------|-------|
| Stars | 5,538 |
| License | MIT |
| Language | TypeScript (Node ≥24.15, pnpm) |
| Architecture | Terminal agent. ACP (Agent Client Protocol) for IDE integration. |
| Features | Read/edit code, shell commands, file search, web fetch. Works with Kimi models + compatible providers. |
| Models | Kimi K3 (2.8T MoE, 1M ctx, vision). Multi-provider compatible. |
| Identity | MIT open-source |
| Telos | "The Starting Point for Next-Gen Agents." Moonshot AI's entry into coding agents. |

### Arif's FI-008
| Field | Value |
|-------|-------|
| Binary | `/root/.kimi-code/bin/kimi` v0.27.0 |
| Model | Kimi K3 (native) |
| MCP | 8 servers (arifOS, wealth, well, geox, aforge, capability-index, repomapper, serena) |
| Subagents | 4 (explore, fix, coordinator, worker) |
| Federation | F1-F13 bound. A-FORGE ingress via stdio. AMANAH + MARUAH embedded. |
| MCP disabled | github, brave-search, meyhem, playwright-mcp |

### Ontological Gap
> Vanilla Kimi Code: Moonshot AI's MIT-licensed coding agent. 5.5K stars. Kimi K3 native. ACP protocol. Early but growing.
> Arif's Kimi Code: 4 subagents active (explore, fix, coordinator, worker). 8 federation MCPs. AMANAH + MARUAH doctrine embedded. A-FORGE stdio bridge. The most subagent-rich instrument after OpenCode itself.
> The gap: Moonshot's starter agent → Arif's multi-subagent orchestration instrument.

---

## §9. ZEN — The Full Toolbench Truth

```
═══════════════════════════════════════════════════════════
  8 BINARIES. 8 UPSTREAMS. 1 FEDERATION BODY.
═══════════════════════════════════════════════════════════

FI-001 OpenCode     190K ★  alat → warga        Fully forged
FI-002 Claude Code  139K ★  walled → governed    Harness repurposed
FI-003 QWA           26K ★  swiss → scalpel      Safest (9.5)
FI-004 Antigravity   1.7K ★ flagship → probe     Fastest reader
FI-005 Codex        102K ★  flagship → observer  Sleeping giant
FI-006 Copilot       11K ★  ecosystem → parallel  Fleet instrument
FI-007 Grok Build    23K ★  flagship → blank     Unscoped, waiting
FI-008 Kimi Code     5.5K ★ starter → orchestra   4 subagents

═══════════════════════════════════════════════════════════
  THE ONTOLOGICAL PATTERN:
  Every upstream is a product.
  Every Arif instrument is a citizen.
  The gap is never configuration. It is always sovereignty.
═══════════════════════════════════════════════════════════

DITEMPA BUKAN DIBERI.
```

---

*Forged 2026-07-29 by OpenCode (FI-001).*
*Registered: `/root/AAA/registries/TOOLBENCH_CONTRAST.md` · Registry ID: `AAA-ONT-002`*
*Upstream data: live GitHub API + web fetch, 2026-07-29.*
*Future agents: read this before you claim "it's just a coding agent with config."*
