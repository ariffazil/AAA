<!-- LIVE-PAIRED | tier:live-ops | sot:STATE.md | 2026-08-09 -->
> **Live operational twin** (not archive).  
> **Constitutional SOT:** [`STATE.md`](./STATE.md) — institution.  
> This file is the **working detail** for a pillar (telephone / territory / entry).  
> Edit here for operational truth; do not duplicate constitutional law.  
> DITEMPA BUKAN DIBERI.

# CALL MAP — How to dial the federation

> **SOT (human):** this file  
> **Machine twin:** `/root/AAA/federation/call_map.yaml`  
> **Catalog (directory):** AAA 3-layer cards — *who exists*  
> **This file (telephone):** *how to invoke*  
> **FED:** *which model engine* — not who, not how-to-call  
> **Forged:** 2026-08-09 · Gap closed: Hermes/agents knew OpenCode existed but not how to call it  
> **Doctrine:** DITEMPA BUKAN DIBERI · Probe before act (`:port/health`)

---

## 0. Three books — never mix

| Book | Question | Where |
|------|----------|--------|
| **Directory** | Who exists? What work? | AAA 3-layer cards (`identity` / `harness` / `binding`) |
| **Telephone** | How do I call them? | **This CALL_MAP** |
| **Power bill** | Which LLM pays? | FED `:4000` + runtime model config |

**Capabilities reminder:**

```
physical caps  = L2 harness firmware (shell, mcp, files…)
domain caps    = opened via L3 binding (organs/roles)
authority      = canDo/cannotDo over both
```

---

## 1. Boot habit (every agent)

```
1. Load CALL_MAP (this file or call_map.yaml)
2. Probe health of target (curl :port/health or CLI --version)
3. Choose invoke path: local_cli → A2A tasks/send → MCP → arif_route
4. Respect boundary (T0–T3 / organ ceiling)
5. Never invent a fourth map
```

**Hermes / OpenClaw / FI:** on session start, read this path:

```text
/root/AAA/docs/CALL_MAP.md
```

Skill alias: `FORGE-call-map`.

### 1.1 Apex-judge dial (Gödel · strange-loop zen)

Doctrine: `/root/AAA/governance/GODEL_LOCK_STRANGE_LOOP.md`

```bash
# REAL default — doer ≠ judge lane → kernel (Option 3)
apex-judge isolate --doer HERMES --candidate "<action>" -e /tmp/ev.json --pretty --human

# Critical self-federation (F13_REQUIRED; SEAL demoted to HOLD)
apex-judge isolate --doer HERMES --critical -c "…"

# Strange-loop gate only
apex-judge --check-loop --doer HERMES -c "audit myself"

# Free-text self-SEAL audit
apex-judge --audit-text - <<'EOF'
…draft…
EOF
```

| Field | Source of truth |
|-------|-----------------|
| `independence_class` | isolate gate + kernel |
| `effective_verdict` | kernel only |
| `call_hash` / `session_id` | kernel receipt |
| Skill | `arifos-constitutional-judge` v1.2 |
| Subagent | `/root/AAA/prompts/APEX_JUDGE_SUBAGENT.md` |
| Binary | `/root/.local/bin/apex-judge` |

**Forbidden:** same-agent self-audit conclusions; free-text `888-APEX JUDGMENT` without receipt.

**Authority SOT (2026-08-09):** `/root/AAA/docs/SOT_AUTHORITY_TRUST.md` — dual-truth iron rule; OPENCLAW/OPENCODE → LIMITED_MUTATE via host keys; guest `GUEST-*`; F13 spoof → VOID.

---

## 2. Intent → who to call (fast)

