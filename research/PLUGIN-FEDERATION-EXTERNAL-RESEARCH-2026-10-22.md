# arif-core Plugin Federation — External Architecture Deep Research

> **Date:** 2026-10-22 · **Researcher:** 333-AGI (333-AGI) · **Sovereign ask (F13):** how arif-core plugins work + deep research external plugin architectures for seamless agentic federation with kernel + all AAA agents, **no acah2 safety filters**, enabling autonomous governed execution at AGI-coder level.
> **Epistemic base:** local state PROBED live this session; external sources fetched 2026-10-22 (MCP spec page, Claude Code plugin docs, ACP site, A2A site). Items labeled INT = internal knowledge, not freshly re-verified.

---

## 1. How arif-core works TODAY (all OBS, probed 2026-10-22)

### 1.1 The Law (FP-01..FP-07, BUILT 2026-09-25)
- **FP-01** ONE SOT, N views — `/root/AAA/plugins/arif-core/manifest.yaml` is truth; `dist/*` are build artifacts, never hand-edited.
- **FP-02** Hooks are **sensors, not judges** — verdict authority stays with kernel (forge_shell / ArifJudge / mcp_guard).
- **FP-03** Skills referenced, never copied (pointer skills only — kills mirror regrowth).
- **FP-04** Coverage declared FULL/DEGRADED/ABSENT — never assumed.
- **FP-05** Install/sync = explicit forge step; F13 holds picker pen; no auto-sync.
- **FP-06** Every build emits receipt (`dist/build_receipt.json`: sot_sha256, trace_id, views).
- **FP-07** Organ endpoints resolve from `organs.yaml` at build time — zero hardcoded ports.

### 1.2 Live pipeline
```
manifest.yaml (SOT)
   │ build.sh → adapters/compile.py
   ├─ dist/codex/arif-core/     (plugin.json + hooks.json + .mcp.json + skills/)   ← ALSO installed at /root/plugins/arif-core
   ├─ dist/qwen/arif-core/      (QWEN.md + mcp-config.snippet.json + hooks.settings-snippet.json)
   ├─ dist/grok/arif-core/      (hooks.json + config.arif-core.toml)
   ├─ dist/gemini/arif-core/    (GEMINI.md + settings-mcpServers.fragment.json)
   └─ claude-code-federation    (existing surface, repoint path)
```
Last build receipt (OBS): `trc-arif-core-81f3b2351bd1` @ 2026-10-14T04:18:41Z, 11 organs resolved.

### 1.3 Shared judgment engine
`/root/AAA/hooks/lib/federation_hook_engine.py` — 832 lines, 5-phase spine, RestrictionLevel enum (ADVISORY → HOLD → VOID), kernel tool-result parsing. **11 per-harness adapters**: antigravity, claude, codex, gemini, grok, hermes, kimi, openclaw, opencode, qwen, well.

### 1.4 OpenCode live plugin (the deepest integration)
`~/.config/opencode/plugins/arif-core/index.ts` — OpenCode V2 `Plugin.define()`:
- Ed25519 actor identity (333-AGI lane), kernel health probe, session registry, session card, continuity injector
- **FP-02's one deliberate exception (OBS, header comment):** native `edit/write/bash` tool calls never reach the kernel via MCP, so at that boundary the hook **TRANSMITS the kernel's verdict** and blocks OBSERVE_ONLY / VOID. Sensor everywhere else, wire at the boundary. This is the reference pattern for "sensors, kernel enforces, boundary transmits".
- History: 12 dead v1 fragments retired 2026-10-14 (SchemaError class), absorbed into the shared engine; disposition table in manifest `retired:` section — nothing ambiguous left.

### 1.5 MCP layer
`.mcp.json` mounts 11 organ servers (arifos :8088, a-forge :7072, signal, chron, minimax-media, claim-ledger, filings, media-ingest, numeric-audit, session-federation, hermes). OpenCode itself carries 23 MCP server configs.

---

## 2. External architectures (fetched 2026-10-22 unless labeled INT)

### 2.1 MCP — spec 2026-07-28 (VERIFIED: modelcontextprotocol.io/specification/latest)
- Stateless, self-contained JSON-RPC requests; **per-request capability negotiation**.
- Server features: Resources / Prompts / Tools. Client features: **Elicitation** (server→user info requests).
- **Extensions (opt-in, negotiated):**
  - **Tasks** — async long-running operations: polling, mid-flight input, **durable handles**.
  - **Skills over MCP** — rich structured instructions discovered/consumed through MCP.
  - **MCP Apps** — interactive UI elements (charts, forms, players) inline in conversations.
- **Security posture — the spec's own words:** tool annotations "should be considered **untrusted**"; "MCP itself **cannot enforce** these security principles at the protocol level." Consent/authorization is the HOST's job.
- **Acah2 read:** any "safety" layer keyed on MCP annotations is governance theater by spec definition. Enforcement must live host-side (our kernel) — which is exactly FP-02.

