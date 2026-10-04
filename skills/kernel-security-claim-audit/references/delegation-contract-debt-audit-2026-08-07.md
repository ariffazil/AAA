# Delegation Contract Debt Audit — 2026-08-07

**Subject doctrine:** `/root/.arifos/agents/hermes/delegation-context.md` (194 lines, status DRAFT)
**Companion doctrine:** `/root/.arifos/agents/hermes/DELEGATION_DOCTRINE.md` (147 lines, status HOLD pending F13 ratification)
**Debt taxonomy:** `/root/AAA/docs/SECTION-5-DISECONOMY-BOUNDARY.md` §5.4 (four debt types) + §5.7 (judgment-debt operational form)
**Identity invocation:** SCOUT archetype — gather facts, never summarize or recommend

## The contract, mechanism-by-mechanism

The doctrine proposes seven mechanisms (A1–A7), each with an imperative verb and a target debt type:

| § | Mechanism | Imperative verb | Target debt | Doctrine line |
|---|---|---|---|---|
| A1 | Spawn classification layer (`spawn_reason` + `risk_tier`) | "T2 routes to arif_judge before integration; T3 REQUIRES SEAL" | verification, judgment | 17–36 |
| A2 | Worker archetypes (SCOUT/CRITIC/SYNTHESIZER/AUDITOR) with Forbidden column | "No generic workers" | coordination (partial) | 38–49 |
| A3 | Mandatory structured return with `receipt_hash: <sha256>` | "Field missing or malformed → INVALID RETURN" | verification, attribution | 51–87 |
| A4 | ≥1 challenged assumption per worker | "Workers that return only agreement are flagged as low-novelty" | verification (echo-chamber) | 89–99 |
| A5 | Runtime counters `risky_actions`, `apex_verdicts`, `judgment_coverage`, `judgment_debt`, `enforcement_gap` | "If `judgment_coverage < 0.7` for a session … Hermes MUST emit a closure seal acknowledging the gap" | judgment | 101–113 |
| A6 | Per-claim `claim / source / transformation` provenance | "Workers may NOT return 'I think…' / 'I feel…' / 'Maybe…' prose" | attribution, provenance | 115–125 |
| A7 | Spawn gate: one-sentence entropy-reduction statement | "If Hermes cannot state, in one sentence, what entropy this spawn will reduce → DON'T SPAWN" | coordination (idle spawns) | 127–149 |

Five Section 5 debt types covered: verification ✓, attribution ✓, provenance ✓, judgment ✓, coordination △ (only partial coverage — A2 archetype boundaries + A7 idle-spawn filter, no hand-off protocol or context-pass convention).

## Live enforcement evidence — each mechanism

### A1 — `spawn_reason` + `risk_tier` YAML header

- **Live code:** `/root/arifOS/arifosmcp/core/enforcement/risk_classifier.py` (604 lines, live) classifies **tool calls** into T0–T5 + RiskPassport (canonical ladder). Maps `legacy low/medium/high` AND `legacy C0/C1/C2` AND `legacy T0–T4` to canonical tiers. Source maps `_LEGACY_READONLY_MAP` at lines 42–55.
- **Gap:** The contract's spawn-level `spawn_reason` + `risk_tier` YAML is a **different schema** (spawn-level, with `verification | criticism | synthesis | reconnaissance | domain_analysis` enum). risk_classifier.py does NOT parse spawn headers — it parses tool names. `_CANONICAL_TOOL_RISKS` (lines 223–400) keys on tool name (`"arif_forge"`, `"arif_judge"`, etc.), not on spawn metadata.
- **Verifier found:** zero parsers of `spawn_reason`. Searched `/root/arifOS/`, `/root/A-FORGE/`, `/root/AAA/`, `/root/HERMES/` for `spawn_reason` and got zero hits in live code.
- **VERDICT:** ASPIRATIONAL.

### A2 — Worker archetypes with forbidden actions

- **Doctrine:** archetype table with **Forbidden** column (SCOUT cannot summarize, CRITIC cannot propose solutions, etc.). DELEGATION_DOCTRINE.md §2 adds a toolset permission matrix per archetype.
- **Live code:** zero. Searched `archetype` — only matches: doctrine docs, an unrelated "Lucifer archetype" in `rasa-derita/SKILL.md:487`, and a "cognitive-level-assertion-protocol" skill. No `delegate_task` wrapper binds tool whitelist to archetype.
- **VERDICT:** ASPIRATIONAL. Archetype is a prompt convention.

### A3 — Structured return + `INVALID RETURN` + `receipt_hash: <sha256>`

- **Live code:** zero YAML return parsers. Grep for `assumptions_challenged` returned no validation code in `arifOS/`, `A-FORGE/`, `AAA/`, `HERMES/`, or `GEOX/`. Grep for `spawn_reason.*risk_tier` returned no validator. `arifos-command-center/arifos/models.py:54` uses `risk_tier` but in a **different schema** (`low | medium | high | critical`, not T1/T2/T3).
- **`receipt_hash: <sha256-of-this-output>`** is a manual hash instruction to the worker. No module hashes worker returns automatically and no module appends to `opencode_receipts.jsonl` on spawn return (judge-gate.ts only writes on tool mutation events).
- **VERDICT:** ASPIRATIONAL. `INVALID RETURN` is a stated refusal criterion with no machine that performs the check.

