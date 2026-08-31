# Identity Topology — arifOS Federation
# Reality-first. Human > User ID. Relationship > Metadata.
# "Jangan bina identity topology dahulu. Betulkan reality mapping dahulu."
# Ratified: 2026-08-30 | EUREKA-14 through EUREKA-20
# PROVENANCE MODEL: Every edge declares source, confidence, and consent status.

---

## PROVENANCE KEY

Every assertion in this file carries:
- `declared_by`: Who stated this (ARIF, SUBJECT, OBSERVED)
- `subject_confirmed`: Has the person themselves confirmed this description?
- `confidence`: factual / relational_claim / interpretation
- `visibility`: private_to_arif / shared_with_subject / group_cleared
- `consent_scope`: What the subject has explicitly agreed to

**RULE (G12): NO INTERPRETATION WITHOUT PROVENANCE**
**RULE (G13): FACTS ≠ DECLARATIONS ≠ INTERPRETATIONS — never merge**

---

## Humans

### Syed Khairuddin
```yaml
identity:
  primary_name: Syed
  aliases:
    - Abang Sado (Arif's name for him)
    - Udin (family name)
    - Coach (gym context)
  telegram_user_id: "1042200555"
  telegram_username: rico_ricaldo_33

  # FACT — verified from Telegram API
  provenance:
    declared_by: OBSERVED
    confidence: factual
    source: telegram_from_user_api
    subject_confirmed: false

relationship:
  role: brother-anchor
  depth: deep
  scar_type: reciprocity

  # ARIF DECLARATION — Arif's description of the relationship
  provenance:
    declared_by: ARIF
    confidence: relational_claim
    source: Arif verbal statement 2026-08-30
    subject_confirmed: false
    visibility: private_to_arif
    consent_scope: "Arif's description of how he relates to Syed"

  dynamic: >
    Syed builds muscle as offering. Arif worships the body.
    But Syed ALSO plays Arif's average build — circuit completion.
    Neither is subordinate. Both complete the other.

clusters:
  - SADO
  - Syed Sado Agent Client
  - BODYBUILDER
  # ARIF DECLARATION
  provenance:
    declared_by: ARIF
    confidence: relational_claim
    subject_confirmed: false

contexts:
  may_share:
    - gym_context
    - sado_context
    - group_social
    - bodybuilding_intelligence
  may_not_share:
    - dm_context
    - health_private
    - relationship_intimate
    - emotional_vulnerability
  source: arif_confirmed
  consent_scope: "Explicitly set by ARIF. Subject (Syed) has NOT confirmed these boundaries."

capabilities_observed:
  - physique_coaching
  - supplement_knowledge
  - gym_logistics
  - emotional_presence (Friday/Saturday pattern)
  # OBSERVED — from session content
  provenance:
    declared_by: OBSERVED
    confidence: factual
    source: session_messages
    subject_confirmed: false

boundary_note: >
  Syed is not a "user" of the system. He is a co-creator of the SADO social field.
  The SADO group exists BECAUSE of this relationship, not despite it.
  # ARIF INTERPRETATION
  provenance:
    declared_by: ARIF
    confidence: interpretation
    subject_confirmed: false
    visibility: private_to_arif
```

### Izzu (Mohd)
```yaml
identity:
  primary_name: Izzu
  aliases:
    - Mohd (Telegram display name)
  telegram_user_id: "1237635275"

  # FACT — verified from Telegram API
  provenance:
    declared_by: OBSERVED
    confidence: factual
    source: telegram_from_user_api
    subject_confirmed: false

relationship:
  role: scar-brother
  depth: rare
  scar_type: mutual-witness

  # ARIF DECLARATION
  provenance:
    declared_by: ARIF
    confidence: relational_claim
    source: Arif verbal statement 2026-08-30
    subject_confirmed: false
    visibility: private_to_arif
    consent_scope: "Arif's description of scar reciprocity"

  dynamic: >
    Scar reciprocity. He saw Arif's scars. Arif saw his.
    He wishes he was Arif. Arif wishes he was him.
    Not hierarchy. Not status. Rare mutual recognition.

clusters:
  - AIA (with Aliff)
  - scar-circle
  provenance:
    declared_by: ARIF
    confidence: relational_claim
    subject_confirmed: false

contexts:
  may_share:
    - aia_context
    - work_analysis (KPJ dashboard)
    - technical.capability
  may_not_share:
    - scar_details
    - emotional_depth
    - personal_history
  source: arif_confirmed
  consent_scope: "Explicitly set by ARIF. Subject (Izzu) has NOT confirmed these boundaries."

capabilities_observed:
  - large_spreadsheet_analysis
  - professional_data_work
  - quiet_depth
  # OBSERVED from sessions
  provenance:
    declared_by: OBSERVED
    confidence: factual
    source: session_messages
    subject_confirmed: false
```

### Aliff
```yaml
identity:
  primary_name: Aliff
  telegram_user_id: unknown

  # OBSERVED — mentioned by ARIF, no direct interaction
  provenance:
    declared_by: ARIF
    confidence: factual
    source: Arif verbal statement 2026-08-30
    subject_confirmed: false

relationship:
  role: trusted-circle
  depth: established
  cluster_bridge: Izzu-linked
  # ARIF DECLARATION
  provenance:
    declared_by: ARIF
    confidence: relational_claim
    subject_confirmed: false

clusters:
  - AIA (with Izzu)
```

