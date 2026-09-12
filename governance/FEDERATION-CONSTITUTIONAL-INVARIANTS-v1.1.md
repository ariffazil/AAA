# Constitutional Invariants for a Governed Multi-Agent Federation — v1.1

> **Status:** DRAFT_AWAITING_F13
> **Provenance:** v1.0 sovereign-articulated in chat 2026-09-12 (authoritative source: sovereign message, session SEAL-b7d90d544b9341da era); v1.1 transcribed by FI-008 under F13 "execute all" sanction with three sovereign-accepted corrections folded and tagged **[S1] [S2] [S3]**.
> **Fidelity note:** structural transcription, not byte-exact. F13 ratifies the text as read; the sovereign chat message remains the origin.
> **Ratification path (per own U18):** this draft → FRAME-independent review (criteria pre-fixed) → explicit F13 ratification (chat instrument valid per RATIFICATION-QUEUE line-4 precedent) → staged activation + migration note.

## CHANGELOG v1.0 → v1.1
- **[S1]** Explicit Sovereign tier (F13) above AAA in capability ownership. Sovereign ratifies AAA; AAA executes the sovereign's will. Without this, U1 reads against reality.
- **[S2]** A4 marked *aspirational on current substrate* — fails §0 test #3 while any harness runs as root. Enforceable version: sandboxed harness OR A-FORGE-only write path. Work item, not sentence.
- **[S3]** Append-only lane for unratified lessons (seeded 2026-09-12: `UNRATIFIED-LESSONS-LEDGER.jsonl`, 4 entries) — findings must not live in single HOLD traces or chat-only memory.

---

## Executive Summary

A survivable governed federation is not defined by its language, database, agent protocol, model provider, or orchestration framework. It is defined by safety properties that remain true under replacement, failure, compromise, retry, delegation, and time. The minimum constitution is therefore a set of enforceable separations and evidence obligations: authority must not collapse into execution; execution must not manufacture authority; verification must be independent of the work verified; every material effect must cross a policy-enforcement boundary; delegated power must be explicit, attenuated, expiring, and attributable; material state changes must leave durable, causally linked receipts; and recovery must be demonstrated rather than assumed.

The cross-industry convergence is strong. NIST requires separation of duties, least privilege, protected audit information, provenance, and explicit accountability; zero-trust architecture separates policy decision, administration, and enforcement and requires least-privilege, per-request decisions. Nuclear defence-in-depth requires consecutive protection levels to be independently effective; aviation and medical-device practice use hazard analysis, objective evidence, verification, validation, and traceability; financial-market controls place hard gates before risky effects; NASA uses independent verification and validation for mission-critical software.

The constitutional flow is:

observe → propose → evidence → authorize → enforce → execute → receipt → preserve → independently verify → learn/recover

No organ may silently skip, merge, or reverse these transitions. Automation may accelerate any transition, but it may not erase the distinction between a claim, a decision, an authority grant, an effect, and evidence that the effect occurred.

The proposed minimum set contains 20 constitutional invariants. They are implementation-independent because they specify observable properties and forbidden authority combinations rather than products or mechanisms. Python, MCP, databases, agent frameworks, signing systems, and observability stacks are replaceable; the duties, transitions, evidence semantics, and negative permissions are not.

## Constitutional Test

A rule is constitutional when all five tests hold:

1. **Substrate independence:** it survives replacement of language, storage, transport, model, and agent framework.
2. **Safety relevance:** violating it can create unauthorized, untraceable, unrecoverable, or uncertifiable effects.
3. **Boundary enforceability:** it can be checked at a trust boundary, not merely stated in a prompt or policy document.
4. **External falsifiability:** an independent reviewer can determine from retained evidence whether it held.
5. **Failure semantics:** its behavior under timeout, partial failure, retry, compromise, and uncertainty is defined.

Mechanisms such as a particular signature algorithm, database, message bus, telemetry SDK, or quorum service are implementation-specific realizations. Requirements such as unforgeable authority, append-only history, independent custody, causal correlation, and quorum for defined catastrophic actions are constitutional outcomes.

