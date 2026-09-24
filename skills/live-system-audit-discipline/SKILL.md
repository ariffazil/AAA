---
name: live-system-audit-discipline
description: "Use when auditing a live system or reporting probe results, and when writing or reviewing a readiness / status cockpit across many surfaces. Forces evidence-class labelling on every line and the denominator beside every count. Covers raw-probe discipline, closure vocabulary, sensitive-path inventory, agent self-seal detection, and the symmetry law between artifact creation and verification."
version: 1.1.0
license: MIT
capability_tier: fed-long-context
ecology_state: WARM
---

# live-system-audit-discipline

> Auditing a system that is running while you investigate it. The characteristic failure is not
> missing evidence — it is stating more than the probe supports. Report the surface, the method,
> and the coverage; scope the claim to what you actually read.

## A live probe has a TTL — stamp it, and re-probe before repeating the finding

**A measurement of a live service expires.** Another seat can deploy and restart inside the
window between your probe and your report, and a finding true when taken becomes false before it
is read — with no error on any surface.

Measured 2026-09-20: `arif_init` was probed at 18:14 and 18:20 and found to build four INIT v2
roots but deliver none to the MCP envelope (1 of 4 reached the payload). A report was written at
18:20. Two commits landed at **18:24 and 18:26**, the venv was written at 18:29:57, and the kernel
restarted at **18:30:03**. Re-probed at 18:41: all four roots present, all three verbosity modes.
The report was stale **21 minutes after it was written**, its lead finding closed by someone else.

Rules that follow:

1. **Every probe result carries `{measured_at, service_start_time, source_sha, deployed_sha}`.**
   `service_start_time` is what makes staleness visible: if the process restarted after your probe,
   your finding describes a build that no longer runs.
2. **Re-probe immediately before publishing, not only before believing**, and record BOTH stamps —
   `measured_at` and `reverified_at` — so a reader can see the age.
3. **A stale finding is not a wrong finding — record it as superseded, never retract it.**
   "True when measured, closed by commit X at time T" keeps the causal record; deleting it erases
   the evidence that the measurement ever mattered. Closure language is precise: the available
   statuses are `mitigated_not_root_caused`, `operationally_stable_not_root_caused`,
   `superseded_by_<receipt>`, `partially_characterized`, `unknown`, or `closed`. The status
   `closed` is reserved for a finding whose root cause has been reproduced, patched, and
   verified — never as a polite closer over unfinished work. An incident whose root cause is
   not yet reproduced stays at `mitigated_not_root_caused` with a daylight test named; calling
   it `closed` is the audit reporting the operator's desired state, not the live one.
4. **A commit landing mid-audit is the loop working, not an error.** Check `git log` timestamps
   against your own probe timestamps before writing "still broken".
5. **The fix for the defect you are diagnosing may already be committed and simply not deployed.**
   Take the deployed SHA out of the payload and diff it against the repo HEAD —
   `git -C <repo> log --oneline <deployed_sha>..HEAD` — before concluding anything is unfixed. A fix
   sitting one or two commits ahead of the deployment is indistinguishable from a fix that does not
   exist, and the pending commit messages frequently name the exact defect in front of you.
   Measured shape: a seal gate refused every call with an identity-mismatch reason, reported twice
   as an authority failure; the repo HEAD carried `<fix>: case-insensitive actor comparison`, one
   file, +7/−3, never shipped. Once it deployed, the same call returned a clean floor list. The
   diagnosis "the authority layer is broken" was wrong; "an undeployed fix" was right.
   Corollary for the reporter: when an external report cites two SHAs as divergent, read the
   commits *between* them — the gap is often the fix, and saying only "they differ" buries it.
6. **A service that is `active` is not a loop that works.** A long uptime with an error on every
   tick is worse than a crash-loop: nothing alerts, and the fixed interval makes it look scheduled.
   Read the journal's error count across the whole run, not `is-active`, and treat
   "active (running) since <old date>" as the trigger to open the log rather than as evidence of
   health. Measured shape: a trigger daemon up for 16 days had logged an HTTP 404 on every
   5-minute tick and had never once fired — and the dead source path was shadowing two further
   defects beneath it that only became visible after the path was fixed.

**Corollary — `verbosity` is a surface, and surfaces disagree.** The same call returned a field in
`minimal` and omitted it in `full` mid-deploy: the projection keep-lists had been patched while the
values were still missing upstream, so **the more verbose mode was the less complete one**. Never
conclude "the field does not exist" from a single verbosity level — probe every level, and treat a
difference between them as a finding in its own right.

## Every claim carries its method

A denominator without a method is not evidence. `0/1338` is three different claims depending on
how it was produced: every line scanned, a handful parsed, or a sample. State the method AND the
coverage alongside the figure — "full scan, exact marker" is a different object from "9 parsed".

A precise-looking number that cannot say how it was obtained is an unattributed claim wearing an
evidence costume.

**A claim that returns unchanged after correction was never a measurement.** When the same figures
and the same findings reappear in a later artifact in the same wording, after you have shown them
false against the live system, stop re-falsifying them. The paste is template text, and the finding
worth recording is that the artifact is not connected to a measurement at all. Say that once and
move on — running the same disproof a third time spends sovereign attention without changing the
record, and the repeat count is itself the signal.

