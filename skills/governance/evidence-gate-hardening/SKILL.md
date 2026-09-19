---
name: evidence-gate-hardening
description: "Use when a validation gate accepts anything non-empty."
version: 1.0.0
owner: F13
risk_tier: high
triggers:
  - "gate accepts anything non-empty"
  - "a HOLD flipped to PASS with no new evidence"
  - "audit a validator"
  - "harden a check"
  - "the gate passes when it should reject"
  - "false rejections after tightening a gate"
  - "evidence / proof / source accepted without resolution"
  - "a verdict tool that can be talked past"
  - "is this control real"
tags: [governance, validation, evidence, audit, adversarial, gate, verification]
---

# Evidence-Gate Hardening

**The class.** Any check whose job is to decide *whether evidence exists* before permitting something:
a promotion firewall, a consent gate, a cross-layer bridge, a claim adjudicator, a memory-write
permission, a seal precondition. This skill is the procedure for reproducing its bypass, fixing it
without breaking legitimate use, and reporting it honestly.

**Why gates fail this way.** They are written to answer *"was the field supplied?"* because that is
the cheap question, and non-emptiness is a one-line predicate. But supplying a field and *having*
evidence are different states, and the gap between them is where every finding below lives.

---

## 1. Measure before you fix

Never edit a validator on the strength of a code read. Produce the flip yourself, in one call, and
keep the output — it is both the receipt and the regression fixture.

```
call the validator directly with a control input that SHOULD reject, and print the verdict
call it with a control input that SHOULD pass, and print the verdict
```

If both return the same verdict, you have found the defect. If the reject-case returns a *different*
rejection than the one you expected, read the real reason before assuming your diagnosis — a
malformed-input branch will mask the logic you are hunting.

**Then ask the question that decides the whole fix:** which side of the predicate is load-bearing?
Validate one side at a time by holding the other constant. A gate usually has two or three
independent fields, and fixing the obvious one only moves the bypass to a neighbour.

---

## 2. The defect class — grep for it

The shape to search for, in any language:

```
bool(x)            bool(x and str(x).strip())            if x:            if len(x):
```

Report every hit where `x` is named `evidence`, `proof`, `source`, `bridge`, `receipt`, `witness`,
`grounding`, `consent`, `observation`, `alternatives`, `verification`. Also flag:

- **Optional parameters whose only gate is truthiness** — these are the bypass surface: a caller who
  omits the field skips the check entirely. An opt-in gate is not a gate.
- **Length-based proxies** — a rule satisfied by a *count* ("at least three alternatives") is
  satisfied by three junk strings. Test it with `["a","b","c"]` and say so if it passes.
- **Constant verdict payloads** — a block asserting what was checked (`witness`, `verified`, scores
  like `dS`/`peace2`) assembled from literals rather than computed. A bypassed verdict must be
  *distinguishable* from a witnessed one; if the payload is constant, it is not.
- **Echo fields** — the caller's own input returned under a name that reads like a finding
  (`"bridge_evidence": bridge_evidence`). Rename to `..._as_supplied` and say what it is.
- **Single-word HOLD suppressors** — a check asking whether the text *mentions* the missing thing
  (`"bridge"`, `"we both agree"`, `"consent:"`). Test by appending the word and watching the
  violation disappear.
- **Fail-open defaults on a stricter sibling** — two functions for the same decision where only the
  permissive one is wired in. Grep for the fail-closed implementation and check whether anything
  imports it.

---

## 3. The exploit battery

Run every row. A gate is only as strong as its weakest accepted string.

| Probe | What it tests |
|---|---|
| `"NONE OFFERED. No evidence was supplied."` | an explicit *absence statement* counted as evidence |
| `"n/a"`, `"tbd"`, `"null"`, `"x"`, `" "` | placeholders and whitespace |
| `"rcpt-anything-i-type"` | a shape-valid, unresolvable identifier |
| `"deadbee"` | a hex-shaped token that is not a real commit |
| a path that exists but lies outside the evidence roots | whether path checking is scoped |
| a URL that 404s, and a domain that does not resolve | whether the anchor is fetched at all |
| the negation pushed past the checker's scan window | a prefix-only absence scan |
| **the gate's own rejection message, fed back as input** | self-laundering — see §5 |
| a well-formed legitimate control | whether the fix cost you real coverage |

---

## 4. Fix: resolve, don't match

The replacement pattern is **resolution**: an anchor counts only if a read-only lookup confirms it
against reality.

