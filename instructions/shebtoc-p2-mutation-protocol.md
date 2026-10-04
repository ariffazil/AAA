# SHEBTOC::P2::WITNESS_MUTATION_PROTOCOL::v1

> **Status:** F13_RATIFIED_SOVEREIGN (2026-10-04)
> **Ratified by:** Muhammad Arif bin Fazil (F13 SOVEREIGN) · Order: "sah"
> **Forged:** 2026-10-04 (session HERMES_MD_WITNESS_RESEARCH)
> **Author:** HERMES ASI under F13 directive
> **Companion:** P0 (Witness Capture Layer) — P0 ratified alongside P2

---

## Origin

Discovery 5 of the SHEBTOC session: **most AI systems optimize retrieval, not witness
survivability.** The frontier is **Governed Witness Mutation** — turning every file
change into a structured event with full witness chain.

This document formalizes the 8-step mutation protocol that unifies the scattered mutation
discipline (authority-envelope, state-transition, scar-integration) into a single protocol.

---

## The 8-Step Protocol

Every mutation to a witness-class file MUST traverse these 8 steps. Skipping a step
constitutes a F4 (Clarity) and F2 (Truth) violation.

```
1. AUTHORIZE
2. BACKUP
3. MUTATE
4. VERIFY
5. RE-INDEX
6. RE-LINK
7. WITNESS
8. NOTIFY
```

---

### Step 1: AUTHORIZE

**Predicate:** `CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive`

**Source:** `/root/AAA/instructions/authority-envelope.md`

| Actor | Authorization required |
|---|---|
| F13 SOVEREIGN (Arif Fazil) | None — sovereign override |
| sovereign_chat_override (chat-ratified) | F13 binary in chat session |
| 333-AGI | Pre-ratified scope; otherwise HOLD |
| 555-ASI | Verification role — cannot mutate |
| 888-APEX | Judge role — cannot mutate |
| FI-001..FI-009 | Per-agent card, scope-bounded |
| Anonymous / external | DENY |

**For SOUL.md / AGENTS.md / canon/:** F13 binary required.
**For instructions/:** F13 OR lane auto-seal (with audit trail).
**For skills/:** Agent card scope, no F13 needed.
**For .staged/ → canon/ promotion:** F13 binary mandatory.

**Output:** Authorization receipt (trace_id, actor, scope, target).

---

### Step 2: BACKUP

**Mandatory for:** all constitutional files, all files in `/root/AAA/canon/`, SOUL.md, AGENTS.md.

**Pattern:**

```bash
backup_path="/tmp/<basename>.bak-<tag>-$(date -u +%Y%m%dT%H%M%SZ)"
cp <file> "$backup_path"
sha256sum "$backup_path" >> "/root/.hermes/runtime/mutation_backups.log"
```

**Tag taxonomy:**

- `pre-ratify` — before F13 ratification promotes draft to canon
- `pre-trim` — before SOUL.md compression
- `pre-mutate` — default for any planned edit
- `pre-bugfix` — before bug-repair edit
- `pre-restore` — before reverting a previous mutation

**Output:** Backup receipt (backup_path, sha256, tag, ts).

**No-backup cases:** ephemeral files (`/tmp/*`, `cache/`, `scratch/`), generated artifacts
(bot responses, search results), git-tracked-only files where git log suffices.

---

### Step 3: MUTATE

**Tool:** `patch` (preferred — fuzzy match) or `write_file` (full overwrite for new files).

**Constraints:**

