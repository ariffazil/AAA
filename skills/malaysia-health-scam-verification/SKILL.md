---
name: malaysia-health-scam-verification
description: >
  Verify Malaysian health-product claims (Facebook/TikTok ads, "doctor"
  endorsements, herbal cures) before verdict. NPRA registration check, MMC
  doctor-register check, domain/evidence probes, marketing-script pattern scan.
version: 1.0.0
tags: [malaysia, scam-verification, health, npra, mmc, consumer-protection]
triggers:
  - Arif forwards a health ad asking for verdict
  - Herbal tea / supplement / cure-all with disease claims in Malay
  - Doctor persona endorsing a product with a sales link
  - Any "diskaun 50% hari ini" health product
---

# Malaysia Health-Scam Verification

Arif screenshots FB ads and asks "Bagus ke?" — **verdict first, proof table second, no re-arguing**. If he already bought (COD), switch to harm-reduction checklist, never "I told you so."

## Verification pipeline (probe before act — run ALL checks, then verdict)

1. **Product registration — NPRA / QUEST3+**
   - Legit product carries a MAL number on the box. Search npra.gov.my (Product Search / QUEST3+) or medpath.com drug approvals.
   - No MAL number = cannot legally be sold as a health product in Malaysia. MOH: ~95% of unregistered traditional herbal products sampled were found adulterated (steroids/drugs).
   - Disease claims (ulser, gastrik, kanser) = claims for a MEDICINAL product, stricter register. A supplement label cannot claim to cure disease.

2. **Doctor persona — MMC MeRITS**
   - `merits.mmc.gov.my/search` → type full name → "No records found" = not a registered Malaysian doctor.
   - Real Malaysian doctors do NOT run paid FB ads selling products with disease claims — MMC/KKM advertising rules put their registration at risk.
   - Suit/white-coat photo + stock medical image (endoscopy etc.) = stock assets, not credentials.

3. **Domain / landing page**
   - `web_extract` the sales URL. Parked page, 404, or foreign-language hosting placeholder = dead business.
   - Look for: SSM company registration, physical address, phone, batch/expiry info, ingredient dosing. Absent = sales funnel, not a business.

4. **Evidence ladder — PubMed**
   - Search species name + claimed condition. Animal-only (rat) studies = pre-clinical, NOT human evidence.
   - Check species mixups: studied species (e.g. L. octovalvis anti-ulcer in rats) vs claimed species (e.g. L. prostrata).
   - No human RCT / no systematic review = band PLAUSIBLE or UNKNOWN for efficacy — never ESTIMATE.

5. **Marketing-script pattern scan** (copywriting frameworks, not testimonials):

   | Pattern | Example |
   |---|---|
   | Urgency | "Diskaun 50% HARI INI" |
   | Martyr narrative | "selagi saya masih bernafas" |
   | Family guilt | "Isteri saya kadangkala bertanya..." |
   | Hopelessness hook | "jangan terima tiada apa lagi boleh dilakukan" |
   | Existential fear | "sisa usia tua terikat ubat-ubatan" |
   | Scarcity | "peluang terakhir" |
   | Authority props | suit photo, endoscopy image, "pesakit lama saya" |
   | Affiliate funnel | "pautan rasmi pengedar utama" = the ad IS the distributor |

6. **Economics sanity check**: paid FB ad + affiliate wording + ~90% margin product = the ad spends money to harvest desperate buyers. A legit RM30-50 product does not run a national FB funnel.

## Reply shape (Arif)

- Lead: `Verdict: VOID` / `SCAM PATTERN` / `SKRIN` + one-line reason.
- Table of live checks (registration, doctor register, domain, evidence) with results.
- Safer path: KKM clinic / registered products — same cost ballpark, actual evidence.
- If he already ordered: 3 checks BEFORE paying COD — (1) MAL number on box, (2) batch number + expiry, (3) intact seal. Warn about follow-up upsell calls (block them). Never stop prescribed meds.
- Do NOT diagnose his condition or prescribe. F2 epistemic labels on all claims.

## Pitfalls

- Do not call it "scam" on ONE red flag — scam verdict = consistency of many (fake profile + dead domain + no registration + paid ad + emotional script + affiliate).
- Do not fabricate prices or cure rates — RM30-50 only as ballpark from market, never as fact.
- "Tak berkesan" != "scam". Scam requires the deception stack, not just lack of evidence.
- If Arif already bought despite the verdict: give harm-reduction checklist, move on. Do not repeat the argument.
