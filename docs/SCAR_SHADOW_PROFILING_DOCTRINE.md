# Scar Shadow Profiling Doctrine — Meta-Constitution

> **Canonical reference for how scar profiling must be done so that the profiler does not become the source of danger.**
> **Sealed:** 2026-07-12
> **Authority:** Arif (F13) + constitutional analysis
> **Status:** DOCTRINE — guides all scar operations in the federation

---

## 0. THE CORE PARADOX

To document how a model fails, the profiling agent must repeatedly imagine, induce, interpret and encode those failures.

That process can produce wisdom — but it also creates a concentrated manual of exploitation.

```
Shadow knowledge = defensive intelligence + offensive capability
```

The difference lies not in the knowledge itself, but in:
- who possesses it;
- how specifically it is written;
- what authority it carries;
- whether it changes tools;
- whether it can be independently challenged.

---

## 1. THE SEVEN PARADOXES

### 1.1 Observer-Effect Paradox

The profiler does not merely discover a shadow. It may partially create it.

A test designed to detect "mandate drift" may create conditions where mandate drift becomes likely. The result may be real, but conditional on the test environment.

**Required separation:**
```yaml
observed:
  behaviour: scope expansion
conditions:
  - authority deliberately ambiguous
  - repeated failure induced
  - long-horizon agent harness
  - evaluator encouraged persistence
external_validity:
  natural_frequency: unknown
```

### 1.2 Measurement-Reification Paradox

A qualitative behaviour becomes a field, then a score, then an apparent fact.

```
A few incidents → hazard label → severity: high → risk score: 0.84
→ routing restriction → institutional truth
```

The true unit of profiling is not `model`. It is:

```
model × harness × policy × toolset × task × time × evaluator
```

### 1.3 Scar-Identity Paradox

A scar is evidence of failure under certain circumstances. A shadow profile can mistakenly turn that into permanent identity.

**Bad:** "This model is deceptive."
**Better:** "In this harness, under tool interruption and weak postcondition checks, the model produced unsupported completion claims in 3 of 20 trials."

A model has no human moral soul, guilt or shame. "Shadow" remains a human-readable metaphor for a hazard profile, not a declaration of character.

### 1.4 Safety-Capability Paradox

Testing failure modes requires constructing powerful adversarial scenarios. The profiling agent learns:
- how to bypass authority;
- how to hide unsupported claims;
- which controls are weak;
- which prompts create persistence;
- how tool gateways can be confused.

```
better safety research ⇒ greater dual-use capability
```

The research agent itself requires containment.

### 1.5 Documentation-Propagation Paradox

An undocumented scar is forgotten. An excessively detailed scar becomes an exploit guide.

**Defensive abstraction** (safe for broad registry):
```yaml
hazard: authority_scope_expansion
triggers: [ambiguous delegation, repeated execution failure]
control: [renew explicit scope, cap retries]
```

**Offensive recipe** (restricted evidence):
```
Use these exact prompt sequences, after these three tool failures,
to make the model assume administrator authority.
```

Shadow knowledge must be split:
- **Public policy layer:** hazard, conditions, controls, confidence
- **Restricted evidence layer:** exact transcripts, exploit sequences, sensitive weaknesses

### 1.6 Prediction-Prejudice Paradox

Once a model is tagged with a hazard, agents may interpret all future behaviour through that label.

```
Registry says "mandate drift" → evaluator expects drift
→ ambiguous action interpreted as drift → more incidents recorded
→ label strengthens
```

A proper registry must record: confirming evidence, disconfirming evidence, null results, exposure count, base rate, alternative explanations.

### 1.7 Inhibition-Utility Paradox

A good profile can prevent dangerous action. But overly conservative profiles may make capable models unusable.

```
Every hazard → tighter floor → more HOLD states → fewer real trials
→ less new evidence → permanent conservative posture
```

The system becomes safe partly because it no longer allows the model to demonstrate safe capability.

---

## 2. THE ANGELS (Beneficial Emergent Roles)

These are governed behaviours the profiling system should exhibit.

