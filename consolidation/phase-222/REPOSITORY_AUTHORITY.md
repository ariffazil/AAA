# Repository Authority Map

**Created:** 2026-07-12T05:35Z

## Authority Hierarchy

| Level | Owner | Authority |
|-------|-------|-----------|
| 1 | **Arif** | Sovereign — final veto, constitutional amendment, irreversible approval |
| 2 | **arifOS** | Constitutional floors F1-F13, verdicts, sessions, identity, routing, audit |
| 3 | **AAA** | Agent instruction surface, state, registry, coordination, cockpit |
| 4 | **A-FORGE** | Bounded execution, verification, rollback, engineering |
| 5 | **Domain organs** | Domain evidence (GEOX, WEALTH, WELL) |
| 6 | **VAULT999** | Immutable audit memory |

## Canonical Ownership

| Artifact | Canonical Owner | Action for Non-Owners |
|----------|----------------|----------------------|
| FEDERATION_CONTRACT.md | arifOS | Import/reference only |
| AGENTS.md | AAA | Per-organ bootstrap only |
| CLAUDE.md | AAA | Thin wrappers or symlinks |
| Constitutional floors (F1-F13) | arifOS | Import from arifOS, don't redefine |
| Tool registry | arifOS (canonical) + each organ (own tools) | Don't claim tools you don't own |
| Port assignments | CLAUDE.md §6 | Don't hardcode conflicting ports |

## Boundary Rules

1. No organ may seal without arifOS
2. Only 888_JUDGE → 999_VAULT emits seals
3. No organ may self-authorize mutation
4. Engineering requires arifOS SEAL → A-FORGE execute
5. Domain organs provide evidence, not decisions