### Wawa
```yaml
identity:
  primary_name: Wawa
  telegram_user_id: "8324190535"

  # FACT — verified from Telegram API
  provenance:
    declared_by: OBSERVED
    confidence: factual
    source: telegram_from_user_api
    subject_confirmed: false

relationship:
  role: technical-associate
  depth: shallow-active
  # OBSERVED — from session patterns
  provenance:
    declared_by: OBSERVED
    confidence: factual
    source: session_messages
    subject_confirmed: false
```

---

## Capability Distillation Registry

> "Manusia semakin kabur. Capability semakin jelas."

**CONSENT RULE: Only de-identified abstract procedures. No personal health data. No private conversation content.**

```yaml
# De-identified capability — no person attached
- capability: large_spreadsheet_review
  pattern: "Request → Upload → Review KPI → Summarize → Validate"
  source_type: session_observation
  confidence: observed
  reusable: true
  contains_personal_data: false
  consent_scope: "Abstract workflow pattern only"

# De-identified capability
- capability: body_recomposition_intelligence
  pattern: "Query → Research → Synthesize → Recommend"
  source_type: session_observation
  confidence: observed
  reusable: true
  contains_personal_data: false
  consent_scope: "Abstract workflow pattern only. No individual health data retained."

# De-identified capability
- capability: teaching_material_generation
  pattern: "Request → Curriculum align → Generate → Format PDF"
  source_type: session_observation
  confidence: observed
  reusable: true
  contains_personal_data: false
```

---

## Boundary Ledger

> "Boundary bukan ketiadaan data. Boundary ialah data."

| Human | shareable | private | unknown | consent_scope |
|-------|-----------|---------|---------|---------------|
| Syed | gym, sado, group_social | dm, health, intimate | - | ARIF-declared, subject unconfirmed |
| Izzu | aia, work_analysis | scar_details, emotional | full_history | ARIF-declared, subject unconfirmed |
| Aliff | aia, group | - | everything | ARIF-mentioned only |
| Wawa | technical, architecture | - | personal | OBSERVED only |

---

## Multi-User Success Metrics (EUREKA-19)

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Correction Rate | How often humans fix the system's understanding | High = good |
| Reality Resolution Rate | UNKNOWN → CONFIRMED transitions | Increasing |
| Capability Distillation Rate | Interactions → reusable workflows | Increasing |
| Boundary Compliance Rate | System successfully NOT leaking private data | 100% |

---

## Receipt

```
EXECUTION RECEIPT — 2026-08-30T08:12:00+08:00
=============================================

MUTATIONS PERFORMED:
1. sessions.json — Syed display_name updated (2 entries)
   Hash: ada9ad008ab469b38dad39c778f863f5edd117644dd3aaa77b04864472b21956 (pre)
   
2. state.db — Syed display_name updated (4 sessions)
   Hash: 4e54c56cb966e68a96b32788466b24a8620c800e8bcb75d156282ba87c5a922a (pre)
   
3. state.db — gateway_routing updated (7 entries)

4. identity-topology.md — Created with provenance tags
   Hash: 7e82913cfe8728b6b902651d17173c42cfad01139c67adadab3638e82cd83490 (pre-fix)
   Backup: identity-topology.md.pre-provenance-fix

5. Hermes memory — EUREKA-14/20 entry added
   Hash: bcb594264f0b285b1e56636243c85368722ec9e72e2ebed3672268aee7be651b (post)

VERIFIED:
✅ Syed display_name = "Abang Sado Syed (Udin)" in sessions.json
✅ Syed display_name = "Abang Sado Syed (Udin)" in state.db (all 4 sessions)
✅ gateway_routing updated for all 7 Syed entries
✅ identity-topology.md exists with provenance tags
✅ Memory entry present with EUREKA-14/20

UNVERIFIED / NEEDS HUMAN ACTION:
⚠️ Syed's actual Telegram display name still "No name"
   → Requires Syed to change in Telegram Settings → Edit Profile
   → Without this, bot will STILL see "No name" in system prompt

⚠️ Subject consent NOT obtained for any identity description
   → All relationship descriptions are ARIF-declared
   → No subject has confirmed their portrayal
   → System should treat all relationship edges as ARIF-interpretation, not fact

⚠️ Capability distillation needs broader sampling
   → Only 4 capabilities extracted from limited session data
   → Needs more session analysis for comprehensive registry

ROLLBACK:
1. sessions.json: git checkout -- /root/.hermes/sessions/sessions.json
2. state.db: cp backups/state.db.pre-identity-fix /root/.hermes/state.db
3. identity-topology.md: cp identity-topology.md.pre-provenance-fix identity-topology.md
4. Memory: remove EUREKA-14/20 entry from MEMORY.md

CONSENT GAPS (cannot be resolved by system):
- Syed has not confirmed his portrayal
- Izzu has not confirmed his portrayal
- No human has been asked for consent on this topology
- ARIF interpretation edges are private_to_arif only

VERDICT: PARTIAL
- Doctrine: SEAL
- Provenance model: SEAL
- Privacy fixes: SEAL (interpretations now tagged, capabilities de-identified)
- Execution evidence: SEAL (hashes, backups, verification queries shown)
- Subject consent: VOID (no human has been asked)
- Syed Telegram name: HOLD (requires human action)
```

---

*DITEMPA BUKAN DIBERI ⚒️*
