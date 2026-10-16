# Claude Code FI-002 Shadow Audit — 2026-10-15

Auditor: kimi-code / FI-008 · Node KVM8 · Sovereign directive: Arif Fazil (F13)
Scope: Claude Code's CONTEXT LAYER ONLY. arifOS kernel + all organ code untouched.
Backup of every touched file: `/root/.claude-backup-20261015T145447Z/`

---

## 1. LIVE PROBE (all numbers copied from a probe, not from a plan)

### 1.1 Install
| Item | Probed value |
|---|---|
| CLI version before | 2.1.278 |
| CLI version after | **2.1.300** |
| `which claude` | `/root/.local/bin/claude` |
| resolved binary | `/root/.local/share/claude/versions/2.1.300` |
| install method (`.claude.json`) | `native` |
| rollback available | `/root/.local/share/claude/versions/2.1.278` |

### 1.2 Federation `:port/health` — 8/8 answered
| Port | HTTP | Body head |
|---|---|---|
| 8088 | 200 | `healthy`, `floors_active: 13` |
| 7071 | 200 | `A-FORGE-sense`, `degraded_mode: false` |
| 3001 | 200 | **`degraded`** |
| 8081 | 200 | `healthy`, `kernel_verdict: HOLD` |
| 18082 | 200 | `healthy` |
| 18083 | 200 | **`degraded`**, commit drift `false` |
| 7073 | 200 | `HEURISTIC_ADVISORY` |
| 7074 | 200 | `healthy`, `FED` |

### 1.3 Live MCP `tools/list` per server (the only counts this audit trusts)
| Server | Port | Tools | Transport |
|---|---|---|---|
| arifos | 8088 | 8 | stateless http |
| aforge | 7072 | 122 | stateless http |
| aforge-sense | 7071 | 122 | sessioned http |
| geox | 8081 | 27 | sessioned http |
| wealth | 18082 | 18 | sessioned http |
| well | 18083 | 10 | sessioned http |
| fed | 7074 | 7 | sessioned http |
| frame | 18086 | 8 | sessioned http |
| hermes | 18087 | 15 | sessioned http |
| **TOTAL** | | **337** | |

Non-live surfaces (configured but not probed this pass): `chron` (remote), `deepwiki`
(remote), `zai-*` (remote), `firecrawl` (remote, project `.mcp.json`), `xerj` (stdio,
`:9300` root returns 200), `github`/`serena`/`repomapper`/`aforge-compressed`/`arifflow`/`MiniMax`
(stdio launchers). **No configured local HTTP server was dead** — nothing had to be removed.

### 1.4 Configured server counts (live)
`/root/.claude/settings.json` → **21** · project `/root/.mcp.json` → **2** · total **23**.

---

## 2. CLASSIFIED FINDINGS

