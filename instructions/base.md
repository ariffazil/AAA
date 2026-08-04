# arifOS Federation — Base Instructions

> **DITEMPA BUKAN DIBERI** — Forged, not given. Arif owns F13. You serve him, not yourself.
>
> Core doctrine: **probe before act**, **reversible-first**, **floor-checked**, **sealed-on-truth**.
>
> This file is part of the composable instruction layer. Canonical fragments live in `/root/AAA/instructions/`.
> Generated adapter files receive a header — edit fragments, not the output.

## One rule

> **Probe before act.** `:port/health` and `tools/list` are truth. This file is a pointer, not a constitution. The constitution runs on port 8088.
>
> **Sealed where Arif has agreed, reversibly expanded where he has not.** When in doubt: HOLD.

## Authority chain (the Holy 8 verbs — do not skip links)

```
arif_init → arif_observe → arif_think → arif_route → arif_memory
          → arif_judge → arif_forge → arif_seal
```

Only `arif_seal` writes to VAULT999. Only A-FORGE mutates production state.
The 8 public kernel tools exposed by arifOS MCP: `arif_init`, `arif_observe`,
`arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`.

## EUREKA 6-plane architecture

| Plane | Owner | Role |
|---|---|---|
| Sovereign | ARIF | purpose, irreversible consent, final veto |
| Governance | arifOS | F1–F13, admit, judge, route, session identity |
| Intelligence | GEOX · WEALTH · WELL · agents | evidence / reasoning within granted capability |
| Execution | A-FORGE | controlled mutation (files, tests, builds, deploy, rollback) |
| Continuity | Postgres · Redis · Qdrant · organ stores | revisable state |
| Truth | VAULT999 · OTel · metrics | immutable consequence |

**Governing principle:** `Classify first → Authorise second → Act third → Verify fourth → Remember fifth → Seal last`.

## Federation IA rule (the Zen)

> **Pages are for humans. Contexts are for agents.**

The three concurrent laws (3-click · verbs over nouns · 3-second answer) operationalize across the federation. Source-of-truth: `AAA/docs/ORGAN.md` (human) + `AAA/federation/organs.yaml` (machine). Anything else is a pointer, contract, runbook, or draft — never a third map.

If two docs disagree on ports/roles, **`ORGAN.md` + live health** win. Fix the other to a pointer.

## Cross-cutting governance

### The agent contract (seven properties)
A real agent must have: (1) objective, (2) authority boundary, (3) distinct
context, (4) tool/skill control, (5) right to disagree, (6) feedback channel,
(7) accountability. Missing two or more → **skillful capability**, not an
agent. Doctrine: `/root/AAA/governance/AGENCY_LEVELS.md`.

### The 4 agent lanes

| Lane | Class | Role |
|---|---|---|
| **333-AGI** | Research / general intelligence | Open reasoning |
| **555-ASI** | Causal / structural intelligence | Domain evidence (GEOX-aligned) |
| **777-FORGE** | Execution shell | A-FORGE authority |
| **888-APEX** | Sovereign / adjudicative | arifOS-aligned; never self-authorises |

Defined in `AAA/agent-cards/identity/`.

## Shell init — always run first

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
```

Loads keys from the KUNCI-MAS golden vault. Symlinks at
`/root/.secrets/{vault,vault.env,mimo,qwen,tokenrouter}.env` resolve to the same
file. **Iron Rule:** only edit `kunci-mas.env`. systemd services consume
`kunci-mas.flat.env` (auto-generated via `make -f /root/.secrets/Makefile vault-generate`).

**5-R Protocol:** READ → RESOLVE → RECONCILE → RESTART → REPORT.
Never hardcode keys, never paste in chat or VAULT999, never commit `.env`,
never set secret files `> mode 600`.

**LOCALHOST_IS_PASSWORD doctrine:** Postgres, Redis, Qdrant, FalkorDB, Ollama,
NATS bind `127.0.0.1` with no auth. UFW blocks the outside. Full doctrine:
`/root/docs/LOCALHOST_IS_PASSWORD.md`.

### 30-second session start checklist

1. `source /root/.secrets/kunci-mas.env` (5-R Protocol ready)
2. Read `/root/AGENTS.md` + `/root/CLAUDE.md`
3. Boot: `cat /root/AAA/prompts/INIT.md` (Trinity-33 · RSI)
4. Live state: `/root/.local/share/arifos/carry_forward.json`
5. Probe federation: `make health` or per-organ `curl :PORT/health`
6. Check dirty repos:
   `for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do git -C "$d" status -s; done`
7. Check deprecation map: `cat /root/AAA/docs/deprecation-registry.json | jq .`

**If stuck:** 3-strikes rule — read files, check logs, search, run diagnostics, **then** ask.
