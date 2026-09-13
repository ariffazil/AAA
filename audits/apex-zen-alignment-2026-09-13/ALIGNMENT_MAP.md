# ALIGNMENT_MAP — APEX-ZEN Sweep v1
> `ARIFOS::AAA_ALIGNMENT_SWEEP::v1` · Authority: ARIF (F13) · Executor: 333-AGI (session `SEAL-42dad7d3d9334310`) · Date: 2026-09-13
> Scope: `/root/AAA` repository + live instruction surfaces rendered into harnesses. Exclusions: `node_modules`, `.git`, `dist`, `*_archive*`, `_superseded`, `.hermes-archived*`.

## 1. Inventory (OBS — live counts 2026-09-13)

| Surface | Class | Files | Notes |
|---|---|---|---|
| `prompts/` | prompts | 25 (25 md) | INIT/SEAL/role prompts |
| `instructions/` | governance fragments | 116 (116 md) | canonical fragments; rendered to `/root/AGENTS.md` |
| `governance/` | doctrine | 293 (248 md) | incl. APEX-ZEN doctrine + consequence ladder |
| `skills/` | capability | 842 (217 × SKILL.md) | excl. `.profile-archive/` |
| `agents/` | identity + runtime | 1618 (653 md) | 53 × `agent-card.json` |
| `plugins/` | runtime hooks | 16 | autonomy plugins, hook scripts |
| `scripts/` | tooling | 212 | incl. `apex-zen-telemetry.py`, `apex-zen-score.py`, `scorecard.py` |
| `federation/` | topology | 269 (74 md) | organs.yaml machine-SOT |
| `docs/` | documentation | 514 (417 md) | |
| `audits/` | audit receipts | 8 → this dir | this sweep adds 5 artifacts |
| a2a-server | orchestration | — | 13 harness cards, gateway :3001 |

## 2. Instruction surfaces (the behavioral control plane)

| Layer | Path | Rendered to | Enforcement |
|---|---|---|---|
| Kernel doctrine | `/root/AGENTS.md` + fragments | all harnesses | SessionStart hooks, kernel :8088 |
| OpenCode warga | `/root/.config/opencode/AGENTS.md` + rules | FI-001 | aaa-autonomy plugin |
| Claude Code | `/root/.claude/CLAUDE_IDENTITY.md` + plugin hooks | FI-002 | hooks (audit/entropy) |
| Per-agent docs | `agents/opencode/`, `agents/hermes-asi/` | harnesses | mixed |
| APEX-ZEN Doctrine v1 | `governance/APEX-ZEN-EXECUTION-DOCTRINE.md` | humans + agents | Layer 1 policy (LIVE) |

## 3. Telemetry surfaces found (Phase 4 seed)

| Surface | Path | State (OBS) |
|---|---|---|
| Layer-2 collector | `scripts/apex-zen-telemetry.py` | CODE LIVE · unscheduled · data file created 2026-09-13T10:56Z (1 record) |
| Layer-3 scoring | `scripts/apex-zen-score.py` + `scorecard.py` | CODE LIVE · no scheduled runs |
| Output stream | `/root/VAULT999/apex-zen-telemetry.jsonl` | 1 record (first ever, this sweep) |
| FQ metabolism | arifFlow `:7073/health` | LIVE · per-actor FQ vector |
| Governance events | arifFlow `flow_gov_events` | LIVE · seal/seal_refused — raw material for DCR |
| VAULT999 seal chain | `seal_chain.jsonl` | LIVE (append-only) |
| Session transcripts (measurement fuel) | `/root/.kimi-code/sessions/**/wire.jsonl`, `agents/*/runtime/**` | PRESENT · formats vary per harness |

## 4. Enforcement ladder state (doctrine → runtime)

```
Layer 1 Policy      ✅ LIVE   (APEX-ZEN-EXECUTION-DOCTRINE.md v1, ratified 2026-09-13)
Layer 2 Telemetry   🟡 CODE-LIVE / UNWIRED  (collector runs manually; no cron; 1 record)
Layer 3 Scoring     🟡 CODE-LIVE / UNWIRED  (score script exists; never scheduled)
Layer 4 Consequence 🟡 DEFINED / ROUTER TBD (consequence ladder doc; no router)
```

**Central finding:** the gap is NOT documentation. It is **wiring** — the last mile from code to scheduled streams to consequence.

## 5. Method (F11 — reproducible)

- Inventory: `find` counts per surface (exclusions above).
- Class scans: `grep -rInE` over instruction surfaces (`prompts instructions governance skills agents plugins scripts`) with archive exclusions; raw hits classified by context (prohibition vs detector vs violation).
- Telemetry: read collector source; executed live against one real transcript; inspected output stream.
- No mutation beyond: telemetry record append (designed path), audit artifacts (this dir).

DITEMPA BUKAN DIBERI — 2026-09-13
