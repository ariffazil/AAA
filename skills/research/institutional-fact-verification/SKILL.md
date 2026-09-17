---
name: institutional-fact-verification
description: "Use when verifying what an organisation did or signed."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F11]
tags: [verification, sourcing, contracts, corporate-structure, provenance]
---

# Institutional Fact Verification

Load when research or a deliverable concerns what an **organisation** did, owns, operates, signed,
reports, or is structured as — contracts, awards, licences, corporate structure, asset ownership,
plant/site lists, appointments, regulatory actions.

These are facts that look like public knowledge and are not. A practitioner in the subject reads
them as a competence test, and being wrong in one line discredits the surrounding work.

## Core rules

1. **Fetch the organisation's own announcement before any report about it.** Coverage reports the
   headline — term, approval, a capacity figure — and routinely omits the asset/party list, any
   structural reorganisation, the legal entities, and the effective-versus-announcement date gap.
   The announcement normally lives on the organisation's news/media page and outranks every
   secondary source. Encyclopaedias, aggregators and regulator archives are corroboration only.

2. **Date the structure, not just the fact.** Ownership, contract areas and asset lists are
   properties of a point in time. After a reorganisation, older maps, tables and archive pages keep
   showing the superseded structure for years. State which vintage you are using, and tell the
   reader that their older reference is now stale.

3. **Separate the entities.** Parent, wholly-owned subsidiary, joint-venture vehicle and regulator
   are four different parties. Name the one that actually signed; name the parent separately only
   if the reader needs the corporate map. Substituting the better-known parent for the subsidiary
   reads to a specialist as not knowing the structure at all.

4. **Never collapse the three dates.** Announcement/ceremony date, effective date, and the expiry
   of the prior arrangement are usually three different numbers — and the effective date often
   *precedes* the ceremony. The overlap window between old and new arrangements is frequently the
   most operationally useful figure in the whole document. Report all three where they differ.

5. **Verify anything you compute, and publish the residual.** Recompute stated areas, distances,
   durations or volumes from published inputs, compare against the published figure, and state the
   difference and its cause. A local planar area from boundary turning points typically runs ~2 %
   under the published geodesic value because straight lines between vertices cut the polygon
   short. Stating the residual reads as real work; silently choosing one number is the weak move.
   Log internal arithmetic contradictions in source documents too (a stated duration that
   disagrees with its own date range) — do not quietly harmonise them.

6. **Audit your own corpus before asserting a coherent account.** Grep your knowledge/resource
   files for the key values, names and structural terms first. Long-running projects accumulate
   conflicting versions, and a document that criticises institutional ambiguity while carrying the
   same defect internally is indefensible. Classify each conflict as **reconcilable** (two distinct
   events one name has collapsed) or **superseded** (an older model still in the tree), then publish
   it as an explicit reconciliation annex with proposed resolutions.

7. **Never edit an artifact marked sealed, ratified or immutable.** That is an authority boundary,
   not housekeeping. Report, propose, and let the owner ratify. Apply the same caution to legacy
   files whose downstream consumers have not been traced.

8. **Declare the gap rather than smoothing it.** A fact not in the public domain is a declared gap,
   not an estimate. Declared gaps outperform smooth numbers: they locate the uncertainty and they
   survive review by someone who works the subject daily.

## Procedure

1. Identify the organisation(s) and the exact fact class (contract / structure / asset list / date).
2. Pull the primary announcement. Only then read coverage — to catch what the announcement omits
   about context, never as the basis for detail.
3. Extract: the full asset/party list, the legal entities, all three dates, and any reorganisation.
4. Recompute every numeric you intend to publish; record the residual against the published value.
5. Grep your own corpus for the same terms. Table any conflicts; classify reconcilable vs superseded.
6. Write the provenance register: exact / indicative / interpretive / declared gap, per element.
7. Publish the reconciliation annex alongside the deliverable — as a finding, not a silent fix.

## Anti-patterns

- **Building the structure from news.** Coverage told you the deal closed; it never told you the
  asset list or that two areas merged. Confident-sounding detail assembled from coverage is the
  exact failure a specialist spots first.
- **Quoting a regulator archive as current.** Regulator field-history and licence pages lag
  reorganisations by years. Date them.
- **Presenting a computed figure as the published one.** If your number and the published number
  disagree, both belong in the deliverable with the reason.
- **Silently harmonising a contradiction you found.** A conflict you noticed and resolved without
  recording it is indistinguishable, to the reader, from one you never noticed.
- **Editing the sealed source because the fix is obvious.** Obvious correctness does not confer
  authority to write.

## References

- `references/reconciliation-annex-recipe.md` — the table shape, classification rules, and
  proposed-resolution format for publishing an internal corpus conflict.
