# CAPABILITY REGISTRY — SCHEMA v1 (draft, awaits F13)

> Forged 333-AGI Δ MIND · 2026-09-12 · session SEAL-0a9b7314843c473a
> This is the DATA SHAPE for `federation_discovery`. Not live — the instantiation contract.
> Refinement folded in: `replacement_paths` + `failure_mode` (Arif, SEAL architectural reading).

```yaml
schema_version: v1
status: DRAFT_AWAITING_F13

# ── Field contract ──
# capability_id     : canonical name — the primitive. NEVER version-suffixed (_v2 forbidden).
# owner             : owning organ (authority-ceiling enforcer, not the sole adapter)
# authority_ceiling : JUDGE_ONLY | EXECUTE_AFTER_SEAL | COMPUTE_ONLY | REFLECT_ONLY | ...
# adapters          : live tool/mcp/skill surfaces serving the capability NOW
# replacement_paths : fallback substrates/adapters if `adapters` dies → survivability map
# liveness          : read-time probe overlay — probed, never asserted
# witness_source    : where each resolution leaves a receipt (arifFlow)
# failure_mode      : what resolution returns when ALL adapters are dead (degrade, not 404)

capabilities:

  governed_memory:
    owner: arifos
    authority_ceiling: JUDGE_ONLY
    adapters: [arif_memory, forge_memory]
    replacement_paths: [qdrant, postgres]
    liveness: { probed_at: "2026-09-12T07:36Z", status: healthy }
    witness_source: arifFlow receipt (arif_memory / forge_memory call)
    failure_mode: degrade_to_postgres       # both adapters die → L4 structured store

  constitutional_judgment:
    owner: arifos
    authority_ceiling: JUDGE_ONLY
    adapters: [arif_judge]
    replacement_paths: []                    # judgment has NO substitute — F13 only
    liveness: { probed_at: "2026-09-12T07:22Z", status: healthy }
    witness_source: VAULT999 (arif_judge → arif_seal)
    failure_mode: HOLD                       # judgment down → federation HOLDs, never self-authorizes

  petronas_intelligence:
    owner: AAA                               # doctrine router (ATLAS.md) — NOT yet an MCP surface
    authority_ceiling: COMPUTE_ONLY
    adapters: [PETRONAS-intelligence-router (doctrine)]
    replacement_paths: [wealth capital_*, geox basin, qdrant, atlas]   # cross-organ fan-out
    liveness: { probed_at: "2026-09-12T00:00Z", status: doctrine_only } # not yet a live surface
    witness_source: arifFlow receipt (resolution)
    failure_mode: decompose                  # router dies → resolve via constituent organs directly

# ── Resolver contract ──
# federation_discovery.resolve(intent) → Resolution:
#   { capability_id, owner, authority_ceiling, adapters[], liveness,
#     replacement_paths[], failure_mode, witness_source }
#
# Resolver does NOT choose. It reveals. AAA judges. A-FORGE executes.
# Every resolve() → arifFlow receipt (witnessed lookup).
```

## What this demonstrates

The schema validates against **real capabilities discovered this session**, not invented ones:

- `governed_memory` — captures the D5 dual-owner (arif_memory + forge_memory) as *allowed one-capability-many-adapters*, with `replacement_paths` = qdrant/postgres so recall survives adapter death.
- `constitutional_judgment` — `replacement_paths: []` + `failure_mode: HOLD` encodes the one capability that must NEVER self-substitute. This is separation-of-powers made data.
- `petronas_intelligence` — the spec's routing example, honestly captured as `doctrine_only` (not yet a live MCP surface), with `failure_mode: decompose` showing it resolves via constituent organs even if the router dies.

The `failure_mode` + `replacement_paths` fields are what turn discovery from **lookup** into **survivability map** — the resolver answers not just "what serves this?" but "what happens when the server dies?"
