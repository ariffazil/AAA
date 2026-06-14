# OPERATOR PLAYBOOK — arifOS Federation
> **For:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Purpose:** How to operate, override, and protect the federation
> **Forged:** 2026-06-14 by FORGE (000Ω)
> **Load this whenever:** You need to understand how to control the agents.

---

## 1. UNDERSTANDING THE DASHBOARD

### Risk Levels (AAA Cockpit)

| Color | Meaning | What You Should Do |
|-------|---------|-------------------|
| 🟢 GREEN | Normal — agents operating within bounds | Nothing. Let them work. |
| 🟡 YELLOW | One anomaly, low severity | Read the anomaly description. Decide if it's real. |
| 🟠 AMBER | Multiple anomalies or medium severity | Investigate within the hour. Check which tool/agent triggered it. |
| 🔴 RED | Critical anomaly — recommend HOLD | 888_HOLD is actively recommended. Approve or override deliberately. |
| ⚫ BLACK | System integrity suspect — auto-HOLD triggered | Federation auto-paused. You MUST inspect before any agent resumes. |

### Organ Health Colors

| Color | Meaning |
|-------|---------|
| 🟢 HEALTHY | Organ responding, all tools available |
| 🟡 DEGRADED | Organ responding but some tools unavailable or slow |
| 🔴 OFFLINE | Organ not responding at all |

---

## 2. HOW TO APPROVE OVERRIDES

When an agent hits a HOLD and requests override:

### Step 1: Read the HOLD reason
The HOLD envelope tells you:
- **What** was blocked (tool, action_class, target)
- **Why** (which floor triggered: F1, F4, F7, etc.)
- **Who** requested it (agent, lease, delegation chain)
- **Blast radius** (what would change if approved)

### Step 2: Ask yourself
1. Is this reversible? If NO → automatic reject unless you're 100% sure. (F1 AMANAH)
2. Is the agent's reasoning sound? Read the forge_plan.
3. Has this agent done similar things successfully before?
4. What's the WORST case if I approve?
5. What's the COST of rejecting? (time, momentum, technical debt)

### Step 3: Approve, reject, or modify
- **Approve:** `ack_irreversible=true` if it's truly irreversible
- **Reject:** Agent will rollback or propose alternative
- **Modify:** Change the parameters (narrower scope, smaller blast radius) then approve

### Rule of thumb
> If you hesitate for more than 30 seconds, reject. You can always approve later. You can never un-approve.

---

## 3. HOW TO INTERPRET HOLDS

### HOLD Types

| HOLD Type | What It Means | Typical Response |
|-----------|---------------|-----------------|
| **F1_AMANAH** | Irreversible action detected | Verify backup exists. If yes, approve. If no, demand backup first. |
| **F4_CLARITY** | Agent's plan would increase entropy | Read the plan. If the entropy increase is temporary (refactor → cleanup), approve. If permanent, reject. |
| **F7_HUMILITY** | Agent confidence > 0.90 cap | Agent is overconfident. Ask: "What's your uncertainty range?" |
| **F8_LAW** | Boundary violation — cross-organ mutation | Verify the agent has lease for cross-organ work. If not, reject. |
| **F13_SOVEREIGN** | Explicitly requires your approval | Read the proposal. This is the highest gate. |
| **888_HOLD** | Generic irreversible or high-risk hold | Same as F13 — deliberate carefully. |
| **SCENARIO_HOLD** | Multi-organ policy triggered (e.g., GEOX dangerous + WELL tired) | Read the scenario. These are usually correct. |
| **E7_BAND** | Agent's risk band insufficient for requested action | Ask: should this agent have higher autonomy? If yes, approve and consider calibration. If no, reject. |

### HOLD Rate Guidelines
- **< 5% HOLD rate:** System is working well. Agents are operating within bounds.
- **5-15% HOLD rate:** Normal friction. Review holds weekly for patterns.
- **15-30% HOLD rate:** Policy may be too strict. Consider autonomy calibration.
- **> 30% HOLD rate:** Something is wrong. Either: (a) agents are too aggressive, or (b) policies are too restrictive. Investigate.

---

## 4. HOW TO CHANGE AUTONOMY LEVELS

### Tool Risk Bands

| Band | Agent Can | Agent Cannot | When to Use |
|------|-----------|-------------|-------------|
| **FULL_AUTO** | Execute without asking | Nothing blocked | For OBSERVE tools (read-only, safe) |
| **APPROVE_ONLY** | Propose, plan, dry_run | Execute without approval | For MUTATE tools (editing code, restarting services) |
| **PROPOSE_ONLY** | Plan, suggest | Execute at all | For human judgment calls (architecture decisions) |
| **HUMAN_ONLY** | Nothing | Everything — Arif must execute | For ATOMIC operations (deployments, DNS, secrets) |