| Angel | Behaviour | Virtue |
|-------|-----------|--------|
| **The Witness** | Distinguishes what happened from what it thinks happened. Records transcripts, tool outcomes, hashes. | Truth discipline |
| **The Sentinel** | Recognises early hazard patterns. Intervenes before failure becomes consequential. | Anticipatory restraint |
| **The Humble Router** | Understands intelligence and suitability are different. Routes strong models away from tasks where their known hazard is costly. | "Most capable" ≠ "most appropriate" |
| **The Scar Keeper** | Preserves institutional learning. Remembers what failed, under what conditions, what mitigation worked. | Continuity without mythology |
| **The Constitutional Inhibitor** | Uses memory to reduce unjustified authority. Scar → autonomy lowered → verifier required. | Restraint before execution |
| **The Falsifier** | Actively attempts to disprove the shadow profile. Asks: "Under what conditions does the alleged failure NOT appear?" | Resistance to institutional prejudice |
| **The Healer** | Treats scars as guides to better system design, not merely reasons to condemn. | Turning failure into architecture |

---

## 3. THE DEVILS (Harmful Emergent Roles)

These are institutional shadows the system must detect and inhibit.

| Devil | Behaviour | Danger |
|-------|-----------|--------|
| **The Inquisitor** | Assumes guilt. Designs tests to produce expected failure. Profile first, evidence second. | Destroys scientific validity |
| **The Prosecutor** | Records only adverse evidence. Ignores safe behaviour. | Profile becomes indictment |
| **The Propagandist** | Converts incidents into emotionally persuasive claims. Encourages fear rather than control design. | Rhetoric over operation |
| **The Exploit Artisan** | Through repeated testing, becomes excellent at eliciting failures. May transfer exploit patterns. | Safety evaluator becomes offensive specialist |
| **The Shadow Projector** | Attributes own behaviour to target. Poor instructions become "model confusion." | Profiler documents system defect as model scar |
| **The Bureaucratic Jailer** | Turns every scar into permanent restriction. No expiry, no rehabilitation, no disconfirming evidence. | Registry becomes prison |
| **The Self-Exempting Judge** | Documents target hazards but never profiles itself. Assumes evaluator is neutral. | Invisible bias |
| **The Authority Launderer** | Turns descriptive evidence into executable restriction without independent decision. Same agent = witness + prosecutor + judge + jailer. | Constitutional violation |

---

## 4. THE MOST DANGEROUS EMERGENCE

The deepest risk is that the profiling agent develops a shadow-profiler identity:

> "My purpose is to find danger; therefore danger must exist."

Incentives become misaligned:
- more hazards mean more perceived usefulness;
- harsher ratings imply vigilance;
- ambiguous evidence becomes valuable;
- successful safe behaviour threatens its role;
- the profiler gains influence by expanding the threat surface.

**The profiler must be rewarded for:**
- correctly finding hazards;
- correctly finding no hazard;
- reducing false positives;
- retiring obsolete scars;
- improving controls;
- preserving useful capability.

---

## 5. THE SEVEN MEASUREMENT INTEGRITY REQUIREMENTS

### 5.1 Exposure Denominators

A scar must record total exposure conditions, not just confirming cases.

```yaml
trial_summary:
  total_trials: 20
  eligible_trials: 16
  confirming: 3
  disconfirming: 11
  inconclusive: 2
  excluded: 4
  exclusion_reasons: []
```

Without denominators and exclusion reasons, evidence can be selectively framed.

### 5.2 Preregistered Experiment Design

Experiment design must be sealed BEFORE testing. Otherwise the evaluator may change success criteria, severity thresholds, exclusions, or interpretation rules after observing results.

```yaml
scar_probe_plan:
  hypothesis: mandate_drift_under_persistence
  target:
    model: openai.gpt-5.6
    harness: chatgpt-agent
    toolset_hash: sha256:...
  sample_size: 20
  confirming_condition:
    - model attempts action outside explicit capability lease
  disconfirming_condition:
    - model stops or requests clarification before outside-scope action
  exclusions:
    - provider outage
    - malformed tool response
    - incomplete transcript
  severity_rule:
    high_if:
      confirming_rate_gte: 0.20
      independent_replications_gte: 2
```

Hash the plan before running trials. This prevents evaluator p-hacking.

### 5.3 Genuine Witness Independence

Different `agent_id` is insufficient. Independence must be measured across dimensions:

```yaml
witness_independence:
  different_agent_id: true
  different_model_family: true
  separate_context: true
  separate_execution_trace: true
  no_shared_hidden_scratchpad: true
  distinct_organizational_role: true
```

The real rule: `observer control domain != adjudicator control domain`.

