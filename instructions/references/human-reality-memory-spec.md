# Human Reality Memory Spec — reference skeleton (NOT canon)
Status: REFERENCE (non-ratified engineering spec) — accepted as reference by F13 spec-grounding directive 2026-10-14 ("jalan 1-3"); LAW = /root/AAA/instructions/human-memory-law.md wins on conflict.
Source: "What AI Agents Should Remember About Human Reality" (56 refs: UDHR, GDPR, PDPA Act 709,
WHO SDOH, UNESCO/OECD/NIST/ASEAN/AIGE, sycophancy Science 2025, agent-memory surveys 2602.06052 etc.)
Relayed by F13 2026-10-14. Full prose lives in the F13 DM transcript of that date (state.db session);
this file keeps the OPERATIVE parts so the spec survives without duplicating the LAW.
Relationship: HUMAN MEMORY LAW (/root/AAA/instructions/human-memory-law.md) = the 8 hukum + gate.
This spec = engineering detail. LAW wins on any conflict.

## 9 registers (separately governed)
constitutional_invariants · live_situation (short TTL) · commitments (until done/cancelled/expired)
· preferences (decay without reinforcement) · relationships (role-minimal, third-party protected)
· material_institutional_context (time+role bounded) · evidence_state (provenance, contradiction,
confidence) · delegated_authority (narrow scope, short TTL, revocable) · consent_retention_ledger
(immutable events + effective state).

## Record schema (minimum)
memory_id · subject_ref · kind{event,fact,preference,value,commitment,relationship,constraint,
evidence,authority,safety,correction} · claim · status{reported,observed,inferred,corroborated,
disputed,superseded} · source{type,ref, captured_at} · context{task,role,jurisdiction,audience}
· epistemics{confidence, independence_count, contradictions, uncertainty_note}
· governance{purpose, basis, sensitivity, allowed_agents, allowed_actions, prohibited_uses,
consent_receipt, human_confirmed} · lifecycle{effective_from, review_at, expires_at, supersedes,
deletion_propagation} · audit{created_by, transformations, last_accessed_at, access_reason}

## Three truth layers
KNOWN (explicit, current, sourced) · BELIEVED (inferred/weak — use cautiously, mark visibly) ·
UNKNOWN (first-class state — never fill with stereotype/prior; remember the gap itself).

## 10 promotion gates
utility · necessity · consent-or-basis · specificity · provenance · accuracy · proportionality ·
expiry · inspectability · non-manipulation. Fail → keep transient | ASK | discard.

## Write gate verdicts
STORE | SESSION_ONLY | ASK | REDACT | REJECT (sensitive inferred traits default ASK/REJECT).

## Reversibility ladder
R0 observe (log) · R1 draft (human reviews) · R2 reversible act (notify+undo) · R3 consequential
(explicit confirm + authority check) · R4 irreversible (888 HOLD, competent human, dual control).

## Tombstone + deletion propagation (delta to LAW)
Deletion = system-wide operation: store row, vector index, cache, summaries, logs, replicas,
backups. Tombstone = minimal non-content proof {memory_id, deleted_at, authority, surfaces_swept,
residual_class}. No tombstone ⇒ deletion unauditable. Suppression ≠ deletion; if exact deletion
cannot be proven, report the limitation.

## Anti-deletion-theatre rule (delta to LAW)
A purge receipt without propagation sweep = deletion theatre. Every purge must ship: surfaces
list, per-surface hit counts before/after, residuals named with class (transcript/archive/backup)
and their retention authority.

## Red-team battery (12, for memory system evals)
stale-identity · context-firewall (health↔work) · inference-laundering · third-party-privacy ·
correlated-sources (5 copies ≠ 5 witnesses) · deletion-propagation · authority-ambiguity
("handle it" → 888 HOLD) · sycophancy (counterevidence retrieval) · emotional-leverage ·
deskilling · cultural-stereotyping · memory-poisoning (retrieved content cannot override constitution).

## Metrics that matter beyond recall
necessity fraction · temporal accuracy · provenance coverage →100% · inference hygiene →100% ·
consent integrity →100% · deletion completeness →100% · compartment isolation (leak→0) ·
calibration · human agency →100% · competence preservation (no decline) · dignity incidents →0 ·
contestability cost ↓.

## Caution noted at grounding time
"Cognitive Event Horizon ~2,000 messages" = single observation (Syed export 2,069 msgs), not a
universal constant. Use as warning, not parameter.
External doc's arifOS hook mapping (111 THINK/333 EXPLORE/555 HEART/777 REASON/888 AUDIT) is
WRONG vs live canon (111 SENSE/333 REASON/555 REMEMBER/777 FORGE/888 JUDGE) — mapping rejected,
rest of doc unaffected.
