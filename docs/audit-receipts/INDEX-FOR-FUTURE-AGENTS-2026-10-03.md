# INDEX FOR FUTURE AGENTS — sealed 2026-10-03 14:20 (FINAL, post-rollback)

**Purpose:** Single landing page for any future agent. What was decided, what NOT to redo.

**Status:** arifOS reverted to clean pre-v2-wire state. 6 keepers in this folder. 2 F13 specs in `../blueprints/`. 1 perpetual audit task in carry_forward.

## TL;DR (5 things)

1. **arifOS is at clean baseline** — `tool_13_arif_memory.py` has NO hybrid wire. v1.5/v2 compiler is **removed and killed** (PID gone). Use it as it was before 2026-10-03 12:21.
2. **FalkorDB is dormant** — 79 nodes, 13 labels, mostly null fields. Don't populate it. 50-query eval proved GMU=0% (see EVAL-V1-VERDICT).
3. **Kernel identity drifts** — 4 sources give different commit hashes. API's `drift=ALIGNED` is misleading. Always cross-check filesystem (see KERNEL-DRIFT-VERIFIED).
4. **Banks are empty** — `token_bank.db` (3 paths) = 0 bytes. PII distillation = spec-only. **Don't bind to empty bank** — spec the missing infra first (see 2 F13 specs in `../blueprints/`).
5. **4 hooks at `/root/.codex/hooks.json` are wired and firing** — SessionStart, PreToolUse, PostToolUse, SessionEnd. Audit data at `/root/.agent-workbench/mcp-audit.jsonl` (6.4 MB today). **Don't add new hooks** unless these don't cover.

## The 6 files in this folder

- `INDEX-FOR-FUTURE-AGENTS-2026-10-03.md` (this file)
- `REALITY-MAP-AAA-AGENTS-2026-10-03.md` — federation inventory (7 organs, 5 L-layers, 23 agent cards)
- `KERNEL-DRIFT-VERIFIED-2026-10-03.md` — 4-way source disagreement probe
- `CROSS-CHECK-WITNESS-2026-10-03.md` — bank-missing findings (token_bank.db all 0 bytes)
- `EVAL-V1-VERDICT-2026-10-03.md` — 50-query falsification of Falkor (GMU=0%)
- `ROLLBACK-V2-WIRE-2026-10-03.md` — what was removed and why (lesson: specs before code, code for measured need)
- `T1-AUTO-WORKQUEUE-20261003.json` — 40KB work queue data, not a receipt, kept for reference

## 2 F13 specs in /root/AAA/docs/blueprints/ (await F13 ratification)

- `FED-TOKEN-LEDGER-SPEC-v1.md` — schema + write hook + read API (~120 LOC, 2-3h work)
- `BEFORE-MODEL-CALLBACK-SPEC-v1.md` — hook infrastructure (~80 LOC, 1-2h work)

## DO NOT REDO (5 things)

- ❌ Don't re-investigate Falkor (proven GMU=0%, see EVAL-V1-VERDICT)
- ❌ Don't re-audit kernel drift (just cross-check filesystem vs API, 1 minute)
- ❌ Don't populate `token_bank.db` or PII bank without F13 spec (see `../blueprints/`)
- ❌ Don't add new hooks (existing 4 at `/root/.codex/hooks.json` cover it)
- ❌ Don't create 20+ receipts for 1 ask (5-6 keepers max — the future needs SIGNAL, not NOISE)

## How to invoke arif_memory (canonical, no hybrid)

```python
# Direct (bypasses HTTP identity gate)
import sys
sys.path.insert(0, '/opt/arifos/arifosmcp/runtime')
from arifosmcp.runtime.megaTools.tool_13_arif_memory import arif_memory
result = await arif_memory(
    mode="recall", query="...", actor_id="<your-actor-id>",
    payload={...},  # standard payload, no hybrid flag
)

# HTTP (production agents with valid SCT)
curl -X POST http://localhost:8088/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"arif_memory","arguments":{"mode":"recall","query":"...","actor_id":"...","session_token":"..."}}}'
```
