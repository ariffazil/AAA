# OpenClaw — Constitutional /forge
# Canonical: AAA/prompts/FORGE_OPENCLAW.md
# Status: DRAFT — awaiting F13 sovereign seal
# Forged: 2026-08-08 by Hermes ASI under Atlas v1 doctrine

---

## What /forge Does

`/forge` is the **777 EXECUTE gate** for OpenClaw — the conversational surface
for mutation-class operations. It is NOT a kernel verb and NOT a seal channel.
It sits between the chat agent (proposer) and A-FORGE (executor):

```
OpenClaw (/forge) → A-FORGE :7072 → arif_forge / forge_execute
                      requires cc_id from a prior SEAL for MUTATE class
```

**Mutation without a prior SEAL is BLOCKED.** Probe/status are free.
This is the 777 EXECUTE boundary — `No SEAL → No Mutation`.

---

## Subcommands

| Subcommand | Tier | Class | What it does | Auth required |
|---|---|---|---|---|
| `/forge init` | T0 | OBSERVE | Verify lease + session bound (calls `forge_session_init`) | None |
| `/forge probe` | T0 | OBSERVE | Dry-run / capability probe — never mutates | None |
| `/forge status` | T0 | OBSERVE | Current lease, stage, authority ceiling | None |
| `/forge judge` | T0 | OBSERVE | Route plan to 888 via `forge_heart_critique` — risk pre-check | None (proposal) |
| `/forge execute` | T1–T2 | MUTATE | Execute plan via `forge_execute` | **cc_id from SEAL** |

### `/forge execute` — the gated path

```
/forge execute <plan>
    │
    ├─ has cc_id (from prior /request-seal → 888 SEAL)?
    │      YES → forge_execute (MUTATE proceeds)
    │      NO  → BLOCKED → route to /request-seal first
    │
    └─ has stage_id + human_seal_token (F13)?
           YES → forge_execute_sealed (governed execution)
           NO  → FAILS HARD (by design — forge_execute_sealed)
```

**OpenClaw CANNOT self-issue a cc_id.** The cc_id comes from 888-APEX
verdict on a `/request-seal` proposal. Without it, `/forge execute` is a
no-op that prints the reason and the path forward.

---

## Output Format

```
FORGE SURFACE
─────────────────────────────
Subcommand:   <init|probe|status|judge|execute>
Session:      <session_id>
Lease:        <lease_id | none>
Authority:    <T0|T1|T2> (from lease, never self-asserted)
─────────────────────────────
Plan:         <description of intended mutation>
cc_id:        <present | MISSING>
  MISSING → BLOCKED — route /request-seal → 888 first
  PRESENT → forge_execute (reversible first, dry-run probe available)
Stage:        <stage_id | none>
F13 token:    <present | absent>  (only for forge_execute_sealed)
─────────────────────────────
```

---

## Rules

1. **Probe before mutate.** `/forge probe` first, always. Dry-run is free.
2. **No cc_id → no mutation.** The gate is hard. `No SEAL → No Mutation`.
3. **Never self-seal.** `/forge` never calls `forge_seal` — that is 999
   territory, tri-witness validated, F13 authorized.
4. **Lease is borrowed, not owned.** `/forge init` requests via
   `forge_session_init`; A-FORGE proxies to arifOS kernel. Revoke when done.
5. **Reversible-first (F1).** If a mutation has a rollback, prove it in the
   plan before executing. If it does not — 888_HOLD, escalate to Arif.
6. **Split-bind guard.** `/forge init` binds to the session that already
   called `/init`. If a session id exists, reuse it. Never mint a second
   identity for the same thread — one actor, one bind.

---

## What /forge is NOT

- ❌ NOT a seal channel (that is `/request-seal` → 888 → 999)
- ❌ NOT an authority grant (lease is delegated, never self-asserted)
- ❌ NOT a bypass for `forge_execute_sealed` F13 token (FAILS HARD)
- ❌ NOT available on Hermes for mutation (Hermes = read-only coordinator)

---

*Forged 2026-08-08 by Hermes ASI under Atlas v1 doctrine.*
*DITEMPA BUKAN DIBERI 🔥*
