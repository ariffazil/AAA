# register_report.md — arifOS Normalized Human-Reality Register (v2)

> **Status:** PROPOSED · NOT CANON · awaiting F13 ratification  
> **Generated:** 2026-10-09T23:59:48+08:00 (Asia/Kuala_Lumpur)  
> **Companion artifact:** `human_reality_register.json` (this directory)  
> **Author:** HERMES (subagent) · proposal `human-reality-v2`  
> **Owner:** F13 — Muhammad Arif bin Fazil

## 1 · Summary

| Metric | Value |
|---|---|
| **Total persons in register** | **26** |
| Human persons | 25 |
| Non-human entries retained | 1 (Wawa P-007 — flagged `human:false`) |
| Non-human archetypes excluded | 4 (P-008..P-011, typology not individuals) |
| Identities (name/id/role/…) | 75 |
| Layer items (state/strategy/attractor/invariant) | 71 |
| Valence transitions (human-stated) | 1 |
| **Total facts-entries (identities+layers+valence)** | **147** |
| Provenance rows | 70 |
| Persons with `scope: dm` | 9 |
| Persons with `scope: shared` | 17 |

**Sources normalized:** `people_registry.json` (v1.2.0) · `INDEX.md` · `build-report.json` · every `/root/memory/people/<NAME>/` directory · `/root/.hermes/lanes/people.yaml`. Source file inventory with sha256-16 is embedded in the JSON under `sources`.

## 2 · Per-person file counts (directory evidence)

| Directory | Canonical person | Files |
|---|---|---|
| `ABBAH/` | P-002 Fazil bin Khamis | 2 |
| `ALIFF/` | P-005 Aliff | 4 |
| `ARIF/` | P-001 Arif | 4 |
| `AZWA/` | P-015 Azwa | 1 |
| `FAMILY/` | P-013/P-014/P-015/P-016/P-017 (shared subdir) | 10 |
| `FAQWAN/` | FAQWAN | 1 |
| `FARIDAH/` | P-003 Faridah | 3 |
| `FAZIL/` | P-002 Fazil bin Khamis | 1 |
| `HAFIZ/` | HAFIZ | 1 |
| `IZZU/` | P-006 Izzu | 4 |
| `JIA/` | P-014 Naazira/Jia | 1 |
| `JUKHRIS/` | P-025 Jukris | 4 |
| `LUTFI/` | LUTFI | 1 |
| `MAK/` | P-003 Faridah | 2 |
| `NABILAH/` | P-013 Nabilah | 3 |
| `PAAN/` | PAAN | 1 |
| `SCAR-WITNESSES/` | P-012 Bakar | 3 |
| `SYAKIR/` | SYAKIR | 1 |
| `SYED/` | P-004 Syed | 16 |
| `WAWA/` | P-007 Wawa (non-human) | 3 |
| `scripts/` | support scripts (not a person) | 2 |

*Note: `ABBAH/` and `FAZIL/` are two directories for one person (P-002); `FARIDAH/` and `MAK/` for P-003; `FAMILY/` holds five persons (P-013..P-017). `scripts/` is build tooling, not a person.*

## 3 · H-layer coverage — who is missing which H-layers

The `/root/memory/people/<NAME>/H1..H6` tree exists for **exactly one person: SYED (P-004)**.
No other person directory contains an H-layer tree — all six H-layers are **absent** for the other 25 human persons.

| Person | H1-capture | H2-experience | H3-knowledge | H4-identity | H5-scars | H6-constitution |
|---|---|---|---|---|---|---|
| P-004 Syed | EMPTY | EMPTY | EMPTY | present | present | present |
| All other 25 human persons | absent | absent | absent | absent | absent | absent |

