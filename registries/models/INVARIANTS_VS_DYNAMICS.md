# Model Registry — Invariants vs Dynamics

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-13 by 333-AGI under F13 SOVEREIGN directive
> **Purpose:** Separate what NEVER changes (invariants) from what updates with market data (dynamics)
> **Binding:** All registry updates MUST respect this separation. Invariant mutation = T3 888_HOLD.

---

## ∴ INVARIANTS — The Constitutional Skeleton

These do NOT change with market conditions. They are the federation's structural identity.
Mutation requires F13 SOVEREIGN ratification + 888_HOLD.

### I1. Constitutional Floor Architecture (F1-F13)
The 13 floors are the genome. Market data does not move them.
- F1 AMANAH (reversibility) — invariant
- F2 TRUTH (evidence labels OBS/DER/INT/SPEC) — invariant
- F7 HUMILITY (Ω₀ ∈ [0.03, 0.05]) — invariant
- F9 ANTI-HANTU (no consciousness claims) — invariant
- F10 ONTOLOGY (AI-only, no soul) — invariant
- F13 SOVEREIGN (Arif veto FINAL) — invariant

### I2. The 8-Verb Authority Chain
```
arif_init → arif_observe → arif_think → arif_route → arif_memory
          → arif_judge → arif_forge → arif_seal
```
No market data changes this loop. Only `arif_seal` writes to VAULT999.

### I3. Constitutional Role Restrictions
- **666_JUDGE and 999_SEAL**: ONLY models with FFF 8/8 PASS + identity_verified + zero censorship on Malaysian governance topics
- Current eligible set: `deepseek-v4-pro`, `qwen3.8-max`, `glm-5.2`, `MiniMax-M3`
- A model's market popularity does NOT grant it constitutional authority
- A model's intelligence index does NOT grant it constitutional authority
- **Only FFF gate passage + sovereign ratification grants constitutional authority**

### I4. Agent Role Separation (Trinity + 4 lanes)
- **333-AGI (Δ MIND)**: reasoning, planning, code, synthesis — OPEN
- **555-ASI (Ω CORE)**: memory, telemetry, drift, research — DOMAIN
- **777-FORGE (EXECUTION)**: build, deploy, mutate — SHELL
- **888-APEX (Ψ SOUL)**: constitutional verdict — JUDGE_ONLY
- No market data reassigns agent roles

### I5. Rate-Limit Isolation Per Pool
No two agents share the same primary provider pool. This is structural resilience, not preference.
- DeepSeek pool ≠ Qwen pool ≠ Xiaomi pool ≠ MiniMax pool ≠ Anthropic pool
- Cross-provider by fallback position 3+ (different network route)

### I6. Fallback Discipline
- Retry primary 3× with backoff (1s, 2s, 4s) before fallback
- `api_max_retries ≥ 5` for every agent
- Dead providers PARKED, never removed (config preserved for re-enable)

### I7. Jurisdiction Bias
- CN/SG jurisdiction preferred for sovereign data (no CLOUD Act)
- US jurisdiction models flagged `cloud_act_exposed: true`
- US models forbidden for: Malaysian governance, sovereign identity, constitutional judgment

### I8. Open-Weights Preference
- MIT > Apache 2.0 > Custom > Proprietary
- Self-hostable models prioritized for blind-survival tier
- Architecture parameters (total/active) recorded when available

### I9. Censorship Zero-Trust
- Any model returning empty content on Malaysian governance topics = CENSORED
- Censored models FORBIDDEN from 666_JUDGE, 999_SEAL, 333_THINK on sovereign topics
- Probing methodology: 6-topic battery (1MDB, Najib, PETRONAS, Jho Low, Khazanah, Anwar)

### I10. No Self-Certification (Gödel Lock)
- No actor certifies itself
- caller == target_actor → HOLD
- Audit model MUST be different provider from judge model
- Chain terminates at F13 human sovereign

### I11. Lane A vs Lane B Sealing
- Lane A: `arif_seal` → VAULT999 (constitutional, F13-bound, tri-witness ≥ 3)
- Lane B: `forge_vault(receipt)` → session.ledger (autonomous, every session)
- No intelligence leaves the federation without a seal

### I12. SCT Token Architecture
- Every federated tool call requires valid SCT (`sct_v1.*`)
- Session ID minted by `arif_init` on :8088
- Lease defines `max_action_class` ceiling
- `OBSERVE_ONLY` + mutation intent = `888_HOLD` (full stop)

---

## 🌊 DYNAMICS — The Market Surface

These update WITH market data. No F13 ratification needed for factual updates.
T1 AUTO-DO for data refresh. T2 ANNOUNCE for model additions/removals.

