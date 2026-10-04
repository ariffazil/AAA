# Surgical Fix Delegation — Phase 8a Template

> **Purpose:** After a constitutional audit finds N critical violations, delegate surgical fixes to a coding agent (OpenCode) with enough precision that the fix is scoped, verifiable, and non-entropic.
> **Doctrine:** ΔS ≤ 0 — an unscoped fix delegation creates more entropy than it removes. Precision is the anti-entropy mechanism.

## Fix Spec Template

Every fix MUST carry:

1. **Exact file path** (absolute) + line number references from the audit
2. **Audit finding it resolves** (tie every fix to a falsified assumption)
3. **Surgical scope** — "make ONLY the changes described. Do NOT refactor or improve unrelated code."
4. **Build + test requirement** — `cargo build --release` must pass with zero NEW warnings; `cargo test` must pass with zero failures
5. **Hard constraints** — do NOT commit, do NOT deploy, do NOT touch untracked files
6. **Adaptation clause** — "if the module API differs from the spec, read the source and adapt. Report what you changed."

## Example: arifFLOW Fix Delegation (2026-08-10)

6 fixes from audit, each tied to a falsified assumption:

| # | Fix | File:Line | Resolves |
|---|-----|-----------|----------|
| 1 | Fail-closed client | `src/py/arifflow/client.py:76` — `allowed: True` → `False`, `action: "Allow"` → `"Block"` | FALSIFIED "system is fail-closed" |
| 2 | FQ single formula | `src/governance/invariants.rs:269-283` — legacy cost-based `self.fq` → alias of v2.1 `self.quotient` | FALSIFIED "FQ measures health" |
| 3 | Auto-enforcement timer | `src/main.rs:596` — spawn 10s interval thread calling `enforce()` | FALSIFIED "gate prevents ungoverned execution" |
| 4 | Chain validation | `src/main.rs:418` — `push_force()` → `push()` with chain checks | FALSIFIED "receipts immutable chain" |
| 5 | `/release` self-release hardening | `src/main.rs:511-519` — add `requester_id`, reject self-release | FALSIFIED "A-FORGE governed" — ⚠️ but see spoiler; the plaintext-check approach is spoofable theater |
| 6 | Wire VAULT999 | `src/main.rs` + `src/governance/vault999.rs` — call sealer on /ingest | FALSIFIED "VAULT999 provides commitment" |

## Delegation Context Block (passed via delegate_task)

```
## REPO
- Path: <repo root>
- Branch: main
- Current commit: <sha>

## RULES
1. Make ONLY the changes described. Do NOT refactor.
2. Follow existing code style.
3. If a fix has multiple approaches, pick the simplest that resolves the audit finding.
4. cargo build --release must pass, zero new warnings.
5. cargo test must pass, zero failures.
6. Report: exact unified diff, build summary, test summary.

## CONSTRAINTS
- Do NOT commit.
- Do NOT restart/deploy — leave the service running.
- Do NOT touch untracked files.
- Do NOT modify anything outside the listed fixes.
```

## Pitfalls

- **Spec drift:** if the auditor said "line 76" but the fix needs a different approach after reading the source, the subagent MUST report the deviation — not silently pick a new path.
- **Over-scoping:** "while I'm here, I'll fix X too" is how entropy enters. The constraint "do NOT refactor unrelated code" must be explicit and repeated. Real case (arifFlow 2026-08-10): agent was told 5 surgical fixes, also rewrote FQ dual-formula + added a `/release` "security" check + imported an unused `Vault999Sealer`. The scope expansion broke 2 tests AND added spoofable theater. **Always `git diff --stat` after the agent returns and review every changed file.** See `verify-before-report` skill → "Scope creep in coding-agent diffs" for the full diff-review pattern (the 4-step pattern + spoofable-theater markers).
- **Spoofable security theater (the `/release` fix above) ⚠️:** the row 5 approach (`requester_id` + plaintext `if req.requester_id == "arif" { allow }`) LOOKS like authorization but is trivially bypassable — any actor can pass `requester_id="arif"` themselves. **Plaintext string checks that compare a request-supplied field to a privileged identity are F9-tier theater — DO NOT ship.** Real auth requires SCT (Ed25519 session capability tokens) routed through arifOS. The arifFlow 2026-08-10 implementation of this row was reverted after Hermes caught it in review; defer to F13 design instead.
  - **Markers of spoofable theater** (any of these = reject the change): `if req.<field> == "arif"`, `if req.role == "admin"`, `if req.actor == "sovereign"`, any request-supplied string compared to a privileged identity without cryptographic verification.
  - **Right path:** SCT-mediated identity via arifOS, or honest "advisory only" with explicit `not_authorized_in_runtime` docstring.
- **The "pre-existing test failure" mislabel (2026-08-10):** coding agents report "tests fail but pre-existing, not from my changes." The failures often come from their OWN edits to shared modules. Always stash-verify before accepting: `git stash && cargo test --lib <module> 2>&1 | tail -5 && git stash pop`. If clean HEAD passes and working tree fails, the failures are from the agent's changes — never ship with them. Update stale tests to the new semantics deliberately (e.g. after a ratified formula migration), or revert the change. See `verify-before-report` for the full pattern.
- **Deployment separation:** the fix subagent never deploys. Coordinator deploys (T2 announce), restarts service, then runs the verification probe. Subagent returns diffs; coordinator owns the blast radius.
- **Verify after deploy:** always run the post-fix probe (verify_fixes.py pattern — one probe per audit finding, PASS/FAIL) against the LIVE service after restart. A green build is not a green system.
- **Make the re-audit recurring (Phase 8d):** after the fix is verified, install a lightweight drift-check script + weekly cron so the institution audits itself, not just the human. One-shot audit → fix → re-audit is observation. Scheduled drift check = institution. See SKILL.md Phase 8d.

## Verification Probe Pattern

Write a small Python probe BEFORE the fixes land (so it tests behavior, not implementation):

```python
# One check per audit finding:
# 1. fail-closed: construct client with unreachable base_url → check().allowed must be False
# 2. FQ consistency: /health quotient == enforcement quotient (same formula)
# 3. auto-enforcement: invariants cycle_count changes / logs show cycles
# 4. chain validation: /ingest with malformed chain → rejected or logged
# 5. self-release: POST /release with requester_id == actor_id → HTTP 403
# 6. VAULT999: sealed file grows after /ingest
```

Each probe prints `[PASS]` or `[FAIL]` with detail. Exit non-zero if any fail. Run it against the live service AFTER deploy — before reporting success to the sovereign.
