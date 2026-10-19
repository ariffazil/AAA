---
name: discovery-surface-verification
description: "Use when a machine claims it found your project."
version: 1.0.0
owner: Hermes
category: governance
capability_tier: fed-long-context
ecology_state: WARM
owned_by: Hermes
authority_of: AAA
---

# Discovery Surface Verification

> **One line:** a discovery story is a causal claim. A repeatable path is not evidence the path was taken.

Public repos, sites and package indexes are read continuously by machines — indexers, scanners,
benchmarks, crawlers that build agent-readable catalogues. When one of them surfaces your project, or
reports a grade/count/listing about it, the natural next question is *how did it find me*, and the
natural failure is to answer with a plausible narrative built from the fact that it *could* have.
This skill covers verifying those claims in both directions: what the surface actually says, and
whether the causal path is known at all.

## Use when

1. An inbound message says a lab / scanner / directory / agent found your project and acted on it.
2. The owner asks "how did they find me?" or "is this real?" about a public index hit.
3. A public surface displays a count, grade, ranking or listing attributed to your project.
4. You are about to state what your public surface says about you — to anyone, in any artifact.

## The one rule

**Separate the SURFACE fact from the CAUSAL claim.**

- *"The repo is discoverable through public search"* — verifiable, and worth verifying.
- *"The agent reached the person by searching for that phrase"* — a causal claim, and typically
  **UNKNOWN** no matter how tidy the narrative is.

Report the first as measured. Report the second as UNKNOWN until you hold provenance: a log entry, a
referral record, an admission, a dated receipt. A handshake is not a receipt.

## Procedure

### 1. Bind the entity before you believe anything about it

One project commonly exists as four different objects — a repo, a hosted site, a published package,
and a named product — with near-identical names and different owners. Every one is cited as "the
project" and none is interchangeable.

```bash
gh api repos/<org>/<repo> --jq '.full_name, .description, .homepage, .created_at'
curl -sI https://<site> | head -3            # who actually serves it
curl -s https://pypi.org/pypi/<pkg>/json | jq -r '.info.name, .info.version'
```

If descriptions or owners differ, they are different objects and a claim about one says nothing
about the other. Name the object in the sentence: *repo X*, *site Y*, *package Z*.

### 2. Control-probe every search surface before trusting a hit

Directory and index sites reflect your query back into the page — title, canonical URL, a serialised
route param, a hydration blob. The term appears whether or not anything matches.

```bash
curl -s "https://<site>/?q=<term>"          | grep -c -i '<term>'        # maybe a listing
curl -s "https://<site>/?q=zzqqxxnothing"   | grep -c -i 'zzqqxxnothing' # >0 means it echoes
```

A non-zero control voids every reading from that surface, including a match count or a highlighted
snippet. Fall back to a surface that takes no input: the sitemap, an API route, a rendered card with
structured fields.

```bash
curl -s https://<site>/sitemap.xml | grep -ic '<slug>'   # presence = listed, absence = not listed
```

Absence from an index is also weak evidence: its crawl coverage is usually undisclosed, so "not
listed" means *not listed*, not *unknown to machines*.

### 3. Separate the populations behind any number

A README claim of "24K+ indexed" and a live site showing "2,914 scanned" are not contradictory:
different scope, different moment, different population. Never reconcile them into one figure and
never quote one as the other. Report each with its surface, or report the gap as the finding.

### 4. Distinguish inference from measurement in any grade or score

A scanner that assigns a risk grade usually reads **tool names and input schemas** and infers
capability ("can reach shell, filesystem, secrets"). That is an inference, not a test — and it is
published in your name and read before anything you wrote. Say which it is:

- measured: an attempt was made and a behaviour observed;
- inferred: a surface was read and a capability assumed;
- unknown: not examined.

When an inferred grade is the loudest public sentence about your project, that is a publication
decision, not a defect report.

### 5. Enumerate possible paths, then mark the actual one

Do the work that can be done: list the surfaces that would have surfaced you, verify each is real,
and note whether a plausible chain is *reproducible*. That is a legitimate finding — "this path
exists and leads here". Then stop and label the causal step:

> Documented: the project is indexed at A and B, and the description field is quotable verbatim.
> UNKNOWN: which surface, which query, or whether any agent was involved in reaching the sender.

Do not upgrade a reproducible path into an observed one. Verbatim quoting of your own description
tells you *what* was read, not *where* it was read — the description propagates to every index.

### 6. Keep the surface fact and the human motive apart

"How did they find me" and "why did they contact me" are two unknowns, and a clean answer to the
first creates a false sense of having answered the second. A sales motion, a research interest and a
philanthropic offer look identical from outside; the distinguishing evidence is the entity record,
the pricing page and prior behaviour — not the warmth of the message.

When the sender is unknown, check the durable record before weighing the words: company registry
status and incorporation age; whether the named person has a prior liquidated entity; whether they
sell the remedy they recommend; whether they publish or rank on projects without invitation. Record
the interest **beside** the evidence, not folded into it — the finding can be true and the motive can
still be commercial.

## Pitfalls

- **A query echo is the most convincing false positive in web research.** You searched, you saw the
  term, you concluded a match. Run the nonsense-term control before any "found it".
- **A machine that found your repo did not read your writing.** It most likely read the description
  field, topic tags, or a structured manifest. Do not claim machines are scrutinising prose you wrote
  — that overstates exposure and invites the wrong defensive response.
- **Absence of a listing is not evidence of invisibility.** Undisclosed crawl coverage. Report it as
  a fact about the index, never about your reach.
- **A signal from one surface is not a reading of the system.** Directory grade, repo metadata, site
  copy and package metadata are four independent claims; when they disagree the disagreement is the
  finding, and none of them is the verdict.
- **Do not narrate a discovery mechanism into an artifact as fact.** If it goes in a report it must be
  phrased as UNKNOWN with the possible paths named. A plausible story, once written, is cited as
  established by the next reader and cannot be retracted cheaply.
- **The machinery that makes you findable also grades you, on a rubric you did not choose.** Being
  visible to agent-readable indexes is a capability with a cost. State the public terms you are being
  measured by; do not treat a discovered grade as either a compliment or an attack.

## Adjacent

- `claimed-defect-verification` — when the inbound claim is a *defect* rather than a discovery, and
  the question is whether the probe or the system is wrong.
- `human-corpus-falsification` — the human-facing counterpart: claims about a person built from text.

## Support files

- `references/probe-recipes.md` — copy-paste probes for entity resolution, echo control, index
  presence, package metadata and company-registry checks.
