# Independent Audit Framework (6-Phase, for Sibling-Generated Deliverables)

When a sibling agent (OpenCode, Claude, Codex, a delegated subagent) produces a multi-document deliverable audit — 5+ markdown files, schema proposals, gap analyses, roadmaps — DO NOT trust the chat-level summary. Verify the deliverables on disk.

This is the heavier cousin of the sibling-ops verification pattern: not a one-shot "did they clear the spam?" but a full structured audit of their work.

## When to use

- Sibling agent wrote 4+ markdown files and a chat summary claims "X deliverables, Y lines, Z claims"
- A schema/spec/roadmap was produced that you will rely on for actual operations
- The sibling's chat summary mentions numbers that you (or a third party) will act on
- A "SEAL" was emitted by the sibling and you need to ratify or downgrade it

## The 6 phases (always run in order)

### Phase 0 — Assume nothing

Treat every claim in the chat summary as a *claim to be verified*. Pull the actual files in question and compare. The sibling's `SEAL::xxx::ΔS=-0.87` is a self-report, not a verdict.

### Phase 1 — Artifact validation

| Check | How |
|---|---|
| Directory exists | `ls -la <dir>/` |
| File count matches | `ls *.md | wc -l` |
| Line counts (file-level) | `wc -l <file>` |
| Total bytes | `du -sb <dir>/` |
| SHA256 of each file | `sha256sum *.md` |
| Line count drift expected | If two OpenCode runs happened concurrently, file sizes/line counts may differ from the chat summary. This is cosmetic, NOT data loss. |

**Verdict options:** PASS / FAIL / WARN. Report any discrepancy verbatim.

### Phase 2 — Quality review (per-deliverable)

For each deliverable ask:
- Do the referenced components exist? (ports, files, services)
- Are the connections real? (no invented system names)
- Is the schema syntactically valid? (YAML/Pydantic/SQL parses)
- Is backward compatibility documented?
- Are numerical claims plausible given the scope?

### Phase 3 — Evidence audit (claim → evidence → confidence)

Build a table. For every major claim in the chat summary, find the supporting evidence in the deliverable *and* verify it independently:

| Claim | Source in deliverable | Live evidence | Confidence |
|---|---|---|---|
| "Qdrant has 15 collections" | 01:34 | `curl :6333/collections` | VERIFIED |
| "Graphiti times out" | 03:xxx | `curl :8000/mcp initialize` works | DOWNGRADED |
| "877 existing records" | 06:53 | `arifos_memory` collection has 49 | NOT VERIFIED |

**Confidence tiers:**
- **VERIFIED** — live probe re-confirms exactly
- **SUPPORTED** — indirect probe (file exists, port open); claim reasonable
- **DOWNGRADED** — claim made but live probe contradicts
- **UNVERIFIABLE** — source not accessible from local probe

### Phase 4 — Independent re-probe (~20% sample)

Pick a random sample of factual claims and re-run them, fresh shell. Compute agreement rate. 80%+ = the audit is trustworthy. <70% = the audit is unreliable, more probes needed.

### Phase 5 — Hallucination audit

| Check | Risk |
|---|---|
| Invented files | grep for the file path; does it exist? |
| Invented ports | `curl :port/health` — does it respond? |
| Invented services | `docker ps` — does the container exist? |
| Invented conclusions | Does the conclusion follow from the evidence cited? |

**Overall risk:** NONE / LOW / MEDIUM / HIGH.

### Phase 6 — Seal review

Verify against F1, F2, F3, F4, F11, F13 (the audit-relevant floors). Output one verdict:

- **SEAL** — fully verified, all claims supporting, ready for sovereign ratification
- **PARTIAL** — directionally correct, 1-3 factual downgrades with T1-level fixes
- **HOLD** — significant issues need resolution before use
- **VOID** — fabricated, unreliable, do not use

Always produce a "Seal conditions" section: the specific corrections needed to upgrade the verdict.

## Graphiti MCP handshake pitfall (concrete)

A bare `curl -X POST :8000/mcp -d '{"method":"tools/list"}'` returns empty (looks like timeout). This is NOT a timeout — MCP requires `initialize` first, then `notifications/initialized`, then `tools/list`. Proper sequence:

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"audit","version":"1.0"}}}'
# Then send notifications/initialized, then tools/list
```

If the audit claims "Graphiti MCP times out", verify with the proper handshake before accepting the claim.

## Concurrent OpenCode run race

If two `opencode run` invocations from the same prompt source target the same output directory (or read MISSION.md simultaneously), the second run may overwrite the first's deliverables. Symptoms:
- Line counts of files differ from the chat summary
- File mtimes straddle the two run windows
- Some files are unchanged, others differ

**Not data loss** — the final state on disk is what matters. Document the race in the validation report and proceed with the disk state. Use `pgrep` to find duplicate opencode processes and kill the older one if you want determinism.

## What to write up

Three artifacts:

1. **0N_validation_report.md** — Phases 1-2-5 detail
2. **0N_evidence_matrix.md** — claim-by-claim table with confidence tiers
3. **0N_seal_review.md** — final verdict with constitutional floor assessment + seal conditions

Concise tables, not prose. Each file should be 4-8KB.

## Cost

~4 minutes total for a 6-deliverable audit. 0 schema changes, 0 services restarted.

## Worked example

See `/root/AAA/reports/multimodal-memory-audit/0{7,8,9}_*.md` (VMA-2026-08-07) — full audit of the MMA-2026-08-07 deliverables. Outputs: 9 markdown files, 2 downgraded claims, 1 PARTIAL seal upgraded to FULL after 15-minute corrections.
