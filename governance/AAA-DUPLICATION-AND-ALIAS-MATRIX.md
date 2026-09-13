---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path)
date: 2026-09-14
parent_doc: WP-01-IDENTITY-CONVERGENCE-DELIVERABLES.md
related: AAA-MODEL-INIT-CANONICAL.v1.md
---

# AAA Duplication and Alias Matrix

> **Status:** DRAFT_PROPOSAL — extends WP-01 identity convergence with duplication audit.
> **Scope:** All 28 AAA directories + arifOS kernel (19 agents) + a2a-server (51 cards) + forge_agent (30 actors) + GEOX (13 cards).

---

## E1_DUPLICATE_RULE observations

### Identified duplicate instructions (DRAFT — needs independent verifier)

| Doc | Has | Should reduce to |
|---|---|---|
| agents/333-AGI/IDENTITY.md | F1-F13 restated + capability list | Canonical pointer to `/root/AAA/instructions/constitutional-floors.md` |
| agents/555-ASI/IDENTITY.md | Same restated | Same canonical pointer |
| agents/888-APEX/AUDIT_MODE.md | Same restated | Same canonical pointer |
| agents/*/WARGAAA_CARD.md | Constitutional reference | Same canonical pointer |
| agents/openclaw/HEARTBEAT.md | 555-ASI rules restated | Same canonical pointer |
| `.kimi-code/AGENTS.md` | F1-F13 + musyawarah restated | Canonical pointer |
| `.claude/settings.json` | skipAutoPermissionPrompt (already optimal) | Keep — harness config, not identity |

**Total duplicate-rule occurrences to reduce:** est. 25-35 across the mesh (UNVERIFIED).

### Anti-duplication rule (from MODEL-INIT-CANONICAL.v1)

If a rule already lives in `/root/AAA/instructions/<canonical>.md`, **DO NOT** copy it into agent init. Reference by ID.

---

## E3_ALIAS_SPLIT observations

### Confirmed aliased actors (DRAFT)

| Canonical | Aliases seen | Collapse target |
|---|---|---|
| `kimi-code` | `kimi-code-fi008`, `FI-008` | DEPRECATED_PENDING_CALLSITE_AUDIT → tombstone first → kimi-code |

### Possible aliased actors (UNVERIFIED — needs git grep)

| Suspect | Aliases to check |
|---|---|
| `333-AGI` | `openclaw`, `AGI_ASI_bot`, `333`, `Δ MIND` |
| `555-ASI` | `555`, `Φ SENSE` |
| `888-APEX` | `888`, `Ψ SOUL`, `apex-judge` |
| `antigravity` | `agy` |
| `hermes-asi` | `Hermes-ASI`, `hermes-asi-llm` |
| `hermes` | `ASI_arifos_bot`, `Hermes-Telegram`, `Hermes-Gateway` |

---

## E4_ORPHAN_IDENTITY observations

### Orphans to arifOS kernel (17 of 28 AAA dirs)

Per WP-01 cross-reference matrix:

```
555-ASI-VISION, aaa-gateway, antigravity, arif-fazil-identity.yaml,
claude-code, codex, forge-bot, grok-build, hermesarifos-bot,
kimi-code, makcikgpt, openclaw, prospect-maturation, protocols,
skill-auditor, skills, warga
```

### Classification by entropy class

| Class | Count | Disposition |
|---|---|---|
| `E4_ORPHAN_IDENTITY` | 12 | PENDING_BIND queue (WP-01 §2) |
| `E11_DEAD_SURFACE` | 4 (decisions, protocols, skills, warga) | TOMBSTONE (NOT delete) — reclassify as doc folders |
| `E11_DEAD_SURFACE` | 1 (aaa-gateway) | Reclassify as infra, not actor |
| `E10_FAKE_FINALITY` | 0 | (none observed at AAA dirs level) |
| `E12_ROLE_LEAK` | 0 | (separate audit at component level) |

---

## Recommended dispositions (canonical taxonomy)

| ID | Class | Source | Recommended disposition | Authority needed |
|---|---|---|---|---|
| DUP-01 | E1_DUPLICATE_RULE | F1-F13 restated in 25+ files | CANONICALIZE: replace with `/root/AAA/instructions/constitutional-floors.md` pointer | AAA + APEX review |
| ALIAS-01 | E3_ALIAS_SPLIT | kimi-code-fi008, FI-008 | TOMBSTONE first; F13 ack for final retire | sovereign |
| ALIAS-02 | E3_ALIAS_SPLIT | openclaw, AGI_ASI_bot (linked to 333-AGI) | CANONICALIZE: link as embodiment, not alias | AAA |
| ALIAS-03 | E3_ALIAS_SPLIT | 555, Φ SENSE | CANONICALIZE: keep as display aliases, canonical is 555-ASI | AAA |
| ORPHAN-01 | E4_ORPHAN_IDENTITY | 12 AAA dirs without kernel binding | BIND via WP-01 queue (PROPOSED, not auto-bound) | arifOS engineer |
| DEAD-01 | E11_DEAD_SURFACE | decisions, protocols, skills, warga | TOMBSTONE: reclassify as doc folders | AAA |
| DEAD-02 | E11_DEAD_SURFACE | aaa-gateway | TOMBSTONE: reclassify as infra, not actor | AAA |

**None of the above are executed.** All are PATCH_READY backlog items.

---

## Acceptance tests

- AT-DUP-01: Identified duplicate instructions resolve to canonical pointer after migration.
- AT-ALIAS-01: Each canonical actor has exactly one canonical_id; aliases marked DEPRECATED or KEEP only.
- AT-ORPHAN-01: Every AAA dir is classified BOUND/PENDING/LEGACY/RETIRED/ARCHIVED/UNKNOWN.
- AT-DEAD-01: Reclassified docs do not appear in active agent roster.

---

*Reversibility: FULL. All dispositions are proposals. No deletion, no rename, no commit.*
*F13 surface: ALIAS-01 (kimi-code tombstone) requires call-site audit + sovereign ack.*
*DITEMPA BUKAN DIBERI ⚒️*