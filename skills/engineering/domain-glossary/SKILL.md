---
name: domain-glossary
id: domain-glossary
version: 1.0.0
description: "Use when a repo or conversation has no shared vocabulary — extract the domain terms, challenge synonyms, write GLOSSARY.md + ADRs, and align code names to the agreed language. Trigger: 'what do we call this', 'shared language', 'glossary', 'domain model', 'ADR'."
owner: AAA/333-AGI
risk_tier: low
floor_scope: [F2, F4, F7]
tags: [glossary, domain-model, adr, naming, shared-language]
---

# Domain glossary — one language, then code

A repo without a shared language makes every agent re-derive the jargon. This skill
builds the smallest durable artifact that fixes it: a repo-local `GLOSSARY.md` plus ADRs
for decisions that are hard to reverse.

It does not invent a federation-wide dictionary, and it does not rename code by itself.

**Trigger:** "what do we call this", "shared language", "glossary", "domain model",
"ADR", "the agent keeps using five words for one thing", or a codebase where the same
concept has three names and two of them are wrong.

## When NOT to use

- One-term lookup — answer it, do not create a document.
- The repo already has a current `GLOSSARY.md` and `docs/adr/` — patch them instead.
- The user wants a federation canon or registry — that is F13 territory, not this skill.
- The terms are only chat shorthand with no code consequence — leave them in chat.

## Procedure

1. **Collect, do not invent.** Read the README, the module names, the issue titles, and the
   last 20 user messages. Extract terms that carry a decision (entity, state, actor,
   boundary, invariant, unit). Skip generic programming words.
2. **Find synonyms.** Group terms that claim the same job. For each group, ask one question:
   "Which one is the real thing, and which are views of it?"
3. **Define each surviving term in one sentence.** Include what it is NOT, if a nearby term
   is commonly confused with it. No marketing prose.
4. **Write `GLOSSARY.md` at the repo root** (or the existing docs location). One table:
   `term | definition | not this | code name`. The `code name` column is the identifier the
   agent should use in code; it may differ from the human term only with an explicit note.
5. **Record hard-to-reverse choices as ADRs.** One file per decision in `docs/adr/`:
   context → decision → alternatives → consequence → reversal cost. A glossary is a map;
   an ADR is a commitment.
6. **Align code names last.** Rename only when the glossary is agreed and tests can prove
   the change. A glossary without a rename is still useful; a rename without a glossary is
   churn.
7. **Keep it current.** Add a term when a new decision introduces one; delete a term only
   when its concept is gone, not when the word is unfashionable.

## File shape

```markdown
# Glossary

| Term | Definition | Not this | Code name |
|---|---|---|---|
| receipt | an append-only record of an executed act | a plan, a promise | `Receipt` |
| verdict | a judgment issued by the judge | a recommendation | `Verdict` |
```

```markdown
# ADR-0001: <decision>

- Status: accepted | superseded
- Context: <the force that made this necessary>
- Decision: <one sentence>
- Alternatives: <what was rejected and why>
- Consequence: <what becomes easier/harder>
- Reversal cost: <cheap | expensive | irreversible>
```

## Rules

- **One glossary per repo.** A second glossary is a second truth.
- **Definitions are falsifiable.** If two engineers can read it and build different things,
  it is not a definition.
- **The human's word wins** unless it is ambiguous; then keep the human word as an alias.
- **Never rename through a glossary PR** without a dependents sweep — code, tests, docs,
  prompts, and skill references all count.
- **No invented acronyms.** If the domain did not name it, do not mint a new brand.
- **ADRs are append-only.** Supersede, never rewrite history.

## Output

```
GLOSSARY: <path> — <N> terms, <M> aliases collapsed
ADRs: <paths> — <K> decisions recorded
CODE ALIGNMENT: <none | list of rename candidates with dependents count>
OPEN TERMS: <terms still disputed — owner: human>
```

## Provenance

Adapted from `mattpocock/skills` `domain-modeling` and `grilling` (MIT), re-authored for
arifOS: repo-local, no federation canon, ADRs for commitments, and code renames gated by a
dependents sweep.
