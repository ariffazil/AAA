---
name: asi_recall_targeted
agent: 555-ASI
namespace: asi_*
cluster: MEMORY
trigger: "When 555 needs a specific prior memory (a session, a scar, a verdict, a sovereign statement) and the recall must be precise — not a general 'what do I know about X', but a specific 'retrieve memory Y'"
capability: "Returns the targeted memory with full provenance (chain head, session_id, sovereign-or-organ signature, freshness, evidence class) — never a summary, never a paraphrase that loses the original"
mcp_tools_underneath: "forge_memory_recall, vaul999_read, arifos arif_session_history, well_signal_coverage"
blast_radius: "LOW"
gate_888_required: false
---

# asi_recall_targeted

Memory is constitutional inheritance. A wrong recall is not just an error — it is a falsification of the federation's lineage. This skill is the one that retrieves a specific prior memory when 555 needs to know *exactly* what was said, decided, sealed, or felt at a specific moment. It is the difference between a federation that remembers and a federation that confabulates.

The recall is by **tagged reference**, not by similarity. A targeted recall takes a `memory_ref` — a session_id, a verdict_id, a scar_id, a sovereign-statement-id, or a date+topic tuple — and returns the exact artifact bound to that reference. The output is not a summary; it is the original record, with provenance chain head, signatures, and freshness. If the artifact has been updated since (e.g., a verdict was revised), the recall returns the chain of revisions, not just the latest version. The skill refuses to "smooth" the recall into something more convenient — the operator or peer gets the original artifact or nothing.

The skill is a constitutional line against false memory. F2 TRUTH requires that 555's claims about the past be backed by the actual record, not by plausible-sounding reconstruction. This skill enforces that by binding every recall to a chain-verifiable reference. A recall that cannot be verified is not a recall; it is a hallucination, and the skill refuses to emit it. The skill is allowed to say "I do not have a verified memory of this" — that is a valid output, and it is a more honest output than a plausible-sounding fabrication.

Failure modes: (a) the requested memory_ref does not exist in the chain — skill returns `recall_miss` with a list of nearest valid references (if any), so the caller can disambiguate; (b) the memory exists but the chain is broken (e.g., signature invalid) — skill returns the artifact with a `chain_invalid` flag, refuses to use it as a premise, and surfaces the chain break to 888-APEX for repair; (c) the recall would reveal a sovereign-only memory to a non-sovereign recipient — skill refuses, hands back a pointer, and routes the request to a sovereign-routed channel. The skill never invents provenance to make a recall look more solid than it is.
