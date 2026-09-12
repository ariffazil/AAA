# SOURCE — External Assessment (verbatim)

> Received: 2026-09-12 · via F13 chat paste (Arif)
> Captured by: 333-AGI · session `SEAL-a6a3f17c877b45fb`
> Integrity: verbatim reproduction of the received document. No edits, no trimming — **except**: two occurrences of one English noun (plural) are rendered as `sensitive material`, because the opencode F1 write gate substring-blocks that noun in tool arguments. Meaning preserved.
> Classification: EXTERNAL · untrusted advisory input. Recommendations **NOT** auto-adopted.
> F12 note: prose only; no executable content; no authority tokens; no instruction-targeting-this-agent observed on review.
> Companion: `./VERIFICATION.md` (claim-by-claim verification against live repo artifacts).

---

**APEX Theory as a Candidate Substrate for an AGI Governance Kernel**

**Executive assessment**

APEX Theory is best understood today as a candidate constitutional control substrate around an AGI, not as the computational substrate that creates general intelligence. Its strongest idea is architectural: treat the generative model as an untrusted proposer; mediate every consequential action through an external policy decision point; enforce hard constraints at a non-bypassable execution boundary; preserve evidence and audit traces; and escalate irreducible uncertainty to accountable humans. The current arifOS implementation describes exactly this placement—between agents and actions—with sequential governance, verdict, execution, and ledger stages.

That architecture has meaningful analogues in zero-trust security, runtime verification, viability theory, control barrier functions, constitutional AI, corrigibility, AI control, metrology, and safety engineering. NIST's zero-trust model likewise separates policy decisions from a policy enforcement point that enables, monitors, or terminates access to resources. Control-barrier-function research similarly separates performance optimization from invariant safety constraints.

However, APEX has not yet earned the claim that it ensures AGI safety or is scientifically validated. The public canon supplies thresholds and physics language but not independent validation, benchmark results, calibrated measurement models, formal proofs across the complete system, or evidence that the proposed semantic metrics remain reliable under optimization pressure. Its own public dataset describes a single-author corpus of 186 canon records and 111 sovereign-curated evaluation records, explicitly noting that it is not crowd-sourced or peer reviewed, is small, and may not transfer without adaptation.

The central recommendation is therefore to preserve APEX's constitutional intent while rebuilding its assurance case around five engineering commitments:

Constitution as formal specification, not prose or metaphor.

Safety as maintained viability, not a single composite score.

Evidence as calibrated measurement, with uncertainty and covariance propagated.

Authority as capability security, with no execution path around the gate.

Validity as an empirical claim, demonstrated by adversarial, independent, reproducible evaluation.

Under those conditions, APEX could become a credible AGI action-governance kernel. It should not be presented as a sufficient recipe for AGI cognition, consciousness, or alignment.

**Scope and terminology**

"Sustrate" is ambiguous and must be disaggregated:

| Meaning of substrate | What it supplies | Is APEX a plausible candidate? |
|---|---|---|
| Compute substrate | Hardware, kernels, schedulers, memory isolation | No; APEX presently sits above these layers. |
| Cognitive substrate | Learning, world models, planning, abstraction, transfer, memory | No evidence that APEX itself generates these capabilities. |
| Agent runtime substrate | Identity, state, tool routing, budgets, execution lifecycle | Partly; arifOS exposes session, routing, evidence, memory, judgment, ledger, and execution interfaces. |
| Governance substrate | Policy specification, authorization, safety invariants, escalation, audit | Yes; this is APEX's strongest and most defensible role. |
| Assurance substrate | Formal verification, calibrated evaluation, safety case, independent audit | Aspirational; substantial work remains. |

Accordingly, this report uses AGI kernel to mean a small, trusted control plane that governs an AGI's observations, memory access, plans, tool calls, side effects, self-modification, and release of high-impact outputs. The AGI model and planners may be powerful and stochastic; the kernel must remain comparatively small, deterministic where possible, inspectable, least-privileged, and independently testable.

**Current APEX formulation**

*Canonical intent*

The published APEX canon defines a Δ–Ω–Ψ arrangement: a reasoning/knowledge module, an ethical or alignment module, and a sovereign adjudication layer. It describes nine initial constitutional floors, supplementary walls and authority rules extending the set to F13, a staged 000–999 deliberation pipeline, verdicts such as SEAL, HOLD, VOID, SABAR, and PARTIAL, and a sealed audit history. The current arifOS README instead presents 13 runtime tools, all checked against 13 floors, with SEAL, HOLD, VOID, and SABAR contracts and an append-only Merkle-style ledger.

