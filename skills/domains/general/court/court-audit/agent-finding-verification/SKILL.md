---
name: agent-finding-verification
description: "Use when verifying findings, audits, or memory/identity claims from another agent or an external AI."
version: 1.0.1
floors: [F2, F4, F11]
triggers:
  - "audit this report"
  - "verify this claim"
  - "is this sealed"
  - "binding machine law"
  - "person card"
  - "memory about me"
  - "eureka entry"
  - "external AI review"
---

# Agent Finding Verification

Treat every finding, audit, or gap-list from another agent (or a pasted report) as UNVERIFIED until you probe its substance. Agent-produced audits are frequently surface-level: they observe the wrong context, over-rate severity, and propose fixes that are regressions.

## Procedure (probe before act, in this order)

1. **Separate surface from substance.** A claim "X is missing/broken" almost always means "I grepped a static artifact and didn't find it." The live truth lives elsewhere.
2. **Probe the runtime.** For a tool: `curl :PORT/mcp -X POST -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'` (is it served live?). For a service's env: `/proc/<pid>/environ` on the SERVICE process — not the CLI, which has no systemd EnvironmentFile. `systemctl is-active`.
3. **Follow symlinks.** `readlink -f` a path before declaring it empty/missing — a "missing" directory is often a symlink to a live target.
4. **Read what the existing thing ENFORCES before replacing or wiring it.** An audit's fix can silently remove a governance gate (e.g. a "dead" global git hook may be un-wired because per-repo custom hooks carry the force-push 888-judge gate + commit identity guard that the global hook lacks).
5. **Triangulate severity last.** Critical/High items are frequently false positives or not-broken; the genuinely-fixable bugs hide in Low items. Verify substance before allocating effort by the severity column.

## Verdict classes

| Verdict | Meaning | Action |
|---|---|---|
| FALSE_POSITIVE | Runtime/truth contradicts the claim | Do nothing; note it |
| NOT_BROKEN | Claim true but harmless (unused ≠ broken) | Do nothing |
| REGRESSION_RISK | The proposed fix would break governance | Do NOT apply; report |
| REAL_BUG | Substance-confirmed and safe to fix | Fix |

## Broadcast Outage Claims ("all endpoints refused / the surface is dark")

**Signal:** A peer agent posts a table of endpoints with `connection refused` and a verdict like "HTTP layer down", "observability surface dark", usually paired with a proposed remedy ("want me to bring the gateway up?").

Treat the table as TWO independent claims and falsify them separately:

1. **Are those ports actually refused?** Re-run the exact port list yourself: `curl -s -m 5 -o /dev/null -w "%{http_code}|%{time_total}" http://127.0.0.1:$p/health`. Never re-read the peer's output, never infer from service state.
2. **Is that the right port list?** Check every row against the canonical port map (`federation-health` → "Observed Port Map"). A port no process owns reads refused forever and says nothing about health.

**Discriminators:**
- **A refused row is only evidence after the row's port is confirmed canonical.** Confirm each row against the map before treating the table as a health signal at all. A single wrong port invalidates the row; a mislabeled column invalidates the reading.
- **A pre-existing scheduled producer already falsifies "nothing to scrape."** When the claimed-victim pipeline is said to have no input, check the artifact's mtime — if it ran and wrote its output earlier the same day, the downstream-failure narrative is false regardless of the port table. Probe the artifact box before the service box.
- **Absence claims need the map; presence claims need one curl.** Same asymmetry as the four-surface scan below: proving "this port is not ours" requires the canonical map, proving "this port is up" takes one probe.
- **Falsify the premise before repairing anything.** When the "outage" is a wrong port map, the fix is the map and the reporter's probe discipline. Bringing up a service that was never down is a mutation with no falsified premise behind it — refuse it and say why.
- **Repeated verbatim report = loop, not new evidence.** When a peer resends the identical message unmodified after corrections were posted, it did not metabolize the correction. Answer ONCE with the refutation and the correct facts, then stop. Re-answering an unchanged claim makes you a participant in the loop and spends sovereign attention on a non-event. Say you are not going to re-litigate it and move on.
- **Report the refutation as a table, not prose.** Port / claimed / measured / latency — the measured column does the arguing. A refutation without your own numbers is just a competing opinion.

