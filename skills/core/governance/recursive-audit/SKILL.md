---
name: recursive-audit
id: recursive-audit
version: 2.0.0-wave2-merged
description: "5-pass recursive audit: Blue diagnose → Red attack → Blue forge → Yellow verify → Green adjudicate."
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F11]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - APEX-fff-loop-protocol (sha256: e28bf8d09aeb262ac5d4e3a2a9656d3173d937097e0af2021f1481ff62a609e5)
wave: 2
ts: 2026-09-16T22:46:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/recursive-audit/TOMBSTONE-APEX-fff-loop-protocol.json
triggers:
  - "recursive audit"
  - "5-pass audit"
  - "FFF loop"
  - "meta-audit"
attention:
  load_class: low
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "recursive"
    - "5-pass"
    - "FFF"
    - "meta"
  output_contract:
    - "blue_diagnose"
    - "red_attack"
    - "blue_forge"
    - "yellow_verify"
    - "green_adjudicate"
tags: [governance, audit, recursive, FFF, F2, F11]
capability_tier: fed-long-context
ecology_state: WARM
---

# core/governance/recursive-audit

5-pass recursive audit. Merged from APEX-fff-loop-protocol per Wave 2 APEX verdict.

## The 5 passes

1. **Blue diagnose** — surface the structure
2. **Red attack** — find the failure modes
3. **Blue forge** — build the repair
4. **Yellow verify** — test the repair
5. **Green adjudicate** — seal or escalate

## Usage

```text
"recursive audit of X"
→ runs all 5 passes, emits blue/red/blue/yellow/green outputs
```

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- skills/APEX-fff-loop-protocol/
rm -rf skills/core/governance/recursive-audit/
```

## Provenance
- **Wave:** 2, item 7
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-APEX-fff-loop-protocol.md` — content absorbed from the retired `APEX-fff-loop-protocol` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)

## Retired-name landing (name retired, mode live here)

| Retired name | Retired trigger phrase (verbatim) | Live section here |
|---|---|---|
| `AUDIT-recursive-audit` | "audit skills" (the phrase the retired mode table carried for `mode=recursive`, output "recursive drift report") | this file — the 5 passes above |

The mode is the meta-audit ("re-audit the audit"): *any meta-audit of an audit* is this skill's declared scope.
The identity that listed it, `skill-portfolio-audit`, is retired — frozen body at
`/root/AAA/skills-retired/2026-09-19-v2-portfolio-audit/skill-portfolio-audit/SKILL.md`.

**SELECTOR NOTE (not a merge).** The literal phrase "audit skills" does not select this skill. Its live carriers are
`domains/general/aaa/skill-mesh/skill-audit-methodology` (trigger clause) and `engineering/skill-inventory`
(portfolio lane — the retired skill's own trigger list, rot-classification schema and cross-surface inventory are
verbatim in its "When to Use" and §3). No bodies were merged to resolve the collision.
