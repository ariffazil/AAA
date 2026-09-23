# Skill Authority Re-Anchor — DRAFT

> **Status:** `DRAFT_AWAITING_F13` · forged 2026-09-23 by FI-008 (Kimi Code)
> **Authority basis:** Arif directive (chat 2026-09-23): *"Merge the registry. Not the files."* + `SOURCE_OF_TRUTH: registry_v3`
> **This file mutates nothing.** It declares precedence. It is the Phase-0 "freeze authority" artifact, additive and reversible.

---

## 1. FREEZE — the single source of truth

```yaml
SOURCE_OF_TRUTH:
  registry_v3: /root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml
  canonical_home: /root/AAA/skills   # already declared inside V3 itself
```

Registry V3 **already declares** `canonical_home: /root/AAA/skills`. The anchor is half-done on
paper; what is missing is the *demotion* of everything else that still claims authority.

## 2. LIVE reconciliation — evidence, not the pasted numbers

The directive message carried `370 physical / 226 retired / 140 aliases / 95 logical`.
That triple does **not** match the machine-derived census. The registry's own
`disk_reconciliation` block (refreshed **2026-09-22T20:37Z** by `skills-census.py --write`) says:

| Field | Value |
|---|---|
| `physical_disk_skills` | **562** |
| `canonical_skills` | **770** |
| `viewed_skills` | 725 |
| `loadable_skills` | 711 |
| `overlay_skills` | codex=0, continue=0, gemini=12, kimi=105, opencode=17, qwen=29 |
| `duplicate_identity_groups` / `_skills` | **25** / **50** |
| `diverged` / `broken_symlinks` / `shells` | 0 / 0 / 4 |
| `verdict` | **WARN** |

The alias table's own reconciliation (2026-09-18, afpass-W2):

| Field | Value |
|---|---|
| `alias_table_rows` | 164 |
| `active_alias_rows` | 133 |
| `tombstone_alias_rows` | 31 |
| `alias_rows_resolvable` | **42** |
| `alias_rows_dead` | **91** |

`total_skills: 95` / `logical_registry_count: 95` **do** match the "95 logical" figure.

**Correction:** the pasted `370 / 226 / 140` are stale or from a different layer. The live
numbers are **562 physical · 770 canonical · 164 alias rows (91 dead)**. The correct problem is
therefore **not** "too many skills", it is "the translation layer is 68% dead and five
authority-claiming documents disagree".

## 3. AUTHORITY DEMOTION — every competing document, classified

| Document | Path | Classification |
|---|---|---|
| Registry V3 | `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` | **AUTHORITY** (canonical) |
| Registry V2 | `/root/.kimi-code/skills/FEDERATED_SKILLS_REGISTRY.yaml` | **HISTORICAL / SUPERSEDED** (real file, 32 KB, not symlinked) |
| Alias table v1.1.0 | `/root/AAA/skills/SKILL_ALIAS_TABLE.json` | **TRANSLATION LAYER** (not authority; 68% dead) |
| Capability registry | `/root/AAA/capability_registry.json` · `/root/.config/capability_registry.json` | **VIEW / DERIVATION** (competing authority) |
| Skills index | `/root/AAA/skills_index.json` (552 KB) · `skills_index.federation.json` (118 KB) | **VIEW (generated census)** |
| Served skills | `/root/AAA/served-skills.json` (95 KB) | **VIEW (served snapshot)** |
| Skill inventory | `/root/AAA/skill_inventory.json` (116 KB) | **VIEW** |
| Skill audit | `/root/AAA/skill-audit-*.json` | **HISTORICAL (audit artifact)** |
| Atlas | `/root/.kimi-code/skills/skill-mesh/AUDIT-skill-atlas` · `/root/web-canon/atlas/WEB_ATLAS.md` | **STALE NARRATIVE** |
| Doctrine core | `/root/.agents/skills` | **VIEW** (not a second authority) |

## 4. VIEW CLASSIFICATION (Arif Phase 2 — classify, do not merge)

```yaml
AAA:        mode: FULL        # /root/AAA/skills — the corpus the registry indexes
Codex:      mode: CURATED     # /root/.codex/skills-curated (22) — parallel curated view
Kimi:       mode: CURATED     # /root/.kimi-code/skills (94) — this harness's view
OpenCode:   mode: FULL_VIEW   # /root/.arifos/agents/opencode/skills (258)
Org-native: mode: CURATED     # /root/{GEOX,WELL,WEALTH,arifOS,HERMES}/skills — where doctrine moved TO
Forge/Grok: mode: VIEW        # /root/.forge/skills (20) · /root/.grok/skills (366, symlink mesh)
```

## 5. KNOWN DEFECT (the real entropy)

91 of 133 non-tombstone alias rows carry `status: RESOLVED|FORGED` while `primary_path` does
**not exist**. Root cause (per V3's own `alias_reconciliation.finding`): the organ doctrine suites
moved to organ-native homes and the table was never re-resolved. Each row needs an individual
verdict (retarget vs tombstone). **This reconciliation sizes the hole; it does not close it.**

## 6. WITNESS + OBSERVE (not yet wired)

- **ArifFlow** (`/root/arifFlow`, Rust service, `flow.db`) — should emit receipts for
  `Skill Added / Retired / Alias Changed / Capability Added / Removed / Registry Drift`.
  **Currently no skill-mutation wiring found in Registry V3.**
- **Kabarkan** — drift observatory. The census already emits `verdict: WARN`; nothing surfaces
  it as a dashboard yet. Kabarkan = *witness* drift, not *control* drift.

## 7. MERGE STRATEGY (one sentence)

> Do not merge AAA skills into one directory. Merge them into one Registry. Expose many Views.
> Witness all mutations through ArifFlow. Observe all drift through Kabarkan.

---

*Evidence: `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` (lines 6-21 disk_reconciliation,
336-359 alias_reconciliation) · `/root/AAA/skills/SKILL_ALIAS_TABLE.json` (v1.1.0).*
