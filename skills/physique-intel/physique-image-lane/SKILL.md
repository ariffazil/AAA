---
name: physique-image-lane
description: "Use when Arif wants physique photo references found."
version: 1.0.0
author: arifOS federation (F13 sovereign private lane)
license: private-sovereign
tags: [physique, bodybuilding, image-search, immich, provenance, private-lane]
capability_tier: fed-agent-subagent
ecology_state: HOT
metadata:
  hermes:
    tags: [physique, bodybuilding, image-search, immich, provenance]
    related_skills: [malaysian-physique-circuit, image-gen-fallback-chain]
---

# Physique Image Lane

## When to Use

- Arif asks to find stage/physique/gym photography, posing references, or contest galleries.
- A physique reference must be credited, dated or checked live before it is used or kept.
- A local photo library (Immich/PhotoPrism) needs to be queried or wired.

Turn "cari foto physique / posing / pertandingan" into live, credited, verifiable references
instead of scraped guesses. Private lane — never published, never sent to third parties, never
used to build content of a named real person.

Tool: `/root/scripts/physique_search.py` (stdlib only, ledger in
`~/.hermes/lane/physique/ledger.db`).

```
python3 /root/scripts/physique_search.py find "<query>" --limit 8 [--domains npcnewsonline.com]
python3 /root/scripts/physique_search.py probe <url> --save
python3 /root/scripts/physique_search.py list --limit 30 [--tier A_OFFICIAL]
python3 /root/scripts/physique_search.py add <url> --creator "X" --license "Y" --review approved
python3 /root/scripts/physique_search.py drop <id>
python3 /root/scripts/physique_search.py immich "<phrase>" --limit 10
```

## Search surface facts (verified 2026-10-20)

- `find` uses the Exa API (`EXA_API_KEY`, read from env or `/root/.secrets/kunci-root.env`).
  Verified live: NPC News Online contest galleries, profitnessphotos galleries, Malaysia NPC
  Worldwide Classic and Mr Malaysia coverage all return real URLs.
- Source tiers come from the domain, not from content sentiment: `A_OFFICIAL`
  (npcnewsonline.com, contests.npcnewsonline.com, ifbb*.com, profitnessphotos.com,
  musclememory.com, malaysiabb.com, msia.org.my) · `B_UNVERIFIED` (everything else,
  `review=pending`) · `BLOCKED` (explicit-adult domains, never inserted).
- `probe` records what the host actually answered (HTTP status, final URL, og:title, og:site_name,
  author, published date). A title from a search API is a claim; probe status is a measurement.
  Only the measurement lands in `live_status`.

## Content filtering — what the software can and cannot do

- **Immich v3.3.3** (latest, 2026-10-14): `POST /api/search/smart` takes
  `{query, page, size, type, ...}` and returns assets under `assets.items[].id`; thumbnails at
  `/api/assets/{id}/thumbnail?size=preview`. Its OpenAPI spec contains **zero** occurrences of
  `nsfw`, `moderation`, `sensitive` or `explicit` — Immich ships no built-in explicit-content or
  age filter. Do not promise one.
- **PhotoPrism** (latest `261007-65faaae5d`): does ship a real detector (`internal/ai/nsfw`,
  wired into classification as `NSFW` / `NSFWConfidence`) plus `photo_quality` search filters.
  If a library needs an explicit-content gate, PhotoPrism is the one that actually has it.
- Age is never inferred from appearance. `age_attested=0` until a source is attested (official
  competitor gallery, federation entry list). Say "not attested" out loud.

## Laws of this lane

1. **Credit or don't keep it.** Creator + licence when observed; `-` when unknown. Never invent.
2. **Tier A first.** Discovery returning only `B_UNVERIFIED` rows is a weak result — say so.
3. **No login-wall scraping.** Instagram/X/Facebook answer with walls from this host; ask for a
   screenshot instead of pretending a fetch worked.
4. **Probe before delivery.** An unprobed URL is "found", not "live".
5. **Delete is a feature.** `drop <id>` works on first ask, no explanation needed.
6. **Local library is optional.** Immich/PhotoPrism index *your* collection; they are not web
   search engines. Never describe them as one.

## Pitfalls

- DeepWiki and other repo-summary services produce plausible tables with missing API detail.
  Verify against the OpenAPI JSON
  (`raw.githubusercontent.com/immich-app/immich/main/open-api/immich-openapi-specs.json`) or the
  source tree — not a summary.
- Exa `publishedDate` is frequently null even for dated galleries. Fill it from the probe.
- `find` dedupes on exact URL; tracking-parameter variants of one gallery create duplicate rows.
  Strip query strings before `add` when the query is only analytics.
- Never merge one athlete's identity across sources. Same face, different person is a real
  failure class in physique photography (lighting, tan, dehydration).
