---
name: short-stay-booking-search
description: "Use when booking a short-stay room under a budget."
version: 1.0.0
tags: [airbnb, accommodation, booking, travel, vetting]
---

# Short-Stay Booking Search — find one, verify it, deliver the link

Class of work: a human needs a room tonight or this week, at a price, with named must-haves, in a named area, and wants a link he can tap. The value is not the search — it is catching what the listing contradicts about itself.

## 1. Read the request before searching

- **Dates absolute, nights computed.** Budget is normally the TOTAL for the stay. Restate it as a total in the reply so a per-night number is never mistaken for the budget.
- **Must-haves are separate gates** (aircond / wifi / TV / washer / kitchen). Score every candidate against each one explicitly; "has most of it" is not an answer.
- **If the human opened with a listing link, that link is the anchor.** Verify that unit first — availability, total, what it has, what the notes say. Search alternatives only when asked, and then recommend one.

## 2. Extract a listing — browser, not a plain fetch

Airbnb renders client-side, so use the browser and read the rendered text:

```python
new_tab("https://www.airbnb.com.sg/rooms/<id>?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD&adults=1&currency=MYR")
wait_for_load()
t = js("(() => document.body.innerText)()")   # let it settle ~3-4s first
```

Four blocks carry the truth:

| Block | What it gives |
|---|---|
| header | unit type, guests, beds/baths, rating + review count |
| **Listing highlights** | what the host considers the sell — washer, kitchenette, pool, LRT |
| **What this place offers** | the top amenities only — a subset, not the full set |
| **Other things to note** | check-in window, fines, parking fee, card count, and the contradictions |

Also read the star distribution and skim the 1–3 star text. One review naming a dead aircond outweighs twenty "nice place" lines for a one-night stay.

## 3. Search with the right price mechanic

Card prices are **totals for the stay**; the `price_max` URL filter is **per night**. Set `price_max = ceil(budget / nights)` — a two-night budget of RM150 means `price_max=75`. Get this backwards and every result sits at double the budget.

```
/s/<City>--<Country>/homes?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD&adults=1
  &currency=MYR&price_max=<per-night>
  &room_types[]=Entire%20home%2Fapt
  &amenities[]=4&amenities[]=8&amenities[]=33&amenities[]=5
```

Confirm the filters actually applied by reading the chips at the top of the results page ("Up to RM 75", "Air conditioning", "Washing machine", "Kitchen", "Wifi"). A silently-dropped filter is indistinguishable from a thin market. Currency follows the domain (`.com.sg` defaults to SGD) — pass `currency=MYR` so the numbers match what the human thinks in.

## 4. Shortlist without opening every card

Collect ids from `a[href*="/rooms/"]` on the results page, then open each candidate with the same date query and scan the text:

```python
for k in ["wifi","netflix","washing machine","kitchen","air conditioning","tv","pool","currently no"]:
    print(k, k in t.lower())
```

Two or three candidates is enough. More is a menu.

## 5. Contradiction and risk scan — the actual deliverable

- **Amenity claim vs the notes section.** A listing can say "Guests also have access to WiFi 24/7" in Guest access and "CURRENTLY NO WI-FI" in Other things to note. Surface the conflict and tell the human to ask the host; never resolve it silently in either direction.
- **Safety fields.** "Carbon monoxide alarm not reported" / "Smoke alarm not reported" are real line items on the page, not noise.
- **Unit substitution.** Hosts running many identical units write "we cannot always give the exact room in the photos". Photos then describe the class, not the unit.
- **Money and house rules.** Parking charged cash per day, access-card replacement fee, smoking fine, one card per booking, no visitors, quiet hours. A 4pm check-in on a tonight booking burns half the first night.
- **Rating vs volume.** A new listing with no reviews and a Superhost with three reviews are both unknowns — say that instead of ranking them confidently.

## 6. Deliver

One line per candidate: price **for N nights** (the discounted payable figure first; the struck-through one only as comparison), the amenities it actually has, what is missing against the ask, and the single riskiest item. Bake the dates into every link so one tap shows the right price:

`https://www.airbnb.com.sg/rooms/<id>?check_in=YYYY-MM-DD&check_out=YYYY-MM-DD&adults=1&currency=MYR`

Close with the one action ("tanya host pasal wifi"), not a question about whether he wants more options.

## Pitfalls

- `price_max` is per night while cards quote totals — divide the budget by nights.
- Quoting the struck-through figure as the price: the payable total is the second number.
- "What this place offers" is a subset, and the expanded "Show all N amenities" panel renders promotional copy — the main page text plus Listing highlights is the reliable read.
- "Smart TV" ≠ Netflix included. Do not promise a streaming service from a TV line.
- Amenity grids are host-declared and unverified; a declared amenity with a contradicting note is a question for the host, not a fact for the reply.
