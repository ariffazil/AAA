# SKILLS_INDEX.md — AAA
## AAAA Skill Registry · Three-Skill Flow

> **Canonical home:** `AAA/SKILLS_INDEX.md`
> **Version:** v2026.05.02.1
> **Authority:** Muhammad Arif bin Fazil

***

## The Three Skills

| Skill ID | Mindset | Primary Repo | Role |
|----------|---------|-------------|------|
| `aaa-agent-registrar` | Legal | `/root/AAA` | Identity verification, contract enforcement, routing compliance |
| `arifos-constitutional-clerk` | Constitutional | `/root/arifOS` | F1–F13 translation, 000–999 pipeline, VAULT999 sealing |
| `aforge-metabolic-operator` | Security | `/root/A-FORGE` | Scope enforcement, reversibility (F1), metabolic observability |

***

## The AAAA Flow

Every command passes through all three skills in strict sequence. No skill may be skipped. No skill may self-approve.

```
HUMAN COMMAND
    ↓
[1] aaa-agent-registrar
    "Who is asking? Identity verified? Layer metadata correct? Routing valid?"
    ↓ YES
[2] arifos-constitutional-clerk
    "What does the Law say? 000–999 pipeline run? Floor-compliant plan sealed?"
    ↓ YES (Constitutional seal + VAULT999 pre-record)
[3] aforge-metabolic-operator
    "Scope valid? Rollback generated? Pulse green? Execute."
    ↓
VAULT999 (append-only execution record)
    ↓
999 SEAL — Telemetry emitted by constitutional clerk
```

**At any step:** if the answer is NO → **888 HOLD. Emit reason. Await Arif.**

***

## Example: "Upgrade the GEOX database"

| Step | Skill | Internal Logic | Result |
|------|-------|---------------|--------|
| 1 | `aaa-agent-registrar` | Who is asking? Does agent carry correct tier? Does `layer_awareness` declare `target_repo: GEOX`? Does `reversibility: true`? | Identity verified. Metadata valid. Route confirmed. |
| 2 | `arifos-constitutional-clerk` | F1: reversibility required — migration must have rollback. F11: seal required. F3: GEOX witness must be called. 333 EXPLORE: ≥3 migration paths generated. 888 JUDGE: rollback path declared. | Constitutional plan sealed. VAULT999 pre-record created. |
| 3 | `aforge-metabolic-operator` | Check `a-forge-permission-mapping.md`: agent has `write_scoped` for GEOX db. Generate rollback SQL. Store to `ops/rollbacks/`. Check pulse: GREEN. Execute migration. | Executed. Post-state verified. Telemetry logged. |

***

## Skill Inheritance Rule

All future agents operating in the arifOS federation **inherit these three skills by default**. An agent that does not honour this flow is not a federated agent — it is an orphan process.

New agents must declare in `agent-card.json`:

```json
{
  "skills": [
    "aaa-agent-registrar",
    "arifos-constitutional-clerk",
    "aforge-metabolic-operator"
  ]
}
```

***

## Skill Files Location

```
AAA/       → SKILLS.md       (aaa-agent-registrar)
arifOS/    → SKILLS.md       (arifos-constitutional-clerk)
A-FORGE/   → SKILLS.md       (aforge-metabolic-operator)
AAA/       → SKILLS_INDEX.md (this file — root registry)
```

***

```json
{
  "epoch":      "2026-05-02T22:40:00+08:00",
  "artifact":   "SKILLS_INDEX",
  "version":    "v2026.05.02.1",
  "authority":  "Muhammad Arif bin Fazil",
  "verdict":    "SEALED",
  "witness":    { "human": 1, "ai": 1, "earth": 0 },
  "confidence": 0.96
}
```

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
