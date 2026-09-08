# Federation Invariants — The Split-Brain Doctrine

> **SEAL SOURCE:** federation-invariant-identification-20260906 (WELL intelligence session, 2026-09-06)
> **FORGED:** 2026-09-06 — KVM8 · session SEAL-3c6e1011bd0d4975
> **STATUS:** DRAFT — MUSYAWARAH GATE OPEN. Promotion to rendered canon (render-agents.sh) requires convergence + F13 token.
> **DITEMPA BUKAN DIBERI**

## Core Membership Test: The Split-Brain Test

A component must be federated as a machine-wide invariant **iff two nodes can silently disagree about it at the same moment.**

Silent is the operative word. Divergence that fail-screams is self-healing. Divergence that wears the same name on every node while meaning different things is the actual enemy.

## The Invariant Set (10 components)

| # | Component | Plane | Silent split-brain | Enforcement class |
|---|-----------|-------|--------------------|-------------------|
| 1 | H-WELL readiness signal (L13 gate) | human | KVM8-local state.json; KVM4 Hermes mutates without L13 check | attestation fan-out |
| 2 | Constitution identity | governance | KVM2 arifosmcp fork (OBS, MACHINE_MAP) | boot parity |
| 3 | VAULT999 seal chain | memory | single copy, no cross-node head verification | attestation fan-out |
| 4 | G-WELL signal flow | governance | triadic governance=0.0 — KVM4/KVM2 emit nothing | attestation fan-out |
| 5 | Time discipline (UTC ISO-8601) | truth | %z off-by-8h scar — ±8h accepted as equal | receipt gate |
| 6 | Evidence labels (OBS/DER/INT/SPEC) | truth | arifFlow silent-400 scar — unlabeled receipts kill Verify lanes | receipt gate |
| 7 | Localhost-binding + 5-R key doctrine | security | unprobed node = unverified node | boot parity |
| 8 | Degradation asymmetry (K-2: fail toward observe, never mutate) | control | a node can fail toward mutation | receipt gate |
| 9 | Health semantics (401/403=UP, /health schema) | observation | same probe, different meaning per node | boot parity |
| 10 | State SOTs (federation-models.json, MACHINE_MAP, triadic snapshot) | memory | routing from stale truth on 2 of 3 nodes | boot parity |
| **11** | **Identity plane** — `card.id` resolvable to one canonical path machine-wide (no `_lanes/` ∥ `agent-cards/` shadow); see `agent-card-registry.js` civ_layer preservation rule | witness | agents discover different cards under same `id` depending on which tree loads first | boot parity |
| **12** | **Schema plane** — `card.schemaVersion === current canon` AND `card.registry_receipt_hash` matches `forge_runtime_verify` ON the source snapshot (enforces existing schema-v2.3.0 INV-005/INV-007) | witness | 31/33 cards had no `registry_receipt_hash` as of 2026-09-08; agents reading stale cards trust phantom tools | boot parity + receipt gate |
| **13** | **Authority plane** — `card.governance_profile.authority_ceiling === organ live mode` (JUDGE_ONLY / EXECUTE_AFTER_SEAL / DISPLAY_ONLY / COMPUTE_ONLY / REFLECT_ONLY / METABOLIZE_ONLY / OBSERVE_ONLY) | witness | cards claim capabilities the organ does not enforce; consumers trust over-promises | boot parity + receipt gate |

**Live verification (OBS, 2026-09-06 04:39-04:42 UTC):** WELL :18083 answers on KVM8 only (degraded); KVM4 + KVM2 refuse. KVM4 carries /root/arifOS without federation-models SOT; KVM2 (flow-edge) carries federation-models.json without canon. Governance plane score 0.0 = partial witness wearing a full-witness name. Human CRITICAL 0.144 = stale biometrics — Void Guard applies: cannot-witness, not all-clear.

## The Template Shape: W0

`OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT` is the one invariant that demonstrably holds machine-wide. Its shape — **not its content** — is the template:

1. **Present in every response** (not in a document)
2. **Cheap to check** (single field, no side-channel)
3. **Sovereign-anchored** (one authority, signed origin)
4. **Fail-visible** (absence is an alarm, not a default)

Every promoted invariant should converge toward this shape. A property carried in traffic beats a paragraph carried in docs.

## Three Enforcement Patterns (not one)

1. **Boot parity check** — constitution hash, SOT hashes, naming canon. Model: forge_runtime_verify (MATCH|DRIFT, fail-closed). Fire at node boot + cross-node handshake.
2. **Signed attestation fan-out** — H-WELL signal, triadic snapshot, vault head. One writer, signed. Every node verifies the signature, never trusts a copy.
3. **Receipt-gate enforcement** — time format, evidence labels, degradation mode. VAULT999/arifFlow rejects non-conforming receipts machine-wide. One enforcement point covers #5/#6/#8.

## Boundary: Specialization is not Drift

The 5-organ backbone (arifOS / A-FORGE / GEOX / WEALTH / WELL) is the universal invariant set. Everything beyond it stays role-specific. **Least-power is itself an invariant** — forced parity of role-specific capability would violate it. KVM4 may run litellm without WELL; it may not *pretend* WELL witnessed anything.

## Priority (by live split-brain risk)

1. #1 H-WELL attestation — live today, touches the human plane
2. #2 constitution parity — KVM2 fork is materialized divergence
3. #4 G-WELL feed — every triadic HOLD is partly artifact of missing witnesses
4. #11/#12/#13 identity-schema-authority plane — identity entropy is the federation's actual disease (eureka 2026-09-08, three-witness convergence)
5. #3 VAULT999 replication
6. #5-#10 as one receipt-gate batch

## The Three-Plane Card Admissibility Check (Identity / Schema / Authority)

Forged 2026-09-08 to close the enforcement gap discovered in the agent-card audit. **Not new doctrine** — enforcement closure of schema-v2.3.0 INV-005/INV-007 plus INV-001. Each invariant is the bouncer at the door:

| Invariant | Card field | Source of truth | Pass criterion |
|---|---|---|---|
| #11 Identity | `card.id` + canonical path | `paths_resolver.CANON_AGENT_CARD_PATHS` (extends `CANON_ORG_PATHS`) | exactly one resolvable path per `card.id`; if two paths resolve, the later one is shadowed |
| #12 Schema | `card.schemaVersion` + `card.registry_receipt_hash` | `forge_runtime_verify --mode=hash` against live source | `schemaVersion === "2.3.0"` AND `registry_receipt_hash` matches live SHA256 of source |
| #13 Authority | `card.governance_profile.authority_ceiling` | organ `/health` mode field | ceiling ∈ {JUDGE_ONLY, EXECUTE_AFTER_SEAL, DISPLAY_ONLY, COMPUTE_ONLY, REFLECT_ONLY, METABOLIZE_ONLY, OBSERVE_ONLY, BOUNDED_TEST, SOVEREIGN} AND matches organ live mode |

**Card admissibility rule:** `card.admissible = (pass #11) AND (pass #12) AND (pass #13)`. Inadmissible cards are **routing-rejected** by the A2A gateway and surfaced to arifFlow FQ stream as F4 violations.

**Why this matters (sanitation-not-trust):** Without these checks, "reversible" mutations to the identity plane (e.g. triple-identity collapse) become trust operations — the operator must believe the migration is reversible without any invariant proving it. With the checks live, **reversibility is a property of the system, not a promise of the operator**.

*Ref: canonical glossary /root/AAA/canon/CANONICAL_GLOSSARY.md · Source analysis: /root/.qwen/projects/-root/memory/project-federation-invariants-20260906.md · Boot-verifier spec: /root/AAA/governance/specs/boot-parity-verifier-v0.md*
