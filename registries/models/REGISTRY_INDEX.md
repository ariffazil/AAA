# Model Registry Index — arifOS Federation

> **Forged:** 2026-06-27 by FORGE (000Ω) per F13 SOVEREIGN directive
> **Updated:** 2026-07-20 — AGENT_MODEL_MAP.json unified registry
> **Authority:** F13 SOVEREIGN (Arif Fazil)
> **CANONICAL SOURCE:** `/root/AAA/registries/models/AGENT_MODEL_MAP.json` (21 models, 13 agents, 9 providers, 6 shadows, 2 scars, 4 fallback chains, 9 routing rules)
> **Supersedes:** `FEDERATION_MODEL.json` (absorbed), scattered prose tables in INIT.md/TOOLS.md/AGENTS.md
> **Soul/shadow profiles:** `/root/AAA/registries/models/{provider}_{soul,shadow}.yaml` (supplementary deep-dives)
> **Model capabilities:** `/root/arifOS/arifosmcp/config/model_registry.json` (constitutional capability registry — referenced, not duplicated)
> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.

---

## How to read this index

Each provider has:
- **Canonical status** — `TRACKED` (in git) / `QUARANTINED` (moved to `.archive/2026-06-27-stub-batch/`) / `MISSING`
- **F11 audit status** — `ACTIVE` / `PARTIAL` / `DRAFT` / `BLOCKED` / (not yet graded)
- **Substrate evidence** — does the file contain `substrate_evidence` / `promotion_evidence` / `cooling_ledger_ref` blocks? (the canonical schema requirements)
- **Status field** — what the file declares as its promotion status

Status legend:
- ✅ complete · ⚠️ partial · ❌ missing · 🔒 quarantined (stub, awaiting F13)

---

## Canonical tracked providers (in git)

7 provider pairs (14 files), all blessed by F13 in commits between 2026-06-12 and 2026-06-22.

| # | Provider | Soul / Shadow | Status (declared) | F11 | Substrate Evidence | Cooling Ledger | Sources | First commit |
|---|----------|---------------|-------------------|-----|-------------------|----------------|---------|--------------|
| 1 | **anthropic** | [soul](anthropic_soul.yaml) / [shadow](anthropic_shadow.yaml) | ACTIVE (shadow) | — | ❌ | ❌ | ✅ sources list | `aab4daa6` 2026-06-12 |
| 2 | **deepseek** | [soul](deepseek_soul.yaml) / [shadow](deepseek_shadow.yaml) | PRIMARY_FEDERATION_MODEL | — | ❌ | ❌ | ❌ | `ed61cd31` 2026-06-12 |
| 3 | **ilmu** (nemo_nano) | [soul](ilmu_soul.yaml) / [shadow](ilmu_shadow.yaml) | BLOCKED (soul) | — | ⚠️ partial | ❌ | ❌ | `0135534e` 2026-06-15 |
| 4 | **kimi** (k2.7_code) | [soul](kimi_soul.yaml) / [shadow](kimi_shadow.yaml) | PROPOSED_SELF_ASSESSMENT | — | ⚠️ partial | ✅ (kimi has cooling_ledger_ref) | ❌ | `7ad598e8` 2026-06-16 |
| 5 | **minimax** | [soul](minimax_soul.yaml) / [shadow](minimax_shadow.yaml) | RATE_LIMITED_SECONDARY | — | ❌ | ❌ | ❌ | `ed61cd31` 2026-06-12 |
| 6 | **qwen** | [soul](qwen_soul.yaml) / [shadow](qwen_shadow.yaml) | PROPOSAL | — | ❌ | ❌ | ❌ | `ed61cd31` 2026-06-12 |
| 7 | **xiaomi_mimo** | [soul](xiaomi_mimo_soul.yaml) / [shadow](xiaomi_mimo_shadow.yaml) | FALLBACK | — | ✅ full substrate | ✅ 3 refs | ❌ | `0135534e` 2026-06-15 |

