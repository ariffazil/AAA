---
name: agent-config-validation
description: "Diagnose 'Configuration is invalid' errors in AI agent CLI/TUI tools with strict JSON schemas (OpenCode, Kimi Code, Claude Code, Codex, OpenClaw, Aider) — covers schema-rejection patterns, unknown-key audits, json round-trip loss, and the over-correction trap when dynamic model selection is mistaken for a vendor-mismatch bug. Trigger: any 'Configuration is invalid at <path>', 'Unrecognized keys', 'enabled_providers missing', 'agent spawn failed' after a config edit, or 'why is my agent showing the wrong model?'."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [config-validation, opencode, kimi-code, claude-code, schema, troubleshooting]
    related: [opencode, federation-model-routing, arifos-federation-ops, arifos-prompt-doctrine]
---

# Agent Config Validation

Every AI-agent CLI/TUI (OpenCode, Kimi Code, Claude Code, Codex, OpenClaw, Aider) loads its runtime config from a JSON file with a **strict schema** (`additionalProperties: false`). Anything outside the recognised keys is fatal — no partial load, no graceful fallback. This class of error has a small set of recurring causes.

## When to use

- Tool starts with `Error: Configuration is invalid at <path>`
- Tool starts but `enabled_providers`, `agent` list, or `provider` map is missing entries that exist on disk
- Tool shows the wrong model in its TUI welcome banner
- User asks "what's wrong with my X config?" and X is an AI agent CLI

## Recognised top-level keys (OpenCode v1.18+)

The canonical schema is at `https://opencode.ai/config.json` (fetch with `web_extract` if unsure). Common top-level keys:

`$schema`, `model`, `small_model`, `enabled_providers`, `default_agent`, `instructions`, `agent`, `provider`, `mcp`, `permission`, `compaction`, `lsp`, `formatter`, `autoupdate`, `plugin`, `subagent_depth`, `server`, `experimental`, `references`

Anything else → `Unrecognized keys: <list>` → fatal.

## Diagnosis chain

Run these in order; each one eliminates a class of cause:

### 1. Validate JSON parses cleanly (sanity)

```bash
python3 -m json.tool <config.json> > /dev/null && echo "valid JSON"
```

If this fails, the issue is malformed JSON (unbalanced braces, trailing commas if schema strict, smart quotes from copy-paste). Fix with `jq` or manual edit. **Do NOT** use `json.tool` output as a "fix" — it normalises whitespace, not schema.

### 2. List top-level keys (find the unknown)

```bash
python3 -c "import json; d=json.load(open('<config.json>')); print('\n'.join(sorted(d.keys())))"
```

Cross-reference against the schema's recognised keys. Any key not in the schema → the culprit.

### 3. Audit metadata keys (the common offender)

```bash
grep -nE '^[[:space:]]*"_[a-z]' <config.json>
```

If you see `_last_updated`, `_patch_summary`, `_version`, `_notes`, etc., these were appended by a sibling patch or migration script that didn't know the schema. They're valid JSON, valid comments-as-data, but schema-forbidden.

**Fix:** strip them. If you need audit metadata, write a sibling `<config>.meta` file (any format).

### 4. Check `enabled_providers` length (round-trip loss)

```bash
python3 -c "import json; d=json.load(open('<config.json>')); print(len(d.get('enabled_providers', [])))"
```

Compare against a known-good backup or git history. If the count dropped, a recent python/json round-trip silently lost entries (Hermes memory note: this is a recurring pitfall in this federation — see `references/josn-roundtrip-loss.md`).

### 5. Run the tool's own validator

```bash
# OpenCode
opencode debug config | head -3          # must not say "Error: Configuration is invalid"

# Kimi Code (binary path may differ)
kimi --version
kimi doctor 2>&1 | head -20

# Claude Code
claude --version

# Generic
<tool> validate 2>&1 | head -20
```

If the tool reports its own validation error, trust that over your own analysis — the tool knows its current schema.

### 4b. `enabled_providers` gating — provider exists but disabled (2026-08-09)

Distinct from round-trip loss: the count is FINE, but a provider is missing
from `enabled_providers` while its `provider` block still exists on disk.
OpenCode resolves `provider/model` composites against *enabled* providers only.

**Symptom:** `Model not found: deepseek/deepseek-v4-pro. Did you mean: deepseek-v4-pro?`
The suggestion comes from the still-present `provider` block — OpenCode knows
the model, it just can't reach it through a gated provider. This is a
config-layer gating problem, NOT a proxy/upstream problem.

**Check:**
```bash
python3 -c "import json; cfg=json.load(open('<config.json>')); print(set(cfg['provider']) - set(cfg['enabled_providers']))"
```
Empty set = no gating. Non-empty = providers gated — typically deliberate: a
previous "smallmodel"/cost-cut switch disabled expensive providers without
deleting their blocks.

