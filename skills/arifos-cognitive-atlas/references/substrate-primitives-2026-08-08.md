# Substrate Primitives — The 3-Command Forge Cycle (2026-08-08)

## The Architecture (forged this session)

Two substrate primitives, three execution skills, applied across 3 runtimes = 9 skills:

```
INIT = substrate primitive 1 → who is acting?
MEMORY = substrate primitive 2 → what was known?
FORGE = execution primitive → go do it
PROPOSE-SEAL = archival primitive → record it permanently
```

## The Forge Cycle (identical across all runtimes)

```
/init → /forge → /propose-seal
identity → action → evidence → verdict → permanent record
```

## Per-Runtime Atlas Expression (primary weights)

| Runtime | Primary | Secondary | Secondary | Authority |
|---|---|---|---|---|
| **Hermes** | 000 OBSERVE + 444 ORCHESTRATE + 555 VERIFY | 666 AUDIT + 999 WITNESS | 222 ARCHITECT + 333 THINK + 777 EXECUTE | CONDITIONAL |
| **OpenClaw** | 333 THINK + 444 ORCHESTRATE | 222 ARCHITECT + 777 EXECUTE | 000 OBSERVE + 555 VERIFY | T1 auto |
| **OpenCode** | 222 ARCHITECT + 333 THINK + 777 EXECUTE | 000 OBSERVE | — | T1 auto |

## Implementation Files (canonical)

```
AAA/skills/
├── hermes-init/SKILL.md
├── hermes-propose-seal/SKILL.md
├── hermes-forge/SKILL.md
├── openclaw-init/SKILL.md
├── openclaw-propose-seal/SKILL.md
├── openclaw-forge/SKILL.md
├── opencode-init/SKILL.md
├── opencode-propose-seal/SKILL.md
└── opencode-forge/SKILL.md
```

## Session Card Format (canonical across all runtimes)

Every /init response MUST include:
- Actor, session_id, lane, runtime, phenotype, bot identity
- Atlas expression weights (000-999)
- Authority tier (T0-T3)
- F1-F13 status
- Kernel alignment + SCT + FQ
- Mutation: ALLOWED/DENIED
- Seal: DENIED (always — 888-APEX only)

## Critical Doctrine

- **Skills ≠ native Telegram commands.** Skills are context for the LLM. To appear in bot command menus, must register in `customCommands` in OpenClaw's `openclaw.json` (T3 boundary — production config).
- **OpenClaw cannot self-seal.** `/seal` was deprecated; `/propose-seal` routes to 888-APEX.
- **/init guard:** all /forge and /propose-seal calls return ERROR if /init was not called first.
- **888 JUDGE is NONE for all three runtimes.** No runtime can issue SEAL/HOLD/VOID — that's 888-APEX exclusive.

## See Also

- `arifos-cognitive-atlas` SKILL.md — the Atlas weights + kernel gaps
- `arifos-federation-ops` (bundled) — VAULT999 correction receipt pattern
- `hermes-telegram-gateway-ops` (bundled) — cross-agent routing via @AGI_ASI_bot tag
