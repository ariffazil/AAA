# Stage 1/2/3 Proposals — Advisory Only, NOT Executed

**Forged:** 2026-08-17 by kimi-code/FI-008 (per Claude external audit + F13 strategic pivot)
**Authority:** F13 SOVEREIGN — these are *proposals*, not mandates. Bearer MUST NOT execute without F13 ratification per IBCT contract clause 4.
**Companion schema:** `../IBCT_SCHEMA_v0.1.json`
**Companion contract:** `../CONTRACT_TEMPLATE_v0.1.md`

---

## � Critical Rule

> **This document is advisory input. NOT authority.**
>
> Per IBCT contract clause 2, any INFERRED claim here MUST be re-verified live by the bearer before acting on it. The receipt must be shown in `outcome_receipt.side_effects`.
>
> Per clause 4, anything in this document is OUT OF SCOPE for Stage 0 execution. These are *proposals* — to be ratified by F13 separately, then minted as their own IBCT contracts.

---

## Stage 1 Proposals (weeks 1-4 per strategic pivot doc)

### 1.1 — Adopt DBOS or Cloudflare Agents SDK for session durability

- **Claim source:** `STRATEGIC_PIVOT_DELEGATION_PROVENANCE_2026-08-17.md` lines 33-34 (verdict: ADOPT, don't build)
- **Status:** UNVERIFIED — bearer MUST re-verify against current `federation_act.py` (which already has session store) and against DBOS release notes
- **Why proposed:** AAA's session store is local; DBOS provides Postgres-backed durability
- **Risk:** Replacing working code with DBOS requires rewriting session lifecycle. Per clause 1 (additive only), this is FORBIDDEN without prior F13 ratification.
- **Open question:** Does DBOS handle Ed25519-signed SCTs natively? (UNVERIFIED — must check.)
- **Action if approved:** Mint a separate IBCT with `allowed_actions: ["read", "compare"]` and `resource_patterns: ["/root/A-FORGE/litellm-config.yaml", "/root/AAA/governance/federation_act.py"]`. Bearer compares DBOS patterns to existing session store. NO code changes.

### 1.2 — Adopt Letta (MemGPT) for memory tiers

- **Claim source:** strategic pivot doc line 34
- **Status:** UNVERIFIED — bearer MUST re-verify that Letta's 23k★ is current, Apache-2.0 license, and that AAA's memory tiers (L1-L6) actually need replacement vs. extension.
- **Risk:** Replacing memory tiers loses 12+ months of constitutional doctrine encoded in H5 scar lineage.
- **Action if approved:** Mint IBCT for `allowed_actions: ["read", "compare"]` against `/root/AAA/skills/opencode-init/SKILL.md` and `/root/.local/share/arifos/carry_forward.json`. NO code changes.

### 1.3 — Express F1-F13 as Cedar policies at AgentGateway

- **Claim source:** strategic pivot doc line 36
- **Status:** PARTIALLY VERIFIED — `cedar_bridge.py` already exists at `/root/arifOS/arifosmcp/arifos_policy/cedar_bridge.py` (Phase 2 placeholder, always returns ALLOW with override=True).
- **Cedar semantics confirmed via research:**
  > "A Deny result for any policy evaluation results in an overall Deny for the request"
  > "An explicit Deny for any one policy always overrides any Allow from other policies"
- **Risk:** Cedar policy compilation could conflict with arifOS's `override=True` semantic (which lets kernel bypass Cedar). Must resolve.
- **Action if approved:** Mint IBCT for `allowed_actions: ["read", "compile_test"]`. Bearer tests Cedar policy compilation against the existing override path. NO production changes.

### 1.4 — Emit OTel `gen_ai.*` semantic conventions

- **Claim source:** strategic pivot doc line 38
- **Status:** UNVERIFIED — bearer MUST check what arifOS already emits (likely has its own tracing).
- **Risk:** Dual instrumentation (OTel + existing) increases noise.
- **Action if approved:** Mint IBCT for `allowed_actions: ["read", "emit_test"]`. Bearer emits test spans and verifies they don't conflict. NO production changes.

---

## Stage 2 Proposals (weeks 4-16 per strategic pivot doc)

### 2.1 — Build the IBCT reference implementation

- **Claim source:** strategic pivot doc lines 47-66
- **Status:** **PARTIALLY ADDRESSED BY STAGE 0.** The `IBCT_SCHEMA_v0.1.json` IS the smallest first cut (one file, no deps, schema only).
- **What's remaining:** A reference implementation (Python or TypeScript) that:
  - Mints tokens (Ed25519 signed)
  - Verifies chains (parent_token_hash, chain_hash)
  - Enforces hard-tier floors (Cedar-style non-compensatory)
  - Rejects token on Clause 1/3/5 violations
- **Where it would live:** `/root/AAA/governance/delegation-ledger/reference-impl/` (new dir, additive)
- **Risk:** Implementation bugs could fail-open on hard floors. Must include fuzz tests.
- **Action if approved:** Mint IBCT with `allowed_actions: ["create_file", "write_test"]`, `resource_patterns: ["/root/AAA/governance/delegation-ledger/reference-impl/*"]`. Bearer writes implementation + tests.

### 2.2 — MCP middleware implementation

- **Claim source:** strategic pivot doc line 60
- **Status:** UNVERIFIED
- **What it would do:** sit between any agent and any MCP server, mint + verify IBCT on every tool call.
- **Where it would live:** `/root/A-FORGE/src/infrastructure/mcp/ibct-middleware.ts` (new file, additive)
- **Risk:** Middleware that breaks MCP would break ALL agents. Must have feature flag + shadow mode first.
- **Action if approved:** Mint IBCT for `allowed_actions: ["read", "create_file"]`, `resource_patterns: ["/root/A-FORGE/src/infrastructure/mcp/ibct-middleware.ts"]`. Bearer writes middleware + shadow test.

### 2.3 — A2A extension

- **Claim source:** strategic pivot doc line 59
- **Status:** UNVERIFIED — bearer MUST engage A2A Discussion #741 + Issue #2026 to confirm scope alignment.
- **What it would do:** add IBCT fields to A2A Agent Cards.
- **Where it would live:** `/root/AAA/aaa-a2a/src/aaa_a2a/extensions/ibct/` (new dir, additive)
- **Risk:** A2A spec is still in flux; contributing early might lock in bad design.
- **Action if approved:** Mint IBCT for `allowed_actions: ["read", "compare_spec"]`. Bearer reads A2A spec + IBCT schema + writes gap analysis. NO spec submission.

---

## Stage 3 Proposals (weeks 12-24 per strategic pivot doc)

### 3.1 — Three verifiable artifacts

- **Claim source:** strategic pivot doc lines 100-109
- **Status:** UNVERIFIED
- **What they are:**
  1. The delegation-ledger spec (open schema) — DONE in Stage 0 as `IBCT_SCHEMA_v0.1.json`
  2. A reference MCP/A2A middleware implementing it — UNVERIFIED (Stage 2.2)
  3. A demo showing A→B→C provenance — UNVERIFIED
- **Where:** `/root/AAA/governance/delegation-ledger/published/`
- **Action if approved:** Mint IBCT for `allowed_actions: ["read", "publish"]`, `constraints.require_live_evidence=true`. Bearer publishes only after F13 ratification.

### 3.2 — Retire or archive AAA/A-FORGE/HERMES as separate "organs"

- **Claim source:** strategic pivot doc lines 110-111
- **Status:** ⚠️⚠️⚠️ **EXPLICITLY FORBIDDEN BY CLAUSE 1 OF CURRENT CONTRACT** ⚠️⚠️⚠️
- **Why forbidden:** Clause 1 (additive only) explicitly forbids removals. This Stage 3 proposal would violate it.
- **Required before execution:**
  1. IBCT contract for Stage 3 (separate from Stage 0)
  2. Clause 1 must be explicitly waived by F13 ratification
  3. Replacement organ MUST be operational BEFORE retirement
  4. Carry-forward MUST be written for all running services
- **Status:** UNVERIFIED and BLOCKED until Stage 1 + Stage 2 deliverables are sealed + verified.

---

## What MUST NOT happen (per IBCT contract)

| Action | Blocked by |
|---|---|
| Delete AAA/A-FORGE/HERMES organs | Clause 1 (additive only) |
| Replace session store with DBOS without F13 ratification | Clause 4 (out of scope) |
| Drop `verdict` field from kernel envelopes | Out of contract scope — separate IBCT required |
| Cite INFERRED claim as VERIFIED | Clause 2 (advisory input, not authority) |
| "✅ Cedar adopted" without passing test | Clause 3 (evidence-required) |
| One-shot execution of all 4 stages | Each stage is its own IBCT contract |

---

## Carry-Forward Notes for Each Stage

When (if ever) a proposal moves to execution, the bearer MUST:
1. Mint a new IBCT (not reuse Stage 0's)
2. Verify the new scope against the new stage's constraints
3. Show evidence per Clause 3
4. Write carry-forward to `/root/.local/share/arifos/carry_forward.json`

---

*DITEMPA BUKAN DIBERI ⚒️ — These are proposals, forged from external audit + F13 directive. Not granted. Not executed. Awaiting ratification per IBCT contract clause 4.*