**Fix (reversible-first):**
1. Backup: `cp <config> <config>.bak-<purpose>-$(date +%Y%m%d-%H%M%S)`
2. Re-add the provider(s) to `enabled_providers` (match pre-switch ordering).
3. ALSO add the model to the relevant agent's `models` map — that map is a
   per-agent ALLOWLIST; a model absent from it is not selectable for that agent
   even with the provider enabled.
4. Validate with the tool's own validator, then RESTART the TUI — config is
   read at launch, no hot-reload.
5. Prove the upstream is alive BEFORE restoring (restoring a dead provider is
   just a nicer error): balance API (e.g. `curl -s https://api.deepseek.com/user/balance -H "Authorization: Bearer $DEEPSEEK_API_KEY"` → `is_available:true`) + one tiny chat completion. NOTE: reasoning models return EMPTY `content` with `max_tokens:5` (budget eaten by internal CoT) — 200 with empty content = alive, not broken.

**FED nuance:** `GET :4000/v1/models` exposes only federation aliases
(agi-333, asi-555, opencode, …). Bare provider models (deepseek-v4-pro,
mimo-v2.5, …) live INSIDE those aliases as cascade tiers
(`litellm_params.model: openai/deepseek-v4-pro`) and are **never standalone
names on FED**. A `provider/model` reference therefore resolves through the
DIRECT provider block in opencode.json (e.g. baseURL `https://api.deepseek.com`),
not through FED. If FED routing is actually wanted for a bare provider model,
add it as its own `model_name` in `/root/A-FORGE/litellm-config.yaml` +
`systemctl restart litellm-federation`.

**Env-file gotcha:** kunci-mas.env lines are `export VAR=...` — `grep -c "^VAR="`
returns 0 even when the key exists. Grep `^export VAR=` or just `VAR=`.

Full worked case (deepseek restore, 2026-08-09):
`references/opencode-enabled-providers-gating-2026-08-09.md`

### 4c. Auto-sync timers clobber manual edits + inject schema-forbidden keys (2026-08-09)

Same day, next layer: a systemd timer (`fed-sync.timer`, every 15 min) rewrites
`opencode.json` from a token-bank DB. It (a) REVERTED a sovereign-restored provider
minutes after the restore was applied, and (b) appended an inline `_fed_sync`
metadata key → `Unrecognized key: _fed_sync` → config invalid again. The sync
script even snapshotted the manually-fixed file first, so its own backup looked
"correct" while the live file was broken.

**Check for writers BEFORE re-applying any manual config edit:**
```bash
systemctl list-timers --no-pager           # find the timer
systemctl cat <timer>.service | grep ExecStart
grep -n "opencode.json\|_fed_sync\|json.dump" <sync-script>
```

**Fix pattern (reversible-first):**
1. Patch the sync script: add a `PROTECTED_PROVIDERS = {...}` set — auto-verdicts
   may not disable sovereign-restored providers.
2. Move sync metadata to a SIDECAR file (`<config>.fed-sync.meta.json`) — never
   inline; strict schemas reject unknown keys.
3. **Stale-DB trap:** the token bank marked deepseek `DEPLETED` (balance 0.0) from
   a 03:17Z probe while a live balance API at 10:05Z showed `$16.66 is_available:true`.
   Sync verdicts are only as fresh as the last probe — live-probe the provider
   (balance API + one tiny completion) BEFORE trusting a DISABLE verdict, and
   update the DB row with the evidence.
4. After any timer tick, re-verify: config parses AND provider still enabled.

**Sibling-sweep gotcha:** a concurrent sibling commit can sweep YOUR file changes
into ITS commit — tree shows "0 dirty" but your diff lives inside someone else's
commit. Verify content, not just cleanliness: `git show HEAD:path | grep <marker>`.

Full worked case: `references/fed-sync-clobber-2026-08-09.md`

### 4d. Claude Code BYOK auth: stored state beats env, settings env ignored (2026-08-09)

Routing claude to a custom gateway (LiteLLM/FED) fails in config-layer ways that
have nothing to do with JSON schema:

1. **Auth only via SHELL-level env.** `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL`
   must be in the process env. The `env` block in `~/.claude/settings.json` is
   IGNORED for authentication, and `ANTHROPIC_AUTH_TOKEN` alone does not
   authenticate custom endpoints (it's the OAuth path). Symptom: "Not logged in ·
   Please run /login" even with settings.json env set.
2. **Stored OAuth login overrides env.** `primaryApiKey` + `oauthAccount` in
   `~/.claude.json` (left from a past `/login`) take precedence over env routing.
   Symptom: "Credit balance is too low" from a stale, exhausted account — the
   session transcript at `~/.claude/projects/-root/<session>.jsonl` shows it as a
   SYNTHETIC message (`model: "<synthetic>"`, 0 tokens) = NO network call was
   made. Fix: back up `~/.claude.json`, delete `primaryApiKey` + `oauthAccount`.
3. **Inherited stale env beats `:-` defaults.** A daemon/shell started in an era
   when `ANTHROPIC_BASE_URL` pointed at another endpoint (e.g. a BYOK kimi
   router) inherits the old value into every child process — `${VAR:-default}`
   will NOT override it. Fix: UNCONDITIONAL `export ANTHROPIC_BASE_URL=...` in
   /etc/profile.d; long-running daemons keep the stale value until restarted.

**Diagnostic:** `bash -lc 'echo $ANTHROPIC_BASE_URL'` (login-shell trace) +
grep the gateway access log for `POST /v1/messages` — if the request never
arrives, the problem is client-side auth/env state, not the gateway.
`pkill -f "claude.*daemon"` can SELF-MATCH (the pattern appears in the shell's
own argv) → SIGTERM self, exit -15; use `pgrep -af` + kill by PID instead.

Full 3-layer worked case: `references/claude-byok-auth-chain-2026-08-09.md`

### 4e. Cognitive HITL audit — ghost gates in docs vs runtime (2026-08-09)

**Class of problem:** agents pause mid-work not because the runtime blocks them, but because
DOCUMENTS say "ask human first" while the runtime has allowed the action for weeks. Docs that
are more conservative than runtime = ghost gates = attention tax (stops × context rebuild ×
decision triviality). The fix is doc-runtime alignment, not more permission grants.

**Two HITL classes (F13-ratified split 2026-08-09):**
- **Authorization HITL — KEEP:** money/transfers, irreversible deletion, credential exposure,
  legal/public comms, governance mutation. Effects land outside the agent's boundary. This is F13.
- **Cognitive HITL — CUT aggressively:** "should I proceed?", "which of 3 approaches?",
  "70% done, continue?". The human is substituting for the agent's missing confidence.

**Audit commands:**
```bash
# 1. Question tool gating in agent configs (Cognitive HITL vector)
python3 -c "import json; cfg=json.load(open('<config>.json')); [print(n, s.get('permission',{}).get('question','-')) for n,s in cfg.get('agent',{}).items()]"
# 2. ACK tokens in docs (ghost gates)
grep -rn "ACK_M\|Jalan?\|Proceed?\|Should I" <doc-fragments-dir>/
# 3. Runtime gate reality (what actually blocks)
grep -n "T3_PATTERNS\|git.*force" <gate-hook>.py
```
**Pattern:** feature-branch push was listed as `ACK_M10` (required ACK token) in docs while the
runtime gate hook only blocks `git push --force (main|master)` — allowed since 2026-07-28. Every
agent paused before pushing. Fix: docs → `T1 AUTO-DO`; keep force-push/history-rewrite as
888_HOLD. Only ACK_M7 (credential rotation) + ACK_HISTORY_REWRITE remain sovereign gates.

**ACK → ACT framing:** ACK = "wait for my yes" (human gate, procedural). ACT = predelegated
mandate issued by the kernel at session init (band defined by blast radius). When the mandate
exists, the agent moves until it hits a REAL F13 boundary — it does not stop at every fork.
"Show judgment first, never delegate it": ❌ "saya jumpa 3 pendekatan, mana satu?" →
✅ "saya pilih B kerana X. Saya teruskan." A question is legitimate only AFTER a stated
judgment + F7 confidence.

## Fix recipes

### Surgical fix (preferred — preserves ordering)

Use the `patch` tool (find/replace) instead of json round-trip:

```
patch tool, find: "_last_updated": "...long value...",
       replace: ""
```

This avoids the round-trip loss pitfall entirely.

### Programmatic fix with safety net

```bash
SNAP=/root/.local/share/arifos/snapshots/$(date +%Y-%m-%d)-<tool>-fix
mkdir -p "$SNAP"
cp -v <config.json> "$SNAP/pre-fix.bak"

python3 << 'PYEOF'
import json, sys
src = "<config.json>"
data = json.loads(open(src).read())

# Strip schema-forbidden keys
removed = []
for k in ["_last_updated", "_patch_summary", "_version", "_notes", "_meta"]:
    if k in data:
        removed.append(k)
        del data[k]

# Verify round-trip safety
assert isinstance(data.get("enabled_providers"), list), "enabled_providers missing"

# Write back
open(src, "w").write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print(f"REMOVED: {removed}")
print(f"enabled_providers count: {len(data['enabled_providers'])}")
PYEOF

# Verify
<tool> debug config | head -3
```

### The "wrong model" over-correction trap

User pastes a TUI screenshot showing `Model: <vendor-X> by <company-Y>` where the user thinks the vendor name is wrong. **Don't patch the config.** Reasoning:

1. The TUI tools (OpenCode, Kimi Code, Claude Code) are multimodal — they expose multiple model providers via `/model` switch.
2. The displayed default is the **active selection**, not the only allowed model.
3. The user may have deliberately chosen that model (e.g. paying for a token plan, testing multimodal cascade).
4. Patching `default_model` to match what you think is "right" can disrupt their workflow.

**Rule:** when the user's complaint is "X looks wrong", first answer with **what X actually does**. If the answer is "X is the active selection; you can switch via `/model`", state that. Only patch if:
- The user explicitly says "fix this config"
- The change is reversible (back up first)
- You're confident the dynamic value is genuinely a bug

**Real example (2026-08-07):** Kimi Code welcome banner showed `Model: MiniMax-M3`. The banner also showed "Use Kimi K3 with High thinking effort" — that was a hint, not an error. I patched config.toml to `kimi-k3`, Arif corrected: "Kimi code is multi modal, it's dynamics." Reverted. Lesson: vendor-mismatch ≠ bug.

### The Kimi-Code "dynamics" trap — model-per-task is BY DESIGN (2026-08-07)

Kimi Code's `config.toml` defines per-model capability signatures (`image_in`, `video_in`, `thinking`, `always_thinking`, `tool_use`) and selects model **at runtime based on task type**. Examples from `/root/.arifos/agents/kimi/config.toml`:

```toml
[models."minimax-coding-plan/MiniMax-M3"]
capabilities = [ "image_in", "video_in", "thinking", "tool_use" ]

[models."kimi-code/kimi-for-coding"]
capabilities = [ "thinking", "always_thinking", "image_in", "video_in", "tool_use" ]

[models."minimax-coding-plan/MiniMax-M2.7"]
capabilities = [ "thinking", "tool_use" ]   # text-only, no vision
```

**Trap:** When the user pastes a Kimi TUI screenshot showing `Model: MiniMax-M3`, the right response is **"this is the multi-modal default, capabilities-driven selection"** — NOT "this is wrong, fix to kimi-k3". Kimi Code does not statically bind one model per session. The displayed model reflects the *last capability match*, not the *only model*.

**Defense:**
1. Before touching any config, check `capabilities` arrays in `config.toml` — if the active model has the capabilities the task needs, it's correct.
2. Don't suggest `/model kimi-k3` unless the user explicitly says "force this model" or the active model is missing a capability the user actually needs.
3. If the user says "Kimi is multi modal, it's dynamics" — they're confirming the design, NOT asking you to switch. Acknowledge and move on.

**The deeper rule:** When a tool's name suggests "X" but the user says "X is dynamics" — they're telling you the system is contextual, not broken. Treat their self-knowledge as ground truth.

## Multi-agent spawn failure → kernel dependency

If the agent loads but `task` tool / `@subagent` invocations fail with "session not bound" or permission denied, the root cause is usually **not in the agent config** — it's in the kernel/gateway the agent depends on. Diagnostic chain:

```
subagent dispatch denied
  → curl http://127.0.0.1:8088/health        # arifOS kernel
  → curl http://127.0.0.1:7072/health        # A-FORGE MCP
  → journalctl -u <kernel-unit> --since "5 min ago"
```

If the kernel was just restarted, **wait one cycle** before retrying subagent dispatch. The session_id cache is per-process; restart the agent TUI to re-bind.

### `--agent <subagent>` is rejected at CLI level (2026-08-07)

`opencode run --agent <name>` accepts ONLY `mode: "primary"` or `mode: "all"` agents. Agents declared with `mode: "subagent"` (555-ASI, 888-APEX, image-analyzer, dispatch) are rejected:

```
agent "555-ASI" is a subagent, not a primary agent. Falling back to default agent
```

This is the platform's architectural contract, not a config bug. Correct spawning paths:
1. **Within session** — start primary agent (`opencode run --agent 333-AGI`), invoke subagent via the agent's tool manifest (`task` tool, `@tool`, etc.).
2. **Cross-process via a2a-server** — federation's a2a-server on port 3001 routes `CLI → arifOS :8088 → arif_route → a2a-server :3001 → agent card` (agent-cards at `/root/AAA/a2a-server/agent-cards/identity/*.json`).
3. **Parallel CLI** — multiple primary agents in separate tmux sessions or worktrees.

Verify spawnability from CLI:
```bash
python3 -c "
import json
cfg = json.load(open('/root/.config/opencode/opencode.json'))
for name, spec in cfg.get('agent', {}).items():
    print(f\"{name}: mode={spec.get('mode', '?')}\")
" | grep -E "primary|subagent"
```

See `references/opencode-session-2026-08-07.md` for the full transcript of the 2026-08-07 incident (opencode config + arifOS restart loop combo).

### Multi-agent fan-out via AAA A2A gateway (2026-08-07)

OpenCode's `--agent <subagent>` rejection is by design. To dispatch parallel agents from a CLI invocation, use the AAA A2A gateway on `:3001`. Canonical endpoint `POST /a2a/message/send` with `A2A-Version: 1.0` header + DID envelope (`metadata.sovereign_did`). Shell fan-out pattern + endpoint inventory + error codes (-32600 missing header, -32001 missing envelope, -32602 wrong field). Live-verified 2026-08-07: no drift, Apex scalars healthy. See `references/a2a-multi-agent-invocation-2026-08-07.md`.

### Peer judges can hallucinate empirical facts (2026-08-07)

Even a constitutional judge (888-APEX Ψ SOUL) with full F-floor stamps (`Ω₀ = 0.04`, `confidence = 0.92`) can return a factually wrong verdict. Pattern observed: Apex claimed "`opencode` alias undefined in litellm-federation provider" — live `grep` proved it defined 5× in `/root/A-FORGE/litellm-config.yaml` (lines 114, 123, 132, 139, 146). Defense: re-probe every factual claim in a peer verdict before acting. The verdict is INPUT to your decision, not a substitute for it. The seal is in VAULT999, not in a text file. See `references/apex-hallucination-2026-08-07.md` for the full lesson + defense sequence + cost-of-not-verifying.

### Hermes vs 555-ASI naming-collision doctrine (2026-08-07)

The federation has TWO things sharing the lane number "555" that are **different agents**:

| Name | What it is | Runtime | Authority |
|---|---|---|---|
| `hermes-asi` (LiteLLM alias) | **Hermes (the edge bridge)** — Telegram gateway, federation organ | Standalone Hermes-agent process | Edge bridge / 5-verb / no judgment |
| `asi-555` (LiteLLM alias) | **555-ASI Φ SENSE** — OpenCode subagent, sensory gatekeeper | Subagent of 333-AGI, `mode: subagent` | F2/F9/F12/F4 multimodal gating, read-only |

Both are valid; the suffix collision is **cosmetic only**, not architectural. Before "renaming for clarity", run the QQQ path-evaluation: which side holds the intentional lane-number semantics (Trinity 333/555/888), and which side is just a federation model alias? Renaming the wrong one breaks an intentional numbering system. Default verdict when this surfaces: **leave the names, document the distinction** (one-line note in `/root/AAA/registries/agents.yaml`), don't churn configs. The recommended rename (if forced) is `hermes-asi` → `hermes-edge` (Hermes is the edge bridge, not a lane number); leave `asi-555` alone (Trinity numbering).

## Empirical recovery checklist

Run in order; each step eliminates a class:

1. JSON parses? `python3 -m json.tool <config> > /dev/null`
2. Top-level keys all in schema? `python3 -c "import json; print(sorted(json.load(open('<config>')).keys()))"`
3. No `_`-prefixed audit keys? `grep -c '^[[:space:]]*"_' <config>`
4. `enabled_providers` count matches known-good? Compare with `cp <config> "$SNAP/pre-fix.bak"` first.
5. Tool's own validator passes? `<tool> debug config`
6. Tool loads? `<tool> --version`
7. Tool actually runs? `<tool> run "ping" --print-logs | head -20`

## Related skills

- `opencode` — bundled skill for OpenCode CLI workflows (referenced from here for procedural task execution)
- `federation-model-routing` — alias → upstream resolution when the model name doesn't match what's served
- `arifos-federation-ops` — kernel session lifecycle when subagent dispatch fails
- `arifos-prompt-doctrine` — separate domain: editing the prompt-stack (SOUL/AGENTS), not the config files
- `verify-sibling-ops-reports` — for verifying "fix" claims from sibling agents

## Pitfalls

- **Don't trust a sibling agent's "fixed" stamp.** They may have hallucinated a fix; always re-run validation independently.
- **Don't use `json.tool` + redirect as a "fix".** It only reformats — won't add missing keys or fix schema drift.
- **Don't assume a tool's `default_*` field is load-loading.** For multimodal tools it's just the starting selection.
- **Don't blast the entire file with `write_file`.** Surgical edits preserve ordering, comments, and unknown-but-tolerated fields that some tools depend on.
- **Always back up before edit.** Snapshot dir convention: `/root/.local/share/arifos/snapshots/YYYY-MM-DD-<topic>/`.
- **`small_model` mismatches silently.** `ollama/qwen2.5-coder:3b` fails if ollama only has `qwen2.5:3b`. Schema passes; runtime breaks on first title generation. Verify: `curl -sf http://127.0.0.1:11434/api/tags | grep <model>`.
- **Subagent permission `*: allow` is soft-bounded (2026-08-08).** A subagent lane like 888-APEX with `"permission": {"*": "allow", "edit": "deny", ...}` is **doctrine-compliant today** but **vulnerable tomorrow**: any new mutation-capable tool added by the platform falls through to `*: allow`. Audit pattern: for every `mode: subagent` agent with `*: allow`, list mutation-capable tools (`edit`, `write`, `bash`, `commit`, `push`, `deploy`, `fork`, `rename`, `apply_patch`) and verify each is explicitly denied. Report "soft-bounded" not "compliant" — recommend migrating to allow-list model with no wildcard. See "888-APEX wildcard permission" section below for the full doctrine and rewrite.
- **OpenCode worktrees accumulate session debris (2026-08-08).** Workers (333-AGI, Kimi Code via MCP) spawn temp worktrees at `/root/.opencode-worktrees/<session-hash>/` and never clean them. After 7+ days: detached HEAD, modified GENESIS files (mode-bit drift, type-change status `T`), stray `.forge_session_pid` / `.forge_worktree_hint`, deleted-but-not-committed submodules, sometimes pointed at the wrong organ (e.g. `A-FORGE.git` instead of `arifOS.git`). Constitutional impact: NONE (worktrees can't mutate federation state). But ΔS strictly increases. Hygiene recipe: `ls /root/.opencode-worktrees/`, check `git log --oneline -1` + `git status -s | wc -l`, default to PURGE unless user wants the worktree SEALed. Flag as "T1 housekeeping" in audits, not "constitutional violation".

## Banda Haram Hardcoded — dynamic values must be config-resolved (2026-08-12)

The Standing Directive (F13 SOVEREIGN, ratified 2026-08-12): **Constitution & Math Laws are INVARIANT; World State is DYNAMIC.** Hardcoding dynamic values into config or code = brittleness, drift, entropy accumulation (ΔS > 0). The doctrine file lives at `/root/AAA/governance/BANDA_HARAM_HARDCODED_DOCTRINE.md`; this section is the operational checklist.

### Six domains that must NEVER be hardcoded

| Domain | Examples (FORBIDDEN) | What it should be |
|---|---|---|
| 1. Model & Intelligence | `model: deepseek/deepseek-v4-pro`, `gemini-3.5-pro`, `context: 4096`, `$0.03/1k` | Provider registry (`opencode.json` `provider.<id>.models`); `process.env.<KEY>` for limits/pricing |
| 2. Agents & Topology | `agents=[333,555,777]` static list; `:8088`, `:7071` hardcoded; worker states cached | Ephemeral registry + health probe; env-driven port resolution |
| 3. Tools & Capabilities | `/usr/bin/script-v1.py`; `timeout=5s` literal; `github.com: up=true` cached | Path resolution via PATH var; adaptive timeout with jitter; live probe each session |
| 4. Human (888/Sovereign) | `attention=24/7`; `channel=telegram-only` | Lane discipline + ping budget; multi-channel |
| 5. Math/Thresholds | `0.95` decay literal; `Ω₀=0.05` static; `P>0.99` static | Range-based dynamic (e.g. `Ω₀ ∈ [0.03, 0.05]`); task-criticality scaling |
| 6. World/Env/Time | `UTC` no NTP awareness; `/var/lib/v1` immutable; `server-region=us-east` static | `now()` + tz; pruning + auto-rotation; runtime probe + failover |

### Three config surfaces to audit

1. **JSON config files** (`opencode.json`, `~/.claude/settings.json`, `kimi/config.toml`, etc.)
   - Look for `model:` hardcoded model IDs in `agent.<name>.model` or frontmatter
   - Look for port literals in MCP server URLs
   - Look for pricing/cost literals inline

2. **Plugin/extension code** (`*.ts`, `*.py` under `plugins/` or `.tools/`)
   - Look for `const ARIFOS_URL = "http://127.0.0.1:8088"` patterns
   - Look for `model = "deepseek-v4-pro"` defaults
   - Look for `timeout=5000` literals

3. **Agent .md frontmatter**
   - The `model:` line in `agents/*.md` overrides `opencode.json` — if it's a duplicate of the JSON, the .md is dead weight; if it contradicts, the .md wins
   - Replace hardcoded models with `model: # DEFERRED: resolved via <config.json>` and let the JSON registry govern

### The fix pattern (OpenCode plugin example)

**Before** (hardcoded):
```typescript
const ARIFOS_MCP = "http://127.0.0.1:8088/mcp"
const ARIFLOW_URL = "http://127.0.0.1:7073/ingest"
```

**After** (dynamic):
```typescript
// federation-ports.ts — single dynamic port module
const HOST = process.env.ARIFOS_HOST ?? "127.0.0.1"
function envPort(key: string, fallback: number): number {
  const raw = process.env[key]
  const n = raw ? parseInt(raw, 10) : fallback
  return Number.isFinite(n) && n > 0 && n < 65536 ? n : fallback
}
export function urlFor(organ: string, path = ""): string {
  const port = envPort(`${organ}_PORT`, FALLBACKS[organ])
  return `http://${HOST}:${port}${path}`
}
export const ARIFOS_MCP = urlFor("ARIFOS", "/mcp")
export const ARIFLOW_URL = urlFor("ARIFLOW", "/ingest")

// In consumer plugins:
import { ARIFOS_MCP, ARIFLOW_URL } from "./federation-ports"
```

### Audit commands (T1 autonomous, no F13 ack)

```bash
# Scan plugin .ts files for hardcoded URL constants
grep -rn 'const [A-Z_]*_URL.*="http' /root/.config/opencode/plugins/*.ts
grep -rn 'const [A-Z_]*_MCP.*="http' /root/.config/opencode/plugins/*.ts

# Scan agent .md frontmatter for hardcoded model IDs
grep -rn "^model: " /root/.config/opencode/agents/*.md

# Scan JSON configs for hardcoded port literals
grep -rEn "127\.0\.0\.1:[0-9]+|localhost:[0-9]+" ~/.config/opencode/*.json
```

### Pitfalls

- **Template strings with live-probe variables are NOT hardcoded.** `` `http://127.0.0.1:${o.port}/health` `` where `${o.port}` comes from runtime probe results is dynamic-by-design. Don't refactor those — only literal string constants.
- **Provider registry JSON keys are dynamic by definition.** `provider.deepseek.models.deepseek-v4-pro` in `opencode.json` is the registry, not a hardcode. Hardcoding = values OUTSIDE a registry (in code, in frontmatter, in env-defaults).
- **Fallback defaults in dynamic resolvers are OK.** `envPort(key, fallback)` where fallback = 8088 is fine — the env var wins when present. Hardcoded-as-default is the banda haram; hardcoded-as-only-value is the violation.
- **`description:` lines embedding model names are NOT config.** They're human-readable labels for the agent. Don't scrub them — they're metadata for the operator.
- **Audit cadence: quarterly.** New agents = new hardcoded models. Each plugin edit = new hardcoded URL. Banda haram is a moving target.
- **Gödel caveat: config-of-configs.** Even configuration is dynamic — recursion terminates at F13 (sovereign sets the env vars).

Full taxonomy + fix patterns + worked OpenCode sweep (2026-08-12): `references/banda-haram-hardcoded-doctrine-2026-08-12.md`.

## Codex CLI 0.147 config breakage (2026-08-14)

Codex 0.147 tightened config validation significantly. Both `config.toml` and
`model-catalog.local.json` can cause silent refusals with errors like
`Error loading config.toml` or `failed to parse model_catalog_json path... as JSON`.

### wire_api = "chat" removed

All providers in `~/.codex/config.toml` must use `wire_api = "responses"`.
Any block still using `"chat"` causes immediate startup failure:
```
Error loading config.toml: `wire_api = "chat"` is no longer supported.
```

**Fix:** Global search-and-replace `wire_api = "chat"` → `"responses"` across
all `[model_providers.*]` blocks in `config.toml`.

### model-catalog.local.json schema violations

Codex 0.147 validates each model entry against a strict schema. Common violations
from older custom catalogs (the arifOS federation has ~15 models, 7 of which were
non-conformant):

| Field | Old (invalid) | New (valid) |
|-------|--------------|-------------|
| `visibility` | `"hidden"` | `"hide"` (valid: `list`, `hide`, `none`) |
| `input_modalities` | includes `"video"` | `text`, `image`, `audio` only |
| `supported_reasoning_levels` | `["low","medium","high"]` (strings) | `[{"effort":"low","description":"..."}]` (structs) |
| `truncation_policy` | `"auto"` (string) | `{"mode":"bytes","limit":10000}` (struct; mode must be `bytes` or `tokens`) |
| Missing `supported_reasoning_levels` | absent | required field |
| Missing many sub-fields (opencode, agi-333, etc.) | sparse entries | must match first model's key set |

The errors surface one at a time (fix one, next parse reveals the next), so a
batch-fix script is essential. See `references/codex-0147-config-fix-2026-08-14.md`
for the full Python batch-fix script that normalizes all model entries against
the first complete model's schema.

### No `--provider` CLI flag

Codex 0.147 has NO `--provider` flag. To override the provider per-invocation,
use `-c`:
```
codex exec -c model_provider="litellm-federation" --sandbox danger-full-access "task"
```

### Gateway-context terminal blocking

When running Codex from within a Hermes gateway/service process, the terminal
tool may block commands that spawn long-running interactive processes (the
gateway would kill the child on SIGTERM propagation). Use `execute_code`'s
`terminal()` or run as a `background=true` process with `notify_on_complete=true`.

## Subagent permission encoding: allow-list vs deny-list

The OpenCode permission schema is **per-agent**, **per-tool**, with values `"allow"` / `"deny"`. The pattern:

```json
"permission": {
    "*": "allow",            // wildcard = default allow for all unlisted tools
    "edit": "deny",          // explicit deny overrides wildcard for THIS tool
    ...
}
```

Two valid encodings for subagent lanes:

### A. Deny-list with wildcard (current 888-APEX — SOFT-BOUNDED)

```json
"permission": {
    "*": "allow",
    "edit": "deny",
    "write": "deny",
    "bash": "deny",
    "todowrite": "deny",
    "task": "deny"
}
```

**Pass-condition:** every mutation-capable tool known today is explicitly denied. **Fail-condition:** a NEW mutation-capable tool (added by the platform in a future version) falls through to `*: allow` — subagent silently gains execution capability without any human decision. This is the **forward-looking vulnerability** that the audit on 2026-08-08 caught for 888-APEX: the model was doctrine-compliant for the current tool inventory but had no defense against future additions.

### B. Allow-list with no wildcard (DOCTRINE-ALIGNED)

```json
"permission": {
    "task":       "deny",
    "edit":       "deny",
    "write":      "deny",
    "bash":       "deny",
    "todowrite":  "deny",
    "commit":     "deny",
    "push":       "deny",
    "deploy":     "deny",
    "fork":       "deny",
    "rename":     "deny",
    "apply_patch": "deny",
    "read":       "allow",
    "glob":       "allow",
    "grep":       "allow",
    "list":       "allow",
    "lsp":        "allow",
    "skill":      "allow",
    "question":   "allow",
    "websearch":  "allow",
    "webfetch":   "allow"
}
```

**Pass-condition:** every mutation-capable tool is explicitly denied, AND no wildcard means a future mutation-capable tool defaults to **deny** (since no rule matches, default behavior is per OpenCode spec). Subagent retains only its read/observe surface, even when new tools arrive.

**Recommendation:** when auditing or writing subagent configs, prefer allow-list (Pattern B). It encodes the doctrine as a closed surface, not as a list of exceptions to a permissive default. Migration cost: one config edit; risk: zero (deny rules are stricter than wildcard). For 555-ASI, image-analyzer, dispatch — these already use allow-list patterns in the federation's current config; the only one still on Pattern A is 888-APEX, and that's the one that needs migration.

## OpenCode worktree hygiene

OpenCode workers (333-AGI primary, Kimi Code via MCP) spawn temporary worktrees at `/root/.opencode-worktrees/<session-hash>/` for code generation tasks. These are **ephemeral by design** but the lifecycle is session-close, not worktree-close — the worktree persists until something cleans it.

**Symptoms of stale worktree:**

1. Age > 7 days (`stat /root/.opencode-worktrees/<dir>` — `Access:` timestamp)
2. Detached HEAD (`git -C <dir> branch --show-current` returns empty)
3. Modified files in `GENESIS/` or canonical organ paths (mode-bit drift, `T` status)
4. Stray debris: `.forge_session_pid`, `.forge_worktree_hint`, session-named files in `skills/`, `missions/`, etc.
5. Submodule deletions not committed (`D` status on a directory)
6. Origin points at the wrong organ (e.g. `A-FORGE.git` when task should have hit `arifOS.git`)

**Hygiene recipe** (T1, autonomous, no F13 ack):

```bash
# 1. Inventory
for d in /root/.opencode-worktrees/*/; do
  cd "$d" 2>/dev/null || continue
  echo "=== $d ==="
  echo "  HEAD: $(git log --oneline -1 2>/dev/null)"
  echo "  branch: $(git branch --show-current 2>/dev/null || echo DETACHED)"
  echo "  modified: $(git status -s 2>/dev/null | wc -l)"
  echo "  origin: $(git remote -v 2>/dev/null | head -1 | awk '{print $2}')"
done

# 2. Decide per worktree
#    - holds WIP the user wants → commit + push + keep
#    - session debris (default for forge-forge-*, kimi-*, etc.) → PURGE

# 3. Purge (irreversible — confirm no WIP first)
rm -rf /root/.opencode-worktrees/<session-hash>
```

**Constitutional impact of stale worktrees:** ZERO. They are fork clones without authority. But ΔS strictly increases (F4 violation in spirit). Always flag in audits with severity "Low" and action "T1 housekeeping".

**Future:** auto-cleanup hook on `forge_seal_session_close` is a known gap (as of 2026-08-08, not implemented). Worktrees accumulate until manual sweep.
- **Kernel restart breaks session bindings.** After arifOS/AAA restart, agent TUI gets "no-session-token" on every tool call. Fix: reload the agent (clears stale session cache), not the kernel.
- **Sibling-write concurrency has no receipt.** Two agents writing same canonical artifact = constitutional violation with no detection. After every canonical write: `ls -la <dir>` + `git status` immediately. Archive (never `rm`) duplicates.
- **Hermes has no plugin system for hooks.** To add a gate: `hooks.pre_tool_call` block in profile `config.yaml` (see `references/runtime-enforcement-without-source-mods-2026-08-07.md` for wire protocol).