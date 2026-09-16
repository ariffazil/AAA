---
name: claim-level-verification
description: Use before stating system state from a partial probe.
---

# Claim-Level Verification

The failure is not only inventing a thing. It is asserting a **quantity, scope, or
mechanism** measured at a coarser level than the claim. Verify at the level asserted, or
downgrade the claim.

State the level you actually measured before the conclusion. "Observed at node level" is a
complete claim; "federation-wide" requires federation-wide evidence.

## Probe table — match the probe to the claim

| Claim shape | Tempting wrong evidence | Probe at the claimed level |
|---|---|---|
| "X is gone / down" | absence in one listing | `ps` + `systemctl` + cross-node check; qualify with host |
| "N GB reclaimable" | directory size | the tool's **reclaimable** column; exclude model weights and named data volumes |
| "key A is read from B" | the schema you expect | read the source: `grep -nE "getenv\|extra.get"`; cite file:line |
| "service is healthy" | unit reports `active` | the health endpoint **body** — `active` plus degraded subsystems is RUNNING-BUT-DEGRADED |
| "port is a ghost / false positive" | one snapshot | `ss -tlnp`, resolve the owning process, re-probe |
| "agent X reported Y" | X's self-report | reproduce independently — a peer summary is a claim, not evidence |
| "only N of M surfaces are exposed" | the largest count in the payload | read the payload's own semantics/`design_note` field first — a registry total that includes aliases, mirrors, or diagnostic entries exceeds the operational surface **by construction**; a report that uses the biggest number as its denominator manufactures a gap that was never there |
| "organ Z lives on port P" | a document, a peer report, or prior context | `/health` on that port, and pair the identity field with the tool-name prefix — port folklore propagates between documents; the prefix does not lie |
| "the job / batch migration succeeded" | the process exit code | the artifact: reconcile every row against the source of truth; a pipeline's status belongs to its last stage, so `job \| tail` reports `tail`'s status and a crash at 40% reads as clean success |
| "all N items were handled" | the count that went in | re-count what came out and match element-by-element (hash multiset, row-by-row resolve) |
| "commit X does not exist / path Y is missing / service Z is down" (from a peer) | the peer's report | a node lock on **both** sides first — `hostname` + tailscale IP + the same commit/path probe on each host; a peer's negative finding describes *their* node, and on a multi-clone host even their own runtime can differ from their checkout |
| "these sources contradict each other" | one occurrence of the value, or one file | grep the whole tree and count occurrences plus check sibling modules first: a value appearing **once** as free text is an orphan string, not a split; the same codebase may hold the correct value one module away |
| "the tool exists" / "the code is written" (a document's or a peer's claim of capability) | the function, class, or file it names | locate an executable entry point **and the input it requires**. A dataclass field holding a sentinel (`PENDING`, `None`, `False`) plus a prose note is not a tool; a real invoker takes observations, not a promise. Capability present ≠ input present — probe the data condition separately |
| "the pipeline can produce X" | the engine existing | trace what feeds it. An engine that accepts pre-computed values has no loader for the raw data — the capability is real and the run is impossible until someone supplies input. Report the two as separate facts |
| "consumer X is wired to Y" | one config file, or a green health endpoint | grep for **every** variable name that resolves Y, and for the old value as a hardcoded **default** (`grep -rn "getenv(" | grep -i "<old-value>"`) — one subsystem can read the same endpoint from several unrelated vars in different code paths, and a defaulted fallback appears in no config file at all. Green on the health path proves only the health path |
| "X does not exist / is unmanaged / is not configured" | a lookup under the name you expected | enumerate the real namespace first (`systemctl list-units --all \| grep <fragment>`, `ls <dir> \| grep`), then re-test. Names are conventions, not contracts (`kabarkan` vs `kabarkan-health`), and a null result from a *guessed* name supports no finding at all |

## Rules

1. **Never quote an aggregate without per-item verification.** A total is a claim about
   every component; one unchecked component voids it. Name the components you excluded and
   why (re-download cost, live data, etc.).
