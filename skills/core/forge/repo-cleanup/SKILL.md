---
name: repo-cleanup
id: repo-cleanup
version: 2.0.0-wave2-merged
description: "Unified filesystem hygiene scan — broken symlinks + secret leaks + key age + missing rotation. Replaces FORGE-{symlink-audit,secret-hygiene}. Use when user asks to 'scan /root for broken symlinks', 'audit secrets', 'check key rotation', 'find plaintext secrets', 'repo cleanup', or any filesystem-hygiene scan."
owner: A-FORGE
risk_tier: medium
floor_scope: [F1, F2, F4, F7]
doctrine: /root/AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md
merged_from:
  - FORGE-symlink-audit (sha256: 7415750584a70c467a0a80ec4307059103b22061410ebf285946f4854dc42734)
  - FORGE-secret-hygiene (sha256: 79a6e1d5ba4565afabe94539fe34d1a7f61a2bbf99096145addb5aea8757e1d9)
wave: 2
ts: 2026-09-16T22:44:00Z
audit: /root/.hermes/reports/hermes-skill-entropy-audit-2026-09-16.md
tombstones: /root/.hermes/.archive_skills_wave2/repo-cleanup/TOMBSTONE-FORGE-*.json
triggers:
  - "scan /root for broken symlinks"
  - "audit secrets"
  - "check key rotation"
  - "find plaintext secrets"
  - "repo cleanup"
  - "broken symlink"
attention:
  load_class: medium
  default_load: false
  prerequisite_skills: []
  mutually_exclusive_with: []
  activation_signals:
    - "symlink"
    - "secret"
    - "cleanup"
    - "hygiene"
    - "key rotation"
  output_contract:
    - "symlink_report"
    - "secret_report"
    - "key_age_matrix"
    - "remediation_receipt"
tags: [symlink, secret, hygiene, repo, cleanup, F1, F2, F4, F7]
---

# core/forge/repo-cleanup

Unified filesystem hygiene scanner. Merged from FORGE-{symlink-audit,secret-hygiene} per the Wave 2 APEX verdict on the Hermes Skill Entropy Audit 2026-09-16.

## What this skill does

Two scan modes, one report:

1. **mode=symlink** — was FORGE-symlink-audit. Find broken symlinks under `/root`, classify by location (skills/, configs/, scripts/), report safe-delete candidates.
2. **mode=secret** — was FORGE-secret-hygiene. Scan env.local, SOPS .env, config files for plaintext secret leaks, key age, missing rotation dates, overlong-lived credentials.

## Modes

| Mode | Was | Trigger |
|---|---|---|
| `mode=symlink` | FORGE-symlink-audit | "broken symlinks", "symlink audit" |
| `mode=secret` | FORGE-secret-hygiene | "secret audit", "key age", "rotate secrets" |
| `mode=both` | (default) | "repo cleanup", "scan /root" |

## Rollback

```bash
git checkout entropy-wave2-pre-act-20260916T144144Z -- \
  skills/FORGE-symlink-audit/ skills/FORGE-secret-hygiene/
rm -rf skills/core/forge/repo-cleanup/
```

## Provenance

- **Wave:** 2
- **AGI proposal order:** item 3 (medium blast radius — scans filesystem)
- **ASI verdict:** clean
- **APEX verdict:** SEAL ✓
- **F13 seal:** implied via "execute the best path fwd"
- **Witness:** 2 TOMBSTONE.json files
- **Deprecation window:** 30 days

**DITEMPA BUKAN DIBERI ⚒️**
## Absorbed references (Wave-2 merge completion)
- `references/absorbed-FORGE-secret-hygiene.md` — content absorbed from the retired `FORGE-secret-hygiene` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
- `references/absorbed-FORGE-symlink-audit.md` — content absorbed from the retired `FORGE-symlink-audit` skill (Wave-2 merge 2026-09-16, recovered 2026-09-17)