### Companion files
- `gpt/GPT_FAMILY.md` — standalone OpenAI GPT family tracker (separate canonical format, NOT soul/shadow split). Tracked `2202dc61` 2026-06-22.
- `kimi_middleware_phase1/` — Kimi K2.7 middleware code (SYSTEM_MD.md, config.toml, aaa-pre-govern.sh, kimi_k27_cooling_probe.py). Tracked `16d88f9e` 2026-06-16.

### Master files
- `model_soul.yaml` — canonical schema definition (30 KB, v4). Lists `shadow_incidents` + `models[]` with the **gold-standard** shape that the soul/shadow files should match.
- `FEDERATION_MODEL.json` — master JSON registry with provider routing + rate-limit metadata. Already references `groq` and `ollama` with API key paths.

---

## Quarantined providers (held for enrichment)

12 provider pairs (24 files) in `.archive/2026-06-27-stub-batch/`, awaiting F13 enrichment ratification.

🔒 All were untracked stubs claiming `forged_by: FORGE (000Ω) via asal.py`. Verified: `asal.py` does NOT write yaml files. Provenance field is inaccurate.

| # | Provider | Coverage | Recommended action |
|---|----------|----------|--------------------|
| 1 | **google_gemini** | 🔒 stubs only | Enrich with substrate evidence |
| 2 | **xai_grok** | 🔒 stubs only | Enrich or HOLD |
| 3 | **zhipu_glm** | 🔒 stubs only | Enrich or HOLD |
| 4 | **nvidia_nemotron** | 🔒 stubs only | Enrich or HOLD |
| 5 | **stepfun** | 🔒 stubs only | Enrich or HOLD |
| 6 | **tencent_hunyuan** | 🔒 stubs only | Enrich or HOLD |
| 7 | **sakana_fugu** | 🔒 stubs only | Enrich or HOLD |
| 8 | **bytedance_seed** | 🔒 stubs only | Enrich or HOLD |
| 9 | **kuaishou_kling** | 🔒 stubs only | Enrich or HOLD |
| 10 | **microsoft_mai** | 🔒 stubs only | Enrich or HOLD |
| 11 | **miromind** | 🔒 stubs only | Enrich or HOLD |
| 12 | **tokenrouter** | 🔒 stubs only | Enrich or HOLD |

## Deleted as duplicates (F13 ratification 2026-06-27)

3 provider pairs (6 files) removed permanently — info was canonical elsewhere:
- ✅ `openai_{soul,shadow}.yaml` — canonical at `gpt/GPT_FAMILY.md`
- ✅ `groq_{soul,shadow}.yaml` — canonical at `FEDERATION_MODEL.json`
- ✅ `ollama_{soul,shadow}.yaml` — canonical at `FEDERATION_MODEL.json`

See `.archive/2026-06-27-stub-batch/README.md` for restoration note (not applicable — files deleted).

---

## Coverage gaps (providers we know exist but no registry entry)

| Provider | Reason missing | Priority |
|----------|---------------|----------|
| **Hugging Face inference (Qwen2-0.5B)** | Used in ASAL eval but no soul/shadow pair | Medium |
| **SGLang / vLLM** | Self-hosted, not yet catalogued | Low |
| **Apple Foundation Model** | Pydantic AI integration only | Low |
| **Cohere Command** | Not subscribed | Low |

---

## Canonical schema (from `model_soul.yaml` v4)

A well-forged soul/shadow pair should contain:

