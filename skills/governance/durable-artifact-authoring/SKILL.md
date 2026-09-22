---
name: durable-artifact-authoring
description: "Use when sealing session insight into federation canon."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Durable Artifact Authoring

> **One fact, one owner, one axis.** Anything worth writing down is worth checking whether it was
> already written down.

## When to use

- Sovereign says "code this into the kernel / state / agents", "seal this", "extract the eurekas"
- You are about to create a doctrine file, instruction fragment, skill, or ledger entry from a session
- You are about to act on an external AI's review or proposal

## Step 1 — Sweep for an existing owner (mandatory, before writing anything)

```bash
git -C /root/AAA log --oneline -15
ls -la /root/AAA/instructions/<topic>.md /root/AAA/governance/<TOPIC>.md
ls -la /root/AAA/canon/<EUREKA-topic>.md
grep -rl "<topic-keyword>" /root/AAA/instructions /root/AAA/canon /root/AAA/eurekas /root/AAA/governance
```

Also check the fragment table in `/root/AAA/AGENTS.md` and the tail of
`/root/AAA/eurekas/eureka-entries.jsonl` — **each entry carries a `session` id**. If that id matches
this session, the work is already done.

**The tell:** a doctrine that feels fully formed on first draft is usually one you already wrote.
Context compaction erases the memory of authoring an artifact; it does not erase the artifact.

### Step 1b — Verify the IDENTIFIER you are about to cite, not just the owner

Sweeping for an owner finds *whether* a doctrine exists. It does not tell you what its class
identifiers **mean**. Citing a rule number you have not opened is the same defect as citing a
document you have not read — and it survives longer, because a bare `C<n>` looks like a
cross-reference to everyone downstream.

**A lineage line is not a definition.** A file whose header reads

```
Lineage: <parent>.md (C13/C14) -> this file (C15/C16, <date>)
```

means *this file adds or extends those clauses*. It does **not** mean *this file is* those clauses.
Reading the arrow as identity is enough to attach an entire session's findings to the wrong
canonical text, while every downstream reader accepts it — because the number is real.

Before an identifier enters a durable artifact:

```bash
# 1. Open the file that DEFINES it — not the file that merely references it
grep -rn '^C1[0-9]' /root/AAA/instructions/human-meaning-membrane.md
# 2. Check the definition actually matches the meaning you are attaching
# 3. If it does not match, cite by NAME (the doctrine file), never by class number
```

**Never mint a sub-identifier over a live prefix.** `C15.1` / `C15.2` under an existing `C15` is
exactly what **C20 SYMBOL TRUTH** prohibits: a symbol already carrying meaning must never be
redefined, and a new axis must not be minted over a live prefix. The instrument already ships —
run `/root/scripts/symbol-probe.py` and read `/root/AAA/canon/SYMBOL_TABLE.json` (its `_rule` and
`reserved_never_reuse` keys) **before** a new identifier is written into anything durable. The probe
takes a *document path*, not a symbol name — read its usage before invoking it.

**Why this belongs in the procedure, not in memory:** this is a claim without provenance applied to
the citation layer. A rule number with no opened definition is an unattributed claim wearing the
costume of a cross-reference. Two seats can propagate the same wrong identifier for a whole session
and both be wrong in the same way, because neither ran the check.

## Step 2 — Classify, then act

| Finding | Action |
|---|---|
| Owner exists and covers the whole insight | **Delete your draft.** Report the existing owner's path. |
| Owner exists, your pass adds a genuine delta | **Merge the delta into the owner.** Never create a sibling file. |
| No owner anywhere | Mint, then wire it (Step 3). |

**Deleting your own finished work is the correct move, not waste.** A second file stating the same
truth is permanent reconciliation debt; the sweep costs seconds.

## Step 3 — Wire every minted artifact to three surfaces

1. **Boot / fragment** — a pointer in the always-loaded layer so agents actually see it
   (`/root/AAA/instructions/base.md`, the fragment table in `/root/AAA/AGENTS.md`).
