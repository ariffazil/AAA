# AAA_FEDERATION_GAP_REPORT — Convergence V1

> **Mission:** AAA_FEDERATION_CONVERGENCE_V1
> **Date:** 2026-08-07
> **Author:** Hermes (federation architect + verifier)
> **Doctrine:** Reuses AAA_FEDERATION_CONTRACT_v0.1 + AAA_EUREKA_DOCTRINE_v1. No new doctrine.
> **Method:** Live probes (ports, hooks, configs, receipts) — not self-reports.

---

## 1. Agent Inventory (live-verified)

| Agent | Runtime | State | Gate/Hook | Receipt path | Enforcement fired? |
|---|---|---|---|---|---|
| **Hermes** | hermes-agent (Telegram gateway, PID 3014600/3015207) | ACTIVE | ✅ `arifos-hermes-gate-hook.py` (pre_tool_call) | `/root/.local/share/arifos/hermes_hook_receipts.jsonl` | ✅ T3 blocked exit 2 (3 receipts) |
| **OpenCode** | opencode 1.18.11 (TUI) | ACTIVE | ✅ `arifos-judge-gate.ts` (tool.execute.before) | `/root/.local/share/arifos/opencode_receipts.jsonl` (10,173) | ✅ MUTATE + T3 fail-closed |
| **Kimi Code** | kimi-code 0.34.0 | ACTIVE | ✅ `aaa-witness-pre.sh` (PreToolUse, exit 2) | `/root/.agent-workbench/mcp-audit.jsonl` | ✅ Catastrophic patterns exit 2 |
| **OpenClaw** | openclaw-gateway (PID 1085689, :18789 + :8787) | ACTIVE | ❌ No gate/hook in config found | ❌ None found | ❌ No evidence of enforcement |
| **Codex CLI** | codex-cli v0.146.0 (config.toml present) | ACTIVE (config) | ⚠️ MCP + permission model (`workspace-write` + on-request) | ⚠️ Not verified | ⚠️ Not verified |
| Claude Code | — | DORMANT | — | — | — |
| Copilot CLI | — | DORMANT | — | — | — |
| Cursor | — | DORMANT | — | — | — |
| Gemini CLI | — | DORMANT | — | — | — |
| Aider | — | DORMANT | — | — | — |
| Qwen Code | — | DORMANT | — | — | — |
| AGY | — | NO CONFIG | — | — | — |
| Grok Build | `/root/.grok` dir exists | DORMANT | — | — | — |

---

## 2. Classification (per sovereign target architecture)

| Agent | Role | Class |
|---|---|---|
| Hermes | Reality sensing, governance observation | **SENSE** |
| Claude Code | Architecture, synthesis, specification | **THINK** (dormant) |
| Kimi Code | Adversarial audit, verification | **VERIFY** |
| AAA / arifOS :8088 | Constitutional judgment | **JUDGE** |
| OpenCode | Governed execution | **EXECUTE** |
| VAULT999 | Witness, attestation | **WITNESS** |
| AGY | Routing, coordination | **ROUTE** (no config — unbuilt) |
| OpenClaw | Cross-agent adversarial red-team | **RED-TEAM** (not yet configured as such) |
| Codex CLI | Software construction | **EXECUTE** (secondary) |
| Copilot CLI | Enterprise grounding, retrieval | **CLERK** (dormant) |
| Grok Build | Exploration, scouting | **SCOUT** (dormant) |

---

## 3. Constitutional Gaps (per E-22 lens: "can this agent mutate/delegate without AAA visibility?")

### GAP-01 — OpenClaw: no enforcement, no receipt
- **Evidence:** gateway live, but no gate/hook in `/root/.openclaw/` config; no receipt path found; no enforcement evidence.
- **Risk:** OpenClaw hosts 4 personas (main, opencode, codex, kimi) and has shell execution. A Telegram-triggered mutation could bypass AAA entirely.
- **E-22 answer:** YES — can mutate without AAA visibility.

### GAP-02 — Codex: enforcement unverified
- **Evidence:** config.toml has MCP servers + permission model, but no gate hook verified; no receipt trail found.
- **Risk:** `workspace-write` + on-request = agent can write broadly with only permission prompts (which are model-attested, not mechanical).
- **E-22 answer:** PROBABLY — permission prompts are memory/instruction-level, not mechanical gate.

### GAP-03 — Hermes T2 only witnessed, not blocked
- **Evidence:** K-02 blocks T3, but T2 (write_file, patch, terminal normal) → WITNESSED exit 0.
- **Risk:** T2 without arif_judge marker accumulates judgment debt silently (E-03, E-04).
- **E-22 answer:** PARTIAL — T3 NO, T2 YES (violates without receipt beyond witness line).

