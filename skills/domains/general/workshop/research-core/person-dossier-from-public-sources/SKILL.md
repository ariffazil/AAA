---
name: person-dossier-from-public-sources
description: "Build an epistemic-tagged human profile dossier from public sources. Hard refusal on fabricated biographical detail."
---

# Person Dossier from Public Sources

## Why this skill exists

Person profiles carry the **highest hallucination risk of any research task**. A name is easy to fabricate but nearly impossible to verify without anchor. The cost of being wrong about a real human is non-recoverable: you cannot un-ring a false claim.

F2 (TRUTH) + F9 (ANTI-HANTU) + F6 (MARUAH) make this non-negotiable. Every claim must carry an epistemic label. Anything that would identify private matter without consent is refused.

## When to use

Trigger phrases
- Deep research about a person
- Tell me everything about a person
- Make a profile or dossier for a person
- Build briefing for a person
- Who is this person in this org

## When NOT to use

- Public figure with extensive Wikipedia/media footprint: use `executive-intelligence-briefing`
- Institutional analysis (a company, a crisis): use `institutional-case-building`
- Chat/text behavior extraction: use `text-forensics`
- Witness/companion briefing about a non-person or archetype: use `witness-companion-briefing`

## Two output modes

### Mode A: Full Dossier (default)
Complete 10-12 page PDF with epistemic labeling. Use when user says "deep profile research task," "full dossier," "complete research on [person]."

### Mode B: Quick Profile (light)
Use for Telegram/WhatsApp-speed requests: "cari info pasal," "siapa [nama]," "tell me about [person]."
- Format: DM summary (structured bullets, not PDF)
- Key info: Name, age, title, education, career path (table), notable moves, BANGANG/insight angle
- Skip epistemic labels on every claim (keep discipline internally)
- Delivery: inline message unless user asks for PDF
- Searches: 2-3 searches in parallel (not 4-6)
- Skip publications, open questions, refused topics section unless asked for

**Mode B anti-skema discipline (lesson: user pushback "jangan skema sangat"):** When initial searches come back empty, do NOT ask 4 verification branches back to the user ("kasi IG / kasi link / confirm personally / full name Noraniza"). That reads like a research form, not like a partner thinking. The right move:
1. State the verified null in 2-3 lines ("7 search kosong semua, bukan aku malas, realiti tool aku tak index").
2. Try ONE more angle (different keyword, parent-anchor search, firecrawl subagent) silently.
3. Ask for ONE anchor, not four. Format as a single "signal hang?" with the most likely unlock first.

Empty-search is not failure; it is early evidence. Reporting it cleanly with discipline earns trust; asking the user to fill in your gaps does not.

### When to choose
| Signal | Mode |
|---|---|
| "Deep profile research task" | FULL |
| "Cari info pasal [nama]" / "Apa cerita pasal" | QUICK |
| "Tell me about [person]" | QUICK |
| "Deep research about a person" | FULL |

## The pattern (5 steps)

### 1. Refuse-to-fabricate boundary (state it first)

Before any search, name what the dossier will and will not claim.

Then ask for ONE of org/role, time window, link to existing public profile, or "go ahead with what you can find."

### 2. Multi-source cross-reference (PARALLEL)

Launch 4 to 6 web searches in parallel covering the full name plus org plus role, the full name plus org plus domain keyword, the full name broadly, the patronymic or surname variant, scispace direct, and linkedin direct. Wait for results, then cross-reference. Same person often appears under multiple name strings (patronymic dropped on LinkedIn, etc.).

### 3. Identity disambiguation (the namesake trap)

Public records duplicate and split names.
- Iban / Dayak Borneo. `<First> Layang anak <Father>` (scispace, full patronymic) vs `<First> <Father>` (LinkedIn display, patronymic dropped) - same person
- Indonesian. `<First> bin/binti <Father>`
- Scispace duplication. surname sometimes appended as a second "Bakon Bakon" string - same person, not two

If two search strings return overlapping evidence (same org plus role plus time window), treat as one person unless contradicted.

### 4. Epistemic labeling (every claim)

