# Relationship Evidence Audit — output skeleton

Use when the ask is to reconstruct what actually happened between the principal and a named human, from
first-party records only. This is an audit, not a profile: the deliverable is a minimum true model and an
UNKNOWN register. Do not end on advice.

## Order of operations

1. Enumerate every record store that could carry the exchanges — chat/gateway logs, session stores,
   per-person lane files, previously exported chat archives, prior agent artifacts about the person.
2. Extract with a file-based script (`scripts/extract_gateway_records.py`) rather than hand-parsing, and
   keep the raw corpus in a workspace directory so every later claim can be re-checked.
3. Report the corpus shape before any finding: source, retained window, record counts per speaker,
   attribution gaps, truncation, dedupe rule, and what the corpus cannot contain at all.
4. Resolve identifiers from data, never from the asker's naming.

## Sections, in this order

1. **Executive compression** (≤10 lines) — what is actually evidenced. No archetype labels unless the
   record earned them.
2. **Chronology** — important interactions in order, each with timestamp, source, initiator.
3. **Behavioural inventory, both directions** — observed/reported behaviour first, interpretation
   afterwards and clearly separated.
4. **Reciprocity loop** — derived from events, with occurrence class stated. A hypothesised loop with
   zero observed instances is reported as such, explicitly.
5. **Attention mechanics** — generic / specific / selective / expected / provoked attention,
   possessiveness, dependence kept as separate rows, each with its own confidence.
6. **Power matrix** — by domain, with evidence and confidence per row.
7. **Hypothesis tests** — verdict, best evidence, counterevidence, alternative, confidence.
8. **Where the reading exceeds the evidence** — the exact gap, without pathologising, plus where the
   reading does NOT exceed the evidence.
9. **What prior AI output projected** — name each transformation, correct it, and correct the record for
   the agent's own past overreach.
10. **UNKNOWN register** — every unresolved variable, each absence graded strong/weak.
11. **Minimum true model** — one paragraph: *"The record establishes X, Y, Z. It suggests A with
    confidence c because .... It does not establish B, C, D."* Then stop.

## Anti-narrative law (state it in the deliverable)

If the records produce a boring answer, preserve the boring answer. If they produce something emotionally
complicated, preserve that too. Do not optimise for romance, eroticism, drama, archetype, or an
entertaining story. Reality outranks archetype.

## Common failures this skeleton prevents

- Answering "did he solicit my attention?" from a persona generated in the same session — fiction read
  back as biography.
- Reporting a one-sided feeling as mutual because both names appear in the same window with similar
  volume.
- Letting a warm, coherent portrait stand in for evidence.
- Treating the principal's own vocabulary as imported context when they authored it.
- Treating a sealed or formally beautiful document as if formality were evidence.
- Applying findings about a population to the individual in front of you.
- Ending with advice, which converts an audit back into a profile.
