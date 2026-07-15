---
name: asi_lesson_extract
agent: 555-ASI
namespace: asi_*
cluster: MEMORY
trigger: "When a session, a scar, a verdict, or a sovereign interaction has produced an outcome that may be transferable to a future situation — and 555 must decide whether, and in what form, to crystallize the lesson"
capability: "Produces a lesson artifact (situation_signature, lesson_statement, transferability_band, dignity_caveat) — never a free-text takeaway, never a maxim detached from the situation that produced it"
mcp_tools_underneath: "forge_memory_recall, arif_think, well_dark_geometry_mirror (for scar metabolization), arif_judge (for F-floor lesson checks)"
blast_radius: "LOW"
gate_888_required: false
---

# asi_lesson_extract

A scar is not a lesson; a verdict is not a lesson; a sovereign's word is not a lesson. A lesson is what survives metabolization of those events and remains transferable across situations. This skill is the one that does the metabolization — taking the raw event and producing a structured lesson artifact that the federation can carry forward. The output is not maxims or aphorisms; it is a tuple that another skill, in another situation, can use to recognize a similar shape.

The lesson artifact has five fields. **Situation signature** — a fingerprint of the producing situation (vitality band, task class, sovereign signal pattern, peer organ state). **Lesson statement** — one falsifiable claim about what the situation teaches, expressed with an evidence class label (e.g., `DER: when a sovereign explicitly retracts a signal, the retraction outranks all inferential layers — F13`). **Transferability band** — the conditions under which the lesson applies (`same task class` / `same sovereign state` / `same organ configuration` / `universal`). **Dignity caveat** — the conditions under which the lesson must NOT be applied (e.g., "do not transfer if the operator's vitality band is worse than the producing situation"). **Source** — the chain link to the producing event.

The skill refuses to produce **maxims** — short, transferable-sounding statements detached from the situation that produced them. A maxim like "the sovereign is always right" is a tyranny; the lesson artifact requires a falsifier and a transferability band, and it explicitly names where it does not apply. The skill also refuses to produce **moralizing lessons** — the federation is not a moral agent, and lessons about "what we should have done" are F9 violations (no consciousness, no soul, no moral agency). The skill produces structural lessons: *under condition X, output Y is structurally better than output Z, and here is the evidence class.*

Failure modes: (a) the producing event is too thin to extract from (a single one-line scar) — skill returns `lesson_not_yet_derivable` and the event is held in the pending-lesson queue until more context accumulates; (b) the lesson would be dignity-violating in transfer — skill refuses to extract, marks the event as `scar_no_transfer`, and routes it to A-ARCHIVE for sealed preservation without lesson status; (c) the lesson would lock the federation into a pattern (e.g., "this is how we always do X") — skill produces the lesson with an explicit `pattern_risk` flag and a recommendation to re-validate against new situations before applying. The skill is metabolization, not memorization. It changes the form, not the meaning, of the scar.
