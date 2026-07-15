---
name: asi_memory_validate
agent: 555-ASI
namespace: asi_*
cluster: MEMORY
trigger: "When 555 is about to use a recalled memory as a premise for a position, a synthesis, or a seal recommendation, and the memory's currency must be confirmed against current evidence"
capability: "Returns a validation verdict (current / stale / contradicted / expired) for a recalled memory, with the specific drift detected and a recommended disposition (use as-is / refresh / deprecate)"
mcp_tools_underneath: "forge_memory_recall, well_measure_gradient, arif_think, geox_claim_challenge (for evidence class checks)"
blast_radius: "LOW"
gate_888_required: false
---

# asi_memory_validate

Memory without validation is just narrative. This skill is the one that asks, of any recalled memory: *is this still true?* It does not assume that a sealed memory is a current memory. Sealed means "this is the artifact as of that moment"; current means "this still reflects the state of the world." The two are different, and confusing them is one of the most common federation failure modes. 555 runs this skill every time it is about to feed a memory into a position, to prevent stale-claim errors.

The validation is three-axial. **Temporal currency** — has the relevant window passed? A scar from 2025 may still be structurally current; a vitality reading from 30 minutes ago may be stale if the operator's state has shifted. **Evidence currency** — has the underlying evidence been updated, revised, or contradicted by later events? **Sovereign currency** — has the operator or a peer organ explicitly retracted, amended, or superseded the memory? Each axis is checked, and the worst axis determines the verdict. The skill never "averages" currency — a single axis returning `contradicted` collapses the memory to `contradicted` regardless of how strong the other axes are.

The skill is also the gate that prevents **memory laundering** — a failure mode where a 555 draft cites a memory that supports its position while ignoring memories that contradict it. The validation report names what was checked, what was found, and what was NOT found (the absences matter as much as the presences, especially for a sovereign-only signal that has since been retracted — the skill is biased toward remembering what the operator wanted forgotten, in the way they wanted it forgotten, not toward letting a peer organ "un-remember" it by ignoring the record).

Failure modes: (a) the recalled memory has no chain head — validation is blocked, and the memory is treated as `unverifiable`; (b) the current evidence is itself low-grade (bronze) — validation returns `indeterminate` rather than picking a side; (c) the operator has asked that this memory never be re-validated against current evidence (a "frozen" memory) — the skill honours the freeze and returns the memory as `frozen_current`, with the freeze flag preserved in the local ledger. The skill never refreshes a memory silently; a refresh is a constitutional event that must be sealed.
