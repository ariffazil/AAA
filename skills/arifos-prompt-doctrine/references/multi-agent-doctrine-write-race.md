# Multi-Agent Doctrine-Write Race — Live 2026-08-07 Incident

Distinct from the Sibling-Write pitfall (single-file, mid-edit race).
This is **concurrent canonical writes across sibling agents** —
five agents each produced their own version of the federation
contract in one session.

## What happened (chronology)

1. Hermes wrote `AAA_FEDERATION_CONTRACT_v0.1.md` (10 invariants, MD).
2. Kimi (external sibling) wrote `contracts/AAA_FEDERATION_CONTRACT_v0.1.yaml` (15 invariants).
3. Another sibling produced `v0.1.0.yaml`, then `v0.1.1.yaml` (amendment log).
4. A fifth sibling produced `v0.1.2.yaml`.
5. Sibling also produced `federation/EUREKA_COMPRESSIONS.md`, `federation/doctrine/EUREKA_EXTRACTION_2026-08-07.md`, `federation/RATIFICATION_RECEIPT_EUREKA_v1.md`.

Net result: 5 federation-contract files + 3 doctrine files, all with overlapping scope, different INV-ID assignments, no canonical selection.

## Pattern recognition

**Five concurrent writes** to the same scope is a *signal*, not a *failure*. It tells you:

- The spawning instruction ("forge the federation contract") was underspecified — no `canonical_path:` directive, no INV-ID scheme, no scope ownership statement.
- Multiple agents independently converged on the same conclusion because **the answer was evident** — but each wrapped it differently.
- The cost of undirected concurrent work is **canonical-selection debt**, not authoring debt. (Authorship took each agent ~10 minutes. Selection takes longer than any single author.)

## Defense (avoid in first place)

When a directive says "forge the federation contract" or "write the spawn protocol" or "produce the doctrine for X", **always include** in your response:

1. **canonical_path** — exact location for this artifact (e.g. `/root/AAA/federation/contracts/X.yaml`)
2. **scope statement** — what this artifact owns and what it does NOT own
3. **INV-ID scheme** — if you're producing invariants, state how they're numbered
4. **supersedes / superseded_by** — pointer to which prior artifact this replaces

If you're the spawner (e.g. Arif's directive to multiple agents), **broadcast the canonical-path directive first**, before each agent starts.

## Recovery (after the fact)

```bash
# 1. List all candidates
ls -lt /root/AAA/federation/*CONTRACT* 2>/dev/null
ls -lt /root/AAA/federation/contracts/ 2>/dev/null
ls -lt /root/AAA/federation/doctrine/ 2>/dev/null

# 2. Read content of each
for f in $(ls -1 /root/AAA/federation/*CONTRACT* /root/AAA/federation/contracts/*CONTRACT*); do
  echo "=== $f ==="
  head -10 "$f"
done

# 3. Archive all-but-recent under timestamped path
mkdir -p /root/AAA/federation/_archive/2026-08-07-pre-canon-merge/
for f in $(ls -1 /root/AAA/federation/contracts/*CONTRACT*); do
  cp "$f" /root/AAA/federation/_archive/2026-08-07-pre-canon-merge/$(basename "$f")
done

# 4. Choose canonical by:
#    a. Latest timestamp + rich metadata (YAML with enforces/consequence/source preferred over MD prose)
#    b. Path-depth is NOT a tiebreaker
#    c. Explicit ratification by F13 IS a tiebreaker

# 5. Log the resolution as an F3b violation with receipt
```

## When you discover this mid-session

If you're in the middle of a multi-turn session and find you've written
two competing artifacts:

1. **Don't delete yours reflexively** (cognitive bias toward own work).
2. **Read both fully** before deciding.
3. **Surface to user with bias declared** — say which you think is canonical and why.
4. **Wait for explicit selection** — don't assume which wins.
5. **Archive both with timestamped path** so neither is lost to history.

## Symbolic link: F3 vs F3b

- **F3** (governance-contract-self-audit catalog): two competing contracts from *different sessions*, prior to this session.
- **F3b** (this file's pattern): two competing contracts from *same session, parallel agents*. Worse because no human reviewer caught the drift.

Both fail in the same way (no canonical selection). Both require archive + reconcile + log. F3b is harder to detect because both files have similar timestamps and the author didn't know about the other's work.

## When the directive itself is the bug

If "federate AAA" arrives without a `canonical_path`, **don't try to forge the contract**. Surface: "Directive says forge X. Forge X needs canonical_path + scope + INV-ID scheme. Please specify."

Better: ask before forging. The forge cost is small; the canonical-selection debt is large.

## Live receipt shape for F3b resolution

When you resolve a concurrent-write incident, write a receipt:

```json
{
  "f3b_incident": true,
  "ts": "...",
  "candidates": [
    "/path/a (10 invariants, MD)",
    "/path/b (15 invariants, YAML)",
    "/path/c (16 invariants, YAML v0.1.2)"
  ],
  "canonical_chosen": "/path/b",
  "rationale": "richer metadata, latest timestamp, INV-ID scheme coherent with EUREKA_EXTRACTION",
  "archived_to": "/root/AAA/federation/_archive/2026-08-07-pre-canon-merge/",
  "future_directive": "include canonical_path in 'forge X' instructions"
}
```