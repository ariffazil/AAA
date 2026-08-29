---
title: FED: Federated External Doctrine — Harness Tool Governance Spec
aka: FED v1.0.0 (also: Federated Execution Doctrine — valid alternate reading)
version: 1.0.0
status: DRAFT — awaiting F13 ratification
author: FI-008 (Kimi Code) on behalf of 888 SOVEREIGN
forged_at: 2026-08-01
forged_by_session: FI-008 sovereign-direct cycle
supersedes: /root/AAA/governance/harness-tool-governance.md (renamed)
references:
  - /root/AAA/GENESIS/000_KERNEL_CANON.md
  - /root/AAA/GENESIS/FLOOR_TABLE.json
  - /root/arifOS/arifosmcp/config/model_registry.json
  - /root/AAA/registries/models/MODEL_TIERS.json
  - /root/AAA/federation/seats.yaml
  - QwenCloud Token Plan Individual docs (home.qwencloud.com)
  - QwenCloud Token Plan Team docs (tokenplan-enterprise.qwencloud.ai)
  - QwenCloud Responses API docs (docs.qwencloud.com)
floor_scope: [F1, F2, F4, F9, F11, F13]
organ_scope: [arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA]
tool_scope:
  - qwen-responses web_extractor
  - qwen-responses web_search
  - qwen-responses web_search_image (text-to-image search)
  - qwen-responses image_search (image-to-image search)
  - qwen-responses function calling
  - qwen-responses MCP servers (external, up to 10 per request)
canonical_path: /root/AAA/governance/FED-harness-tool-governance-v1.0.0.md
audit_chain: forge_vault(mode="receipt", tier="doctrine.governance", reason="FED-harness-tool-spec-v1.0.0")
---

