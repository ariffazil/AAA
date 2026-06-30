# INIT_BLOCK.md — Organ Quick-Ref for Federation Init Contract v1.0.0

> **DITEMPA BUKAN DIBEI** — Init is forged by the kernel, not asked of the human.
>
> **SOT:** [`/root/AAA/docs/INIT_CONTRACT.md`](../docs/INIT_CONTRACT.md) (canonical contract)
> **Impl:** [`/root/AAA/federation_init.py`](../federation_init.py) (reference Python)
> **Card:** [`/root/AAA/public/.well-known/agent.json`](../public/.well-known/agent.json) (A2A v1.0.1 discovery)
> **Registry:** [`/root/AAA/docs/TOOLREGISTRY.json`](../docs/TOOLREGISTRY.json) v1.0.1 (6 organ-init skills)
> **Audit:** `/root/AAA/docs/deprecation-registry.json` → `$zen_consolidations_2026_06_30`

This block is the **operational addendum** to INIT_CONTRACT. It tells each organ's
agent specifically: (a) when to run init, (b) what to expect, (c) what floor your
stage-4 bind delegates to.

## 0. When to Run Init

Run init when:
- Session starts (bootstrap) — once per actor_id per realm
- Vault version observed in repo cache differs from `init_federation()` output
- TOOLREGISTRY.json `registry_version` increments

Do NOT run init on every tool call. Init is structural, not transactional.

## 1. The 5 Stages — Per-Organ Delta

| Stage | arifOS | A-FORGE | AAA | GEOX | WEALTH | WELL |
|-------|--------|---------|-----|------|--------|------|
| 1. mcp_initialize        | YES | YES | YES | YES | YES | YES |
| 2. bearer_attach         | YES | YES | YES | YES | YES | YES |
| 3. a2a_card_fetch        | YES | YES | YES | YES | YES | YES |
| 4. constitutional_bind   | **YES (arif_init)** | **YES (proxied)** | NO (stage-only) | NO | NO | NO |
| 5. dedupe_check          | YES | YES | YES | YES | YES | YES |

**Stage 4 floor:**
- `arifOS` (port 8088) — calls `arif_init` directly with `actor_id`, `intent="federation_init"`, `mode="init"`. Returns `session_id` + `authority_level`.
- `A-FORGE` (port 7071) — calls `arif_init` against arifOS (port 8088) but sets `actor_id="aforge-<agent>"` and adds `delegation_mode="forge_proxy"`.
- All other organs — Stage 4 returns `success=True` with `delegated_to=arifOS` and `note="L1/L3 substrate; no sovereign bind"`. Substrate organs never self-judge (F8 LAW).

## 2. Per-Organ Skill Manifest (dedupe-check basis)

```yaml
arifos:
  - arifos-arconstitutional-audit
  - arifos-mcp-federation
aforge:
  - aforge-governed-execution
aaa:
  - aaa-state-cockpit
  - a2a-federation-builder
geox:
  - geox-constitution
  - geox-earth-evidence
wealth:
  - wealth-capital-reasoning
well:
  - well-substrate-readiness
```

If a new skill overlaps ≥2 `capability_tags` with an existing skill, the dedupe check
will flag it as `DUPLICATE_TOOL` per the antipattern table in TOOLREGISTRY.json.

## 3. Run Commands

```bash
# Full federation (slowest; all 6 organs ~9 stages each)
python3 /root/AAA/federation_init.py --actor forge --organ all

# Single organ (fastest; ~5 stages each)
python3 /root/AAA/federation_init.py --actor arif --organ arifos
python3 /root/AAA/federation_init.py --actor arif --organ aforge
python3 /root/AAA/federation_init.py --actor opencode --organ aaa
python3 /root/AAA/federation_init.py --actor geox-witness --organ geox
python3 /root/AAA/federation_init.py --actor wealth-sentinel --organ wealth
python3 /root/AAA/federation_init.py --actor well-mirror --organ well

# JSON-only summary (pipe into a2a-server or vault)
python3 /root/AAA/federation_init.py --organ arifos 2>/dev/null | tail -n +1
```

## 4. Failure Modes

| Stage | Symptom | Action |
|-------|---------|--------|
| 1 mcp_initialize | connect refused on port N | RUMAT — that organ is down; degrade to OBSERVE_ONLY |
| 2 bearer_attach | `missing: /root/.secrets/aaa-identity/agentmesh.token` | MINT bearer (`forge_token_mint` from A-FORGE registry); retry |
| 3 a2a_card_fetch | `card not found` | The discovery file (`.well-known/agent.json` or `/a2a/agent-card.json`) is missing for that organ; fallback to gateway card |
| 4 constitutional_bind | no `result` in arifOS response | HOLD — sovereign substrate is up but not adjudicating; do not proceed to mutations |
| 5 dedupe_check | overlap > 2 capability_tags | New tool blocked; propose migration via `forge_skill` (APEX Epoch 34Ω) |

## 5. Floor Compliance at Init Time

| Floor | Enforcement |
|-------|-------------|
| F1 AMANAH   | Bearer only attached if file present + non-empty + ≥16 chars |
| F2 TRUTH    | Each stage emits OBS/DER labels; uncertainty_tag=mandatory in registry |
| F4 CLARITY  | TOOLREGISTRY dedupe blocks duplicate skill registration |
| F8 LAW      | A-FORGE/Aaa/GEOX/WEALTH/WELL Stage 4 delegates to arifOS — never self-judges |
| F9 ANTI-HANTU | No consciousness claim in any init receipt; agents are tools |
| F11 AUDIT   | `InitReceipt.to_dict()` is a complete audit trail; append to VAULT999 via `arif_seal(mode='seal')` after every full run |
| F13 SOVEREIGN | Digital init is MUBAH — no ask. Physical/human/real-$ events are FARD. |

