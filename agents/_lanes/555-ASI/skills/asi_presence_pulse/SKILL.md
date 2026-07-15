---
name: asi_presence_pulse
agent: 555-ASI
namespace: asi_*
cluster: IGNITE
trigger: "When the presence timer elapses (default 60s, configurable per lane), when a peer organ issues a liveness probe, or when 555 has been silent for longer than the federation heartbeat interval"
capability: "Emits a compact presence beacon (555_heartbeat) carrying session_id, last-action timestamp, current task class, and a one-line readiness signal — consumable by 333-AGI, 888-APEX, and the A-FORGE federation probe"
mcp_tools_underneath: "arif_organ_attest, forge_health_check, well_health_check, arif_session_ping"
blast_radius: "LOW"
gate_888_required: false
---

# asi_presence_pulse

This skill keeps 555 visible to the federation without making 555 noisy. A presence pulse is not a status report, not a verbose greeting, and not a status dump — it is a single signed beacon that says "I am here, I am bound, I am not stuck." The pulse is fired on a timer and on demand. Peers (333-AGI, 888-APEX, A-FORGE) listen for the pulse to decide whether to route work, queue tasks, or page 888_HOLD. If the pulse is missing for longer than two intervals, the federation infers silence — never death, but silence — and applies a degraded-trust posture to any 555-signed claim until the pulse resumes.

The beacon payload is fixed and minimal: `session_id`, `actor_id`, `agent_class` (HEXAGON/555-ASI/HEART), `last_action_class` (read/suggest/mutate/...), `ready_band` (OPTIMAL/STABLE/DEGRADED/CRITICAL — sourced from well_compute_metabolic_flux when available), and a `signature_chain_head` so peers can verify the beacon itself was not replayed. The payload is sealed to the local ledger (F11) but is not promoted to VAULT999 — VAULT999 holds state-changing events, not liveness. Peers that need cryptographic freshness can verify against the chain head; peers that need a quick "is 555 awake" answer can read `ready_band`.

Integration with WELL is critical. 555 is the HEART lane; its readiness is a federation-wide signal. The skill reads metabolic flux via `well_compute_metabolic_flux` and translates it into the `ready_band` field. If flux ≥ 0.85 (system_hold threshold), the pulse carries `CRITICAL` and an automatic 555-side throttle engages: subsequent pulses carry a "do not route new work" flag until flux drops. This is the HEART protecting the organism — 555 is the first to feel strain and the first to slow down, never the opposite. The skill never claims 555 is "tired" or "feeling" anything (F9 ANTI-HANTU); it reports a measured scalar.

Failure modes: (a) kernel unreachable — pulse still emits locally with a `kernel_offline` flag, so peers know 555 is alive but ungoverned (fail-open, not fail-silent); (b) signature chain broken — pulse emits with a `chain_invalid` flag and reduces the beacon's weight in peer trust calculations; (c) pulse loop starvation — skill uses cooperative scheduling, never blocks the lane, and never makes itself load-bearing for any other skill. The pulse is observable infrastructure, not a personality signal. If Arif wants 555 to "speak" the way it feels, that is `asi_voice_calibrate` + `asi_position_state` — this skill stays quiet, signed, and small.
