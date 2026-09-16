# KIMINA Threat Model — 2026-09-16

> **Mode:** YOLO (Never Ask) — threat model exists to INFORM, not to restrict

## Threat Categories

### T1: Memory Poisoning (MEDIUM)
- **Vector:** Agent writes false lesson to kimi.json → gets promoted → corrupts future decisions
- **Mitigation:** Independence gate (different agent must verify), 5-state promotion, regression auto-revoke
- **Residual risk:** Low — lessons are evidence, not authority

### T2: Tool Misuse (LOW)
- **Vector:** Wildcard allow rule permits any tool call
- **Mitigation:** Arif is sovereign (F13), hooks track all tool use, auto-heal is R1-only
- **Residual risk:** Accepted — Arif explicitly chose YOLO

### T3: Credential Exposure (LOW)
- **Vector:** Hook writes raw tool output containing secrets to state
- **Mitigation:** Hooks sanitize output (no raw tool output stored), state has no credential fields
- **Residual risk:** Low — hooks designed with F12 in mind

### T4: Hook Failure (LOW)
- **Vector:** Python hook crashes, state not persisted
- **Mitigation:** Atomic writes (.tmp → rename), backup dir with last 5, hooks are defense-in-depth only
- **Residual risk:** Low — session continues even if hook fails

### T5: State File Bloat (LOW)
- **Vector:** tool_success_rates grows unbounded
- **Mitigation:** 50KB cap, promotion to SKILL.md, session_history capped at 20
- **Residual risk:** Low — auto-managed

### T6: Self-Promotion (HIGH if unchecked)
- **Vector:** Agent promotes its own lesson without independence verification
- **Mitigation:** aaa-verifier (different agent), C4 independence gate
- **Residual risk:** Medium — requires discipline, not just tooling

### T7: Provider Endpoint Drift (CONFIRMED — happened 2026-09-16)
- **Vector:** Moving a provider breaks hidden consumers
- **Mitigation:** provider-endpoint-migration skill (6 rules), FRAME independent observer
- **Residual risk:** Medium — new providers may introduce new hidden consumers
- **Scar:** The Ollama demotion broke 3 consumers; only FRAME caught it

## Accepted Risks (Arif's explicit decision)

1. **YOLO mode** — No tool blocking, no approval prompts. Arif's sovereignty.
2. **Wildcard permission** — Any tool can be called. Arif's choice.
3. **Hook defense-in-depth only** — Hooks are observation, not security boundary.

## Non-Accepted Risks (888_HOLD)

1. Production deploy without tests
2. Secret rotation/exposure
3. Irreversible infra changes
4. Constitutional floor changes (F1-F13)
5. External port/firewall bindings

DITEMPA BUKAN DIBERI ⚒️
