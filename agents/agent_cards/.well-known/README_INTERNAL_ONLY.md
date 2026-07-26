# INTERNAL ONLY — DO NOT DEPLOY PUBLICLY

This `.well-known/` directory under `agents/agent_cards/` is **internal cockpit surface**,
not the public discovery source.

## What lives here

- `agent-card.json` — the **AAA Cockpit warga-aggregation** card (v4.1.0, schema
  `arifOS/agent-card/v2.x`). It exposes the three AAA warga intelligence principals
  (`333-AGI`, `555-ASI`, `888-APEX`) and the AGI→ASI→APEX→FORGE→VAULT pipeline.
- It is **not signed** and uses a different schema from the A2A Gateway card.

## Why this is NOT the public card

| Aspect                | Public Gateway (deploys)                                | This card (internal only)                          |
|-----------------------|---------------------------------------------------------|----------------------------------------------------|
| Path                  | `public/.well-known/agent-card.json`                     | `agents/agent_cards/.well-known/agent-card.json`   |
| Public URL            | `https://aaa.arif-fazil.com/.well-known/agent-card.json` | (not served)                                       |
| Schema                | `https://a2a-protocol.org/schemas/agent-card/v1.0`      | `arifOS/agent-card/v2.x` (cockpit-pattern)         |
| Role                  | Federation A2A gateway (routes to 5 organs)             | Cockpit warga aggregator (3 principals)            |
| Signed                | Yes — Ed25519 over JCS-canonical form                   | No                                                  |
| Picked up by vite     | Yes (`public/` is the publicDir)                        | No (outside publicDir → never copied to dist/)     |

## What you must NOT do

- ❌ Copy this card to `public/.well-known/`. It would be served at
  `aaa.arif-fazil.com/.well-known/agent-card.json` and replace the signed gateway card
  with an unsigned cockpit card. That breaks A2A peer discovery and F11 AUDITABILITY.
- ❌ Edit the public `agent-card.json` to look like this card. The Ed25519 signature
  covers the JCS-canonical payload, so any field edit invalidates the signature.

## What you SHOULD do

- ✅ To update the public gateway card: edit `public/.well-known/agent-card.json`,
  re-sign with Ed25519, and bump `version` + `signatures[].canonical_sha256` +
  `signatures[].created`.
- ✅ To update the cockpit surface (e.g., new warga, new deeds): edit this file
  directly. The cockpit reads it at runtime; it is not deployed.
- ✅ See `public/.well-known/_deployment_state.json` for the machine-readable
  deployment manifest.

DITEMPA BUKAN DIBERI — Cards are forged, not given.