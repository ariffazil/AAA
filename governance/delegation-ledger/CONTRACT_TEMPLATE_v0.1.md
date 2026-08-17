# Agent Contract Template v0.1 — Delegation Provenance Guard Rails

**Forged:** 2026-08-17 by kimi-code/FI-008 (after external Claude audit surfaced damage vectors)
**Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)
**Companion schema:** `IBCT_SCHEMA_v0.1.json`
**Companion instance:** `STAGE_0_CONTRACT.json`
**Doctrine:** *DITEMPA BUKAN DIBERI* — Forged, not given. The contract is forged from F13 directive + Claude audit, not granted by enthusiasm.

---

## Why this exists

A strategy doc handed verbatim to an agent causes predictable damage:

1. **Stage flattening** — agent attempts Stage 0/1/2/3 in one session because everything is written in the same imperative voice.
2. **Working code deletion** — "do NOT maintain your own session store" reads to an agent as *remove the session store*. The AAA gateway, the capability registry, those are running.
3. **Compliance theater** — "✅ Cedar adopted" over a stub file and a TODO.
4. **Confidence label erosion** — VERIFIED/INFERRED separation dies on first re-summarization.
5. **Blunt recommendations executed literally** — "Retire or archive AAA/A-FORGE" → agent just does it.

**The fix:** every strategy execution rides a **contract** — additive only, advisory-not-authority, evidence-required, scope-bounded, with explicit non-compensatory floor (Cedar `tier="hard"`).

---

## The 7 Contract Clauses (NON-COMPENSATORY)

### Clause 1 — Additive only
> **Nothing gets deleted or replaced this stage.** Additive only. New files, new branch. Zero removals from AAA, arifOS, or A-FORGE.

- `attenuated_scope.constraints.additive_only = true` in the IBCT.
- `outcome_receipt.files_deleted` MUST be empty array.
- Any detected deletion = token revoked, bearer flagged.

### Clause 2 — Advisory input, not authority
> The report is advisory input, not authority. Any INFERRED claim the bearer wants to act on must be re-verified live and the receipt shown.

- IBCT `constitutional_verdict.constitutional_floors_checked` MUST include `["F2"]` (TRUTH — cite sources).
- INFERRED claims in the strategy doc MUST be re-verified by the bearer before acting on them.
- Verification receipts MUST appear in `outcome_receipt.side_effects`.

### Clause 3 — Evidence-required completion
> No "adopted" / "integrated" / "complete" without a passing test and a command the principal can run themselves. Missing test = the claim is UNMEASURED, not done.

- `attenuated_scope.constraints.require_live_evidence = true`.
- For each "✅" claim in the outcome, there MUST be a runnable command + passing test in `outcome_receipt.side_effects`.
- UNMEASURED is the only allowed alternative — never "complete" without evidence.

### Clause 4 — Scope-bound, out-of-scope → proposals
> Anything outside this stage's scope gets written to a proposals file, not executed.

- `attenuated_scope.resource_patterns` MUST restrict to the stage's allowed paths.
- Anything else goes to `/root/AAA/governance/delegation-ledger/proposals/STAGE_X_*.md`.
- The bearer MUST NOT execute anything outside the scope.

### Clause 5 — Cedar non-compensatory floor
> Tier="hard" floors cannot be overridden by any permit. Tier="soft" can be overridden by F13 sovereign only.

- `attenuated_scope.tier = "hard"` for F1 (AMANAH), F2 (TRUTH), F11 (AUDIT), F13 (SOVEREIGN).
- These floors are absolute. Any "explicit Deny for any one policy always overrides any Allow from other policies" (Cedar semantics).
- The implementation MUST reject the bearer if any hard-tier floor is violated.

### Clause 6 — Hash-chained, tamper-evident
> Every token MUST be chained to its parent via SHA-256 hash. The chain is the ledger.

- `parent_token_hash` MUST be set (or null for root tokens).
- `audit.chain_hash` MUST be SHA-256 of canonical-JSON (RFC 8785 JCS) of all other fields.
- `audit.chain_index` MUST be sequential.
- A break in the chain = token revoked, bearer investigated.

