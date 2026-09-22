---
id: makcikgpt-civic-intelligence
name: makcikgpt-civic-intelligence
description: "Use when writing or planning a MakcikGPT article."
version: 1.0.2-2026.09.21
owner: AAA/Hermes
risk_tier: low
floor_scope: ['F2', 'F6', 'F7']
capability_tier: fed-reasoning-heavy
ecology_state: WARM
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

### 0a — Anchor on a dual figure the reader has already touched
For cost, subsidy, price and scarcity stories, the load-bearing figure is a **pair**: what the reader pays and what the thing actually costs, in the same paragraph, with the gap derived — pump price vs true price, bill vs generation cost, shelf price vs cost of inputs. One of the two numbers is something the reader has physically handled this week, and that is what makes the other one land. A single headline figure (a national subsidy bill, a total dividend, a restructuring headcount) stays abstract however large it is — attach it to a household unit within two sentences or cut it. Derive the gap inside the article instead of quoting anyone's summary of it; the arithmetic is the argument.

### 0b — The gap is the lagged channel, not the crisis already in every feed
The strongest gap for this series is the cost that has been **announced but not yet felt** — the second-order channel with a named delay (an input-cost shock that reaches the household basket months later; a scheduled restructuring whose consequences are future-dated). The story already in the headline is not a gap. Before drafting, write the sentence "X happens at N; the reader feels it at N+?" — if the answer is "already", the piece is a recap and needs a different gap.
State the delay out loud in the text; a reader told the timeline trusts the warning more than one shown only the direction.