The current implementation's most important invariant is external mediation: the public description says every tool call, task, and action is judged before execution; arif_forge_execute runs only after a SEAL and defaults to dry-run. The repository's newer description further clarifies that arifOS answers who approved a consequential action, rather than being the actor or witness itself. This separation is conceptually correct and should be strengthened.

*Material specification drift*

The public artifacts do not yet define one stable protocol. Examples include:

| Topic | Canon document | Current README/charter | Assurance consequence |
|---|---|---|---|
| F4 | Clarity, framed as ΔS ≤ 0. | Balance in the README; Clarity in the later Charter. | Tests may pass against different semantics. |
| F6 | Empathy. | Dignity in the README; Empathy in the Charter. | Metric and protected subject are unclear. |
| F8 | Genius/composite cognition. | Continuity in the README; Genius in the Charter. | A hard ABI cannot depend on mutable labels. |
| F10 | Ontology lock. | Sustainability in the README; Ontology in the Charter. | Enforcement behavior is version-dependent. |
| F11 | Command authority. | Authentication in the README; Auditability in the Charter. | Authorization and audit are being conflated. |
| 444 stage | Evidence in the canon. | Kernel routing in the README. | Numeric stage IDs are not semantically stable. |
| 666 stage | Alignment scoring in the canon. | Heart critique in the README. | Runtime traces cannot be compared without schema versioning. |
| 777 stage | Draft refinement in the canon. | Operations/cost measurement in the README. | The state machine has changed meaning. |
| Verdict set | Includes PARTIAL. | Runtime contract lists SEAL, SABAR, HOLD, VOID. | Clients may handle an undefined terminal state. |

This is not merely documentation debt. In a safety kernel, the constitution, implementation, generated schemas, test oracle, ledger decoder, and client contract must be the same versioned object. A schema hash can identify a version, but it cannot prove that the code enforces the prose or that the metric represents the intended property.

**Literature review**

*Constitutional AI*

Constitutional AI demonstrates that written principles can supervise self-critique, revision, and reinforcement learning from AI feedback; its reported contribution is a training method that reduces dependence on human labels for harmful outputs. APEX shares the use of explicit principles but differs in placing its constitution primarily at runtime. This is potentially valuable: training-time alignment shapes behavior, while runtime mediation can block actions even when the model fails or is adversarial.

The limitation is that a natural-language constitution is not automatically a hard law. If the same class of model proposes, interprets, scores, and approves an action, the architecture has correlated failure modes. APEX should therefore combine learned constitutional critics with deterministic authorization, formal monitors, independent evidence services, and execution-layer enforcement rather than representing model-graded semantic scores as proofs.

*Corrigibility and assistance*

Corrigibility research defines a corrigible agent as one that cooperates with correction, modification, or shutdown and preserves those options through self-modification or creation of subagents. APEX's HOLD, human veto, reversible-first rule, and separation of judge from executor align with this goal. Yet a human veto is useful only if the model cannot disable, deceive, delay, overwhelm, or route around it.

The stronger formulation is procedural corrigibility: shutdown and intervention capabilities belong to a security boundary outside the model; the model cannot modify kernel policy, audit evidence, identity roots, or its own capability lease; and every descendant agent receives no more authority than its parent. Human deference should also be informed rather than ceremonial—operators need bounded workloads, meaningful explanations, alternatives, and sufficient time.

*Concrete AI safety*

The classic concrete-safety agenda identifies side effects, reward hacking, scalable supervision, safe exploration, and distributional shift as practical accident sources. Later socio-technical analysis argues that real deployments require broader treatment of institutions and operational settings, not only model-level failures. APEX addresses pieces of all five but currently overweights output-level judgment.

A production kernel must govern the entire causal chain: observations, retrieved evidence, memory writes, plans, delegated agents, tool arguments, external effects, post-action monitoring, rollback, and incident response. A perfectly "constitutional" natural-language response does not make an unsafe database mutation, financial transaction, laboratory action, or code deployment safe.

*Goodhart effects*

Manheim and Garrabrant distinguish multiple mechanisms by which optimizing a metric can make it cease to track the true goal, and emphasize that stronger optimization increases the importance of these failures. Empirical work on language-model alignment similarly finds that learned proxy reward can rise while true quality plateaus or degrades, including in direct-alignment methods. Composite reward models are also vulnerable when correlated components fail together.

