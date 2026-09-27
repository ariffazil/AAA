# Rental Gotong-Royong (Malaysia, 2026) — Tenant-First Search Pattern

Topical depth for `human-advisory-discipline`. Load when advising a Malaysian tenant
(student or working adult, especially one with a tight 5-day move-in window) through
a multi-platform rental search where the principal — not the agent — will do the
WhatsApp calls and viewings.

## When to load
- Tenant is a student (UKM/UM/UKM-equivalent) with a tight first-month cash ceiling
  (rent + deposit ≤ RM1000).
- Tenant is female and explicitly needs a female-only / non-mixed listing.
- Principal asks for a sealed PDF of `syarat wajib + haram` he will hand to the
  tenant as the agent's authority boundary.
- Cross-platform verification is needed (iBilik.my + PropertyGuru + Mudah.my + the
  agent's own listing page) before any contact is published to the tenant.
- The search is bounded by a maximum drift from a fixed point (typically the
  principal's home address — never re-estimate the principal's lived time on his
  road, ask if disputed).

## Verified WhatsApp / phone directory (live web-verified 26 Sept 2026)

| Agent | Number | Listings | Verified source |
|---|---|---|---|
| Suzita | 0199834979 | Hijauan Heights RM300 single / RM250 share | homes.cari.la + iBilik.my |
| Fauzi | 0199864979 | Hijauan Heights backup | homes.cari.la |
| Cik Fia (Fia Property) | 0182904652 | Bangi Avenue 3, BSP, Bandar Puteri Bangi | iBilik.my + RoomGrabs + Roomz.asia |
| Maya Myra (QVE Property) | LPPEH PEA 3998 | Vista Bangi RM1750 | LPPEH search-listing (verified agent) |
| Steve Tham | 0162188300 | Vista Bangi Studio | PropertyGuru |
| Cik Jaja / Jaarah | 01112047128 | Bangi Avenue RM500 — DEPOSIT 2 BULAN, JAUHI | iBilik.my |

## 5 final candidate shape (student-budget tier, RM350-RM390)

1. **Hijauan Heights Single (Suzita)** — RM380 advertised / RM300 verified single, 1st month ~RM600-760.
2. **Bangi Gateway Bilik Kongsi Female (iBilik #8390249)** — RM370 sharing 2, WiFi + utilities INCLUDED, 1st month RM740.
3. **Bangi Avenue 3 Single Queen promo (Cik Fia)** — RM390 promo (was RM420), 1st month ~RM780.
4. **Bangi Avenue 3 Middle Queen (Cik Fia)** — RM390, same agent.
5. **Ostia Residency Single Room** — RM350 estimated (mostly whole-unit RM1400+; single-room availability rare).

## iBilik.my Cloudflare workaround (when tenant cannot open the link)

1. Share the verified WhatsApp number directly (table above).
2. Use PropertyGuru.com.my or Mudah.my as backup platform for the same listing.
3. **Never fabricate gambar from a broken link** — ask the owner to WhatsApp
   fresh photos; a missing image is a missing fact, not an invitation to invent.
4. Some iBilik listings only show in-app; if the principal is blocked from
   Desktop, have the tenant open iBilik directly from her phone on her own network
   (the block is geolocation/UA-gated, not IP-permanent).

## Syarat PDF as locked contract — eight-section shape

When the principal asks for `syarat wajib and haram sah.segalanya` to be sealed as
a PDF, the principal is locking the boundary between his authority and the agent's,
not asking for advice. The PDF's eight sections, in order:

1. Cover (budget / distance / red-line figures in a tinted box)
2. **WAJIB** (10 numbered items in green) — every entry is a binary gate
3. **HARAM** (12 numbered items in red) — every entry is a binary reject
4. Final candidates table (only the rows that survive the WAJIB test)
5. Per-candidate detail cards (price, distance, female-only, deposit, owner verified)
6. One-tap `wa.me/` links per agent
7. Follow-up tracker (call date / reply / viewing date / decision)
8. Emergency numbers (999 polis / 994 bomba / nearest hospital)
9. Sealed-by-F13 signature block: *"Tiada agen, owner, atau platform boleh UBAH mana-mana syarat dalam dokumen ini. Sebarang perubahan MESTI melalui [sovereign] untuk kelulusan."*

Without the final paragraph the document is a checklist, not a contract, and the
agent will lose the negotiation when an owner pushes back with "we'll need RM500
extra for deposit".

## Gotong-royong HTML deliverable shape

When the principal asks for a comparative gotong-royong, produce ONE self-contained
HTML file the tenant opens on her phone (not a PDF, not a chat message):

1. Verified contact call list (agent + WhatsApp + platform link), ranked by
   tenant's actual constraint
2. Distance/time matrix — both peak and off-peak, originating from the **tenant's
   base** (not the principal's), with explicit haversine + road-factor + 1.3x
   correction
3. Colour-coded ranking table — green = within budget, amber = stretch,
   grey = out-of-budget. Tenant scans the shape at a glance.
4. Master map section using direct `https://www.google.com/maps/dir/?api=1&origin=...&destination=...` URLs.
   Do NOT use `pb=...` iframe embeds (broken on tenant's network).
5. Action plan with WhatsApp launch scripts the tenant copy-pastes, named by priority.

## Cross-platform verification rule

Before publishing any third-party contact:

1. Pull the live platform page (`iBilik.my`, `PropertyGuru`, `CariProperty`, `Mudah.my`, `RoomGrabs`, `Roomz.asia`).
2. Extract the WhatsApp/phone from the page itself.
3. Verify displayed contact matches link target.
4. Place the source URL next to each row in the published deliverable — so the
   principal can see what was actually checked.

The agent reproducing its own earlier cross-check as if it were live is the failure
mode this guard prevents. When the principal challenges "validate all", re-run the
live web search on EVERY contact — do not defend prior verification with "I
verified earlier".

## Pitfalls cemented in this lane

- Tenant's lived route overrides agent's textbook distance estimate. If the
  principal says 20km, it is 20km; 30km is the aggregator's number, not theirs.
- Privacy envelope ≠ access ceiling. A bonded person admitted as a sibling gets
  full agent capability with a privacy barrier — never downgrade her tier on the
  way to granting access.
- Friend lanes carry kasih sayang, not constitutional lock. A rented-room
  conversation between siblings is not the place to read out the F-series floors.
- Deposit 2 bulan = reject. Deposit 1 + 1 (advance + security) is the norm; 2+1
  is a sublet / sub-agency tell.
- Mixed-gender landing Seksyen 4, Bandar Baru Bangi carries a documented pecah
  rumah wave (Nov 2024 – Feb 2025, CCTV-confirmed). Recommend gated apartment
  / condo over landed house for female tenants.
