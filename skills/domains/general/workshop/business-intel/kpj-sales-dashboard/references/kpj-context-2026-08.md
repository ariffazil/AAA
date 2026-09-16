# KPJ Corporate & Empire Context (August 2026)

Session-detail reference for the KPJ vending lane. Read when renewal, expansion,
vendor-policy, or KPJ corporate-news questions come up.

## Empire state (as of 23 Aug 2026)

| Venue | Launched | Week-1 baseline | Notes |
|---|---|---|---|
| KPJ Damansara (KPJD) | pre-Aug 2026 | RM 140–250/day, ~RM 190 avg | Flagship. 8-day total 316 txn / RM 1,520.50 (14–21 Aug). Night window 9pm–12am = ~40% of revenue. |
| KPJ Rawang (KPJR) | 16 Aug 2026 | RM 24/day → RM 92–168 after day-5 breakout | Back area near staff/service lift. Breakout driven by Dendeng Nyet restock + burger stock. Week-1 total RM 395.70. Sales are SUPPLY-limited, not demand-limited — stock-outs (burger finished Fri, no top-up Sat) crater the day. |
| KPJ Ampang Puteri (KPJAP) | 20 Aug 2026 | RM 36–96 by day 3 | Fastest ramp of the three. TNG-dominant payment mix (55%), lunch rush 11am–2pm + late night 10pm+. Sandwich + milk sell well here. |

Cross-venue facts: all three report under merchant M46098 `WebOfProjects-VM(Cheras)` — venue separation is filename-only. Saturday is the softest day at every venue. Long weekends (holiday Tuesday + Monday leave) soften Sat–Tue across the board; Wednesday rebounds.

## KPJ leadership transition (user-relevant risk window)

- **Chin Keat Chyuan stepped down as President & MD effective 1 Sep 2026.** Confirmed via The Edge Malaysia (bourse filing, 21 Aug 2026): resigning "to pursue other interests" after 3 years. Prof. Datuk Dr Hanafiah Harunarashid (Group Chief Medical Director) is officer-in-charge pending a permanent appointment.
- 1HFY2026 financials at his exit: net profit RM 173.6M (+24.8% YoY), revenue RM 2.25B (+12.9%) — he left on strong numbers, so the exit is not performance-driven on the surface.

### MD/OIC succession history (verifiable portion, The Edge 21 Aug 2026)

| Period | Leader | What happened |
|---|---|---|
| ~2020–Apr 2022 | Datuk Mohd Shukrie Mohd Salleh | Ex-Pos Malaysia/MAHB CEO. Stepped down after a very short tenure (Edge cites 5 months for the final stretch). |
| 5 Sep 2022 – Sep 2023 | **Norhaizam Mohammad — OIC, NOT promoted** | CFO by role; held officer-in-charge ~1 year. Board hired outsider Chin instead of promoting her. Stayed on as CFO under Chin, left KPJ entirely Jun 2024. Current whereabouts unverified (SearXNG garbage results; marketscreener blocked). |
| Sep 2023 – 1 Sep 2026 | Chin Keat Chyuan | 25-year J&J veteran (country director J&J Malaysia, MD ONE J&J Malaysia). Left "to pursue other interests." |
| 1 Sep 2026 → | **Prof. Dr Hanafiah Harunarashid — OIC** | Group Chief Medical Director. Doctor, not corporate/finance. |

**The succession pattern (user asked about this 23 Aug):** the only prior OIC (Norhaizam, finance background) was passed over for an external hire. KPJ's board has repeatedly preferred external MD candidates (Shukrie from Pos Malaysia/MAHB, Chin from J&J) over internal promotion. Base case: Hanafiah returns to CMD when a permanent MD is announced, and the new MD is another external hire — watch for it. Unverified: the 4th MD departure in the decade count (likely the pre-2020 era, e.g. Amiruddin Abdul Satar) — don't cite as fact until confirmed.

- KPJ has had **4 MDs leave in 10 years** — leadership churn is normal there, don't over-index one resignation.
- The user wrote an advocacy letter (dated 14 Jul 2026) to the Johor MB / Johor Corp chairman criticizing the outgoing MD's Bumiputera vendor/leadership record — including naming Mynews, ZUS Coffee, QL/FamilyMart and CoffeeBot crowding out small Bumiputera operators in KPJ hospitals. The user's own vending business is one of the small operators that letter advocates for. Letter was sent **anonymous** (user confirmed 23 Aug) — lowers direct retaliation risk to his tenancy, but does not protect against a group-wide vendor policy change that hits all vending operators equally. Letter→resignation gap was ~5½ weeks; causation unproven and should NOT be asserted. User believes the MB acted on it behind the scenes — treat as unproven; advise watching ACTIONS (MD appointment character, vendor policy) not vibes.
- **Vendor risk window**: transition periods (Sep → new MD appointment) usually freeze new commitments but preserve existing arrangements. Officer-in-charge is a doctor (clinical focus), lowering near-term vendor-rationalization risk. Real exposure begins when a permanent MD lands — monitor Bursa/The Edge announcements for KPJ Healthcare leadership news.
- Practical advice given: don't act reactively; know tenancy/contract renewal dates; the user's 16+ daily dashboards are the strongest pitch asset if vendor review ever happens.

## News-verification pattern for theedgemalaysia.com (proven 23 Aug 2026)

`web_extract` fails (SearXNG backend is search-only) and `firecrawl_scrape` may fail on credits. The working fallback:

```bash
curl -sL --max-time 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "<url>" -o page.html
# then python: strip <script>/<style>, strip tags, unescape, find keyword, print ±window
```

Also note: SearXNG `web_search` for Malaysian proper names can return garbage (anatomy "chin" results for "Chin Keat Chyuan", Causeway/Antarctica pages for "Norhaizam"). If search returns irrelevant hits, go straight to the known outlet URL the user provides. marketscreener.com blocks curl with Akamai Access Denied — don't retry it.
