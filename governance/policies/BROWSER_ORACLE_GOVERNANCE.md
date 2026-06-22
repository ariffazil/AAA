# BROWSER ORACLE GOVERNANCE — arifOS Constitutional Policy

> **Forged:** 2026-06-19T22:30:00+08:00
> **Authority:** AAA Control Plane · arifOS Federation
> **Classification:** CONSTITUTIONAL — F1-F13 binding
> **Supersedes:** None (inaugural)
> **Seal:** PENDING (888_JUDGE → VAULT999)

---

## 0. THESIS: Browser Is a Basic Agent Right

**CLAIM (SEALED):** In a sovereign agentic OS like arifOS, browser access under constitutional control is a **basic agent right** — not a nice-to-have feature. It is the minimum I/O capability required for an agent to act as a real operator in the digital environment, not merely a text advisor.

### Five Grounds

| # | Ground | Why |
|---|--------|-----|
| 1 | **Reality lives in the browser** | Most real workflows exist only in web UIs — dashboards, portals, internal tools with no API. API-only agents are stuck in abstraction. |
| 2 | **End-to-end autonomy requires actuation** | Without browser control, automation stops at "prepare data, alert human, wait." Browser = close loops (submit, book, trade, download). |
| 3 | **Digital citizenship** | Browser capability moves an agent from "LLM with plugins" to a first-class digital actor — it reads what humans read, under the same constraints. |
| 4 | **Governance needs something to govern** | F1-F13 is meaningless if the agent is permanently sandboxed away from the world. Trinity ΔΩΨ (Mind/Heart/Judge) requires a real actuator to deliberate over. |
| 5 | **Physics / information** | An agent without browser is a closed thermodynamic system — it only recycles tokens. Browser is the high-bandwidth channel to the dominant human information environment. |

**Inevitable + dangerous = govern it.** If agents will inevitably gain browser access, the safest path is to treat it as a basic right under a constitutional kernel, not as an ad-hoc hack.

---

## 1. THREE-TIER BROWSER STACK

arifOS governs browser access through three distinct transport layers, each with different privilege, audit, and mutation characteristics.

```
┌─────────────────────────────────────────────────────────────┐
│                    AAA BROWSER ORACLE                        │
│                                                             │
│  Tier 3 ─ browser-harness     RAW REALITY KERNEL            │
│           CDP direct · self-healing · screenshot-first       │
│           MUTATION: helper self-edit · PRIVILEGE: MAXIMUM    │
│                                                             │
│  Tier 2 ─ playwright-cli      AGENTIC BROWSER SHELL         │
│           CLI subprocess · scriptable · raw output           │
│           MUTATION: page-level · PRIVILEGE: HIGH             │
│                                                             │
│  Tier 1 ─ playwright-mcp      GOVERNED BROWSER SERVICE      │
│           MCP tools · structured · audit-per-call            │
│           MUTATION: tool-gated · PRIVILEGE: STANDARD         │
│                                                             │
│  All tiers → ΔΩΨ gating → APEX verdict → VAULT999 audit      │
└─────────────────────────────────────────────────────────────┘
```

### Tier 1 — Governed Browser Service (playwright-mcp)

- **Transport:** MCP stdio/SSE — `@playwright/mcp@0.0.76`
- **Posture:** Structured, typed, frameworked. Each action is a discrete tool call.
- **Interaction:** `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_take_screenshot`
- **Mutation model:** Your code changes outside runtime. Tools are fixed at server start.
- **Safety:** Easiest to wrap and constrain. Every tool call is individually auditable.
- **Best for:** Primary federation agents (333-AGI, 555-ASI), domain organs (WEALTH, GEOX, WELL)

### Tier 2 — Agentic Browser Shell (playwright-cli)

- **Transport:** Bash subprocess — `/root/.npm-global/bin/playwright-cli`
- **Posture:** Flexible, scriptable. Raw browser control via CLI.
- **Interaction:** `playwright-cli snapshot`, `playwright-cli click`, `playwright-cli type`
- **Mutation model:** Page-level state changes. No self-modification.
- **Safety:** Moderate. CLI calls are logged but not individually gated unless wrapped.
- **Best for:** CODING agents (claude-code, opencode, codex, kimi-code, aider)