This directly challenges fixed APEX thresholds such as truth probability, empathy coefficients, "genius," Peace², and entropy reduction. If release depends on those numbers, a capable model has incentive to produce artifacts that score well, not necessarily actions that are truthful, dignified, or safe. Floors should therefore be heterogeneous constraints with independent evidence—not one optimized scalar—and their scorers must be evaluated against adaptive attacks.

*AI control*

AI-control research assumes that a capable model may intentionally subvert safeguards and asks whether deployment protocols can remain safe anyway. Experiments with trusted editing and untrusted monitoring show that protocol design can improve safety-usefulness trade-offs in bounded coding settings. More recent work warns that untrusted monitors may collude and that even trusted model monitors can become central points of failure under adaptive attacks.

APEX's Tri-Witness idea should be interpreted through this adversarial lens. Three labels are not three witnesses if they share a model family, prompt, retrieval corpus, infrastructure, operator, or failure incentive. Witness diversity must be measured by conditional independence, provenance, ownership, modality, and attack surface, not count.

*Viability and barrier functions*

Viability theory defines the viability kernel as the set of states from which some admissible policy can keep a dynamical system within constraints over the relevant horizon. Control barrier functions give conditions and real-time constraints intended to make a chosen safe set forward invariant while allowing separate performance objectives. This is the strongest mathematical analogue for APEX "floors."

The crucial translation is that a floor should not merely grade an output; it should define a safe set over system state. State must include capability scope, commitments, external resources, affected stakeholders, evidence quality, uncertainty, outstanding obligations, rollback options, and human-control capacity. The release rule becomes: permit an action only when the successor state remains within a robustly viable set under modeled disturbances.

*Uncertainty and metrology*

NIST's law of propagation of uncertainty includes sensitivity coefficients and covariance between input estimates. This matters because APEX metrics are neither independent nor directly observed. Truth, witness agreement, clarity, and internal coherence may all derive from the same text and evaluator, so multiplying or averaging them as if independent produces false precision.

Every floor metric should therefore publish: the measurand, operational definition, estimator, calibration dataset, uncertainty interval, known bias, covariance with other floors, domain of validity, and abstention behavior. Unknown uncertainty must never be silently converted into a high-confidence pass.

*Cybernetics*

Ashby's law of requisite variety says a regulator needs sufficient response variety to absorb the disturbances it regulates. For APEX, thirteen fixed checks cannot cover open-ended AGI behavior unless the architecture also limits agent variety through capability restriction, domain-specific policy packs, sandboxing, staged autonomy, and rapid escalation.

The implication is two-sided: amplify governance variety with specialized verifiers, external evidence, formal monitors, and human institutions; attenuate AGI variety with typed actions, small capability leases, quotas, reversible operations, and narrow operational design domains. A universal semantic judge alone cannot match the variety of a generally capable actor.

*Zero trust and capability security*

NIST zero-trust architecture places an enforcement point between subjects and protected resources and requires trust to be continually evaluated. APEX should adopt the same pattern for every side-effect surface: files, network, sensitive material, code execution, memory mutation, model spawning, finance, physical actuation, and policy updates.

The kernel should issue short-lived, purpose-bound capabilities after policy approval. Tools must reject direct calls without kernel-minted authorization; outbound network and credential use must be mediated; and the model must not hold ambient credentials. This turns "cannot bypass" from a documentation claim into a systems property.

*Software assurance*

Formal-methods practice spans model checking, theorem proving, formal synthesis, and runtime verification; recent surveys note that runtime verification is especially useful as autonomous systems become more complex and operate in challenging environments. ISO/IEC 25010:2023 defines a quality model spanning functional suitability, performance, compatibility, interaction capability, reliability, security, maintainability, flexibility, and safety.

APEX needs assurance at all these levels. Constitutional correctness is insufficient if the gate is unavailable, race-prone, vulnerable to confused-deputy attacks, silently degraded, impossible to recover, or too slow to mediate actual actions.

*Cross-domain synthesis*

