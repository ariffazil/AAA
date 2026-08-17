# Vendor-First Integration Plan — Reuse Before Reinvent

**Forged:** 2026-08-17 by kimi-code/FI-008
**Trigger:** External Claude audit + arifOS pivot doc (STRATEGIC_PIVOT_DELEGATION_PROVENANCE_2026-08-17.md)
**Status:** PROPOSAL — pending F13 ratification
**Reference:** `/root/AGENTS.md` (canon), `/root/AAA/governance/STRATEGIC_PIVOT_DELEGATION_PROVENANCE_2026-08-17.md`

---

## Operating principle

> "**Adopt, don't build.** Reuse mature open source for every plumbing layer.
> Ship only the one slice nobody else ships — capability-token + hash-chained
> delegation ledger, gated by a non-compensatory constitutional check."

This plan is the concrete adoption order for the principle above. Every layer has
a chosen vendor, a reason, and a verification surface. None of this depends on
building GEOX, WEALTH, or any full-stack organ. The federation stays incomplete by
design — Earth-bound and capital-bound reasoning goes to vendor services or stays
deferred.

---

## 1. Layer-by-layer adoption

### 1.1 Identity & registry — **A2A Agent Cards** + signed cards (JWS/JSON Canonicalization)

**Why:** A2A v1.0.1 is now adopted across Google, Microsoft, AWS, Linux Foundation.
150+ organizations supporting per the April 2026 LF press release. Don't compete.

**Adopt:**
- A2A Agent Cards for tool/agent identity
- OAN `did:oan` (arXiv 2606.03163) for cross-org trust
- `agent://` URI scheme (arXiv 2601.14567) for topology-independent identity

**Build here:**
- An A2A gateway in AAA that speaks the protocol correctly
- A registry at `https://aaa.arif-fazil.com` exposing agent cards for arifOS + AAA agents

**Do not build:** another identity scheme. Just sign the cards.

**Verification:** `forge_a2a_conformance` — does our card validate against the A2A conformance test? AAA already has `npm run validate:a2a-cards`.

---

### 1.2 Capability / tool registry — **MCP** + Smithery

**Why:** MCP is the de-facto agent-to-tool architecture (~97M monthly SDK downloads
by March 2026). The capability registry is solved.

**Adopt:**
- MCP native tool surface (FastMCP for arifOS, FastMCP for organs)
- `forge_registry` for runtime capability gating (already deployed)
- Smithery manifests for public tool cards (when shipping public surface)

**Do not build:** another tool catalog. Use MCP.

**Verification:** `forge_registry_status` + `forge_surface_guard check`. Already wired.

---

### 1.3 Session / lease durability — **DBOS** (Postgres) OR **Cloudflare Agents SDK** (Durable Objects)

**Why:** Temporal, Restate, DBOS, Inngest, LangGraph checkpointers, and Cloudflare
Agents SDK all already implement journaled steps, exactly-once tool execution,
idempotency keys, crash-recovery — exactly what the "lease" and "session/lease
state" concept needs.

**Adopt (Phase 1 — pick ONE):**
- **DBOS** if staying on bare-metal Postgres (lower ops burden for solo). The kernel
  already binds Postgres at `:5432`. DBOS adds workflow-as-DB-transaction semantics.
- **Cloudflare Agents SDK** if going to the edge. State = Durable Object with embedded
  SQLite. Zero-infra, but requires a Cloudflare account + Workers budget.

**Do not build:** another session store. Don't even maintain the one in AAA.

**Verification:** Crash-recovery smoke test — kill the kernel mid-session, restart,
verify the session resumes from where it left off, with the same lease.

**Open question for F13:** DBOS (keeps everything on this VPS) vs Cloudflare Agents SDK
(moves state to the edge, requires Cloudflare billing).

---

### 1.4 Memory tiers — **Letta** (formerly MemGPT, Apache-2.0)

**Why:** Letta has 23k+ stars, 2.4k+ forks, 100+ contributors, Apache-2.0. Purpose-built
OS-style tiered memory (core/recall/archival) with Postgres persistence. Exactly the
"memory tiers" component, maintained by people who know memory systems deeply.

**Adopt:**
- Letta for the L1/L2/L3 layers (now / session / similarity search)
- AAA's existing memory store becomes a Letta client (drop-in)
- The "what to remember" policy is the only thing arifOS owns — Letta handles storage,
  retrieval, forgetting

**Do not build:** another memory store. Don't even maintain the existing one.

**Verification:** `letta-ai/letta` integration test — does the AAA cockpit recall correctly
after integration? Migration script: import existing L2 Redis store into Letta core.

---

### 1.5 Delegation chains + provenance — **THE WHITESPACE**

