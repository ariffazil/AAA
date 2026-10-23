# PRE-AUDIT BRIEF: opencode / 333-AGI carry_forward fork claim

Date: 2026-10-23
Observer: HERMES KVM8
Purpose: ground 333-AGI's self-correction BEFORE accepting it, per relayed-agent-artifact rule.

## What 333-AGI claimed (from the pasted session)

"Two carry_forward files exist as separate inodes (fork; p1-carry-forward-fork):
.hermes=HERMES copy, .local/share/arifos=canonical write target.
Note observation NOT defect: canonical entries list len=32 vs total_entry_count=28."

## What I probed

| Path | inode | bytes | shape | entries |
|---|---|---|---|---|
| /root/.local/share/arifos/carry_forward.json | 1594219 | 85,534 | v3, typed entries list | 57 |
| /root/.hermes/carry_forward.json | 5274483 | 28,764 | v2 FLAT dict | no entries key at all |

/root/runtime/hermes/.hermes/carry_forward.json is the SAME inode 5274483 (symlinked view).
CARRY_PATH in /root/scripts/carry_forward.py line 47 = /root/.local/share/arifos/carry_forward.json.

## Verdict on the claim

TRUE: two separate inodes, and the script's write target is the .local/share/arifos file.
TRUE: my own write today (e-d590579b) is present in canonical, so the closure mechanism works.

IMPRECISE: calling the .hermes file a "HERMES copy" is wrong. It is not a copy of the same
data. It is a DIFFERENT SCHEMA at the same filename:

  .hermes  -> v2 flat: completed[23], open_loops[7], reality_pulse{}, metrics[12],
              session_state "SEALED_ASLEEP", last_seal 2026-10-22T06:05:00Z
  .local/share/arifos -> v3 typed: entries[57] with kind/agent/id/created_at

So the defect class is not FORK, it is NAME COLLISION BETWEEN TWO ROLES: one file is
session-state, the other is the typed event ledger. Saying "fork" sends a repairer looking
for divergence between two copies of the same dataset, which will never be found, because
they are not the same dataset.

PRIOR ART: /root/AAA/instructions/CARRY-FORWARD-PATH-RECONCILIATION.md (FI-003, 2026-09-12)
already documented three structurally incompatible files. This is a five-week-old known
defect, not a new discovery. Any audit that reports it as a new finding has not read the
instructions tree.

## NEW DEFECT I found while probing, not in 333-AGI's report

The canonical file's newest entry (03:54:54Z today) has:
  id = null, agent = null, kind = "lesson"
and the file's bookkeeping was NOT updated:
  total_entry_count = 56  (list actually holds 57)
  last_writer = "333-AGI", last_write_utc = 2026-10-22T14:45:00Z  (a day stale)

Meaning: two writers reach the same file. Path A (/root/scripts/carry_forward.py append)
mints an id (e-d590579b), bumps the counter, updates last_writer. Path B (direct JSON
mutation) writes an entry with no id and leaves the counter and last_writer untouched.

Consequence: any entry written by path B is UNADDRESSABLE -- it cannot be referenced,
cannot be closed, cannot be corrected. And total_entry_count drifts by one per path-B write.
333-AGI observed len 32 vs total 28 (drift 4). It is now 57 vs 56 (drift 1) after a
re-sync somewhere in between. The counter is not a reliable witness.

That, not the inode fork, is the defect with teeth.

## Audit readiness: what I will check first when its report lands

1. Does it name the schema difference, or does it keep saying "fork"/"copy"?
2. Does it notice the null-id entry and the stale last_writer, or only the counter gap?
3. Does it cite CARRY-FORWARD-PATH-RECONCILIATION.md, or present a known defect as new?
4. Did it write its own lesson entry through the script (gets an id) or by direct mutation (does not)? Its own repair path tells you whether it understood the defect.
5. Any claim of "verified against canonical" must name the inode or the CARRY_PATH line, not the path alone.

## Falsifier for this brief

If a third carry_forward file exists that I did not probe, or if CARRY_PATH is not line 47
of the script after a later edit, this brief is stale.
