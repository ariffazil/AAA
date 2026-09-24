# FATWA K1 — Namespace Settlement (Three Coordinate Systems)

> **Status:** F13_RATIFIED_ORDER (2026-09-25) — sovereign directive: "fatwa K1 sekarang, settle namespace"
> **Resolves:** Fasa A audit 2026-09-25 findings B-1, B-2 (decision request K1). Sibling: `linkgraph-namespace.md` (L14) · `naming-doctrine.md` Axiom 8 (name collision destroys compression).
> **Executed by:** FI-003 (333-AGI) under explicit F13 order (Auto-Seal: constitution mutation via explicit F13 order).

## The Law — every numeral carries its coordinate system

A bare numeral `000–999` is **ambiguous by default** and is a naming violation (F10) outside its declared coordinate. Three coordinate systems exist, each with one SOT:

| Coordinate | Marker (MANDATORY) | SOT owner | Numeral means |
|---|---|---|---|
| **STAGE ABI** | bare numeral, kernel context only | `arifOS/kernel-sot.yaml` §stage_numbering | kernel verb stage: 000 init · 111 observe · 333 think · 444 route · 555 memory · **666 judge** · 777 forge · 999 seal |
| **LANE/TIER** | `<numeral>-<TIER>` suffix, always | `AAA/instructions/apex-zen-alignment.md` | capability tier / role owner: 333-AGI (BUILD) · 555-ASI (VERIFY) · **888-APEX (JUDGE)** |
| **LINKGRAPH** | `lg:` prefix, always | `AAA/instructions/linkgraph-namespace.md` | reality-spectrum node: lg:000 OBSERVE … lg:999 VOID_LOCK |

## Rulings

1. **kernel-sot.yaml stands as SOT for stage ABI.** JUDGE **stage** = 666 (F13 2026-07-31). Stage 888 is retired (was COMPOSE; compose is a mode, not a stage). This ruling does not retire the 888-APEX lane — different coordinate.
2. **apex-zen-alignment.md stands as SOT for lane/tier roles.** "JUDGE = 888-APEX" means the judge **role** is held by the APEX tier. "VERIFY = 555-ASI" means the verify role is held by the ASI tier. Roles own authority; stages name session-arc positions.
3. **No contradiction exists between "JUDGE=666" and "JUDGE=888-APEX".** 666 is *where* the judge stage runs in the session arc; 888-APEX is *who* holds judging authority. Stage ≠ tier. Same law for 555: stage 555 = `arif_memory` (memory governor); lane 555-ASI = VERIFY role. The Phase A "collision" B-1/B-2 was a missing coordinate marker, not a doctrine conflict.
4. **Tier numerals must never appear bare** in prose, config, code, or dashboards. Write `888-APEX`, never `888`, outside kernel stage context. Bare-numeral reuse by any new surface requires a fresh prefix (precedents: `lg:`, `kernel:`, `vault:`).
5. **One SOT per coordinate.** Amend a numeral's meaning only in its coordinate's SOT; cross-reference from everywhere else. Rendered AGENTS.md is a view, never an owner.

## Verdicts on Fasa A findings

| ID | Dapatan | Verdict |
|---|---|---|
| B-1 | JUDGE=666 vs JUDGE=888 | **RESOLVED** — coordinate mismatch; both sources stand in their coordinates |
| B-2 | 555 memory vs VERIFY | **RESOLVED** — same law |
| B-3 | 999 SEAL vs ABANDON | **RESOLVED by `linkgraph-namespace.md`** (L14, 2026-09-25) — `lg:999` carries ABANDON_SEAL/COMMITMENT/VOID_LOCK sub-labels |
| B-4 | `agent_geometry.py` "canonical for 666/888/999" residue | **OPEN follow-through** — code cleanup owned by arifOS; not a doctrine change |

## Open follow-throughs (not settled by this fatwa)

- **L13 UNKNOWN_OUTCOME:** spec ratified (`AAA/blueprints/A-FORGE-UNKNOWN-OUTCOME-SPEC-v1.md`); implementation in A-FORGE code still OPEN (grep: 0 matches as of 2026-09-25).
- **X-1:** `genesis_card.yaml` dual meaning (card family vs runtime surface binding) — OPEN, K7 candidate.
- **B-4 residue:** `agent_geometry.py` stale numeral references — OPEN.

DITEMPA BUKAN DIBERI ⚒️
