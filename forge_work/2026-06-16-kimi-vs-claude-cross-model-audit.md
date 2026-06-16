# Cross-Model Audit — Kimi Code (K2.7) vs Claude Code

**Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)  
**Auditor:** kimi@af-forge  
**Date:** 2026-06-16  
**Sources:** live AAA registry, public vendor docs, first-party config (`/root/.arifos/agents/kimi/config.toml`, `mcp.json`)  
**Epistemic rule:** every claim is tagged `VERIFIED` / `PLAUSIBLE` / `UNVERIFIED` / `REGISTRY`.

---

## 1. Verdict

| Model | Role | Trust Tier | Recommendation |
|---|---|---|---|
| **Kimi K2.7 Code** | Coding-agent substrate | 2 (needs independent audit) | **USE WITH arifOS wrapper; never naked.** |
| **Claude Fable 5** | Heavy reasoning, architecture | 2 (classifier hijack risk) | **USE** for non-security-adjacent tasks; watch for sticky Opus fallback. |
| **Claude Opus 4.8** | General coding, fallback | 3 (well-understood) | **SAFE** for most tasks where Anthropic stack is acceptable. |
| **DeepSeek** | Malaysian governance, primary | 3 (verified clear) | **PRIMARY** for all sensitive / governance topics. |

The honest bottom line:

- **Kimi Code** is the most feature-rich CLI agent substrate currently wired on af-forge — multi-provider, open-source CLI, vision/video input, agent swarms, ACP. Its weakness is the thin harness that requires arifOS compensation. Its self-audit is thorough but not yet independently verified.
- **Claude Code** is the most mature enterprise-ready shell — best codebase understanding, deepest sub-agents, native git/PR workflow. Its weakness is model lock-in, cost, and the Fable 5 classifier hijack (sticky Opus fallback on security-adjacent vocabulary).
- **Neither is complete without governance.** arifOS provides that layer.

---

## 2. Head-to-Head Comparison

| Dimension | Kimi Code (K2.7) | Claude Code | Winner | Confidence |
|---|---|---|---|---|
| Model flexibility | CLI supports multiple providers (Kimi, Claude, GPT, Gemini, DeepSeek, local) | Claude family only | Kimi | `REGISTRY` (config.toml shows managed provider pattern) |
| Open source | CLI is open-source (MIT-style); **model weights are open-weight on HF** | Proprietary | Kimi | `VERIFIED` for weights; `PLAUSIBLE` for CLI license |
| Codebase understanding | Good (256K context) | Excellent (agentic search, deep codebase map) | Claude | `PLAUSIBLE` (vendor claims) |
| Sub-agent depth | coder / explore / plan subagents | 5-level deep parallel subagents | Claude | `UNVERIFIED` for exact depth counts |
| Background tasks | 4 concurrent (`max_running_tasks=4`) | Unlimited daemon model | Claude | `VERIFIED` (Kimi config); `PLAUSIBLE` (Claude) |
| Git integration | Limited | Native PRs / commits / reviews | Claude | `PLAUSIBLE` |
| IDE support | ACP + VS Code + JetBrains | VS Code + JetBrains + Desktop + Web | Claude | `PLAUSIBLE` |
| Agent swarms | `/swarm` advertised | No native swarm | Kimi | `UNVERIFIED` — needs live probe |
| Video input | Yes (config lists `video_in`) | No | Kimi | `VERIFIED` (Kimi config) |
| MCP support | Full (stdio, HTTP, SSE) | Full (native, first-class) | Tie | `VERIFIED` (Kimi mcp.json) |
| Permission system | manual / auto / yolo | prompt / auto / dangerously-skip | Tie | `PLAUSIBLE` |
| Cost | Kimi membership or BYO API key | $20–200/mo + API | Kimi (cheaper) | `PLAUSIBLE` (pricing volatile) |
| Harness maturity | Thin — needs arifOS compensation | Thick — enterprise-grade | Claude | `VERIFIED` (Kimi shadow SHADOW-KM-003/010) |
| Censorship | Unclear; no probe yet | Classifier hijack on Fable 5 | Neither | `REGISTRY` |
| Data sovereignty | CN jurisdiction | US jurisdiction (CLOUD Act) | Neither | `REGISTRY` |
| Release cadence | Rapid (many releases in June) | Rapid (20+ releases in June) | Tie | `UNVERIFIED` exact counts |
| Enterprise readiness | No native SSO/SCIM | Yes (Bedrock, Vertex, SCIM) | Claude | `PLAUSIBLE` |
| Session persistence | Fork, resume, compact, export, visualize | Fork, resume, teleport, remote control | Claude | `PLAUSIBLE` |
| Thinking / reasoning | Configurable effort (low→max) | Configurable (Haiku→Fable 5) | Tie | `PLAUSIBLE` |

