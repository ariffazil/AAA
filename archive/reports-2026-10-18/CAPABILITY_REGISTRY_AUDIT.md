# CAPABILITY REGISTRY DEDUPLICATION AUDIT (P2)

> **Status:** AUDIT COMPLETE · P2 CAPABILITY GROUNDING (2026-09-08)  
> **Authority:** ARIF (F13 Sovereign Directive — Governance Hygiene)  
> **Axiom:** Static Number → Dynamic Probe · Documentation Claim → Runtime Authority  
> **Truth Rule:** `live :port/health` beats every prose table. Static counts are historical snapshots, never canonical law.

---

## 1. Executive Summary

Static tool counts, service counts, and capability tallies represent the **highest frequency of drift** across the federation repository.

An exhaustive census comparing documented claims against **live HTTP runtime probes** (`localhost:PORT/health`) on 2026-09-08 demonstrates why static counts must be stripped of normative authority.

### The Contrast: Doc Claims vs Live Reality

| Organ | Documented Static Claims | Live Discovery Probe | Live Reality (Observed) | Drift Verdict |
|---|---|---|---|---|
| **arifOS** | "8 public tools" | `curl :8088/health` (`contract_status.tool_count`) | **8 tools** | **MATCHED** (Stable Kernel) |
| **A-FORGE** | "116 API / 112 MCP", "77 / 82 whitelist", "110+" | `curl :7072/health` (`tools_listed` / `stateless_tools`) | **118 listed** (81 stateless) | **LAG DRIFT** (+2 to +8 new tools unreflected in docs) |
| **GEOX** | "32 tools", "33 tools" | `curl :8081/health` (`canonical_tools`) | **26 tools** | **INFLATION DRIFT** (-6 tools; pruned or consolidated) |
| **WEALTH** | "14 public (9 canonical)", "8 tools" | `curl :18082/health` (`canonical_tools`) | **11 tools** | **CLASSIFICATION DRIFT** (Canonical tools consolidated to 11) |
| **WELL** | "10 tools", "10 (health degraded)" | `curl :18083/health` (`tool_count`) | **31 tools** | **MASSIVE DRIFT** (21 tools added since last doc update) |
| **arifFLOW** | "2 tools", "flow_health" | `curl :7073/health` (`metric_frame`, `vector`) | **Metabolic Engine** | **CATEGORY ERROR** (Metabolic bus, not a tool vendor) |
| **FRAME** | Omitted in older tables | `curl :18085/health` (`chambers`) | **7 active chambers** | **OMISSION DRIFT** (Now recognized in SOT) |

---

## 2. Classification of Capability Claims

Every capability mention across `/root/AAA` and `/root/arifOS` is now formally classified into three epistemic tiers:

1. **Runtime Fact (Dynamic Authority):**
   * Emitted exclusively by the running daemon via HTTP `/health` or MCP `tools/list`.
   * Never hardcoded into markdown files.
   * Accessible via CLI: `now`, `make health`, or direct curl.

2. **Historical Snapshot (F11 Audit Lineage):**
   * Retained in historical seal documents, release notes, and archived logs (e.g. "T₁ snapshot 2026-07-30").
   * Must carry the standard header:
     `> [HISTORICAL SNAPSHOT · NOT SOT] For live capability, query live runtime.`

3. **Documentation Example (Illustrative):**
   * Code snippets showing how to invoke a tool (e.g. `aforge_forge_shell`).
   * Expresses pattern and interface schema, never a commitment to total tool inventory.

---

## 3. Grounding Policy (The Anti-Staleness Rule)

To prevent future capability drift without inflating doctrine:

1. **Purge Static Tallies from Canonical Titles:**
   * Do not write "The 13-Tool Manifest" or "The 20-Tool Matrix" in permanent law. Tool inventory is an implementation detail; governance binds the **authority ceiling** (`JUDGE_ONLY`, `COMPUTE_ONLY`, `EXECUTE_AFTER_SEAL`), not the count.
2. **Standard Discovery Vector:**
   * When an agent needs to know what an organ can do, it MUST NOT read a markdown list. It MUST introspect:
     * Kernel: `call arif_route` or query `:8088/health` (`capability_map`)
     * Actuator: `curl :7072/health` (`tools_listed`, `stateless_tools`)
     * Specialists: Query local MCP endpoint via `list_tools`
3. **Zero New Files / Zero New Doctrine:**
   * P2 does not add a new "capability registry" database. The daemons *are* the registry.

---

## 4. Conclusion

```text
Static Count Drift:          EXPOSED AND QUARANTINED
Documentation Authority:     REVOKED for tool counts
Runtime Authority:           AFFIRMED (:port/health is sole truth)
Net Inflation:               0 new files · 0 new doctrines · ΔS ≤ 0
```

DITEMPA BUKAN DIBERI.
