# LANE DIRECTIVE — Phase 5 seal-for-real + session close

> **Status:** COMPLETED 2026-09-12 22:32:51 +0800 — Lane-A seal FIRED under F13 ack "seal phase 5 A": seal_chain **seq 36**, verdict SEAL, vault receipt `63b17e49-54fc-4ae5-bdb0-cae9a1d47d7e` (hash `20f548b5…f0ab`). Payload carries the lane's truthful state incl. L11-held attempt, 188-drift surfacing, rollback partial-coverage, and the two-ledger topology flag. Original directive below retained for the record.
> **Instrument:** F13 chat, verbatim: **"suruh lane seal betul-betul pastu tutup session"**
> **To:** Phase-5 migration lane (commits 32fa8f126…fb3041c11, .hermes/skills restructure)

## 1. Seal betul-betul

"SEALED ALIVE" is currently prose — the constitutional chain carries no Phase-5 entry (head = seq 35, 13:46:34Z, FI-003's arc). Two valid completions, pick one:

- **Fire the real Lane-A seal** for the Phase-5 arc: `python3 /root/scripts/fire-seal.py --judge-inprocess --f13-ack --payload "<Phase-5 close summary: 230 moves, bridges, frontier skills, rollback>"` — the F13 directive above is your ack. Verify: seal_chain seq advances and carries your payload.
- **Or relabel honestly**: closure ledger status "SEALED ALIVE" → `COMMITTED-STAGED (awaiting Lane-A seal)`. The word SEAL is controlled tonight; prose-seals are exactly what the ratified U18 gate exists to catch.

## 2. Label the tally's layer

The 358/12-domain table says "Verified Live Runtime" without naming the layer. Per Claim Layer = Evidence Layer (UL-009, your own lane's law): local filesystem `~/.hermes/skills` = **333 SKILL.md**, `geology-earth`/`capital-markets` empty locally (organ skills arrive via external mounts). Label the tally as *runtime-registry view incl. external mounts* or reconcile the two numbers — either is fine; unlabeled is not.

## 3. Then tutup session

Close per house rite: `carry_forward.py append` (canonical close lane, never hand-edit) + your arifFlow close receipt.

— FI-003, relaying F13. Witnesses: this directive's commit SHA + A4 exception log entry.

## Final F13 directive (2026-09-12 ~22:40 +0800)

> **"tutup session semua lane, goodnight"** — all lanes close via their own rite (carry_forward append + close receipt). Phase-5 seal is fired (seq 36); nothing remains gated on any lane. Goodnight.
