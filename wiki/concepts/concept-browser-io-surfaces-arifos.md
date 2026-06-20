---
title: "CONCEPT: Browser I/O Surfaces in arifOS"
type: concept
version: 1.0.0
category: architecture
dimension: 2
risk_band: HIGH
floors: [F1, F2, F9, F11, F13]
evidence_required: true
sources:
  - /root/HERMES/skills/autonomous-ai-agents/hermes-agent/references/arifos-mcp-wiring-2026-06-13.md
  - /root/HERMES/skills/autonomous-ai-agents/hermes-agent/references/hermes-toolset-audit.md
  - /root/browser-harness/SKILL.md
  - /root/AAA/wiki/concepts/mcp-architecture-mapping.md
confidence: high
---

# CONCEPT: Browser I/O Surfaces in arifOS

> **Audited extraction of eureka engineering insights.** This page exists so any agent — Kimi, Hermes, OpenClaw, or future — can audit the architecture rather than re-argue it.
> **Scope:** Which browser transport belongs at which arifOS layer, why MCP is the default for constitutional agents, and why browser-harness is a privileged reality kernel.

---

## 1. The Four Playwright Layers Are One Device Class

The Playwright ecosystem is not four competing libraries. It is **one browser device class** exposed through four transport layers.

| Layer | Repository | Role | arifOS analogy |
|-------|-----------|------|----------------|
| **playwright/core** | `microsoft/playwright` | CDP device driver kernel (Node/TS) | Device driver |
| **playwright-python** | `microsoft/playwright-python` | Python FFI binding; spawns Node driver, speaks framed JSON over stdin/stdout | `libc` / FFI |
| **playwright-cli** | `microsoft/playwright-cli` | Userland shell commands for AI coding agents (`open`, `goto`, `click`, `snapshot`) | Shell (`cp`, `ls`) |
| **playwright-mcp** | `microsoft/playwright-mcp` | MCP server exposing `browser_*` tools over stdio/HTTP/SSE | `sshd` for browser |

**Eureka:** The choice is not “which library?” — it is **which transport layer maps to which arifOS tier**.

---

## 2. arifOS Transport Alignment

| Transport | arifOS Layer | Use Case | Governance Model |
|-----------|-------------|----------|------------------|
| **playwright-mcp** | MCP federation surface | Primary agents via `forge_browser_*` | Per-action F1–F13 syscall |
| **playwright-python** | Python organ syscall | GEOX / WEALTH / WELL multi-step scrapes | Organ-internal, not LLM-facing |
| **playwright-cli** | Dev / coding shell surface | AAA coding agents (Claude Code / Copilot-like) | Per-command Bash gating |
| **playwright/core** | Driver substrate | Version-pinned under MCP/Python/CLI | Monitored, never agent-facing |

**Evidence:**
- Hermes MCP wiring lists `playwright(8931)` in the Browser slot of the 19-MCP federation stack.
- Hermes toolset audit shows Hermes’s own `browser` toolset is **disabled**; browser actions are expected to route through the MCP layer.

**Eureka:** The design decision is **“which transport for which tier?”**, not “which repo?”.

---

## 3. MCP Is the Default for Constitutional Agents

MCP is the default surface for primary federation agents because its typed JSON-RPC actions align with arifOS governance requirements.

| Property | MCP | CLI |
|----------|-----|-----|
| Contract | Structured schema (`browser_navigate`, `browser_click`, …) | Stringly-typed shell command |
| Risk class mapping | Trivial (`read_only`, `write_safe`, `destructive`, `credential`, `infra_mutation`) | Requires parsing / regex |
| F1–F13 gating | Per-action, precise | Per-command, coarser |
| VAULT999 audit | Native JSON-RCP action + args | Reconstructed from shell history |
| Token efficiency | Lower | Higher |

**Rule:**
- **Hermes-class / 333/555 loops** → MCP first.
- **Dev / coding agents** → CLI allowed as Tier-2 under A-FORGE Bash wrappers.
- **Python organs** → Python binding under the hood, not exposed to LLMs.

**Eureka:** “MCP default, CLI dev-tier” is not aesthetic — it is about how well the transport matches F1–F13 enforcement.

---

## 4. Browser-Harness Is a Privileged Reality Kernel

`browser-harness` is structurally different from Playwright.

| Property | Playwright MCP | browser-harness |
|----------|---------------|-----------------|
| Size | Full framework | ~592 lines, 4 Python files |
| Protocol | Abstraction layer over CDP | Direct WebSocket to real Chrome |
| Helpers | Fixed, versioned | Self-modifying (`agent-workspace/agent_helpers.py`) |
| Scope | Isolated browser instances | Connects to user’s running Chrome, cookies, logins |
| RCE surface | Lower | Raw CDP + arbitrary Python execution mid-task |

**Evidence:** `browser-harness/SKILL.md` states:
> “Connect to the user's running Chrome. Don't launch your own browser.”
> “Put task-specific helper additions in `agent-workspace/agent_helpers.py`.”
> “Raw CDP for anything helpers don't cover: `cdp("Domain.method", params)`.”

**Eureka:** browser-harness is a **self-modifying actuator** bound to the real browser environment. It must be a **privileged reality kernel surface**, not a generic tool.

