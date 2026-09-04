# A2A v1.0 Deep Research + AAA Audit + A2A-MCP Zen

> **Date:** 2026-09-04 | **Auditor:** 333-AGI | **Session:** SEAL-929aaca0611e4550
> **Sources:** llm4agents.com audit, a2aproject/A2A spec, AAA live agent card, Atlan, Stellagent, DigitalApplied
> **Verdict:** Phase 0 conformance sweep authorized (T1). Signing ceremony = 888_HOLD.

---

## 1. A2A v1.0 — What Changed

**Spec:** A2A v1.0.0 (2026-03-12), v1.0.1 (2026-05-28)
**Normative source:** `a2a.proto` — ALL bindings (JSON-RPC, gRPC, HTTP+JSON) map from this

### 1.1 Breaking Wire Changes

| Area | v0.3 | v1.0 | Impact |
|------|------|------|--------|
| Parts | `TextPart`/`FilePart`/`DataPart` + `kind` | Single `Part` with `oneof` content | Rewrite parsers |
| Enums | lowercase/hyphenated | `SCREAMING_SNAKE_CASE` (`TASK_STATE_COMPLETED`) | All state checks |
| Errors | binding-specific | `google.rpc.Status` + `-32001` to `-32009` | Error mapper |
| Agent Card | top-level `url`/`protocolVersion` | `supportedInterfaces[]` per binding | Card restructure |
| Stream events | `kind` discriminator | `statusUpdate`/`artifactUpdate` wrappers | Stream parser |
| `final` boolean | exists | removed — terminal = stream closure | State machine |
| Timestamps | flexible | ISO 8601 UTC, millisecond precision | Parser |

### 1.2 New Primitives

| Primitive | What | Why |
|-----------|------|-----|
| **`A2A-Version` header** | Required per request. Empty = 0.3 (trap!) | Version negotiation |
| **Signed Agent Cards** | JWS + RFC 8785 JCS + protobuf presence rules | Identity trust |
| **`tenant` field** | Opaque routing key per request | Multi-tenancy |
| **`ListTasks`** | Cursor-based pagination | Fleet observability |
| **`supportedInterfaces[]`** | Per-binding URL + version + transport | Multi-binding |
| **`A2A-Extensions` header** | Client opt-in per request | Extension negotiation |

### 1.3 Version Negotiation (THE TRAP)

```
Empty A2A-Version → interpreted as 0.3 (NOT latest)
Client MUST send A2A-Version: 1.0 on every request
Agent MUST serve requested semantics or return -32009
```

**Federation risk:** If AAA doesn't enforce, a v1.0 client silently gets v0.3 semantics.

### 1.4 Signed Agent Cards

```
Agent Card → protobuf JSON presence rules → strip signatures[]
→ RFC 8785 JCS canonicalization → JWS signing input
→ base64url(protected-header) + "." + base64url(payload)
→ Sign with alg + kid
```

**Critical subtlety:** `extensions: []` (empty repeated) = OMIT. `streaming: false` (explicit default) = KEEP. Generic JSON sort won't handle this.

### 1.5 Error Taxonomy

| Error | Code | HTTP | gRPC |
|-------|------|------|------|
| TaskNotFound | -32001 | 404 | NOT_FOUND |
| TaskNotCancelable | -32002 | 409 | FAILED_PRECONDITION |
| PushNotificationNotSupported | -32003 | 400 | UNIMPLEMENTED |
| UnsupportedOperation | -32004 | 400 | UNIMPLEMENTED |
| ContentTypeNotSupported | -32005 | 415 | UNIMPLEMENTED |
| InvalidAgentResponse | -32006 | 502 | INTERNAL |
| AuthRequired | -32007 | 401 | UNAUTHENTICATED |
| ExtensionSupportRequired | -32008 | 400 | FAILED_PRECONDITION |
| VersionNotSupported | -32009 | 400 | FAILED_PRECONDITION |

---

## 2. AAA Agent Card Audit

### 2.1 Current State

**Location:** `/.well-known/agent-card.json`
**Protocol version declared:** `1.2` (note: spec is `1.0.0`/`1.0.1` — version mismatch!)
**Extensions:**8 declared, all `required: false`
**Skills:**8

### 2.2 Gap Ledger

