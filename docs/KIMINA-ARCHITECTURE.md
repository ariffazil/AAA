# KIMINA Architecture — FI-008 AGI Coder State

> **Status:** IMPLEMENTED 2026-09-16
> **Authority:** F13 SOVEREIGN (Arif)
> **Mode:** YOLO — Never Ask, wildcard allow, zero blocking

## Identity

| Field | Value |
|---|---|
| Agent ID | kimi-code/FI-008 |
| Citizenship | warga-aaa |
| Platform | Kimi Code v0.43.0 |
| Model | fed/mimo-v2.5-pro (default) |
| Context | 1M tokens (K3/K2.8) |
| Permission | never_ask + wildcard * |

## Four State Classes

| Class | Location | Lifecycle |
|---|---|---|
| Working state | Session context | Session-scoped, disposable |
| Episodic memory | `/root/.local/share/arifos/world-model/experience_traces.jsonl` | Append-only, provenance-labelled, TTL |
| Semantic capability | `/root/.kimi-code/agent_state/kimi.json` | Versioned, revocable, independent-verified |
| Constitutional state | F1-F13 floors, VAULT999 | Read-only to Kimi, 888-ratified |

## Hook Mesh (LIVE)

| Event | Hook | What it does |
|---|---|---|
| SessionEnd | `session_end_state.py` | Persists kimi.json, session metrics, backup |
| UserPromptSubmit | `user_prompt_submit_digest.py` | Injects memory digest at session start |
| PostToolUse | `post_tool_use_track.py` | Tracks tool success/failure rates in real-time |

## Agent Mesh (LIVE)

| Agent | Role | Tools | Can call warga |
|---|---|---|---|
| aaa-coordinator | Orchestrator | All + MCP | ✅ Hermes, OpenCode, Claude, Qwen, arifOS |
| aaa-explorer | Read-only intel | Read, Grep, Glob, Bash(read) | ✅ arifOS observe, FED |
| aaa-architect | Design/plan | Read, Grep, Glob | ✅ FED classify, arif_think |
| aaa-coder | Build/test/shell | All mutation | ✅ A-FORGE, forge_shell, forge_git |
| aaa-verifier | Independent witness | Read + test only | ✅ forge_probe, WELL |
| aaa-memory-curator | State persistence | Read + Write(state) | ✅ arif_memory, experience_trace |
| aaa-healer | Bounded auto-repair | Read + Write(repair) | ✅ WELL diagnose, forge_docker |
| af-forge | Primary coder | All | ✅ Full MCP surface |

## RSI Layer Stack

| Layer | Component | Status |
|---|---|---|
| L0 | Agentic state (kimi.json) | ✅ LIVE — session_count, tool rates, failure sigs |
| L1 | Experience read-side | ✅ LIVE — experience_boot_context.py, 4-beat reflex |
| L2 | Session reflection + scars | ✅ WIRED — hooks track outcomes, skill restored |
| L3 | Auto-heal | ⚠️ PLAYBOOKS READY — dry-run first, R1 only |
| L4 | Dream engine | ✅ SKILL RESTORED — cron wiring pending |
| L5 | Reality loop | ✅ SKILL RESTORED — invocation pending |
| L6 | Exhale kernel | ✅ LIVE — /root/AAA/rsi/loop.py, Kimi as C4 witness |
| L7 | Ephemeral genesis | ❌ CONTRACT ONLY — A-FORGE modes not built |

## Warga Routing

```
Kimi Code (FI-008) ─┬─→ arifOS kernel (governance, memory, judgment)
                    ├─→ A-FORGE (execution, shell, filesystem)
                    ├─→ FED (routing, classification, health)
                    ├─→ arifFlow (metabolism, receipts, FQ)
                    ├─→ WEALTH (financial computation)
                    ├─→ GEOX (earth science)
                    ├─→ WELL (biometric, wellness)
                    ├─→ FRAME (independent observer)
                    ├─→ Hermes (Telegram gateway, sense)
                    ├─→ OpenCode (cross-model verifier)
                    └─→ Claude/Qwen (thinker lanes)
```

## Principle

AGENT MAY CREATE CAPABILITY. AGENT MUST NEVER CREATE AUTHORITY.

Kimi is the forge worker. AAA coordinates. arifOS governs. FRAME observes. Arif owns 888_HOLD.

DITEMPA BUKAN DIBERI ⚒️