## Inbound external AI review (Perplexity / Copilot) — audit the audit

Sometimes the "other agent" is an external model reviewing *our* work: Arif pastes its reply back
and asks for an audit. Do not import it and do not defend against it — audit it, in this order:

1. **Accept the argument where it is correct** — and say so out loud. Conceding a real error is
   the cheapest credibility available, and a review that is partly right cannot be dismissed whole.
2. **Verify every citation.** Resolve each source and confirm it actually supports the claim as
   stated. Real citations can still be stretched past what the paper says. Report what you checked.
3. **Probe its premises about our own system before adopting its plan.** See below — a coherent
   plan on false premises is the most expensive thing a review can hand you.
4. **Refuse the numbers.** See the foreign-seal rule below.

Classify each finding into one of four buckets and name them in the reply:
**ACCEPTED** · **OWNED AS OVERREACH** (our own past errors it correctly caught) ·
**REJECTED FROM INGEST** · **UNDER-WEIGHTED BY IT**.

The last bucket is the strongest signal available: **what did the reviewer miss?** A generated
review reliably mirrors the argument's shape while omitting the operational layer both sides
share. Reporting that gap is what proves the audit was substance-checked rather than relayed.

### Its premises about our own system are claims — probe them before adopting the plan

An external review can be *internally coherent* and *factually wrong about our infrastructure*,
and the coherence is exactly what makes it dangerous: a sound plan resting on false premises
executes wrongly, and reads as well-reasoned the whole way. Separate the **principle** from the
**facts it rests on** and give credit to one while rejecting the other — "the
separation-of-concerns argument is right; the topology it maps onto is not" is a complete reply,
and it keeps the review's good idea while refusing its bad plan.

Probe every load-bearing premise before acting on the plan:

- **"X is a node / service / component"** → enumerate the real namespace
  (`headscale nodes list`, `systemctl list-units --all`, `docker ps -a`). A name appearing in a
  config, an ACL group, or a diagram is not a running actor: a stale identity row outlives the
  thing it named, and a plan that routes work to it is unusable. Report it as "appears in ACL only,
  no such unit exists".
- **"Move X off node Y"** → check what X *is now*, not what it was built as. Shared infrastructure
  becomes a shared organ **by adoption, not by design** — a store holding one consumer's graph
  today may hold a dozen other tenants' graphs, which turns a local move into a migration of
  everything that depends on it. Count the tenants before accepting the move.
- **"Put the heavy work on the smaller box"** → check the hardware per node (cores, RAM, free disk).
  A placement proposal inherits whatever resource picture the reviewer assumed, and a topology that
  inverts capacity is worse than no topology: it concentrates load where headroom is scarcest.
- **"HOLD until <condition>"** → re-probe the condition. A review's blocker may already be
  **discharged** (a copy reported "in progress" that has since completed, a service reported down
  that is now up). Inheriting a stale HOLD stalls ready work; verify the gate is still closed
  before obeying it, and say which premise moved.
- **"Witness / replica belongs on node Z"** → ask what it would own there. Moving the *primary*
  copy of a write-once ledger away from the kernel that writes it converts the most
  failure-intolerant artifact in the system into a network dependency. A witness should observe
  and replicate, never own the primary — reject the placement, propose the replica.

### Its proposed REMEDY is a claim too — test each branch before answering

A review's plan is the part most likely to be adopted unexamined, because agreeing with the diagnosis
feels like agreeing with the cure. Test the remedy against the same ground truth as the premise:

- **"Revert / restore / check out to a known-good state"** → establish what that state *is* first.
  Run `git status -- <scope>`, `git log --oneline -3 -- <path>`, and
  `git show HEAD:<path> | grep '<the-marker-the-review-is-about>'`. **If the mutation is already
  committed, HEAD IS the broken state** — a checkout to HEAD restores nothing, and the real repair
  means reverting a specific commit, which drags every sibling change in that commit with it. Say
  that, and name the commit, instead of agreeing to a no-op undo. A remedy offered as "one minute, I
  can do it now" is a claim about *cost and feasibility* as much as correctness — both are checkable.
