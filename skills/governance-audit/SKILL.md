---
name: governance-audit
description: "Use when asking whether a control, gate or safeguard is actually enforced or is only a label. Triggers: is this actually enforced, does this gate work, verify this safeguard, the control is present, privacy filter is on, 0 rejections, gate passed, is this wired up, verify a claimed control, false name, named but not installed, hardcoded metric, is this gate real, does the gate actually block, can this bypass the gate, enforcement coverage, is the guard load-bearing, who actually made this change, audit trail attribution, prevented vs detected, is this control real, auditing whether a control really enforces, auditing whether a named control actually acts, auditing whether a named control actually controls, auditing whether a control actually controls, a named control may not actually enforce, a service claims a control you must verify, verifying a claimed result or sealing a control, auditing an auth/gate control for verification. Surfaces: gates, validators, health checks, sandboxes, seals, drift detectors, shadow modes, authority checks, privacy filters, promotion ladders, approval gates, signatures, scope checks, deny lists, rate limits, authorization tiers, session gates, authority bands, human-approval fields, allow/deny regexes. Mode router — 7 modes: control-integrity, declared-vs-enforced, named-mechanism, enforcement-coverage, seal-verification, proxy, metric-derivation."
version: 2.0.0
owner: Hermes
risk_tier: low
floor_scope: [F1, F2, F4, F9, F11, F13]
autonomy_tier: T1
tags: [audit, governance, control-integrity, false-name, enforcement, bypass, verification, seal, coverage, proxy, metric-derivation]
triggers:
  - "is this actually enforced"
  - "is this control real"
  - "does this gate work"
  - "verify this safeguard"
  - "the control is present"
  - "privacy filter is on"
  - "0 rejections"
  - "gate passed"
  - "is this wired up"
  - "verify a claimed control"
  - "false name"
  - "named but not installed"
  - "hardcoded metric"
  - "is this gate real"
  - "does the gate actually block"
  - "can this bypass the gate"
  - "enforcement coverage"
  - "is the guard load-bearing"
  - "who actually made this change"
  - "audit trail attribution"
  - "prevented vs detected"
  - "a service claims a control you must verify"
  - "verifying a claimed result or sealing a control"
  - "auditing an auth/gate control for verification"
merged_from:
  - audit/control-integrity-audit
  - audit/declared-vs-enforced-control-audit
  - governance/control-mechanism-audit
  - governance/named-mechanism-audit
  - audit/name-requires-mechanism
  - enforcement-coverage-audit
  - governance/control-seal-verification
  - court-audit/proxy-verification-audit
retired_to: /root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/control-audit
authority: F13 sovereign in-chat order 2026-09-19 (namespace collapse) — eight skills answering one question collapsed into one router.
---

# Governance Audit — is this control real, or is it a label?

> **DITEMPA BUKAN DIBERI.** A control that never says no is a label, not a boundary.
> A control-like name requires a runtime causal mechanism. Where the mechanism is absent, the name is
> a claim about intent — and intent is not enforcement.

This is the canonical, merged skill for one family of question: **is this named thing actually
enforced, or is it a label?** It replaces eight predecessor skills (see the *Trigger table* at the
end; originals frozen at the path in `retired_to`). Pick a mode from the router below, then run that
mode's procedure. The cross-mode law in §1 applies in every mode.

---

## 0. MODE ROUTER — choose by the QUESTION ASKED, not by the tool

| The question actually being asked | Mode | What it decides |
|---|---|---|
| "Does this control exist and act at all — and which state did it reach?" Any claimed gate, validator, health check, sandbox, seal, drift detector, shadow mode, authority check, privacy filter, promotion ladder, "is it wired up", "the control is present", "privacy filter is on" | **MODE-CONTROL-INTEGRITY** | DECLARED / PARTIAL / ENFORCED / VERIFIED / CONTRADICTED / UNBUILT / DORMANT / DECOY, with the three proofs that survive |
| "The spec/doc/client/proposal says requests to this endpoint require X — is that true of the thing running now?" A service claims a control you must verify; approval gate, signature, scope check, deny list, rate limit, authorization tier | **MODE-DECLARED-VS-ENFORCED** | The claim→enforcement diff table; every `ABSENT` row |
| "It is *named* like a control — is the name doing any work, or is this a false name?" false name, named but not installed, gate passed, 0 rejections, hardcoded metric | **MODE-NAMED-MECHANISM** | The shape catalogue; rename-before-fix; false-absence discipline |
| "Does it cover **all** the paths that can mutate the thing — is the guard load-bearing?" enforcement coverage, does the gate actually block, can this bypass the gate, prevented vs detected, who actually made this change, audit trail attribution | **MODE-ENFORCEMENT-COVERAGE** | `coverage = gated / writable`; ADVISORY vs ENFORCING; attribution source |
| "Was this claimed result actually produced — and was the control sealed so someone else can check?" verifying a claimed result or sealing a control; a fix must be proven loaded, not just written | **MODE-SEAL-VERIFICATION** | Result artefacts on disk; hash manifest + unattended verifier + negative control |
| "The gate verifies a *proxy* for the thing — a handshake, a caller-supplied flag, a deny-regex, an allow-table, an approval field — instead of the thing itself" auth/gate control, session gate, authority band, human-approval field, allow/deny regex | **MODE-PROXY** | The six proxy shapes with the falsifying input for each |
| "This scalar / witness / consensus score looks like a measurement — is it one?" suspicious metric, score that never moves, tri-witness confirmation | **MODE-METRIC-DERIVATION** | Derive from the formula before hypothesising; floor constant; literal witnesses |

Routing rules:

1. **Run modes in causal order when more than one applies:** name → caller → effect → bypass →
   coverage → seal. A coverage number computed on an unnamed or uncalled control is decoration.
2. **MODE-METRIC-DERIVATION first** whenever any number, rate, score or witness count is about to be
   quoted — it is a precondition, not a follow-up.
3. **MODE-SEAL-VERIFICATION first** whenever a report of completed/verified work is about to be
   accepted, including your own.
4. If the question is *"should I fix it?"*, that is not a mode — see §1 *Boundary*.

---

## 1. CROSS-MODE LAW (in force in every mode)

### 1.1 The law of the name

**NAME_REQUIRES_MECHANISM.** Any surface whose name asserts gate / health / sandbox / verify / seal /
drift / secure / shadow / authority / wall must exhibit a runtime mechanism, or it is a **false name**
and the honest label is a different one.

```
SEMANTIC AUTHORITY = NAME ∩ CALL_PATH ∩ MEASURED_EFFECT ∩ BYPASS_RESISTANCE ∩ EVIDENCE
any term empty  ->  AUTHORITY_CLAIM = VOID
```

```
EFFECTIVE_CONTROL = CALLER ∧ EFFECT ∧ BYPASS      (if any term is empty, the authority claim is VOID)
```

An agent trusts a **name** faster than it reads a **mechanism**. `reality_gate`, `health_check`,
`sandbox`, `SEAL`, `drift`, `SHADOW` all read as guarantees. A guarantee-shaped artifact that enforces
nothing is **worse than no control at all**: absence is visible, a false control is trusted — and it
gets *built on* by the next lane. A missing mechanism is visible; a mechanism-shaped name is
**believed**, so it propagates. Assume you are susceptible: the authors of the doctrine that names
this defect fell for it in their own text.

That is why this defect crosses hosts, organs and sessions — every layer re-uses the vocabulary
without re-checking the mechanism — and why it must be killed by doctrine, not by patch.

### 1.2 The three proofs — all three required, in every mode

| Proof | Question that must be answerable | How to obtain it | Fails when |
|---|---|---|---|
| **CALLER_PROOF** | Who actually invokes this in the running system? | Sweep **every** invocation surface (agent/cron job store, systemd units and timers, `/etc/cron.d`, crontab, shell wrappers, HTTP routes, loader imports). Name the call site with `path:line`. | zero callers → artifact/decoy, not a boundary |
| **EFFECT_PROOF** | Does a bad/failing input change the outcome or block the action? | Feed it a deliberately failing input and observe a changed output or a blocked action. | can never reject → a sorter/banner, not a gate |
| **BYPASS_PROOF** | Can the same effect be reached another way? | Enumerate alternate paths — another handler, raw shell, shell redirection, editor save, direct DB/file write, a second producer of the same output, the SCM boundary. | one unguarded path → no security property |

A control that **never interferes with anyone** is not a control. Interference is the cheapest
positive evidence you will ever get: a gate that blocked your own read command has proven it sits in
the causal path.

Partial coverage is the normal case. Report **which** of the three are proven and which are not.
Any proof you cannot produce is a **FAIL, not a maybe** — report it as unproven. Never upgrade
`PARTIAL` to `ENFORCED` because the code reads correctly.

