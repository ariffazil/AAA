---
name: drift-watch
id: drift-watch
version: 2.0.0
description: >
  Source-vs-runtime drift detection + live baseline comparison. Detect drift between
  federation source and runtime. Reads organ topology from canonical SOT, probes live
  health endpoints, compares git SHAs, and compares live state against saved baselines
  across tool manifests, agent cards, skill registries, and runtime-injected files.
owner: AAA
risk_tier: low
autonomy_tier: T0
floor_scope: [F1, F2, F4, F7, F11]
tags: [drift, watch, runtime, source, baseline, manifest, registry, probe, health]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Drift Watch — Source-vs-Runtime & Baseline Comparison

> **A service running is not the same as a service running what you think.**
> **DITEMPA BUKAN DIBERI** — Drift is invisible until it causes a bug.

## What This Skill Is

A unified drift detection skill covering two modes:

1. **Source-vs-Runtime Drift** — probe-based comparison of git source SHAs against deployed runtime SHAs using live organ registry data
2. **Baseline Drift Detection** — compare live state against saved baselines across tool manifests, agent cards, skill registries, and runtime-injected files

## When to Use

- After deploy, when organ behavior surprises you
- Weekly health audit, before any "is it running what I think?" question
- "Check drift", "verify registry", "detect manifest drift", "tool surface audit"
- "Runtime injection detection", "drift watch", "source vs runtime"

## When NOT to Use

- Curiosity probes without a specific concern
- When the task is about skill inventory (use `skill-inventory`)
- When the task is about incident response (use `incident-response`)

## §1. SOURCE-VS-RUNTIME DRIFT

### Canonical SOT

The organ registry at `/root/AAA/federation/organs.yaml` is the single source of truth for organ names, source paths, runtime locations, ports, and health endpoints. Read it FIRST.

```bash
python3 -c "
import yaml
with open('/root/AAA/federation/organs.yaml') as f:
    reg = yaml.safe_load(f)
for o in reg.get('organs', []):
    print(f'{o[\"id\"]} src={o.get(\"source_path\",\"?\")} runtime={o.get(\"runtime_path\",\"?\")} port={o.get(\"port\",\"?\")}')
"
```

### Steps

1. **Read organ registry** — gives source_path, runtime_path, and port for every organ

2. **For each organ** with a source_path:
   - `git -C <source_path> rev-parse HEAD` → source SHA
   - `cat <runtime_path>/.git_commit 2>/dev/null` → runtime SHA
   - Compare → if mismatch → DRIFT

3. **For each organ** with a port:
   - `curl -sf --max-time 2 http://localhost:<port>/health` → probe live health
   - Parse the software_release block for deployed_commit
   - Cross-reference with source SHA

4. **If DRIFT detected:**
   - Source newer than runtime → `make deploy-local` candidate
   - Runtime newer than source → runtime patch not in source → 888 HOLD
   - Runtime `.git_commit` missing → warn, treat source as truth

5. **Also check (from registry, not hardcoded):**
   - Caddy port map: `/etc/caddy/Caddyfile`
   - systemd units: `systemctl list-units --type=service | grep -E 'arifos|aforge|geox|wealth|well|aaa|arifflow'`
   - env file presence: `/root/.secrets/kunci-mas.env` (mode 600)

### Verification Loop

- Match → no action
- Mismatch → log + 888 HOLD with both SHAs + recommended action
- `.git_commit` missing → log warning, treat source as truth
- Organ DOWN → skip SHA comparison, flag in report

## §2. BASELINE DRIFT DETECTION

### Drift Dimensions

1. **Build vs Runtime Manifest Drift** — Canonical check via `arifOS/runtime/manifest.py`
2. **Tool Manifest Drift** — Live MCP tools vs registered tools vs agent card references
3. **Skill Registry Drift** — SKILL_ALIAS_TABLE vs actual directories vs agent card skill IDs
4. **Agent Card Drift** — Card skill IDs vs existing skill directories
5. **Schema Drift** — Tool input schemas vs documented schemas
6. **Floor Drift** — Declared floor_scope vs actual floor enforcement
7. **Verdict Taxonomy Drift** — Verdict emissions vs closed 6-value set

### Detection Pipeline

1. **Snapshot** — Capture current state of all registries
2. **Compare** — Diff against saved baseline (or last-known-good)
3. **Classify** — Each mismatch: CRITICAL (breaks routing), WARNING (orphan), INFO (cosmetic)
4. **Report** — Structured drift report with fix recommendations
5. **Escalate** — CRITICAL drift → 888_HOLD before any SEAL operation

### Runtime-Injected Files

Some organ services modify files at runtime:
- **WELL `index.html`**: WebMCP adapter injected on service start
- **arifOS session-state**: Runtime state files that change during operation

When dirty after clean commit: check if injected content was already committed → if yes, re-commit; if no, actual drift.

### Baselines

- **Canonical drift check**: `arifOS/runtime/manifest.py`
- Tool registry: `/root/arifOS/tool_registry.json`
- Agent cards: `/root/AAA/a2a-server/agent-cards/`
- Skill alias: `/root/AAA/skills/SKILL_ALIAS_TABLE.json`
- MCP surface: Live `tools/list` from each organ
- Verdict taxonomy: `arifOS/runtime/verdict.py`

## Failure Modes

- Runtime file missing → assume source is truth, surface to operator
- Mismatch in `.git_commit` only (cosmetic) → warn, don't HOLD
- Source repo not on `main` → flag, ask if intentional
- Registry unreachable → fall back to filesystem inspection of known paths

## Floors

- F1 AMANAH: Reversible-first. Drift correction must be reversible.
- F2 TRUTH: Report only what is actually observed. No inference without evidence.
- F4 CLARITY: Drift report must be actionable, not noise.
- F7 HUMILITY: Confidence cap. Uncertain drift → flag, don't assert.
- F11 AUDITABILITY: Every drift check logged with timestamp and findings.
