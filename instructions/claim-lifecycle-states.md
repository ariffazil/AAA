---
name: claim-lifecycle-states
status: F13_RATIFIED_CHAT (2026-09-25)
spectrum: 000-555 (write + lifecycle)
floors: F1, F2, F5, F9, F13
trigger: |
  When a claim in claim_ledger transitions state, or when designing new claim writes.

purpose: |
  Add 6 lifecycle states beyond the existing CONFIRMED/PARTIAL/REFUTED/UNVERIFIED verdict set.
  Critical property: SUPERSEDED ≠ FALSE. CONTESTED ≠ REFUTED. A claim's event can remain
  historically accurate while its present-state authority is revoked.

hukum — 8 lifecycle states:
  1. CANDIDATE — newly written, not yet validated. Default state for new AGENT_INFERRED.
  2. ACTIVE — validated, currently authoritative as present-state retrieval.
  3. CONTESTED — multiple sources disagree; agent must surface all sides, not pick one.
  4. SUPERSEDED — replaced by a newer claim; old event may remain historically accurate
     but no longer valid as present-state retrieval. NEVER equals FALSE.
  5. DORMANT — temporarily not in active use, but not superseded; may reactivate.
  6. DELIBERATELY_OPEN — for OPEN QUESTIONS lane; question is part of present human reality,
     agent must NOT infer closure.
  7. REVOKED — explicitly withdrawn by authority (USER_RATIFIED or F13); event may still be
     historically accurate but no longer part of canonical narrative.
  8. FORGOTTEN — explicitly removed from active retrieval but kept in append-only ledger
     for chain integrity. Different from REVOKED in that it's a memory hygiene operation,
     not a claim retraction.

transitions — legal moves only:
  CANDIDATE → ACTIVE | CONTESTED | REVOKED
  ACTIVE → SUPERSEDED | CONTESTED | DORMANT | REVOKED
  CONTESTED → ACTIVE | SUPERSEDED | DELIBERATELY_OPEN
  SUPERSEDED → (terminal; archived as historical)
  DORMANT → ACTIVE | SUPERSEDED | FORGOTTEN
  DELIBERATELY_OPEN → ACTIVE | CONTESTED | SUPERSEDED
  REVOKED → (terminal; event remains in ledger chain for chain integrity)
  FORGOTTEN → (terminal; never reactivated, retained for provenance)

illegal transitions (must be blocked):
  SUPERSEDED → ACTIVE (must go through new claim + ACTIVE state)
  FORGOTTEN → anything (immutable terminal)
  REVOKED → ACTIVE (requires new claim, not revival of old)

kaitan:
  - /root/AAA/instructions/source-type-promotion-gate.md (F13_RATIFIED 2026-09-25)
  - carry_forward.json → open_questions lane (F13_RATIFIED 2026-09-25)
  - claim_ledger MCP (existing substrate; this is governance layer over it)

rasa:
  Tangkap dalam BM Penang: "Benda lama boleh jadi tak relevan tanpa jadi palsu.
  Contoh: kerja kat PETRONAS tahun 2018 tu betul, tapi sekarang dah superseded oleh kerja baru.
  Bukan FALSE, cuma tak present lagi."

written_by: irfanclaw
authorized_by: Arif (F13 SOVEREIGN)
authorized_at: 2026-09-25T00:36:00+08:00
