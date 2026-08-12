# AAA FEDERATION — TODO / CARRY-FORWARD

> Created: 2026-08-12 by 333-AGI
> Federation brain ALIVE: 25 models, 8 FI agents, e2e verified

## P0 — CRITICAL

### 1. Fix qwen-code (FI-003) Actor Binding — DONE 2026-08-12
- [x] Add "qwen-code": "operator" to exempt list in session_auth.py
- [x] Register qwen-code in agent_identities.json (canonical name, not qwen-code-fi003)
- [x] Install qwen-code binary
- [x] Restart kernel

### 2. Add All Missing FI Agents to Kernel Exempt List
File: /root/arifOS/arifosmcp/runtime/session_auth.py
Add after "openclaw": "operator",
"qwen-code": "operator", "codex": "operator", "copilot": "operator",
"copilot-cli": "operator", "gemini-cli": "operator", "grok": "operator",
"grok-build": "operator", "agy": "operator", "aider": "operator",
"continue-cli": "operator", "mesa-test-agent": "operator",

### 3. Register Missing Agents in agent_identities.json
- [x] qwen-code, opencode, claude-code, codex, copilot, copilot-cli, gemini-cli, grok, agy, aider, continue-cli, mesa-test-agent

## P1 — HIGH (Amber)

### 4. A-FORGE Deployment Drift
- [ ] cd /root/A-FORGE && pip install -e . && systemctl restart aforge

### 5. W3 Tri-Witness Threshold
- [ ] W3=0.7439 (0.006 below F3 threshold 0.75)

### 6. Fix FI Slot Conflicts
- [ ] FI-005: codex OR copilot-cli
- [ ] FI-009: agy OR skill-auditor

### 7. Assign FI Slots to Core Agents
- [ ] 333-AGI, 555-ASI, 888-APEX

## P2 — MEDIUM

### 8. Clean Up Duplicate Agent Cards
### 9. Upgrade Minimal Cards to v2.2.0
### 10. Create identity.json for Priority Agents

## CARRY-FORWARD
| Metric | Value |
|--------|-------|
| Last session | 2026-08-12, 333-AGI |
| Federation | ALIVE (25 models, 8 FI agents) |
| P0 open | 3 |
| P1 open | 4 |
| P2 open | 3 |
| arifFlow FQ | 13.14 OPTIMAL |
| Receipt | 64c3d3df-94e0-4182-a8cb-c5f85e49c71e |

DITEMPA BUKAN DIBERI
