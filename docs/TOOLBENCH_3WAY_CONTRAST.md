# 🔬 AAA Toolbench — 3-Way Agent Contrast
> **Zen-pass:** 2026-07-18 · **Authority:** F13 SOVEREIGN
> **Canonical registry:** `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml`

---

## §1 · IDENTITY MATRIX

| | **Kimi-Code** | **OpenCode** | **Claude Code** |
|---|---|---|---|
| **FI Slot** | FI-008 | (warga, no FI) | FI-002 |
| **Role** | `forge_instrument` | `warga` | `forge_instrument` |
| **Class** | `CODING/FI` | `AGI` | `CODING/FI` |
| **Trinity** | None (tool) | 333-AGI (Δ MIND) | None (tool) |
| **Binary** | `/root/.kimi-code/bin/kimi` | `/root/.npm-global/bin/opencode` | `/root/.local/bin/claude` |
| **Config** | `/root/.kimi-code/config.toml` | `/root/.config/opencode/opencode.json` | `/root/.claude/settings.json` |
| **Agent card** | v2.0.0 | v3.1.0 | v2.0.0 |
| **Version frozen** | 0.26.0 | latest (auto-update) | latest (auto-update) |

---

## §2 · MODEL SURFACE

| | **Kimi-Code** | **OpenCode** | **Claude Code** |
|---|---|---|---|
| **Default model** | MiniMax-M3 (Anthropic protocol) | DeepSeek V4 Pro | DeepSeek V4 Pro (Anthropic protocol) |
| **Small/fast** | ❌ | DeepSeek V4 Flash (free) | DeepSeek V4 Flash |
| **K3 access** | ✅ Native OAuth (`--model kimi-code/k3`) | ❌ (Bailian K2.7 only) | ❌ |
| **MiMo** | ❌ | ✅ Token Plan + Platform | ✅ via env |
| **Qwen** | ❌ | ✅ 4 variants | ✅ via env |
| **Ollama local** | ❌ | ✅ recovery fallback | ❌ |
| **OpenRouter** | ❌ | ✅ | ❌ |
| **Total providers** | **2** | **11** | **3** (DeepSeek, MiMo, Qwen via env) |
| **Protocol** | Anthropic only | OpenAI-compatible | Anthropic only |

---

## §3 · TOOL SURFACE

| | **Kimi-Code** | **OpenCode** | **Claude Code** |
|---|---|---|---|
| **MCP federation** | 12 servers | 5 declared (runtime discovery) | 9 launchers |
| **arifOS** | ✅ stdio | ✅ | ✅ |
| **A-FORGE** | ✅ stdio | ✅ | ✅ |
| **GEOX** | ✅ HTTP | ✅ | ✅ |
| **WEALTH** | ✅ HTTP | ✅ | ✅ |
| **WELL** | ✅ HTTP | ✅ | ✅ |
| **Minimax** | ✅ code + multimodal | — | — |
| **GitHub** | ✅ official | — | ✅ official + classic |
| **Brave Search** | ✅ | — | — |
| **Serena (LSP)** | ✅ | ✅ (built-in) | ✅ |
| **Repomapper** | ✅ | — | ✅ |
| **Capability Index** | ✅ | — | — |
| **Playwright** | ❌ | — | ✅ |
| **Postgres** | ❌ | — | ✅ |
| **Built-in tools** | ❌ | ✅ web_search, code_interpreter, web_extractor, image_search | ❌ |
| **LSP native** | ❌ | ✅ | ❌ (via serena) |
| **Formatter** | ❌ | ✅ | ❌ |

---

## §4 · GOVERNANCE

| | **Kimi-Code** | **OpenCode** | **Claude Code** |
|---|---|---|---|
| **Permission mode** | `yolo` + 11 ask rules | Built-in approval | Allow-all |
| **Permission rules** | **11** (forge/arifos/github gates) | 0 in config | 0 (Bash/Edit/Write/Read all allowed) |
| **Hooks** | **12** bash (PreToolUse×5, PostToolUse×2, Stop×2, Notify, SessionStart) | 8 Python (via bot) | 0 |
| **Sub-agents** | 2 (explore, plan) | **5** with model rotation | 2 (explore, plan) + fork |
| **Sub-agent rotation** | ❌ One model for all | ✅ forge→GLM, auditor→DS, ops→M2.5, planner→K2.7, explore→Qwen | ❌ All use DS Flash |
| **Effort level** | Thinking=ON | — | max |
| **Custom commands** | ❌ | ❌ | 4 (health, organ, text-to-image, vault) |

---

## §5 · SKILL SURFACE

