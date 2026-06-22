# SUBSTRATE_MANIFEST — The 5-Layer Law

> **Canonical substrate architecture for the arifOS Federation.**
> MD = law. Schema = contract. Code = actuator. JSON = truth. YAML = posture.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
> **Sealed: 2026-06-21 | Ratified: F13 SOVEREIGN (Arif bin Fazil)**

---

## 0. THE INVARIANT

```
┌─────────────────────────────────────────────────────────────────┐
│  SUBSTRATE        ROLE              WHAT IT CARRIES              │
│                                                                   │
│  MD               Constitutional    Doctrine, law, ceremony,      │
│                   intent            constitution, floor policy    │
│                                                                   │
│  SCHEMA           Enforceable       JSON Schema, Zod types,       │
│  (JSON Schema)    contract          Tool inputSchema, registry    │
│                                                                   │
│  CODE             Actuator          Python (data/ML), TS (API),   │
│  (TS/Go/Python)   muscle            Go (system), SH (ops)        │
│                                                                   │
│  JSON             Runtime truth     State snapshots, receipts,    │
│                   packet            event lineage, vault entries  │
│                                                                   │
│  YAML             Human-tuned       Organ configs, Caddy,         │
│                   operating posture  Prometheus, systemd, CI      │
└─────────────────────────────────────────────────────────────────┘

  ▎ MD declares the law. Schema defines the contract.
  ▎ Code executes the capability. JSON carries the truth.
  ▎ YAML tunes the posture.

  NO substrate may serve another substrate's role.
  This is the constitutional separation of concerns.
```

---

## 1. MD — Constitutional Intent (Markdown)

### What belongs in Markdown

| Content | Examples | Must NOT contain |
|---------|----------|------------------|
| Constitutional floors | `F1_AMANAH.md`, `F13_SOVEREIGN.md` | Executable code |
| Doctrine | `SOUL.md`, `IDENTITY.md`, `AGENTS.md` | JSON schemas >10 lines |
| Agent instructions | `CLAUDE.md`, `BOOTSTRAP.md` | YAML config values |
| Architectural narrative | `ADR-*.md`, `ARCHITECTURE.md` | Full tool contracts |
| RUNBOOKs (operational prose) | `RUNBOOK.md`, `DEPLOYMENT_GUIDE.md` | Inline test suites |
| Audit reports | `FORGE_SEAL_*.md`, audit summaries | Database connection strings |
| Skill doctrine | `SKILL.md` (trigger + workflow) | Full program listings |
| Changelog narrative | `CHANGELOG.md` | Live credentials |

### Government policy for `.md` files

1. **Example code** in Markdown MUST be short (<10 lines), illustrative, non-executable fragments.
   - ❌ A 30-line Python class definition with methods
   - ✅ A 3-line pseudocode snippet showing the algorithm shape
2. **Schema examples** in Markdown MUST be minimal (≤5 fields) to show shape only.
   - ❌ The full 40-field `ArtRequest` JSON Schema
   - ✅ `{"action_class": "MUTATE", "blast_radius": "low"}`
3. **Config examples** MUST use placeholders, never real values.
   - ❌ `port: 8088` in a config table
   - ✅ `port: <ORGAN_PORT>` or a pointer to the canonical config
4. **Every `.md` file with >20 lines of fenced code** is a violation — extract to proper substrate.
5. **NOTE:** RUNBOOK files are an exception — they may contain executable shell commands because `RUNBOOK.md` IS the canonical operation record. The distinction: RUNBOOK commands tell a human what to type; they are not loaded by any runtime.

### Enforcement

A `make audit:substrate` check will flag any `.md` file with:
- >50 total lines of fenced code blocks (all languages combined)
- Any code block >30 lines
- Any JSON file embedded in a `.md` file (the canonical location is `schemas/*.json`)

---

## 2. SCHEMA — Enforceable Contract (JSON Schema / Zod / TypeScript types)

### What belongs in Schema

| Content | Format | Location |
|---------|--------|----------|
| MCP tool inputSchema | JSON Schema | `schemas/<organ>/` or inline in server code |
| Tool output contract | JSON Schema / Zod | `contracts/<organ>/` |
| Tool registry shape | JSON Schema | `registry/*.schema.json` |
| ArtRequest dataclass | Zod / Pydantic | `arifosmcp/runtime/art.py` |
| Envelope/transport schema | JSON Schema | `contracts/transport/*.json` |
| Verdict schema | JSON Schema | `contracts/verdict_contract.json` |
| Receipt schema | JSON Schema | `schemas/receipt.schema.json` |
| Vault event schema | JSON Schema | `schemas/vault999_event.schema.json` |

