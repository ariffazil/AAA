# AAA COMPILATION FABRIC — migration law (F13 direction, 2026-10-02)

> Many AAA "skills" are not skills. They are compiler passes, profiles, adapters, or validators.
> One router + a small set of typed compilers. **Compiler coordinates organs; compiler never becomes an organ.**

## The five fates of every existing skill

| Fate | Meaning | Applied example (PDF, done) |
|---|---|---|
| COMPILER | orchestration becomes a compiler pass | forge-pdf-delivery → publish pass in pdf-federation |
| PROFILE | domain-specific config/content | scientific-pdf-generation, civic-intelligence-pdf → style presets in PDF_OPERATIONS.md §2.4 |
| ADAPTER | provider/channel/tool interface | ocr-and-documents, nano-pdf stay external adapters of pdf-federation |
| VALIDATOR | independent acceptance logic | pdf_verify.sh gates; empirical-audit rule → §4 |
| PRUNE | wrapper with no unique behavior | open-slide-integration, powerpoint (empty), pdf-realmap |

Merge means **extract semantics into typed architecture**, never concatenate SKILL.md text.

## Family status (honest, 2026-10-02)

| Compiler | Status | Evidence |
|---|---|---|
| artifact | ACTIVE via pdf-federation | 13→1 consolidation, G1–G4 live PASS |
| runtime | **PROVEN** | 3 schema-conformant live packets: `runtime/packets/2026-10-02-*.json`; drift classification live (UNMEASURED→baseline→CONVERGED) |
| capability | PARTIAL | health probes live (8088/7072/8081 → 200); CapabilityGraph builder pending (provoked by WELL advertised-but-rejected class) |
| evidence | PARTIAL | interim door agent-claim-verification; EvidencePacket/JudgeDocket pending; **EvidenceCompiler ≠ Judge (888 stays arifOS)** |
| research · task · release · media · context · dispatch · event · delivery | PLANNED | registered in `router/job-types.yaml` — deliberately NOT skeleton-built (no architecture cosplay) |

## Drift lenses — do not conflate

Cockpit MD5 drift (file hash vs gate manifest) and RuntimePacket baseline drift (identity
stability: source/import/surface/process) are **two different lenses**. A subject can read
CONVERGED on one and DRIFT on the other. Both are valid evidence; report which lens, always.

## Boundaries — compilers CONSUME, never absorb

arifOS kernel verbs · HERMES meaning tools · CHRON temporal truth · WELL readiness · GEOX/WEALTH
domain computation · A-FORGE mutation primitives · independent verifier + FRAME witness · 888
JUDGE · 999 VAULT. (Full list: `router/job-types.yaml` §boundaries.)

## Target (estimate, not claim)

104 overlapping entrances in the observed high-overlap families → **9–12 compilers + profiles +
adapters + validators** (≈88.5% routing-surface reduction). Migration order per F13: PDF ✓ →
Evidence → Session → Federation Routing → Research/Web → Telegram → Runtime Ops (runtime-compiler
PROVEN ahead of schedule) → Memory/Context → Skill Governance.

## Invariants

1. `Skill = Profile ∨ Adapter ∨ Validator ∨ CompilerPass` — a SKILL.md that cannot name its fate is architectural debt.
2. One human job family → one canonical front door.
3. Different implementation ≠ different skill door.
4. **Do not federate by concatenating skills. Federate by extracting their shared state machine.**
5. Default = capability metabolism, not capability accumulation (skill-genesis-compiler, PLANNED).

---

## 2026-10-02 (evening) — ISA frozen, Identity first, no runtime seal

**The AAA ISA (10 contracts, `/root/AAA/schemas/ir/` (repo-canonical)):** IdentityPacket (what is this thing?) ·
CapabilityGraph (what can be done NOW?) · TaskIR (what is requested?) · AuthorityEnvelope (what may
this actor do?) · RuntimePacket (what is running?) · EvidencePacket (what was observed?) ·
TemporalPacket (when is this valid?) · DispatchPlan (who executes?) · ResultPacket (what happened?) ·
ArtifactBundle (the human product). Skills = legacy front-end syntax · profiles = domain semantics ·
adapters = drivers · compilers = transformations · **schemas = ISA** · validators = type checkers ·
A-FORGE = execution backend · 888 = judge · HERMES/CHRON/WELL = witnesses · F13 = sovereign.

**Revised P0 sequence:** Identity → Capability → Task → Runtime → Evidence → Temporal; then
research/context/artifact/release/delivery above. Capability truth is a function of identity:
C = f(I_tool, I_server, I_deployment, I_schema, t).

**Identity finding (live, packet `identity/packets/20261002-0228-arifos.json`):** arif_init
(release lens) said drift=false with wheel_hash=null; forge_runtime_verify (worker-reported, not
independently replicated — ACT gate) said wheel-edge DRIFT + HOLD. Direct measurement found the
decisive fact: **no dist-info exists for arifosmcp** — the package identity was never installed as
a wheel, so every wheel-based MATCH/DRIFT verdict measured a phantom artifact. IdentityPacket emits
`AMBIGUOUS_LENS_CONFLICT` with the unresolved edge named, instead of a false verdict. Rule now in
the ISA: **MATCH/DRIFT forbidden until every claimed equivalence edge carries measured evidence.**

