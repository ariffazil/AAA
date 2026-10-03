---
name: cross-ai-analysis-distillation
description: "Distill pasted external AI analysis against live disk."
version: 1.0.0
license: MIT
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Cross-AI Analysis Distillation

> The principal regularly pastes reviews from other AI systems (Perplexity,
> Copilot, ChatGPT, OpenClaw, Gemini) and asks for them to be brought into our
> system. **A pasted analysis is a proposal about reality, not a finding about
> reality.** Convert it into evidence — and the most valuable output is the
> bucket that says what is wrong.

## When this fires

- "distill this to our system", "audit this", "review this analysis"
- A long architecture / roadmap / audit document pasted from another AI
- Three or more sections of prose with recommendations and no runnable artifact

Adjacent but different: if the peer delivered a **runnable artifact** (zip, repo,
code drop) with a self-verdict block, or a **proposal naming concrete target
paths**, the verification shape differs — see `external-artifact-verdict`.

## The one rule

> Grade against **disk**, never against the document.

An analysis that reviews our design doc inherits that doc's assumptions and hands
them back as findings. A peer that says our proposed object is "surprisingly
close" or "approximately correct" is often grading the proposal against the
proposal — the same external lineage wrote both. Open the object as it exists on
disk and compare field by field.

Reviewing a proposal against a proposal is a closed loop, and its verdict is
flattering every time.

## Procedure

**0. Read the whole thing before probing.** Do not start testing the first claim
you can check; you will lose the source's structure and mis-bucket later claims.
Read once, list, then probe.

**1. Classify every claim into three kinds.**

| Kind | Test | Handling |
|---|---|---|
| **Checkable** | names our file, line, port, count, capability, or log | MUST get a live probe |
| **Literature** | Allen algebra, Event Calculus, Lamport, CQRS, another product's internals | accept as literature, say so, no local referent exists |
| **Advice** | "do not build X", "prefer Y" | accept or hold on judgement; record the decision |

**2. Probe every checkable claim live.** One probe each: read the file, curl the
port, grep the symbol, run the script, print raw log rows. Cheap and decisive.

**3. Bucket into exactly three.** ACCEPTED · REFUTED · FOUND-MISSED-BY-THE-SOURCE.
Never merge them. The third is where you add value the source could not.

**4. Write the distillate as a JSON artifact** in the work area carrying
`distillate_id`, `source`, `method`, `verdict_in_one_line`, the three buckets,
`not_testable_here`, and `net_effect_on_our_position` (`changed` / `unchanged` /
`sharpened`). Record durable claims in the claim ledger. Commit with an honest
message.

**5. Report to the human: lead with the refutation**, then the single thing the
source missed. Do not re-narrate the source's sections back at them. One line per
refuted claim, with the disk evidence that killed it.

## The four tests

### 1. Before accepting "build X", check whether X already exists

Recommendations arrive as hypotheses about our estate, not as gaps. Expect
several to name capabilities that are already built, wired, and running — a
routing registry, a temporal query surface, an independent witness plane. In any
mature system the base rate of *already exists* is high.

> Resolve the named entity against live state BEFORE writing a build plan. The
> recommendation then degrades to a CHECK ("does this measure independently?")
> instead of a project.

### 2. Verify the remediation ADDRESS, not just the finding

A diagnosis can be right about the defect class and wrong about the line. A named
line number is a claim like any other.

> Open the cited line and read the guard scope around it before accepting the
> target. An audit that names a line *inside* a condition that already measures
> correctly sends a fixer to patch working code. Then grep for sibling triggers —
> the same predicate usually appears more than once, and the audit found only the
> first.

### 3. Beware the compliment aimed at a dead system

Praise is a claim too, and the most dangerous one to leave unverified because it
reads as good news.

> For any subsystem named healthy, rich, or ready, read its most recent write
> timestamp. Artifacts that look fine while the process has silently ceased is the
> defect class this intake exists to catch. Same family as a gate that runs only
> after the object it checks.

### 4. Watch for a name that hides state

A key, field, or section heading can assert a stronger — or narrower — state than
its contents.

> When reading any artifact, list the container names and confirm at least one
> reader-facing name matches the contents. When writing one, name it plainly. A
> change list filed under a scoped key is invisible to a reader searching for the
> plain name, and that has already produced a false "the data is absent"
> conclusion in this estate.

## Timestamp filters are the most productive false-absence generator

Filtering a log by the **local** date when the records carry **UTC** stamps
manufactures "no data found" out of good data. A receipt stamped `...T22:45Z`
belongs to the *next* local day.

> Before reporting "no records for <period>", print the raw last few rows and
> check the timezone of the stamp. A null from a filter that could not have
> matched is not evidence of absence — and it will be read as a finding.

## When the authority refuses you the seal

Verdict work ends in an artifact, and the temptation is to call it a seal. Ask the
authority first. A kernel that answers `seal_allowed: false`,
`mutation_allowed: false`, `actor_cryptographically_verified: false` has told you
the ceiling. Do not lift an immutability flag on a tree you do not own to store
your own notes, and do not write the word SEAL over a document with no chain.

> Emit a RECORD that (a) states what it is and is not, (b) quotes the refusal
> verbatim as its reason, (c) computes a real sha256 chain where each row carries
> the previous row's hash, and (d) lists what is still open. A receipt that names
> its own limits is usable; a document that overstates itself is the exact defect
> this intake is meant to find. `scripts/hash_chain_receipt.py` does (c).

## After you edit a registered artifact, re-verify the claim

When a claim is bound to an artifact hash, any later edit — including one by a
subagent you authorised — decays that binding. Re-verify rather than leaving the
old digest live. The ledger reports `artifact_recheck: "mismatch"` and names BOTH
the registered and the live hash.

> The claim text may still be true while its evidence has moved. Say exactly that,
> rather than confirming or refuting.

## Pitfalls

- **Do not let a subagent's edits disappear into your commit.** Check
  `git show --stat <sha>` and make the commit message name every file changed. An
  unmentioned change inside your own commit is the same defect class you are
  auditing.
- **Do not rewrite history to fix a stale record.** A record correct when written
  and later superseded is STALE, not FALSE. Fix it with a supersedes note.
- **Do not charge the source with dishonesty for being stale or circular.** Most
  of it is a prior, not a claim. Name the mechanism.
- **Do not accept a "your system is nearly there" verdict without counting
  objects.** Grading a design is not counting its instances.
- **Do not skip the literature bucket.** Not everything is testable; "accepted as
  literature, not re-derived" is honest and keeps the buckets clean.
- **Confirm a probe CAN match before trusting a null.** A grep or find with the
  wrong path, pattern, or scope returns empty for reasons unrelated to absence.
- **Do not treat an immutable canonical tree as writable.** Doctrine directories
  may be `chattr +i` on purpose. Put work references in the work area and have
  the file say so in its own header.

## Support files

- `scripts/hash_chain_receipt.py` — build a real sha256 chain over artifacts and
  repo heads, refuse the word SEAL, and print an independent verification. Use
  when the authority will not grant a seal but the work still needs a record.