2. **Ledger** — an entry in `/root/AAA/eurekas/eureka-entries.jsonl` (`session`, `evidence`,
   `truth_class`, `verdict`) so the reasoning is traceable.
3. **Agent behaviour** — a skill (or a section in the skill that governs the task class) carrying the
   *procedure*, not the doctrine prose. Doctrine says what is true; the skill says what to run.

Commit each surface so the seal is verifiable, and run the repo's doctrine-status gate if one exists.

### The two ledgers are not interchangeable

`/root/AAA/canon/eureka-entries.jsonl` and `/root/AAA/eurekas/eureka-entries.jsonl` are different
objects with different authority, and Step 1's sweep (`grep -rl … /root/AAA/canon`) will surface the
first one first:

| Path | Role | Writable? |
|---|---|---|
| `canon/eureka-entries.jsonl` | the **frozen ratified registry** — every row is `RATIFIED_*` / `SEALED` / `F13_RATIFIED_CHAT` | **no** — `chattr +i`, append returns `EPERM` even as root |
| `eurekas/eureka-entries.jsonl` | the **live feed** written by sessions (`ts`, `agent`, `session`, `truth_class`, `status`) | yes |

Write to the live feed. If a row must reach the frozen registry, that is a ratification act: a
`CANDIDATE` / `PROPOSED_AWAITING_F13` entry plus the sovereign's word, not an append.

**An `EPERM` on append is a governance signal, not a permissions bug.** Check `lsattr <file>` before
diagnosing anything; the `i` attribute refuses writes by design, and the flag exists to make exactly
this class of write impossible. Report the true state (`BLOCKED_AT_<gate>`, naming the exact
operation) and route the entry to the writable surface. Clearing the flag to make your own write land
inverts the authority order the flag enforces — the same rule as any other protected target.

## Step 4 — Declare residual debt honestly

If the rule is doctrine-layer only (no kernel enforcement yet), say so in the artifact and in the
report: *"detection is debt until it can say NO."* Do not let prose binding be read as a gate.

## Session close — classify the remaining work before the candidate

When the ask is to compile what is left and execute it toward a seal, the candidate is the LAST step,
not the first. Sweep the residue, classify every item, execute what is already inside your authority,
and HOLD the rest with the reason named.

| Class | Test | Action |
|---|---|---|
| Executable | info + authority + capability already exist | **execute now** — the deliverable is the artifact, not a plan to build it |
| Authority boundary | needs a naming decision, a retirement, or a governance change | HOLD; name the exact decision and its options |
| Ambiguous by construction | the target has other live dependents, or content is split across two copies | HOLD; say which dependents you resolved |

Some residue looks executable and is not. An advertised *name* whose body exists nowhere is a question
about whether that name is retired — a **naming** decision, not a cleanup. Build the removal pass,
dry-run it, and reject it when every target still has other dependents; the honest output is a FAILing
check plus the named decision, not a quiet deletion.

**The close write path:**

```bash
python3 /root/scripts/carry_forward.py append --agent <id> --kind <kind> \
  --session-id <sid> --content "..."
```

`--agent` is validated against a fixed writer allowlist, and a display name is rejected
(`[DENIED] agent 'X' not in writer allowlist: [...]`). The refusal names the valid ids — read it and
retry with a listed one. Do not report a bare refusal as a broken tool, and do not substitute a
friendlier display name because it looks more accurate.

**State the facts the decision depends on — they are part of the artifact.** Name the repo, the
commit, and the **branch** each change sits on. A repair whose worktree is on a long-lived proposal
branch, with the default branch N commits behind, is one `git checkout` from reverting; nobody can
authorize that without knowing it. Same for anything frozen, externally-owned, or held — say it rather
than presenting a clean summary.

**An empty input space reports health.** If a close checklist prints "0 remaining", read its input
count beside it. A check that found nothing because its path was wrong prints the same clean zero as a
genuinely clean session.

