---
name: hermes-openclaw-audit
description: Red team + blue team audit comparing Hermes Agent (ASI/MiniMax) vs OpenClaw Agent — skill coverage, capability scoring, gap analysis, and complement strategy
trigger: "audit hermes vs openclaw, compare agents skills, score agents capabilities, red team agents, agent gap analysis"
version: 1.0.0
category: governance
---

# Hermes (ASI) vs OpenClaw Agent — Red Team Audit

## Audit Context
- **Hermes Agent**: MiniMax M2.7 terminal session at `af-forge VPS` (10.30.42.143), Hermes runs as primary AI agent via MiniMax's platform (ASI-level session)
- **OpenClaw Agent**: Local `openclaw` CLI agent running on same VPS at `localhost:18789` — runs `arifOS_bot` in Telegram "Chatgpt" supergroup
- **Federation**: Hermes orchestrates → ASI decides → OpenClaw executes in group
- **Both share**: MiniMax API key, arifOS MCP federation, `/srv/openclaw/workspace/` workspace

---

## Step 1 — Capability Baseline (16-point grid)

Score each capability 0 (absent) / 0.5 (broken/incomplete) / 1 (working). Both agents on same 2026-05-04 audit.

| # | Capability | Hermes (ASI) | OpenClaw | Gap |
|---|-----------|-------------|----------|-----|
| 1 | Web search | ✅ 1 | ⚠️ 0.5 (Discord broken) | Hermes |
| 2 | Multimodal vision | ✅ 1 (mmx vision describe --image <path> --prompt "?" ) | ✅ 1 (MiniMax MCP tool via arifOS) | Tie |
| 3 | Terminal/CLI | ✅ 1 | ✅ 1 | Tie |
| 4 | Python coding | ✅ 1 | ✅ 1 | Tie |
| 5 | TypeScript/Node.js | ⚠️ 0.5 (deferred to Claude Code) | ✅ 1 (native) | OpenClaw |
| 6 | arifOS MCP tools | ✅ 1 (localhost:8080) | ✅ 1 (localhost via patched URL) | Tie (FIXED) |
| 7 | Scheduling/cron | ✅ 1 (cronjob tool) | ✅ 1 | Tie |
| 8 | Email (Gmail) | ✅ 1 (gmail skill) | ❌ 0 | Hermes |
| 9 | File read/write | ✅ 1 | ✅ 1 | Tie |
| 10 | Skill loading | ✅ 1 | ✅ 1 (skills copied to /srv/openclaw/workspace/skills/) | Tie (FIXED) |
| 11 | Claude Code exec | ⚠️ 0.5 (installed, no SKILL.md) | ⚠️ 0.5 (installed, no SKILL.md) | Tie (STILL BROKEN) |
| 12 | Apple/creative | ❌ 0 | ⚠️ 0.5 (some apple skills) | OpenClaw |
| 13 | MLOps/infra | ⚠️ 0.5 (Docker commands) | ✅ 1 (docker-compose, kubectl) | OpenClaw |
| 14 | SecOps | ✅ 1 (secops-by-joes skill) | ⚠️ 0.5 (audit tool present) | Hermes |
| 15 | Governance/Floors | ✅ 1 (arifOS sense, F1-F13) | ❌ 0 | Hermes |
| 16 | Speech/TTS | ✅ 1 (text_to_speech) | ❌ 0 | Hermes |
| 17 | A2A delegation | ✅ 1 (A2A mesh live port 18001) | ✅ 1 (A2A adapter port 18002) | Tie (FIXED 2026-05-04) |
| 18 | Telegram independence | ✅ 1 (sole poller @ASI_arifos_bot) | ✅ 1 (@AGI_ASI_bot separate bot) | Tie (FIXED 2026-05-04) |
| | **TOTAL** | **13.5/18** | **12.0/18** | **Hermes leads slightly** |

---

## Step 2 — Red Team: Hermes (ASI) Weaknesses

### W1 — Multimodal Vision Broken Pipe (CRITICAL)
**Finding**: `vision_analyze` tool fires but `mmx` skill never gets called. The tool handler exists in Hermes tools but has no description → can't be triggered by natural language. Even when invoked manually, the vision pipeline is not wired to `mmx` CLI.

**Evidence**:
```
User: 👁️ vision_analyze: "What does this image show?"
Result: Tool fired with no description, mmx skill NOT activated, pipe broken
```

