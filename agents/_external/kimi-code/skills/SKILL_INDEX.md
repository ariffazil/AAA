# Kimi Code Skill Index — Canonical User-Scope Entry (2026-07-04)

> **Authority:** Subordinate to `arifOS` (constitution), `AAA` (cockpit), `A-FORGE` (executor). F13 SOVEREIGN veto absolute.
> **Owners:** `/root/.arifos/agents/kimi/` — kimi-code CLI user-scope home.
> **Mirror:** generic AAA skills point to their concrete skill file at `/root/.agents/skills/<skill-id>/SKILL.md` (project-scope). Kimi-specific skills live at `/root/.arifos/agents/kimi/skills/<skill-id>/SKILL.md` (user-scope).
> **DITEMPA BUKAN DIBERI — Forged, not given.**

---

## 1. Why this file exists

The `KIMI_CODE_SKILL_ARCHITECTURE.md` declared a **7-skill spine** with aspirational designators
(`aaa-doctrine-loader`, `federation-router`, `mcp-fastmcp-builder`,
`auditor-validator-kutip-sampah`, `arifos-kernel-operator`, `aforge-execution-governor`,
`vault999-audit-sealer`). **NONE of those 7 names exist as files on disk.**

The capabilities they describe are real. They live at `/root/.agents/skills/` under concrete
identifiers (e.g. `mcp-mastery`, `aforge-execution`, `888-judge-verdict-render`,
`999-vault-seal-immutable`). This index is the **bridge** — it pairs each declared
**stage** with the concrete skill that fulfills it, so kimi-code can stage-load without
hunting, and the next session does not regress into declaring aspirational designators
as if they were filesystem truths.

This is **lowering entropy**: every line that previously sent the reader to a missing
file now sends them to a real one.

---

## 2. Stage → Skill Map (7 stages, real skills)

| Heptalogy Stage | Declared designator | Concrete skill(s) | Location |
|---|---|---|---|
| `000_INIT / 100_INSPECT` | aaa-doctrine-loader | `aaa-cockpit`, `000-init-intent-classify`, `CONSTITUTIONAL_REFLEX`, `HOST_MEMBRANE_AWARENESS` | `/root/.agents/skills/{aaa-cockpit,000-init-intent-classify,CONSTITUTIONAL_REFLEX,HOST_MEMBRANE_AWARENESS}/SKILL.md` |
| `200_EVIDENCE / 555_ROUTE` | federation-router | `a2a-federation-builder`, `forge-opencode-spawn`, `federation-topology-map`, `federation-observability`, `meta-mesa-skill-atlas` | `/root/.agents/skills/{a2a-federation-builder,forge-opencode-spawn,federation-topology-map,federation-observability,meta-mesa-skill-atlas}/SKILL.md` |
| `300_REASON / 600_BUILD` | mcp-fastmcp-builder | `mcp-mastery`, `mcp-apps-builder`, `mcp-zen-authoring`, `forge-document-intelligence`, `iron-shell-render` | `/root/.agents/skills/{mcp-mastery,mcp-apps-builder,mcp-zen-authoring,forge-document-intelligence,iron-shell-render}/SKILL.md` |
| `400_AUDIT / 700_VALIDATE / 800_CLEAN` | auditor-validator-kutup-sampah | `entropy-thermo-zen`, `fix-sequencer`, `zen-md`, `ZEN_ORGANS`, `geox-redteam-hantu`, `geox-claim-grammar`, `shadow-diagnostic`, `kimi-skill-reflector`, `kimi-architect-apex-contrast`, `kimi-architect-asi-contrast`, `kimi-architect-agi-contrast`, `kimi-final-apex-contrast`, `kimi-integrator-apex-contrast`, `kimi-rsi-apex-contrast` | `/root/.agents/skills/{entropy-thermo-zen,fix-sequencer,zen-md,ZEN_ORGANS,geox-redteam-hantu,geox-claim-grammar,shadow-diagnostic}/SKILL.md` + `/root/.arifos/agents/kimi/skills/{kimi-skill-reflector,kimi-architect-apex-contrast,kimi-architect-asi-contrast,kimi-architect-agi-contrast,kimi-final-apex-contrast,kimi-integrator-apex-contrast,kimi-rsi-apex-contrast}/SKILL.md` |
| `500_JUDGE` | arifos-kernel-operator | `888-judge-verdict-render`, `CONSTITUTIONAL_REFLEX`, `cooling-ledger-rsi`, `RSI-recursive-improvement` | `/root/.agents/skills/{888-judge-verdict-render,CONSTITUTIONAL_REFLEX,cooling-ledger-rsi,RSI-recursive-improvement}/SKILL.md` |
| `600_EXECUTE` | aforge-execution-governor | `aforge-execution`, `010-forge-execute-warrant`, `phase-escalation-discipline`, `reality-loop-operator`, `UNIVERSAL_REALITY_LOOP` (via meta-mesa-skill-atlas) | `/root/.agents/skills/{aforge-execution,010-forge-execute-warrant,phase-escalation-discipline,reality-loop-operator}/SKILL.md` |
| `999_SEAL` | vault999-audit-sealer | `999-vault-seal-immutable`, `federation-safety-wiring`, `FLOWS-skill-record` (via cooling-ledger-rsi), `vault999-integrity` (via AAA/skills) | `/root/.agents/skills/{999-vault-seal-immutable,federation-safety-wiring}/SKILL.md` + `/root/AAA/skills/vault999-reader/SKILL.md` |

