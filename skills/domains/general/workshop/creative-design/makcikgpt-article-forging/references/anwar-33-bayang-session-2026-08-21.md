# Anwar Ibrahim 33-Bayang Session — Research + Build Notes (2026-08-21)

Session that produced `/world/politics/shadow/anwar-ibrahim` (33 shadows, 3 axes × 11) and the clickable hub card.

## The full research trail

1. **Subagent deep-research delegation worked.** One background leaf with an `output_schema` (childhood/schooling/activism/UMNO-rise/sodomy-cases/personal/wealth as JSON keys) ground through 85 API calls / ~27 min while the main thread kept answering Arif. Result: `/root/anwar-research/ANWAR_IBRAHIM_RESEARCH_BRIEFING.md` (322 lines, 13 sources).
   - Search engines were ALL degraded that day: SearXNG returned identical junk for every query, firecrawl credits exhausted, browser_exec crashed (exit 1), Reuters 401, Al Jazeera/BBC 404, archive.org 429, DuckDuckGo captcha, Mojeek 403.
   - What worked: direct `curl` of Wikipedia EN+MS (main + family members + Reformasi + ABIM + MCKK + sodomy-trials + 2023 film pages), Britannica via Wayback, Wikipedia search API for name-collision resolution.

## Key verified facts behind the class-thesis ("anak orang senang acah orang susah")

- Father Ibrahim Abdul Rahman: hospital porter → UMNO → **MP Seberang Tengah 1959 & 1964** → Parliamentary Secretary Health 1964–69 → Dato'/DSPN 1989 → died resident of **Country Heights Kajang**. Malay Wikipedia carried the Country Heights + titles facts; English didn't.
- Mother Che Yan: head of UMNO Women Bukit Mertajam division.
- Britannica's three-word verdict: **"the son of politicians."**
- MCKK ("Eton of the East") — one of only 3 Penang boys selected; classmates Sanusi Junid, Kamaruddin Jaafar.
- 1974 Baling trigger: starvation-death report **later proven false**; rubber hardship real; 20 months ISA = real price paid. Structure: borrowed others' pain, paid in own freedom, exited as brand.
- 1982 UMNO entry on al-Faruqi's advice; Permatang Pauh = seat carved from father's old constituency. DPM in 11 years.
- Birthplace itself is audience-relative: Cherok Tok Kun (record) vs Sungai Bakap (claimed while campaigning there, 2023 — FMT/MalayMail receipts).
- Wan Azizah: born Singapore, Peranakan Chinese descent, Royal College of Surgeons Ireland, ophthalmologist — the other half of the class story.
- Sexuality: write ONLY the court-record grey zone + "konspirasi" as sole answer across 26 years. No orientation claims either way. Unverified YouTube interview = UNKNOWN, excluded.
- Final collapse line: "Acah bukan strategi dia. Acah adalah identiti dia" — and the stronger form: "Anwar bukan orang susah yang berjaya. Dia orang senang yang jumpa rezeki dalam cerita orang susah."

## Build notes (33-bayang page)

- Standalone HTML at `public/politics/shadow/anwar-ibrahim/index.html`, ~45KB. CSS = hub's full `<style>` copied + additive block for `.shadow-card/.shadow-num/.shadow-title/.shadow-quote/.shadow-body/.shadow-evidence/.axis-label/.summary-box`.
- Axis structure came FROM Arif verbatim ("3 axis - 11 each. Socio politics - economy - personal") — do not invent your own taxonomy when he specifies.
- Card #33 gets `border-color:var(--gold)` + surface background = the "deepest" visual rank.
- Editorial register (his ask: "Real editorial psychology analysis... Not makcikGPT voice"): BM formal-analitical, Jung cited, evidence line per card, no kampung metaphors.

## Deploy gotchas hit (all fixed same session)

- `/world/politics/*` serves from `/var/www/html/world/...` — different webroot than `/var/www/html/arif/...`. Deploy to BOTH.
- `curl --resolve` without `-L` on a 308 path returns empty body — verify greps read nothing.
- Card HTML string-inserts can break `legacy-label` div nesting — compare against a healthy sibling card + HTMLParser balance check before rsync.
- Public verify must hit `/world/politics/shadow/...` (canonical), not `/politics/...` (redirect).
- Cloudflare purge API returned success:false (token scope) but public edge refreshed anyway — don't block on purge failure; re-check public before assuming stale.

## Sibling-agent co-working note

Claude Code (PID on pts/6) had concurrently: written a richer `taufik-klcc-ceo-petronas.ts` (Tanjung Deputy Group CFO Feb–Dec 2012, 11 months; SapuraKencana CFO Dec 2012–Jan 2015 with $2.83B Seadrill + $900M Newfield debt acquisitions; chow Jan 2015 before oil crash; FY2025 numbers) AND shipped cover/fact-box/pull-quote CSS + reading-time badges + next/prev nav + spa-shell. Right move: ingest + build on top, commit their uncommitted work on the shared feature branch (`feat/taufik-article-20260821`), never revert. Their article was BETTER-sourced than the Hermes draft — deploy theirs, not yours, when both exist.
