---
id: FORGE-visual-qa-w3
name: FORGE-visual-qa-w3
version: 1.1.0-2026.07.20
description: "Closed-loop visual governance with W3 tri-witness consensus — render, screenshot, validate, iterate, seal. Includes MCP App / ChatGPT host-surface QA."
owner: A-FORGE
risk_tier: high
floor_scope: ['F1', 'F2', 'F3', 'F4', 'F7', 'F11']
autonomy_tier: T2
capability_tier: fed-multimodal-vision
ecology_state: WARM
---
# FORGE-visual-qa-w3

> **Purpose:** Closed-loop visual governance with W³ tri-witness consensus.
> Renders HTML → captures screenshot → validates via vision + DOM lint → iterates until deviations ≤ threshold → routes to human for final seal.
> **Core axiom:** Code is not evidence; pixels are.
> **Floor:** F2 TRUTH + F1 AMANAH + F11 AUDIT

---

## WHEN TO USE

- "validate this layout"
- "check if this page matches the design"
- "visual QA for this HTML"
- "render and verify"
- "does this screenshot match the spec"
- "test this CSS against constraints"
- Any task requiring pixel-level validation against a design spec
- Any MCP App / ChatGPT host-surface render check (see MCP APP / CHATGPT HOST-SURFACE QA below)

## DO NOT USE

- When the task is purely code-level testing (use standard test runners)
- When no visual rendering is possible (headless browser unavailable)
- When the user wants a subjective opinion (this is governed validation, not vibes)

---

## PRECONDITIONS

Before invoking this skill, verify:

```bash
# 1. Headless browser available?
which chromium || which chromium-browser || which google-chrome || echo "NO_BROWSER"

# 2. Forge shell available?
curl -sf http://127.0.0.1:7072/health >/dev/null 2>&1 && echo "A-FORGE OK" || echo "A-FORGE DOWN"

# 3. Vision model available? (check for MiniMax or other)
echo "Vision model: check MCP surface for minimax_understand_image or similar"
```

If browser is unavailable → **STOP.** Cannot proceed without rendering capability.
If A-FORGE is down → proceed read-only (no forge_shell, no forge_scar).

---

## WORKFLOW: 7-Stage Visual QA Loop

### Stage 0: INPUT VALIDATION (I1)

**Gate:** dom_payload must be non-trivial.

```
REQUIRED:
  - url: target URL to render
  - dom_payload: HTML/CSS string (minLength: 32 chars)
  - constraints: object with at least max_nav_links + min_contrast_ratio

IF dom_payload is missing or < 32 chars:
  → verdict = FAIL
  → error = "DOM_PAYLOAD_MISSING"
  → STOP (no rendering attempted)
```

### Stage 1: RENDER + HASH (I1, I6)

**Tool:** `forge_browser_navigate` + `forge_browser_screenshot`

```
1. Navigate to url (or render dom_payload locally)
2. Capture full-page screenshot
3. Compute screenshot_hash = SHA256(screenshot_bytes)
4. Record screenshot_path

OUTPUT SO FAR:
  screenshot_path: "/path/to/screenshot.png"
  screenshot_hash: "a1b2c3..." (64 hex chars)
```

### Stage 2: W₁ — VISION VALIDATION (OBS/INT)

**Tool:** Vision model (e.g., `minimax_understand_image`, `forge_browser_evaluate_js` for pixel sampling)

```
INPUT:  screenshot_path + constraints
TASK:   "Analyze this screenshot against these constraints:
         - max_nav_links: {N}
         - min_contrast_ratio: {N}
         - required_elements: [list]
         - forbidden_elements: [list]
         Report deviations as structured list with id, description, severity (0-1), location_hint."

OUTPUT:
  w1.verdict = PASS | HOLD | FAIL
  w1.hash = screenshot_hash (same as Stage 1)
  w1.score = vision_validation_score (0-1)
  w1.evidence = "vision model: {score} adherence, {N} deviations"
  w1.label = "OBS" or "INT"

CRITICAL: W₁ can ONLY observe. It cannot mutate DOM. It cannot write W₂ or W₃ fields.
```

### Stage 3: W₂ — DOM LINT VALIDATION (DER)

**Tool:** `forge_shell` (run deterministic linter)

