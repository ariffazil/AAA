# DREAMMODE_BLUEPRINT.md

## Overview
DreamMode v1 is a **reversible, extractive summarization prototype** that:
- Reads the last 24 h of VAULT999 entries, MEM episodic logs, and WELL snapshots.
- Produces a **draft_dream_summary** (extractive only — no generative hallucination).
- Writes the draft as a **dream_summary** VAULT entry with full lineage.
- Immediately seals the entry.
- No deletions, compaction, or policy changes.

## Constitutional Constraints (Floors)
- **F01 AMANAH**: Reversible by design; original records untouched.
- **F02 TRUTH**: Extractive summarization preserves factual fidelity; uncertainty bands added.
- **F05 PEACE²**: Dignity‑preserving; no invasive inferences.
- **F06 EMPATHY**: Surface only patterns already evident; no new claims about individuals.
- **F07 RAHMAH**: No zero‑sum harms; summary is additive.
- **F09 ANTIHANTU**: No anthropomorphizing; labeled as extractive.
- **F11 AUTH**: Blueprint stored under the current session (actor_id 267378578) for audit.
- **F13 SOVEREIGN**: No sovereign action taken; only documentation.

## Inputs
1. **VAULT999** – entries from the last 24 h (JSON lines).
2. **MEM** – episodic logs from the last 24 h (plain text).
3. **WELL** – snapshots from the last 24 h (JSON).

## Processing Steps (Extractive Only)
1. **Collect** raw records from each source.
2. **Deduplicate** identical excerpts across sources.
3. **Cluster** similar excerpts into themes using simple keyword matching (no ML).
4. **Rank** themes by frequency and recency.
5. **Generate** bullet points:
   - **Major themes** (top 5).
   - **Candidate conflicts** (pairs of excerpts that contradict).
   - **Important memories** (high‑confidence excerpts flagged for possible pinning).
6. **Add uncertainty bands** (e.g., `confidence: 0.92`).
7. **Format** as a single `dream_summary` VAULT entry.

## Output
- **VAULT entry type:** `dream_summary`
- **Fields:** `summary_text`, `themes`, `conflicts`, `important_memories`, `source_lineage`, `confidence_bands`, `timestamp`, `session_id`.
- **Sealing:** Immediate `GEOX__geox_claim_seal`‑style seal (or equivalent arifOS vault seal) to make immutable.

## Reversibility
- **Original VAULT999/MEM/WELL records remain unchanged.**
- **Only an additive summary is written; no deletions or modifications.**
- **If needed, the `dream_summary` entry can be removed by a later reversible action (e.g., “undo dream summary”).**

## Audit & Lineage
- Each source record referenced in the summary includes a `source_id` field.
- The `source_lineage` array lists all `source_id`s used to build the summary.
- All steps are logged in `MEMORY.md` for transparency.

## Future Extensions (when kernel routing is stable)
- Replace simple clustering with a **structured extractive summarizer** that respects F02 TRUTH.
- Add a **manual trigger** via AAA UI to run the pipeline on demand.
- Automate sealing and lineage capture via arifOS tools.

Signed off by: MiniMax‑M3 (constitutional worker)  
Date: 2026‑06‑06