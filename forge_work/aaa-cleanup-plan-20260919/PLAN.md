# AAA Cleanup Plan — 2026-09-19

## Mandate
Arif directive: "major AAA cleanup. no redundant no chaos confusions for future agents aligned it with A2A protocol gitops all and deploy live." Full authorization across all gates (F13 confirmation received).

## State at start
- Branch: `proposals/orthogonality-v02-hermes-mapping` (NOT main)
- Working tree: 20+ dirty files at root (mostly 12:07:59 bulk timestamp from codex's parallel cleanup pass; my federation-shadow-ack changes at 12:56-13:46 are visible separately)
- Repo size: 1.6 GB, 1326 dirs
- A2A gateway: HEALTHY at :3001, vault CONNECTED, deployment_drift: false
- arif-fazil.com: HTTP 200, Caddy active
- A2A spec compliance: ALREADY MET — `@a2a-js/sdk: ^1.1.0` integrated, gateway serves A2A protocol
- MCP spec compliance: ALREADY MET — `@mcp-b/global: ^5.0.1` integrated
- Codex concurrently cleaning (visible in `opencode_receipts.jsonl`, 48 MB updated 14:12)

## Critical context for downstream agents
| Item | Status |
|---|---|
| `arifOS` repo | **3 unpushed commits on `main`** ahead of `origin/main` — must reconcile before any federation-wide push |
| `A-FORGE` repo | clean, on main |
| `telegram-miniapp/node_modules` | 172M, mtime 2026-07-09, regenerable via `npm install` — leave for now, archive later if confirmed unused |
| `codex` workspace | `.quarantine-redundancy-2026-09-19/` exists — DO NOT COLLIDE |
| Production deploy | 6 systemd services (aaa-a2a, aaa-mcp, aaa-signing, caddy, falkordb, qwen-serve); no AAA docker image in registry (DEPLOYMENT.md says `docker compose up -d` from source) |

## Archive-not-delete policy
All cleanup moves go to `/root/AAA/archive/2026-09-19-aaa-cleanup/` per existing team pattern (`.archive-20260805`, `.quarantine-redundancy-2026-09-19`). No `rm -rf`. Every move is git-tracked and reversible.

## Phase 0 (T0 reads) — DONE
Probed AAA structure, A2A spec, MCP spec, git remotes, codex footprint, production services.

## Phase 1 (T1 cleanup) — IN PROGRESS
Conservative batch-by-batch approach. Each batch = move + commit + validate. Halts on any validator failure.

### Batch 1.1 (this commit) — temporary artifacts + regenerable cache
| Source | Destination | Size | Rationale |
|---|---|---|---|
| `tmp/pet1h26.pdf` | `archive/2026-09-19-aaa-cleanup/tmp-pet1h26/` | 420K | PETRONAS geological PDF dump, clearly temporary |
| `tmp/pet1h26.txt` | same | 104K | PDF text extract |
| `tmp/pet1h26_high.pdf` | same | 1.3M | high-res variant |
| `tmp/pet1h26_high.txt` | same | 16K | text extract |
| `tmp/ptuk/` | `archive/2026-09-19-aaa-cleanup/tmp-ptuk/` | 27M | "ptuk" = PT UK tmp dir, not in live paths |
| `tmp/smd/` | `archive/2026-09-19-aaa-cleanup/tmp-smd/` | 560K | "smd" — SMD-related tmp, not in live paths |
| `graph/codegraph.db` | `archive/2026-09-19-aaa-cleanup/graph-codegraph/` | 74M | FalkorDB codegraph snapshot, regenerable from `graph/indexer.py` |
| `graph/audit-mcp-20260825T*.json` (3 files) | same | 300K | dated audit snapshots, superseded by newer audits |

**KEEP** in `graph/`:
- `indexer.py`, `mcp_audit.py`, `prune_context.py` (live scripts)
- `FI-011-DESIGN.md`, `WATCHER-INSTALL.md`, `delegation_envelope_patch.md` (design docs)

**NOT TOUCHED in this batch**:
- `a2a-server/` (live gateway code, deployed)
- `agents/_external/*` (my federation-shadow-ack work)
- `.git/`, `.env`
- `skills/`, `skills-deprecated/`, `skills-retired/` (skill inventory is canonical)
- `.quarantine-redundancy-2026-09-19/` (codex's workspace)
- `.backup-2026-09-17-openclaw-align/` (recent codex backup)

### Batch 1.2 (next turn) — backups redundancy
| Source | Size | Action |
|---|---|---|
| `backups/skills-pre-namespace-collapse-2026-09-19.tar.gz` | 7M | Archive — the skills/ dir already has the same content |
| `backups/skills/` (147M) | 147M | Triage — likely a full skills snapshot; archive but keep current `skills/` canonical |
| `backups/skill-collapse-20260918/` | 2.3M | Archive — superseded |

### Batch 1.3 (next turn) — telegram-miniapp runtime
- Confirm `telegram-miniapp` is/isn't a live surface
- If not live: archive `telegram-miniapp/` (with node_modules — can be reinstalled)

### Batch 1.4 (next turn) — node_modules bloat
- AAA repo `node_modules` (330M) — `.gitignore`'d already, not committed
- `telegram-miniapp/node_modules` (172M) — same status
- These don't enter git; they're regen costs, not repo bloat
- Action: verify `.gitignore` covers them, then no further action

### Batch 1.5 (next turn) — skills-retired migration
- `skills-retired/` (4.8M) — should move to `archive/` to match the archive-not-delete pattern
- Triage each subdir: `2026-09-19-*` are recent — check git log for why retired

## Phase 2 (T2 gitops + F13 deploy) — AFTER Phase 1 + halts
- Reconcile `arifOS` 3 unpushed commits first (separate F13-class call — arifOS is sovereign)
- Merge feature branch to local `main`
- Push to `origin/main`
- Trigger production deploy (manual docker compose, or whatever the deploy mechanism is)
- Verify: `curl https://arif-fazil.com/health`, AAA `:3001/health`, vault chain integrity
- `arif_seal` to close session

## Validation gates (run after each batch)
1. `npm run validate:aaa` (must pass)
2. `npm run validate:a2a-cards` (must pass)
3. `curl http://127.0.0.1:3001/health` (still HEALTHY)
4. `curl https://arif-fazil.com/` (still 200)
5. `git status` (clean working tree, branch tracked)

## Reversibility
Every archive move = `mv src dst` followed by git commit. To reverse: `mv archive/.../* src && rm -rf archive/2026-09-19-aaa-cleanup` (single command, fully scripted).