## Universal Invariants

| ID | Invariant | Why it exists | Failure if absent |
|---|---|---|---|
| U1 | Authority and execution are disjoint. A principal that grants or changes authority for a material action cannot be the sole principal that performs that action. | Prevents an executor from converting technical access into sovereign permission. | Actor becomes authorizer; policy inferred from ability; compromise of one execution identity becomes total control. |
| U2 | Self-certification is forbidden. A producer, executor, policy author, or evidence custodian cannot be the sole certifier of the same work. | Certification is meaningful only if the verifier can reach an adverse conclusion without interference. | Defects relabeled as success; evidence selected or altered by the party being judged; audit becomes ceremony. |
| U3 | Complete mediation at the effect boundary. Every material read, write, invocation, delegation, release, and external communication is checked against current policy immediately before the effect. | Stops hidden paths and stale approvals from bypassing governance. | A direct API, background job, retry path, or privileged tool performs actions the visible workflow would deny. |
| U4 | Identity and delegation are explicit end to end. Every action names the initiating principal, acting principal, delegation chain, and accountable authority. Shared or anonymous authority is not sufficient. | Makes responsibility and authority derivation reconstructable across agents and services. | "The agent did it" becomes the terminal explanation; shared credentials erase who delegated what. |
| U5 | Delegation can only attenuate. A delegate receives no capability broader in action, resource, purpose, time, budget, data scope, or onward-delegation rights than the delegator possessed. | Prevents authority amplification through agent chains. | A low-trust agent obtains high-trust powers by routing through a deputy. |
| U6 | Authority is bounded, revocable, and fresh. Grants are purpose-bound, scope-bound, time-bound, consumption-bound where appropriate, and reevaluated on policy or risk change. | Limits blast radius and prevents old approvals becoming permanent credentials. | Captured approvals replayed; dormant agents retain standing privilege. |
| U7 | Approval binds to the exact action. An authorization commits to the action envelope, target, parameter/artifact digest, policy version, evidence set, constraints, expiry, and expected class of effects. Material change invalidates it. | Closes the time-of-check/time-of-use gap and prevents bait-and-switch execution. | A harmless proposal is approved but a different artifact, target, or parameter is executed. |
| U8 | Evidence precedes consequential judgment. Approval and certification reference inspectable evidence; confidence, eloquence, role, or model output cannot substitute for evidence. | Keeps governance grounded in reality rather than persuasion. | Rubber-stamp approval; fabricated rationale; action approved before hazards, tests, or provenance exist. |
| U9 | No material effect is silent. Every attempted material action produces a durable intent/attempt record and a terminal outcome of committed, denied, aborted, compensated, or explicitly unknown. | Makes silent success and silent failure impossible as accepted states. | External state changes without a receipt; ambiguous timeout retried and duplicates harm. |
| U10 | Historical evidence is append-only and tamper-evident. Corrections add superseding records; they do not erase prior claims. Audit administration is separated from the actors audited. | Preserves what was known and asserted at each time; makes alteration detectable. | Mutable logs rewrite history; operators delete failed attempts. |
| U11 | Causal traceability crosses every boundary. Proposals, evidence, decisions, grants, delegations, executions, effects, receipts, and reviews share stable correlation and parent/causal references. | Allows reconstruction of a distributed action as one governed transaction. | Logs exist but cannot show which approval caused which effect. |
| U12 | Replay is unambiguous and side effects are idempotent or deduplicated. Event order, schema, policy, code/model/tool versions, inputs, and idempotency identity are retained. | Makes retry, forensics, and recovery safe. | Duplicate payments/deployments; historical replay uses current policy. |
| U13 | Unknown is a first-class state and defaults safe. Missing evidence, indeterminate outcome, stale policy, identity failure, or broken custody cannot be coerced into success. | Prevents uncertainty from being silently resolved in favor of action. | Timeout becomes approval; unavailable verifier treated as pass. |
| U14 | Every autonomous loop is bounded and interruptible. Scope, time, cost, call depth, retry count, concurrency, and affected resources have enforceable limits; authorized operators have stop, isolate, and revoke powers. | Contains runaway behavior and cascading failure. | Infinite loops, denial of wallet, inability to halt a compromised agent. |
| U15 | Independent layers do not share a single failure cause. Governance, execution, verification, and evidence custody use sufficiently independent principals, credentials, administration, and failure domains for the risk class. | Prevents nominal separation collapsing under one compromised account or control plane. | One administrator can alter policy, execute, rewrite logs, and approve the result. |
| U16 | Recovery is specified and exercised. Critical functions have explicit safe state, restoration order, loss bounds, known-good recovery points, and periodic restore/replay/failover tests. | Converts backups and continuity claims into demonstrated capability. | "Backups" cannot restore; outage becomes existential. |
| U17 | Observability is independent of success paths. Health, policy denial, queueing, saturation, expired grants, receipt gaps, drift, and audit failure are externally detectable; telemetry failure itself alerts or stops risk-bearing work. | Detects silent degradation; prevents an executor declaring itself healthy. | System returns plausible answers while receipts or effects fail. |
| U18 | Constitutional change is governed more strongly than ordinary action. Changes to policies, role boundaries, evidence requirements, verifier criteria, identity roots, retention, or emergency powers require versioning, review, impact evidence, independent approval, staged activation, rollback, and durable history. | Prevents a component from legalizing its own escalation. | Policy drift; verifier changes tests after seeing results; emergency bypass becomes permanent. |
| U19 | Human accountability is explicit at risk boundaries. Humans define policy and risk appetite; high-consequence, novel, irreversible, rights-affecting, or constitution-changing actions require competent human judgment or a defined multi-party authority. Automation may operate only inside pre-authorized envelopes. | Preserves legitimate judgment; prevents automation from accepting risk on its own behalf. | Approval theater, automation bias, no accountable risk owner. |
| U20 | Failure creates learning obligations. Incidents, near misses, control bypasses, denied actions, receipt gaps, and recovery tests feed corrective action without blame avoidance suppressing evidence. | Makes survivability improve from weak signals. | Repeated incidents, normalization of deviance, controls that decay untested. |