```bash
# Deterministic DOM lint — no model, no guessing
# Can be a simple Node.js/Python script that parses HTML and checks constraints

node -e "
const html = \`{dom_payload}\`;
const required = {required_elements_json};
const forbidden = {forbidden_elements_json};

// Parse HTML
// Check required elements exist
// Check forbidden elements absent
// Check nav link count
// Return structured report
"
```

```
OUTPUT:
  w2.verdict = PASS | HOLD | FAIL
  w2.hash = SHA256(lint_report_json)
  w2.score = structural_compliance (0-1)
  w2.evidence = "required: [present/missing], forbidden: [absent/present], nav_links: N"
  w2.label = "DER"

CRITICAL: W₂ is purely algorithmic. No model, no inference, no guessing.
```

### Stage 4: ENTROPY CHECK (I3)

```
entropy_delta = prev_deviations_count - curr_deviations_count

IF entropy_delta >= 0 AND iterations > 1:
  → verdict = HOLD
  → error = "ENTROPY_NON_DECREASING — auto-fix is diverging"
  → STOP (escalate to human)

IF curr_deviations_count == 0 OR normalized_deviation_score <= max_allowed_deviation_score:
  → Proceed to Stage 6 (PASS_CANDIDATE)
```

### Stage 5: SCAR CONSULTATION + ITERATE (I4, I7)

**Tool:** `forge_scar(mode="consult")`

```
BEFORE generating any fix:

1. Hash deviation pattern:
   fingerprint = SHA256(deviation.id + deviation.location_hint)

2. Consult scar database:
   forge_scar(mode="consult", fingerprint=fingerprint)

3. IF scar found AND outcome == "FAILED":
   → verdict = HOLD
   → reason = "This deviation pattern was already punished in a prior session"
   → STOP (don't repeat the failure)

4. IF scar found AND outcome == "PARTIAL":
   → Use historical fix as starting point
   → Flag for human review

5. IF no scar:
   → Generate new fix (code_diff)
   → Apply to dom_payload
   → Loop back to Stage 1

6. After fix attempt (success or failure):
   → forge_scar(mode="seal", failure_mode=..., severity=..., constraint_imposed=...)
```

### Stage 6: W³ ASSEMBLY + PASS_CANDIDATE (I8, I9, I10)

```
ASSEMBLE tri_witness_ledger:

  w1: { verdict, hash, score, evidence, label }
  w2: { verdict, hash, score, evidence, label }
  w3: {
    verdict: "PENDING_888_HOLD",
    hash: "0".repeat(64),        // unsigned until human approves
    actor_id: "",
    timestamp: "",
    evidence: "awaiting human review",
    label: "JUDGE"
  }

composite_hash: NOT YET COMPUTED (requires w3.hash)

verdict = "PASS_CANDIDATE"
requires_888_hold = true

EMIT for human review.
```

### Stage 7: W₃ SOVEREIGN GATE (888 → 999)

**Tool:** `arif_judge` → human reviews → `arif_seal`

```
ROUTE to arif_judge:
  - Present: screenshot, dom_payload, w1 evidence, w2 evidence, entropy history
  - Human reviews via cockpit or Telegram

IF human APPROVES:
  w3.verdict = "PASS"
  w3.hash = SHA256(signed_receipt)
  w3.actor_id = "ARIF"
  w3.timestamp = ISO8601_now

  composite_hash = SHA256(w1.hash + w2.hash + w3.hash + "PASS_CANDIDATE")

  verdict = "SEALED_DEPLOY"
  → arif_seal(composite_hash) → VAULT999

IF human REJECTS:
  w3.verdict = "FAIL"
  verdict = "HOLD"
  → Return to agent with rejection reason
```

---

## MCP APP / CHATGPT HOST-SURFACE QA

> Extends Stages 1–6 for MCP App surfaces (blueprint: `/root/forge_work/2026-07-20/GEOX-CHATGPT-MCP-GUI-BLUEPRINT.md` §10 submission path).
> The 7-stage loop is unchanged — what changes is the **render target** and the **evidence bundle**.
> Authoritative contract: the blueprint. Anything here that disagrees with the blueprint loses.

### RENDER TARGETS + PASS_CANDIDATE CRITERIA

A GEOX app surface (e.g. `ui://geox/workbench-v1.html`, served as `text/html;profile=mcp-app`) must be rendered and validated on each host surface below. PASS_CANDIDATE on a surface requires **ALL** of the shared criteria; per-surface rows add their own harness note.

