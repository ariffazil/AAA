---
registry: governance-RETENTION
version: 0.1
compiled_on: 2026-10-11
compiled_by: FI-008 (kimi-code)
authority_resolution: /root/AAA/canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md (Canon #0)
companion_to: /root/AAA/canon/INDEX.md
build_policy: READ-ONLY with respect to /root/AAA/governance/* — no rewrites of existing governance files
seed_principle: Authority is entropy-cleaned; lifecycle is explicit; quarantine precedes deletion
---

# Governance RETENTION — Lifecycle & Quarantine Law

**Authority:** ARIF (sovereign). This law governs the lifecycle of every file in the federation that claims any authority whatsoever (canon, instruction, governance, report, scar, eureka, witness).

**Companion to:** `/root/AAA/canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md` (Canon #0 — three-test gate for new law).

---

## 1. Status vocabulary (5-state for canon/governance)

| Status | Meaning | Operational consequence |
|---|---|---|
| `ACTIVE` | Sealed/ratified, in force. | Authority binds. Loader reads. |
| `DRAFT` | Pending F13 ratification. | No operational authority. Visible to humans. |
| `SUPERSEDED` | Replaced by another `ACTIVE` canon. | History only. Marked in `supersedes` chain. |
| `ARCHIVED` | Moved to `*/archive/`. | Removed from loader scan. History only. |
| `VOID` | Rejected. | No authority. Quarantine then optional delete. |

`SEALED`, `FINAL`, `LATEST`, `v3-final-final` are NOT lifecycle status. They appear as frontmatter metadata or receipt references only. A file claiming `FINAL` without being listed ACTIVE in `/root/AAA/canon/INDEX.md` has no operational authority.

## 2. Status vocabulary (5-state for reports/)

| Status | Meaning | Operational consequence |
|---|---|---|
| `OPEN` | Filed, not yet consumed by any canon. | Searchable. Quarantine-eligible after one working cycle. |
| `CONSUMED` | Cited as witness by ≥1 ACTIVE canon. | Authority bound to consumer. Retention-tier attached. |
| `SUPERSEDED` | Replaced by newer report with same purpose. | History only. |
| `QUARANTINED` | No inbound reference; exceeds working cycle. | Moved to `_quarantine/`. |
| `VOID` | Rejected. | Optional delete after quarantine period. |

Rule: **Report without `consumed_by`, without inbound reference, and exceeding one working cycle = quarantine candidate, NOT canon candidate.**

## 3. Frontmatter requirements

### 3.1 Canon/governance/instruction files MUST carry:

```yaml
---
canon_id: AAA-CANON-001           # OR governance_id, instruction_id
status: ACTIVE                     # only ACTIVE/DRAFT/SUPERSEDED/ARCHIVED/VOID
authority: ARIF                    # ratifier id
canonical_path: <absolute path>
supersedes: [<canon_id>, ...]      # empty for first-of-kind
evidence:
  - <report path witnessing this canon>
last_reviewed: YYYY-MM-DD
fingerprint: <content sha256[:16]>
fs_flag: i                          # file-level immutable when ACTIVE
---
```

### 3.2 Reports/witnesses MUST carry:

```yaml
---
report_id: <kebab-case>
report_status: OPEN | CONSUMED | SUPERSEDED | QUARANTINED | VOID
consumed_by:
  - <canon_id this report witnesses>
retention: ARCHIVE | DELETE-OK | PERMANENT
authority_claim: NONE               # reports never claim authority
filed_on: YYYY-MM-DD
fingerprint: <sha256[:16]>
---
```

## 4. Quarantine criteria (4 must all hold)

A file becomes `_quarantine/` candidate iff **all four** are true:

```
no inbound reference
AND not ACTIVE in canon/INDEX.md
AND not loader-wired
AND no unresolved HOLD against this file
```

Quarantine destination: `/root/AAA/_quarantine/` (federation-wide, year-tagged).

## 5. Delete criteria (3 must all hold after quarantine)

```
quarantine period completed (≥30 days)
AND second reference scan clean (grep shows zero hits)
AND human acceptance by ARIF (explicit)
```

No automated deletion. No cron-based sweeping. Quarantine is the cooling step.

## 6. Four Invariants (binding)

1. **One Canon ID, One Active Path.** No two files may be `ACTIVE` for the same authority.
2. **Reports Witness, Canon Governs.** A report proves; only canon establishes.
3. **Supersession Must Be Explicit.** A new canon must name the files it replaces in `supersedes:`. Implicit supersession is invalid.
4. **No Orphan Authority.** A file claiming `FINAL`, `SEALED`, or `CANONICAL` but not listed `ACTIVE` in `/root/AAA/canon/INDEX.md` has zero operational authority. Loading it is a violation.

## 7. File-system contract (F13 enforcement surface)

The kernel-level immutable flag (`chattr +i`) is the lowest enforcement layer:

- Every `ACTIVE` canon file MUST carry the file-level `i` flag.
- Every directory of canon artifacts (`canon/`, `governance/`) carries directory-level `i` to block ad-hoc additions.
- Adding a new ACTIVE canon requires the **lift-write-reflag ritual**:
  1. `chattr -i <dir>` (sovereign-class action)
  2. write the file
  3. `chattr +i <new file>` (file-level)
  4. `chattr +i <dir>` (directory-level restore)
- The `/root/AAA/scripts/canon_scanner.py` reads `/root/AAA/canon/INDEX.md` and answers "is file X canon-active?" without touching the filesystem flags.

## 8. Build pipeline (canonical order — Canon #0)

```
Inventory  →  Classify  →  Build Canon Registry  →  Build inbound-reference map
   →  Mark supersession  →  Quarantine orphans  →  Verify loaders
   →  Human acceptance  →  Later deletion
```

NOT:

```
List old files  →  Guess dust  →  Delete  →  Discover hidden dependency
```

## 9. Companion registries (built today, pass 1)

- `/root/AAA/canon/INDEX.md` — canon authoritative registry (14 of ~210 rows; pass 2 pending)
- `/root/AAA/reports/INDEX.md` — witness disposition registry (built today)
- `/root/AAA/scripts/canon_scanner.py` — read-only scanner

Pass 2 will: filesystem-wide scan of `/root/AAA/canon/`, classify the 196 uncatalogued files, populate the supersession column, and produce the quarantine candidate list. **No file moves in pass 1.**

---

**Maintainer:** ARIF. **Patch author:** FI-008. **Status:** v0.1 draft 2026-10-11.
**Verification:** `/root/AAA/scripts/canon_scanner.py` (read-only lookup).