```yaml
# Identity
model_id: <canonical-string>             # e.g. "xiaomi_mimo"
model_family: <vendor family>            # e.g. "Xiaomi MiMo (小米 MiMo)"
provider: <vendor legal entity>
endpoint: <canonical URL>
license: <proprietary|open-source>

# Status
status: <ACTIVE|PARTIAL|DRAFT|FALLBACK|BLOCKED|RATE_LIMITED_SECONDARY|...>
canonical_series: <current canonical version>
legacy_series_under_migration: [<prior versions>]

# Evidence (REQUIRED for F11 audit)
substrate_evidence:
  wired_at: '<ISO timestamp>'
  key_path: <secrets path>
  endpoint: <live URL>
  plan: <plan tier + renewal>
  primary_consumer: <consumer file>
  smoke_tests: [<list of pass results>]
  f11_audit_status: <PARTIAL|ACTIVE|...>
  promotion_blocker: <what's missing for next grade>

# Live tests
live_evidence_<date>:
  test: <test name>
  models_tested: [<list>]
  results: {<model>: {verdict: PASS|FAIL, content_delivered: ..., ...}}
  finding: <narrative>
  epistemic: <n for sample size>

# Authority
sources:
  - <url list>

# Federation
agents_using: [<list of agents currently consuming>]
cooling_ledger_ref: vault://path/to/cooling/receipt
cooling_ledger_path: /root/path/to/cooling/file.json
```

### Coverage of canonical schema across tracked providers

| Field | anthropic | deepseek | ilmu | kimi | minimax | qwen | xiaomi_mimo |
|-------|-----------|----------|------|------|---------|------|-------------|
| `model_id` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `provider` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `endpoint` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `status` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `canonical_series` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `substrate_evidence` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| `live_evidence_*` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| `sources` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `agents_using` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `cooling_ledger_ref` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| `f11_audit_status` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Richness score** | 4/11 | 3/11 | 5/11 | 6/11 | 3/11 | 3/11 | **9/11** |

**Finding:** Only `xiaomi_mimo` (the most recently promoted provider) has full canonical coverage. The other 6 are partial — they have identity + status but lack substrate/live-evidence chains.

---

## Routing posture (from `FEDERATION_MODEL.json`)

For reference, `FEDERATION_MODEL.json` already encodes the following routing decisions:

- `general_queries`: DeepSeek primary, Groq secondary (free tier), Ollama last-resort
- `code_infra_tools`: DeepSeek primary, Groq (llama-4-maverick fast code), Ollama fallback
- `high_throughput`: Groq
- `openai` access: via `tokenrouter` (Anthropic-style proxy)
- **Many providers in FEDERATION_MODEL.json have NO soul/shadow pair** (these are the gap providers)

---

## TokenRouter Top-7 FFF Smoke Evaluation (2026-06-30)

A fast smoke run of the seven TokenRouter flagship models against the `ariffazil/FFF` Federation Fitness Gate is recorded here:

- [TOKENROUTER_FFF.md](TOKENROUTER_FFF.md)

**Bottom line:** MiMo-V2.5-Pro and DeepSeek-V4-Pro passed all smoke gates. GPT-OSS-120B fabricated a historical event (G2 Truth fail). Kimi-K2.7-Code returned API errors via TokenRouter. Qwen-3.7-Max, GLM-5.1, and MiniMax-M2.7 had partial endpoint errors leaving gates untested.

---

## Audit trail

| Date | Action | Authority |
|------|--------|-----------|
| 2026-06-12 | First model registry commit (`ed61cd31`) | F13 |
| 2026-06-12 | Anthropic stack added (`aab4daa6`) | F13 + Hermès |
| 2026-06-14 | KIMI K2.7 shadow/soul (`7ad598e8`) | F13 |
| 2026-06-15 | ILMU + MiMo promoted (`0135534e`) | F13 |
| 2026-06-16 | Kimi middleware Phase 1 (`16d88f9e`) | F13 |
| 2026-06-22 | Semantic reorg — `gpt/` subfolder + `GPT_FAMILY.md` (`2202dc61`) | F13 |
| 2026-06-27 | **Audit + quarantine of 28 stub files** (this index) | F13 directive |

---

*Forged 2026-06-27 by FORGE (000Ω) — MiniMax-M3*
*Per F13 SOVEREIGN directive: "audit model registry in AAA github repo. please organize the model registry accordingly"*
*DITEMPA BUKAN DIBERI*