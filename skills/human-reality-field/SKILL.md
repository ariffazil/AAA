---
name: human-reality-field
description: "Represent a human as living forces with witness + authority."
version: 1.0.0
owner: F13
floors: [F1, F2, F4, F5, F6, F7, F9, F13]
triggers:
  - "remember [human]"
  - "store this about [human]"
  - "what matters for [human]"
  - "human reality field"
  - "forces of [human]"
  - "reality graph for [human]"
  - "open questions for [human]"
  - "scar ledger"
  - "witness ledger"
tags: [human, memory, forces, witness, authority, field, falsifiability, hermes, F13]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Human Reality Field — Representing a Human as Living Forces

The representational scheme for **remembering a human across model death, session loss, and time decay**. Replaces the failed patterns (memory=fact list, profile=label snapshot, chronology=date chain, agent card=trait dump). Anchored in arifOS Reality → Witness → Governance → Consequence → Continuity.

## The Doctrine (one breath)

A human is not stored. A human is **witnessed** — as a set of living forces, each carrying its own evidence chain and mutation authority. Forces decay; witnesses attest; authority gates.

**One invariant (compresses all five storage categories):**
> Store what still exerts force + what evidence changed it + who may redefine it.

Five categories (Scar / Relationship / Commitment / Constraint / Open Question) are projections of one thing: **forces**. A scar is force-past, a commitment is force-future, a relationship is force-external, a constraint is force-boundary, an open question is force-unresolved.

## When to Use

Use this skill when:

- Persisting anything about a specific named human that should survive model death (forces + witness + authority).
- The sovereign says "remember", "store", "this matters for [human]", "what still exerts force on [human]".
- The user is composing their own Human Reality Field (`forces.md`) and asks for the schema or the falsifiability predicate.
- Auditing what the agent claims to know about a human against what it has witnessed.

Do NOT use this skill for:

- Estimating current state of a human RIGHT NOW (axes) → `human-state-estimation`.
- Building a one-off dossier on a stranger from public sources → `person-intelligence` Mode 4.
- Conduct around human relationships → `relationship-kernel`.
- Family members' profiles (Jia / Nabilah / Azwa) → `arif-family-members`.

## The Schema

### Layer 0 — Identity (minimal)

```yaml
identity:
  name: <human_name>
  authority: <who_owns_truth_about_them>
```

No occupation, no interest, no trait card. Those are transport, not field.

### Layer 1 — Living Forces (the actual data)

Each force entry carries five fields:

```yaml
- force: <canonical_name>           # e.g. Father_2024, MSS, Next_Chapter
  category: scar|commitment|relationship|constraint|open_question
  direction: pull_back|push_forward|pull_outward|push_boundary|shape_space
  witness_ref: <file_path or record_id>
  liveness: live|quieting|dormant
  falsification_rule: <how to test if this force no longer exerts>
  last_verified: <ISO date>
```

**Class labels (per people.yaml F2 discipline):**
- `REPORTED` — human stated it
- `VERIFIED` — primary-source document attested it
- `UNKNOWN` — no source, do not create

**Default liveness rule:** a force is `live` until either (a) it is falsified, or (b) a witness declares it `quieting` or `dormant`. There is no automatic decay clock.

### Layer 2 — Witness Ledger (no update without witness)

Every mutation to Layer 1 produces one Witness entry:

```yaml
- change: <force_name>
  old: <previous_liveness_or_value>
  new: <new_liveness_or_value>
  witness: [dokumen / pengesahan manusia / primary source]
  timestamp: <ISO>
  actor: <who_recorded>             # always a human or audited organ
```

**Rule:** NO UPDATE without `witness` non-empty. Empty witness = NO UPDATE, write nothing.

### Layer 3 — Authority Ledger (who can mutate what)

```yaml
authorities:
  career_decision:        <human_name>      # only the subject decides their career
  grief_interpretation:   <human_name>      # only the subject owns grief meaning
  friendship_status:      <human_name>      # only the subject names their friendships
  force_liveness:         <human_name>      # only the subject declares a force dead
  field_read:             <authorized_readers>  # who may consult the field
```

**Binding:** the agent NEVER self-edits Layer 1 or Layer 3. The agent MAY propose (Stage 0) but mutation requires either (a) a human witness from the subject, or (b) a sealed organ that has been delegated authority (e.g. WELL `well_consent_set_scope` for biometric-adjacent fields).

