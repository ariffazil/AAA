---
name: scar-integration
id: scar-integration
version: 2.0.0-wave2-merged
description: "Capture session failure patterns as constitutional scars — reusable diagnostics that prevent repeat mistakes. Replaces wisdom-scar-session-audit. Use when user asks to 'capture wisdom scar', 'session failure audit', 'scar ledger', 'constitutional scar', or any session-pattern-to-scar promotion."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F7, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - wisdom-scar-session-audit (sha256: f168d9ddf0418241b1afabc9393573ba9ea4de65e2e438be4efb81766763586d)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/scar-integration/TOMBSTONE-wisdom-scar-session-audit.json
triggers:
  - "capture wisdom scar"
  - "session failure audit"
  - "scar ledger"
  - "constitutional scar"
attention:
  load_class: medium
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "scar"
    - "failure pattern"
    - "wisdom"
  output_contract:
    - "scar_receipt"
    - "scar_severity"
    - "scar_remediation"
tags: [governance, scar, wisdom, session, F2, F7, F11]
---

# core/governance/scar-integration

Session failure pattern → constitutional scar promotion. Merged from wisdom-scar-session-audit per Wave 2 APEX verdict.

A scar is a reusable diagnostic that prevents repeat mistakes. Severity: P0-P4 per AGY/SCAR doctrine.

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/wisdom-scar-session-audit/
rm -rf skills/core/governance/scar-integration/
```

## Provenance
- **Wave:** 2, item 10
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-wisdom-scar-session-audit.md` — content absorbed from the retired `wisdom-scar-session-audit` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
