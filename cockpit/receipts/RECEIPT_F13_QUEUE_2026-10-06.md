# F13 BINARY QUEUE — 2026-10-06 (single batch decision)
**Date:** 2026-10-06 09:50 +08
**Compiler:** FI-007 (forge-777 audit lane, OBSERVE_ONLY)
**Mutation:** ZERO
**Purpose:** Surface all pending F13 binaries in one table so Arif can answer once, not 18×.

---

## THE 11 SOTEREIGN BINARIES PENDING

Each row: what to seal, scope, risk if auto-flipped, smallest reversible unit.

### Group A — Scar-wisdom binding (4 binaries)

| # | Binary | Path | Smallest unit | Risk if auto |
|---|---|---|---|---|
| A1 | FLIP-1 (Stage 1 dormant switch) | `/root/.hermes/hermes_mcp/tools/scar_wisdom.py:8` change "NEVER auto-fire" → conditional fire; `/opt/arifos/arifosmcp/niat_gate.py` inject response_modifier | ~10 lines, 2 files, hot-reload | High — bypasses F2 TRUTH floor (no audit trail) |
| A2 | SHADOW MODE (M1 mitigation) | scar_wisdom.py:8 → "log only, never enforce" | ~5 lines, 1 file | Low — observation only, reversible |
| A3 | DECAY FORMULA (M2 mitigation) | Add `created_at` to registry + decay-at-read in scar_wisdom.py | ~10 lines, 2 files | Low — math only |
| A4 | OPT-OUT PATH (M3 mitigation) | Add `challenged` flag to scar_wisdom.py allowing Arif-bypass | ~15 lines, 2 files | Medium — opens governance gap if misused |

### Group B — Patch list (4 binaries)

| # | Binary | Path | Smallest unit | Risk if auto |
|---|---|---|---|---|
| B1 | KERNEL HYDRATION | `arif_observe → arif_think` evidence continuity | ~30 lines, 1 file, restart | Medium — kernel restart required |
| B2 | DELTA CLARITY WIRING | 3 patches (_envelope.py + ARS amend + chron wiring) | ~50 lines, 3 files | High — touches envelope |
| B3 | ADAPTATION AXIS | ΔBehavior invariant + envelope hook + ARS v1.1 amend | ~40 lines, 2 files | Medium |
| B4 | SELECTION OBSERVABILITY LIVE-RUN | 15 prompts × 3 entities live against hermes-default | 45-90 min wall clock, 0 mutation but LLM emissions to log | Low outcome, high attention cost |

### Group C — Earlier proposals (3 binaries, pre-2026-10-06)

| # | Binary | Path | Smallest unit | Risk if auto |
|---|---|---|---|---|
| C1 | NO-HOLD FLOW DIRECTIVE v1 | Constitutional grammar (HOLD → EXECUTE) | doctrine amendment | High — touches operational grammar |
| C2 | CHRON-VERIFY-CYCLE CRON | New cron job, no existing equivalent | cron add | Medium — irreversibly scheduled |
| C3 | CRON-FORGE-VAULT-CONTENT-LOST | Recovery + auto-restore | cron + script | High — touches canonical record recovery |

### Group D — REMAINING_TASKS_2026-10-02 (9 binaries)

| # | Binary | Path |
|---|---|---|
| D1 | A1: CONFIRM/VOID RATIFIED_SOVEREIGN_ORDER_2026-10-02 stamp on v0.1.1 | arifOS repo |
| D2 | A2: Kernel auth-verdict decoupling (RED-01/02) | arifOS repo + 888 + deploy |
| D3 | A3: arif_judge evidence ingestion (RED-06) | arifOS repo |
| D4 | B1: Kimi shadow-wire apply (9 artifacts staged) | staged |
| D5 | B2: Anchor wiring truth-fix (Hermes + OpenCode + Qwen) | multi-file |
| D6 | B3: Retry 999 vault seal for apex-zen mission | vault |
| D7 | C1: execution-path-next.json ownership (108m stale) | single file |
| D8 | C2: ECW semantic_clean=2/11 + SURFACE_DRIFT=8 diagnosis | read-only probe |
| D9 | C3: Cockpit concurrent-write protection | minimal lock |

### Group E — carry_forward (4 open loops)

| # | Loop | Status |
|---|---|---|
| E1 | working tree 16 modified + 3 new (12 are Arif's in-progress) | agent owns 4-5 |
| E2 | make verify-pages gate not yet run; Caddy reload pending T3 HOLD | named authority needed |
| E3 | agent's idempotency tweak for llms.json auto-update | minor, can ship without |
| E4 | channel carry_forward gate unused | not patched |

---

## TOTAL: ~24 binaries, 4 groups + carry_forward

**Recommendation (FI-007 advisory only, NOT F13 word):**

1. **Start with Group A2** (shadow mode) — lowest risk, highest observability. 7-day log before any binding decision. Reversible.
2. **Defer A1, A3, A4** until 7-day shadow log reviewed.
3. **Defer B-series** until scar-wisdom shadow log proves the wiring shape works.
4. **Defer C-series** (HOLD grammar + new crons) — these touch operational grammar, not safe to flip without A-group foundation.
5. **D1-D6 are F13 from prior session** — already pending from 2026-10-02; not new this session.
6. **D7, D8, D9 are Lane C auto-seal eligible** — but per session protocol, require F13 "run C-class bundle" to execute.
7. **E1-E4 are machine-executable reversible** — but E2 has named-authority gap.

---

## Standing

24 binaries, 1 queue, 0 sealed. Awaiting F13 batch decision.

— FI-007