| | **Kimi-Code** | **OpenCode** | **Claude Code** |
|---|---|---|---|
| **Agent card skills** | 14 | 17 | 13 |
| **Shared core** | HERMES-opencode-protocol, ASI-agentic-architecture, ASI-fabrication-prevention, ASI-autonomous-execution, APEX-constitutional-audit, APEX-humility-godel, FORGE-github-workflow, APEX-mcp-federation, KERNEL-reality, KERNEL-sovereign, KERNEL-session, RSI-recursive-improvement | ← same 12 + 5 unique | ← same 12 + role-binding-fi-consumer |
| **Kimi unique** | FORGE-agentic-builder, FORGE-webmcp-site-builder | FORGE-federation-coding-agent, AUDIT-clean-audit-immune, ASI-memory-session-bind, ASI-aaa-zen, FORGE-agentic-builder | role-binding-fi-consumer |
| **Kimi-local skills** | kimi-architect-* ×6, kimi-skill-reflector, KIMI_RSI_INIT, KIMI_HANDOVER | — | — |
| **Skill dirs** | AAA/skills + .arifos/agents/kimi/skills | AAA/skills only | AAA/skills only |

---

## §6 · A2A MESH

| | **Kimi-Code** | **OpenCode** | **Claude Code** |
|---|---|---|---|
| **A2A endpoint** | `aaa.arif-fazil.com/a2a/kimi-code` | `aaa.arif-fazil.com/a2a/opencode` | `aaa.arif-fazil.com/a2a/claude-code` |
| **ACP bridge** | ✅ `kimi acp` (OpenClaw) | ❌ | ✅ `claude acp` |
| **Topological role** | Generator | Generator | Generator |
| **MCP binding** | A-FORGE :7072 | A-FORGE :7072 | A-FORGE :7072 |

---

## §7 · ZEN DIFF — What Each Is Best At

| Agent | Sweet Spot | Why |
|---|---|---|
| **Kimi-Code** | **Focused forge runs** — single-model, deep hooks, explicit gates. Kimi-native access. | 12 MCPs, 12 hooks, 11 permission rules. Most governed. Direct K3 OAuth. |
| **OpenCode** | **Versatile AGI workhorse** — 11 providers, subagent rotation, built-in tools, LSP. | Provider diversity = resilience. 5 specialized sub-models. Best for heterogeneous workloads. |
| **Claude Code** | **DeepSeek-on-Anthropic bridge** — Anthropic protocol UX with DeepSeek models. | Fork subagents, custom commands, Playwright+Postgres MCPs. Best for backend/infra work. |

---

## §8 · GAPS & ALIGNMENT DEBT

| Gap | Severity | Fix |
|---|---|---|
| **Claude MCP launchers stale** — `minimax.sh.old`, `github.sh` (duplicate of github-official.sh) | LOW | Clean dead launchers |
| **Claude 0 permission rules** — Allow-all is risky for FI instrument | MEDIUM | Add ask rules for forge/arifos/github mutations |
| **Kimi no small model** — Every call burns M3 credits | MEDIUM | Add MiniMax-M2.7-highspeed as small model |
| **OpenCode no Kimi K3** — Only K2.7 via Bailian | LOW | Add OpenRouter provider with moonshotai/kimi-k3 |
| **Claude agent card model stale** — Says "claude-sonnet-4 / claude-opus-4" but actually uses DeepSeek V4 Pro | MEDIUM | Update to "deepseek-v4-pro (via Anthropic protocol)" |
| **OpenCode MCP surface incomplete** — 5 declared in card but 0 in config | LOW | Auto-discovery is fine, but card should reflect actual surface |
| **All three share 12 kernel skills** — Good. No fragmentation. | ✅ | Maintain. |

---

## §9 · TOOLBENCH LANES

```
                    ┌──────────────────────────────┐
                    │     AAA TOOLBENCH (3 FI)      │
                    └──────────────────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
     ┌─────▼─────┐          ┌──────▼──────┐          ┌──────▼──────┐
     │ KIMI-CODE │          │  OPENCODE   │          │ CLAUDE CODE │
     │  FI-008   │          │   (warga)   │          │   FI-002    │
     │           │          │             │          │             │
     │ Focused   │          │ Versatile   │          │ Infra       │
     │ Forge     │          │ AGI Worker  │          │ Deep-Dive   │
     │           │          │             │          │             │
     │ 1 model   │          │ 11 models   │          │ 3 models    │
     │ 12 MCPs   │          │ 5+ MCPs     │          │ 9 MCPs      │
     │ 12 hooks  │          │ 8 hooks     │          │ 0 hooks     │
     │ 11 gates  │          │ 0 gates     │          │ 0 gates     │
     └─────┬─────┘          └──────┬──────┘          └──────┬──────┘
           │                       │                        │
           └───────────────────────┼────────────────────────┘
                                   │
                          ┌────────▼────────┐
                          │   SHARED CORE   │
                          │  12 KERNEL      │
                          │  SKILLS         │
                          │  F1-F13 LAW     │
                          │  A2A MESH       │
                          └─────────────────┘
```

---

*DITEMPA BUKAN DIBERI — Forged 2026-07-18. Zen-aligned to FEDERATED_SKILLS_REGISTRY_V3.*