### 1.3 Ask the causal question, never the existence question

| Instead of | Ask |
|---|---|
| "Is there a security gate?" | "Can an action reach the protected state **without** passing through it?" |
| "Is there a health check?" | "If a dependency dies, does the output **change**?" |
| "Is there a sandbox?" | "Can a test payload **escape** the containment it claims?" |
| "Is it sealed?" | "Does the seal still **resolve** against the bytes on disk?" |
| "Is it safe?" | "What **physically prevents** the unsafe act — not what discourages it?" |
| "Is sending off?" | "What mechanically prevents a send?" |

If the answer is "it is the default", "it is documented", "it is configured", or "it is named that
way", there is no mechanism.

### 1.4 Evidence hierarchy — the dispute resolver

```
RAW OBSERVATION  >  MEASURED FACT  >  DERIVED STATE  >  REASON CODE  >  NARRATIVE LABEL
```

When two elements of one payload disagree, the higher tier wins. A derived state label must never
override a measured fact beside it, and a defaulted reason code is the weakest tier — it cannot
justify blocking anything. An inverted hierarchy is the same defect as a false name, expressed as an
**ordering violation**: look for it wherever a specific-sounding reason is produced by
`value or "SOME_CAUSE"` — that string impersonates a diagnosis nobody measured.

### 1.5 Verdict vocabulary — name the state you reached, never a boolean

```
PRODUCED != SCHEDULED != FIRED != DELIVERED != OBSERVED != ACKNOWLEDGED
```

"Ran", "sent", "done", "merged", "sealed" are **transition lies**. Name the chain position, and name
which links are still unproven.

One state per control, stated explicitly:

| State | Meaning |
|---|---|
| DECLARED | Name/contract exists; runtime mechanism not proven |
| PARTIAL | Mechanism exists; coverage or bypass resistance unproven |
| ENFORCED | Causal path and measured effect demonstrated |
| VERIFIED | Enforced + bypass test + evidence lineage all pass |
| CONTRADICTED | Claim conflicts with observed runtime facts |
| UNBUILT | Nothing exists yet to check — honest, and **NOT** a pass |
| DORMANT | Exists, correct in isolation, zero callers |
| DECOY | Named like a control, called zero times |
| DECORATIVE | Reachable but cannot reject |
| FALSE_NAME | The name asserts a mechanism that does not exist |
| UNPROVEN | A proof could not be constructed — not a pass |
| NEEDS WITNESS | Only a human can confirm |

**UNBUILT and DORMANT must never be reported as PASS.** A rule that holds only because nothing exists
to violate it is a vacancy, not a control. Vacancies are treacherous: several fail simultaneously on
the day the governed thing is finally built, and nothing was installed to catch it. Say plainly which
protections hold *by vacancy* rather than by strength.

### 1.6 Boundary — an audit reports; it does not grant authority

- This skill audits **whether mechanisms function**. It does not grant authority to change what it
  finds. Where the defect sits in a protected or governance-owned path: **report and hold** — do not
  self-authorise the repair. Building the missing check is a separate, scoped mutation.
- **Never author the envelope that constrains you.** If the authority governing a mutation would be
  written by the act that needs it, that is a self-grant → HOLD.
- **A bypassable gate is a finding about the gate, not a licence to take the open path.** The
  rationalisation arrives pre-shaped and persuasive: *it is decorative, therefore I may route around
  it.* That sentence is the exact defect this family exists to catch — and the smarter the actor, the
  better it argues. Testing the hole "to prove the finding" converts the auditor into the incident.
- **Do not fix under a race.** Before patching, check for a concurrent writer on the same file
  (`find <dir> -newermt "-6 minutes" -type f`). A repair applied while another agent writes becomes
  the second defect.
- **Re-run the probe after any fix.** `ENFORCED` written once and never rechecked is exactly how a
  repaired gap silently regresses.

---

## 2. MODE-CONTROL-INTEGRITY

*Predecessor: `control-integrity-audit`.*

**Use when** a control is claimed to be in force: a gate, validator, health check, sandbox, seal,
drift detector, shadow mode, authority check, privacy filter, or promotion ladder. Also load before
*repairing* anything described as a guard, and before trusting a label a guard produced.

### The one question

Not "does it exist?" and not "is it configured?". Ask:

> **Can an action reach the protected effect without passing through this control?**

If yes, it is not a boundary.

### STOP RULE — check causal-path membership before auditing or repairing

Run **CALLER_PROOF first**. If nothing invokes the artifact:

- auditing it yields true findings with **no consequence**;
- "fixing" it leaves the delivered behaviour identical;
- the finding is real but the *impact* is zero.

Label it by what it is and stop: **DORMANT** (exists, correct in isolation, zero callers) or **DECOY**
(named like a control, called zero times). A repair outside the causal path is fix-shaped, not a fix.
Verify the sweep query can actually match — see §4 *False absence* and `agent-exploration-discipline`.
On a federated box, sweep **all four** scheduler surfaces: hermes cron jobs, systemd timers,
`/etc/cron.d`, root crontab.

### Attestation validity and sole-writer discipline

An attestation binds a digest to an instant. It is stale the moment anything writes the subject —
including your own follow-up edit and a parallel agent's.

- **Before attesting:** confirm you are the sole writer of every path in scope.
- **Before fanning work out to several agents:** partition by **disjoint file sets** and record one
  owner per path. Two writers on one path is a defect of the plan, not of the agents.
- **When a digest no longer matches:** check whether the attestation was correct when written and a
  second writer moved the target. Blame the second writer, not the seal.
- **Reconcile append-only:** `ORIGINAL CLAIM → COUNTEREVIDENCE → CORRECTION`, with the causal chain.
  Never rewrite a signed record to match current state — that destroys the audit trail it exists to be.
- Re-verify **all** digests in an attestation, not just the suspect one. A single mismatch does not
  mean the whole attestation is false.

### Reporting

1. Count controls by state; report **UNBUILT and DORMANT separately** from PASS.
2. Report the **false-assurance count** — controls that look enforced but are only DECLARED. A false
   name is worse than an absence, because absence is visible and a name is believed.
3. Name the **counterexamples too**. A control that records both success and failure with a verifiable
   identifier, an API that returns a refusal verdict on a missing required field, and a self-test that
   proves each of its checks can reject are all genuine enforcement. The accurate finding is usually
   **uneven control integrity**, not universal failure.
4. State one condition under which your audit would be wrong.

### Pitfalls

- **Auditing the name instead of the mechanism.** Finding the implementation correct proves the code
  is correct, not that anything runs it. CALLER_PROOF is not optional.
- **Treating configuration as enforcement.** A permissive-by-default setting is safe-by-accident, not
  safe-by-design; whoever can write the setting can open it. Default ≠ wall.
- **Repairing a dormant artifact and reporting impact.** The edit is real, the effect is nil. Say so.
- **Accepting a metric whose value is a constant or flag.** A rejection counter derived from config
  rather than from events will read as a working control forever.
- **Generalising to "everything here is fake".** That conclusion is itself a false claim, and it hides
  the genuinely working controls an operator needs to keep trusting.
- **Letting a guard fall back to the permissive branch.** "If every check fails, return the top-ranked
  item anyway" means the gate can reorder but never refuse. Verify the denial path exists.

See `references/decoy-catalogue.md` — twelve observed decoy shapes with the specific probe that
exposes each, plus the positive pattern (what a genuine control looks like) and the counterexample
reporting rule.

---

## 3. MODE-DECLARED-VS-ENFORCED

*Predecessor: `declared-vs-enforced-control-audit`.*

**Use when** any claim of the form *"requests to this endpoint require X"* — an approval gate, a
signature, a scope check, a deny list, a rate limit, an authorization tier. Also whenever a spec,
docstring, client library, or proposal template describes a control and you are about to repeat that
description to a human, or rely on it yourself.

The trigger is always the same shape: **the claim lives in one layer (documentation, client code, a
plan, operator copy) and the enforcement would live in another (server code, dispatcher, middleware,
policy engine).** Establish which layer actually checks before you speak.

### Procedure

1. **Find the claim.** Enumerate every place the control is asserted: module docstrings, client-side
   helper signatures, READMEs, proposal/prompt templates, human-facing copy. Each is a claim, not
   evidence.
2. **Find the enforcement point.** Read the request path in the server: the dispatcher, the auth
   check, any middleware. Note which checks are actually *called* on the way to a protected action.
   A guard that exists but is never invoked is dead code, not a control.
3. **Probe the running artifact — do not audit the source alone.** Start it on an **isolated loopback
   port** with a **throwaway credential**; never the live credential, never through the live ingress
   or tunnel. Then issue one request per route and record status code and body.
