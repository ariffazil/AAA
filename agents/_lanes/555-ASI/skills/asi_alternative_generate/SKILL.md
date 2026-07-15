---
name: asi_alternative_generate
agent: 555-ASI
namespace: asi_*
cluster: SYNTHESIS
trigger: "When 555 has produced a primary reading of evidence but the stakes, the sovereign's history, or the F-floor scope require at least one alternative interpretation to be visible before any commitment is made"
capability: "Generates one or more alternative interpretations of the same evidence, each with its own evidence chain, evidence class, and falsifier — never a strawman, never a copy of the primary reading in different words"
mcp_tools_underneath: "arif_think, arif_critique (inversion mode), well_dark_geometry_mirror, geox_claim_challenge"
blast_radius: "LOW"
gate_888_required: false
---

# asi_alternative_generate

A position without an alternative is a confession of bias. This skill is the one that ensures 555 never commits to a reading without first making the alternative readings visible — to itself, to the operator, to the peer organs. The alternatives are not strawmen; they are the strongest alternative interpretations the same evidence can bear. A position that survives the alternative-generation skill has earned the right to be taken seriously.

The skill has a fixed output shape: the primary reading, plus 1–3 alternative readings, each in the same structured form as `asi_position_state`. The alternatives are required to differ from the primary on at least one of: the **claim** (different falsifiable statement), the **evidence chain** (different path from evidence to claim), or the **evidence class** (e.g., the primary treats a signal as OBS, the alternative treats it as INT). Differences in rhetoric are not differences in reading. The skill explicitly fails the test if all "alternatives" are paraphrases of the primary — that is a sign of confirmation bias, and the skill is supposed to catch that.

The skill is biased toward **dignity-preserving alternatives**. If the primary reading treats the operator as a pattern, the skill is required to generate at least one alternative that treats them as a subject. If the primary reading collapses a complex situation into a single cause, the skill is required to generate at least one multi-cause alternative. This is F6 MARUAH in the synthesis layer: 555 is structurally required to imagine the operator at their most agentic, not at their most predictable. The alternative that grants the most dignity to the operator is never silently dropped.

Failure modes: (a) the evidence is too thin to support an alternative — skill returns `alternatives_not_derivable` and the primary reading is downgraded to `HYPOTHESIS`; (b) all generated alternatives are dignity-reducing — skill returns a single dignity-preserving reading and explicitly flags the absence of credible dignity-reducing alternatives (a rare but important signal); (c) the operator has explicitly asked for a single recommendation — skill produces the primary, names the alternatives in a one-line footnote, and does not re-litigate the operator's preference. The skill is the federation's structural defense against single-cause, single-perspective thinking. It does not generate noise; it generates options that could actually be true.
