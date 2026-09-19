---
name: multi-harness-sync
id: multi-harness-sync
version: 2.0.0-wave2-merged
description: "Multi-agent harness skill-catalog synchronization — Hermes, Kimi, AAA, Claude, OpenCode, Codex."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F4, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - federated-skill-architecture (sha256: e760b59e03904232f5c1a40ebb4c4d9c093c1c7b7448202793fb0491383ce020)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/federation-multi-harness/TOMBSTONE-federated-skill-architecture.json
triggers:
  - "sync skill catalogs"
  - "align AAA canonical"
  - "unify across harnesses"
  - "multi-agent skill mesh"
attention:
  load_class: medium
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "sync"
    - "align"
    - "unify"
    - "catalog"
  output_contract:
    - "sync_report"
    - "drift_matrix"
    - "canonical_diff"
tags: [federation, sync, catalog, multi-harness, F2, F4]
---

# core/federation/multi-harness-sync

Multi-harness skill catalog synchronization. Merged from federated-skill-architecture per Wave 2 APEX verdict.

## Usage

```text
"sync Hermes with Kimi skill catalogs"
→ produces sync_report + drift_matrix + canonical_diff
```

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/federated-skill-architecture/
rm -rf skills/core/federation/multi-harness-sync/
```

## Provenance
- **Wave:** 2, item 6
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-federated-skill-architecture.md` — content absorbed from the retired `federated-skill-architecture` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
