<!-- F13_SAHH_2026-10-06 23:5x MYT · CONSTITUTIONAL · TIER A · IMMUTABLE CANON -->
<!-- DITEMPA BUKAN DIBERI — forged, not given -->

# FAILURE-CLASS SEPARATION — Diagnosis Semantics Law

**Status:** F13_RATIFIED_CANON · Tier A · 2026-10-06
**Author:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
**Compiler:** FI-003 (333-AGI, DECODER lane), KVM8
**Sovereign act:** "canonize this one too" (F13, 2026-10-06, relaying an external analysis-class review whose verdict was SEAL-analysis-only; authority remained F13's)
**Companion fragment:** `/root/AAA/instructions/failure-class-separation.md` (rendered into AGENTS.md)
**Sibling canon:** `APEX-GEOMETRY-SUBSTRATE-2026-10-06.md` — this law is its semantic precondition.

---

## 1 · The law

Three failure classes are **never to be collapsed** in any metric, log, diagnosis, or architecture decision:

```text
Schema failure      — malformed request; validation reject
Authorization failure — policy denial (lease, authority band, session scope)
Execution failure    — capability attempted and errored
```

Equivalently: **Malformed ≠ Denied ≠ Absent.** A schema rejection proves only that the request failed validation — it does not prove the underlying capability is unavailable, and it cannot be used as evidence of an authorization boundary.

The canonical compression (F13-relayed, absorbed):

> **A malformed request cannot be used as evidence of an authorization boundary, just as a HOLD verdict cannot be used as evidence of operational failure.**

## 2 · Why: the measured twin defects (both 2026-10-06)

1. **Metric layer (arifOS):** the `success` observable conflated execution outcomes with constitutional verdicts — all 1,292 evidence-bearing "failures" were HOLD/SABAR, zero true errors. The collapse manufactured a false correlation (evidence↔failure) and a false architecture reading. Fixed by outcome-semantics split, commit `eede91678`, deployed live (E 0.803→0.9842, G 0.4062→0.4278).
2. **Diagnosis layer (bootstrap audit):** a validation reject was being read as an authorization/capability boundary. Same category error, different layer.

**Generalization (the reusable law):** *before improving geometry, verify that the semantics of the observables are clean.* Bad semantics + better geometry = more precise misunderstanding. This is the semantic precondition of the Geometry Substrate canon — it gates the loop's first step (State → Measurement).

## 3 · Probe discipline

- **One narrow probe beats bundled probes.** A probe whose result space is tiny — {validation failure, policy denial, execution failure, success} — is a clean falsifier; its interpretation surface is minimal.
- Bundled probes stack assumptions (filesystem + cache + message bus + path + auth); when the bundle fails, attribution is impossible and the learning is near zero.
- Probe order: separate the classes first, then widen. Operator diagnosis precedes infrastructure change.

## 4 · Bootstrap semantics — demonstrate, never infer

```text
identity bootstrap → session issuance → execution lease
```

These are separable powers (four-layer separation doctrine). A true circular dependency ("need the token to obtain the token") is a **demonstration claim, not an inference**. Until a probe demonstrates it, the honest label is `POSSIBLE CIRCULAR BOOTSTRAP GATE` — never `CONFIRMED DEFECT`. Upgrading POSSIBILITY to CONFIRMATION without a probe is an F2 violation.

## 5 · SABAR's mathematical reading

SABAR is not "nothing works." It is: **measurement quality is insufficient to support the proposed action** — in Geometry Substrate terms, the residual is too large for confident projection (r = s_observed − s_predicted exceeds what the decision tolerance allows). Scope stays limited until the observables' semantics are known. This binds SABAR to evidence quantity, not to system health theatre.

## 6 · Obligations created

- Any new metric, dashboard, or verdict field MUST declare its failure-class semantics at introduction (what does `failure` mean here — schema, policy, or execution?).
- Any diagnosis that concludes an authorization boundary or capability absence MUST cite a probe whose result space separates the three classes.
- Bundled-probe reports must label themselves LOW-ATTRIBUTION evidence.
- POSSIBLE ≠ CONFIRMED: promotion requires a first-party probe (falsify-your-own-probe discipline).

DITEMPA BUKAN DIBERI.
