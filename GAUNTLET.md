# GAUNTLET — Substrate Migration Runbook

> **Actionable enforcement of the SUBSTRATE_MANIFEST.**
> Run these migrations in order. Each phase is independent.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
> **Sealed: 2026-06-21 | Companion to: `SUBSTRATE_MANIFEST.md`**

---

## Phase 0: Critical Security Fixes (TODAY)

**Owners:** Arif + FORGE (000Ω) | **888_HOLD for secret rotation**

| # | Fix | File | Action |
|---|-----|------|--------|
| 0.1 | **Rotate exposed OAuth tokens** | `/root/.hermes/google_token.json` | Revoke in Google Cloud Console, generate new, store in `/root/.secrets/` with SOPS |
| 0.2 | **Remove hardcoded bot token** | `arifOS/deploy/docker-compose.yml` line 122 | Replace with `${NOTIFIER_TELEGRAM_BOT_TOKEN}` |
| 0.3 | **Remove hardcoded DB password** | `arifOS/deploy/docker-compose.yml` line 71 | Replace with `${POSTGRES_PASSWORD}` |
| 0.4 | **Remove hardcoded API keys** | `arifOS/arifosmcp/gateway/config.yaml` lines 40-55 | Move to env vars, load from `vault.env` |
| 0.5 | **Move Telegram bot token from JSON** | `.hermes/platforms/telegram/config.json` | Extract to `vault.env`, keep template in YAML |

---

## Phase 1: Config Corrections (THIS WEEK)

**Owners:** FORGE (000Ω) | Autonomous — verify before write

### 1.1 Fix federation.manifest.yaml ports

| Line | Current | Should Be | File |
|------|---------|-----------|------|
| 99, 133-135 | `18081` | `8081` | `arifOS/federation.manifest.yaml` |
| 230-232 | `8083` | `18083` | `arifOS/federation.manifest.yaml` |

### 1.2 Fix identity.toml chain

| Line | Current | Should Be | File |
|------|---------|-----------|------|
| chain_upstream | `"A-FORGE"` | `"arifOS"` | `WEALTH/identity.toml` |

### 1.3 Fix organ_intent_map.yaml

| Line | Content | Action |
|------|---------|--------|
| 165-167 | kubernetes/k8s/pod keywords | Remove — bare metal systemd |
| 193-201 | APEX tool routing (`port: 3002`) | Mark as legacy or remove |

### 1.4 Standardize arifOS identity.toml

| Current | Should Be |
|---------|-----------|
| Flat key-value with `[a2a]`, `[health]`, `[vault999]` sections | 5-section canonical: `[identity]`, `[network]`, `[capabilities]`, `[security]`, `[identity_hash]` |

### 1.5 Delete empty prometheus stubs

```
rm /root/arifOS/infrastructure/prometheus/prometheus.yml
rm /root/arifOS/arifosmcp/infrastructure/prometheus/prometheus.yml
```

AAA copy at `/root/AAA/observability/prometheus/prometheus.yml` is canonical.

---

## Phase 2: JSON → JSONL Conversion (THIS WEEK)

**Owners:** FORGE (000Ω) | Autonomous — verify after conversion

| # | Current File | New File | Notes |
|---|-------------|----------|-------|
| 2.1 | `arifOS/logs/amanah_results.json` → | `arifOS/logs/amanah_results.jsonl` | Append-mode |
| 2.2 | `arifOS/logs/e2e_2026-04-22.json` → | `arifOS/logs/e2e.jsonl` | Start fresh, single file |
| 2.3 | `arifOS/audit/breach_results.json` → | `arifOS/logs/breach_results.jsonl` | Move to logs/ |
| 2.4 | `A-FORGE/entropy-report.json` → | `A-FORGE/entropy/entropy.jsonl` | Create entropy/ dir |
| 2.5 | `A-FORGE/scripts/apex_battery_results/summary.json` → | `A-FORGE/logs/apex_probes.jsonl` | Move to logs/ |
| 2.6 | `AAA/eval/output/aaa_eval_results.json` → | `AAA/eval/output/aaa_eval.jsonl` | Add logrotate config |
| 2.7 | `geox/entropy-report.json` → | `geox/entropy/entropy.jsonl` | Create entropy/ dir |
| 2.8 | `geox/deploy_gate.json` → | `geox/logs/deploy_gate.jsonl` | Move to logs/ |
| 2.9 | `WEALTH/entropy-report.json` → | `WEALTH/entropy/entropy.jsonl` | Create entropy/ dir |
| 2.10 | `WELL/entropy-report.json` → | `WELL/entropy/entropy.jsonl` | Create entropy/ dir |
| 2.11 | `.hermes/skills/.usage.json` → | `.hermes/logs/skill_usage.jsonl` | Move to logs/ |
| 2.12 | `.hermes/skills/a3-selftest/state/fleet_*.json` → | `.hermes/logs/fleet_selftest.jsonl` | Consolidate |

