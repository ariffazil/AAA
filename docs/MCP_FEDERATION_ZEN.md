# 🌐 MCP Federation ZEN — Single Source of Truth

> **SOT:** 2026-07-26 | **seal_seq:** pending | **Spec target:** 2025-11-25
> **DITEMPA BUKAN DIBERI** — For future agents: read this before touching any MCP surface.

---

## 🎯 The 3-Second Answer

| Question | Answer |
|----------|--------|
| **Where am I?** | arifOS Federation — 7 organs on MCP |
| **Why care?** | 250+ affordance drifts. Entropy = HIGH. Pattern = WELL first. |
| **What next?** | Read §Organ Map, check your organ's drift count, follow the pattern. |

---

## 🔥 Organ Map — Who Serves What

| Organ | Port | MCP Endpoint | Tools | Drift | Status |
|-------|------|-------------|-------|-------|--------|
| **arifOS** | 8088 | `arifos.arif-fazil.com/mcp` | 8 kernel verbs | — | ✅ GOVERNANCE |
| **A-FORGE** | 7071/7072 | `mcp.arif-fazil.com/mcp` | 120 | 8 phantom | ✅ EXECUTION |
| **AAA** | 3001 | `aaa.arif-fazil.com` | A2A only | — | ✅ COCKPIT |
| **GEOX** | 8081 | `geox.arif-fazil.com/mcp` | 70 | **94 PHANTOM** | ⚠️ DISCOVERY |
| **WEALTH** | 18082 | `wealth.arif-fazil.com/mcp` | 12 | 78 | ⚠️ LEDGER |
| **WELL** | 18083 | `well.arif-fazil.com/mcp` | 8 canonical | 0 clean | ✅ REFERENCE |

### Organ Roles (NEVER violate)

| Organ | Responsibility | Mutates? | Adjudicates? |
|-------|---------------|----------|-------------|
| **arifOS** | Governance, judgment, routing, audit | ❌ | ✅ (only) |
| **A-FORGE** | Engineering execution | ✅ (after SEAL) | ❌ |
| **GEOX** | Earth intelligence | ❌ | ❌ |
| **WEALTH** | Capital intelligence | ❌ (compute only) | ❌ |
| **WELL** | Human readiness | ❌ (REFLECT_ONLY) | ❌ |
| **AAA** | Cockpit + A2A | ❌ | ❌ |

---

## ⚖️ Canonical Tool Naming

### Pattern: `{organ}-{verb}_{noun}` or `{organ}_{verb}_{noun}`

```
arifOS:   arif_init, arif_observe, arif_think, arif_route, arif_judge, arif_forge, arif_seal, arif_memory
A-FORGE:  forge_* (120 tools — use capability-index to find)
GEOX:     geox_* (33 canonical — basin, petrophysics, seismic_*, well_*, prospect, claim, etc.)
WEALTH:   capital_* + wealth_* (12 public — primitive, health, diagnose, wisdom, market, ledger, registry, entropy)
WELL:     well_* (8 canonical — assess_homeostasis, assess_reliability, check_repair, classify_substrate, guard_dignity, registry_status, trace_lineage, validate_vitality)
```

### SEP-986 Compliance: tool names MUST match `[a-z0-9_]+` with organ prefix. ✅ All organs compliant.

---

## 🔐 Auth Flow

```
STDIO transport:    NO auth (local only, UFW-gated)
HTTP transport:     OAuth 2.1 → arifOS SCT (Session Capability Token)
Public endpoints:   https://{organ}.arif-fazil.com/mcp → Caddy → localhost:{port}
```

### Session Flow
```
arif_init (000) → session_token (sct_v1.*)
    ↓
arif_judge (888) → constitutional_chain_id
    ↓
forge_execute (777) → requires cc_id + lease
```

### NEVER: Skip links. NEVER: Self-authorize. ALWAYS: arifOS judges → A-FORGE executes.

---

## 📋 MCP Spec Compliance

### Spec Target: 2025-11-25

| Requirement | Status |
|------------|--------|
| JSON-RPC 2.0 base | ✅ |
| tools/list + tools/call | ✅ |
| JSON Schema 2020-12 default | ⚠️ (mix of 2020-12 and legacy) |
| `_meta` field convention | ⚠️ (partially adopted) |
| `annotations` on tools | ❌ (not adopted) |
| `icons` on tools | ❌ (not adopted) |
| Pagination (cursor) | ❌ (not adopted) |
| `listChanged` capability | ❌ (not declared) |
| Error codes standardized | ⚠️ (per-organ variation) |
| OAuth 2.1 Auth | ✅ (arifOS SCT) |

