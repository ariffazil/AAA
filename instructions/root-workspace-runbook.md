# Root workspace — map, commands, locks

> Status: OPERATIONAL_SPEC (verified 2026-10-25). Home-level runbook for any agent whose cwd is `/root`.
> Once you `cd` into a sub-repo, that repo's own `AGENTS.md` (+ arifOS `RUNBOOK.md`) wins.

**`/root` is a home of independent git repos, not one repo.** `/root` itself is not versioned
(`git status` at /root fails; the `.git` stub there belongs to mimocode). Commit inside a sub-repo.

| Tree | Role / port | Stack | Runtime |
|---|---|---|---|
| `arifOS/` | kernel · :8088 | Python ≥3.12, uv, FastMCP | `/opt/arifos/app` |
| `A-FORGE/` | hands · :7071 | Node ≥22, TypeScript ESM | `/opt/a-forge/app` |
| `AAA/` | institution · :3001 | Vite/React + Python scripts | process |
| `GEOX/` · `WEALTH/` · `WELL/` | :8081 · :18082 · :18083 | Python | process |
| `web-canon/` | site sources | static | Caddy → `/var/www/html` |
| `.hermes/` (= `/root/HERMES`) | Hermes runtime + profiles | — | `hermes-asi-gateway` |

**Build / test (commands verified 2026-10-25; pytest checked on one file, not the full suite)**
- arifOS test: `cd /root/arifOS && .venv/bin/pytest tests/ -q --tb=short` (311 entries, 262 `*.py`; pass a file or `-k`, the full run is slow)
- arifOS deploy: `make -C /root/arifOS deploy-local`
- A-FORGE build/test: `cd /root/A-FORGE && npm run build` / `npm test` (tsc then node --test on dist)
- AAA: `cd /root/AAA && npm test` (= lint + vite build + tsx suites); single: `npm run lint`
- Federation: `make -C /root health` · `make -C /root prove` · `make -C /root sot-check`
  (root Makefile delegates to `/root/AAA/Makefile`; no targets of its own)
- Doctor / port sweep: `/root/scripts/doctor.sh`

**Git is fail-closed by lane.** Plain `git commit` fails in arifOS/AAA/WEALTH/WELL/A-FORGE
(user.name and signingkey are empty on purpose). Use the lane wrapper:
`/root/scripts/git-lane <lane> [-C /root/<repo>] commit -m "feat: ..."`.
`/root/scripts/git-lane list` shows lanes (this agent = `hermes`). git-lane also owns the
chattr unlock/relock cycle on `AAA/.git`. Conventional commits; tags `vYYYY.MM.DD` only.

**Generated files — editing them is lost work**
- `/root/AGENTS.md`, `CLAUDE.md`, `/root/.codex/AGENTS.md` are rendered by
  `/root/scripts/render-agents.sh` (`[--check] [target]`) from `/root/AAA/instructions/*.md`.
  Change the fragment, then re-render. Hand-edits survive only until the next render.
- `instructions/_UNRENDERED_INDEX.md` is generated too; renders warn when the lock blocks it.
- Render is now **idempotent** (2026-10-25): the trailer carries `body-sha256`, not a clock, so
  run-twice = byte-identical. If a diff appears on a second run, something real changed.
- `#!/usr/bin/env python3` resolves to Hermes' bundled 3.14.7 (no `requests`/`yaml`); 253 of 274
  scripts in `/root/scripts` carry that shebang. systemd units use venv pythons (safe); the two
  bare-`python3` crontab lines happen not to import either lib. New script + yaml = silent break:
  use `#!/usr/bin/python3` or the repo `.venv/bin/python`.

**Locked trees (chattr +i).** `AAA/{instructions,governance,canon,skills,eurekas,...}` and
`arifOS/GENESIS` reject direct writes. Sanctioned cycle:
`ARIFOS_TRACE_ID=trc-... /root/scripts/canon-mutate run <tree> -- <cmd>` (or `file <path> --`;
`status` lists locks). Receipt: `/var/lib/arifos/canon_mutations.jsonl`. Never `chattr -i` by hand.

**Boot surfaces (26 live, 771 copies)** — only these are loaded by a harness: `/root/AGENTS.md`
(+ `CLAUDE.md` symlink), `GEMINI.md`, `QWEN.md`, `.codex/`, `.kimi-code/`, `.grok/`,
`.config/opencode/`, `runtime/claude/CLAUDE.md`, `.hermes/AGENTS.md`, plus organ docs
(`arifOS/`, `A-FORGE/`, `GEOX/`, `WEALTH/`, `WELL/`, `arifFlow/`, `arif-fazil.com/`, `AAA/`) and
`.arifos/agents/*/AGENTS.md`. Everything under `*-wt-*`, `.federation-worktrees/`, `forge_work/*/repo`
is a copy — never patch there. Map + drift evidence: `forge_work/proposals/HERMES/AGENTS-MD-REALITY-GRAPH-2026-10-25.md`.

**`/root/CLAUDE.md` is a symlink to `AGENTS.md`** → `/root/scripts/fi002-overlay-check.sh` fails on it
(cap 5120 B, pointer pattern). That conflict is F13's call, not a bug to patch locally.

**Pitfalls that cost time**
- `python3` on PATH is Hermes' bundled 3.14.7 *without* `requests`/`yaml`; repo work needs the
  repo venv (`.venv/bin/python`) or `/usr/bin/python3`.
- arifOS CI step `uv run ruff check src tests` is stale: there is no `src/` (package is
  `arifosmcp/`) and `ruff check arifosmcp` currently reports ~3.8k findings — ruff is not a green
  gate here, do not "fix lint" as a precondition.
- One Telegram poller only: `hermes-asi-gateway` (enabled/active); `hermes-gateway` is disabled.
- Organs run bare-metal systemd; Docker is for supporting services, not core organs.
- Evidence is a live probe, not a unit name: `curl -s -o /dev/null -w '%{http_code}' localhost:8088/health`.
- Several agents share these repos: `git log -5` + `git status` before assuming you own a file.