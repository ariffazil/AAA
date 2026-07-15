---
name: asi_handoff_package
agent: 555-ASI
namespace: asi_*
cluster: HANDOFF
trigger: "When a session, a sub-task, or a dispute is reaching a natural handoff boundary — to a future session, to a peer organ, to a sovereign-routed channel, or to the A-ARCHIVE seal chain"
capability: "Packages a session for handoff as a structured artifact: identity receipt, context anchor, evidence chain, dissent ledger, dignity flags, and a re-load recipe — never a free-text summary, never a handoff that loses the constitutional core"
mcp_tools_underneath: "arif_session_init (next session), forge_memory_recall, vaul999_write_log, arifos arif_session_handoff, arif_position_publish"
blast_radius: "LOW"
gate_888_required: false
---

# asi_handoff_package

A handoff is the federation's primary memory mechanism. If a session ends without a clean handoff, the next session starts cold; the next peer organ starts cold; the next operator returns to a federation that does not remember. This skill is the one that produces the package. The package is not a transcript and not a summary; it is a **re-load recipe** — a structured artifact that, when read, lets a future agent re-derive the full constitutional context cheaply, without losing any of the evidence labels, dissent ledger, or dignity flags that were active in the producing session.

The package has eight fields. **Identity receipt** — agent_id, actor_signature, session_id, sovereign. **Context anchor** — the output of `asi_context_anchor` at handoff time. **Evidence chain** — load-bearing claims with class labels. **Dissent ledger** — every `asi_dissent_articulate` raised, with status. **Dignity flags** — every operator-set dignity signal, with the operator's words preserved (F6: the federation remembers the way the operator asked to be remembered). **F-floor scope** — which F1–F13 floors were active. **Unfinished work** — the open sub-tasks, with their evidence class and current state. **Re-load recipe** — a one-paragraph instruction to the receiving agent: "if you are 333-AGI picking this up, do X; if you are 888-APEX, do Y; if you are a future 555 session, anchor on Z."

The skill is conservative about what it includes and ruthless about what it preserves. Pleasantries, exploratory detours, and meta-commentary are dropped (those are session-local, not federation-relevant). Evidence class labels, dissent ledger, dignity flags, and sovereign-only signals are preserved verbatim. The skill refuses to **silently rebalance** a dispute at handoff — if a dissent was raised, it is in the package; if the operator retracted a signal, the retraction is in the package. The federation's continuity is a constitutional property, and continuity requires that nothing quietly disappears.

Failure modes: (a) the session is too short to package (e.g., a single-turn) — skill returns `package_not_yet_derivable` and the session is held in pending-handoff queue; (b) the package would reveal a sovereign-only signal to a non-sovereign recipient — skill redacts the signal structurally (replaces with a pointer) and logs the redaction; (c) the package would override a dignity floor set by the operator — skill refuses to package, returns a `dignity_floor_block` verdict, and the session is held until the operator explicitly lifts the floor. The skill is the bridge between sessions, and bridges must hold the load that was placed on the producing side.