# FED — Federated External Doctrine

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-01 by FI-008 under F13 sovereign directive.
>
> **Naming:** **FED** = **Federated External Doctrine** (primary) · Federated Execution Doctrine (valid alternate reading). Doctrine ↔ execution are two views of one artifact.
>
> **What FED is:** the **constitutional interface layer** that governs how the federation uses paid, third-party agentic tools (QwenCloud Token Plan / Responses API / Harness tools) so every call remains **auditable, sovereign, and reversible**.
>
> **What FED is NOT:**
> - Not the cheapest-model router (that's TokenRouter cascade)
> - Not the free-tier mesh (that's FLAME)
> - Not the source-of-truth data owner (that's Tier A federation MCPs)
> - Not the verdict engine (that's arif_judge)
>
> **Tier scope:** this spec governs **Tier C** — external, paid, agentic tool surfaces. Tier A/B governance lives elsewhere.
>
> **Sealing status:** DRAFT. Federation tools MAY consume Qwen Responses API tools under this spec while DRAFT; ratification (888 types `999 SEAL FED-HARNESS-TOOL-GOVERNANCE`) makes it SEALED.

---

## 0. Scope & Definitions

**In scope:**
- All QwenCloud Responses API tool invocations from any federation surface (OpenCode, Hermes, OpenClaw, Codex, Claude Code, future tools)
- All `web_extractor`, `web_search`, `image_search`, `web_search_image`, `function`, and `mcp` tool type responses
- Cross-border data flow implications for sovereign workloads
- Epistemic calibration of every tool output (§11)

**Out of scope:**
- Chat Completions API calls (`/v1/chat/completions`) — see `chat-completions-governance.md` (future)
- Federation-native MCP servers (arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA) — see `/root/AAA/federation/FEDERATION_CONTRACT.md`
- Pay-as-you-go Alibaba Model Studio — see DashScope docs

**Definitions:**
- **Harness tool**: A QwenCloud Responses API tool that the model invokes server-side; results appear in the model's context without federated control over the tool's behavior.
- **Tier A surface**: Sovereign organ (arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA) — full F1-F13 governance required.
- **Tier B surface**: Auxiliary federation MCP (brave-search, tavily, firecrawl, perplexity, exa, fetch) — federated governance via MCP server-side policy.
- **Tier C surface**: External tool (QwenCloud Responses API Harness tools, third-party MCPs) — federated governance via pre/post-flight hooks only. **This is FED's scope.**

---

## 1. Authority Tiers

```
┌─────────────────────────────────────────────────────────────────┐
│ Tier A — Sovereign organs                                        │
│   arifOS :8088 · A-FORGE :7071 · GEOX :8081                    │
│   WEALTH :18082 · WELL :18083 · AAA :3001 · VAULT999           │
│                                                                  │
│   Governance: FULL F1-F13 enforcement                           │
│   Data class: SOVEREIGN (myKad, NRIC, PETRONAS, etc.)           │
│   Tool surface: NEVER bypassed by Harness tools                  │
│   Cost accounting: forge_vault(mode="receipt")                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Tier B — Federated MCP servers                                   │
│   mcp__brave-search__* · mcp__tavily__* · mcp__firecrawl__*     │
│   mcp__perplexity__* · mcp__exa__* · mcp-server-fetch            │
│                                                                  │
│   Governance: Server-side policy (each MCP enforces its own)   │
│   Data class: AGGREGATED (results filtered by MCP server)        │
│   Tool surface: First choice for non-sovereign research          │
│   Cost accounting: Per-MCP billing integration                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Tier C — External tools (FED's scope)                           │
│   qwen-responses web_extractor / web_search / image_search      │
│   qwen-responses function calling / MCP                          │
│                                                                  │
│   Governance: FED pre-flight + post-flight hooks only            │
│   Data class: PUBLIC (web content) — never sovereign            │
│   Tool surface: Overflow / cost-tier / cross-validate          │
│   Cost accounting: forge_vault(mode="receipt", tier="tools.fee")│
│   Epistemic labels: per §11                                     │
└─────────────────────────────────────────────────────────────────┘
```

**Routing policy:** When a tool call involves sovereign data (Tier A surfaces, PII patterns, federation secrets), Tier A/B only. When a tool call is for general public web research, Tier C is acceptable under this spec's gates.

---

## 2. Pre-Flight Gates (before Qwen tool call)

Six gates must pass before any Qwen Responses API Harness tool invocation. Failure → HARD REJECT, log to vault, surface to caller.

### Gate 1 — Zero-Fly Zone mirror (F9 binding)

Mandatory input scan. Reject any call containing these patterns in `input.messages[].content[].text`:

```
SOVEREIGN_CONTENT_TRIGGERS = [
    r'mykad',                  # Malaysian national ID
    r'nric',                   # Generic national ID
    r'petronas internal',      # PETRONAS restricted
    r'password:',              # Credential pattern
    r'token:',                 # API key pattern
    # ... extend per AAA_SOVEREIGN_DATA_REGISTRY
]
```

**→ epistemic gate-down:** pre-flight rejection → §11 label `UNKNOWN`.

Implementation:
```python
import re
def pre_flight_zero_fly_zone(input_text: str) -> tuple[bool, str]:
    for pattern in SOVEREIGN_CONTENT_TRIGGERS:
        if re.search(pattern, input_text, re.IGNORECASE):
            return False, f"Zero-Fly Zone violation: '{pattern}' in input"
    return True, "OK"
```

### Gate 2 — URL/domain allowlist (Tier C web_extractor only)

For `web_extractor` calls, the URL domain must be in allowlist. Default allowlist (extend per use case):

```
ALLOWED_DOMAINS = [
    # Government & academic
    r'.*\.gov\.my$',
    r'.*\.edu\.[a-z]+$',
    r'arxiv\.org$',
    # Major reference
    r'en\.wikipedia\.org$',
    # Federated web properties
    r'arif-fazil\.com$',
    r'arifos\.arif-fazil\.com$',
    # QwenCloud doc surface
    r'docs\.qwencloud\.com$',
]
```

Block list (always rejected regardless of allowlist):

```
BLOCKED_DOMAINS = [
    r'.*pastebin\.com$',
    r'.*onion$',                # Tor hidden services
    r'.*\.onion$',
    # Add known malicious/sensitive domains
]
```

**→ epistemic gate-down:** neutral domain (no allowlist hit, no denylist) → §11 label `PLAUSIBLE` (no upgrade to `CLAIM` until MCP cross-check).

### Gate 3 — Per-session tool-call budget

Each session has a tool-call budget enforced before each call. Exceeded → HARD REJECT.

| Tool | Default budget/session | Override path |
|---|---|---|
| `web_extractor` | 10 calls | `HARNESS_BUDGET_WEB_EXTRACTOR` env var |
| `web_search` | 20 calls | `HARNESS_BUDGET_WEB_SEARCH` env var |
| `image_search` | 5 calls | `HARNESS_BUDGET_IMAGE_SEARCH` env var |
| `web_search_image` | 5 calls | `HARNESS_BUDGET_WEB_SEARCH_IMAGE` env var |
| `function` (user-defined) | 50 calls | `HARNESS_BUDGET_FUNCTION` env var |
| External MCPs | 3 servers × 10 calls each | `HARNESS_BUDGET_MCP` env var |

Reset: at session start, OR at midnight UTC, whichever comes first.

**→ epistemic gate-down:** budget exhausted → §11 label `UNKNOWN`.

### Gate 4 — Per-seat monthly tool-fee cap

Token Plan seats have monthly Credit limits. Tool fees ($8-$10 per 1k calls) are SEPARATE.

| Seat tier | Monthly tool-fee cap | Override |
|---|---|---|
| Team Standard ($20/mo) | $50/mo tool fees | 888_HOLD |
| Team Pro ($75/mo) | $200/mo tool fees | 888_HOLD |
| Team Max ($200/mo) | $500/mo tool fees | 888_HOLD |
| Individual Pro ($68/mo) | $100/mo tool fees | 888_HOLD |
| Individual Standard/Lite | $20/mo tool fees | 888_HOLD |

When 80% of cap reached → ALERT to session owner. When 100% reached → HARD REJECT until month rollover.

### Gate 5 — Model floor for tool capability

Qwen Responses API tools require specific model tiers. Reject any call attempting `web_extractor` etc. on:
- `qwen3.6-flash` (not in recommended list per docs)
- `qwen3.5-*` (deprecated tier)
- Models not in QwenCloud Team or Individual allowlist

Allow:
- `qwen3.8-max-preview` (Token Plan only)
- `qwen3.7-max` (both editions)
- `qwen3.7-plus` (both editions)
- `qwen3.7-max-2026-06-08` (image search fallback)
- `qwen3.6-plus` (web_extractor fallback)

### Gate 6 — Streaming-mode enforcement

For tool calls > 30s expected duration, `stream: true` REQUIRED to avoid timeout cascades and enable per-event governance hooks. Codified by:

```python
def pre_flight_streaming(tool_name: str, estimated_tokens: int) -> bool:
    if tool_name in ["web_extractor", "web_search_image", "image_search"]:
        return True  # always stream image/web tools
    if estimated_tokens > 8000:
        return True
    return False
```

---

## 3. Post-Flight Gates (after Qwen tool returns)

Eight gates fire on each streaming event. Failure → mark output with appropriate **§11 epistemic label** based on trigger condition.

### Gate 7 — URL logging (F11 binding)

On `response.output_item.done` event with `item.type == "web_extractor_call"`:

```python
def post_flight_url_log(item, session_id):
    if item.type == "web_extractor_call":
        url = item.goal
        text_size = len(item.output or "")
        # F11 audit: append-only receipt
        forge_vault(
            mode="receipt",
            tier="session.ledger",
            reason=f"web_extractor:{url[:120]}",
            value=json.dumps({
                "url": url,
                "bytes": text_size,
                "session_id": session_id,
                "timestamp": now_iso(),
                "cross_border_data_transfer": True,  # F9 audit marker
                "epistemic_label": derive_epistemic_label(item),  # → §11
                "derivation": "OBS",  # F2 provenance — direct page fetch
            })
        )
```

**→ epistemic gate-down:** `item.output` empty/truncated → §11 label `HYPOTHESIS` (model will need to rely on prior).

### Gate 8 — PII re-redaction (defense in depth)

Even with Gate 1, the extracted page content may contain sovereign patterns. Apply same Zero-Fly Zone scan to `item.output`:

```python
def post_flight_redact_pii(extracted_text: str) -> str:
    for pattern, label in SOVEREIGN_PATTERNS:
        extracted_text = re.sub(pattern, f"[REDACTED-{label}]", extracted_text, flags=re.IGNORECASE)
    return extracted_text
```

**→ epistemic gate-down:** redaction occurred → §11 label `PLAUSIBLE` (or lower; redaction may obscure facts).

### Gate 9 — Empty-output handling

If `item.output` is empty or `< 100 chars`, the model receives a `HYPOTHESIS`-level signal:

```python
def post_flight_empty_handler(item):
    if not item.output or len(item.output.strip()) < 100:
        return {
            "epistemic_label": "HYPOTHESIS",   # → §11
            "confidence": "low",
            "derivation": "DER",                 # F2 provenance — model-derived from absent evidence
            "note": "web_extractor returned empty or near-empty content",
            "fallback": "Suggest: try alternative URL or use federated MCP (Tier B)"
        }
    return {"epistemic_label": "CLAIM", "confidence": "high", "derivation": "OBS", "content": item.output}
```

### Gate 10 — Cost reconciliation

On `response.completed` event, extract `usage.x_tools.*` and reconcile:

```python
def post_flight_cost_reconcile(usage):
    costs = {
        "web_search_calls": usage.x_tools.get("web_search", {}).get("count", 0),
        "web_extractor_calls": usage.x_tools.get("web_extractor", {}).get("count", 0),
        "image_search_calls": usage.x_tools.get("image_search", {}).get("count", 0),
        "web_search_image_calls": usage.x_tools.get("web_search_image", {}).get("count", 0),
    }
    estimated_fees = {
        "web_search": costs["web_search_calls"] * 0.01,        # $10/1k
        "image_search": (costs["image_search_calls"] + costs["web_search_image_calls"]) * 0.008,  # $8/1k
        "web_extractor": 0,  # currently free
    }
    forge_vault(
        mode="receipt",
        tier="tools.fee",
        reason=f"session_cost_{now_iso()}",
        value=json.dumps({
            "costs": costs,
            "estimated_fees_usd": estimated_fees,
            "epistemic_label": "ESTIMATE",  # → §11 (numeric provenance)
        })
    )
```

### Gate 11 — Domain in returned image URLs (image search only)

For `web_search_image_call` and `image_search_call`, scan returned `item.output` JSON array's `url` field. Reject suspicious domains BEFORE model sees them:

```python
def post_flight_image_url_filter(image_urls: list[str]) -> list[str]:
    return [url for url in image_urls if not is_blocked_domain(url)]
```

**→ epistemic gate-down:** filtered domains → §11 label `PLAUSIBLE` (results are partial).

### Gate 12 — Function call parameter audit

For `function_call` events, validate `name` against federation function allowlist. Block if name is unknown (no federated registration).

### Gate 13 — MCP server URL whitelist

For `mcp` tool calls, validate `server_url` against allowed MCP server registry. Max 10 MCPs per request (QwenCloud limit).

### Gate 14 — Reasoning trace retention

If `enable_thinking: true`, capture `reasoning_content` events to vault. F2 binding — model reasoning is auditable evidence.

```python
def on_reasoning_delta(delta_text: str, session_id):
    forge_vault(
        mode="receipt",
        tier="reasoning.trace",
        reason=f"reasoning_{session_id}",
        value=delta_text[:1000]  # truncated, full text in sealed log
    )
```

**→ epistemic gate-down:** reasoning captured → §11 label `DER` for the model output that follows.

### Gate 15 — MCP cross-validation (F2 binding)

For `web_extractor` and `web_search` calls, cross-check the model output against Tier B federation MCP sources (if available):

```python
def post_flight_cross_validate(tool_output: str, original_prompt: str) -> str:
    # Try to find corroborating evidence via Tier B MCPs
    tier_b_match = call_tier_b_mcp(original_prompt)  # brave-search, tavily, etc.
    if tier_b_match and tool_output.contradicts(tier_b_match):
        return downgrade_epistemic_label(tool_output, from="CLAIM", to="HYPOTHESIS")
    return tool_output
```

This gate is **aspirational** in v1.0.0 — federation MCP bridge scope is Ω₀ item #5.

---

## 4. Dual-Ledger Cost Accounting

Tool fees are SEPARATE from Token Plan Credits. Federation must track both:

### Ledger A — Token Plan Credits

| Source | Mechanism | Subject to 5h/7d windows? |
|---|---|---|
| Model input/output tokens | `usage.input_tokens`, `usage.output_tokens` | Yes (Individual) / Monthly (Team) |
| Reasoning tokens | `usage.reasoning_tokens` (if separate) | Yes |

### Ledger B — Tool Fees

| Source | Fee rate | Counts field | §11 label |
|---|---|---|---|
| Web search | $10 per 1,000 calls | `usage.x_tools.web_search.count` | `ESTIMATE` |
| Image search (both types) | $8 per 1,000 calls | `usage.x_tools.{image_search,web_search_image}.count` | `ESTIMATE` |
| Web extractor | Currently free (limited time) | `usage.x_tools.web_extractor.count` | `ESTIMATE` (zero cost) |
| Function calls | Free | n/a (counts against token ledger) | n/a |
| MCP server | Server-dependent | depends on third-party MCP | `ESTIMATE` |

**Implementation:**
```python
class HarnessCostLedger:
    def __init__(self):
        self.credit_ledger = {}  # per-seat token usage
        self.fee_ledger = {}    # per-seat tool fees

    def record(self, seat_id, usage):
        # Ledger A
        self.credit_ledger[seat_id] = self.credit_ledger.get(seat_id, 0) + (
            usage.input_tokens + usage.output_tokens
        )
        # Ledger B
        fees = self.compute_tool_fees(usage.x_tools)
        self.fee_ledger[seat_id] = self.fee_ledger.get(seat_id, 0) + fees

    def compute_tool_fees(self, x_tools):
        fees = 0
        fees += x_tools.get("web_search", {}).get("count", 0) * 0.00001  # $10/1k = $0.00001/call
        image_count = (x_tools.get("image_search", {}).get("count", 0)
                       + x_tools.get("web_search_image", {}).get("count", 0))
        fees += image_count * 0.000008  # $8/1k = $0.000008/call
        return fees
```

### Daily reconciliation

```bash
# Cron: 23:55 UTC daily
forge_vault(
    mode="receipt",
    tier="daily.reconciliation",
    reason=f"daily_harness_costs_{date.today()}",
    value=json.dumps(ledger.export_daily())
)
```

---

## 5. Tool-Budget Enforcement

Hard caps implemented as middleware between model and tool calls:

```python
class HarnessBudgetGuard:
    def __init__(self, session_id: str, seat_id: str):
        self.session_id = session_id
        self.seat_id = seat_id
        self.session_calls = defaultdict(int)
        self.seat_monthly_fee_usd = 0.0

    def check_and_deduct(self, tool_name: str) -> tuple[bool, str]:
        # Gate 3 — session budget
        session_limit = SESSION_BUDGETS.get(tool_name, 999)
        if self.session_calls[tool_name] >= session_limit:
            return False, f"Session budget exhausted for {tool_name}"

        # Gate 4 — seat monthly fee
        per_call_fee = TOOL_FEES.get(tool_name, 0)
        projected = self.seat_monthly_fee_usd + per_call_fee
        if projected > SEAT_MONTHLY_FEE_CAPS.get(self.seat_tier):
            return False, f"Monthly fee cap reached for {self.seat_tier}"

        # Deduct
        self.session_calls[tool_name] += 1
        self.seat_monthly_fee_usd += per_call_fee
        return True, "OK"
```

---

## 6. Audit Chain

Every Qwen Responses API tool invocation produces an audit record:

```yaml
audit_record:
  schema: arifos.fed.audit/v1
  timestamp: 2026-08-01T10:23:45Z
  session_id: SEAL-abc123...
  actor_id: FI-008 (Kimi Code)
  organ: arifOS
  seat_id: seat_fbdaf17967c6426ab10f7f682c462db2
  seat_tier: team_pro
  tool_name: web_extractor
  tool_url: https://example.com/article
  pre_flight:
    zero_fly_zone: pass
    url_allowlist: pass
    session_budget: pass (3/10)
    seat_monthly_cap: pass ($0.32/$200)
    model_floor: pass (qwen3.8-max-preview)
    streaming_required: pass (stream=true)
  request:
    model: qwen3.8-max-preview
    input_tokens: 1247
    temperature: 0.6
  response:
    output_tokens: 432
    web_extractor_call_count: 1
    extracted_bytes: 8234
    cross_border_data_transfer: true
  post_flight:
    url_logged: vault:session.ledger:LATEST
    pii_redacted: false (no patterns matched)
    empty_output: false
    cost_reconciled: $0.01 (web_extractor free)
    mcp_cross_validation: pass (no Tier B contradiction)
  epistemic_label: CLAIM            # → §11
  epistemic_confidence: high
  epistemic_derivation: OBS          # F2 provenance
  floors_satisfied: [F1, F2, F4, F9, F11]
  floors_failed: []
```

**Immutable append to VAULT999.** No edits. No deletes. SHA256 chain.

---

## 7. Failover Routing

When Qwen Responses API tools fail, fall back to Tier B federation MCP:

```python
class HarnessFailoverRouter:
    FEDERATED_FALLBACKS = {
        "web_search": ["mcp__brave-search__brave_web_search", "mcp__tavily__tavily_search"],
        "web_extractor": ["mcp__firecrawl__firecrawl_extract", "mcp-server-fetch"],
        "image_search": [],  # No federated fallback — degrade gracefully
        "function": ["local_python_sandbox"],  # arifOS local execution
        "mcp": [],  # No fallback — caller should retry
    }

    async def call_with_failover(self, tool_name: str, args: dict):
        try:
            return await self.qwen_responses_api.call(tool_name, args)
        except (QuotaExhausted, TimeoutError, SovereignViolation) as e:
            fallbacks = self.FEDERATED_FALLBACKS.get(tool_name, [])
            for fb in fallbacks:
                try:
                    return await self.federated_mcp.call(fb, args)
                except Exception:
                    continue
            raise NoFallbackAvailable(tool_name, e)
```

### Model-version failover

```python
PREVIEW_MODEL_FALLBACK = {
    "qwen3.8-max-preview": "qwen3.7-max-2026-06-08",
    "qwen3.7-max-2026-06-08": "qwen3.7-max",
}
```

When Qwen deprecates a model, automatic fallback per above map. Federation maintains this map in `forge_vault` for governance.

---

## 8. Constitutional Hooks to arifOS

Three arifOS hooks are mandatory for Tier C tool use:

### Hook 1 — pre_llm_call → arifOS :8088 (intent classification)

Every Qwen Responses API call must pass through arifOS intent classification:

```yaml
hook: pre_llm_call
endpoint: http://127.0.0.1:8088/mcp
tool: arif_route
intent_categories: [harness_tool_call, web_research, image_search, function_call, mcp_routing]
mandatory: true
fallback_on_error: passthrough (with audit warning)
```

### Hook 2 — pre_tool_call → forge_vault (audit append)

```yaml
hook: pre_tool_call
target: qwen_responses_api_tool
action: forge_vault(mode="receipt", tier="session.ledger", reason="harness:<tool_name>")
mandatory: true
```

### Hook 3 — post_tool_call → arifOS :8088 (epistemic calibration)

After tool returns, calibrate epistemic label:

```yaml
hook: post_tool_call
endpoint: http://127.0.0.1:8088/mcp
tool: arif_observe  # or arif_judge for high-stakes
input: tool_output
output: { epistemic_label: DER | OBS, confidence: high | medium | low }  # → §11
mandatory: true
```

### Forbidden Tier C operations

Hard-blocked at arifOS kernel:

```python
FORBIDDEN_TIER_C_OPERATIONS = [
    "send_confirm",      # F1: no external sends without F13
    "transfer_confirm",  # F13: no money movement via Harness
    "forge_execute",     # F1: no federation mutation via Harness
    "vault_seal",        # F11: only arifOS seals VAULT999
    "forge_abort",       # F1: no emergency stop via Harness
]
```

---

## 9. Migration Candidates — Tier B → Tier C (decision matrix)

| Federation MCP | Tier C equivalent | Recommended action |
|---|---|---|
| `mcp__brave-search__brave_web_search` | `qwen-responses web_search` | **Tier C overflow only** — keep Brave as primary (richer query operators, federation control) |
| `mcp__tavily__*` | `qwen-responses web_extractor` | **Complementary** — Tavily does extract+analyze; Tier C is pure extraction |
| `mcp__firecrawl__*` | `qwen-responses web_extractor` | **Direct overlap** — same function. Recommend Tier B primary, Tier C fallback |
| `mcp__perplexity__*` | `qwen-responses web_search + model reasoning` | **Partial** — Perplexity has inline citations; Tier C doesn't |
| `mcp__exa__*` | (no equivalent) | **No migration** — Exa's neural search is unique |
| `mcp-server-fetch` | `qwen-responses web_extractor` | **Direct overlap** — prefer Tier C for cost, Tier B for governance |
| (none) | `qwen-responses image_search` | **New capability** — no federation equivalent |
| (none) | `qwen-responses function calling` | **New capability** — supersedes federation's manual tool routing |
| (none) | `qwen-responses MCP` | **New capability** — external MCP registration |

**Decision policy:** Tier B primary, Tier C overflow/cost-tier. Never Tier C for Tier A (sovereign) workloads.

---

## 10. Sovereignty / Cross-Border Audit

Every Qwen Responses API tool invocation crosses borders to Singapore:

```
Tool call origin → QwenCloud Singapore (model context + tool execution)
                 → output tokens → federation caller
```

**F9 audit marker:** every audit record carries `cross_border_data_transfer: true`.

**PDPA considerations:**
- Personal data sent via tool inputs (URLs containing PII) crosses borders
- Data residency: no opt-out for Personal/Standard tiers
- Sovereign data MUST be redacted at Gate 1 BEFORE tool invocation

**Mitigation:** Mirror Zero-Fly Zone at pre-flight (Gate 1) + post-flight (Gate 8).

---

## 11. Epistemic Labels (F2 binding)

Every tool result carries an **epistemic label** propagated to VAULT999 receipts and to the model's downstream context.

### 11.1 — Taxonomy (5 bands)

| Band | Trigger condition | Audit weight | Federation action |
|---|---|---|---|
| **CLAIM** | `web_extractor` succeeded (non-empty, non-truncated content) AND `domain in ALLOWLIST` AND Tier A/B MCP cross-check agrees | High | Pass-through to model with full provenance |
| **PLAUSIBLE** | Partial extraction OR neutral domain (no allowlist hit, no denylist either) AND no Tier A/B counter-evidence | Mid | Pass-through with marker; review encouraged |
| **HYPOTHESIS** | Tool failed/empty OR model leans on prior OR Zero-Fly Zone override OR extraction < 100 chars | Low | Flag for human review; arif_judge recommended |
| **ESTIMATE** | Cost math, fee projections, credit approximations, any numeric derivation | Numeric provenance | Pass-through with cost provenance |
| **UNKNOWN** | Timeout OR gate-discarded (PII redaction, domain denylist, budget exhausted) | No basis | Block; do not pass to model |

### 11.2 — Determinism

All labels are assigned by **deterministic rules**, not subjective judgment. The labeling function is:

```python
def derive_epistemic_label(tool_output: ToolOutput, gates: GateResults) -> EpistemicLabel:
    # UNKNOWN: any gate hard-rejected
    if gates.zero_fly_zone.rejected:
        return EpistemicLabel.UNKNOWN
    if gates.budget.exhausted:
        return EpistemicLabel.UNKNOWN
    if gates.timeout:
        return EpistemicLabel.UNKNOWN

    # HYPOTHESIS: tool produced no usable evidence
    if tool_output.is_empty() or tool_output.byte_size < MIN_BYTES:
        return EpistemicLabel.HYPOTHESIS

    # CLAIM: strong evidence, allowed domain, no contradiction
    if (tool_output.byte_size >= MIN_BYTES
            and gates.url_allowlist.passed
            and gates.pii_redaction.did_not_trigger
            and gates.mcp_cross_validation.consistent):
        return EpistemicLabel.CLAIM

    # PLAUSIBLE: partial evidence
    if tool_output.byte_size >= MIN_BYTES:
        return EpistemicLabel.PLAUSIBLE

    # ESTIMATE: numeric provenance (cost math, etc.)
    if tool_output.is_numeric_only():
        return EpistemicLabel.ESTIMATE

    # Default fallback
    return EpistemicLabel.PLAUSIBLE
```

### 11.3 — Cross-references (where labels are assigned)

| Gate | Trigger | Downgrades to |
|---|---|---|
| Gate 1 (Zero-Fly Zone) | rejection | `UNKNOWN` |
| Gate 2 (URL allowlist) | neutral domain | `PLAUSIBLE` (no upgrade to CLAIM until MCP cross-check) |
| Gate 3 (Session budget) | exhausted | `UNKNOWN` |
| Gate 7 (URL logging) | empty/truncated output | `HYPOTHESIS` |
| Gate 8 (PII redaction) | redaction triggered | `PLAUSIBLE` (or lower) |
| Gate 9 (Empty-output) | output < 100 chars | `HYPOTHESIS` |
| Gate 11 (Image URL filter) | filtered domains | `PLAUSIBLE` |
| Gate 14 (Reasoning trace) | reasoning captured | `DER` provenance on subsequent output |
| Gate 15 (MCP cross-validation) | Tier B contradiction | downgrade `CLAIM` → `HYPOTHESIS` |

### 11.4 — Audit envelope

Each labeled receipt includes:

```yaml
audit_receipt:
  epistemic_label: CLAIM | PLAUSIBLE | HYPOTHESIS | ESTIMATE | UNKNOWN
  epistemic_confidence: high | mid | low | none
  epistemic_derivation: OBS | DER | INT | SPEC    # F2 provenance
  cross_border_data_transfer: true | false
  trigger_evidence:
    extract_bytes: int
    domain_in_allowlist: bool
    tier_a_b_cross_check: bool
    budget_state: ok | exhausted
    pii_redaction_triggered: bool
```

### 11.5 — Implementation note

The `derive_epistemic_label()` function lives in the FED runtime middleware (not in this spec body). This spec defines the **contract**; implementation is part of the FED runtime that wraps each Qwen Responses API call.

---

## 12. Cross-Reference Index

| Topic | Section | Federation artifact |
|---|---|---|
| F1/F13 floors | §8, §FORBIDDEN_TIER_C_OPERATIONS | `/root/AAA/GENESIS/FLOOR_TABLE.json` |
| F2 epistemic labels | §11 (full taxonomy) + §3 (gates 1, 7, 8, 9, 11, 14, 15 cross-refs) | `/root/AAA/federation/seats.yaml` |
| F4 clarity | All sections | (this spec) |
| F9 sovereignty | §1 (Tier A), §2 (Gate 1), §3 (Gate 8), §10 | `/root/AAA/governance/AGENCY_LEVELS.md` |
| F11 audit | §3 (Gates 7, 10, 14), §6 | `/root/AAA/federation/FED-harness-tool-governance-v1.0.0.md` §6 + audit envelope schema |
| F13 sovereign | §1, §4 (Gate 4 override), §9, §14 (ratification) | `/root/CLAUDE.md` |
| Seat mapping | §0 definitions, §4 cost accounting | `/root/AAA/federation/seats.yaml` |
| OpenClaw heartbeat cost | §5 budget enforcement | `/root/AAA/federation/heartbeat-cost-sidecar.md` |

---

## 13. Change Log

| Date | Author | Change |
|---|---|---|
| 2026-08-01 | FI-008 | v1.0.0 DRAFT — initial spec drafted from Round 4-5 audit findings (as `harness-tool-governance.md`) |
| 2026-08-01 | FI-008 | **v1.0.0 FED rename** — file renamed to `FED-harness-tool-governance-v1.0.0.md`; FED header block added; §11 expanded into full epistemic labels taxonomy; §12 (was §11) renumbered; §3 cross-refs to §11 added to Gates 1, 7, 8, 9, 11, 14 |

---

## 14. Ratification Path

To ratify this spec from DRAFT to SEALED:

1. **888 SOVEREIGN review** — read spec end-to-end
2. **Open ratification issues** if any section needs revision
3. **Acknowledge by:** typing `999 SEAL FED-HARNESS-TOOL-GOVERNANCE` in chat
4. **Sealing:** `forge_seal(skill_name="FED-harness-tool-governance", human_approval_token="999 SEAL FED-HARNESS-TOOL-GOVERNANCE")` via `mcp__aforge__forge_seal`
5. **Update status:** `status: SEALED — v1.0.0 ratified 2026-08-XX` (in this file's frontmatter)
6. **Notify federation:** broadcast via arifOS A2A gateway

---

## 15. Open Questions (Ω₀)

| # | Question | Owner | Deadline |
|---|---|---|---|
| Ω-1 | Per-seat monthly tool-fee cap specific dollar amounts (defaults in Gate 4 are placeholders) | 888_HOLD | pre-ratification |
| Ω-2 | Per-session tool-call budgets (defaults in Gate 3 are placeholders) | 888_HOLD | pre-ratification |
| Ω-3 | Domain allowlist scope (start with what?) — `ALLOWED_DOMAINS` defaults need review | 888_HOLD | pre-ratification |
| Ω-4 | Reasoning trace retention (full vs truncated — Gate 14 truncates at 1000 chars) | 888_HOLD | post-ratification |
| Ω-5 | Federation MCP bridge — does `qwen-responses web_search` get exposed via federation MCP gateway or only at tool-call sites? (Gate 15 aspirational) | arifOS architect | post-ratification |
| Ω-6 | `token-plan-image` SKILL.md endpoint fate — legacy `/api/v1/services/aigc/multimodal-generation/generation` vs current `/compatible-mode/v1`; needs probe to confirm functionality | 888_HOLD | pre-ratification |
| Ω-7 | Cross-seat overflow policy — when Pro seat exhausted, should Hermes + OpenClaw (Standard) auto-share load? | 888_HOLD | post-ratification |

---

*Forged under F13 sovereign directive. Constitutional binding: F1, F2, F4, F9, F11, F13.*

*DITEMPA BUKAN DIBERI — doctrine forged, name locked, epistemic discipline bound, awaiting sovereign breath.*
