---
name: enforcement-coverage-audit
description: "Use when auditing whether a control actually controls."
version: 1.0.0
owner: AAA
risk_tier: medium
autonomy_tier: T1
triggers:
  - "is this gate real"
  - "does the gate actually block"
  - "enforcement coverage"
  - "can this bypass the gate"
  - "who actually made this change"
  - "audit trail attribution"
  - "prevented vs detected"
  - "is the guard load-bearing"
floor_scope: [F1, F2, F11]
---

# Enforcement Coverage Audit

A control's block-rate on the traffic it sees says nothing about whether it covers the paths that
can actually mutate the thing you are protecting. This skill audits the *reach* of a control, not
its verdicts — and audits whether the evidence trail about a mutation is attributable at all.

Sibling skills (load them too; do not duplicate their content here):
- `forge-execution-governance` — alive ≠ governed; listing ≠ calling; a structural zero is not a
  measurement. That is SERVICE-level governance; this skill is CONTROL-level coverage.
- `self-recurrence-guards` GUARD 6 — attribution guards for claims about events and actors.

## Core equation

```
EnforcementCoverage = paths that intersect a gate / paths that can write protected state
```

A gate that blocks 100% of the attempts routed to it, while covering 1 of N write paths, has
`PreventedUnauthorizedRate → 1.0` and `UnauthorizedEscapeRate → 1.0` simultaneously.

**The prevention metric's denominator only contains attempts the gate observed.** An attempt that
bypasses the gate is *not in the denominator* — so the rate reads perfect while the escape happens.
Report coverage alongside prevention, or report neither.

## Procedure

### 1. Name the protected set before naming the control

Write down the actual targets: authority/config files, canonical registries and records, governance
documents, secrets, production state, and the control's own configuration. If the protected set is
not written down, coverage cannot be computed and the audit is theatre.

### 2. Enumerate EVERY path that can write, then probe each one

Do not audit the intended path. Enumerate the possible ones:

| Path | Probe |
|---|---|
| Direct file API / interpreter | write the target from a tool call or one-liner; observe whether anything refused |
| Shell redirection / editor tool | append to the target; save from the editor into the tree |
| Version-control boundary | stage + commit the target, and watch whether a hook fires (`ls -l <repo>/.git/hooks/`, then read what the symlink target actually runs) |
| Test / build / migration runner | anything that writes outside the normal edit flow |
| The control's own config | if the gate's rules are writable by the actor it constrains, coverage is zero by construction |

A hook that exists is not a hook that fires: read what each hook invokes and confirm the invoked
script is present and executable. An unwired engine is a library with no callers —
`grep -rl <engine-name>` across the live runtime, plugins, and harness configs. Zero hits means it
gates nothing, however complete it looks.

### 3. Compute coverage explicitly

```
Coverage:  <gated paths> / <writable paths> = <ratio>
Uncovered: <explicit list>
```

If any uncovered path is reachable by the actor under audit, the control is **advisory, not
enforcing**. Say that plainly — "policy in language" is the accurate description, and it is a
finding, not an insult.

### 4. Verify the mutation from evidence the executor does not control

Never accept a completion report as proof a change landed. Read the artifact: version-control
log/diff for tracked state, hash or mtime for untracked state, the live endpoint for deployed state.

A witness that reads the executor's own success log is not an independent witness. Independence
comes from the *evidence path*, not from using a different agent: probe the deployed hash, the
external endpoint, or the observed behaviour directly. Different agent ≠ independent witness.

### 5. Check whether the trail can name the actor at all

Before trusting any attribution recorded in a ledger, open the ledger and find where the actor
field comes from.

- A repo-level VCS `user.name` is ONE value shared by every session, harness, and lane writing to
  that repo. Changes minutes apart from different actors all carry the same name. **Authorship read
  from a shared config value is non-identifying.**
- The correct source is session-derived — session id + host + objective — captured at the write
  boundary by the boundary itself, not self-reported by the writer.
- If the ledger attributes several actors to one name, the trail is corrupted at the source and
  every later forensic read inherits the error. Report the defect; do not paper over it by guessing.

### 6. Keep epistemic resolution and mutation authority separate

Coverage work routinely surfaces an adjacent collapse. State the separation explicitly:

- `UNKNOWN → RESOLVED` is an epistemic transition. `RESOLVED → MUTATED` is an authority transition.
  Neither implies the other.
- `CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive`. Confidence is
  deliberately absent from that conjunction and must not be smuggled into it.
- "I should not bother the owner with this" is never a grant. The more capable the actor, the *less*
  its permissions may depend on its own agreement with them.
- Never author the envelope that constrains you: if the authority governing a mutation would be
  written by the act that needs it, that is a self-grant → HOLD.
- Scope is checked against the diff, not the intent: `ActualDiff ⊆ AuthorizedScope`, computed from
  what would actually change.
- Two escalations, not one. Asking the owner to **choose** among facts the machine can resolve is a
  defect — resolve it. Asking them to **authorize** what only they may authorize is correct — route
  it as a binary decision, never as a work handoff.

## Pitfalls

- **Auditing the intended path and calling it coverage.** The control is usually installed on the
  polite route. Probe the impolite ones — a one-liner, a redirect, the SCM boundary — before saying
  "the gate blocks it".
- **Reporting a prevention rate without a coverage ratio.** See the core equation: with partial
  coverage the rate is arithmetically perfect and operationally meaningless.
- **Treating a complete-looking control as wired.** Read for callers. A large engine with zero
  invocation sites in the live runtime protects nothing.
- **Trusting a ledger's actor field because the field exists.** Check its provenance; a shared
  config value produces confident, wrong attribution.
- **Accepting an incident attribution from a report without checking provenance** — including
  accepting blame for it. A wrong attribution is the same error as a wrong fact, one layer out, and
  a trail naming the wrong actor teaches every later reader to read it wrongly.
- **Becoming the enforcement.** If the audit finds the boundary must live outside the actor's
  reasoning, that is a finding for the owner of the enforcement path — not a mandate to write your
  own authority envelope.
- **Concluding "nothing to fix" from an absence of attempts.** No observed attempt ≠ no reachable
  path. That is a structural zero; the reachable-path enumeration is the evidence, not the traffic.
- **A gate's rule list is itself a mutation target.** Confirm the protected set appears in it; a
  forbidden-target list that omits the governance tree gates exactly the wrong things.

## Output

```
Protected set:        <targets>
Enforcement coverage: <gated>/<writable>    Uncovered: <list>
Verdict:              ENFORCING | ADVISORY | ABSENT
Attribution:          IDENTIFYING | NON-IDENTIFYING (source: <where the actor field comes from>)
Witness:              independent evidence path used, or UNWITNESSED
Open defect:          the smallest concrete fix, addressed to the owner of the enforcement path
```

DITEMPA BUKAN DIBERI.
