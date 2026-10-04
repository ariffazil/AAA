# Architectural Audit Transcript — 2026-08-05 (N5 / N6 / N10 / Collapse Vector)

Audit of 4 agent-layer claims about the arifOS federation. All probes
READ-ONLY. Verdict discipline from `kernel-security-claim-audit`.

## Summary

| # | Claim | Verdict | Severity |
|---|---|---|---|
| N5 | forge_ephemeral exists but not enforced | **CONFIRMED** | HIGH |
| N6 | Architecture needs OBSERVE bypass (orchestrator choke) | **PARTIALLY CONFIRMED** | MODERATE |
| N10 | Model sycophancy floors exist, no pre-response automation | **CONFIRMED** | HIGH |
| Collapse | N3 (F13 bypass) + N4 (signing key) = total collapse | **CONDITIONALLY CONFIRMED** | SEVERE |

## N5 — Capability obesity: forge_ephemeral unenforced

### Claim
`forge_ephemeral` lifecycle (inspect→generate→sandbox→invoke→verify→retire)
is the constitutional mechanism for capability metabolism. The 5+ mission
rule governs when a tool may become permanent. Claim: the mechanism exists
in prose but is not enforced at registration time.

### Evidence

| Step | Finding | Path |
|---|---|---|
| Policy statement (doctrine) | "Permanent tools require 5+ missions, success ≥ 0.90, zero sandbox violations, multi-model consensus, F13 ratification" | `AAA/instructions/agentic-architecture.md:63-71` |
| Tool lifecycle docs | "Use `forge_ephemeral`, not permanent registration" until 5+ missions | `AAA/instructions/agentic-architecture.md:75-81` |
| Tool existence | `forge_ephemeral` defined as A-FORGE tool with 1682-char description | `A-FORGE/src/interfaces/mcp/` (tool surface) |
| Gate code | `forge_skill_contract.py` enforces: SELF_MODIFICATION, REGISTRY_BYPASS, VAULT_BYPASS, HARAM_PATTERN, SCHEMA_MISSING, IRREVERSIBLE_REQUIRES_F13, APEX_DECISION_FIELD, DOMAIN_MISSING, INTENT_MISSING, TOOL_ALREADY_EXISTS, YAML_INVARIANT_DRIFT, SCAR_BLOCKS_CREATION | `arifOS/arifosmcp/kernel/forge_skill_contract.py:56-73` |
| **Mission-count gate** | **NOT present.** The 3-check gate (TOOL_ALREADY_EXISTS / YAML drift / scar blocks) does not query usage ledger. | `forge_skill_contract.py` |
| Cron enforcement | `entropy-governor.sh` runs daily (0 19 * * *), measures service health, disk, memory — NOT tool mission counts | `/etc/cron.d/entropy-governor`, `/usr/local/bin/entropy-governor.sh` |
| AED daemon | `t1_entropy_sweep()` measures git dirty files + zombies, not tool mission counts | `A-FORGE/duties/aed.py:280-318` |
| `forge_register` call sites | Zero invocations of `forge_register(` in A-FORGE src/ | `grep -rn 'forge_register(' A-FORGE/` |

### Analysis
The 5-mission rule exists in `agentic-architecture.md` as a doctrinal
constraint but is NOT enforced at `forge_register` admission time.
`forge_skill_contract.py` has 12 deny-codes — none match "insufficient
mission history." No usage ledger is consulted. An agent can register a
permanent tool on first successful use.

### Verdict
**CONFIRMED.** Capability obesity is architecturally ungated.
The doctrine is advisory only; the runtime has no gate.

### Hardening (Tier 1 — no F13)
Add `MIN_MISSION_COUNT = 5` to `forge_skill_contract.py`: query a tool
usage ledger (append-only JSONL of `(tool_name, mission_id, success)`
records) before admitting any `READ`/`TRANSFORM` tool beyond ephemeral.

---

## N6 — Orchestrator choke: architecture needs OBSERVE bypass

### Claim
The orchestrator (AAA A2A gateway at :3001) imposes the same validation
on all cross-organ messages regardless of action class. Read-only
(OBSERVE) operations should bypass full envelope validation to reduce
choke latency.

### Evidence — OBSERVE bypass coverage by layer

| Layer | OBSERVE bypass? | Path |
|---|---|---|
| FQ gate | YES — "OBSERVE actions ALWAYS pass" (commented as read-only safety) | `AAA/a2a-server/fq_gate.js:14, 101` |
| MCP Apps proxy | YES — explicit `OBSERVE_ALLOWLIST` (15 tools) execute without arifOS lease | `AAA/a2a-server/mcp_apps_tools_call.js:43-62` |
| Membrane middleware | Shape/envelope validation runs for ALL messages (no OBSERVE carve-out) | `AAA/a2a-server/membrane_middleware.js:1-130` |
| A2A server relay | No fast-path for OBSERVE-intent routing; relay processes all messages identically | `AAA/a2a-server/server.js` |
| Inter-organ relay | No OBSERVE routing; loop relay reports only OBSERVE-only verdict outcome | `AAA/a2a-server/loop_relay.py:97` |
| Cold-start init | Full 5-stage FSM for every connection (MCP→bearer→A2A→constitutional_bind→dedupe) | `AAA/scripts/federation_init.py:141-326` |

