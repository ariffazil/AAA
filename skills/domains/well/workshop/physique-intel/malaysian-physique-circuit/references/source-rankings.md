# Malaysian BB Scene — Source Authority Map

Proven scraping quirks + authority ranking, captured 2026-08-28.

## Authority ranking (1 = top)

### Tier 1: Primary reporting (use first)

| Source | URL | Best for | Verified quirks |
|--------|-----|----------|-----------------|
| Daily Express Sabah | dailyexpress.com.my | Mr Enrich Kinabalu results, Sabah BB news | Clean curl. Article URLs in search results. Full text extractable. |
| Stadium Astro | stadiumastro.com/sukan/... | Event announcements, prize/entry counts | Clean curl. Short articles — full body extractable. |
| Molek FM | molekfm.audio | Event announcements (NSTP syndicated) | Article body short — links back to NSTP for full text. |

### Tier 2: Industry media (login-walled)

| Source | URL | Best for | Quirks |
|--------|-----|----------|--------|
| TegapTV Malaysia FB | facebook.com/tegaptvmalaysia/ | Athlete names, captions, lineup | **Login-walled. curl returns 449KB login shell.** Use web_search for snippet extraction. |
| TegapTV Malaysia IG | instagram.com/tegaptvmalaysia/ | Photo captions, athlete reels | **Login-walled. curl returns 412KB login shell.** |
| TegapTV.com main | tegaptv.com | Industry articles | Clean. Upcoming-events page is **empty since Dec 2019** — schedule lives only on FB/IG. |

### Tier 3: Federation direct (sparse)

| Org | Verified contact/role |
|-----|----------------------|
| SSBA (Sabah Bodybuilding Association) | Pres Clarence Runggi |
| MFBB (Malaysian Federation of Bodybuilding) | VP Johanness Stanesslaous (also SSBA advisor) |
| Enrich Bodybuilding Club | Pres Krishnakumar Kalimuthu (pledged yearly Mr Enrich) |
| INBA/PNBA Malaysia | Asian Natural Bodybuilding site |
| WNBF Malaysia | worldnaturalbb.com (Malaysia slot listed but Date TBA) |

### Tier 4: International calendars

| Source | URL | Quirks |
|--------|-----|--------|
| WNBF | worldnaturalbb.com/international-events/ | **Clean curl.** 2026 calendar full; 2027 sparse. Malaysia Muscle Mash date TBA. |
| WFF International | wff-international.com/calendar/ | **JS-rendered — curl returns near-empty body.** Skip direct scraping. |
| IFBB Pro | ifbbpro.com/schedule/ | Pro only; not Syed's lane yet. |

## Scraping failure patterns (don't waste time on these)

- **Search engines on "Mr [Negeri]":** garbage disambiguation ("Mr." abbreviation noise). Always go direct to source URL.
- **WFF calendar:** JS-rendered. Don't curl.
- **TegapTV FB/IG:** Login-walled. Don't curl expecting content.
- **Tegaptv upcoming-events:** Empty since 2019. Don't curl expecting schedule.

## Recommended discovery order

1. `web_search "<event_name> 2026" site:dailyexpress.com.my` or `stadiumastro.com`
2. If poster/photo needed: `curl` IG/FB via `web_search` snippet, then `vision_analyze` if visual
3. Federation dates: direct to MFBB/SSBA FB pages (also login-walled — use search snippets)
4. International circuit: WNBF curl (works), WFF skip, IFBB Pro scrape if Pro-card relevant