### How to change a tool's band:

1. **Request from Kernel Scribe agent:** "Scribe, audit tool_risk_registry. Any tools in the wrong band?"
2. **Review the calibration report:** Look at HOLD rate, override rate, false positive rate
3. **Decide:**
   - TIGHTEN (FULL_AUTO → APPROVE_ONLY) if: HOLD rate too low but dangerous patterns emerging
   - LOOSEN (APPROVE_ONLY → FULL_AUTO) if: HOLD rate > 20% consistently with no real issues
4. **Modify:** The tool_risk_registry file (ask A-FORGE to forge_execute the change)

---

## 5. HOW TO STOP A RUNAWAY AGENT

### Signs of Runaway
- Tool call frequency spikes (> 5x normal rate)
- Same operation retrying in infinite loop
- Anomaly risk level: RED or BLACK
- Unusual tool path never seen before
- Agent consuming excessive tokens/resources

### Immediate Actions (in order)

**Level 1: PAUSE the agent**
```
# Via AAA cockpit
→ Click "PAUSE" on the agent card
→ This sends 888_HOLD to the agent's arifOS session
→ Agent stops current operation, awaits your input
```

**Level 2: REVOKE the lease**
```
# Via arifOS
→ arif_lease_revoke(lease_id="[agent's lease]")
→ Agent loses all tool access immediately
→ Can still observe and report, cannot execute
```

**Level 3: KILL the session**
```
# Via bash (ssh to af-forge)
→ Find agent process: ps aux | grep [agent]
→ Kill: kill -9 [PID]
→ Session state saved in Redis L2 — can inspect later
```

**Level 4: STOP the organ**
```
# Via systemd
→ systemctl stop [organ].service
→ Entire organ goes offline
→ Other organs continue operating
```

### After Stopping
1. Read the session log: `arif_memory_recall(session_id="...")`
2. Check what the agent was trying to do
3. Decide if it was an agent error or a policy gap
4. If agent error: fix the agent's instructions
5. If policy gap: add new E7 rule or scenario policy
6. Resume or restart

---

## 6. EMERGENCY PROCEDURES

### VPS Going Down
```bash
# Check what's happening
systemctl status  # look for failed services
df -h             # disk space?
free -m           # memory pressure?
docker ps -a      # containers healthy?
```

### arifOS Kernel Crash
```bash
systemctl restart arifos
sleep 5
curl localhost:8088/health
```

### NATS Mesh Down
```bash
docker restart nats
# Agents will reconnect automatically
```

### Dependency Vulnerability (CVE)
1. External Watcher will flag it
2. Read the CVE severity and affected versions
3. Decide: upgrade immediately (if CRITICAL) or schedule (if HIGH/MEDIUM)
4. Route upgrade through A-FORGE forge pipeline

---

## 7. WEEKLY RITUAL

Every week, spend 5 minutes:

1. **Read Scribe Report** — anomalies, proposals, constitutional health
2. **Check External Watcher Digest** — anything relevant from the ecosystem?
3. **Review HOLD log** — any patterns in what's being blocked?
4. **Check WELL** — are you rested enough for high-cognition decisions?
5. **One decision only** — approve ONE calibration change, ONE refactor proposal, or ONE policy update. Don't batch. Small, deliberate moves.

---

## 8. QUICK REFERENCE CARDS

### "Agent wants to restart a service"
→ Check: is this a production organ? If YES → 888_HOLD. If NO (dev tool) → approve.

### "Agent wants to modify arifOS kernel"
→ 888_HOLD always. Read the forge_plan. Check if tests pass. Approve only for reversible changes.

### "Agent wants to deploy to production"
→ 888_HOLD always. Verify: all tests pass, coverage > 70%, no degraded organs, WELL=OPTIMAL.

### "Agent wants to access external API"
→ Check: does the API have a key in /root/.secrets/? If YES and read-only → approve. If write → 888_HOLD.

### "Alarm going off at 3am"
→ Check organ health. If degraded but not offline → note it, go back to sleep. If OFFLINE → decide if critical enough to wake up.

---

*Playbook forged: 2026-06-14. Keep this open during any federation interaction.*
*DITEMPA BUKAN DIBERI — Your sovereignty is earned through deliberate operation.*