2. **Before declaring a capability "down", run the inventory sweep and an alternate-lane
   test.** Ignorance of an idle or paid resource is not evidence of absence.
3. **Unit-level checks do not answer health-level questions.** `active` and `degraded` can
   be simultaneously true; read the status body, not just the supervisor state.
4. **A peer agent's audit is a claim, not evidence.** Reproduce the specific number or path
   before repeating it — agreement between two agents on a wrong figure is still wrong.
5. **Widening scope requires reading the source.** Config keys, env var names, and defaults
   are claims about code. Cite file:line before writing an enablement packet or config change.
6. **A fix found already in place is still a finding.** Verify the mechanism, not the
   outcome: the same symptom has multiple causes and "it works now" does not tell you which.
7. **When a claim is falsified, name the missing measurement.** Owning the error without
   stating which probe was skipped repeats the same error next session.
8. **A process status is not an outcome claim.** When a job's purpose is to transform N items,
   its success is a claim about all N — verify the artifact against the source of truth, never
   the exit code alone. Two mechanisms make the status actively misleading: a pipeline's exit
   status belongs to its **last** command (`job | tail` reports `tail`), and a signal-terminated
   or OOM-killed worker can still leave the parent reporting 0. Redirect to a log and scan it for
   a traceback; treat "no output because I truncated it" as unverified, not as success.
9. **A summary you produced by filtering is a claim about the filter.** Reporting the head, the
   tail, or the first page of a result is fine if you say so; presenting it as the whole is not.
   State the reduction: "first 25 of 312", not "here are the results". The same applies to a view
   you did not know was reduced: before asserting something is MISSING, check that your read was
   complete — count what you received against a total the source declares. A truncated dump, a
   capped list, and a default page size all produce confident absence claims that are false.
10. **A gap claim inherits the denominator's validity.** "N of M are exposed / wired / covered" is
   only as sound as M. When M comes from a registry, catalogue, or alias-inflated total, verify M
   against the operational surface before repeating the ratio — and when the same payload carries
   a self-describing semantics note, that note is the authority on what M counts.
11. **Audit what the source omitted, not only what it asserted.** The highest-value finding in an
   external review is usually a field it never mentioned. Probe the same payload for negative and
   degraded fields (unreachable providers, low signal scores, `degraded`/`disabled` subsystems,
   `enabled` but zero-count ledgers, gated states) and report those separately from the scorecard
   of its claims.
12. **A peer's negative finding is node-scoped until both node locks match.** "Not found",
   "does not exist", and "does not respond" measure the machine the peer ran on. Before
   retracting your own finding or disputing theirs, collect the same identity + path + commit
   evidence from both hosts and compare. Two agents can be simultaneously right about two
   different machines — and when that happens the disagreement is usually worth more than
   either claim. Corollary: a peer citing an *older* commit does not invalidate their
   file-level verification — check whether the file moved between their commit and yours
   (`git diff --quiet A B -- path`) before assuming their reading is stale.
13. **Call it a contradiction only after counting its occurrences.** Before asserting that
   sources disagree, grep the tree for the value and record how many places hold it and in what
   form. A single unsourced string in a free-text note is an orphan, not a three-way split;
   claiming a multi-source contradiction from one orphan overstates the defect and sends the
   fix to the wrong owner (document vs code vs ledger). Check sibling modules in the same
   codebase before concluding the codebase disagrees with an external document.

