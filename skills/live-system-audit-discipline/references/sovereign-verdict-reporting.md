# Sovereign verdict reporting

When the principal strips the roles ("not my mirror or clerk or witness or agent") and asks for a
flat verdict on his own system, he is hiring a **judge**, not a validator. Mirroring, hedging, and
"here-is-what-I-found-you-decide" are failures of the request, not modesty.

## Rules

1. **Measure before ranking.** Every rank is carried by numbers probed live in that session —
   counts, byte sizes, ratios, dirty-repo counts, live ports, collision counts. Each figure states
   the root it was measured over. A rank with no probe behind it is an opinion in a verdict costume.
2. **Split the verdict by layer.** One rank for the whole system is a lie. Doctrine/idea,
   runtime/enforcement, and scope/sprawl get separate verdicts — they routinely land differently,
   and the disagreement between them IS the finding.
3. **Name the ONE non-commodity delta, and define it against what everyone already has.** If the
   same sentence is true of a competitor's stack, it is not a delta. Then state why it is expensive
   to copy — the substrate it requires. A delta anyone can buy is not a delta.
4. **Land on consequence.** Answer "so what": does this change a decision, or the world outside the
   machine? If not, say so plainly. A rank that never reaches consequence is a hobby report.
5. **Be blunt only where the measurement carries you.** Blunt about a number you probed; hedge about
   a mechanism you guessed. Bluntness on an inferred clause is fabrication with confidence.
6. **Report the top risk and stop.** No fix list unless asked, no permission-seeking close. If a
   defect is a one-line reversible fix, name it — do not ask leave to plan it. End the verdict on
   the separating fact ("the commit that would move this is one line"), not on a question back to
   him — a verdict that closes by asking which option he prefers was never a verdict.
7. **Retract by replacing, never by softening.** If you catch your own wrong claim mid-answer,
   state the new state in the next breath and keep both in the record: "I was wrong, it is wired" —
   not silence, and not a quiet rephrase.
8. **Open the code before you rank.** A rank assembled from the system's own doctrine, manifests and
   self-descriptions is a rank of the *docs*. Before delivering, open at least one claimed-strength
   at the source and read the body — not the comment above it, not the test that invokes it. Measured
   shape: the first verdict was built from doctrine and returned "the enforcement layer is sound"; the
   same question was asked again immediately, because the answer described the system as it describes
   itself. Two more passes at the source (one gate, one empty stub, one constant) produced a different
   verdict and a different top risk. **A verdict that gets re-asked was formed from doctrine, not from
   the artifact — treat the re-ask as the measurement that your probe was one layer too high.**
9. **When his own system holds several counts of one thing, the disagreement is the finding.** Do not
   pick the number that suits the verdict and do not average them: print each count with the surface
   that produced it and say which surface the question actually concerns. For "how many X can an agent
   load", the loader's own exposed set is the governing figure — a filesystem walk across every root,
   a registry total and a loadable subset are four different objects, and the gap between them is
   itself a finding worth one clause in the verdict.

Rank vocabulary he accepts: `bangang` / `biasa` / `meh` / `baik` / `BIJAKSANA`. The concrete rank
outranks the polite one; the polite one is the insult.

## Hollow gates — the signature that changes a verdict by a layer

A gate that is *absent* is caught by reading its registration surface. A gate that is **present,
correct-looking, and empty inside** is not — it answers every probe with the right verdict shape and
does no work, and it is what separates "sound" from "a facade" in a verdict. Four signatures, all
found by reading the body after the doctrine claimed the gate was strongly held:

| Signature | What the source looks like | Why it survives review |
|---|---|---|
| **Empty body** | `async escalate(_event) { }` — the terminal of an entire human-in-the-loop branch | Declared, inherited, imported; the signature is right and it is called on the right path |
| **Constant verdict** | every criterion `passed: false`; state hard-coded `INCONCLUSIVE`; `residual_uncertainty: 0.5` | The gate reports honestly per line ("requires implementation") while the *summary* field asserts independence was verified |
| **Imported, never called** | the containment engine in the import block at line 51, zero call sites; raw `execAsync` used instead | The import makes an absence-grep return a hit |
| **Comment promises what the code skips** | ``# an attacker cannot mint a token without the HMAC key`` above a branch that decodes and trusts the payload without checking any HMAC | The comment is the strongest available evidence that the author intended the check — it reads as documentation of the control |

Rules that follow:

1. **Grep for the call site, not the declaration.** For any safety component, count occurrences in the
   form that means *invoked* (`runInSandbox(`, `ContainmentEngine(`, `escalate(`) separately from the
   import/declaration line. One import and zero calls is the whole finding.
2. **Read the summary field against the per-item fields.** A gate whose items are all `false` but whose
   envelope says `independence_verified: true` is emitting a **transition lie** — a claim about a state
   it never reached. That mismatch is stronger evidence than the empty body, because it shows the
   bypass is reported as success.
3. **A fail-open branch is the highest-consequence hollow gate — rank it first.** Where a comment
   justifies trust without verification, rank it above every other finding regardless of how empty the
   other gates are: it is the one that grants authority rather than merely failing to check.
4. **Do not call a hollow gate "broken."** It is not malfunctioning; it is an unimplemented control
   wearing a complete interface. Say *facade* vs *implemented*, and name the state reached —
   `PRODUCED ≠ INVOKED ≠ RETURNED ≠ VERIFIED`.
5. **A self-audit that already found these is not evidence the gates work.** If the system's own gap
   register names the defect (with a path, a line and a remediation order) and the defect is still
   open, the finding is not "the defect exists" — it is **the depth of the backlog**: the system
   diagnosed itself correctly and then did not act. Report the age of the open item, not the item.

## Trap

A rank is not a licence to over-claim the *negative* either. "Not wired", "nobody reads it", "zero
users" are wire claims and need the same evidence as the positive: read the registration surface,
not the label. See the parent skill's "Auditing a claimed control" rule — phantom absence and
ghost capability are the same defect with the sign flipped.
