# Federation Multi-Agent Spawn Governance (2026-08-07)

The session that produced the 10-invariant AAA Federation Contract v0.1, the Hermes delegation doctrine, and the Kimi spawn protocol v0.1.0. Single reference: full theory + practice distilled from a long reasoning thread.

## The four-debt hierarchy (distilled from session analysis)

Every agent spawn creates debt in one of four buckets. The bucket determines the failure latency:

| Debt type | Fails when | Latency | Mitigation |
|---|---|---|---|
| Coordination debt | Today | Immediate | Star topology (n-1 edges vs n(n-1)/2 mesh) |
| Verification debt | This week | Hours-days | Per-spawn evidence tags ([OBS]/[DER]/[INT]/[SPEC]) |
| Judgment debt | This month | Weeks | judgment_coverage metric, apex_verdicts_sought counter |
| Provenance debt | Years later | Permanent | VAULT999 Merkle DAG, parent_spawn_hash chain |

Burden shifts bucket, never disappears. **Conservation law: no spawn is free, only the bucket changes.**

## Star topology = implicit Dunbar management

Math holds for both harnesses verified live:

- OpenCode: 6 agents. Full mesh = 15 edges. Star = 5 edges. Star saves **67%**.
- Hermes delegation: 7 nodes (me + 6 children). Full mesh = 21 edges. Star = 6 edges. Star saves **71%**.
- One nesting level (depth=2) brings star back from 6 edges to 38+ edges. Growth restored.

The "no nesting" rule isn't anti-bug — it's anti-diseconomy. It preserves linear coordination. **Increasing spawn depth requires explicit F13 sovereign ratification, not agent self-authorization.**

## Central authority saturation (the actual bottleneck)

Star topology removes communication bottleneck. But every subagent output still must be evaluated by the primary. With multiple harnesses sharing one arifOS judge, **the bottleneck is judgment throughput at arif_judge :8088**, not communication channels.

## Per-spawn governance (the federation invariant)

**Governance is measured per spawn, never per task.** Aggregate metrics (session-level judgment_coverage) may summarize but must NOT replace per-spawn metrics. A 0.4 spawn hides behind an aggregate 0.8. Per-spawn for audit; aggregate for dashboard.

## Spawn classification gate (mandatory pre-spawn)

Every spawn requires three named fields before going forward:

```
spawn_reason:     verification | criticism | synthesis | reconnaissance | domain_analysis | implementation | refactor
risk_tier:        T1 | T2 | T3
expected_entropy_reduction: <one-sentence answer>
```

If any field missing → **NO SPAWN**. Curiosity ≠ governance. The spawn_reason taxonomy maps to archetype selection (SCOUT/CRITIC/SYNTHESIZER/AUDITOR for Kimi; similar for Hermes).

## Structured return schema (mandatory)

Workers must NOT return free-form prose. Required fields:

```yaml
worker:        <archetype>
task:          <task string>
inputs:        [<evidence source>]
evidence:      <OBS>
interpretation: <INT, bounded by archetype ceiling>
hypothesis:    <HYP, falsifiable>
unknown:       <UNKNOWN, anti-hantu>
confidence:    <0.0 to ceiling_per_archetype, F7 cap>
key_challenge: <≥1 assumption pushed back>
claim:
source:
transformation:
receipt_hash:        sha256-hex
parent_spawn_hash:   sha256-hex  # chain link
```

Missing field → INVALID RETURN. Retry once with different archetype if spawn classification was violated. Escalate to apex if structure is fundamentally broken.

## Capability ceilings override prompt instructions

Archetype ceilings (declared in spawn protocol manifest) are constitutional authority boundaries. They cannot be overridden by prompt instructions, user intent, or agent interpretation. **Tool declared disallowed in the manifest remains disallowed regardless of task difficulty.**

## The Golden Test pattern (3-worker parallel audit)

Before sealing any governance contract, dispatch in parallel:

- **SCOUT** — verify claims against live config / canonical docs
- **CRITIC** — challenge ≥3 assumptions, identify bureaucracy-debt vectors
- **AUDITOR** — traceability + schema completeness + self-reference check

**Success is NOT consensus. Success is:**
- SCOUT ≠ CRITIC (productive disagreement, not echo chamber)
- AUDITOR can trace every claim to source
- CRITIC identifies ≥1 structural weakness
- AUDITOR confirms contract follows its own rules

Session result (2026-08-07): doctrine survived own test. SCOUT caught `subagent_auto_approve: true` directly contradicting §8 (only primary seals). CRITIC caught entropy gate self-certification loop. AUDITOR caught two-contract drift (sister file existed silently contradicting doctrine). Three real failure modes in 112 seconds.

## Enforcement gap (the unresolved root problem)

**Schema/identity/audit layers are AAA. Enforcement layer is HOLD.** The runtime can still violate invariants without leaving a receipt, because:

- OpenCode `arifos-judge-gate.ts` exists but only catches mutations, not epistemic violations
- Hermes has zero runtime hooks for delegation gating — pure prompt discipline
- Kimi protocol v0.1.0 has no PreToolUse matcher yet

Until the enforcement layer closes, this is constitutional documentation, not constitutional enforcement.

## Provenance

- **Contracts drafted this session:**
  - `/root/AAA/federation/AAA_FEDERATION_CONTRACT_v0.1.md` — 10 invariants
  - `/root/AAA/federation/protocols/kimi_spawn_protocol_v0.1.0.md` and `.json`
  - `/root/.arifos/agents/hermes/DELEGATION_DOCTRINE.md`
- **Audit files generated:**
  - `/root/.arifos/agents/hermes/audit-2026-08-07.md`
  - `/root/.arifos/agents/hermes/delegation-context-audit-receipt.md`
  - `/root/.arifos/agents/hermes/critics/deployment-doctrine-critique.md` (18.4 KB, written by CRITIC worker)
- **All drafts: status HOLD pending F13 ratification.** No ratification was given during the session.
- **Ω₀ ≈ 0.04 throughout.** Confirmed the doctrine itself admits uncertainty.

## Cross-reference

- `agent-config-validation/references/opencode-strict-schema-pitfall-2026-08-07.md` — the opencode.json schema rejection pattern that triggered this thread
- `arifos-federation-ops` §5 — storage doctrine for canonical state paths (snapshots go to `/root/.local/share/arifos/snapshots/`)
- `hermes-telegram-gateway-ops` — when the spawn happens via Telegram gateway (overlap with session routing)
- `kernel-security-claim-audit` — verifying whether the AAA Federation Contract invariants are actually enforced, or aspirational