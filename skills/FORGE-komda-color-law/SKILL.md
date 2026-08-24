---
name: FORGE-komda-color-law
description: Komda Color Law lint — enforces SOVEREIGN_DECREES §04 (territory color families). Use when generating, editing, or auditing any visual artifact (HTML/SVG/CSS) that claims a federation territory (arifos / geox / wealth / well / aaa). Foreign-family color in territory DOM = violation per F13 SOVEREIGN doctrine (2026-08-01).
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# FORGE-komda-color-law

The Komda Color Law is **SOVEREIGN DECREES §04** — F13-ratified doctrine (2026-08-01). It enforces that every visual artifact claiming a federation territory uses only that territory's closed color family plus the universal PRIMER-1 dark field.

## Doctrine (verbatim from §04.1)

> *Foreign-family color appearing in a territory DOM is a violation.*

Each territory has a closed color palette. Cross-family escape is permitted only via **EUREKA bridges** with explicit semantic justification. Any other color = violation.

## Territory Tokens (canonical at §04.2)

| Territory | Primary | Accent | Field | Notes |
|-----------|---------|--------|-------|-------|
| arifos  | `#A82733` | `#6F2DBD` | `#0A0A0F` | crimson + royal-purple — constitutional kernel |
| geox    | `#2D5F8B` | `#8B4513` | `#0A0A0F` | deep blue + sedimentary brown — Earth intelligence |
| wealth  | `#FFCC00` | `#1E3A8A` | `#0A0A0F` | gold + deep blue — capital intelligence (XAU macro) |
| well    | `#5FB84A` | `#E07A5F` | `#0A0A0F` | vital green + life coral — human readiness |
| aaa     | `#9A9AA8` | `#FFD54F` | `#0A0A0F` | silver + certified gold — cockpit |
| universal | —       | —       | `#0A0A0F` | PRIMER-1 dark field — base layer for all |

**EUREKA bridges** (decorative cross-family escapes only):
- `arifos ↔ geox` : `#FFD54F` — eureka-overlay
- `wealth ↔ aaa`  : `#FFD54F` — certified-mark

## Use

### Lint a directory

```bash
/root/arif-fazil.com/scripts/lint-komda-colors.sh <scan-path>            # warn-only
/root/arif-fazil.com/scripts/lint-komda-colors.sh <scan-path> --gate     # exit 1
FORCE_KOMDA_GATE=1 /root/arif-fazil.com/scripts/lint-komda-colors.sh .   # env gate
```

### Detect territory

The lint reads filename patterns:
- `wealth-komda.html` → territory `wealth`
- `aaa-overview.html` → territory `aaa`
- `arifos-session.html` → territory `arifos`
- `index.html`, `999-chain.html` → no territory claim → skip

Files without an explicit territory claim are skipped (no false positives on shared base files).

### Promotion (warn → gate)

Currently `--warn-only` at deploy time. To promote to gate:

1. Set `FORCE_KOMDA_GATE=1` in deploy env, OR
2. Edit `deploy-vps.sh` Step 3.6 to call with `--gate` instead of `--warn-only`.

**Sovereign word required for promotion.**

## Canonical Pointers

| What | Path |
|------|------|
| Doctrine (canonical) | `/root/docs/design-rules/SOVEREIGN_DECREES.md` §04 |
| Declarative registry | `/root/arif-fazil.com/data/family-colors.yaml` |
| Lint script | `/root/arif-fazil.com/scripts/lint-komda-colors.sh` |
| Deploy hook | `deploy-vps.sh` Step 3.6 (post-`_shared` sync) |
| Reference implementation | `/_shared/design-system/geometry/wealth-komda.html` |
| This skill | `/root/.arifos/agents/kimi/skills/FORGE-komda-color-law/SKILL.md` |

## Constitutional Binding

| Floor | Binding |
|-------|---------|
| **F1 AMANAH** | Files reversible. Doctrine is append-only. |
| **F2 TRUTH** | Each lint finding labelled OBS. |
| **F9 ANTIHANTU** | No false-positive minimization. Reports each violation distinctly. |
| **F13 SOVEREIGN** | Doctrinal promotion (warn→gate) requires sovereign word. New bridges require §04.x appendix. |

## When to invoke

- After generating any new visual artifact (HTML/SVG) that names a territory
- Before deploy (automatic via `deploy-vps.sh` Step 3.6)
- During visual audits or 777-forge loops
- When rehearsing new organ brand palettes

## Reversibility

| Aspect | Reversibility |
|--------|---------------|
| Files (yaml, sh, SKILL.md) | F1 — delete + recreate |
| SOVEREIGN_DECREES §04 history | F13 — append-only |
| Promote warn → gate | F13 — sovereign word required |
| Add new bridge | F13 — append §04.x |

## Misuse modes

- ❌ **Don't** modify `family-colors.yaml` without also updating lint script's `ALLOWED` map (drift = silent violations).
- ❌ **Don't** promote to `--gate` without sovereign word (reverses Phase 1 doctrine).
- ❌ **Don't** add bridges without §04.x appendix (reverses F9 ANTIHANTU bridge ratification).

*DITEMPA BUKAN DIBERI* — the law is forged, not given.