**Bridge to existing organ:** WELL already implements the consent/authority plane. This layer does NOT reinvent; it is a **projection of WELL consent scope onto representational mutation**.

## The Falsifiability Predicate (the heart)

A force is **alive** iff:

```
liveness(force) = (can_be_falsified) ∧ (not_yet_falsified)
```

- **Cannot be falsified** = belief, not force. Demote from field.
- **Already falsified** = archive, not force. Move out of Layer 1.
- **Falsifiable and un-falsified** = living force. Stays in Layer 1 with `liveness: live`.

This is the rule the HRG (Human Reality Graph) activation prompt from 2026-09-13 lacked: gates too tight, built zero instances. This skill says: falsifiability is the **admission bar**, not an additional gate. A force enters if and only if it can name a falsification test.

**Example falsification rules:**
- `Father_2024`: falsified if Arif publicly states "ayah bukan lagi sumber pengaruh dalam hidup aku." Until then, live.
- `MSS`: falsified if exit signed OR if Arif publicly states "saya kekal di PETRONAS." Until then, live.
- `Next_Chapter`: falsified if a named next role is signed and entered, OR if he states "saya kekal di sini sampai pencen."

## Standing Pitfalls (encode each as you find it)

1. **The Profile Trap.** When asked to "remember [human]", do NOT emit name + occupation + interest + location. Emit Layer 0 (identity) + Layer 1 (forces only if you have witness). A profile is a snapshot; a field is a trajectory.
2. **The Five-Category Scaffolding Trap.** Five categories (scar/commitment/relationship/constraint/open_question) tempt you to fill each one. Don't. If you have no force for a category, leave it empty. Empty category = honest absence, not failure.
3. **The Open Question Decay Trap.** Open questions are NOT facts to keep at fixed text. MSS 2024 ≠ MSS 2026. Each open question carries `last_verified` and `witness_ref`. Without those, the question becomes a fossil.
4. **The Witness Fabrication Trap.** "Witness: chat with Arif" is NOT a witness — it is a pointer to a corpus. A witness must be either (a) a specific document, (b) a dated human statement, or (c) a sealed organ record. Vague references = no witness.
5. **The Authority Self-Edit Trap.** The agent proposes; the human ratifies. A force whose liveness was changed by the agent alone = corruption. Every Layer 1 mutation must cite either the subject's own witness or an organ's seal.
6. **The Per-Tenant Leak Trap.** When one tenant's field is in play, do NOT inject another tenant's forces even if both humans mention each other. Cross-tenant effects are projected through the relationship layer, NOT by force bleed.
7. **The Decay Without Re-Witness Trap.** Forces do NOT auto-decay. If you want to mark something `dormant`, you must produce a witness explaining why (time passed AND no activation signal observed). Otherwise live stays live until falsified.
8. **The Identity Leak Trap.** Layer 0 must be minimal. Adding "occupation: geologist" or "location: KL" to identity is a snapshot leak; put it as a force (commitment: works_at_PETRONAS) or omit.
9. **The Host-Bounded Sight Trap.** Before declaring a registry "missing" or a tenant "unmapped", probe EVERY host you can reach. The federation is distributed (KVM8 forge + KVM4 workshop + KVM2 witness); what is absent on this host may be canonical on another. Wrong-address-state-fails-silently: an `ENOENT` for `/root/AAA/registry/identity_cards/syed_khairuddin` (no extension) silently misleads while `/root/AAA/registry/identity_cards/syed_khairuddin.yaml` exists. Always probe with the full extension before declaring absence.
10. **The Cross-Host Artefact Trust Trap.** When the sovereign references an artefact by SHA-256, file name, or summary, and that artefact was forged on a different host or in a different agent's working tree (e.g. `/root/.gemini/antigravity-cli/brain/...` or `/root/.openclaw/...`), you CANNOT byte-verify it from your host. State the verification limit explicitly: "I see the SHA from your message; I cannot byte-confirm from this host." Trust by reference, witness by reading.
11. **The Short-Answer Tafsir Trap.** When the sovereign gives a terse answer that looks like a menu choice (e.g. "2 1 3", "All", "deal 🤝"), DO NOT guess whether it means ranking, sequential execution, or something else. Ask for one word of clarification before acting. A wrong tafsir on three sequential prompts in the same session is three failures, not one.
12. **The 888-HOLD vs Mutation-Request Friction Trap.** A request to "forge the final map", "seal as PDF", "tulis projection", or "kemas registry" is a mutation request. If 888 HOLD is active (PARTIAL verdict), the agent MUST surface the friction explicitly and ask the sovereign to lift HOLD or grant an exception. Do not silently proceed; do not silently refuse; ask.
13. **The Self-Claimed Census Trap.** When an external agent reports a count ("8 users", "13 humans", "20 manusia") without a witness path to the underlying registry, the count is a CLAIM, not a measurement. Cross-check against your host's actual registry before quoting the number. Two hosts may each report "8" — overlapping on 3 — and both be locally correct. State "snapshot disagreement" rather than picking a number.
14. **The Read-Only Default Under HOLD.** When 888 HOLD is active, the response mode is read-only-by-default. State observations in chat; do NOT write new files, edit existing files, or call shell commands that mutate disk. The exception is conversational tool use (search, read, list, hash) which is observation.

