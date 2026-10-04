# SEA Bodybuilding Event Sources & URL Patterns

Compiled from Aug-Nov 2026 calendar research. Use as starting point for future event-finding tasks.

## Tier 1: Federation Websites (authoritative for dates, categories, fees)

### NPC Worldwide / IFBB Pro League
- **Master schedule**: https://www.ifbbpro.com/npc-worldwide/schedule/ — HTML table, filter by country. Last updated date shown. May miss some Philippines events.
- **IFBB Pro Malaysia**: https://www.ifbbpromalaysia.com/ — NPC Regional events in Malaysia. Pages per event: `/npc-regional-oct-2026` pattern. Includes categories, venue, hotel, registration tiers (Early Bird/Regular/Late).
- **IFBB Pro League Thailand**: https://ifbbproleaguethailand.com/events/ — Thailand NPC events. Individual event pages: `/thai-muscle-regional/`, `/thailand-nationals-pro-qualifier/`, `/thailand-pro-qualifier/`, `/thailand-mens-physique-pro-show/`. Promoter: Moe Elmoussawi (moesmuscle@yahoo.com).
- **NPC/IFBB Pro Korea** (handles Philippines): https://ifbbprokorea.com/philippines/ — NPC Philippines events. Promoter: Alex Hong (info@ifbbprokorea.com).
- **Musclecontest International**: https://musclecontestinternational.com/2026-musclecontest-philippines-event/ — MCI Philippines events. Also Vietnam: `/2026-musclecontest-vietnam-event/`. Promoter: Tamer El Guindy.
- **Muscleware registration**: https://www.muscleware.com/contests/<ID>/register — NPC athlete registration portal.

### PCA (Physical Culture Association)
- **International listing**: https://www.pcaofficial.com/international — **BEST single source** for PCA events globally. Lists date + city for all countries.
- **Thailand events** (promoter: Nic Edgerton):
  - `/bkknaturals2` — BKK Naturals 2 (2,400 THB)
  - `/eliteclassic` — Elite Classic Pattaya (1,900 THB)
  - `/firsttimerspattaya` — First Timers Pattaya (1,900 THB)
  - `/thailandnaturals3` — Naturals 3 Phuket (2,400 THB)
  - `/thailandnaturalchampionships` — Naturals Championships Phuket (2,400 THB)
  - `/thailandchampionships` — Thailand Championships Bangkok (2,200 THB)
- **Malaysia events**: CloudJoi ticketing: https://www.cloudjoi.com/shows/pca-malaysian-championships-2026
- **Indonesia**: `/indonesianchampionships` — 70 USD entry + £50 membership
- **Philippines**: `/philippineschampionships` — 3,000 PHP entry + £50 membership
- **PCA membership**: £50+VAT/year required BEFORE entry. Non-refundable.
- **Key pattern**: PCA Thailand runs 10+ shows/year. All promoter pages show fee + refund policy inline.

### INBA/PNBA (Natural)
- **Asia hub**: https://asianaturalbodybuilding.com/ — lists shows for SG, MY, PH, TH, VN, CN, JP, IN
- **Malaysia**: `/inbapnba-malaysia` — Rise of the Naturals (KL)
- **Singapore**: `/inbapnba-singapore` — Natural Universe (biggest Asia event)
- **Registration**: via Active.com (e.g., `/inba-pnba-pro-am-natural-universe-amateur-and-pro-qualifier-2026`)
- **Fees**: SGD 120-220/category depending on registration period. Doping test SGD 70.
- **Natural Olympia qualifier** — 15+ Pro Cards at Natural Universe.

### WNBF (Natural)
- **Singapore**: https://www.wnbfsingapore.com/event — Natural Elite Grand Prix
- **Member portal**: https://member.wnbfsingapore.com/
- **World Natural BB**: https://worldnaturalbb.com/international-events/ — lists dates for affiliates
- **Testing**: Polygraph + WADA-standard urine for EVERY athlete.

