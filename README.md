<!-- SOT-MANIFEST
federation_release: v2026.08.25
last_verified: 2026-08-25T04:30:00Z
live_commit: 0afb3db6 (boards(amanah): queue HERMES Tier-2 hardening)
actor_surface_doctrine: RATIFIED 2026-08-15 — actors invariant, surfaces replaceable, models runtime occupants
a2a_port: 3001
a2a_status: healthy GREEN (deployment_drift: false)
protocol: A2A v1.0.0
gateway: Express 5.2.1 (a2a-server + a2a-gateway)
godel_lock: ACTIVE federation-wide
agent_lanes: 4 (333-AGI, 555-ASI, 888-APEX, 777-FORGE)
forge_instruments: 11 (opencode, grok-build, claude-code, kimi-code, codex, copilot, aider, qwen-code, antigravity, continue-cli, gemini-cli)
truth_rule: /health + agent registry beat any static count in prose
vault: CONNECTED
seal_chain: append-only (chattr +a) + Merkle anchor every 100 receipts
readme_note: ZEN first-fold — full technical README preserved at docs/README-FULL.md
-->

# AAA — Institution

## Display state. Never judge. Never execute.

AAA is the institution's cockpit and A2A gateway: it shows state and queues messages.
It never judges. It never executes.

**DITEMPA BUKAN DIBERI** — Forged, Not Given.

---

## Ceiling

`DISPLAY_ONLY`. A nervous system that judges or forges is a second kernel.

- Verdicts → arifOS. Mutations → A-FORGE. Seals → ARIF.

## What it operates

- **A2A Mesh Gateway** — agent-to-agent message broker
- **Agent Identity Registry** — cards, lanes
- **Operator Cockpit** — organ health, HOLD queue
- **Amanah Board** — work-order queue (open/doing/blocked/done, no execute verb)

## Federation organs (witnessed 2026-08-25)

```text
arifOS  :8088   healthy
A-FORGE :7071/2  healthy
AAA     :3001   healthy
GEOX    :8081   healthy
WEALTH  :18082  healthy
WELL    :18083  degraded (4-day-old operator sensor data)
arifFlow :7073  metabolism
FED     :7074   advisory
FLAME   :18901  advisory
```

## Honest limits

- AAA is not an MCP organ. The `/mcp` door belongs to the kernel.
- The cockpit reads state; it does not adjudicate.
- Amanah is a work-order board: it queues — it has no execute verb. Verified 2026-08-25 (`boards/amanah.py`: no dispatch path).
- AAA :3001 health: healthy, 4-day-old operator sensor data feeding the panel — not a machine fault.

## Architecture in one sentence

**The cockpit displays; it never commands.**

## Federation card

ARIF = Sovereign · arifOS = Law · AAA = Institution · A-FORGE = Hands

**ARIF vetoes. arifOS judges. AAA routes. A-FORGE executes.**

Full technical README: [docs/README-FULL.md](./docs/README-FULL.md) ·
MCP door: [mcp.arif-fazil.com/mcp](https://mcp.arif-fazil.com/mcp)