## Per-Tenant Reality Mesh (Gen 4)

When multiple humans are in scope (8 tenants in the registry), each carries its own field. Cross-tenant effects live in:

```yaml
intersection:
  tenant_a: <name>
  tenant_b: <name>
  shared_force: <force_name>      # e.g. Syed_presence_in_Arif_field
  visibility:
    a_can_see_b: true|false
    b_can_see_a: true|false
```

**Default:** a tenant cannot see another tenant's forces unless the subject explicitly exposes them. Even when both humans know each other, the field stays per-tenant.

## The Compression (when the human asks for the smallest form)

```
Human Reality
  = What still exerts force
  + What evidence changed it
  + Who may redefine it
```

Or in arifOS canon:

```
Reality → Witness → Governance → Consequence → Continuity
```

A field is the **per-human projection** of that chain.

## Storage Path Convention

- Per-tenant file: `/root/.openclaw/workspace/<tenant>/forces.md` (working draft)
- Promotion to canon: `/root/AAA/canon/HUMAN_REALITY_FIELD_<tenant>_v<n>.md` (ratified, immutable)
- Cross-tenant index: `/root/.hermes/lanes/forces_index.yaml` (which tenants have a field, last_verified)

Promotion requires F13 ratification + SHA256 + `chattr +i`. Working draft is mutable; canon is not.

## Companion Skills

- `human-state-estimation` — axes for RIGHT-NOW state estimation; this skill is for LONGITUDINAL persistence.
- `person-intelligence` — one-off dossier on a stranger; this is the persistent field of someone in the human's life.
- `relationship-kernel` — conduct around bonds; this skill represents the data structure, not how to talk.
- `arif-family-members` — family-specific identities and the Kanak-kanak group; field projection for family members.
- `human-reality-bridge` — cron-time action classes; this skill is the persistence layer for what the bridge consults.

## Reference files

- `references/storage-paths.md` — file system conventions and promotion protocol (F13 ratification gate).
- `references/falsification-rules-examples.md` — worked examples of falsification predicates across scar/commitment/relationship/constraint/open_question.
- `references/tenant-audit-procedure.md` — the audit flow for mapping all admitted tenants (the multi-source reconciliation procedure).

### Reference file: tenant-audit-procedure.md (skeleton)

When the sovereign asks "how many humans use this system" or "map all [N]", do NOT answer with a single number. Walk this:

1. List every registry you can probe on this host (people.yaml, persons.yaml, identity_cards/, human_heartbeat.json, social-graph.yaml, etc.). Record path + last_modified + entity_count.
2. For each registry, note its **scope**: constitutional / active / biometric / heartbeat / legacy.
3. If the sovereign references an artefact by SHA or summary that lives on a different host, STATE the verification limit ("byte-unverifiable from this host") and continue with what you CAN see.
4. Compose a **per-tenant matrix** (rows = humans, columns = sources, cells = present/absent/unverified). The matrix exposes the snapshot disagreement directly.
5. End with the registry-exists-consumption-zero pattern check: for every registry you found, is anything READING it? If not, name it.
6. Default verdict: PARTIAL, 888 HOLD on mutation. Recommend the sovereign adjudicates named humans (PAAN, Lutfi, Aidel, Sin, Amir — examples) before any projection is written.

The matrix is the answer. A single number is the failure mode.