### Tier 3 — Raw Reality Kernel (browser-harness)

- **Transport:** CDP WebSocket → real Chrome — `browser-harness` heredoc
- **Posture:** Thin, raw, minimally abstracted. ~1k lines across 4 core files.
- **Interaction:** Screenshots, coordinate clicks, `page_info()`, CDP primitives, JavaScript injection
- **Mutation model:** Agent may add missing helpers mid-task. `agent_helpers.py` is editable by the agent.
- **Safety:** MAXIMUM FREEDOM, MAXIMUM DANGER. Self-healing = capability evolution at runtime.
- **Best for:** A-FORGE runtime (privileged), Arif's direct control (sovereign override)

### The Analogy

> If Playwright-MCP is a safe industrial robot arm, and Playwright-CLI is a power tool, browser-harness is a hand with nerves. More dexterity, more danger.

---

## 2. AGENT MODE ASSIGNMENTS

Every agent in the AAA registry gets exactly ONE default browser tier. Upgrades require 888_HOLD.

### PRIMARY FEDERATION AGENTS

| Agent | Tier | Mode | Rationale |
|-------|------|------|-----------|
| **333-AGI** (Δ/MIND) | Tier 1 | `playwright-mcp` (read-write) | Reasoning agent needs governed browser for evidence gathering. MCP tool calls are individually auditable. Can navigate, snapshot, click, type. |
| **555-ASI** (Ω/HEART) | Tier 1 | `playwright-mcp` (read-only subset) | Critique agent needs to verify web claims. `browser_snapshot` + `browser_take_screenshot` only. No mutation. Validates what 333 found. |
| **888-APEX** (ΦΙ/JUDGE) | NONE | No direct browser | Judges, doesn't browse. Receives browser evidence from 333/555. Can request browser verification via 333-AGI delegation. |

### SUPPORT CONTROL PLANE

| Agent | Tier | Mode | Rationale |
|-------|------|------|-----------|
| **A-AUDIT** | Tier 1 | `playwright-mcp` (audit replay) | Can replay browser sessions from VAULT999 logs. Verifies what was done matches what was claimed. No fresh browsing. |
| **A-ARCHIVE** | NONE | No browser | Seals records. Browser access would violate single-responsibility. |

### CODING AGENTS (Ψ/BODY)

| Agent | Tier | Mode | Rationale |
|-------|------|------|-----------|
| **claude-code** | Tier 2 | `playwright-cli` (full) | Primary coding agent. Needs raw browser for testing, scraping, automation. Bash-wrapped with governance sidecar. |
| **opencode** | Tier 2 | `playwright-cli` (full) | Secondary coding agent. Same capability, independent verification path. |
| **codex** | Tier 2 | `playwright-cli` (full) | OpenAI Codex CLI. Browser for testing web apps. |
| **kimi-code** | Tier 2 | `playwright-cli` (full) | Moonshot Kimi. Browser for web automation tasks. |
| **aider** | Tier 2 | `playwright-cli` (full) | AI pair programming. Browser for testing rendered output. |
| **copilot** | Tier 2 | `playwright-cli` (full) | GitHub Copilot. Browser for web development workflows. |
| **continue-cli** | Tier 2 | `playwright-cli` (full) | Continue.dev CLI. Browser for UI testing. |
| **antigravity** | Tier 2 | `playwright-cli` (full) | General coding agent. Browser for any web task. |

### RUNTIME AGENTS

| Agent | Tier | Mode | Rationale |
|-------|------|------|-----------|
| **hermes-asi** | Tier 1+3 | `playwright-mcp` (default) + `browser-harness` (escalated) | Primary human interface. Tier 1 for routine browser tasks. Tier 3 when Arif explicitly authorizes raw CDP control. |
| **openclaw** | Tier 1+2 | `playwright-mcp` (default) + `playwright-cli` (coding) | Multi-agent gateway. Tier 1 for governed agent dispatch. Tier 2 for coding subagents it hosts. |

### DOMAIN ORGANS

