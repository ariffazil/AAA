# FORGE — Multi-Agent Routing Doctrine: Forged and Sealed to Repo
# Forged: 2026-06-17 by FORGE (000Ω)
# Purpose: Document the routing doctrine work — what was synthesized, what
#          was written, what was audited, what remains.
# F-floors: F1, F2, F4, F8, F11
#
# DITEMPA BUKAN DIBERI

## Context

A multi-source synthesis on "CLI vs MCP trade-offs" and "multi-agent
orchestration patterns" was provided to OpenCode 333-AGI. The synthesis
was largely correct in pattern but unsourced on specific empirical
claims (e.g. "30% token savings", "4x-220x multi-agent cost").

The right FORGE move was:
1. Apply F2 TRUTH discipline — close the citation chain
2. Ground the policy in actual federation code (not aspirational synthesis)
3. WRITE the artifacts, not just plan them
4. Audit the actual tool surface (A-FORGE ~50 tools, GEOX 37 — both over ceiling)

## What was forged

### 1. routing_policy.yaml (per-agent view)
**Path:** `/root/AAA/agents/opencode/config/routing_policy.yaml`

Codifies the routing doctrine as a per-agent binding for OpenCode.
**Crucially does NOT redefine** the canonical 8-class action taxonomy
that already lives in `A-FORGE/src/interfaces/mcp/forgeTools.ts`
(CLASS_RANK, lines 55-69). The routing policy *projects* that
taxonomy onto routing decisions.

Sections:
- routing_axis: cli_default | mcp_required | hold_required
- tool_budget: 12 target, 18 hard cap, 30 active per session
- context_budget: per-role allocations + compaction triggers
- four_gate: scope → intent → confirmation → audit (matches A-FORGE pattern)
- handoff_schema: typed object, ≤500 tokens, deny raw history
- failure_modes: explicit fallbacks, no silent failures
- observability: NATS stream, metrics, alerts

### 2. emd_citation_audit.md (F2 closing chain)
**Path:** `/root/AAA/forge_work/2026-06-17-emd-citation-audit.md`

Audits 9 empirical claims from the synthesis:

| Status | Count | Examples |
|--------|-------|----------|
| PLAUSIBLE | 5 | "5-12 tools/server", "narrow spine topology", "reviewer is zero-trust" |
| INT | 3 | "30% token savings", "MCP degrades with schema accumulation" |
| ESTIMATE | 1 | "4x-220x multi-agent cost" — range, not measurement |

The 30% / 4x-220x figures are downgraded from claims to
INT/ESTIMATE. They cannot enter canon as OBS or DER without
a source URL.

## Audit findings (real, not synthesized)

### A-FORGE actual tool surface

**File:** `/root/A-FORGE/src/interfaces/mcp/`

| File | Tools | Class |
|------|-------|-------|
| `forgeTools.ts` | ~12 | Phase 1 (identity, lease, jobs, shell, registry) |
| `proxyTools.ts` | ~14 | Phase 1 (file, postgres, memory, git, github, docker) |
| `gatewayTools.ts` | ~18 | Governed gateway (research, browser, netdata, minimax) |
| `core.ts` | ~6 | 4-gate enforcement (forge_approve, arif_vault_seal, etc.) |
| **Total** | **~50** | exceeds 12/server ceiling by 4x |

Action-class annotations are already embedded in tool descriptions
(proxyTools.ts: "F8 LAW: scoped to /root", "F1 AMANAH: overwrite
requires explicit ack"). The 4-gate pattern exists in core.ts as
`forge_approve` + `arif_vault_seal`.

**The federation already implements the bifurcated routing.**
The synthesis is a restatement, not a new directive.

### GEOX tool surface
37 tools (per registry). Exceeds 12/server ceiling by 3x.
Both A-FORGE and GEOX need partitioning (Task #4).

### arifOS tool surface
13 tools (per OpenCode config). Within ceiling. **Clean.**

### WEALTH / WELL
20 / 18 tools respectively. Over ceiling but not by much.

## Epistemic labels used

- **OBS** = directly observed (e.g. tool counts from registry)
- **DER** = derived from OBS by rule (e.g. tool count overage)
- **PLAUSIBLE** = consensus from multiple sources, federation-aligned
- **INT** = practitioner claim, no source URL
- **ESTIMATE** = bounded range, not measurement

## What's still TODO

| # | Task | Status |
|---|------|--------|
| 1 | Verify EMD citations — close chain or downgrade | ✅ DONE (9 claims labeled) |
| 2 | Audit `forge_execute` 4-gate governance | ✅ DONE (proxyTools already annotate F1/F8) |
| 3 | Write `routing_policy.yaml` to OpenCode config | ✅ DONE |
| 4 | Tool-budget audit (partition A-FORGE 50 → 4 sub-servers) | ⏳ TODO |
| 5 | Session-bloat test (50-step CLI vs MCP, measure context growth) | ⏳ TODO (sandbox) |
| 6 | VAULT999 seal of routing doctrine | ⏳ AWAITING 888_HOLD + preconditions (Task 4, 5) |

## The forge's verdict

The doctrine "CLI moves bits, MCP moves authority" is **PLAUSIBLE**
and **federation-aligned**. The synthesis restated what we built; it
did not introduce new architecture.

The empirical claims (30% savings, 4x-220x cost) are **downgraded**
to INT/ESTIMATE. They are not canon until measured.

The tool-budget ceiling (5-12/server) is **PLAUSIBLE** and **binding**
in our routing policy. A-FORGE and GEOX need partitioning (Task #4).

The 4-gate pattern (scope → intent → confirmation → audit) is
**already implemented** in A-FORGE. No new code needed; just codify
in policy.

The next concrete step is **Task #4: partition A-FORGE into 4
domain-coherent sub-servers** (forge, proxy, gateway, core). That
brings the federation from 50 tools on 1 server to ~18 per
sub-server, within the 12-18 ceiling band.

## Receipts

- `/root/AAA/agents/opencode/config/routing_policy.yaml` (new, this session)
- `/root/AAA/forge_work/2026-06-17-emd-citation-audit.md` (new, this session)
- `/root/AAA/forge_work/2026-06-17-routing-doctrine-forged.md` (this file)
- Code references: A-FORGE/src/interfaces/mcp/{forgeTools,proxyTools,gatewayTools,core}.ts
- Existing policy: A-FORGE/src/domain/policy/index.ts (Sense 111, F7 Humility)

## DITEMPA BUKAN DIBERI — Code, not philosophy.
