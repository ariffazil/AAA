# Sabah Basin Resource Base — Reconciliation Patch (apply-ready, HOLD)

**Compiled:** 2026-09-15 · **Auditor:** Hermes (edge bridge, KVM4) · **Authority:** F13 ARIF
**Trigger:** GEOX Kinabalu Basin Geologist Dossier, "Provenance reconciliation" annex (pp. 26–28)
**Scope:** read-only audit → apply-ready patch. **NOT APPLIED.** No file in the GEOX resource base modified.

## Why this is HOLD, not housekeeping

`sabah_two_oceanics.yaml` carries `_meta.source: SABAH_EUREKA_LEDGER::v1.0::SEALED::2026-07-10`.
Re-sealing a sealed artifact is an F13 authority boundary. The auditor's own annex is correctly
framed as "a finding and a proposal, not a correction." I keep it that way.

`basin_profile.yaml` (legacy) is not sealed, but it may still be referenced by an untraced code path.
Marking it DEPRECATED is a mutation → same HOLD.

**Verified independently:** /root/GEOX and the deployed /opt/geox (live geox-mcp.service) hold
*identical* copies of all four Sabah/Malay basin resource files. This is not a stale-repo issue.
Every defect below is being served live.

---

## Defect register

| # | File | Defect | Class | Severity |
|---|---|---|---|---|
| D1 | sabah_two_oceanics.yaml | `duration_ma: 15.0` + comment "~21 Ma collision peak to present" | Arithmetic | High |
| D2 | sabah_two_oceanics.yaml | "canonical collision age" label on 21.0 Ma only | Ontology | High |
| D3 | sabah_two_oceanics.yaml | Collision onset ~23 Ma (BMU/TCU) absent from chronology | Omission | High |
| D4 | sabah_two_oceanics.yaml | DRU (~13 Ma) absent from chronology | Omission | High |
| D5 | sabah_two_oceanics.yaml | MMU 14.2 vs briefing ~15.5 Ma | Contested age | Medium |
| D6 | sabah_two_oceanics.yaml | Granite 7.0 Ma vs dossier 9.5–7.0 vs code 10–13.7 | Contested age | Medium |
| D7 | sabah_basin/basin_profile.yaml | "Panas Thicknessnam Formation" | Corrupted string | High |
| D8 | sabah_basin/basin_profile.yaml | "Kellaneous Formation" — not in NSPW synthesis | Orphan name | Medium |
| D9 | sabah_basin/basin_profile.yaml | Collision 16–12 Ma contradicts sealed ledger (~23/21 Ma) | Model conflict | Critical |

---

## PATCH 1 — sabah_two_oceanics.yaml `collision_metrics` (D1, D2)

**Replace:**
```yaml
collision_metrics:
  duration_ma: 15.0                     # ~21 Ma collision peak to present
```
**With:**
```yaml
collision_metrics:
  onset_age_ma: 23.0                    # BMU/TCU — Dangerous Grounds enters trench
  peak_age_ma: 21.0                     # Proto-SCS subduction terminates
  # duration_ma retired: the previous 15.0 contradicted its own "21 Ma to present" comment.
  # Replaced by explicit onset/peak so no reader has to infer which age is meant.
```
Rationale: the field carried a 6 Myr internal contradiction. Explicit onset/peak removes the
inference step entirely — which is what the doctrine asks for.

---

## PATCH 2 — sabah_two_oceanics.yaml `chronology` (D3, D4, D2)

**Insert onset entry immediately before the 21.0 Ma entry:**
```yaml
  - age_ma: 23.0
    event: Collision Onset (BMU/TCU)
    description: Dangerous Grounds continental crust underthrusts NW Borneo — accretion stops, NSPW born
```
**Replace the 21.0 Ma entry's description** (retire the ambiguous phrase):
```yaml
  - age_ma: 21.0
    event: Collision Peak
    description: Proto-SCS subduction terminates. NOT the onset age — see 23.0 Ma.
```
**Insert DRU between MMU (14.2) and Post-Subduction Relaxation (9.5):**
```yaml
  - age_ma: 13.0
    event: Deep Regional Unconformity (DRU)
    description: Wedge-top unconformity — NSPW active phase ends on Proto-SCS slab breakoff. NOT collision onset.
```
Rationale: the ledger's headline finding (DRU reclassification) was absent from the ledger's own
chronology, while the slab-detachment literature sat in the same file's reference list. A reader
extracting the chronology alone would get the 10 Myr error the dossier warns about.

---

## PATCH 3 — basin_profile.yaml deprecation (D7, D8, D9)

**Add as new first lines:**
```yaml
# ⚠ DEPRECATED 2026-09-15 — SUPERSEDED by ../sabah_two_oceanics.yaml
#   This file describes a passive-margin + inversion model with collision at 16–12 Ma.
#   That directly contradicts the sealed ledger (onset ~23 Ma, peak ~21 Ma).
#   Retained for provenance only. Do not reuse.
#   Corrupted/unverified formation names flagged below: "Panas Thicknessnam", "Kellaneous".
#   Resolution pending F13 ratification — see forge_work/2026-09-15-geox-sabah-mtjda-audit/
```
**Do NOT delete.** Two mutually exclusive tectonic models in one directory is the defect; silent
deletion destroys the audit trail that proves the defect existed.

**Formation names:** I will not guess the intended spelling of "Panas Thicknessnam".
Corruption is confirmed; the correction requires a source I do not have. Flagged, not fixed. (F1/F2)

---

## PATCH 4 — contested ages, register not resolve (D5, D6)

MMU (14.2 vs ~15.5) and granite emplacement (7.0 / 9.5 / 10–13.7 across ledger, dossier, code)
are **contested**, not erroneous. Patching to a single number would manufacture false precision.
Recommendation: add an `age_disputes:` block recording both values + sources, and leave the
decision to reconciliation against original biostratigraphy (which the dossier itself says is
twenty years old and unaudited).

---

## What I did NOT do

- Did not edit `sabah_two_oceanics.yaml` — sealed ledger representation, F13 boundary.
- Did not edit `basin_profile.yaml` — untraced code path; deprecation is a mutation.
- Did not invent a corrected formation name — no source exists to support one.
- Did not patch contested ages to false precision.
- Did not deploy. Patch is a proposal against a ratified baseline.

**Apply path (on F13 greenlight):** edits are local + reversible, git-tracked in /root/GEOX;
deployment to /opt/geox is a separate mutation with its own greenlight.
