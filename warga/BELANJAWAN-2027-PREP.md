# Belanjawan 2027 — Chron Verification Prep (2026-10-09)

**Window:** 9.5 days from 2026-09-30 → verification day 2026-10-09
**Two predictions due that day (audience=both):**

| ID | Claim | Expected | Confidence | Falsifier |
|---|---|---|---|---|
| `pred-fdb40342252b` | PETRONAS dividen to federal government ≥ RM30b for FY2027 | ≥30b | 0.6 | Announced dividen < RM30b |
| `pred-e3808eff19ee` | RON95 subsidy rationalisation announced/reaffirmed in budget speech | announced | 0.7 | Budget speech makes no mention of fuel subsidy reform |

---

## Verification day commands (run on 2026-10-09 after budget speech)

```bash
# 1. Capture observation (replace with real budget speech outcome)
mcp__chron__chron_record_verification(
  prediction_id="pred-fdb40342252b",
  observed_outcome="<actual dividen announced in Belanjawan 2027 speech, e.g. RM32b>",
  correct=True  # or False if <RM30b
)
mcp__chron__chron_record_verification(
  prediction_id="pred-e3808eff19ee",
  observed_outcome="<actual RON95 mention in speech, e.g. 'subsidi bahan api diselaraskan'>",
  correct=True  # or False if no mention
)

# 2. Then run lessons extraction
mcp__chron__chron_lessons(limit=10)

# 3. Calibration impact
mcp__chron__chron_calibration_state()
```

---

## What to look for in budget speech text

1. **Dividen PETRONAS** → search for "dividen PETRONAS", "RM30 bilion", "petroleum dividend"
   - Source: Ministry of Finance speech, Parliament Hansard
   - Backup source: MOF press release at treasury.gov.my
2. **RON95 subsidy** → search for "subsidi RON95", "subsidi bahan api", "penyelarasan subsidi"
   - Source: Belanjawan 2027 speech text
   - Backup: The Edge / Bernama coverage

---

## Audit chain reference

These are Arif-personal predictions (audience=both, principal=arif). On verification, Brier scores will update chron calibration state — this affects:
- `chron_calibration_state()` → Brier, accuracy, error distribution
- `chron_lessons()` → new CANDIDATE lessons for ratification
- Future prediction confidence calibration across all organs

## Reversibility

chron_record_verification is **append-only** — wrong verifications can be:
1. Supplemented with a contradicting verification (chron supports correction via supersedes field)
2. Voided via `chron_resolve_unverifiable` (if the question becomes meaningless)
3. Lessons are CANDIDATE until Arif F13-ratifies them — they don't change behavior until ratified

So verify-once-is-fine. If you spot an error later, the chain records both the original and the correction.

— Kimi Code / FI-008, session SEAL-031ea2c31cb04934