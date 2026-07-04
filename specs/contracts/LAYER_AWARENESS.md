# Layer Awareness Execution Contract

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*

This contract defines the machine-readable obligations for agents operating across Layers 2–4 of the arifOS federation.

## L2: Security (Auth · Auth · Audit)
- **Obligation**: Every irreversible action must carry an `888_HOLD` metadata block.
- **Obligation**: Every tool execution must emit a `receipt_hash` anchored to VAULT999.
- **Obligation**: Agents must verify `identity_scope` before requesting system-level tools.

## L3: Structural (A2A Alignment)
- **Obligation**: Cross-agent communication must use the `A2A v1.0.0` protocol with `epistemic_signal` headers.
- **Obligation**: Any drift in federation topology (e.g., unauthorized organ registration) must be flagged as a policy violation.

## L4: Grade (Triple-A Sovereign)
- **Obligation**: All substantive claims must carry an epistemic tag: `CLAIM`, `PLAUSIBLE`, `HYPOTHESIS`, `ESTIMATE`, or `UNKNOWN`.
- **Obligation**: G-score must be maintained above `0.80` for high-stakes reasoning tasks.

---

**Failure to uphold this contract triggers immediate VOID status for the current session.**
