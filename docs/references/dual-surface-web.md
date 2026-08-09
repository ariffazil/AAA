# Dual-Surface Web Applications

> **When one organ serves both humans and agents, the implementation must be one service with two faces — not two services pretending to be one.**

---

## 1. The Three Layers

Every dual-surface application has exactly three layers:

```
┌─────────────────────────────────────────────────┐
│  Human Surface (HTML)                           │
│  Forms · Navigation · Explanatory content       │
│  Served via HTTP/HTTPS to browsers              │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  Shared Domain Service                          │
│  Business logic · Data access · Policy engine   │
│  Single source of truth for both surfaces       │
└────────────────────▲────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────┐
│  Agent Surface (MCP / WebMCP)                   │
│  Tools · Resources · Prompts · Schemas          │
│  Served via MCP transport (stdio/HTTP/SSE)      │
└─────────────────────────────────────────────────┘
```

### Rules

| # | Rule | Consequence of violation |
|---|---|---|
| 1 | HTML and MCP must NOT contain separate business logic | Divergent behaviour — humans see one answer, agents see another |
| 2 | Human and agent surfaces must use the same canonical service layer | Bug fixes in one surface don't propagate to the other |
| 3 | Tool manifests must be generated from runtime registration | Stale manifests → model calls tools that don't exist or have wrong schemas |
| 4 | Agent tools must declare side effects and authority requirements | Model cannot distinguish read from mutate; governance gates can't fire |
| 5 | Public health endpoints must not require sovereign sessions | Health probes are observational (T1); requiring auth blocks monitoring |
| 6 | Protected tool routes must validate signed session capability tokens | Unprotected mutation tools → authorization bypass |
| 7 | Browser-facing actions must have equivalent machine-readable semantics | Agents can't replicate what humans do; humans can't understand what agents did |

---

## 2. Architecture Pattern

### 2.1 Shared Domain Service

The domain service owns all business logic. Neither surface implements its own.

```python
# domain/capital_service.py — single source of truth

class CapitalService:
    """Shared capital computation service.
    
    Used by both the HTML surface (via route handlers)
    and the MCP surface (via tool implementations).
    """
    
    def compute_npv(self, cash_flows: list[float], discount_rate: float) -> float:
        """Net present value — canonical implementation."""
        ...
    
    def get_market_data(self, commodity: str) -> dict:
        """Live market data — canonical implementation."""
        ...
```

### 2.2 Human Surface (HTML)

Routes render HTML using the shared service. No business logic in templates.

```python
# routes/html_routes.py

from domain.capital_service import CapitalService

service = CapitalService()

@app.route("/wealth/npv")
def npv_page():
    """Human-facing NPV calculator."""
    result = service.compute_npv(
        cash_flows=request.args.getlist("cf", type=float),
        discount_rate=float(request.args.get("rate", 0.10)),
    )
    return render_template("npv.html", result=result)
```

### 2.3 Agent Surface (MCP)

Tools call the same shared service. No business logic in tool handlers.

```python
# mcp/tools.py

from domain.capital_service import CapitalService

service = CapitalService()  # same instance, same logic

@mcp.tool(name="capital_primitive",
          annotations={"readOnlyHint": True})
async def capital_primitive(mode: str, cash_flows: list[float] = None, 
                            discount_rate: float = None) -> str:
    """Compute capital primitives (NPV, IRR, EMV, Kelly, ...).
    Use when the user asks about financial calculations, investment analysis,
    or capital allocation decisions.
    """
    if mode == "npv":
        result = service.compute_npv(cash_flows, discount_rate)
        return json.dumps({"mode": "npv", "result": result, "tool_name": "capital_primitive"})
    ...
```

---

## 3. Tool Manifest Generation

Tool manifests must be generated from runtime registration, not hand-maintained.

```python
# scripts/generate_manifest.py
"""Generate the tool manifest from the live MCP server.

Run after any tool change to update the conformance suite's expected set.
"""
from mcp_server import mcp  # import the live server

tools = mcp.list_tools()
manifest = {
    "organ": "wealth",
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "tools": [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.inputSchema,
            "annotations": t.annotations,
            "side_effects": t.annotations.get("sideEffects", "none"),
            "authority_required": t.annotations.get("authorityRequired", "OBSERVE_ONLY"),
        }
        for t in tools
    ],
}
print(json.dumps(manifest, indent=2))
```

