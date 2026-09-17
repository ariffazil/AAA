# Provenance Sourcing — the checks to run before an article is registered

The published page carries a machine-readable Claim Register and Source Ledger, which means the
sourcing is part of the artefact a reader can inspect. Run these checks before registration,
not after publication.

## 1. Every `url` in the Source Ledger must resolve

```bash
# read the REGISTRY, the source dir and the published mirror - all three
{ grep -rhoE "[a-z_-]+://[^\"' )|]*" src/data/essays.json; \
  grep -rhoE "[a-z_-]+://[^\"' )|]*" src/data/makcikgpt/; \
  grep -rhoE "[a-z_-]+://[^\"' )|]*" dist/makcikgpt-md/; } \
  | sed 's|^\([a-z_-]*\)://.*|\1|' | sort | uniq -c | sort -rn
```

Any scheme that is not `http`/`https` is a defect. An invented internal scheme — a newspaper name, a
company name, a filing registry used as a URL prefix — is citation-*shaped* and unreachable, and it
is worse than no citation because it makes an unsourced claim read as audited. The date and format
attached to it are what defeat the reader's scepticism.

**The URLs live in `src/data/essays.json`, not in `src/data/makcikgpt/` — pointing the check at the
article directory is how this defect survived.** Measured 2026-09-17: `essays.json` holds **81**
source-ledger URLs and only **25** are `https://`. The other **56 (69%)** are invented schemes —
`petronas://` ×7, `the-edge-malaysia://` ×4, `public-record://` ×4, `bernama://` ×3, `bursa://`,
`nst://`, `malaysia-law://`, `cna://`, `linkedin://`, `book://` and ~20 more — and **27 of the 29
published mirrors** render at least one of them into a public `| source_id | type | title | url |`
table. They are live: `https://arif-fazil.com/world/makcikgpt-md/petronas-dna.md` returns 200 and
shows `petronas://corporate-documents/cobe-2022-mission-1988` as the source for a factual claim.
The check in this section, aimed at `src/data/makcikgpt/`, returns **zero** defects against that
corpus.

**Do not quote-anchor the pattern.** The same check written as `"[a-z_-]+://[^"]*"` matches **only
double-quoted** URLs — 24 of 107 occurrences, i.e. **22%** — and reports zero defects on a clean
tree for the wrong reason. A planted control settles it: that pattern caught **2 of 4** forms (missed
single-quoted, missed unquoted `url: bnm://…`); the pattern above catches **5 of 5**. **Run the
positive control before trusting any clean result** — plant one invented scheme per form you can
imagine, confirm the check fires, delete the plants, then run it on the real tree. A check whose
clean result you have not seen fail is decoration.

**Sweep the mirrors too — and sweep the tracked one, not only the build copy.** The generator emits
`dist/makcikgpt-md/<slug>.md` and `.html` twins, so the same unusable string lands in the published
copy as well as the source. Two mirror trees exist and they are not equivalent: `dist/makcikgpt-md/`
is an **untracked build artifact**, while `public/makcikgpt-md/` is the **git-tracked, served** copy
(116 tracked files) reachable at `https://arif-fazil.com/world/makcikgpt-md/<slug>.md`. Grep both,
but know which one carries the recorded seal before you reason about fixing anything — see §7.

When a source genuinely cannot be linked, write it as `UNVERIFIED` with what you do have
(publication, title, date) rather than minting a scheme for it.

## 2. Tag every load-bearing sentence at authoring time

`OBS` observed · `DER` derived · `INT` interpretation · `SPEC` speculative. The `INT` row is what
keeps a sharp piece publishable: a tagged interpretation is a stated reading, an untagged one reads
as a factual assertion and is what converts commentary into a liability.

An article claiming `provenance_status: 'sealed'` with no claim register is not registrable as sealed.
Either write the register or declare the piece `legacy` — do not ship the HTML alone.

## 3. Verify the byline and date of any supplied document before building on it

A column handed over as "what he wrote" may be by a different author, decades old, and written about
a different situation. Fetch it, read the byline and the issue date, and if they contradict the
assumption, say so plainly and rebuild the piece around the real artefact.

