# CREDIT-PACE — Standing Rule (F13-ratified 2026-09-07)

> **Ratification (Arif, verbatim parameters):** "Lock the exhaustion ceiling to ONE reconciled number (cycle-start + last-7-day actual burn, EVIDENCE-tagged). Then run pace-watch autonomously against it — ping me ONLY on exception (projected >90% or <70% at renewal). No manual MiMo pacing reaches me again."

## 1. The TWO locked quantities (never conflate them again)

| Quantity | Definition | Value @ 2026-09-07 | Tag |
|---|---|---|---|
| **CEILING** (can-burn) | `remaining_credits / days_to_renewal` — a tautological budget line, recomputed every run | **2.79B/day** | DERIVED from EVIDENCE anchors |
| **PACE** (is-burning) | Δused / Δdays across the two most recent EVIDENCE anchors | **2.42B/day** (14.65-day window) | INTERPRET — true last-7-day burn is NOT observable (no usage API; dashboard is Arif-only). Refreshed on each dashboard paste. |

**EVIDENCE anchors** (`/var/lib/mimo-doctor/anchors.jsonl`):
- `2026-08-23 12:00Z approx` → 16.65B used (dashboard read, memory-anchored)
- `2026-09-07 03:30Z approx` → 52,086,903,022 used (Arif's dashboard paste)
- Cycle-start: INFERRED 2026-08-17/18 ±1d (auto-renew backward; NOT dashboard-stamped). Renewal: `2026-09-17T23:59:59Z` (epoch 1789689599 — generated via `date -u -d`, never hand-computed).

**First state (2026-09-07):** projected **95.1%** of 82B at renewal → **HIGH band** → one exception ping sent at watch birth. Then silence unless a band boundary is crossed.

## 2. Enforcement mechanics
- **Runner:** `mimo-doctor` (systemd timer 06:00 + 22:00 MYT; PAYG-liveness mode — zero token-plan spend).
- **Math:** local python inside `pace_watch()`; every run appends `/var/lib/mimo-doctor/pace.log.jsonl` (full audit trail) and updates `pace-state.json`.
- **Bands:** HIGH = projected >90% · MID = 70–90% · LOW = <70%. **Ping ONLY on band TRANSITION** (entry counts; steady-state = silence).
- **Ping path:** `openclaw-send-telegram` → `forge-send.sh` → @arifOS_bot → AAA group. (This wrapper was created 2026-09-07 — the original reference was a PHANTOM: doctor failure alerts silently no-op'd since 2026-06-15. Now revived for both alert paths.)
- **Anchor protocol:** dashboard paste from Arif = EVIDENCE → `mimo-doctor --anchor <used_credits>` appends it. Agent math = INTERPRET, always labeled.
- **Action guidance baked into pings:** HIGH → "throttle MiMo p12 rules or accept" (demote p12→p8 in federation-models.json); LOW → "shift more load onto MiMo".

## 3. Scars encoded in this rule
1. **Unit slip** — "77.8 billions" read as "78%" (2026-09-07 morning). Cure: always restate landing as BOTH % and absolute B.
2. **Pace↔ceiling conflation** — three "drifting ceilings" were two different quantities. Cure: the two-quantity table above.
3. **Hand-computed epochs** — Aug-23 anchor landed 7 weeks early → false LOW band (silent exhaustion risk!). Cure: epochs only via `date -u -d ... +%s`.
4. **Phantom ping path** — a sender that never existed. Cure: wrapper + failure line in doctor output (`PACE: telegram send FAILED`) so transport death is never silent.

## 4. Success criterion
Arif never manually checks MiMo pacing again. The watch speaks only on band transitions; its log is the audit trail; its anchors are only his pastes.
