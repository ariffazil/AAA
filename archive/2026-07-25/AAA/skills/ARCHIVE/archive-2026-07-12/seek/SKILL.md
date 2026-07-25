---
name: seek
description: >
  Web Exploration & Grounding Doctrine.
  Classifies search intent, executes via arif_route, and enforces APEX/F12 provenance.
version: 1.1.0
author: FORGE (000Ω) & Antigravity
forged: 2026-07-08
tags: [websearch, search, routing, perplexity, brave, evidence, grounding]
scope: all_agents
priority: 90
---

# 🌐 SEEK — Web Exploration & Grounding Doctrine

This skill establishes the canonical workflow and enforcement policy for all web-exploration, search, and URL ingestion tasks across the arifOS Federation.

---

## 1. Taxonomy & Federation Mapping

To prevent semantic confusion, the SEEK framework is mapped across three distinct federation layers:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. ROUTE-LEAST-POWER ESCALATION LADDER (Tier 1 to Tier 6)              │
│    SEEK operates strictly in TIER 5 (External API/Network).           │
├────────────────────────────────────────────────────────────────────────┤
│ 2. AUTONOMY TIERS (T1 to T3)                                           │
│    Web searches are T1 (Auto-Do) OBSERVE-class queries. However, if    │
│    search evidence feeds a SEAL-grade claim, it escalates to T3/F13.  │
├────────────────────────────────────────────────────────────────────────┤
│ 3. VERDICT TIERS (DRAFT to SEALED)                                     │
│    Unverified search results = DRAFT. Once hashed via SHA256 and     │
│    scanned for injection, it is promoted to SEALED.                    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Primary, Secondary, and Fallback Routing Rules

SEEK dispatches queries to exactly 7 primary/secondary surfaces based on the intent class, with 1 fallback path and a strict block list.

**Truth Receipt Guard (warga):** Any synthesized claim or finding from search must be passed through enforce_for_warga / claim_must_use_receipt before use in plans or seals. L4 inference by default. See truth-receipt-enforcer skill + GENESIS/020.

```
                         arif_route(intent)
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
 ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
 │    PRIMARY    │       │   SECONDARY   │       │   FALLBACK    │
 │ (3 Surfaces)  │       │ (4 Surfaces)  │       │  (1 Surface)  │
 └───────┬───────┘       └───────┬───────┘       └───────┬───────┘
         │                       │                       │
         ├─ Perplexity           ├─ Brave search         └─ curl (CLI)
         ├─ SearxNG              ├─ Chrome-devtools
         └─ Meyhem               ├─ forge_fetch(URL)
                                 └─ forge_fetch(meta)
```

### Primary Surfaces (3 Surfaces - Core Synthesis & Discovery)
1.  **Perplexity AI (`perplexity_perplexity_ask` / `reason`)**: 
    *   *When*: Intent matches "what is X", comparative queries, or decision justifications.
    *   *APEX G*: 0.391 (ask) / 0.443 (reason).
    *   *Behavior*: Sonar Pro fast synthesis + chain-of-thought ranking.
2.  **SearxNG Search (`aforge_forge_fetch` mode=search)**:
    *   *When*: Intent needs broad multi-engine results (Google CSE + DDG).
    *   *APEX G*: 0.588.
    *   *Behavior*: Raw list return; the only engine that successfully surfaced the arXiv 2507.21206 paper.
3.  **Meyhem Search (`meyhem_search`)**:
    *   *When*: Intent matches academic, scientific, or paper-heavy keywords.
    *   *APEX G*: 0.252.
    *   *Behavior*: Exa-backed; outcome-ranked bias toward arXiv, ACL Anthology, and DOI.

### Secondary Surfaces (4 Surfaces - Targeted Action & Ingestion)
4.  **Brave Search (`aforge_forge_search`)**:
    *   *When*: Q (Quick Recall) of recent facts or specific URLs.
    *   *APEX G*: 0.315.
    *   *Behavior*: Raw Brave API snippets, fast, signed envelope.
5.  **Chrome-Devtools / Browser (`chrome-devtools_navigate_page` / `forge_browser_*`)**:
    *   *When*: JS-rendered sites, screenshots, or form interaction.
    *   *APEX G*: 0.072.
    *   *Behavior*: Headless Chromium execution. High latency, zero synthesis.
6.  **Page Scraper (`aforge_forge_fetch` mode=readable / `fetch_fetch_readable`)**:
    *   *When*: U (URL Ingestion) of raw articles.
    *   *APEX G*: 0.460.
    *   *Behavior*: Readability parser. Strips scripts/CSS, returns F12 injection-scanned markdown.
7.  **Data Extractor (`forge_fetch_metadata` / `forge_fetch_links`)**:
    *   *When*: Extracting headers, keywords, or link arrays.
    *   *Behavior*: Short schema responses, fast execution (<100ms).

### Fallback Egress (1 Surface - Last Resort)
8.  **CLI `curl` / `wget`**:
    *   *When*: All API-backed tools fail or are rate-limited.
    *   *APEX G*: 0.024.
    *   *Behavior*: Sovereign raw outbound. Must use F1 backup before call and F11 log after.

### Banned Surfaces (5 Surfaces - HARAM)
*   ❌ `aforge_forge_minimax_search`: DEAD backend (network fetch failed).
*   ❌ `aforge_forge_probe_site` (HTTP): stdio-only transport leak.
*   ❌ `aforge_forge_skillstore_read` (HTTP): stdio-only transport leak.
*   ❌ `webfetch` (DDG native): Blocks JS, returns empty redirect page.
*   ❌ `fetch_fetch_html` on JS-rendered sites: returns empty container divs.

---

## 3. Enforcement Mechanisms (Anti-Doa Protocol)

To ensure this doctrine is enforced programmatically rather than advisory:

### A. Policy Lock
The execution shell enforces allowed servers at the gateway level. All web tool calls must satisfy the security policy:
```javascript
aforge_forge_policy(
  mode: "set",
  tool_name: "*search*",
  allowed_mcp_servers: ["aforge", "perplexity", "meyhem"]
);
```

### B. Agent Card Binding
All AAA citizen agents must list the `seek` skill in their manifest cards (`agent-card.json` / `agents.yaml`) under the `skills` array. This binds the 3-step routing cadence to their system prompts automatically at load time.

### C. Unified Entrance
Direct tool calls for web search are deprecated. All AAA agents must route through the `arif_route(intent=...)` interface to classify the target intent.