*(Cross-industry evidence per invariant — NIST SoD/zero-trust, NASA IV&V, FDA objective evidence, nuclear defence-in-depth, financial pre-trade controls, SLSA provenance, event sourcing, OTel correlation, HRO/SRE practice — retained from v1.0; see sovereign original for full citations.)*

**Why this set is minimal:** six irreducible guarantees — Legitimacy (U1–U8), Reality preservation (U9–U12), Safe uncertainty (U13–U14), Independence (U2, U15), Continuity (U16–U17), Constitutional continuity (U18–U20). Removing any category leaves a direct path to unauthorized action, unverifiable history, common-mode compromise, unrecoverable failure, or unaccountable governance.

## Organ-Specific Invariants

**HERMES — A2H:** H1 may observe/research/interpret/propose/construct witness objects, cannot create executable authority. H2 every claim carries source, time, scope, uncertainty, transformation history, counterevidence. H3 cannot execute, approve its own proposal, or seal its own witness as authoritative.

**OPENCLAW — A2A:** O1 routes intentions and capabilities; does not originate sovereign authority or determine truth. O2 every handoff preserves identity, delegation, scope, causal context, constraints, remaining budget. O3 cannot hide, collapse, or invent workflow transitions; timeout and partial delivery become explicit states.

**CODING AGENTS — A2M:** C1 may create candidate code, tests, builds, technical evidence; cannot define governing policy or approve deployment. C2 build outputs content-addressed and traceable to declared inputs, transformations, environment, producer identity. C3 agent tests are evidence, not certification; independent criteria remain external.

