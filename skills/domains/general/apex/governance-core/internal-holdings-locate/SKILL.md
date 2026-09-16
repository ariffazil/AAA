---
name: internal-holdings-locate
description: "Use when asked what we hold on X. Sweep hidden surfaces."
version: 1.0.0
author: Hermes (arifOS federation)
license: F13-Sovereign
tags:
  - governance
  - memory
  - inventory
  - evidence
triggers:
  - "find me info you have about X"
  - "what do you have on X"
  - "what do we already know about X"
  - "search the server for X"
  - "do we have anything on X"
  - "where does X live"
  - "no data"
  - "not found"
  - "inventory sweep"
---

# Internal Holdings Locate

> A visible-only sweep is not an inventory. Zero visible hits is NOT "no data" — it is "not found yet."

## When to use

Any question of the form "what does the system already hold about X" — a person, an org, a
project, an artifact — and, conversely, any moment you are about to answer "nothing", "no record",
"we don't have that". Applies before the answer, not after the pushback.

## The rule

The subject's records live on **hidden surfaces**. The default search path skips dot-directories
and gitignored files and only *warns* about the matches it skipped. That warning is the map of
the scope you have not searched — treat it as a to-do, never as noise.

## Procedure

1. **Sweep by shape first.** Run both file-name and content search for the subject; run the same
   for each alias/handle/ID (see step 4). Record what you actually searched.
2. **Read the warning line.** A `total_count: 0` next to "N matches in M hidden or gitignored
   file(s)" is NOT FOUND YET. The ignore rules the search tool respects are the exact list of
   places to widen, and `grep`/`ls` do not respect them.
3. **Grep the hidden surfaces directly:**
   ```bash
   ls -la /root/.hermes/output/          # forged artifacts: dossiers, PDFs, reports
   grep -ril '<term>' /root/.hermes/memories/ /root/.hermes/workspace/ /root/.hermes/logs/ 2>/dev/null | head -20
   grep -io '.\{0,150\}<term>.\{0,250\}' /root/.hermes/mem0-promotion-ledger.jsonl | head
   grep -io '.\{0,150\}<term>.\{0,250\}' /root/.hermes/workspace/zen/mem0_dump.jsonl | head
   ```
   Full surface list, with what each one holds: `references/federation-record-surfaces.md`.
4. **Widen the identifier, not just the query.** Name → alias → handle → numeric uid → chat/group
   id are five spellings of one subject and each retrieves different records. A person lookup that
   searched one spelling has not happened.
5. **Aggregate, don't narrate.** Dedupe by record; keep the source path for each fact. If the same
   fact appears in several layers, cite the most authoritative one and note the rest as copies.
6. **Only then answer** — and carry the scope qualifier: "found in X and Y, not searched in Z."

## Delivery shape

Lead with what is held, in this order — not with your search process:

1. **stored record** — the profile/entry itself;
2. **lane & routing config** — for a person: which group carries them, whether `require_mention`
   is off, which allowlist surfaces include them (allowlists live on several surfaces; the one the
   runtime actually reads is the one that counts — verify against the live process env, not a file
   you just edited);
3. **artifacts on disk** — send the file (`MEDIA:/abs/path`), never a description of it; an
   artifact re-described is an artifact the human cannot use;
4. **source-of-truth caveat, unprompted** — say which numbers inside an artifact are external
   ranges or assumptions rather than the authoritative source's own figures. The caveat you omit
   becomes the human's problem when he hands the artifact to someone else.

When the human then adds a fact you did not hold ("X is also ⟨role⟩"), the correct response is a
single memory write plus a one-line confirmation. Do not narrate the relationship or the search
back to him.

## Pitfalls

1. **Reporting absence from one window.** "We have nothing on X" from a visible-only sweep is a
   quantifier swap; the probe was honest, the generalization was not.
2. **Reading the skip-warning as noise.** It is the widening instruction. `gitignore`, `dockerignore`,
   `excluded by default`, "hidden matches" — all the same signal.
3. **One-spelling search.** Alias and numeric id are separate keys into the same records.
4. **Trusting an edited config file over the running process.** Several surfaces can declare the
   same allowlist; only the one in the live environment governs.
5. **Delivering a description of an artifact instead of the artifact.** Send the file.
6. **Answering before you sweep because the answer feels obvious.** The sweep is cheap; the
   retraction is not.

## Related

- `assertion-window-discipline` — the parent rule this operationalizes (window vs world).
- `claim-level-verification` — probe at the level the claim is asserted at.
- `human-intelligence-gathering` — what to do with the record once located (modes, labelling).
