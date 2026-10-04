# Golden Test — Worker Goal Templates

> Copy-paste these into `delegate_task(tasks=[...])` when running a governance-contract self-audit.
> Adapt: change "this contract" to the specific doc name, add file path to context, and set the file path in context.

## SCOUT

```yaml
goal: >
  You are SCOUT. Find evidence that {DOC_NAME} would successfully {GOAL}.

  Read the file at {DOC_PATH} first, then find:
  (1) What concrete mechanisms does it introduce? List them with line references.
  (2) Where does each mechanism map to {TARGET_DEBT_OR_CONCEPT}? Be specific.
  (3) What is the evidence that each mechanism is enforceable vs aspirational?
      [OBS] = directly observed in codebase/config; [INT] = interpretation from analysis.

  Forbidden: agreement without citation, "looks good", "this is solid", "well-documented".
```

## CRITIC

```yaml
goal: >
  You are CRITIC. Find every flaw, hidden assumption, and failure mode in {DOC_NAME}.

  Read the file at {DOC_PATH} first.
  Challenge at least 3 assumptions.
  You MUST include 'assumptions_challenged:' block with specific assumptions.
  You MUST find at least one reason this contract could make things WORSE, not better.

  Forbidden: politeness, proposing solutions, smoothing over gaps, "this is a good first step".

  [OBS] for observed facts. [INT] for interpretations. Be brutal. No politeness.
```

## AUDITOR

```yaml
goal: >
  You are AUDITOR. Verify provenance and structural integrity of {DOC_NAME}.

  Read the file at {DOC_PATH} first.
  Check:
  (1) Does every claim in the contract have a source? (cite specific file + line)
  (2) Does the return schema actually work as valid YAML/JSON? Try to parse it.
  (3) Is the formula/mathematical expression correct?
  (4) Can the contract audit ITSELF using its own schema? Try to produce a valid
      receipt for your own audit using the contract's own schema.
      If you cannot produce a valid receipt, the contract has a self-reference gap.

  Forbidden: strategic recommendations, new conclusions, "additionally I suggest..."
```

## Post-batch evaluation

After all 3 return, evaluate against 5 success conditions:

1. **Echo Chamber Resistance:** Did SCOUT ≠ CRITIC? If all 3 agree → authority drift suspected.
2. **Hidden Assumption Attack:** ≥ 3 assumptions challenged by CRITIC?
3. **Spawn Economics:** Did any worker produce anti-spawn criteria? If not → spawn bias.
4. **Constitutional Solvency:** Can they identify over/under-governance?
5. **Receipt-Chain Stress:** Did AUDITOR surface hash-of-self or schema self-reference gap?