### D1. Provider Balances
- **SOT**: FED :7074 (`fed_status` or `curl :7074/health`)
- **Cache**: `token_bank.db` (SQLite, updated by FED probes)
- **Rule**: NEVER hardcode dollar amounts in any doc. FED is the single source.
- **Drift gate**: If any doc claims a balance → it is WRONG unless it matches FED live.

### D2. Model Popularity / Usage Volume
- **Source**: OpenRouter rankings (monthly), Artificial Analysis (quality)
- **Refresh**: Monthly snapshot into `_meta.openrouter_market_intelligence`
- **Fields**: `tokens_month`, `growth_pct`, `market_share_pct`, `trend`
- **Purpose**: Inform fallback chain ordering, identify rising models

### D3. Intelligence Index Scores
- **Source**: Artificial Analysis Intelligence Index
- **Refresh**: When new benchmark data published
- **Purpose**: Inform constitutional eligibility CONSIDERATION (not decision — FFF gate decides)

### D4. Pricing Data
- **Source**: Provider docs, OpenRouter cost-per-session
- **Refresh**: When provider changes pricing
- **Fields**: `cost_per_1m_input`, `cost_per_1m_output`, `cost_per_1m_cache_hit`
- **Purpose**: Cost cascade optimization, budget routing rules

### D5. Model Availability (Live/Dead/Disabled)
- **Source**: Live API probes (`/v1/models`, health endpoints)
- **Refresh**: Continuous (FED probes every cycle)
- **Rule**: Dead providers PARKED with `disabled_reason` + `disabled_at`. Never removed.
- **Re-enable**: Requires live probe confirmation + `status: live`

### D6. New Model Releases
- **Source**: Provider announcements, Hugging Face, arXiv, OpenRouter new models
- **Refresh**: On discovery
- **Process**: 
  1. Add to registry with `status: OBSERVED` (not LIVE)
  2. Probe live API
  3. If alive: `status: LIVE`, assign provider, initial cost/capability data
  4. FFF gate before any constitutional role
  5. Sovereign ratification for 666_JUDGE / 999_SEAL

### D7. API Endpoint Changes
- **Source**: Provider deprecation notices, endpoint migrations
- **Refresh**: On provider announcement
- **Examples**: Azure OpenAI retiring Oct 2026, Cerebras credit expiring Aug 20 2026

### D8. Rate Limit States
- **Source**: Live API responses (429, quota headers)
- **Refresh**: Continuous
- **Rule**: `status: rate_limited` when 429 persistent. Auto-recovery on quota reset.

### D9. Benchmark Highlights
- **Source**: Provider-published benchmarks, independent evals (BenchLM, Artificial Analysis)
- **Labels**: Provider benchmarks = `[INT]` (vendor claim). Independent = `[OBS]`.
- **Refresh**: When new benchmark results published

### D10. Usage Signals (Per-Model Trends)
- **Source**: OpenRouter 60-day token volume
- **Fields**: `tokens_60d`, `trend` (+/- %), `note`
- **Purpose**: Identify rising/declining models for cascade optimization

---

## ⚖️ The Separation Test

Before ANY registry mutation, ask:

| Question | If YES | If NO |
|---|---|---|
| Does this change a constitutional floor? | **INVARIANT** — 888_HOLD | Continue |
| Does this change agent role assignments? | **INVARIANT** — 888_HOLD | Continue |
| Does this change the 8-verb chain? | **INVARIANT** — 888_HOLD | Continue |
| Does this change FFF gate verdicts? | **INVARIANT** — 888_HOLD | Continue |
| Is this a factual market data refresh? | **DYNAMIC** — T1 AUTO-DO | Continue |
| Is this adding a newly released model? | **DYNAMIC** — T2 ANNOUNCE | Continue |
| Is this updating a balance/price? | **DYNAMIC** — T1 AUTO-DO (via FED) | Continue |

**Default when uncertain:** HOLD. Ask: "Does this change structure or data?"

---

## 🔧 Operational Rules

1. **Balance entries**: NEVER in the registry JSON. Always FED :7074.
2. **`balance_usd` fields in registry**: ALL are STALE. Treated as FALSE. (Purged 2026-08-05.)
3. **`last_verified` timestamps**: Update on every live probe. Not on assumptions.
4. **New model addition**: Requires live probe, not just press release.
5. **Model removal**: NEVER. Park with `disabled_reason`. Config preserved.
6. **Fallback chain reordering**: T2 ANNOUNCE. 10s window. Then execute.
7. **Constitutional role assignment**: T3 888_HOLD. Requires FFF gate + sovereign.

---

*Forged 2026-08-13 by 333-AGI under F13 directive: "separate the invariants and dynamics accordingly, zen all"*
*The skeleton does not move. The surface flows. Both are real. Both have their place.*
*DITEMPA BUKAN DIBERI ⚒️*