**Why:** Per arXiv 2606.31498 (Kang & Diponegoro, Governance Gaps paper), the G5
(human escalation) and G6 (audit/replay) gaps are universal across MCP v1.1, A2A v1.0.1,
ACP, ANP, ERC-8004. A2A's Traceability extension is observability-only (Jaeger/Zipkin).
AIP/IBCT (arXiv 2603.24775, `draft-prakash-aip`) is an individual Internet-Draft,
not working-group adopted. The IETF draft-reece-wimse-cross-org-delegation-00 explicitly
says "no widely deployed mechanism today lets a relying party in one organization
verify, locally and without a callback, a recursively attenuated, principal-bound
delegation chain that originated in another organization."

**This is the one layer worth shipping.** No mature project owns it.

**Build here (8-week target):**
- A **capability-token** using **Biscuit tokens** (Clever Cloud, Apache-2.0) for
  attenuable chained authorization
- A **hash-chained delegation ledger** — standard Merkle append-only log, content-
  addressed, hash-linked. Bind each entry to: issuer identity, attenuated scope,
  parent-token hash, constitutional verdict, outcome receipt
- An **A2A extension** + **MCP middleware** that wrap any agent and emit the ledger
- A **reference implementation** in TypeScript (matches A2A ecosystem) with tests

