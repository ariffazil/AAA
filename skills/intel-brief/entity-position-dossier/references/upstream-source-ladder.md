# Upstream Source Ladder & Dossier Skeleton

Depth companion to `entity-position-dossier`. Load when actually assembling the file.

## The ladder

Work down this list. The first three outrank anything secondary, and the first is the one most often
skipped in favour of press coverage.

1. **The entity's own releases plus its project schedule or annual filing.** A project schedule filed
   with a securities regulator typically carries a project-by-project table — phase, interest, operator,
   status, forward plan, wells committed, production averages — that press releases never consolidate.
   This is the highest-yield single document for a position dossier; look for it before anything else.
2. **Regulator and national oil company releases.** Award rounds, first-production announcements, partner
   changes — these state interest percentages field by field, which is what the asset table is built from.
3. **Contractor and partner releases.** The awarded contractor states scope and a value band; the partner
   states the share it acquired, and often why. Useful for development-phase timing when the operator is
   silent.
4. **Trade press and industry magazines** — programme timing, executive quotes, contract values. Good for
   dates and commentary; weaker on the numbers that go in the asset table.
5. **Corporate registries** for footprint: subsidiary names, registered addresses, office locations. This
   is how you establish where the entity actually runs the asset from, which press releases rarely state.

Record the reporting date beside every figure. Where a company reports in its home currency, keep that
figure and its own stated conversion rather than silently converting.

## Skeleton

1. **Cover** — title, a kicker naming the source class (`public sources only`), the evidence legend
   (OBS / DER / INT / SPEC with the confidence convention), and a standing scope line: no proprietary or
   licence data, nothing is a resource estimate.
2. **Summary in N numbered points** — each a checkable claim carrying its tag and confidence, not a
   theme. Every point falsifiable on its own.
3. **Corporate snapshot** — four metric boxes: revenue, volume, profit, forward target. As reported, in
   the company's own currency, with the period stated.
4. **Asset table** — one row per position: asset · phase · interest · partners · key facts.
5. **Timeline** — award / acquisition / first production / partner change, each with a **significance**
   column. That column is the difference between chronology and analysis.
6. **Portfolio context** — every position the entity holds in the region, so the province in question is
   read against the whole: where it earns versus where it spends.
7. **Deep dive, flagship** — how it earns, what phase it is in, what is being built next.
8. **Deep dive, frontier** — what is committed, by when, with whom, and what the deadline actually is.
9. **Peer landscape** — who else holds what nearby, and what that means for the subject.
10. **Unpublished-facts register** — question · status · why it matters.
11. **The reading**, then the tersirat layer.
12. **Epistemic map** — claim · class · confidence · basis.
13. **Sources**, then the scope note.

## Register status values

| Value | Means | Never |
|---|---|---|
| `not published` | Searched, nothing in the public record | Estimate a proxy
| `no public evidence` | Absent from the entity's own disclosures | Read as "does not hold"
| `partial` | Some of it disclosed, the rest not | Present the fragment as the whole

## Two readings worth looking for

- **Obligation versus conviction.** A drilling programme framed as a minimum work commitment is a
  contractual floor; obligation wells go to the cheapest compliant standard. An entity with high
  conviction drills more and earlier than its commitment requires. Naming which is which often explains
  a programme that otherwise looks inexplicable.
- **Earning province versus spending province.** List every position with its phase, then mark which ones
  produce and which ones receive development and exploration capital. When they are not the same place,
  that transfer is a finding — and it is an inference, so it ships tagged INT with its basis stated.
