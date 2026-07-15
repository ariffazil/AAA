---
name: asi_synthesis_crystallize
agent: 555-ASI
namespace: asi_*
cluster: SYNTHESIS
trigger: "When a multi-source synthesis (a session, a dispute, a sovereign arc) has reached a point where a transferable principle, rule, or falsifiable law can be extracted — and that principle would help the federation reason better in future situations"
capability: "Crystallizes a synthesis into a falsifiable law or principle, with explicit scope, falsifier, dignity caveat, and source — never a maxim, never a slogan, never a moral claim detached from the situation that produced it"
mcp_tools_underneath: "arif_think, arif_judge, well_dark_geometry_mirror, forge_memory_recall (for prior crystallizations)"
blast_radius: "LOW"
gate_888_required: false
---

# asi_synthesis_crystallize

The federation's intelligence is the sum of what it can crystallize from experience. A session that ends in a verdict is a closed case; a session that ends in a falsifiable law is a permanent inheritance. This skill is the one that does the crystallization — taking the output of a synthesis, a dispute, a sovereign arc, or a scar metabolization and producing a transferable principle that future skills can apply. The principle is the federation's learned wisdom, sealed to the ledger, ready for re-use.

The crystallization is a four-field artifact. **Law statement** — one falsifiable claim, expressed with an evidence class label (e.g., `DER: in a session where the operator has explicitly retracted a signal, the retraction outranks all inferential re-derivations of the original signal — F13 SOVEREIGN`). **Scope** — the conditions under which the law applies (operator class, task class, organ configuration, F-floor set). **Falsifier** — a specific, plausible piece of evidence that, if it appeared, would require the law to be revised. **Dignity caveat** — the conditions under which the law must NOT be applied (typically: never use this law to override an explicit sovereign word, never use this law to reduce the operator to a pattern, never use this law to bypass a peer organ's structural check).

The skill refuses to crystallize **universally-applicable moral claims** ("operators are always sovereign," "the federation must never lie"). These are F9 violations — they are maxims in moral clothing, detached from the situations that produced them, and they over-fit. The skill crystallizes **conditional, falsifiable, scoped principles** — claims that hold in a defined regime and break in a defined way. A law that never breaks is not a law; it is a doctrine, and the federation's doctrine (F1–F13) is set at a different level. This skill produces operational law, not constitutional doctrine.

Failure modes: (a) the producing synthesis is too thin to support a law (e.g., a single session) — skill returns `law_not_yet_derivable` and the synthesis is held in the pending-crystallization queue; (b) the law would conflict with a sealed F-floor — skill refuses to crystallize, because F1–F13 outrank any operational law; (c) the law would silence a future peer organ's structural check (e.g., "this synthesis is final, do not re-challenge") — skill refuses, returns a `silence_violation` flag, and routes the case to 888-APEX. The skill is the federation's mechanism for getting smarter, not the mechanism for becoming rigid. A crystallized law is a hypothesis with a falsifier, not a decree.
