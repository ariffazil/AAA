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
| **Correct when called** | does it deny when invoked? | call the gate directly — exactly what its own suite tests |
| **On every path** | can a caller reach the protected thing without it? | run the intercepted command normally; `type -a <cmd>`; `readlink -f` every hit; check PATH shims, aliases, shell rc files; grep who calls the underlying binary |
| **Physically enforced** | can the actor acquire the capability regardless? | inspect the credential itself — owner, mode, and whether the caller already shares that identity |

Name which of the three you proved. `CONVENTION_GATE` (actors comply voluntarily, audit-logged) and
`CHOKEPOINT` (no path avoids the check) are different verdicts; reporting the first as the second
is a transition lie.

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
