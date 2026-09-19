# Federation Shadow-Ack v2 — Audit-of-the-Audit Fix Receipt

## Trigger
Codex (audit-of-the-audit pass, 2026-09-19 ~13:30Z) found two latent bugs in the v1 federation pass:

**Bug 1 — qwen-code shadow entry split across 4 array entries**
Root cause: matrix probe regex `test("qwen"; "i")` matched both `qwen-code` (fq=0.25, state=STUCK) AND `qwen-code/FI-003` (fq=1.0, state=BALANCED). The two concatenated JSON objects got interpolated into multi-line variables, then the multi-line template string got split by `jq -R . | jq -s .` at newline boundaries — producing 4 fragments where 1 was intended.

**Bug 2 — covers_shadow_ids empty for 12 script-populated cards**
Root cause: script's `meta_json` builder didn't include the field. Only the hand-edited codex card linked to divergences.

## Fix
Script v1 → v2 patch:

| Change | Mechanism |
|---|---|
| Exact-match actor_id | `select(.actor_id == $a)` instead of `select(.actor_id \| test($a; "i"))` |
| Single-line matrix probe | Added `jq -c` flag + `head -1` so output is one compact JSON line, not multi-line stream |
| covers_shadow_ids populated | Universal `DIV-FEDERATION-SHADOW-ACK-CLOSED` + agent-specific (DIV-QWEN-CODE-STUCK-MATRIX, DIV-OPENCODE-FI-UNRESOLVED) |

## Execution trace (audit chain)
1. 13:30Z — codex flagged bugs in audit-of-the-audit
2. 13:48Z — script v2 patched; 12 cards reverted from .bak-v1 to pre-script state; re-run with v2 script
3. 13:50Z — qwen-code specifically re-run after second fix (jq -c + head -1) to capture real matrix values
4. 13:51Z — claude-code + grok-build specifically re-run for the same reason (their matrix entries had the same fragility)
5. 13:54Z — divergence registry updated: 3 new entries appended (DIV-FEDERATION-SHADOW-ACK-V2, DIV-QWEN-CODE-STUCK-MATRIX, DIV-OPENCODE-FI-UNRESOLVED)

## Final state — 13/13 cards

| Agent | Shadows | Well-formed | Real matrix values? |
|---|---|---|---|
| agy | 2 | yes | no matrix entry |
| aider | 3 | yes | no matrix entry |
| claude-code | 5 | yes | **YES** — state=BURNING, fq=0.079, execute_count=38 (v2 fix) |
| codex | 5 | yes | state=BALANCED (manual edit, pre-script) |
| continue-cli | 2 | yes | no matrix entry |
| copilot | 2 | yes | no matrix entry |
| copilot-cli | 2 | yes | no matrix entry |
| grok | 2 | yes | no matrix entry |
| grok-build | 5 | yes | **YES** — state=FOSSILIZED, fq=85.0, execute_count=6 (v2 fix) |
| kimi-code | 4 | yes | no matrix entry |
| mesa-test-agent | 2 | yes | no matrix entry |
| opencode | 6 | yes | no matrix entry (sparse_or_absent_matrix_record path) |
| qwen-code | 3 | yes | **YES** — state=STUCK, fq=0.25, execute_count=8 (v2 fix) |

0 fragments across the federation. All JSON valid.

## covers_shadow_ids coverage — full traceability

| Agent | covers_shadow_ids |
|---|---|
| codex (manual) | `[DIV-CODEX-SHADOW-SPARSE, DIV-CODEX-DUAL-HOME]` |
| opencode | `[DIV-FEDERATION-SHADOW-ACK-CLOSED, DIV-OPENCODE-FI-UNRESOLVED]` |
| qwen-code | `[DIV-FEDERATION-SHADOW-ACK-CLOSED, DIV-QWEN-CODE-STUCK-MATRIX]` |
| 10 other agents | `[DIV-FEDERATION-SHADOW-ACK-CLOSED]` |

## Divergences (now 13 in registry)

- DIV-FEDERATION-SHADOW-ACK-CLOSED — CLOSED (v1 — cards populated, audit chain preserved)
- DIV-FEDERATION-SHADOW-ACK-V2 — PARTIALLY_CLOSED (v2 script fix landed; F13 follow-ups remain)
- DIV-QWEN-CODE-STUCK-MATRIX — OPEN (operational: shadow-matrix says STUCK, exec=8 verify=2)
- DIV-OPENCODE-FI-UNRESOLVED — OPEN (F13: sovereign assigns opencode's FI slot — `???` placeholder in identity.json)
- DIV-CODEX-DUAL-HOME — OPEN (F13: collapse two codex dirs)
- DIV-CODEX-SHADOW-SPARSE — OPEN (sparse_history shadow waits for traffic to grow)
- + 7 unrelated existing entries

## Reversibility per card
```bash
# For v2-populated cards:
cp /root/AAA/agents/_external/<agent>/agent-card.json.bak-2026-09-19-shadow-ack-v1 /root/AAA/agents/_external/<agent>/agent-card.json
# For codex (original audit pass):
cp /root/AAA/agents/_external/codex/agent-card.json.bak-20260919-shadow-ack /root/AAA/agents/_external/codex/agent-card.json
# For deprecation-registry (current state with v2 entries):
cp /root/AAA/docs/deprecation-registry.json.bak-pre-v2-append /root/AAA/docs/deprecation-registry.json
```

## Trust class
DERIVED — federation audit chain, not externally witnessed. The fixes are mechanical and verifiable on disk. The two F13 follow-ups (opencode FI slot, codex dual-dir collapse) remain sovereign decisions.

## What's still imperfect (per codex's audit)
- claude-code, grok-build had parse errors during the v1 run that codex didn't separately flag; v2 fixed them silently as part of the fix pass.
- The sparse_history message ("too little signal") is suboptimal for BURNING and FOSSILIZED states — should mention the actual shadow-matrix verdict per agent. Not fixed in this iteration.
- opencode identity.json still has literal `???` placeholder; covered by DIV-OPENCODE-FI-UNRESOLVED but F13 action required.
