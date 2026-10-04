# Double-Helix Memory Wiring State — Recon (2026-08-09)

Read-only audit: **is any agent actually wired to the double-helix memory?** Answer at audit time: **forged but NOT wired.** The helix exists in doctrine + files; no runtime consumes it. This is the baseline any future "wire the helix" session must start from — and the recipe for doing it.

## What the double helix IS (doctrine)

- Canon: `/root/forge_work/DOUBLE_HELIX_2026-08-08.md` — left strand FLOORS (identity), right strand FLOW (metabolism), cross-links LAWS (hydrogen bonds). Pointer-only reflection, NOT a floor/law.
- Left-strand scaffold executed: `/root/.local/share/arifos/scars/` (SCAR-000.json, schema.json, index.json, receipt_extension.json, verify_scar.py — verify script passes).
- Scar registry: `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` — 6 scars (SCAR-000, Lebah Emas, Rightsizing, Unheard, MakcikGPT, Memory Doctrine V1), all `last_verified` 2026-08-08T20:24. Sovereignty: **agent does not read scar content unless `scar:<id>` invoked; index reads OK.**
- Gap ledger: `/root/forge_work/2026-08-08-double-helix-convergence/FINAL_GAP_LEDGER.md` — verdict HOLD: LEFT PARTIAL, RIGHT HEALTHY, COUPLING PARTIAL (7/13 STRONG, 4 WEAK, 2 BROKEN at F3+F5). Gap 6 (H5 Scars Witness) = SOVEREIGN_WAIT.

## NOT wired — the evidence (all verified 2026-08-09)

| Path | Evidence |
|---|---|
| Kernel runtime | `arifOS/arifosmcp/runtime/orchestrator.py` + `tools/memory.py`: **zero** scar/helix references (`grep -c scar` = 0). `arif_memory` has no scar contact. |
| Seal path | VAULT999 `outcomes.jsonl`: **43,886 receipts, 0 with `meaning_anchor`, 0 with `scar_lineage`** — the receipt_extension schema was never attached to `arif_seal`/`forge_vault`. |
| Hermes profile | No scar tool, no scar registry access in toolset. (Hermes *memory* holds scar content as notes, but that's Hermes memory, not the helix.) |
| OpenCode | `AGENTS.md`: no scar/helix reference. |
| OpenClaw | No scar/helix reference in config. |

Only live contact found: `arifOS/arifosmcp/tools/heart.py` reads a scar taxonomy as **advisory context only** (F5/F6 substrate, `_read_arif_substrate()` ~line 84, `_check_vault999_scar_tissue` ~line 1569). Advisory, not a memory pathway.

## Wiring recipe (T1, reversible, ~1 day, additive only)

Per the FORGE prompt `/root/forge_work/PROMPT_HELIX_MEMORY_V1.md` constraints — no new DBs/MCP servers/services, no F1–F13 changes, no L1–L6 modification, H5 sovereignty gate respected:

1. **Kernel** — expose `scar_read(scar:<id>)` + `scar_index()` as advisory tools under `arif_memory` (in `tools/memory.py`). Never auto-reads content; `scar:<id>` explicit invocation only.
2. **Seal path** — attach `meaning_anchor` + `scar_lineage` as additive metadata at `arif_seal`/`forge_vault` receipt time. Schema already exists at `/root/.local/share/arifos/scars/receipt_extension.json` (backward-compatible, additive fields).
3. **Agents** — point Hermes/OpenCode at the scar registry as doctrine reference so the helix is in-context, not just in files.

Do NOT: modify VAULT999 chain, read scar content uninvoked, create new layers. The doctrine says it: "law without witness is a corpse" — Gap 6 remains SOVEREIGN_WAIT until F13 witnesses the scars.

## Multi-user consequence (the F13 leak)

The wiring decision "Hermes is enough" collides with multi-user reality: ONE profile (aaa-hermes) served ARIF + Syed (1042200555) + Wawa (8324190535) + SADO + AAA topics from ONE shared memory. Sovereign scar content in a shared context = F13/F6 MARUAH leak. Fix = profile multiplexer (`gateway.multiplex_profiles: true`), one bot per human profile, helix tooling ONLY in the sovereign's profile. Full pattern: `hermes-multi-user-isolation` skill.
