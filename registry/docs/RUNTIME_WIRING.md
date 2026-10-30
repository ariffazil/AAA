# Runtime Wiring — Model Governance Card

ARIFOS::AAA_MODEL_GOVERNANCE_RUNTIME_WIRING::2026-10-30::v1 — F13-sealed. Executed 2026-10-30T08:00+08:00 → 2026-10-31T10:05+08:00 (envelope closeout).

## What is live

1. **Card compiler (AAA)** — `registry/governance_cards.py`; deterministic per-lane
   cards in `generated/model-governance-cards/<lane>.json` (333/555/888/999/forge/hermes).
   REALITY ladder: `resolved_model` only from a probe receipt, else UNKNOWN → HOLD.
   Budget: target 1200B, hard max 2048B (fail-closed compaction). Tests:
   `tests/registry_supply_chain/test_governance_cards.py` (10).
2. **MCP resource (arifOS)** — `arifos://model-governance-card/{lane}`, live on the
   production kernel (canary: 333 → glm-5.3→glm-5.3 matched BOUND; unknown lane →
   UNAVAILABLE/UNKNOWN with zeroed ceiling). Surface count 32→33, locked test synced
   (completing the tree777 sync owed by 91a1281fd).
3. **arif_init binding (arifOS)** — `SessionManifest.model_governance` field; card
   attached at all arif_init `_sm` returns + post-strip projection. **CLOSED
   2026-10-31T10:0x+08:00 (arifOS@84efcec47):** the last-mile wrapper was
   `trim_for_verbosity` minimal mode (verbosity.py `_SEMANTIC_PRESERVED_FIELDS`);
   the card now joins the preserved set. Wire canary proof: actor QWEN → card
   PRESENT on the HTTP envelope, `card_hash` byte-identical to the compiled
   projection (a39b54df8639…); unmapped actor → explicit UNKNOWN card with zeroed
   ceiling, never silent omission.

## Laws carried into runtime

- `REALITY > EVERYTHING`: OBSERVED > DECLARED > REQUESTED; IMAGINED forbidden.
- The card may LOWER confidence; NEVER raise authority (`authorize` is false on
  every card, always).
- Fail-closed: card source unavailable → explicit UNKNOWN payload + zeroed ceiling;
  INIT never fabricates identity from the requested alias.
- Card is revision-bound; immutable within session; no silent hot-reload (refresh =
  witnessed transition: old/new card hashes, changed fields, reason, receipt).
- MCP scope: this wiring uses the three server primitives (resource, prompt, tool) —
  a mission-scoped projection, not a protocol-exhaustive claim.

## Producer context (boundary statement, Phase 5)

Full chain: INIT card → model invocation binds card hash → output producer_context →
tool invocation inherits → A-FORGE receipt binds → memory writer persists.
**This mission wired the INIT end only.** No producer_context binding exists yet on
invocation envelopes, A-FORGE receipts, or memory writes — that is the next brief's
work; nothing here claims it.

## A2AReality reference slot

`UNKNOWN_SOURCE_UNRESOLVED` (404 both branches + API miss, probed 2026-10-30).
NOT substituted with a2aproject/A2A. Falsifier: repo reachable or F13 pointer.
The REALITY ladder stands on the sovereign doctrine line, not on that repo.

## Known scars from this deploy (receipted in arifOS history)

- deploy-release lease ABI drifted (--session required, acquire AND release) — fixed.
- Multiple stamp surfaces (releases/deployed-commit, app/.git_commit, repo .git_commit,
  kanon version) can disagree after a partially-blocked deploy — all synced by hand
  this run; consolidation is DEBT.
- Bulk line-patching truncated session.py once (function-end misdetected) — recovered
  from 70c517a65 in-commit; AST-bounded rewrites are the rule from now on.
