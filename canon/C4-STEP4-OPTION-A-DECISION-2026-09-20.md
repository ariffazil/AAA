# C4 STEP4 Option A Decision (2026-09-20)

F13 SOVEREIGN 'execute all' directive applied.

- Status: DECIDED
- Action: Option A selected — additive plane namespacing (`planes: {transport, operation, governance, authority, persistence}`) with each field namespaced. Keep legacy top-level fields as aliases with `plane_of:` provenance. No verdict semantics change.
- Implementation: Open loop. Code changes to `runtime/verdict.py`, `runtime/contradiction_detector.py`, and `tools/session.py` to be done separately.