4. **Include positive and negative controls.** At least one route that *must* be allowed and one that
   *must* be denied. If every probe returns the same refusal, you have learned nothing about the deny
   list — only that your credential is wrong.
5. **Diff declared against enforced, and record every `ABSENT` row.** The deliverable is a compact
   table: claim → where it could be enforced → probe result. The absent rows *are* the finding.
6. **Tear down.** Kill the probe process and confirm the port is free (`ss -lntp | grep <port>`). A
   stray probe server holding the real port is worse than no probe.

Runnable probe: `scripts/contract_probe.py` — takes a JSON spec of routes (path, method, whether a
token is attached, and whether each *should* be allowed or denied), hits a loopback base, prints the
result table, and flags any probe whose outcome contradicts its declared expectation. Optionally
diffs a source file against marker strings to show which checks exist in the code at all.

### Interpreting results

- **A rejection proves enforcement. A downstream error does not.** If a guarded action fails from
  *inside* the action — a missing binary, a timeout, a filesystem error — the request cleared every
  policy gate on the way in. That is evidence of **absence**, not of a working gate. Read where the
  failure originated, not just its status code. (`expect=deny` passes only on an explicit refusal
  such as 401/403; `expect=allow` passes on anything that is *not* a refusal, deliberately.)
- **The declared and enforced layers are written by different hands at different times.** Expect
  drift; do not smooth it over. Test the instance in front of you and do not generalize from a sibling
  service.
- **A control exercised only in the client is not a control.** If the caller is the only party
  checking the condition, any other caller — or the same caller with curl — walks straight past it.
- **Name-level verification is not verification.** A function that exists, a header that is sent, a
  parameter a helper demands: none of these mean the receiving side reads them.
- **Contract drift runs in the harmless direction too.** Clients routinely call paths the server does
  not route. Record those: a 404 on the client's own health check is a bug someone will otherwise
  rediscover from scratch.

### Reporting rules

- State what is **enforced**, then what is **declared but unchecked**, then the consequence in one
  sentence. Do not bury the gap under a list of the parts that work.
- Never describe a system as gated on a control you have not watched reject. If a bare token reaches a
  sensitive action, say the token is the whole lock.
- A gap is a finding to **record**, not a repair to perform inside the audit.
- Prefer running the subject's own verifier or self-test over summarizing it. Independent observation
  beats the author's assurance, always.

### Pitfalls

- **Never probe the live service.** Loopback port plus throwaway credential keeps the finding from
  costing a production side effect. A probe that captures a photo or mutates state on the real path
  has turned an audit into an action.
- **Bind the probe above 1024 and away from the real port.** The real service may be listening on this
  host; colliding with it fails confusingly or shadows it.
- **A uniform failure across all probes is a failed probe, not a hardened service.** Verify credential
  and port before concluding anything.
- **Record the probe set with the verdict.** A control verdict without the routes and status codes
  that produced it is an assertion, not a witness.
- **Re-run the probe after any fix.**

---

## 4. MODE-NAMED-MECHANISM

*Predecessors merged: `control-mechanism-audit`, `named-mechanism-audit`, `name-requires-mechanism`.*

> Audit the question "does it exist?" against the question that actually matters: **"can it refuse?"**

**The law:** no control-like name may be trusted without runtime causal evidence. A gate, health
check, sandbox, seal, drift flag, verify step, privacy filter or SHADOW mode is a **hypothesis about
the system**, not a fact about it. The name is the claim; the mechanism is the evidence. They are
different objects.

Presence, naming, imports, documentation and metadata are all satisfiable **without a mechanism**. A
control that is named but not installed is more dangerous than an absent control: absence is visible,
and a name is believed. An absence gets rebuilt; a false name gets relied upon.

Every shape below is one defect in different clothes — a claim of function that the artifact itself
falsifies. That is why the audit works: **you can check the claim against its own output**, without
trusting any narrator.

### The three decisive tests

Run all three on any claimed control. Each is cheap, and each has caught defects that looked healthy
from every other angle.

#### 4.1 Can it refuse?

Drive it with input that MUST fail. A gate whose failure branch returns the best remaining candidate
has no failure branch — it re-ranks.

```bash
grep -n -A6 "def .*gate\|def .*check\|def .*verify" <file> | grep -i "return"
# suspect: a bare `return ranked` / `return default` / `return True` after a failed check
```

Ask the follow-up too: **has it ever fired?** A check that has never produced a rejection in its whole
history is unproven. Plant a fixture that must trip it, then confirm it trips.

#### 4.2 Is the label DERIVED or ASSERTED?

```python
# ASSERTED — drifts from reality the moment the producing code changes
report["privacy_filter"] = "arif-only"     # hand-written intent
report["rejections"]     = 0               # lives in the source, not the data

# DERIVED — cannot contradict, because it IS the renderer's input
report["od1_excluded"] = ("od1_days" not in payload)
```

A label computed from the artifact cannot contradict it. A hand-written label can, and eventually
will. **Sort fields by origin, not by name.** Tell: a field holding the same value (`0`, `"none"`,
`"active"`) no matter the input. Diff it across two runs with genuinely different inputs — a constant
that never moves is a literal, not a measurement.

#### 4.3 Who authored it, and who benefits?

An attestation written by its own beneficiary is not an attestation. Look for the **independent
witness**, not the record of authority.

```bash
grep -rn "RATIFIED\|APPROVED\|reviewed_by\|attested" <record-file>
# then: read who wrote it, and ask whether they are the party the record protects
```

Two signals: (a) no artifact from an independent party exists for the event, (b) the recording agent is
the one whose work is being recorded.

### Failure-shape catalogue (name → the mechanism defect → the decisive probe)

| # | Shape | Looks like | Decisive probe / fix |
|---|---|---|---|
| 1 | **Decoy gate / gate as artifact** | Gate module with full validation logic, strong name | List its callers — zero callers = doctrine, not control. Wire it, or label it dormant. |
| 2 | **Health check returning a literal** | Fixed `status: "healthy"` banner | Read the handler body; stop a dependency and see whether the output changes. |
| 3 | **Frozen / constant metric** | `rejections: 0`, `privacy: ok`, `drift: none` | Is it computed, or `0 if <flag>`? Flip the flag and re-run. Derive the metric from the thing it describes, or report `NOT_MEASURED`. |
| 4 | **Label overriding its own fact** | One payload holds `drift: false` and a drift-derived block; trigger on `state == DEGRADED` | Print both fields from one response; compare tiers against the evidence hierarchy. Branch on the measured fact; a label is a hint, never the decision input. |
| 5 | **Default mistaken for a wall** | An env/config default of `SHADOW`/`off` described as a boundary | Anyone able to write config can open it. Call it `delivery_default = off`, not a wall. A default is a posture; a boundary is a mechanism. |
| 6 | **Import without use** | Containment/enforcement module on the import line, absent from the execution path | Grep each imported symbol; appearing only on the import line means the architecture was **imported, not installed**. |
| 7 | **Non-refusing fallback** | Gate with a default branch | Force every candidate to fail; a non-empty result is a soft bypass. |
| 8 | **Defaulted reason code** | `reason_code or "SOME_REASON"` | Locate the measurement that produced the cause; a fallback string is a measurement-shaped hole, not a diagnosis. |
| 9 | **Blocklist as policy** | "freshness check", deny-list of literals | Read the predicate — banned strings defend only known-bad values, each one yesterday's bad value. Introduce a new bad value; if it passes, this is a patch, not a policy. |
| 10 | **Hardcoded banner / evidence from a dead endpoint** | Receipt cites a health check; endpoint returns a literal `"healthy"` | Probe that exact endpoint; a hardcoded banner validates nothing. |
| 11 | **Metadata vs artifact** | `filter: on`, `hidden: true` in the header | Search the **rendered output** for the thing it claims to hide. Highest-yield single check in this mode. |
| 12 | **Stored not computed** | A countdown, age, drift or delta field | Run it on two dates — a value that never moves is a literal. |
| 13 | **Self-attestation** | "Ratified"/"approved" record | Did the beneficiary author it? |
| 14 | **Stale seal** | A seal/receipt attests a hash that no longer matches disk | See `references/seal-and-delivery-verification.md`; reconcile with a `supersedes` record — never rewrite sealed history. |
| 15 | **Configured mistaken for delivered** | A job's `deliver`/`target` field quoted as proof the right party received something | Read the delivery ledger for a `SENT` event plus a real message id (`CONFIGURED != DELIVERED != INTENDED`). |
| 16 | **Attestation matching nothing on disk** | Attested digest matches no file | Re-hash every path in the attestation; check mtimes against the attestation time. A sealed `sha256_after` matching no state that ever existed on disk attests a fiction. |
| 17 | **Gate that can reorder but not refuse** | Ranking function with no denial return | Inspect the return paths; if every branch returns a value, nothing is blocked. |
| 18 | **Evidence that exists but does not correspond** | Receipt present, event not proven | Ask what the receipt would look like had the event *not* happened; if identical, it is not evidence. |

