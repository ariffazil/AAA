# Decoy Catalogue — shapes of a control that does not control

Each entry: the shape, the tell that exposes it, and the probe that proves it. Use as a checklist when
CALLER_PROOF or EFFECT_PROOF looks suspicious.

| # | Shape | Tell | Probe |
|---|---|---|---|
| 1 | Gate with zero callers | Strong name, real code, no invocation | Sweep all scheduler surfaces and loader imports; grep the identifier tree-wide and confirm the query could match |
| 2 | Health check returning a literal | Fixed `status: "healthy"`, no dependency read | Read the handler body; stop a dependency and see whether the output changes |
| 3 | Metric that is a constant or flag | `rejections = 0` from config, or a 0/1 flag | Trace the value to source; if it derives from a setting rather than events, it is theatre |
| 4 | Guard whose fallback is permissive | All checks fail → return the ranked result anyway | Force every check to fail; unchanged output means it cannot refuse |
| 5 | Blocklist masquerading as a rule | Deny-list of literals, each one yesterday's known-bad value | Introduce a new bad value; if it passes, this is a patch, not a policy |
| 6 | Metadata asserting what the artifact contradicts | Declares `hidden: true` while the renderer prints it | Render, then grep the artifact for the supposedly-suppressed content |
| 7 | Mechanism imported but never invoked | Containment/sandbox module on the import line, absent from the execution path | Grep the symbol; appearing only on the import line means imported, not installed |
| 8 | Attestation matching nothing on disk | Attested digest matches no file | Re-hash every path in the attestation; check mtimes against the attestation time |
| 9 | Label overriding its own fact | One payload holds `drift: false` and a drift-derived block | Print both fields from one response; compare tiers against the evidence hierarchy |
| 10 | Defaulted reason code | `reason or "SPECIFIC_CAUSE"` | Locate the measurement that produced the cause; a fallback string is not a diagnosis |
| 11 | Gate that can reorder but not refuse | Ranking function with no denial return | Inspect the return paths; if every branch returns a value, nothing is blocked |
| 12 | Evidence that exists but does not correspond | Receipt present, event not proven | Ask what the receipt would look like had the event *not* happened; if identical, it is not evidence |

## The positive pattern — what to copy, not just what to flag

When you find a genuine control, characterise it so others can be modelled on it:

1. **It can fail**, with a defined failure vocabulary (auth, network, timeout, refusal).
2. **It records both outcomes** — success *and* failure — with an identifier the caller can verify.
3. **It has actually run**, with retained evidence of a pass and a failure.
4. It distinguishes *generated* from *delivered*, and *delivered* from *receipted*.
5. It carries its invariant in its own header, so the next reader knows what it promises.

A control that has never rejected anything, and cannot express rejection, has not been tested — it has
merely been present.

## Reporting the counterexamples

Balance every decoy list with the controls that hold. Verifying only failures produces a doctrine of
universal distrust, which is a false claim in its own right and removes the operator's ability to rely
on anything. The honest finding is almost always **uneven integrity**, with the failures clustered in
the path the institution most depends on.
