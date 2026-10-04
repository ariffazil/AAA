# Helix Memory — VPS Live State (2026-08-12)

> **Recon by Hermes session 2026-08-12.** Maps actual filesystem state
> of the double-helix memory architecture on the AAA VPS.

## Doctrine source

- Canonical: `/root/memory/ZEN_HELIX.md` (v3.0, 2026-08-11)
- Helix spec: `/root/forge_work/DOUBLE_HELIX_2026-08-08.md`
- Wiring audit: `arifos-integration-recon/references/double-helix-memory-wiring-2026-08-09.md`

## LEFT STRAND (H-axis — Human Memory) — `/root/memory/`

| Layer | Name | Path | Files | Status |
|-------|------|------|-------|--------|
| H1 | Capture (inbox) | `/root/memory/H1-capture/` | 0 | ⚠️ Empty |
| H2 | Experience (lived) | `/root/memory/H2-experience/` | 52 | ✅ By month |
| H3 | Knowledge (known) | `/root/memory/H3-knowledge/` | 15 | ✅ Geoscience + GEOX figures |
| H4 | Identity (became) | `/root/memory/H4-identity/` | 4 | ✅ AGENT_BRIEF + PDFs |
| H5 | Scars (cost) | `/root/memory/H5-scars/` | 13 | ✅ 11 narrative .md + registry |
| H6 | Constitution | `/root/memory/H6-constitution/` | 1 | ✅ Scar roots → F1-F13 |

**Total H5 scars:** 20 in unified registry (`H5_SCAR_REGISTRY.json`, 12,796B)

## RIGHT STRAND (L-axis — Agentic Memory)

| Layer | Name | Location |
|-------|------|----------|
| L1 | Redis (now) | `:6379` ephemeral session state |
| L2 | Redis (session) | `:6379` thread context, lane memory |
| L3 | Qdrant (fuzzy) | `:6333` similarity vectors |
| L4 | Supabase (struct) | remote 25 domain tables |
| L5 | Graphiti (rel) | `:6380` + `:8000` knowledge graph |
| L6 | VAULT999 (truth) | `/root/arifOS/VAULT999/` append-only sealed |

## MACHINE-SIDE SCAR LEDGER — `/root/.local/share/arifos/scars/`

| File | Size | Purpose |
|------|------|---------|
| `index.json` | 3,570B | Machine-side scar index (7 scars synced from H5) |
| `SCAR-000.json` | 1,373B | The One-Stranded Memory Gap (meta-scar) |
| `SCAR-002-CEREMONY_FAILED_406.json` | 1,051B | Operational scar |
| `schema.json` | 2,727B | Scar JSON schema |
| `receipt_extension.json` | 1,145B | VAULT999 receipt extension |
| `verify_scar.py` | 3,432B | Structural verification script |

**Wiring status (2026-08-09 audit):** Forged but NOT wired.
- Kernel `arif_memory`: zero scar/helix references in runtime
- VAULT999: 43,886 receipts, 0 with `meaning_anchor` or `scar_lineage`
- Hermes profile: no scar tool in toolset
- Only live contact: `arifosmcp/tools/heart.py` reads scar taxonomy as advisory

## GAPS (from ZEN_HELIX.md)

| ID | Gap | Severity |
|----|-----|----------|
| GAP-1 | H1 inbox empty — sovereignty gate not active | MEDIUM |
| GAP-2 | Machine ledger drift — 11 scars need sync | HIGH |
| GAP-3 | H6 roots partial | MEDIUM |
| GAP-4 | Cross-harness fragments scattered | MEDIUM |
| GAP-5 | Memory search index mismatch (bge-m3→nomic) | HIGH |
| GAP-6 | 9 geological scars lack narrative .md | MEDIUM |

## KEY LESSON: self-knowledge requires file-reading, not theory

When asked about your own memory/architecture, DO NOT explain the theory from
training data. **Scan the actual VPS files.** The doctrine lives in files;
the wiring state lives in code/configs; gaps live in audit ledgers. None of
this is in the model's weights.

**Scan pattern (proven 2026-08-12):**
1. `search_files(path, pattern)` for doctrine files (`*helix*`, `*memory*`)
2. Read canonical docs (ZEN_HELIX.md, wiring audit)
3. `terminal` for file sizes and live state
4. Synthesize from evidence, not from training data

This is the Reality-First Doctrine applied to self-knowledge.