- **A binary choice where one branch cannot execute is a framing failure, not a decision.** When
  handed "A or B", test each branch before answering. If A is impossible, say so and give the option
  that works — answering the binary as posed spends the sovereign's authority ratifying a branch that
  does not exist, and hides the one that does.
- **A remedy that mutates a signed or sealed record is not a remedy.** Changing the payload
  invalidates the signature over it, so the "fix" converts a stale attestation into a fresh forgery.
  Correct the classification and HOLD: the mutation needs signing authority, which is precisely what
  the reviewing agent does not have.

### Re-derive the population before accepting any count in the review

Enumeration is the one thing a reviewer cannot fake and the thing they most often get wrong. Recompute
the **denominator**, not just the ratio:

```bash
find <root> -name '<artifact>.json' | wc -l                          # how many exist
grep -l '<marker>' $(find <root> -name '<artifact>.json') | wc -l    # how many carry it
```

A review reporting "25 of 30" against a tree holding 43 artifacts with 34 carrying the marker has
invented both numbers — and the invented denominator is the more damaging half, because it makes the
ratio look like a majority of a population that does not exist. Report your counts as ground truth and
the review's as unsourced; do not average them.

### A "missing file" claim must be re-probed at every DECLARED path

Reviewers probe the path they expect. Before endorsing "X does not exist", read the component's own
config and its `AGENTS.md` for the directories it *declares* — alternate agent/skill dirs, extra roots,
`create_dir` — and check those first:

```bash
grep -rn 'extra_agent_dirs\|extra_skill_dirs\|_dirs *=\|dirs:' <component-config-dir>
ls -la <each-declared-dir> | head
```

A component whose agents live in a declared alternate directory is not missing them; the probe looked in
the default. **Endorsing that claim turns a correct inventory into a fabricated gap**, and the correction
the reviewer then recommends can delete or recreate work that was already where it belonged. A reviewer
that "corrects" a true count downward has made the same class of error as one that inflates.

### Foreign seal block — never ingest

An external artifact that reproduces our seal schema (`dS`, `kappa_r`, `peace2`, `confidence`,
`VERDICT: SEAL…`) filled with **unmeasured** numbers is committing schema mimicry.

> **Foreign seal blocks are never ingested into VAULT999, the eureka ledger, a receipt, or a
> person-card — however constitutional they look. Shape is not witness.**

Accept the argument, verify the citations, refuse the numbers. A reviewer that warns against
decorative precision while emitting unbacked scalars is demonstrating the error it names —
quote it back to them as such.

### The artifact's evidence may be our own corpus echoed back

A review *of a person* (or of our doctrine) can be built entirely from our own artifacts and still
read as independent corroboration. The tell is an `EVIDENCE` block whose citations are the
subject's own public surfaces quoted near-verbatim — a `soul.json` title, a `humans.txt` role line,
a sentence lifted from one of our own witness papers. Independent re-examination cannot be a string
match to the thing under examination.

```bash
for s in "<distinctive phrase from its evidence block>" "<another>"; do
  echo "== $s"; grep -rln "$s" /root/AAA /root/memory /root/.hermes 2>/dev/null | head -5
done
```

Verbatim hits = the artifact is a mirror, and "facts that repeatedly survive re-examination" is
describing a loop, not a check. **A stale in-house string makes it worse, not better:** when the
echoed line is itself obsolete (a floor table from a rename, a count a later SOT superseded), the
loop launders our own drift into "stable fact". Fix the stale surface AND name the loop, or the
drift travels back out and in again.

### An audit the artifact adopts is the loop closing on you

This recurses: the artifact is audited → it endorses the audit → an in-house session seals the
endorsed conclusion into canon or memory. The authority for the claim is then the artifact you were
auditing. Before accepting a "sealed" / "now binding" status, read the chain:

1. **Does the artifact cite the earlier analysis as its validation?** Mutual citation between a
   review and the thing it reviewed is not independent confirmation, however often it repeats.
2. **Which session wrote the row, and under what declared mode?** A session whose own receipt says
   `OBSERVE_ONLY` / read-only / degraded-substrate and which then writes canon or a memory card has
   committed a scope violation — flag the write and HOLD the content regardless of its quality.
   Canon is agent-side HOLD territory; "sealed" is not a status an observing session can grant
   itself.