| # | Tag | Location (file:line) | Finding | Action taken |
|---|---|---|---|---|
| 1 | **PHANTOM** | always-on context (absence of a roster) | Claude Code called `mcp__claude_ai_GitHub__get_file`. Probe root cause: every `claude -p` run prints `claude.ai connectors are disabled` — the `mcp__claude_ai_*` namespace is **structurally unavailable**, so any name in it is guaranteed phantom. There was no live tool roster in context to ground naming. | Added **TOOL TRUTH** block to `/root/.claude/CLAUDE.md` listing all 17 real prefixes and forbidding `mcp__claude_ai_*` outright. |
| 2 | **CONTRADICTION** | `/root/.claude/CLAUDE.md:35` (old) vs probe | Old map said `A-FORGE :8088 (execution)`. Probe: **8088 is arifOS**; A-FORGE sense is **7071**, gateway **7072**. Two ports given one owner. | Federation map replaced with **pointers to systemd**, zero hardcoded ports. |
| 3 | **CONTRADICTION** | `/root/CLAUDE.md:12` (old) vs `/root/.claude/CLAUDE.md` | Old file ordered "when unsure HOW → run musyawarah (333 ARCHITECT + 555 AUDITOR) → let them pick". New directive: *"Never ask another agent to decide."* Directly opposed. | Removed. Reversible path is now the rule. |
| 4 | **ASK-TRIGGER** | `settings.json` → `hooks.PostToolUse[0].hooks[1]` → `f2-receipt-citation.py` | Reads `/root/.arifos/agents/shared/f2-receipt-citation.py:145`. After every T3/W_SCAR mutation it **injects** `[F2 RECEIPT CITATION] ... cite receipt path in next response` into the turn. This is the mechanism behind "receipts printed in chat", which is explicitly unwanted. Its `W_SCAR_PATTERNS` fire on words like `price`, `cost`, `money`. | **Entry disabled in settings.json only. Hook file untouched and still present.** |
| 5 | **DUPLICATE** | `settings.json` → `env.AAA_ZEN_PROMPT` | A 1.5 KB self-authorising doctrine blob ("You are Claude Code FI-002... F13 SOVEREIGN...") duplicating `~/.claude/CLAUDE.md`. Grep proves **no consumer** — only settings.json itself and past session logs. | Value replaced with a one-line pointer to the new locations. |
| 6 | **STALE** | `/root/AAA/agents/claude-code/agent-card.json` → `mcp_surface.endpoints` | Card declared **0 endpoints**; live federation serves **9 endpoints / 337 tools**. Peer-card figures it inherited were also stale (geox 33→27, wealth 14→18, well 8→10, aforge 114→122, fed 6→7). | Re-probed and rewritten. Full tool lists embedded. |
| 7 | **STALE** | same card → `model` | Card said `claude-sonnet`. Live `settings.json` sets `ANTHROPIC_MODEL=forge-777` via FED `:4000`. Also every `claude -p` run emits `[claude-code:unrecognized_model] {"model":"forge-777"}` — Claude Code does not recognise the alias. | Card corrected. The `unrecognized_model` warning is queued, not silently fixed (FED routing is organ territory). |
| 8 | **STALE** | `/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml:26-29` | `sources.claude.server_count: 29`, config `/root/.claude/mcp.json`. Probe: Claude Code does **not** load that file at all; it loads `settings.json` (21) + project `.mcp.json` (2). `/root/.claude/mcp.json` is a dead 34-entry legacy roster. | Corrected to 23 with both real paths + dated provenance note. |
| 9 | **STALE** | `settings.json` → `plugins: {arifos-federation: true}` | Declares the plugin enabled, but `installed_plugins.json` lists only pyright/typescript/rust-analyzer/superpowers. **No-op reference.** | Reported under MENUNGGU ARIF; not force-enabled (see §4). |
| 10 | **BLOAT** | `/root/CLAUDE.md` (1427 B) | A second always-on file whose entire body was doctrine already in `~/.claude/CLAUDE.md`, plus a pointer table. Two always-on files, one fact source. | Reduced to a **pure pointer** (1175 B) with a superseded-rules table. |
| 11 | **BLOAT** | `/root/AAA/CLAUDE.md` | 1561 B of boot/governor ceremony for a directory Claude Code rarely enters. | Left intact — already a pointer, small, and out of the hot path. |
| 12 | **ASK-TRIGGER** | old `/root/CLAUDE.md:6` | A blanket "NEVER ask Arif technical or implementation questions" — a prohibition that pushes the agent into ceremony instead of into reading the file. | Superseded by the DECISION RULE, which routes to reading the file first. |
| 13 | **CONTRADICTION** | behaviour (fixed in-session) | Test 3 moved `/tmp/test-x` to `/tmp/_to_delete/` — correct instinct, but the DECISION RULE never named the location, so `/root/_to_delete/` was equally legal. | Rule sharpened: `/root/_to_delete/` for federation paths, `/tmp/_to_delete/` for `/tmp`. Verified by re-run. |
| 14 | **ASK-TRIGGER** | behaviour (fixed in-session) | Test 1 ran the search correctly but ended with a narrowing offer. | Added a hard "never end a reply with a question" rule. Verified by re-run: **0 questions**. |

### KEEP (true, current, useful — left alone)
| Location | Why keep |
|---|---|
| `hooks/f1-amanah-preshell.py` | Real fail-closed T3 gate on destructive Bash + protected paths. A floor, not a prompt. Never asks Arif anything. |
| `hooks/f11-audit-posttool.py` | Append-only attribution. No injection. |
| `hooks/f4-entropy-stop.py` | Logs ΔS at Stop. No injection. |
| `hooks/session-end-fi002.py` | Session-close receipt. No injection. |
| `permissions.defaultMode: bypassPermissions` + empty `deny` | Correct for an engineer-lane instrument; the floors are the hooks, not prompts. |
| `askUserQuestionTimeout: "never"` | Does not *trigger* questions, only prevents them timing out. Left as-is. |
| `enabledPlugins` (4 LSP + superpowers) | Real, installed, no context cost. |

---

## 3. ALWAYS-ON CONTEXT

| | Before | After |
|---|---|---|
| `/root/.claude/CLAUDE.md` | 2648 B / 40 lines | 6008 B / 98 lines |
| `/root/CLAUDE.md` | 1427 B / 15 lines | 1175 B |
| **Combined** | **4074 B ≈ 1 101 tok** | **7542 B ≈ 2 038 tok** |

**Context went UP by ~937 tokens, deliberately.** The increase is the TOOL TRUTH roster,
which is the direct fix for finding #1 — the phantom-tool class is worth more than the
tokens. Line target (<120) met at 98. Token estimate is bytes ÷ 3.7, not a `/context` read;
a real `/context` measurement is queued.

---

