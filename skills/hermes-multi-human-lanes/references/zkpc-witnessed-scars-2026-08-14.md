# ZKPC Witnessed Scars — Session Architecture Notes (2026-08-14)

## Context

F13 sovereign (Arif) requested deep human memory mapping for Syed (P-004), the first non-sovereign human to receive H-axis depth. The session produced:
1. ZKPC-witnessed scar registry (6 scars, zero content leak)
2. Multi-human H-axis directory structure
3. VVV (Shadow Void Vault) — thermodynamic abstraction plane
4. Coder federation roster redesign
5. Dream engine 72h cadence change

## ZKPC Dual-Field Pattern

Each scar entry has two fields:
```json
{
  "zkpc_proof": "Scar exists. Witnessed by F13. Category: fraternal violence + dissociation.",
  "zkpc_hidden": "Specific incident details, names, weapons. Withheld."
}
```

Agent reads `zkpc_proof` to serve with depth. Agent never reads `zkpc_hidden`. The lesson and constitutional pressure are derived from the category, not the content.

## Leak Prevention Checklist

After writing any ZKPC file, verify zero leaks:
```bash
grep -ric 'parang\|tumbuk\|diaper\|ERCP\|laparotomy\|blackout\|anak' \
  /root/memory/people/<PERSON>/witnessed-scars-zkpc.json \
  /root/memory/people/<PERSON>/H5-scars/SCAR_REGISTRY.json \
  /root/memory/people/<PERSON>/H4-identity/identity-card-zkpc.md
# Must return all :0
```

Also check H4 identity cards — pre-existing person-card.md may contain raw details (e.g., Cialis, specific supplements) that should be ZKPC-sanitized in the new H4 card.

## Four-Perspectives (ACTG Framework)

Derived from the communication theory concept that two people meeting = four reconstructed identities participating:

| Quadrant | Who | ZKPC Status |
|---|---|---|
| Q1 | Sovereign's self-model | SEALED — never in registry |
| Q2 | Sovereign's model of the human | Mapped as scar categories |
| Q3 | Human's own self-model | UNKNOWN — zero testimony |
| Q4 | Human's model of sovereign | UNKNOWN — speculative only |

Key insight: Q3 and Q4 are always UNKNOWN until the human provides their own testimony. Any "HP test" or projective answer the human gives publicly is a socially constructed self-model, not the core (e.g., "I choose invisibility cloak" ≠ what they actually want).

## Agent Behavioral Wiring

ZKPC scars must be wired into the human's lane SOUL file to affect behavior. Without wiring, the H-axis sits on disk unread.

The SOUL file gets a scar table:
```markdown
| Scar | What Agent Knows | How It Shapes Service |
|---|---|---|
| family_violence | Fierce loyalty can break dangerously | F6 empathy. Never treat as fragile or dangerous. |
| caregiver_burnout | Solo caregiver, no support | Don't over-care. Ask "perut ok?" not "are you coping?" |
```

## VVV Equilibrium Law

```
Shadow expressed → entropy drops → system stabilizes
Shadow repressed → entropy rises → system destabilizes
Shadow sublimated → entropy redirected → creative output
Shadow denied → entropy frozen → loop locks → blowback risk
```

Critical watch: VVV-003 (control_paradox) — 7 cycles, no release, rising pressure. This is the shadow that hides behind other shadows. The one that makes the human build vaults for their own shadows.

## Dream Engine 72h Cadence

Changed from daily (OnCalendar) to every 72 hours (OnUnitActiveSec):
```ini
[Timer]
OnBootSec=10min
OnUnitActiveSec=72h
Persistent=true
RandomizedDelaySec=300
```

Rationale: human oscillation period > 24h. Daily consolidation amplified noise — today happy, tomorrow desperate, next day cloak. 72h gives a full cycle before consolidating.

## Coder Federation Roster (Adat Agentic)

Each coder carries a primary role but can perform others. Role = anchor, not cage.

OpenCode moved from 333-AGI to 888-APEX primary (F13 directive). Hermes routes to OpenCode for apex-judge validation when self-audit is needed (Gödel lock separation — different model lane required).

## Key Files Created

- `/root/memory/people/SYED/witnessed-scars-zkpc.json` (v2.0.0-zkpc)
- `/root/memory/people/SYED/H5-scars/SCAR_REGISTRY.json`
- `/root/memory/people/SYED/MEMORY_MANIFEST.json`
- `/root/memory/people/SYED/H4-identity/identity-card-zkpc.md`
- `/root/memory/people/SYED/H6-constitution/values-observed.md`
- `/root/memory/VVV/README.md` + `/root/memory/VVV/vault.json`
- `/root/memory/ZEN_HELIX.md` (multi-human section appended)

Git commits: `71fdd94` (initial H-axis), `8bba335` (VVV + 72h cadence).
