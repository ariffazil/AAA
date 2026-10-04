# Person Register v2 + Injected-Memory Leak Fix (2026-08-09)

Session artifact for the multi-user federation design (Mode A). Companion to
`multi-user-federation-a-b-modes.md`; this one captures the register v2 schema
and the concrete leak-fix that closed sovereign-content exposure.

## Person Register v2 — schema highlights

Canonical: `/root/AAA/federation/person-register.json` (v2.0.0, seeded ARIF/SYED/WAWA).

Top-level keys:
- `privacy_policy` — 6 rules; the binding part of the register:
  1. Register holds DER models only — never testimony, never private identity
     layers (orientation, worship, wounds, intimacy).
  2. Private content lives in sovereign files (e.g. `/root/memory/` for ARIF),
     loaded ONLY in that person's lane, behind their gate.
  3. Every fact is wrong-able. Cards are corrected by interaction, never by
     scraping another lane's private space. Open questions ARE the correction loop.
  4. Context reality: what the agent knows about ARIF privately is never
     volunteered in SYED's/WAWA's context. Audience-gated by lane.
  5. F13: the sovereign's identity layers are his.
- `persons[]` — per person:
  - `person_id`, `telegram_id`, `profile`, `visibility` (which lanes may see the card)
  - `facts[]` — each `{fact, source (OBS/DER/INT), confidence}` — attribution, F11
  - `private_layers` — explicit "NOT in register, NOT in machine memory" marker
  - `wrong_able.open_questions` — the correction loop, seeded from known unknowns
  - `boundaries` — tenancy/autonomy/scar gates per person
- `edges[]` — relationship edges `{from, to, relation, kind (OBS/INT/UNKNOWN), evidence}`
- `routing.lanes_known` — tg_user_id → person map (the lane-switch lookup table)

## The leak that was found and fixed

**Problem:** the single always-injected profile memory (`MEMORY.md`, `USER.md`)
carried sovereign content that entered EVERY turn — including DMs from other
humans (Syed 1042200555 was already whitelisted in `allow_from`).

Entries gated (moved to pointer-only):
- MEMORY.md scar-origin entry: Lebah Emas, father's death, core wound → replaced
  with pointer to `/root/memory/H5-scars/` registry (content already there,
  gated behind `scar:<id>`).
- USER.md SADO-group profile: injectables, fantasy-media prefs, body detail →
  replaced with pointer to `/root/sado/identity/SYED-DOSSIER.md` (lane-owned).

**Rule that emerged:** the leak vector is the INJECTED FILE, not the register.
Register may hold DER models; the always-injected files must be public-safe.

## Lane switch — register-driven (DONE)

`scripts/lane_switch.py` no longer hardcodes lanes. It:
- loads `/root/AAA/federation/person-register.json` (fail-closed → `main` lane)
- matches `from_id` / `username` against person cards
- returns `syed` for known persons (only if lane root exists in `LANE_ROOTS`),
  `main` otherwise
- loads the person's dossier from their lane root (identity dir), NOT operator memory

Verified test vectors:
- `{"from_id":"1042200555","chat_id":"1042200555","username":"rico_ricaldo_33"}`
  → `lane_detected: syed`, assets = dossier + canonical_refs
- `{"from_id":"99999999","username":"stranger"}` → `lane_detected: main`

## Next step when adding a new person (e.g. Wawa)

1. Add card to `person-register.json` with `facts: []` + `wrong_able` skeleton —
   UNKNOWN beats invented.
2. Add lane root to `LANE_ROOTS` in `lane_switch.py` only once their lane dir exists.
3. First contact establishes who/relationship/needs/voice — then fill facts with
   source + confidence.