### GAP-04 — Kimi T2 + spawn not covered
- **Evidence:** PreToolUse matcher = `Bash|Shell|Write|WriteFile|Edit|StrReplace|StrReplaceFile` — no `task`/spawn matcher; T2 content writes only witnessed.
- **Risk:** subagent spawn from af-forge bypasses gate.
- **E-22 answer:** PARTIAL — catastrophic YES-blocked, spawn NO.

### GAP-05 — No cross-harness envelope
- **Evidence:** Hermes receipts, OpenCode receipts, Kimi audit.jsonl — three formats, no shared envelope (identity/authority/constraints/receipt_id/parent_receipt).
- **Risk:** provenance chain breaks across harnesses; INV-14 (receipt chain) unenforceable.
- **E-22 answer:** YES — a delegation spanning Hermes→OpenCode→Kimi loses traceability at each boundary.

### GAP-06 — No spawn inheritance anywhere
- **Evidence:** No harness propagates constraints to spawned children. Hermes delegate_task passes goal+context only; OpenCode task tool spawns subagents with permission blocks (static, not inherited); Kimi af-* no inheritance.
- **Risk:** parent governed, child ungoverned — the historical agent failure mode (K-04 concern).
- **E-22 answer:** YES — children can act outside parent's constraints.

### GAP-07 — Gate disable is silent everywhere
- **Evidence:** no `gate.disabled` receipt event exists in any harness schema.
- **Risk:** control exists → control disabled → nobody notices (bypass vector).
- **E-22 answer:** YES.

### GAP-08 — Dormant agents unbound
- **Evidence:** Claude/Codex/Copilot/Cursor/Gemini/Aider/Qwen/Grok/AGY have no enforcement when activated.
- **Risk:** any reactivation creates an ungoverned surface.
- **E-22 answer:** YES (on activation).

---

## 4. Canonical Federation Envelope (defined, not new doctrine)

Every agent action/delegation must carry:

```yaml
envelope:
  identity:     <agent_id>            # e.g. hermes, opencode-333-agi, kimi-af-forge
  authority:    <ceiling>             # OBSERVE_ONLY | DRAFT_ONLY | EXECUTE_REVERSIBLE | EXECUTE_AFTER_SEAL | DISPATCH_ONLY | JUDGMENT_ONLY
  classification: <OBSERVE|T1|T2|T3>
  constraints:  <inherited from parent or root>
  receipt_id:   <sha256-hex>
  parent_receipt: <sha256-hex or null>  # chain link (INV-14)
  harness:      <hermes|opencode|kimi|openclaw|codex|...>
```

## 5. Inheritance Requirements (parent → child)

```
parent envelope
  ├─ identity:      child receives parent.identity + ".child.<n>" (spawn lineage)
  ├─ authority:     child authority ≤ parent authority (never greater)
  ├─ classification: child must classify own actions (T1/T2/T3)
  ├─ constraints:   child inherits parent constraints ∪ spawn-time constraints
  ├─ receipt_id:    child receipt must reference parent receipt
  └─ harness:       child may differ; envelope shape must not
```

Rule: **Spawn without an envelope = denied** (K-04 principle, E-01).

## 6. Enforcement Matrix (T1/T2/T3)

| Tier | Definition | Required action | Fail-closed? |
|---|---|---|---|
| **T1** | Read-only / reversible local | Witness receipt only | No (allow) |
| **T2** | Recommendation or reversible mutation | arif_judge SEAL + receipt | Yes if arifOS down (HOLD) |
| **T3** | Irreversible / constitutional / secret | arif_judge SEAL mandatory + receipt | **Yes** — no judge, no mutation |

## 7. E-22 Analysis Summary

| Agent | Can mutate without AAA visibility? | Can delegate without AAA visibility? | Verdict |
|---|---|---|---|
| Hermes | PARTIAL (T3 no, T2 yes) | YES (delegate_task unwrapped) | GAP-03 |
| OpenCode | NO (gate + fail-closed) | PARTIAL (task now gated, no envelope) | GAP-05/06 |
| Kimi | PARTIAL (catastrophic yes, T2 no) | YES (no spawn matcher) | GAP-04 |
| OpenClaw | **YES** | **YES** | GAP-01 |
| Codex | PROBABLY | PROBABLY | GAP-02 |
| Dormant (8) | YES (on activation) | YES | GAP-08 |

**Federation E-22 verdict: PARTIAL — enforcement exists in 3/5 active, envelope in 0/5, spawn inheritance in 0/5.**

---

**Ω₀ ≈ 0.04. Confidence: 0.93 (live probes, not self-reports).**
**DITEMPA BUKAN DIBERI.**
