# arifOS vs AutoGen — Integration Blueprint

> DITEMPA BUKAN DIBERI
> Forged: 2026-06-14 | Companion to: AAA_BENCHMARK_EXTERNAL.md

---

## Strategic Position

AutoGen is stronger for agent society. arifOS is stronger for law above that society.

```
AutoGen = parliament of agents
arifOS = constitution above parliament
```

## Scorecard

| Dimension | AutoGen | arifOS | Winner |
|-----------|---------|--------|--------|
| Multi-agent conversation | 9.3 | 6.0 | AutoGen |
| Distributed runtime | 7.0 | 5.0 | AutoGen |
| Research prototyping | 8.5 | 5.5 | AutoGen |
| Constitutional separation | 2.5 | 9.0 | arifOS |
| Human sovereignty | 6.0 | 9.5 | arifOS |
| Audit law | 6.5 | 8.5 | arifOS |

## Integration Pattern

Build `adapters/autogen_arifos_parliament/`:

Every AutoGen agent must carry:
```
role: string
allowed_tools: [string]
forbidden_actions: [string]
authority_level: L0-L6
lease_scope: [string]
may_propose: true
may_authorize: false
```

## Key Distinction

| Capability | AutoGen | arifOS |
|-----------|---------|--------|
| Create agents | ✅ Unlimited | ❌ Bounded by lease |
| Agent-to-agent chat | ✅ Full mesh | ❌ Requires scope transfer |
| Authorize actions | ✅ Self-authorizing | ❌ Must go through judge |
| Constitutional limits | ❌ None built-in | ✅ F1-F13 enforced |

## Boundary Rules

- AutoGen may create many agents. arifOS decides which agent actions are legitimate.
- AutoGen agent roles are aspirations. arifOS leases are enforcement.
- AutoGen agent conversations are internal. arifOS seals external actions.

## Eureka

AutoGen creates agent society. arifOS gives that society a constitution.
