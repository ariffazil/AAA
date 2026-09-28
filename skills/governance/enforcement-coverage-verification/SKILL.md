---
name: enforcement-coverage-verification
description: "Use when verifying a gate enforces on all paths."
version: 1.0.0
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T1
tags: [audit, enforcement, boundary, chokepoint, mediation, verification]
triggers:
  - "chokepoint"
  - "complete mediation"
  - "the gateway is the only route"
  - "direct invocation is DENIED"
  - "no path bypasses"
  - "enforcement coverage"
  - "is this control real"
  - "guard script"
  - "wrapper vs boundary"
  - "all paths pass through the gate"
  - "acceptance suite passed"
  - "citizens can no longer bypass"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Enforcement Coverage Verification

> **Law:** every path to protected state passes the gate, or there is no property — only ethics
> suggestion. The question is never *how many attempts did the gate block?* but *do all paths that
> can change protected state pass through the gate?*

## When this applies

Any claim of the form: *"direct invocation is DENIED"*, *"citizens can no longer bypass X"*,
*"the gateway is the only route"*, *"enforced end-to-end"*, *"true chokepoint"*. Also whenever a
build report presents a green acceptance suite for a newly written guard.

## The three properties

A control carries three independent properties. An acceptance suite usually measures only the
first, and a report that measures the first while claiming the third is the failure this skill
exists to catch.

| Property | Question | Probe |
|---|---|---|
| **Correct when called** | does it deny when invoked, with well-formed input? | call the gate directly with real parameter names taken from its own schema — a malformed call tests the schema, not the boundary |
| **On every path** | can a caller reach the protected thing without it? | run the intercepted command normally; `type -a <cmd>`; `readlink -f` every hit; check PATH shims, aliases, shell rc files; grep who calls the underlying binary |
| **Physically enforced** | can the actor acquire the capability regardless? | inspect the credential itself — owner, mode, and whether the caller already shares that identity |

Name which of the three you proved. `CONVENTION_GATE` (actors comply voluntarily, audit-logged) and
`CHOKEPOINT` (no path avoids the check) are different verdicts; reporting the first as the second
is a transition lie.

## Scope — which object does the gate actually validate?

Coverage asks *can a caller avoid the gate?* **Scope asks which object the gate examines.** A gate
can have perfect coverage of an object that is not the one in production, and it will sign for it.

Do not accept the verdict; enumerate the gate's subject set and compare it against what production
serves:

```bash
# iterate EVERY declared subject (profile / class / target) and record which ones the gate checks
for subject in $ALL_DECLARED; do
  printf '%s gated=%s\n' "$subject" "$(<does the gate validate this one?>)"
done
```

Measured: a deploy gate validated one profile (6 tools) and printed `✅ registries consistent`,
while the wire served a different profile (8 tools) — the execute verb and the durable-write verb
sat outside its scope. Running the same gate over all six declared profiles returned **one `GATED`,
five `UNCHECKED`**. A gate narrower than the surface is worse than no gate, because it *signs*.
Report `SCOPE` alongside coverage; `GATED` and `UNCHECKED` are different verdicts and must never be
merged into one green.

## Procedure

1. **Read the guard, then find its callers — not its tests.**
   ```bash
   grep -rn "<guard_file>" /root/<organs>/ 2>/dev/null | grep -v __pycache__
   ```
   If the only hit is the verifier script that calls the guard by absolute path, the guard has no
   production caller. That is the finding.

2. **Run the intercepted command normally.** Not through the guard — through the shell, from the
   normal PATH, the way a citizen agent would.
   ```bash
   <cmd> <subcommand> <args>
   echo "exit=$?"
   ```
   This single probe is the whole audit. Do it before writing any verdict.

3. **Resolve the command identity on every PATH entry.**
   ```bash
   type -a <cmd>
   readlink -f $(command -v <cmd>)
   ls -la /usr/bin/<cmd> /usr/local/bin/<cmd>
   ```
   A shim installed somewhere off-PATH, or a wrapper that is not first in PATH order, enforces
   nothing. Absence of a shim plus a working direct call = bypass open.

4. **Grep who actually invokes the protected tool.** A gateway that shells out to the bare binary
   has already bypassed its own guard. Mediation is complete only when the enforcing path is the
   *only* path.
   ```bash
   grep -n "subprocess\|cmd = \[\|<binary>" <gateway>.py | head -20
   ```