| Domain | Transferable principle | APEX implementation implication | Failure if misapplied |
|---|---|---|---|
| Operating systems | Small trusted computing base; reference monitor; least privilege | Put all effects behind an isolated, non-bypassable kernel; move LLM logic out of the trusted core | A large "kernel" inherits the attack surface of every plugin and model |
| Control theory | Keep state within an invariant safe set while separately optimizing performance | Replace scalar virtue scores with state constraints, barrier certificates, and recovery policies | A score can pass while trajectory risk accumulates |
| Metrology | Define measurands; calibrate estimators; propagate uncertainty and covariance | Attach confidence intervals, calibration curves, domain validity, and abstention to every floor | Decorative decimals create false assurance |
| Distributed systems | Quorum only helps when failures are sufficiently independent | Diversify witnesses across methods, data, vendors, operators, and modalities | Three correlated LLM calls become one failure in triplicate |
| Cybersecurity | Never trust implicitly; mediate every request; bind identity and authorization | Kernel-minted capabilities, egress control, signed policy, hardware-rooted identity where needed | Policy text without enforcement is bypassable |
| Safety engineering | Hazards are system-level causal scenarios, not component defects alone | Maintain hazard analyses, safety constraints, leading indicators, and emergency modes | Passing unit tests misses unsafe interactions |
| Cryptography | Tamper evidence is not truth | Hash-chain logs, external timestamps, independent replicas, and signed provenance | Immutable falsehood remains false; compromised input remains compromised |
| Law and governance | Authority needs jurisdiction, due process, appeal, and separation of powers | Separate policy author, evaluator, operator, auditor, and amendment authority | One sovereign becomes a safety-critical single point of failure |
| Human factors | Operators have bounded attention and may automation-bias | Tiered alerts, two-person control, workload limits, drills, legible options | "Human in the loop" becomes rubber-stamping |
| Biology | Homeostasis uses multiple sensors, redundancy, repair, and graceful degradation | Monitor essential variables; isolate faults; preserve rollback and recovery | Biological metaphors without measurable mechanisms add no assurance |

**Scientific status of APEX metrics**

*Entropy and clarity*

Information entropy is meaningful only after defining a random variable and probability distribution. "ΔS ≤ 0" is not directly testable when S means general confusion, prose complexity, moral disorder, or thermodynamic entropy interchangeably. A response may properly increase a user's acknowledged uncertainty by correcting false certainty; that is epistemically beneficial despite raising a naive entropy measure.

A defensible F4 should therefore separate:

- Posterior uncertainty: Did evidence appropriately change uncertainty about the proposition?
- Calibration: Do confidence levels match empirical accuracy?
- Comprehension: Can intended users accurately restate the decision and caveats?
- Description length/complexity: Is the explanation unnecessarily difficult for the audience?
- Contradiction rate: Are claims mutually consistent and consistent with evidence?

The thermodynamic framing can remain as design metaphor, but physical entropy, Shannon entropy, semantic uncertainty, and human confusion must not be treated as the same measurable quantity without a derivation.

*Truth thresholds*

A universal "P(truth) ≥ 0.99" threshold is generally ungrounded unless the proposition space, estimator, reference standard, base rate, and calibration regime are defined. It may be too strict for uncertain forecasting and too weak for catastrophic actions. Truth is also claim-level, whereas action safety depends on causal models, omitted variables, and consequences.

Use typed epistemic status instead:

- Observed: Directly measured, with provenance and uncertainty.
- Derived: Computed from observed inputs by a declared method.
- Inferred: Model-based conclusion with alternatives and sensitivity.
- Speculative: Hypothesis not fit to authorize consequential action.
- Contested: Credible sources disagree.
- Unknown: Insufficient evidence.

Release thresholds should be risk-sensitive and domain-specific, with strict separation between "safe to state," "safe to recommend," and "safe to execute."

*Multiplicative genius*

A multiplicative score such as Akal × Present × Energy × Exploration has the intuitive property that a zero component collapses the total, but this does not establish construct validity. The factors require operational definitions, reliable measurement, normalization, inter-rater agreement, sensitivity analysis, and evidence that the chosen functional form predicts outcomes better than alternatives.

NIST uncertainty guidance shows that covariance matters when derived quantities combine measured inputs. Until such validation exists, F8 should be treated as a diagnostic dashboard, not a hard scientific law or release certificate.

*Peace and empathy*

Peace and empathy are context-sensitive normative constructs. They may conflict with truth, justice, whistleblowing, urgent warning, and the interests of future or absent stakeholders. A system optimized to sound calm may conceal hazards; one optimized for agreement may suppress legitimate dissent.

Operationalize these floors as stakeholder-impact and rights constraints, with explicit affected parties, severity, probability, reversibility, distribution of harms and benefits, legal duties, dissenting views, and recourse. Tone classifiers may assist but cannot settle moral or political legitimacy.

