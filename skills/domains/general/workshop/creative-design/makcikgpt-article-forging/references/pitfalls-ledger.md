# Pitfalls ledger — makcikgpt-article-forging (full)
> Moved verbatim 2026-10-23. SKILL.md keeps the top pitfalls.

## Pitfalls

1. **Don't write without research.** Minimum 3 searches before writing. MakcikGPT articles are data-driven, not opinion-driven.
2. **Don't use English in body.** BM only. English for direct quotes, data values, and proper nouns.
3. **Don't summarize news.** MakcikGPT finds the HIDDEN THREAD. If the article reads like a news summary, rewrite.
4. **Register in BOTH places or article won't appear in RSS/sitemap/llms.txt:**
   - `src/data/makcikgpt/index.ts`: add import + `makcikArticleModules` + `makcikArticlesMeta` entry
   - `src/data/essays.json`: add entry with `lang: "bm"`, `dest.type: "onsite"`, `dest.path: "/world/makcikgpt/<slug>"`
   - **Article scavenger audit:** Before any deploy, scan for orphan .ts files that exist but aren't registered in index.ts:
     `for f in src/data/makcikgpt/*.ts; do slug=$(basename "$f" .ts); [ "$slug" = "index" ] || [ "$slug" = "types" ] || [ "$slug" = "fix" ] || [ "$slug" = "jsonld-blocks" ] || grep -q "'$slug'" src/data/makcikgpt/index.ts || echo "⚠️ UNREGISTERED: $slug"; done`
   - **NOTE:** index.ts uses SINGLE quotes for slugs (`'slug-name'`), not double quotes. A grep for `"$slug"` will return false negatives.
   - **essays.json check:** Also verify registration in essays.json via `grep "/world/makcikgpt/$slug" src/data/essays.json`. The slug lives in the `dest.path` field.