### Cardinal rule

**Schema is the bridge between MD and Code.** ART checks schema before PROCEED. ACT verifies schema after EXECUTE. If schema is out of sync with code, the system is broken.

- Schema MUST be the single source of truth for data shape.
- Code MUST validate against schema (Pydantic, Zod, JSON Schema validators).
- Schema drift between layers is an F2 TRUTH violation.

---

## 3. CODE — Actuator Muscle

### Optimal language per tool domain

| Tool Domain | Optimal Language | Organs | Rationale |
|-------------|-----------------|--------|-----------|
| Constitutional governance | Python | arifOS | Reasoning, session, memory, vault — analytic |
| Scientific computation | Python | GEOX, WEALTH, WELL | NumPy, SciPy, PyTorch, domain libraries |
| Financial analysis | Python | WEALTH | numpy-financial, riskfolio, pymc |
| Biometric assessment | Python | WELL | Data analysis, state management, scoring |
| Web API gateway | TypeScript / Node.js | AAA a2a | REST, JSON-RPC, A2A protocol, webhooks |
| Web automation | TypeScript | A-FORGE | Playwright, browser agents, structured I/O |
| API wrappers | TypeScript | A-FORGE | GitHub, search, cloud APIs |
| **Filesystem operations** | **Go** | A-FORGE | Zero-copy reads, file I/O, bulk operations |
| **Git operations** | **Go** | A-FORGE | Git plumbing, diff, merge, status |
| **Docker operations** | **Go** | A-FORGE | Container lifecycle — Docker itself is Go |
| **Shell/process management** | **Go** | A-FORGE | Process spawn, timeout, signal handling |
| **Log streaming** | **Go** | A-FORGE | Journalctl, tail, structured log parsing |
| System orchestration | Go | All (future) | MCP servers, network, background daemons |
| Operator scripts | Shell / Bash | All | One-shot setup, cron, deploy glue |

### Migration queue (from audit)

| Priority | Tool Group | Current | Target | Reason | Effort |
|----------|-----------|---------|--------|--------|--------|
| P3 | A-FORGE filesystem (5 tools) | TS | Go | File I/O, bulk ops, zero-copy reads | Medium |
| P3 | A-FORGE git (4 tools) | TS | Go | Git plumbing, system-level operations | Medium |
| P3 | A-FORGE docker (4 tools) | TS | Go | Container orchestration (Docker is Go) | Medium |
| P3 | A-FORGE shell + log (2 tools) | TS | Go | Process management, journalctl streaming | Low |

**~15/77 A-FORGE tools (19%) would benefit from Go migration. No urgent migrations — architectural improvement cycle.**

### Code rules

1. **Python tools MUST use FastMCP** framework (not raw Starlette/Express).
2. **TypeScript tools MUST use `@modelcontextprotocol/sdk`** for MCP compliance.
3. **Go tools MUST expose an MCP-compatible surface** (JSON-RPC over stdio or HTTP).
4. **Every tool MUST declare its `inputSchema`** — no untyped tools.
5. **Pydantic v2** for all Python schemas. **Zod** for all TypeScript schemas.
6. **No tool exceeds 500 lines** without decomposition (enforced by ART reflex).

---

## 4. JSON — Runtime Truth Packet

### What belongs in JSON

| Content | Format | Location | Rotation |
|---------|--------|----------|----------|
| Runtime state snapshots | `.json` | `data/*.json`, `state/*.json` | Overwrite on change |
| Vault chain receipts | `.json` | `core/vault999/seals/` | Append-only, retention: permanent |
| Tool registry snapshots | `.json` | `registry/*.json` | Overwrite on deploy |
| Package manifests | `package.json` | Each repo root | Git-managed |
| Lock files | `package-lock.json` | Each repo root | Auto-generated |
| Agent card / discovery | `.json` | `static/*.json`, `agent-cards/` | Git-managed |
| **Event logs** | **`.jsonl`** | `logs/*.jsonl` | **Append-only, rotate daily** |
| **Entropy reports** | **`.jsonl`** | `entropy/*.jsonl` | **Append-only, rotate weekly** |
| **Deploy gate logs** | **`.jsonl`** | `logs/deploy_gate.jsonl` | **Append-only, rotate monthly** |
| **Eval results** | **`.jsonl`** | `eval/output/*.jsonl` | **Append-only, rotate per run** |
| **Test results** | **`.jsonl`** | `logs/test_results.jsonl` | **Append-only, rotate per run** |
| CONFIG values (any) | **YAML** | `config/*.yaml` | **JSON is FORBIDDEN for config** |