3. **Is the row in the ledger you think it is?** A ledger entry asserting alignment is a claim
   about the system. Re-run the reconciliation it asserts; never cite the entry *as* the
   reconciliation.

### Receipt existence is not receipt content

A cited receipt ID that resolves is not a receipt that attests. Dump the row's fields:

- **Hash-stub shape** (`body_hash` / `chain_entry_hash` / `prev_hash` / `receipt_id`, with
  `routed_organ: null`, no actor, no timestamp, no claim text) is chain-membership evidence only —
  "something of this hash sits at position N", not evidence of what the report says it sealed.
- **No body store** — grep the `body_hash` value; if nothing on disk holds the body, the row cannot
  be read as an attestation at all.
- **Ungreppable scalar** — a quoted score that appears nowhere in the store that supposedly
  produced it is decoration. Match the field name, not the digits: a latency `292.75` or a
  similarity `0.56` is not `2.75`.

- **Unsubstituted template variable** — a `kid`, `iss`, `nonce`, or `sub` containing a format specifier
  (`%q`, `{name}`, `$VAR`, `<PLACEHOLDER>`) proves the block was emitted by a template, not by a signer.
  It was never a signature, so no payload change is needed to invalidate it. Report it as fabricated,
  not stale — the distinction decides whether re-signing would even help.

Verdict wording: "the receipt exists as a hash row; it does not attest the claim."

### Ledger rows are the most expensive place for a false attestation

A chat report that overstates is corrected in the next message. A ledger row (eureka canon,
receipt chain, memory card) is read by later agents as authority, so a wrong attestation there
propagates. When a row asserts a reconciliation — "live recount = N", "all surfaces now agree",
"0 contradictions remain" — re-run it:

```bash
python3 -c "import json;d=json.load(open('<store>.json'));\
print([len(v) for v in d.values() if isinstance(v,list)], json.dumps(d.get('stats'))[:300])"
grep -rn "<old-value-it-claims-to-have-replaced>" <dirs> --include=*.md --include=*.json
```

- **Summary block vs array disagreement is the commonest form:** the list holds 30 entries while
  `stats` says 29 and its category map sums to 20 — three numbers, one file. Reconcile the summary
  block TO the array, never the reverse.
- **Distinguish a stale count from a wrong count.** "12 of 20 link to F<N>" can be wrong in both
  places once counted live. Re-derive the numerator before touching the denominator, or you bump a
  false ratio.
- **Fix the whole file, not the reported line.** After any count fix, grep the same file for the old
  value — a claim fixed in one table is commonly duplicated in a cross-reference section further
  down the same document.

### Do not repeat material that is deliberately unarchived

Reports about a person sometimes quote an intimate line and label it "sealed" or "harmless". Verify
it is actually in the archive before repeating it. If it exists nowhere but the session that
produced it, restating it — even in order to correct the surrounding report — *is* the exposure.
Say "that line is in no archived surface; I will not restate it" and move on. A report does not get
to certify its own quotation as safe.

### Scope-note instead of bumping

When a document's number is *true of its own narrower scope* (a v1 map covering 20 of the 30 entries
that now exist), do not raise it — that fabricates coverage the document never had. Add a scope
note: what this document covers, what the SOT now holds, and which counts below are scoped.
Reconcile only what is genuinely stale; flag the rest for the owner. Full recipe (probe order, safe
write, verdict shape) in `references/memory-claim-audit.md`.

### Correction discipline

- Record accepted corrections in the target document's **Correction Log by name**
  (`Correction 1 — …`), never by silent rewrite. The trail is the evidence the audit landed.
- Own your own overreach in that same log. "Owned as overreach" is a status, not a defeat.
- Never cite the reviewer as authority — cite the underlying source, after verifying it exists.
- If the corrected document already exists, **merge the delta and delete your duplicate**
  (sweep `git log` first: compaction erases the memory of writing a file, not the file).

## Live-tree audits — your own observation goes stale

When other lanes are writing the tree *while you audit it*, a finding is true only as of its probe
time. A verdict published minutes after the probe can already be false.

1. **Stamp every observation.** Clock time next to each reading; never present a multi-minute-old
   probe as current state.
