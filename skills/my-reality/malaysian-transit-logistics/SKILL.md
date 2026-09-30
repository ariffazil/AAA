---
name: malaysian-transit-logistics
description: "Use when planning transit to a Malaysian venue or event."
metadata:
  hermes:
    tags: [malaysia, klang-valley, transit, mrt, ktm, logistics, events]
    related_skills: [my-reality, human-logistics-advisory, arif-family-members]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Malaysian Transit & Event-Day Logistics

Planning a real person's journey to a real venue: which line, which station, what time to leave, and — the part that decides the whole plan — whether they can still get home.

## When to use
- "Macam mana <orang> nak pi <tempat>?" / how does X get to the venue.
- The principal shares a ticket, order PDF, booking confirmation, or event notice and asks about attendance.
- Any Klang Valley A→B journey where a missed last service strands someone.
- Hospital / campus / airport / concert runs for a named person.

## Procedure

1. **Read the artifact before answering.** Extract the shared PDF (`pdftotext -layout <file> -`, else pymupdf) and pull: event, venue, date, doors/session time, seats, ticket codes, price, T&C lines (no refund/exchange, no resale, admit on-screen or printed). Confirm the printed weekday independently — `date -d '<date>' '+%A %d %B %Y'` plus days-to-event. Never repeat a document's weekday on trust.
2. **Probe the traveller's situation from federation memory before asking anyone.** Stable facts in `/root/.hermes/lanes/people.yaml`; current operational state (where they are now, deadlines, standing backup offers) in `/root/.hermes/workspace/SESSION-*.md` handoffs and `carry_forward.json`. Ask the principal only when memory is silent, and then one short question — never a menu. The principal is not middleware for a lookup you can do.
3. **Pin the venue to its nearest station, then measure the walk.** The last 500 m decides the route, not the line map. Verify adjacency from a source; two buildings on the same road can be 1.5 km apart.
4. **Compute the return leg as seriously as the outbound.** Deliver: leave-home time (peak-aware), line/transfer sequence, walking leg, and the last service that can actually carry them home. Where the margin is thin, name the fallback in the same breath (late ride-hail, overnight at a known-close address) — that choice is usually what the principal is really weighing.
5. **Close on material, not on a question.** End with the depart time and the facts that change action. If one unknown genuinely alters the plan, state it as a conditional ("kalau X, plan sama") instead of interrogating.

## Rules

- **Never say "trains run until about midnight."** Quote the station-specific, direction-specific last departure from the operator's own table. For KL: `mrt.com.my/g-around/Operation_Hours.htm` — per-station, per-direction, and split into a Monday–Saturday table and a Sunday/public-holiday table that runs up to ~30 minutes earlier. Pick the row matching the event day. Verified numbers below.
- **Terminus dispatch ≠ last train at your station.** The table carries both; a plan built on the wrong one strands the traveller.
- **Prefer the single-train route.** A line running direct from near-home to the venue's station beats a nominally shorter route with an interchange — interchanges are where the last-train margin disappears.
- **Rail ends before the doorstep does.** Budget the last mile after alighting (~10–25 min ride-hail from suburban stations) and the hour they actually reach home. "Sampai 12:45 pagi" is incomplete without the line that covers the final 15 km.
- **Ticket handover is part of the answer.** Order PDFs bundle every seat and each ticket carries its own QR. The attendee needs their own QR on their own phone (screen scan accepted; printing optional) — so the plan includes screenshotting their ticket to them and never assumes the buyer will be at the gate. A no-resale/no-sharing clause governs how the file is forwarded, not whether it can be.
- **Write it forwardable.** The reply is usually read by, or relayed to, the traveller: BM, plain words, no internal jargon, no hedging loops, no "nak aku buat X?" menu.
- **Stay inside what the principal disclosed.** Plan the trip he put in the room; never add the person's whereabouts, routines, or unrelated movements. A logistics answer is not a schedule extraction.
- **Label money and durations honestly.** Per-ticket price and seat total are facts off the artifact; fares and travel times are estimates — say so, and give ranges.
- **Adjacent seats ≠ a couple.** The second ticket's owner is unknown until the principal says. Plan for two travellers without asserting who.

## Verified Klang Valley rail facts (re-check before promising)

Last trains, Monday–Saturday table: **Hospital Kuala Lumpur** → toward Putrajaya Sentral 12:11 am, → toward Kwasa Damansara 12:22 am; **TRX** (Kajang Line) → toward Kajang 12:12 am, → toward Kwasa Damansara 12:01 am; last train reaches **Kajang** terminus ~12:47 am; **UPM** → toward Putrajaya Sentral 12:44 am. Sunday/public-holiday: ~15–35 min earlier (Hospital Kuala Lumpur → Putrajaya Sentral 11:39 pm).

**KTM Komuter is not in these tables** — it keeps its own schedule and generally ends earlier than the MRT. Verify with KTMB for any KTM leg; never borrow MRT hours for it.

Line geography (city section): **Putrajaya Line** runs Jalan Ipoh · Sentul Barat · Titiwangsa · **Hospital Kuala Lumpur** · Raja Uda · Ampang Park · Persiaran KLCC · Conlay · TRX · Chan Sow Lin, then Kuchai · Taman Naga Emas · Sungai Besi · Serdang Raya Utara/Selatan · Serdang Jaya · UPM · Taman Equine · Putra Permai · Cyberjaya · Putrajaya Sentral. **Kajang Line** runs Muzium Negara (walkway to KL Sentral) · Pasar Seni · Merdeka · Bukit Bintang · TRX · Cochrane · Maluri … Stadium Kajang · Kajang. Interchanges that matter: **TRX** (Kajang ↔ Putrajaya) and **Titiwangsa** (Monorail, LRT Ampang/Sri Petaling, Putrajaya Line).

Venue ↔ station: **Istana Budaya / Panggung Sari** and the National Art Gallery sit on Jalan Tun Razak with the **Hospital Kuala Lumpur** station between them and the hospital — walk of a few minutes. The Bangi/UKM → city corridor works as one ride-hail to MRT **UPM** or **Serdang Jaya** (~15 min), then Putrajaya Line direct to Hospital Kuala Lumpur (~40 min, **no interchange**); via Kajang it is Kajang MRT → TRX → Putrajaya Line north. Seri Kembangan (One South) sits on that same corridor, which makes it a short overnight fallback instead of a post-midnight ride home.

## Pitfalls

- Inferring where the person is instead of probing. The federation holds it (people.yaml facts, workspace session handoffs, carry_forward); asking "dia kat mana sekarang?" when the answer is already on disk spends the principal's attention on your lookup.
- Assuming a venue's nearest station from general city knowledge rather than verifying it. Wrong adjacency produces a confident, unusable plan.
- Treating "the line runs late" as "they can stay to the end." Compute backwards from curtain call to the platform.
- Borrowing hours from one rail operator for another — MRT tables say nothing about KTM Komuter.
- Answering the logistics while leaving the ticket in the principal's hands: the attendee cannot enter without their QR.
- A departure time that ignores Friday-evening peak produces a plan the traveller cannot use.