### JSON vs JSONL

| Feature | `.json` | `.jsonl` |
|---------|---------|----------|
| Structure | Single document | One JSON object per line |
| Append-friendly | No — must rewrite entire file | Yes — `>>` append |
| Best for | State, schema, manifests, receipts | Logs, events, entropy, eval output |
| Rotation | Manual or overwrite | `logrotate` friendly |
| Search | Needs full parse | `grep` line-by-line |

### Enforcement

All `.json` files classified as LOG must be converted to `.jsonl`:
- `/root/arifOS/logs/amanah_results.json` → `logs/amanah_results.jsonl`
- `/root/arifOS/logs/e2e_2026-04-22.json` → `logs/e2e.jsonl` (with rotation)
- `/root/A-FORGE/entropy-report.json` → `entropy/entropy.jsonl`
- `/root/A-FORGE/scripts/apex_battery_results/summary.json` → `logs/apex_probes.jsonl`
- `/root/AAA/eval/output/aaa_eval_results.json` → `eval/output/aaa_eval.jsonl`
- `/root/geox/entropy-report.json` → `entropy/entropy.jsonl`
- `/root/WEALTH/entropy-report.json` → `entropy/entropy.jsonl`
- `/root/WELL/entropy-report.json` → `entropy/entropy.jsonl`
- `.hermes/skills/.usage.json` → `logs/skill_usage.jsonl`
- `.hermes/skills/a3-selftest/state/fleet_*.json` → `logs/fleet_selftest.jsonl`

### CRITICAL: Security

- `/root/.hermes/google_token.json` — contains live OAuth tokens. **Emergency: rotate immediately, move to SOPS-encrypted secrets.**
- All config files in JSON (`mcp.json`, `fastmcp.json`, `claude_desktop_config.json`, etc.) — migrate to YAML.

---

## 5. YAML — Human-Tuned Operating Posture

### What belongs in YAML

| Content | Examples | Current Status | Action |
|---------|----------|----------------|--------|
| Organ identity | `identity.toml` | ✅ All 4 organs have it | Standardize to 5-section schema |
| Federation manifest | `federation.manifest.yaml` | ⚠️ Stale ports/tool counts | Fix GEOX=8081, WELL=18083 |
| MCP server config | `fastmcp.json`, `mcp.json` | ❌ 6 files in JSON | Migrate to YAML |
| Claude desktop config | `claude_desktop_config.json` | ❌ JSON | Migrate to YAML |
| Provider/model config | `config/PROFILES/*.json` | ❌ 10+ files in JSON | Migrate to YAML |
| Caddyfile | `deploy/Caddyfile` | ✅ Already Caddyfile format | Deduplicate (5 copies → 1 canonical) |
| Prometheus config | `prometheus.yml` | ✅ AAA copy is canonical | Delete empty arifOS stubs |
| Systemd units | `*.service` | ✅ Already `.service` format | Canonicalize in `/etc/` |
| Docker Compose | `docker-compose.yml` | ⚠️ 2 rival compose files | Reconcile or delete stale |
| Agent config | `opencode.json`, `.mcp.json` | ❌ JSON | Migrate to YAML |
| Organ intent map | `organ_intent_map.yaml` | ✅ Already YAML | Remove stale kubernetes refs |
| Cron definitions | `cron/jobs.json` (.hermes) | ❌ JSON | Migrate to YAML |
| Skill metadata | `.metadata.json` | ❌ JSON | Migrate to YAML (minimal) |

### Identity.toml canonical schema

All organs MUST use this 5-section identity structure:

```toml
[identity]
name = "organ-name"
role = "What this organ does"
sovereign = "Arif bin Fazil"

[network]
port = <PORT>
health_endpoint = "http://127.0.0.1:<PORT>/health"
mcp_endpoint = "http://127.0.0.1:<PORT>/mcp"
caddy_domain = "<organ>.arif-fazil.com"

[capabilities]
tools_count = <N>
floors = ["F1", "F2", ...]

[security]
chain_upstream = "parent-organ"  # arifOS has no upstream
chain_downstream = ["child-organs"]

[identity_hash]
method = "sha256"
value = "<hash-of-identity-fields>"
```

### Critical config fixes needed