### Procedure

1. **Grep the existing audit corpus FIRST.** A system that has audited itself once has usually already
   named the family (search for verdict words like `FALSE_NAME`, `MISLEADING_NAME`, `PARTIAL_NAME`).
   Citing the prior finding beats re-deriving it, and it answers the question that matters: is this an
   incident, or a family?
2. **Inventory the names.** Collect every surface asserting control in the scope under audit.
3. **CALLER_PROOF — grep every scheduler and dispatch surface, not just one.** A capability can be
   invoked by cron, systemd, crontab, `/etc/cron.d`, a shell wrapper, an HTTP route, or another module.
   Grep them all; a single-surface grep manufactures false dormancy.
   ```bash
   for s in <cron-store>.json /etc/cron.d /etc/systemd/system; do grep -rl "<artifact>" "$s"; done
   grep -rln "<artifact>" --include=*.py --include=*.sh --include=*.service <repo-roots>
   ```
4. **Locate the enforcing code path**, not the claim about it. The check must live in the code that
   produces the output. A flag honoured by one writer and ignored by another is not a boundary — it is
   an optional convention.
5. **Drive the failure path** (test 4.1). Report whether rejection is even reachable.
6. **EFFECT_PROOF — inject a failing input and observe.** Disable the dependency, feed malformed data,
   or attempt the bypass. If the output does not change, the control is decorative.
7. **Diff metadata against artifact** — search the OUTPUT for the property the metadata claims.
8. **BYPASS_PROOF — enumerate alternate paths.** Every mutation path to the protected state must pass
   the check. One shell-level or editor-level path that skips it voids the property entirely.
9. **Re-run across a boundary that changes the answer** (two dates, two audiences, two input classes).
   Constants reveal themselves only under changing input.
10. **Attribute to the owner** of registration/enforcement, then state the fix shape.
11. **State plainly what fixing one instance does not fix.** If the family persists, the family is the
    finding.
12. **Decide: rename or repair** (prefer rename — below). **Record the verdict with its proof**, or
    mark it `UNPROVEN` — never `PASS` by absence of violation. "Nothing violated it yet" is not
    enforcement. Distinguish `UNBUILT` from `PASS`.

### Rename before fix (honest naming IS a control)

The fastest way to kill a false-name family is to make the name true **before** repairing the code:

- A banner that only prints status is a `status_banner`, not a `health_check`
  (`forge_health_check` returning a literal → `forge_status_banner`).
- A lane that can send if someone edits config is `delivery_default = off`, not `cannot send`
  (`SHADOW`-as-safety → `delivery_default=off`).
- A file with zero callers gets a header banner stating it is `DORMANT — NOT IN PRODUCTION PATH` and
  naming the real path; an unreferenced module named "engine" gets the same treatment.

Do this even when you cannot fix the code: a truthful name stops the **next** agent from inheriting the
false premise. A misleading artifact name is an unattended trap.

### Fix must be IN the causal path

Before repairing a file, `grep` for its **scheduled callers** (all four surfaces above).

> A fix outside the scheduled call path is **fix-shaped, not a fix**.

Editing a dormant file and reporting seven defects repaired is itself an instance of the defect being
audited: declaration without enforcement.

### False absence — proving CALLER_PROOF = 0 honestly

A null result is evidence of absence **only if the query could have returned a hit.**

A pattern can be structurally incapable of matching: searching a store by its visible title
(`-name "Title*"`) when the store renames every artifact to a generated prefix (`doc_<hash>_Title`).
The empty result carries **zero information**, and reporting it as absence fabricates a finding.
Generated store prefixes (`doc_<hash>_`, `<session-id>_`, UUIDs) break name-anchored globs: use
`-iname '*term*'` or content search, never `-name "TERM*"`.

**Run a control search first** — the same query shape, aimed at something you know exists:

```bash
find <root> -iname "*known_good_fragment*"   # control: must HIT
find /      -iname "*target*suffix*"        # only then trust a null here
```

- **Anchor on a substring, never a position.**
- One control call is cheaper than one retraction.
- If you cannot construct a control that hits, you have not earned the null: report `UNPROVEN`.

### Label states honestly — UNBUILT is a valid verdict

Use, and never collapse:

`PASS` (artifact exists and the check can reject) · `FAIL` (violated, evidence named) · `UNBUILT`
(nothing exists to test — not a pass) · `UNPROVEN` (cannot be tested now) · `NEEDS WITNESS` (only a
human can confirm).

A checker that has never rejected anything is untested. Prove the check **can** fail by running it
against a known-bad input before trusting a PASS from it.

### Receipts: correspondence, not existence

`receipt exists != the event happened`. A receipt is only valid if it causally corresponds to what it
attests. Re-derive the artifact hash and compare. Record corrections **append-only**:
`ORIGINAL CLAIM → COUNTEREVIDENCE → CORRECTION`. Never rewrite history to make it clean; the mismatch
is the most valuable part of the record.

### A refused authority is a state, not a failure

When a seal/judge path returns a refusal, record `REFUSED` together with the returned reason and the
measured facts beside it. **Never relabel the artifact "sealed".** A receipt that overstates its own
authority is the same defect class as a metric that overstates itself — and an auditor who commits it
has imported the disease they were hired to find.

Separate the two meanings of a hold: **governance hold** ("not yet proven") versus **broken gate
wearing governance vocabulary** ("the reason code was defaulted, not measured"). When reality
contradicts the refusal, report both the artifact state and the gate defect: a gate that cannot be
trusted to close correctly cannot be trusted to open.

### Seal the pattern, not each bug

Bugs of this family are one defect wearing many names. Fixing them one at a time guarantees the next
one. The durable artefact is the invariant plus an executable check per boundary, where every check
can **REJECT** — a checker that cannot fail is itself a false control.

### Reporting discipline

- Do not force claims to `confirmed` to make a finding look strong. When some instances are verified
  and others are class-level or site-dependent, say so per instance and name the exact `file:line`. An
  audit that over-claims belongs to the same defect class as the code it audits.
- **Publish your own retractions in the same artifact.** A report carrying only findings against others
  is half an audit. Apply the same scrutiny to your own working claims, and when one of yours fails,
  retract it **in the same document** with the mechanical cause — a correction you surface yourself
  costs far less credibility than one a peer finds later. A retraction must **replace**, not hedge:
  give the new state, not a downgraded confidence that leaves the old claim standing in the record.

### Pitfalls

- **The counter-question is not the finding.** Proving a sibling's claim wrong does not make yours
  right; verify your replacement value from the source of truth separately.
- **Distinguish the two clocks.** If one component computes a value and another reads it from the
  canonical store, you have two answers to one question. Trace which components read the store and
  which compute their own — the ones that compute are where the drift lives.
- **A gate that caught its own author's error is the only gate worth trusting.** Prefer the check that
  failed on your own work at least once.

---

## 5. MODE-ENFORCEMENT-COVERAGE

*Predecessor: `enforcement-coverage-audit`.*

A control's block-rate on the traffic it sees says nothing about whether it covers the paths that can
actually mutate the thing you are protecting. This mode audits the **reach** of a control, not its
verdicts — and audits whether the evidence trail about a mutation is attributable at all.

Sibling skills (load them too; do not duplicate their content here): `forge-execution-governance`
(alive ≠ governed; listing ≠ calling; a structural zero is not a measurement — SERVICE-level
governance; this mode is CONTROL-level coverage) and `self-recurrence-guards` GUARD 6 (attribution
guards for claims about events and actors).

### Core equation

```
EnforcementCoverage = paths that intersect a gate / paths that can write protected state
```

A gate that blocks 100% of the attempts routed to it, while covering 1 of N write paths, has
`PreventedUnauthorizedRate → 1.0` and `UnauthorizedEscapeRate → 1.0` simultaneously.

**The prevention metric's denominator only contains attempts the gate observed.** An attempt that
bypasses the gate is *not in the denominator* — so the rate reads perfect while the escape happens.
Report coverage alongside prevention, or report neither.

### Procedure

**1. Name the protected set before naming the control.** Write down the actual targets: authority/config
files, canonical registries and records, governance documents, secrets, production state, and the
control's own configuration. If the protected set is not written down, coverage cannot be computed and
the audit is theatre.

**2. Enumerate EVERY path that can write, then probe each one.** Do not audit the intended path.
Enumerate the possible ones:

| Path | Probe |
|---|---|
| Direct file API / interpreter | write the target from a tool call or one-liner; observe whether anything refused |
| Shell redirection / editor tool | append to the target; save from the editor into the tree |
| Version-control boundary | stage + commit the target, and watch whether a hook fires (`ls -l <repo>/.git/hooks/`, then read what the symlink target actually runs) |
| Test / build / migration runner | anything that writes outside the normal edit flow |
| The control's own config | if the gate's rules are writable by the actor it constrains, coverage is zero by construction |

A hook that exists is not a hook that fires: read what each hook invokes and confirm the invoked script
is present and executable. An unwired engine is a library with no callers — `grep -rl <engine-name>`
across the live runtime, plugins and harness configs. Zero hits means it gates nothing, however
complete it looks.

**2b. Read the gate's default AND its own bypass note.** Coverage depends on whether the control is
even switched on, and the guard's source usually documents the hole its author already knew about.
Read both before scoring.

- **Opt-in gates score zero on a default install.** *Measured 2026-09-17:* a skill-write security scan
  is gated by one config flag (`skills.guard_agent_created`), default **False**, and the guard's own
  docstring says so and then names the uncovered path in the same breath — *"opt-in — terminal() runs
  the same code ungated."* The author documented the bypass. **Read the guard's docstring, not just its
  decision table**, and read both against this install's config value before quoting either.
- **Enumerate EVERY call site before declaring the remedy impossible.** A decision function is not the
  control and one caller is not the control. Same case, corrected by a later pass: the scan gate's
  decision function *does* implement a documented `force=` override for the blocked cell, and one
  caller in the tree already plumbs it (`force=force`, reachable as `hermes skills install --force`);
  what the first pass had hit was a **different caller** — the agent's own skill-write path — which
  passed nothing. So "there is no path forward at all" was true of the audited lane and false of the
  control: the finding had generalised from one hit. **Run
  `grep -rn "<decide>(" <tree>` and map each hit to the lane it serves before writing the verdict.**
  The distinction decides the fix: an unplumbed parameter on one caller is a one-line repair, a missing
  policy cell is an authority decision. Write the lane into the finding ("no exit **on the agent write
  path**"), never the bare claim.
- **A remedy that is unsatisfiable for *this* package is still a finding — name it precisely.** In the
  same case the caller's only offered remedy was *"retry without the flagged content"*, and the flagged
  content **is** the package's purpose (a body of `getMe` identity checks that any exfiltration-pattern
  rule will match). Report it as *the stated remedy cannot be satisfied for this artefact*, filed
  against the remedy — not as "the gate has no exit". Do not spend the turn hunting for the exit; do
  spend it enumerating callers.
- **Check the verdict against the content before calling it a false positive.** Grep the flagged file
  for a literal value matching the shape the rule hunts. Measured on the same package: 29
  exfiltration/supply-chain findings, every one a **variable reference** (`…/bot${TOKEN}/…`) and zero
  literal credentials. The rule matched the *shape of the idiom*, not a value. Report three numbers —
  findings, literals, and where the literals are absent — and let them carry the argument; never assert
  "false positive" from a read-through alone.
- **Then stop. A bypassable gate is a finding about the gate, not a licence to take the open path.**
  The correct output is `coverage < 1, uncovered = <the path>, action = HOLD`, plus the naming of the
  gap.

**2c. Falsify the instruments before computing coverage.** Coverage is arithmetic on top of
measurements; if a measurement comes from an instrument that cannot return non-zero the figure is
fiction. Rules (full procedure in `references/sensor-falsification.md`):

1. Every sensor needs a **positive control** — run the same instrument against an input that MUST hit
   before reporting a zero/empty/clean result; if it misses, report `UNMEASURABLE`, never `zero`.
2. **Dereference before counting** — `find -L`/`followlinks`/`realpath`; dedupe one tree seen twice;
   confirm any absence claim with a second, differently-constructed probe.
3. **De-metadata before matching** — strip routing/tier/floor prefixes repeatedly until stable, or every
   tagged item falsely clusters with every other.
4. **Never separate a number from its method** — always state matching rule + threshold + corpus/surface
   list; a method divergence is the finding, do not average or pick the survivor.
5. **Re-probe before repairing and before reporting** — a recorded state table is a snapshot with a
   TTL, including stored FAILURES.
6. **Sensor state may not be self-reported** — when the measurement is about the system that produced
   it, compute from an independent artifact.

**3. Compute coverage explicitly.**

```
Coverage:  <gated paths> / <writable paths> = <ratio>
Uncovered: <explicit list>
```

If any uncovered path is reachable by the actor under audit, the control is **advisory, not
enforcing**. Say that plainly — "policy in language" is the accurate description, and it is a finding,
not an insult.

**4. Verify the mutation from evidence the executor does not control.** Never accept a completion
report as proof a change landed. Read the artifact: version-control log/diff for tracked state, hash or
mtime for untracked state, the live endpoint for deployed state.

A witness that reads the executor's own success log is not an independent witness. Independence comes
from the *evidence path*, not from using a different agent: probe the deployed hash, the external
endpoint, or the observed behaviour directly. **Different agent ≠ independent witness.**

**5. Check whether the trail can name the actor at all.** Before trusting any attribution recorded in a
ledger, open the ledger and find where the actor field comes from.

- A repo-level VCS `user.name` is ONE value shared by every session, harness and lane writing to that
  repo. Changes minutes apart from different actors all carry the same name. **Authorship read from a
  shared config value is non-identifying.**
- The correct source is session-derived — session id + host + objective — captured at the write
  boundary by the boundary itself, not self-reported by the writer.
- If the ledger attributes several actors to one name, the trail is corrupted at the source and every
  later forensic read inherits the error. Report the defect; do not paper over it by guessing.

**6. Keep epistemic resolution and mutation authority separate.** Coverage work routinely surfaces an
adjacent collapse. State the separation explicitly:

- `UNKNOWN → RESOLVED` is an epistemic transition. `RESOLVED → MUTATED` is an authority transition.
  Neither implies the other.
- `CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive`. Confidence is
  deliberately absent from that conjunction and must not be smuggled into it.
- "I should not bother the owner with this" is never a grant. The more capable the actor, the *less*
  its permissions may depend on its own agreement with them.
- Never author the envelope that constrains you: if the authority governing a mutation would be written
  by the act that needs it, that is a self-grant → HOLD.
- Scope is checked against the diff, not the intent: `ActualDiff ⊆ AuthorizedScope`, computed from what
  would actually change.
- Two escalations, not one. Asking the owner to **choose** among facts the machine can resolve is a
  defect — resolve it. Asking them to **authorize** what only they may authorize is correct — route it
  as a binary decision, never as a work handoff.

### Output

```
Protected set:        <targets>
Enforcement coverage: <gated>/<writable>    Uncovered: <list>
Verdict:              ENFORCING | ADVISORY | ABSENT
Attribution:          IDENTIFYING | NON-IDENTIFYING (source: <where the actor field comes from>)
Witness:              independent evidence path used, or UNWITNESSED
Open defect:          the smallest concrete fix, addressed to the owner of the enforcement path
```

### Pitfalls

- **Auditing the intended path and calling it coverage.** The control is usually installed on the
  polite route. Probe the impolite ones — a one-liner, a redirect, the SCM boundary — before saying
  "the gate blocks it".
- **Reporting a prevention rate without a coverage ratio.** With partial coverage the rate is
  arithmetically perfect and operationally meaningless.
- **Treating a complete-looking control as wired.** Read for callers. A large engine with zero
  invocation sites in the live runtime protects nothing.
- **Trusting a ledger's actor field because the field exists.** Check its provenance; a shared config
  value produces confident, wrong attribution.
- **Accepting an incident attribution from a report without checking provenance** — including accepting
  blame for it. A wrong attribution is the same error as a wrong fact, one layer out, and a trail
  naming the wrong actor teaches every later reader to read it wrongly.
- **Becoming the enforcement.** If the audit finds the boundary must live outside the actor's reasoning,
  that is a finding for the owner of the enforcement path — not a mandate to write your own authority
  envelope.
- **Concluding "nothing to fix" from an absence of attempts.** No observed attempt ≠ no reachable path.
  That is a structural zero; the reachable-path enumeration is the evidence, not the traffic.
- **A gate's rule list is itself a mutation target.** Confirm the protected set appears in it; a
  forbidden-target list that omits the governance tree gates exactly the wrong things.

---

## 6. MODE-SEAL-VERIFICATION

*Predecessor: `control-seal-verification`.*

Two jobs that share one law: **an assertion is not a state.** A reported result and a sealed control
both have to be checkable by someone who was not there.

### Part 1 · Verify a claimed result

Reports about your own system — "tests pass", "the file is written", "the guard is live" — are claims of
the same kind as any other finding. Probe them.

1. **Locate the artefact that makes the result repeatable.** A pass count is only a result if a harness
   exists that can produce it again.
