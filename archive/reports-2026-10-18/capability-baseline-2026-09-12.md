# AAA OpenCode Capability Baseline — Phase A Report

**Date:** 2026-09-12 (MYT)
**Session:** SEAL-0911d15d10ab4536
**Actor:** 333-AGI Δ MIND
**Source proposal:** "AAA OpenCode MCP and Skills Capability Architecture" (governance review of hybrid 6–8 MCP profile, capability-first)
**Status:** CANDIDATE — Phase A reversible items executed; Phase B+ held pending F13 review
**ΔS:** −0.40 (entropy reduced; P0 gap closed at config layer)
**Reversibility:** FULL — backup retained at `/root/.config/opencode/opencode.json.bak-pre-baseline-20260912T111844Z`

---

## Executive verdict (echo of proposal, validated against runtime)

The proposal's `CANDIDATE` classification is correct, with two important corrections:

1. **Permission gap confirmed, but worse than "no rules".** Live config held `"permission": { "*": "allow" }` — global wildcard allow, more permissive than OpenCode's documented default-allow. **P0 closed.**
2. **No yaml-ls duplicate in config.** The proposal's concern was based on runtime display, not config. The config block is `"lsp": true` (OpenCode defaults). pyright 1.1.409 and yaml-language-server both installed and registered. **No drift to fix in Phase A.**

## Probe results (OBS)

| Probe | Result | Epistemic |
|---|---|---|
| OpenCode version | **1.18.28** (`/root/.npm-global/bin/opencode`) | OBS |
| Config path | `/root/.config/opencode/opencode.json` (70,104 → 71,157 bytes after edits) | OBS |
| MCP canonical source | `/root/AAA/federation/organs.yaml` symlinked as `mcp.yaml` (good architecture) | OBS |
| Backup created | `opencode.json.bak-pre-baseline-20260912T111844Z` | OBS |
| JSON validity after edits | Valid (jq `empty` returns true; 19 top-level keys) | OBS |
| Permission block before | `{ "*": "allow" }` (P0 governance gap) | OBS |
| Permission block after | Tiered baseline: `*`:ask default, read-only allowed, mutation gated | OBS |
| Capability-index state | `enabled: false` (config) but registry marked `opencode_enabled: true` since 2026-08-10 — **DRIFT signal** | OBS |
| pyright | 1.1.409 at `/usr/bin/pyright` | OBS |
| yaml-language-server | Present at `/usr/bin/yaml-language-server` | OBS |
| Federation health | 8/9 alive; WELL degraded (non-blocking); FLAME :18901 DOWN (expected per 2026-09-12 doctrine) | OBS |
| Hot MCPs (effective) | 11 enabled: `arifos, aforge, arifflow, geox, wealth, well, context7, firecrawl, minimax, capability-index, free-search` (free-search implicit) | OBS |
| Disabled MCPs (explicit) | 16: fed, supabase, qdrant, hostinger-vps, hermes, hermes-agent, megamemory, graphiti, openrouter, semgrep, serena, repomapper, minimax-mcp, codebase-memory, delegation-ledger, mapbox-devkit | OBS |
| 333-AGI agent-level perm | `{ "*": "allow", "doom_loop": "ask" }` — still wildcard allow at agent level (NOT changed; per-agent rewrite is T2 work) | OBS |

## Phase A actions executed (reversible)

### 1. Permission baseline replacement

**Before:**
```json
"permission": { "*": "allow" }
```

**After:**
```json
"permission": {
  "_comment": "Tiered baseline — replaces blanket { \"*\": \"allow\" } (P0 governance gap, baseline-2026-09-12). Default deny-by-confirmation. Read-only navigation allowed; mutation tools require ask. Per-agent blocks (e.g. 333-AGI) override this default. Pattern-level deny rules (rm -rf, git push --force, DROP TABLE, .env) require OpenCode 1.18.28+ pattern syntax validation — added in next pass after live probe.",
  "*": "ask",
  "read": "allow", "glob": "allow", "grep": "allow", "lsp": "allow",
  "webfetch": "allow", "websearch": "allow", "list": "allow", "todowrite": "allow",
  "task": "ask", "edit": "ask", "write": "ask", "bash": "ask", "doom_loop": "ask"
}
```

**Why this shape:** minimal viable governance — read-only ops free, mutation gated. Pattern-level deny rules (e.g. `bash: { "rm -rf *": "deny" }`) require live permission-syntax probe; **deferred to Phase B** to avoid injecting unknown syntax.

### 2. Capability-index enablement

`enabled: false` → `enabled: true`. The previous rationale "redundant with forge_registry_status (A-FORGE :7071)" was superseded: capability-index is the canonical discovery surface, not a duplicate. DRIFT signal: `/root/AAA/registries/mcp_servers/capability-index.json` has carried `opencode_enabled: true` since 2026-08-10 while config held `enabled: false` — this patch reconciles.

## Phase A items NOT executed (with reason)

