# Gödel Lock · Strange Loop Zen — Real Apex Judge

> **Forged:** 2026-08-09 · F13 context: Hermes self-audit cannot certify Hermes.  
> **CLI:** `apex-judge isolate` · **Skill:** `arifos-constitutional-judge`  
> **DITEMPA BUKAN DIBERI**

## The paradox (named)

```
Agent does X
Agent audits X
Agent concludes "X is fake / X is SEAL"
→ conclusion is also from the agent
→ GÖDEL LOOP
```

Logs can be true (OBS). **Conclusions about the system by the system are not independent.**

## Independence ladder

| Class | Who | Independent? | Use |
|-------|-----|--------------|-----|
| `STRANGE_LOOP_VOID` | Same agent judges self | ❌ | Rejected before kernel |
| `ACTOR_SEPARATED` | Different harness actor (still LLM lineage) | ⚠️ | Option 3 minimum |
| `KERNEL_ARBITER` | arifOS `arif_judge` (non-LLM constitutional) | ✅ organ | Required for any gate language |
| `F13_REQUIRED` | Muhammad Arif / F13 SOVEREIGN | ✅ true external | Critical / T3 / federation self-audit |

**Only F13 is true external audit.** Kernel is independent of the *conversation* and of free-text SEAL; F13 is independent of the *system*.

## Separation of concerns (iron)

```
DOER     → work + OBS evidence only (no verdict prose)
JUDGE    → isolated process, actor_id ≠ doer
KERNEL   → arif_judge effective_verdict + call_hash
F13      → human approve for critical / unresolved HOLD
```

Never: doer = judge = reporter of SEAL in one chat.

## How agents must call it

```bash
# Hermes audited by separate judge lane + kernel
apex-judge isolate \
  --doer HERMES \
  --candidate "Claim: zero arif_judge tool calls in session logs" \
  --evidence-file /tmp/ev.json \
  --pretty --human

# Critical (self-federation) — SEAL demoted to HOLD until F13
apex-judge isolate --doer HERMES --critical -c "…"
```

Evidence file must be **OBS/DER only** — no `verdict: SEAL`, no `888-APEX JUDGMENT`.

## What parent may print after return

```markdown
### Kernel judgment (not agent opinion)
- independence_class: KERNEL_ARBITER
- doer: HERMES
- judge_actor: OPENCLAW
- judge_persona: 888-APEX
- effective_verdict: …
- session_id: …
- call_hash: …
- reasons: …
```

Anything labeled `888-APEX JUDGMENT` **without** those fields = VOID prose.

## Option map

| Option | Shape | Status |
|--------|--------|--------|
| 1 | Doer calls `arif_judge` directly | Allowed only as tool path; still use isolate when possible |
| **3** | **isolate: doer ≠ judge → kernel** | **Default real path** |
| 2 | A2A → 888-APEX agent card | Long-term persona mesh |
| F13 | Human sovereign | Critical / T3 / strange-loop residual |

## Calhoun / anti-beautiful-one

If governance spends more tokens self-auditing than producing sovereign value → flag Calhoun. Force external (kernel + F13), reduce self-referential prose.

## Receipts

Isolated judgments persist under `/root/forge_work/apex_receipts/`.

DITEMPA BUKAN DIBERI.
