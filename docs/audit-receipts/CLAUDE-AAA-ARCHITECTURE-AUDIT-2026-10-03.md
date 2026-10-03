# Claude Code + AAA Architecture Audit — 2026-10-03 14:40

**Actor:** FI-005 (codex-cli) per Arif's revised directive after live GitHub audit.

**Method:** F2 probe (live filesystem + GitHub content) + 7 specs (F13-stage). **ZERO code modified.**

## Live probe results (F2 truth)

| Claim | Verified | Evidence |
|---|---|---|
| `/root/.claude/identity.json` (excluded by .gitignore) | ✅ Confirmed excluded in policy, but `agents/claude-code/identity.json` IS in GitHub | `curl HTTP=200` for the GitHub file |
| Live settings.json has 0 hooks | ⚠️ **Partially wrong** — 11 hits on `hooks\|SessionStart\|...` grep. Not "empty" but unverified runtime firing. | `grep -c` result 11 |
| Skills are 3x copies, not symlinks | ✅ Confirmed | All 3 paths are DIR, not symlinks |
| carry_forward.json size | ✅ 742KB (was 441 entries when last tallied) | `stat` output |
| Agent card `authority_ceiling: PROPOSE_AND_VERIFY` | ✅ Confirmed via GitHub | `curl + jq` |

## What I will NOT do (per Arif's corrections)

1. ❌ **No F13_RATIFIED_ASIDE stamp.** Per Arif: "F13 stamp ≠ live authority". Stamp is provenance, not signal. Live authority = `actor_verified` from arifOS response.
2. ❌ **No Codex hooks copied to Claude.** Per Arif: "4 implementations drift". Solution is ONE canonical ABI + render adapter per harness (see Spec 1).
3. ❌ **No `claude_carry_forward.json` new file.** Per Arif: dual ledger. Solution is ONE federation task ledger with per-agent attribution (see Spec 3).

## 7 specs sealed (F13-stage, no build)

| # | Spec | Problem it solves |
|---|---|---|
| 1 | `AAA-HOOK-ABI-SPEC-v1.md` | One canonical hook ABI, render per harness (no 4x drift) |
| 2 | `AAA-SKILLS-RENDERER-SPEC-v1.md` | Single skill source + read-only projection (no 3x copy) |
| 3 | `FEDERATION-TASK-LEDGER-SPEC-v1.md` | ONE shared ledger with `owner: "claude-code"` field (no dual file) |
| 4 | `IDENTITY-SPLIT-SPEC-v1.md` | 3 files: `identity.public.json` (GitHub), `identity.private.json` (host), `identity.key` (host). Mechanical rule for what to commit. |
| 5 | `AAA-CONFIG-COMPILER-SPEC-v1.md` | One compiler, N renderers. `C_i = C_AAA ⊕ C_adapter ⊕ C_machine ⊕ S_secret`. |
| 6 | `AAA-DRIFT-CANARY-SPEC-v1.md` | 6 synthetic tasks × 4 harnesses. Equivalent outcomes (ALLOW/HOLD/VOID) required. |
| 7 | `CODEX-IDENTITY-CONTRACT-SPEC-v1.md` | Witness consumes full contract from arifOS (not just "init returned 200"). Fail-closed on `!actor_verified` or `!mutation_allowed` when action mutates. |

## Three-sovereignty boundary (per Arif)

```
AAA PUBLIC          ← in `ariffazil/AAA` GitHub
─────────────────
code, generic skills,
schemas, templates,
agent cards, public
doctrine, tests

AAA PRIVATE         ← on host only, NOT in git
────────────────────
personal skills,
private workflows,
internal business,
private memory,
human relationship

HOST RUNTIME        ← on host, ephemeral
──────────────────
credentials,
sessions, logs,
cache, tokens,
PIDs, leases,
generated config
```

## What is in each blueprint (F13-stage)

| Artifact | In GitHub? | Reason |
|---|---|---|
| `identity.public.json` | YES | public by definition |
| `identity.private.json` | NO | has secrets |
| `identity.key` | NO | raw key |
| `settings.template.json` | YES | desired state, declarative |
| `mcp.profile.yaml` | YES | semantic SOT |
| `skills.profile.yaml` | YES | per-harness subset |
| `hooks.profile.yaml` | YES | per-harness adapter source |
| `permissions.policy.yaml` | YES | testable policy |
| `canary_spec.yaml` | YES | drift test |

## Reversibility

All 7 specs are F13-stage. NONE have been built. They are recommendations for future agent (or F13 ratification) to decide whether to build.

If a spec is rejected: just `rm /root/AAA/docs/blueprints/<spec>.md`. Zero system change.

## What I did NOT do (per Law 10)

- ❌ Did not modify any config (`/root/.claude/settings.json`, `/root/.codex/config.toml`, etc.)
- ❌ Did not create `claude_carry_forward.json` or any new file in host filesystem
- ❌ Did not write new hooks
- ❌ Did not add new MCP server
- ❌ Did not add F13 stamp
- ❌ Did not change agent-card (the existing `PROPOSE_AND_VERIFY` ceiling is already correct per Arif)

## State after this audit

```
audit-receipts:  7 files (5 keepers + 2 patches, all action-validated)
blueprints:      10 files (2 F13 specs from earlier + 1 v1 spec + 7 new)
                  (the 7 new are F13-stage, NOT yet ratified)
Mutasi kod:      0 (this turn)
Mutasi config:   0
New hooks:       0
New MCPs:        0
New files (host): 0
```

## SABAR not SEAL (per Arif)

Claude Code's runtime is still under-wired. AAA architecture still has 4 harnesses drifting. **The specs exist, not the system.** Future F13 ratification decides whether to build.