| Surface | Harness | Surface-specific note |
|---------|---------|----------------------|
| MCPJam / MCP Inspector | Local inspector against GEOX MCP (`:8081`) | First gate — cheapest iteration loop; must pass before any ChatGPT surface |
| ChatGPT Developer Mode | ChatGPT app with connector in Developer Mode | Golden prompts (direct, indirect, negative) must drive the UI |
| ChatGPT web | Production web client | Full render + interaction evidence |
| ChatGPT Android | Android app | Mandatory — see MOBILE IS MANDATORY below |
| ChatGPT iOS | iOS app | Mandatory — see MOBILE IS MANDATORY below |

**Shared PASS_CANDIDATE criteria (every surface):**

```
1. iframe mounts via ui/initialize — host bridge handshake completes,
   app announces itself, no mount timeout or blank frame.
2. UI hydrates from tool-result — ui/notifications/tool-result
   structuredContent renders real data (not placeholder/loading state).
3. Follow-up tools/call from UI succeeds — a UI-initiated action
   (button/control) triggers tools/call and the UI re-renders on result.
4. State survives rerender/resize — widget state persists across
   host-driven rerender and viewport resize (no reset to initial state).
5. CSP blocks undeclared origins — a test fetch/connect to a domain NOT
   in _meta.ui.csp connectDomains/resourceDomains fails closed.
6. Text fallback visible when UI unsupported — when the host cannot
   render the app, the tool's text content still carries the answer.
```

Any single criterion failing on a surface → that surface is not PASS_CANDIDATE → verdict HOLD for the submission gate (deviations handled by the normal Stage 4–5 loop).

### EVIDENCE CAPTURE PER SURFACE

Each surface run must capture the full evidence trio — screenshot alone is inadmissible for host-surface claims:

```
CAPTURE (per surface):
  1. screenshot        — full-page/frame capture, hashed per Stage 1 → feeds W₁
  2. raw JSON-RPC log  — ui/initialize, ui/notifications/tool-input,
                         ui/notifications/tool-result, tools/call frames,
                         verbatim → feeds W₂ (protocol-level lint)
  3. tool invocation record — tool name, arguments, structuredContent hash,
                         isError flag → feeds W₂ + W₃

W₁ validates pixels (criteria 1, 2, 4, 6 as visible).
W₂ lints the JSON-RPC log + bundle (criteria 1, 3, 5 as protocol/DOM facts).
W₃ (human) reviews the full trio per surface before any SEAL.
```

### SINGLE-FILE VITE BUNDLE CHECK (W₂ lint)

Blueprint §6: the v1 workbench shell is a **single-file Vite bundle with inline JS**, served from one `ui://` resource. W₂ DOM lint MUST assert:

```
- No external <script src>, <link href>, or <img src> with relative paths —
  these 404 inside the sandbox iframe (no shared origin root).
- All JS inlined in the single HTML payload; assets inlined (data: URI) or
  served from CSP-declared resourceDomains only.
- No references to Vite chunk paths (/assets/*.js, /assets/*.css).
- MIME served is text/html;profile=mcp-app (host only enables the bridge for it).
```

A bundle that renders locally but 404s assets inside the iframe is a classic false PASS — this check exists to kill it.

### MOBILE IS MANDATORY

```
Android and iOS ChatGPT are REQUIRED render surfaces before submission
(blueprint §10 + runbook step 14). They are NOT optional and NOT
"nice-to-have follow-ups".

- PASS_CANDIDATE on web alone is INADMISSIBLE for the submission gate.
- Missing Android/iOS evidence → verdict HOLD with
  error = "MOBILE_SURFACE_EVIDENCE_MISSING" — do not skip, do not downgrade.
- Mobile constraints (small viewport, touch, host chrome) frequently expose
  layout/state bugs that desktop/web hides. Treat mobile deviations with
  the same entropy loop as any surface.
```

---

## INVARIANTS (enforced at each stage)