### Annotations for Dual-Surface Tools

Every tool in a dual-surface application MUST declare:

| Annotation | Type | Meaning |
|---|---|---|
| `readOnlyHint` | `bool` | `true` = observation only, no state change |
| `sideEffects` | `string` | `"none"` / `"state_change"` / `"external_action"` / `"irreversible"` |
| `authorityRequired` | `string` | Minimum authority band: `OBSERVE_ONLY` / `OPERATOR` / `LIMITED_MUTATE` / `FULL` / `SOVEREIGN` |
| `destructiveHint` | `bool` | `true` = operation cannot be undone |
| `humanEquivalent` | `string` | Route or action on the human surface that does the same thing |

Example:

```python
@mcp.tool(
    name="wealth_transfer",
    annotations={
        "readOnlyHint": False,
        "sideEffects": "irreversible",
        "authorityRequired": "SOVEREIGN",
        "destructiveHint": True,
        "humanEquivalent": "/wealth/transfer",
    },
)
async def wealth_transfer(amount: float, currency: str, recipient: str) -> str:
    """Execute a capital transfer.
    Use when the sovereign authorises a fund transfer.
    REQUIRES: SOVEREIGN authority. Irreversible.
    """
    ...
```

---

## 4. Authority and Session Enforcement

### 4.1 Public Endpoints (No Auth Required)

These endpoints serve observational data and must NOT require session tokens:

| Pattern | Examples |
|---|---|
| Health check | `/health`, `/ready` |
| Public content | `/`, `/about`, `/docs` |
| Read-only MCP tools | `readOnlyHint: true` tools with `authorityRequired: OBSERVE_ONLY` |
| Discovery | `/.well-known/agent.json`, `/mcp` (initialize + tools/list) |
| Static assets | CSS, JS, images, fonts |

### 4.2 Protected Endpoints (SCT Required)

These endpoints perform mutations and MUST validate session capability tokens:

| Pattern | Validation |
|---|---|
| Mutation MCP tools | `authorityRequired >= OPERATOR` → validate SCT via `verify_federation_sct()` |
| Form submissions (HTML) | CSRF token + session cookie → same authority check server-side |
| API endpoints | Bearer token or SCT in `Authorization` header |
| WebSocket/SSE mutations | SCT in initial handshake or first message |

### 4.3 Validation Flow

```
Request arrives
    │
    ├─ Is it public (health, read-only, discovery)?
    │   └─ YES → proceed without auth
    │
    ├─ Is it an MCP tool call?
    │   └─ Check tool.annotations.authorityRequired
    │       ├─ OBSERVE_ONLY → proceed
    │       └─ >= OPERATOR → extract SCT from _meta → verify_federation_sct()
    │           ├─ ok=True → proceed with claims
    │           └─ ok=False → reject with structured error
    │
    └─ Is it an HTML form submission?
        └─ Validate CSRF + session → check role authority → proceed or reject
```

---

## 5. WebMCP and Agent Card

### 5.1 WebMCP Manifest

Dual-surface applications MUST expose a WebMCP manifest at `/.well-known/webmcp.json`:

```json
{
  "name": "wealth",
  "version": "v2026.07.14",
  "description": "WEALTH capital intelligence — NPV, risk, conservation, flow",
  "mcp_endpoint": "/mcp",
  "health_endpoint": "/health",
  "agent_card": "/.well-known/agent.json",
  "human_surface": "/",
  "tools_count": 8,
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": false
  }
}
```

### 5.2 Agent Card

Every dual-surface organ MUST expose an A2A agent card at `/.well-known/agent.json`:

```json
{
  "name": "wealth",
  "url": "https://wealth.arif-fazil.com",
  "description": "Capital intelligence — NPV, risk, conservation, flow",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "capital-compute",
      "name": "Capital Primitives",
      "description": "NPV, IRR, EMV, Kelly criterion, Monte Carlo"
    }
  ]
}
```

---

## 6. Navigation Consistency

