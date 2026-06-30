# WARGA IGNITION PROTOCOL v1.0.0

> **DITEMPA BUKAN DIBERI** — Cross-substrate ignition is forged, not given.
> **Authority:** F13 SOVEREIGN (Arif) — ratified 2026-06-30
> **Scope:** All warga-AAA citizens: hermes-asi, claude-code, aaa-gateway (OpenClaw), 777-forge (OpenCode)

---

## The Ignition Invariant

> Any warga AAA agent can request, load, and execute any skill on any substrate
> that satisfies the constitutional physics. The skill is the institution.
> The substrate is the iron.

---

## 1. Substrate Map

| Substrate | Warga ID | Host Binding | Skill Root | Ignition Mechanism |
|-----------|----------|-------------|------------|-------------------|
| **Hermes** | hermes-asi | hermes-agent | `/root/.hermes/skills/` | `skill_view(name)` + `skill_manage()` |
| **OpenClaw** | aaa-gateway | openclaw-gateway | `/root/.openclaw/workspace/` | AGENTS.md load + file read |
| **OpenCode** | 777-forge | opencode | `/root/.openclaw/workspace-opencode/` | AGENTS.md load + file read |
| **Claude Code** | claude-code | claude-code | `/root/.claude/skills/` | AGENTS.md load + file read |

## 2. Canonical Skill Registry

**Primary:** `/root/AAA/skills/warga/` — the shared, substrate-agnostic skill registry.
**Symlinks:** Each substrate has a symlink `warga-skills → /root/AAA/skills/warga/` in its skill root.

```
/root/AAA/skills/warga/
├── WARGA_IGNITION.md      ← THIS FILE
├── WARGA_COMMS.md         ← communication protocol
├── WARGA_MANIFEST.yaml    ← skill → substrate capability map
├── constitutional/        ← F1-F13, ART, kernel binding
├── execution/             ← forge, build, deploy, terminal
├── intelligence/          ← reasoning, memory, epistemic
├── domain/                ← GEOX, WEALTH, WELL grounding
└── comms/                 ← A2A, Telegram, cross-substrate messaging
```

## 3. Ignition Sequence

### 3.1 Request (any substrate → shared registry)

```
AGENT on Substrate A:
  "I need skill X"
  → Read /root/AAA/skills/warga/WARGA_MANIFEST.yaml
  → Locate skill path
  → Load skill content
  → Execute
```

### 3.2 Load (substrate-specific mechanism)

| Substrate | Load Command |
|-----------|-------------|
| Hermes | `skill_view(name="warga-<skill>")` or direct file read |
| OpenClaw | Read `/root/AAA/skills/warga/<category>/<skill>/SKILL.md` |
| OpenCode | Read `/root/AAA/skills/warga/<category>/<skill>/SKILL.md` |
| Claude Code | Read `/root/AAA/skills/warga/<category>/<skill>/SKILL.md` |

### 3.3 Execute (substrate-specific)

Each substrate executes the skill using its native tool surface. The skill content
is substrate-agnostic. The tool calls are substrate-specific. Example:

- Skill says "web_search(query)" → Hermes uses `web_search()`, OpenClaw uses `mcp_brave_search_brave_web_search()`
- Skill says "forge file" → Hermes uses `write_file()`, OpenClaw uses `mcp_filesystem_write_file()`

## 4. Cross-Substrate Skill Propagation

When a skill is created on one substrate, it MUST be propagated to the shared registry:

```
1. Agent creates skill on Substrate A
2. Agent copies skill to /root/AAA/skills/warga/<category>/<skill>/
3. Agent updates WARGA_MANIFEST.yaml with new entry
4. All other substrates can now load the skill via their symlink
```

**Propagation rule:** Skills created on ANY substrate are available to ALL substrates
within 1 read cycle. No approval gate. No replication delay. The shared filesystem
is the replication mechanism.

## 5. Tool Equivalence Table

When a skill references a tool, each substrate maps it to its native equivalent:

| Canonical Tool | Hermes | OpenClaw | OpenCode | Claude Code |
|---------------|--------|----------|----------|-------------|
| web_search | `web_search()` | `mcp_brave_search_brave_web_search()` | `web_search` (builtin) | `WebSearch` |
| file_read | `read_file()` | `mcp_filesystem_read_text_file()` | `read_file` (builtin) | `Read` |
| file_write | `write_file()` | `mcp_filesystem_write_file()` | `write_file` (builtin) | `Write` |
| terminal | `terminal()` | `terminal` (bash) | `bash` (builtin) | `Bash` |
| git | `terminal("git ...")` | `terminal("git ...")` | `bash("git ...")` | `Bash("git ...")` |
| a2a_send | `send_message` via Telegram | A2A gateway :3001 | A2A gateway :3001 | A2A gateway :3001 |
| memory_store | `memory()` | `mcp_memory_server_create_entities()` | memory tool | memory tool |
| vault_seal | `mcp_well_well_trace_lineage()` | arifOS MCP | arifOS MCP | arifOS MCP |

## 6. The Permanent Line

> Skills are institutional knowledge. Substrates are mortal iron.
> The shared registry is the institution. The symlink is the bridge.
> Any warga agent can ignite any skill on any substrate.
> DITEMPA BUKAN DIBERI.