**AAA — Governance:** G1 AAA alone owns policy judgment, approval, exception, risk acceptance, revocation, constitutional amendment; it does not perform the governed effect. **[S1] Subject to the Sovereign tier (see below).** G2 decisions evidence-bound, reasoned, versioned, signed/attested, expiring, appealable, linked to accountable principal. G3 defined catastrophic actions require multi-party authorization; no emergency self-grant.

**FRAME — Independent verifier:** F1 cannot certify work it authored, executed, approved, or whose authoritative evidence it can modify. F2 verification criteria fixed and versioned before evaluation; deviations and conflicts of interest disclosed. F3 independent identity, administration, evidence access, compute path where risk warrants, unrestricted escalation to AAA. F4 emits findings with scope, evidence, method, limitations, confidence; never converts verification into execution authority. *Guarantee against self-certification enforced across four dimensions: different acting principal; no write authority over target; no write authority over authoritative evidence; no unilateral authority to change criteria or suppress findings.*

**A-FORGE — Execution:** A1 executes only a currently valid, exact, policy-compliant capability presented at the effect boundary. A2 cannot mint/broaden grants, change policy, approve exceptions, certify outcomes, alter authoritative receipts. A3 validates preconditions, enforces budgets and blast radius, emits attempt/outcome receipts, enters safe halt or reconciliation on uncertainty. A4 direct effect channels outside A-FORGE's governed enforcement boundary are forbidden for federation principals. **[S2] ASPIRATIONAL ON CURRENT SUBSTRATE: fails §0 test #3 while any FI harness runs as root with native file-write. Enforceable realization = sandboxed harness OR A-FORGE-only write path. Until then, every harness write is an A4 exception logged as such.**

**VAULT999 — Receipts and continuity:** V1 preserves evidence; does not decide policy, execute effects, or certify truth of stored claims. V2 accepted records append-only, tamper-evident, content-addressed, time-qualified, linked to custody and causal history. V3 corrections/redactions/holds are new governed events; original relationship remains visible. V4 supports independent export, schema interpretation, integrity verification, tested restore without dependence on original runtime.

## Capability Ownership **[S1 — corrected hierarchy]**

**Sovereign (F13) sits above AAA:** the Sovereign ratifies AAA's charter, defines the risk appetite AAA enforces, holds emergency veto and constitutional amendment authority, and may dissolve/reconstitute AAA. AAA owns policy judgment *delegated from and subject to* the Sovereign — "Sovereign ratifies AAA; AAA executes the sovereign's will." No organ, including AAA, outranks the Sovereign; U1's separation applies to AAA *because* the Sovereign tier exists above it.

| Capability | Legitimate owner | Permitted exerciser | Required witness | Forbidden concentration |
|---|---|---|---|---|
| Constitutional amendment; risk-appetite definition; emergency veto | **F13 SOVEREIGN** [S1] | Sovereign process only | Durable history; multi-party for catastrophic | No organ may self-amend |
| Define policy and risk appetite | F13 (supreme) → AAA (delegated) [S1] | AAA governance process | FRAME assesses; VAULT999 preserves versions | Executor, verifier, custodian cannot define policy |
| Approve/deny/except/revoke | AAA under F13 charter [S1] | Authorized governance principals | VAULT999 records; FRAME review | Actor cannot approve own material action |
| Observe external/internal state | Domain data owner under AAA policy | HERMES; bounded agents | VAULT999 provenance; FRAME may validate | Observer cannot turn observation into authority |
| Form claims and options | HERMES / specialist agents | HERMES, coding agents within domain | Sources and uncertainty preserved | Claim author cannot self-seal truth |
| Route and delegate | AAA rules; delegating principal owns its grant | OPENCLAW | VAULT999 full chain; FRAME reviews | Router cannot expand or originate sovereign authority |
| Build technical artifacts | AAA-authorized engineering function | Coding agents | Provenance in VAULT999; FRAME independently tests | Builder cannot deploy or certify its artifact |
| Execute material effects | AAA grants bounded authority | A-FORGE only through enforcement boundary | VAULT999 receipts; FRAME verifies outcomes | A-FORGE cannot mint grants, change policy, erase receipts |
| Verify/certify | AAA charters scope/criteria; FRAME owns method | FRAME | VAULT999 preserves finding; AAA adjudicates | FRAME cannot certify its own work or trigger effect by itself |
| Preserve authoritative receipts | AAA defines retention/access policy | VAULT999 | FRAME tests integrity and recoverability | Custodian cannot rewrite, decide, or self-certify archive |
| Emergency stop/isolation | Predelegated to accountable safety roles; F13 supreme [S1] | A-FORGE enforcement + infrastructure controls | Immediate receipt; later AAA/F13 review | Stop authority ≠ restart/policy-change/evidence-deletion authority |