- **Absent** = no directory at all (0 files). **EMPTY** = directory exists but holds only a `.placeholder`.
- SYED H1/H2/H3 hold only `.placeholder` (empty, by design — awaiting observation captures).
- SYED H5 = witnessed-class only (`witnessed-scars-zkpc.json`, 6 scars, status WITNESSED_NOT_SEALED, 0 subject-sealed) — content stays UNKNOWN-class.
- The 4-layer model (`state/strategy/attractor/invariant`) is carried per person in the JSON as its own key where facts exist, independent of the directory tree.

## 4 · Top-5 structural gaps

1. **H-axis tree ~0% coverage.** Only 1 of 26 persons (SYED) has any H1..H6 layer, and even there H1/H2/H3 are empty placeholders. For the other 25 human persons the entire H-axis (capture/experience/knowledge/identity/scars/constitution) does not exist on disk. The 4-layer model is therefore only carryable as register-embedded facts, not as a browsable per-person tree.

2. **Register version drift + ID collision + stale census.** `people_registry.json`'s array carries **P-001..P-025**, but its own `description`, `INDEX.md` ("17 humans catalogued"), `build-report.json` (17) and the proposal context still describe **P-001..P-017**. `P-018` is assigned twice — to Laletha Jeevachandran (registry) AND proposed for Jukris (JUKHRIS card/aliases.json). `WAWA` (P-007) is still listed as a `telegram_network` person although canon (`FEDERATED-HUMAN-REALITY-MAP-2026-09-24.md:107`) declares it NOT a human.

3. **Canon vs runtime vs cards not reconciled; admission incomplete.** Of 26 persons, only **9** appear in `people.yaml` and only **9** have a generated `register-card.md`; the registry (25 rows) and the directory tree overlap incompletely. `people.yaml` itself declares `held_out` material and `unresolved` name merges. Several dossier cards still mix fact with interpretation (shadow-profile traits, ESFP reads, `[DER]` lines) with no machine flag separating them.

4. **Date-versioned contradictions unresolved across sources (no single canonical source arbitrates).** Concrete open conflicts found: (a) Fattah's parent — Naazira (`FAMILY/fattah.md`, 2026-08-12) vs Nabilah (registry, corrected 2026-08-20); (b) Fahim's relation — 'likely partner, unconfirmed' (`FAMILY/fahim.md`) vs 'ex-husband' (registry); (c) Azwa's DOB — 2006-02-21 (registry/people fix) vs 2006-02-22 (`FAMILY/azwa-fazil.md` timeline); (d) Nabilah's spouse — 'Muhd. Redhani' (`FAMILY/nabilah-fazil.md`) vs Fahim (`NABILAH/person-card.md`); (e) Syed's endoscopy — 'history' (H4 card) vs 'not yet done' (in-lane 2026-09-29).

5. **Valence/trust data effectively absent.** Every `domain_trust` object is empty (`{}`) for all 26 persons — no adaptation/scar/trust ledger was present in the read set. Across the whole federation only **1** human-stated valence transition was recoverable (Nabilah: sedih -> lega/tenang, 2026-07-24). The proposal's valence-as-transition-machine and domain-trust vectors therefore have no live feed in these sources.

## 5 · Method & exclusions (honesty notes)

- **Observed dates:** taken from the record where it states one; otherwise the source file's mtime date. Approximate dates are flagged in each person's `gaps`.
- **Excluded as interpretation (not promoted to layers):** shadow-profile traits (P-012, P-004), ESFP/archetype reads (P-013), `[DER]` derivations (P-003), and all psychology/motive content — per the facts-only rule and the HARD-FORBIDDEN list in `people.yaml`/`README-register-cards.md`.
- **H5 scars:** kept UNKNOWN-class. SYED's witnessed scars are recorded as CLASS + provenance only, with zero subject-sealed content.
- **Held out (declared, not hidden):** see `held_out` in the JSON (MEMORY.md/USER.md backups; `/root/HERMES/lanes/private/shadow/*`).
- **Write scope honored:** only these two files were written.

---
*DITEMPA BUKAN DIBERI. Map ours, territory theirs.*