5. **Check the identity boundary.** If every actor runs as the same Unix user and that user owns
   the credential store or the executable, no process can be blocked by a sibling process. There is
   no same-UID isolation to install. Say so plainly, and treat the real fix as identity separation
   (dedicated service user + mode-700 store + socket or RPC hop), not another wrapper file.

6. **State the verdict with the property you proved.** Include the probe command and its output.
   Anything not probed is `UNKNOWN`, not `PASS`.

## Pitfalls

- **The tautological test.** A suite that does `run_cmd(["bash", guard, "gmail", ...])` and asserts
  `exit == 13` proves the guard returns 13 when called. It cannot discover a bypass, because it
  never attempts one. Grep the suite for how it reaches the control before trusting its green.
- **Do not report a client-side artifact as server breakage.** A stdio/pipe probe that writes every
  request at once and reads at the end will report a closed connection for tools that work fine.
  Re-drive it one request at a time before concluding anything is broken.
- **Asserting both halves in one report.** When a write-up says in one section *"this is only a
  convention gate, not a physical chokepoint"* and in another *"this is now a true chokepoint"*,
  the two contradict. The stronger half is not licensed by the weaker half appearing first —
  resolve the contradiction before repeating either.
- **A file that exists is not a control that runs.** Guard script present + guard never on any
  execution path = `DOCTRINE_PRESENT / ENFORCER_ABSENT`. Report both halves honestly; this is the
  most common shape.
- **Probe coverage decays.** Another agent can re-point the binary, add a PATH entry ahead of the
  shim, or move the credential. Stamp the probe with a timestamp and re-run it before publishing a
  sealed verdict.
- **A workflow that runs is not a control that binds.** A CI gate is enforced only if it appears in
  the branch's required status checks:
  ```bash
  gh api repos/<owner>/<repo>/branches/<branch>/protection --jq '.required_status_checks.contexts'
  ```
  A check whose name says mandatory but which is absent from that list is *advisory red*: pushes
  land anyway, and the red X reads as enforcement to everyone who never opened the list. Check the
  list before describing any CI gate as binding.
- **A gate whose reporter crashes fails blind.** When a check fails, confirm it printed the
  *offending item*, not merely a count. A diagnostic path that throws on its own input emits
  `❌ N finding(s)` followed by nothing — unreadable, and indistinguishable from a gate that found
  nothing real. Re-run the checker locally against the checkout and read the findings list before
  relaying its verdict. Concrete instance: `sorted(pairs)` where each pair is
  `(filename, dict)` raises `TypeError: '<' not supported between instances of 'dict' and 'dict'`
  as soon as one file has two findings; sort with an explicit key
  (`key=lambda x: (x[0], x[1].get("line_number", 0))`). The lesson generalises: any sort over
  tuples holding a mapping crashes on the duplicate-prefix case, which is exactly the case a
  reporter must handle.
- **One check, two code paths, two scopes.** A check that branches on environment (inside a git
  working tree vs not, CI vs local, repo present vs absent) must carry an identical exclusion and
  scope list in every branch. Divergent lists yield contradictory verdicts on the same tree — the
  same run PASSes outside the repo and FAILs inside it. Diff the branches' exclude lists before
  trusting either verdict, and never widen one branch's scope to clear a red on the other.

- **A denial from a malformed payload is not evidence the gate holds.** An empty or wrong-shaped
  argument set fails *schema validation*, and schema validation returns the same terse refusal an
  authority gate does. A boundary "tested" that way has not been asked the question. Pull the real
  parameter names from the control's own schema first, send well-formed input, then read *what the
  refusal cites*: a named floor, an unverified identity, a missing session, an authority class, a
  required human witness — that is a boundary verdict. A validation error is not a verdict at all,
  and reporting it as "the gate blocked it" credits the boundary with work the schema did.
- **Prove the gate discriminates, not merely that it denies.** A gate that refuses everything passes
  *did it deny?* while being indistinguishable from a broken one. Run a counterfactual control: the
  legitimate operation the gate is supposed to permit must actually succeed on the same surface, in
  the same session, before you call the denial enforcement. Denial alone is half a test — without
  the allow case you cannot separate enforcement from outage, and you will not notice the day the
  gate starts refusing its intended callers.
- **Read the refusal's numbers, not the operator printed beside them.** Generated justification text
  is formatted by the same code path that produced the decision and can invert it — a failed
  threshold rendered with a satisfied-looking operator (`score: 0.960 >= 0.99` against a 0.99 floor).
  Re-derive each cited comparison yourself before reporting the gate as having passed or failed a
  specific floor; a floor that failed is what makes the gate credible, so misreading it as a pass
  both flatters the control and hides a real finding.
