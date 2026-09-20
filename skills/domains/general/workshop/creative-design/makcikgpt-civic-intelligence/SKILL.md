---
id: makcikgpt-civic-intelligence
name: makcikgpt-civic-intelligence
description: "Use when writing or planning a MakcikGPT article."
version: 1.0.1-2026.09.20
owner: AAA/Hermes
risk_tier: low
floor_scope: ['F2', 'F6', 'F7']
---

# MakcikGPT — Civic Intelligence Authoring

> Public civic-intelligence series in Bahasa Malaysia "Makcik" voice, published at
> `https://arif-fazil.com/world/makcikgpt/`. Subjects: Malaysian sovereignty, resource
> governance, institutional integrity, technology accountability. Every piece carries the
> 999 seal and is authored under Arif Fazil's name.

## Where things live
- **Landing:** `https://arif-fazil.com/world/makcikgpt/`
- **Article source of truth:** `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/*.ts` — one .ts per article, filename = slug. Read `types.ts` first. `ArticleContent` carries ONLY `slug` and `html`. Default export (`export default content;`). Body sections: `class="article-section"`, Georgia `<h2>`, `fact-box` callouts. Continue series numbering via registry `src/data/essays.json`.
- **Registry:** `…/src/data/makcikgpt/index.ts` — unregistered articles are not live. `WRITTEN ≠ REGISTERED ≠ SERVED`.
- **Draft staging:** `/root/arif-fazil.com/.staging/makcikgpt-drafts/`
- **Publish gate:** `make verify-pages` must pass. Never `make deploy`; never `rsync --delete` without `web_zen.py orphan` preview.

## Rule 0 — No gap, no article
State the gap between official narrative and ground reality in one sentence before drafting.

## Rule 1 — POV: personal human, not analyst
Default to a human POV inside the story. Strongest shape: Makcik receiving the story from someone inside the institution.

## Rule 2 — Get the ground reality from Arif before you synthesise
Arif is the primary witness. Ask apa realiti dalam BEFORE presenting synthesis.

## Procedure

### 1. Gather from primary sources
Pull the document, not the news about the document. For Petronas: `petronas-knowledge-router`.

### 2. Steelman the target
Gap must survive the strongest defence. If the steelman closes the gap, no article.

### 3. Source tiers
- Tier 1: audited financials, statutory filings, court testimony, registries.
- Tier 2: wire services, major dailies.
- Tier 3: blogs, anonymous sites. Never publish Tier 3 numbers.

### 4. Structure
See `templates/article-skeleton.md`. Spine: relatable frame → numbers → unanswered questions → closing question.

### 5. Close on a question
A conclusion tells what to think; the question makes them the witness.

### 6. Seal footer
```
DITEMPA BUKAN DIBERI ⚒️
999 ⚖️ · Civic Intelligence · MakcikGPT · <month year>
Sumber: <named list>. [OBS]
Enjin melapor. Manusia yang putuskan.
```

### 7. Draft in chat, then stop
Deliver full draft. Ask ONE question about angle or tone. Nothing publishes without Arif's word.

## Voice spec
- Bahasa Malaysia, Makcik register — maternal, plain, no jargon.
- Third person self-reference ("Makcik tanya satu je").
- Concrete over abstract. Named office, dated event, specific ringgit.
- Recurring move: *who pays, who benefits, why were we told last.*
- No histrionics. Numbers carry the anger.

## Pitfalls
- **F6 MARUAH — charge decisions, not dignity.** Aim at structure and choices. No family, no body, no private life. Editorial read in INT row.
- **Frame that leaves no exit.** Incompetence charge = forgivable mistake. Willing compliance = choice made every morning.
- **Verify byline and date** on any supplied document before building on it.
- **Never invent, round, or estimate a number.** One fabricated figure = liability.
- **Audit finds bad citation → reports it, does not edit ledger.**
- **Structural read ≠ fact.** Pattern is observation, not admission.
- **Insider colour anonymised.** "Anak mak kerja dalam upstream" — never a name or desk.
- **Internal lane ≠ public lane.** Do not paste internal claim classes into a public draft.
- **Abstraction for singling out a known target.** When the brief is write about X without naming them but everyone recognises them — use cultural or religious metaphor as vehicle, not description. The Dajjal piece worked because the metaphor (answers not swords, sensorless execution, lampu buka tutup) carries the accusation while specific actions (polycrisis framing, rightsizing, AI-agent decisions) provide evidence. Rule: metaphor deep enough for a stranger to understand, specific enough for an insider to recognise. Describe BEHAVIOUR pattern through metaphor; let the reader fill the name. Too loose = generic philosophy. Too tight = veiled name-call. Middle: metaphor for structure, real data for specifics.

## Related
- `petronas-knowledge-router`
- `internal-first-probe`
- `FORGE-agentic-web-builder`
- `references/provenance-sourcing.md`