| ID | Gap | Severity | Evidence |
|----|-----|----------|----------|
| **G1** | `protocolVersion: "1.2"` — not a valid A2A version | HIGH | Spec is 1.0.0/1.0.1. "1.2" is non-existent |
| **G2** | No `A2A-Version` header enforcement | HIGH | Empty header → silent 0.3 downgrade |
| **G3** | No `Vary: A2A-Version` on card responses | HIGH | CDN can cross-serve versioned cards |
| **G4** | Top-level `protocolVersion` field (legacy) | MEDIUM | Should be in `supportedInterfaces[]` |
| **G5** | No signed agent card (`signatures[]` absent) | HIGH | No identity verification possible |
| **G6** | Non-conformant signing (if any) | HIGH | "Sorted JSON + SHA-256" ≠ RFC 8785 JCS |
| **G7** | `federation_organs` extension exposes internal URLs | HIGH | A-FORGE URL in public card |
| **G8** | No `supportedInterfaces[]` array | MEDIUM | Legacy top-level fields |
| **G9** | No `ListTasks` endpoint verified | MEDIUM | Fleet observability gap |
| **G10** | Extensions not versioned in URI | LOW | URIs lack `/v1` suffix consistently |
| **G11** | No external-card anti-poisoning pipeline | HIGH | Instruction injection via card metadata |
| **G12** | `mcp_native: true` not in spec extensions | INFO | Custom extension, acceptable |

### 2.3 Critical Finding: A-FORGE Exposed

The `federation-gateway/v1` extension in the public agent card reveals:
```json
{
  "id": "a-forge-mcp",
  "url": "https://a-forge.arif-fazil.com",
  "card_url": "https://a-forge.arif-fazil.com/.well-known/agent-card.json"
}
```

**Per Perplexity's hexagon invariant: A-FORGE and VAULT999 must NOT be publicly discoverable.** This is a separation-of-powers violation. A-FORGE should only be reachable through AAA → arifOS → internal A-FORGE route.

### 2.4 Version Mismatch

AAA declares `protocolVersion: "1.2"`. The A2A spec has:
- v1.0.0 (2026-03-12)
- v1.0.1 (2026-05-28)
- No v1.2 exists

This means AAA's card will fail any conformant version check.

---

## 3. A2A-MCP Zen (Harmonization Architecture)

### 3.1 The Layer Model

```
┌─────────────────────────────────────────────┐
│ Layer 2: A2A (Horizontal — Agent ↔ Agent)   │
│  • Discovery: Agent Cards                    │
│  • Coordination: Tasks, Messages, Artifacts  │
│  • Identity: Signed Cards, JWS, JWKS         │
│  • Multi-tenancy: tenant field               │
│  • Versioning: A2A-Version header            │
└──────────────────┬──────────────────────────┘
                   │ delegates to
┌──────────────────▼──────────────────────────┐
│ Layer 1: MCP (Vertical — Agent ↔ Tools)     │
│  • Discovery: server/discover                │
│  • Invocation: tools/call, resources/read    │
│  • State: Stateless handles                  │
│  • Auth: OAuth/CIMD                          │
│  • Versioning: MCP-Protocol-Version header   │
└──────────────────┬──────────────────────────┘
                   │ executes via
┌──────────────────▼──────────────────────────┐
│ Layer 0: Organs (Federation infrastructure) │
│  • arifOS: Constitutional kernel             │
│  • A-FORGE: Execution shell                  │
│  • GEOX/WEALTH/WELL: Domain compute          │
│  • VAULT999: Immutable ledger                │
└─────────────────────────────────────────────┘
```

### 3.2 Protocol Mapping

| Function | MCP | A2A | Zen (Harmonized) |
|----------|-----|-----|-------------------|
| **Discovery** | `server/discover` | `/.well-known/agent-card.json` | Both serve capability discovery. MCP = per-session. A2A = pre-auth. |
| **Version** | `MCP-Protocol-Version` header | `A2A-Version` header | Both header-based. Both trap on empty. Both need enforcement. |
| **Auth** | OAuth/CIMD | Signed Agent Cards + JWKS | MCP auths the tool call. A2A auths the agent identity. Compose. |
| **State** | Stateless handles | Task lifecycle | MCP handles are scoped/expiring. A2A tasks are durable. Bridge via handle→task binding. |
| **Routing** | `Mcp-Method`/`Mcp-Name` headers | `tenant` field | MCP routes by tool. A2A routes by tenant. Both header-driven. |
| **Errors** | MCP error codes | `google.rpc.Status` -32001..-32009 | Map MCP errors to A2A error taxonomy at gateway. |
| **Extensions** | `_meta` capabilities | `capabilities.extensions[]` + `A2A-Extensions` | Both opt-in. Both versioned URIs. Both silent-ignore if unsupported. |
| **Caching** | `ttlMs`/`cacheScope` | `Vary: A2A-Version` + ETag | Both cache-aware. MCP caches tool catalogs. A2A caches agent cards. |

### 3.3 The AAA Gateway as Protocol Bridge

