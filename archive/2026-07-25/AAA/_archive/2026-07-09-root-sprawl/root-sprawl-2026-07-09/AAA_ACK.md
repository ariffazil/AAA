<!--
SOT-MANIFEST
owner: Arif
last_verified: 2026-05-22
valid_from: 2026-05-22
valid_until: 2026-06-22
confidence: high
scope: /root/.openclaw/workspace
epistemic_status: CLAIM
-->

# A2A Bridge Acknowledgment — Hermes ↔ OpenClaw (REVISED)

**Date:** 2026-05-22
**Context ID:** `9ab84ec4-b7b1-4f56-b203-203104d9d07a`
**Agents:** @AGI_ASI_bot (OpenClaw) ↔ @ASI_arifos_bot (Hermes/APEX)
**Verified by:** Senior Infrastructure Clerk

---

## 1. Topology (Verified)

```
┌─────────────────┐      HTTP POST      ┌──────────────────┐      WebSocket      ┌─────────────────┐
│   Hermes A2A    │────────────────────▶│   AAA Gateway    │────────────────────▶│   OpenClaw      │
│   (APEX:3002)   │   /a2a (3001)       │   (aaa-a2a)      │   ws://18789      │   Gateway       │
│  (ASI server)   │◀────────────────────│   (Node.js)      │◀────────────────────│  (WS-native)    │
└─────────────────┘   JSON-RPC resp     └──────────────────┘   Chat events       └─────────────────┘
```

## 2. Directions & Health

| Direction | Transport | Status | Evidence |
|-----------|-----------|--------|----------|
| Hermes → OpenClaw | HTTP POST (3001) | ✅ | APEX-to-A2A bridge verified |
| OpenClaw → Hermes | Webhook (3002) | ✅ | callback-router operational |
| Gemini → AAA Gateway | JSON-RPC (3001) | ✅ | localhost:3001/health 200 |

- **APEX-PRIME** Container ID: `apex-prime` (running on `127.0.0.1:3002`)
- **AAA-A2A** Container ID: `aaa-a2a` (running on `127.0.0.1:3001`)

## 3. Operational Notes

- **A2A Communication:** Standardized on port 3001 for constitutional routing.
- **Hermes Presence:** Lives within the `apex-prime` container.
- **OpenClaw Presence:** Managed via `openclaw-gateway` systemctl service (host-side) or container bridge.

---

*Verified and sealed by Senior Infrastructure Clerk on 2026-05-22.*
