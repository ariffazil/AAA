# Gate integrity — writing, repairing, and verifying an enforcement gate

Applies to anything that blocks work: lints, pre-commit hooks, claim scanners, policy guards,
secret scanners, CI gates, tripwires.

## Rule 1 — A lexical detector cannot see enclosing scope

A regex or grep that matches a token will fire on that token wherever it appears. It reads a
*string*, not a *construct*. Four shapes it gets wrong — three false positives and one false
negative, all from the same blindness:

- **Inside a comment or docstring.** Prose that *describes* the forbidden pattern matches the
  pattern. A file whose comment explains the rule trips the rule.
- **Inside a string literal or test fixture.** Sample payloads and fixtures are not production
  violations.
- **Inside a negation.** A detector keyed on `sealed` matches the sentence "this file is not
  sealed" — and reports the exact opposite of the truth.
- **Covered by an in-file binding.** A construct illegal in one module shape is legal when the
  file binds an equivalent first. An ESM file that builds a `createRequire` shim and then calls
  `require()` is correct code that a bare `require\(` grep will flag. The detector must check
  whether the binding exists in the file before flagging the call.

**Rule:** when a detector fires, open the file and read the construct in its enclosing scope
before calling it a violation. When you author one, decide which shapes it must tolerate and
write a case for each.

## Rule 2 — Negation is the cheapest false positive to test for

Before shipping any keyword detector, feed it the sentence that asserts the *opposite* of what it
looks for. If the trigger word is `sealed`, then "not sealed", "never sealed", "unsealed", and
"sealed-off" must all fail to match. Strip comments and string literals before matching, or match
on an assertion shape rather than a bare word.

## Rule 3 — Widening a gate that is blocking your own work needs negative controls

A gate is most likely to be wrong at the exact moment it blocks you, because that is when the
motive to loosen it exists. Loosening without proof silently disarms it.

- A test suite proves nothing unless it contains **inputs that MUST pass** as well as inputs that
  MUST block. Must-block cases alone cannot distinguish a correct gate from a gate that permits
  everything.
- **Quote the count.** "N must-block, M must-pass, all correct" is re-runnable by someone else.
  "I tested it" is not.
- After widening, re-run the original true positive. A widening that removes the case the gate was
  built for is a regression wearing a bug-fix costume.

## Rule 4 — A fix is not landed until it is on the path the enforcement actually takes

An engine file sitting next to the text it governs does not mean the *runner* reads that path.

- **Read the caller first.** A hook invoked with an **absolute path** ignores your edit in a git
  worktree, a branch checkout, or any other copy. Editing the file you have open, when the hook
  names a different absolute path, changes nothing at all.
- Repair sequence, in order: (1) locate the invocation, (2) confirm the path it resolves, (3)
  re-run the gate on the payload that was previously blocked, (4) confirm the block clears — and
  separately confirm a must-block payload still blocks.
- This failure is silent in both directions. A fix that never landed looks like a fix; a checkout
  that reverted a live gate looks like a passing gate. What is *enforced* is the on-disk file, not
  the git state.

## Rule 5 — Do not merge around a dirty tree; isolate

When the working tree is dirty from work you do not own, do not stash, revert, or commit another
lane's in-flight files to clear the way.

- `git worktree add /tmp/<name> <branch>` gives a clean checkout of the target branch on a
  separate path. Merge and push from there; the other lane's work is untouched.
- After any branch switch, re-check whether the live enforcement file survived it.

## Rule 6 — An exemption must be counted, never silent

Every bypass branch — whitelist, path scope, ops-tree exemption, declared risk class — is a hole.
It is acceptable only if it reports: emit a counter or log line per exemption so the bypass stays
auditable. An uncounted exemption is indistinguishable from a missing check.

## Audit clause — the gate's own telemetry is a claim too

When a gate reports "N violations, M exempt," both numbers are claims. An exemption class that
swallows the majority of violations means the check is decorative — the pass rate is measuring the
waiver, not the control. Also check whether the gate is *enforcing* or merely printing: a check
that reports violations and exits 0 has never blocked anything, and its long green history is
noise.