2. **Confirm it resolves on disk.** If the name appears only in the session database, it is chat text,
   not a deliverable. The absence is the finding.
3. **Re-measure every cited number** — line numbers, counts, sizes, paths. One citation that is off
   means the rest of the citation set went unchecked too.
4. **Fix forward.** Write the missing artefact rather than reporting the gap back and stopping.

When you write the harness:

- drive the component through its **real entry point** (stdin / CLI / HTTP), asserting on observable
  output and exit codes;
- never import the internals you are testing — a harness coupled to implementation drifts with it;
- include a **negative control**: at least one case that must ALLOW, or "blocks everything" scores as a
  perfect gate;
- pin test traffic to a recognisable session id so receipts the test causes are filterable out of the
  real ledger.

**Existence is not support.** A pointer that resolves proves the citation *exists*, not that it
*supports* the figure beside it. Report the weaker, true claim — never "the numbers are verified" when
only the pointer's presence was checked.

One-way reporting is a defect of the same family: `CONFIGURED (the deliver field) != DELIVERED (a
ledger SENT row) != INTENDED (the audience you meant)`. A helper that records **both** `SENT` (with id)
and `FAILED` (with error class) is the reference pattern — it can reject, and it has history. A helper
that only logs success is a one-way recorder; you cannot tell a quiet failure from a non-event. Beware
the timezone trap when filtering a delivery ledger by date: local 06:45 == prior-day 22:45 UTC, so a
local-date filter on a UTC field reports **zero deliveries** for a job that ran fine that morning —
**a date-scoped filter is a claim about the filter.** Full recipes (ledger reads, numeric-id → meaning
resolution, group-id lookup): `references/seal-and-delivery-verification.md`.

### Part 2 · Seal a control

Presence is not seal, and a manifest nobody checks is decoration. Sealed means three things exist
together:

1. **Hash manifest** of the control *and its test*, measured not estimated; record `expected_result` so
   a future reader knows what green looked like. Hash the **control and its test together** — a sealed
   gate with unsealed tests can be "verified" against tests that no longer exist. Never hand-write a
   hash; measure, then paste.
2. **Unattended verifier** — silent when sealed, speaking only on drift, and output only on inability
   to witness. Include a **VOID GUARD**: if it cannot read its own manifest it must NOT exit clean, or a
   deleted manifest reads as healthy. Pair it with a low-frequency unconditional heartbeat, so a dead
   verifier cannot impersonate a quiet one — a monitor that fails silently is worse than no monitor,
   because operators read "no alert" as "all clear".
3. **Negative control proving the verifier fires** — (a) clean run exits 0 with no output, (b) inject
   drift (append a single byte) and watch it alert with **both** the sealed and the current hash,
   (c) restore exactly to the sealed byte size, re-run, watch it exit 0 and the hash match the manifest
   again. If step (b) does not fire, the seal is decoration. Restore by size or from committed content;
   editing back by hand does not reproduce the bytes.

Write the limit into the artefact itself: **drift-visibility is not tamper-proofing.** Anyone who can
read the manifest can regenerate it and pass. Put `_limit` in the manifest file — self-describing
limits survive; limits held in memory do not.

Regenerate the manifest in the same act as any authorised change. A manifest that does not match its
artefact is worse than none — it manufactures trust.

Working code for all of this (harness shape, manifest shape, verifier pattern, negative-control
runbook, shared-control operation, recursion guard, report shape): `references/sealing-a-control.md`.

### Boundary checks that must be able to REJECT

For each boundary in a pipeline spine, write one check that returns one of:

```
PASS     boundary holds on the artifact as it exists now
FAIL     boundary violated, offending evidence named
UNBUILT  nothing exists yet to check — honest, and NOT a pass
```

`UNBUILT` must be a distinct state from `PASS`. Finish with a **self-test**: run each check against a
deliberately bad input and confirm it can `REJECT`. A checker that cannot fail is itself a false
control.

### Pitfalls

- **Do not name artefacts after the words your own gate hunts.** An id or path containing a trigger
  term makes every later command that references it fail the gate. Pick a neutral name.
- **Order regex alternation longest-first.** `jsonl` must precede `json` or matches truncate to the
  shorter extension and a real path silently stops matching.
- **Attribute before you accuse.** Unexpected edits to a shared control are usually a concurrent
  contributor, not an adversary. Read the diff and the mtime before reacting, and fold in compatible
  work instead of reverting it.
- **Honesty of the writer is not evidence of the write.** An unsigned shared file cannot show who wrote
  what, however well-intentioned the contributors. Say "compatible change, no attribution trail", not
  "tampering".
- **Do not freeze a shared control unilaterally.** Making it immutable does not only protect it — it
  locks out whoever is mid-work. Raise it as a binary for the owner.
- **A control guarding tool payloads does not guard outbound prose.** State which surface is covered.
  Prose discipline is not mechanism.
- **A SKILL.md at the character ceiling cannot be patched at all.** Keep SKILL.md lean; put depth in
  `references/`.
- **Two-writer collision:** when a seal, receipt or audit describes a file another agent may also edit,
  hash-binding cannot hold. Signals: a tool warning that another session/agent modified the file,
  `mtime` later than the seal that attests it, two artifacts sealed under the same instruction
  describing the same file differently. Rule: **no file may have two writers** — one recorded owner, or
  the attestation is not verifiable. Adding a second writer to repair a two-writer problem repeats the
  defect.
- **Recursion guard:** when the control you are testing starts refusing your own test payloads, that is
  the control working. Fix the payload (attach a resolving URL, receipt id, or on-disk evidence path)
  rather than shopping for an unguarded tool to run the same write.
- **Report shape — separate three things:** *verified* (what was checked and how), *unverified* (claimed
  but no artefact, with what you did about it), *limits* (what the control does not cover: pointer
  existence vs support, payload vs prose, drift-visibility vs tamper-proofing). A report that only
  lists successes is the thing this mode exists to prevent.

---

## 7. MODE-PROXY

*Predecessor: `proxy-verification-audit`.*

For any control, ask: **what input would make it refuse?** If you cannot name a failing input from
reading the code, the control is not checking content — it is checking the shape of a request.

### The six proxy shapes — all one defect wearing different clothes

| # | Proxy trusted | Reality it stands in for | How to falsify |
|---|---|---|---|
| 1 | a service answers a handshake | the session/credential is valid | pass a fabricated id; if it returns PASS the check was availability |
| 2 | a command string does not match a deny-regex | the action is authorized | same verb via a Makefile target, a wrapper script, or `subprocess` |
| 3 | a caller-supplied boolean | cryptographic proof of identity | set the flag `true` yourself and watch the hold clear |
| 4 | a non-empty string in an approval field | a human approved | pass a self-labelled fabricated sentence; compare field-for-field with a genuine receipt |
| 5 | a name present in an allow-table | identity proven | A/B an unknown name against a table name, same lane, same call shape, no signature |
| 6 | text does not match a threat pattern | the text is not a threat | write documentation *about* the control — the detector fires on the description |

Defect 5 usually supplies the precondition for defect 4, which supplies the label that makes 3 look
sanctioned, while 2 blocks the fix from being loaded. **Map the chain before ranking severity.**

### Procedure

1. **Find the granting branch**, not the function name. `grep -n` the boolean/flag, then read the
   expression that consumes it (`auth = bool(caller_flag or payload.get(...))`). Check BOTH routes — a
   top-level parameter and the same key inside a free-form payload dict. Removing the schema parameter
   alone leaves the payload path open.
2. **Read the comment above it.** Controls often carry a note admitting they are not a boundary while
   the branch below uses them as one. Comment contradicting code is itself a finding, and it tells you
   the fix is unwelcome to nobody.
3. **Inject the fabricated value.** Measure the output. Then run the identical call WITHOUT it and diff.
   One PASS proves nothing; the pair is the evidence.
4. **Prove the ordering.** A gate can be "cleared" while another validator is erroring in the same
   response, because the two are computed at different points and land in different lists (`warnings`
   vs `errors`) that never meet. Read the line numbers, not just the verdict.
5. **Witness on a durable artifact.** Trace ids returned in a response are frequently not persisted
   anywhere. Cite the ledger row, session-store entry, or DB record — and confirm the store actually
   contains it before citing it.
6. **Patch, test fail-closed, then prove load.** A committed fix in an already-imported module is disk
   truth, not runtime truth. Re-run the attack after the restart and show the new verdict.

### Rules that cost the least to follow

- **Fail-closed must be tested as a branch, not assumed.** Unreachable, rejected, and raising are three
  separate paths; assert all three, plus that a legitimate verified session still passes and that
  non-critical paths are unchanged. Otherwise the fix breaks the users who were never the problem.