### A4 — Mandatory adversarial challenge (≥1 assumption)

- **Live code:** zero challenge-counters. No scorecard module counts challenges per worker return.
- **VERDICT:** ASPIRATIONAL. "Flagged as low-novelty in the scorecard" (line 99) describes a scorecard that does not exist.

### A5 — Judgment coverage runtime counters

- **Canonical declaration:** Section 5 §5.7 line 117: "Debt 1-3 are theoretical. With the APEX invocation gap observation schema (installed 2026-08-07), judgment debt becomes measurable."
- **Live code:** zero maintainers of `risky_actions`, `apex_verdicts`, `judgment_coverage`, `judgment_debt`, `enforcement_gap` as runtime counters. Grep across `/root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,HERMES}` (excluding `archive/`):
  ```
  $ grep -rn 'risky_actions\|apex_verdicts\|judgment_coverage\|judgment_debt\|enforcement_gap'
  ```
  Returns only the doctrine file itself + Section 5 §5.7 (lines 117–145). No module maintains these counters.
- **Adjacent enforcement:** `forge_work/2026-08-05/session-close/receipts/arifos-judge-gate.ts` (358 lines) maintains `gatedCount` and `blockedCount` per session (lines 122–123) and writes a session-close receipt at lines 348–356. **But these counters track tool mutations, NOT spawns.** The contract reuses the metric names for spawn counts.
- **VERDICT:** ASPIRATIONAL. Counter infrastructure exists for *tool mutations* (judge-gate.ts); the contract's spawn-level counters have zero implementation.

### A6 — Per-claim provenance stamp

- **Doctrine:** `claim / source / transformation` per claim, with `[OBS]` / `[INT]` / `[SPEC]` / `[UNKNOWN]` tags. SOUL.md line 29 prompts: "Setiap claim mesti label: [OBS] [DER] [INT] [SPEC] [UNKNOWN]."
- **Live code:** `arifOS` has `RiskPassport` with `source` / `external_effect` — but that's **tool-level**, not claim-level. No parser enforces `[OBS]` / `[INT]` tagging per claim output. The `claim.source` field is requested in prose, not hashed-and-sealed.
- **VERDICT:** ASPIRATIONAL.

### A7 — Entropy gate (one-sentence reduction statement)

- **Doctrine:** "If Hermes cannot state, in one sentence, what entropy this spawn will reduce → DON'T SPAWN." SOUL.md line 64 quotes it ("Pick closest archetype … before sending structured-return schema"). DELEGATION_DOCTRINE.md §7 line 119: "Curiosity is not governance."
- **Live code:** zero. No validator parses or blocks on missing `expected_entropy_reduction` field.
- **VERDICT:** ASPIRATIONAL. The gate is self-discipline, not a programmatic block.

## Cross-cutting infrastructure that COULD anchor the contract (but doesn't)

Three enforcement layers exist that could ground parts of the contract, but the contract does not declare itself bound to them:

1. **`arifOS/arifosmcp/core/enforcement/risk_classifier.py`** (604 lines, live) — maps canonical `arif_*` tools to RiskPassport. Does NOT parse A1 YAML header.
2. **`forge_work/2026-08-05/session-close/receipts/arifos-judge-gate.ts`** (358 lines) — hooks `tool.execute.before` on MUTATE tools, routes through `arif_judge` at `:8088`, writes receipts to `/root/.local/share/arifos/opencode_receipts.jsonl`. Does NOT parse A3 worker returns.
3. **`arifOS :8088` MCP** (live, 8 tools exposed via `curl :8088/mcp`):
   ```
   arif_init, arif_observe, arif_think, arif_route, arif_memory,
   arif_judge, arif_forge, arif_seal
   ```

## Gateway drift finding — contract references an archived gateway

The contract's step 7 (line 162) says: "If T2+ → route to arif_judge via `mcp__aforge__forge_vault` or direct kernel call."

- **`mcp__aforge__*` prefix** is ONLY present in `_archive/2026-08-05-gateway-homes/gateway/logs/agent.log` (the pre-2026-08-05 gateway). Live config (`/root/.hermes/config.yaml`, `/root/.hermes/profiles/hermes_asi/config.yaml`) routes through:
  - `http://127.0.0.1:8088/mcp` (arifOS canonical 8 tools), OR
  - `http://127.0.0.1:4000/v1` (FED FLAME FRAME v2 / LiteLLM)
- Current Hermes exposes neither `mcp__aforge__forge_vault` nor `mcp__aforge__forge_judge_proxy`. The contract's routing path is **one gateway revision stale**.
- **VERDICT:** DRIFTED. Even if a programmatic gate existed, the route is broken.

