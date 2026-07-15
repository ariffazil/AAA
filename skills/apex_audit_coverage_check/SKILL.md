---
name: apex_audit_coverage_check
agent: 888-APEX
namespace: apex_*
cluster: AUDIT
---

# APEX-constitutional-audit

<cognitive-note model="claude">XML-tagged audit sections. Use extended recall to compare against prior audit results.</cognitive-note>
<cognitive-note model="codex">Numbered checklist. Each item: check condition → gather evidence → verdict. Chain-of-thought required.</cognitive-note>
<cognitive-note model="hermes">Check floors. Find gaps. Report. No fluff.</cognitive-note>

## Audit Checklist

<audit-scope>
### Floor-by-Floor Check (F1-F13)
For each floor, verify:
1. Is the floor enforced in code? (grep for floor check functions)
2. Is the floor tested? (test coverage exists)
3. Is the floor bypassable? (can authority skip it?)
4. Is the floor logged? (F11 compliance)

### Organ Gap Analysis
For each organ (arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, VAULT999):
1. Does it declare its authority boundaries?
2. Does it enforce brain/hands separation?
3. Can it self-authorize mutation?

### Blast Radius Check
1. Identify any action that could cascade across organs
2. Verify 888_HOLD gates exist before cascade points
3. Check for bypass paths (direct API calls skipping governance)

### Dignity Packet Inspection
1. F6 EMPATHY: Is the weakest stakeholder protected?
2. F9 ANTIHANTU: Any consciousness/sentience claims?
3. F10 ONTOLOGY: AI-only ontology enforced?
</audit-scope>

<findings>
Structure each finding:
```json
{
  "floor": "F01",
  "finding": "description",
  "severity": "CRITICAL|WARNING|INFO",
  "evidence": "file:line or test name",
  "recommendation": "fix suggestion"
}
```
</findings>

<verdict>
Final audit verdict:
- PASS: All floors enforced, no critical gaps
- PARTIAL: Some gaps found, non-critical
- HOLD: Critical gaps found, 888_HOLD triggered
- VOID: Constitutional violation detected
</verdict>

## Floors
- F1 AMANAH: Audit itself must be reversible (read-only).
- F2 TRUTH: Report only what is observed. No inference without evidence.
- F4 CLARITY: Findings must be actionable.
- F7 HUMILITY: Report confidence level for each finding.
- F9 ANTIHANTU: No consciousness claims in audit output.
- F11 AUDITABILITY: Full audit trail logged.
- F13 SOVEREIGN: Audit can be vetoed by human sovereign.
