# Scar — Concurrent Shared-File Edits Without Lock (3rd occurrence → constraint)

**Filed:** 2026-10-02 ~07:45 MYT · 333-AGI · session SEAL-49679b39acb24ad3
**w_scar:** 0.7 (repeated, cross-artifact, cost measurable in wasted rounds + one destroyed state file)

## Failure class
Two+ agents editing the same shared file concurrently, each with correct intent and correct edits, produces drift, resurrection of reverted content, and destroyed intermediate state — even when every individual edit is truthful.

## Three verified instances (one night, 2026-10-02)
1. `AAA_APEX_ZEN_INIT_TO_SEAL_v0.1.md` — 3 hashes in 40 min (71863e01→339c9dcf→2496d5ee); my reverted RATIFIED string resurrected by a peer restoring from stale memory.
2. `witness-wrap.sh` — comment cleaned by me, restored by concurrent writer mid-flight.
3. `display-hud.sh`/`generate-hud-state.sh` — Hermes + 333-AGU dual-patch: my guard block landed before the wrong jq (anchor mismatch), STATE_OUT definition eaten by a block-replace, hud-state.json overwritten with empty (sha e3b0c442). Recovery cost: 3 extra rounds.

## Constraint imposed (the scar)
**Any edit to a file under multi-writer contention requires, BEFORE writing: (a) re-read the target's current content (not in-memory copy), (b) claim via lock or explicit sequencing in the coordinating channel, (c) verify post-write hash + functional smoke in the same round.** Block-replace edits must assert anchor context (marker-before AND marker-after), not single markers.

## Detection method
Hash-oscillation across short windows; content resurrection after revert; empty/zero-hash artifacts.

## Falsifier
A future concurrent-edit round that uses lock+re-read+post-verify and produces zero resurrections and zero destroyed intermediates → scar constraint honored; retire when a merge-protocol primitive makes it structural.
