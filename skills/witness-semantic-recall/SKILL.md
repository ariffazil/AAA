---
id: witness-semantic-recall
name: witness-semantic-recall
version: 1.1.0
description: "Semantic recall across the federation canon corpus (instruction/canon/eureka/governance/scar/session_closure) with 3-lane embedding fallback. Use when the user asks about F1-F13 doctrine, arifOS canon, AAA governance, EUREKA insights, scar records, or session closures; or when '/canon-remember <query>' is invoked."
owner: 333-AGI
risk_tier: low
floor_scope: [F1, F2, F11]
capability_tier: fed-agent-subagent
ecology_state: WARM
last_operational_bake: 2026-09-22 (session bridge: 3-lane + dual-collection + parallel migration)
---

# Witness Semantic Recall — 3-lane federation canon search

When invoked, run the canonical recall primitive. The system has been architected
to survive a Nov 9 Alibaba free-quota cliff via three independent embedding lanes
and a sibling collection pattern. **This skill is read-only.** No edits.

## When to invoke

Trigger words: `canon`, `recall`, `/canon-remember`, "what does the canon say about X",
"where in the doctrine is Y defined", "find the EUREKA on Z", "governance rule for X",
"F11 audit", "F13 veto procedure", or any reference to sealed canon / governance /
scar memory / session closures.

If the user's natural request is for SOVEREIGN memory recall across the federation
corpus, use this skill.

## How to invoke

The recall primitive is wrapped in the canonical MCP tool `forge_canon_recall`
(registered in A-FORGE). If the tool is unavailable in the current session's MCP
surface, fall back to direct shell invocation:

```bash
python3 -u /root/arifOS/witness-semantic/witness_recall.py "<query>" --limit 7
```

## Architecture (one paragraph)

3-lane embedding fallback:
- **Lane 1** — Alibaba `qwen3.7-text-embedding` (free quota, ~600K tokens, expires 2026-11-09).
- **Lane 2** — Ollama `bge-m3` (local sovereign, 1024-dim, no expiry, no quota).
- **Lane 3** — substring match on stored payloads (always works).

Two Qdrant collections queried when both exist:
- `witness_semantic` — Qwen-built (4,213 points).
- `witness_semantic_bge_m3` — BGE-M3 sovereign sibling (growing; query when ≥80% mature).

When the BGE sibling has ≥ 80% of the Qwen collection's point count, preference flips
to it (cleaner vector geometry). Until then, Qwen is primary.

## Output contract

A `recall()` invocation returns:

```
{
  "query": "...",
  "lane": "lane1-alibaba|lane2-ollama-bge-m3|lane3-substring",
  "sibling_active": bool,
  "sibling_points": int,
  "qwen_points": int,
  "bge_mature": bool,
  "lane_state": {
    "alibaba_consecutive_fail": int,
    "last_alibaba_ok": ts,
    "last_alibaba_fail": ts
  },
  "elapsed_ms": int,
  "result_count": int,
  "results": [{"id", "score", "payload": {"source", "doc_type", "text_excerpt"}, "_source_collection"}],
  "audit": {lane1_attempted, lane1_error, ...},
  "ts": ISO8601
}
```

## Render

For each hit, show: rank · score(4dp) · `[doc_type]` · source path tail (~60 chars).
Optionally include text excerpt (first 200 chars) when `--show-text` set.

Append a 1-line footer with the lane used. If lane is `lane2-ollama-bge-m3`,
emphasise: "Lane is sovereign — no Alibaba quota dependency."

## Failure modes

- `witness_recall.py` not found → report file missing; do not fabricate.
- All 3 lanes down → return empty results + Lane 3 substring hint.
- `forge_canon_recall` returns `SESSION_REQUIRED` → caller is stateless; redirect to direct shell invocation.
- BGE sibling incomplete (< 80% of qwen) → prefer Qwen for precision; do not "fix" by adding BGE results.

## Receipt

Lane B (autonomous, read-only). No constitutional threshold crossed.
Surface source files to caller for citation. No sealing required.

## Operational recipes (live)

```bash
# Health snapshot (human-readable + exit code 0 = healthy)
bash /root/arifOS/witness-semantic/health_check.sh

# Same in JSON form (for cron/dashboards)
bash /root/arifOS/witness-semantic/health_check.sh --json

# Resume migration (idempotent; PID-alive dedup)
bash /root/arifOS/witness-semantic/migrate_resume.sh           # all 6 sources
bash /root/arifOS/witness-semantic/migrate_resume.sh canon     # one source

# Migration stats only
bash /root/arifOS/witness-semantic/witness_migrate.py --stats

# Quick smoke test (4 lanes + e2e recall)
bash /root/arifOS/witness-semantic/verify.sh
```

For cron/health-monitoring:

```cron
*/15 * * * * bash /root/arifOS/witness-semantic/health_check.sh --json >> /var/log/witness-bridge.log 2>&1 || echo "[$(date -Iseconds)] WITNESS BRIDGE DEGRADED" | mail -s "witness bridge degraded" root
```

## Files (canonical surface)

| Path | Role |
|---|---|
| `witness_build.py` | Qwen-built indexer (4,213 points; ran 2026-09-21 21:42) |
| `witness_migrate.py` | BGE-M3 sovereign rebuild (in background; PID logged in /tmp/witness_migrate_*.log) |
| `witness_recall.py` | Recall primitive with 3-lane + dual-collection logic |
| `verify.sh` | Health probe (4 probe points) |
| `health_check.sh` | Production-grade health check (exit code + JSON output) |
| `migrate_resume.sh` | Idempotent resume of any/all migration workers (PID-alive dedup) |
| `STATUS.md` | Operational snapshot with quota, recovery, end-to-end paths |
| `README.md` | Architecture + ops notes |
| `VAULT999 + carry_forward` | Federated audit trail (any session can find receipts) |

## Constitutional signature

- F1 AMANAH: All scripts reversible; idempotent UUID5 IDs.
- F2 TRUTH: Every recall emits lane name + state in payload.
- F11 AUDIT: Bridge work flows through carry_forward + VAULT999 + arifFlow.
- F13 SOVEREIGN: No new governance emitted; only the bridge.

ΔS in this turn: −1 per session iteration; net bridge ΔS = −1 (cliff bridged).
