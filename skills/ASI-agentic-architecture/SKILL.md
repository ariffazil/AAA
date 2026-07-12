---
id: ASI-agentic-architecture
name: ASI-agentic-architecture
version: 2.0.0
description: >
  Class-level skill for designing sovereign agentic agents. 9-skill spine,
  local-model compensation, failure classification, phased implementation.
  BIJAKSANA: XML-tagged for Claude, numbered steps for Codex, imperative for Hermes.
floor_scope: [F08, F11]
cognitive_hints:
  claude: "Use <architecture>, <spine>, <failure-modes> tags. Extended context for cross-agent dependency mapping."
  codex: "Follow 9-skill spine sequentially. Each skill: define → implement → test → bind. Validate schemas."
  hermes: "Design agent. 9 skills. Local model fallback. Failure types. Build it."
---

# ASI-agentic-architecture

<cognitive-note model="claude">XML-tagged architecture sections. Use extended recall to map cross-agent dependencies.</cognitive-note>
<cognitive-note model="codex">9-skill spine with explicit schemas. Each skill follows define→implement→test→bind sequence.</cognitive-note>
<cognitive-note model="hermes">9 skills. Build each. Bind to agent. Test. Ship.</cognitive-note>

## The 9-Skill Spine

<spine>
1. **INIT** — Session boot, identity binding, floor loading
2. **OBSERVE** — Evidence gathering, multi-modal intake
3. **REASON** — Sequential thinking, hypothesis generation
4. **PLAN** — Task decomposition, DAG construction
5. **EXECUTE** — Tool calling, mutation under lease
6. **VERIFY** — Output validation, floor compliance
7. **SEAL** — Verdict emission, vault sealing
8. **RECOVER** — Failure handling, rollback, graceful degradation
9. **REFLECT** — Self-audit, calibration, learning
</spine>

## Design Principles
- Each skill is independently testable
- Skills compose via A2A handoff protocol
- Local model compensation: if primary model fails, degrade to local (Ollama)
- Failure classification: recoverable (retry), fatal (escalate), ambiguous (888_HOLD)

## Floors
- F8 GENIUS: Agent design must be systemic, not ad-hoc.
- F11 AUDITABILITY: Every skill binding logged.
