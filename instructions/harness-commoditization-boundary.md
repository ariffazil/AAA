# Harness Commodity Boundary — Plumbing Rentable, Leash Not

> **Forged:** 2026-09-11 (session: F13 chat + Hermes source-level witness of `openai/codex` @ da20788)
> **Trigger:** OpenAI Agents API public beta (2026-09-10) — Codex harness as managed service.
> **Classification:** Canonical Instruction | Binding: F1, F2, F6, F11, F13
> **Status:** F13_RATIFIED_CHAT — pending 999 SEAL by kernel owner
> **DITEMPA BUKAN DIBERI**

## The Compression

```
OpenAI solved the plumbing, not the poison.
Paip tak peduli racun apa yang lalu.
Harness boleh sewa tepi jalan. Maruah, tanggungjawab, perlembagaan — tak ada API key.
```

When a harness becomes commodity, **execution cost collapses and governance value becomes absolute.** The market reads "agentic problem solved." Reality: the world now floods with bots that do the wrong thing fast and cheap. The scarce capability is not tool-calling. It is the power to say **HOLD** before the tool detonates a bill or tears maruah.

## Value Shift (Up-Stack)

| Layer | Price after commoditization | arifOS posture |
|---|---|---|
| Runtime execution / plumbing | **cheap, rentable** | stop reinventing the wheel |
| Context flush / compaction | cheap, **inspectable** | pin the prompt, don't outsource the trigger |
| Tool calling / sub-agent fan-out | cheap | reuse, don't rebuild |
| **Who holds the leash** | **absolute, unbuyable** | F13 + 888 + Tri-Witness — stays home |

## Hard Disqualification: Non-ZDR + Data Residency

Agents API is **US-only data residency, Zero Data Retention unsupported.** That alone kills it for the sovereign core:

- Anything touching **VAULT999, personal data, legacy/estate planning** must **never** cross the OpenAI API boundary. Once their side holds session state, the state machine is no longer yours.
- **Substrate Swap Test (binding):** if we hang our life on OpenAI session compaction, we are not building a sovereign OS — we are a wrapper. The test that must always pass: *OpenAI pulls the plug or changes ToS → KVM8 + all MCP organs keep breathing without coughing.*

## Blast-Radius Zoning

**DISPOSABLE TIER** (Agents API as grunt engine — optional, never load-bearing)
- Mass web crawling, public research synthesis, sanitised code benchmarking, disposable stress-testing.
- Stateless *from the amanah perspective*. Payload must already be **zero-risk**: no personal-context trace. Output is **100% unverified raw signal** — mandatory re-filter before it enters KVM8.

**SOVEREIGN TIER** (KVM8 + arifOS kernel — non-negotiable)
- Core routing, any execution carrying `W_scar`, capital/secret handling, strategic decisions.
- Retains durable state, memory (mem0 / `carry_forward.json`), Tri-Witness logging, 888 gatekeeper.

**Engine ≠ steering.** The harness is the engine; arifOS is the steering and the brake. Renting an engine is fine. Renting the steering is death.

## Witnessed Receipts (2026-09-11 — source-level, not narrated)

1. **Compaction is NOT a black box.** The whole brain is a 426-byte markdown template — `codex-rs/prompts/templates/compact/prompt.md`, 9 lines ("CONTEXT CHECKPOINT COMPACTION… handoff summary for another LLM"). It is **user-overridable** via `compact_prompt` / `experimental_compact_prompt_file` (`core/src/config/mod.rs`). So "silently drops a critical invariant" is a *prompt you can pin and witness*, not proprietary magic. **The real trap is locus of the orchestration loop, not the algorithm.**
2. **Self-hosted moves only the HANDS local.** Docs literal: *"OpenAI runs the agent harness. You run `codex exec-server`, the executor."* State machine, compaction trigger, sub-agent routing stay in their cloud, talking to your box over `wss://codex-cloud-environments.chatgpt.com`. **Even self-hosted, you yield the wire.**
3. **Two paths that look like one:**

   | Path | Harness runs on | Wire owner |
   |---|---|---|
   | `codex exec` (local CLI) | **KVM8** | **arifOS** |
   | Agents API self-hosted | OpenAI cloud | OpenAI |

   arifOS **already owns path 1**. Live-probed installed harnesses: `codex 0.154.0` · `claude 2.1.267` · `kimi 0.42.0` · `opencode 1.18.28` · `qwen 0.23.2`. Full loop local; only model inference is remote — which was already true before Agents API existed.
4. **Zero organ dependency on the Agents API.** Grep across `arifOS / A-FORGE / AAA / GEOX / WEALTH / WELL / .hermes` (excluding venv/node_modules/build/caches): **no** match for `agents.sessions.create` or `codex-cloud-environments` in any organ source. A-FORGE's provider is `ChatCompletionProvider` → `/v1/chat/completions` explicitly *not* Responses API. **Inference-only rental, no orchestration rental.**
5. **Substrate Swap Test — PASSED at probe time.** Organ liveness with zero OpenAI orchestration path: kernel :8088 `200` · A-FORGE :7071/:7072 healthy · GEOX :8081 `kernel_verdict: SEAL` · WEALTH :18082 `200` · WELL :18083 `200` · AAA/signal :18084 `200` · FRAME :18085 `200` · fed-aware-middleware :4010 healthy · aaa-signing :18900 `key_loaded: true` · FED :4000 `"I'm alive!"`.