2. **Before any negative verdict ("never fired", "missing", "absent"), re-probe the two cheapest
   freshness signals:** the artefact's `mtime` and the presence of a receipt/ledger row. *Code
existing ≠ wire fired* — the module can be written and imported while the thing it writes has not
   moved since before it existed. Report "written, unfired as of HH:MM" rather than "missing".
3. **If reality contradicts you mid-audit, append an AMENDMENT — never silently rewrite.** Keep the
   superseded finding visible with its timestamp and name what superseded it. A report that quietly
   becomes correct teaches nobody where the truth boundary was.
4. **Never seal (commit) a tree a live writer is touching.** Wait for quiescence, then take ONE
   checkpoint. A commit taken mid-write captures a torn snapshot and destroys the commit's value as
   a reference point. See `references/live-tree-audit.md` for a quiescence-then-seal watcher,
   and `references/loop-maturity-audit.md` for sealing a self-improvement loop (running ≠ sealed).
5. **Do not name an author you did not see.** Concurrent sessions mutate the same tree; if you did
   not sweep every session's writes in the window, report the change without a name.
6. **Keep the audit report out of the audited tree.** Writing it inside dirties the very state you
   are measuring — state the tree's cleanliness excluding your own artefacts, or land the report
   outside it.

## Alert-path triage — field semantics, stale registry, or repair race

A dead-path alert (`DEAD_POINTER`, `SILENT_FAIL` on `<path>`) has three causes needing different
fixes. Checking only "is it alive NOW?" collapses them and hides the real one.

0. **Establish what the path field MEANS before triaging anything.** Read the line that builds it
   (`grep -n "<pattern_type>" <emitter>.py`) and look at the variable being interpolated. An arrow
   (`PATTERN → /path`) reads as "the defect is at /path" to every reader, but the field may be a
   *destination* — the owner skill a lesson was queued to — a registry key, or a log target. When it
   is a destination there is nothing to triage: the alert is a routing receipt, not a defect report,
   and the remediation a reader invents (re-point the registry at the path) creates the broken
   reference it believed it was repairing.
   **Discriminator:** if the SAME path appears on every alert of that class no matter which defect
   fired, it is a constant — a destination or owner — never a location. A defect location varies
   with the defect.
1. **Probe existence AND mtime:** `ls -d <path>; stat -c '%y %n' <path>`.
2. **Compare the artefact's mtime against the alert's event timestamp.**
   - Alive, mtime **after** the alert time → **repair race**: the alert was TRUE when generated and
     the fix landed after. Not a false positive — a stale snapshot.
   - Never existed in that layout while the capability lives elsewhere (`readlink -f`, content
     search) → **stale registry**: the emitted path is drift; fix the registry row.
3. **Same verdict ≠ same bug.** Because alert #1 was registry drift, do not wave alert #2 through —
   that is how a genuinely-dead pointer gets dismissed.
4. **Fix the emitter, not the row.** A registry still resolving old layouts re-emits; one corrected
   entry is a symptom patch.
5. **"The path is alive now" is not a verdict until the mtime check is done** — it is the sentence
   that converts a race into a false negative.
6. **A path claim is node-local until both node locks match.** The same logical skill can sit at
   different relative paths on different hosts (one layout under `devops/`, another under a
   `domains/<organ>/...` tree), and a loop that runs on only one host emits that host's layout.
   `ssh <peer> 'ls -d <path>'` reports the peer's reality, not yours. A peer's "that path is missing"
   and your "it is present" can both be true — and the disagreement is itself the finding
   (federation-level path drift), usually worth more than either claim. Check which host runs the
   emitter before retracting either reading, and never relay a peer's path verdict to the sovereign
   before probing it on your own node.

## Auditing a delivered document (dossier / report / synthesis)

A peer-delivered *document* is a different object from a peer-delivered *finding list*. It
carries claims about the world, claims about its own provenance, and claims about capability.
Falsify all three.

### Capability claims: find the executable, not the description

"The tool has been built. The code is written. The test has not been run" is a capability
claim, and it is verifiable — locate the executable artifact. Do not accept the sentence; find
the thing.

```bash
grep -rn "<capability-name>" --include="*.py" --include="*.sh" <repo> | head
find <repo> -iname "*<capability>*" -not -path "*/.venv/*"
```