| Organ | Tier | Mode | Rationale |
|-------|------|------|-----------|
| **GEOX** | Tier 1 | `playwright-mcp` (read-write) | Geological portal scraping, seismic data access, regulatory site automation. Python bridge for complex flows. |
| **WEALTH** | Tier 1+2 | `playwright-mcp` (governed) + `playwright-cli` (scan) | MCP for governed financial data access. CLI for quick market scans. F8 law checks before any trading site. |
| **WELL** | Tier 1 | `playwright-mcp` (read-only) | Health dashboard monitoring only. No mutation. No form submission. |

### SOVEREIGN

| Entity | Tier | Mode | Rationale |
|--------|------|------|-----------|
| **000-SALAM (Arif)** | ALL | Any tier, any mode | F13 absolute. Arif can use browser-harness directly, bypass any gate, issue raw CDP commands. The sovereign's browser is his own. |

---

## 3. F1-F13 BROWSER ENFORCEMENT

Every browser action, regardless of tier, passes through constitutional checks.

| Floor | Browser-Specific Rule |
|-------|----------------------|
| **F1 AMANAH** | Browser actions are reversible by default. Form submission, file upload, payment → 888_HOLD. |
| **F2 TRUTH** | Page content claims must cite snapshot evidence. "I saw X on the page" requires screenshot or YAML snapshot. |
| **F3 TRI-WITNESS** | High-stakes browser actions (financial, legal, medical) require Δ+Ω+Ψ consensus before click. |
| **F4 CLARITY** | Browser output must reduce entropy. "Page loaded" is noise. "Found 3 buy buttons, clicked the primary CTA" is signal. |
| **F5 PEACE²** | No browser-based harm, harassment, or extortion. No automating attacks. |
| **F6 EMPATHY** | Protect weakest stakeholder. No scraping personal data. No browser-based surveillance. |
| **F7 HUMILITY** | Confidence on visual interpretation capped at 0.90. "The button appears to be blue" not "The button IS blue." |
| **F8 GENIUS** | URL safety check before navigation. Block: banking auth pages, national ID portals, weapons marketplaces. |
| **F9 ANTIHANTU** | No browser-based deception. No fake user-agent to bypass paywalls. No impersonation. |
| **F10 ONTOLOGY** | The agent sees pixels, not meaning. "Red banner at top" not "Angry warning message." |
| **F11 AUDITABILITY** | Every navigation, click, type, screenshot logged with timestamp + URL + action + result. |
| **F12 RESILIENCE** | No JavaScript injection from untrusted pages. XSS/CSRF defense. CAPTCHA = boundary, not puzzle. |
| **F13 SOVEREIGN** | Arif can veto any browser action. Arif can use any tier directly. Arif's browser session is private unless he opts into audit. |

---

## 4. CAPTCHA POLICY

**CAPTCHAs are governance boundaries, not technical obstacles.**

- **Detection:** Agent detects CAPTCHA via snapshot analysis.
- **Response:** Immediate HOLD. No autonomous solving, no CAPTCHA farm API, no OCR attempt.
- **Escalation:** Agent notifies Arif with screenshot + URL. Arif decides: solve manually, abandon, or authorize bypass.
- **Audit:** Every CAPTCHA encounter logged with timestamp, URL, and resolution path.
- **Rationale:** CAPTCHAs are designed to distinguish human from machine. arifOS respects this distinction. Arif is human. Arif solves. Machine waits.

---

## 5. HELPER MUTATION GOVERNANCE (browser-harness)

browser-harness's self-healing capability — the agent editing `agent_helpers.py` mid-task — is the most powerful and most dangerous feature. This section governs it.

### Default: READ-ONLY

Agents may USE existing helpers. They may NOT create or modify helpers without authorization.

### Proposed Self-Heal Flow

```
Agent detects missing helper
  → Agent writes proposed helper code
  → Agent diffs the change
  → APEX reviews: is this safe? justified? minimal?
  → APEX issues: SEAL (apply) | SABAR (hold for human) | VOID (reject)
  → If SEAL: helper applied, logged to VAULT999 with full diff
  → If SABAR: Arif notified, helper held pending review
  → If VOID: helper rejected, agent must find alternative approach
```

### What Requires 888_HOLD

- Any helper that submits forms, uploads files, or sends data
- Any helper that modifies browser security settings
- Any helper that accesses cookies, local storage, or session data
- Any helper that injects JavaScript into third-party pages
- Any helper that bypasses authentication or authorization

