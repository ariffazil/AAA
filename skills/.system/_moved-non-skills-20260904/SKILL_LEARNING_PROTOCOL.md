# SKILL LEARNING PROTOCOL — Auto-Update Contract (v1.0)

> Forged 2026-09-04 by 333-AGI (session SEAL-83defc585b5a4296), ratified direction 888-APEX SEAL.
> Doctrine: **When any agent learns, the federation learns. Once. Everywhere. Instantly.**

## Flow

```
Agent learns (scar, eureka, failed prediction, new technique)
   |
   v
drops learning atom -> /root/AAA/skills/.learning/queue/<ISOts>_<agent>_<skill>.json
   |
   v
cron skill-learn-ingest.py (hourly)  -- F2 gate: evidence required
   |
   v
canonical SKILL.md gains '## Lessons (auto)' entry + patch version bump
   |
   v
ALL agents see it instantly (mount homes read canonical directly)
```

## Learning atom schema (STRICT)

```json
{
  "skill_id": "geox-prospect-evaluation",
  "agent": "kimi-code/FI-008",
  "lesson": "POS decomposition must cite its chance-factor source; hand-set POS without factors fails review.",
  "evidence": "session SEAL-x; geox_prospect verdict=compute rejected POS=0.25 without factor breakdown",
  "ts": "2026-09-04T02:00:00Z"
}
```

## Rules

1. **F2 TRUTH** — no evidence, no merge. Atoms without evidence rot in queue as .rejected.
2. **F4 CLARITY** — Lessons section is append-only. Never rewrite history; supersede with a newer lesson.
3. **F7 HUMILITY** — lessons are observations, not laws. No "always/never" inflation.
4. **Ownership** — the atom targets a SKILL, never an agent. owner_org unchanged.
5. **Idempotent** — duplicate lesson hashes are skipped, not double-appended.
6. **Human override** — Arif (F13) may purge any lesson; ledger records the purge.

## Invocation by agents

Any AAA warga agent appends this to its session-close ritual:

```bash
cat > /root/AAA/skills/.learning/queue/$(date -u +%Y%m%dT%H%M%SZ)_<agent>_<skill>.json <<'EOF'
{ ...atom... }
EOF
```

The dream-engine (AGI-dream-engine skill) and wisdom-scar-session-audit now write into this queue.
