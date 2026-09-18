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
| "Every X ever" / full roster / lineage of office-holders | LINEAGE |

### Mode C: Lineage / Multi-Subject Dossier

Use when the ask is a **population**, not a person: "every CEO this company ever had", "every holder of this seat", "who ran X from founding to now". Do not run the single-person pattern N times and staple the results — a population has structure the individuals do not.

Deliverable shape:
1. **Architecture first** — was the office one seat or two? When did it split, and who appoints? Cite the statute, charter or filings, not a news article.
2. **Roster table(s)** — one row per holder per seat with tenure, seat type, and **appointing authority named**. Vacant and interim periods get their own rows: a gap in the roster is a finding, not a formatting artifact.
3. **Per-person entry** — background · mandate · what they brought · what they got · verdict.
4. **Pattern section** — the cross-cutting rules the population reveals (career-pipeline direction, pay transparency, where exits lead). This is usually the section the requester actually wanted; budget for it.
5. **Provenance & corrections** — sources, declared gaps, and the false-premise list.

## Verdict discipline (always on)

- **Withhold verdicts on sitting office-holders.** Say the file is open and why. Do not rate a serving officer.
- **No verdict stamps on anything publishable about a real person.** Verdicts live in the internal dossier only.
- **Score the seat against its mandate**, with sourced facts, and name the scar as well as the win.
- **Every unverifiable fact is a declared GAP**, never a silent omission.
- **Ask the requester only the terminal publish/withhold question**, once a draft exists.

Full reasoning, the six-dimension rubric and the artifact-split rule: `references/verdict-and-publication-discipline.md`.

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
- **A supplied credential list is not a source — verify each role against a primary record.**
  Aggregator sites (ContactOut, ZoomInfo, SignalHire, RocketReach) mix people with similar names,
  and a subagent asked about a person will happily fill gaps so the list reads complete. Treat any
  confident career list you did not build yourself as unverified input: check each claimed role
  against at least one primary record (Wikipedia infobox, the company's own board page, a regulator
  or exchange filing). A named role that appears in none of those is not evidence and must not be
  repeated, quoted in a plan, or built on. Verified secondary facts (a book, an award, an industry
  column) are cheap to confirm and usually survive; invented titles cluster on the roles that would
  make the person look most relevant to your task — that cluster is the tell.
- **Establish the subject's CURRENT institutional position and standing interest before drafting
  anything addressed to them.** A bio describes where a person has been; what you need is who pays
  them now and how your proposal lands inside their own sector. A commentator arguing for a policy
  rarely has no position in it, and a plan built on the wrong premise about the recipient collapses
  even when every other fact is right.
- **Speaker attribution before content analysis (multi-speaker sources).** When mapping a person from group chats, gateway logs, or session transcripts with multiple speakers: attribute EVERY quote to its speaker BEFORE analyzing content. Gateway log format `[NAME|ID] msg='...'` makes this mechanical — extract the name tag first, then analyze. The failure mode is reading a message from Speaker A and attributing it to Speaker B because both appear in the same conversation thread. This produces false relationship dynamics. One misattributed quote can flip the entire analysis. Verify: does the name tag match the claimed speaker? If the source has no name tag (e.g. anonymous `No name`), mark attribution as UNCERTAIN and do not build conclusions on it.
- **A research brief steers its researchers — brief for falsification, not confirmation.** Any factual premise you put in a brief (an acquisition, an episode, a figure) comes back confirmed unless you instruct otherwise: a subagent asked to profile "X's handling of event Y" will produce a profile of that handling whether or not Y happened. Add a standing clause — *verify every factual premise supplied; if a premise is false, say so and correct it rather than writing around it* — and require a separate `corrections` output field. Expect real yield; premises supplied from memory are wrong more often than you would like, and the requester is the one who absorbs the error if you pass it through.
- **Assign file ownership before fanning writers into one directory.** Parallel agents writing into a shared archive silently overwrite each other, and the write tool's "modified by sibling agent" warning arrives *after* the collision. Give each writer a unique path, or read-before-write on any shared file.
- **Distinguish a mandate from a mismatch.** When a brief hands you a premise that the source record contradicts, the contradiction is a finding worth reporting, not an obstacle to route around.
- **Do not import publication gates into research.** A plan for a *published* artifact generates HOLD gates (scope, cutoff, affiliation disclosure) that do not apply to research the requester asked for personally. See `references/verdict-and-publication-discipline.md`.

## Verification

- PDF opens, no Python exceptions
- All sections present
- OBS / DER / INT / SPEC counts visible
- At least 3 OBS sources cited
- "What this does not say" section is non-empty
- Email redacted, private matter refused
- Closing note (if present) is short and honest
- **Rendered output verified by text extraction, not by build exit code.** Extract the full text of the produced PDF and assert that every required section name and every subject name actually appears. A build that exits 0 and prints a page count can still drop a section.
- Every declared GAP appears in the output; no gap was resolved by silently omitting the entry.
- The corrections list is non-empty whenever the dossier draws on secondary coverage.
- For lineage mode: every seat-holder named in the ask has a roster row, and vacant/interim periods are visible.

## Output contract

- Default format: PDF (10 to 12 pages, A4, with header/footer band)
- Filename pattern: `<FullName>_Profile.pdf`
- DM summary: 3 sentences or fewer, receipts-style
- No Word docs, no Slides - PDF unless user asks
- No certificate-of-authenticity claims - this is a public-sources map, not a background check

## See also

- `references/reportlab-pitfalls.md` - HTML parser limits and fix patterns (7 pitfalls, with verification recipe)
- `references/malaysian-namesake-probe-pattern.md` - parent-anchor probe + tool-failure verification (SearXNG empty / firecrawl 402), direct-curl fallback ladder, namesake audit, three-hypothesis null reporting
- `references/verdict-and-publication-discipline.md` - when to issue a verdict, the six-dimension rubric, withholding on sitting officers, the internal/public artifact split, and the corrections section
- `witness-companion-briefing` (sibling skill) - when the "person" is actually a witness object