**Root cause**: Tool-to-skill wiring gap. `mmx` skill exists (`/root/.hermes/skills/mmx/SKILL.md`) with `vision_analyze()` documented but NOT auto-loaded by the tool handler.

**Fix**: Two options:
1. **Fast patch** (no code change): Load mmx skill explicitly in session → call `mmx gen image-prompt` or use MiniMax vision API directly
2. **Proper fix**: Patch Hermes tool handler to call mmx skill when vision_analyze fires

### W2 — Claude Code Not Wired
**Finding**: `codex` directory exists at `/srv/openclaw/workspace/codex/` but has no `SKILL.md`. Claude Code binary is installed (`/usr/bin/codex`) but Hermes has no SKILL.md to define how to invoke it.

**Fix**: Create `/root/AAA/skills/codex/SKILL.md`:
```markdown
# Claude Code Skill

## Trigger
"codex", "typescript", "node.js debug", "fix TS error"

## Command
codex --acp --stdio

## Notes
- Installed at /usr/bin/codex
- Use with acp_args: ['--acp', '--stdio']
- Works inside /srv/openclaw/workspace/
- skill_forensics: rate 8/10 (rate code changes 8, security 8)
```

### W3 — No Jupyter Live Kernel
**Finding**: Python coding is sync-only (`execute_code` tool). No REPL, no notebook, no stateful execution between calls.

**Fix**: Not critical for Arif's workflow — `execute_code` covers most needs.

---

## Step 3 — Red Team: OpenClaw Weaknesses

### W1 — Claude Code Not Wired (STILL OPEN)
**Finding**: `codex` binary is installed at `/usr/bin/codex` but has no `SKILL.md` for either Hermes or OpenClaw. Neither agent can invoke it properly.
**Status**: UNCHANGED — still needs SKILL.md creation.
**Fix**: See Step 5, FIX 3 in this skill.

### W2 — Multimodal Vision (RESOLVED ✅)
**Finding (STALE)**: `vision_analyze` tool fires but `mmx` skill never gets called.
**Resolution (2026-05-04)**: `mmx vision describe --image <path> --prompt "?"` works correctly. MiniMax MCP `minimax__understand_image` also available via arifOS federation.
**Verification**: `mmx vision describe --image /tmp/audit_vision_test.png` returned "pink pig's head" ✅

### W3 — No Jupyter Live Kernel (UNCHANGED)
**Finding**: Python coding is sync-only (`execute_code` tool). No REPL, no stateful execution between calls.
**Status**: Not critical for Arif's workflow — `execute_code` covers most needs.

---

## Step 3 — Red Team: OpenClaw Weaknesses

### OW1 — MCP URLs (RESOLVED ✅)
**Finding (STALE)**: All 5 MCP servers configured with Cloudflare public URLs — all timeout from VPS.
**Resolution (2026-05-04)**: All MCP URLs patched to `http://127.0.0.1:PORT/mcp`:
- arifOS → `localhost:8080` ✅
- WEALTH → `localhost:8082` ✅
- GEOX → `localhost:8081` ✅
- WELL → `localhost:8083` ✅
**Verification**: JSON-RPC probes returned correct tool counts (13, 50, 118, 45).

### OW2 — arifOS MCP REST Routes Module Error (STILL OPEN)
**Finding**: `docker exec arifosmcp cat /app/arifosmcp/runtime/rest_routes/rest_routes.py` shows missing imports: `from arifosmcp.runtime.build_info` and `from .floors`.
**Impact**: `/health` returns 404, but MCP protocol at `/mcp` still works.
**Status**: UNCHANGED — MCP tools still functional via `/mcp` endpoint. REST routes degrade but don't break core function.
**Fix**: See `arifos-fastmcp-http-app-debug` skill.

### OW3 — Claude Code Not Operational (STILL OPEN — shared with Hermes)
See W1 above. Both agents have partial install.

### OW4 — Orphaned Gateway Process (RESOLVED ✅)
**Finding (STALE)**: `systemctl --user status openclaw-gateway` showed `failed (exit-code 78)` but gateway alive as orphaned root process.
**Resolution (2026-05-04)**: Root cause was Telegram bot polling collision. Fixed by giving each agent its own bot token:
- Hermes = `@ASI_arifos_bot` (NousResearch OAuth)
- OpenClaw = `@AGI_ASI_bot` (token `8149595687:*`)
**Result**: OpenClaw gateway restarted under systemd control. No more orphan. Memory dropped from 1.6GB to 344MB.

