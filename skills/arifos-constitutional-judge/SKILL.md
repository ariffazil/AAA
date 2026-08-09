---
name: arifos-constitutional-judge
id: arifos-constitutional-judge
version: 1.1.0
owner: AAA
description: >
  Single load-bearing constitutional-judgment skill. Routes all F1–F13,
  verdict, hold, seal, scope, authority and floor-check calls through the
  live arif_judge surface. FORBIDS free-text self-SEAL ("888-APEX JUDGMENT"
  without kernel receipt). Option 3: CLI or isolated subagent must call
  kernel. Option 2 (A2A → 888-APEX) is the long-term path.
agent: 888-APEX
namespace: arifos
cluster: CONSTITUTION · VERDICT · ACT
risk_tier: high
autonomy_tier: T2
floor_scope: [F1, F2, F4, F7, F9, F11, F13]
---

# arifos-constitutional-judge (LOAD-BEARING · GÖDEL LOCK)

> **Forged:** 2026-08-01 · **Hardened:** 2026-08-09 (auto apex-judge federation-wide)  
> **Status:** Single canonical entry. DITEMPA BUKAN DIBERI.  
> **Reversible:** delete this file + restore from forge_work quarantine.

## The problem this skill kills

Agents (Hermes especially) emit **text** like:

```text
## 888-APEX JUDGMENT
Verdict: SEAL
```

…without calling `arif_judge`. That is **self-certification** — Gödel loop.  
Invalid as constitutional fact. Treat as **VOID prose**.

## Use When

1. Evaluating an action against F1–F13 (floor, authority, scope, verdict, hold, seal, audit).
2. Before any irreversible / T2+ mutation when a verdict is required.
3. After `delegate_task` returns T2+ results (parent must re-judge before integrate).
4. Anytime the agent is about to type `SEAL` / `888-APEX` / `HOLD` as a formal gate.

## Do NOT Use When

1. Pure T0 read with no constitutional claim.
2. Casual chat with no gate language.
3. Local lint that does not claim federation authority.

## Iron rules (non-bypassable)

| # | Rule |
|---|------|
| G1 | **Never** free-text a constitutional verdict. |
| G2 | Verdict source must be `arifOS.kernel.arif_judge` (MCP or `apex-judge` CLI). |
| G3 | Quote `effective_verdict` + `call_hash` + `session_id` when reporting. |
| G4 | Top-level MCP `status=completed` is **execution**, not SEAL. Use `effective_verdict`. |
| G5 | If kernel unreachable → **HOLD**, never invent SEAL. |
| G6 | Subagent/CLI isolation preferred (Option 3) so the judge has no parent chat to rubber-stamp. |

## Procedure — Option 3 (default, all harnesses)

### Path A — CLI (universal, every agent runtime)

```bash
# installed as /root/.local/bin/apex-judge
apex-judge --candidate "<action under judgment>" --actor <HERMES|OPENCLAW|GROK|CLAUDE|OPENCODE|…> --human --pretty
```

Optional evidence:

```bash
apex-judge -c "…" -a HERMES -e /tmp/evidence.json --pretty
```

Audit draft for self-SEAL:

```bash
apex-judge --audit-text - <<'EOF'
…draft response…
EOF
```

### Path B — MCP tools (same session or subagent)

1. `arif_init(mode="init", actor_id="<HARNESS>", requested_authority="STANDARD", verbosity="minimal")`
2. `arif_judge(mode="judge", candidate="…", session_id, session_token, evidence={…, "in_band": true})`
3. Read **`effective_verdict`**, not prose.

MCP names by harness (all are the same tool):

| Harness | Tool name examples |
|---------|-------------------|
| Grok Build | `arifos_mcp__arif_judge` |
| Hermes / Claude | `mcp__arifos__arif_judge` or `arif_judge` |
| OpenClaw | organ MCP `arif_judge` |
| Any shell | `apex-judge` CLI |

### Path C — Isolated subagent (when parent has rich chat bias)

Load prompt: `/root/AAA/prompts/APEX_JUDGE_SUBAGENT.md`  
Spawn with **only** MCP arifOS tools (or shell `apex-judge`).  
Parent integrates **only** the returned JSON receipt.

## Verdict mapping (kernel truth)

| `effective_verdict` | Agent behavior |
|---------------------|----------------|
| `SEAL` | Proceed; mint receipt if required. |
| `SABAR` | Proceed with stated conditions only. |
| `HOLD` | Stop. Surface reasons. No mutation. |
| `VOID` | Blocked. New evidence required. |

If `constitutional_check.hold_required=true` → treat as **HOLD** even if prose says otherwise.

## Failure modes

| Mode | Response |
|------|----------|
| MCP down | CLI against `127.0.0.1:8088`; still HOLD if both fail |
| `EVIDENCE_HASH_MISSING` | Add `"in_band": true` or proper `evidence_hash` |
| Free-text SEAL detected | `apex-judge --audit-text` → VOID that draft |
| Actor OBSERVE_ONLY / no SCT | Still call judge — kernel returns real HOLD/SEAL; do not fake FULL |

## Option 2 backlog (A2A — correct architecture, later)

```
Hermes/OpenClaw → A2A tasks/send → 888-APEX agent card
  → 888-APEX calls arif_judge → returns kernel receipt
```

Do **not** wait for Option 2 to stop self-certifying. Option 3 is mandatory now.

## Reporting template (only valid form)

```markdown
### Kernel judgment (not agent opinion)
- source: arifOS.kernel.arif_judge
- effective_verdict: <from receipt>
- session_id: <sid>
- call_hash: <hash>
- reasons: <kernel reasons>
```

Anything labeled `888-APEX JUDGMENT` **without** those four fields is **VOID prose**.

## Empirical reference

Live smoke 2026-08-09: `apex-judge` → `arif_init`+`arif_judge` for OPENCLAW/HERMES/GROK/CLAUDE/OPENCODE returns kernel `effective_verdict` + `call_hash`. Free-text path forbidden by this skill v1.1.0.

DITEMPA BUKAN DIBERI.