5. **Don't skip the build.** Always run `npm run build` before deploying. If build fails with TS2688 (vite/client type defs), run `npm install --legacy-peer-deps` first.
6. **Don't deploy without verifying.** Run the Deploy Verification Protocol (above) — check JS bundle hash, article 200, listing 200, feed/sitemap/llms.txt all contain the slug.
7. **Don't use the cover-title for the slug.** Slug should be kebab-case English, title can be BM.
8. **Don't omit the epistemic declaration for kutuk-mode articles.** But for rakyat marhaen articles — strip it. Arif: "The moment aku nampak epistemik. Aku dah down." Detect from phrasing: "rakyat marhaen", "makcik kampung", "relatable", "jangan susah" = rakyat marhaen mode.
9. **VERIFY EVERY FINANCIAL NUMBER before publishing.** Cross-check against primary sources (PETRONAS IR, FRED, BNM). In session 2026-07-13, FY2022 PAT was incorrectly stated as RM55b (actual: RM101.6b). Gemini external audit caught it. Pitfall: mixing FY2024 numbers with FY2022 narrative. Always check the five-year table in IR2025 page 218.
10. **VPS deploy is safer than Cloudflare Pages.** Use manual rsync (dist/ + public/makcikgpt-md/) + caddy reload. `deploy-vps.sh` may fail with registry schema validation; `scripts/deploy-site.sh arif-fazil.com --apply` is reliable but manual sync is safest.
11. **Don't moralize confidentiality on routine internal docs.** When Arif shares an internal email (HRBP memo, MYPR procedure, division circular), treat as governance visibility, NOT as classified leak. "Internal Use For Internal Distribution Only" = internal etiquette, not securities-grade confidentiality.
12. **Don't default to v1 kutuk when Arif asks for mass-reach essay.** When Arif signals "pastikan manusia boleh relate" / "relate to my life" / "bukan untuk AI lab orang", switch to v2 relatable mode automatically.
13. **"Verify again" = full re-check, not just confirmation.** When Arif says "verify again" or "check balik", re-run verification against primary sources. Don't just confirm.
14. **"Check balik X" = find the primary source.** Search the SOURCE ARTICLE title, not the person's name + role. Wrong search terms produce false negatives.
15. **NEVER report access blocks as problems. NEVER ask Arif to paste content.** Exhaust the full fallback chain (search → browser → forge_search → subagent → local files → training data) before admitting defeat.
17. **Don't assume deploy = distribution.** After deploying to arif-fazil.com, run Stage 8 (DISTRIBUTE): Telegram link, WhatsApp excerpt, social teaser. "Published on arif-fazil.com" is not "read by jiran-jiran."
18. **Don't overuse "DITEMPA BUKAN DIBERI" as a closer.** Arif: "Hang jangan nak ditempa sangat." It's becoming a filler word that dilutes the phrase's meaning. Use it ONCE at the end of articles that genuinely earned it through the forging process. For quick-response pieces or conversation replies — skip it entirely. The phrase is a constitutional marker, not a sign-off ritual.
19. **Don't write essays when Arif wants conversation.** Arif's signals for SHORT mode: "tell me about X", "what do you see", "ok now tell me about Y" — these are invitations to discuss, not to produce a thesis. Match length to signal. If the question is one line, the answer should be 1-3 paragraphs max. Save the long-form for when he says "draft one article" or "buat pdf."
20. **Verify claims against LinkedIn before writing.** Arif made a claim about Taufik ("ex CFO Sapura sebelum PN17") — I initially got the framing wrong ("jaga syarikat bagi tak runtuh"). LinkedIn showed the actual dates: Taufik chow Jan 2015, PN17 May 2022. He left BEFORE the collapse. The correction changed the article from "he protected the company" to "he left before the bomb he built went off." Always check the timeline against primary sources before accepting the user's framing — they may be approximately right but temporally wrong.
21. **Check BOTH webroots for /world/* sections before adding pages (2026-08-21).** /world/politics/* (and other /world/ sections) serve from /var/www/html/world/... — a DIFFERENT root than /var/www/html/arif/. The canonical public URL is /world/politics/shadow/<slug>; the /politics/* form 308-redirects. Before building an SPA page for a /world/ path, ls /var/www/html/world/<section>/ — a parallel Claude/OpenCode session may have already deployed a static page there, and Caddy try_files static match beats your SPA fallback on every URL variant. Verify greps with -L (redirects return empty bodies without it). Full collision story + page-build detail: references/anwar-33-bayang-page-build-2026-08-21.md
22. **npx tsc --noEmit can pass while npm run build (tsc -b) fails (2026-08-21).** When a hand-written .ts data file has unescaped quotes inside double-quoted strings (TS1005/TS1002 at specific columns), --noEmit and -b resolve differently. Trust tsc -b. Fix loop: locate exact positions via sed -n Np piped to python3 char-scan, repair with python line-replace (inner double quote to single quote, terminator .', to .", ). Prevention: write data-file bodies with single-quote internals from the start.
23. **Don't populate an unnamed relationship role with a specific person's traits (2026-09-30).** When the user asks for an article about an unnamed relationship role ("apa yang perempuan x faham", "what X is doing to me", "why men want Y"), write at the class/archetype level (patterns, types, observations across many people) rather than inventing a specific person's traits to fill the role. Writing a specific person without naming them converts the article from an analysis of social patterns into a complaint record against an unspecified individual — a record that cannot be retracted and encodes one session's conflict as durable truth. When the user says "buat ja" (just do it), treat it as a stop-asking signal: produce the article at the archetype level (no faces, no names, no role-proxy) and flag in the delivery that the document covers patterns, not a person.


---

## References

- `references/session-2026-07-15-learnings.md` — Key learnings: "Fix all" pattern, 13-article audit pattern, rasa rewrite pattern, Gödel lock now LIVE in kernel, unified site header, SOUL.md v3 sealed, infrastructure audit edge+origin pattern, "verify again" = full re-check not confirmation.
- `references/site-deployment-pitfalls.md` — AAA Cockpit dist/ in .gitignore (must copy to /var/www/html/aaa/), arifOS kernel restart pattern (stuck deactivating → kill → start), A-FORGE stub redirect, GitHub push protection Mapbox key.
- `references/deploy-architecture.md` — Cloudflare Pages + VPS deploy mechanics
- `references/research-pattern.md` — search strategy & evidence tagging
- `references/hitl-essay-v2-2026-07-10.md` — concrete example of "kutuk mode" essay
- `references/hitl-essay-2026-07-10.md` — kutuk mode essay (dual-target sharp critique)
- `references/narrative-debunking-pattern.md` — 3-layer pattern for articles that debunk popular narratives. "Betul, tapi..." rhythm: acknowledge kernel truth → show what's wrong → reveal hidden thread.
- `references/religious-authority-research-brief.md` — Malaysia religious authority misconduct research brief.
- `references/searah-evidence-archiving-pattern.md` — immutable evidence pack pipeline: Companies House deep-read → press release fetch → WoodMac analysis → evidence ledger → browser screenshots.
- `references/rakyat-marhaen-voice-pattern.md` — how to write for makcik kat pasar: no epistemic labels, no Greek symbols, numbers as words, metaphors replace analysis.
- `references/external-auditor-framework.md` — External auditor agent cards (ChatGPT/Gemini/Grok), Gödel lock enforcement code paths.
- `references/site-infrastructure-audit-pattern.md` — Edge + origin dual probe for site auditing. Diagnosing blank pages (hash mismatch, runtime error, stub). Cloudflare cache purge.
- `references/makcikgpt-article-404-diagnostic.md` — Two-handler split-brain diagnostic workflow. Bot-vs-browser divergence patterns. Decision tree for 404 root causes (2026-07-31).
- `references/anwar-9-shadows-factpack-2026-08-21.md` — Sourced fact pack behind the 9-shadows Anwar profile: class origin (father hospital porter→MP), MCKK elite path, false Baling starvation report, 2010 APCO censure inversion, family machine, DNAA/Zahid, RM1.3T debt record. Wikipedia multi-pass extraction method documented inside.
- `references/anwar-33-bayang-page-build-2026-08-21.md` — 33-bayang page build: SPA-vs-static parallel-agent collision, /world/* dual-webroot routing, TS quote-repair loop, 33-shadow content spine for N-shadow dossiers.
- `references/anwar-33-bayang-session-2026-08-21.md` — Session notes for the 33-bayang deep-dive page: subagent research delegation pattern (output_schema → 322-line sourced briefing), search-engine-total-failure fallback chain, /world/ vs /arif/ dual-webroot deploy rule, hub-card clickable wiring, editorial-register voice switch, Claude Code sibling co-working (ingest + build on top, deploy the better-sourced draft).