```
OBS  - observed / publicly verifiable
DER  - derived from cited evidence
INT  - interpreted (inference grounded)
SPEC - speculative (unverified)
```

Target distribution 60 to 70 percent OBS, 10 to 15 percent DER, 15 to 20 percent INT, 5 to 10 percent SPEC. If SPEC > INT, you are speculating too much. Stop and ask the user for anchor.

### 5. Output structure

1. Provenance and Honest Limits - what it is, what it is not
2. Identity and Naming - disambiguation, origin
3. Career Timeline - table
4. Field / Project Assignments - domain-specific work
5. Publications / Technical Authority - papers, talks, awards
6. Domain Fit (if user has context) - match against user question
7. Open Questions - to take to the person themselves (3 to 8 questions)
8. What This Dossier Does NOT Say - refused topics
9. Sources Cited - auditable list
10. Closing Note (optional) - for the person themselves, honest paragraph

## Pitfalls (lessons from this session)

- reportlab `<span style='...'>` is NOT supported - see `references/reportlab-pitfalls.md`
- Scispace duplicates the surname into the author name. Do not treat as two people.
- The Activity like timing signal - a single like on a relevant recruiter post is a *signal* of attention, NOT proof of involvement. State as INT.
- Email patterns from RocketReach etc. are partial (`f******@petronas.com`). REDACT - do not store, do not share.
- Do not infer private matter from public career - religion, marital status, children, salary, politics, health. Refused section.
- Conference paper PDFs are gold - they often have details the academic portal hides. Extract from the PDF directly via `web_extract`.
- The "Freddy as witness AND person" trap - when the user says "Tell [name] about X," first disambiguate: is the name a witness object (plush, archetype) or a real person? The brief differs entirely. See `witness-companion-briefing`.
- **Empty search ≠ empty reality.** A single `web_search` returning zero hits is NOT proof the person doesn't exist or the relationship is wrong. Three failure modes look identical from the result shape: (a) the tool is broken (SearXNG backend bug returning empty), (b) quota exhausted (firecrawl HTTP 402), (c) genuine zero footprint. Before declaring null, **probe the tool**: check `firecrawl_health`, dispatch a subagent with direct-curl fallback to Bing/Wikipedia/Malaysian portals, look for the parent/anchor first ("Noraniza Idris" anchor was solid via Wikipedia even when "Aliff Haiqal" returned nothing). The parent-anchor finding lets you state a clean partial result instead of total null. Pattern lives in `references/malaysian-namesake-probe-pattern.md`.
- **Namesake audit before null claim.** When the primary query is empty, search for OTHER famous Malaysians with similar names (Aliff Aziz, Aliff Syukri, Aliff Rakib) so the user knows you checked and ruled out the obvious lookalikes. Stating "checked Aliff Aziz, Aliff Syukri — different people" turns a dead-end into evidence.
- **Three honest hypotheses when footprint is empty.** Don't fabricate to fill silence. State three: (1) person exists but zero online presence (private IG, no content), (2) the reported relationship is incorrect, (3) the name is misremembered. List what would unlock each.

## Verification

- PDF opens, no Python exceptions
- All sections present
- OBS / DER / INT / SPEC counts visible
- At least 3 OBS sources cited
- "What this does not say" section is non-empty
- Email redacted, private matter refused
- Closing note (if present) is short and honest

## Output contract

- Default format: PDF (10 to 12 pages, A4, with header/footer band)
- Filename pattern: `<FullName>_Profile.pdf`
- DM summary: 3 sentences or fewer, receipts-style
- No Word docs, no Slides - PDF unless user asks
- No certificate-of-authenticity claims - this is a public-sources map, not a background check

## See also

- `references/reportlab-pitfalls.md` - HTML parser limits and fix patterns (7 pitfalls, with verification recipe)
- `references/malaysian-namesake-probe-pattern.md` - parent-anchor probe + tool-failure verification (SearXNG empty / firecrawl 402), direct-curl fallback ladder, namesake audit, three-hypothesis null reporting
- `witness-companion-briefing` (sibling skill) - when the "person" is actually a witness object