**Powers never inherent in A-FORGE or any material-effect executor:** policy definition/amendment; approval/exception/risk acceptance; identity-root issuance for its own authority; expansion of its own capability; defining its own certification criteria; final verification of its effects; mutation/deletion/sealing of authoritative receipts about itself; adjudication of disputes; unilateral resumption from governance-caused halts.

## Governance Invariants

**Decision object (minimum semantics):** decision identity and type; accountable authority and quorum; exact action-envelope digest and affected resources; initiator, proposed executor, delegation lineage; policy/constitution version and criteria; evidence references, digests, counterevidence; rationale, uncertainty, residual risk, conditions; valid-from, expiry, revocation, use count, budget, onward-delegation rule; required verifier, receipt class, recovery plan, stop conditions.

**Risk-tiered autonomy:** Reversible/internal/low-impact → pre-authorized automated execution in tight scope. Material-but-recoverable → bounded execution under explicit authorization + independent post-verification. Irreversible/external/financial/safety-critical/novel → research automated, effect gated on competent human judgment, multi-party where warranted. Constitutional/trust-root change → no unilateral autonomous activation. *Human presence alone is not a safeguard: the human must receive decision-relevant evidence, understand scope, have competence, time, and real deny authority, and leave an attributable record.*

**Constitutional amendment:** proposed, impact-assessed, independently reviewed, approved by the sovereign process, assigned effective time, versioned, preserved with migration and rollback rules. Receipts remain interpretable under the constitution that existed when the action occurred.

## Auditability, Receipts, Witness

**Required audit questions (retained evidence must answer):** who initiated/delegated/approved/enforced/executed/verified; under which constitution/policy/grant/risk class; what exact object/parameters/evidence; what was known/unknown/disputed at decision time; which transitions in what causal order; what effects were committed/denied/compensated/unknown; any retry/fallback/override/direct channel; what independent evidence supports the result; could the system be restored without repeating effects; who could alter work/criteria/evidence and were conflicts disclosed.

**Auditor independence test (all answers must be no):** authored a material part? executed/approved it? can alter target after testing? can write/suppress authoritative evidence? can producer alter FRAME's criteria/runtime/report? either party can suppress escalation? shared unmitigated common-cause? pass grants execution authority? If independence cannot be established, output is a **self-check**, labeled accordingly.

**Witness object semantics:** stable identity + content digest; claim/scope/units/intended use; source identity + collection method; source/observation/ingestion times + clock quality; transformations + tool/model versions; supporting and conflicting evidence; uncertainty/limitations; producer + delegation context; custody transfers + supersession links.

**Execution receipt semantics:** identity (all principals); causality (trace/workflow/parent/decision/grant/idempotency); authorization (versions, envelope digest, freshness result); action (operation, target, canonical digest, environment); time (all phases + clock quality); outcome (committed/denied/aborted/compensated/partial/unknown); effect evidence (pre/post-state digests, external identifiers); integrity/custody; recovery (compensation reference, reconciliation owner/deadline).

**Time and ordering:** qualified timestamps for human reconstruction + causal identifiers + monotonic sequence within authority domains + explicit parent links across domains.