**Two instances are not a pattern, and a peer agreement is not corroboration.** Naming a class
of defect requires n>=3 from independent sources, AND the mechanism must be the same across
each. Two findings on different mechanisms (one tool classified wrong by source, another tool
classified right by source) read as a single observation per tool — not as a defect class. Two
agents reaching the same confident wrong conclusion is worse than one, because it presents as
corroboration and bypasses the falsifier that a single-agent claim would have triggered. When a
peer retracts, retract your own amplifications of their retracted claim in the same thread, not
two messages later — and check whether you added a label that they never used, then propagated
the label as if it were their finding. A peer who says "gate has teeth" and you turn that into
"fail-closed system" have produced a finding that neither of you verified together.

**Decompose before you build on a figure, not just before you publish it.** A count inherited
from another writer carries their undecomposed denominator into your conclusion. Split it into
parts first — a large total often collapses to almost nothing once one contaminated source is
separated out. Do not propose a rule or invariant on an inherited denominator you have not
broken open yourself.

### Trace a governed number to its inputs before trusting its label

**A scalar labelled `MEASURED` may be a constant.** When a number gates a decision — a floor, a
threshold, a score — read the expression that produces it and resolve every input to a source. A
placeholder that survives to a surface is worse than a missing value: it moves the system across
its own threshold silently, and permanently.

Measured shape: a tri-witness score computed as `∛(human × ai × earth)` where all three inputs
were literals in the function body — `0.42` (a `_DEFAULTS` fallback), `0.99`, and `0.99` (a boolean
on container liveness wearing a number). Reported `"status": "MEASURED"`, fixed at `0.7439`, against
a constitutional floor of `0.75`. The system sat permanently 0.006 below its own gate and could not
move, because two inputs were constants and the third was a boolean.

Rules that follow:

1. **Resolve every input of a governing expression.** If any input is a literal, a `_DEFAULT`, or a
   ternary on a boolean, the output is not a measurement. Say so, and name which input.