An old instrument that *praises* the institution cuts deeper than a fresh attack, because it cannot
be dismissed as a critic's hostility — so a mis-dated source is not only a correctness problem, it is
a lost opportunity.

## 4. Series numbering is read, not coined — and read from the right file

The registry is **`src/data/essays.json`**, a list of entries each carrying
`series: {"id": "M6", "n": 3}`. The ids there are **uppercase** (`M1`…`M6`, `S1`…`S9`); the lowercase
`m6-3` form is *derived* by the generator (`generate-md-mirrors.cjs` → `article_id: ${p.id}`) and is
only visible in the built mirrors. **`src/data/makcikgpt/` is not the registry** — grepping it for a
series id returns at most a passing mention inside prose.

```bash
python3 - <<'PY'
import json
d = json.load(open("src/data/essays.json"))
g = {}
for e in d:
    s = e.get("series")
    if isinstance(s, dict):
        g.setdefault(str(s["id"]), []).append(s.get("n"))
for sid in sorted(g):
    ns = sorted(n for n in g[sid] if isinstance(n, int))
    gaps = [n for n in range(min(ns), max(ns)+1) if n not in ns]
    dup = [n for n in set(ns) if ns.count(n) > 1]
    print(sid, "slots:", ns, "gaps:", gaps or "-", "duplicates:", dup or "-")
PY
```

**"Highest" is not enough — enumerate, because the registry drifts in two ways that a max never
shows.** Measured 2026-09-17 on this tree: **M6 has a gap at n=4** (1,2,3,5 present) and **M1 has a
duplicate at n=3** — two entries, `m1-3` and `m1-2-dossier`, both claim slot 3, and the second one's
slug contradicts its own `series.n`. A writer who coins the max+1 leaves the gap permanent; a writer
who greps only the mirrors sees `m6-3` and collides with a live slot. Neither failure is visible from
the number alone.

When the enumeration shows a gap or a duplicate, that is a **finding for the owner**, not a licence
to pick one. Report the table, name what you would fill, and let Arif choose — the numbering is part
of the published artefact and a duplicate slot is a live citation defect.

## 5. Check the tree before you build

`git status -s` first. Other lanes leave in-flight edits in the same tree (`index.html`,
`generate-discovery.cjs`, untracked generator scripts), and a build run over someone else's
half-finished change attributes their breakage to your article. One writer at a time: if the tree is
dirty with work that is not yours, say so instead of building through it.

## 6. The hold is the deliverable

Where a claim cannot be sourced, the correct output is a named HOLD, not a draft with the number
softened. Publishing an unsourced figure is the failure the hold exists to prevent; report the state
reached and the check that stopped it.

## 7. The seal binds the ledger — so an audit REPORTS, it does not repair

A defect found by §1 cannot be fixed in place. The seal is a hash over the ledger itself:
`computeCanonicalPayloadHash` in `scripts/lib/makcik-source.cjs` hashes
`{id, slug, claim_register, source_ledger}` (claim and source arrays sorted by id), and the generator
writes the result as `merkle_leaf` in the frontmatter of a file carrying `seal: 999` and
`provenance_status: sealed`. That file is git-tracked and clean in the repository.

Therefore **editing one source `url` to point at a real page silently re-seals the article.** The
merkle leaf changes, the recorded seal no longer describes the artefact, and the change lands as a
diff on a published, sealed document. A 56-citation cleanup is not a citation cleanup; it is a
re-seal of every article it touches, and that decision belongs to Arif.

What the agent does instead:

1. **Report the count and the shape** — how many unreachable `url` values, across how many articles,
   in how many published mirrors (§1's command gives all three).
2. **Name the fix form without applying it:** replace the invented scheme with
   `UNVERIFIED <publisher, title, date>` — the information actually held — rather than minting a
   reachable-looking alternative.
3. **State the consequence in the same breath:** a new `merkle_leaf` per affected article, so the old
   seal becomes historical record rather than current attestation.
4. **Stop and ask.** This is an authority boundary, not a judgement call about tidiness.

The same logic blocks "regenerate the mirrors to clear the warning": a rebuild recomputes every
leaf from whatever the source currently says, so it re-seals the corpus without repairing any
citation. Never run a generator over a sealed tree to make a provenance check green.
