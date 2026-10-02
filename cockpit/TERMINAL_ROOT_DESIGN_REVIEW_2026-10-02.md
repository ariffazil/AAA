# TERMINAL ROOT DESIGN REVIEW — 2026-10-02 (FI-008, session SEAL-e4afa0df3ca94a2c)
Scope: /root/AAA/cockpit/display-hud.sh + generate-hud-state.sh as rendered at login (ROOT surface).
Canon reference: AAA_APEX_ZEN_INIT_TO_SEAL v0.1 §Attention Conservation (ROOT return = BURNING / WAITING / SOURCE≠RUNTIME / FRESHNESS / LAST SEAL).

## 0. Stale-screenshot note
Arif's paste = 23:26Z render. The 07:41 bounded repair (other lane) already fixed:
literal \033 leak · stray "0" · import=# · empty mission line. Do not re-report those.

## 1. BROKEN-BUT-WIRED (data exists, HUD shows ?)
- brier=? — generator line 74 reads `.brier`; calibration.json has `mean_brier` (=0.1978, n=10). One-key fix.
- WELL=? — generator reads /root/AAA/cockpit/well.json which DOES NOT EXIST (ghost source). WELL telemetry lives in WELL organ machine_state.json (cron /proc collector). Rewire source.
- STATE "FRESH age=0s" is render-freshness masking NEXT staleness: execution-path-next.json mtime 06:24 (1.5h+ old) but panel implies current. Freshness must be per-source. Honesty bug, not cosmetic.

## 2. MISSING vs canonical ROOT lines (the contract the machine itself ratified)
- LAST SEAL — absent entirely. One line: last consequential act + verdict + hash/ref. Status board ≠ consequence ledger without it.
- BURNING — absent. One item needing attention, else "none".
- WAITING + age — "held=7" has no ages. Canon: oldest unresolved sovereign decision + age.
- SOURCE≠RUNTIME — drift exists inside [2] but not as the named scannable line.

## 3. MISSING ORGANS (all @-mentioned by sovereign, none surfaced)
- arifFlow FQ / APEX vector: G=0.4134 PATHOLOGICAL · W3=0.7439 CAUTION · FQ=1.02 · hermes-asi STUCK · chron actor HELD · primary_pathology=GOVERNANCE_COLLAPSE. Federation heartbeat invisible. Source: :7073/health (verified live, one curl + 3 jq keys).
- WEALTH / attention denominator: canon forbids AttentionReturn=∞ when attention=0; HumanLeverage needs both numerator and denominator. No cost/attention line exists.
- HERMES human line: carry_forward.human_state (last_seen, current_focus, energy) — one line, the machine's picture of the human it serves.
- leases=0 rendered as neutral while agents>0: after RED-08 (concurrent writer, zero locks) this number is a warning, not a green. Interpret it.

## 4. MINIMAL CHANGE SET (add 3 lines, fix 2 keys, interpret 1 number — remove nothing)
1. `LAST SEAL` line: read newest vault999/mission receipt → `LAST SEAL 888=HOLD · apex-zen RBG · trc-d3a4252a · 08:00MYT`.
2. `BURNING` + `WAITING age=` lines (generator already holds held[] items; add age calc).
3. Fold FQ/G/W3 into existing [4] JUDGMENT segment (no new panel): `G=0.41🔴 W3=0.74🟡 FQ=1.02✓ path=GOVERNANCE_COLLAPSE`.
4. `chron_brier` key `.brier`→`.mean_brier`; WELL source → machine_state.json vitality fields.
5. `STATE` freshness per-source: NEXT panel shows its own age (epn_age=1h37m) instead of inheriting render age.
6. `leases=0 ⚠no-lock` when agents>0.
Later (not now): attention/cost line, HERMES human line.

## 5. What the HUD would say RIGHT NOW if §4 landed
BURNING   G=0.41 PATHOLOGICAL · chron actor HELD (FQ=0.00) · GOVERNANCE_COLLAPSE
WAITING   v0.1.1 ratification binary (sha 7fc8e1d9) age≈45m · staged shadow-wire 9 artifacts
LAST SEAL none unsealed · 999 RECORD HOLD trc-d3a4252a · 888 HOLD trc-deb80924
SOURCE≠RUNTIME  hook contract declares 5-harness wiring; Kimi has 0 registrations

## 6. Constraints
- HUD owned by parallel lane until 07:41; repairs explicitly "dilapur, TIDAK dibina — ikut perintah" (report-only per order). No mutations performed by this review.
- Anti-bangang: every cell MEASURED or honestly "—" — a ? is an unwired contract, and panels that show ? train the human eye to ignore the panel.
