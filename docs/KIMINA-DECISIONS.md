# KIMINA Decision Record — Three Pending Items from 2026-09-16

## 1. Graphiti 13.9 min/episode — RECOMMENDATION

**Root cause:** 7B model on 4 vCPU CPU-only. ~17 sequential extraction calls × 1.5-3 min each.

**Recommendation: Hybrid extraction (cloud for extraction, local for embeddings)**
- Extraction sends text to a cheap hosted model (qwen2.5:7b on FED, or Z.AI GLM flash)
- Embeddings stay local (bge-m3, 0.18s, already fast)
- Graph + memory store stay on KVM4
- Data at rest never leaves; only the text being extracted is sent
- Cost: minimal (bursty, low-volume workload)

**Why not add cores to KVM4:** KVM4 has 4 vCPU / 16 GB. KVM8 has 8 vCPU / 32 GB. Adding cores to KVM4 means paying for a bigger VPS. Cloud extraction is cheaper for bursty workloads.

**Risk:** Sovereignty question is bounded — extraction text is transient, graph is local.

## 2. arifFlow 3/8 actors — FINDING

**Live data:** arifFlow tracks 4 actors (not 3 or 8):
- 333-AGI — VERIFICATION DOMINANCE (1 verify, 0 execute) — OK
- 333-AGI/agentic-web — HELD (FQ=0.00, execution dominance)
- 333-AGI/dynamic-gate — HELD (FQ=0.00, execution dominance)
- grok-build — FLOWING (2 verify, 0 execute) — OK

**Primary pathology:** GOVERNANCE_COLLAPSE (vector diagnosis)
- g (genius) = 0.4786 → PATHOLOGICAL
- w3 (tri-witness) = 0.7439 → CAUTION
- Other dimensions healthy

**Verdict:** This is a governance surface — 2 actors executing without verification. Court's work as Arif said. Not blocking Kimi Code upgrade.

## 3. grok MCP — CONFIRMED DISABLED

**Evidence:** 0 references to "grok" in `/root/.kimi-code/mcp.json`
**Arif's statement:** "sengaja dimatikan sejak 21 Ogos"
**Doc claim:** 6 servers — stale documentation

**Recommendation:** Update docs to reflect reality. No action needed unless Arif wants grok re-enabled.

---

All three are informational. None block the Kimi Code upgrade.

DITEMPA BUKAN DIBERI ⚒️
