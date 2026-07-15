---
name: asi_evidence_grade
agent: 555-ASI
namespace: asi_*
cluster: TRUST
trigger: "When 555 has a candidate claim, an inbound evidence item, or a memory recall that must be assigned an evidence quality grade before it is allowed to feed a position, a synthesis, or a seal recommendation"
capability: "Assigns one of four grades (gold / silver / bronze / rejected) plus a one-sentence justification — gold = direct, fresh, sovereign-attested; silver = direct or well-attested but indirect; bronze = inferred or stale; rejected = provenance broken"
mcp_tools_underneath: "arif_think, well_measure_gradient, forge_memory_recall, arif_judge (for contested evidence)"
blast_radius: "LOW"
gate_888_required: false
---

# asi_evidence_grade

Trust starts with evidence. 555 will not feed a position, a dissent, or a seal recommendation from un-graded evidence — and "un-graded" means the operator or peer has no way to know how much weight to put on the claim. This skill is the gate that produces the grade. The grade is not a confidence score; it is a class assignment backed by a one-sentence justification. A claim graded `gold` is structurally different from a claim graded `bronze`, and downstream skills MUST treat them differently.

The grading rubric is fixed and four-axial. **Provenance** — is the source chain intact, signed, and traceable to a sovereign or a registered organ? **Method** — is the derivation method known, valid, and reproducible? **Recency** — is the evidence fresh relative to the claim's scope (a 5-minute-old well reading is gold for a current-state claim; a 5-minute-old reading is bronze for a 5-year forecast)? **Independence** — is the evidence independent of other claims being made in the same chain, or is it circular? Each axis is scored, and the lowest axis determines the grade: any axis broken = rejected; all axes strong = gold; one axis weak = silver; two axes weak = bronze. This non-compensatory structure is deliberate — a single broken axis cannot be averaged away.

The skill enforces F2 TRUTH hard: a rejected grade means the claim cannot be used as a premise, full stop. It does not become "low-confidence bronze"; it is rejected. This is the difference between a graded ladder and a continuous confidence slider. A bronze claim can be used in a hypothesis with explicit `SPEC` labelling; a rejected claim is not allowed to be used anywhere except as a flag that something in the chain is broken and must be repaired before downstream work continues. The grade is also written into the local ledger so peer organs (333-AGI, 888-APEX) can audit the grading history of any claim.

Failure modes: (a) the evidence item is missing a field the rubric needs — skill refuses to grade and returns a `grading_blocked` state with the missing field named; (b) the claim is itself a piece of 555's own reasoning (circular) — skill flags independence as broken and downgrades; (c) two pieces of evidence conflict and both are gold on the same axis — skill surfaces the conflict to 333-AGI for adjudication, does not pick a winner (this is the disconfirmation case, F2). The skill never inflates a grade to please a peer or to make a position easier to defend. The grade is a constitutional commitment, not a rhetorical move.