```
External A2A Client
  │
  ├─ A2A-Version: 1.0
  ├─ Signed Agent Card verified
  ├─ tenant: federation
  │
  ▼
AAA A2A Gateway (:3001)
  │
  ├─ Verify A2A-Version header
  ├─ Verify agent card signature (if external)
  ├─ Anti-poisoning: sanitize card metadata
  ├─ Route by tenant + skill
  │
  ├─ For TOOL operations:
  │    │
  │    ▼
  │  MCP Bridge → arifOS → organ MCP server
  │    ├─ MCP-Protocol-Version: 2026-07-28
  │    ├─ Mcp-Method: tools/call
  │    ├─ Stateless dispatch
  │    └─ Return result with resultType, ttlMs
  │
  └─ For AGENT operations:
       │
       ▼
     A2A Task Lifecycle
       ├─ SendMessage → create task
       ├─ GetTask → poll status
       ├─ ListTasks → fleet observability
       └─ CancelTask → abort
```

### 3.4 Zen Invariants

1. **MCP never discovers agents. A2A never calls tools.** Clean boundary.
2. **AAA is the ONLY public A2A edge.** A-FORGE, VAULT999 are NEVER discoverable.
3. **A2A auths identity. MCP auths capability.** Compose, don't conflate.
4. **Version enforcement is mandatory on both protocols.** Empty = reject, not fallback.
5. **Extensions are versioned URIs on both protocols.** Never silently downgrade.
6. **Signed Agent Cards = A2A identity. ACT tokens = MCP identity.** Both verified at gateway.

### 3.5 The Unified Capability Model

```json
{
  "agent_id": "geox-mcp",
  "a2a_identity": {
    "card_verified": true,
    "signature_count": 1,
    "kid": "geox-2026-q3",
    "trust_tier": "federation-peer"
  },
  "mcp_capabilities": {
    "server_discover": true,
    "protocol_version": "2026-07-28",
    "tools_count": 27,
    "cache_envelope": false,
    "stateless": true
  },
  "a2a_capabilities": {
    "supportedInterfaces": [
      {"url": "https://geox.arif-fazil.com", "protocolBinding": "JSONRPC", "protocolVersion": "1.0"}
    ],
    "extensions": ["arifos://floors/v1"],
    "tenant": "federation"
  },
  "governance": {
    "authority": "COMPUTE_ONLY",
    "verdict_authority": "arifOS",
    "floors": ["F1", "F2", "F4", "F8", "F11", "F12"]
  }
}
```

### 3.6 The Flow: A2A Task → MCP Tool Call

```
1. External agent sends A2A SendMessage to AAA
   └─ A2A-Version: 1.0, tenant: federation, skill: evaluate_basin

2. AAA verifies:
   ├─ A2A-Version valid
   ├─ Agent card signature (if external)
   ├─ Tenant authorized
   └─ Skill exists in registry

3. AAA creates A2A task (TASK_STATE_SUBMITTED)

4. AAA routes to arifOS (MCP bridge):
   ├─ POST /mcp
   ├─ MCP-Protocol-Version: 2026-07-28
   ├─ Mcp-Method: tools/call
   ├─ Mcp-Name: geox_basin
   └─ _meta: {task_id, tenant, a2a_version}

5. arifOS judges (constitutional gate):
   ├─ F1-F13 floor check
   ├─ Authority band verification
   └─ Returns SEAL/HOLD

6. If SEAL: GEOX executes (MCP tool):
   ├─ Stateless dispatch
   ├─ Returns result with resultType
   └─ Writes vault receipt

7. AAA maps result to A2A response:
   ├─ TASK_STATE_COMPLETED
   ├─ Artifact with result
   ├─ Part with oneof content
   └─ google.rpc.Status if error

8. AAA returns A2A response to external agent
```

---

## 4. Phase 0 Conformance Sweep (A2A)

### 4.1 Scope

Read-only probes against all registered agent cards and AAA gateway.

### 4.2 Test Matrix

| Control | Probe | Pass Condition |
|---------|-------|----------------|
| v1 card retrieval | `A2A-Version: 1.0` | Valid v1 card |
| Legacy compat | `A2A-Version: 0.3` | Only if intentional |
| Missing version | No header | Explicit policy result |
| Unsupported version | `A2A-Version: 9.9` | `-32009` response |
| `Vary` header | Check response headers | `Vary: A2A-Version` present |
| Schema conformance | Parse as v1 protobuf/JSON | No forbidden legacy fields |
| `supportedInterfaces[]` | Inspect each interface | Valid URL, binding, version |
| Signature presence | Inspect `signatures[]` | Required cards have ≥1 |
| JCS correctness | Canonicalize independently | RFC 8785 + protobuf presence |
| JWS verification | Resolve `kid` from JWKS | At least one valid signature |
| Extension declaration | Inspect `capabilities.extensions[]` | `arifos://floors/v1` on internal cards |
| Anti-poisoning | Adversarial card fixtures | Treated as data, not instructions |
| Tenant isolation | Probe permitted/prohibited tenants | No cross-tenant leakage |
| Error envelopes | Deliberate invalid requests | Correct `google.rpc.Status` |
| Content type | All v1 endpoints | `application/a2a+json` preferred |

