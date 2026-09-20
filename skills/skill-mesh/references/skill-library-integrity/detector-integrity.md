# Detector Integrity — auditing the instrument before you trust its number

Companion depth for the SKILL.md pitfalls on false-positive guards. Load this when you are about to
report a count from a check you or a sibling just wrote, or when a number from an audit does not
survive contact with the disk.

The governing assumption: **an instrument that measures a class of defect is subject to that defect**
until proven otherwise. A sensor that cannot fail reports safety. A counter whose name does not match
its question reports confidence. Both are silent.

---

## 1. Run the check you just wrote — an unrun gate is an absent gate

A verification script that raises on every invocation (unterminated string, bad import, misread flag)
produces no verdict and no failure anyone notices. Its existence implies the property is covered, so
the absence looks like safety.

Procedure after adding or editing ANY check:

1. Run it on a case whose answer you already know. The verdict must be the one you expect.
2. Confirm a `--strict`-style mode exits non-zero. A tool that only prints reassurance cannot fail.
3. Confirm the check is reachable: in version control, referenced from the skill body, and invoked
   by whatever is supposed to invoke it.
4. Prove it can FAIL. Feed it, or reason it against, a known-bad input and watch it refuse. A gate
   never observed failing has an unknown verdict domain.

A check that has never executed is not a weak check; it is a missing one that has been counted as
present. Prefer a smaller set of checks that have each been seen to fail over a broad set that has
only been seen to exist.

## 2. One word, two counters — name the question

Two instruments in the same house can both report something a reader would call "duplicate
identity":

| Question the counter answers | Typical reading |
|---|---|
| How many identity keys overlap ACROSS surfaces? | a cross-surface overlap measure, in the hundreds |
| How many routing names have bodies that DIFFER? | genuinely unloadable capabilities, usually zero |

They differ by more than an order of magnitude, and quoting either under the other's name yields a
figure that **cannot be falsified from outside** — the reader supplies their own definition of the
word and every later audit appears to contradict you.

Rule: before quoting a field, read the code that increments it. Then state the question it answers in
the same sentence as the number. If you cannot name the question in one clause, you do not yet know
what you measured.

Corollary for prose: a word like "duplicate", "drift", "stale", "unused", or "broken" in a summary
must carry its instrument or it is a claim about your own vocabulary, not about the system.

## 3. Publish the before/after, or the audit manufactures work

Every audit of this class gets rerun and its first number is always too large. Report, together:

- the raw count BEFORE the guards were applied,
- the count AFTER, per guard, with one clause naming what each guard removed,
- the rescue count — entries the first pass called defective that a corrected extractor resolved.

Without the before/after, a successor reading the corrected number cannot tell whether the detector
was fixed or the threshold was moved. Without the rescue count, the audit reads as a machine for
producing work that does not exist.

## 4. A lineage claim needs the same warrant as the number

When you attribute a figure to an ancestor ("this came from last week's audit", "already resolved in
that commit"), you have made a second claim that nobody will re-check, because it is attached to a
number they already accepted.

Verify before attributing:

- the **date** of the commit or document you name, read from it, not from memory;
- the **count** it actually states, read from it, not from your recollection of it;
- that the ancestor counted the SAME thing. An ancestor that counted collisions *inside* one tree
  does not establish descent for a counter that measures overlap *across* trees.

If those three do not line up, the honest output is a named gap, not a genealogy. An ancestry claim
that skips this is the very defect it is trying to explain, reproduced one level up — and the
correction of a correction is where it hides.

## 5. Borrowed bodies — the store can publish what it does not hold

An address inside the store may resolve to a body that lives elsewhere (a runtime profile, a vendor
checkout, an archived tree). The store then advertises a capability it cannot guarantee: move the
borrower and the entry silently empties.

This is cheap to sweep and it is a countable class, so it belongs in the report rather than in a
footnote: resolve every entry, compare the resolved path against the store root, and publish the
count separately from the collision count. They are different questions (see §2) and merging them
inflates whichever number is quoted first.

## 6. Retracting a delivered claim

When a number that already reached a human is withdrawn, the correction must travel the same channel
the claim travelled. A retraction that stays on disk leaves the recipient holding a withdrawn
statement while every local surface reads as corrected.

Two shapes to keep:

- **Write the correction as a standing artifact beside the original, not over it.** A delivered
  artifact is a record of what was said; editing it in place destroys the ability to audit the
  delivery.
- **Keep your own retraction visible.** If the first correction was itself wrong, state that inside
  the correction rather than silently rewriting it. A correction that hides its own retraction is the
  same failure class as an instrument that cannot fail.
