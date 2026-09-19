---
name: skill-portfolio-audit
id: skill-portfolio-audit
version: 2.0.0-wave2-merged
description: "Unified skill-portfolio audit — drift + mesh + recursive + atlas. Replaces 4×AUDIT-{recursive-audit,drift-detector,agent-skill-mesh,skill-atlas}. Use when user asks to 'audit skills', 'find drift across surfaces', 'check skill mesh sync', 'unified skill inventory', or any cross-surface skill-portfolio question."
owner: AAA / F13 SOVEREIGN
risk_tier: low
floor_scope: [F1, F2, F4, F7, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - AUDIT-recursive-audit (sha256: 4228872ab95adf27e7ea4aa77ed129fdad186c42986bf421758266189b1134a7)
  - AUDIT-drift-detector (sha256: 4481e8d529de4aaf66b391650ce6cc4132d7b98895d967c6707d1a6df74ca308)
  - AUDIT-agent-skill-mesh (sha256: e42c1df82e812f54ca202658eeae9b417b1d1c8720e8053748400903b92a098c)
  - AUDIT-skill-atlas (sha256: fb5e86f626d5985cc33995c713208860a71528fe8e5164c33de78e99d085e7e4)
wave: 2
ts: 2026-09-16T22:42:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/audit-family/TOMBSTONE-AUDIT-*.json
triggers:
  - "audit skills"
  - "find drift across surfaces"
  - "check skill mesh sync"
  - "unified skill inventory"
  - "skill atlas"
  - "recursive audit"
  - "drift detector"
  - "skill mesh"
attention:
  load_class: low
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "audit"
    - "drift"
    - "skill mesh"
    - "skill atlas"
  output_contract:
    - "drift_report"
    - "mesh_report"
    - "atlas_index"
    - "remediation_receipt"
tags: [audit, drift, mesh, atlas, recursive, governance, F2, F4, F11]
---

# core/governance/skill-portfolio-audit

Unified cross-surface skill-portfolio audit. Merged from the 4×AUDIT family per the Wave 2 APEX verdict on the Hermes Skill Entropy Audit 2026-09-16.

## What this skill does

Replaces the 4×AUDIT cluster. For any "audit skills" / "find drift" / "skill mesh" / "skill atlas" question, this single skill:

1. **Discover** — enumerate skill surfaces (user overlay, install, profile overlays, archives).
2. **Inventory** — produce a unified atlas with id, owner, risk, floor scope, trigger count.
3. **Drift detect** — compare live runtime vs source-of-truth manifests.
4. **Mesh check** — verify same core skills across agents (Hermes, Kimi, AAA, Claude).
5. **Recursive audit** — re-audit the audit (does the audit itself contain drift?).
6. **Receipt** — emit a sealed drift/mesh/atlas report.

## Modes (sub-skills, selected by activation signal)

| Mode | Was | Trigger | Output |
|---|---|---|---|
| `mode=recursive` | AUDIT-recursive-audit | "audit skills" | recursive drift report |
| `mode=drift` | AUDIT-drift-detector | "find drift" | source-vs-runtime drift |
| `mode=mesh` | AUDIT-agent-skill-mesh | "skill mesh sync" | cross-agent mesh matrix |
| `mode=atlas` | AUDIT-skill-atlas | "skill atlas", "unified inventory" | gap-detection atlas |

## Usage

```bash
# In chat:
"audit skills"             → recursive mode
"find skill drift"         → drift mode
"check skill mesh"         → mesh mode
"skill atlas please"       → atlas mode
```

## Rollback

```bash
# Restore the 4 original skills:
git checkout entropy-wave2-pre-act-20260916T144144Z -- \
  skills/AUDIT-recursive-audit/ \
  skills/AUDIT-drift-detector/ \
  skills/AUDIT-agent-skill-mesh/ \
  skills/AUDIT-skill-atlas/
# Remove the canonical merged skill:
rm -rf skills/core/governance/skill-portfolio-audit/
```

## Provenance

- **Wave:** 2
- **AGI proposal order:** item 1 (lowest blast radius)
- **ASI verdict:** clean (no falsification)
- **APEX verdict:** SEAL ✓
- **F13 seal:** implied via "execute the best path fwd" against audit's planned Wave 2 batch
- **Witness:** 4 TOMBSTONE.json files at `/root/.hermes/.archive_skills_wave2/audit-family/`
- **Deprecation window:** 90 days (governance family — safety-critical)

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-AUDIT-agent-skill-mesh.md` — content absorbed from the retired `AUDIT-agent-skill-mesh` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
- `references/absorbed-AUDIT-drift-detector.md` — content absorbed from the retired `AUDIT-drift-detector` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
- `references/absorbed-AUDIT-recursive-audit.md` — content absorbed from the retired `AUDIT-recursive-audit` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
- `references/absorbed-AUDIT-skill-atlas.md` — content absorbed from the retired `AUDIT-skill-atlas` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