### 6.1 Global Navigation

All federation surfaces share a consistent navigation structure:

```
┌─────────────────────────────────────────────────┐
│  [arifOS]  [GEOX]  [WEALTH]  [WELL]  [AAA]     │  ← global nav
├─────────────────────────────────────────────────┤
│  [Overview] [Live Data] [Tools] [Methodology]   │  ← local nav
├─────────────────────────────────────────────────┤
│                                                 │
│  Page content                                   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 6.2 Agent Discovery Parity

Every human-visible navigation item must have a machine-discoverable equivalent:

| Human element | Agent equivalent |
|---|---|
| Global nav links | Agent card `skills[]` or WebMCP manifest |
| Local nav sections | MCP resource templates or tool groupings |
| "About" page | `description` field in agent card |
| "Methodology" page | MCP resource at documented URI |
| Search | MCP tool with query parameter |
| Error page | Structured error envelope in MCP response |

---

## 7. Design System Contract

### 7.1 Shared Tokens

All federation surfaces use the same design tokens:

```css
:root {
  /* Typography */
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* Colours — from arifOS identity */
  --color-bg: #0a0a0a;
  --color-surface: #141414;
  --color-text: #e5e5e5;
  --color-accent: #3b82f6;
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  
  /* Layout */
  --max-width: 1200px;
  --nav-height: 3.5rem;
}
```

### 7.2 Responsive Breakpoints

| Breakpoint | Width | Layout |
|---|---|---|
| Mobile | < 640px | Single column, hamburger nav |
| Tablet | 640–1024px | Two column, collapsible sidebar |
| Desktop | > 1024px | Full layout, persistent nav |

---

## 8. Testing Requirements

Every dual-surface application must pass:

| Test | Scope | Tool |
|---|---|---|
| Link check | All `<a href>` resolve | `check_links.py` |
| Schema validation | MCP tool schemas match runtime | `validate_manifest.py` |
| Accessibility | WCAG 2.1 AA | axe-core or pa11y |
| Security scan | No XSS, CSRF, injection | semgrep / OWASP ZAP |
| Manifest parity | WebMCP manifest matches actual tools | `validate_surface.py` |
| Agent card parity | Agent card skills match tool surface | custom assertion |
| Health endpoint | Returns 200 without auth | curl |
| SCT enforcement | Mutation tools reject missing/invalid SCT | `test_federation_sct.py` |
| Navigation parity | Every human nav item has agent equivalent | manual or custom crawl |

---

## 9. Anti-Patterns

| Anti-Pattern | Why it's wrong |
|---|---|
| Separate Express + FastMCP servers with duplicated logic | Bug in one doesn't fix the other |
| HTML templates containing business logic | Can't test logic independently; agents can't access |
| MCP tools reimplementing what HTML routes already do | Two sources of truth; divergent answers |
| Hand-maintained tool manifest JSON | Stale manifests; conformance suite reports false drift |
| Health endpoint behind auth | Monitoring breaks; can't probe liveness |
| Mutation tools without `authorityRequired` annotation | Model treats destructive ops as safe reads |
| `humanEquivalent: null` on mutation tools | No audit trail linking agent action to human-visible effect |
| Different error messages for HTML vs MCP | Humans and agents get different answers for the same failure |

---

## 10. Reference Implementation

The canonical dual-surface pattern for the arifOS federation:

| Organ | Human surface | Agent surface | Shared service |
|---|---|---|---|
| WEALTH | `wealth.arif-fazil.com` | WEALTH MCP `:18082` | `domain/capital_service.py` |
| GEOX | `geox.arif-fazil.com` | GEOX MCP `:8081` | `domain/earth_service.py` |
| WELL | `well.arif-fazil.com` | WELL MCP `:18083` | `domain/vitality_service.py` |
| arifOS | `arif-fazil.com` | arifOS MCP `:8088` | `domain/kernel_service.py` |
| AAA | `arif-fazil.com/aaa` | AAA A2A `:3001` | `domain/control_plane.py` |

---

*Forged: 2026-07-14 · PR2 of agentic site builder plan*
*DITEMPA BUKAN DIBERI — One service, two faces, one truth.*
