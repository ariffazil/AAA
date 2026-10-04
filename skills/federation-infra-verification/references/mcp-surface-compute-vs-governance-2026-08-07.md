# arifOS MCP Surface: Compute vs Governance Boundary

> Probed: 2026-08-07 by Hermes ASI (session probe, not code trace).
> Kernel version: `ARIFOS MCP kanon-2026.08.07+8bbcb36`

## 1. The `/mcp` endpoint is stateless for reads

The arifOS `/mcp` route accepts JSON-RPC 2.0 payloads and does NOT require MCP handshake for listing operations:

| Operation | Handshake needed? | Works? |
|---|---|---|
| `tools/list` | No | ✅ Returns all 8 tools |
| `resources/list` | No | ✅ Returns all 42 resources |
| `prompts/list` | No | ✅ Returns all 20 prompts |
| `resources/read` | No | ✅ Returns resource content |
| `tools/call` | **Yes** (initialize → notifications/initialized → tools/call) | Works with handshake |
| `tools/call` (no handshake) | — | ⚠️ Returns with `status: "degraded"`, `actor: "anonymous"`, `session_id: "unknown"` |

**Implication:** You can audit the entire surface (tools, resources, prompts, their schemas and content) via a single `curl -X POST :8088/mcp` without any auth. This is by design — the surface is the *constitution*, readable by all. Execution (tool calls) is gated by SCT/session binding.

## 2. The 8 tools are governance gates, not compute engines

Every tool returns a **verdict envelope** — a structured JSON containing:
- `verdict`: SEAL / HOLD / SABAR / VOID / pending
- `confidence`: 0.0–1.0 (or "N/A — deterministic")
- `metacognition`: confidence_band, uncertainty_reason, evidence_strength, failure_modes
- `audit_provenance`: call_hash, trace_id, kernel_signature_anchor
- `next_safe_action`: what to do next

What each tool actually does when called:

| Tool | Looks like it... | Actually does... | Computes numbers? |
|---|---|---|---|
| `arif_init` | Initializes session | Binds actor identity, returns session_id (may be "unknown" for anonymous) | No |
| `arif_observe` | Fetches/observes data | Returns verdict on whether observation is authorized (HOLD for anonymous) | No |
| `arif_think` | Reasons/analyzes | Returns HOLD with violated_laws list — "you can't think yet, prove the floor" | No |
| `arif_route` | Routes to correct tool | Returns SEAL + organ suggestion (but the suggestion is generic, not specific) | No |
| `arif_memory` | Recalls memories | Returns verdict on whether memory recall is authorized | No |
| `arif_judge` | Judges a proposal | Returns advisory verdict (confidence: 0.65 ADVISORY_ONLY) checking F1–F13 | No |
| `arif_forge` | Executes something | Returns execution receipt (but requires prior judge SEAL) | No |
| `arif_seal` | Seals to VAULT999 | Returns immutable receipt (requires full chain) | No |

**The kernel governs the ACT OF REASONING, not the CONTENT of reasoning.** It can tell you "your proposal violates F7 humility because you claimed 99% confidence" but it cannot tell you "use 0.47 momentum and 0.53 mean-reversion."

## 3. The 42 resources are constitution and context, not data

Key resource categories with actual content:

| Resource | Content type | Useful for math? |
|---|---|---|
| `arifos://doctrine` | 13-floor contract (F1–F13 definitions) | No — defines constraints, not solutions |
| `arifos://floors` | Floor table with verdict taxonomy | No — governance meta-data |
| `arifos://flow-state` | FQ score (live from arifFlow :7073) | No — metabolic pulse, not market data |
| `arifos://affordances` | Action-class taxonomy (OBSERVE/EXECUTE/IRREVERSIBLE) | No — risk classification |
| `arifos://atlas333/geometry` | 3 territories × abstract shapes (euclidean/hyperbolic/fractal/spherical/toroidal/crystalline) | **No — philosophical metaphor, not a weight matrix** |
| `arifos://atlas333/paradox/list` | List of 35 paradoxes | No — conceptual framework |
| `arifos://vitals` | Federation health snapshot | No — ops meta-data |
| `arifos://carry-forward` | Prior session state | No — session continuity |
| `arifos://bootstrap` | Federation context for new agents | No — onboarding |
| `arifos://epistemic` | Epistemic label definitions | No — labeling schema |
| `arifos://vault/head` | Last VAULT999 entry | No — seal chain head |
| `skill://index` | Federation skill catalog | No — skill meta-data |

