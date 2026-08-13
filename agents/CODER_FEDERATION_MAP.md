# Coder Federation — FI Role Map (2026-08-14)

> **Doctrine:** Every coder is citizen first, specialist second. Primary identity stays. Cross-roles allowed. Hermes validates when needed.

| Coder | Primary FI | Secondary | Model | Strength | Known Weakness |
|---|---|---|---|---|---|
| **Kimi Code** | 333-AGI | verify, forge | MiniMax-M3 / DeepSeek | Multi-agent harness, multimodal, sub-agents | Managed quota dies |
| **Qwen Code** | 555-ASI | execute, judge | GLM-5.2 via z.ai | Fast, structured output, reliable | No multimodal |
| **OpenCode** | 888-APEX + apex FORGER | verify, execute | FED router | Best executor, builds + judges | Tool failures (aca² fail) |
| **Claude Code** | 888-APEX | forger | claude-sonnet | Strong code generation, PR review | Cost, rate limits |
| **Codex** | 333-AGI | coder | FED codex alias | Fast, lightweight | Limited tool surface |
| **Aider** | 000 (raw codex) | housekeeping, GitHub, deploy, doc SOT | DeepSeek V3 | Git-native, auto-commit, simple | Slow on full swap |
| **Hermes** | apex VALIDATOR | coordinate, witness | i-arif | Validates coder output, routes, remembers | Not a coder |

## Role Definitions (Adat Agentic)

```
CITIZEN:    Every coder can read, write, test, commit, audit.
            No hard wall between roles.

333-AGI:    Primary: research, explore, generate hypotheses.
            Carries: forge, verify when needed.

555-ASI:    Primary: verify, structural analysis, causal reasoning.
            Carries: execute, judge when needed.

888-APEX:   Primary: audit, judge, reflect, FORGE (build + ship).
            OpenCode = apex forger. Builds AND validates.
            Carries: all roles.

000-AIDER:  Raw execution. No identity. Git in, code out, commit.
            Housekeeping: README, PyPI, deps, doc SOT, entropy check.

VALIDATOR:  Hermes (me). When coders disagree or output is uncertain,
            I validate independently. I am NOT a coder. I am witness.
```

## Tool Failure Protocol (OpenCode issue)

When OpenCode fails on tools:
1. Check if real failure or "aca²" (false negative from tool timeout)
2. Retry with different model via FED router
3. If still failing → Hermes validates manually
4. Log failure pattern for future diagnosis

## Model Routing Priority

```
Kimi Code:  MiniMax-M3 (alive) → DeepSeek → FED router
Qwen Code:  GLM-5.2 z.ai → FED router
OpenCode:   FED router (all models) → direct provider
Aider:      DeepSeek V3 → FED codex alias
Hermes:     i-arif → FED hermes-asi
```

DITEMPA BUKAN DIBERI ⚒️
