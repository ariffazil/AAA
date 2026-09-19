---
name: dignity-substrate
id: dignity-substrate
version: 2.0.0-wave2-merged
description: "Cultural, dignity, and sovereignty lens for AAA state records."
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F7, F9, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - AGI-nusantara-substrate (sha256: 4e7f04d7529a6e7b1c3f1f81604df6336a6e1c122a4a362beeb22ea78b6bd689)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/dignity-substrate/TOMBSTONE-AGI-nusantara-substrate.json
triggers:
  - "apply Nusantara substrate"
  - "cultural dignity check"
  - "sovereignty lens"
  - "Nusantara intelligence"
attention:
  load_class: low
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "Nusantara"
    - "dignity"
    - "sovereignty"
    - "cultural lens"
  output_contract:
    - "dignity_audit"
    - "sovereignty_assessment"
    - "cultural_lens_report"
tags: [governance, dignity, sovereignty, cultural, F7, F9, F11]
---

# core/governance/dignity-substrate

Cultural, dignity, and sovereignty lens. Merged from AGI-nusantara-substrate per Wave 2 APEX verdict.

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/AGI-nusantara-substrate/
rm -rf skills/core/governance/dignity-substrate/
```

## Provenance
- **Wave:** 2, item 9
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-AGI-nusantara-substrate.md` — content absorbed from the retired `AGI-nusantara-substrate` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