**Adopt (vendored crypto, don't re-invent):**
- Biscuit tokens for the capability chain
- Any standard Merkle log library for the ledger
- Optional: OTel GenAI spans for trace_id linking

**Do not build:** a new auth scheme. Biscuit covers it.

**Verification:**
- Demo: Agent A delegates to B which delegates to C. Remote relying party verifies
  the chain offline (no callback to issuer).
- RFC 8693 token exchange interop test — single-hop works without breaking
  recursively attenuated chain.
- Schema aligns with `draft-prakash-aip` so we can adopt rather than fork.

**Engage external:**
- Comment on A2A Discussion #741 + Issue #2026 (existing open threads)
- Respond to `draft-prakash-aip-00` with our schema reference
- Reference `draft-reece-wimse-cross-org-delegation-00` in the README

---

### 1.6 Policy / non-compensatory gate — **Cedar** (AWS, CNCF) at **AgentGateway**

**Why:** Cedar (CNCF, default-deny, human-readable, machine-analyzable) + AgentGateway
(Solo.io → LF, now CNCF too) already implement non-compensatory policy at the gateway.
Bedrock AgentCore uses Cedar too. Don't write another policy engine.

**Adopt:**
- Cedar for all F1-F13 floors expressed as Cedar policies
- AgentGateway as the gateway runtime that enforces them
- The arifOS `core/floors.py` becomes a thin compatibility layer — the real policy
  lives in Cedar

**Do not build:** another policy engine. The One Skill (Knowing What NOT To Do)
is not a novel infrastructure problem — Cedar expresses it well.

**Verification:**
- All 13 floors compile as Cedar policies (no exceptions)
- AgentGateway denies by default and we have explicit grants, not implicit allow
- Cedar's analyzer proves no policy shadowing or unintended grants

**Open question for F13:** Cedar vs OPA (Rego). Cedar is the AWS + CNCF choice; OPA is
the Kubernetes + Solo.io choice. Both solve the same problem. Pick on which ecosystem
is closer (probably Cedar — we already use AWS for some bits).

---

### 1.7 Audit ledger — **VAULT999** stays as the binding artifact; OTel for tracing

**Why:** Per arXiv 2606.31498 G6 finding, no protocol mandates a hash-chained audit
log. Our VAULT999 is a legitimate instance of the missing primitive. But tracing
belongs in OTel — we shouldn't hand-roll spans.

**Adopt:**
- VAULT999 stays as the binding tamper-evident ledger
- OTel GenAI semantic conventions (`gen_ai.*`) for tracing — agent name, tool calls,
  latency, cost, parent spans
- OpenInference / Phoenix (Apache 2.0) as the tracing UI

**Do not build:** another tracing system. Don't extend VAULT999 with tracing fields.

**Verification:**
- Every tool call emits a `gen_ai.*` span (instrument once)
- VAULT999 entries are hash-linked (already implemented — Merkle anchor every 100)
- Phoenix dashboard shows the live trace alongside VAULT999 seals

---

### 1.8 Observability — **OpenTelemetry GenAI** + **OpenInference/Phoenix**

**Why:** OTel is the industry standard. GenAI semantic conventions are stable.
Phoenix is Apache 2.0 and the reference implementation for LLM observability.

**Adopt:**
- OTel `gen_ai.*` spans emitted from arifOS + all organs
- Phoenix as the backend UI (Apache 2.0)
- Federation trace_id linking across organs via OTel context propagation

**Do not build:** another observability stack. Stop hand-rolling.

**Verification:** Phoenix dashboard shows every arif_init → arif_judge → arif_seal
chain as one trace, with cost/latency attribution.

---

## 2. Adoption order (12 weeks)

### Stage 0 — Reframe (this week, days 0-3)

- [ ] Remove unverifiable claims from PyPI / Medium / README badges
  ("governs 80% of Python ecosystem", "world's first", "mathematically provable")
- [ ] Publish single canonical "what arifOS actually is" statement
  (link to `STRATEGIC_PIVOT_DELEGATION_PROVENANCE_2026-08-17.md`)
- [ ] Close AAA's session store — mark as "transition to Letta"

### Stage 1 — Adopt (weeks 1-4)

- [ ] Pick: DBOS or Cloudflare Agents SDK for session/lease
- [ ] Replace AAA's session store with the chosen vendor
- [ ] Migrate memory to Letta (read existing data, import, verify)
- [ ] Express F1-F13 as Cedar policies at AgentGateway
- [ ] Instrument arifOS + organs with OTel `gen_ai.*`
- [ ] Deploy Phoenix as observability backend
- [ ] Retire the hand-rolled tracing in `runtime/verbosity.py`

### Stage 2 — Build the novel artifact (weeks 4-12)

- [ ] Spec the capability-token delegation ledger (open schema)
- [ ] Implement Biscuit-token chain in TypeScript (matches A2A ecosystem)
- [ ] Implement Merkle append-only log (content-addressed, hash-linked)
- [ ] Build A2A extension (request/response headers + audit events)
- [ ] Build MCP middleware (intercept tools/call, emit entries)
- [ ] Reference implementation with tests + receipts
- [ ] Demo: A → B → C delegation chain, offline verification

### Stage 3 — Engage and verify (weeks 12-16)

- [ ] Comment on A2A Discussion #741 + Issue #2026
- [ ] Respond to `draft-prakash-aip-00`
- [ ] Reference `draft-reece-wimse-cross-org-delegation-00` in README
- [ ] Ship 3 artifacts: schema + middleware + demo
- [ ] External adoption check: any non-self stars, any third-party production use?

### Stage 4 — Retire or fold (weeks 16+)

- [ ] Retire AAA/A-FORGE as separate "organs" — fold what survives into the single artifact
- [ ] Keep arifOS kernel as the constitutional gate; make it small
- [ ] GEOX + WEALTH: stay deferred unless Earth-bound or capital-bound work
  actually materializes. Default = no.

---

## 3. What this means for the existing federation

- **GEOX + WEALTH**: not installed, not built. Per audit, don't build. The federation
  is structurally incomplete by design.
- **A-FORGE**: stays as the engineering actuator for the delegation ledger build.
  It already speaks the right API surface (TS, MCP, capability registry).
- **AAA**: stays as the human-facing cockpit + A2A gateway. The internal session
  store moves to vendor; the React SPA stays.
- **arifOS kernel**: stays as the constitutional gate. Becomes smaller, not larger.
- **HERMES**: stays as the Telegram edge. Out of scope for this pivot.

---

## 4. Verification artifacts

| Verification | Command | Pass criterion |
|---|---|---|
| Schema deployed | `curl -s :8088/mcp -X POST .../tools/list` | outputSchema lenient (no required beyond status/tool/result/meta/timestamp) |
| Biscuit chain demo | `npm run test -- delegation` | A→B→C chain, offline verify, RFC 8693 interop |
| Cedar policies | `cedar validate --policies ./policies` | All 13 floors compile, no shadows |
| Letta migration | `letta migrate --from redis://... --to postgres://...` | L1/L2 preserved, no data loss |
| OTel instrumentation | Open Phoenix dashboard | Every canonical tool emits `gen_ai.*` span |
| Federation probe | `python3 - <<PY ... PY` (§2 probe) | 5/5 organs responding `2025-06-18` |

---

## 5. Open questions for F13

1. **Session/lease vendor**: DBOS or Cloudflare Agents SDK? (DBOS = keep on VPS;
   Cloudflare Agents SDK = edge, requires billing)
2. **Policy engine**: Cedar or OPA? (Cedar is AWS/CNCF; OPA is Kubernetes/Solo.io)
3. **GEOX + WEALTH**: defer indefinitely, or commit to "build only if a paying
   use case shows up"? This is a real cost — building them is ~6 months of work
   that the audit says is misuse of effort.
4. **External engagement**: authorize commenting on A2A Discussion #741, #2026 and
   responding to `draft-prakash-aip-00` under ariffazil/arif-fazil names? Or do
   we want a separate org identity for these threads?
5. **Marketing purge deadline**: when do the unverifiable claims have to be off
   public surfaces? 7 days? 30 days? Same question for any "production-grade"
   badge on PyPI or README.

---

*DITEMPA BUKAN DIBERI ⚒️ — Reuse the plumbing. Ship only the gap. Build what's
adopted, retire what's not.*