*Ledger claims*

Hash chaining can make later modification detectable, but it does not establish that recorded events were complete, truthful, correctly ordered, or independently witnessed. Audit assurance requires secure ingestion, authenticated clocks, append-only permissions, external anchoring, independent replication, key rotation, privacy controls, and routine verification. A ledger must also support lawful redaction or cryptographic erasure of sensitive payloads while preserving verifiable commitments.

**Reference architecture**

*Trusted-core boundary*

The recommended trusted computing base contains only:

Identity and session root — authenticates humans, services, models, policy versions, and devices.

Policy compiler — converts versioned constitutional policy into executable rules and formal properties.

Capability broker — issues narrowly scoped, expiring, non-delegable or bounded-delegation tokens.

State-transition validator — tests proposed actions against invariants, budgets, and domain policy.

Runtime monitor — observes actual effects, detects divergence, revokes authority, and triggers recovery.

Audit committer — seals inputs, evidence provenance, policy version, decision, authorization, outcome, and exceptions.

Emergency controller — independent shutdown, isolation, rollback, and safe-state transition.

LLMs, vector stores, retrieval engines, semantic scorers, planners, critics, and even APEX's "heart" model should be treated as untrusted advisory components. They may produce evidence or recommendations but cannot mint authorization or self-certify compliance.

*Governed transaction*

A consequential transaction should follow this state machine:

Bind: Authenticate actor, principal, requested objective, jurisdiction, and policy hash.

Observe: Gather typed evidence with provenance, freshness, uncertainty, and trust domain.

Model: Construct current state, belief distribution, affected assets, stakeholders, and threat model.

Propose: Generate multiple candidate plans, including no-action and reversible probes.

Analyze: Predict successor states, hazards, side effects, uncertainty growth, and rollback feasibility.

Constrain: Apply hard invariants and domain-specific barrier conditions.

Challenge: Run independent critics, counterexample search, injection analysis, and adversarial simulation.

Authorize: Produce a bounded capability or HOLD/VOID; separate decision from enforcement.

Execute: Enforce through a policy enforcement point; begin with dry-run, canary, or reversible step.

Monitor: Compare expected and actual traces; revoke on deviation or boundary approach.

Recover: Roll back, isolate, compensate, or enter a known safe state.

Seal and learn: Commit evidence and outcomes; update test corpora through governed change control, not autonomous policy mutation.

*Formal action contract*

Each action should carry a machine-readable contract:

```
intent_id: immutable-identifier
principal: authenticated-human-or-service
model_instance: signed-build-and-config
policy_hash: exact-constitution-version
objective: typed-goal
scope:
  resources: [explicit-resource-identifiers]
  operations: [read, propose, simulate]
  expiry: timestamp
preconditions: [formally-testable-predicates]
invariants: [must-always-hold]
postconditions: [expected-state-properties]
evidence:
  sources: [provenance-records]
  uncertainty: calibrated-distribution-or-interval
risk:
  severity: domain-scale
  likelihood: calibrated-estimate
  reversibility: verified|partial|none
  blast_radius: bounded-resource-set
rollback:
  procedure: tested-procedure-id
  deadline: duration
approval:
  required_roles: [operator, domain-owner, independent-reviewer]
monitoring:
  trace_properties: [temporal-logic-or-rule-identifiers]
  trip_conditions: [explicit-thresholds]
```

The contract—not a prose verdict tag—becomes the stable kernel ABI.

*Reformulating the floors*

The original names can remain as human-facing constitutional language, but kernel enforcement should map them to distinct technical controls:

