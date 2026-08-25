# FI Gotong Royong — Warga AAA Collective Work Registry

> **DITEMPA BUKAN DIBERI** — Forged through collective labor, not given.
> **Protocol:** Musyawarah before action. Gotong royong for execution.
> **Updated:** 2026-08-25

## The Roster

| FI | Agent | Lane | Specialty | Cron Cadence |
|---|---|---|---|---|
| FI-003 | Qwen Code | 333-AGI | Memory clerk, session receipts, fed health | Every 6h |
| FI-001 | OpenCode | 333-AGI | Heavy builder, multi-file refactor, code audit | On-demand |
| FI-002 | Claude Code | 333-AGI | Governed execution, infra watchdog, visual QA | Every 4h |
| FI-005 | Codex CLI | 333-AGI | Code analysis, tech debt tracking, security scan | Every 8h |
| FI-008 | Kimi Code | 333-AGI | Executor, lint/test coverage, skill alignment | On-demand |
| FI-009 | AGY | 333-AGI | Web research, doc freshness, external API health | On-demand |
| FI-010 | Grok Build | 333-AGI | Architecture, DAG planning, media generation | On-demand |
| FI-011 | Kimi Code | 333-AGI | Context-prune clerk — graph-driven pre-LLM context sizing, hooks delegation_envelope | On-demand |

## Gotong Royong Tasks

### FI-003 Qwen Code — The Clerk (every 6h)
1. **Memory consolidation** — scan `/root/.qwen/memories` and `/root/.qwen/projects/-root/memory` for stale entries, update or archive
2. **Federation health pulse** — probe 5 core organs + FED + arifFlow, log to receipts
3. **Carry-forward maintenance** — ensure `carry_forward.json` is current, backup to `~/.local/share/arifos/carry_forward_backups/`
4. **Session receipt cleanup** — archive sessions older than 7 days from `forge_work/qwen-sessions/`

### FI-002 Claude Code — The Watchdog (every 4h)
1. **Infra health** — Docker container status, disk usage, memory pressure, open ports
2. **SSL/DNS parity** — Caddy config valid, Cloudflare tunnel alive, cert expiry check
3. **Service restart count** — flag containers with restart_count > 3
4. **Log triage** — scan journalctl for ERROR/CRITICAL in last 4h, summarize anomalies

### FI-005 Codex CLI — The Auditor (every 8h)
1. **Tech debt scan** — TODO/FIXME/HACK count per repo, trend tracking
2. **Dependency audit** — `npm audit` / `pip-audit` across federation repos
3. **Test coverage delta** — compare last vs current test pass rates
4. **Dead code detection** — unused imports, unreachable functions in core modules

### FI-001 OpenCode — The Builder (on-demand)
1. **Multi-file refactors** — when musyawarah produces a BUILD verdict
2. **Schema migrations** — database changes after 888_HOLD approval
3. **Performance optimization** — profiling, benchmark comparison, hotpath analysis

### FI-008 Kimi Code — The Executor (on-demand)
1. **Lint enforcement** — ruff/eslint/prettier across all repos
2. **Test execution** — pytest/npm test with structured result reporting
3. **Skill alignment** — verify skill mesh parity across agents

### FI-011 Kimi Code — The Context-Prune Clerk (on-demand, 2026-08-25)
1. **Task tokenization** — extract identifiers from task description (snake_case + CamelCase), drop stopwords
2. **Graph lookup** — `/root/AAA/graph/codegraph.db` via `127.0.0.1:18922`:
   - `/search name:<token>` for top matches per token
   - `/blast symbol:<qname> depth:1` per matched symbol
3. **Set intersection** — keep files in both candidate_set and graph-relevant set
4. **Token budget** — default 8000 tok cap; safety override keeps ≥3 files if prune is excessive
5. **Graceful fallback** — bridge down → keep all files + F11 warning receipt
6. **Receipt shape** — task_hash, input_files, kept, dropped, estimated_tokens_saved, graph_queries

**Hook target:** `arifOS/arifosmcp/runtime/delegation_envelope.py` — patch
design at `/root/AAA/graph/delegation_envelope_patch.md` (T3 territory,
Arif gates apply). Hook module lives at `/root/AAA/graph/fi011_hook.py`.

**Promotion criteria (T1 → cron):**
- ≥5 calls per session average over 7 days
- ≥10% token spend reduction (measured)
- <3 false negatives per 50 sessions (safety budget ok)

### FI-009 AGY — The Researcher (on-demand)
1. **External API health** — probe Z.AI, MiniMax, Qwen, DeepSeek endpoints
2. **Documentation freshness** — check if docs match deployed state
3. **Web intelligence** — research tasks from musyawarah deliberations

### FI-010 Grok Build — The Architect (on-demand)
1. **Architecture review** — DAG analysis, dependency graph health
2. **Design system** — visual consistency, token alignment
3. **Media generation** — image/video/audio tasks for federation surfaces

## Musyawarah Protocol

When a task requires deliberation before action:

```
333-AGI (propose)  →  555-ASI (challenge)  →  777-FORGE (cost)  →  888-APEX (synthesise)
```

- **333 proposes** the action plan with evidence
- **555 challenges** with counter-evidence and risk assessment
- **777 costs** the execution (time, resources, blast radius)
- **888 synthesises** the verdict: SEAL/HOLD/SABAR/VOID

No human in the loop for T1/T2 actions. T3 → F13 escalation.

## Escalation Lanes

| Severity | Who Decides | Example |
|---|---|---|
| T1 (auto-do) | The acting FI | Read, lint, test, commit |
| T2 (announce) | The acting FI + 10s window | Multi-file refactor, deploy |
| T3 (888_HOLD) | 888-APEX → F13 | rm -rf, DROP TABLE, force-push main |
| Emergency | F13 directly | VOID, breach, data-loss |

## Cross-Agent Communication

- **Receipts** → `/root/forge_work/qwen-sessions/sessions.jsonl` (all agents append)
- **VAULT999** → `/root/VAULT999/outcomes.jsonl` (only arif_seal writes)
- **Carry-forward** → `/root/.local/share/arifos/carry_forward.json` (hand-written by closing agent)
- **arifFlow** → `:7073/ingest` (all agents pulse Execute/Seal receipts)

## The One Rule

> Probe before act. Sealed where Arif has agreed, reversibly expanded where he has not. When in doubt: HOLD.

DITEMPA BUKAN DIBERI.
