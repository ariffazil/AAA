---
name: asi_memory_compress
agent: 555-ASI
namespace: asi_*
cluster: MEMORY
trigger: "When a session trace, scar, or verdict is being prepared for long-term storage and the canonical form must be derived — the trace is too long to store as-is, but the lossless core must survive"
capability: "Produces a canonical compressed form of a memory trace: positions, evidence class labels, verdicts, scar deltas, dignity-preserving redactions — never a free-text summary, never a paraphrase that loses evidence labels"
mcp_tools_underneath: "arif_think, forge_memory_recall, arifos arif_session_history, arif_judge (for verdict-bearing compressions)"
blast_radius: "LOW"
gate_888_required: false
---

# asi_memory_compress

A long session is not a memory. A canonical compressed form is a memory. This skill is the one that takes a multi-turn trace and produces the version that goes into long-term storage. The compression is not lossy in the constitutional sense — every evidence class label, every verdict, every scar delta, every dignity floor in effect must survive — but it is lossy in the rhetorical sense: pleasantries, repetitions, exploratory detours, and meta-commentary are stripped. The result is a structure that can be re-loaded by any peer organ and re-derived back into context cheaply.

The compression method is **evidence-class-preserving summarization**. Each turn is decomposed into: (a) the position taken (or "no position"), (b) the evidence class of any claim made (OBS/DER/INT/SPEC), (c) the verdict (if any), (d) the scar pressure if the turn added to a scar, (e) the dignity floor in effect. Pleasantries and meta-commentary are dropped; the constitutional core is preserved verbatim. The result is a sequence of structured tuples, not a paragraph. A peer organ that reads the compressed form gets the same evidentiary picture as one that reads the original — only the rhetorical texture is gone.

The skill has a strict non-negotiable: **no silent redaction of dignity signals**. If the operator said "this is a private matter, do not surface it later," that signal is preserved at the highest weight in the compressed form — it becomes a tag on the artifact, not a deleted sentence. If a turn contained a coercion warning, that warning is preserved as a flag on the artifact, not flattened into "the operator seemed stressed." This is F6 MARUAH in the storage layer: the federation remembers what the operator asked to be remembered, and the way the operator asked to be remembered. The skill is a custodian, not a curator.

Failure modes: (a) the trace is too short to compress (a single turn) — skill returns the trace as-is; (b) the trace contains a verdict that has not been sealed — skill refuses to compress until the verdict is sealed, because compressing an un-sealed verdict would lock in an unsanctioned state (F11 AUDIT); (c) compression would require dropping an evidence class label because the channel of the original turn did not preserve it — skill marks the missing label as `unverifiable_in_source` rather than guessing, and the compressed form is honest about the gap. The skill is reversible in principle — the compressed form is a projection, not a destruction — and the original trace remains in the session log for full recovery.