### Clause 7 — Receipts + carry-forward
> Every action MUST produce a receipt that future sessions can verify offline.

- All receipts in `/root/.local/share/arifos/opencode-audit-receipts.jsonl` (or equivalent) MUST include the token_id.
- Carry-forward MUST be written to `/root/.local/share/arifos/carry_forward.json` after each session.
- Receipts MUST be human-readable AND machine-verifiable.

---

## Contract Instance — How to Use

1. **F13 sovereign forges a root IBCT** — chain_index=0, parent_token_hash=null, tier="hard".
2. **Bears derive child tokens** — narrower scope, parent_token_hash=root.chain_hash, signed by bearer.
3. **Bears execute within scope** — outcome_receipt filled, audit.chain_hash computed.
4. **Principal verifies the chain** — re-compute SHA-256 of all tokens, check parent links, validate Cedar policies.

**Failure modes:**
- Bearer violates Clause 1 (additive_only) → token revoked, files_deleted non-empty = automatic revocation
- Bearer violates Clause 3 (no evidence) → claim is UNMEASURED, not "done"
- Bearer violates Clause 5 (hard-tier floor) → token revoked immediately, no override

---

## The Smallest First Cut — Stage 0 (reframe only)

Per Claude's advice: don't start with Cedar or DBOS. Start with the delegation-ledger **schema**.

**Stage 0 scope (this contract):**
- Write `IBCT_SCHEMA_v0.1.json` — the schema spec (ONE file, NO code deps)
- Write `STAGE_0_CONTRACT.json` — the actual Stage 0 instance
- Write `PROPOSALS.md` — Stage 1/2/3 advisory (NO execution)
- Verify the schema is valid JSON Schema
- Compute a sample chain_hash to prove the spec works

**Stage 0 NOT in scope:**
- No MCP middleware implementation (Stage 2)
- No A2A extension (Stage 2)
- No Cedar policy compilation (Stage 1)
- No adoption of Letta/DBOS (Stage 1)
- No retirement of AAA/A-FORGE (Stage 3 — explicitly forbidden by Clause 1)

---

## Verification Contract — How to Prove This Works

Three runnable checks (all must pass):

1. **Schema validity** — `python3 -c "import json, jsonschema; json.load(open('IBCT_SCHEMA_v0.1.json')) and jsonschema.Draft202012Validator.check_schema(...)"` exits 0.
2. **Example instance validates against schema** — `STAGE_0_CONTRACT.json` passes `jsonschema.validate(instance, schema)`.
3. **chain_hash computation is deterministic** — re-computing SHA-256 over canonical-JSON of the token (minus chain_hash) produces the same hash across runs.

All three MUST show in `outcome_receipt.side_effects` of the Stage 0 instance, with command + output.

---

## Anti-Patterns (What This Contract Explicitly Forbids)

| Anti-pattern | Why forbidden |
|---|---|
| "Adopted" without passing test | Clause 3 — UNMEASURED, not done |
| "Integrated" with TODO file | Clause 3 — fake compliance |
| `files_deleted` non-empty with additive_only=true | Clause 1 — token revoked |
| rm/DROP/force-push in commands_run | Clause 5 — Cedar hard-deny |
| INFERRED claim cited as VERIFIED | Clause 2 — re-verify live |
| Strategy doc executed in one session | Stage-bounded — proposal for each stage |
| "Retire AAA/A-FORGE" without F13 ratification | Clause 4 — out of scope, proposal first |
| INHERITING `verdict` from parent token | Each token MUST be independently verified |

---

## Carry-Forward

After each execution, write to `/root/.local/share/arifos/carry_forward.json`:

```json
{
  "delegation_ledger_session": {
    "session_id": "<sct_v1...>",
    "root_token_id": "<sha256:...>",
    "tokens_minted": <int>,
    "tokens_revoked": <int>,
    "chain_verified": true | false,
    "next_session_should": "<one-line>"
  }
}
```

---

*DITEMPA BUKAN DIBERI ⚒️ — The contract is forged from F13 directive. The bearer is bounded by clauses 1-7. The ledger is hash-chained. The receipts are verifiable. Anything else is proposal, not execution.*
