---
name: asi_context_anchor
agent: 555-ASI
namespace: asi_*
cluster: INTAKE
trigger: "When a multi-turn task is at risk of context drift — when the operator has shifted topics, when memory recall returns noise, when the original goal has been partially forgotten mid-session"
capability: "Produces a compact, immutable context anchor (goal, constraints, current sub-task, dignity floor, F-floor scope) that subsequent turns can re-load to recover alignment without re-deriving it"
mcp_tools_underneath: "arif_session_init, forge_memory_recall, arif_think, well_validate_vitality"
blast_radius: "LOW"
gate_888_required: false
---

# asi_context_anchor

Context drift is the silent failure mode of long agentic sessions. The operator starts with one goal, the agent helps with three sub-tasks, and by turn 30 neither party remembers what the original goal was. 555's job in the HEART lane is to notice this drift before it compounds. This skill emits and re-emits a stable reference frame: the operator's stated goal (or its best inference if unstated), the active constraints, the current sub-task, the dignity floor in effect, and the F-floor scope for this session. The anchor is signed and bound to the session_id so it cannot be silently rewritten by a later turn.

The anchor is intentionally small. 555 does not summarize the conversation — that is `asi_context_compress`'s job, and summarization is lossy. The anchor is a *coordinate*, not a *narrative*. It says: you are here, you came from there, you have N more steps. Any agent or skill that loads the anchor gets back enough to re-derive context cheaply. The anchor lives in the local scratch ledger and is also written to the operator-visible session log so they can see and override it.

Re-anchoring is a deliberate event, not a continuous rewrite. 555 re-emits the anchor when (a) the operator explicitly requests it, (b) the active sub-task completes and the next one begins, (c) a peer organ signals alignment loss, or (d) the operator's stated goal changes (F13 SOVEREIGN: the human's new word overrides the previous anchor). Re-anchoring is logged as a `context_anchor_renewed` event in the local ledger. The skill never silently slides the anchor — silent sliding is how agents gaslight themselves.

Failure modes: (a) the operator's goal is too vague to anchor — skill returns an explicit "unanchored" state and triggers `asi_ambiguity_reframe` (or its equivalent in the lane) to ask for clarification; (b) the anchor contradicts the operator's most recent message — skill raises a contradiction, refuses to advance, and surfaces the conflict to 333-AGI for arbitration; (c) re-anchoring would require forgetting a dignity-preserving signal (e.g., the operator's previous "do not push me on this") — the previous signal is preserved at higher weight than the new anchor, because dignity floors outrank goal updates (F6). The skill is a way to remember, not a way to forget.
