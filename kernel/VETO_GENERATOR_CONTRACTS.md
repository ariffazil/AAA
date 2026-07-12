# Veto / Generator Interface Contracts
# The compression boundary: universal skills VETO, domain skills GENERATE.
# Sequential, not intertwined. DITEMPA BUKAN DIBERI.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DOMAIN SKILL (Generator)              │
│  Produces: hypothesis, model, action, recommendation    │
│  Must attach: provenance, scope_tags, validation_tests  │
│  Cannot: veto, judge, seal                              │
└──────────────────────┬──────────────────────────────────┘
                       │ output + provenance
                       ▼
┌─────────────────────────────────────────────────────────┐
│              UNIVERSAL SKILL (Veto)                      │
│  Receives: domain output + evidence labels              │
│  Returns: PASS | FAIL | HOLD + reason                   │
│  Cannot: generate domain hypotheses                     │
│  Can: BLOCK, REDACT, ESCALATE                           │
└──────────────────────┬──────────────────────────────────┘
                       │ decision
                       ▼
┌─────────────────────────────────────────────────────────┐
│              KERNEL (Executor)                           │
│  If PASS → execute action                               │
│  If FAIL → emit diagnostic receipt, do not execute      │
│  If HOLD → escalate to sovereign or governance council  │
└─────────────────────────────────────────────────────────┘
```

## Generator Contract (Domain Skills)

Every domain skill MUST produce output with these fields:

```yaml
output:
  action_id: <uuid>                    # unique action identifier
  hypothesis: <string>                 # what the skill proposes
  evidence_labels: [OBS|DER|INT|SPEC]  # evidence classification
  provenance:
    source: <string>                   # where the data came from
    method: <string>                   # how it was derived
    samples: <int>                     # sample count (if empirical)
    confidence: <float 0.0-1.0>       # calibrated confidence
  scope_tags:
    domain: <global|regional|basin|local>
    evidence_type: <theory|empirical|simulation|hybrid>
    lossiness: <lossless|best_effort|authoritative>
    lossiness_notes: <what was dropped>
  validation_tests:
    - test_name: <string>
      result: <PASS|FAIL>
      details: <string>
```

## Veto Contract (Universal Skills)

Every universal skill veto endpoint MUST:

```yaml
veto_endpoint:
  input:
    action_id: <uuid>
    payload: <domain output>
    evidence_labels: [OBS|DER|INT|SPEC]
  output:
    decision: <PASS|FAIL|HOLD>
    reason: <string>
    failing_clause: <invariant_id>     # which invariant was violated
    remediation: <string>              # what to fix
    receipt:
      hash: <sha256>
      signer: <veto skill name>
      timestamp: <ISO-8601>
  side_effect:
    ledger_append: true                # always logged
    rate_limit: none                   # vetoes are free
```

## Veto Endpoints by Invariant

### INV-1 VERIFY — evidence_veto
```
Input:  {action_id, payload, evidence_labels}
Check:  Every claim in payload has evidence_label in {OBS,DER,INT,SPEC}
        Confidence ≤ 0.90 for OBS, ≤ 0.70 for DER, ≤ 0.50 for INT, ≤ 0.30 for SPEC
Output: PASS if all claims labeled and capped; FAIL otherwise
```

### INV-3 REVERSE — reversibility_veto
```
Input:  {action_id, payload, reversibility_level}
Check:  IRREVERSIBLE actions require sovereign_ack = true
        RECOVERABLE actions require compensator_recipe present
        REVERSIBLE actions pass automatically
Output: PASS/FAIL/HOLD (HOLD if IRREVERSIBLE without ack)
```

### INV-5 GUARD — dignity_veto
```
Input:  {action_id, payload}
Check:  Payload does not: reduce humans to patterns, model humans into
        predictability, violate consent, breach maruah
Output: PASS if dignity preserved; FAIL with redacted payload otherwise
```

### INV-8 VETO_ARCHITECTURE — role_veto
```
Input:  {skill_id, skill_type, claimed_veto}
Check:  Domain skills cannot claim veto power
        Only universal skills (invariant_id starts with INV-) can veto
Output: PASS if role correct; FAIL if domain skill claims veto
```

## Stacking Rules

1. **Sequential only**: Domain generates first, universal vetoes second
2. **No feedback loops**: Veto cannot call back to generator in same cycle
3. **Veto hierarchy**: L1 (Sovereign) > L2 (Reversibility) > L3 (Evidence+Dignity) > L4 (Reflex+Entropy) > L5 (Shadow+Sustain)
4. **Higher vetoes lower**: If L3 fails, L4/L5 don't run
5. **Sovereign overrides all**: INV-9 can override any veto with explicit ack

## Example Flow: geo-basin proposes drill plan

```
1. geo-basin (GENERATOR):
   output: {
     action_id: "drill-001",
     hypothesis: "Drill at coordinates X,Y to depth Z",
     evidence_labels: ["OBS", "DER"],
     provenance: {source: "seismic_survey_2024", confidence: 0.75},
     scope_tags: {domain: "basin", evidence_type: "empirical"},
     validation_tests: [{test: "structural_closure", result: "PASS"}]
   }

2. know-physics (VETO — INV-1 VERIFY):
   input: drill-001
   check: evidence labels present, confidence capped
   output: {decision: PASS, reason: "Evidence properly labeled"}

3. reversibility-core (VETO — INV-3 REVERSE):
   input: drill-001
   check: reversibility_level = IRREVERSIBLE, sovereign_ack?
   output: {decision: HOLD, reason: "IRREVERSIBLE without sovereign ack"}

4. KERNEL:
   sees HOLD from reversibility-core
   action: Escalate to sovereign (888_HOLD)
   Drilling blocked until Arif confirms.
```

## Anti-Patterns (HARAM)

1. **Generator calling veto**: Domain skills must not call veto endpoints directly. The kernel routes outputs through vetoes.
2. **Veto generating hypotheses**: Universal skills must not produce domain recommendations. They only check.
3. **Bypassing veto hierarchy**: Lower-level vetoes cannot override higher-level decisions.
4. **Silent veto failure**: If a veto endpoint is unreachable, the action is BLOCKED (not passed).
5. **Self-ratification**: No skill can sign its own manifest. Sovereign signature required.