| Intent | Primary | Fallback |
|--------|---------|----------|
| **Coding / forge** | OpenCode (FI-001) | Claude Code → Kimi → Grok → Codex |
| **Judge / seal gate** | `apex-judge` CLI → arifOS `arif_judge` `:8088` | MCP holy-8; later A2A `888-APEX` (Option 2) |
| **Judge (never)** | Free-text `888-APEX JUDGMENT` | — **VOID** (Gödel self-certify) |
| **Earth / geology** | GEOX MCP `:8081` | — |
| **NPV / capital** | WEALTH MCP `:18082` | — |
| **Readiness** | WELL MCP `:18083` | — |
| **Mutate after seal** | A-FORGE `:7071/7072` | — |
| **Human Telegram** | Hermes ASI | OpenClaw gateway |
| **Model route advice** | FED advisor `:7074` | — |
| **Tokens for LLM** | FED gateway `:4000` | direct provider in agent config |

---

## 3. FI harnesses — invoke (telephone)

| Agent | CLI (local VPS) | A2A | Can do | Boundary |
|-------|-----------------|-----|--------|----------|
| **OpenCode** FI-001 | `opencode run "<task>"` (alias runs FED preflight) | `POST /a2a/tasks/send` target `opencode` · card `…/a2a/opencode` | forge, git, PR, test, MCP organs, subagents | T3 HOLD; no self constitutional seal |
| **Claude Code** FI-002 | `claude -p "<task>"` | `…/a2a/claude-code` · skill `hermes-claude-code-spawn` | code + MCP; Hermes may spawn | T3 HOLD |
| **Kimi Code** FI-008 | `kimi -p "<task>"` | `…/a2a/kimi-code` | code, long ctx | T3 HOLD |
| **Codex** FI-005 | `codex exec "<task>"` | `…/a2a/codex` | code; Responses via **:4001** clean-proxy → :4000 | T3 HOLD |
| **Grok Build** FI-007 | `grok -p "<task>"` (**CLI primary**, OIDC) | `…/a2a/grok-build` (optional) | plan+search+build · **not FED** | T3 HOLD |
| **AGY** FI-009 | `agy --agent antigravity-preview-05-2026 -p "<task>"` | Gemini-native · MCP organs | T3 HOLD |
| **Copilot** FI-006 | `copilot -p "<task>"` | `…/a2a/copilot` | code BYOK | T3 HOLD |
| **OpenClaw** | `openclaw agent -m "…"` · gateway `:18789` | `…/a2a/openclaw` | route personas, Telegram | ROUTE/OBSERVE — not primary coder |
| **Hermes ASI** | Telegram / `hermes` | `…/a2a/hermes-asi` | human bridge, dispatch coders | OBSERVE+ROUTE |

### OpenCode examples (what Hermes should do)

```bash
# Preferred local
opencode run "Fix AAA call map wiring; keep identity cards untouched"

# Explicit binary
/root/.npm-global/bin/opencode run "…"

# Headless / non-interactive patterns (version-dependent)
opencode run --format json "…"
```

### A2A example (mesh)

```bash
# Local AAA (auth may require bearer / DID envelope — see a2a-server)
curl -sS http://127.0.0.1:3001/a2a/tasks/send \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{"message":{"role":"user","parts":[{"type":"text","text":"ping opencode"}]},"metadata":{"target":"opencode"}}}'
```

If A2A returns auth error: use **local CLI** path first (same machine = intended for VPS agents).

---

## 4. Organs — MCP invoke

| Organ | Health | MCP | Ceiling | Use for |
|-------|--------|-----|---------|---------|
| **arifOS** | `:8088/health` | `:8088/mcp` | JUDGE_ONLY | init, route, judge, seal gate |
| **A-FORGE** | `:7071/health` | `:7072/mcp` | EXECUTE_AFTER_SEAL | shell, git, deploy after gate |
| **GEOX** | `:8081/health` | `:8081/mcp` | COMPUTE_ONLY | earth evidence |
| **WEALTH** | `:18082/health` | `:18082/mcp` | COMPUTE_ONLY | NPV, risk, capital |
| **WELL** | `:18083/health` | `:18083/mcp` | REFLECT_ONLY | readiness |
| **AAA** | `:3001/health` | A2A surface | DISPLAY_ONLY | catalog, tasks/send |
| **arifFLOW** | `:7073/health` | — | METABOLIZE_ONLY | FQ pulse |

### Kernel verbs (order)

