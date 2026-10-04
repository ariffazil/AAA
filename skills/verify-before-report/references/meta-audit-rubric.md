# Meta-Audit Rubric — For Evaluating Audit Reports

> Origin: Arif Fazil (F13 SOVEREIGN), 2026-08-10
> Context: arifFlow constitutional audit by OpenCode (DeepSeek V4 Pro)
> Use: When evaluating any audit/report produced by a sibling agent or subagent

## The 5 Tests

Apply these to ANY audit report before integrating its findings:

| # | Test | Question | How to evaluate |
|---|------|----------|-----------------|
| 1 | **Reality Test** | Did the auditor discover something unexpected by current doctrine? | Check if findings include items NOT previously known or discussed. If all findings match pre-existing concerns → possible confirmation bias. |
| 2 | **Contradiction Test** | Did at least one assumption get weakened or falsified? | Count falsified + weakened vs supported. If zero contradictions → audit may be validating narrative, not probing reality. |
| 3 | **Bridge Test** | Were integration nodes found through evidence, not analogy? | Check if bridge/integration findings cite specific code paths, runtime probes, or file inspections. Analogy-only findings are INT, not OBS. |
| 4 | **Strawberry Test** | Were critical dependencies proven through code-path or runtime evidence? | Verify that critical component rankings cite actual dependency traces, not architectural assumptions. |
| 5 | **Unknown Test** | Did the auditor return UNKNOWN when evidence was insufficient? | Count UNKNOWN labels. Zero unknowns in a complex system = auditor is overconfident or fabricating certainty. |

## Red Flags (audit is likely auditing narrative, not reality)

- All findings are SEAL / supported / positive
- Zero contradictions found
- Zero UNKNOWN labels
- Zero falsified assumptions
- Findings perfectly match what the commissioning party already believed
- No unexpected dependencies or hidden coupling discovered

## Green Flags (audit is likely genuinely probing)

- Unexpected dependencies found
- Governance drift identified
- Hidden bridge nodes discovered
- Undocumented coupling exposed
- Assumptions proven wrong
- UNKNOWN labels present where evidence is insufficient
- At least one finding contradicts the commissioning party's prior beliefs

## Key Question

> What is the most surprising finding that the commissioning party did NOT expect before the audit began?

If the auditor can answer this with evidence, the audit is likely valuable.
If not, it may be a restructured version of what was already known.

## Applied Example (arifFlow audit, 2026-08-10)

| Test | Result | Key Evidence |
|------|--------|-------------|
| Reality | ✅ PASS | Daemon doesn't write receipts to disk; external clients do |
| Contradiction | ✅ PASS | 2 falsified (VAULT999, cross-organ coordination) + 3 weakened |
| Bridge | ✅ PASS | MCP shim, FQ mirror timer found via code inspection |
| Strawberry | ✅ PASS | push_force() chokepoint, daemon SPOF traced to source |
| Unknown | ✅ PASS | 6 unknowns declared (who writes receipts? scheduler tested?) |

**Meta-audit verdict: SEAL** — All 5 tests passed. Audit is constitutionally sound.
**System verdict: SABAR** — arifFlow's declared and observed architectures diverge significantly.
