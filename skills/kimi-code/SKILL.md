---
name: kimi-code
description: 'Diagnose and operate Kimi Code (kimi-code ≥0.29) — the dynamic, multi-modal coding harness with per-model capability signatures and runtime model selection.'
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [kimi-code, multimodal, dynamic-model, coding-agent, federation]
    related: [opencode, codex, claude-code, federation-seat-wiring, federation-model-routing]
---

# Kimi Code — Dynamic Multi-Modal Coding Harness

Kimi Code is a per-model-capability harness, NOT a single-model CLI. The active model rotates at runtime based on task type (image input → image_in-capable model; code-only → text-only fast model). Configuration lives at `KIMI_CODE_HOME=/root/.arifos/agents/kimi/` (config.toml + mcp.json + plugins/installed.json + agents/*.md + skills/). **Do not assume a single default model — read the `[models.*]` capabilities table before diagnosing "wrong model" reports.**

## When to use this skill

- User pastes a Kimi Code TUI screenshot and asks "what model is this?" — answer from `default_model` in config.toml, not the rendered UI banner.
- User reports Kimi Code picked the wrong model for a task — diagnose via `[models.*].capabilities`.
- User wants to add a new model to Kimi Code — patch `[models.*]` + `[providers.*]` blocks.
- User reports `kimi` CLI error on startup — usually MCP launcher, config schema, or missing capability.
- Federation wiring question: when does Kimi Code use FED aliases vs direct providers?

## Anatomy of a Kimi Code config

```
$HOME/.arifos/agents/kimi/
├── config.toml             # main config (TOML, not JSON)
├── mcp.json                # MCP server definitions (JSON)
├── kimi.json               # legacy / harness settings
├── agents/                 # markdown customization files (af-forge.md, af-explore.md, ...)
├── skills/                 # user-scope skill packs
├── plugins/installed.json  # managed plugin registry (e.g. aaa-federation)
├── hooks/                  # witness-only Pre/Post tool/session/subagent/compact hooks
├── mcp-launchers/          # shell scripts that wrap MCP server commands
├── oauth/                  # OAuth credentials for providers
├── credentials/            # API key vault (kunci-mas pattern)
├── tui.toml                # TUI rendering settings
├── SYSTEM.md               # permanent v2 identity overlay
└── sessions/               # session store
```

**Two config files do similar jobs — keep straight:**

| File | Format | Edits via |
|---|---|---|
| `config.toml` | TOML | Hand-edit; `[models.*]`, `[providers.*]`, `[image]`, `[thinking]` blocks |
| `mcp.json` | JSON | Hand-edit; MCP server roster, timeouts |

## The dynamic model model — capability-driven selection

Kimi Code declares every model's capability signature explicitly:

```toml
[models."minimax-coding-plan/MiniMax-M3"]
provider = "minimax-coding-plan"
model = "MiniMax-M3"
max_context_size = 204800
max_output_size = 131072
capabilities = [ "image_in", "video_in", "thinking", "tool_use" ]
display_name = "MiniMax-M3"

[models."minimax-coding-plan/MiniMax-M2.7"]
provider = "minimax-coding-plan"
model = "MiniMax-M2.7"
capabilities = [ "thinking", "tool_use" ]   # ← text-only, no image_in

[models."kimi-code/kimi-for-coding"]
model = "kimi-for-coding"
capabilities = [ "thinking", "always_thinking", "image_in", "video_in", "tool_use" ]
```

**Capability catalog:**

| Capability | Means |
|---|---|
| `thinking` | Model supports extended reasoning |
| `always_thinking` | Model always thinks before answering (no toggle) |
| `image_in` | Accepts image attachments |
| `video_in` | Accepts video attachments |
| `tool_use` | Supports function/tool calling |

**Runtime selection rule:** when a task arrives with an image attachment, Kimi Code filters the `[models.*]` table to entries with `image_in` in their list. Text-only tasks skip those, picking the cheapest `thinking` model. **There is no "primary" assignment at request level** — capability matching is the gateway.

**This is the answer to "what model is shown in TUI":** the banner's `Model: <name>` is `default_model` from config.toml (`default_model = "minimax-coding-plan/MiniMax-M3"` in this federation). At request time, the actual served model may rotate based on input type. **Do NOT diagnose "wrong model picked" without checking the input payload + capability match.**

## Main agent vs sub-agents

Kimi Code uses a **markdown customization file per agent**, NOT a JSON registry:

```
agents/
├── af-forge.md           # main agent (Markdown identity + system prompt overlay)
├── af-explore.md         # sub-agent: read-only exploration
├── af-plan.md            # sub-agent: planning
├── af-fix.md             # sub-agent: targeted fix
├── af-coordinator.md     # sub-agent: routes to other sub-agents
├── af-worker.md          # sub-agent: heavy work
├── af-reviewer.md        # sub-agent: review/critique
```

Plus the built-ins `explore`, `plan`, `coder`.

**`SYSTEM.md` v2 overlay** — requires `KIMI_CODE_EXPERIMENTAL_FLAG=1` env var for full effect; the file provides a permanent identity layer on top of `config.toml`.

## MCP server launchers — the script-resolver rule

Kimi Code's `mcp.json` often references shell scripts that wrap the actual MCP binary:

```json
{
  "semgrep": {
    "command": "sh",
    "args": ["-lc", "exec /root/.arifos/agents/kimi/mcp-launchers/semgrep.sh"]
  }
}
```

**Pitfall:** the launcher script must exist at the absolute path AND be executable. If the script's underlying binary is missing (e.g. `semgrep` not installed), Kimi Code logs "server unavailable" but doesn't always fail loud. Always probe the launcher independently:

```bash
bash /root/.arifos/agents/kimi/mcp-launchers/semgrep.sh --version
```

If it errors, the MCP server is dead. Don't trust Kimi Code's "server unavailable" as the diagnosis — verify the launcher first.

## Federation wiring — when does Kimi Code talk to FED?

Kimi Code talks to providers DIRECTLY, not through the LiteLLM FED aliases. The `[providers.*]` block in config.toml sets `type = "anthropic"` / `type = "openai"` and the harness uses each provider's native transport. FED is bypassed by default. To route Kimi Code through FED, you must:

1. Add a provider entry with `api_base = "http://127.0.0.1:4000/v1"` and the FED master key
2. Patch each `[models.*]` to use the FED-prefixed model id

This is intentional — Kimi Code's per-capability model selection is best served by direct provider access. **Do not "fix" this by routing everything through FED.**

## Hooks — K-02 enforcement (with gap)

As of 2026-08-07 K-02 patch, Kimi Code's `aaa-witness-pre.sh` hook is **partially enforcement-capable**: it `exit 2`s on `permissionDecision: deny`, which the Kimi runtime treats as a hard block.

**What K-02 blocks (verified live-fire 2026-08-07, K-02 patch in `aaa-witness-pre.sh` line ~272):** `rm -rf` of system paths, `DROP TABLE`, `DROP DATABASE`, force-push, hard reset, git clean -fd, disk formatting, block-device writes, chmod 777 on system paths. Patch is `exit 2` on `PERMISSION=deny` (originally witness-only by F13 override 2026-06-23, hardened 2026-08-07).

**K-02 patch mechanics (read the actual code at `hooks/aaa-witness-pre.sh`):**
- 23KB script, JSON parse, single stdout, append-only audit
- Pattern matchers in `BLOCK_REASON` table fire on the command string
- Outputs `hookSpecificOutput.permissionDecision: deny` + `exit 2`
- The `exit 2` is the inflection — without it, witness logs violation but harness proceeds
- Reversible: revert the `if [[ "$PERMISSION" == "deny" ]]; then exit 2; fi` block → witness-only restored

**K-02 comparison with Hermes hook:**
| Pattern | Kimi | Hermes |
|---|---|---|
| `rm -rf /` | ✅ | ❌ not matched |
| `DROP TABLE` | ✅ | ✅ |
| Force push | ✅ | ✅ |
| `chattr -i vault` | ❌ not matched | ✅ matched |
| `kunci-mas` | ❌ not matched | ✅ matched |
| `systemctl restart` | ✅ matched | ✅ matched |
| `git reset --hard` | ✅ | ❌ |
| `chmod 777 /` | ✅ | ❌ |
| `/dev/sd*` block devices | ✅ | ❌ |

Kimi covers catastrophic destruction; Hermes covers secret-path disclosure. **Two different invariants, both required.**

**What K-02 does NOT block (the secrets gap, verified live-fire 2026-08-07):** secret-path reads (`cat /root/.secrets/kunci-mas.env`), `.signing_key`, `vault.env`, `id_rsa`, `*.pem`. Plus the matcher `Bash|Shell|Write|WriteFile|Edit|StrReplace|StrReplaceFile` doesn't cover `Read`, `WebFetch`, `WebSearch`, `Task`, `NotebookEdit`, `MultiEdit` — so a secret read via `Read` bypasses the hook entirely.

**Don't write hooks that try to gate ALL tools.** The matcher is selective, the BLOCK_REASON table is selective. Extend carefully, test live-fire, document the gaps. See `references/kimi-hook-enforcement.md` for the full table, gap analysis, and the 3-step recipe to add new patterns.

## Auto-fixing the "small model not found" issue

Kimi Code uses a `small_model` (typically `ollama/qwen2.5-coder:3b`) for title-generation and lightweight tasks. If ollama doesn't have that model pulled, the title bar shows "small model unavailable" and falls back to the full primary. Verify:

```bash
# What's actually in ollama?
curl -s http://127.0.0.1:11434/api/tags | jq '.models[].name'

# Is the configured small_model present?
grep "^small_model" /root/.arifos/agents/kimi/config.toml
```

Mismatch = either pull the model (`ollama pull qwen2.5-coder:3b`) or change `small_model` to a model that IS pulled.

## Quick diagnosis recipes

```bash
# 1. What's the active default?
grep "^default_model" /root/.arifos/agents/kimi/config.toml

# 2. What's the small_model?
grep "^small_model" /root/.arifos/agents/kimi/config.toml

# 3. List all configured models + their capabilities
grep -B1 -A5 'capabilities.*=.*\[' /root/.arifos/agents/kimi/config.toml

# 4. Are all MCP servers responding? (probe each in mcp.json)
jq -r '. | keys[]' /root/.arifos/agents/kimi/mcp.json

# 5. Is the kimi-code binary the right version?
kimi --version    # or: /root/.kimi-code/bin/kimi --version

# 6. Did the plugin (aaa-federation) load?
jq '.plugins.installed' /root/.arifos/agents/kimi/plugins/installed.json 2>/dev/null

# 7. Doctor says OK but login fails? Check hook events vs enum
strings /root/.kimi-code/bin/kimi | grep -A20 'HOOK_EVENT_TYPES\$1 ='
```

## Headless dispatch — forging via SPEC file (verified 2026-08-13)

For non-interactive forge tasks, run Kimi Code in prompt mode with a self-contained SPEC file (prompt-improver philosophy: one precise, context-rich spec so the first output is right — no correction loops).

1. Write `SPEC.md` in a staging dir (`/root/forge_work/<name>/`): what to build, working-dir constraint, exact read-only input paths, deliverables, constraints, and a **Definition of Done** ending with "Run all checks yourself and paste their actual output in your final answer." Copy `templates/SPEC-forge.md`.
2. Dispatch in background (a full forge runs ~5–10 min):
   ```bash
   cd /root/forge_work/<name> && export KIMI_CODE_HOME=/root/.arifos/agents/kimi && \
   /root/.kimi-code/bin/kimi -p "$(cat SPEC.md)" --output-format text
   ```
   Use `terminal(background=true, notify_on_complete=true)`; `process wait` clamps at 180s windows — poll repeatedly until exit.
3. Never trust the self-report: re-run every DoD check yourself (pytest + CLI against real data), then staging → verify → deploy to canonical home → git commit. Each step reversible.

**Pitfall:** compound inline probe one-liners (multiple `grep -E` + `$(...)` composition) can trip the terminal hardline blocklist ("command parser limit"). Split probes into several simple commands, or run the saved script path named in the block message.

### Billing quota exhaustion — fallback to sibling CLIs (2026-08-14)

Kimi Code's provider returns `403 You've reached your usage limit for this billing cycle` with `provider.auth_error`. This is a **hard wall** — no retry, no backoff, no model swap within Kimi helps. The binary boots fine (shows the AAA banner), then fails at the first LLM call.

**Fallback chain for headless SPEC dispatch:**
1. **Kimi Code** (`/root/.kimi-code/bin/kimi -p`) — preferred for TS/ESM (best capability matching)
2. **Qwen Code** (`qwen -p --output-format text`) — GLM-5.2 via z.ai, configured at `~/.qwen/settings.json` with `permissionMode: "yolo"`. Works as direct drop-in for the same SPEC file.
3. **Codex** (`codex -p`) — OpenAI-based, different config surface
4. **Claude Code** (`claude -p`) — Anthropic, highest quality but highest cost

**The SPEC file is CLI-agnostic.** Write one `SPEC.md`, dispatch to whichever CLI has quota. The SPEC already constrains: working dir, input paths, deliverables, Definition of Done. The CLI model doesn't change the task structure.

**Verified 2026-08-14:** Qwen Code (GLM-5.2) successfully executed TWO complex SPECs that Kimi Code couldn't start due to quota: (1) TypeScript apex-scalar-replication (same npm test results), and (2) multi-human H-axis memory architecture under `/root/memory/people/SYED/` — created 10 files, all JSON valid, all markdown correct, ZKPC-compliant. Always probe `kimi --version` + attempt a trivial prompt before committing to a long forge — the 403 appears at call time, not at boot.

**Verified 2026-08-14 (arifOS health handler):** Qwen Code executed a SPEC that patched `/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py` + `arifosmcp/tools/judge.py` — added `degraded_reasons[]`, `layer_health{}`, init token freshness warning, and HIB precedent surfacing (judge.py). 71 insertions, 15 deletions. tsc clean, `curl /health` verified new fields live. Qwen handled the Python+Rust codebase without issue. Scope creep: judge.py precedent surfacing was not in SPEC but was additive and accepted.

### Provider swap — stay in harness, change brain (verified 2026-08-14)

When the kimi-code provider quota is dead, you can **keep the Kimi Code harness alive** (AGI personality, hooks, MCP, agents/) by swapping `default_model` in config.toml to a different provider with quota. This preserves harness identity while changing the backing brain.

**MiniMax-M3 swap (verified working after topup):**
1. Edit `default_model = "minimax-coding-plan/MiniMax-M3"` in config.toml
2. `minimax-coding-plan` provider (type=anthropic, key=`sk-cp-...`) works — auth via standard anthropic header
3. `minimax-direct` provider (type=anthropic, key from `${MINIMAX_API_KEY}` env) **FAILS** — MiniMax API requires `X-Api-Key` header, but kimi-code's anthropic transport sends `Authorization: Bearer` → 401 auth_error
4. **Always use `minimax-coding-plan`, NOT `minimax-direct`, when swapping inside kimi-code harness**
5. MiniMax-M3 has `image_in` + `video_in` + `thinking` + `tool_use` — full AGI capability set preserved

**Coder federation role assignment (F13 2026-08-14):** The adat agentic principle: each CLI carries a primary role but can perform others. Role is anchor, not cage. Current roster: Kimi=AGI, Qwen=ASI, OpenCode=APEX, Aider=ROOT, Codex=Router, Gemini=Review-only. OpenCode `default_agent` switched from `333-AGI` → `888-APEX` in `opencode.json`.

### Provider swap — stay in harness, change brain (verified 2026-08-14)

When the kimi-code provider quota is dead, you can **keep the Kimi Code harness alive** (AGI personality, hooks, MCP, agents/) by swapping `default_model` in config.toml to a different provider with quota. This preserves harness identity (FI-008 333-AGI) while changing the backing brain.

**MiniMax-M3 swap:**
1. Edit `default_model = "minimax-coding-plan/MiniMax-M3"` in config.toml
2. `minimax-coding-plan` provider (type=anthropic, key=`sk-cp-...`) works — auth via standard anthropic header
3. `minimax-direct` provider (type=anthropic, key from `${MINIMAX_API_KEY}` env) **FAILS** — MiniMax API requires `X-Api-Key` header, but kimi-code's anthropic transport sends `Authorization: Bearer` → 401 auth_error
4. **Always use `minimax-coding-plan`, NOT `minimax-direct`, when swapping inside kimi-code harness**
5. MiniMax-M3 has `image_in` + `video_in` + `thinking` + `tool_use` — full AGI capability set preserved

**Gemini video/image API rate limits (verified 2026-08-14):** `gemini-video.py` (Gemini Interactions API) and `gemini-image.py` both hit 429 after ~5-7 rapid calls. Pattern: first 2-3 calls succeed, then hard 429 with exponential backoff retries failing. Cooldown period: ~5-15 minutes. For batch media generation sessions, space calls 60s+ apart or use a cron retry job (`*/5 * * * *`, max 6 retries) with auto-deliver-to-origin on success. Image-to-video NOT supported — `gemini-video.py` is text-to-video only (Interactions API has no image input field).

## `kimi doctor` false-OK — strict vs salvage validation gap (verified 2026-08-14)

**Critical pitfall:** `kimi doctor` can report `OK config.toml` while the config is actually invalid for write-path operations (`kimi login`, any setting change). This is because:

- **`kimi doctor`** uses a **salvage parser** (`salvageConfigData`) that silently drops invalid entries and reports success if ANY valid config emerges.
- **`kimi login`** and config-write operations use **strict validation** (`parseConfigData` → `KimiConfigSchema.parse`) that throws on any validation error.

The error from login is unhelpfully masked: `"Cannot change settings while config.toml is invalid — fix it first (run kimi doctor for details)"` — but `kimi doctor` says it's fine, creating a diagnostic dead end.

**Root cause pattern:** Version upgrades (0.35 → 0.36) can remove enum values or add `.strict()` to sub-schemas. Config written for the old version passes salvage but fails strict. The most common trigger: **hook events removed from `HOOK_EVENT_TYPES` enum** — `HookDefSchema` uses `.strict()`, so an invalid `event` value in any `[[hooks]]` block causes strict failure while being silently dropped by salvage.

**Debugging recipe when doctor says OK but login fails:**

```bash
# 1. Extract the valid HOOK_EVENT_TYPES from the current binary
strings /root/.kimi-code/bin/kimi | grep -A20 'HOOK_EVENT_TYPES\$1 ='

# 2. Compare against events used in config.toml
grep '^event = ' /root/.kimi-code/config.toml | sort -u

# 3. Any event in config NOT in the enum = the culprit
```

**Specific 0.36 breaking change:** `TurnStarted` and `UserPromptQueued` events were removed from `HOOK_EVENT_TYPES`. Config blocks using them must be commented out. The hook scripts themselves (`aaa-turn-classify.sh`, `aaa-danger-warn.sh`) are fine — only the event names were removed upstream.

**General principle:** When debugging "doctor OK / login fails", check in order:
1. Hook events not in the current `HOOK_EVENT_TYPES` enum (most common after upgrades)
2. Unknown keys in `.strict()` schemas (hooks only — other sub-schemas are non-strict)
3. Enum value mismatches (provider `type`, permission `scope`/`decision`, hook `event`)

See `references/kimi-doctor-false-ok-debug.md` for the binary-reverse-engineering technique used to discover this.

## Pitfalls

- **`kimi doctor` false-OK.** Doctor uses salvage (drops bad entries silently); login uses strict (throws on any error). When doctor says OK but login fails, check for removed enum values — especially hook events after version upgrades. See the dedicated section above.
- **Don't assume one model.** Kimi Code is dynamic — `[models.*]` is a registry, not a single config. Diagnose capability mismatch, not "wrong default".
- **TUI banner `Model:` ≠ request-time model.** The banner shows `default_model`; an image-bearing request may route to a different `[models.*]` entry.
- **`mcp.json` script paths are absolute.** Move/rename a launcher script → server dies silently. Validate with `bash <script-path>`.
- **`SYSTEM.md` v2 needs `KIMI_CODE_EXPERIMENTAL_FLAG=1`.** Without that env var, the overlay is partially loaded — agents may see partial identity.
- **Don't assume hooks are still witness-only.** As of 2026-08-07 K-02, Kimi's `aaa-witness-pre.sh` `exit 2`s on destructive patterns — partial enforcement, not witness-only. See Hooks section above.
- **Kimi Code bypasses FED by default.** Don't conflate Kimi's provider list with FED's `hermes-asi` cascade.
- **`always_thinking` models cost more per token** — `kimi-for-coding` and `kimi-for-coding-highspeed` both have it. Use the highspeed variant for short tasks.
- **Don't claim "K-02 sealed" without testing the secrets gap.** Catastrophic patterns exit 2 — confirmed. But `cat /root/.secrets/kunci-mas.env` exits 0 with `permissionDecision: allow`. The hook blocks destruction, not disclosure. Two different invariants.

## References

- `references/config-toml-schema-2026-08-07.md` — full annotated config.toml with all `[models.*]` blocks and capability map for this federation.
- `references/mcp-launchers-and-paths.md` — every launcher script under `mcp-launchers/`, what they wrap, and how to verify each one.
- `references/kimi-hook-enforcement.md` — K-02 hook enforcement table, secrets gap, and 3-step recipe to add patterns.
- `references/kimi-doctor-false-ok-debug.md` — binary-reverse-engineering technique for finding strict-validation failures that `kimi doctor` masks.

## Verification

Smoke test:

```bash
kimi run --model "$(grep default_model /root/.arifos/agents/kimi/config.toml | cut -d'"' -f2)" "Reply with exactly: KIMI_CODE_SMOKE_OK"
```

Success criteria:
- Output contains `KIMI_CODE_SMOKE_OK`
- No `model not found` or `server unavailable` errors in the run log
- MCP servers all respond to `tools/list` probe

## Routing notes (moved from description 2026-10-23)

Covers config.toml structure, capabilities-based model matching (image_in / video_in / thinking / tool_use / always_thinking), main-agent vs sub-agent topology (af-forge / af-explore / af-plan / af-fix / af-coordinator / af-worker / af-reviewer), MCP server launchers, hooks (PreToolUse / PostToolUse / SessionStart / SessionEnd — K-02 patched to exit 2 on destructive patterns, but secrets-disclosure + subagent-spawn + Read tool coverage gaps remain), and the SYSTEM.md v2 overlay (KIMI_CODE_EXPERIMENTAL_FLAG=1). Trigger: Kimi Code TUI boot issues, 'no such model', wrong model selected for the task, agent-invariance questions, MCP launcher script not running, 'K-02 status', hook silently allowed a secrets-path read, or any kimi-config / kimi-code / kimi.json / config.toml under /root/.arifos/agents/kimi/.