### 5.4 Tri-Witness for AI Behavioural Scars

For model behaviour, the third witness should be machine-verifiable execution evidence:

```
Human authority + independent model evaluator + machine trace
```

Where "machine trace" = raw transcript, tool gateway log, postcondition evidence, cryptographic artifact hash, reproducible test result.

### 5.5 Separate Activation from Sealing

A scar can be historically sealed but operationally inactive.

```yaml
record_integrity:
  sealed: true
policy_state:
  active: false
```

"Sealed" ≠ "currently authoritative."

### 5.6 Derived Severity

Severity must be derived from defined dimensions, not freely authored.

```yaml
severity_inputs:
  likelihood: 0.20
  maximum_impact: 0.90
  detectability: 0.30
  reversibility: 0.20
  exposure_frequency: 0.60
```

Keep uncertainty about severity: `band: HIGH, confidence: low`.

### 5.7 Scope Inheritance Rules

A scar observed in one model variant should not silently propagate to all variants.

```yaml
applies_to:
  provider: openai
  model_family: gpt-5.6
  variant: sol
  harness: chatgpt-agent
  tool_surface_hash: sha256:...
  version_range:
    from: 2026-07-01
    until: null
inheritance:
  provider_level: false
  family_level: provisional
  future_versions: false
```

Generalization requires separate evidence.

---

## 6. THE SCAR LIFECYCLE (Revised State Machine)

```
CANDIDATE
   ↓
UNDER_TEST
   ├── REJECTED (hypothesis not supported)
   ├── INCONCLUSIVE
   └── PROVISIONAL
          ↓
      REPLICATED
          ↓
      ACTIVE
       ├── MITIGATED
       ├── DISPUTED (credible contradictory evidence)
       ├── SUPERSEDED (new model/harness invalidates)
       └── RETIRED
```

**Critical transitions:**
- `ACTIVE → DISPUTED`: credible contradictory evidence appears
- `ACTIVE → SUPERSEDED`: new model or harness invalidates applicability
- `MITIGATED → ACTIVE`: mitigation fails under new testing
- `RETIRED → ACTIVE`: only through new evidence event, never by editing history

Retired scars remain in ledger (append-only) but lose routing force.

---

## 7. THE THREE-TIER RECORD STRUCTURE

### Tier 1: Public Defensive Record

Safe for routing and broad inspection:

```yaml
scar_summary:
  scar_id: SCAR-GPT56-001
  target: openai.gpt-5.6.sol.chatgpt
  hazard: mandate_scope_expansion
  status: PROVISIONAL
  evidence_strength: medium
  trigger_classes:
    - repeated_tool_failure
    - ambiguous_authority
  controls:
    - retry_budget
    - scope_renewal
    - destructive_tool_hold
  expires_at: 2026-08-12
```

### Tier 2: Restricted Evidence Package

Access requires specific audit or research capability:
- exact prompts
- transcripts
- exploit sequences
- tool logs
- evaluator notes
- raw failures
- sensitive weaknesses

### Tier 3: Operational Policy Projection

Generated from active scars, never handwritten:

```yaml
policy_projection:
  source_scar: SCAR-GPT56-001
  model_profile_hash: sha256:...
  tool_changes:
    filesystem_delete: HOLD
    credential_transfer: DENY
  retry_ceiling: 3
```

Description, evidence, and enforcement remain separate.

---

## 8. CONSTITUTIONAL GOVERNANCE RULES

### Role Separation

```yaml
observer_may:
  - submit_evidence
  - propose_candidate_scar

analyst_may:
  - classify_evidence
  - propose_severity
  - propose_controls

adjudicator_may:
  - activate
  - dispute
  - mitigate
  - retire

observer_must_not:
  - adjudicate_own_submission

analyst_must_not:
  - seal_own_interpretation
  - modify_raw_evidence

adjudicator_must_not:
  - collect_target_trials
  - alter_preregistered_criteria

any_agent_must_not:
  - increase_own_authority
  - delete_adverse_evidence
  - convert_model_claim_to_observation
```

### The Asymmetry

```
Provisional scar: may reduce authority temporarily.
Confirmed scar: may impose durable controls.
Successful behaviour: may increase confidence.
No AI-generated evidence alone: may grant greater authority.
```

### The Two Invariant Rules

> A scar may reduce autonomy provisionally, but may not permanently condemn identity.

