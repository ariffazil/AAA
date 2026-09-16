# Malaysian Namesake Probe Pattern

When a Mode B (quick profile) request for a Malaysian person returns zero hits from default `web_search`, do NOT immediately declare null or ask the user for 4 verification branches. Use this ladder instead.

## The problem

Three failure modes look identical from the search result shape:

1. **Tool is broken** — `web_search` (SearXNG backend) returning empty on every query even for real public figures (e.g., Noraniza Idris, born 1968, has Wikipedia entry + verified IG, but `web_search` returned `{"web": []}`)
2. **Quota exhausted** — `firecrawl_search` returns HTTP 402 ("Payment Required") without doing the query
3. **Genuine zero footprint** — the person has no online presence, or the relationship is wrong, or the name is misremembered

The wrong move is to report empty = real-null and ask the user to do your verification. The right move is to PROBE the tool and check the anchor before reporting.

## The 5-step probe ladder

### Step 1 — Verify the tool, not the query

If 2-3 parallel `web_search` calls all return `{"web": []}`, dispatch a subagent and tell it to:

1. Try `firecrawl_search` first (different backend) — note HTTP 402 if quota dead
2. Fall back to direct-curl `terminal`/`execute_code` calls to Bing search results page, Wikipedia API, and Malaysian portals
3. Decode any redirect URLs (Bing `ck/a` URLs) to verify destinations

This separates "tool dead" from "no data" cleanly. The subagent should report which rung failed and why.

### Step 2 — Anchor on the parent / known relation

If the user gives a relationship ("anak Noraniza Idris"), search the **anchor first**. The anchor (Noraniza Idris) is the verification:

- If the anchor has solid public footprint → the relationship question is open, but the family does exist
- If the anchor is also empty → something is broken upstream

Example result: Noraniza Idris confirmed via Wikipedia (`/wiki/Noraniza_Idris`, 14 languages), birthdate 27 Aug 1968, "Queen of Ethnic Pop," verified IG `@noraniza_idris`. Even with zero hits for "Aliff Haiqal," you can state the anchor as solid and the son-search as null.

### Step 3 — Namesake audit

Before declaring null, check for OTHER famous Malaysians with similar names. This turns a dead-end into evidence:

| Query | What to look for |
|---|---|
| "Aliff Haiqal" | Search variants → "Aliff" alone to surface Malaysian Aliffs (Aliff Aziz singer, Aliff Syukri entrepreneur, Aliff Rakib) |
| "Noraniza Idris" anak | Check Wikipedia family section explicitly — if missing, state that. Song titles are NOT children |
| Common Malay surnames | Idris, Noraniza — both common names, namesake trap is high |

State the ruling: "checked Aliff Aziz (singer), Aliff Syukri (entrepreneur) — different people, ruled out."

### Step 4 — Three-hypothesis null report

Don't fabricate. Don't ask 4 follow-ups. State three hypotheses with what unlocks each:

1. **Person exists but zero online presence** (private IG, no content creation) → unlock: IG handle, gym/workplace, event where seen
2. **Reported relationship is incorrect** (Noraniza Idris might be someone else, or the son is someone else's) → unlock: how user learned of the relationship
3. **Name is misremembered** → unlock: any alternate spelling, approximate age, what Ariff/Arif/etc. variants

End with: "Signal hang?" — single anchor ask, not four.

### Step 5 — Tool repair flag (for the operator, not the user)

If firecrawl_search returned HTTP 402 or SearXNG returned empty across the board, flag this in the subagent transcript. The session report (e.g., `/root/aliff_haiqal_report.json`) should note which rung failed so the operator knows to:

- Top up firecrawl billing
- Debug SearXNG backend (returns empty for real queries)

Don't write this as a session-blocking finding; treat as background maintenance.

## Worked example: Aliff Haiqal session

**User request:** "Find info about anak Noraniza Idris. Aliff Haiqal. Geng2 sado. Online reality"

**Walkthrough:**

1. Parallel `web_search` × 9 — all `{"web": []}` (SearXNG backend bug, not real null)
2. User pushback: "Jangan la skema sangat" — Mode B anti-skema lesson
3. Dispatch subagent with firecrawl tools
4. Subagent: firecrawl HTTP 402 (quota) → fell back to direct Bing curl + Wikipedia
5. Subagent found: Wikipedia anchor solid for Noraniza Idris, zero hits for Aliff Haiqal across 8 portals, no family section in Wikipedia
6. Namesake audit: Aliff Aziz, Aliff Syukri, Aliff Rakib — ruled out
7. Reported three hypotheses + single anchor ask
8. Wrote `/root/aliff_haiqal_report.json` for future reference

**Final user-facing message structure (Mode B anti-skema):**

- 2-3 line verified null
- "Apa aku tak boleh buat" refused section
- 4 unlock options (one IG/one workplace/one event/one confirm) — listed, not asked as form fields
- "Signal hang?" close

## When to skip this pattern

- User explicitly says "deep profile research task" → go full dossier Mode A, accept slower search cadence
- Public figure with extensive footprint (executives, ministers, A-list celebrities) → use `executive-intelligence-briefing`
- User gives a link / handle / known org at request time → go straight to verify, no probe ladder needed

## Pitfall: don't write "tool X doesn't work" as durable rule

The session note about firecrawl HTTP 402 / SearXNG empty is **environment-dependent failure**, not a durable constraint. Capture the FIX (top up billing / debug backend) as background maintenance, NOT as a "firecrawl is broken" skill rule. The agent should still try firecrawl first on the next run and report the actual state, not pre-refuse.