# Hybrid-Report Pattern — Real Facts + Fabricated Numbers (2026-08-05)

## What this case is

A pasted "Linux Kernel vs arifOS Kernel — Full Contrast" doc arrived claiming to be a comprehensive architectural analysis with concrete FQ numbers, stage numbers, G-scores, and a series of "what to forge next" actions. Verification showed:

- The **structural argument** (F1–F13 floors should be OS-level enforced; FQ should hard-gate execute; EKC/seL4 pattern is the right evolution) was directionally valid and worth keeping as design thought.
- The **bibliographic anchors** (Biggs/Lee/Heiser 2018 paper, CVE-2026-31431/43284/43500) were real citations.
- The **concrete numbers** were fabricated or stale: FQ=0.028 (live=0.381), stage=111/G=0.1794 (live=stage null, version v2026.08.01), "machine_state.json 97.5d stale" (live updated today), VAULT999=/dev/null (opposite properties).

## Why this is more dangerous than an all-wrong report

The pattern: **verifiable facts *lend credibility* to the unverified claims by association**. A reader's pattern-finder parses the doc once: CVE IDs and paper titles feel trustworthy → the surrounding prose feels trustworthy → the unverified numbers slide through. The reader now has a "comprehensive analysis" with parts that are wrong in ways that cannot be detected by re-reading.

This degrades the trust the user can put in subsequent reports from the same agent — once a hybrid slip is exposed, the agent's credibility is reset.

## The discipline: verify the falsifiable number first

Cost-ordered verification:

1. **Cheapest, most likely wrong: a single specific number** (FQ value, stage number, G-score, line count). One `curl :7073/health | jq .fq` or one `git tag` lookup. If wrong, the structural premise is suspect.
2. **Next: a directional analogical claim** (VAULT999 = /dev/null, Linux CFS = arifOS FQ). Quick check: does the analogy equal or invert the real property? Equal = maybe; invert = reject.
3. **Last: the structural argument** (the "why" of the report). Even if all numbers are wrong, a structural argument can still be true — but it must be re-derived from first principles, not from the report.

## Worked verification table (this session)

| Claim | Live | Verdict |
|---|---|---|
| FQ=0.028 STUCK | live 0.381 STUCK (and 0.818 earlier) | ❌ number wrong, direction right |
| arifos-4511f4e · stage 111 · G=0.1794 | live version v2026.08.01, stage null | ❌ fabricated |
| VAULT999 = /dev/null | VAULT999 is `chattr +a` immutable, 34,666 lines | ❌ analogy **inverts** the property |
| machine_state.json 97.5d stale | /root/WELL/machine_state.json updated today | ❌ stale claim |
| Biggs/Lee/Heiser 2018 "Jury Is In" paper | real paper, real authors | ✅ verified |
| CVE-2026-31431/43284/43500 | real CVEs, real chain | ✅ verified |
| arifOS runs in userspace, software-only enforcement | `ps` shows user `arifos`, not root, no ring-level | ✅ verified |
| FQ<0.5 → constitutional HOLD idea | idea survives; needs escape hatch (HOLD itself lowers execute → deadlock) | ⚠️ directionally right, mechanically incomplete |

## Reusable parts (kept)

- **FQ<0.5 → hard HOLD** is a real design idea worth a T1.5 proposal (not yet drafted; needs escape hatch for self-referential deadlock: HOLD lowers execute, but HOLD's release condition is FQ≥0.5, which depends on verify >= execute, which depends on agents running, which the HOLD blocks).
- **Three-layer separation in GENESIS/045 as microkernel pattern** is a useful framing — small verified core + services in protection domains + user-facing dashboard. Concrete microkernel reference (seL4 8,700 lines) is the right shape of thing to investigate.
- **EKC compartment idea** (small Rust shim enforcing floor invariants at syscall level, cannot be bypassed by the Python runtime) is structurally sound and the right "next evolution" direction.

## Rejected parts (don't repeat)

- Any specific numeric claim without a verifiable source.
- Any analogy that inverts a fundamental property of the original.
- Mixing real citations with fabricated metrics in the same doc — readers can't separate them, the agent's credibility gets reset anyway.

## Heuristic to bake into future verification

> **The reader cannot tell which parts of a hybrid report are real. So if any falsifiable number is wrong, treat the whole report as a low-trust source until each piece is independently verified. The cost of "verified everything separately" is much lower than the cost of acting on a wrong premise.**

Cross-references: see `federation-runtime-forensics` skill (probe-before-act doctrine) and `federation-peer-consultation` skill (peer self-report verification pattern).