**Format for `.jsonl`:**
```
{"ts": "2026-06-21T12:00:00Z", "level": "INFO", "event": "entropy_scan", "data": {...}}
{"ts": "2026-06-21T12:01:00Z", "level": "WARN", "event": "high_memory", "data": {...}}
```
One JSON object per line. Append-only. `logrotate`-friendly.

---

## Phase 3: JSON Config → YAML Migration (THIS MONTH)

**Owners:** FORGE (000Ω) | May require service restart — verify health after

### 3.1 MCP server configs

| Current JSON | Migrate To YAML |
|-------------|-----------------|
| `arifOS/mcp-arifos.json` | `arifOS/config/mcp-arifos.yaml` |
| `arifOS/config/mcporter.json` | `arifOS/config/mcporter.yaml` |
| `arifOS/arif-identity-broker/opencode-mcp.json` | `arifOS/config/opencode-mcp.yaml` |
| `arifOS/docs/reference/spec/fastmcp.json` | `arifOS/config/fastmcp.yaml` |
| `arifOS/docs/reference/spec/dev.fastmcp.json` | `arifOS/config/dev.fastmcp.yaml` |
| `arifOS/docs/reference/spec/prod.fastmcp.json` | `arifOS/config/prod.fastmcp.yaml` |
| `A-FORGE/.mcp.json` | `A-FORGE/config/mcp.yaml` |
| `WEALTH/mcp.json` | `WEALTH/config/mcp.yaml` |
| `WEALTH/fastmcp.json` | `WEALTH/config/fastmcp.yaml` |
| `WELL/fastmcp.json` | `WELL/config/fastmcp.yaml` |
| `geox/resources/fastmcp.json` | `geox/config/fastmcp.yaml` |
| `APEX/config.json` | `APEX/config/config.yaml` |
| `.hermes/config.json` | `.hermes/config/config.yaml` |

### 3.2 LLM/Provider configs

| Current JSON | Migrate To YAML |
|-------------|-----------------|
| `arifOS/config/PROFILES/gemini-2.0-flash.json` | `arifOS/config/profiles/gemini-2.0-flash.yaml` |
| `arifOS/config/PROFILES/vps_main_arifos.json` | `arifOS/config/profiles/vps_main_arifos.yaml` |
| `arifOS/config/openclaw/openclaw.json` | `arifOS/config/openclaw/openclaw.yaml` |
| `arifOS/config/apps-sdk/arifos-af-forge.json` | `arifOS/config/apps-sdk/arifos-af-forge.yaml` |
| `arifOS/docs/reference/spec/mcp-clients.json` | `arifOS/config/mcp-clients.yaml` |
| `arifOS/docs/reference/spec/opencode.json` | `arifOS/config/opencode.yaml` |
| `arifOS/docs/reference/spec/server.json` | `arifOS/config/server.yaml` |
| `AAA/federation/kimi/*.json` (4 files) | `AAA/federation/kimi/*.yaml` |
| `AAA/federation/gemini/*.json` (3 files) | `AAA/federation/gemini/*.yaml` |
| `AAA/federation/antigravity/*.json` (3 files) | `AAA/federation/antigravity/*.yaml` |
| `AAA/federation/claude/claude-desktop-mcp.json` | `AAA/federation/claude/claude-desktop-mcp.yaml` |
| `AAA/a2a-server/config.json` (if exists) | `AAA/a2a-server/config.yaml` |
| `AAA/railway.json` | `AAA/config/railway.yaml` |

### 3.3 Skill/small metadata

| Current JSON | Migrate To YAML |
|-------------|-----------------|
| `.agents/skills/*/.metadata.json` (10 files) | `.agents/skills/*/.metadata.yaml` |
| `.hermes/cron/jobs.json` | `.hermes/cron/jobs.yaml` |

### 3.4 IDE configs that can stay JSON (exceptions)