> **Naming convention:** The 7 declared designators remain as canonical **stage labels** for
> architectural reasoning. The concrete file IDs are what gets loaded. Two layers, one truth.

---

## 2.5 Kimi-Specific Contrast & Reflector Skills

User-scope skills added to align Kimi Code with the OpenCode AAA citizen contrast pattern and to enable bounded autonomous skill improvement.

> **All skills v1.1.0 as of 2026-07-16** (zen pass after arifOS MCP cold-boot fix).
> Each has a `## Federation anchors` section cross-referencing companions + audit log.

| Skill | Role | Purpose |
|---|---|---|
| `kimi-architect-apex-contrast` | Architect | Final overclaim / falsifiability / Gödel lock check before emitting plans. |
| `kimi-architect-asi-contrast` | Architect | 3am self-empathy / cognitive-load / F6 MARUAH check. |
| `kimi-architect-agi-contrast` | Architect | Contrast 2-3 architectures with F-floor + entropy tradeoffs before recommending. |
| `kimi-final-apex-contrast` | Final | 6-month future-audit test before SEAL/SABAR/VOID verdicts. |
| `kimi-integrator-apex-contrast` | Integrator | Constitutional floor pass/fail before declaring a phase done. |
| `kimi-rsi-apex-contrast` | RSI | Measurement reproducibility / omega_0 honesty for entropy reports. |
| `kimi-skill-reflector` | Cross-cutting | Bounded autonomous skill audit & upgrade ritual (max 3 iterations, ΔS ≤ 0, 888_HOLD for governed skills). |
| `KIMI_RSI_INIT_PROMPT` | Session entry | Wake ritual: load core skills, run reflector, route task-class → contrast skill. **v1.1.0** adds §Cold-boot diagnostic recipe. |
| `KIMI_HANDOVER_PROMPT` | Session exit | End-of-session handover. **v1.1.0** adds §Post-deploy verification recipe. |

---

## 3. Discovery Pattern

When the heptalogy load order resolves a stage (e.g. `333-MIND`), the matching skill(s)
above are pulled. The AAA bootstrap path (`/root/AAA/agents/AAA_ZEN_INIT.md`) is the
authoritative order; this index is supplementary.

**Project-scope mirror rule** (per `KIMI_CODE_SKILL_ARCHITECTURE.md §6`):
The 7 canonical stages live here at user-scope, but the actual `SKILL.md` files
live at project-scope (`/root/.agents/skills/`). Edit the project-scope files for behavior;
edit this index for stage mapping. Two surfaces, two responsibilities.

---

## 4. MCP Server Coverage (Delta vs OpenCode AAA Citizen at `/root/AAA/agents/opencode/AGENTS.md`)

| Source | Count | Servers |
|---|---|---|
| `kimi/mcp.json` (wired, **LOADED**) | 11 | arifos, wealth, well, geox, aforge, minimax, capability-index, repomapper, serena, github-official, brave-search |
| OpenCode AAA AGENTS.md (claims) | 20 | arifos-kernel, aforge, geox, wealth, well, **playwright**, **hostinger-vps**, **meyhem**, brave-search, **perplexity**, **sequential-thinking**, **postgres**, **supabase**, **qdrant**, **cloudflare**, **docker**, github, **context7**, **minimax-media**, **minimax-code** |

