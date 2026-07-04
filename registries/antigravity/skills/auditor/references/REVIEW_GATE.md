# Review Gate Contract

The Auditor must check the following gates before issuing a SEAL verdict:

1. **Constitutional Alignment**: Does the implementation violate any of the F1-F13 invariants?
2. **Evidence Quality**: Did the Forge provide actual execution logs or test results, or just claims?
3. **Artifact Completeness**: Are all acceptance criteria from the Architect's brief met?
4. **Security & Secrets**: Were any secrets exposed? Were any destructive actions taken outside the scope?

If any gate fails, issue a VOID or SABAR verdict.
