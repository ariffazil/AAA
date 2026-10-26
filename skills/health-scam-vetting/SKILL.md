---
name: health-scam-vetting
version: 1.0.0
description: >
  Vet health products and "doctor" endorsements from social-media ads
  (Facebook/Instagram/TikTok herbal teas, supplements, rawatan) before anyone
  buys. Live checks: product registration (NPRA), doctor registry (MMC),
  domain liveness, species-level evidence, scam narrative patterns.
tags: [health, scam, vetting, malaysia, consumer-protection, verification]
triggers:
  - user sends a screenshot or link of a health product ad asking "bagus ke", "scam ke", "boleh percaya ke"
  - user asks whether a "doctor" advertising a cure on social media is legit
  - family/friends are considering buying a herbal product from a FB/TikTok ad
  - user asks to check a supplement, teh herba, or traditional remedy
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Health Product Scam Vetting

Arif (and his family circle) get targeted by Malaysian Facebook health-scam ads
— fake "Dr" testimonials selling herbal teas for ulcers, diabetes, high blood
pressure, etc. When he sends a screenshot asking "bagus ke benda ni", run the
pipeline below. The answer is a VERDICT, not an essay.

## Response contract

- Lead with verdict: `VOID` (no trust/evidence) / `SKRIN` (red flags present) / `CAUTION` (plausible but unproven).
- Show the live check results (registry, domain, evidence) — never just assert "scam".
- End with the safer alternative path (real care route), not just debunking.
- No fabricated prices, no invented clinical outcomes. If you don't know the cost, say so (decision-advisory rule).

## The 5 live checks (run in order)

### 1. Product registration — NPRA (Malaysia)
- Search product name at NPRA product search / QUEST3+ (npra.gov.my).
- No MAL number → cannot legally be sold in Malaysia with health claims.
- Products with disease-related claims ("menyokong ulser", "merawat kencing manis") are regulated as MEDICINAL products, not supplements — unregistered = illegal.
- Context to cite: KKM found ~95% of unregistered traditional preparations contain undeclared steroids/drugs (Malaysian J. Pharmacy).

### 2. Doctor identity — MMC MeRITS
- Live search: https://merits.mmc.gov.my/search (Name field → save Search).
- "No records found" → NOT a registered Malaysian doctor → the "Dr" is fake.
- Specialists: also check NSR (nsr.org.my).
- Real doctors do not run FB ads with affiliate "pautan rasmi pengedar" links — that alone is disqualifying (MMC advertising rules).

### 3. Domain liveness
- web_extract the advertised site. 404 / parking page / foreign-language placeholder (e.g. Vietnamese "Tên miền..." page) = dead storefront, no real company behind it.

### 4. Species-level evidence
- Verify the EXACT binomial claimed. Sellers swap species: e.g. Ludwigia prostrata (claimed) vs L. octovalvis (studied) — different plants.
- Evidence tier: human RCT > animal model > in vitro > "Perubatan Tradisional" citation. Rat studies = PLAUSIBLE at best, NOT proof for humans.

### 5. Narrative pattern (the scam script)
Check for these in the ad copy:
- Urgency: "Diskaun 50% hari ini", "Beli Sekarang"
- Martyr/redemption: "saya pernah di jurang keputusasaan", "selagi saya masih bernafas", "isteri saya bertanya..."
- Fear play: "sisa usia tua terikat ubat-ubatan", "jangan terima 'tiada apa lagi boleh dibuat'"
- Affiliate funnel: "pautan rasmi pengedar utama" — the author is a dealer earning commission
- Borrowed medical imagery: endoscopy/scan photos copied from the web
- Overclaiming: one product treating 3+ unrelated conditions
- Vague credentials: "Menurut Rujukan Perubatan Tradisional" instead of a real trial

## Pitfalls

- Don't debunk the narrative alone — run checks 1–3 first. The registry/domain hits are the irrefutable evidence; the narrative is supporting colour.
- Check the exact species, not the genus. Ads and sibling products blur binomials.
- If the user (not a family member) actually has the condition — e.g. gastric — give the real care route: KKM clinic → UBT/breath test → H. pylori triple therapy. Never let a debunk end with zero alternative.
- Don't fabricate product prices or clinic costs. "Klinik KKM RM1" is well-known; private costs are not — ask or stay silent.
- Offer the report-the-ad action (FB: Report Ad → Misleading health claims) as a concrete next step, don't just warn.

## References

- `references/ludwigia-prostrata-case.md` — worked example: the 2026-08 Teh Herba Ludwigia Prostrata FB campaign (both ads, all findings).