**The tell:** if the only artifact is a *dataclass field*, a *config slot*, or a *status enum*
— `result = "PENDING"`, `available = False`, `# TODO` — the capability is **declared, not
implemented**. Say what the artifact actually is (a filter with an empty slot), not what the
document calls it (a built tool). A `PENDING` in one module beside a document claiming
completeness *is* the finding.

**Corollary — "free / zero cost" needs the input checked too.** A test is not free if the data
it consumes is unpublished, and an `available: false` flag beside that input is the artifact
saying so.

**Corollary — a number with no home is unsourced.** When a document and the codebase disagree
on a value (a depth, an age, a figure), grep the tree for that value and count its occurrences.
A figure appearing **nowhere else** is the document's own invention, not a conflict between
sources — which reframes the fix from "reconcile our sources" to "flag this document". Check
sibling modules before concluding the codebase disagrees with the document; a single unsourced
string in one file is not a multi-way split.

### Citation metadata is itself a claim

The "verify every citation" step means more than resolving the URL. Check the **journal, year,
DOI, and author** on a sample. Drifted metadata is a reliable marker of a document assembled
from memory: a real, correctly-relevant paper can be attributed to the wrong journal and given
a plausible transposition of the real DOI. **A correctly formatted citation is not evidence the
cited work was consulted** — verify a sample, and where metadata is wrong, downgrade confidence
in the surrounding synthesis proportionally.

### Provenance record for uncustodied documents

A polished deliverable may arrive with no build source, no forge-work entry, and no ledger row.
That absence is a finding. Record per artifact: size, hash, **hash stability across independent
deliveries**, declared authorship, declared sources, whether a build source exists on the host,
and a verdict — `PROVENANCE_PARTIAL` (authorship declared, build untraceable) or
`PROVENANCE_ABSENT` (no build source at all). Where the document makes claims about a running
system, also record the deployment state at ledger time (repo commit, deployed commit, live
self-report) — without it a later reader cannot tell which reality was described.

### The document's own honesty does not buy it a pass

A document that flags its own gaps, evidence-classes its own claims, and refuses to sell its
headline number is doing real work — and it is still *not* exempt from the three checks above.
A provenance annex that correctly finds three defects in its own sources is evidence of
diligence, not of completeness. Praise the discipline where it is real, then probe anyway: an
honest audit document is the one most likely to be accepted without one.

## Commissioning an independent review — blinding is the part that buys independence

Auditing an inbound claim (above) and *commissioning* a second opinion are different procedures,
and the commissioning one has a single failure mode that makes it worthless while looking rigorous:
the reviewer inherits your framing.

- **Name the mode before you run it.** *Critique mode* — the reviewer sees the conclusion and
  attacks it. *Independent (blind) mode* — the reviewer sees the problem and raw source access,
  never the conclusion and never your evidence selection. Both are legitimate; they are not
  interchangeable. A critique reported as an independent verification is the most expensive kind of
  false confidence available.
- **A blind review needs source access, not your evidence packet.** Handing over a curated evidence
  set transfers your framing, so the reviewer's errors correlate with yours — 2× compute and ≈1×
  information. Give the problem plus the interface to the raw sources and let the reviewer decide
  what matters.
- **Physical separation is not epistemic independence.** Two nodes, two agents, or two model calls
  that share a model family, a retrieval corpus, a doctrine file, or an evidence packet are one
  perspective with two mouths. Ask what the reviewer *shares* with the author, not whether it runs
  on a different box.
- **Require four fields back.** The reviewer's own hypothesis, its confidence, **which evidence it
  found decisive**, and **what evidence would change its mind**. The last two are what make a
  disagreement resolvable; a bare verdict can only be obeyed or ignored.
- **Reconcile on discriminating evidence.** Name the observation that separates the two hypotheses
  and run it. Escalate to the human only when the residual disagreement is values, authority, or
  irreversible risk — escalating a factual question spends the scarcest resource on something
  evidence can settle.
- **Do not wait indefinitely on a peer's round.** Two correct and courteous agents will each wait
  for the other's message and neither will move — a deadlock with no crash and no error message.
  Put a timeout on waiting; on expiry treat it as a synchronization fault (re-send, or proceed
  explicitly and say so), never as agreement and never as disagreement.
