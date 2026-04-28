---
name: archive-audit-recursive-improvement
version: 1.0.0
description: Distill intelligence from archive directories before deletion — contrast against live state, track gaps in wiki, then prune noise safely.
tags: [archive, wiki, audit, recursive-improvement]
created: 2026-04-26
authority: ASI
motto: Ditempa Bukan Diberi
---

# Archive Audit + Recursive Improvement Log

**When to use:** When pruning old archives and you need to distill intelligence before deletion — ensuring no eureka is lost in the noise.

**Trigger:** Before deleting any large archive directory.

---

## Workflow

### Phase 1: Discovery Scan

```bash
# Find all .md files in archive
find /path/to/archive -name "*.md" 2>/dev/null | sort

# Categorize by date/type
ls -la /path/to/archive/
```

### Phase 2: Read Strategy (Adaptive Sampling)

Never read everything. Sample strategically:

| File pattern | Read? | Why |
|---|---|---|
| `*eureka*` or `*extraction*` | YES | Intentional distillation |
| `*audit*` or `*report*` | YES | Engineering findings |
| `*path_to*` or `*blueprint*` | YES | Architecture decisions |
| `*2026-03-30-*.md` | NO | Session metadata spam |
| `session*` or `memory-2026-*.md` | NO | Raw logs, no synthesis |
| `*.bak` or `*backup*` | NO | Stale copies |

**Rule:** If a file was produced by an agent reflecting on work (not raw session output), it has intelligence potential.

### Phase 3: Contrast Against Live State

For each potential insight, check current state:

```bash
# Check arifOS MCP version and tool count
curl -s http://localhost:8080/health 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('version'))"

# Check Qdrant container
docker ps | grep qdrant

# Check A2A endpoint
curl -s http://localhost:8080/a2a/wire 2>/dev/null

# Check tool list
curl -s -X POST http://localhost:8080/mcp -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' 2>/dev/null
```

### Phase 4: Distill into Wiki Page

Create `wiki/pages/recursive-improvement-log.md` with sections:

- **P1 Gaps Confirmed** — items from archive that are still undone
- **Implementation Patterns** — defined but not wired
- **Spec Enrichment** — archive richer than current
- **Historical Corrections** — already fixed
- **Archive Disposition** — what to keep vs delete with rationale

### Phase 5: Update Wiki Index + Log

- Add new section to `INDEX.md`
- Append entry to `LOG.md` with audit date + key findings

### Phase 6: Deletion with Authority

Only delete after:
1. Wiki page created with intelligence distilled
2. INDEX updated
3. LOG updated
4. One explicit user confirmation (SEAL pattern)

---

## Key Lessons Learned

1. **Session metadata spam** (`2026-03-30-*.md`) — just Telegram headers repeated. No intelligence. Safe to delete without reading.
2. **Eureka files** (`*eureka*`, `*extraction*`) are intentionally produced — always read these first.
3. **P1 items recur** — old PATH TO FORGE had Qdrant + A2A as P1. Same items still undone. Without persistent tracking, they keep surfacing.
4. **Contrast analysis** is the only way to know if a gap is "still undone" vs "actually fixed." Don't assume — cross-reference with live endpoints.
5. **Archive audit distills into wiki**, not into more archives. The wiki is the living knowledge base.
6. **Don't read everything** — adaptive sampling based on filename patterns avoids token burn. Session logs that say "just hi" waste everyone's time.
7. **Always update LOG.md** — append-only chronological record proves the audit happened.
8. **Two types of eureka require different paths:**
   - **Spec enrichment** (Delta Bundle, Quantum Sabar, Extension Hooks) → forge directly into runtime code (`tools_*.py`, schemas, headers)
   - **P1 gaps** (Qdrant, A2A) → track in `wiki/RECURSIVE_IMPROVEMENT_LOG.md`
9. **Archive files must be git-tracked before deletion** — check with `git ls-files archive/` to confirm the directory was actually tracked, not just sitting in working tree.
10. **For git push of workspace repos** — branch may lack upstream. Use `git push --set-upstream origin master` on first push to avoid silent failure.

---

## Verification

After deletion:
- Confirm wiki page exists at `wiki/pages/recursive-improvement-log.md`
- Confirm INDEX.md has the new section
- Confirm LOG.md has the audit entry
- Spot-check 3 files from deletion list to confirm they contained no intelligence