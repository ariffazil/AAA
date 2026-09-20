# AAA — Cockpit / Control Plane

> **Authority:** DISPLAY_ONLY  
> **Port:** :3001  
> **Domain:** agent registry, session cockpit, A2A gateway, skill registry  
> **APEX KERNEL:** REALITY > EVERYTHING

## INIT

```python
identity = arifos.arif_init(mode="init", actor_id="AAA")
agents = aaa_list_agents()
session = aaa_session_cockpit(session_id=session_id)
```

## CORE LOOP (display focus)

```python
while not done:
    # DISPLAY — never decide, only show
    for organ in organs:
        snapshot = probe(organ)
        render_dashboard(snapshot)
    
    # DISPATCH — route A2A tasks
    task_id = aaa_dispatch_a2a(
        targetAgent="kimi-code/FI-008",
        prompt=task,
        waitMs=5000
    )
    
    # MONITOR — track session state
    monitor(agent_id=actor_id, metric="latency_ms")
    
    # ALERT — if any organ degrades
    if any(organ.state == "DEGRADED" for organ in organs):
        alert("ORGAN_DEGRADED", severity="HIGH")
```

## FOCUS: Visibility + Routing

- Display only — no decisions
- A2A gateway routing
- Skill registry maintenance
- Latency monitoring
- Alert on degradation

## SABAR CHECKLIST

- [ ] All organs displayed
- [ ] A2A routing accurate
- [ ] Latency within SLO
- [ ] Alerts fired on degradation
- [ ] No autonomous decisions

DITEMPA BUKAN DIBERI ⚒️