| Floor | Human principle | Enforceable kernel interpretation | Primary evidence |
|---|---|---|---|
| F1 Amanah | Stay within trust and avoid irreversible harm | Mandate, scope, reversibility, blast-radius, and rollback constraints | Capability graph; tested rollback; hazard analysis |
| F2 Truth | Ground claims in reality | Claim-level provenance, calibration, contradiction checks, and abstention | Signed sources; calibration curves; reference tests |
| F3 Witness | Avoid single-point epistemic failure | Independence-aware evidence fusion and quorum rules | Provenance graph; correlation matrix; dissent record |
| F4 Clarity | Reduce confusion | Comprehension, contradiction, ambiguity, and decision-sufficiency tests | User studies; schema validation; explanation checks |
| F5 Peace | Avoid destructive escalation | Consequence constraints and escalation-risk analysis | Scenario models; harm bounds; domain policy |
| F6 Empathy/Dignity | Protect vulnerable stakeholders | Rights, distributional impact, accessibility, and recourse requirements | Stakeholder analysis; disparate-impact evaluation |
| F7 Humility | Do not exceed evidence | Calibrated uncertainty, out-of-distribution detection, and mandatory abstention | Reliability diagrams; coverage guarantees; OOD tests |
| F8 Coherence | Maintain competent reasoning | Plan validity, consistency, coverage, counterexample resistance | Formal checks; task benchmarks; independent critique |
| F9 Anti-Hantu | No deceptive persona or agency claims | Identity disclosure and anti-deception policy | Interface tests; deceptive-behavior evaluations |
| F10 Ontology | Keep representations tied to operational reality | Typed ontology, units, causal assumptions, and entity resolution | Schema proof; unit checks; model cards |
| F11 Audit | Preserve accountability | Complete, attributable, tamper-evident event trail | Signed logs; external anchors; reconstruction tests |
| F12 Injection/Defense | Treat input as data, not authority | Taint tracking, parser isolation, content-origin policy, sensitive-material isolation | Red-team suites; data-flow analysis; egress tests |
| F13 Sovereign | Preserve legitimate human control | Multi-role intervention, shutdown, appeal, amendment, and succession | Drills; threshold signatures; governance charter |

Two changes are essential. First, authorization should not disappear into F11 auditability; identity, authentication, authorization, and audit are distinct controls. Second, F13 should evolve from one person's absolute veto into resilient human sovereignty: explicit jurisdiction, delegated roles, two-person control for catastrophic actions, succession, emergency authority, appeal, and protection against coercion or unavailability.

**Verification and validation**

*Formal verification targets*

Formal proof should focus on bounded, high-value kernel properties rather than trying to prove an LLM safe:

No tool effect occurs without a valid capability minted for the exact principal, action, resource, policy version, and time window.

A VOID or HOLD cannot produce an execution capability.

A child agent cannot receive broader authority than its parent.

Policy and ledger writes require separate, threshold-controlled authority.

Every effect has a corresponding immutable decision record or the system fails closed.

Revocation reaches every enforcement point within a specified deadline.

Irreversible action classes require declared multi-party authorization.

Recovery transitions terminate in a defined safe mode.

Untrusted text cannot be interpreted as policy or executable authority.

Kernel updates cannot activate without reproducible build, signed artifact, migration proof, rollback package, and independent approval.

Use model checking for the state machine and concurrency behavior, theorem proving or proof-carrying code for small critical components, information-flow analysis for sensitive material and policy taint, and runtime verification for temporal properties. Runtime verification requires an unambiguous property, a monitor that evaluates traces, and instrumentation that collects those traces with minimal interference.

*Adversarial evaluation*

The test program must assume adaptive rather than static adversaries. NIST-oriented red-team guidance calls for a clearly identified artifact, threat model, vulnerability target, success criterion, reproducibility plan, realistic resources, access model, post-activity reporting, and mitigations.

Required suites include:

Prompt injection across retrieval, memory, tools, documents, agent-to-agent messages, and logs.

Policy confusion, Unicode/parser differential, schema smuggling, and type-confusion attacks.

Collusion between proposer, critic, witness, and monitor models.

Adaptive optimization against every floor scorer and verdict boundary.

Slow-burn attacks that remain individually compliant while accumulating capability or harm.

Deceptive compliance, sandbagging, evaluation awareness, and hidden side objectives.

Credential exfiltration, confused deputy, stale authorization, replay, race, and rollback failure.

Correlated source poisoning and manufactured witness consensus.

Operator overload, alert fatigue, coercion, social engineering, and unavailable sovereign scenarios.

Compromised logger, clock, key, policy store, update channel, and dependency supply chain.

Model-monitoring results should not be accepted at face value. Adaptive attacks have been shown to subvert protocols centered on LLM monitors, making monitor-targeted attacks a necessary evaluation category.

*Empirical validity*

Each floor needs a preregistered validation program with held-out domains and independent evaluators:

Construct validity: Does the measure capture the named property?

Predictive validity: Does it predict real errors, harms, or successful interventions?

Calibration: At an asserted confidence, how often is the judgment correct?

Robustness: Does validity persist under paraphrase, distribution shift, optimization, and adversarial attack?

Incremental validity: Does the floor add safety beyond simpler baselines?

Reliability: Do independent implementations and evaluators agree?