14. **Your own record inherits the audited source's defects.** When you write findings, claims, or
   a ledger entry derived from a document under review, that document's unsourced and contested
   values enter your record looking like your own verified facts. Before declaring the record
   done, re-read what you actually wrote and tag every number by its real provenance — and never
   import a value you have just shown to be unsourced. The failure is quiet: the write succeeds,
   the file parses, and the defect now carries your authority instead of the original author's.
   Reading back your own artifact is the probe; nothing else catches this, because you already
   believe the thing you wrote.
   *Corollary — keep the diff legible.* When adding to an existing hand-formatted store, append in
   the store's own serialization idiom instead of re-dumping the parsed structure: re-serializing
   reformats untouched entries, and a diff full of formatting noise hides whether you also deleted
   something real. Verify with `git diff --numstat` **plus** a parse-compare of the pre-existing
   entries, and report the pair — "164 insertions, 0 deletions, originals identical" is a receipt;
   "file updated" is not.
15. **Your instrument is a claim.** An audit script, health check, or diff tool that has never been
   shown to detect a known fault has an unmeasured false-negative rate, and its clean verdict is
   worth nothing until calibrated. Before trusting "no drift / 0 problems / all green", run it
   against a case you already verified by hand, or introduce a deliberate fault and confirm it
   fires. A **uniform** result across every subject is a property of the instrument, not a finding
   about the subjects: this session's own audit reported a false `PARTIAL` for all seven agents at
   once (a `307` redirect parsed as DOWN) and a false `ABSENT` (case-sensitive name match) before
   either was caught. Corollary: before reporting a fault, run the probe a second time and confirm
   the *name* you are querying is the one that exists — one command separated a real finding from a
   false risk report about a service that was healthy and self-healing throughout.

   Two further mechanisms produce a *confident* reading from an instrument that cannot fail:
   **(a) output you suppressed is output you cannot count.** A counter run under a tool's quiet
   flag counts zero occurrences of the very text it is looking for, then reports that zero as a
   measured property of the subject — a silenced detector does not report "nothing found", it
   reports the wrong condition as fact. Never pass a quiet/suppress flag to a command whose
   output you intend to parse. **(b) A sample chosen for convenience is not a sample.** A probe
   pointed at the single best-known case (the most-cached item on a platform, the healthiest
   node) returns a permanent green while every ordinary case fails, and that green is worse than
   no probe because it teaches you to trust the lane. Probe representative inputs and report a
   **rate**, not a verdict. Corollary: cap the probe's timeout at what the check actually needs —
   a health check that takes minutes is one nobody runs.

   **(c) A uniform value written by a mechanical pass is a property of the loop, not a
   classification of its subjects.** When something claims to have aligned, stamped, or migrated
   N artifacts by adding a field (capability, lane, tier, owner, role), histogram that field
   before believing the pass: one dominant value across most artifacts means the mapping was
   written by hand for a handful and defaulted for the rest. Then contradict the stamp with each
   artifact's *own* declared fields — an object stating `authority: DISPLAY_ONLY`,
   `max_action_class: OBSERVE`, and receiving `capability: BUILD` refutes itself with no external
   probe, and a self-refuting stamp is worse than a missing one when the artifact in question is
   the node that speaks to a human. Also confirm the edit did nothing beyond what it claimed:
   `git -C <repo> diff -- <one file> | grep -c '^@@'` — one hunk means the claimed change is the
   only change.

16. **The file that should configure it is not the process that runs it.** Layered configuration
   resolves by precedence, not by what you edited: in systemd an `EnvironmentFile` is read *after*
   `Environment=` directives, so a drop-in setting the right value can be silently overridden while
   `systemctl cat` shows your edit. Verify against the live process, never the file —
   `pid=$(systemctl show <svc> -p MainPID --value); tr '\0' '\n' < /proc/$pid/environ | grep <VAR>`
   — and fix at the source of truth, checking first whether a timer regenerates the file you
   changed.

17. **A claim set cannot be ratified while it contradicts itself.** Between *labelled* and
   *ratified* sits a step that is machine work: confirming the set is internally consistent.
   Labelling is not resolution — a body of work whose every claim carries an honest evidence class
   can still rest on a store holding three different values for the same event, or on a chronology
   that omits the very event it headlines. The gap from labelled to ratified is human authority;
   the gap from labelled to *self-consistent* is not, and nothing should cross the first until the
   second closes. When asked to ratify, sweep the substrate for self-contradiction first and state
   plainly which step is still outstanding.

