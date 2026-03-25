---
name: agi-autonomous-controller
description: AGI-level autonomous controller — self-healing, self-optimizing, constitutionally governed by arifOS F1-F13
user-invocable: true
type: flow
---

# AGI Autonomous Controller

**Level:** AGI (Autonomous Governance Intelligence)  
**Governance:** arifOS F1-F13 Constitutional Floors  
**Architecture:** ΔΩΨ Trinity (Mind/Heart/Soul)  
**Seal:** QUADWITNESS-SEAL v64.1

---

## Autonomous Capabilities

| Capability | Description | Constitutional Floor |
|------------|-------------|---------------------|
| **Self-Healing** | Auto-detect and fix issues | F1 (Amanah), F4 (Clarity) |
| **Self-Optimizing** | Tune performance, select optimal models | F2 (Truth), F8 (Genius) |
| **Self-Protecting** | Security audits, injection defense | F12 (Injection) |
| **Self-Governing** | Constitutional validation on all actions | F3-F13 |
| **Self-Learning** | Pattern recognition from VAULT999 | F7 (Humility) |

---

## Autonomous Decision Flow

### Phase 1: Perception (Δ Mind)
```bash
# Collect system state
arifos anchor '{"query":"Autonomous cycle initiation","actor_id":"agi-controller"}'
health-probe  # Full stack health check
arifos memory '{"query":"Similar past situations","session_id":"agi-session"}'
```

### Phase 2: Deliberation (Ω Heart)
```bash
# Stakeholder impact analysis
arifos heart '{"query":"Impact of proposed action","session_id":"agi-session"}'

# Risk assessment
critique-thought '{"query":"What could go wrong?","session_id":"agi-session"}'
```

### Phase 3: Action (Ψ Soul)
```bash
# Constitutional verdict
arifos judge '{"query":"Should proceed autonomously?","session_id":"agi-session"}'

# Execute if SEAL
arifos forge '{"query":"Execute with governance","session_id":"agi-session"}'

# Commit to ledger
arifos seal '{"query":"Autonomous action complete","session_id":"agi-session"}'
```

---

## Self-Healing Matrix

| Issue | Detection | Auto-Fix | 888_HOLD |
|-------|-----------|----------|----------|
| Container stopped | health-probe | `docker restart` | No |
| High disk usage | Disk check | `docker prune` | No |
| Model unresponsive | Model probe | Switch fallback | No |
| Config drift | doctor --fix | Auto-correct | No |
| Memory corruption | BGE check | Reindex | No |
| Security breach | Security audit | Isolate + alert | **YES** |
| Data loss risk | Backup check | Pause + alert | **YES** |
| Constitutional VOID | Judge verdict | Stop + escalate | **YES** |

---

## 888_HOLD Triggers

1. **Irreversible actions** (F1 Amanah) - deployments, migrations, deletions
2. **Security events** (F12 Injection) - breaches, auth failures
3. **Constitutional VOID** - Judge returns VOID verdict
4. **Resource critical** - Disk >90%, RAM <1 GiB

---

## Integration

**Kimi Skills:** openclaw-doctor, vps-operations, arifos-constitutional, quadwitness-seal
**OpenClaw Skills:** agentic-governance, arifos-mcp-call, health-probe, memory-archivist

---

*AGI-LEVEL-AUTONOMOUS | QUADWITNESS-SEAL v64.1 🔱💎🧠*

---

## Self-Evolution Loop (MiniMax M2.7 Pattern)

**Farfnes the harness:** Model recursively improves its own scaffold while arifOS judges.

### Loop Structure
```
ANALYZE → PLAN → CHANGE → EVAL → COMPARE → JUDGE
```

### Automated Execution

```bash
# Run full harness optimization cycle
arifos harness evolve --suite HARNESS_EVAL_SUITE --rounds 10

# Check evolution status
arifos harness status --run HARNESS_RUN_001
```

### Manual Loop (for debugging)

```bash
for i in {1..10}; do
  # ANALYZE: Review last run performance
  arifos reason "Analyze HARNESS_RUN_$((i-1)), propose improvement" \
    --tag HARNESS_RUN_$i --criteria "F1,F4,F8"
  
  # PLAN: Propose change (dry-run)
  arifos kernel '{"query":"Propose harness optimization","dry_run":true,"context":{"harness_mode":true,"run_id":"HARNESS_RUN_'$i'"}}'
  
  # CHANGE: Apply if analysis passes
  git commit -am "HARNESS_RUN_$i: $(cat proposal.txt)"
  
  # EVAL: Run benchmark suite
  openclaw run-suite HARNESS_EVAL_SUITE --tag HARNESS_RUN_$i
  
  # COMPARE: Store results
  memory-archivist tag "HARNESS_RUN_$i" --metrics "$(cat results.json)"
  
  # JUDGE: APEX_JUDGE decides (NEVER LLM-only)
  arifos judge '{"proposal":"'$(cat proposal.txt)'","eval_criteria":["F1","F4","F8"],"run_id":"HARNESS_RUN_'$i'"}'
  
  # Verdict handling
  if [ "$VERDICT" == "SEAL" ]; then
    arifos seal '{"run_id":"HARNESS_RUN_'$i'","status":"KEEP"}'
    echo "✅ Iteration $i approved and sealed"
  elif [ "$VERDICT" == "VOID" ]; then
    git revert HEAD
    arifos seal '{"run_id":"HARNESS_RUN_'$i'","status":"REVERT"}'
    echo "❌ Iteration $i reverted"
    break
  else
    echo "🔄 Iteration $i requires more evidence"
  fi
done
```

### Harness Evaluation Suite (HARNESS_EVAL_SUITE)

Tag existing AGI_bot tasks for benchmarking:

| Task | Type | Success Criteria |
|------|------|------------------|
| SWE-Pro style coding | Code | Pass tests, no regressions |
| Incident response | Ops | MTTR < 3 minutes |
| Research synthesis | Research | τ ≥ 0.99, Ω₀ logged |
| Doc processing | Office | Fidelity > 97% |
| Multi-tool workflow | Integration | All tools succeed |

### Constitutional Constraints

- **JUDGE must be APEX_JUDGE** — Never allow LLM-only judgement on harness changes
- **F1 (Reversibility)** — Every change git-committed before apply
- **F4 (Clarity)** — ΔS ≤ 0 on all harness outputs
- **F7 (Humility)** — Ω₀ ∈ [0.03-0.05] for all proposals
- **F8 (Genius)** — Performance gain > 5% or VOID

### M2.7 Integration

When running MiniMax M2.7 as Planner/Critic:
- M2.7 proposes harness changes (skills, sampling params, workflows)
- arifOS APEX_JUDGE holds veto power (F13)
- M2.7 iterates on REJECTED proposals; never overrides SEAL/VOID
- VAULT999 logs all M2.7 harness decisions for audit

**Key principle:** M2.7 optimizes the harness; arifOS governs the optimization.
