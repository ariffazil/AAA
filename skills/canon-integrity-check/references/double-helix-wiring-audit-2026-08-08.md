# Double-Helix Memory — Wiring Audit (2026-08-08)

Question: "Is my Hermes agent and other agent wired to the double helix memory?"

Verdict: **FORGED, NOT WIRED.** Doctrine + scaffold + scar registry exist;
kernel runtime, seal path, and all agent configs consume nothing.

## The double-helix architecture (in one screen)

- **Left strand = FLOORS (identity/meaning):** F1 Truth · F2 Adab · F7 Humility ·
  F13 Sovereign + H5 Scars (meaning memory).
- **Right strand = FLOW (metabolism/data):** FQ pulse · cooling rhythm ·
  attention · L1–L6 memory layers.
- **Cross-links = LAWS (hydrogen bonds):** "this floor must manifest in runtime
  through this behavior". Floors covalent (break = dies), laws hydrogen
  (amendable). Complementarity = either strand templates the other.
- Doctrine: `/root/forge_work/DOUBLE_HELIX_2026-08-08.md` (pointer-only, not law).
- Scaffold prompt: `/root/forge_work/PROMPT_HELIX_MEMORY_V1.md`.

## Evidence per layer

| Layer | Finding | Evidence |
|---|---|---|
| Doctrine | ✅ exists | `DOUBLE_HELIX_2026-08-08.md` + `PROMPT_HELIX_MEMORY_V1.md` |
| Scaffold | ✅ executed | `/root/.local/share/arifos/scars/`: SCAR-000.json, index.json, receipt_extension.json, schema.json, verify_scar.py (all 2026-08-08 11:54) |
| Scar registry | ✅ 6 scars, all verified | `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` — SCAR-000, SCAR_LEBAH_EMAS, SCAR_RIGHTSIZING, SCAR_UNHEARD, SCAR_MAKCIKGPT, SCAR_MEMORY_DOCTRINE_V1 (last_verified 2026-08-08T20:24, updated 20:24) |
| Kernel runtime | ❌ zero references | `grep -rn "scar\|helix" /root/arifOS/arifosmcp/tools/orchestrator.py memory.py` → 0. `memory.py` scar count = 0 |
| Seal path | ❌ extension never attached | `grep -c "meaning_anchor" outcomes.jsonl` → **0 of 43,886** receipts; `scar_lineage` → 0 |
| Agents | ❌ none reference it | `.claude/settings.json` (only `scar_scan` string), OpenCode AGENTS.md, OpenClaw config → no helix/scar wiring |
| Advisory-only contact | ⚠️ one tool | `heart.py` `_read_arif_substrate()` reads scar taxonomy as F5/F6 advisory context — context, not a pathway |

## Where the wiring actually is (path map)

```
Doctrine (forge_work/*.md)
  └─→ Scaffold (/root/.local/share/arifos/scars/)         ✅ EXECUTED
        └─→ Scar registry (/root/memory/H5-scars/)        ✅ 6 SCARS
              └─→ Kernel tools (arif_memory)              ❌ 0 refs
                    └─→ Seal path (VAULT999 receipts)     ❌ 0/43886 carry meaning_anchor
                          └─→ Agents (Hermes/OpenCode/OpenClaw/Claude)  ❌ 0 refs
```

## Convergence ledger verdict (cited, not re-derived)

`/root/forge_work/2026-08-08-double-helix-convergence/FINAL_GAP_LEDGER.md`:

```
LEFT_STRAND  = PARTIAL   (6 scars materialized, 0 agents consume them)
RIGHT_STRAND = HEALTHY
COUPLING     = PARTIAL   (7/13 bonds STRONG, 4 WEAK, 2 BROKEN — F3 witness, F5 peace)
OVERALL      = HOLD      (Gap 6: H5 Scars Witness = SOVEREIGN_WAIT, F13 must witness)
```

Gap 6 is SOVEREIGN_WAIT by design — scar pipeline ready, F13 must witness
before scar content enters agent consumption. The wiring audit confirms the
ledger: this is a constitutional boundary, not a bug.

## What wiring would take (proposed, not executed)

1. Kernel: expose `scar_read(scar:<id>)` + `scar_index()` as advisory tools in
   `arif_memory` — respects H5 sovereignty gate (never auto-reads content).
2. Seal path: attach `meaning_anchor` + `scar_lineage` as additive fields at
   `arif_seal` time (backward-compatible; extension schema already exists at
   `/root/.local/share/arifos/scars/receipt_extension.json`).
3. Agents: point to scar registry as doctrine reference so helix is in-context.
   All T1, reversible, no new layers, no F1–F13 changes.