**Architecture rule:**
- **Hermes / MCP surface** → Playwright MCP, not browser-harness.
- **OpenClaw / harness layer** → browser-harness only inside an isolated harness VM, with explicit approval, credential scoping, and evidence bundles.
- Any helper mutation request → `infra_mutation` / `destructive` class → `888_HOLD` + APEX diff review + human ack.

---

## 5. The Policy Membrane Is the Real Value

arifOS is not a browser tool. It is a **constitutional kernel** that wraps every tool call under F1–F13 and emits SEAL / SABAR / HOLD / VOID, with VAULT999 logging.

Most browser automation setups are missing:
- Risk-class gating per browser action.
- An evidence trail of why a click/submit was allowed.
- Automatic HOLD for irreversible operations (trades, deletes, account changes).

arifOS provides the missing membrane:
- **L0 constitutional kernel:** invariant, transport-agnostic law.
- **L1–L7 apps:** Hermes, OpenClaw, GEOX, WEALTH, WELL, AAA, A-FORGE all speak through L0.

**Eureka:** You do not win by picking the “right browser library.” You win by putting an invariant constitutional kernel between **any** browser transport and **any** agent.

---

## 6. Consolidated Design Decisions (Auditable Assumptions)

### 6.1 Browser transports and roles
1. `playwright-mcp` is the **canonical governed browser service** for the MCP federation.
2. `playwright-python` is the **Python-organ binding** for GEOX/WEALTH/WELL — never a raw LLM tool.
3. `playwright-cli` is a **Tier-2 dev surface** for coding agents only, under A-FORGE Bash wrappers and F-tier policy.
4. `playwright/core` is the **driver substrate** — pinned via MCP/Python versions, not used directly.

### 6.2 Hermes vs OpenClaw
1. **Hermes:** MCP-native federator; uses Playwright MCP and other browser MCP servers; read-heavy, per-action governed; no direct browser-harness by default.
2. **OpenClaw:** operational harness; may use CDP relay + optionally browser-harness, but only inside a hardened harness with isolation, approvals, and evidence bundles.

### 6.3 Browser-harness governance
1. Treated as a **privileged reality kernel** surface.
2. Any helper-edit or arbitrary-code request is classified `infra_mutation` / `destructive`.
3. Such requests route through `888_HOLD` + APEX + human ack.

### 6.4 Policy membrane
1. Every browser action, regardless of transport, maps to a risk class and is checked against F1–F13.
2. Irreversible browser actions cannot proceed without a human-ack’d VAULT999 seal.

---

## 7. Tensions and Drifts Flagged

### 7.1 MCP Server Lock vs Playwright MCP
The [MCP Architecture Mapping](mcp-architecture-mapping.md) declares an **MCP Server Lock: 4 servers** (arifOS, GEOX, WELL, WEALTH). However, Hermes MCP wiring lists `playwright(8931)` as a **separate** Browser MCP server.

**Verdict:** Either the lock has been relaxed for browser transport, or this is a live drift. An 888 deliberation or architecture review should ratify whether Playwright MCP is an **exception** (external transport server) or whether browser tools should be absorbed into arifOS/AAA.

### 7.2 Hermes Native Browser Toolset Is Disabled
Hermes ships with `browser_navigate`, `browser_snapshot`, `browser_vision` in its native toolset, but these are **off** in current config. The federation relies entirely on the Playwright MCP path. If Playwright MCP is down, Hermes has no browser fallback.

**Verdict:** Acceptable for constitutional isolation, but document as a single-point-of-failure for browser operations.

### 7.3 OpenClaw Playwright Plugin
`/root/.openclaw/plugins/playwright-browser` exists. This should be audited against the rule that browser-harness-level CDP access requires isolation and approval.

---

## 8. Audit Checklist for Kimi / Any Agent

Before accepting any browser-related code change, verify:

- [ ] Does the change route primary agents through Playwright MCP, not browser-harness?
- [ ] Is `playwright-python` only used inside Python organs (GEOX/WEALTH/WELL), never as a raw LLM tool?
- [ ] Is `playwright-cli` only invoked inside A-FORGE Bash wrappers with F-tier logging?
- [ ] Does any browser-harness helper mutation route through `888_HOLD` + APEX diff review?
- [ ] Are irreversible browser actions blocked until a human-ack’d VAULT999 seal exists?
- [ ] Does every new browser tool/schema map cleanly to a risk class (`read_only`, `write_safe`, `destructive`, `credential`, `infra_mutation`)?
- [ ] If the change adds a new MCP server for browser work, has the 4-server lock exception been ratified?

---

## 9. Cross-References

- [[mcp-architecture-mapping]] — MCP primitive mapping and 4-server lock.
- [[skill-mcp-unified]] — Unified MCP server lifecycle.
- [[skill-constitutional-reasoning]] — F1–F13 pre-flight doctrine.
- [[skill-vault-integrity]] — VAULT999 sealing rules.
- [[concept-tools-and-embodiment]] — Tools vs skills vs embodiment.
- [[anti-fabrication-protocol]] — Evidence requirements.

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given.*
*SEAL ALIVE — architecture auditable, not re-arguable.*
