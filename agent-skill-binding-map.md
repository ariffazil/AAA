# Agent → Skill Binding Map

> Generated 2026-07-13. Sources: 22 agent-card.json files across `/root/AAA/agents/`, `/root/AAA/agents/_lanes/`, `/root/AAA/agents/_external/`, and `/root/AAA/.well-known/`.

## Summary

| Category | Count | Agents |
|----------|-------|--------|
| Warga (in `agents/`) | 6 | arifOS_bot, opencode, openclaw, hermes-asi, prospect-maturation, makcikgpt |
| Lanes: HEXAGON (in `_lanes/`) | 5 active + 1 archived | 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE, (777-forge RETIRED) |
| External: Forge Instruments (in `_external/`) | 9 | claude-code, codex, continue-cli, gemini-cli, grok-build, kimi-code, qwen-code, copilot, aider |
| .well-known | 1 | arifOS_bot (duplicate of `agents/main/`) |
| **Total unique** | **21** | |

---

## Agent Overview with Custom Fields

### WARGA (primary agents)

| Agent ID | Path | Class | Bound To | Power Band | Tier | FI Slot |
|----------|------|-------|----------|------------|------|---------|
| arifOS_bot | agents/main/ | — | — | — | — | — |
| opencode | agents/opencode/ | AGI | **333-AGI** | Δ MIND | FI | FI-001 |
| openclaw | agents/openclaw/ | — | — | — | — | — |
| hermes-asi | agents/hermes-asi/ | **ASI-Peripheral** | **555-ASI** | conversation_media_routing | — | — |
| PROSPECT-MATURATION | agents/prospect-maturation/ | C2 explorer | — | — | — | — |
| makcikgpt | agents/makcikgpt/ | investigative | **WEALTH** | — | AGI | — |

### LANES: HEXAGON constitutional organs

| Agent ID | Path | Status | Class | Trinity | Requires Jitu |
|----------|------|--------|-------|---------|---------------|
| 333-AGI | agents/_lanes/333-AGI/ | active | architect | Δ MIND | No |
| 555-ASI | agents/_lanes/555-ASI/ | active | architect | Ω HEART | No |
| 888-APEX | agents/_lanes/888-APEX/ | active | architect | ΦΙ JUDGE | **Yes** |
| A-AUDIT | agents/_lanes/A-AUDIT/ | active | watchdog | observer | **Yes** |
| A-ARCHIVE | agents/_lanes/A-ARCHIVE/ | active | archivist | vault | No |
| 777-forge | agents/_lanes/777-forge/ | **RETIRED/ARCHIVED** | AGI | Δ MIND (spawn instrument) | No |

### EXTERNAL: Forge instruments

| Agent ID | Path | Class | Model | FI Slot |
|----------|------|-------|-------|---------|
| claude-code | agents/_external/claude-code/ | CODING/FI | claude-sonnet-4 / claude-opus-4 | FI-002 |
| qwen-code | agents/_external/qwen-code/ | CODING/FI | qwen / MiniMax-M3 bridge | FI-003 |
| codex | agents/_external/codex/ | CODING/FI | gpt-5-codex / o3 | FI-005 |
| copilot | agents/_external/copilot/ | CODING/FI | gpt-5 / claude-sonnet-4 | FI-006 |
| aider | agents/_external/aider/ | CODING/FI | claude-sonnet-4 / gpt-5 | FI-007 |
| kimi-code | agents/_external/kimi-code/ | CODING/FI | kimi-k2 / kimi-for-coding | FI-008 |
| gemini-cli | agents/_external/gemini-cli/ | CODING/FI | gemini-3.5-pro / gemini-3.5-flash | FI-009 |
| grok-build | agents/_external/grok-build/ | HARNESS | grok-4.3 | FI-010 |
| continue-cli | agents/_external/continue-cli/ | CODING/FI | provider-agnostic | FI-011 |

---

## Skill-to-Agent Binding Matrix

### Governance / Constitutional Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **070-lock-humility-godel** | opencode, 555-ASI, 888-APEX, A-ARCHIVE, claude-code, codex, continue-cli, gemini-cli, copilot, aider, kimi-code, qwen-code |
| **APEX-constitutional-boot** / **constitutional-boot** | arifOS_bot (both variants) |
| **APEX-kernel-bridge** / **arifos-kernel-bridge** | arifOS_bot (both variants) |
| **APEX-sovereign-veto** / **sovereign-veto-respect** | arifOS_bot (both variants) |
| **arifos-arconstitutional-audit** | opencode, 888-APEX, A-AUDIT, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| **constitutional-arbitration** | 888-APEX |
| **constitutional-kernel-patch** | 888-APEX, A-ARCHIVE |
| **floor-compliance-check** | A-AUDIT |
| **kernel-observation-self-test** | 888-APEX |
| **arifos-paradox-engine** | 333-AGI, 555-ASI |

### Execution / Forge Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **FORGE-federation-routing** / **federation-routing** | arifOS_bot (both variants) |
| **FORGE-agentic-builder** | opencode, kimi-code |
| **FORGE-agent-dispatch** | openclaw |
| **FORGE-agent-handoff** | openclaw |
| **FORGE-browser-automation** | openclaw |
| **FORGE-federation-ops** | openclaw |
| **FORGE-gateway-routing** | openclaw |
| **FORGE-github-ops** | grok-build |
| **FORGE-github-workflow** / **github-workflow** | claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| **FORGE-image-video** | grok-build |
| **FORGE-implement-loop** | grok-build |
| **FORGE-mcp-boot-diagnosis** | openclaw |
| **FORGE-mcp-smoke-test** | A-AUDIT |
| **FORGE-openclaw-doctor** | openclaw |
| **FORGE-shell-execution** | openclaw |
| **FORGE-status-query** | openclaw |
| **FORGE-subagent-spawn** | grok-build |
| **FORGE-webmcp-site-builder** | kimi-code |
| **FORGE-federation-coding-agent** | opencode |
| **autonomous-governed-execution** | opencode, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| **AUDIT-clean-audit-immune** | opencode |

