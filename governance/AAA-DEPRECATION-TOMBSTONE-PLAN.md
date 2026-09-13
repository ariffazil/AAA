---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path)
date: 2026-09-14
related: WP-01-IDENTITY-CONVERGENCE-DELIVERABLES.md §3 (Alias Deprecation Manifest)
---

# AAA Deprecation Tombstone Plan

> **Status:** DRAFT_PROPOSAL — proposes tombstone-first protocol for retired/dormant entities.
> **No deletion. No rename. No commit.** Tombs are pointers with provenance + sunset date.

---

## Tombstone schema (canonical)

```yaml
---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path)
date: 2026-09-14
related: WP-01-IDENTITY-CONVERGENCE-DELIVERABLES.md §3
---

# AAA Deprecation Tombstone Plan

> **Status:** DRAFT_PROPOSAL — proposes tombstone-first protocol for retired/dormant entities.
> **No deletion. No rename. No commit.** Tombs are pointers with provenance + sunset date.

---

## Tombstone schema (canonical)

```yaml
---
tombstone_id: <canonical-id>-deprecation-<date>
status: TOMBSTONE_PROPOSED  # or TOMBSTONE_ACTIVE after governed ack
entity_type: actor | alias | file | endpoint | skill | doctrine
canonical_id: <id-being-tombed>
aliases_to_tombstone: [<alias_1>, <alias_2>]
sunset_date: <ISO-date>  # when tombstone becomes permanent; before that, reversible
provenance:
  created_by: <actor>
  session: <session-id>
  created_at: <ISO-datetime>
  reason: <1-line justification>
  related_doctrine: <pointer>
  call_site_audit: <DONE | NOT_DONE | IN_PROGRESS>
replacement: <canonical-id>  # what to use instead
reversibility: FULL | PARTIAL | NONE
f13_surface: <true | false>
authority_needed: <lane>
---
```

---

## Tombstone candidates (DRAFT)

### 1. Alias: `kimi-code-fi008` → tombstone toward `kimi-code`

- **Reason:** Three identifiers (kimi-code-fi008, FI-008, kimi-code) for one actor. Per MODEL-INIT-CANONICAL.v1, one canonical ID.
- **Call-site audit:** NOT_DONE (BLOCKING)
- **Sunset:** TBD after audit
- **Replacement:** `kimi-code`
- **Reversibility:** FULL (alias only)
- **F13 surface:** TRUE (final retire requires sovereign ack)
- **Authority needed:** arifOS engineer lane + sovereign ack

### 2. Alias: `FI-008` → tombstone toward `kimi-code`

- Same as #1.
- **Reversibility:** FULL

### 3. Actor: `forge-bot` → ARCHIVED

- **Reason:** RETIRED-TBD per WARGA STATUS injection; no active process; no documented use.
- **Call-site audit:** NOT_DONE (likely zero; just need to confirm)
- **Sunset:** 90d from approval
- **Replacement:** none
- **Reversibility:** FULL
- **F13 surface:** TRUE (sovereign review)
- **Authority needed:** AAA + sovereign ack

### 4. Actor: `agent-zero` → ARCHIVED

- **Reason:** ARCHIVED per ARCHIVE.md; pre-2026-06-30 last activity.
- **Call-site audit:** NOT_DONE (likely zero; already archived)
- **Sunset:** TBD
- **Replacement:** none
- **Reversibility:** FULL (already archived)
- **F13 surface:** TRUE (sovereign review for final commit of tombstone)
- **Authority needed:** AAA + sovereign ack

### 5. Bot: `hermesarifos-bot` → DORMANT tombstone

- **Reason:** DORMANT per IDENTITY_LOCK; bot still exists at /opt/hermesarifos-bot/bot.py.
- **Call-site audit:** NOT_DONE
- **Sunset:** TBD
- **Replacement:** none (dormant but preserved)
- **Reversibility:** FULL
- **F13 surface:** TRUE
- **Authority needed:** AAA + sovereign ack

---

## Tombstone protocol (canonical)

1. **Call-site audit FIRST** — enumerate every reference to the candidate
2. **Tombstone** — add `*.TOMBSTONE` marker file with the canonical schema above
3. **Wait period** — 30 days for actor-aliases, 90 days for actor-tombstones
4. **Sunset commit** — controlled by sovereign ack
5. **Original preserved** — original files retained for reversibility until FULL irreversibility accepted

**No alias is deleted in any WP. Only tombstones.**

---

## Acceptance tests

- AT-TOMB-01: Every tombstone has all required schema fields.
- AT-TOMB-02: Every tombstone has a `replacement` (or explicit `none` with rationale).
- AT-TOMB-03: Every tombstone has a `sunset_date` (reversible until then).
- AT-TOMB-04: Call-site audit status is `DONE` before sunset (BLOCKING for FINAL retire).
- AT-TOMB-05: Originals retained until FULL reversibility accepted.

---

*Reversibility: FULL until sunset. After sunset, requires sovereign explicit ack.*
*F13 surface: TRUE for all candidates.*
*DITEMPA BUKAN DIBERI ⚒️