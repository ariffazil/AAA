# af-forge CLI Federation Binding

> **Scope:** observed coding CLIs and toolbenches on `/root` VPS `af-forge`
> **Purpose:** bind every real local harness to AAA with clear A2A identity, MCP posture, and authority boundary
> **Verified:** 2026-06-26 UTC

This file is the operator-facing map of the coding surface on `af-forge`.
It is not new doctrine. It is the live binding layer between installed CLIs/toolbenches and the AAA control plane.
If this file disagrees with constitutional canon, the canon wins.

## Binding Rule

Every coding harness on `af-forge` must answer four questions:

1. **Who are you in AAA?** Agent/citizen ID + agent card.
2. **How do you speak?** A2A endpoint/card location.
3. **How do you touch tools?** Native MCP, MCP-ready, or bridge-only.
4. **What are you allowed to do?** T1/T2/T3 under F1-F13.

## CLI Citizens

| Citizen | Observed binary | AAA card surface | A2A surface | MCP posture | Notes |
|---|---|---|---|---|---|
| `opencode` | `/root/.npm-global/bin/opencode` | `/root/AAA/agents/opencode/agent-card.json` | `/root/AAA/a2a-server/agent-cards/opencode.json` | Native | Primary local forge worker |
| `claude-code` | `/root/.local/bin/claude` | `/root/AAA/agents/_external/claude-code/agent-card.json` | `/root/AAA/a2a-server/agent-cards/claude-code.json` | Native | First-class FI citizen |
| `codex` | `/root/.npm-global/bin/codex` | `/root/AAA/agents/_external/codex/agent-card.json` | `/root/AAA/a2a-server/agent-cards/codex.json` | Native/ready | OpenAI CLI bound to AAA |
| `kimi-code` | `/root/.kimi-code/bin/kimi` | `/root/AAA/agents/_external/kimi-code/agent-card.json` | `/root/AAA/a2a-server/agent-cards/kimi-code.json` | Native | Moonshot FI citizen |
| `qwen-code` | `/root/.npm-global/bin/qwen` | `/root/AAA/agents/_external/qwen-code/agent-card.json` | `/root/AAA/a2a-server/agent-cards/qwen-code.json` | Bridge | Bounded observe/reason/draft citizen |
| `gemini-cli` | `/usr/bin/gemini` | `/root/AAA/agents/_external/gemini-cli/agent-card.json` | `/root/AAA/a2a-server/agent-cards/gemini-cli.json` | Native | Google FI citizen |
| `copilot` | `/usr/bin/copilot` | `/root/AAA/agents/_external/copilot/agent-card.json` | `/root/AAA/a2a-server/agent-cards/copilot.json` | Native | IDE/CLI FI citizen |
| `continue-cli` | `/usr/bin/cn` -> `/root/.npm-global/bin/cn` | `/root/AAA/agents/_external/continue-cli/agent-card.json` | `/root/AAA/a2a-server/agent-cards/continue-cli.json` | Native | Open-source FI citizen; config at `/root/.continue/config.yaml` |
| `grok-build` | `/root/.grok/bin/grok` | `/root/AAA/agents/_external/grok-build/agent-card.json` | `/root/AAA/a2a-server/agent-cards/grok-build.json` | Native + toolbench | Highest-power harness on box |

## Toolbench / Harness Citizens

| Citizen | Role | Surface | Why it matters |
|---|---|---|---|
| `grok-build` | high-power build harness | CLI + rich toolbench object in registry | parallel agents, plan/search/build FSM, heavy MCP surface |
| `openclaw` | live gateway | `/root/AAA/agents/openclaw/agent-card.json` + `a2a-server/agent-cards/openclaw.json` | hosts multi-agent execution and routing |
| `777-forge` | witness spawn anchor | `/root/AAA/agents/777-forge/IDENTITY.md` + `a2a-server/agent-cards/777-forge.json` | proves session spawn reality with PID receipts |

## Alignment Contract

- **A2A identity:** every citizen needs a discoverable card or mirror in `AAA/a2a-server/agent-cards/`.
- **MCP alignment:** preferred path is native MCP; acceptable fallback is bridge mode through A-FORGE/arifOS until native support exists.
- **Authority alignment:** all citizens inherit T1/T2/T3 bands and cannot self-issue verdicts.
- **Audit alignment:** consequential actions route toward A-FORGE and VAULT999, not direct self-authorization.

## Current Status

- `qwen-code` was previously half-bound: forge card existed, top-level AAA citizen did not. This file and its companion card close that gap.
- `777-forge` existed in A2A but was absent from the machine registry. That gap is now closed at registry level.
- Several FI cards had stale binary paths. Those paths are normalized to observed VPS reality in the current repo state.
- `continue-cli` was normalized via Continue's official Linux installer path and now resolves to observed local version `1.5.47`.
- `aider` remains declared in AAA but is not currently installed on `af-forge`. It is a spec citizen, not an observed active harness.

## Sovereign Read

Short version:

AAA now has one clean sentence for the coding surface on `af-forge`:

> every real CLI and every real toolbench is either a first-class AAA citizen with A2A identity and MCP wiring, or it is explicitly marked bridge-mode or spec-only.
