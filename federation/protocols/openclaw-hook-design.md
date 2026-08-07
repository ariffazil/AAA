# OpenClaw Pre-Mutation Hook (Phase 1 — close GAP-01)
# Mission: AAA_FEDERATION_CONVERGENCE_V1
# Owner: Hermes (architect) for F13 approval before live wire
# Date: 2026-08-07
# Status: DRAFT — pending F13 ratification

# Gap closed: GAP-01 (OpenClaw live gateway, zero enforcement, zero receipt)
# Before: E-22 YES — can mutate without AAA visibility
# After: E-22 NO — T3 blocked, T2 witnessed

# OpenClaw hook schema (from openclaw.json):
#   hooks.internal.entries
#   hooks.mappings: [{id, name, match, action, agentId, messageTemplate, deliver}]
#   hooks.allowedAgentIds: ["main"]

# Proposed mapping (add to hooks.mappings in openclaw.json):

id: aaa_federation_envelope_check
name: "AAA Federation Envelope Gate"
match:
  event: pre_mutation
action: agent
agentId: main
sessionKey: hook:aaa_envelope
wakeMode: now
deliver: false

messageTemplate: |
  FEDERATION ENVELOPE CHECK

  Verify envelope before mutation:
  - identity.agent_id: {agent_id}
  - authority.ceiling: {ceiling}
  - classification.tier: {tier}
  - judgment.verdict: {verdict}
  - receipt.parent_receipt: {parent}

  BLOCK if:
  - tier=T3 and verdict!=SEAL
  - tier=T3 and judge unavailable (fail-closed)

  WITNESS if tier=T2
  ALLOW if tier=T1 or OBSERVE

# Receipt path: /root/.local/share/arifos/openclaw_hook_receipts.jsonl
# Schema: shared with Hermes + OpenCode (federation_envelope.yaml)
# Reversibility: remove mapping from hooks.mappings → restore witness-only
# F13 decision: T2 territory — runtime change on live gateway

# Phase 1 VERIFIED (2026-08-07 by 333-AGI):
# 1. ✅ OpenClaw natively supports PreToolUse hook events
#    - Native hook relay: hooks-cli --event <event> --pre-tool-use-unavailable <mode>
#    - Internal events: "agent:bootstrap" pattern confirmed
#    - emitCodexNativePreToolUseFailureDiagnostic / nativePreToolUseFailures in source
# 2. ⚠️ Hook mapping format uses match.path, not match.event — design needs update
# 3. ⬜ Test with T3 command → expect BLOCK
# 4. ⬜ Confirm receipt written to openclaw_hook_receipts.jsonl
# 5. ⬜ Wire live (requires F13 approval — T3: production Telegram bridge)
#
# CORRECTED FINDING:
# The enforcement matrix reported "No gate/hook in config found" — this is accurate
# for CONFIGURED hooks, but OpenClaw HAS native PreToolUse hook capability.
# It needs a hook MAPPING added to openclaw.json hooks.mappings that intercepts
# PreToolUse events and routes to arifOS for constitutional floor check.
# 
# The existing opencode_thermodynamic_precheck mapping shows the pattern:
# match.path triggers → action:agent → agentId → messageTemplate → agent evaluates
# A similar pattern for PreToolUse would need: match.event (or match.path for
# native relay) → constitutional check → allow/witness/block decision.
