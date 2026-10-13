# TRANSLATION-WITNESS LAW — Verification Across Representation Boundaries

> **F13_SEAL via sovereign-chat** ("seal all", 2026-10-11) · ritual marker `F13_SEAL::SEAL-5d425fc9ad8244fa::translation-witness-law::seal_all`
> Kernel `arif_seal` NOT used (OBSERVE_ONLY session, `seal_allowed=false`) — sovereign-chat + ritual-marker seal per A-Z precedent (2026-09-13).
> Provenance chain: arXiv:2610.08144 (external measured incident) → eureka `E-TRANSLATION-WITNESS-2026-10-11` + CORR1–CORR3 (`/root/AAA/eurekas/eureka-entries.jsonl` lines 24–27) → three F13-channel audit rounds (verdicts PARTIAL ×3, corrections metabolized) → sovereign "seal all".

## Parent principle (canonical form)

> **A witness verifies a named object under a named representation. A token proves only what its typed authority source establishes. Neither prefix, compilation, signature nor transport integrity may silently inherit meaning from another object.**

## Primitive law

**Lexical resemblance must not confer semantic authority.**

```
prefix(X, "SEAL")   != verdict(X) == SEAL
shape(X, "SEAL-hex") != verified_identity(X)
session_id(X)        != authority_token(X)
signed(X)            != faithful(X, Y)
compiled(X)          != equivalent(X, Y)
verified(X)          != verified(Y)
```

Three object classes must never share meaning by shape: **session identifier · canonical seal token · verdict vocabulary.**

## Causality + falsifier

- proximate cause: prefix/shape-based semantic inference
- systemic cause: namespace and type separation failure
- contributing cause: incomplete consumer inventory/review

Root-cause falsifier: if all `SEAL-*` session identifiers are replaced by a neutral namespace yet privilege/verdict misclassification persists **without** any lexical dependency on `SEAL`, namespace collision is not a sufficient cause (review gap co-exists).

## Ratified corollaries

**A. Representation change = governed mutation.** Every transformation that can alter meaning is a governed mutation, even when labelled translation or verification. The statement-level diff is the receipt; a signature attests transport, never fidelity. — RATIFIED

**B. Witness-target naming (receipt schema, design canon — not yet implemented).** Every verification receipt must identify: (1) witnessed_object {object_id, representation, version_or_hash}; (2) checked_property {name, method, result}; (3) witness {actor_or_mechanism, independence_class}; (4) correspondence_claim {target_object, fidelity_property, evidence_ref — required if target present}; (5) authority {authorization_source, acceptance_actor separate_from_witness}; (6) integrity {receipt_hash, parent_receipt}. Principle: *signature attests this receipt; it does not attest equivalence with another object unless the receipt names and evidences that equivalence.* — RATIFIED AS DESIGN CANON

**C. Machine observes, human judges.** Machine comparison produces observations and suspected divergences (high recall, low precision); human judgment accepts, rejects, or leaves semantic equivalence unknown — acceptance authority + consequence ownership, **not infallibility**. The roles must not collapse. — RATIFIED

## Receipt-token discipline

`RECORDED::` = ledger append. `SEALED::` = canonical ratification only. `session_id` never doubles as verdict. **One token, one meaning** (closes the A-FORGE `status:"SEAL"` collision class).

## Named defect sites & remediation state (2026-10-11)

| Site | Defect | State |
|---|---|---|
| `A-FORGE SealService.ts:173` | `startsWith('SEAL')` → PASS/0.1 | **FIXED** WO-1 · commit `adb09ef3` · exact-match parser `mapArifOSVerdictText`, negative family → VOID, unknown → fail-closed HOLD · 15 regression cases |
| `A-FORGE AaaAgentRegistry.ts:123` | `/^SEAL-[a-f0-9]{16}$/` → 888-APEX binding | **FIXED** WO-2 · commit `adb09ef3` · branch removed, null→HOLD fail-closed (caller chain measured) · 6 regression cases |
| `arifOS tools.py:24295` | `session_binding_pass` from prefix (diagnostic spine, not authorization) | **OPEN** WO-3 · P2 · kernel deploy lane + ratified 13-key schema consumers · evidence class MACHINE_LOCAL_OBS |
| Namespace `SEAL-` for sessions | systemic collision source (mint sites `tools.py:7947`, `vault_registry.py:104`; doc drift: tool docs say `sess-`) | **OPEN** WO-4 · design deliverable only; migration execution F13-gated → grant-pack M6 |
| Precedent | sessionGate P0.2 (2026-07-19): SEAL-* tokens no longer auto-accepted; ACT HMAC sid-claim match | same class, fixed earlier at session gate |

## Kin

representation-reality-invariant · proxy-reality-paradox (F13 2026-10-02) · grant pack `07-RISK-REGISTER.md` R2/R18 · `05-MILESTONES` M6 · Pillar VI `G_complete = G × I` (SCI=∞: fidelity gate not mechanizable in the limit — governance justification of F13, not proof-theoretic omniscience) · W³ witness-target rule · scar `2026-10-11-lexical-authority-token-overclaim`
