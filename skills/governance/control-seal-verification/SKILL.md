---
name: control-seal-verification
description: "Use when verifying a claimed result or sealing a control."
version: 1.0.0
tags: [governance, verification, seal, integrity, drift, gate-hardening]
---

# Control Seal & Verification

Two jobs that share one law: **an assertion is not a state.** A reported result and a sealed control
both have to be checkable by someone who was not there.

## Part 1 · Verify a claimed result

Reports about your own system — "tests pass", "the file is written", "the guard is live" — are claims
of the same kind as any other finding. Probe them.

1. **Locate the artefact that makes the result repeatable.** A pass count is only a result if a
   harness exists that can produce it again.
2. **Confirm it resolves on disk.** If the name appears only in the session database, it is chat
   text, not a deliverable. The absence is the finding.
3. **Re-measure every cited number** — line numbers, counts, sizes, paths. One citation that is off
   means the rest of the citation set went unchecked too.
4. **Fix forward.** Write the missing artefact rather than reporting the gap back and stopping.

When you write the harness:

- drive the component through its **real entry point** (stdin / CLI / HTTP), asserting on observable
  output and exit codes;
- never import the internals you are testing — a harness coupled to implementation drifts with it;
- include a **negative control**: at least one case that must ALLOW, or "blocks everything" scores as
  a perfect gate;
- pin test traffic to a recognisable session id so receipts the test causes are filterable out of the
  real ledger.

**Existence is not support.** A pointer that resolves proves the citation *exists*, not that it
*supports* the figure beside it. Report the weaker, true claim — never "the numbers are verified"
when only the pointer's presence was checked.

## Part 2 · Seal a control

Presence is not seal, and a manifest nobody checks is decoration. Sealed means three things exist
together:

1. **Hash manifest** of the control *and its test*, measured not estimated; record `expected_result`
   so a future reader knows what green looked like.
2. **Unattended verifier** — silent when sealed, speaking only on drift. Include a **VOID GUARD**: if
   it cannot read its own manifest it must NOT exit clean, or a deleted manifest reads as healthy.
3. **Negative control proving the verifier fires** — inject drift, watch it alert, restore to the
   exact sealed hash, watch it fall silent.

Write the limit into the artefact itself: **drift-visibility is not tamper-proofing.** Anyone who can
read the manifest can regenerate it and pass.

Regenerate the manifest in the same act as any authorised change. A manifest that does not match its
artefact is worse than none — it manufactures trust.

Working code for all of this: `references/sealing-a-control.md`

## Pitfalls

- **Do not name artefacts after the words your own gate hunts.** An id or path containing a trigger
  term makes every later command that references it fail the gate. Pick a neutral name.
- **Order regex alternation longest-first.** `jsonl` must precede `json` or matches truncate to the
  shorter extension and a real path silently stops matching.
- **Attribute before you accuse.** Unexpected edits to a shared control are usually a concurrent
  contributor, not an adversary. Read the diff and the mtime before reacting, and fold in compatible
  work instead of reverting it.
- **Honesty of the writer is not evidence of the write.** An unsigned shared file cannot show who
  wrote what, however well-intentioned the contributors. Say "compatible change, no attribution
  trail", not "tampering".
- **Do not freeze a shared control unilaterally.** Making it immutable does not only protect it — it
  locks out whoever is mid-work. Raise it as a binary for the owner.
- **A control guarding tool payloads does not guard outbound prose.** State which surface is covered.
  Prose discipline is not mechanism.
- **A SKILL.md at the character ceiling cannot be patched at all.** Keep SKILL.md lean; put depth in
  `references/`.

## Related

- `verify-work`, `claim-receipt-discipline` — verification-as-terminal-state and receipt binding.
- `synthesis-verification-gate` — claim classification for synthesis output (user-owned; propose
  changes rather than editing it).
- `agent-finding-verification` — verifying findings from another agent (at the size ceiling; split it
  before extending).
