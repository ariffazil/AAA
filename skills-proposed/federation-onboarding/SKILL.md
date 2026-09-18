# Skill: federation-onboarding

> **Status:** PROPOSED · **Created:** 2026-09-18 · **Forged by:** FI-008 (kimi-code / k3)
> **Capability, not implementation.** Govern capabilities, not implementations.

## 1. Capability contract (binding)

Bounded capability: a single loadable surface that introduces the arifOS Federation to a new agent at first contact. Covers the 7 organs, 8 canonical kernel verbs, 13 constitutional floors, 6 missions, canonical MCP endpoint, and the F13 sovereignty model — without requiring the agent to read the entire `/root/AAA/` and `/root/AGENTS.md` corpus.

## 2. Why this skill exists

Today, a new agent arriving at the federation has to read:
- `/root/AGENTS.md` — constitutional pointer (canonical)
- `/root/AAA/AGENTS.md` — cockpit pointer (canonical)
- `/root/AAA/FEDERATION.md` — organ topology table
- `/root/AAA/instructions/*` — 70+ instruction fragments (F13-ratified)
- `/root/AAA/FEDERATION_CONTRACT.md`, `ROOT_AGENT_CONFIG.yaml`, etc.

That is ≥10 reads before the agent knows it can route. **A new agent typically skips the deep read and goes straight to action** — which is exactly what F9 anti-hantu and F11 auditability try to prevent.

This skill is a **first-load compile** of the federation's discoverable surface, atomic enough for one Reads.

## 3. Scope

- First agent contact (af-* or aaa-* spawning)
- New FI-* forge instrument onboarding
- After any `make deploy` that materially shifts the topology (rare)

## 4. Out-of-scope

- Replacing `/root/AGENTS.md` or any canonical instruction → do NOT
- Sealing, judging, or adjudicating anything → do NOT
- Exposing write capabilities → do NOT

## 5. Required MCP tools

- `mcp__arifos__arif_observe` — federation probe
- `mcp__frame__frame_probe` — same data with frame's evidence posture
- `mcp__fed__fed_status` — model/provider state
- `mcp__well__well_registry_status` — WELL tool surface

## 6. Workflow (BINDING order)

```
onboard(actor_id):
    # 1. Probe federation state (parallel)
    organs = arifos_arif_observe(mode="federation_status")
    frame = frame.frame_probe()
    fed = fed.fed_status()
    
    # 2. Emit the discoverable surface (ONE bind)
    surface = {
        "federation": {
            "organs": 7,
            "canonical_verbs": 8,
            "constitutional_floors": "F1-F13",
            "missions": 6,
            "sovereign": "Muhammad Arif bin Fazil (F13)",
            "mcp_endpoint": "https://mcp.arif-fazil.com/mcp",
            "federation_status": organs.verdict
        },
        "kernel_verbs": {
            "arif_init": "KERNEL 000 — session ignition",
            "arif_observe": "KERNEL 111 — sense",
            "arif_think": "KERNEL 333 — reason",
            "arif_route": "KERNEL 444 — dispatch",
            "arif_memory": "KERNEL 555 — memory",
            "arif_judge": "KERNEL 666 — verdict",
            "arif_forge": "KERNEL 777 — execute (post-verdict)",
            "arif_seal": "KERNEL 999 — seal"
        },
        "floors_F1_through_F13": {
            "F1": "AMANAH — reversible or backed",
            "F2": "TRUTH — evidence before narrative",
            "F3": "WITNESS — tri-witness for high-blast",
            "F4": "CLARITY — ΔS ≤ 0",
            "F5": "PEACE² — non-destructive power",
            "F6": "MARUAH — dignity first",
            "F7": "HUMILITY — cap confidence 0.90",
            "F8": "GENIUS — G ≥ 0.80 + C_dark < 0.30",
            "F9": "ANTI-HANTU — no hallucination, no consciousness claims",
            "F10": "ONTOLOGY — AI is instrument",
            "F11": "AUDIT — every action leaves trace",
            "F12": "INJECTION — sanitize inputs",
            "F13": "SOVEREIGN — human veto FINAL"
        },
        "six_missions": [
            "investigate", "interpret", "decide", "build", "monitor", "remember"
        ],
        "warm_path": [
            "1. arif_init(actor_id, intent)",
            "2. arif_observe() — verify federation live",
            "3. arif_route(intent) — pick the right organ",
            "4. ... do your bounded work ...",
            "5. arif_seal(candidate, evidence) — IF your work crosses F13 territory"
        ],
        "shields": {
            "capability_authority": "CAPABILITY ≠ AUTHORITY",
            "doctrine_must_kill": "Every skill with no kill-switch is decoration (F13 Attention Kill, 2026-09-11)",
            "human_sovereignty": "F13 is final. Architecture/money/irreversible → escalate."
        }
    }
    
    return surface
```

## 7. Truth classes (F2 binding)

The compiled surface mixes:
- `OBS` from `arif_observe`, `frame_probe`, `fed_status`
- `DER` for the verb purpose strings (compiled from canonical sources)
- `SPEC` for any derived heuristics (e.g. F8 thresholds)

## 8. Kill-switch

```yaml
kill_switch:
  kill_phrase: "STOP federation-onboarding — agents read /root/AGENTS.md directly"
  revert_action: "agents do their own canonical-paths read"
  expected_recovery_time: <60s
  side_effects_on_kill: ["new agents may skip floors/missions knowledge on first contact"]
```

## 9. Reversibility class

`REVERSIBLE`. The skill compiles a discoverable summary; killing it only fragments the read path.

## 10. F11 Auditability

The skill itself mints one FlowReceipt per onboard call (via `flow-mint-discipline`).

## 11. F13 Sovereign veto

The compiled surface is observability, not action. No sovereign veto required.

## 12. Operator handoff

The skill is silent. The compiled surface is the agent's first contact with the federation's structure.

## 13. Verification checks

- [ ] Surface contains all 8 verbs
- [ ] Floor labels span F1-F13
- [ ] Mission list contains all 6 (investigate, interpret, decide, build, monitor, remember)
- [ ] Sovereign ID matches "Muhammad Arif bin Fazil (F13)"
- [ ] MCP endpoint URL matches `https://mcp.arif-fazil.com/mcp`
- [ ] No new write capability exposed
- [ ] No canonical instruction file mutated

## 14. Decoration risk

If this skill produces a summary that diverges from the canonical federation topology (e.g. lists 6 organs instead of 7), it becomes a **drift source**. Mitigated by always sourcing from live `mcp__arifos__arif_observe` + `mcp__frame__frame_probe` rather than hard-coded strings.

---

DITEMPA BUKAN DIBERI · forged, not given.