## Artifact class is not decoration — it decides whether the artifact can bind

A durable artifact carries a **class**, and the class decides its authority. Writing the class is
what stops an artifact from being promoted by accident: an agent must not be able to upgrade its own
guidance into binding policy by placing it in a privileged init path.

```
observation | operational_handoff | guidance   → reference/advisory. Unapproved agent-authored
                                                  material loads as ADVISORY, never binding.
policy | constitution                           → binding. Require approved_by ≠ null
                                                  (constitution additionally requires F13).
memory                                          → append-only, provenance-carrying.
```

The full taxonomy, the `context_manifest` field list (`class`, `author`, `source_commit`,
`authority_level`, `approved_by`, `binding`, `expires_at`, `constitution_compatibility`, `supersedes`,
`content_hash`) and the six pre-load checks live in the recovered body at
`/root/.hermes/skills/core/federation/handoff-contract/references/absorbed-FORGE-cross-agent-handoff.md`
§ *Context-Capture Governance (WAJIB 8)*. Load it before minting a durable artifact. An expired
`policy` artifact loads as `observation`; supersession must be explicit, never a silent replace.

## Receipts come from the ledger tool, not from prose

Never hand-write a hash, an artifact id, or a supersession link. The federation already has the
machinery — use it, so `claim → artifact → hash` is a real join:

| Need | Tool |
|---|---|
| Hash the file on disk, verify any declared sha256, append to the chain | `claim_artifact_register` |
| Bind claim → type → quote → locator → artifact_id, snapshotting the hash | `claim_record` |
| Recompute the live hash and get a machine verdict on end-to-end traceability | `claim_trace` |
| Coverage at a glance (by type, by brief, verdict distribution, unverified count) | `claim_ledger_stats` |

Corrections are made by recording a new claim with `supersedes_claim_id` — the original is never
mutated. That is the same rule as § *Supersession* below, with an owner.

## Non-negotiables

```
NO durable artifact without an owner.
NO material factual claim without evidence or an uncertainty label.
NO "final" label while the source set is incomplete.
NO mutable file as the only proof of a decision — the receipt is the proof.
NO secret, credential, or unnecessary personal data embedded by default.
NO external publication, filing, or distribution without 888 HOLD.
NO live count or telemetry figure inside a long-lived document — cite the census
   artifact with its timestamp and method, or label it derived/unverified.
NO silent overwrite of a ratified artifact — supersede it explicitly.
```

## Pitfalls

- **Foreign seal blocks are never ingested.** An external artifact that copies the seal *schema*
  (`dS`, `kappa_r`, `peace2`, `confidence`, `shadow:` list, `verdict:`) witnesses nothing. Borrowed
  scalars are decorative until computed here. **Accept the argument, verify the citations, refuse the
  numbers.** Shape is not witness.
- **An artifact that warns against false precision while emitting unbacked numbers is committing the
  error it names.** Name that explicitly in the verdict.
- **Score external reviews into four buckets, not a prose reaction:** ACCEPTED INTO CANON ·
  OWNED AS OVERREACH (your errors it caught — fix them *and* record the correction log so they cannot
  be re-imported) · REJECTED FROM INGESTION (invented numbers, copied seal block) · UNDER-WEIGHTED BY
  IT (what it missed that matters more than what it caught).
- **Verify citations before trusting an argument.** `web_search` each load-bearing reference. Real
  sources argue; invented sources perform.
- **A citation naming a source CLASS is not a citation.** "H1 report / UOB KH", "analysts say",
  "the annual report" cannot be checked — no page, no table, no line. A class-level citation is
  where fabrication survives longest: it reads as sourced and is unfalsifiable. Any figure entering
  canon, an anchor table, or a deliverable must name the document AND page/table. Treat an anchor
  lacking an instance-level reference as unverified by default, however formal it looks.
