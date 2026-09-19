# Orthogonal Verification Surfaces

> **Status:** DRAFT_AWAITING_F13 — extracted from AGENT-STACK-2026 (15 OSS repos, 2026-09-19) + Google Agentic Engineering contrast (2026-09-18)
> **Source eureka:** Functional Verification ≠ Constitutional Verification. Four surfaces, not two. (Single biggest eureka of the AGENT-STACK analysis.)
> **Applies to:** Every evaluation, every review, every readiness check. Capability class. Authority class. Scar class.
> **Filter test passed:** ✅ survives implementation changes ✅ re-examinable in 2 years ✅ not vendor-specific ✅ changes future architecture decisions ✅ not merely tool preference.

## The Problem This Solves

Most agent stacks reduce verification to a single axis: **does it work?**

That single axis is **Functional Verification**. It is necessary but not sufficient. A system can pass functional verification and still be:

- unauthorised (it acted without authority),
- un-attested (no witness recorded the action),
- un-instructive (no scar recorded to constrain future behavior).

A system that passes only Functional Verification is a **capable but unaccountable** agent.

## The Four Orthogonal Surfaces

Every consequential mutation must clear **all four**:

| # | Surface | Question | Failure mode if absent |
|---|---|---|---|
| 1 | **Functional** | *Did it do the right thing correctly?* | Hallucination, wrong answer, broken pipeline. |
| 2 | **Constitutional** | *Was it allowed to do it?* | Privilege escalation, scope creep, F1–F13 violation. |
| 3 | **Witness** | *Can we prove what happened?* | Un-attributable incidents, audit failure, no receipt. |
| 4 | **Scar** | *Can future behavior change because of this?* | Same failure repeats, no learning, no scar-pressure compression. |

Each surface is **orthogonal** — passing one does not imply passing the others. A system that has only Functional coverage has 25% of the verification envelope. A system with only Functional + Constitutional has 50%. A system with all four has full coverage.

## Mapping to Existing Federation Primitives

| Surface | Federation primitive |
|---|---|
| Functional | A-FORGE `forge_evaluate`, `forge_predict`, GEOX domain evidence |
| Constitutional | arifOS `arif_judge` (666), 888-APEX, F1–F13 floor checking |
| Witness | VAULT999, `arif_seal` (999), Claim-Receipt Binding, FRAME observer |
| Scar | `forge_scar`, APEX scar-pressure, Trauma Theorem, scar-weight registry |

The federation already operates the four surfaces — this doctrine is the **declaration** that they are non-substitutable.

## Verification as a Matrix, Not a Scorecard

Wrong mental model: **a single score that aggregates everything** (e.g., "G = 0.83").

Right mental model: **four separate verdicts, each HOLD/SEAL/VOID/SABAR**:

```text
Functional:        SEAL
Constitutional:    SEAL
Witness:           HOLD  ← this blocks, regardless of other SEALs
Scar:              VOID  ← and this blocks future behaviour
```

A failure on any one surface is a failure of the whole system. The other surfaces do not "compensate."

## Why This Doctrine Is Falsifiable

If a system passes all four surfaces and still produces harmful outcomes, the surfaces are insufficient — the doctrine is wrong and needs a fifth. If a system passes only Functional + Constitutional and produces no governance failures over 24 months of operation, the doctrine is over-specified and Scar/Witness can be relaxed for that class of action.

## Related Doctrines

- Six-Graph Federation Model — Witness is a constitutional primitive.
- AGI/ASI Skills System — capability truth both directions (C17/C18/C19).
- Authority Envelope — confidence is not authority (Constitutional surface).
- Memory Promotion Gate — Witness ≠ Seal ≠ Memory.
- Capability-Rich / Authority-Poor Theorem — this doctrine is the remedy.

## Compression

> **Correct ≠ Authorised ≠ Proven ≠ Instructive. Four orthogonal surfaces, all four required, none substitutes for another.**

DITEMPA BUKAN DIBERI ⚒️