### 0c — Universality first — no named company in pattern articles
When the article is about an institutional pattern (not a specific company's financials), do NOT name the company. Use archetypes: 'the last CEO who said no' instead of Wan Zul, 'the engineer who got an email instead of a conversation' instead of a named person, 'the department got smaller' instead of rightsizing. Every reader must see their own workplace in it. Specific numbers that only make sense with one company context → cut or generalise. The reader's own experience fills the details. Named companies belong in data-driven dossier articles (Rule 0a/0b apply); pattern articles belong to everyone.

### 0d — Character-as-evidence (the strongest angle)
When a real person's story illustrates the institutional pattern, that story IS the article's spine. Not data supporting a thesis. The person IS the thesis. Wan Zul resigning over Sarawak sales tax is not a data point — it is the entire argument about institutional shadow in one body. The GM who stays two hours talking about life is not colour — it is proof that humanity still exists inside the machine. Lead with the character. Numbers follow the character, not the other way around.

### 0e — Verify the URL the reader actually lands on
The slug in the .ts file is not the URL the reader sees. After `deploy-makcik.sh` reports "ALL CHECKS PASSED", the article is registered, built, served — but if the slug drifted mid-task (subagent rename, typo, sibling race), there may be two .ts files, one stale folder, or one URL that 200s the SPA fallback. **Never trust the slug you wrote; verify the slug the user clicks.** Test the exact URL you expect them to paste into chat: `curl -s <url> | grep -c "<unique signature word from your article>"`. A 200 + zero signature matches = the SPA is serving a fallback. The fix is a Caddy 301 redirect from the stale URL to the working one (see Pitfalls — Stale-slug recovery).

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
- **Timeline and encyclopedia pages are navigation, not sources.** For an event running across many months, a structured timeline page is the fastest way to establish the chronology — which actor did what, in which order, starting when — and it should be used for exactly that. Every figure it supplies must be re-sourced to Tier 1 or Tier 2 before it enters the draft, and the article names the Tier 1/2 source, never the timeline page. A number traceable only to the timeline page does not ship: derive it yourself from the primary figures instead, or leave it out. The timeline establishes the sequence; the primary document establishes the amount.

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
- **Register: felt by the ordinary reader, not deciphered by the analyst.** Arif's brief for these pieces is *bahasa manusia penuh rasa* — plain human language that a reader who does not work in the industry (and who does not read the filings) feels in the body. Machinery gets named as physical objects and household scenes (lampu buka tutup, muka orang yang kena, anak mak balik rumah), not as frameworks; the analysis arrives *after* the human detail, carried by Makcik in her own words. If a sentence would only land for someone who already knows the sector, it is the wrong register.
- **Never write as a mirror, a clerk, or a neutral witness.** A mirror reflects the institution's own framing back ("they say it is a polycrisis"), a clerk records facts without consequence, a neutral witness attests without weight. The piece exists to carry the consequence to the reader: name who pays, plant it in one person's ordinary evening, and let the anger come from the arithmetic rather than the adjectives.

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
- **Missing character = missing proof.** If the institutional pattern has no human face, the article stays abstract. The Wan Zul article works because one person's departure IS the entire argument. "Rightsizing" without a named story of a 13-year zero-dry-wells geoscientist receiving an AI email is a press release, not a MakcikGPT article. Always ask: whose body illustrates this pattern?
- **essays.json AND git tracking are both manual.** Creating the `.ts` file, adding to `index.ts`, AND adding to `essays.json` is NOT enough. The files must also be `git add` + `git commit` before `npm run build`. Untracked files do not appear in the build output. Symptom: `curl` returns the old markdown mirror instead of the SPA shell. Deploy-makcik.sh will warn about unregistered articles but will NOT auto-register or auto-commit. Missing git commit = article missing from live site even though code exists.
- **Subagent scope drift — extra files beyond the article trio.** When delegating article forging to a background `delegate_task` subagent, scope drift is common: subagent creates React components (panels, pages), video assets, audit reports, or unrelated companion articles that were never requested. ALWAYS constrain in the directive: "ONLY create `<slug>.ts`, `<slug>.md`, and modify `index.ts`. No components, no panels, no pages, no video assets, no other source files. If you think you need anything else, STOP and ask." Post-delegation audit: `git status --short sites/arif-fazil.com/` — anything outside the article trio + index.ts is drift.
- **Subagent slug rename breaks deployment.** Subagent may rename the slug mid-write (e.g., `truth-dalam-void` → `truth-sembunyi-dalam-void`), creating two .ts files where one was requested. Both files share the same internal `slug` string, so React throws a duplicate key warning and one slug 404s. Lock the slug at delegation time: "Use this slug: `<exact-slug>`. Do NOT rename it for any reason." After delegation, `ls src/data/makcikgpt/ | grep <topic>` should return exactly one file.
- **Probe-for-existing BEFORE delegating an article.** If the topic already exists in the corpus (e.g., "Kenapa Syarikat Tu Hantu" already existed at 16k chars when a subagent was asked to write it), the subagent will silently overwrite the existing draft. Always include in the directive: "First, run `ls src/data/makcikgpt/ | grep -i <topic>` and `grep -l '<core-concepts>' src/data/makcikgpt/*.ts`. If similar content exists, READ it before writing. Either build on it or explicitly fork a different angle." Proven 2026-09-22: an existing 16k-char article was overwritten with a sub-shorter draft before main thread noticed.
- **Stale-slug recovery: Caddy 301 redirect, not code rollback.** When slug drift has already deployed — wrong URL 200s the SPA fallback, right URL serves the article — the surgical fix is one Caddy 301 redirect block in `/etc/caddy/vhosts/arif-fazil.com.conf` (template: see OP 3 in `forge-agentic-web-builder` for the redirect snippet). Do NOT git revert the .ts rename; do NOT rebuild+rsync hoping the SPA falls back differently. A Caddy redirect is one config block + one reload + one HTTP probe. The user clicks the wrong URL → 301 → working URL → article. Time to fix: ~3 minutes. Time to fix by rebuild+rsync with a fresh slug: ~30 minutes plus the risk of breaking other articles.
- **Verify by content, not by status code, after URL fix.** When the user reports "page is wrong" or "page says X but should say Y", a 200 is not enough. `curl -s <url> | grep -c "<distinctive word from your article>"`. If the count is zero (or matches only the SPA fallback template), the page is serving the wrong content. Status-200 + content-wrong is the silent failure mode; doctor must read the body, not just the headers.

## Related
- `petronas-knowledge-router`
- `internal-first-probe`
- `FORGE-agentic-web-builder`
- `references/provenance-sourcing.md`
- `references/subagent-delegation-discipline.md`