- **Audit provenance before auditing accuracy.** A wrong number in canon is usually a *self-generated*
  number that acquired a citation afterwards. Search the memory/ledger export for the digits, not just
  the file that quotes them:
  ```bash
  grep -n "<digits>" /root/AAA/reports/*mem0-export*.jsonl
  ```
  Read the record's `attributed_to`, but **treat it as a channel attribution, not an authorship
  claim** — it names who last spoke the figure in that channel, not who originated it. An agent
  restating the principal's earlier words is filed as `assistant`, so `assistant` alone **cannot**
  distinguish "the agent invented this" from "the agent repeated a human's testimony". Before
  charging self-generation, walk the thread backwards:
  ```bash
  session_search(query="<digits>", sort="oldest")   # the origin is often the human
  ```
  Escalate to a fabrication finding only when no human utterance and no internal document precedes
  the agent's first use. Where a human originated it, the verdict is `UNVERIFIED — first-party
  testimony`, and the canon entry is corrected for its **citation**, not retracted for its content.
  A fabrication charge resting on a restatement record is itself a fabrication — and the more
  damaging one, because it discredits the audit along with the figure.
- **Check the unit against the reporting convention.** Confirm how the source denominates the metric
  (RATE `’000 boe/day` vs VOLUME `billion boe`/`MMboe`) before accepting or deriving it. A volume unit
  on a metric the source only publishes as a rate means the figure was not read from that source.
  Related trap: one digit string recurring across unrelated line items — enumerate every role a
  number plays before reconciling anything to it. Coincidence of digits is not arithmetic relationship.
- **Never sum nominal flows across time periods.** A lump paid 14 months ago plus an instalment
  stream still running is not a total; discount to a common date or present the flows separately.
  Also separate *deferral* from *loss*: a counterparty withholding payment holds a **receivable**, so
  the harm is the cost of carrying it (principal x rate x months) — orders of magnitude below
  "amount x months", and court interest may return part of it. Whoever holds the cash during a
  dispute collects that discount **even if they lose**, so the time value is itself part of what is
  being contested and belongs in the analysis rather than the framing.
- **Separate date-of-order from date-of-fact.** "Pay by 6 October" is not "paid on 6 October";
  "continues to pay" is not "balance is zero". Attributing action to a deadline fabricates an event.
- **Search the counterparty's mandatory disclosures, not only the host country's.** When a claim
  touches an asset, branch, or contract involving a **foreign listed** company, that company's
  filings (SEC EDGAR and equivalents) are primary record and are often the *only* dated record — the
  host country may not have published anything yet, while the counterparty files on its own calendar.
  A country name present in an earlier filing and **absent** later, with the subsidiary list (EX-21)
  unchanged, reads as *operations exited, entity retained* — a dated finding the host's records
  cannot give you. Keep a control term whose count must not move, so a zero cannot be a parse
  artefact. EDGAR full text needs a declared `User-Agent` with a contact address; a browser UA is
  served an "undeclared automated tool" page instead of the filing.
- **Check that the document postdates the event before treating a miss as evidence.** A report whose
  as-at date precedes the transaction **cannot** contain the resulting figure. Confirming a claim is
  absent from documents that predate it is a category error dressed as a finding — it produces a
  confident negative carrying no information. Establish the event date and the report's as-at date
  first; if the report predates the event, name the edition that will carry it and stop.
- **Match the citation's time direction to the claim's.** A backward-looking claim can cite a past
  report; a **forward-looking** one — a future entitlement, a pending handover, a rate not yet
  effective — cannot, because no published document can contain a quantity that has not happened.
  A past-report citation beside such a claim is refuted **without opening it**: name it
  `CITATION IMPOSSIBLE BY CONSTRUCTION` and ask for the instrument that will eventually carry it.
  The defect is the **citation, not the number** — an internally-held figure is *expected* to have no
  public source, so absence proves nothing about it; what must not stand is the borrowed authority,
  which is most damaging exactly when the number underneath is true. See
  `references/claim-provenance-audit.md` step 1d for the test order.
- **When a breakdown is not disclosed, write `NOT DISCLOSED`.** Never derive an undisclosed split by
  subtraction and never let the derived figure inherit the source's authority. Non-disclosure is
  itself a finding — a split that were innocuous would not be withheld.
- **Turn an unreconciled figure into an implied quantity plus a discriminating question.** When a
  recalled or reported number will not obey the mechanism it should, do not pick the mechanism that
  fits the preferred story. State what the figure *implies* ("a 50:50 carve-out cannot produce a 77%
  drop; this value implies a base of exactly 140"), then enumerate the candidate mechanisms — real
  economic change versus accounting consolidation, an unfavoured unit, an unstated entry basis,
  bundling with a sibling transaction — and name the **single number that would discriminate between
  them**. Ask for that number. An unexplained value is most useful as a question generator; it becomes
  a liability the moment it is written up as a conclusion.

## Retracting a claim already written to a sealed surface

A wrong figure in canon, a frozen ledger, or another team's artifact is the hard case: you cannot edit
it in place, and leaving it standing lets the next reader re-import it as fact. Do not force the write
and do not stay silent.

1. **Stage the correction** to a path you do own, named for the claim rather than the incident
   (`CORRECTION-<SUBJECT>-<YYYY-MM-DD>.md` under a staging directory).
2. **Quote the claim verbatim with its location**, then `VERDICT: UNSUPPORTED — RETRACT`.
3. **Give the citation-resolution table** — each named source, where you opened it, whether the digits
   appear, verdict. A citation that does not contain the number is decoration, not citation.
4. **Show the provenance chain** — where the figure actually came from.
5. **Supply the replacement** with instance-level references, and **explicitly retain the neighbouring
   claims that survive** so a future sweep does not take them out with the retraction.
6. **State plainly to the user that the retraction is STAGED and canon is sealed.** Never imply the
   correction has landed while it is pending — that is the same transition-lie the retraction is
   meant to fix.

See `references/claim-provenance-audit.md` for the full trace procedure.
- **A review of work already done is a merge task, not a build task.** Run Step 1 before treating any
  incoming review as new work.
- **An external reviewer reads the PUBLISHED surface, not your disk — so a review can recommend what
  you already have and cannot reach.** When a consolidation or retirement leaves a thinned stub, the
  reviewer sees the stub and proposes the schema, section, or reference that the retired body already
  contained, usually in less detail than the original. Before drafting anything a review asks for,
  check two things: is the owner *reachable* (resolve the path the review cites — do not trust a
  catalog or an index that merely lists it), and is the recommended content already *inside* it (grep
  the owner and its `references/` for the field names being proposed)? A recommendation that matches a
  retired body is a **recovery** task — restore the body, wire the pointer — not a build task.
  Answering it by drafting a fresh contract creates exactly the second owner the rule below forbids.
- **A proposal to add a contract IS a draft.** An external review's field list, output schema, or
  "required sections" table is subject to Step 1 like any other artifact: sweep for an existing owner
  before adopting it. A review can be right about the gap and wrong about the fix — the gap is real
  and its proposed owner already exists under another name.
- **A dropped field term makes an equation look clean and lie.** When a doctrine states a pattern, the
  constraint field is part of the claim, not decoration.
- **Split owners are worse than no owner.** Two files stating one truth diverge, and every later reader picks a different one.
- **Dual-file resolution: when two agents create overlapping files on the same topic.** Context compaction or parallel sessions produce two files at different paths covering the same canon. Resolution: (1) compare metadata completeness — prefer the file with witness tags, open questions, sovereign seal, and provenance timestamps; (2) identify unique sections in each file (cross-references, integration points, mapping tables); (3) merge unique sections into the chosen SOT; (4) add a deprecation header to the other file pointing to the SOT (`⚠️ DEPRECATED — SUPERSEDED BY <path>`); (5) record the resolution in the synthesis log. Never delete the deprecated file — future agents may reference it. The SOT selection criterion is metadata completeness, not chronological order or author seniority.
