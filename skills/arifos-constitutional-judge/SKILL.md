---
name: arifos-constitutional-judge
id: arifos-constitutional-judge
version: 1.2.0
owner: AAA
description: >
  Real apex-judge skill. Gödel lock + strange-loop zen: doer ≠ judge lane,
  evidence-only packages, kernel arif_judge is sole effective_verdict source,
  F13 is true external for critical. FORBIDS free-text self-SEAL and same-agent
  self-audit. Default: apex-judge isolate. Option 2 A2A 888-APEX is backlog.
agent: 888-APEX
namespace: arifos
cluster: CONSTITUTION · VERDICT · ACT
risk_tier: high
autonomy_tier: T2
floor_scope: [F1, F2, F4, F7, F9, F11, F13]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# arifos-constitutional-judge (LOAD-BEARING · GÖDEL · STRANGE-LOOP ZEN)

> **Forged:** 2026-08-01 · **Zen:** 2026-08-09 (real isolate apex-judge)  
> **Doctrine:** `/root/AAA/governance/GODEL_LOCK_STRANGE_LOOP.md`  
> **Status:** Single canonical entry. DITEMPA BUKAN DIBERI.

## The problem (two layers)

1. **Free-text SEAL** — agent writes `888-APEX JUDGMENT` without `arif_judge`.
2. **Strange loop** — agent audits itself; logs may be true, **conclusion is not independent**.

```
Hermes audits Hermes → report says "fake" → report is also Hermes
→ GÖDEL LOOP (even with correct log evidence)
```

## Independence ladder

| Class | Meaning |
|-------|---------|
| `STRANGE_LOOP_VOID` | doer == judge; rejected exit 6 |
| `ACTOR_SEPARATED` | different actor_id (still AI) |
| `KERNEL_ARBITER` | `effective_verdict` from arifOS only |
| `F13_REQUIRED` | human sovereign for critical |

**Only F13 is true external.** Kernel is independent of the chat; F13 is independent of the system.

## Iron rules

| # | Rule |
|---|------|
| G1 | Never free-text a constitutional verdict. |
| G2 | Verdict source = `arifOS.kernel.arif_judge` only. |
| G3 | Quote `effective_verdict` + `call_hash` + `session_id` + `independence_class`. |
| G4 | `status=completed` ≠ SEAL. |
| G5 | Kernel down → HOLD. |
| G6 | **doer ≠ judge_actor** — use `apex-judge isolate`. |
| G7 | Evidence = OBS/DER only; no smuggled SEAL prose. |
| G8 | Critical/self-federation → `--critical` → F13_REQUIRED. |

## Procedure — default (all harnesses)

### Path A — ISOLATE (mandatory for self-audit / T2+ gates)

```bash
apex-judge isolate \
  --doer HERMES \
  --candidate "<action or claim under judgment>" \
  --evidence-file /tmp/ev.json \
  --pretty --human

# critical self-federation
apex-judge isolate --doer HERMES --critical -c "…"
```

Strange-loop only:

```bash
apex-judge --check-loop --doer HERMES --candidate "audit myself"
```

### Path B — Isolated subagent

Prompt: `/root/AAA/prompts/APEX_JUDGE_SUBAGENT.md`  
Parent passes evidence package only (no chat). Subagent runs Path A.

### Path C — MCP (judge actor ≠ doer)

1. `arif_init` as **judge lane** (e.g. OPENCLAW), not as the doer.
2. `arif_judge` with `evidence.in_band=true`.
3. Parent quotes receipt only.

### Path D — Audit prose

```bash
apex-judge --audit-text - <<'EOF'
…draft…
EOF
```

## Separation table

| Role | Who | May produce |
|------|-----|-------------|
| DOER | Hermes / Grok / OpenCode / … | work + OBS evidence |
| JUDGE LANE | different actor (`OPENCLAW` default) | no free text SEAL |
| KERNEL | arifOS `:8088` | `effective_verdict` |
| F13 | Arif | critical approve |

## Reporting template (only valid form)

```markdown
### Kernel judgment (not agent opinion)
- independence_class: KERNEL_ARBITER
- doer: <X>
- judge_actor: <Y≠X>
- judge_persona: 888-APEX
- effective_verdict: <from receipt>
- session_id: …
- call_hash: …
- reasons: …
```

## Option backlog

- **Option 2:** A2A → `888-APEX` agent card (persona mesh).  
- Do not wait for Option 2 to stop self-certify — isolate is live.

DITEMPA BUKAN DIBERI.
