# AAA Boundary

<!--
SOT-MANIFEST
owner: Arif
last_verified: 2026-05-19
scope: /root/AAA
epistemic_status: CONTRACT
-->

AAA is the federation control plane and operator cockpit. It makes agent state,
session state, and human-in-the-loop controls visible. It does not adjudicate
constitutional truth and does not own deployment substrate.

## Owns

- React cockpit UX and operator-facing federation dashboards.
- A2A gateway surfaces, agent cards, identity display, and session anchoring.
- Operator task visibility, hold queues, bridge status, and control-plane
  workflows.
- Prompt/identity/skill bundles used to orient agent sessions.
- AAA-specific schemas, exports, and validation of cockpit/control-plane
  contracts.

## Does Not Own

- F1-F13 constitutional law or final verdict semantics.
- `888_JUDGE`, `999_SEAL`, VAULT999, or canonical memory governance.
- GEOX earth-science calculations or WEALTH capital math.
- Docker, Caddy, systemd, release assembly, or host deployment ownership.
- Secret rotation, public production deploy approval, or irreversible operations.

## Imports From

- arifOS: verdict context, floor policy, session state, memory/audit summaries,
  canonical federation contracts.
- A-FORGE: deployment and release status for operator display.
- GEOX/WEALTH/WELL: domain health, artifacts, and evidence summaries.
- Hermes/OpenClaw: bot/gateway status and A2A context when exposed to the
  cockpit.

## Exports To

- arifOS: operator intent, session identity, approval/hold context, and A2A
  event references.
- A-FORGE: bounded execution requests after governance checks.
- Hermes/OpenClaw: human-readable cockpit context and agent-card metadata.
- Public/operator surfaces: status, dashboards, and non-secret control-plane
  views.
