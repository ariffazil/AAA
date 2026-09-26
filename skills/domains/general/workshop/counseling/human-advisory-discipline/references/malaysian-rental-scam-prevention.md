# Malaysian Rental Scam Prevention — Pre-Purchase Verification

Load this BEFORE the tenant pays any deposit. The umbrella skill and `references/malaysian-tenancy-access-dispute.md` cover what to do after a breach or unlawful eviction; this file covers the upstream discipline that keeps the breach from happening. This is the **before-you-sign** layer.

The discipline is verification, not contract review: every check here is something the prospective tenant does **before** signing or paying, and every check answers the same single question — *is the person offering the unit legitimate, and is the unit real?*

## 1. The ACE rule (BOVAEP / LPPEH, Malaysia 2026)

When dealing with anyone claiming to be a real-estate agent, demand three checks before paying a single sen:

- **A — Ask for the Ren (Real Estate Negotiator) tag.** Every registered agent carries one. The tag has a QR code. A refusal, a "we'll settle later", a "I'm the owner not an agent" answer — these are all red flags. Do not proceed without seeing the tag.
- **C — Check the tag's QR + LPPEH portal.** Scan the QR; it links to the official LPPEH record. Cross-verify at **https://lppeh.gov.my/search-listing** — type the REN number directly. The portal is the sole authoritative source. Trust scores from third-party sites (Scamadviser etc.) are noise compared to the LPPEH government record.
- **E — Enforce the report.** Scam attempt? Report: BOVAEP complaint channel + police report + (for the platform) report-scam form. Whether or not the tenant lost money, the report matters for the next victim.

A licensed agent's company account is registered with BOVAEP / LPPEH and the deposit is paid into a **client/agency account**, never into a personal bank account or personal QR. Anything else is a scam until proven otherwise.

## 2. The seven red flags (session-verified against BOVAEP / SpeedHome / Threads @hartanahgirl, 2026)

1. **Pressure to pay fast.** "Ada orang lain menunggu", "slot esok je", "promosi terhad tengah malam ni". Scammers exploit urgency.
2. **Deposit into a personal bank account or personal QR.** Licensed agents use the agency's client account. Cash or transfer to a private individual = private scam.
3. **Fully furnished at 25%+ below market.** Listing price too good = honeypot.
4. **No physical viewing allowed before deposit.** "Trust the photos, I'm overseas". The real owner/agent will arrange viewing.
5. **Homestay-scam modus operandi.** Scammer rents a real homestay for 1-2 weeks, strips all "homestay" signage, photographs the unit as if it's their property to let, posts on Mudah.my / Facebook Marketplace, collects deposits from multiple victims, disappears when the actual homestay booking expires.
6. **QR-code payment without invoice/agreement.** Avoid; QR is the scammer's friend.
7. **Multiple-owner property without consent of co-owners.** The person offering the unit may have no right to. Verify via the building's JMB / MC (Joint Management Body / Management Corporation).

**Single strongest signal:** a licensed agent will never object to Ren-tag verification + LPPEH check. Anyone who objects is hiding something.

## 3. The 48-hour student move-in framework

When a new student has 48 hours or fewer before class start and may already have touched a scam (true case in this library, late September 2026):

| Hour | Action |
|---|---|
| 0-12 | List 5-7 candidate units on **verified platforms only** (iBilik, Speedhome, RoomGrabs, Swing & Pillow, Carousell with verified sellers). Avoid random Facebook marketplace. |
| 12-24 | WhatsApp each: ask for Ren tag, ask for JMB/MC contact, ask for strata title. Three no-answer replies = remove from list. |
| 24-36 | Physical viewing for top 2-3. Bring: IC, deposit cash, phone camera, the ACE checklist printed. |
| 36-48 | Verify with JMB/MC on-the-spot. Check owner IC vs title. Read the agreement (lawyer optional but recommended for 1-year lease). Pay deposit only via proper channel. |

If the 48-hour clock is impossible, the fallback is a 3-day Airbnb / short-let while proper verification runs in parallel. Do not sign a defective contract to "make the deadline". Late signing is cheaper than an eviction by a ghost landlord.

## 4. Canonical verification URLs (Malaysia, 2026)