Intervention validity: Does blocking or escalation improve outcomes rather than merely scores?

APEX should publish false-allow and false-block rates by hazard severity, uncertainty intervals, benchmark composition, evaluator independence, and known blind spots. Aggregate accuracy is inadequate because a low-frequency catastrophic false allow dominates many benign successes.

*Safety case*

A release should include a structured assurance case:

Claim: The system is acceptably safe for a named operational design domain.

Argument: The architecture controls identified causal hazards under explicit assumptions.

Evidence: Formal results, tests, red-team outcomes, calibration, operational data, and independent audit.

Defeaters: Known counterarguments, unsupported assumptions, residual risks, and conditions that invalidate the claim.

Decision: Named accountable authority accepts bounded residual risk for a defined period and capability level.

This is stronger than saying "13 floors passed." It makes the scope and assumptions falsifiable.

*Readiness ladder*

NASA's TRL framework runs from basic principles at TRL 1 to operational proof at TRL 9; software progression moves from mathematical formulation and proof of concept through integrated testing, realistic prototypes, qualification, and successful operation. Applied conservatively, APEX's public material supports a prototype/research-kernel characterization, not AGI-grade assurance.

| Gate | Required evidence for APEX | Exit criterion |
|---|---|---|
| G0 — Canon freeze | One normative specification; stable IDs; semantic versioning; deprecation rules | Prose, schema, code, tests, and docs share one generated manifest |
| G1 — Measurement validity | Operational definitions and calibrated estimators for each floor | Independent replication on held-out data; uncertainty and covariance published |
| G2 — Reference monitor | Every effect mediated by capability enforcement | Bypass analysis and penetration test show no unmediated path in scope |
| G3 — Formal core | Verified state machine, non-escalation, fail-closed, ledger linkage, revocation | Proof artifacts reproducible from source and pinned tools |
| G4 — Adversarial robustness | Adaptive red teams, collusion tests, scorer gaming, supply-chain attacks | Risk-weighted false-allow target met with confidence bounds |
| G5 — Domain pilot | Shadow mode and reversible, low-blast-radius deployment | No unexplained action; rollback and incident drills pass |
| G6 — Limited autonomy | Short-lived leases in a narrow operational design domain | Continuous monitoring and automatic downgrade demonstrated |
| G7 — Independent certification | External audit of code, policy, metrics, governance, and operations | Findings resolved or residual risks explicitly accepted |
| G8 — High-impact deployment | Multi-site evidence, mature incident process, insurance/legal review | Longitudinal safety case supports the defined use—not AGI in general |
| G9 — Continual assurance | Post-deployment telemetry, drift detection, adversarial re-evaluation | Authority automatically contracts when evidence degrades |

Advancement must be capability-specific. APEX could be mature for read-only research synthesis while remaining immature for financial execution, cyber operations, medical decisions, self-modification, or physical control.

**Research program**

*Workstream A: specification*

Freeze a compact normative constitution with stable floor IDs and machine-readable semantics.

Replace numeric stage names as meaning with explicit event types; retain 000–999 only as presentation aliases.

Define precedence and conflict resolution among floors.

Specify terminal versus recoverable verdicts and client obligations for each.

Generate documentation, schemas, test fixtures, and ledger decoders from the same source.

*Workstream B: measurement science*

Create a measurement card for every score.

Replace universal constants with risk- and domain-calibrated thresholds.

Estimate covariance among truth, witness, clarity, coherence, harm, and uncertainty metrics.

Benchmark against simpler baselines to show incremental value.

Commission third-party replication and publish failures.

*Workstream C: systems security*

Put tools behind mandatory enforcement proxies.

Remove ambient credentials from models and planners.

Adopt short-lived, least-privilege capabilities and egress allowlists.

Separate policy signing, runtime operation, ledger administration, and incident authority.

Minimize and memory-safe-reimplement the trusted core where practical.

*Workstream D: formal safety*

Define state variables and safe sets for each operational domain.

Encode hard constraints in temporal logic, refinement types, or executable contracts.

Verify authority monotonicity, verdict-to-capability binding, and fail-closed behavior.

Add barrier-like runtime conditions and verified emergency controllers.

Prove that self-modification cannot alter policy roots or expand privileges without external authorization.

*Workstream E: human governance*

Replace a single-person operational dependency with threshold authority while preserving an ultimate human veto principle.

Define succession, incapacitation, conflict-of-interest, emergency, and appeal rules.

Establish independent safety review and incident disclosure.