### Reasoning / AGI Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **role-binding-delta** | 333-AGI |
| **evidence-reasoning** | 333-AGI |
| **hypothesis-generation** | 333-AGI |
| **task-decomposition** | 333-AGI |
| **sequential-thinking-hermes** | 333-AGI |
| **AGI-plan-mode** | grok-build |
| **AGI-workflow-dag** | grok-build |
| **AGI-kanban-playbook** | openclaw |
| **APEX-mcp-federation** | opencode, 333-AGI, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| **fff-loop-protocol** | 333-AGI, 888-APEX, A-AUDIT, A-ARCHIVE, grok-build |

### Ethical / ASI Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **role-binding-omega** | 555-ASI |
| **ASI-ethical-critique** | 555-ASI |
| **ASI-deep-memory-synthesis** | 555-ASI |
| **ASI-anti-beautiful-one** | 555-ASI |
| **ASI-substrate-validation** | 555-ASI |
| **HERMES-human-model** | 555-ASI |
| **ASI-sovereignty-entropy-guard** | 555-ASI |
| **ASI-scar-forge** | 555-ASI |
| **ASI-aaa-zen** | opencode |
| **ASI-memory-session-bind** | opencode |
| **ASI-federated-memory-query** | arifOS_bot |
| **role-binding-phi** | 888-APEX |
| **ASI-web-research** | openclaw |
| **ASI-memory-search** | openclaw |

### Archival / Memory Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **ARCHIVE-vault-seal** / **vault-seal** | arifOS_bot (both variants) |
| **seal-write** | A-ARCHIVE |
| **seal-read** | A-ARCHIVE |
| **integrity-proof** | A-ARCHIVE |
| **tiered-memory** | 555-ASI, A-ARCHIVE |
| **dream-engine** | A-ARCHIVE |
| **AUDIT-clean-audit-immune** | opencode |

### Audit / Oversight Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **inter-agent-consistency** | A-AUDIT |
| **behavioral-health** | A-AUDIT |
| **claim-heavy-essay-audit** | A-AUDIT |
| **orthodoxy-auditor** | A-AUDIT |
| **repository-hygiene-audit** | A-AUDIT |
| **KERNEL-symbolic-trust** | A-AUDIT |
| **KERNEL-symbolic-bias** | A-AUDIT |

### Trinity / Verdict Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **trinity-witness** | 888-APEX |
| **hold-protocol** | 888-APEX |
| **judge.deliberate** | arifOS_bot (.well-known variant) |
| **lease.issue** | arifOS_bot (.well-known variant) |
| **session.identity** | arifOS_bot (.well-known variant) |
| **agent.discover** | arifOS_bot (.well-known variant) |

### Gateway / Role Binding Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **role-binding-gateway** | openclaw |
| **role-binding-fi-consumer** | claude-code |
| **role-binding-phi** | 888-APEX |

### Agentic Architecture / Design Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **agentic-architecture** | opencode, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| **ASI-agentic-architecture** | claude-code, codex |
| **fabrication-prevention** | opencode, continue-cli, gemini-cli, copilot, aider, kimi-code, qwen-code |
| **ASI-fabrication-prevention** | claude-code, codex |
| **APEX-constitutional-audit** | claude-code, codex |
| **APEX-humility-godel** | claude-code, codex |
| **APEX-godel-humility** | grok-build |

### Geoscience / Prospect Skills

| Skill ID | Agents Binding This Skill |
|----------|--------------------------|
| **geological-artifact-rigor** | PROSPECT-MATURATION |
| **geox-epistemic-ladder** | PROSPECT-MATURATION |
| **geox-contradiction-engine** | PROSPECT-MATURATION |
| **geox-petrophysics-bounds** | PROSPECT-MATURATION |
| **wealth-capital-reasoning** | PROSPECT-MATURATION |

### Hermes-specific (prefix-based)

| Skill Prefix | Agent |
|-------------|-------|
| **HERMES-** (skills_prefix) | hermes-asi (power_band: conversation_media_routing) |

Agents with **empty skills arrays**: makcikgpt (`skills: []`), hermes-asi (prefix-based only), 777-forge (RETIRED).

---

## Most-Widely-Bound Skills (Impact of Archiving)

| Skill ID | # of Agents | Agents Affected |
|----------|------------|-----------------|
| APEX-mcp-federation | 9 | opencode, 333-AGI, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| arifos-arconstitutional-audit | 8 | opencode, 888-APEX, A-AUDIT, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| autonomous-governed-execution | 7+ | opencode, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| 070-lock-humility-godel | 7+ | opencode, 555-ASI, 888-APEX, A-ARCHIVE, claude-code, codex, continue-cli, gemini-cli, copilot, aider, kimi-code, qwen-code |
| agentic-architecture / ASI-agentic-architecture | 7+ | opencode, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| fabrication-prevention / ASI-fabrication-prevention | 7+ | opencode, claude-code, codex, continue-cli, gemini-cli, copilot, aider, kimi-code, qwen-code |
| github-workflow / FORGE-github-workflow | 7+ | opencode, claude-code, codex, continue-cli, gemini-cli, grok-build, copilot, aider, kimi-code, qwen-code |
| fff-loop-protocol | 4 | 333-AGI, 888-APEX, A-AUDIT, A-ARCHIVE, grok-build |
| hermes-opencode-protocol | 5 | opencode, continue-cli, gemini-cli, copilot, aider, kimi-code, qwen-code |