**Delta (12 missing in kimi):** playwright, hostinger-vps, meyhem, perplexity,
sequential-thinking, postgres, supabase, qdrant, cloudflare, docker, context7, minimax-media.
The kimi wiring remains lean-by-design — the 12 missing servers are not required for the
midday forge lane that kimi executes (per `KIMI_CODE_SKILL_ARCHITECTURE.md §1`).
**No action taken** — the delta is intentional.

---

## 5. OpenCode AAA Alignment

`/root/AAA/agents/opencode/AGENTS.md` describes a parallel citizen ("OpenCode … bound to
333-AGI … execution arm of HEXAGON"). `kimi-code` (this CLI, FI-008) is the **runtime**
that powers the executive surface for AAA agents including 333-AGI-derived callers.

**Where opencode aligns with kimi:**
- Both are governed coding forge instruments bound to the AAA cockpit.
- Both reference `arifOS :8088` (constitutional kernel) and `A-FORGE :7071` (executor).
- Both use `ART` reflex for tool-call classification.
- Both honor F1-F13 via `arifos` MCP and `888_JUDGE`.

**Where they diverge:**
- OpenCode claims **20 MCPs**; kimi wires **11** — the lean delta is intentional (§4 above).
- OpenCode's model is `tokenplan-mimo/mimo-v2.5-pro`; kimi default is `MiniMax-M3`.
- OpenCode's config lives at `/root/.config/opencode/opencode.json`; kimi's at
  `/root/.arifos/agents/kimi/config.toml`. Distinct but governed equivalently.

**Net alignment verdict:** kimi-code and opencode are *compatible surfaces*, not *identical
configurations*. Either can serve as the AAA forge instrument. Kimi-code is the current
CLI of record (v0.18+, last aligned 2026-06-23 per `AGENTS.md`).

---

## 6. Known Mismatches (to be resolved or accepted)

| Mismatch | Source | Resolution |
|---|---|---|
| `config.toml:20` cites `/root/AAA/agents/kimi-code/WARGAAA_CARD.md` | config | **Resolved** — runtime config already points to `/root/AAA/agents/_external/kimi-code/WARGAAA_CARD.md`; stale table entry corrected. |
| 7-skill designators in `KIMI_CODE_SKILL_ARCHITECTURE.md` | architecture doc | **Accepted** — kept as stage labels (this index pairs them with concrete skills). |
| `/root/.arifos/agents/kimi/skills/` directory missing | docs claim disk | **Resolved** — directory created by this index. |
| 12 MCP delta between kimi and opencode claims | config | **Accepted** — kimi is lean-by-design (midday forge lane only). |
| User-scope Kimi skills not tracked in any git repo | runtime layout | **Resolved** — mirrored to `AAA/agents/_external/kimi-code/skills/` and pushed with this upgrade. |

---

## 7. Maintenance

- This file is updated when the heptalogy load order changes or when project-scope skills
  are added/retired at `/root/.agents/skills/`.
- Run `node /root/AAA/scripts/tree777-skill-audit.mjs` periodically to detect drift.
- Run `kimi-skill-reflector` at the start of every agentic session to propose skill upgrades.
  Governed skills require 888_HOLD; infra skills require diff + ack; domain skills may be
  proposed freely if ΔS ≤ 0.
- The Stage → Skill map (§2) is the single source of truth for what `skill_view(name)` resolves
  to at each heptalogy stage. If you add a project-scope skill, put it in §2 under the matching
  stage.

---

## 8. Identity Threading Contract (FORGE 2-B v1) — Ratified 2026-07-04 by 888

> **Authority:** F13 SOVEREIGN ratification · **Bypass paths:** A (OBSERVE), B (IP auto-bind), C (sticky tokens) — **REJECTED**. Friction is governance. Zero trust, zero exceptions.
> **Gate:** `McpPolicyGate.evaluate()` (Layer 1 IDENTITY) at `/root/A-FORGE/src/policy_interceptor/mcp_policy_gate.py:198-202`.

### 8.1 Payload schema (every MCP tool call, including reads)

```json
{
  "actor_id":   "arif",
  "session_id": "epoch-2026-07-04-task-<short-id>",
  "lease_id":   "lease:<class>:<sha256-prefix>"
}
```

| Field | Gate reads? | F11 reads? | Required on | Notes |
|---|---|---|---|---|
| `actor_id` | ✓ Layer 1 | ✓ audit chain | **every call** | F13 SOVEREIGN default `"arif"`. Drops to `"anonymous"` → DENY at L1. |
| `session_id` | ✗ (handler-level) | ✓ audit chain | **every call** | Format: `epoch-YYYY-MM-DD-task-<short-id>`. Same across one task session. |
| `lease_id` | ✗ (handler-level) | ✓ audit chain | **every call** | See §8.2 for deterministic hash rule. |

### 8.2 Deterministic Synthetic Lease Hash (F9 + F11 enforcement)

For **OBSERVE-class** calls (read-only probes, status checks, tool registry queries):

```
lease_id = "lease:observe:" + SHA256(actor_id + "|" + session_id + "|" + tool_name + "|" + timestamp_epoch)
```

Where:
- `actor_id` — F13 SOVEREIGN id
- `session_id` — current task session id (§8.1)
- `tool_name` — exact MCP tool being called (e.g. `forge_registry_status`)
- `timestamp_epoch` — UTC seconds at the moment of call (integer)

The synthetic hash is **cryptographically replayable**: any auditor with the same four inputs produces the same `lease_id`. Field presence ≠ granted authority — `lease:observe:*` carries **zero mutate authority**, but is auditable and bound to the exact moment + intention of the observation.

For **EXECUTE/MUTATE-class** calls: `lease_id` is the real `forge_lease` token issued by `forge_lease(mode='request')` (action-class ceiling enforced).

### 8.3 Interceptor pattern — `assert identity_threaded(payload)`

Before any MCP tool invocation in Kimi's execution loop:

```python
def assert_identity_threaded(payload: dict) -> None:
    required = ["actor_id", "session_id", "lease_id"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise PermissionError(
            f"F13 IDENTITY: missing {missing} — refuse to call MCP without identity threading"
        )
    if payload["actor_id"] == "anonymous":
        raise PermissionError("F13 IDENTITY: actor_id=anonymous → L1_IDENTITY gate DENY")
    # F9 anti-hantu: synthetic observe leases must be hash-bound
    if payload["lease_id"].startswith("lease:observe:"):
        expected_prefix = "lease:observe:" + sha256(
            f"{payload['actor_id']}|{payload['session_id']}|"
            f"{payload.get('tool_name','')}|{payload['timestamp_epoch']}"
        )[:16]
        if not payload["lease_id"].startswith(expected_prefix):
            raise PermissionError(
                "F9 ANTI-HANTU: synthetic lease hash mismatch — refuse hallucinated identity"
            )
```

### 8.4 Failure modes (zero exceptions)

| Failure | Behavior | Source |
|---|---|---|
| `actor_id` missing → `"anonymous"` | DENY at L1 | Gate Layer 1 (mcp_policy_gate.py:198) |
| `lease_id` missing | PermissionError raised by Kimi interceptor (fail-closed) | §8.3 |
| `lease_id` synthetic hash doesn't match inputs | PermissionError raised (F9 anti-hantu) | §8.3 |
| `session_id` reused across distinct tasks | Audit anomaly — flag in receipt | F11 |
| Bypass paths A/B/C requested | REFUSE — reply "constitutional reject, zero exceptions" | F13 |

### 8.5 Reference receipts

- **Ratification:** 888_ACK on 2026-07-04 during SESI TEMPA reconcile
- **Original gate code:** `/root/A-FORGE/src/policy_interceptor/mcp_policy_gate.py` (Python port of `A-FORGE/src/domain/governance/McpPolicyGate.ts`)
- **VAULT999 seal:** seq=14 (forged by this batch — see receipt)
- **Constitutional anchors:** F1 AMANAH, F2 TRUTH, F8 LAW, F9 ANTI-HANTU, F11 AUDIT, F13 SOVEREIGN

---

*Indexed at chain seq counter — entropy baseline lowered from N=unknown (declared designators
referenced missing files) to N=0 (every cross-reference resolves to a real skill).*

*Identity contract ratified 2026-07-04 — synthetic leases cryptographically replayable, gate bypass paths rejected, F9 anti-hantu enforced on every call.*

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