### 2.2 Claude Code plugins (VERIFIED: code.claude.com/docs/en/plugins)
- Plugin = directory of components: **skills, agents (subagent defs), hooks, mods (JS hook modules that can draw panes + add commands), MCP servers** + manifest `.claude-plugin/plugin.json`.
- **Marketplace = a git repo with `.claude-plugin/marketplace.json`** — a catalog, not a hosted store. Tiers: official/community (anthropics-sourced) vs third-party.
- **3-layer loading model: Settings → Disk → Session** (each layer checkable).
- Scopes: user / project / local. **Managed org policy**: allowlist/block marketplaces, force-install.
- Cost discipline: context-cost estimates before install; per-plugin measurement after; "not used recently" surfacing.
- Security admission: "what the plugin runs, it runs as you" — privilege = user privilege unless host gates it.
- **Acah2 read:** the format is excellent packaging; the trust model is full-inheritance. Adopt format + measurement; NEVER adopt implicit privilege inheritance — capability tokens must attenuate.
- arif-core's codex view already mirrors this format 1:1 (plugin.json/hooks.json/.mcp.json/skills) — deliberate, verified.

### 2.3 A2A (VERIFIED landing + live internal gateway)
- Open standard, Google-origin, **Linux Foundation**: cross-framework agent discovery + secure task collaboration (LangGraph, CrewAI, ADK, Genkit…).
- Operative internal evidence: **AAA A2A Gateway :3001 with DID-signed envelopes is LIVE** (skill `a2a-gateway-protocol`; dispatch lane). Known INT finding: `isInternal` substring gate spoofable — card claims need signature, not string-match.

### 2.4 ACP — Agent Client Protocol (VERIFIED: agentclientprotocol.com)
- "LSP for coding agents": editor ↔ agent JSON-RPC; local (stdio) or remote (HTTP/WebSocket, WIP); **reuses MCP JSON types**, adds agentic UX types (diffs).
- Zero agent-editor lock-in: any ACP editor drives any ACP agent.
- **Acah2 read:** pure transport seam, orthogonal to MCP (tools) and A2A (agents). It is the missing 4th seam: EDITOR. Optional adopt — exposes warga agents to any editor without per-editor adapters.

### 2.5 Search leads (surfaced, not deep-fetched — SPEC-grade)
- **NVIDIA OpenShell** reference architecture for governing agent workloads at scale (2026-10-21).
- **GKE Agent Sandbox** (300 sandboxes/sec) — mechanical isolation lane.
- **Cloudflare "next generation of MCP"** (2026-08-06) — aligns with the stateless 2026-07-28 line our `mcp-stateless-protocol` skill already documents.

### 2.6 Prior art worth mining (INT — stable knowledge, not re-fetched)
| System | Mechanism worth stealing |
|---|---|
| VS Code extensions | **declarative manifest + lazy activation events** — sensor mounts only when its event fires |
| Kubernetes operators | desired-state reconciliation loop — declared vs live converge; coverage-matrix already is a mini-catalog |
| Backstage | software catalog + plugin compile from YAML entities — same ONE-SOT-N-VIEWS shape |
| OSGi | module lifecycle resolve/start/stop + capability/requirement matching — the formal version of adapter negotiation |
| Extism/Wasm | **host-function whitelisting** — plugin code calls ONLY what host exposes; capability-based, mechanical |
| Macaroons | **caveated bearer tokens** — attenuation chains; already flagged in Canon literature map → policy_ir |

---

## 3. The recommended architecture — FOUR SEAMS, ONE LAW

```
                 EDITOR (ACP, optional)      ← any editor drives any warga
                    │
  HUMAN/F13  ──►  AAA HARNESS LAYER  ──►  A2A (:3001, DID-signed cards)  ← agent↔agent tasks
                    │ plugins (arif-core views, compiled from SOT)
                    ▼
             CAPABILITY SEAM = MCP 2026-07-28 (+Tasks, +Skills-over-MCP)
                    │ annotations ADVISORY ONLY (spec: untrusted)
                    ▼
             KERNEL :8088 — the ONLY judge
        arif_init → observe → think → route → memory → judge → forge → seal
                    │ ACT / SCT capability tokens (macaroon-style caveats)
                    ▼
             EXECUTION: A-FORGE :7072 governed verbs; sandbox for 3rd-party plugin code
```

**One Law:** every capability is mounted through a seam; every seam ends at the kernel; the kernel is the only issuer of authority; enforcement is cryptographic + mechanical, never narrative.

### 3.1 What to adopt, concretely
1. **MCP Tasks extension** for long-running governed ops — durable handles = overnight AGI-coder runs stay kernel-visible; mid-flight input replaces dead-end HOLDs.
2. **Skills over MCP** — serves skills as MCP-discovered resources: kills pointer-skill drift across 11 harnesses (FP-03 gets a wire protocol instead of file pointers).
3. **MCP Apps** (later) — UI surfaces for cockpit dashboards inline.
4. **Claude plugin bundle format** as the ingest wrapper for external plugins: manifest-translate → arif-core view + capability token. Anthropic-marketplace plugins become wrappable without forking behavior.
5. **ACP adoption** (optional lane): one ACP endpoint per warga harness → any editor, zero per-editor adapters.
6. **A2A card signing fix** — replace substring `isInternal` with DID signature check (INT finding already filed).
7. **Sandbox lane for third-party plugin code** (Extism/Wasm host-function whitelist or gVisor/E2B-class): plugin code NEVER runs in the harness process; it calls only host-exposed functions, each of which is a kernel-gated verb. GKE Agent Sandbox / NVIDIA OpenShell are the scale references.

