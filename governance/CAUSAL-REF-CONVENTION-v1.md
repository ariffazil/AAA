# CAUSAL-REF CONVENTION v1 — cross-artifact reference field

> **Status:** ACTIVE convention (2026-09-12) — operationalizes U11 of FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 (F13_RATIFIED_CHAT) · Gate-2 item 4, additive layer
> **Resolver:** `scripts/causal_spine.py <ref>` — 1-hop reconstruction across git (AAA/scripts/arifOS), AAA tracked content, UL lane, seal chain, forge_work.
> **Origin:** generalizes the INV-4 `cc_id` contract (A-FORGE mutations) to every receipt-bearing surface.

## The field

Every receipt, ledger entry, or governance artifact that references another artifact carries:

```json
"refs": [{"kind": "<class>", "ref": "<id>"}]
```

Kinds: `git_commit` · `ul_entry` · `flow_receipt` · `seal_receipt` · `vault_receipt` · `review_sha` · `chat_instrument` · `artifact`.

## Where it lands (tonight, no schema changes)

- **arifFlow FlowReceipts**: structured `payload.refs` — agents include it on every ingest from now on (payload is free-form; convention needs no daemon change).
- **UL lane**: `--refs kind:ref,kind:ref` on `unratified_lessons.py append`; tool builds the structured list.
- **Git commit bodies**: keep citing raw ids in prose (resolver already indexes these).

## Where it needs kernel work (scoped, NOT tonight)

Per UL-007 next_action ("do NOT cascade into 2026-09-12 night") — kernel + arifFlow schema generalization is scoped to the kernel lane:
1. `cc_id` promoted from MUTATE-class-only to ALL forge receipt classes.
2. `refs` as a first-class field in the arifFlow ingest schema (queryable, not payload-borne).
3. arifFlow receipt ledger exposed to read queries (storage location unprobed from FI-003 seat tonight — resolver declares this layer UNKNOWN, per Claim Layer = Evidence Layer).

## The U11 falsifier (acceptance test)

An independent party, given ONE seed reference, reconstructs the governed transaction without manual multi-artifact forensics:

```
python3 scripts/causal_spine.py UL-011   → neighbors across git + lane + review + protocol
python3 scripts/causal_spine.py ae2c1bb  → reverse direction
```

Exit 1 = ISOLATED (seed exists only in its own artifact) — that is a U11 gap signal, not an error.
