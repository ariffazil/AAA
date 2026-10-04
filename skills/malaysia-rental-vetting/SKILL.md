---
name: malaysia-rental-vetting
description: Use when vetting a Malaysian rental listing from photos.
---

# Malaysia Rental Vetting — Bilik Sewa / Rumah Sewa Pre-Deposit Check

Proven 2026-08-15 (Azwa · Bilik Sewa Seksyen 3 Bangi, RM360 all-in, "muslimah pekerja UKM" listing vetted from one room photo + one listing collage).

## Trigger
- User shares room/house photos or a rental listing collage and asks "ok ke ni", "aduan penduduk kat mana", "kedai makan kat mana", "worth it ke", or asks for a decision / guide PDF.
- Often for a family member or friend — personalize the deliverable with the tenant's name when known.

## Workflow (5 steps)

### 1. Intake — extract what the images actually contain
- **Room photos** → `vision_analyze` with the 7-point question template below.
- **Listing collage** → `vision_analyze` asking it to read ALL text exactly (price, terms, target tenant, contact number) AND describe every photo. Listing collages almost always show every room EXCEPT the bathroom — the single most common omission. Always demand bathroom photos.
- **EXIF caveat:** images received via Telegram have EXIF/GPS stripped (verified 2026-08-15: PIL `getexif()` returns empty on the saved file). Do NOT try to geolocate from the photo — ask the user for taman/bandar, then continue.

### 2. Room assessment question template (vision_analyze)
Ask exactly these 7 points, honest tone ("be concrete and honest"):
1. Overall condition — walls, ceiling, floor tiles, cleanliness.
2. Electrical safety — wall fan, socket placement, visible wiring.
3. Ventilation & light — windows, air circulation.
4. Furniture quality — bed frame, mattress condition.
5. What the decor suggests — approximate occupant/purpose.
6. Signs of damp, mold, water stains, disrepair, neglect.
7. Anything unsafe for a child (sockets low, sharp frame edges).

### 3. Area research (web_search — 4 probes minimum)
1. `<area> aduan penduduk / persatuan penduduk` — an active residents' association is a good sign (organized maintenance, complaints escalated to majlis get action).
2. `<area> banjir masalah` — flood history. **Flood zones are hyper-local**: greater-Bangi floods (Taman Bangi Indah, PKNS Batu 6, Sg Merab) do NOT apply to Seksyen 3. Never generalize "X floods" to a specific section; cite the specific taman, and phrase the finding as "no flood record found for THIS section — confirm with owner".
3. `kedai makan <area>` — nearest eateries with name, street, food, price, hours.
4. `<area> bilik sewa harga` — live price benchmark (mudah.my listings, RoomSOS ads carry real numbers). Normalize "all-in" vs "+utiliti" before comparing (all-in ≈ +RM50–80/mo value).

### 4. Verdict discipline — conditional, never full-approve from photos
Framing that landed: **"LULUS BERSYARAT"**. Separate evidence-based passes (price, location, area, food) from open gates that REQUIRE physical action before money moves:
- Physical viewing — photos choose best angles; smell/state cannot be photographed.
- Bathroom inspection + how many tenants share it (the real comfort determinant).
- Tenant composition — "perempuan/muslimah only" is marketing until verified on site.
- Owner identity + written receipt (anti-scam; refuse if no receipt).
- Deposit math disclosed up front: first-month out = sewa + deposit (refundable) + utility deposit (refundable) + key fee.

If the user jokes "apex judge approve ke?" — keep the courtroom framing light but the gates firm. The final decision belongs to the tenant; we supply judgment on evidence.

### 5. Deliverable — PDF guide (usually requested next)
Load `productivity/pdf-report-generation` and use its **lightweight personal-guide register** (8–10pp, 5 simple charts, casual BM, verdict/caution boxes). Include a questions-for-owner table written as copy-paste WhatsApp messages addressed to the listing's contact number.

## Pitfalls
- Telegram strips EXIF — no geolocation from photos.
- Listing collages omit bathrooms almost always — demand photos.
- Don't claim "no flood" — claim "no flood record found for this section; ask owner: 'rumah ni pernah masuk air tak?'"
- Benchmark only from live listings (mudah/RoomSOS), not stale blog posts or homestay nightly rates.
- "All-in" and "+utiliti" prices are not directly comparable — normalize first.

## Files
- `references/bangi-seksyen3-data-bank.md` — worked-example data bank (Seksyen 3 Bangi: PPJ3 residents' association, hyper-local flood-zone map for greater Bangi, 5 eateries with 2026 prices, RM350 benchmark, RM360 deal terms) so future Bangi rental questions start ahead of zero.