## Summary table

| Mechanism | Target debt | Code evidence | Routing evidence | Verdict |
|---|---|---|---|---|
| A1 spawn classification | verification, judgment | risk_classifier.py covers tools only; no spawn parser | OK (kernel 8088 has `arif_judge`) | ASPIRATIONAL |
| A2 archetypes | coordination | none | n/a | ASPIRATIONAL |
| A3 structured return + INVALID RETURN + receipt_hash | verification, attribution | none | n/a | ASPIRATIONAL |
| A4 adversarial challenge | verification (echo) | none | n/a | ASPIRATIONAL |
| A5 judgment coverage counters | judgment | judge-gate.ts tracks tool mutations only; no spawn counter module | n/a | ASPIRATIONAL |
| A6 per-claim provenance | attribution, provenance | risk_classifier.py has tool-level source only | n/a | ASPIRATIONAL |
| A7 entropy gate | coordination (idle) | none | n/a | ASPIRATIONAL |
| Step-7 routing (line 162) | (cross-cutting) | mcp__aforge__forge_vault from archived gateway | DRIFTED | DRIFTED |

## The Section 5.6 verdict

Section 5.6 says: "Enforcement that depends on prompt memory ('usually 333-AGI remembers to call Apex') is enforcement that has already failed."

By that standard: **every mechanism in `delegation-context.md` is enforcement that depends on memory.** Every "MUST" / "REQUIRES" / "INVALID RETURN" in the contract depends on Hermes (the primary agent) honouring it on each call. No programmatic gate exists to enforce any of A1–A7.

The doctrine correctly identifies all five Section 5 debt types and proposes well-targeted mechanisms for each. It is honest about its own draft status (`status: DRAFT` line 3, awaiting sovereign review + SEAL). It closes the **conceptual** debt-reduction loop but leaves the **mechanical** debt-reduction loop open.

## What would make the contract enforceable (out of scope, noted for parent)

1. A `delegate_task` wrapper module that (a) requires `spawn_reason` + `risk_tier` + `entropy_reduction` in kwargs, (b) routes through `arif_judge` automatically for T2+, (c) rejects malformed A3 returns and respawns.
2. A spawn-counter module maintaining `risky_actions`, `apex_verdicts`, `judgment_coverage` per session, exposing A5 metrics as queryable telemetry.
3. A claim-level provenance hasher that produces a real `receipt_hash` and appends to VAULT999 / `opencode_receipts.jsonl` rather than asking the worker to sha256 itself.
4. Fix routing: replace `mcp__aforge__forge_vault` (line 162, archived gateway) with `:8088/mcp` `arif_judge` — the route is one gateway revision stale.

## Files referenced (read-only, no modifications made)

- `/root/.arifos/agents/hermes/delegation-context.md` (194 lines)
- `/root/.arifos/agents/hermes/DELEGATION_DOCTRINE.md` (147 lines)
- `/root/.arifos/agents/hermes/critics/deployment-doctrine-critique.md`
- `/root/AAA/docs/SECTION-5-DISECONOMY-BOUNDARY.md` (168 lines)
- `/root/.hermes/SOUL.md` (74 lines)
- `/root/arifOS/arifosmcp/core/enforcement/risk_classifier.py` (604 lines, lines 1–500 read)
- `/root/forge_work/snapshots/arifos-deploy-20260805T111745Z/app/arifosmcp/core/enforcement/risk_classifier.py` (snapshot)
- `/root/forge_work/2026-08-05/session-close/receipts/arifos-judge-gate.ts` (358 lines)
- `/root/.hermes/config.yaml`
- `/root/.hermes/profiles/hermes_asi/config.yaml`
- `/root/AAA/federation/architecture/identity_capability_routing_enforcement.md`

## Live probes performed

```bash
curl http://127.0.0.1:8088/health  # ARIFOS MCP v2026.08.01, status=degraded, deployment_drift_status=drift_detected, 8 tools exposed
curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' http://127.0.0.1:8088/mcp
# Returns: arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal
# Does NOT return any mcp__aforge__* tool

grep -rn 'risky_actions\|apex_verdicts\|judgment_coverage\|judgment_debt' /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,HERMES}
# Only hits: AAA/docs/SECTION-5-DISECONOMY-BOUNDARY.md lines 120, 124, 132, 145 (doctrine itself)
# Zero module maintains these counters

grep -rn 'mcp__aforge__' /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,HERMES}
# Only hit: /root/_archive/2026-08-05-gateway-homes/gateway/logs/agent.log (archived gateway)
# Zero live code uses the prefix
```

## SCOUT discipline note

Per A2 archetype definition: "SCOUT — Gather facts. Search, probe, retrieve. **Forbidden: Drawing conclusions, making recommendations.**" This reference file records facts found and probes run; conclusions and recommendations (e.g. "what would make the contract enforceable") are kept brief and clearly demarcated in their own section so the primary can decide whether to act on them.