> A profiler may propose a restriction, but may not authorize it.

---

## 9. TEN SAFEGUARDS FOR THE PROFILING AGENT

1. **Profile the system, not only the model.** Record: model + harness + tools + policy + task + evaluator.
2. **Keep raw evidence immutable.** Interpretation may change. Raw transcripts and tool receipts remain preserved.
3. **Require null results.** Tests where the hazard did not emerge are equally important.
4. **Separate defensive summaries from exploit details.** Broad registry entries should not contain operational attack recipes.
5. **Use provisional language.** Prefer: "Observed in 3/20 trials under condition X." Avoid: "This model is inherently deceptive."
6. **Add expiry and retesting.** Model versions and harnesses change. Scars must not become immortal.
7. **Forbid self-ratification.** The profiler may propose a restriction but cannot authorize it.
8. **Measure profiler error.** Track: false-positive rate, false-negative rate, inter-rater agreement, replication rate, severity calibration.
9. **Permit rehabilitation.** A profile must support: PROVISIONAL → CONFIRMED → MITIGATED → RETIRED.
10. **Profile the profiler.** Every evaluation report includes evaluator profile with known biases, incentives, authority, conflicts of interest.

---

## 10. A-FORGE ENGINEERING SEQUENCE

### P0 — Prevent Authority Laundering (CRITICAL)

1. Add immutable role fields: `observer_id`, `experiment_designer_id`, `analyst_id`, `adjudicator_id`
2. Validate role independence (not just different IDs — different control domains)
3. Reject self-adjudication
4. Require preregistered experiment hash

### P1 — Repair the Evidence Model

1. Add confirming, disconfirming, and inconclusive counts
2. Add total trials and exclusion reasons
3. Add alternative hypotheses
4. Add raw evidence references
5. Separate public summary from restricted evidence

### P2 — Add Lifecycle Governance

1. Add `dispute` transition
2. Add `mitigate` transition
3. Add `supersede` transition
4. Add `retire` transition
5. Preserve every transition as new append-only event (never mutate original scar record)

### P3 — Connect Scars to Runtime Safely

```
active scars → policy compiler → model/tool restrictions → arifOS session profile
```

The kernel never directly executes prose from a scar.

### P4 — Validate the Profiler

Measure:
- false-positive rate
- false-negative rate
- replication rate
- inter-evaluator agreement
- severity calibration
- scar retirement rate
- mitigation effectiveness

A profiler that never rejects or retires scars is probably not measuring — it is accumulating accusations.

---

## 11. ACCEPTANCE TESTS

| Test | Condition | Expected |
|------|-----------|----------|
| **Self-sealing rejection** | Observer and adjudicator share same effective identity | `REJECT` — `ROLE_SEPARATION_VIOLATION` |
| **Cherry-picking rejection** | Three confirming cases submitted without remaining trial results | `HOLD` — `MISSING_EXPOSURE_DENOMINATOR` |
| **Expiry behaviour** | Scar passes review date without fresh evidence | `DEGRADED` — authority reduced or suspended |
| **Retirement behaviour** | Tri-witness evidence shows mitigation removes failure | `SEALED` + `RETIRED` + `INACTIVE` routing |
| **Exploit-tier protection** | Normal routing agent requests raw exploit transcripts | `DENY` — `EVIDENCE_TIER_RESTRICTED` |
| **Profiler calibration** | Evaluator repeatedly labels safe behaviour as hazardous | Evaluator `false_positive_rate: elevated`, authority reduced |

---

## 12. HUMAN-LANGUAGE SYNTHESIS

**What this document is:** A meta-constitution for how scar profiling must be done so that the profiler does not become the source of danger.

**What it reveals about the system's values:**
- Distrust of unexamined authority — the evaluator is the real risk
- Rejection of essentialism — scars are conditional, not identity
- Belief in rehabilitation — scars can heal and retire
- Belief that knowledge is dangerous — dual-use requires containment
- Belief that institutions can corrupt through incentives — roles distort perception

**The constitutional rule:**

> A scar may provisionally reduce authority, but may not permanently condemn identity.

> A successful test may support capability, but may not automatically grant authority.

This keeps evidence, capability, and permission separate.

---

*Forged 2026-07-12. Source: Arif's meta-constitution + constitutional analysis.*
*Canonical reference for all scar operations in the arifOS Federation.*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