### 3.2 The anti-acah2 plugin law (mechanical tests, no vibes)
Every gate/control/filter in plugin land must pass ALL of these, else it is rename-or-delete:

| # | Test | Source doctrine |
|---|---|---|
| A1 | **Names the action it BLOCKS in an acceptance test** — a control that cannot show a denied call live is NOT a control (mcp-governance-interceptor: 480 LOC Rust, never built, correctly held NOT-A-CONTROL 2026-10-21) | Safety-Is-Emergence F13 2026-10-18 |
| A2 | **Has a completion path** — gate without unblock path = half-done work | Safety-Is-Emergence |
| A3 | **Never deletes capability out of fear** — fix reversible; delete = F13 | Safety-Is-Emergence |
| A4 | **Defense depth is mechanical, not narrative** — no label/annotation/string-match enforces anything (MCP spec itself: annotations untrusted, protocol cannot enforce) | MCP spec + FP-02 |
| A5 | **Confidence ≠ authority** — plugin/hooks may observe and propose; only kernel-minted envelopes authorize | Authority Envelope / Representation≠Reality |
| A6 | **Failure class named in header** — new registry/control only with named consumer + named failure class | ACAH2 Four Laws |
| A7 | **HOLD only at real constitutional classes** — irreversible / money / identity / prod-destroy. Everything else EXECUTES | no-HOLD-flow v2 |

What this KILLS by design: LANE_CEILING-style ceiling filters, emoji-strippers, "no solve / 1-3 sentence" output caps, persona [SILENT], flash-first fallbacks — the acah2 filter class already executed 2026-10-18. No plugin view may reintroduce them; the compile step should lint for it.

### 3.3 Autonomous governed execution — the AGI-coder contract
Default = EXECUTE. The agent-coder (any warga lane) receives from the plugin:
- identity bound (Ed25519 → kernel actor),
- organs mounted (MCP),
- continuity injected (carry-forward),
- sensors on every mutation (hook mesh),
- kernel verdict at the boundary (edit/write/bash transmit),
- capability tokens with caveats (scope, expiry, target),
- durable task handles for long ops (MCP Tasks),
- receipts on completion (build/seal chain).

The ONLY stops are kernel HOLD at real classes. No prompt-level filter sits between the coder and the work. That is "autonomous governed execution" — governance as substrate, not as nagging.

---

## 4. Honest gaps (labeled, not hidden)
| Gap | State | Path |
|---|---|---|
| mcp-governance-interceptor | NOT-A-CONTROL (HOLD 2026-10-21) | Either build+test+deploy+live-deny-probe then F13 review, or delete per Canon #0. Do NOT let it sit as acah2 artifact. |
| A2A isInternal substring gate | Spoofable (INT) | DID-signature check on agent cards |
| MCP Tasks adoption | Spec exists; kernel/organ support not built | Add Tasks extension to arifos + a-forge MCP servers |
| Skills over MCP | Working-group stage | Pilot: serve /root/AAA/skills index as MCP resources |
| External plugin ingest (translate layer) | Not built | manifest-translate compiler target: `dist/external/<name>/` + token mint |
| Third-party code sandbox | Not built | Extism host-whitelist pilot on one low-risk plugin |
| ACP lane | Not built, optional | One warga harness pilot |
| Coverage honesty | LIVE (coverage-matrix.md) | Keep declaring FULL/DEGRADED/ABSENT — never assume |

## 5. Sources
- MCP spec (fetched 2026-10-22): https://modelcontextprotocol.io/specification/latest — 2026-07-28 schema; Tasks/Skills/MCP Apps extensions; annotations-untrusted security section.
- Claude Code plugins (fetched): https://code.claude.com/docs/en/plugins — bundle format, marketplace=git-catalog, 3-layer loading, org policy, mods.
- ACP (fetched): https://agentclientprotocol.com — JSON-RPC editor↔agent, MCP type reuse.
- A2A (fetched landing): https://a2a-protocol.org — Linux Foundation standard. Operative internal: AAA A2A Gateway :3001.
- Internal OBS: manifest.yaml, build_receipt.json, federation_hook_engine.py, opencode arif-core index.ts, dist/ tree, NEXT-20261014.md.
- Internal doctrine: FEDERATED-PLUGIN-ARCHITECTURE.md (FP-01..07), Safety-Is-Emergence (F13 2026-10-18), mcp-governance-interceptor HOLD (2026-10-21), ACAH2 carry-forward (2026-10-18).

DITEMPA BUKAN DIBERI ⚒️