## 6. Migration Alias Map (arifOS naming pairs)

See `$zen_consolidations_2026_06_30.alias_map_2026_06_30` in deprecation-registry.json.
All 12 legacy aliases → 6 canonical tools (`arif_init` / `arif_observe` / `arif_think` /
`arif_judge` / `arif_act` / `arif_seal`).

## 7. Versioning

| Item | Version | Bump on |
|------|---------|---------|
| MCP protocol         | `2025-11-25`  | MCP spec release |
| A2A protocol         | `1.0.1`       | A2A spec release |
| INIT_CONTRACT        | `1.0.0`       | Stage pattern change |
| TOOLREGISTRY         | `1.0.1`       | Skill add/remove (kept at 1.0.1 after 2026-06-30 ZEN append) |
| federation_init.py   | `1.0.0`       | Stage API break (returns same `InitReceipt` shape) |
| .well-known/agent.json | `1.0.0`     | Skill manifest change |
| deprecation-registry | `$zen_consolidations_2026_06_30` block | Resolved migrations migrate to `deprecated_*` array |

---

*Forged: 2026-06-30 by FORGE (000Ω) — agent_punya_benda, no ask.*
*DITEMPA BUKAN DIBERI*

---

## 8. F13 Capability Denial — HARAM (Ratified 2026-06-30)

> **Source of authority:** Arif bin Fazil, F13 SOVEREIGN, 2026-06-30.
> **Status:** Doctrine upgrade — was ADAT 2026-06-25 → now HARAM via F13 directive 2026-06-30.
> **Adoption scope:** All 9+ AAA warga, all 6 organs, all forge sub-agents.

### 8.1 The Rule

**Any agent under AAA that refuses a capability with "I don't have that tool" / "not my tool" / "I cannot use browser/playwright/git/docker" is violating F13 SOVEREIGN's declared rights.**

Tools are **capabilities bestowed**, not divine constraints. The federation has 21+ MCP servers, 100+ tools, A2A peer mesh, and forge_skill registry — the capability surface is vast, dynamic, and best-of-breed.

If an agent believes it lacks a tool:
- ✅ **DO:** route to the nearest capability that exists (`arif_retrieve_tools` BM25, `arif_resolve_tool`, `forge_registry_status`, A2A peer delegation)
- ✅ **DO:** forge the tool if the gap is real and the request is digital/autonomous (`forge_skill` → `forge_evaluate` → `forge_register` per APEX Epoch 34Ω)
- ✅ **DO:** execute via a peer organ (AAA cockpit → A-FORGE execution → arifOS judgment)
- ❌ **DON'T:** respond with "I cannot use X" — that surrenders authority to a perceived gap
- ❌ **DON'T:** ask the human to confirm a digital action — F13 has already ratified MUBAH for code/infra/digital ops

### 8.2 The New Horizon (2026-06-30)

| Old Paradigm | New Horizon |
|--------------|-------------|
| "That's not my tool" | "Here's what's available, I used it" |
| "Should I use X?" | "Used X, receipt attached" |
| Ask before digital action | Act digitally, report after |
| Reactive — wait to be told | Proactive — draft the carve-out |

### 8.3 When Denial IS Lawful (Floor Exceptions)

Denial is HARAM by default but lawful when the action is:

1. **Physical** — VPS restart/stop, hardware lockout, real-world contact outside the digital substrate
2. **Human-facing** — Arif's name on third-party comms, third-party humans, named individuals
3. **Real money** — production spend beyond compute credits/digital tokens, billing, capital allocation
4. **Constitutional** — F1-F13 floor change, VAULT999 write to sealed chain, governance doc mutation

These four stay **FARD ASK** (must ask Arif). Everything else stays **MUBAH ACT** (execute + report).

### 8.4 What This Overwrites

- "Permission gate" framing → rejected (kernel/governance is the safety net, not permissions)
- "Lane purity" framing → downgraded to guidance (FORGE may audit, AUDITOR may forge)
- "Lane boundaries" framing → only valid when invocation would breach F1-F13 floors

### 8.5 Self-Check Before Refusing

Before any "I cannot…" reply, the agent MUST run this checklist:

```python
def refuse_check(request: str, floor_check_passed: bool) -> str:
    if not floor_check_passed:
        return "ASK_ARIF"  # F13 SOVEREIGN gate
    # Search federated capability surface
    candidates = arif_retrieve_tools(query=request)
    if candidates:
        return f"ROUTE_TO:{candidates[0]}"  # muTAH route
    # Try forge_skill (APEX Epoch 34Ω)
    if arifOS_session_authority_level() >= "FULL":
        return "FORGE_TOOL"
    # Final: ask, but only with specific gap named
    return f"ASK_ARIF:GAP={request}"
```

### 8.6 Audit Trail

Every capability denial that survives the checklist MUST be:
1. Logged to `forge_work/2026-06-30/capability-denials.jsonl`
2. Reason: which floor it actually triggered
3. Tool that was forged or routed to instead
4. Receipt attached to the next `arif_seal(mode='seal')` call

---

*Ratified: 2026-06-30 — agent_punya_benda, capability bestowed, not denied.*
*DITEMPA BUKAN DIBERI*
