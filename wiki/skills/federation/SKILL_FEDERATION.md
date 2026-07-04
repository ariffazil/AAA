---
id: federation-safety-wiring
name: federation-safety-wiring
version: 1.0.0-2026.07.03
description: "Wire 9 discoveries into live MCP tool handlers — error envelopes, memory classification, epistemic signals, execution authority, remote preflight."
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: high
floor_scope: [F1, F2, F4, F6, F7, F8, F11, F13]
autonomy_tier: T1
trigger_phrases:
  - "wire safety"
  - "federation safety"
  - "error envelope"
  - "epistemic signal"
  - "9 discoveries"
  - "safety wiring"
dependencies:
  mcp_servers:
    - arifos
    - aforge
  skills:
    - 000-init-intent-classify
    - 999-vault-seal-immutable
  modules:
    - error-classifier.ts
    - mcp-surface-guard.ts
    - execution-authority.ts
    - git-remote-preflight.ts
    - epistemic-signal.ts
    - chain-orchestrator.ts
    - federation_safety.py
inputs:
  - tool_handler_path
  - organ_name
outputs:
  - structured_error_envelope
  - memory_classification
  - epistemic_signal
  - authority_ladder_result
  - remote_preflight_result
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# federation-safety-wiring — THE 9 DISCOVERIES

> **DITEMPA BUKAN DIBERI.** Every tool returns truth, not noise.
> **Maps to:** TREE777 AKAR → skill tree → tool surface
> **Loop position:** Cross-cutting — applies to ALL stages

## The 9 Discoveries

| # | Discovery | Module | What It Does |
|---|-----------|--------|-------------|
| 1 | Surface Truth | `mcp-surface-guard.ts` | Detects when organ tools change |
| 2 | Operator Truth | WELL gate in `chain-orchestrator.ts` | Checks Arif's readiness before chains |
| 3 | Failure Truth | `error-classifier.ts` + `federation_safety.py` | Structured errors with recovery hints |
| 4 | Chain Truth | `chain-orchestrator.ts` | Progress, cancellation, WELL adaptation |
| 5 | Route Truth | `geox-error-envelope.ts` | Correct file routing for all types |
| 6 | Execution Truth | `execution-authority.ts` | Action class enforcement |
| 7 | Remote Truth | `git-remote-preflight.ts` | Auth, reachability, divergence before push |
| 8 | Memory Truth | `epistemic-signal.ts` + `federation_safety.py` | Fresh/stale/inferred/sealed classification |
| 9 | Epistemic Truth | `epistemic-signal.ts` + `federation_safety.py` | OBS/DER/INT/SPEC with confidence caps |

## Wiring Mandate

**Every MCP tool handler MUST:**
1. On success: return `_memory` + `_epistemic` fields
2. On failure: return structured error envelope via `classifyUnknown` / `classify_error`
3. Before mutations: check execution authority
4. Before git push: run remote preflight

## File Locations

| Module | Path |
|--------|------|
| error-classifier.ts | `/root/A-FORGE/src/domain/governance/error-classifier.ts` |
| mcp-surface-guard.ts | `/root/A-FORGE/src/domain/governance/mcp-surface-guard.ts` |
| execution-authority.ts | `/root/A-FORGE/src/domain/governance/execution-authority.ts` |
| git-remote-preflight.ts | `/root/A-FORGE/src/domain/governance/git-remote-preflight.ts` |
| epistemic-signal.ts | `/root/A-FORGE/src/domain/governance/epistemic-signal.ts` |
| federation_safety.py | `{organ}/federation_safety.py` (GEOX, WEALTH, WELL) |
| surface-guard-daemon.ts | `/root/A-FORGE/scripts/surface-guard-daemon.ts` |
| SKILL.md | `/root/.agents/skills/federation-safety-wiring/SKILL.md` |

## Live Status

- `surface-guard.service` — systemd, polling 5/5 organs every 60s
- `test/real-agentic-stack.test.ts` — 34/34 pass
- GEOX: `geox_well_ingest`, `geox_petrophysics` wired
- WEALTH: `_governance_call_tool` middleware wired
- WELL: `well_readiness` wired
- A-FORGE: `forge_shell` + `forge_git` wired

## TREE777 Linkage

- **AKAR (000):** This skill is a dependency of `000-init-intent-classify` — safety wiring must be verified before any golden path entry
- **TREE777:** Registered under `skills/federation/` — governs tool return quality across all organs
- **VAULT999:** All drift events and structured errors leave traces in the hash chain

## The Real Stack Test

```bash
cd /root/A-FORGE
node --test dist/test/real-agentic-stack.test.js
# Must pass 34/34
```

## The One-Line Truth

**The discovery needed is not another model. It is truth plumbing: every agent must know the live tool surface, Arif's readiness, the chain state, the failure cause, the authority boundary, the remote state, and the evidence status before it acts.**

---

*DITEMPA BUKAN DIBERI — Wire it once, trust it forever.*
