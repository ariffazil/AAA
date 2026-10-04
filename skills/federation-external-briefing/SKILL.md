---
name: federation-external-briefing
description: "Prepare external-facing architecture references for any AI platform to consume the arifOS system. Verifies public endpoint accessibility (HTTP status), compiles a copy-paste prompt template + reality context, and always includes APEX Theory. Use when Arif asks for 'links for external AI', 'external reference', 'architecture briefing', 'what URLs can I paste into ChatGPT/Claude/Gemini', or any task to share the system with someone outside the federation."
version: 1.0.0
author: Hermes Agent (aaa-hermes profile)
license: MIT
metadata:
  hermes:
    tags: [external, briefing, architecture, public-urls, llms.txt, well-known, mcp, github, apex-theory]
    related_skills: [apex-theory-canon, arif-sites-ops, arifos-mcp-audit, federation-infra-verification]
---

# Federation External Briefing

> Prepare external-facing architecture references that any AI platform (ChatGPT, Claude, Gemini, etc.) can fetch to understand the arifOS system.

## When to load

- Arif asks for "links for external AI" / "external reference" / "architecture briefing"
- Someone new needs to understand the system
- New organs or endpoints go live and the reference needs refreshing
- Arif wants to paste system context into an external AI

## Pitfalls

### CRITICAL: External ≠ Local paths
When Arif says "links for external AI", he means **publicly fetchable URLs** (HTTP 200), NOT local `/root/...` paths. An external AI cannot read files on our VPS. Default to `https://` URLs only. Local paths are supplementary context for the briefing document itself, not the deliverable.

### ALWAYS include Apex Theory
Arif explicitly requested APEX Theory in the briefing. Always include `https://arif-fazil.com/doctrine/apex-theory` and the GitHub AAA repo APEX docs.

### ALWAYS verify, don't assume
Run actual HTTP status checks on every URL before including it. Don't list URLs you haven't verified are live. The `llms.txt` or `.well-known` endpoints may change or go down.

### Copy-paste prompt block is the primary deliverable
The most useful format is a ready-to-paste prompt block that includes all URLs + a structured "after reading, explain" request. The comprehensive reference doc is secondary.

## Workflow

### Step 1: Discover all public surfaces

```bash
# Check GitHub repo visibility
for repo in arifOS A-FORGE AAA GEOX WEALTH WELL HERMES arifFlow arif-fazil.com ariffazil web-canon arifOS-model-registry; do
  status=$(curl -sf -o /dev/null -w "%{http_code}" "https://github.com/ariffazil/$repo" 2>/dev/null)
  echo "$repo → HTTP $status"
done

# Check .well-known endpoints
for path in ".well-known/agent.json" ".well-known/identity.json" ".well-known/capability.json" ".well-known/did.json" ".well-known/arifos-federation.json" ".well-known/webmcp.json" "policy.json" "knowledge/corpus.json" "llms.txt" "llms.json" "graph.json" "floors.json" "000/claims.json"; do
  status=$(curl -sf -o /dev/null -w "%{http_code}" "https://arif-fazil.com/$path" 2>/dev/null)
  echo "$path → HTTP $status"
done

# Check MCP endpoints
for ep in "https://arifos.arif-fazil.com/health" "https://mcp.arif-fazil.com/mcp" "https://geox.arif-fazil.com/health" "https://wealth.arif-fazil.com/health" "https://well.arif-fazil.com/health"; do
  status=$(curl -sf -o /dev/null -w "%{http_code}" "$ep" 2>/dev/null)
  echo "$ep → HTTP $status"
done
```

### Step 2: Fetch key content for reality context

```bash
# Site overview (the #1 starting point for any external AI)
curl -sf https://arif-fazil.com/llms.txt

# Federation manifest
curl -sf https://arif-fazil.com/.well-known/arifos-federation.json

# Agent identity
curl -sf https://arif-fazil.com/.well-known/identity.json

# Capability manifest
curl -sf https://arif-fazil.com/.well-known/capability.json

# Constitutional floors
curl -sf https://arif-fazil.com/floors.json

# Sovereign claims (Gödel Lock)
curl -sf https://arif-fazil.com/000/claims.json
```

### Step 3: Compile the briefing

Produce two artifacts:

