# System-Prompt Context Injection Map — Hermes v0.20.1 (verified 2026-09-02)

Task class: "which files feed the Hermes system prompt / map context files /
inventory what's injected vs on-demand." Answer by reading the RUNTIME SOURCE,
never by guessing from file names. Verified live on KVM8, hermes_agent 0.20.1.

## How to verify (the recipe)

1. **Locate the runtime source.** The install is an editable pip install:
   read `/usr/local/lib/hermes-agent/venv/lib/python*/site-packages/__editable___hermes_agent_*_finder.py`
   → the `MAPPING:` dict maps module names to source dirs. On this box every
   module lives under `/usr/local/lib/hermes-agent/` (agent/, tools/, run_agent, ...).
   Do NOT grep the venv site-packages (nothing there but stubs) and do NOT
   grep the whole tree (see pitfalls).
2. **Read the two authoritative files:**
   - `agent/system_prompt.py` — 3-tier assembly docstring + tier construction
     (context tier ~line 595, volatile tier ~line 626).
   - `agent/prompt_builder.py` — `build_context_files_prompt` (~line 2330)
     with the priority ladder and char caps; `load_soul_md` (~line 2137).
3. **Cross-check config:** `/root/.hermes/config.yaml` → `context.engine`,
   `memory.*` (char limits, transient_file), `voice.persona_prompt_file`.

## The 3-tier system prompt (v0.20.1)

- **stable** — identity (SOUL.md or DEFAULT_AGENT_IDENTITY), tool guidance,
  platform hints. Byte-stable across turns for prompt-cache reuse.
- **context** — caller system_message + ONE project context file (priority:
  `.hermes.md`/`HERMES.md` → `AGENTS.md`/`agents.md` (merged git-root→cwd
  chain) → `CLAUDE.md` → `.cursorrules` — FIRST FOUND WINS, only one type
  loads) + coding-workspace snapshot. Char-capped (dynamic by model context
  window; fallback 20,000 chars; `context_file_max_chars` in config wins).
- **volatile** — skills index (name + description only), MEMORY.md block
  (capped `memory_char_limit`), USER.md block (capped `user_char_limit`),
  external memory provider block, plugin sections, timestamp/session line.
  Rebuilt on compaction; skills index deliberately fronted in this band.

## Injected vs on-demand (this box, 2026-09-02)

**Injected:**
| File | Tier |
|---|---|
| `/root/.hermes/SOUL.md` (14.4KB) | stable — identity slot, always |
| `/root/AGENTS.md` (6.5KB) | context — when cwd resolves to /root |
| `/root/.hermes/memories/MEMORY.md` (~4KB) | volatile, capped 4,000 chars |
| `/root/.hermes/memories/USER.md` (~2.5KB) | volatile, capped 2,500 chars |
| `/root/.hermes/skills/*/SKILL.md` (~197 active) | index only (57-char trigger window); body on-demand via skill_view |

**NOT injected (on-demand / upstream-only / TTS-only):**
- `/root/CLAUDE.md` — shadowed by /root/AGENTS.md (first-found-wins); compat copy only.
- `/root/AAA/instructions/` (35 fragments) — CANONICAL SOURCE of /root/AGENTS.md;
  rendered by `render-agents.sh`. Reaches the prompt only via the rendered artifact.
  Editing /root/AGENTS.md directly = drift (its header says so).
- `/root/AAA/governance/`, `/root/AAA/knowledge-graph/` — on-demand ("load on
  demand, not by reflex" is explicit in AGENTS.md itself).
- `/root/AAA/prompts/INIT.md` — manual session-start read (checklist step), not injected.
- `/root/.hermes/prompts/iarif_persona.md` — TTS-only (`voice.persona_prompt_file`),
  never enters the system prompt.
- `/root/.hermes/memories/SESSION.md` — transient, explicitly NOT injected into
  long-term LLM context (config `transient_purpose`).
- `.hermes/STATE.md`, `CALL_MAP.md`, `carry_forward.json` — symlinks into
  /root/AAA/docs/, on-demand via `now` CLI.

**False-path trap:** `/root/.hermes/profiles/default/memories/memory.md` (193B,
stale since 2026-08-04) is NOT the live memory store. Live store =
`/root/.hermes/memories/` (MEMORY.md, USER.md, SESSION.md, governed.json,
episodic/). `/root/SOUL.md`, `/root/MEMORY.md`, `/root/USER.md` do not exist —
canonical paths are under `/root/.hermes/`.

## Pitfalls hit during the mapping (2026-09-02)

1. **`bash -lc` output pollution.** Root's login shell sources the arifOS CRF
   banner (~7KB of box-drawing frame) on EVERY `bash -lc` invocation — it
   buries the actual command output and can push a 50KB cap into truncation.
   Fix: pure-Python reads via `execute_code` (`open()`, `os.walk`, `os.stat`)
   or non-login `bash -c`; never `bash -lc` for output-sensitive probes.
2. **Full-tree grep times out.** `grep -rn` over `/usr/local/lib/hermes-agent/`
   from `execute_code` hit the 300s timeout (tree is large; the box runs hot).
   Fix: use the indexed `search_files` tool scoped to one subdir (e.g.
   `path=/usr/local/lib/hermes-agent/agent`), which returns in seconds.
3. **Version-pinch this map.** Tier structure and file priority are release
   internals — re-verify `system_prompt.py`/`prompt_builder.py` after any
   `hermes update` before citing line numbers or the priority ladder.
