---
name: machine-discovery-surface-audit
description: Use when auditing a repo's machine discovery surface.
version: 1.0.0
author: Hermes Agent
tags:
  - discovery
  - machine-readable
  - public-surface
  - verification
  - osint
  - agentic-web
---

# Machine Discovery Surface Audit

A public software project now has two audiences. Humans read the README when they
arrive. **Indexers read the repo before any human arrives, and their output is what
the human reads first.** A directory grade, a catalog entry, a scanner note or a
search ranking is often the first sentence a stranger sees about the project — and
it was written by a machine that never ran the software.

Use this skill to answer three questions:

1. Which machine surfaces already describe this project, and what do they say?
2. Is a claimed listing or grade real, or is it an artefact of how search works?
3. Which sentences in the public surface are falsifiable, and therefore need a
   timestamp and a measurement method?

## The layer map

Check these classes in this order. Each one is a different kind of claim.

| Layer | What it does | Typical verdict shape |
|---|---|---|
| MCP server directories + scanners | Enumerates servers, infers risk from tool names and input schemas | Composite letter grade, "review prompts" |
| Agent-mod catalogs | Reads agent config files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`), counts tokens per session | Inventory + token cost + changelog watches |
| Skill / agent directories | Crawls GitHub by seed list, publishes stars, forks, install counts | Listing page with metadata |
| Package registries | Release cadence, download counts, wheel contents | Numeric time series |
| Code search / repo search | Description text, topics, stars | Ranking position for a phrase |

Two distinct kinds of output, and they must not be reported as one:

- **Tested** — the surface actually executed something (a scanner that ran probes).
- **Inferred** — the surface read names and schemas and reasoned about them.
  An inferred grade is a review prompt, not a finding. Say which one you have.

## Step 1 — Find what already exists, from the machine's side

Search the project name on each surface, live. Do not trust a prose claim that a
listing exists — open the listing.

```bash
# repo metadata (the machine-readable description is the discovery bait)
gh api repos/<owner>/<repo> --jq '{description,topics,stars:.stargazers_count,created:.created_at}'
# package download reality
curl -s "https://pypistats.org/api/packages/<pkg>/recent"
```

## Step 2 — The control probe (do not skip this)

**A search page that contains your query string is not a search result.** Many
sites echo the query into the HTML, into a client-routed param, or into the
hydration payload. Grepping the fetched page for the name will then "find" it
every time.

Run the identical fetch with a nonsense token:

```bash
curl -s "https://<site>/search?q=<real-name>"    -o /tmp/real.html
curl -s "https://<site>/search?q=zzqqxxnothing"  -o /tmp/ctrl.html
grep -c -i "<real-name>" /tmp/real.html
grep -c -i "zzqqxxnothing" /tmp/ctrl.html   # >0 ⇒ page echoes queries; the test is void
```

If the control also matches, the page proves nothing. Resolve the listing another
way — a direct record URL, an API endpoint, a sitemap entry. If neither works,
report **UNKNOWN**, not "listed".

## Step 3 — Separate marketing numbers from live numbers

Repos and landing pages routinely quote a bigger number than the live site shows.
Both can be true at different times, or one can be a stale template. Quote the
live figure with its date, and name the discrepancy rather than averaging it.

```bash
curl -s https://<site>/sitemap.xml | grep -c "<loc>"   # scale of the live catalog
```

## Step 4 — Resolve name collisions before citing

Two unrelated projects share a name more often than you would expect: one is the
research repo, the other is the hosted directory that actually lists you. Citing
the repo while describing the directory's behaviour is the most common error in
this class of audit.

Rule: for every surface you cite, record (a) the exact URL you read, (b) whether
it is a repo or a hosted service, (c) the operator named in the footer. If the
footer names a different operator than the citation implies, you have the wrong
surface.

## Step 5 — Grade the claims, not the prose

Not every word is scrutinised. Machines test **falsifiable** statements and quote
them out of context. Split the public surface accordingly.

| Class | Example | Risk |
|---|---|---|
| Prose, philosophy, positioning | why the project exists | none — no machine scores it |
| Numbers | "13/13 floors passing", "342k receipts" | high — needs date + method or it decays |
| Status words | verified, audited, production-ready, secure, sealed | highest — scanners and humans both grep these |
| Config and manifests | `AGENTS.md`, tool names, permission declarations | high — read as behavioural evidence |

Handle each falsifiable claim as **scoped + versioned + dated**. A claim without a
timestamp is not cautious, it is simply wrong later.

Do not import a second claim taxonomy. The federation already runs
MEASURED > DERIVED > UNMEASURED > UNKNOWN. An outside agent offering a five-class
vocabulary (PROVEN / CURRENT / TARGET / RESEARCH / UNKNOWN) is describing the same
distinction — take the idea if useful, never run two ontologies for one question.

## Step 6 — Report

- What is listed where: surface → exact URL → what it says → tested or inferred.
- What could not be verified: say UNKNOWN and say what would resolve it.
- Which public claims are currently falsifiable-and-stale, ranked by how often that
  sentence is likely to be quoted.
- Never present an inferred grade as a measured one; never present a directory's
  grade as a security verdict.

## Pitfalls

- **Query-echo false positive.** Grepping a fetched search page for the search term
  always matches. Control probe or it is not a finding.
- **Repo marketing number taken as live state.** The README's "24k+ indexed" and the
  site's "2,914 tools scanned" are different claims about different things.
- **Same name, different project.** Verify operator and URL before attributing
  behaviour to a citation.
- **Inferred grade quoted as a verdict.** A letter grade computed from tool names
  and schemas is a review prompt. Presenting it as "the scanner found X" misstates
  what ran.
- **Treating a listing's absence as absence of interest.** Not being in a catalog
  says nothing about who is reading the repo.
- **Assuming a mechanism from a reproducible path.** "This route exists and is
  repeatable" is not "this is how it happened." Discovery provenance — who found it,
  with what query, when — stays UNKNOWN without logs or admission. State the path as
  possible, the event as unproven.
- **Letting scrutiny become paralysis.** The rule is not "every sentence must be
  un-misreadable" — that is impossible. The rule is: every material claim is scoped,
  versioned, falsifiable, and does not run ahead of measured reality.

## Companion checks

- Inbound contact from a lab, auditor or vendor → verify the entity, not the pitch:
  registry number, officer appointments, prior entity status, DOI/standard footprint.
- A pasted agent report about any of this → audit it claim by claim; machine-written
  audits of machine surfaces are still self-reports.
