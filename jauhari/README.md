# JAUAHARI — Calibration Ledger + Atrophy Scheduler

> **Status:** LIVE (Lane B, T1) · Forged 2026-09-16 by 333-AGI
> **Closes:** UNCODED-EUREKA-REGISTRY-2026-09-16 items #1 and #2 — the confirmed prerequisite pair.
> **Doctrine:** `/root/AAA/instructions/jauhari-intelligence-doctrine.md` §VIII — *"jauhari are made by the loop… approval card must remain periodic training, not emergency brake alone."*

## What this measures

The doctrine's own success criterion, until now unmeasured: **does sovereign judgment track reality better over time?**

- `calibration-ledger.jsonl` — every sovereign challenge of a machine claim (falsified / upheld / qualified), with later reality outcomes and Brier scores on machine confidence.
- `gem-candidate.json` — the atrophy scheduler's current pick: the next unchallenged, consequence-bearing machine action, surfaced for an *unasked* sovereign drill.

## Usage

```bash
# record a challenge the moment Arif attacks a machine claim
python3 /root/scripts/jauhari_calibration.py log \
  --claim "scar-teeth 65% confidence" --source <seal/receipt id> \
  --machine-verdict "supported" --confidence 0.65 \
  --sovereign-verdict falsified --session <SEAL-id>

# attach reality's verdict later → Brier computed
python3 /root/scripts/jauhari_calibration.py resolve \
  --event-id JCAL-... --outcome "claim withdrawn, correction sealed" --machine-was wrong

# calibration + atrophy status
python3 /root/scripts/jauhari_calibration.py report

# pick next drill target
python3 /root/scripts/jauhari_calibration.py gem
```

## Cadence (documented, NOT installed)

Cron registration is T3-gated (F1: never mutate crontabs without 888_HOLD).
Intended line, pending ratification:

```cron
0 9 * * 1  python3 /root/scripts/jauhari_calibration.py gem   # weekly drill pick, MYT Monday
```

## Seeded history

Three challenges from the doctrine's empirical anchor night (2026-09-07, session
SEAL-ff45077c07894615, documented in sealed doctrine appendix — OBS):
FLAME-stale catch, scar-teeth 65%, "is this true". Scar-teeth carries the first
resolved Brier: (0.65 − 0)² = **0.4225** — the machine was confident where it
should not have been, and the sovereign caught it. That number is the entire
argument for this ledger.

## Consumers (planned)

- `report` output → person-card operational model (PrimaryThreat: jauhari atrophy)
- gem-candidate → session-start surfaces / `now` pane (wiring pending)
- resolved Briers → tuning substrate for conformal HOLD (registry item #4)

DITEMPA BUKAN DIBERI ⚒️