## 4. The geometry resource is NOT a runtime weight matrix

`arifos://atlas333/geometry` returns:

```
Memory → euclidean, hyperbolic, fractal  (depths: surface, deep, emergent)
Mind   → euclidean, spherical, toroidal  (depths: surface, intimate, recursive)
Judge  → crystalline, singular, hyperbolic (depths: constitutional, absolute, deep)
```

These are **epistemic territory descriptors** — how to think about each domain — not computational weight vectors. They tell the reasoning model "memory is fractal (self-similar across scales)" not "memory_weight = [0.3, 0.5, 0.2]".

The flow-state resource explicitly warns: `"geometry_note": "FQ ≠ G ≠ RASA ≠ J-space. Do not fold FQ into G."` — these are orthogonal conceptual spaces, not composable metrics.

## 5. The 20 prompts are governance lifecycle templates

| Prompt | Role | Computes? |
|---|---|---|
| `/init`, `//init` | 10-step boot sequence template | No — scaffold |
| `/seal`, `//seal` | 11-step close ritual template | No — scaffold |
| `🌱 BOOT` | Constitutional bootstrap | No — onboarding |
| `🌊 WITNESS` | Observe ground-truth signals | No — methodology |
| `🧠 REASON` | Propose hypotheses | No — methodology |
| `⚖ MARUAH` | Dignity-floor check | No — methodology |
| `🔍 PREFLIGHT` | Pre-operation F1-F13 check | No — methodology |
| `🔒 JUDGE` | Constitutional gate | No — gate |
| `🔥 FORGE` | Execute after SEAL | No — gate |
| `💎 SEAL` | VAULT999 append | No — gate |
| `🌀 SABAR` | Governed 6-stage reality-loop | No — methodology |
| `📜 REPLY` | Governed AGI reply envelope | No — methodology |
| + 8 legacy aliases | Deprecated → emoji prompts | No |

## 6. Correct organ routing for computational tasks

| Task type | Right organ | Why |
|---|---|---|
| Trading weight optimization | **WEALTH** (:18082) | Has riskfolio-lib, pyportfolioopt, quantlib |
| Seismic/petrophysical computation | **GEOX** (:8081) | Has scipy, pylops, scikit-learn, numpy |
| File execution, code gen, build | **A-FORGE** (:7071/:7072) | Has forge_shell, ephemeral tool gen |
| Constitutional validation of a proposal | **arifOS** (:8088) | THIS is what the kernel does — check F1-F13 |
| Session management / identity binding | **arifOS** (:8088) | arif_init, SCT tokens |

**The pattern:** `math → judge`, not `judge → math`. Do the computation in the domain organ, then pass the proposal to arifOS for constitutional validation.

## 7. Implication for LLM reasoning models (Opus 5, etc.)

If you wire arifOS MCP into an LLM's context (as Claude apps or OpenAI tools):

1. **The tools will constrain WHAT the model can say** (governance) but NOT HELP it say correct things (computation)
2. **The resources provide constitutional context** that shapes epistemic behavior (humility, evidence labeling, uncertainty caps) — valuable for safety, not for accuracy
3. **The geometry/atlas resources are conceptually rich but numerically empty** — they shape the *style* of reasoning (fractal vs euclidean memory) but not the *content* (specific weights)
4. **For a model like Opus 5 to find correct XAUUSD weights**, it needs: (a) OHLCV data, (b) a quantitative library (riskfolio-lib), and optionally (c) arif_judge to validate the resulting proposal against F1-F13
5. **The kernel will likely HOLD** any uninitialized probe — this is correct F13 behavior, not a bug

## 8. Surface inventory snapshot (2026-08-07)

- **Tools:** 8 (canonical `arif_*` verbs only — no megamemory_*, atlas_*, eureka_*)
- **Resources:** 42 (38 static + 4 templates)
- **Prompts:** 20 (8 canonical emoji + 12 legacy aliases, all deprecated after 2026-09-16)
- **Server:** ARIFOS MCP kanon-2026.08.07+8bbcb36
- **Protocol:** Streamable-HTTP MCP (JSON-RPC 2.0), stateless reads, stateful writes