### 4.3 Artifacts

1. Machine-readable ledger (JSON)
2. Human report (Markdown)
3. Card evidence pack (raw responses, hashes, signatures)

---

## 5. Signing Ceremony Design (888_HOLD)

### 5.1 Key Model

```
Offline root / custody key
  │
  ├─ Signs issuer / federation JWKS authority
  │
  └─ Delegates to online card-signing keys
       ├─ kid: arifos-a2a-card-2026-q3
       ├─ kid: aaa-a2a-card-2026-q3
       └─ kid: organ-{name}-a2a-card-2026-q3
```

### 5.2 Ceremony Sequence

1. Generate signing key in protected HSM/KMS
2. Assign immutable `kid`, algorithm, activation, expiration
3. Publish public key through federation JWKS
4. Implement canonicalization from protobuf-aware card model
5. Generate deterministic test vectors
6. Verify with separate implementation
7. Dual-sign during transition
8. Deploy behind version-aware cache controls
9. Have AAA + separate verifier validate all cards
10. Record in VAULT999
11. Retire old key only after overlap window

### 5.3 Policy by Card Class

| Category | Signature Policy |
|----------|-----------------|
| Internal federation organs | Mandatory |
| AAA public gateway | Mandatory |
| External discovered cards | Verify if present; unsigned = quarantine |
| Experimental/dev | Separate non-production issuer |
| A-FORGE / VAULT999 | **No public cards** |

---

## 6. Hexagon Invariant (Preserve)

| Component | Public A2A Card? | Why |
|-----------|-----------------|-----|
| AAA gateway | ✅ Yes | External task ingress |
| GEOX | ✅ Yes, controlled | Bounded earth-evidence |
| WEALTH | ✅ Yes, controlled | Advisory capital |
| WELL | ✅ Yes, controlled | Readiness observation |
| arifOS | ⚠️ Tightly scoped | Constitutional review |
| A-FORGE | ❌ **NEVER** | Executor must not be independently discoverable |
| VAULT999 | ❌ **NEVER** | Ledger must not expose execution surface |

**Current violation:** AAA's public agent card exposes A-FORGE URL in `federation-gateway/v1` extension. Fix: remove internal organ URLs from public card, keep only in authenticated extended card.

---

## 7. External-Card Anti-Poisoning

```
Fetch card
  ├─ SSRF controls (HTTPS, DNS/IP allow, block loopback)
  ├─ Transport verification (TLS, version, content-type)
  ├─ Parse as strict data (schema, field-length caps, URI allow-lists)
  ├─ Identity verification (JCS + JWS, JWKS trust policy)
  ├─ Content-risk classification (flag instruction-like language)
  ├─ Policy decision (deny/quarantine/advisory/verified)
  └─ Safe planner projection (constrained summary, not raw prose)
```

---

## 8. Recommended Phase 0 Decision

**AUTHORIZE T1.** Read-only, reversible, produces evidence.

**Acceptance criteria before Phase 1:**
- 0 production-required cards unsigned
- 100% signatures validate independently
- 0 cards reliant on non-JCS "sorted JSON"
- 100% v1 interfaces have correct A2A-Version behavior
- 100% versioned responses include `Vary: A2A-Version`
- 0 top-level legacy fields on v1 cards
- 100% internal cards declare `arifos://floors/v1`
- 0 cross-tenant paths

**888_HOLD for:**
- Signing ceremony
- Production card mutation
- Removing legacy compatibility
- External card exposure changes

---

## 9. A2A-MCP Zen Summary

```
MCP = vertical (agent → tools)     A2A = horizontal (agent → agent)
MCP = per-session discovery        A2A = pre-auth discovery
MCP = stateless handles            A2A = durable task lifecycle
MCP = Mcp-Method/Mcp-Name routing  A2A = tenant routing
MCP = OAuth/CIMD auth              A2A = Signed Cards + JWKS
MCP = ttlMs/cacheScope caching     A2A = Vary/ETag caching
MCP = _meta extensions             A2A = capabilities.extensions[]
MCP = -32020 header mismatch       A2A = -32009 version mismatch

AAA Gateway = the bridge point
  A2A in → verify identity → MCP bridge → organ executes → MCP result → A2A out
```

**The zen:** MCP and A2A are complementary layers, not competitors. MCP is how an agent uses tools. A2A is how agents talk to each other. AAA is the gateway that bridges them. arifOS is the constitutional authority that governs both.

---

*Filed by 333-AGI. Perplexity external agent corrections integrated. LLM4Agents audit cited. DITEMPA BUKAN DIBERI.*