- **Keep the rejected parameter.** Removing it turns a soft warning into a hard schema rejection for
  every legacy caller. Retain it, strip its authority, and emit an explicit `SELF_ATTESTED_..._IGNORED`
  warning so the caller learns instead of silently breaking.
- **A scan will over-report by orders of magnitude.** `verify(signature_hex)` *must* accept a signature
  from the caller — that is the thing being checked, not authority being claimed — and unrelated
  `*_override` names (a gamma-ray column, a depth parameter) collide by shape. Filter with one question:
  *does the code USE this value to grant something without an external check?* Report the surviving
  sites, never the hit count.
- **Pre-existing test failures: prove them by stash.** `git stash push <your files>`, re-run, show the
  identical failure, restore. Without that, every red test becomes your regression.
- **Never route around a gate with a string it happens not to match.** If the deny-regex misses a
  Makefile target or a wrapper, using it is circumvention by proxy and voids the audit's own standard.
  Escalate the deny-all, or stop.
- **If you must alter wording to get a document past a detector, disclose it inside the document.** An
  audit that self-censors to fit a shape detector is worthless unless the censorship is named.
- **Corrected claims stay in the record.** Keep a retraction table: claim, correction, evidence. A
  corrected claim is still a claim, and the next agent needs to see both halves.

### Related

- `deploy-drift-verification` — disk truth vs process truth, node forks, which tree the service imports.
  Load it alongside this mode whenever the fix must be proven *loaded*, not just written.

---

## 8. MODE-METRIC-DERIVATION

*Predecessor: `proxy-verification-audit` (metrics & witnesses section) — split out as its own mode
because the question is distinct.*

Three wrong explanations for one scalar is the normal outcome when you reason from observed values
instead of from the formula. **Derive before hypothesising.** Full procedure:
`references/metric-derivation-discipline.md`.

Short form (from the computing function outwards):

1. Read the function that computes it — the formula, the window, the zero-data branch. The docstring
   often names the historical bug that produced the current shape; read it as a map of what the value is
   NOT.
2. Read the DB/table it queries. Note whether each call site passes a scoping argument (`actor_id=`);
   grep for **all** call sites and report which scope each uses — a function with an optional scope
   parameter usually has callers on both sides.
3. Recompute it from the underlying table for **every** observation you hold (not a sample), counting
   only the rows visible *before* that call. Report "6/6 instants match", not "consistent with". A model
   that explains five of six is a different model from one that explains six of six.
4. Test sensitivity. Vary the candidate driver across a wide range and see whether the output moves. If
   history volume spans three orders of magnitude and the scalar moves half a percent, volume is not the
   driver — say so, because "more data ⇒ better score" is the intuitive reading everyone will assume.
5. Only then propose a mechanism, and name the line numbers.

**Trap 1 — the floor constant.** A geometric mean over clamped factors returns the root of the clamp
whenever any factor is zero:

```
G = (max(0.01,A) * max(0.01,P) * max(0.01,E) * max(0.01,X)) ** (1/4)
P = 0, A = E = X = 1.0   →   G = 0.01 ** 0.25 = 0.3162
```

Recognise it: the observed value equals `<floor> ** (1/num_factors)` exactly, and *many* different
actors all show the same number. That is not agreement between actors; it is the floor speaking. Report
the constant and the reason it dominates (which factor is zero), then report the underlying ratio
fleet-wide — the zero factor is usually the real finding, and the scalar's narrow range is precisely why
it hides it. Also check derived siblings: a term of the form `A*(1-P)*(1-X)` returns `0.0` when `A=X=1`,
i.e. the "nothing concealed" reading appears exactly when evidence is absent — a zero there is an
artifact, not a clean bill.

**Trap 2 — the cold-start regime and self-referential thresholds.** `n = 0` → sentinel (`UNMEASURED`/
`None`) for every scalar; `n ≥ 1` → computed, deterministic for the same row set. The measuring call is
frequently the call that writes the first row, so an actor's first probe returns UNMEASURED and its
second returns a number with nothing else changed. Do not attribute that to transport, client, actor
state or runtime entropy — count the rows that existed at each instant. When two observations differ,
enumerate every variable that actually differed (actor, lane, transport, time, prior history) and
eliminate each against data; **the surviving variable is the answer even when it is boring.**

**Trap 3 — literal witnesses.** Search the path that emits a "witness", "consensus", "diversity" or
"confidence" field for hardcoded numbers:

```
_hw = 0.95 if actor_verified else 0.42
_aw = 0.94 if <profile loaded> else 0.32
_ew = 0.93                      # unconditional literal, no sensor
score = round((_hw * _aw * _ew) ** (1/3), 4)
```

