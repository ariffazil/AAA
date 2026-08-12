# Scar Record: scar-001-esm-sct-silent-fail

```yaml
scar_id: scar-001-esm-sct-silent-fail
timestamp: 2026-08-13T00:30:00Z
failure_pattern: "require(node:crypto) silently failed in ESM scope, causing all SCT verifications to return {valid:false}"
root_cause: "CommonJS require() inside ESM module (package.json type:module). The try/catch was designed for crypto errors, not module-system ReferenceErrors. The ReferenceError was swallowed, returning {valid:false} without explanation."
successful_recovery: "Commit cb341202 — replaced require() with top-level ESM imports (createHmac, timingSafeEqual from node:crypto)"
scar_pressure: 0.85
test_fixture: "grep -rn 'require(\"node:' src/ --include='*.ts' in ESM packages"
generated_skill: "FORGE-esm-require-guard"
skill_path: "/root/.agents/skills/FORGE-esm-require-guard/SKILL.md"
verification_method: "known_answer"
verification_result: "PASS (logic verified by commit diff inspection)"
promoted_by: "333-AGI (OpenCode FI-001)"
promotion_date: "2026-08-13T01:00:00Z"
behavior_change: "Next TS commit to ESM packages scanned for require() calls"
review_date: "2026-11-13"
status: ACTIVE
foodset_derived: true
```
