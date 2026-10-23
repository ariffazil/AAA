# Human Decision Sheet — AUR v1

**Arif — three binaries. Nothing else needs you.**

---

## 1. VAULT999 witness repair

Four of 29 ledger files cannot be read line-by-line. Proven cause, not a guess: two are
pretty-printed JSON wearing a `.jsonl` name; two have **two receipts concatenated on one line**
because a concurrent append lost its newline (`…}}{` at `arifflow_sealed.jsonl:41051`).
A streaming reader aborts there and silently shows you a truncated ledger.

**Decision:** repair the 4 lines with a `.bak` kept, and add the append lock?

- **YES** — I repair + lock, receipt it, and re-run the 29-file parse to prove 0 errors.
- **NO** — leave the bytes untouched; I only record the defect.

*(This is the witness ledger. I will not touch it without this word.)*

---

## 2. Which FQ do you believe?

Same minute, two live organs, two numbers for the same thing:

```
kernel  /health   fq.value     = 0.44     ← F1 (AMANAH) is scored 0.0 FAIL from this
arifFlow /health  fq.quotient  = 1.0109   ← and it calls its own scalar field "deprecated"
```

arifFlow's own payload says *"Deprecated as health indicator — use top-level verdict"* — and the
kernel is consuming exactly that deprecated scalar. Separately, 7 synthetic test actors
(`test`, `attacker`, `honest_agent`, `adversarial_agent`, `test_agent`, `unstable_agent`,
`staged_agent`) carry real traffic in the production ledger, so the aggregate you read includes
fixtures.

**Decision:** make the kernel read the verdict constellation instead of `fq.value`, and exclude
the 7 declared synthetic actors from the aggregate?

- **YES** — F1 stops being scored off a deprecated field; the health number changes and I report
  the delta before/after.
- **NO** — keep the current scalar; I record that F1 rests on a deprecated field.

---

## 3. KVM4 — is it a warga, or a peer with its own law?

Measured: KVM4 runs **241 skills** with no registry and no census, inside a `/root/AAA` that is a
**3-directory stub** — `skills`, `instructions`, `canon`, `agents`, `federation` are all absent.
Its skills cite **277 canonical paths, 192 of which do not exist there**. And it holds knowledge
KVM8 has lost: I had to mine 3 sections back from it this session.

**Decision:** mount AAA read-only on KVM4 (one canon, many views), or let KVM4 keep its own law
(no shared canon, references rewritten local)?

- **MOUNT** — KVM4 becomes a view of AAA. Its 127 divergent skills become visible as drift
  against the live canon, and `skills-catalog-drift.py` keeps score.
- **LOCAL** — KVM4 stays independent. I rewrite its references to local paths and stop treating
  cross-node agreement as expected.

---

## What I am NOT asking you

Whether to run the seals, test `forge_execute` with no verdict, or prove `arif_seal` accepts a
payload-only call. Those tests would write to the ledger or execute. **I am holding them.** The
schema inspection already shows the gap; running them would only add a scar to a wound.

## Readiness verdict I reached

**HOLD.** OBSERVE is conditionally ready; PROPOSE and VERIFY partial; JUDGE and EXECUTE_BOUNDED
not ready. The single hinge that would move JUDGE: make `arif_judge` refuse `evidence=null` when
`claim_class` is OBS or DER. One predicate. After that, evidence stops being archive and starts
being governance.