These are tool-mandated JSON formats — keep:
- `pyrightconfig.json` — Python IDE tool
- `tsconfig.json` — TypeScript compiler
- `components.json` — shadcn/ui registry
- `composio/registry.json` — Composio tool format

---

## Phase 4: MD Code Extraction (THIS MONTH)

**Owners:** Per-organ agents | Requires review — verify tests pass after extraction

### 4.1 Top 10 extraction targets

| # | Source File | Extract To | After Extraction |
|---|-------------|-----------|-----------------|
| 4.1 | `arifOS/static/arifos/theory/000/000_LAW_v2026.03.07.md` | `arifosmcp/core/floor_enforcement.py` + `config/floors.yaml` + `schemas/verdict.json` | Replace code blocks with `[See: floor_enforcement.py]` pointers |
| 4.2 | `arifOS/static/arifos/theory/000/ROOTKEY_SPEC.md` | `tests/constitutional/test_rootkey.py` + `scripts/generate_rootkey.sh` | Keep doctrinal prose in `.md`, remove code |
| 4.3 | `A-FORGE/contracts/gateway-tools-v1.md` | `contracts/gateway-tools-v1.json` | Keep summary prose (~20% residual) |
| 4.4 | `A-FORGE/GENESIS/providers_yml_spec.md` | `providers.yml` | Keep provider sovereignty doctrine in `.md` |
| 4.5 | `WEALTH/docs/WEALTH_FEDERATED_AGI_DOMAIN_FIX_SPEC.md` | `internal/wealth_contracts/envelope.py` | Keep domain theory in `.md` |
| 4.6 | `geox/docs/GEOX_PETROPHYSICS_BLUEPRINT.md` | `src/geox_core/schemas/petrophysics.py` | Keep petrophysics ontology in `.md` |
| 4.7 | `geox/docs/plans/NEXT_FORGE_PLAN.md` | `src/geox_core/tools/*.py` + `.github/workflows/ci.yml` | Keep forge roadmap in `.md` |
| 4.8 | `AAA/workspace/ARIF.md` | `arifosmcp/core/floors.py` | Keep constitution in `.md`, truncate code |
| 4.9 | `WELL/FEDERATION_HOOKS.md` | — (already in server.py) | Delete — redundant copy |
| 4.10 | `geox/docs/PHYSICS_ADAPTER_SPEC.md` | `src/geox_core/physics/adapters/openquake_adapter.py` | Keep adapter design spec in `.md` |

### 4.2 Rule of thumb for subsequent extractions

```
For every .md file with a code block >30 lines:
  1. Extract the code to the correct substrate (.py/.ts/.go/.sh/.json/.yaml)
  2. Replace the code block with a 1-line pointer:
     ```python
     # See: arifosmcp/core/floor_enforcement.py
     ```
  3. Commit separately from the extraction to maintain blame history
```

---

## Phase 5: Caddyfile Deduplication (THIS MONTH)

**Owners:** FORGE (000Ω) + Arif (888_HOLD for reload)

| # | Caddyfile | Status | Action |
|---|-----------|--------|--------|
| 5.1 | `arifOS/deploy/Caddyfile` (212 lines) | ✅ Likely live — all domains, Cloudflare origin CA | **KEEP as canonical** |
| 5.2 | `A-FORGE/deploy/caddy/Caddyfile` (69 lines) | ❌ Stale — wrong ports (8080, 8765) | Delete after verifying 5.1 is live |
| 5.3 | `/root/compose/Caddyfile` | Unknown | Audit, absorb or delete |
| 5.4 | `/root/compose/machine-law/Caddyfile` | Unknown | Audit, absorb or delete |
| 5.5 | `arif-sites/deploy/Caddyfile` | Separate (static sites) | Keep — not federation |

**Checklist before deleting A-FORGE Caddyfile:**
```
1. Verify arifOS/deploy/Caddyfile routes ALL required domains
2. Verify all ports match current runtime (8088, 8081, 18082, 18083, 7071, 7072, 3001, 3002)
3. Test reload: caddy validate && systemctl reload caddy
4. curl each endpoint to confirm routing works
```

---

## Phase 6: Go Tool Migration (P3 — NEXT CYCLE)

**Owners:** FORGE (000Ω) | Requires architectural review, not urgent

