# Alias Re-resolve — Phase 2d Handoff

**Generated:** 2026-09-23 (session SEAL-23431e96df4f4853)  
**Author:** 333-AGI (apex-zen reality auditor + namefield mapping agent)  
**CLEAR:** Class A + Class B from prior session (T1+T2 lane); canonical-record mutation still HELD for F13 binary

---

## 1. Headline findings (corroborating prior report)

### 1.1 Symlinks collapse to canonical tree
```
/root/.agents/skills  →  /root/AAA/skills      (symlink)
/root/.grok/skills    →  /root/AAA/skills      (symlink)
/root/.claude/skills  →  /root/AAA/skills      (symlink)
/root/.opencode/skills → /root/.agents/skills   (transitive)
```
Doctrine-core and grok view are NOT separate authorities — they are alias views onto `AAA/skills`.

### 1.2 Real separate skill trees (not symlinks)
| Root | SKILL.md count |
|---|---|
| `/root/AAA/skills/` | 562 active (canonical) |
| `/root/.config/opencode/skills/` | ~30 (geox/wealth/well lanes + FORGE/mimo/mmx) |
| `/root/HERMES/skills/` | 17 |
| `/root/GEOX/skills/` | 5 (organ-native) |
| `/root/WEALTH/skills/` | 4 |
| `/root/WELL/skills/` | 4 |

The previous worklist missed the FIFTH root (`/root/.config/opencode/skills/`) — fixed in Phase 2b.

### 1.3 Renames not deletions
The 56 "dead adapters" are renamed doctrines on disk, not deletions. Geo prefix migrated to `geox-*`, wealth to `wealth-capital-*`, well-substrate-readiness covers `well-boundary`/`well-readiness`. Bulk-tombstone would have destroyed living doctrine.

---

## 2. Final namefield mapping proposal — Phase 2d

**116 worklist rows resolved → 31 RETARGET + 42 FLAG_REVIEW + 43 TOMBSTONE**

### 2.1 Verified RETARGET (31 rows, all SKILL.md present on disk)

**Organ-native mapping (curated rules, HIGH confidence) — 12 rows:**
- `geo-basin` → `geox-basin-evaluation`
- `geo-constitution` → `geox-claim-falsification`
- `geo-petrophysics` → `geox-basin-evaluation` (folded)
- `geo-prospect` → `geox-prospect-evaluation`
- `geo-well-tie` → `geox-well-log-qc`
- `geo-writing` → `aaa-pdf-voice-protocol` (geo writing → AAA PDF voice)
- `geo-artifact-rigor` → `aaa-pdf-voice-protocol` (folded)
- `wealth-reason` → `wealth-capital-primitives`
- `wealth-thermo` → `wealth-runway-conservation`
- `wealth-collapse` → `wealth-ledger-discipline`
- `well-boundary` → `well-substrate-readiness`
- `well-readiness` → `well-substrate-readiness` (also alias dedup)

**Semantic mapping (MEDIUM-HIGH confidence, ≥0.7 score) — 19 rows:** case-only renames, lifecycle aliases, exact-name matches.

### 2.2 FLAG_REVIEW (42 rows)
Human judgment needed — semantically possible but ambiguous. Full list in `ALIAS-RERESOLVE-MAPPING-FINAL-20260923.md`.

### 2.3 TOMBSTONE (43 rows)
No plausible disk truth. Examples: `domain-causal`, `ops-compress`, `ops-google`, `mcp-shopping-list-2026-09`.

### 2.4 Files produced (all additive, no canonical mutation)
| File | Purpose |
|---|---|
| `ALIAS-RERESOLVE-WORKLIST-DRAFT-20260923.json` | Phase 1b (prior) — 116 rows raw |
| `ALIAS-RERESOLVE-MAPPING-FINAL-20260923.json` | Phase 2d — RETARGET/FLAG/TOMBSTONE |
| `ALIAS-RERESOLVE-MAPPING-FINAL-20260923.md` | human-readable summary |
| `ALIAS-MIGRATION-PREVIEW-20260923.json` | what SKILL_ALIAS_TABLE would become IF F13 ratifies |
| `alias_namefield_mapping_v2.py` v3 v4 | the generators (reproducible) |

---

## 3. Authority & scope

- **Phase 1b/2a–2d executed:** read-only analysis, generators, disk indexing, semantic matching. All within Class A.
- **Canonical mutation HELD:** `SKILL_ALIAS_TABLE.json` was previously sealed (`status: SEALED_TABLE_AUDITED_RENAMED`). Re-anchoring its aliases is a canonical-record mutation (T3 territory). The **migration preview is ready** but **not applied**.
- **Two phantoms noted (FLAG_REVIEW in prior worklist):** `apx_init_substrate`, `hermes-text-to-speech`, `kernel-superposition`, `mcp-shopping-list-2026-09` — declared but no disk truth.

---

## 4. Sovereign binary required to proceed beyond proposal

Two paths forward (mutually exclusive):

**A. RATIFY Phase 2d RETARGET application**  
Apply 31 rows to `SKILL_ALIAS_TABLE.json` (preview ready). Triggers: re-seed of `tombstone=false`, `restored_live=true`, `status=RETARGETED`. FLAG_REVIEW rows handled by chosen default heuristic.

**B. PARALLEL musyawarah for FLAG_REVIEW**  
Run FORGE-musyawarah-gotong (333 ARCHITECT + 555 AUDITOR) to resolve 42 ambiguous rows before any write. Adds ~30-60 minutes of deliberation, no mutation until deliberation completes.

Currently **HOLDING on both paths**. Do not enact either without explicit F13 binary.

---

## 5. Receipt
`0b052aab-c8ba-4918-8f58-e02ac5338c24` (final settlement, prior session) + artifact-mint receipts in `arifflow` ledger for each generator run.