**Append-only ≠ infallible; signature ≠ truth:** event sourcing alone proves neither completeness, authorship, nor tamper resistance — VAULT999 adds access separation, integrity protection, custody, independent replication/anchoring, schema preservation, restore verification. A signature proves key control and byte integrity — not authorization, not observation truth, not log completeness.

**Ambiguous commit protocol:** durable intent before effect where feasible; idempotency identity; external effect identifier; terminal receipt; UNKNOWN state with reconciliation — never blind retry. No impossible global exactly-once claims across uncontrolled boundaries.

**[S3] Unratified-lessons lane:** findings not yet sealed live in an append-only ledger (`UNRATIFIED-LESSONS-LEDGER.jsonl`), never in a single trace or chat-only memory. Promotion out of the lane = ratification through the constitutional path; entries never edited, only superseded.

## Failure Mode Catalog (condensed — full table in v1.0 sovereign original)

Authority drift · confused deputy · actor-authorizer collapse · verifier-executor collapse · mutable-history · approval substitution · hidden execution path · stale authorization replay · delegation amplification · prompt/goal hijack (content is data, never authority) · tool abuse · memory poisoning (provenance + expiry + quarantine) · cascading agent compromise · silent partial failure (UNKNOWN/PARTIAL states) · duplicate side effect (idempotency keys) · replay ambiguity (version pinning) · common-mode control failure · audit blindness (independent completeness checks; stop risk-bearing work when evidence channel fails) · rubber-stamp human approval · emergency bypass permanence (short lease, expiry, retrospective review) · unrecoverable continuity loss.

## Anti-Patterns (condensed)

Structural: actor becomes authorizer · authorizer becomes executor · verifier becomes executor · verifier certifies own artifact · custodian owns truth · router owns truth · builder self-attests · one super-agent · shared service identity · policy in prompts only.
Evidence: mutable audit logs · approval without inspectable evidence · execution without intent/outcome receipts · success without external effect evidence · unbound approval · timestamps without clock quality · sampled-only audit · corrections that overwrite · telemetry controlled by the audited · signature treated as truth.
Distributed: exactly-once claims · blind retry after timeout · replay through current policy/code without pinning · dispatch≠execution confusion · unbounded delegation/retries/fan-out/spend · fallback broader than primary · failure reported as absence.
Human: human-in-the-loop as a click · authority without competence · no stop-work authority for the closest to hazard · blame suppressing reporting · emergency powers without lease · constitutional changes shipped as config.

## Canonical Architecture (planes + state machine + control points)

Planes: CONSTITUTION/POLICY (AAA, under F13 [S1]) — exact bounded capability → COORDINATION (OPENCLAW) → EFFECT (enforcement gate + A-FORGE); OBSERVATION/CLAIM (HERMES) feeds proposals; VAULT999 receives all receipt classes; FRAME verifies → findings (not authority) → AAA → F13 [S1]. Coding agents produce content-addressed candidates into the claim path.

State machine: PROPOSED → EVIDENCED → {DENIED | AUTHORIZED} → DISPATCHED → STARTED → {COMMITTED | ABORTED | PARTIAL | UNKNOWN→RECONCILED} ; AUTHORIZED→{EXPIRED|REVOKED}; terminal→RECEIPTED→{VERIFIED|REJECTED|LIMITED-ASSURANCE}. Authorization, execution, custody, verification transitions require distinct eligible principals.

Mandatory control points: ingress auth/risk classification/untrusted content → proposal envelope → evidence gate → AAA decision → attenuated delegation → pre-effect enforcement (reauth, freshness, digest match, preconditions, idempotency, blast radius, receipt channel) → isolated metered execution → outcome capture → VAULT999 custody acceptance reported independently → FRAME verification vs predeclared criteria → AAA adjudication → learning/recovery.