**Forbidden mappings (binding):** compiler→authority · EvidenceCompiler→verdict ·
CapabilityCompiler→permission · RuntimeCompiler→truth-by-assertion · IdentityCompiler→identity
creation. Allowed: compiler→typed claim · validator→contract validity · witness→independent
evidence · 888→judgment · F13→sovereign · 777→execution · 999→irreversible record.

**Seal status:** this migration is NOT runtime-sealed (L13 inconsistent-state caution honored;
seal_allowed=false this session). Schemas + compilers are reversible files; the seal decision
belongs to 888/F13 when the state is consistent.

---

## 2026-10-02 (night) — repo alignment: schemas/ir is canonical, the estate measured

Live repo facts (verified on disk, not narrative): `schemas/` exists with SCHEMA_REGISTRY.json
stale since 2026-06-04 — the runtime IRs were absent until tonight. Alias self-audit in
FEDERATED_SKILLS_REGISTRY_V3.yaml: **133 active alias rows, only 42 resolvable, 91 dead** —
a skill name that resolves in prose but has no body is the strongest argument for
IdentityCompiler + CapabilityCompiler. `registries/CAPABILITY_INDEX.json` declares 343 tools
(WELL 48, GEOX 33) while live runtime says WELL 10, GEOX RT1 26 — **CapabilityIndex (declared)
≠ CapabilityGraph (measured) is now law** (schemas/ir/capability-graph.v1).

Landing state (one owner per layer):
- `schemas/ir/` — 12 contracts incl. promoted `task-ir.v1` (from forge_compile_task; concurrent-worker
  version adopted as strict superset, FI-008 duplicate removed same hour) + `IR_REGISTRY.v1.json`.
- `compilers/` — transformations only (identity + runtime PROVEN; others registered PLANNED).
- Legacy `schemas/compile.py` representation compiler → demoted to **backend adapter compiler**
  (vendor representations), no longer the conceptual main compiler.
- Skills classify into exactly three legacy classes: PROFILE · ADAPTER · LEGACY_FRONTEND.

**Migration invariant (binding):** `Behavior_old ≃ Behavior_compiled` must be demonstrated before
any legacy tombstone. **Not-merged chain (binding):** Identity ≠ Capability ≠ Authority ≠ Dispatch
≠ Execution ≠ Evidence ≠ Judgment ≠ Seal; Temporal ≠ timeless; Profile ≠ Compiler; Adapter ≠ Compiler.
Consolidation that collapses these produces 10 god-objects — entropy changes shape, not magnitude.

**Seal status unchanged:** not runtime-sealed (L13 caution); reversible files; 888/F13 decides.

---

## 2026-10-02 (02:40) — CHRON maturity recorded + one falsification receipt

**CHRON state (live-probed by concurrent witness, consistent with reconciliation invariants):**
R1 MCP ✅ · R2 temporal-truth ✅ · R3 falsification ✅ · R4 calibration 🟡 (n≈10 real, acc ≈61.7%,
Brier ≈0.208 — too few to trust, enough to matter) · R5 learning 🟡 · R6 adaptation ❌ unproven.
`CHRON_operational = READY · CHRON_learning = PARTIAL · CHRON_recursive = UNPROVEN`.
Learning bottleneck is now the frontier: Verification→DurableLesson→ChangedBehavior
(last loop: 0 verified, 0 lessons, 4 unclassified outcomes).

**Four powers — do not merge:** CHRON says "we were wrong" · PHOENIX-72 decides whether the error
earns durable memory (cool→VOID or cool→SEALED) · arifOS decides whether that memory has authority
here · A-FORGE executes the authorized transition.

**Readiness criterion (the only one that counts):** E_{n+1} < E_n with causal lineage — the
institution makes fewer of the same mistakes twice. New first-class verbs beyond THINK+ACT:
**WAIT · VERIFY · FORGET**.

**Anti-Goodhart primitive:** CHRON proxy↔reality tracking, 14 pairs, all correlation UNKNOWN —
which is the CORRECT state (UNKNOWN beats plausible). Compilers consume it; none may claim PASS
from a single observation.

**Falsification receipt (this fabric's first catch):** concurrent witness reported "A-FORGE now
source_vs_wheel MATCH · wheel_vs_import MATCH · block=false — biggest blocker disappeared."
IdentityCompiler re-ran at 02:40: **dist-info still absent** (phantom confirmed, 12 min after
packet 0228), git HEAD unchanged `800eb0ae0`. A wheel-edge MATCH on a package with no wheel on
disk is vacuous, not healed. Recorded as lens conflict; no state change accepted on that claim.
This is the exact failure class (truth-by-assertion) the typed control plane exists to catch.

**Temporal compiler:** registered as CONSUMER of the CHRON primitive (TemporalPacket,
schemas/ir/temporal-packet.v1.schema.json). CHRON stays prediction→time→observation→calibration;
the compiler never schedules, judges, or seals.