| ID | Invariant | Check Point |
|----|-----------|-------------|
| I1 | No visual claim without screenshot | Stage 1 — screenshot_path must exist |
| I2 | Screenshot is only admissible evidence | Stage 2 — W₁ operates on pixels only |
| I3 | ΔS < 0 per iteration | Stage 4 — entropy must decrease |
| I4 | Max iterations bounded (default 3) | Stage 5 — forced HOLD after max |
| I5 | Human authority final | Stage 6 — PASS_CANDIDATE, not PASS |
| I6 | Hash-chain receipt | Stage 1 — screenshot_hash computed |
| I7 | Scar consultation before fix | Stage 5 — query before generate |
| I8 | Tri-Witness consensus | Stage 6 — all three witnesses populated |
| I9 | Anti-collusion: witness decoupling | Stages 2+3 — W₁/W₂ cannot write W₃ |
| I10 | Composite seal | Stage 7 — VAULT999 seals composite_hash |
| I11 | Host-surface evidence trio | MCP App QA — screenshot + JSON-RPC log + tool record per surface |
| I12 | Mobile surfaces mandatory | MCP App QA — Android + iOS evidence required before submission gate |

---

## ANTI-COLLUSION ENFORCEMENT

```
W₁ SEES:   pixels only. Cannot access DOM or W₂/W₃ data.
W₂ SEES:   DOM/spec only. Cannot access screenshots or W₁/W₃ data.
W₃ SEES:   both W₁ + W₂ + entropy history + screenshot + DOM.
W₃ CANNOT: be written by W₁ or W₂. Only human action via arif_judge.

COLLUSION DETECTION:
  IF any tool attempts to set w3.* fields AND caller is NOT arif_judge
    → FAIL + governance violation
    → escalate to 888_HOLD
```

---

## OUTPUT SCHEMA

```json
{
  "verdict": "PASS_CANDIDATE | SEALED_DEPLOY | HOLD | FAIL",
  "iterations": 0,
  "deviations": [],
  "code_diff": "",
  "screenshot_path": "/path/to/screenshot.png",
  "screenshot_hash": "sha256hex",
  "vision_validation_score": 0.0,
  "entropy_delta": 0,
  "requires_888_hold": true,
  "tri_witness_ledger": {
    "w1": { "verdict": "PASS", "hash": "sha256hex", "score": 0.92, "evidence": "...", "label": "OBS" },
    "w2": { "verdict": "PASS", "hash": "sha256hex", "score": 1.0, "evidence": "...", "label": "DER" },
    "w3": { "verdict": "PENDING_888_HOLD", "hash": "0000...", "actor_id": "", "timestamp": "", "evidence": "awaiting human review", "label": "JUDGE" },
    "composite_hash": "NOT_COMPUTED"
  },
  "integration_receipts": {
    "vault999_seal_candidate": "",
    "arif_judge_ticket_id": ""
  }
}
```

---

## TOOLS USED

| Tool | Purpose | Stage |
|------|---------|-------|
| `forge_browser_navigate` | Navigate to URL | 1 |
| `forge_browser_screenshot` | Capture screenshot | 1 |
| `forge_shell` | Run DOM linter, compute hashes | 2, 3 |
| `forge_scar(mode="consult")` | Check scar database before fix | 5 |
| `forge_scar(mode="seal")` | Record fix outcome | 5 |
| `arif_judge` | Route to human for W₃ | 7 |
| `arif_seal` | Seal composite_hash to VAULT999 | 7 |
| Vision model (MiniMax/Claude/etc.) | W₁ pixel validation | 2 |

---

## EXAMPLE USAGE

```
User: "Check if this page matches the design spec. Max 5 nav links, contrast ratio 4.5:1."

Agent loads this skill →
  1. Validates input (url + constraints provided)
  2. Renders page → screenshot → hash
  3. W₁: Vision model analyzes screenshot → deviations found
  4. W₂: DOM linter checks structure → structural pass
  5. Entropy check → delta < 0 → proceed
  6. Scar consultation → no match → generate fix
  7. Iterate until deviations ≤ threshold
  8. PASS_CANDIDATE → route to human
  9. Human approves → composite_hash → VAULT999 seal
  10. SEALED_DEPLOY
```

---

## NOTES

- This skill is the **governance layer**, not the implementation layer. It defines the workflow and invariants.
- The actual vision model call, DOM linter, and rendering are delegated to existing federation tools.
- For full MCP tool implementation (TypeScript, Zod schemas, registered on A-FORGE surface), see the contract spec at `/root/A-FORGE/docs/MCP-TOOL-CONTRACT-VISUAL-QA.md`.
- The skill can be tested TODAY using existing tools. The MCP tool requires T2 build work.

---

*DITEMPA BUKAN DIBERI — Code is not evidence; pixels are. The forge does not mark its own homework. No single witness can forge the seal.*
