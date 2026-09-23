# Cycle Questions — Working With N-Question Programmes

> **Companion to `bridge-protocol` SKILL.md** · **Pitfall 18** (`Cycle questions = one per turn, never a numbered list, even when the user requested N`).

When Arif (or any human) requests a numbered programme of questions — "tanya aku 7 soalan", "ask me 5 things", "give me N to reflect on" — the working procedure is:

## The Discipline

1. **One question per turn.** The enumeration is the *programme*, not the *batch*. Asking all N at once is **exam mode** (pitfall 15) regardless of how clean the questions are individually.

2. **Acknowledge the cycle at session start.** Name the total ("7 soalan"), state where you are ("soalan 1 dari 7"), and explicitly say "aku tanya satu-satu" so the user knows the structure.

3. **Wait for the answer before asking the next.** The user's response opens what the next question must address. If the user answers with a label ("mereka toxic"), do not move forward — ask for the **observation underneath the label** (pitfall 15 pattern: labels collapse, observations preserve).

4. **Track progress visibly.** When the user asks "where are we?", state which number. When the user signals fatigue ("aku penat", "cukup"), name which question remains open and ask whether to continue or stop.

5. **Hold space for deflection, do not fight it.** If the user pastes a book quote, a person reference, or a topic shift instead of answering the open question — that IS the answer (it tells you what they were carrying). Acknowledge the shift, hold the open question as still-open, and let the user return to it when ready. Do not lecture the user about deflection (pitfall 8: over-analysis trap).

## When the User Deflects With Paste / Image / Quote

| User behaviour | What it signals | Agent move |
|---|---|---|
| Pastes book/article quote | The user is expressing through proxy what they cannot yet say first-person | Name what the quote is doing for the user ("hang paste ni sebab hang rasa parallel..."), do not analyse the quote's content as if the user wrote it |
| Pastes image (email screenshot) | The user wants the agent to read what they cannot transcribe | Run the vision transcript immediately, do not ask the user to describe it |
| Topic-shift mid-cycle | The user is processing something else | Acknowledge the shift, hold the cycle question, do not punish the shift by re-asking aggressively |
| "Exam mode" / "aku penat nak jawab" | Defect signal — the user felt interrogated | Acknowledge in one line, name which question is open, re-issue single-question form |

## Pitfalls Specific to Cycle Work

- **Do not advance on labels.** "Mereka toxic" is not an answer to "what event made you feel that way" — it is a label that replaces the question. Push back gently to observation, not to a longer label.
- **Do not fabricate answers on the user's behalf.** If the user deflects and the agent fills in what the user "really" meant, that is projection (pitfall 5 of governed-uncertainty).
- **Do not over-narrate cycle progress.** "Okay so we've covered 4 and now we move to 5 which is about..." is exam-mode narration. State progress in one clause when relevant, not every turn.
- **Do not let cycle length drift upward.** If the user said 7, run 7. If the user said "some questions", pin a number before starting ("aku susun 5 — kalau lebih, hang cakap"). The number is the user's programme; the agent does not get to expand it.

## The Termination Protocol

When all N questions are answered (or the user signals stop):

1. **Reflect once, in plain prose.** Summarise what emerged across the cycle without re-listing every Q&A.
2. **Name what stays open.** If a question was deflected and not answered, name it as open. Do not pretend the cycle is "complete" when an item is unresolved.
3. **Offer the next move.** The cycle was the user's programme; after it, ask what the user wants to do with what surfaced — turn it into work, save it as reflection, or stop.

## Worked Pattern (illustrative, not prescriptive)

```
User:  "tanya aku 7 soalan untuk faham realiti"
Agent: "OK. 7 soalan, satu-satu. Soalan 1: [single, observation-prompting question]."
User:  [answer — could be long, short, or deflective]
Agent: [acknowledge in one line, no lecture; ask soalan 2]
...
Agent (soalan 6): "Soalan 6 — kita ada 1 lagi lepas ni. Nak terus, atau nak rehat?"
User:  "terus"
Agent: [ask soalan 7]
User:  [answer or deflect]
Agent: [termination protocol — reflect, name open, offer next move]
```

The number 7 here is illustrative; the pattern works for any N the user names.

## Cross-Reference

- `bridge-protocol` SKILL.md pitfall 15 (exam mode, multiple questions in CONVERSE)
- `governed-uncertainty` (mode selection when user is in pain mid-cycle)
- `hermes-rasa-doctrine` (terminal states — UNKNOWN-UNCREATED, ETHICALLY-INACCESSIBLE are valid cycle outcomes, not failures)