**A. Copy-paste prompt block** (primary — this is what Arif will actually use):
- Group URLs by purpose: SITE OVERVIEW → AGENT DISCOVERY → CONSTITUTIONAL FLOORS → FEDERATION GRAPH → HUMAN CONTEXT → GITHUB → PUBLIC DOCTRINE → MCP
- End with structured "After reading, explain: 1. What arifOS is 2. 6-organ topology 3. 13 floors 4. 8 canonical tools 5. APEX Theory 6. EUREKA 6-plane 7. EMD reflex arc 8. Authority chain"

**B. Comprehensive reference doc** (secondary — for pinning):
- Full table of all verified URLs with HTTP status
- Reality context (what's live right now)
- APEX Theory summary (3 layers, key insight)
- Doctrine summary (DITEMPA BUKAN DIBERI)
- Save to `/root/AAA/docs/EXTERNAL_ARCHITECTURE_REFERENCE.md`

### Step 4: Verify the deliverable

Before reporting, verify at least the top 5 URLs still return HTTP 200. The briefing is useless if the URLs are dead.

## Canonical URL Inventory (as of 2026-08-10)

| Category | URL | Status |
|----------|-----|--------|
| **SITE OVERVIEW** | `arif-fazil.com/llms.txt` | ✅ |
| **AGENT** | `.well-known/agent.json` | ✅ |
| **IDENTITY** | `.well-known/identity.json` | ✅ |
| **CAPABILITY** | `.well-known/capability.json` | ✅ |
| **DID** | `.well-known/did.json` | ✅ |
| **FEDERATION** | `.well-known/arifos-federation.json` | ✅ |
| **WEBMCP** | `.well-known/webmcp.json` | ✅ |
| **FLOORS** | `arif-fazil.com/floors.json` | ✅ |
| **POLICY** | `arif-fazil.com/policy.json` | ✅ |
| **GRAPH** | `arif-fazil.com/graph.json` | ✅ |
| **KNOWLEDGE** | `arif-fazil.com/knowledge/corpus.json` | ✅ |
| **STRUCTURED** | `arif-fazil.com/llms.json` | ✅ |
| **CLAIMS** | `arif-fazil.com/000/claims.json` | ✅ |
| **DOCTRINE** | `arif-fazil.com/words/doctrine` | ✅ |
| **APEX THEORY** | `arif-fazil.com/doctrine/apex-theory` | ✅ |
| **GENESIS** | `arif-fazil.com/000` | ✅ |
| **PROOF** | `arif-fazil.com/999` | ✅ |
| **MCP GATEWAY** | `mcp.arif-fazil.com/mcp` | ✅ |
| **KERNEL HEALTH** | `arifos.arif-fazil.com/health` | ✅ |
| **GITHUB arifOS** | `github.com/ariffazil/arifOS` | ✅ |
| **GITHUB A-FORGE** | `github.com/ariffazil/A-FORGE` | ✅ |
| **GITHUB AAA** | `github.com/ariffazil/AAA` | ✅ |
| **GITHUB GEOX** | `github.com/ariffazil/GEOX` | ✅ |
| **GITHUB WEALTH** | `github.com/ariffazil/WEALTH` | ✅ |
| **GITHUB WELL** | `github.com/ariffazil/WELL` | ✅ |
| **GITHUB HERMES** | `github.com/ariffazil/HERMES` | ✅ |
| **GITHUB arifFlow** | `github.com/ariffazil/arifFLOW` | ✅ |
| **GLAMA** | `glama.ai/mcp/servers/ariffazil/arifos` | discovery |
| **SMITHERY** | `smithery.ai/server/arifos` | discovery |

## APEX Theory Summary (for inclusion in every briefing)

**Source:** `github.com/ariffazil/AAA` (docs/canon/APEX_THEORY.md) + `arif-fazil.com/doctrine/apex-theory`

Three layers of intelligence:
- **L3: CIVILIZATION (ASI)** — "What should we do?" → Hermes, AAA
- **L2: GOVERNED (AGI)** — "How should we do it?" → A-FORGE, OpenClaw
- **L1: SUBSTRATE (Domain)** — "What are the facts?" → GEOX, WEALTH, WELL

Key insight: No layer can replace the one above it.
Falsifiable core: An unanchored AI cannot produce output with equivalent multi-dimensional structural coherence to anchored arifOS output.

## References

- `/root/AAA/docs/EXTERNAL_ARCHITECTURE_REFERENCE.md` — last compiled briefing (2026-08-10)
- `apex-theory-canon` skill — for deep APEX THEORY questions
- `arif-sites-ops` skill — for operating the public website
- `federation-infra-verification` skill — for verifying federation infrastructure