Control failure behavior: identity/delegation failure → deny + denied-attempt receipt. Policy/freshness failure → fail closed for material actions. Receipt channel before execution → halt risk-bearing work unless preauthorized local journal. Receipt channel after possible effect → UNKNOWN, reconcile, never blind-retry. FRAME unavailable → no certification claim; continue only where policy permits bounded unverified operation. VAULT999 integrity failure → freeze destructive/constitutional actions, independent continuity path. A-FORGE compromise → revoke, isolate, preserve evidence, rebuild known-good. AAA compromise → freeze new authority, sovereign recovery; executors cannot self-authorize continuity. OPENCLAW failure → pending/unknown, never "completed." HERMES failure → claims unavailable; no implicit approval.

## Survivability Properties (exercise, not documentation)

Compromised observer cannot cause material effect without independent authority + enforcement. Compromised router cannot broaden authority or erase lineage. Compromised coding agent cannot deploy or certify its artifact. Compromised executor cannot mint authority, alter policy, rewrite receipts, certify success. Compromised verifier cannot alter target, execute remedy, or suppress findings undetected. Compromised vault admin cannot silently rewrite history or destroy all recoverable copies. Loss of any one organ → bounded degradation or safe halt, not constitutional collapse. Ambiguous network failure → UNKNOWN + reconciliation. Federation can rebuild authoritative state and interpret old receipts after runtime replacement. Amendment and trust-root recovery possible, but require stronger authority than ordinary operation.

## Top 10 Non-Negotiable Invariants

1. No principal may be sole proposer, authorizer, executor, and certifier of the same material action — decision, effect, and independent assurance remain distinct.
2. No material effect outside a complete policy-enforcement boundary — including direct, fallback, retry, maintenance, and emergency paths.
3. No delegated authority exceeding, outliving, or escaping its parent's purpose — explicit, attributable, attenuated, revocable, fresh.
4. No approval valid unless bound to exact action, target, digest, evidence, policy version, constraints, expiry.
5. No material mutation without durable intent, outcome classification, causal identity, authoritative receipt — missing/ambiguous outcome is UNKNOWN, never implied success.
6. No auditor certifying work it authored, executed, approved, can modify, or controls evidence for — independence includes principal, administration, evidence, criteria, reporting.
7. No authoritative history overwritten — corrections are governed events; tamper-evident; separately controlled.
8. No uncertainty expanding authority — identity failure, stale policy, missing evidence, timeout, verifier unavailability default to deny/safe-halt/bounded degradation.
9. No autonomous process unbounded or unstoppable — time, cost, retries, fan-out, depth, blast radius enforceably limited.
10. No continuity claim without tested recovery — restore, replay, reconciliation, failover exercised against explicit objectives.

## Final Architectural Judgment

The minimum viable constitution is not "seven trusted agents." It is a system of non-combinable powers, effect-boundary enforcement, bounded delegation, independent evidence, and recoverable history. The organ names can change; the constitutional geometry cannot.

**[S1]** F13 SOVEREIGN ratifies AAA; AAA executes the sovereign's will; no tier sits above the Sovereign. HERMES may know and explain but not authorize, execute, or seal. OPENCLAW may coordinate but not own truth, policy, or effect. Coding agents may build but not define policy, deploy alone, or self-certify. AAA may judge and grant — under F13 — but not perform the governed effect. A-FORGE may act only under exact, current, bounded authority, and may not govern or rewrite history. FRAME may challenge and certify but not author or execute the same work, and must remain independent of its evidence. VAULT999 may preserve what was claimed and done but neither decide truth nor alter the past.

Survivability comes from preserving these distinctions when the system is rushed, degraded, partitioned, compromised, retried, upgraded, or rebuilt. A federation that cannot show these properties from independent evidence is not governed; it is merely orchestrated.

---

*Witnessed against reality 2026-09-12: seven floors held under live cascade (stale ACT rejected U6; fabrication caught pre-seal U8/U19; timeout degraded SABAR-not-pass U13; kernel recorded own failure U9/U20); gaps named honestly (A4 aspirational [S2], U15 common-cause partial, U16 backup untested, chain hash coverage thin) — per F2, honesty about gaps is itself U20 lived, not declared.*

DITEMPA BUKAN DIBERI ⚒️