| Finding | Severity | Action |
|---------|----------|--------|
| `federation.manifest.yaml`: GEOX port is 18081 (should be 8081) | CRITICAL | Fix port |
| `federation.manifest.yaml`: WELL port is 8083 (should be 18083) | CRITICAL | Fix port |
| `organ_intent_map.yaml`: kubernetes/k8s/pod keywords | HIGH | Remove — bare metal only |
| `organ_intent_map.yaml`: APEX still routed (decommissioned) | MEDIUM | Remove or mark legacy |
| `organ_intent_map.yaml`: Gateway has hardcoded API keys | CRITICAL | Move to env vars |
| `identity.toml` chain: WEALTH → A-FORGE (should be → arifOS) | HIGH | Fix chain_upstream |
| Caddyfile: 5+ copies, A-FORGE copy uses wrong ports | HIGH | Deduplicate, keep 1 canonical |
| `docker-compose.yml`: Hardcoded bot token + DB password | CRITICAL | Move to ${VAR} |
| `prometheus.yml`: 2 empty stubs in arifOS | MEDIUM | Delete |
| `identity.toml`: arifOS uses flat format (outlier) | MEDIUM | Standardize to 5-section |
| `smithery.yaml`: floor numbering mismatch (F01 vs F1), A-FORGE missing floors | LOW | Align |
| `federation.manifest.yaml`: last_verified 33 days stale | MEDIUM | Update |

---

## 6. ENFORCEMENT — The GAUNTLET

### Every session start

```bash
# 1. Bind the 5-substrate invariant
echo "MD = law | Schema = contract | Code = actuator | JSON = truth | YAML = posture"

# 2. Check the SUBSTRATE_MANIFEST exists
cat /root/AAA/SUBSTRATE_MANIFEST.md > /dev/null || (echo "MANIFEST MISSING" && exit 1)
```

### Every mutation, ask

1. **Which substrate am I writing to?**
   - `.md` → Is this doctrine, law, or narrative? If it's code/schema/config, WRONG SUBSTRATE.
   - `.py` / `.ts` / `.go` → Is this executable? Good. Is it >500 lines? Decompose.
   - `.json` → Is this state, receipt, or schema? If config, WRONG SUBSTRATE (use YAML).
   - `.jsonl` → Is this an event log? Good. Is it a `.json` that should be `.jsonl`? Convert.
   - `.yaml` / `.yml` → Is this config? Good. Is it hardcoded secret? Use env var.

2. **Is there already a canonical copy of this data in another substrate?**
   - If schema exists in both `.md` and `.json`, the `.md` copy is ROgue — delete it.
   - If config exists in both `.json` and `.yaml`, keep the `.yaml`, delete the `.json`.

3. **Does this file belong to the organ that owns it?**
   - `federation.manifest.yaml` lives in arifOS (the kernel owns the federation map).
   - `identity.toml` lives in each organ repo.
   - `Caddyfile` lives in arifOS (the kernel serves as reverse proxy).

### Pre-commit check

Every repo MUST have a pre-commit hook that validates:

```
1. No .md file with >50 lines of fenced code → WARN
2. No .md file with >30 lines in a single fenced block → WARN
3. No config in .json that should be .yaml → WARN
4. No secrets hardcoded (gitleaks) → BLOCK
```

### Drift detection

`make audit:substrate` checks:
1. **Schema drift:** Does every MCP tool's actual I/O match its declared `inputSchema`?
2. **Config drift:** Does `federation.manifest.yaml` match live runtime ports?
3. **Identity drift:** Does each organ's `identity.toml` match its systemd unit and Caddy route?
4. **State drift:** Is WELL `state.json` fresh (<24h)?
5. **JSON→JSONL drift:** Are there `.json` files that should be `.jsonl`?

---

## 7. EXCEPTIONS

| Exception | Rationale | Expiry |
|-----------|-----------|--------|
| RUNBOOK.md may contain shell commands | Operational — tells humans what to type, not loaded by runtime | Permanent |
| SKILL.md may contain short code examples (≤10 lines) | Teaching material, not runtime code | Permanent |
| README.md may contain 1-line `curl` examples | Discovery/setup — minimal illustration | Permanent |
| vault999 seals in JSON are acceptable | Append-only, chain-anchored, immutable — not config | Permanent |
| `package.json`, `tsconfig.json`, `composio/registry.json` | Tool-mandated formats | Permanent |
| Grafana dashboard JSON | Tool-mandated format (Grafana imports JSON) | Permanent |
| ComfyUI workflow JSON | Tool-mandated format | Permanent |
| `pyrightconfig.json`, `railway.json`, `components.json` | Tool-mandated; minor footprINT | Accept with note |
| `forge_work/*.md` with long receipts | Operational transcripts — not doctrine | 90-day retention |

