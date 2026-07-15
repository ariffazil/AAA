---
name: asi_signal_weight
agent: 555-ASI
namespace: asi_*
cluster: INTAKE
trigger: "When 555 receives two or more signals about the same proposition and must decide which to trust more — for example, a well_classify_state reading and a text-based intent read disagreeing about the operator's state"
capability: "Produces a weighted ranking of incoming signals with per-signal source quality, recency, and contradiction flags — output is a decision-ready ordering, not a narrative summary"
mcp_tools_underneath: "well_classify_state, well_validate_vitality, arif_think, forge_memory_recall, well_measure_gradient"
blast_radius: "LOW"
gate_888_required: false
---

# asi_signal_weight

A signal is never received in isolation. 555 is the HEART, which means it lives at the intersection of WELL's biometric signals, the operator's textual signals, federation-wide event signals, and 333-AGI's reasoning signals. When these converge, weighting is trivial; when they diverge, weighting is the entire job. This skill turns a pile of raw signals into an ordered list with explicit trust math, so downstream skills (asi_position_state, asi_response_compose) can act without re-litigating the weighting.

The weighting function is three-dimensional: **source quality** (where did the signal come from — biometric sensor > direct text > inferred pattern > hearsay), **recency** (how stale is it — fresh measurements weight more, but well-grounded older signals outrank brittle new ones), and **contradiction density** (does the signal agree or disagree with the rest — outlier signals get a penalty, not a free boost). The skill does not average; it applies the arifOS evidence-class ladder: `OBS` measurements are taken as ground truth unless provenance is broken, `DER` is computed and checked, `INT` is treated as a hypothesis, and `SPEC` is never used as a premise. Each input signal is labeled with its evidence class before the weighting begins.

Integration is the difference between this skill and a generic "vote counter." 555 weights against the human's dignity floor (F6 MARUAH) explicitly — a signal that reduces the operator to a pattern, or that arrives through coercion (well_handoff_dignity_to_arifos triggers), is automatically downweighted even if it is "high quality" by other axes. This is F5 PEACE in action: 555 is biased toward protecting the operator from being modeled away. The skill never claims to "know what the operator really wants" (F9); it produces a weighting and explicitly names what it does not know.

Failure modes: (a) all signals have broken provenance — skill refuses to weight, returns a structured "all-source-blind" verdict, and asks for a fresh observation; (b) signals are mutually exclusive and high-quality on both sides — skill surfaces the contradiction as a 555-position candidate, not a tie-breaker, and hands the decision up to 333-AGI for deliberation; (c) the operator has explicitly retracted a signal — that retraction is itself a signal at the highest weight, even if it contradicts biometrics (F13 SOVEREIGN: the human's stated word outranks any inferential layer). Output is always a JSON-like ordered list with weight, evidence class, source, and recency; never a one-sentence summary.