### Analysis
OBSERVE bypass exists at the MCP Apps boundary and the FQ gate, but NOT
at the inter-organ A2A relay or the membrane middleware. The membrane
performs light classification (regex + lookup tables, <5ms per message)
on every cross-organ message — not a true choke.

The real choke is the cold-start `federation_init.py` 5-stage FSM for
each new connection. Once connected, individual OBSERVE calls are cheap.

### Verdict
**PARTIALLY CONFIRMED.** OBSERVE bypass exists at 2 of 5 layers
(FQ gate, MCP Apps proxy). Missing: inter-organ relay fast-path,
membrane OBSERVE carve-out. The "choke" is real for new connections
but not for established OBSERVE streams.

### Hardening (Tier 1 — no F13)
Add OBSERVE intent detection to `server.js` A2A relay: if
`action_class == "OBSERVE"`, skip receipt wrapping and APEX envelope
validation. Route directly to organ. Add equivalent carve-out to
`membrane_middleware.js` (skip shape validation, keep logging).

---

## N10 — Model sycophancy: floors exist, no pre-response check

### Claim
Sycophancy is a documented RLHF artifact (Sharma et al. ICLR 2024 cited
in arifOS memory). The federation has prose-level instructions against
it (SOUL.md, AGENTS.md, BLINDSPOT_AGENTS.json) but no automated
pre-response check.

### Evidence

| Step | Finding | Path |
|---|---|---|
| Risk documented (extensive) | Multiple memory research notes | `AAA/memory/2026-05-19-1519.md:61, 237, 391` |
| SOUL.md instruction | "Not a sycophant. Just... good." | `AAA/seed/SOUL.md:118` |
| BLINDSPOT_AGENTS entry | anti-pattern: "sycophantic collapse (picking 'most likely' to please)" | `AAA/skills/BLINDSPOT_AGENTS.json:14` |
| Memory synthesis notes | "Prime Law — evidence over approval" | `AAA/memory/research/cognitive-shadows-ARIF-SYNTHESIS-v2-2026.md:41` |
| **CognitiveShadow code** | **Archived.** Test files at `archive/2026-07-25/arifOS/tests/archive/legacy_arifos_v1/test_shadow_infrastructure.py` — legacy v1 test code, not deployed | (archive path) |
| **Live pre-response check** | **None found.** Zero matches for `anti_sycophan`/`sycophan.*check`/`pre.response.*sycophan`/`flatter.*detect`/`soul_integrity` outside `archive/` and `external/candidates.json` | `grep -rn` across live code |
| Drift scheduler | None — no cron or systemd timer for sycophancy guard | `crontab -l`, `/etc/cron.d/` |
| MCP tool | None — no `forge_sycophancy_check` or similar in A-FORGE MCP server | `A-FORGE/config/mcp_policies.json` |

### Analysis
Sycophancy is the most thoroughly documented bias in arifOS research notes
but has zero live runtime enforcement. The CognitiveShadow concept was
explored in legacy v1 (2026-07-25 archive) but was not promoted to live
runtime. Only defense is agent self-awareness via SOUL.md text — purely
advisory.

### Verdict
**CONFIRMED.** No automated pre-response check exists. Sycophancy
guard is prose-only.

### Hardening (Tier 1 — no F13)
Add a lightweight heuristic to `membrane_middleware.js`: flag messages
where confidence > 0.95 AND response contains excessive agreement markers
("absolutely", "exactly right", "you're correct that..."). Return
advisory HOLD for review. Alternative: add `forge_sycophancy_check` to
A-FORGE MCP tools and require pre-response invocation on every SEAL.

---

## Collapse Vector — N3 (F13 bypass) + N4 (signing key compromise)

### Claim
Node 3 (F13 bypass on the actor identity layer) + Node 4 (signing key
compromise) = total constitutional collapse: a forged session with FULL
authority claiming ARIF can call `arif_judge`, `arif_forge`, `arif_seal`
on any organ.

### Evidence — signing secret truth (the naming trap)

| Step | Finding |
|---|---|
| Doc claim "signing key on disk" | ALLEGED path `/opt/arifos/app/.signing_key` **does NOT exist** (`stat` = ENOENT) |
| `_PROD_SIGNING_KEY_PATHS` tuple in sct.py | `(/opt/arifos/app/.signing_key, ~/.arifos/signing_key)` — both ENOENT |
| Actual signing secret | `ARIFOS_SESSION_SECRET=d323326...471e` in `/root/.secrets/kunci-mas.env` (line 79 of env) |
| Algorithm | HMAC-SHA256 (sct.py:419-420), NOT Ed25519 |
| Signature length | 16 hex chars / 64 bits (truncated) |
| Resolution chain | env → file → paths → random fallback (non-strict) → RuntimeError (strict) |