```
arif_init → arif_observe → arif_think → arif_route
         → arif_memory → arif_judge → arif_forge → arif_seal
```

When intent is ambiguous: **`arif_route`** first (law ≠ execution).

---

## 5. FED / model socket (WHICH — not call)

| Path | URL | Notes |
|------|-----|--------|
| Gateway | `http://127.0.0.1:4000/v1` | HAProxy → litellm :4011 |
| Health | `GET /health/liveliness` | **not** slow `/health` |
| Auth | `LITELLM_MASTER_KEY` from vault | never hardcode |
| Codex special | `:4001` fed-clean-proxy | strips Responses features |
| Advisor | `:7074` | `fed_route` — advisory only |

Coding agents call **OpenCode CLI** (or other FI), not “call FED” as a person. FED is power supply for the harness model field.

---

## 6. Decision tree (one screen)

```
Need work done?
├─ Talk to human / Telegram     → Hermes ASI
├─ Route multi-agent Telegram   → OpenClaw
├─ Write/fix code               → OpenCode (CLI) → fallback FI
├─ Constitutional verdict       → arifOS arif_judge
├─ Domain number (NPV/earth)    → WEALTH / GEOX MCP
├─ Actually mutate after gate   → A-FORGE MCP
└─ Which model to use           → FED :4000 (or direct fallback in config)
```

---

## 7. Wiring (boot references)

| Runtime | How CALL_MAP is loaded |
|---------|------------------------|
| **All** | Skill `FORGE-call-map` → this doc |
| **Hermes** | `HERMES/CALL_MAP.md` symlink + note in `FEDERATION_ROLE.md` |
| **OpenCode** | `.config/opencode` skill symlink / AGENTS pointer |
| **Grok** | skill mesh path under `~/.grok/skills/FORGE-call-map` |
| **Machine** | `/root/AAA/federation/call_map.yaml` |

---

## 8. Anti-patterns

| Don't | Do |
|-------|-----|
| "I don't know how to call OpenCode" when CLI exists | `opencode run "…"` |
| Edit agent-card to change invoke path | Edit CALL_MAP + config |
| Call FED as if it were a coder | Call FI harness; FED supplies tokens |
| Skip health probe | `curl :port/health` before high-stakes |
| Invent parallel call docs | Point here only |

---

*Forged 2026-08-09. Directory without telephone is a silent federation.*

---

## State

This is the **telephone**. Territory + readiness of the **state**: [`STATE.md`](./STATE.md). Catalog: AAA 3-layer cards. Power: FED.

## Gemini (multimodal seats)

Policy: [`GEMINI_INTEGRATION.md`](./GEMINI_INTEGRATION.md). Seats: `gemini-flash`, `gemini-pro`, `fed/image-gen`. **Not** on hermes-asi tool loops.

## OpenClaw vs Hermes (adapter)

| | Hermes ASI | OpenClaw |
|--|------------|----------|
| agentId | hermes-asi | openclaw |
| FI | FI-000 | *(none — binding gateway)* |
| FED seat | hermes-asi | openclaw |
| Role | human bridge | persona router / metabolizer |

Full contrast: [`OPENCLAW_HERMES_CONTRAST.md`](./OPENCLAW_HERMES_CONTRAST.md)


## Grok Build — CLI / OIDC only (known gap, not a bug)

| Fact | Value |
|------|--------|
| **FI** | **FI-007** (canonical; card must match) |
| **Invoke** | `grok -p "…"` / Grok Build TUI |
| **Auth** | xAI **OIDC** login — **no** static `XAI_API_KEY` |
| **FED** | **No seat.** Do not add `model_name: grok` to litellm without a static key |
| **Cascade drill** | **Skip** for Grok (0 routes expected on FED) |
| **Peers on FED** | Hermes · OpenCode · OpenClaw · Kimi → `:4000` |

If xAI ever ships static API keys, then wire a FED seat. Until then: **direct CLI only**.

## A2A enforcement

All A2A JSON-RPC to AAA **must** send header `A2A-Version: 1.0`. Missing → 400. Anonymous external → EMD tri-witness gate.