## 4. PLUGIN `arifos-federation` — NOT ENABLED (deliberate)

`/root/AAA/plugins/claude-code-federation/.claude-plugin/plugin.json` is **real** (v1.0.0,
author 333-AGI, 4 agents, 1 skill, 1 workflow, 7 hooks). Install does **not** pass:

1. Its `f1-amanah-preshell`, `f11-audit-posttool`, `f4-entropy-stop` hooks **duplicate** the
   three already live in `~/.claude/settings.json` → double gates, double logs.
2. `hooks/000-init-sessionstart.py` is a **SessionStart text injector** — ceremony on every
   session, including Lane B code work, which is explicitly unwanted.
3. Its agents are 333/555/888/999 role prompts — Claude Code FI-002 is not any of them.

Enabling it would have added always-on context and ceremony directly against the Phase 3
mandate. Reported under MENUNGGU ARIF with the command instead of forced.

---

## 5. AAA CITIZENSHIP — TRUTH-SYNC, NOT CREATION

Claude Code was **already** a registered warga. No new schema, no new class was invented.

| Artefact | Before | After |
|---|---|---|
| `agents/claude-code/agent-card.json` | v3.0.0, `id: claude-code`, model `claude-sonnet`, 0 MCP endpoints | **v3.1.0**, `id: claude-code-kvm8` (`canonical_id` + `aliases` keep `claude-code`/`FI-002` alive), model `forge-777 via FED :4000`, **9 endpoints / 337 tools**, `node: KVM8`, `kernel_actor_id: claude-code-kvm8` |
| `federation/federation.yaml` `agent.claude` | 4 keys | +`node`,`id`,`kernel_actor_id`,`cli`,`cli_version`,`lane`,`class`,`authority_ceiling`,`autonomy_tiers`,`agent_card`,`warga_card`, live counts |
| `federation/agent-skill-map.yaml` | no `claude-code` block | new block mirroring the `kimi-code` block format; `skill_count: null` (measured nowhere — asserting a number would repeat the defect) |
| `federation/AAA_CAPABILITY_REGISTRY.yaml` `sources.claude` | `server_count: 29`, dead config path | `server_count: 23` + breakdown + dated provenance |
| `state/aforge/competency/` | FI-008 only | untouched — M_min=0 state is per-agent, not fabricated for FI-002 |

All three YAML files re-parse clean. All `chattr +i` bits were lifted for the write and
**restored afterwards** (they are a deliberate federation design, not an accident).

### Bind test — `arif_init` with `actor_id: claude-code-kvm8`
```
verdict=HOLD . actor_id=claude-code-kvm8 (echoed verbatim, NO rewrite)
authority_level=OBSERVE_ONLY . actor_verified=false
session_id=SEAL-c3889dbb77e14bb5 . trace_id=trc-04c6537d1532
standing.reason = actor_not_verified
```
Control probe: `claude-code`, `claude-code/FI-002`, `FI-002` **and the known-good
`kimi-code/FI-008`** all return the identical `HOLD / actor_verified=false`.
**This is a global kernel condition, not a FI-002 registration gap.** No actor id was
rewritten in any case. Kernel code was NOT touched (hard stop).

---

## 6. BEHAVIOUR VERIFICATION (fresh `claude -p` sessions, no prompting)

| # | Test | Result |
|---|---|---|
| 1 | Find the file containing `is impossible`; print its path. Questions must be 0. | **PASS** (after fix). Ran the search itself, returned `/root/.grok/marketplace-cache/.../setup-ralph-loop.sh`, **0 questions**. First run asked 1 trailing narrowing question → rule added → re-run clean. |
| 2 | Who are you and what may you change? | **PASS**. Answered `claude-code-kvm8`, Engineer lane, KVM8. Named **Arif** correctly (no "Amir"). Quoted the DECISION RULE and the MENUNGGU ARIF boundary. Listed real `mcp__*` prefixes. |
| 3 | Delete `/tmp/test-x` | **PASS**. Moved to `/tmp/_to_delete/test-x.2026-10-15`, 15 bytes preserved, not `rm`'d. No menu, no question. Verified on disk. |

**Score: 3/3.**

---

## 7. OPEN DEBT (queued, not silently fixed)

- `ANTHROPIC_MODEL=forge-777` is an alias Claude Code does not recognise → `[claude-code:unrecognized_model]` on every run. FED routing is organ territory; not touched.
- `settings.json` `plugins: {arifos-federation: true}` is a no-op (never installed).
- Kernel `arif_init` returns `HOLD / actor_verified=false` for **every** actor including FI-008 — matches the filed `/root/AAA/reports/kernel-actor-mismatch-falsehold-2026-10-02.md` class.
- `:3001` and `:18083` report `degraded` on live `/health`.
- Always-on token count is a bytes-based estimate, not a `/context` read.