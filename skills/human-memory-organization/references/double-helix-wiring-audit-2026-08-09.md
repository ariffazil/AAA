# Double-Helix Memory — Wiring Audit (2026-08-09)

Question answered this session: "Is my Hermes agent and other agents wired to the double helix memory?"
**Answer: NO — the helix is forged (doctrine + files) but NOT wired into any agent runtime.**

## What exists (verified on disk)

| Layer | Location | State |
|---|---|---|
| Doctrine | `/root/forge_work/DOUBLE_HELIX_2026-08-08.md` | Reflection, pointer-only (NOT a floor/law) |
| Left-strand scaffold | `/root/.local/share/arifos/scars/` — SCAR-000.json, schema.json, index.json, receipt_extension.json, verify_scar.py | Executed 2026-08-08 11:54 |
| Scar registry | `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` — 6 scars (SCAR-000, Lebah Emas, Rightsizing, Unheard, MakcikGPT, Memory Doctrine V1) | All verified 2026-08-08T20:24 |

## What is NOT wired (the gap — verified with grep/counts)

| Path | Evidence |
|---|---|
| Kernel runtime | `orchestrator.py` + `memory.py`: **zero** scar/helix references. `arif_memory` has 0 scar contact. |
| Seal path | VAULT999 `outcomes.jsonl` = **43,886 receipts, 0 with `meaning_anchor`, 0 with `scar_lineage`** — the receipt_extension.json schema was never attached to sealing. |
| Hermes | No scar tool, no scar registry access. Hermes memory holds scar *content* (from 2026-08-08 conversation) but that is Hermes memory, not the helix pathway. |
| OpenCode / OpenClaw | No scar/helix reference in AGENTS.md / configs. |
| Only live contact | `arifosmcp/tools/heart.py` reads a scar taxonomy as advisory F5/F6 substrate context (`_read_arif_substrate`, `_check_vault999_scar_tissue`) — advisory only, not a memory pathway. |

Gap ledger (authoritative, forged 2026-08-08): `/root/forge_work/2026-08-08-double-helix-convergence/FINAL_GAP_LEDGER.md`
- `LEFT_STRAND = PARTIAL (6/13 FULL)`, `RIGHT_STRAND = HEALTHY`, `COUPLING = PARTIAL (7/13 STRONG, 4 WEAK, 2 BROKEN: F3 + F5)`
- Overall verdict: **HOLD** — Gap 6 (H5 Scars Witness) = SOVEREIGN_WAIT: "scar pipeline ready, F13 must witness"

## What wiring would take (T1, reversible, ~1 day, all additive)

1. **Kernel:** expose `scar_read(scar:<id>)` + `scar_index()` as advisory tools in `arif_memory` — respects H5 sovereignty gate (never auto-reads content).
2. **Seal path:** attach `meaning_anchor` + `scar_lineage` as additive fields at `arif_seal` time (extension schema already exists, backward-compatible).
3. **Hermes/OpenCode:** point to the scar registry as doctrine reference so the helix is in-context.

Do NOT: modify F1–F13, modify L1–L6, read scar content uninvoked, or create new databases/agents. The doctrine itself says "no new floors, no new laws, no spawned agents — one problem, one patch, one day."

## Key doctrine anchors

- "Law without witness is a corpse" — scar pipeline complete but unwitnessed = Gap 6.
- "VAULT999 records reality AT THE MOMENT OF SEAL — benar secara forensik, palsu secara temporal."
- Registry rule: registry is the index, scar files are the content, never merged. `meaning_anchor` (one line) may live in registry; full testimony requires `scar:<id>`.

DITEMPA BUKAN DIBERI.