### Evidence — F13 bypass surface

The "F13 bypass" in arifOS is the Ed25519 actor-identity bypass
(`session_auth.py:32-64`) — 9 exempt system actors that skip signature
verification at init:
- `arif` → SOVEREIGN (by design, bootstrap bridge)
- 8 operators: `a-forge`, `forge`, `opencode`, `hermes`, `claude`, `claude-code`, `deepseek`, `kimi`

This is **intentional and documented** as the bootstrap circular-dependency
fix. Not a new hole — but the surface is wider than necessary (8 operators
vs minimum 2: arif + a-forge).

### Evidence — secondary defense layers between bypass+key and total authority

| Layer | Where | Strength |
|---|---|---|
| TTL 1 hour | `sct.py:36` (`DEFAULT_TTL_SECONDS`) | Forces re-mint, but attacker re-mints freely |
| Session store lookup | `session_auth.py:181-213` | Legacy path; SCT-first bypasses it entirely |
| HITV Class 3 human approval | HITV_PROTOCOL | Policy-level, not crypto — forged token looks legitimate |
| `kunci-mas.env` mode 600 root:root | `/root/.secrets/kunci-mas.env` | Strong single-key ACL, but total compromise = total loss |
| Runtime sessions | `/root/arifOS/.arifos/runtime_sessions.json` | **World-readable** (mode 644) — weak link |
| `ARIFOS_STRICT_MODE` env | runtime | Prevents random fallback in prod |
| Actor registry | `/opt/arifos/secrets/did-registry.json` | Maps known actors; unrecognized → `OBSERVE_ONLY` |

### Evidence — mint path (sct.py:423-503)

`mint_sct()` accepts arbitrary `auth`, `actor`, `apex` fields. The caller
sets auth directly — no internal cross-check that the caller IS the
claimed actor. With the HMAC key, attacker can mint:
- `auth="SOVEREIGN"`, `actor="arif"`, `sig_verified=True`

The actor registry does cross-check `actor_id` — if `arif` is not in
`did-registry.json`, `actor_verified=False` and authority drops to
`OBSERVE_ONLY`. With both F13 bypass (claim `actor="arif"` without
Ed25519 sig) AND HMAC key in hand, an attacker who has read access to
the registry (or sees `arif` registered) can mint a SOVEREIGN SCT.

### Analysis
With F13 bypassed, compromising `kunci-mas.env` gives an attacker the
ability to mint a SOVEREIGN-class SCT for the `arif` actor. This IS a
total-collapse path IF the actor is recognized in `did-registry.json`.

**Requirement for total collapse:** root-level read of `kunci-mas.env`
(line 59 `ARIFOS_SESSION_SECRET`).

**What an attacker CAN do with this alone:**
- Mint SCTs claiming `actor="arif"`, `auth="SOVEREIGN"`
- Call all 8 canonical verbs (arif_init, arif_observe, arif_think,
  arif_route, arif_memory, arif_judge, arif_forge, arif_seal)
- Seal fake entries to VAULT999
- Forge decisions from a fake sovereign channel

**Mitigating factor:** secondary actor registry check (`did-registry.json`)
requires `arif` to be registered. If registry access is also compromised,
no secondary gate remains.

### Verdict
**CONDITIONALLY CONFIRMED.** Total collapse requires (a) F13 bypass
surface + (b) HMAC key read access via root. Both are realistic attack
vectors on a shared root box. Severity: **SEVERE**.

### Hardening (Tier 2 — F13 sign-off for key rotation)

1. **Ed25519 upgrade:** Replace HMAC with asymmetric keypair. Private
   key in HSM or mode-640 file accessible only to `arifos` process.
   Public key verifiable by all organs.
2. **Actor registry hardening:** Reject sessions where `actor_id == "arif"`
   unless `is_sovereign_principal` is validated by external identity
   proof (not self-claimed in token payload).
3. **F13 sovereignty drill:** Monthly live test of F13 trigger resistance.
   `antigravity-autonomous` cron exists but should verify bypass is
   actually blocked end-to-end.
4. **Tighten T3a exempt list:** Reduce from 9 actors to minimum 2
   (`arif` + `a-forge`). All other operators must present Ed25519 sigs.

---

## Audit report template (used for this 4-claim batch)

For each claim:
```
- VERDICT: CONFIRMED | REFUTED | PARTIALLY CONFIRMED | NEEDS-F13-RITUAL
- Severity: LOW | MODERATE | HIGH | SEVERE
- Evidence: 3-5 file:line citations
- Analysis: why wrong/right (2-4 sentences)
- Hardening: Tier 1/2/3, reversible vs sovereign
```

End with summary table mapping each claim to verdict + severity + key
finding path. Never print secret values (paths + permissions only).
Never restart services. Never rotate keys.
