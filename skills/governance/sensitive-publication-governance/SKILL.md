---
name: sensitive-publication-governance
description: "Use when publishing adversarial work about an institution."
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [publishing, legal-risk, sourceability, claims, audit, delegation, verification]
    category: governance
    floors_protected: [F1, F2, F4, F7]
---

# Sensitive Publication Governance

For written work that attacks, exposes, or questions an institution — above all when the author
is professionally *inside* the institution being written about, or holds material a reader cannot
independently obtain.

Three jobs. Keeping them separate is the discipline; conflating them is the failure mode.

| Job | Question it answers | Where |
|---|---|---|
| **Sourceability** | Could every sentence be grounded in something a reader can look up? | this file |
| **Risk inventory** | Which existing sentences can't? | `references/sourceability-inventory.md` |
| **Verifiable publication** | Did the piece actually reach the live surface, unaltered? | `references/delegated-publication-contract.md` |

---

## 1. Sourceability — the always-on rule

**Every checkable assertion carries its own home.** If a sentence states a number, a date, a sum,
a named act, or an internal fact, either a citable public source exists for it, or the register
grades it down and says so where it is published.

**The register is not decoration — it is the defence.** Adversarial writing usually carries two
layers: a *voice* (register, persona, tone) and a *substrate* (claims, sources, hashes, version
lineage). The voice buys reach; the substrate buys survivability. Rules that follow:

- **Never carry rigour in the voice, or reach in the substrate.** Caveats belong with the claims,
  story in the voice. Hedging in the voice reads as sincere; storytelling in the substrate reads
  as a dossier nobody reads.
- **Any "I'm just asking" persona is itself a factual claim.** It protects only while true. A
  humble register laid over content only an insider could know converts the persona from shield
  into mask — an adversary reads the gap as evidence of knowledge, not restraint.
- **Keep voice and substance at the same depth.** Insider-grade detail beneath outsider-grade
  voice is the exact mismatch that gets hooked.
- **Never upgrade a claim; always ship the grade.** A weak figure with its caveat is fine; the
  same figure with the caveat stripped is not. Grade evidence A/B/C and publish the grades beside
  the claims — a visible grade is itself evidence of care, which is what a fair-comment line of
  defence actually tests.
- **The defence hangs on the thinnest cell, not the average.** One ungrounded assertion is the
  attachment point; two hundred sealed ones do not compensate. A source that collapses under
  scrutiny was never a source. Treat the register as ongoing hygiene, not a one-time seal.
- **Say the mechanism, not the comfort.** Strong sourcing does not prevent an attack on the work —
  it raises its cost. Never tell the author his registers "protect" him.

**When sourcing a number, prefer the primary artefact.** A figure circulating widely without a
primary source is grade C and must be labelled as such; a headline number quoted from another
outlet that itself lacks it is *not* sourced. Downgrading a claim is the normal, correct action;
so is cutting it entirely when no public home exists.

## 2. Hard boundaries — what this skill never does

- **No legal verdicts.** Never characterise a piece as defamatory, actionable, safe, or
  defensible. The inventory is evidence; the legal call belongs to the author and his counsel.
- **One method line, once.** A single plain disclaimer such as "I read the record, I am not a
  lawyer" and then straight to mechanics. Do not repeat it every turn, and do not hedge every
  sentence with it — that trades the author's judgement for your comfort.
- **No speculation about who supplied what.** If a sentence could only have come from inside, say
  it needs a non-public source. Never name, hint at, or reason about a source.
- **No unrequested advice on publish / retract / amend / respond.** Those are singular decisions
  reserved for the author. Present the mechanism; let him pull the trigger.
- **Never present a partial audit as complete.** A sweep that read some of the corpus and reports
  as though it read all of it is the specific failure this skill exists to prevent.

## 3. Auditing an existing corpus

Run the full procedure from `references/sourceability-inventory.md`. The shape, in brief:

1. **Extract** the bodies to plain text before reading anything — never audit from a rendered
   page you have to re-render. `scripts/extract-makcikgpt-bodies.py` does this for the arifOS
   article corpus.
2. **Print extracted-vs-source counts and check them.** A content extractor that matches only
   one storage shape silently drops part of the corpus and still reports success. The article
   `.ts` files alone store the body in two shapes (`html:` and `const html =`); a scanner keyed
   on one anchor returned 30 of 35 files and looked fine.
3. **Batch, then delegate one reader per batch — mutually blind.** A reader that sees another's
   findings converges on them; independent coverage is the point. Give each reader the identical
   task text, category list, and severity scale in its own context.
4. **Merge mechanically** (dedupe on `(slug, quote)`), group by severity, and report the
   **negative** as well as the positive: which pieces came back clean is half the value.
5. **Quote-anchored only.** A finding without a verbatim quote is an opinion.

## 4. Publishing

When the piece is going to a live surface and the build is being handed to another agent, the
contract in `references/delegated-publication-contract.md` applies. The load-bearing rules:

- **Pin hashes of every input in the brief, with an explicit STOP on mismatch.** Shared working
  directories are overwritten by sibling agents mid-task; without a pin a stale input produces a
  complete, plausible, wrong deliverable and the report still says "done".
- **A 200 proves nothing on a client-rendered route.** Plant a unique marker in the page and
  grep the *shipped bundle*. Marker count 0 = stale build. Never accept an HTTP check alone as
  evidence of publication.
- **Grade discipline survives the medium.** Converting print to web must not upgrade a claim or
  drop a caveat. Retargetting a section from one named reader to a general audience may change
  the addressee and nothing else.

## Support files

- `references/sourceability-inventory.md` — the sweep procedure, reader task template, taxonomy,
  output schema, and report rules.
- `references/delegated-publication-contract.md` — the verifiable mission-brief skeleton for
  handing a build to another agent.
- `scripts/extract-makcikgpt-bodies.py` — extract article bodies from the canonical `.ts` files
  to text, with round-robin batching for parallel review.
