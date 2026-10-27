# B1 · BOUNDARY BEFORE DETAIL — Anti-Authority-Laundering Law

> **Status:** BERASAS (F13 authorized 2026-10-27, bounded lane: doctrine + falsifiers only)
> **Scope:** Canonical compression. NO new registry, dashboard, ontology, service, or duplicate doctrine tree. Each law maps to invariants that already live.
> **Owner of this file:** this file itself (single compression artifact). Runtime mutation defects are NOT fixed here.

## Canonical form

> **Reality exists in states, but consequence emerges at transitions. Every consequential boundary must be identified, typed, governed, witnessed, and falsifiable before the internal details on either side are optimized.**

BM dapur: Keadaan duduk dalam detail. Akibat lahir bila sesuatu melintas sempadan. Jaga sempadan dulu, kemas isi kemudian.

```text
REALITY > BOUNDARY > TRANSITION > DETAIL > NARRATIVE
```

## Laws → existing invariants (no duplication)

### B1.1 Boundary Visibility — no consequential transition stays implicit
Maps to: witness-before-mutation (AAA invariant 6); state-transition discipline (PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED).

### B1.2 Non-Equivalence — adjacency is not equivalence
Maps to: capability ≠ authority (AAA invariant 3); receipt ≠ SEAL (AAA invariant 4); a representation of a person is not the person (AAA invariant 7). Standing non-equivalence list:

```text
Capability ≠ Authority · Priority ≠ Permission · Verdict ≠ Identity
Test pass ≠ World outcome · Transport success ≠ Governance success
Receipt ≠ Consequence · Memory ≠ Truth · Consensus ≠ Independent verification
Discoverability ≠ Endorsement · Liveness ≠ Correctness
```

### B1.3 PROVENANCE NON-ESCALATION — the core law (new single owner)
> **No claim, status, verdict, identifier, receipt, or transport result may acquire a stronger provenance, identity, authority, safety, or completion class merely by crossing a boundary. A class may be strengthened only by new evidence from an authorized verifier whose provenance is explicit and independently checkable. Missing verification metadata MUST NOT default to true.**

BM: Tiada claim naik darjat hanya kerana ia melintas adapter/API/transport. Naik darjat sah hanya dengan bukti baharu daripada verifier b provenance jelas. Medan keselamatan hilang = gagal-tertutup, bukan default benar.

**Canonical owner of the active authority-laundering defect family** (recorded 2026-10-27, falsifiers below; implementation fix requires a separate tests-first lane — currently HOLD):

- `A-FORGE src/interfaces/mcp/core.ts` — accepts `actor.actor_verified OR status=="resumed" OR verdict=="SEAL"` → emits `{verified:true}`
- `A-FORGE src/domain/types/mcp-bridge.ts` — defaults `scope_valid=true`, `replay_safe=true` when meta absent; infers `token_valid` from PASS/SEAL
- `A-FORGE src/interfaces/mcp/shell/forgeShell.ts` — same default-true pattern
- Ledger evidence: 331/331 A-FORGE ledger lines carry `verdict:null`; `refusal_cause` non-null in 0 of 22,492 lines (measured 2026-10-25)

Resolved (do not reopen): `sessionGate.ts` verdict→identity inference removed 2026-10-25; binds only `actor.actor_verified === true`.

### B1.4 Boundary Ownership — one transition owner, one authorization source, one witness path
Maps to: separation of powers (AAA invariant 5: proposer ≠ judge ≠ executor; 333 proposes, 555 verifies, 888 judges, A-FORGE executes under sealed lease).

### B1.5 Fail-Closed Margin — ambiguity at a consequential boundary resolves UNKNOWN/SABAR/HOLD, never silent passage
Maps to: AAA invariant 2 (fail-closed on UNKNOWN — UNKNOWN and HOLD are outcomes, not errors to smooth).

### B1.6 Boundary Conservation — semantic class, authority class, provenance, scope, uncertainty survive transport
Maps to: kernel-sot.yaml "transport/UI aliases are NOT constitutional verdicts"; arifFlow legacy verdict/scalar_fq fossils. Living counter-example: a kernel HOLD still persisted as `ok:true` via `withInvocationLog` (open defect, invocationLog.ts).

### B1.7 Margin Discovery — eureka lives where two locally coherent systems disagree at their shared boundary
Maps to: APEX-ZEN Reality Loop OBSERVE; eureka doctrine. Both sides locally correct + globally false handoff = the finding.

## Falsifiers (required, this lane records them — run them in the separate fix lane)

1. `verdict=SEAL` with `actor_verified=false` must remain **unverified**
2. `status=resumed` with `actor_verified` absent must remain **unverified**
3. Missing `scope_valid` must resolve **false/UNKNOWN**, never true
4. Missing `replay_safe` must resolve **false/UNKNOWN**, never true
5. PASS/SEAL alone must not prove token validity

## Closed regression invariant (Margin #10, retired from active defect register)

```text
Live judge identity = 666 JUDGE
888 = retired label, no operational authority, historical mirrors only
```

Sources: arifOS README §Stage numbering; A-FORGE README stage-map note (both live as of 2026-10-27).

## Final compression

```text
EUREKA::BOUNDARY_FIRST_SYSTEM::v1
Reality lives in states. Consequence emerges through transitions.
Governance stands at boundaries, not inside details.
B1.3 is the law: no class upgrade without new evidence from an
authorized verifier. Missing metadata fails closed.
REALITY > EVERYTHING. BOUNDARY BEFORE DETAIL.
WITNESS BEFORE MUTATION. HUMAN ACCEPTANCE AFTER CONSEQUENCE.
```