### WFF (World Fitness Federation)
- **Events page**: https://wff-international.com/events/ — global calendar with posters
- **WFF Thailand**: Instagram @wff_thailand, Facebook page
- **SE Asia Championships**: Pattaya, typically October
- **Malaysia circuit**: NABBA/WFF affiliated shows covered by TegapTV (typically local/state-level)

### ABBF/WBPF
- **ABBF events**: https://www.abbf.asia/Event.html — Asian continental championships
- **WBPF World Championships**: December annually (2026: Vientiane, Laos)
- **Registration**: via national federations, US$850 per person (accommodation included)

### State Federations (Malaysia)
- **PABBM**: Mr Malaysia national championship (Oct, various cities). Date announced via news.
- **SBBA**: Mr Sabah — Sabah state qualifier. Announced via Nabalu News, Daily Express.
- **PBBA**: Mr Penang — Penang state qualifier. Announced via Gabra MY, Kwong Wah.
- **State events feed into Mr Malaysia**: athletes qualify at state level to represent at nationals.

## Tier 2: Event Platforms (registration details, tickets)

| Platform | URL Pattern | Best For |
|---|---|---|
| CloudJoi | cloudjoi.com/shows/<event-slug> | Malaysian events, PCA Malaysia |
| Eventbrite | eventbrite.com/e/<event-id> | WFF, NPC, independent shows |
| Eventibus | eventibus.com/e/<event-id> | Global aggregator |
| HappeningNext | happeningnext.com/event/<slug> | Malaysian events |
| Active.com | active.com/n-a/other-endurance/<event-slug> | INBA/PNBA, FM Singapore |
| Muscleware | muscleware.com/contests/<id>/register | NPC athlete registration |

## Tier 3: Curated Calendars (cross-reference)

- **CrazyBadman**: https://www.crazybadman.com/blogs/news/2026-bodybuilding-fitness-competition-calendar — SEA competition calendar by country
- **Kompak store**: https://www.kompak.store/blog/2026-international-bodybuilding-show-calendar — International calendar
- **FM Singapore**: https://fitnessmovement.com.sg/ — Singapore nationals info

## Tier 4: News Sources (state events, local coverage)

- Nabalu News (nabalunews.com) — Sabah events
- Daily Express (dailyexpress.com.my) — Sabah
- BorneoPost (theborneopost.com) — Sarawak, national
- BorneoNews (borneonews.net) — Sarawak
- Harian Metro (hmetro.com.my) — National (use curl for extraction, see skill)
- Astro Stadium (stadiumastro.com) — National sports coverage
- Utusan (utusan.com.my) — National
- Kosmo (kosmo.com.my) — National
- Kwong Wah (kwongwah.com.my) — Penang focus

## Promoter Contacts (verified)

| Promoter | Region | Email |
|---|---|---|
| Hugo Chan | Malaysia, Indonesia | globalclassicmy@gmail.com |
| Moe Elmoussawi | Thailand | moesmuscle@yahoo.com |
| Alex Hong | Philippines, Korea | info@ifbbprokorea.com / alex@ifbbprokorea.com |
| Tamer El Guindy | Philippines (MCI) | tamer@musclecontest.com |
| Nic Edgerton | PCA Asia (all countries) | via pcaofficial.com |
| Steve Kim | Indonesia (Monsterzym) | contact@monsterzym.com |

## Verified Event Data (Aug-Nov 2026)

Key confirmed data points from this research session:
- Mr Malaysia 2026 = 55th edition, Oct 8-12, Alor Setar, Kedah
- NPC Regional Malaysia Oct 2026: 8 Pro Cards, Nexus Connexion Bangsar South, Early Bird closes 15 Jul
- PCA Malaysian Championships: First-ever PCA Malaysia Pro Qualifier, Oct 11, KLPAC
- INBA PNBA Natural Universe: First time in Asia, Sep 5-6, Singapore Airlines Theatre
- WNBF Singapore: 3-day event Oct 23-25, Kreta Ayer People's Theatre
- ABBF Asian Championships: Sep 22-28, Alexander Hotel Bangkok
- Musclecontest Vietnam: Oct 24, Rach Mieu Stadium HCMC (Pro + Olympia qualifier)