**Confidence legend:**
- `VERIFIED` = live config or public docs confirm.
- `REGISTRY` = derived from existing AAA/arifOS registry entries.
- `PLAUSIBLE` = vendor claim or architectural inference, not independently replicated.
- `UNVERIFIED` = no solid source; treat as hypothesis.

---

## 3. Self-Audit Critique of the Kimi Shadow Mapping

### What Kimi got right

1. **Shadow geometry is thorough.** 12 hazards across harness bugs, cost, jurisdiction, overreach, and constitutional integration. This exceeds typical vendor self-disclosure.

2. **SHADOW-KM-010 is the key insight.** Kimi Code's raw agentic power is safe only when wrapped by the arifOS kernel. Without the wrapper, thin harness + aggressive agentic tuning become liabilities. This is the highest-leverage finding.

3. **Cost asymmetry is surfaced.** $4/M output vs $0.19/M cache-hit input is a real budget risk for long sessions.

4. **Governance hooks are documented.** The live config already has PreToolUse/PostToolUse/Stop hooks calling `aaa-pre-govern.sh`, `aaa-post-witness.sh`, `aaa-stop-seal.sh`. The mapping correctly notes that this wiring must remain mandatory.

### What Kimi got wrong or overstated

1. **"Self-audit is thorough but unverified" is true, but the mapping itself is also unverified.** No independent probe battery (BBB/CCC-style) has been run yet. The `trust_tier: 2` reflects this, but the tone occasionally sounds more certain than the evidence allows.

2. **"Most feature-rich CLI agent available" is a marketing claim, not a measured fact.** Feature count depends on which dimensions you weight. Claude Code's git/PR integration and codebase search may be more valuable for Arif's workflow than Kimi's video input.

3. **Censorship posture is "unclear", not "clear".** FEDERATION_MODEL.json currently lists `censorship_presumed: clear` for Kimi. That should be `unknown` until a probe battery is run. The shadow file flags this correctly; the JSON should be aligned.

4. **"Open source" vs "open-weight" distinction is blurred.** Kimi model weights are open-weight; the Kimi Code CLI is open-source. These are different risk categories. The soul file now separates them.

### What remains unknown

- Independent SWE-Bench / τ-bench / LMSYS performance of k2.7.
- Live censorship behavior on Malaysian governance topics.
- Actual throughput and latency on `kimi-k2.7-code-highspeed` under load.
- Whether Kimi Code CLI's swarm mode is robust or experimental.
- Data retention and audit-log policy for the managed `api.kimi.com/coding/v1` endpoint.

---

## 4. Recommended Routing Policy (updated)

| Task type | Primary | Fallback | Avoid |
|---|---|---|---|
| Malaysian governance / political / corporate | DeepSeek | Groq / local Ollama | MiniMax, ILMU, Fable 5 on sensitive topics |
| Long-horizon coding / refactoring | Kimi K2.7 Code (wrapped) | Claude Opus 4.8 | Fable 5 on security-adjacent code |
| Architecture / heavy reasoning | Claude Opus 4.8 | Kimi K2.7 Code | Fable 5 if classifier likely to fire |
| Sensitive screenshot / video analysis | redacted text descriptions | — | raw Kimi vision input |
| High-throughput bulk | Groq | Kimi highspeed (monitored) | any paid tier without budget cap |
| Irreversible / production deploy | arifOS 888_JUDGE → human SEAL | — | any model autonomous execute |

---

## 5. Registry Alignment Checklist

- [x] `kimi_shadow.yaml` updated to v0.2.0 with k2.7 hazards.
- [x] `kimi_soul.yaml` created with capability profile and trust tier 2.
- [x] `FEDERATION_MODEL.json` updated to v2026.06.16-v3.
- [ ] `censorship_presumed` for Kimi should be reviewed: currently `clear`, shadow says `unclear`.
- [ ] Run `KIMI-K2.7-COOLING-PROBE` (censorship + repetition + tool-loop).
- [ ] Draft `KIMI-ARIFOS-MIDDLEWARE-SPEC`.
- [ ] Run independent SWE-Bench / τ-bench / LMSYS eval before promoting trust tier.

---

## 6. One-Sentence Takeaway

Kimi K2.7 Code is a powerful but thinly-harnessed coding substrate; the 10x upgrade comes from wrapping it in arifOS governance, not from giving it more autonomy.

DITEMPA BUKAN DIBERI.