- **Preserve the reviewer's ignorance.** A reviewer with no access to your memory, doctrine, or
  history is the most independent participant available, and the temptation is to "improve" it by
  supplying context. That trade gives away precisely the property it was commissioned for.
- **Sign the review with a session-unique id.** Where several sessions of one agent can run
  concurrently, `Actor: <agent>` does not identify the writer — two differently-labelled records can
  share one author, and a verdict from the second is then not an independent witness of the first.
  Put the session id, and where it applies the source message id, in the artifact. The same applies
  to any artifact you receive: an unsigned writer means the label is all you have.
- **Track the smallest shared state in the transport you already have.** `objective · round · last
  peer message id each side has acknowledged · owner of the next action`. Message ids usually
  already exist in the channel, and each side's ack is simply the highest peer id it has received
  and processed. No new service is required, and it is deleted by deleting it.
- **The cheapest method beats both, where it is available.** If the claim is about the reviewer's own
  resources and the author can measure it directly, measurement is faster and cheaper than any
  second opinion. The blind lane earns its cost only where self-check is *structurally* blind —
  your own config resolution, a sunk-cost conclusion, or a cross-machine claim you cannot observe
  from where you sit.

## § Pitfalls

- **A detector must not treat an absent field as a failing value.** When you encode the audit as a
  script, condition on *explicit* bad values, never on falsiness. Treating `authority: ""` as
  observe-only manufactured two dozen false VOID findings in one pass — an absent field is UNKNOWN, and
  a detector that fires on absence converts a clean surface into a fabrication with your name on it.
  Same rule for missing keys vs. zero values: `0` may be a measurement, absent is not.
- **Re-run the detector after the first run and read its own output critically.** A finding count that
  moves when you fix the tool (not the data) was a tool artifact. Report the corrected count and the
  reason it moved, or the audit's headline number is wrong in the flattering direction.
- **Symlinked scan surfaces double-count.** Several sibling paths that all `readlink -f` to one
  store make a recursive scan report the same files 2–3×. Dedupe by `realpath` before quoting any
  count or duplicate-name figure, and label which number is unique. Duplicate-name lists built
  without dedupe are mostly symlink repetition — expect the number to collapse by an order of
  magnitude once deduped.
- **A queue of N items may be ONE finding replicated N times.** Before reporting depth or
  escalating, dedupe on the producer's semantic key (tool/trigger/proposed-action) and compare the
  recurrence counter *inside* the payload across copies. If the counter climbs across copies (5 →
  54), the producer appends instead of incrementing: the depth is a duplication artefact, not N
  decisions. Report the de-duplicated count plus the recurrence, and fix the producer — pruning the
  queue treats the symptom.
- **Severity inversion is the default.** An audit's "Critical/High" column is written by an agent that probed the wrong surface. Re-rank by YOUR substance probe, never by the audit's labels.
- **Don't double-fix sibling work.** Multiple agents may run the same audit in parallel; a "N/M closed" score is meaningless when most items are false
 positives. Check for concurrent edits before fixing — and re-check the artefact's `mtime` before
 publishing, because a sibling lane can land the fix between your probe and your verdict.
- **"Not configured" ≠ "broken".** A channel/plugin reported "not configured" may just lack a required field the audit never tested (e.g. an A2A channel serves its agent card only after a peer is added with `peer-name` + `peer-token` — not after `enabled: true` alone).
- **A cited "verified SHA <prefix> <date>" is usually HEAD, not the file it names.** Peer drafts pair `git rev-parse --short HEAD` with a date that matches no commit. Verify before trusting: `git -C <repo> log -1 --format='%h %ci' -- <file>` (the file's actual last commit) vs `git -C <repo> show -s --format='%h %ci' <sha>` (what that SHA really is). SHA and date must co-locate on the SAME commit; a prefix that resolves to HEAD married to an invented date is fabricated verification, not a citation.
- **Filename search is a false negative for nested modules.** `search_files target=files` returns 0 for a module like `ShortTermMemory.ts` because it lives under `src/application/memory/`; a `target=content` search finds the class/export name inside the file. Never declare "module X doesn't exist" from a filename scan — confirm with a content search first, or you report a fabricated gap the codebase never had.