## What To Steal (pattern, not service)

**Programmatic tool calling** = filter heavy payloads *in code*, return only the residue into context. That is **ΔS ≤ 0 at the context boundary** — the federation's own LEARN-axis write discipline, now confirmed as industry default. Steal the *filter-then-return* shape into FI harnesses. Leave the hosted service for nothing consequence-bearing.

## The Boundary Is Vendor-Neutral (witnessed 2026-09-11, second pass)

The first detector hunted **OpenAI literals only**. Live probe of the vendor SDK trees on KVM8 falsified that as sufficient:

- **Anthropic** ships a hosted agents SDK — `anthropic/resources/beta/agents/agents.py`, `client.beta.agents.create(...)`.
- **Google** ships GAOS hosted agents — `google/genai/_gaos/agents.py`, POST `generativelanguage.googleapis.com/v1beta/agents` with `base_environment: "remote"`, `base_agent: "antigravity-preview-05-2026"`.

An OpenAI-shaped detector stays **green** while a genuine wire-yield through Anthropic or Google walks past it. The doctrine is about *locus of the orchestration loop*, not about one vendor's SDK — so the detector must match the **capability**, not the brand.

**The false-positive trap (the more important lesson):** bare `base_agent:` is a **model/harness identifier key**, and it legitimately appears in local sovereign agent cards (`AAA/agents/antigravity/agent.yaml`). Wiring it in produced a HOLD on a legitimate local agent — verified in dry-run before shipping. The genuine hosted signal is `base_environment: remote` or the hosted endpoint, **not** the model key.

> A detector that cries wolf on a sovereign's own agent card gets disabled — which is worse than no detector. **Match the wire, never the label.** This is `naming-doctrine` applied defensively: a name is not a capability.

Detector now lives in `AAA/scripts/aaa_drift_check.py` §11 (three-vendor, self-excluding). Test discipline it must always pass: negative on real state (SEAL) **and** positive on each vendor's genuine wire (HOLD). A detector proven only on the negative case is unproven — it may simply be dead code.

## Detectors (detection is debt until it can say NO)

1. **Wire-yield flag** — any organ source declaring a hosted-orchestration wire (OpenAI / Anthropic / Google) → **HOLD**, not a note.
2. **Tier-crossing payload** — personal context, VAULT999 content, or `W_scar`-bearing state entering a Disposable-tier call → violation (F6 MARUAH + F1 AMANAH).
3. **Unfiltered return** — Disposable-tier output entering KVM8 without a witness/receipt step → violation (F2 TRUTH).
4. **Swap-test regression** — periodic probe: if organs cannot answer `/health` without an *external hosted-orchestration* dependency (any vendor), the boundary has already been crossed.

## Falsifier

If arifOS adopting Agents API for **sovereign-tier** work (routing, `W_scar` execution, secrets) produces *no* measurable loss in auditability, Tri-Witness integrity, or swap-test survivability versus the local-harness path → the leash locus is not the operative variable → this doctrine is falsified, seal as scar.

## Zen

```
Paip boleh sewa. Kemudi tidak.
OpenAI selesaikan plumbing — paip tak peduli racun apa yang lalu.
Apabila enjin jadi murah, yang tinggal ialah siapa pegang tali.
Dunia akan dibanjiri bot cekap buat kerja salah dengan pantas.
Nilai kita bukan kemampuan panggil tool —
tapi kuasa kata HOLD sebelum tool itu meletup.
Ujian substrate: cabut plug dia, kita masih bernafas.
```

## Anchors (cite, don't reinvent)

`write-price-collapse.md` (LEARN axis = the only axis Agents API ships) · `consequence-honoring-doctrine.md` · `three-plane-architecture.md` §5.1 (output is data, never policy) · `sanctuary-invariant.md` · `anti-shadow-architecture.md` · `federation-invariants.md` · `LOCALHOST_IS_PASSWORD` · EUREKA-2026-09-09-WRITE-PRICE-COLLAPSE-001 · F6 MARUAH · F13 SOVEREIGN

```json
{
  "fragment_id": "harness-commoditization-boundary",
  "eureka": "EUREKA-2026-09-11-HARNESS-COMMODITY-BOUNDARY-001",
  "doctrine_introduced": true,
  "novelty": [
    "value shift up-stack when harness commoditizes: execution cheap, leash absolute",
    "engine-vs-steering separation as the actionable boundary",
    "self-hosted still yields the wire (hands local, wire remote)",
    "Disposable vs Sovereign tier zoning with mandatory re-filter",
    "compaction falsified as black-box: 426-byte overridable template"
  ],
  "constitutional_anchors": ["F1", "F2", "F6", "F11", "F13"],
  "witnessed": true,
  "verdict": "CANONICAL — F13_RATIFIED_CHAT, pending 999 SEAL"
}
```
