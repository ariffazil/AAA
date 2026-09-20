# The newest-state trap

When a report asserts integrity ("chain intact", "data corrected", "all hashes match"), test it
against the **object**, not against the state the reporter happened to open. A claim can be true of
the newest entry and false of the set — and that gap is where the damage hides.

## Rules

- **A mutable artifact written to a fixed path destroys its own ledger.**
  If a cycle log records `sha256(OUT/<NAME>.png)` and the writer always overwrites that path, every
  earlier row hashes a file state that no longer exists. Re-hash **every** row's artifact and compare
  to the row. Checking only the newest row is how "chain intact" gets reported over a mostly-stale log.
  Fix direction: content-address the artifact (`<NAME>-<hash8>.png`), or add `superseded_by` to the row.

- **Resolve the cited paths before concluding a deliverable is missing.**
  Reporters name plausible paths that do not exist; the artifacts often sit elsewhere. A verifier who
  concludes "not built" from a path miss has produced a false negative, which damages as much as a
  false positive. Report path discrepancies explicitly rather than silently correcting them.

- **Re-derive the value; do not confirm that an edit was made.**
  "Corrected" is a claim about the object. Run the function and read what it returns. A component can
  gain a working gate in one area while the defect named in the report sits untouched in another.

- **Audit your own probe before you publish.**
  Run the check against a known-good input first. A probe that mis-reads a schema — treating a scalar
  field as a list, matching an exact class string when a variant suffix exists — will appear to refute
  a correct claim, and the auditor then reports the other agent as wrong.

- **A check that always returns the same answer is broken, not reassuring.**
  Regex that stops at the first delimiter, or a pattern that misses a variant suffix, yields a clean
  result that means nothing. Prove each detector can FAIL before trusting it to pass.

- **Re-count rather than repeat.**
  Reported totals drift in both directions. Re-run the counter against the store.

## Auditing is not owning

- An auditor may record **conditions and non-negotiables**; the auditor may not pick which lane wins.
  Recommending your own lane as owner is self-authorization — the same defect the authority envelope
  forbids for executors.

- State the hazard **structurally** ("two components compute the same quantity, so they can disagree")
  rather than as a preference between teams. Structural framings survive a change of owner; preferences
  do not.

- When a defect recurs across independent lanes, name the shared root cause. That is the finding — not
  a scorecard of who was wrong.