### OW5 — Telegram Collision (RESOLVED ✅)
**Finding (STALE)**: Both gateways polling SAME Telegram bot simultaneously.
**Resolution (2026-05-04)**: Each gateway now polls its own bot exclusively. Confirmed via `ps aux` showing separate PIDs, separate bot tokens.

---

## Step 4 — Complement Strategy

### Hermes Covers OpenClaw's Gaps:
1. **Email** → Hermes has gmail skill; OpenClaw has none
2. **Governance/Floors** → Hermes has arifOS-sense; OpenClaw is pure execution
3. **Speech/TTS** → Hermes has text_to_speech; OpenClaw has none
4. **Web search** → Hermes has brave-search; OpenClaw Discord broken
5. **arifOS MCP** → Hermes talks to arifOS MCP directly; OpenClaw MCP URLs broken

### OpenClaw Covers Hermes's Gaps:
1. **TypeScript/Node.js** → OpenClaw is native; Hermes defers to Claude Code
2. **MLOps/infra** → OpenClaw has docker-compose, kubectl; Hermes limited to basic Docker
3. **Apple/creative** → OpenClaw has some apple skills; Hermes has none
4. **Long-running background agents** → OpenClaw has persistent `main` + `codex` agents; Hermes is single-shot per session

### Shared Gaps (Both Broken):
1. **Multimodal vision** — both need mmx vision wiring fix
2. **Claude Code** — both have partial install, need SKILL.md

---

## Step 5 — Priority Fixes (What Still Needs Doing)

### FIX 1 — Claude Code SKILL.md (Medium priority — both agents)
```bash
mkdir -p /root/AAA/skills/codex
cat > /root/AAA/skills/codex/SKILL.md << 'EOF'
---
name: codex
description: Claude Code CLI — full Claude Opus-4 coding agent with ACP stdio transport
trigger: "codex, typescript, node.js debug, fix TS error, refactor node"
version: 1.0.0
category: coding
---

# Claude Code Skill

## Invocation
Binary: `/usr/bin/codex`
Transport: ACP stdio — use with `acp_args: ['--acp', '--stdio']` in delegate_task

## When to Use
- TypeScript/Node.js debugging or refactoring
- Complex multi-file TypeScript changes
- A-FORGE related work (A-FORGE is TypeScript/Node.js)
- When Hermes says "deferring to Claude Code"

## Environment
- Workspace: `/srv/openclaw/workspace/`
- Use delegate_task with role='leaf' and acp_command='codex'

## skill_forensics rating
- Rate code changes: 8/10
- Security review: 8/10
EOF
```

### FIX 2 — arifOS REST Routes Module Errors (Low priority — MCP still works)
- Missing modules: `arifosmcp.runtime.build_info` and `.floors` in Docker image
- Impact: `/health` returns 404 (cosmetic only)
- Core MCP tools at `/mcp` unaffected
- See skill: `arifos-fastmcp-http-app-debug`

### FIX 3 — Systemd Services for A2A Adapters (Low priority)
- Adapters currently run via nohup (working but not restart-on-boot safe)
- Systemd unit files exist at `/opt/arifOS/a2a-adapters/*.service`
- Need: `systemctl --user daemon-reload` + `systemctl --user enable hermes-a2a openclaw-a2a`

---

## Step 6 — Scoring Summary (Updated 2026-05-04)

| Agent | Score | Strongest | Weakest |
|-------|-------|-----------|---------|
| **Hermes (ASI)** | 13.5/18 | Governance, Email, arifOS, SecOps, TTS, A2A, Vision | Claude Code, TypeScript |
| **OpenClaw (AGI)** | 12.0/18 | TypeScript, MLOps, Apple, A2A, Telegram independence | Email, Governance, TTS |

**Federation verdict**: Hermes leads slightly on constitutional intelligence. OpenClaw leads on execution infrastructure. Both needed — complementary, not redundant.

**Remaining shared technical debt**: Claude Code SKILL.md, arifOS REST routes cosmetic error.

**Resolved this session**: vision pipeline, MCP URL routing, Telegram collision, A2A mesh, OpenClaw Telegram independence.
