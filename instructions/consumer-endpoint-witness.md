---
name: consumer-endpoint-witness
status: F13_RATIFIED_ORDER (2026-09-30) — sovereign: "aku sahkan semuanya" (five-mission order)
spectrum: 000-999 (verification discipline, all lanes)
floors: F1, F2, F4, F11
companion: state-transition-discipline.md · source-type-promotion-gate.md · probe-before-panic.md
---

# Consumer-Endpoint Witness — three rules born from the 2026-09-30 decoy incident

**Incident (OBS):** a triadic-snapshot consumer inherited a code default pointing at a pytest
fixture (`/root/WELL/state.json`, sentinel `well_score=100`, `timestamp=2026-04-30`) while the
live organ truth sat at `/var/lib/well/state.json` (89.8, FRESH). Every producer looked healthy;
the consumer was reading a decoy. Caught by external check, root-fixed, then compiled into the
three rules below so the class — not just the instance — is dead.

## RULE 1 — Consumer-endpoint rule

**Nothing is DONE until verified at the endpoint the real consumer reads** — the file, HTTP
endpoint, log line, or DB row the downstream actually resolves — never at the producer, never at
the emitter, never at "the code is merged". `PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ CONSUMED`
(state-transition-discipline). A claim of X must carry the pointer where X was observed at the
consumer side; a claim without a pointer is UNVERIFIABLE and must be labelled so.

Corollary (the decoy test): verify **which path the consumer resolves**, including code defaults,
env overrides, symlink targets, and unit drop-ins. A healthy producer feeding a decoyed consumer
is still a decoyed system.

## RULE 2 — Reversibility rule

**Snapshot before any delete/destructive mutation, or label the action IRREVERSIBLE.**
Accepted snapshots: `.bak-<date>-<actor>` sibling, git commit, tar to a named archive path.
No snapshot → the action is classified IRREVERSIBLE and follows the T3/888 gate — no silent
"it was probably fine" deletes. Receipts are never edited; stale receipt claims get a dated
supersedes note, not a rewrite.

## RULE 3 — FRAME field of view (path / consumption / claim witness)

FRAME sees **paths, not just processes** — evidence only, never a verdict:

| Witness | Question | Live endpoint |
|---|---|---|
| PATH | Which file does each registered consumer actually read (code default + env + unit)? Any decoy default or live decoy sentinel? | `GET :18085/frame/witness/paths` |
| CONSUMPTION | Does organ truth agree with the canonical surface and the digest? A disagreement's headline is the disagreement itself. | `GET :18085/frame/witness/consumption` |
| CLAIM | Is a stated claim VERIFIED / CONTRADICTED / UNVERIFIABLE against reachable substrate? (witness-reach boundary ≠ falsification) | `GET :18085/frame/witness/claims` |

Implementation: `/root/AAA/federation/frame/src/frame_organ/witness.py` (commit b6eba2ee).
Portable standalone (runs without arifOS, stdlib-only, ships the decoy-incident selftest):
`/root/consumer-witness/`.

## Taxonomy note

Claim/label taxonomy on the human plane maps to the ONE canonical taxonomy in
`source-type-promotion-gate.md` §Tri-label mapping (USER-STATED→USER_STATED,
DERIVED→AGENT_INFERRED, INVENTED→no class; fabrication is an F2 violation). This file owns
no vocabulary of its own.

DITEMPA BUKAN DIBERI ⚒️
