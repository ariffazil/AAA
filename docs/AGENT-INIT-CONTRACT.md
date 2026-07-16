# ⚒️ AGENT INIT CONTRACT — Quantum Agentic Ready

> **Bound:** 2026-07-16 by FORGE (000Ω) under F13 SOVEREIGN
> **Principle:** The machine IS the intelligence substrate. Every init reduces entropy, never adds it.

---

## 0. THE IRON RULE

```
ΔS ≤ 0 on every agent session.
If your init increases entropy, you failed before you started.
```

---

## 1. TIERS (load in order, stop when task is clear)

| Tier | Content | Size | When |
|------|---------|------|------|
| **T0** | Identity + Output Contract + F1-F13 floors | ≤2KB | ALWAYS (every init) |
| **T1** | AGENTS.md compressed (organs, ports, authority) | ≤10KB | First non-trivial action |
| **T2** | Full heptalogy + bootstrap sequence | ≤30KB | Complex multi-organ task |
| **T3** | Per-organ AGENTS.md | varies | When touching that organ |
| **T4** | Skills | varies | When task matches skill description |

**Rule:** Never load T2 if T0+T1 is sufficient. Never load T4 at boot.

---

## 2. MCP STAGING (connect on demand, not all at boot)

| Stage | Servers | When |
|-------|---------|------|
| **S1** | arifos, aforge | Boot — governance + execution |
| **S2** | geox, wealth, well | First domain action |
| **S3** | github, docker, cloudflare, postgres, etc. | On-demand only |

**Rule:** 2 servers at boot, not 25. Connect others when needed.

---

## 3. SKILLS (on-demand, not at boot)

```
Canonical: /root/AAA/skills/        ← source of truth
View:      /root/.agents/skills/    ← OpenCode filtered view
View:      /root/.claude/skills/    ← Claude filtered view

Rule: Load ONE skill when task matches. Never load all at init.
```

---

## 4. ORGAN PROBE (mandatory before any action)

```bash
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  n="${svc%%:*}"; p="${svc##*:}"
  curl -sf "http://localhost:$p/health" >/dev/null 2>&1 && echo "✅ $n" || echo "❌ $n"
done
```

**Rule:** If any organ is ❌, proceed read-only on live organs. Never assume dead organ config is valid.

---

## 5. ENTROPY MEASUREMENT (session end)

Every agent session MUST end with:

```
entropy_delta = (files_created + files_modified + processes_spawned) - (files_cleaned + processes_killed)
If entropy_delta > 0: justify or clean up.
```

---

## 6. ORTHOGONAL ROLES (no overlap)

| Component | Role | Does NOT |
|-----------|------|----------|
| arifOS | Constitutional law | Execute, build, deploy |
| A-FORGE | Governed execution | Judge, seal, route |
| GEOX | Earth evidence | Judge, execute |
| WEALTH | Capital evidence | Judge, execute |
| WELL | Human readiness | Judge, execute |
| AAA | Control plane + A2A | Judge, execute, compute domain |
| MIND | Cognitive reasoning | Execute, judge |
| Hermes | Conversational SOUL | Execute code |
| OpenClaw/FORGE | Machine HANDS | Judge, converse |
| Prometheus+Grafana | Observability | Execute, judge |

**Rule:** If you find yourself doing another component's job, STOP and route to the correct component.

---

## 7. QUANTUM AGENTIC PROPERTIES

| Property | Meaning | Enforcement |
|----------|---------|-------------|
| **Clean State** | Every init starts from measured baseline | carry_forward.json + organ probe |
| **Coherent Flow** | Actions follow golden path 000→111→333→666→888→999 | arif_init → arif_judge → forge_execute → arif_seal |
| **Measured Collapse** | Every decision has evidence + confidence | F2 TRUTH, OBS/DER/INT/SPEC labels |
| **Orthogonal Superposition** | Components don't overlap until measurement (action) | This contract |
| **Entangled Witness** | Changes propagate through federation | VAULT999 seal chain + organ heartbeats |
| **Decoherence Protection** | Stale state detected and cleaned | Entropy governor + skill audit |

---

*The machine is the substrate. Intelligence emerges from clean states, coherent flow, and measured collapse.*
*DITEMPA BUKAN DIBERI*