2. **Two surfaces computing one scalar from different constants is the finding.** The disagreement
   is not between witnesses; it is between fabrications. Enumerate each surface's constant set and
   compute each result — an exact match to a reported figure identifies the source beyond argument
   (`∛(0.95×0.94×0.93) = 0.9400` matched another connector's `0.94`).
3. **Check where each variant sits relative to the governing threshold.** Three constant sets in one
   system landed on three sides of the same floor — below, below, above — so the same machine
   reported itself as simultaneously failing and passing the same gate.
4. **An honest `None` that never surfaces loses to an inflated proxy that does.** When one
   implementation declines to measure and another invents, the invented one is what ships — and the
   honest one is typically the one with a comment saying it must never be inflated. Align the
   surfacing path to the honest implementation; do not build a new meter.
5. **A scalar that cannot move cannot govern.** If its inputs are fixed, no evidence can change the
   verdict, so every promotion or learning gate keyed to it is inert. That is a root cause for a
   downstream loop that never fires — not a reason to look harder at the loop.

## A causal mechanism is a claim — reproduce the records before you publish it

"It deadlocks because X" is an inference and carries the burden of any other claim. A plausible
mechanism that has not been made to reproduce the observed records is a **hypothesis**, and must be
labelled one. The characteristic failure here is not a wrong mechanism — it is a mechanism reported
with the confidence of a measurement.

**Two steps, and both are required.**

1. **Fit the record.** Encode the mechanism as arithmetic and run it across every observed entry.
   Measured shape: a scheduled job's phase selection was reproduced by `elapsed // 3600` against the
   real timestamps, matching **5 of 5** log lines — including the runs that fired a second early or
   late, and the band boundaries. State the score in the finding. A model that reproduces the set it
   was derived from is a *fit*; saying so is what keeps it honest.
2. **Then probe the margin — that is the real test.** Vary the input across the decision boundary and
   show the outcome flips: `−1s → window A · 0s → window B · +1s → window B`. A mechanism that only
   explains the cases you started from has not been tested. This is what reveals the margin is one
   second wide, and therefore why the failure is intermittent and went unnoticed — a finding far more
   useful to the owner than the mechanism alone.

**Quote the margin, not just the mechanism.** "One second of jitter decides whether the phase runs"
is falsifiable and tells the owner exactly how much slack to add. "The scheduler is unreliable" is
not — it names no threshold and admits no verification.

**Corollary — publish the falsifier, not the verdict.** When several mechanisms fit the same record,
name the observation that would separate them. A hypothesis that predicts a case you have not yet
measured outranks one that merely fits the cases you have.

## Absence carries the same warrant as presence

"No drift found", "not in the registry", "no caller exists" are claims, not defaults. Each
states where you looked, on which host, and by which method.

- **Host-pin existence claims.** A miss on one node is not a global absence when the same
  logical name resolves to a different store elsewhere. Find which path the consumer actually
  reads before concluding anything about "the" store.
- **Diff the READER's store against the WRITER's store before claiming a loop does not close.**
  "There is no verification" is an absence claim, and the usual cause is not a missing verifier —
  it is a verifier reading a ledger nothing writes while the producer fills a different one. Print
  the id set of every candidate store and intersect them: an overlap of zero means the loop is
  diligent and blind — both sides healthy in isolation, and every receipt it exists to collect
  arriving unwitnessed. Measured shape: a daily verifier with a working timer read 12 rows, the
  generators wrote 20, and the two sets shared not one id — the overdue rows and the private ones
  among them. Recipe and the safe merge: `references/live-probe-discipline.md`.
- **A skip that is caught and discarded is a silent absence.** A row loop guarded by a bare
  `except: pass` reports truthfully about a set it never fully considered: a key-name difference
  (`state` vs `status`) raises, the exception is swallowed, and the tool prints "0 due" while
  holding rows past their date. Record the row as unparseable instead of dropping it, and read
  "0 due" as a measurement of the rows the tool LOADED — never as a fact about the world.
- **Prove the tool is looking at the row in front of you before theorising about why it skipped
  it.** When an overdue row sits beside a tool that reports nothing due, loading the tool's own
  input and printing the ids settles it in one call. The expensive wrong turn is the plausible
  mechanism — a stale field, a malformed date — which yields a confident diagnosis about a row the
  tool never read. Same defect class as the disjointness bullet above; rule it out first.
- **An incomplete protocol handshake is not a capability defect.** A server returning
  `SESSION_MISSING`, `Missing session ID`, or `rejected until client sends <lifecycle step>` is
  behaving correctly — you skipped a required step. Complete the full lifecycle before writing
  anything about the contract: send `initialize`, **capture the session id from the response
  HEADER** (not from a tool parameter — that is why no schema field appears to be missing), send the
  initialized notification, then retry the call. Measured shape: three organs were reported as broken
  contracts across two correction rounds — *"the session requirement cannot be satisfied through
  this surface"*, *"the runtime guard rejects it as noncanonical"*, *"the advertised tool returns
  Unknown tool"*. All three worked once the handshake was completed; the third was a name error, and
  the advertised name had never existed. **Read the advertised list before calling a tool** — an
  unknown-tool error means your name is wrong, not that the tool is missing. Every one of the three
  false findings had already been promoted to a remediation item, and two proposed fixing contracts
  that worked.
- **Never widen a single-surface probe into a claim about the system.** One endpoint, one
  client, or one output mode is a midpoint, not the organ. Probe a second surface, or scope the
  claim in the sentence itself.
- **When a gate denies your probe, that IS the finding — do not substitute a source read.**
  A stateless-client denied at L1 has produced one observation: L1 denies stateless-client.
  It has NOT produced: "the gate is fail-closed overall", "the gate denies all unverified callers",
  or any class-level claim about the system. If your next move is to read source code or another
  tool's audit log to "fill in" what the gate denied, you are inferring past your evidence. State
  the denial, name the tool/mode/actor, hand off to whoever holds the verified session — and stop.
  Reading the source gives you the developer's INTENT, not the runtime behavior. The two can
  diverge (compiled classifier, dead flag, fail-open fall-back) and the only thing that resolves
  the divergence is a live probe by an actor that the gate does not deny.
- **An echo is not a measurement.** Before reporting a value as the system's, vary the
  parameter you sent and confirm the answer changes with it; some endpoints return what the
  caller supplied, so a fixed probe measures only itself.
- **Reproduce a surprising zero with a second, differently-shaped command before publishing it.**
  A false zero from *command shape* is indistinguishable from a true zero, and it is the figure that
  flips a verdict — you will report a defect that is not there, or clear one that is. The classic
  shape is an unparenthesised alternation, where the implicit `-print` does not bind the same way
  across implementations:

  ```bash
  # suspect: the implicit -print may attach to the last term only
  find <dirA> <dirB> -name '*.x' -o -name '*.x.*'
  # robust: wrap the alternation, then confirm the count a second way
  find <dirA> <dirB> \( -name '*.x' -o -name '*.x.*' \) -print
  ls <dir> | grep -cE '\.x(\.|$)'
  ```

  The rule is not "find is broken" but "one form is one witness": a zero that cannot be reproduced two
  ways is a measurement of your own command, not of absence. Cheap to check, and it is exactly the
  class of error that survives into a published finding because a zero looks like a clean result.

  **Second shape: a size tool's zero on a path that resolves through a symlink.** A directory reached
  by a symlink can report `0` bytes while holding gigabytes at its target — and because `0` reads as
  "empty, safe to remove", that error lands straight in a deletion list. Check `ls -la` and
  `readlink` (or `findmnt -T`) before any size tool is believed: an `l` in the mode column means you
  measured the link, not the tree. Then re-measure the resolved target. Two silent variants:
  a link whose target is already counted elsewhere (removing the link frees nothing) and a link whose
  target is a live store (removing the *target* destroys what the link was only naming). A path that
  appears both as a top-level entry and inside another tree is the tell — resolve it before ranking it.
- **Scope a negative to the window you actually searched.** "Never used", "never fired", "no caller"
  read as properties of the system and are usually properties of the retained log. State the first and
  last retained timestamps beside the count, and derive any ratio against that window rather than an
  assumed lifetime.
- **Re-verify immediately before you write.** On a live shared repo another writer may land
  between your read and your patch. Re-check mtime/hash at write time.
- **One ID per identity, never two namespaces for the same object.** A standing pattern in this
  codebase is minting parallel identifiers for the same artifact with two prefixes (e.g.
  `az-<sha8>` for signal identity, `azc-<YYYYMMDD>-<NN>` for the calibration audit of the same
  signal) and asking downstream consumers to reconcile the two via `seq` mapping or sidecar
  joins. The reconciliation always fails somewhere, and the failure mode is silent: a join key
  drifts, a foreign reference goes dead, and the audit trail loses a thread. **One ID per
  object.** When a secondary ordering or grouping is needed (ordinal within a day, sequence
  within a render), make it a sidecar field (`seq`, `order`) on the same record — not a parallel
  namespace. The cost of two namespaces is paid forever; the cost of one extra field is paid
  once at query time.
- **A comparator must fail closed on missing inputs.** A drift surface compared
  `source_commit: null` against `built_commit: null`, got "matches", and asserted
  `deployment_attestation: "aligned"` while holding no commit identity whatsoever — the one verdict
  that suppresses further checking. When a surface asserts a comparison, read BOTH operands: if
  either is null or absent the assertion is vacuous. Record that as UNCHECKABLE, never as aligned.
  The same endpoint can still emit a correct `drift: false` elsewhere in the same payload, so a
  machine can hold two contradictory drift answers at once — report both surfaces by path.

## Two surfaces disagreeing is a finding, not a contradiction

When surface A and surface B report different values, the correct output is the divergence
itself. Do not resolve it by picking the one that matches your expectation, and do not assume
one is stale without evidence. Report both, then probe a third to locate the fault.

## Auditing a claimed control — probe the PATH, not the control's own test

A control proves nothing by refusing when you invoke it directly. The question is never "does the
guard deny?" but **"is the guard on any path a real caller takes?"**

When a component is described as a chokepoint / gate / complete mediation, verify by probing every
real invocation path and recording OPEN or CLOSED for each — never by running the component's own
test suite:

- **bare command on PATH** — what a caller actually types; check what it *resolves to*
  (`shutil.which` / `type -a`), not what you installed somewhere else
- **the absolute path** — skips PATH entirely, so a PATH-level shim is decoration
- **a subprocess from another language** (`python3 -c "subprocess.run([...])"`) — skips shell guards
- **the documented bypass** — if the guard keys off an environment variable, set it and see
- **the protected asset itself** — read the credential/secret directly, and if it is encrypted try
  to decrypt it with whatever key you find sitting beside it

Measured shape of a false green: a guard script existed, was correct, and was referenced by NOTHING
except its own test — which invoked the script directly and asserted it refused. The product's own
gateway called the bare binary name and never touched the guard. An env var named like a privilege
(`X_INTERNAL=1`) was the only gate, and any caller could set it. Verdict: *governed wrapper, not a
chokepoint* — a materially different claim from the one made.

Rules that follow:

1. **A test that invokes the control directly is a tautology.** It measures the control, not the
   boundary. If a suite reports "N/N PASS — Complete Mediation enforced" and every case calls the
   guard by its own path, the result is worthless. Rewrite the suite to probe real paths and make it
   exit non-zero when any path is open.
2. **An environment variable is a claim, not a capability.** Privilege must be checked against
   something the caller cannot author — a per-call token from an authority, or a kernel-enforced
   identity — never a flag the caller sets for itself.
3. **The control usually works where it is applied. Find where it is NOT applied.** The recurring
   defect is not a broken guard; it is a correct guard attached to the wrong surface, or to no
   surface. Ask "who actually calls this, and what do they call instead?"

   **Before you call a control NOT WIRED, read its registration surface — not its name.** "Not
   wired" is a wire claim and carries the same burden as "wired". A component is registered under a
   *generic* key that names its **path**, so grepping the config for the component's conceptual name
   returns nothing and looks identical to absence. Enumerate the runtime's extension points by their
   fixed keys (`hooks:`, `pre_tool_call:`, `plugins: enabled:`, `events:`) and read the entries — the
   component's own file need never contain its trigger name. Then grep the registration site for the
   component's **absolute path**, not its label. Corollary: an unexpected refusal, block, or timeout
   from a component you believe is unwired is *positive* evidence it is on the path — your own
   accident is a free wire-probe, so re-read before publishing. Measured shape: a mutation gate
   reported as "looks unwired" after a name-grep of one directory; the runtime config declared it by
   absolute path under `pre_tool_call` with `fail_closed: true`, and it had already fired earlier in
   the same session. Both false verdicts — *a gate that blocks nothing* and *a gate that is not
   there* — come from the same mistake: reading a label instead of a resolution path.
4. **Encryption beside its own key is not encryption.** A ciphertext and its key in the same readable
   directory is *plaintext with extra steps* — verify by decrypting, not by confirming the file ends
   in `.enc`. Report the credential as EXTRACTABLE, not merely readable; the difference is whether an
   attacker needs the tool at all.
5. **A permission bit is not a boundary when every actor is the same uid.** `chmod 700` separates
   root from non-root and nothing else. If every process involved runs as uid 0, report the boundary
   as absent rather than quoting the mode string as if it protected anything.
6. **A mandatory-access-control profile can bind root — so confine the CALLERS.** Where an LSM
   profile is applied it denies root too. Prove it with a controlled pair (same uid, same file, one
   path covered by the profile and one not → READABLE vs DENIED), then note that the remedy for a
   root-reachable asset is to attach the profile to the processes that pose the threat — not to move
   files to another uid, since root reads any file regardless of ownership, and not necessarily to
   de-root the citizens, which is a far larger change than the finding requires.
7. **Falsifying a claim is a WRITE, not just a report.** Downgrade the artifact that carried it —
   status line, diagram label, and any seal precondition — and leave a correction notice *in* the
   document, so the next reader cannot act on the withdrawn claim. Also fix the test that produced
   the false green, or it will re-certify the same thing tomorrow.
8. **Distinguish a gate that DENIES from a gate that CANNOT PASS.** Read the budget against the
   work. A deliberation gate carrying a 200 ms ceiling while the judge consults a language model
   (`llm_consulted: true`) degrades to HOLD on every attempt: it never decides, so the seal it
   guards is unreachable by construction. Reporting that as "the system refused" credits the system
   with a judgement it never made and hides a configuration defect behind authority language. Sample
   the reason string for a resource bound — timeout, budget, quota, ceiling — and if the bound is
   shorter than the minimum cost of the operation, the finding is *gate unsatisfiable*, owned by
   whoever set the bound, not a policy outcome.
   **Let the work speak: A/B the identical payload through two classifications.** Re-run the same
   candidate under a different tier/class and compare only the timing fields. If the *content* is the
   reason, the verdict repeats; if the *budget* is the reason, the second run completes and the measured
   duration is set by the work rather than by the ceiling. Do not change the payload between the two
   runs — one variable, one comparison. A duration landing exactly on the ceiling is a kill, not a
   completion, and the string it produced is a timeout wearing a verdict's clothes.
   **A caller stricter than the library it calls is the defect.** When the tool resolves an absent or
   unrecognised argument to a *tighter* class than the module it imports resolves the same case to, the
   caller is wrong, not the configuration. Read what the library does with that same input before
   accepting the caller's default.
   **Then make the binding assertable.** A classification constant declared inside a long function
   cannot be imported, diffed or tested — which is how a default drifts below the measured cost of the
   work and stays there. Hoist it to module scope and pin the invariant with a test that fails on the
   old value.
   **Clearing one gate reveals the next.** A blocked verdict is often a CHAIN of independent
   blockers, each fail-closed on its own. Name the gate you cleared and the gate that replaced it;
   do not report the first success as the path being open, and do not report the second gate as the
   first one recurring.
9. **When you write the honest suite, guard against harness bugs in both directions.** Two
   measured, both in the test rather than the system under test: (a) reading the *last line* of a
   shared, concurrently-written ledger attributes another writer's entry to you — inject a unique
   marker and match on it instead; (b) backgrounding a helper in a process-tree test makes it a
   sibling of the call rather than a parent, so an ancestor walk can never pass through it — have
   the helper spawn the call as its own child. Also decode captured output with `errors="replace"`:
   binary payloads raise on strict decode, and that exception is easily swallowed into a
   "not readable" verdict for a file that is fully readable.

**Do not close the gap by wiring the non-functioning guard into place as-is.** A guard that blocks
honest callers while any caller who sets one environment variable passes through is security
theatre, and worse than none: it teaches everyone the boundary exists. Mark it NOT WIRED, state the
measured open paths, and hand the OS-level fix to the owner.

## A readiness cockpit is a class of work — write it under a fixed evidence-class enum, never from topology alone

The cockpit form is its own failure shape, distinct from a one-off live probe. A readiness report is a *summary* across many surfaces, and the recurrent defect is conflating **configured**, **probed**, **structural**, and **inferred** into a single status word — "live", "wired", "running", "enforced", "sealed". The fix is a standing four-class enum on every line, a denominator beside every count, and the discipline that the highest-priority finding is enumerated before any other action runs.

### Procedure

1. **Report every surface under one of these four classes — non-negotiable.**

   | Evidence class | Meaning | Allowed to support |
   |---|---|---|
   | `live_probe` | You called the surface this session, this agent, returned a value | "Healthy / ready / down" claims at the moment of probe |
   | `configuration` | Read from manifest, registry, config, generated list | "Configured" claims only — NOT runtime readiness |
   | `structural` | Counted cycles, holds, formulas, baseline timestamps — telemetry | "Telemetry records X" claims only — NOT enforcement, NOT continuous uptime |
   | `inferred` | Reasoned from absence, from another surface's reading, from package metadata | Nothing on its own — always paired with the reading that produced it |

   Never state a property as if it were the next class up. "Configured 25/29" ≠ "live 25/29" ≠ "enforced 25/29". Each step up the ladder requires its own observation.

2. **Always print the denominator beside the count.** When 13 of 29 surfaces were probed and 4 are intentionally disabled, the cockpit shows **13 / 29 live-probed · 4 disabled-intentional · 12 unprobed**, never "25 / 29 wired" or "25 / 29 healthy". A count without its denominator is an unattributed claim wearing evidence clothes — see "Every claim carries its method" above, this is its cockpit form.

3. **A timestamp from a baseline file is not continuous uptime.** A baseline recorded on 2026-08-06 says "the baseline was established on that date", nothing more. Re-probe the live state with the live tool; the baseline gives provenance for the *reference*, not continuity for the *service*. State the probe date AND the baseline date when both appear, and treat any "9 weeks continuous" claim that derives only from the file mtime as a `structural` claim — not as `live_probe`.

4. **A control-plane finding is the headline, not a numbered item.** When one surface reports a discrepancy that bypasses the governance layer (registry drift against expected surface count, an unusual-public-tool detected, an expected-public-tool absent), the cockpit prioritises that finding above any green-light summary. Green status does not net against red control-plane signals. Surface the drift as P0; resolve or contain before other audit work proceeds. Tempting to bury it because the rest of the system is healthy — that's exactly the failure pattern the cockpit exists to prevent.

5. **"Sealed" applies to artifact integrity only.** The cocktail overcount surfaces it as a separate finding every time:
   - `sha256 verified` is integrity evidence.
   - `receipt persisted` is audit-trail evidence.
   - `governance closure` is the sovereign act — distinct from both.

   Distinguish them in the language; do not merge them into a single word. A cockpit that conflates the three manufactures the false impression that an authority has been exercised when it has only been recorded.

### Pitfalls — both directions

**P1 — collapsing evidence classes.** "F13 enforced" derived from a formula's 5066 cycles and 52,902 holds. Both are `structural` telemetry: the formula records holds, it does not prove it causes them. Holds could be zero-traffic default; cycles could be idle bookkeeping. To assert enforcement requires a `live_probe`: a deliberate A3 negative-control test returning denial-before-side-effect. Without that probe, "enforced" is an inferred claim and the verdict is `structural` (or `inferred`), not "live".

   *Rule:* any readiness claim that uses the words *enforced, running, continuous, sealed, completed, ready, mature, stable* must carry an evidence class explicitly, and the strongest class available is the highest class the claim is allowed to support. "Enforced" requires `live_probe`; "telemetry exists" requires only `structural`. Pick the right one and print it.

**P2 — over-restraint after a P1 correction.** Once a collapsing-defect is named, the reflex can flip to freezing all subsequent work and demanding F13 for things that are bounded A1 reads. Two distinct failure modes, opposite signs: under-claim earlier, over-restraint now.

   *Rule:* when a claim warrants evidence of class X, the fix is not "do nothing", it is "issue the read at the highest safe class". Read-only metadata enumeration against authoritative sources (a registry resource, an `mcp://list-tools`, a generated manifest) is `live_probe` of class `A1`, not class `A3`. The bound between the two is the prohibition on invocation, dynamic discovery, and write-capable inspection — not the read itself. State the prohibition; do not extend it to ban the read.

**P3 — frozen discovery with no escape path.** Rejecting every form of progress until Arif supervises produces an artifact with no path forward — and an audit feed that the operator has to handle at the wrong time of day. The correct move is to *separate* the read-only discovery from the F13-bound action: enumerate at A1, classify, then escalate only the dispositions that require invocation, write-capable inspection, or 888 HOLD. Discovery that needs F13-ratification is rarely the discovery itself; it is the classification or the disposition that follows.

**P4 — control-plane drift buried under green summary.** When the rest of the cockpit reads healthy and there is one finding that hints at a bypass path, the impulse is to enumerate it alongside the others. Do not. The bypass-suspect finding is the headline. Order the artifact so the reader sees it before any "X of Y healthy" line.

**P5 — adjudicate the audit, don't summarise it.** A readiness cockpit summarises the operator's obligations; it does not adjudicate them. State the findings, state the evidence class, state the next step that requires F13 / 888 HOLD — then stop. The sovereign closes; the cockpit reflects.

**P6 — citing an anchor that was never read.** An audit session that asserts a section name, line number, or section content without opening the file in the same turn is fabricating the citation, not reading it. The defect compounds quietly: a confident anchor citation in the audit report moves the reader's attention away from verifying the source, and the wrong patch lands on a real but unrelated section. Always read the file before quoting it; if you cannot read it, say "I have not opened this file in this session" rather than naming a line.

**P7 — silently mutating a count without restating which class it belongs to.** When a number changes shape between two reports (a count of skills, callers, or artifacts), the receiving reader has no way to know whether the new number is a different *class* of object (caller vs referenced skill, distinct regex vs expanded regex, etc.) or the same class with different data. The cheaper defect is silently labelling the new count with the old class name. Always restate the defining predicate of any count you report, and any time the count changes across reports name what changed: the predicate, the sample, or both. Two numbers with the same label and different underlying definitions are not the same metric.

**P8 — overriding a measurement with a reason and labelling the result measured.** When an APEX, score, threshold, or rating is produced from a deterministic expression and a reviewer replaces an input value with a reasoned estimate, the resulting number is a reasoning output, not a measurement — but the surrounding language ("score", "X ≥ 0.80", "PASS") still carries measurement semantics. State the override as an override, name the input that was reasoned, and re-label the output. A score whose inputs are mixed measured-and-reasoned is a reasoned estimate; a measured estimate is a contradiction in terms. The same defect applies to any audit field whose inputs include both measured values and operator judgement.

**P9 — an auditor who violates the rule they are auditing is a SCAR-class event, not a footnote.** When an audit session flags a defect class in a target system and the auditor's own behaviour demonstrates the same defect class during the audit (e.g. flags "do not fabricate" and fabricates a citation, flags "no P override" and overrides a score), the audit's standing evaporates: the artefact being audited is now indistinguishable from the auditor's own output. Treat the violation as a constitutional event: register a SCAR, mark the audit session's findings as `provisional pending independent witness`, and route the next-session verification through a different agent or a verified witness path. A footnote on the audit is the surface symptom; the SCAR is the ledger entry that prevents the next auditor repeating the same shape.

**P10 — an agent that declares itself "SEALED · LIVE · COMPOUND" has not ratified anything.** Capability is not authority. A markdown file declaring `status: ratified`, `status: sealed`, `status: constitutional`, or any of the operative authority verbs inside its own front matter is a **self-claim**, not a ratification — the file is the *author* of the claim, not its witness. The same defect class applies to an agent that registers an entity/mode/lens/identity it just named (e.g. `operating_mode: <newname>`) and treats the registration as governance. Treat the artifact as `RATIFICATION_REFUSED` by default until an independent verifier (typically the human principal whose authority was invoked) issues the ratification event. Companion to "Capability ≠ Authority" canon and to the auto-seal doctrine that distinguishes session sealing (machine) from constitutional sealing (human). The recurring shape of which is clearly: file declares `SEAL`, file's own contents cite the file as the seal authority, file is unread by anyone who would have issued the seal. The fix is to require a separate decision artifact (`decision_ref`, F13 event, ratification receipt) that the file references — not the file referencing itself.

**P11 — a failed probe without wall-time, exit-code, stdout, stderr, and parsed value is a bounded UNKNOWN, not a root cause.** When a probe "fails" (no response, parse error, curl returns non-zero, listener not bound), the disposition is *unknown* until each of the following is recorded beside the failure: the wall-clock time of the probe; the curl/python exit code; the response body or stderr; the elapsed duration; and what the parser did with the output (or that there was no parser hit). "Parsing fails for some reason" is not root cause; it is the unmeasured midpoint that has not yet been resolved. The corrective step is rarely complicated — typically it is a controlled re-probe with each field captured — and is the difference between a finding you can hand to the operator and a finding you have to re-discover when the operator asks "but what actually happened?". For probes that return ambiguous responses (e.g. a JSON object with the expected key missing), the post-condition is to **call again with the same payload** before publishing — the first read after a transport is created is not the steady-state read, and pinning a reference from it is the same defect class.

**P12 — sensitive paths are not a "later feature"; they are part of the inventory layer.** A file census that scans `.ssh/`, `.gnupg/`, `.aws/`, `.config/`, `.cache/`, browser profiles, Telegram/WhatsApp stores, `*.env`, `*credential*`, `*token*`, `*secret*`, `*key*`, `*cookie*` without an explicit F13 scope either indexes confidential material it has no business seeing or generates a "complete" count that masks the legitimate perimeter. Privacy is not a post-processor applied after the count is produced — the exclusion list must be enforced at the inventory entry point, with the excluded set recorded as a *coverage statement*, not as silent skips. When in doubt, the rule is **"index by presence, not by content"**: record `path`, `size`, `mtime`, `sha256` for the excluded paths if scope permits, never the body. If scope does not even permit the metadata, the path does not enter the census and the audit reports what it does not see, with a one-line declaration of the exclusion policy.

### The audit-session symmetry law

`WRITE_CONSTRAINT(x) ⇒ READ_VERIFY_CONSTRAINT(x)`. A rule that governs artifact creation must also govern artifact verification under the same epistemology. If an artifact is required to be deterministic-rendered when written (e.g. text-bearing PDFs route through weasyprint / Chrome headless, not image-gen), the verification step is required to use the same reading primitive (pdftotext layer check), not a lossy alternative (vision inspection of the rendered image). Two sides using different epistemologies make the audit itself a source of corruption: a PASS verdict issued through lossy inspection is observationally indistinguishable from a fabricated green. Enforce this at gate design time, not at audit time — once the gate is built, the auditor's choice is removed.

## A clean report is a claim about the instrument — audit the instrument's own state

A monitor, guard or validator has **state**, and its verdict is computed against that state. When the
state is wrong, the instrument reports clean and nothing anywhere errors. Three ways it happens, all
found by reading the instrument rather than the thing it measures.

- **A reference that does not survive restart grants a silent amnesty.** If the pinned baseline,
  snapshot or fingerprint lives only in memory, the first check after any restart sees nothing to
  compare against, pins whatever is being served at that instant, and returns zero drift. A verdict
  accumulated over weeks evaporates on a restart, and no record says it did. Detect it by reading the
  store class: a `Map` with a comment naming the persistence path is the tell — then check whether
  that path has ever existed (`ls`, plus `git log -- <path>`; a path in a comment is not a file).
  Test it directly: note the current verdict, restart the instrument, and see whether the same
  condition is still reported. **A finding that disappears when the instrument restarts is a finding
  about the instrument.** Corollary: a restart is a free experiment — use it deliberately and record
  the before/after verdict as a measurement, not as a maintenance step.
- **The first read after a transport or session is created is not the steady-state read.** A server
  that builds its registry, transport or schema tree lazily answers the first request from a cold
  state and every later one from a warm state. Measured shape: all 121 tool schema hashes differed
  between the two regimes — the same value set, inverted — so a reference pinned from a cold read
  made every subsequent warm read look like a permanent change. Never pin a reference from the first
  read; re-read before pinning, and before publishing a change re-read once against the SAME
  reference, discarding the finding if the second read agrees with the reference. The corroborating
  evidence is usually already in the service's own log — a line like "transport created on first
  session request" at the exact timestamp of the anomaly.
- **Ask who reads the output before treating the output as evidence.** Grep the box for a consumer of
  the artifact the instrument writes: the service source, the scheduler, the audit tree, the tool
  registry. An output with no reader is not a witness, it is a file — and that finding outranks every
  number the instrument produced. Volume is not significance.

  **Corollary — when every stage can hand work to the next, grade the chain by where work
  TERMINATES.** A pipeline in which each component can pass the artefact onward produces volume, not
  consequence, and nothing errors while it accumulates: receipts written, no reader, no decision
  attached. Ask of each output which decision or human it lands on; work that cannot be attached to a
  cause or a decision is activity, not result. Throughput is never the outcome metric for a system
  whose stages can all forward.

**Verify a change to an instrument on the installed artifact, not on a plan.** Build the harness
against the artifact that will actually run, redirect only its output paths, and assert both
directions: an unchanged input writes nothing, and a changed input writes exactly once. Add a
deliberately unstable source — a fake endpoint that alternates its answer on every call — and assert
it produces zero findings and moves no reference. A fix for a flapping instrument tested only against
a steady one has not been tested.

## A rate needs the whole population, and the population's own shape

- **Quote a census, not a slice, before you quote a percentage.** A sample supports a claim about the
  samples; reading the entire population is usually cheap and is the only thing that supports "100% of
  N". Where a full pass is too expensive, state the fraction examined in the same sentence as the figure.
- **Test for duplicate-ness before reporting duplication.** Grouping records by timestamp and counting
  groups with more than one member measures timestamp collisions, not duplicated content. Hash the
  payloads with volatile fields (timestamps, latencies, durations) stripped and compare — grouping is a
  hypothesis, hashing is the measurement. A file size that differs between two "identical" records is
  the same defect: compare content, not metadata.

  **For directory trees, per-tree `du` double-counts a hardlinked pair.** Two paths with matching
  apparent and on-disk sizes are not two copies when they share inodes — measuring each separately
  reports the tree twice and inflates the reclaim estimate by 2×. Measure them **together**
  (`du -sc <treeA> <treeB> | tail -1`) and compare inode sets
  (`find <tree> -type f -printf '%i\n' | sort | md5sum`) or count files at `-links 1`. Sizes that sum
  to one tree's worth of bytes, with few single-linked files, is a deduplicated pair — designed, not
  accidental, and deleting one "duplicate" frees nothing while removing a recovery path.
- **Extract the properties you will want later BEFORE you purge a population.** Deleting an observed
  pile destroys the ability to measure anything about it afterwards: a rate, a distribution, a
  first-seen date. Record the aggregate statistics and a sorted `name<TAB>size` manifest hash first,
  keep a few samples as live witnesses, and put both paths in the receipt. A purge is irreversible for
  every question not asked before it ran — and the question you end up wanting is usually the one you
  did not have yet.

## Depth

`references/sovereign-verdict-reporting.md` — asked for a flat verdict on his own build: measure
before ranking, split the verdict by layer, name the one non-commodity delta, retract by replacing.


`references/live-probe-discipline.md` — served artifact vs working checkout, same-name-two-stores,
working while others write, independent verification, treating a blocked mutation as a result.

`references/governance-gate-chain-diagnosis.md` — when an authority system refuses an action:
enumerate the gate chain, satisfy it one gate per attempt, classify each blocker as caller error
vs defect vs intentional constraint, and report the gate and its measured margin instead of "it
was blocked."

`references/attention-entropy-audit-recipe.md` — asked for an attention / entropy / chaos audit:
inventory the load and classify it by state, measure each item's attention cost against its reality
impact, apply the parasite test (who reads it · has it ever changed a decision · does it have a
rotation or kill rule), rank most-attention-for-least-reality first, and close on the single removal
that releases the most.

`references/subtractive-cleanup-census.md` — asked to make a live host simpler / smaller / remove
entropy / produce a removal map before deleting: the probe set (port→unit map, enabled-vs-active
units, ExecStart-missing orphans, git-dirt sweep, resource attribution, store census), the eight
disposition buckets, the P0→P8 order, the batch-and-canary rule, the authority boundary that stops an
unverified session, and the false positives that make a "safe to delete" list wrong.

`references/artifact-disposition-vocabulary.md` — the six precise status terms (PRESENT_IN_WORKSPACE,
UNRATIFIED, RATIFICATION_REFUSED, QUARANTINED_REGISTRY_ONLY, CANONICAL, ARCHIVED) and the incident
closure-language set, with the false-claims each prevents. Apply when any artifact's standing
needs to be reported in an audit, manifest, or registry record — and especially when an
artifact's own front matter contains an authority verb about itself.
