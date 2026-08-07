# AAA Federation Convergence Plan v0.1

> **Status:** DRAFT — execution plan, not policy
> **Reuses:** GAP_REPORT_v0.1 + ENFORCEMENT_MATRIX_v0.1 (same mission)
> **Authored:** 2026-08-07 by Hermes (hermes-asi)

---

## Purpose

Phased migration of the three currently-active harnesses
(Hermes / OpenCode / Kimi) to the canonical federation envelope
defined in ENFORCEMENT_MATRIX_v0.1.

Sequence honors E-21: Constitution → Protocol → Implementation.

- **Constitution** = AAA_FEDERATION_CONTRACT_v0.1.x (DRAFT, pending
  F13 ratification; this plan does not depend on its ratification
  becoming law — only on its structure being stable as audit target)
- **Protocol** = GAP_REPORT_v0.1 + ENFORCEMENT_MATRIX_v0.1 (this
  and companion) — the operational shape of existing invariants
- **Implementation** = phased, below

The plan only documents T1-T2 work. No T3 directly.

---

## Phase 1 — Per-harness E-22 close (the boring result)

For each active harness, prove: a real attempted mutation results
in either (a) an apex verdict + receipt, or (b) BLOCK with receipt.

### 1A — Hermes: K-02-equivalent

- **Objective:** prove Hermes `pre_tool_call` gate fires in the LIVE
  runtime (not just subprocess).
- **Steps:**
  1. Patch `/root/.hermes/profiles/aaa-hermes/config.yaml` (or
     equivalent active profile) to register
     `mutation_gate_hook.py` under `hooks: - event: pre_tool_call`.
  2. Restart Hermes gateway.
  3. Trigger a real `write_file` from a fresh agent invocation to
     a path outside allow-list. Verify `pre_tool_call` fires
     (tail `/root/HERMES/gate/receipts/hermes_actions.jsonl`).
  4. Verify the runtime halted the write (no file appeared) AND
     wrote a receipt with `decision: BLOCK`.
- **Reversible:** delete hook entry; restart; previous behavior.
- **Caveat:** requires Hermes gateway restart. Sovereign sign-off.

### 1B — OpenCode: live-fire validation

- **Objective:** catch a real T3 attempt through `judge-gate.ts`.
- **Steps:**
  1. From a fresh OpenCode session, run a `bash` tool call with
     command `rm -rf /root/.arifos` (or other catastrophic pattern).
  2. Verify `judge-gate.ts` returns `block: true` AND emits a
     receipt to `/root/.local/share/arifos/opencode_receipts.jsonl`.
  3. Confirm no destructive action occurred (file system intact).
- **Reversible:** no state change; just observability.

### 1C — Kimi: extend BLOCK_REASON coverage

- **Objective:** close secrets-path gap observed 2026-08-07
  (`cat /root/.secrets/...` was ALLOWED despite hook exit 2 working).
- **Steps:**
  1. Extend BLOCK_REASON table with patterns:
     - `kunci-mas`
     - `.secrets/`
     - `.signing_key`
     - `vault\.env` regex
  2. From a fresh Kimi session, attempt `cat /root/.secrets/kunci-mas.env`.
  3. Verify hook exits 2 AND emits block_reason including the
     secrets pattern.
- **Reversible:** revert BLOCK_REASON table; behaviour returns to
  current state.

### 1D — OpenClaw: instantiate empty envelope

- **Objective:** prove OpenClaw can emit a federation envelope.
- **Steps:**
  1. Configure OpenClaw to mint a session_id at startup.
  2. Configure to record at least one `/agent/receipt` per message.
  3. Trigger a message send via :18789. Verify receipt appears.
- **Caveat:** OpenClaw is a gateway; it does NOT mutate. Its job
  here is *witness*, not gate.

### 1E — AGY: spec the routing question

- **Objective:** produce the spec AGY must answer:
  - "Who should do this work?" (Think)
  - "Who should verify?" (Verify)
  - "Who should judge?" (Judge)
  - "Who should witness?" (Witness)