| Anchor | Resolves when |
|---|---|
| absolute path | exists **and** sits under an allow-listed evidence root |
| receipt / claim id | appears as an **identifier field** in a readable ledger — not as free text |
| URL / DOI | `HEAD` returns status < 400 (never fetch a body) |
| commit sha | `git cat-file -t <sha>` succeeds, or the sha appears in a local evidence tree |
| `verbatim: "<quote>"` | the quote is found, whitespace-normalised, inside a named corpus file |
| declared observation | names all three of class + observer/instrument + timestamp |

**Fail closed.** When the resolver cannot reach reality — no network, ledger unreadable, repo absent —
that anchor does **not** resolve, and the reason string must say so (`network unavailable — cannot
resolve`), never imply success. Cache per call so no page is fetched twice, and keep every lookup
read-only: no writes, no restarts, no mutating calls.

**Declare a legitimate anchor-free form.** Real evidence often has no file, URL or id — a direct
observation with an instrument and a timestamp is evidence. If the gate cannot accept it, honest work
starts routing *around* the gate, which is worse than the original bug. Give that form an explicit,
reviewable shape and document it. Do not whitelist the specific strings that failed.

**Widening the read surface is a decision, not a detail.** Adding a root, a ledger or a corpus to a
resolver's scope grants the gate new reach over private data. Treat it as a separate, receipted act.

---

## 5. Pitfalls that cost real time

- **Self-laundering.** A gate that logs its refusals, plus a resolver that searches those logs, will
  verify its own invented ids on the next call — you can watch it flip to ALLOW. Search identifier
  *fields* in ledger records, not free text across the log. This is the most surprising defect in
  this class.
- **Path-scoped evidence.** `os.path.exists()` alone passes a real file that carries no evidence for
  any claim in the system. Scope to roots deliberately.
- **Anti-loosening.** Tightening one field while silently relaxing another is not a fix. Re-run both
  contracts (must-reject *and* must-accept) after every change and print both.
- **Editing the fixtures instead of the rule.** If legitimate evidence now fails, fix the *acceptance
  rule* to admit the evidence class; do not edit the test's inputs to match the new gate. A test
  edited to pass proves nothing.
- **Stale running code.** Your fix on disk is not your fix in production. Compare the process start
  time against the file mtime of every module it imported, and check which surface reads what. A
  health endpoint and a CLI can call the same function and still disagree, because they hold
  different versions in memory.
- **Retracted numbers still served.** A value the ledger has voided will keep being served by any
  long-lived process started before the retraction. After a repair, search for surfaces still
  quoting the withdrawn figure.
- **A malformed branch masking the logic.** Validate field and layer names through the same function
  you are testing, or an early return will hide the bug you are chasing.

---

## 6. Prove the fix — three conditions, simultaneously

All three must hold at once. If they cannot, report which one is impossible and why; never weaken one
silently to satisfy another.

1. Every probe in §3 **rejects**.
2. Every legitimate positive control still **passes** — and the pre-existing suite is green, not
   reduced.
3. The fix is **non-vacuous**: run the new tests against a pre-fix copy of the module and confirm
   they *fail* there. A test that passes against both versions is not testing the fix.

Then verify the claims of whoever wrote the fix yourself. A subagent's summary is a self-report: run
the suites and the probe battery from your own shell, and compare the file hashes it quoted against
the hashes on disk. Report `PRODUCED` / `TESTS-GREEN` / `DEPLOYED` / `BLOCKED_AT_GATE` as distinct
states — a patch that is green but not running is not done.

**Dispatch the fix and the audit separately.** One agent writes the change; a different one sweeps the
same defect class read-only across the rest of the surface. An agent auditing its own fix finds what
it already believes.

---

## 7. Reporting this to a human

A gate audit is a report to a person, so it obeys the human-facing register rules, not an engineer's
log format. No findings table, no severity list, no numbered register into chat.

- Lead with the **consequence**, not the pattern: what the gate let through, and what that costs.
- Name the **one decision** waiting on him, and say plainly if it can wait.
- State the **state reached** for each artifact — separate what is written from what is running from
  what is sealed.
- **Never mark work done because it is green.** Green tests plus un-deployed code plus an unopened
  gate is not completion. Say so, and name the open items.
- Report every residual defect the audit found but did not fix. An audit that quietly carries nine
  unfixed criticals while presenting one clean fix is the same failure the audit was looking for.

DITEMPA BUKAN DIBERI ⚒️
