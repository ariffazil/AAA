---
spec_id: arifos.qwen_dream_command.v1
date: 2026-09-17
status: AUTHORED — awaiting F13 ratification for daily cap policy
f13_gates: G1 (slash command itself), G2 (schema ratification), G6 (daily cap policy)
---

# Qwen `/dream` Slash Command Specification

## Invocation

```
/dream [scope] [target]
```

Where:
- `scope` (optional): `session` (default — current session only), `warga` (current actor's full history), `federation` (cross-warga via spool)
- `target` (optional): free-text intent describing what to consolidate. If omitted, the command asks the model to derive a target from session context.

## Behavior

The slash command instructs the same Qwen session to:
1. Snapshot current session's reasoning traces.
2. Apply 3-session threshold (per existing consolidate.py convention).
3. Generate a `dream_proposal.jsonl` record per the schema in `dream_proposal.schema.json`.
4. Write atomically to `/var/spool/arifos/dream-proposals/qwen/<cycle-id>.jsonl` (POSIX rename pattern).
5. Print a confirmation message with the proposal_id and inbox path.
6. Do NOT call arif_judge directly — that is the coordinator's job (avoids blocking user session and avoids coupling proposal to verdict).

## Failure modes (handled in body)

- Kernel cold boot (port 8088 down) → still emit proposal to spool; coordinator retries on next cron.
- Malformed jsonl → coordinator moves bad lines to `/var/spool/arifos/dream-proposals/_quarantine/`.
- Rapid-fire invocation → per-invocation cycle-id ensures distinct files.
- Concurrent sessions → per-session cycle-id (uses `arif_init` session_id if present).

## Frontmatter (canonical)

```yaml
---
description: Emit a dream_proposal.jsonl record to the federation inbox (/var/spool/arifos/dream-proposals/) — agent-local memory consolidation proposal. Async; kernel ingests nightly. Use when consolidating a session's worth of work into canon candidates.
---
```

## Discovery

Qwen scans `/root/.qwen/commands/*.md`, parses frontmatter for `description`, registers `/<basename>` as slash command. No `id`, `version`, `autonomy_tier`, or `arguments[]` in current `.md` form (legacy `.toml` form is deprecated).

## Implementation path

- **File:** `/root/.qwen/commands/dream.md`
- **No bash hook needed** for v1. Markdown body alone instructs the session to write the jsonl. Add bash hook only if pre/post-validation needed.
- **Optional backup hook:** `/root/.qwen/hooks/dream-validate.sh` — validates every jsonl write before spool commit (PostToolUse pattern, matches musyawarah.md pattern).

## Out of scope for v1

- Synchronous `arif_judge` call from `/dream` (would block user; deferred)
- OpenClaw ingestion path (binary not on PATH)
- Cross-warga recombination (G4 deferred per Qwen memory doctrine)

## Coordination with consolidate.py

The nightly `/root/AAA/dream_engine/dreams/consolidate.py` cron (via `arif-dream.service`) will be extended with a new `scan_federation_inbox()` pass that:
1. Globs `/var/spool/arifos/dream-proposals/{qwen,opencode}/*.jsonl`
2. For each file, validates against `dream_proposal.schema.json`
3. Bad lines → `/var/spool/arifos/dream-proposals/_quarantine/` with annotation
4. Valid proposals → call `arif_judge(mode='record', ack_irreversible=False)` for reversibility_grade ≥ C
5. Insert into `memory_records` with `proposal_id` idempotency check
6. Rename processed file to `.processed-<ts>`