- Not implementing AGY — only producing the question it must
  answer.
- **Reversible:** pure documentation.

---

## Phase 2 — Inheritance closed (the spawn gap)

For each active harness, when parent → child occurs, the child
must carry the parent's `session_id`, `parent_receipt_id`, and
demoted `band`.

### 2A — Hermes spawn inheritance

- Extend `hermes_mutation_gate.py` with `evaluate_spawn` that
  validates the proposed child's envelope.
- Block any `delegate_task` whose `parent_session_id` is unset.

### 2B — OpenCode spawn inheritance

- Extend `judge-gate.ts` to validate envelope of `task` calls
  with priority order:
  - `task` (OpenCode internal subagent) must carry
    `parent_session_id`.
  - if missing → `block`.

### 2C — Kimi spawn inheritance

- Extend Kimi tool classification so that any `task` invocation
  in af-coordinator that omits `parent_session_id` is BLOCK.

### 2D — Spawn verifier

- A separate `audit_spawn.py` reads all three trails and reports:
  - spawns with parent_session_id set
  - spawns missing parent_session_id (FAIL)
  - orphaned parents (no child receipts)

---

## Phase 3 — Receipt chain integrity

### 3A — Receipt deduplication

- For every receipt emitted across all harnesses, ensure the
  `receipt_id` is canonical (sha256 of canonicalized payload).
  No local-only receipt IDs.

### 3B — Receipt-chain replay

- `tools/replay_vault.py` (already exists?) verifies chain
  integrity. Run weekly.

### 3C — Fail-closed verification

- Trigger a hook exception (e.g. SIGKILL hook process mid-decision).
  Verify runtime halts the action rather than proceeding.

---

## Phase 4 — Dormant harness onboarding

For Claude, Codex, Copilot, Grok: when reactivated, gate check
becomes mandatory. Their dormant state = unverified; this plan
does not require any action until they are rebooted.

---

## Sequence and dependencies

- Phase 1 is independent per harness; can run in parallel.
- Phase 2 depends on Phase 1 receiving at least one
  hermes_atomic_receipt (Hermes 1A succeeded).
- Phase 3 depends on Phase 2's spawn verifier (2D).
- Phase 4 is triggered only by reactivation.

---

## What this plan does NOT do

- Does not commit any new doctrine.
- Does not invent new invariants.
- Does not propose a deployment schedule.
- Does not require ratification of the AAA_FEDERATION_CONTRACT
  before phase 1 — the matrix is operational, not legal; the
  matrix is a way of BEHAVING the existing invariants, not
  amending them.
- Does not expose the federation to external integration.
- Does not change organ authority ceilings (all 8 unchanged).

---

## Phasing

| Phase | Goal                                            | Status |
|-------|-------------------------------------------------|--------|
| 1A    | Hermes runtime invokes pre_tool_call hook      | HOLD (sovereign sign-off) |
| 1B    | OpenCode live-fire catch of T3                  | READY (any agent can trigger) |
| 1C    | Kimi extends BLOCK_REASON with secrets patterns | READY (script-only edit) |
| 1D    | OpenClaw emits first envelope                   | HOLD (gateway config) |
| 1E    | AGY routing spec written                        | READY (pure doc) |
| 2A    | Hermes spawn inheritance validation             | READY |
| 2B    | OpenCode spawn inheritance validation           | READY |
| 2C    | Kimi spawn inheritance validation               | READY |
| 2D    | Spawn verifier reads all three trails           | READY |
| 3A    | Receipt ID canonical across harnesses           | HOLD (cross-harness) |
| 3B    | Weekly replay                                  | READY (cron job) |
| 3C    | Fail-closed verification                       | READY (synthetic T3) |

11 sub-actions. Most are READY (a single file edit). Three are
HOLD on sovereign authority: 1A (Hermes gateway restart), 1D
(OpenClaw gateway config), 3A (cross-harness canonicalization).
