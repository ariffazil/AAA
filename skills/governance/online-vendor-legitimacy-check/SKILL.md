---
name: online-vendor-legitimacy-check
description: Use when asked to check if an online vendor is legit.
version: 1.0.0
triggers:
  - "check website ni ok x"
  - "is this site legit / trustworthy"
  - "ikey x website ni"
  - "can I buy from here"
  - "supplier / vendor verification"
  - "online pharmacy or supplement shop check"
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Online Vendor Legitimacy Check

**Vendor legitimacy and product efficacy are two independent questions.** "Does this product work?" is
`health-product-claim-audit` / `external-technology-evaluation`. "Is there a real, licensed entity
behind this checkout page?" is this skill. Answer the one that was asked; do not trade one for the
other.

A vendor can be a lawful registered company selling a useless product, and a useful product can ship
from an entity that does not legally exist. Say which axis your verdict sits on.

## When to use

- A user shares a shop URL and asks whether it is legitimate.
- Before advising on a purchase from a non-mainstream retailer (grey-market pharmacy, "research
  chemical" supplier, dropship gadget store, reseller of a regulated good).
- When a vendor's own marketing is the ONLY thing asserting its quality.

## Core principle

> **The vendor's website is a claim, never evidence.** Its About page, its "GMP standards" sentence,
> its QR authenticity code, and its testimonials are all self-issued. Legitimacy is established off-site
> or not at all.

Four independent checks, each of which can fail on its own: **entity → licence → jurisdiction →
product reality.** A pass on three does not carry the fourth.

## Step 1 — Extract the claimed legal identity

The operator must name a real legal entity and a real place. Pull from the About / Terms / imprint
page, not the marketing header:

- the registered company name as a legal person (e.g. `ACME LTD`), not a brand or domain
- the declared registered address
- any licence, registration, or batch number they cite

If the site names only a brand and no legal entity or address, that is already the first finding: an
unidentifiable seller. German/EU sites are legally required to publish an imprint (Impressum) — its
absence where it is required is itself informative.

## Step 2 — Entity registry check

Search the quoted legal name against the company registry of the claimed country.

```
web_search "\"<EXACT LEGAL NAME>\"" company registration <country>
web_search "\"<EXACT LEGAL NAME>\"" Handelsregister        # DE
web_search "\"<EXACT LEGAL NAME>\"" Companies House        # UK
web_search "\"<EXACT LEGAL NAME>\"" SSM                     # MY
```

A registered company leaves a footprint: registry number, VAT/tax id, filings, a director, often a
maps listing. **Absence of that footprint is the finding.** Report the absence — "no registry record
found for the named entity" — rather than asserting fraud you have not shown.

## Step 3 — Regulator grep

A licensed manufacturer or pharmacy appears in its regulator's database. Search the entity against the
regulator, not the product.

```
web_search "\"<ENTITY>\"" GMP certificate OR licence OR warning letter
web_search site:bfarm.de "<ENTITY>"      # DE
web_search site:fda.gov "<ENTITY>"       # US
web_search site:npra.gov.my "<ENTITY>"   # MY
```

Zero rows across the regulator and the registry together is the strongest single signal available from
outside.

## Step 4 — Jurisdiction law, both ends

Check the claimed origin country AND the buyer's country, because they are separate questions and
usually both unfavourable for controlled goods.

- **Origin**: is the goods class saleable there at all, and under what authorisation? (Anabolic
  steroids are controlled substances in Germany under the narcotics act; a German "manufacturer" of
  them is not operating lawfully, whatever the site says.)
- **Destination**: what does import of that class require? (Malaysia: Poisons Act / Dangerous Drugs Act
  — import without approval means seizure and personal liability for the importer, not the seller.)
- Note who bears the loss. Customs seizure lands on the buyer: money gone, goods gone, no recourse
  against a foreign seller, and the enforcement record names the importer.

## Step 5 — Domain and brand pattern

- The same brand name reappearing across multiple unrelated domains is a trust-recycling pattern, not
  an expansion. Each copy inherits credibility the name earned elsewhere.
- Newly registered domain + a claimed decade of history + no archive of that history = a broken
  provenance chain.
- A "research purposes only / not for human consumption" label is a **legal shield, not a quality
  claim**. It exists to move the transaction out of consumer-protection and pharmaceutical law while
  the product is plainly sold for human use.

## Step 6 — Product reality (only what changes the vendor verdict)

You do not need to audit efficacy to judge a vendor, but one check belongs here: does the headline
compound have ANY human data or regulatory approval anywhere? A compound that is mouse-only and
approved by no regulator cannot be sold as a consumer product lawfully — which tells you the seller's
compliance posture, independent of whether the molecule ever works.

## Verdict shape

```
## <vendor> — Vendor Check

**Claimed entity:** <name, address as declared>
**Registry:** FOUND <number> | NOT FOUND
**Regulator:** <body> — MATCH | NO RECORD
**Jurisdiction:** origin <status> · import to <buyer country> <status>
**Product:** <compound> — human data <yes/no>, approved <body/none>

**Verdict:** verified regulated vendor | unverifiable | non-compliant seller
**What would change it:** <the one document that would move the verdict>
```

Three verdicts, and they are not interchangeable:

- **verified** — entity + licence both resolve.
- **unverifiable** — no record found. This is the honest verdict for absence of evidence. It is NOT
  "proven scam"; do not upgrade it.
- **non-compliant** — the entity exists but the goods class is unlawful at origin or destination, or
  the marketing is engineered to evade regulation (the "research purposes" shield on a consumer
  product).

## Pitfalls

- ❌ **Reading the About page as verification.** "We operate under GMP standards", "12 years
  experience", "scannable authenticity QR" are unbacked self-assertions. Nothing on the seller's own
  site can verify the seller.
- ❌ **Resolving the brand instead of the entity.** A brand name is not a legal person; searching it
  returns the vendor's own pages, which proves only that they exist on the web.
- ❌ **Substituting a product-efficacy verdict for a vendor verdict.** Answering "the compound has no
  human trials" when the question was "is this shop legitimate" leaves the actual risk (an
  unidentifiable counterparty holding your money) unaddressed.
- ❌ **Upgrading absence into proof.** No registry record means no record. Say that. Claiming fraud you
  did not demonstrate is the same epistemic failure as certifying a vendor you did not check.
- ❌ **Treating a `.com` and a server in the claimed country as evidence of presence there.** Domain and
  hosting prove nothing about where the operator is or who they are.
- ❌ **Naming a specific vendor as a scam in public writing without the on-record finding.** State the
  check, the result, and the limits; let the reader draw the conclusion.

## Support files

- `references/vendor-red-flags.md` — red-flag pattern table by goods class, jurisdiction quick notes,
  and the questions that separate a legitimate regulated seller from a grey-market one.
