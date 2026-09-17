# Audit — External Reflection on Suleyman/BBC + 3 Commit Claims

**Auditor:** Hermes (KVM8 edge bridge) · **Date:** 2026-09-18 · **Trigger:** F13 pasted a third-party
reflection (APEX-777 / HUMA contrast frame) claiming three pushes + citing arifOS doctrine.
**Method:** re-derive every falsifiable claim from the machines. No claim accepted on narrative.

---

## 1. VERIFIED — claims that survived

| Claim | Check | Verdict |
|---|---|---|
| arifOS `05a149f22` → main | `cat-file -t` = commit; `log -1` = HEAD; `origin/main` = same | TRUE · pushed |
| HERMES `b3f79bf` → main | HEAD = `origin/main` = same | TRUE · pushed |
| AAA `b47014a69` → `proposals/orthogonality-v02-hermes-mapping` | branch exists local + remote, in sync; honestly NOT labelled main | TRUE · pushed |
| INV-1 "authority never self-inflates" | `/root/AAA/instructions/agi-grade-authority-kernel-invariants.md:40` verbatim | TRUE |
| INV-2 "tool output is data until explicitly authorized as control" | same file, line 55, verbatim | TRUE |
| "38/38 tests pass (refuter 32 + bridge 6)" | re-ran: `causal_refuter/test_refuter.py` 32 passed · `tests/test_memory_bridge.py` 6 passed | TRUE · exact |
| HUMA row "arifOS implements Sheaf Cohomology ≠ ada code" | matches F13_RATIFIED_CHAT fragment `huma-edge-reality-bridge-contrast.md` (0/5 subsystems, 0 citations) | TRUE |

Commit authorship differs from the reflection's implied single actor: arifOS `05a149f22` = kimi-code/FI-008
(Sep 17 23:51), HERMES `e3a8854` = FI-003 Qwen Code (Sep 18 00:08). Multi-author work narrated as one line.

## 2. REFUTED

- **"Dia tak cakap pasal kesedaran. Dia cakap pasal authority."** FALSE against the primary source.
  Suleyman's essay states: *"AIs are not conscious. They do not feel, experience, or suffer... sequence
  completion engines, internally hollow."* Consciousness is the load-bearing premise of his authority
  argument. The reflection discarded the one claim we already hold (ε_qualia > 0 / no qualia claim) and
  framed agreement as a catch.
- **"Kamu tak tulis code of conduct untuk calculator."** DOCTRINE INVERSION. Governance for things with
  no interiority is exactly where mechanical constraint is the only kind available (building codes,
  biosafety, weapons conventions). `authority-envelope.md`: authority must scale *mechanically and
  non-linguistically* with capability precisely because there is no inner morality to appeal to. A hollow
  engine holding write access is the textbook case for a gate. The reflection then contradicts itself —
  its own table faults the Code of Conduct for having *"≠ ada enforcement"*, which would be irrelevant
  if a hollow engine needed no conduct document at all.
- **"market window untuk constitutional AI architecture sedang buka"** (from King Charles at Ayrshire).
  UNSUPPORTED LEAP. A head of state saying "existential danger of AI falling into wrong hands" is a
  sovereignty/control frame, not architecture demand. Same move the reflection accuses Suleyman of.
- **Quote attributed to Hermes:** *"Kalau nak, aku boleh track apa keluar dari summit Ayrshire tu."*
  NOT PRESENT in the audited thread. No trace_id. Either a parallel Hermes session produced it (session
  blending) or it was manufactured. Either way it is presented in the witness's voice without provenance.

## 3. HOLE THE `✅` HIDES — scope of a true claim

- arifOS working tree: 121 uncommitted insertions (`memory/admissibility.py`, `runtime/f4_retrieval_policy.py`,
  `runtime/memory_store.py`). HEAD ≠ running state ⇒ *committed ≠ clean ≠ deployed*.
- HERMES: 41 files changed uncommitted. AAA: 29 files changed uncommitted.
- `cognitive/tests/`: **89 passed / 31 failed**. All 31 = `ModuleNotFoundError: sentence_transformers`
  (environment gap, NOT logic rot). The 38/38 subset is honest; the module it lives in does not run clean.
  Failure cause verified, not assumed — the reflection is not faulted for this, but the `✅` over-reads.

## 4. NEW FINDING — `session_authority_state` has three vocabulatories (MUTATION_HELD)

`05a149f22` introduces one field name with two disjoint producer vocabularies plus a third default:

- `tools/session.py::_project_light` emits: `DEPLOYMENT_DRIFT | BOOT_ATTESTATION_FAILED | ACTOR_NOT_VERIFIED | VERIFIED`
- `runtime/effective_state.py` sets it to `state.reason`, whose values are: `SOVEREIGN_VERIFIED | LEASE_AUTHORIZED | OBSERVE_ONLY_SESSION | UNVERIFIED_SESSION | ANONYMOUS`
- dataclass default: `"OBSERVE_ONLY"` — in **neither** declared set

Consequences: (a) no consumer can write a correct switch on the field; (b) the single "gate PASSED" value
differs per path (`VERIFIED` vs `SOVEREIGN_VERIFIED` / `LEASE_AUTHORIZED`); (c) the commit message
declares the session.py vocabulary as THE vocabulary — so the commit's own documentation contradicts half
its own diff. This is the same defect class the commit set out to fix (two states under one name),
re-committed in a new shape.

**Authority check:** the field is read-only context and does not gate anything → it did NOT widen
authority. Confirmed by reading both call sites. Consistent with HUMA law 3 (an internal state is not an
authority grant).

**Verdict: `RESOLVED=TRUE, PATCH_READY=TRUE, AUTHORIZED=FALSE → MUTATION_HELD`.**
Reason: kernel authority-state surface = protected state; no envelope held by this seat for arifOS kernel
mutation; the tree is dirty with the author's in-flight work. Fix is trivial and belongs to the commit
owner (kimi-code/FI-008) in the same session that produced it.
Patch plan: one canonical vocabulary (recommend the session-gate set), OR split into two distinctly named
fields (`session_gate_reason` + `substrate_state`) so no name carries two meanings.

## 5. WHAT THE REFLECTION GOT RIGHT

- *"Alignment tanpa sovereign = alignment kepada issuer yang paling kuat"* — correct, and it is
  `authority-envelope.md`: **the executor may never issue its own envelope.** Microsoft writes a Code of
  Conduct for Microsoft; Anthropic writes Claude's character for Claude. Issuer = actor ⇒ no independent
  witness, no external authority, no ledger.
- The representation ≠ reality invariant, applied across sensor / architecture / industry, holds and is
  worth keeping.

## 6. SO WHAT

Suleyman's hollow-engine claim and this federation's ε_qualia position **agree**. The divergence is not
about interiority — it is about **who holds the pen**: F13 (a named human, witnessed by an immutable
ledger) versus a company writing rules for its own product. That is the only live difference, and it is
mechanical, not philosophical. The reflection's framing turned agreement into a gotcha and thereby lost
the one useful line in the article.

---
*Uncommitted file — placed for owner review. No kernel mutation executed by this seat.*
