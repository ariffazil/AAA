# CCC — Codex Coder Compiler

> **SEAL: 2026-08-14 by F13 + ASI review**
> CCC = portable coding-worker contract. NOT a model, role, judge, or federation.

## Pipeline

```
ARIF → AAA → FED → CCC(harness, role=?) → A-FORGE → arifFlow → VAULT999
                                ↓
                         LiteLLM gateway
```

## What CCC Is

CCC is the **capability standard** for any coding worker. Any CLI harness can be instantiated as a CCC worker:

```
CCC(Kimi)     — MiniMax-M3 default + zai glm-5.3 forge lane (config.toml)
CCC(Qwen)     — runtime-resolved (federation-models.json agents[qwen-code]; last: glm-5.3)
CCC(OpenCode) — runtime-resolved (litellm-federation/forge-777 cascade, GLM-primary)
CCC(Aider)    — DeepSeek V3
CCC(Codex)    — FED cascade (codex.forge lane: glm-5.3 primary)
```

## What CCC Is NOT

- NOT an identity (AGI/ASI/APEX are functions, not harnesses)
- NOT a judge (judgment routes through AAA → apex-judge)
- NOT permanently authorized for all tools

## Roles (task-scoped, not harness-scoped)

```
CCC(harness, role=planner)    — read-only, propose architecture
CCC(harness, role=builder)    — write in worktree/branch, isolated
CCC(harness, role=verifier)   — test, lint, verify, separate session
CCC(harness, role=reviewer)   — read-only audit, no mutation
```

Role assigned per task. Role expires when task completes.

## Tool Access Rules

| Baseline (always available) | Task-scoped (temporary grant) |
|---|---|
| bash, grep, rg, find, shell | MCP mutation tools |
| read, search, analyze | git push to main |
| test, lint, type-check | deploy, service restart |
| git commit (branch only) | secrets access |
| mgrep (semantic search) | external publish |

"All tools available" ≠ "all tools permanently authorized."

## Spawn Rules

1. **Never spawn 3 CCC simultaneously for mutation on same target.**
2. Spawn separate workers for proposal, build, verification — in isolated worktree/branch.
3. Merge or deploy only through ONE governed execution gate (A-FORGE).
4. Baseline tools = permanent. Risky tools = task-scoped + temporary + logged.

## mgrep

- Additional capability, not replacement for grep/rg/find/shell.
- Requires MXBAI_API_KEY — credential boundary audit needed before FED-wide rollout.
- Installed at `/root/.npm-global/bin/mgrep` v0.1.13.

## Governance

CCC workers operate under AAA constitution. T3 actions → 888_HOLD. Everything reversible → execute. All mutations logged to arifFlow.

## SEAL Hierarchy (three planes, never collapsed)

```
Worker COMPLETE  = evidence gathered, commit ready (attestation only)
APEX SEAL        = constitutional judgment (authorization)
A-FORGE          = authorized integration/deploy (execution gate)
```

Worker attestation ≠ sovereign authorization. Worker never SEALs. Worker declares COMPLETE.

## CCC → AAA Escalation

When a CCC worker encounters something requiring F1-F13 judgment:
1. Worker HOLDs (stops, does not self-authorize)
2. Worker proposes (evidence package)
3. Escalates to AAA governance layer
4. apex-judge or F13 approves/rejects
5. A-FORGE executes if approved

CCC never governs. CCC never judges. CCC builds, verifies, and escalates.

DITEMPA BUKAN DIBERI ⚒️