- **Name the layer that actually refused.** When a stack has several gates, the refusal you received
  may come from an outer floor rather than the one under audit — and a control that appears to deny
  may simply be downstream of a different control that denied first. Read the full reason list and
  attribute the denial to the specific floor that fired, then report the others as *also satisfied*
  or *not reached*, never as one merged score.
- **A gate placed after the mutation cannot fail-closed.** Record where the check sits in the
  sequence relative to the write it guards (stamp write, service restart, deploy). If it runs
  *later* than the change, its failure arrives with the change already live — it is a report, not a
  gate. Read the line numbers, not the step's name: a step numbered `5.5` can still execute after
  step 6. Order is verify → mutate → observe; a check that runs third is decoration.
- **Audit the failure posture of every branch, including the ones a normal call cannot reach.** A gate's
  `except` arms are the boundary under load: unavailable dependency, failed import, timeout, degraded
  mode. A soft-pass arm (`except ImportError: return passed=True`) converts *not evaluated* into
  *passed* while the pipeline still emits a pass-shaped result — so "N floors active" silently becomes
  "N floors not checked", with nothing red anywhere. Grep the control for every `except` and read what
  each arm returns. A gate is only as strong as its weakest failure arm, and the happy path never
  exercises it, which is why a direct call to the gate reports PASS.
- **Compare sibling gates in the same module for posture consistency.** Measured: one module's primary
  gate returned `passed=True` on `ImportError` while the neighbouring gate in the same file returned
  `passed=False` with a written `FAIL-CLOSED` comment for the same class of condition. Both were
  deliberate; only one was right for that action class. The inconsistency *is* the finding, and the
  in-repo precedent is the argument — cite the sibling gate's own comment when proposing the fix
  rather than inventing a new policy from outside.
- **Separate LATENT from LIVE before reporting severity.** Having found a fail-open arm, probe whether
  it can fire today — import the module, resolve the dependency, inspect the packaged artifact — and say
  which you found. An arm that cannot currently trigger is a latent defect to fix on a branch;
  describing it as a live outage is the same class of overclaim as calling a convention a chokepoint.
  The converse also holds: "it imports fine here" does not clear it, because the arm exists for the
  environment you did not test — partial install, omitted optional dependency, broken packaging.
- **One "value belonging to a different object" is a family, not an incident.** When a surface
  reports a neighbouring object's state, sweep the whole family before stopping. Three instances
  measured in one session: a deploy stamp taken from the source tree's `git HEAD` rather than the
  built artifact; a gate keyed to a profile other than the served one; an exit status read through a
  pipe. The generalisation: **every surface that reports state must be asked *of which object is
  this a fact?*, and the answer must be the object its reader cares about.**
- **Never read exit status through a pipe.** In `cmd | tee log`, the reported status is *tee's*. A
  failed command is recorded as success by every caller that reads the pipeline status — use
  `${PIPESTATUS[0]}`, or avoid the pipe. Reproduce it once before trusting any harness that reports
  exit codes for piped work: `bash -c 'exit 1' | tee /dev/null` reports `0`.
- **A field that compares two artifacts to each other reports `aligned` by construction.** A drift
  field computed as *built vs live* reads `aligned` whenever both derive from the same tree, even
  while the deployment sits several commits behind the canonical reference. Ask what the *reference*
  is; if the answer is "the other half of itself", the field cannot see the drift its name promises.
  Either add a comparison against the canonical reference or rename the field to what it measures.

## What the probe licenses

When the probe comes back thin — one path tested, one identity checked, the remainder unexamined —
the output must *shrink*, not grow. Thin evidence licenses exactly: the observation, the competing
readings, and the cheapest next discriminating test. It does not license a synthesis, and a longer,
more elaborate write-up over thin evidence is the failure rather than thoroughness.

Symmetrically, catching one fabricated or bypassed item licenses exactly one claim — *this* item is
not enforced. It does not license "nothing is enforced." An unchecked remainder stays `UNCHECKED`,
never refuted; the negative universal carries the same denominator obligation as the positive.

## Related

- Complete-mediation and authority-envelope doctrine (`CanMutate = AuthorityGranted ∧ ScopeMatches ∧
  TargetPermitted ∧ BoundaryActive`) — this skill is the *verification* half of that law.
- `claim-receipt-discipline` — receipt and denominator discipline for the verdict you emit; it is
  the natural home for the weak-signal rule above.
- `live-probe-audit-pattern` — narrative-vs-state audits and detector auditing more broadly.