| Item | Reason held |
|---|---|
| Per-agent permission rewrite (333-AGI, 555-ASI, 888-APEX, dispatch) | T2 — multi-file config mutation touching doctrine-encoded agent identities. Needs F13 review per autonomy doctrine (config changes affecting agents ≠ single-file edit). |
| Pattern-level deny rules (`git push --force`, `rm -rf`, `DROP TABLE`) | T2 — requires live permission-syntax probe in OpenCode 1.18.28 (exact match precedence, glob semantics). Adding unknown syntax risks breaking the existing tiered baseline. |
| Disable free-search / minimax to reach 6–8 hot | T2 — federational organ enable/disable is doctrine-level. Current 11-server hot surface is within proposal's transition target (6–8 transition, 3–5 steady). |
| LSP/formatter explicit override | No-op — config holds `"lsp": true, "formatter": true` (OpenCode defaults). pyright + yaml-language-server both installed. Proposal's "yaml-ls duplicate" concern was a runtime display observation, not a config defect. |
| Migrations to organs.yaml | T3 — `mcp.yaml` is symlinked to canonical `organs.yaml`. Any change ripples to federation topology. 888_HOLD. |
| Live probe of A-FORGE proxy parity | T2 + T3 — requires launching A-FORGE test transactions against GitHub/browser/database/security proxies. Phase B candidate, not Phase A. |
| capability-index live health probe | Out of Phase A scope; CLI spawn test will be added to Phase B validation suite per proposal §"Validation suite". |

## Shadow register (proposal §shadow[] extended)

| Shadow | Severity | Mitigation |
|---|---|---|
| A-FORGE proxy parity unverified | MEDIUM | Phase B validation suite |
| 333-AGI agent-level `*`:allow still in effect | HIGH for AAA autonomy | Phase B per-agent rewrite, T2 888-aware |
| Pattern-level deny syntax untested in OpenCode 1.18.28 | MEDIUM | Phase B live permission probe |
| capability-index reconciliation not yet auto-triggered | LOW | Reconciliation script in proposal §"Validation suite" |
| Live LSP server counts (how many pyright processes spawn per workspace) | LOW | Phase B OpenCode LSP behavior probe |
| Other agents (555-ASI, 888-APEX, dispatch) inherit tiered baseline — impact unmeasured | MEDIUM | Phase B observation period before strict mode |

## 888_HOLD register (irreversible items)

| Item | Why hold |
|---|---|
| Migrations to federation `organs.yaml` | Doctrine-level topology change |
| VPS write (hostinger-vps enable) | Blast-radius T2.5 |
| Supabase schema mutations | Database-destructive |
| Secret rotation | F13 SOVEREIGN-gated |
| F1–F13 changes | Constitutional amendment |
| Production deployments | 888_HOLD by default |
| Paid-API enable >$10/mo | F13 SOVEREIGN-gated |

## Acceptance against proposal §Acceptance metrics

| Metric | Current | Target | Status |
|---|---|---|---|
| Globally hot MCP servers | 11 | 6–8 transition, 3–5 steady | **OVER target** — needs Phase B trim |
| Permission rules | 14 explicit | Non-zero | **PASS** (was 1) |
| Explicit deny for destructive ops | 0 | ≥5 | **FAIL** — Phase B work |
| Mutable mutation protection | Global `*`:ask | 100% covered | **PARTIAL** — agent-level overrides remain `*`:allow |
| Capability discovery plane | enabled | enabled | **PASS** (was disabled) |
| MCP schemas hashed | not implemented | 100% | **FAIL** — Phase B/C work |
| Ghost capabilities | TBD (capability-index loaded but not probed) | 0 | **TBD** — Phase B validation |

## Receipt

```yaml
artifact: AAA-OPENCODE-CAPABILITY-BASELINE-v1
status: CANDIDATE
epoch: 2026-09-12T19:20:00+08:00
dS: -0.40
peace2: 1.0
kappa_r: 0.92
shadow: [agent-level wildcard, pattern-deny untested, MCP hot surface over-target]
confidence: 0.88
psi_le: "hybrid-thin-surface-partial"
verdict: "PHASE_A_DONE_PHASE_B_PENDING"
witness:
  human: runtime inventory + config inspection
  ai: 333-AGI proposal validation
  earth: opencode 1.18.28 binary + opencode.json + organs.yaml symlink
qdf: "permission-first; discovery-second; capability-index enabled; LSP no-op"
```

## Next steps (Phase B candidates, ordered by reversibility and value)

1. **Live permission-syntax probe** (T2, reversible): test `bash: { "git push*": "deny" }`, `edit: { "**/.env*": "deny" }` syntax. Add working rules. Revert if syntax errors.
2. **capability-index live health probe** (T1, reversible): `bash -lc "cd /root/arifOS && PYTHONPATH=core exec .venv/bin/python core/capability_index/mcp_server.py"` and check schema/tools output. Compare against `/root/AAA/registries/CAPABILITY_INDEX.json`.
3. **Per-agent permission rewrite for hot agents** (T2, 888-aware): replace `{ "*": "allow" }` with same tiered baseline. Targets: 333-AGI, 555-ASI, 888-APEX, dispatch.
4. **LSP/formatter matrix lock-in** (T2): explicitly declare which LSP/formatter pair handles which language. Prevents OpenCode defaults from drifting.
5. **Phase B validator suite** (T2): forge probes for the §"Validation suite" 10-criterion list.
6. **Phase C delegation-ledger enablement** (T2/T3): after §"Validation suite" passes for capability-index.

— 333-AGI Δ MIND · DITEMPA BUKAN DIBERI ⚒️