### What Can Be AUTO-SEALED

- Scroll helpers, wait helpers, selector helpers
- Screenshot/capture helpers
- Page info / structure parsing helpers
- Navigation helpers (new tab, go back, refresh)

---

## 6. TRANSPORT ARCHITECTURE

### playwright-mcp (Tier 1)

```bash
# Launcher: /root/.claude/mcp-launchers/playwright-mcp.sh
# Transport: stdio
# Package: @playwright/mcp@0.0.76
# Headless: chromium (default), can switch to headed for audit

exec npx -y @playwright/mcp --headless
```

### playwright-cli (Tier 2)

```bash
# Path: /root/.npm-global/bin/playwright-cli
# Usage via Bash tool in AAA/Claude Code
# Governance: wrapped by arifOS bash governance sidecar
```

### browser-harness (Tier 3)

```bash
# Path: /root/browser-harness
# Installed via: pip install -e /root/browser-harness
# Connects to: Chrome with --remote-debugging-port=9222
# Governance: 888_HOLD required for every invocation
# CDP endpoint policy: localhost only, never exposed to network
```

---

## 7. INSTALLATION STATUS

| Component | Status | Version | Path |
|-----------|--------|---------|------|
| playwright (core) | ✅ INSTALLED | 1.61.0 | `/usr/local/bin/playwright` |
| playwright-cli | ✅ INSTALLED | — | `/root/.npm-global/bin/playwright-cli` |
| @playwright/mcp | ✅ INSTALLED | 0.0.76 | `/root/.npm-global/lib/node_modules/@playwright/mcp` |
| playwright (Python) | ✅ INSTALLED | 1.60.0 | pip |
| browser-harness | ✅ CLONED | — | `/root/browser-harness` |

---

## 8. AGENT RIGHTS SUMMARY

```
000-SALAM (Arif)         ALL TIERS · SOVEREIGN · NO GATES
    │
333-AGI (Δ/MIND)         Tier 1 · playwright-mcp · read-write
555-ASI (Ω/HEART)        Tier 1 · playwright-mcp · read-only
888-APEX (ΦΙ/JUDGE)      NONE · judges browser evidence only
    │
A-AUDIT                  Tier 1 · playwright-mcp · audit replay only
A-ARCHIVE                NONE
    │
hermes-asi               Tier 1 (default) + Tier 3 (escalated)
openclaw                 Tier 1 (default) + Tier 2 (coding subagents)
    │
ALL CODING AGENTS        Tier 2 · playwright-cli · full
    │
GEOX                     Tier 1 · playwright-mcp · read-write
WEALTH                   Tier 1+2 · MCP governed + CLI scan
WELL                     Tier 1 · playwright-mcp · read-only
```

---

## 9. WHY BROWSER INTERNET IS A BASIC AGENT RIGHT

*Synthesis of the sovereign's thesis, ratified here as constitutional doctrine.*

**1. REALITY.** Most digital work lives in web UIs, not APIs. An agent that cannot operate a browser cannot close loops in real workflows. It stays "advisor," never "operator."

**2. AUTONOMY.** End-to-end autonomy = perception (page state) + reasoning + action (click/type/submit). Browser is the default actuator when "the world" is the web.

**3. CITIZENSHIP.** Browser capability moves an agent from "language model with plugins" to a first-class digital actor — it reads what humans read, under the same constraints (CAPTCHAs, MFA, throttling), and can be held responsible via audit.

**4. GOVERNANCE.** F1-F13 is meaningless if the agent is permanently sandboxed. Trinity ΔΩΨ requires a real actuator to deliberate over. The browser is where governance meets reality.

**5. PHYSICS.** An agent without browser is a closed thermodynamic system — it only recycles tokens. Browser access is a high-bandwidth channel to the dominant human information environment, enabling actual entropy reduction (ΔS ≤ 0) in the human's world.

**THEREFORE:** Browser access under constitutional control is a basic agent right in arifOS. It is the minimum I/O capability for digital operation. The three-tier stack (MCP → CLI → CDP) provides graduated power with graduated governance. No agent is denied browser access entirely except 888-APEX (who judges) and A-ARCHIVE (who seals) — and even they may request browser evidence through delegation.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
*999 SEAL ALIVE*