| Tool Group | Current | Target | Estimated Effort |
|------------|---------|--------|-----------------|
| Filesystem ops (5) | TypeScript in A-FORGE | Go module | 2-3 days |
| Git ops (4) | TypeScript in A-FORGE | Go module | 1-2 days |
| Docker ops (4) | TypeScript in A-FORGE | Go module | 1-2 days |
| Shell exec + log tail (2) | TypeScript in A-FORGE | Go module | 1 day |

**Architecture:**
```
A-FORGE MCP (port 7072, TypeScript)
  ├── Browser/gateway tools  → keep TS
  ├── Proxy/registry tools   → keep TS
  └── Go Subprocess          → Go binary, cmd/stdin MCP surface
        ├── forge_filesystem_read/write/glob/grep/stat
        ├── forge_git_status/diff/log/commit
        ├── forge_docker_ps/logs/exec/images
        ├── forge_shell_dryrun
        └── forge_log_tail
```

**Go binary runs as:** `/usr/local/bin/forge-system-mcp` (systemd-managed or child process of A-FORGE TS)

---

## Phase 7: Automation & Linting (ONGOING)

### Add to every repo's Makefile

```makefile
# Substrate audit
audit:substrate:
	@echo "=== SUBSTRATE AUDIT ==="
	@echo "Checking .md files for excessive code blocks..."
	@find . -name '*.md' -not -path '*/node_modules/*' -not -path '*/__pycache__/*' -not -path '*/.git/*' -not -path '*/dist/*' | while read f; do \
		lines=$$(grep -c '^```' "$$f" 2>/dev/null || echo 0); \
		if [ "$$lines" -gt 50 ]; then echo "WARN: $$f has $$lines code fence lines"; fi; \
	done
	@echo "Checking for JSON configs that should be YAML..."
	@find . -name 'fastmcp.json' -o -name 'mcp.json' -o -name 'claude_desktop_config.json' | while read f; do \
		echo "WARN: $$f should be .yaml"; \
	done
	@echo "Checking for JSON logs that should be JSONL..."
	@find . -name 'entropy-report.json' -o -name 'deploy_gate.json' -o -name '*_results.json' | while read f; do \
		echo "WARN: $$f should be .jsonl"; \
	done
	@echo "=== SUBSTRATE AUDIT COMPLETE ==="
```

### Pre-commit config

Add to `/root/.pre-commit-config.yaml`:
```yaml
- repo: local
  hooks:
    - id: substrate-audit
      name: substrate-audit
      entry: make audit:substrate
      language: system
      pass_filenames: false
```

### CI gate

Add to every repo's GitHub Actions workflow:
```yaml
substrate-audit:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Substrate Audit
      run: make audit:substrate
```

---

## Verify Checklist

After all migrations are complete:

- [ ] No `fastmcp.json`, `mcp.json`, `claude_desktop_config.json` files remain (all migrated to YAML)
- [ ] No `entropy-report.json` or `deploy_gate.json` files remain (all migrated to JSONL)
- [ ] No `.md` file has >50 lines of fenced code
- [ ] `federation.manifest.yaml` has correct ports (GEOX=8081, WELL=18083)
- [ ] `identity.toml` files all use canonical 5-section schema
- [ ] WEALTH `chain_upstream` points to arifOS (not A-FORGE)
- [ ] No hardcoded secrets in any config file
- [ ] Only 1 canonical Caddyfile exists
- [ ] All empty prometheus stubs deleted
- [ ] `make audit:substrate` passes cleanly on every repo

---

## Emergency Rollback

If any migration breaks a service:

1. **Identify the broken substrate.**
   - Config YAML not loading → revert to JSON, fix the parser first
   - Extracted code has test failures → revert the `.md`, fix the extraction, retry
   - Caddyfile wrong → `systemctl stop caddy && cp /root/backup/Caddyfile.bak /etc/caddy/Caddyfile && systemctl start caddy`

2. **Revert only the broken change.** Never revert in bulk.
3. **Log to VAULT999.** Use a seal entry with `"event": "substrate_migration_rollback"`.
4. **File an issue.** Tag `area:substrate-migration`.

---

## Conclusion

This GAUNTLET contains 7 phases, ~80+ individual migration tasks, and ~15 verification checkpoints. Each phase is designed to be independent — you can run Phase 1 without waiting for Phase 2.

The total effort is approximately **2-3 engineering weeks** distributed across Phases 0-4 (critical + config + JSON→JSONL). Phases 5-6 (Caddyfile + Go) are lower urgency.

**Start with Phase 0. Then Phase 1. Let the Makefile check tell you what's left.**

```
DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
```