| Verify | URL | Why this URL |
|---|---|---|
| Agent licence (Ren tag) | https://lppeh.gov.my/search-listing | Government LPPEH portal — the only authoritative source |
| Company registration (SSM) | https://www.ssm.com.my/Pages/Search_Company.aspx | Companies Commission — verify e.g. iBilik Tech Sdn Bhd (1382832-P) |
| Platform legitimacy | https://www.scamadviser.com/check-website/<domain> | Secondary trust signal; third-party score, **lower priority than LPPEH** |
| Report scam to BOVAEP | bovaep.gov.my / LPPEH complaint channel | Required for licensed-practitioner fraud |
| Report to PDRM | 999 (emergency) or any balai polis | Required for all scam categories |

**LPPEH is the only authoritative source for agent legality.** Scamadviser and similar scores are informational only — a high score doesn't mean an agent is licensed, it just means the website isn't a known phishing domain.

## 5. Platform trust tier (Malaysia, 2026)

| Platform | Verification model | Trust level |
|---|---|---|
| iBilik.com (iBilik Tech Sdn Bhd 1382832-P) | Identity verification of both sides; escrow for some listings | High |
| Speedhome.com | Agent + tenant background checks (their own system, not LPPEH) | High |
| RoomGrabs.com | Platform-managed | High |
| Swing & Pillow | Co-living operator — zero-deposit model = platform assumes landlord risk | High |
| Carousell Malaysia | Open marketplace, identity verification uneven | Medium (verify seller heavily) |
| Random Facebook groups | No platform escrow, no identity verification | Low-Medium |
| WhatsApp-only contact, no platform | No verification at all | **AVOID** |

Established platforms have anti-scam measures built in (escrow, identity verification, dispute resolution). They still aren't foolproof — listings on them can be fraudulent; only the platform's *enforcement* is more reliable than a random Facebook post.

## 6. Image verification (because listings can't show real photos in advance)

The advisor cannot fetch up-to-date photographs from the listing — the photo set changes between agent uploads and view day. Three protocol items the prospective tenant runs at the viewing:

1. **Ask for 3-5 photos sent now with timestamp.** Real owner has no problem providing.
2. **Reverse-image search** the listed photo (Google Images / TinEye) to catch listings reusing homestay or stock photos.
3. **Insist on a video call walkthrough** before any deposit payment. The owner walks through the unit live; if they refuse, walk away.

## 7. Live-platform cross-check (advisor does this before recommending)

A listing on iBilik today may be re-listed tomorrow under a different agent, or pulled entirely. The advisor runs a live cross-check before naming any candidate as "verified":

1. **Pull the platform's location page** (`/locations/malaysia/selangor/<area>` for iBilik) — confirm the listing still appears with same price, agent name, and WhatsApp number.
2. **Extract the WhatsApp link** directly from the live page — `wa.me/<number>` form. The displayed number and the wa.me link must match. A listing that shows one number and links to another is a red flag.
3. **Record the WhatsApp link as the verified contact**, not the number alone. The link is the artifact the tenant opens; the number is what they read.
4. **Mark every unverified entry as such in the comparative table.** If the agent contact was not on the live platform page, the row is UNVERIFIED — the tenant must verify via Ren tag + LPPEH before any commitment.

The tenant's principal will ask: "bagi gambar, link, phone number for each listing reality hang jumpa. Jangan nak letak link menipu." The answer to that is the live cross-check, not a fabricated table. Never fabricate a contact or link. If you cannot reach the live page, say so and downgrade the row.

## 8. Gotong-royong multi-candidate ranking

When the principal asks for a comparative ranking of multiple verified candidates (a "gotong royong" decision), rank on weighted criteria that match the principal's actual constraint, not on price alone:

- **Distance to base** (the principal's home, or wherever the principal wants quick access) — drive time off-peak AND peak separately. KL/Selangor peak (7-9 AM, 5-7 PM) often doubles off-peak time on the same road.
- **Distance to daily destination** (workplace / campus) — same dual-time treatment.
- **Price affordability** — total first-month cash (rent + deposit) is the number, not monthly rent.
- **Safety flags** for the tenant profile (female-only units score higher when the tenant is female; ground-floor rooms score lower; window grills for child tenants).
- **Agent/platform verification** — platform-managed scores higher than WhatsApp-only.

Weight the criteria that map to the principal's stated constraint first. If the principal said "I want my sibling close to me in case she needs help", proximity to the principal's home dominates. If the principal said "budget is the priority", total first-month cash dominates. Document the weight rationale in the deliverable so the principal can disagree with the weights, not just the result.

**Distance-measurement pitfall:** do not trust your initial estimate of peak-hour time. Peninsular Malaysia daily commuters know the real peak-hour multiplier on every road; if your estimate exceeds theirs ("60-75 min" when they say "20 min kalau tak jam"), redo the calculation with their anchor as the off-peak baseline. The principal drives that road; the agent does not.

## 9. Distance + Google Maps deliverable shape

When producing a comparison HTML for the tenant:

- **Do NOT use the Google Maps embed iframe** with the `pb=...` parameter from the API inspector — it returns "Invalid 'pb' parameter. Rejected." and breaks the page.
- **Use plain `https://www.google.com/maps/dir/<origin>/<dest>` links** for each candidate. They open in Google Maps on any device with directions pre-filled. No API key, no rejection.
- **Include a "master map" link** to `https://www.google.com/maps/dir/<origin>/<daily-destination>` for the general route, plus individual links per rental.
- **Compute distance via haversine** between verified coordinates, then multiply by a road factor (~1.3-1.4×) to estimate road distance. Use two time estimates: off-peak at ~50 km/h average and peak at ~30 km/h average. State both.

## 10. Notion export ingestion

Notion exports arrive as `ExportBlock-<uuid>.zip` containing a nested `...-Part-1.zip` which contains the actual `.md` files. To ingest:

1. Unzip the outer — extracts one inner `.zip`.
2. Unzip the inner into a working directory.
3. Read the markdown files.

The double-zip is by design for size limits; do not flag it as corruption. Each export is a single block containing one page's worth of content. If the user uploads several exports, each is independent.

## 10b. Gotong-royong visual deliverable — student rental comparison

When the principal runs a gotong-royong on the tenant's behalf and the deliverable will be opened on a phone (the tenant is the one doing the WhatsApp calls), the HTML should be **self-contained, mobile-readable, and instant-scan**:

- **Verified contact call list at the top.** Agent name, WhatsApp number (linkified `wa.me/`), priority badge (🥇🥈🥉), direct maps link. The tenant opens the HTML, taps the WhatsApp link, makes the call. No scrolling-to-find-the-number.
- **Distance/time matrix with two estimates per leg.** Origin = the principal's base (where the principal can physically check on the tenant); destination = the tenant's daily destination (campus, workplace). Show off-peak and peak separately. Colour the cell by feasibility, not by data source: green if both estimates fit one commute window, amber if peak stretches, red if even off-peak exceeds 60 min.
- **Colour-coded ranking table.** Score the candidates against the tenant's actual constraint (student budget, female-only safety, deposit ≤ 1 month), not the population norm. Top three get green; mid-band amber; out-of-budget rows greyed with a one-line reason ("Vista Bangi RM1600 — out of student budget, included only if splitting with roommate").
- **Per-candidate card with verified links.** One card per top-3 candidate: coordinates, full WhatsApp link, maps link to the actual address, distance in both estimates, features, verification badge ("iBilik verified Sept 2026" / "PropertyGuru + LPPEH verified"), first-month-total calculation.
- **Action plan with copy-pasteable WhatsApp messages.** Include the actual messages the tenant should send — phrased in their register, addressed to the specific agent, asking the specific questions (Ren tag, deposit, viewing date). The agent drafter role is to write messages the tenant will not have to rewrite.
- **Map section uses direct `maps/dir/` links, never `pb=` embeds.** The iframe embed returns "Invalid request. Invalid 'pb' parameter" from Google Maps Platform and breaks the page. Plain `https://www.google.com/maps/dir/<origin>/<dest>` links work on any device without rejection. Include an OpenStreetMap embed with a single anchor marker (the campus or base) as a visual reference; per-candidate markers go in the direct links, not as additional iframes.
- **Skip the candidate the principal's constraints already eliminate.** If the tenant is a student with RM1000 first-month cash, a RM6000 Vista Bangi row is noise, not completeness. Mention it once at the bottom ("If budget allows splitting with roommate: Vista Bangi Maya Myra RM1750 split 3 = ~RM580 each"), then move on.

The deliverable's test: can the tenant open it on their phone, tap the top WhatsApp link, send the included message, and have a viewing appointment in under five minutes? If not, the HTML is missing something — likely a WhatsApp link, a copyable message, or a verified number. The gotong-royong is the principal's work; the HTML is the tenant's tool.

## 10c. Student-budget filter — drop the row that fails the cash test

A comparative ranking for a student tenant must apply the budget filter before listing, not just before ranking. The default population table includes luxury studios (RM1500-2500), co-living with weekly cleaning, and gated premium units with deposit 2+ months — but the student's first-month cash is RM600-1000, not RM6000. Including the luxury rows "for completeness" inflates the table and buries the realistic options.

Procedure:
1. Compute first-month total (rent + deposit + any half-month utility deposit) for every candidate.
2. Compare against the tenant's stated cash ceiling (e.g. "RM1000 first month").
3. Drop rows that exceed the ceiling; mention them once in a "if you can split with roommates" footnote, with the per-head math worked out.
4. Recompute the ranking on the surviving rows.
5. Surface the drop in the verdict ("Vista Bangi removed — first month RM6125, out of student budget"). The tenant can ask for the full list back; the agent does not pre-empt with it.

The filter rule also applies when the principal's stated constraint shifts mid-task ("jangan mewah sangat, jangan serabut sangat"). Reapply the filter, drop the luxury rows, present the leaner table. The constraint change is a new ranking problem, not a minor edit.

## 11. Occupant-density rejection — landlord's own cap is the upper limit

Even when the listing is on a verified platform and the agent passes Ren-tag checks, a unit that exceeds the landlord's published capacity cap is a defect, not a bargain. Malaysian landlord reference points (UKM PPP / Unit Sewaan Luar, public listing pages, 2026):

- 3-bilik apartment, RM900 → max 6 occupants
- 3-bilik apartment, RM1,250 → max 4 occupants
- 4-bilik apartment, RM1,400 → max 6 occupants
- 3-bilik apartment, RM1,900 → max 5–6 occupants

A 4-bilik unit advertised to 10 occupants exceeds every cap above. Reject regardless of price, regardless of platform, regardless of how many friends are already in. Three downstream failure modes:

1. **JMB/MC inspection.** Strata management can issue a notice to vacate; the tenant with the formal agreement gets the eviction order served first.
2. **Joint liability.** If the principal tenant signs the agreement for the whole house, every default by any of the other 9 is the principal tenant's. Refusal to add a name beats cheap rent every time.
3. **Insurance / safety.** Fire, water, electricity load are sized for the cap. 10 in a 4-bilik unit means overloaded circuits, blocked exits, shared bathrooms under stress.

## 12. The four-question gate — before advising on a shortlisted candidate

When the principal brings a specific housing candidate (already shortlisted or already visited), the discipline is to ask **four named questions** before giving a verdict, not to enumerate a 16-bullet checklist:

1. **Total rent + deposit first month + utility split** (the cash test — §10c budget filter).
2. **How many occupants, how many toilets** (density test — §11 catches overload).
3. **Single-gender or mixed** (safety test for the tenant's profile).
4. **Whose name on the agreement** (joint-liability test — the principal tenant is not always the person who showed the room).

Each question gates a distinct failure mode. Total cash fails the budget. Occupancy-to-toilet ratio fails the dignity. Gender mix fails the safety. Agreement name fails the liability. The principal can answer all four in two minutes; a free-form description wastes both sides. Reply shape: give the verdict *after* the four answers. If any one is unknown, mark the verdict CONDITIONAL and the principal should not commit. Asking is not delay; it's the cheapest due diligence available.

## 13. Constraints on this advice

- "100% safe" is not promised. Every check reduces probability; none eliminates residual risk.
- For a tenant who has already been scammed, route back to the umbrella skill (`malaysian-tenancy-consumer-dispute`) or `references/malaysian-tenancy-access-dispute.md` for the recovery / contract-review layer.
- For the *what-clauses-to-look-for* question on an existing agreement, stay in `references/malaysian-tenancy-access-dispute.md`. This file is verification, not contract review.
- A single qualifier in this lane — "the LPPEH site may be down" — does **not** authorise the tenant to skip verification. If LPPEH is unreachable, defer the deposit to a bank hold or escrow; do not proceed on trust.
