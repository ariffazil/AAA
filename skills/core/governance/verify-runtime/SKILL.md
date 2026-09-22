---
name: verify-runtime
id: verify-runtime
version: 2.0.0-wave2-merged
description: "Verification-as-terminal-state — a task is done ONLY when verified."
owner: A-FORGE
risk_tier: low
floor_scope: [F2, F4, F7, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - FORGE-verify-runtime (sha256: 19d695c89fdc4ddfd411d95eb13e748176f0ee4cf061de3ddcb8ddb2583f62d1)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/verify-runtime/TOMBSTONE-FORGE-verify-runtime.json
triggers:
  - "verify runtime"
  - "verification as terminal state"
  - "task done only when verified"
attention:
  load_class: low
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "verify"
    - "terminal state"
    - "done only when"
  output_contract:
    - "verification_pass"
    - "verification_fail"
    - "verification_hold"
tags: [governance, verification, runtime, F7, F11]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# core/governance/verify-runtime

Verification-as-terminal-state. Merged from FORGE-verify-runtime per Wave 2 APEX verdict.

A task is done only when verified. Verification produces one of three verdicts:
- **verification_pass** — proceed to SEAL
- **verification_fail** — return to BUILD
- **verification_hold** — escalate to F13

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/FORGE-verify-runtime/
rm -rf skills/core/governance/verify-runtime/
```

## Provenance
- **Wave:** 2, item 8
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-FORGE-verify-runtime.md` — content absorbed from the retired `FORGE-verify-runtime` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