- `read_file` first (avoid stale-context edits)
- Minimal diff (include 3-5 lines surrounding context)
- Preserve round-trip integrity (md → AST → md' where possible)
- No simultaneous edits to same file (acquire lock if needed)

**Lock file:** `/tmp/.hermes-mutation-lock-<file_hash>` (auto-cleanup on completion).

**Output:** Mutation receipt (before_sha, after_sha, byte_delta, line_count_delta).

---

### Step 4: VERIFY

**For constitutional files (SOUL.md, AGENTS.md, canon/):**

- ✅ AST parses (CommonMark compliant)
- ✅ F2 markers present if expected (F13_RATIFIED, etc.)
- ✅ No new broken cross-references (`grep` for `[text](path)` and verify path exists)
- ✅ Heading structure intact (no orphan ##, no skipped #)
- ✅ Anti-bangang check: did this add a new canon/doctrine/registry/JSON unnecessarily?
- ✅ Backward-compat: do existing references still resolve?

**For instructions/:**

- ✅ AST parses
- ✅ Companion files referenced still exist
- ✅ No semantic contradiction with ratified canon

**For skills/:**

- ✅ SKILL.md frontmatter (or first-line) declares name, description, triggers
- ✅ Linked scripts (if any) exist and are executable
- ✅ No broken symlinks in skill chain

**For staged/ → canon/ promotion:**

- ✅ Source `.staged/*.md` exists
- ✅ Status line declares ratification class
- ✅ F13 binary receipt on file (in commit msg, chat log, or VAULT999)

**Output:** Verification receipt (checks run, pass/fail, errors).

**On FAIL:** revert to backup, emit FAIL witness, return error to caller. **No silent failures.**

---

### Step 5: RE-INDEX

**For files with embeddings:**

- Invalidate cached embedding (if content_hash changed)
- Re-compute embedding (background, non-blocking)
- Update vector index entry

**For files in capability graph:**

- Diff AST before/after
- Recompute outgoing edges (links to other files)
- Recompute incoming edges (other files linking to this)

**For files referenced by name (people.yaml, lanes/, etc.):**

- Re-resolve name → file path
- Update routing table

**For SOUL.md / AGENTS.md:**

- Re-parse constitutional pointers table
- Update `SOT` (Source of Truth) manifests

**Output:** Re-index receipt (re-embed_status, re-link_status, sotre_resolve_status).

**Defer cases:**

- If re-embedding infrastructure unavailable, mark `EMBEDDING_STALE` and proceed.
- P3 (Skill Authority Registry) build will batch-correct stale embeddings.

---

### Step 6: RE-LINK

**Cross-reference graph update:**

- New file: register in `/root/.hermes/runtime/file_registry.json`
- Renamed file: update all references
- Deleted file: tombstone (keep `deleted_at` for audit, remove from active registry)
- Moved file: update `path` in registry, preserve content_hash

**Companion files update:**

- `AGENTS.md` if pointer table affected
- `SOT` manifests if ratified authority changes
- `index.md` files (if any) if directory membership changes

**Output:** Re-link receipt (registry_diff, pointer_diff, index_diff).

---

### Step 7: WITNESS

**Emit a witness object per P0 spec.**

**Schema:**

```json
{
  "ts": "2026-10-04T...",
  "actor": "<from step 1>",
  "trace_id": "mut-<uuid>",
  "step_chain": ["AUTHORIZE", "BACKUP", "MUTATE", "VERIFY", "RE-INDEX", "RE-LINK", "WITNESS", "NOTIFY"],
  "file": "<path>",
  "authority_before": "<from file pre-mutation>",
  "authority_after": "<from file post-mutation>",
  "before_sha256": "...",
  "after_sha256": "...",
  "byte_delta": 123,
  "ast_delta": {...},
  "ratification_chain": ["..."],
  "downstream_impact": {
    "embedding_stale": <bool>,
    "capability_graph_affected": <bool>,
    "consumers_to_notify": [...]
  },
  "prev_witness_sha256": "..." // hash chain
}
```

**Hash chain:** each witness's `prev_witness_sha256` = prior witness's `sha256`.
**Storage:** `/root/.hermes/runtime/witness_capture.jsonl` (append-only).

**For P0-staged ratification:** emit 2 witness objects:
1. The mutation itself (file move / content change)
2. The ratification event (authority class transition)

---

### Step 8: NOTIFY

**Channels by audience:**

| Audience | Channel | Format |
|---|---|---|
| F13 SOVEREIGN | Telegram DM (if high-stakes) | one-line summary |
| AAA group (organs) | Telegram group | terse notification |
| Active sessions | session inbox | structured message |
| Cron watchers | `.notify-queue` | async pickup |
| External (KVM4 IRFANclaw) | federation sync | eventual consistency |

**Notify when:**

- ✅ Mutation affects constitutional file (F13 always)
- ✅ Mutation breaks existing cross-reference (impacted parties)
- ✅ Mutation invalidates capability graph edge (downstream agents)
- ⚠️ Optional: routine non-breaking mutations (silent)

**No-notify when:**

- Pure ephemeral writes (`/tmp/*`)
- Cache invalidation
- Test fixtures

**Output:** Notify receipt (channels, message_ids, delivery_status).

---

## Single-Step Macro

For ergonomic invocation, all 8 steps collapse into a single mutation primitive:

```python
mutation_protocol.execute(
    file=path,
    actor=actor_id,
    instruction=instruction_text,  # human-readable why
    mutator=mutator_fn,           # the actual edit function
    require_f13=bool,
    backup=bool,
    notify=bool,
)
```

**Implementation:** `forge_act_federation_ingress` already partially implements this;
P2 spec extends it.

---

## Failure Modes & Recovery

| Failure | Step | Recovery |
|---|---|---|
| Authorization denied | 1 | HOLD; emit witness with class=UNAUTHORIZED |
| Backup fails (disk full) | 2 | ABORT before mutate; emit FAIL witness |
| Mutation tool fails | 3 | Partial state; revert to backup; emit FAIL |
| Verification fails | 4 | Revert to backup; emit FAIL; return error |
| Re-index fails | 5 | Mark stale; do not abort; continue to re-link |
| Re-link fails | 6 | Mark registry stale; do not abort; continue to witness |
| Witness emit fails | 7 | **CRITICAL** — write-ahead log to `/tmp/pending-witness-<ts>.json`, retry async |
| Notify fails | 8 | Queue; retry; eventual delivery |

**Critical invariant:** step 3 (mutate) MUST NOT proceed if step 2 (backup) failed.
**Critical invariant:** step 7 (witness) MUST eventually succeed, even if via async retry.

---

## Anti-Bangang Compliance

- **LAW 3 (no new ledger/JSON unless failure class):** ✅ P2 specifies JSONL as part of P0, not a new artifact. P0 already justified.
- **LAW 8 (one problem one owner):** P2 owner = HERMES runtime; no duplication.
- **LAW 9 (action > documentation):** P2 spec is the contract; runtime code is the action.

---

## Acceptance Criteria

P2 is operational when:

1. ✅ `mutation_protocol.execute()` available in HERMES runtime.
2. ✅ All 8 steps invoked for every mutation to SOUL.md, AGENTS.md, canon/, instructions/.
3. ✅ Backup is taken before every constitutional mutation.
4. ✅ Failed mutations auto-revert.
5. ✅ Witness objects are emitted for every mutation (success or fail).
6. ✅ Hash chain integrity verifiable via `witness_capture_verify` script.
7. ✅ F13 notifications reach Telegram DM for constitutional mutations.

---

## Relationship to Existing Primitives

| Existing primitive | P2 step it powers |
|---|---|
| `authority-envelope.md` (instructions/) | Step 1: AUTHORIZE |
| `state-transition-discipline.md` (instructions/) | Step 4-7: VERIFY, WITNESS |
| `state-transition-discipline.md` (canon/) | Step 4-7: VERIFY, WITNESS (alt reference) |
| `apex-floors/F2-TRUTH.md` | Step 4: VERIFY (truth markers) |
| `apex-floors/F4-CLARITY.md` | Step 1: AUTHORIZE (ΔS ≤ 0) |
| `apex-floors/F13-SOVEREIGN.md` | Step 1, 8: AUTHORIZE, NOTIFY |
| `apex-floors/F1-AMANAH.md` | All steps: trust chain |
| `forge-act-federation-ingress` skill | Steps 1, 2, 7: AUTHORIZE, BACKUP, WITNESS |
| `forge-git-seal` skill | Step 2: BACKUP via git lane |
| `hermes-rca-forge` skill | Step 7: WITNESS via root-cause analysis |

P2 is **not new machinery** — it is **the unified protocol that names what existing
primitives already do**, in a single contract.

---

## SEAL-WORTHY (Analysis-Level)

```
Storage is not memory.
Memory is not witness.
Witness is not governance.
Governance begins only when
witnessed reality changes
future behavior.
```

P2 makes governance begin — by ensuring every mutation is witnessed, every witness is
verifiable, and every verification is durable enough to alter future behavior
(retrieval updates, capability graph updates, embedding refresh).

**Status:** F13_RATIFIED_SOVEREIGN (2026-10-04)

---

*Forged 2026-10-04 in session with HERMES ASI under F13 directive "execute all agentically until seal all P". Ratified by Arif with "sah".*