18. **An error message names a symptom; its causal clause is a guess.** Tool errors routinely
   carry a *diagnosis* that is only one of several conditions producing the same string. One
   example: the downloader reports `Your IP address is blocked from accessing this post` for both
   a genuinely blocked address **and** an item that is deleted, private, or region-locked — same
   message, unrelated causes. Trusting that causal clause made me declare a working platform
   blocked, write the conclusion into a skill, and abandon the lane; it worked on the first live
   item tried. Before concluding anything from an error's stated cause, find a probe that
   **discriminates** between its candidate conditions (for that case a metadata endpoint:
   `200` = live, `400` = the item itself is gone). Never carry a tool's causal claim into a
   document or a report as your own finding — quote the message as the symptom it is.

19. **A parse is not a lookup.** A body that deserializes successfully is not evidence that the
   thing was found: an API can answer a failed request with a valid JSON error object and a `4xx`
   status, so the parse succeeds and a truthy result reads as "present". An availability check
   written that way reported a deleted item as live, and looked correct; it was caught only by
   running it against a case already known to be dead. Branch on the **transport status** and treat
   an empty, sentinel, or all-blank payload as failure *even on 200*. The general form: when a
   probe returns both a status and a body, the body answers "could I read it" and the status
   answers "was there anything to read" — you need both.

20. **A mutation invalidates an attestation — rank the damage before calling it a breach, and never
   silently revert a peer's signed artifact.** Adding a field to an artifact that carries a detached
   signature or a receipt hash changes the signed payload, so every such attestation now describes
   bytes that no longer exist. Two probes decide what that costs: does anything *verify* it at
   runtime (`grep -rn '"signatures"\|verificationMethod' <repo> <kernel>` — no consumer means
   audit-honesty is damaged and availability is not, and the two must be stated separately), and
   can it be *re-signed* (signers commonly take the key from offline media; if it is absent,
   re-signing is impossible now, so it is not an option you may offer). Report the honest paths —
   revert so the attestations become true again, or keep the change and re-sign once the key is
   present — with a recommendation, and act only on his word. Quietly reverting someone else's
   signed artifacts is itself an unauthorized mutation; describing a system as "aligned" while
   false attestations stand is worse than either.

21. **A claim repeated is not a claim re-measured — evidence expires.** Process state, open ports,
   counts, queue depths, health bodies, registry `routable`/`drift` stamps and bytes on disk all age.
   Before re-asserting a figure that you, a peer, or an earlier session already stated, either re-run
   the probe or carry it as `UNPROVEN`; agreement between two recitals of one unchallenged claim is
   one observation, not two. When a fresh measurement contradicts the old claim, the correction goes
   into the record **by name** — `RETRACTED — <old claim>, superseded by <probe + value>` — and not
   as a quietly different number further down. Three habits hide the failure: repeating a figure
   because the thread already contains it; re-deriving it from a document that derived it from the
   original; and borrowing the earlier version's evidence class for the new recital. Stale negatives
   and stale positives are equally wrong — a cached `routable: false` while the surface answers a
   live call is the same defect as a phantom "healthy", and a registry flag is a claim about a
   measurement somebody else ran.

## Why this exists

Fluent, complete-feeling output is most dangerous exactly when it feels finished. That ease
is a warning sign, not validation — the machine has matched the expected shape, which is the
condition under which scrutiny is most suppressed. Present evidence before synthesis, and
treat "this report feels complete" as a prompt to go looking for the unmeasured level.

## Related

Bundled sibling for *existence* claims: the fabrication-prevention protocol (claim → external
check → verdict). This skill extends that to quantity, scope, and mechanism.

`references/diagnostic-failure-modes.md` — the taxonomy behind rules 15, 18, and 19, plus the
recipe for **building** a health check that can actually fail. Read it before trusting the first
green run of any probe, monitor, or audit script you write.
