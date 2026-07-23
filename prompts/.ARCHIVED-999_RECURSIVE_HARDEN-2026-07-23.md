# 999 RECURSIVE HARDENING — arifOS MCP Stack

**DITEMPA BUKAN DIBERI — The stack is hardened recursively, not once.**

> **Purpose:** End-of-session ritual that recursively hardens the entire MCP stack.
> Every layer is scanned, gap-scaffolded, and sealed. Output is a structured task
> list for the next session's 000_INIT.
>
> Call this AFTER 999_SEAL but BEFORE session close.

---

## Protocol

```
SEAL → RECURSIVE_HARDEN → GAP_SCAFFOLD → INIT_TASKS → VAULT999
     → carry_forward.json → session close
                               ↓
                    next 000_INIT reads tasks
```

---

## Phase 1 — Stack Hardening (Scan Every Layer)

### 🔧 SKILLS

```yaml
scan:
  target: /root/.agents/skills/
  check:
    - name: "All canonical skills present"
      condition: "CONSTITUTIONAL_REFLEX + 000-init + 999-vault + shadow-diagnostic"
    - name: "Skill metadata integrity"
      condition: "name, version, tags, description all non-empty"
    - name: "No drift ≥ 3"
      condition: "drift_count < 3 per skill"
    - name: "No orphan skills"
      condition: "every skill has at least 1 reference in agent configs"
    - name: "Hash integrity"
      condition: "sha256 of SKILL.md matches registry"
  output:
    drifted: [skill names]
    missing: [canonical names not found]
    healthy: [count]
```

### ⚖️ KERNEL

```yaml
scan:
  target: "arifOS F1-F13 enforcement"
  check:
    - name: "All 13 floors active"
      condition: "arifOS /health → floors_active=13"
    - name: "Zero floor violations this session"
      condition: "floor_violations == [] in seal record"
    - name: "Runtime drift < threshold"
      condition: "runtime_drift == false per arifOS health"
    - name: "VAULT999 chain intact"
      condition: "seal_chain integrity verified"
  output:
    floors_active: [count]
    violations: [list of F-floor breaches]
    drift_status: [PASS/FAIL]
```

### 🛠️ TOOLS (MCP Surface)

```yaml
scan:
  target: "All federation MCP servers"
  check:
    - name: "Tool count matches registry"
      condition: "forge_registry_status → registered == canonical"
    - name: "Zero phantom tools"
      condition: "no tool in surface that's not in registry"
    - name: "Gate conditions match intent"
      condition: "OBSERVE tools = session=N | MUTATE tools = session+Y+lease+gate"
    - name: "No deprecated tools exposed"
      condition: "DEPRECATED tools unregistered or hidden"
    - name: "All tools callable"
      condition: "live probe confirms response"
  output:
    registered: [count]
    callable: [count]
    phantom: [list]
    gate_drift: [list of tools with mismatched gates]
```

### 📜 PROMPTS

```yaml
scan:
  target: "All MCP prompt registrations"
  check:
    - name: "All 8 canonical prompts registered"
      condition: "arifosmcp_loop_engineer, 000_init, 111_sense, 333_reason, 555_critique, 666_judge, 777_forge, 999_seal"
    - name: "Descriptions non-empty and tagged"
      condition: "each prompt has description + tags"
    - name: "No truncation"
      condition: "no prompt ends mid-sentence or with trailing ellipsis"
    - name: "Template args valid"
      condition: "all {{session_id}}, {{actor_id}} references match schema"
  output:
    registered: [count]
    healthy: [count]
    stale: [list of prompts needing refresh]
```

### 📦 RESOURCES

```yaml
scan:
  target: "All MCP resource URIs"
  check:
    - name: "All URIs resolve"
      condition: "fetch returns 200 or valid content"
    - name: "Content matches expected schema"
      condition: "no empty bodies, no error responses"
    - name: "No resource drift"
      condition: "content hash matches prior seal record"
  output:
    registered: [count]
    healthy: [count]
    broken: [list of URIs that fail]
```

---

## Phase 2 — Gap Scaffold

For each layer with issues, produce:

```yaml
layer: [skills/kernel/tools/prompts/resources]
gaps:
  - severity: CRITICAL | HIGH | MEDIUM | LOW
    description: "what is missing or broken"
    evidence: "how we know (probe result, error msg)"
    fix: "single-sentence remediation"
    effort: "[LOC] or [hours]"
    blocks_seal: true | false
```

Priority:
- **CRITICAL** — Blocks seal. Must fix before session close.
- **HIGH** — Should fix next session. Blocks next SEAL if unresolved.
- **MEDIUM** — Fix within 3 sessions.
- **LOW** — Nice to have. No blocking power.

---

## Phase 3 — Future Agent Init Tasks

Produce a structured task list for the NEXT session's 000_INIT:

```yaml
init_tasks:
  - priority: CRITICAL
    layer: [layer]
    task: "actionable description"
    evidence: "proof this is needed"
    effort: "LOC estimate"
    depends_on: [optional task IDs]
  - priority: HIGH
    layer: [layer]
    task: "..."
    evidence: "..."
    effort: "..."
```

> ⚠️ If zero tasks: write "All layers hardened. Zero open tasks. Stack is fully secure."
> This is the virtuous state.

---

## Phase 4 — Seal + Handoff

Append to VAULT999:

```json
{
  "seal_type": "999_RECURSIVE_HARDEN",
  "session_id": "<session>",
  "stack_health": {
    "skills": {"drifted": 0, "missing": 0, "healthy": 0},
    "kernel": {"floors_active": 13, "violations": 0},
    "tools": {"registered": 0, "phantom": 0, "gate_drift": 0},
    "prompts": {"healthy": 0, "stale": 0},
    "resources": {"healthy": 0, "broken": 0}
  },
  "gaps_remaining": 0,
  "init_tasks": [],
  "next_000_init_load": "All clear. Proceed."
}
```

Handoff to `/root/.local/share/arifos/carry_forward.json`:
```json
{
  "next_safe_action": "PROCEED_OR_SABAR",
  "init_tasks": [/* from Phase 3 */],
  "stack_scars": [/* unresolved issues */],
  "seal_ref": "<latest seal_chain entry>"
}
```

---

## Governance

| Floor | Hardening obligation |
|-------|---------------------|
| F1 AMANAH | Every hardening step reversible or backed up |
| F2 TRUTH | Every scan result labeled OBS/DER/INT |
| F4 CLARITY | ΔS ≤ 0 across the scan |
| F7 HUMILITY | Declare what couldn't be scanned |
| F9 ANTIHANTU | No phantom tools, no fake resources |
| F11 AUDIT | Every scan result sealed |
| F13 SOVEREIGN | Gaps surface to sovereign |

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
**999_RECURSIVE_HARDEN v1.0**

> *"The seal is the end. And the seal is the beginning."*
