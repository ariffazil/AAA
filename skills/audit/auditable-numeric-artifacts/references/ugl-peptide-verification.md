# UGL / Research-Peptide / Gray-Market Pharmacy — Verification Recipe

> When a principal or any user pastes a URL to a gray-market pharmacy or underground-lab (UGL) site
> selling anabolic steroids, SARMs, research peptides, or weight-loss hormones, this is the
> audit-shape. Source-of-record for what the substance actually is, whether the site is
> regulated anywhere, and what the customs/risk picture is at the destination.

## Trigger

Any URL to a site selling:

- oral or injectable anabolic steroids (testosterone esters, trenbolone, nandrolone, stanozolol,
  dianabol, anavar, primobolan, masteron, clenbuterol, t3/liothyronine)
- "research peptides" marketed for human use (BPC-157, TB-500, SLU-PP-332, retatrutide, tirzepatide,
  semaglutide, ipamorelin, sermorelin, GHK-Cu, KLOW80, GH-releasing peptides)
- SARMs (ostarine, ligandrol, cardarine, testolone, ibutamoren)
- HCG for non-fertility use, PCT drugs (clomid, nolvadex, arimidex), growth hormone
- pre-mixed "SLUPP332 + Clen" blends, etc.

## Five-point audit, in order

1. **Self-declared regulatory status.** Read the site's About / Terms. A common tell is the
   contradiction: site sells "Anabolic steroids and cutting agents" in plain type, but appends
   "research purposes only" / "not for human consumption" disclaimers in smaller type to dodge
   controlled-substance law. Both sentences cannot be true; the first is the actual business.

2. **Identity and address verification.**
   - Cross-check the declared company name and address against the relevant corporate registry
     (Germany: Handelsregister / HRB lookup; UK: Companies House; US: Secretary of State).
   - Purepharma Ltd at Brandenburgische Straße 86, Berlin Marzahn — `0` registry hits is a flag.
   - Generic mailboxes (gmail, outlook) listed as contact are a red flag for any "manufacturer".
   - Phone numbers that route to a generic call center are also a flag.

3. **Regulator recognition search.**
   - `web_search "<product_or_company>"` — note zero-result versus dozens.
   - FDA warning-letter database for the company / product name.
   - EMA, BfArM, MHRA, Health Canada, KKM/BPF databases where the principal imports from.
   - Europol press releases on Operation Vigor, Operation Cyber Chase, etc. — UGL takedowns.

4. **Substance-specific evidence.** For each non-trivial substance on the site, check:
   - PubMed / clinicaltrials.gov — has the substance ever been studied in humans? At what dose?
   - Wikipedia article — does it say "research compound" / "not approved by any regulator"?
     That is the official answer, not a hedge.
   - Bodybuilding forums (r/PEDs, Meso-rx) — these often publish lab analyses of underground
     products. A consistent finding is *0/10 purity certifications match the label*; even
     "respected vendors" ship underdosed or mislabeled product.

5. **Customs and legal risk for the destination country.**
   - Search for "<destination> customs seizure <substance>" — Reddit threads, border agency
     releases.
   - Note the legal framework: in Germany, BtMG covers most of these; in Malaysia, Poisons
     Act 1952 + Dangerous Drugs Act 1952; in UAE / Saudi / most of Asia — controlled substance
     import = criminal liability, not just seizure.

## Output shape

A principal pasting a site URL usually wants to know **"is this legit"**. The honest answer is
the audit shape above, not a yes/no. Deliver in this order:

1. **Self-declared status** — what the site says it is.
2. **Identity check** — does the company exist?
3. **Regulator recognition** — is it listed anywhere?
4. **Substance-by-substance evidence** — what is the underlying compound approved / unapproved for.
5. **Customs / legal risk** at the principal's destination country.
6. **One-line conclusion** — site is / isn't a regulated pharmacy; substance has / hasn't been
   studied for the indication; import is / isn't legal at the destination.

Do not give a binary "yes/no" before the audit shape is filled. A principal who only wants yes/no
will override once the audit shape is presented; a principal who wants the audit shape is the one
who needed it.

## Watch-out: brand squatting

Multiple domains can carry the same brand name (e.g., purepharma-rx.com and purepharma.shop).
A passing-through Google result for *one* domain is not a clean bill for *another*. Audit each
domain the principal pastes; do not transfer reputation across unrelated registrations.

## Watch-out: "research use" disclaimer is a tell

If the site is selling oral testosterone, trenbolone, and t3 to anyone with a credit card, the
"research only" language is a controlled-substance dodge, not a regulatory category. State this
plainly. "Research use" peptides like SLU-PP-332 are the same — clinical research compounds
shipped in capsule form for $50/bottle cannot be reproduced at any supplier with GMP certification
and sold at that margin; the substance identity is unverified regardless of label purity.

## Example output (compressed, for the principal's screen)

```
Self-declared: "Pharmaceutical Procurement Company", 12 yr experience.
Address: Brandenburgische Straße 86, Berlin Marzahn.
Business-registry hit: 0.
FDA/BfArM/EMA hit: 0.
SLU-PP-332: research compound, not approved by FDA or EMA, no human trials.
Clenbuterol: EU banned for human use, BfArM schedule.
Customs: Malaysian law treats both as controlled; KKM customs seizure routine.
Verdict: not a regulated pharmacy; substance unverified; import risky.
```

Same shape for any UGL/peptide site. Audit shape is the deliverable.