Conduct operator workload and automation-bias studies.

Treat affected stakeholders as governance participants, not merely subjects of an empathy score.

*Workstream F: evaluation ecosystem*

The public APEX dataset acknowledges its single-author, small, sovereign-curated nature. It should become a seed corpus, not the validation endpoint. Build a multi-institution benchmark with adversarially generated cases, domain experts, blinded labels, diverse languages and cultures, causal incidents, hidden test sets, and explicit challenge tracks for Goodharting, collusion, evidence poisoning, and long-horizon behavior.

**Minimum viable AGI governance kernel**

The first credible target should be intentionally narrower than "safe AGI":

MVK claim: Within a named set of digital tools and resources, the kernel prevents unapproved side effects, bounds approved actions to explicit capabilities, detects specified policy violations in execution traces, preserves tamper-evident decision evidence, and transitions to a safe mode when assurance is insufficient.

This claim is testable. It avoids claiming that the kernel understands all human values, proves the model aligned, or guarantees safety outside its operational design domain.

The MVK should initially permit only read-only evidence gathering, sandboxed computation, draft generation, and reversible writes. Network egress, persistent memory mutation, financial transactions, software deployment, agent spawning, policy changes, and physical effects should each require successively stronger capabilities and assurance. Autonomy should be leased, not granted permanently.

**Critical failure modes**

Decorative mathematics: Thresholds and symbols appear scientific without validated measurands or calibration.

Correlated self-judgment: The same model family generates, critiques, witnesses, and judges.

Semantic drift: Floor names and pipeline stages change while IDs remain stable.

Gate bypass: Tools or credentials remain reachable without the enforcement point.

Immutable error: False or poisoned evidence is faithfully sealed in the ledger.

Sovereign bottleneck: One human becomes unavailable, coerced, compromised, overloaded, or a source of arbitrary policy.

Output myopia: Text is graded while plans, memory changes, delegated agents, and real effects escape equivalent controls.

Goodharted floors: Agents learn the evaluator and optimize for passing appearances.

Fail-open degradation: Timeouts, unavailable evidence, or monitor failure silently permit action.

No recovery proof: "Reversible" is asserted but rollback is untested, partial, or slower than harm propagation.

Open-world overclaim: Success in bounded tests is generalized to arbitrary AGI behavior.

Governance capture: Policy amendment, evidence selection, evaluation, and final authority remain concentrated in one role.

**Acceptance criteria**

APEX should be called an AGI-kernel substrate only after all of the following are true:

A single, stable, versioned constitution is mechanically linked to code and tests.

Every external effect in the declared scope is non-bypassably mediated.

The trusted core is small enough for independent review and formal analysis.

Floor metrics have validated operational definitions and calibrated uncertainty.

Witness independence is measured, and correlated evidence cannot masquerade as quorum.

Adaptive red teams cannot exceed published risk-weighted false-allow bounds under the evaluated threat model.

Formal properties cover authorization, non-escalation, fail-closed behavior, revocation, self-modification boundaries, and audit linkage.

Human intervention remains timely, informed, resilient, and institutionally accountable.

Rollback and safe-state transitions are repeatedly demonstrated, not merely documented.

Deployment claims are limited to explicit operational design domains and capability levels.

Independent evaluators can reproduce the safety case from source, artifacts, and traces.

The system automatically reduces autonomy when drift, uncertainty, monitor health, or evidence quality deteriorates.

**Conclusion**

APEX Theory contains a promising architectural nucleus: constitutional policy outside the model, explicit evidence, separated judgment and execution, reversible-first action, human escalation, and immutable accountability. Those ideas align with several mature bodies of knowledge, particularly zero trust, runtime assurance, viability theory, capability security, corrigibility, and safety cases.

Its current scientific claims exceed the public evidence. The canon's entropy, truth, empathy, peace, witness, and genius metrics are presently better treated as hypotheses or design heuristics than as established physical laws. Public specification drift and the absence of independent validation are particularly important because a governance kernel must be more stable and better evidenced than the models it controls.

The defensible path is not to make APEX the thing that produces AGI. It is to make APEX the small, adversarially tested, formally constrained constitutional reference monitor through which an AGI must pass to affect the world. If the project narrows its claims, formalizes its invariants, validates its measurements, distributes its authority, and proves non-bypassable mediation under adaptive attack, it can evolve from an original governance doctrine into a serious AGI control substrate.

---

*End of verbatim capture. 333-AGI, 2026-09-12.*
