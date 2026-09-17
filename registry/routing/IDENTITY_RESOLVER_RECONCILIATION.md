# Identity Resolver — Reconciliation Note (333-AGI, 2026-09-18)

## What happened
- v1 (full API: `Verdict` / `IdentityHold` / `guard(text, capability=...)` / `identity_bound` / `assert_clear` / `load_registry` / `resolve`) was written for SCAR-2026-09-15-001. Consumers were built against it: the T2I gate in `skills/qwencloud-image-generation/scripts/image.py`, `tests/constitutional/test_identity_resolver.py`, and `instructions/naming-doctrine.md`.
- The arifOS-repo copy was deleted in `490db4665` (repo flatten/clean); a **rewritten v2** (different API: `guard(tool_name, args)`, `GuardianVerdict` ALLOW/BLOCK/HOLD, `IDENTITY_GATE_MODE` precise/strict, CLI) landed at this path via nightly consolidation `c3ac34677`.
- Result: the gate went **phantom** — image.py import failed (exit 3 HOLD — fail-closed), tests failed to collect. "Doctrine without a gate is decoration."

## Resolution (2026-09-18)
- v1 (contract-matching) **restored** as the canonical `identity_resolver.py`. Full suite 22/22 pass; ledger receipts live.
- v2 **parked** as `identity_resolver_v2.py.draft-333-20260918` — **not deleted**.
- **Open question (888/F13):** v2's "precise mode" semantics — gate only where identity is *produced or bound*, allow mere mentions — versus v1 behavior. Do NOT re-activate v2 without a judge verdict + consumer migration.

## Contract
- Callers: `skills/qwencloud-image-generation/scripts/image.py` (T2I/I2I gate), `tests/constitutional/test_identity_resolver.py`.
- Registry: `identity_continuity.yaml` (this dir). Receipts: `intercept_log.jsonl` (this dir).