---

## 8. AUDIT SUMMARY (2026-06-21)

### Files counted: ~2,000+ across 7 repos + .agents + .hermes

| Violation | Count | Severity |
|-----------|-------|----------|
| `.md` files with executable code blocks (HIGH) | ~96 files | 🔴 Must extract |
| `.md` files mixing doctrine + tech spec (MEDIUM) | ~120 files | 🟡 Should split |
| `.md` files with RUNBOOK-level commands (LOW) | ~147 files | ⚪ Acceptable |
| `.json` config files that should be `.yaml` | ~51 files | 🟡 Migrate |
| `.json` log files that should be `.jsonl` | ~10 files + 11 test fleet files | 🟡 Convert |
| CRITICAL config errors (ports, hardcoded secrets, OAuth tokens) | 11 findings | 🔴 Fix immediately |
| Tools in wrong language (should be Go) | ~15 A-FORGE tools | 🟢 P3 improvement |
| Secret exposure (plaintext tokens) | 3 locations | 🔴 Rotate & encrypt |

### Top 10 files needing immediate extraction

| Rank | File | Current | Should Be | Substrate |
|------|------|---------|-----------|-----------|
| 1 | `arifOS/static/arifos/theory/000/000_LAW_v2026.03.07.md` | 20+ code blocks in constitutional doc | `arifosmcp/core/floor_enforcement.py` | CODE |
| 2 | `arifOS/static/arifos/theory/000/ROOTKEY_SPEC.md` | Entire pytest test suite in markdown | `tests/constitutional/test_rootkey.py` | CODE |
| 3 | `A-FORGE/contracts/gateway-tools-v1.md` | 36 JSON tool contracts (80% of file) | `contracts/gateway-tools-v1.json` | SCHEMA |
| 4 | `A-FORGE/GENESIS/providers_yml_spec.md` | Full YAML spec in markdown | `providers.yml` | YAML |
| 5 | `WEALTH/docs/WEALTH_FEDERATED_AGI_DOMAIN_FIX_SPEC.md` | Entire Pydantic envelope.py in markdown | `internal/wealth_contracts/envelope.py` | CODE |
| 6 | `geox/docs/GEOX_PETROPHYSICS_BLUEPRINT.md` | Entire petrophysics schema in markdown | `src/geox_core/schemas/petrophysics.py` | CODE |
| 7 | `geox/docs/plans/NEXT_FORGE_PLAN.md` | Complete tool implementations + CI YAML | `src/geox_core/tools/*.py` + `.github/workflows/ci.yml` | CODE + YAML |
| 8 | `AAA/workspace/ARIF.md` | 13 consecutive Python enforcement blocks | `arifosmcp/core/floors.py` | CODE |
| 9 | `WELL/FEDERATION_HOOKS.md` | Complete function signatures for handoff tools | `server.py` (already exists — remove from .md) | CODE |
| 10 | `geox/docs/PHYSICS_ADAPTER_SPEC.md` | Complete `OpenQuakeAdapter` class code | `src/geox_core/physics/adapters/` | CODE |

---

## 9. THE TEST

A new agent lands on this federation and asks one question:
> "What substrate do I use for what?"

The answer is this manifest. One read.

| If you need to... | Use substrate | Because |
|-------------------|---------------|---------|
| Declare a constitutional floor | MD | Law is narrative |
| Define a tool's input shape | JSON Schema | Contract must be enforceable |
| Implement a tool | TS/Go/Python | Code actuates |
| Record what happened | JSON or JSONL | Truth must be machine-readable |
| Tune a port or endpoint | YAML | Humans edit config |
| Store a secret | SOPS/AGE env var | Never in any substrate |
| Log an event stream | JSONL | Append-only, rotatable |

---

## 10. SEAL

This manifest is ratified at the constitutional level.

- **Ratified by:** Arif bin Fazil (F13 SOVEREIGN)
- **Date:** 2026-06-21
- **Binding on:** All 7 federation organs, all 9 agent directories, all future forks
- **Enforcement:** `make audit:substrate` in every repo (pending CI integration)
- **Review cycle:** Quarterly or on any constitutional amendment

```
MD = law. Schema = contract. Code = actuator. JSON = truth. YAML = posture.
Tools cannot be MD because MD is law, not power.
DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
```