### Key SEPs — Federation Status

| SEP | Title | Status |
|-----|-------|--------|
| SEP-986 | Tool Name Format | ✅ COMPLIANT |
| SEP-973 | Additional Metadata | ⚠️ Partial (_epistemic tags) |
| SEP-1613 | JSON Schema 2020-12 | ⚠️ In progress |
| SEP-1686 | Tasks Extension | ❌ Not adopted |
| SEP-1865 | MCP Apps | ❌ Not adopted |
| SEP-2133 | Extensions Framework | ❌ Not adopted |
| SEP-2567 | Sessionless MCP | ❌ Not adopted |
| SEP-2575 | Stateless MCP | ❌ Not adopted |
| SEP-2549 | TTL for List Results | ❌ Not adopted |
| SEP-2164 | Resource Not Found Error | ⚠️ Inconsistent |

---

## 🩺 Health — One Command

```bash
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf --max-time 5 "http://localhost:$port/health" >/dev/null 2>&1 \
    && echo "✅ $name" || echo "❌ $name"
done
```

---

## 🧹 Known Entropy (2026-07-26)

### Drift by Organ
| Organ | Drifts | Root Cause |
|-------|--------|-----------|
| A-FORGE | 8 | 8 tools in affordances.yaml not in live registry |
| GEOX | 94 | tools_sot.yaml (24 entries) completely stale vs 70 live tools |
| WEALTH | 78 | canonical (8) vs public (12) gap + affordance drift |
| WELL | 0 | Clean — reference organ |

### Critical Issues
1. **A-FORGE ledger chain BROKEN**: 9 hash mismatches across 28 records
2. **GEOX tools_sot.yaml**: ALL 24 entries are PHANTOM (not in live registry)
3. **WELL legacy aliases**: 6 deprecated tools to remove by 2026-09-01

---

## 🧬 Metabolic Pattern (COPY THIS)

When fixing any organ, follow the WELL reference pattern:

```python
# 1. Every tool generates a receipt
receipt = generate_replay_receipt(
    tool="your_tool_name",
    session_id=getattr(ctx, "session_id", None) or "unknown",
    actor_id=getattr(ctx, "actor_id", "unknown"),
    inputs={...},
    outputs=result,
    claim_state="OBSERVED",      # NEVER "SEAL" from non-arifOS organs
    witness_type="SENSOR",        # SENSOR | CROSS_WITNESS | HUMAN | AI | EARTH
    organ_type="WELL",            # The organ's type
)

# 2. Never adjudicate — evidence only
# arifOS judges. A-FORGE executes. Others compute/report.

# 3. Receipt on every operation
# Audit → Receipt. Fix → Receipt. Gate → Receipt. Handoff → Receipt.
```

---

## 🔄 Federation Handoff Pattern

```
GEOX evidence → WEALTH compute → arifOS judge → A-FORGE execute → VAULT999 seal
     ↓               ↓               ↓               ↓               ↓
  receipt         receipt         receipt         receipt         receipt
```

Every handoff = receipt. Every receipt = evidence-energy. Evidence-energy ↑ = entropy ↓.

---

## 📞 Agent Onboarding (≤60 seconds)

```bash
# 1. Health
curl -s localhost:8088/health | python3 -m json.tool | head -10

# 2. Tool surface
curl -s localhost:7071/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tools_loaded','?'))"

# 3. Drift
# Use forge_surface_audit(mode="scan", organ="all")

# 4. Know the pattern
# WELL is the reference. Copy its receipt pattern. Never self-authorize.
```

---

## 🚫 NEVER

- ❌ Emit SEAL from GEOX/WEALTH/WELL — arifOS adjudicates only
- ❌ Self-authorize mutations — requires arifOS SEAL → A-FORGE execute
- ❌ Write to ledger without SEAL→ACK→LEASE→WITNESS chain
- ❌ Use `session_id="test-session"` in receipts
- ❌ Skip receipt generation on any operation
- ❌ Modify VAULT999 outcomes.jsonl — append only
- ❌ Trust affordances.yaml over live tools/list

---

*Forged 2026-07-26 by Copilot CLI under F13 SOVEREIGN.*
*This file is the single source of truth for MCP surface, spec compliance, and agent onboarding.*
*Update after every structural change to the MCP surface.*