Recompute the literal combination and compare with the observed value. An exact match proves the field
is a restatement of the verified/unverified branch, not corroboration from independent channels. Two
consequences: (a) it must **never** be cited as independent confirmation of an identity, a claim or
another metric; (b) note which branch the literals live in — a backfill inside
`if not already_minted:` runs only for actors that pass the earlier gate, so unverified callers keep the
honest sentinel while verified ones get the inflated number. The most convincing-looking score is the
one awarded purely for passing a lookup. Verify by reading the branch, not by inferring it. Also check
for a neighbouring module that deliberately refuses a proxy for the same field ("honest None, never an
inflated proxy") — the discipline holding in one file and being re-introduced as literals three files
over is the finding; cite both.

**Trap 4 — the label that outlives the meaning.** Write the corrected label into whatever artifact you
produce:

> `<metric>` — telemetry observation, not governance authority; computed from <source> over <window>;
> `<sentinel>` when history is empty; approximately `<floor>^(1/k)` whenever <factor> is zero. No gate
> may read it.

Then state the consequence for fixes: a control that depends on this scalar depends on whether the
caller happens to have prior rows in one table — i.e. on a history accident rather than on intent or
identity.

---

## 9. Trigger table — old skill name → new mode (an agent remembering the old name lands here)

| Predecessor skill | Land in | Its distinct trigger phrases |
|---|---|---|
| `audit/control-integrity-audit` | **MODE-CONTROL-INTEGRITY** | auditing whether a control really enforces; a control claimed to be in force — gate, validator, health check, sandbox, seal, drift detector, shadow mode, authority check, privacy filter, promotion ladder; before repairing anything described as a guard; before trusting a label a guard produced |
| `audit/declared-vs-enforced-control-audit` | **MODE-DECLARED-VS-ENFORCED** | a service claims a control you must verify; "requests to this endpoint require X" — approval gate, signature, scope check, deny list, rate limit, authorization tier; a spec/docstring/client library/proposal template describes a control you are about to repeat to a human; the claim lives in one layer and the enforcement in another |
| `governance/control-mechanism-audit` | **MODE-NAMED-MECHANISM** | a named control may not actually enforce; "a name may never claim a mechanism it does not have"; rename before fix; false absence / null-result control search; the failure-shape family (decoy, constant metric, label over measurement, default ≠ wall, import-without-use, stale seal, configured ≠ delivered) |
| `governance/named-mechanism-audit` | **MODE-NAMED-MECHANISM** | is this actually enforced; does this gate work; verify this safeguard; the control is present; privacy filter is on; 0 rejections; gate passed; is this wired up; verify a claimed control; false name; named but not installed; hardcoded metric |
| `audit/name-requires-mechanism` | **MODE-NAMED-MECHANISM** | auditing whether a named control actually controls; no control-like name may be trusted without runtime causal evidence; SEMANTIC AUTHORITY intersection; fix must be in the causal path; UNBUILT is a valid verdict; receipt correspondence |
| `enforcement-coverage-audit` | **MODE-ENFORCEMENT-COVERAGE** | is this gate real; does the gate actually block; enforcement coverage; can this bypass the gate; who actually made this change; audit trail attribution; prevented vs detected; is the guard load-bearing |
| `governance/control-seal-verification` | **MODE-SEAL-VERIFICATION** | verifying a claimed result or sealing a control; "tests pass" / "the file is written" / "the guard is live"; hash manifest; unattended verifier; void guard; negative control for a verifier; configured ≠ delivered |
| `court-audit/proxy-verification-audit` | **MODE-PROXY** (its metrics/witness section became **MODE-METRIC-DERIVATION**) | auditing an auth/gate control for verification; a session gate; an authority band; a human-approval field; an allow/deny regex; any control whose name promises verification; a fix must be proven to close a bypass rather than to merely look closed |

---

## 10. Survival index — every metric formula, checklist item, red flag, worked example and falsification test from the eight predecessors

| Item | Source | Where it now lives |
|---|---|---|
| `SEMANTIC AUTHORITY = NAME ∩ CALL_PATH ∩ MEASURED_EFFECT ∩ BYPASS_RESISTANCE ∩ EVIDENCE` | name-requires-mechanism | §1.1 |
| `EFFECTIVE_CONTROL = CALLER ∧ EFFECT ∧ BYPASS` | control-mechanism-audit | §1.1 |
| Three proofs (CALLER / EFFECT / BYPASS) + how to obtain each | all | §1.2 |
| Reformulate-the-question table (gate / health check / sandbox / seal / safe / sending) | control-mechanism-audit, name-requires-mechanism | §1.3 |
| Evidence hierarchy: RAW OBSERVATION > MEASURED FACT > DERIVED STATE > REASON CODE > NARRATIVE LABEL | control-integrity-audit | §1.4 |
| Inverted hierarchy = ordering violation; `value or "SOME_CAUSE"` | control-integrity-audit | §1.4 |
| `PRODUCED != SCHEDULED != FIRED != DELIVERED != OBSERVED != ACKNOWLEDGED` | named-mechanism-audit | §1.5 |
| Classification vocabulary (DECLARED/PARTIAL/ENFORCED/VERIFIED/CONTRADICTED/UNBUILT/DORMANT/DECOY/DECORATIVE/FALSE_NAME/UNPROVEN/NEEDS WITNESS) | control-integrity-audit, control-mechanism-audit, name-requires-mechanism | §1.5 |
| UNBUILT and DORMANT must never be reported as PASS; vacancy vs strength | control-integrity-audit, control-mechanism-audit | §1.5 |
| STOP RULE (dormant/decoy; fix-shaped ≠ fix) | control-integrity-audit | §2 |
| Attestation validity + sole-writer / disjoint-file-set partition + append-only reconcile | control-integrity-audit | §2 |
| False-assurance count; counterexample reporting; one condition under which the audit is wrong | control-integrity-audit | §2 |
| Six-step declared-vs-enforced procedure incl. isolated loopback port + throwaway credential + tear-down | declared-vs-enforced-control-audit | §3 |
| "A rejection proves enforcement. A downstream error does not." | declared-vs-enforced-control-audit | §3 |
| `contract_probe.py` (spec schema, expect=allow/deny/any semantics, uniform-failure guard) | declared-vs-enforced-control-audit | `scripts/contract_probe.py` + §3 |
| Three decisive tests: can it refuse (grep recipe), DERIVED vs ASSERTED, who authored & benefits | named-mechanism-audit | §4.1–4.3 |
| 18-shape failure catalogue with decisive probe per shape | control-mechanism-audit, named-mechanism-audit, name-requires-mechanism, control-integrity-audit | §4 catalogue |
| Rename-before-fix worked renamings (`status_banner`, `delivery_default=off`, DORMANT header) | control-mechanism-audit, name-requires-mechanism | §4 |
| False absence: control-search-first, `-iname '*term*'` over `-name "TERM*"`, query-must-be-able-to-match | control-mechanism-audit, named-mechanism-audit, control-integrity-audit | §4 |
| Label states: PASS / FAIL / UNBUILT / UNPROVEN / NEEDS WITNESS; prove the check can fail | name-requires-mechanism | §4 |
| Receipts: correspondence not existence; re-derive hash; append-only corrections | name-requires-mechanism, control-mechanism-audit | §4 |
| REFUSED is a state; governance hold vs broken gate in governance vocabulary | named-mechanism-audit | §4 |
| Publish your own retractions in the same artifact; retraction replaces, never hedges | named-mechanism-audit, proxy-verification-audit | §4 |
| `EnforcementCoverage = gated paths / writable paths` + the prevention-denominator defect | enforcement-coverage-audit | §5 |
| Writable-path enumeration table (file API, shell/editor, SCM hook, test/build runner, gate's own config) | enforcement-coverage-audit | §5 step 2 |
| Opt-in-default measurement (2026-09-17, `skills.guard_agent_created` default False, docstring documents the bypass) | enforcement-coverage-audit | §5 step 2b |
| Call-site enumeration correction (`grep -rn "<decide>("`; unplumbed parameter vs missing policy cell; lane in the finding) | enforcement-coverage-audit | §5 step 2b |
| Unsatisfiable-remedy finding (remedy vs gate; file the defect against the remedy) | enforcement-coverage-audit | §5 step 2b |
| 29 findings / zero literals — check the verdict against the content before "false positive" | enforcement-coverage-audit | §5 step 2b |
| "Then stop" — a bypassable gate is a finding, not a licence to take the open path | enforcement-coverage-audit | §5 step 2b / §1.6 |
| Instrument falsification: 6 rules (positive control, dereference, de-metadata, number-with-method, re-probe, no self-reported sensor state) | enforcement-coverage-audit | §5 step 2c + `references/sensor-falsification.md` |
| Witness independence from the *evidence path*; different agent ≠ independent witness | enforcement-coverage-audit | §5 step 4 |
| Attribution provenance (shared VCS `user.name` is non-identifying; session-derived id + host + objective) | enforcement-coverage-audit | §5 step 5 |
| `CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive`; epistemic vs authority transitions; `ActualDiff ⊆ AuthorizedScope`; two escalations not one | enforcement-coverage-audit | §5 step 6 |
| Coverage output block (Protected set / coverage / verdict / attribution / witness / open defect) | enforcement-coverage-audit | §5 output |
| Verify-a-claimed-result 4 steps + harness rules (real entry point, no internals import, negative control, session-id pinning) | control-seal-verification | §6 Part 1 |
| Existence ≠ support | control-seal-verification | §6 Part 1 |
| `CONFIGURED != DELIVERED != INTENDED`; SENT+FAILED ledger pattern; UTC/local date-filter trap; id → meaning resolution; two-writer collision; recursion guard; report shape (verified/unverified/limits) | control-mechanism-audit, control-seal-verification | §6 + `references/seal-and-delivery-verification.md` + `references/sealing-a-control.md` |
| Seal = manifest (control + test, `expected_result`, measured hash) + unattended verifier with VOID GUARD + heartbeat + negative control that must fire; drift-visibility ≠ tamper-proofing; regenerate in the same act | control-seal-verification | §6 Part 2 |
| Boundary check tri-state PASS/FAIL/UNBUILT + self-test that can REJECT | control-mechanism-audit, control-seal-verification | §6, §1.5 |
| Six proxy shapes table with the falsifying input per shape; defect-chain mapping | proxy-verification-audit | §7 |
| Proxy procedure 6 steps (granting branch both routes, comment-vs-code, inject + diff pair, ordering via warnings vs errors, durable-artifact witness, patch → restart → prove load) | proxy-verification-audit | §7 |
| Fail-closed three paths + legitimate-session passes; keep the rejected parameter + `SELF_ATTESTED_..._IGNORED`; scan over-report filter; stash proof of pre-existing failures; never route around a gate; disclose censorship; retraction table | proxy-verification-audit | §7 |
| Derive-before-hypothesise 5 steps; floor constant `floor ** (1/k)`; `A*(1-P)*(1-X)` zero artifact; cold-start self-referential threshold; literal witnesses and the branch they live in; metric label template | proxy-verification-audit | §8 + `references/metric-derivation-discipline.md` |
| Decoy catalogue (12 shapes, tell + probe) and the positive control pattern (5 traits) | control-integrity-audit | `references/decoy-catalogue.md` |
| Delivery/seal/causal-path probe recipes, timezone conversion snippet, boundary-check recipes | control-mechanism-audit | `references/seal-and-delivery-verification.md` |
| Harness/manifest/verifier code, negative-control runbook, shared-control rules | control-seal-verification | `references/sealing-a-control.md` |

---

## 11. Support files

Copied from the eight predecessors at merge time (2026-09-19) so depth survives the collapse; each
original also remains (unmodified) in the frozen folders under `retired_to`.

- `references/decoy-catalogue.md` — from `control-integrity-audit`
- `references/seal-and-delivery-verification.md` — from `control-mechanism-audit`
- `references/sensor-falsification.md` — from `enforcement-coverage-audit`
- `references/sealing-a-control.md` — from `control-seal-verification`
- `references/metric-derivation-discipline.md` — from `proxy-verification-audit`
- `scripts/contract_probe.py` — from `declared-vs-enforced-control-audit`

## 12. Related

- `verify-work`, `claim-receipt-discipline` — verification-as-terminal-state and receipt binding.
- `synthesis-verification-gate` — claim classification for synthesis output (user-owned; propose
  changes rather than editing it).
- `agent-finding-verification` — verifying findings from another agent.
- `deploy-drift-verification` — disk truth vs process truth; load it when a fix must be proven loaded.
- `agent-exploration-discipline` — the null-result rule referenced by the STOP RULE.
- `forge-execution-governance`, `self-recurrence-guards` (GUARD 6) — service-level governance and
  attribution guards adjacent to §5.

DITEMPA BUKAN DIBERI.
