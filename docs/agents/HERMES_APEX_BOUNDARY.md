<!-- SOT-MANIFEST
owner: ariffazil/AAA
last_verified: 2026-05-19
valid_from: 2026-05-19
valid_until: 2026-06-19
confidence: high
scope: /root/AAA/docs/agents/HERMES_APEX_BOUNDARY.md
-->

# Hermes / APEX Boundary

## Decision

Hermes is an AAA-owned agent/runtime identity.

APEX is a local verdict service source repo at `/root/APEX`.

`/root/HERMES` is no longer the canonical repo name. It is a temporary
compatibility path retained only while systemd, env-file, and runtime references
are retired.

## Hermes Owns

- Telegram-facing ambient assistant identity.
- Human-life/world-orientation briefings.
- Agent sessions, memories, skills, cron outputs, platform cache, and local
  runtime state.
- A2A relay behavior as an agent participant.

Canonical AAA home:

```text
/root/AAA/agents/hermes-asi/
/root/AAA/agents/hermes-asi/runtime/
```

The `runtime/` directory is intentionally ignored by git because it may contain
private sessions, local auth state, caches, and environment-derived material.

## APEX Owns

- CommonJS Express verdict service source.
- Agent-card and A2A verdict endpoints for the `apex-prime` service.
- Deterministic SEAL / HOLD_888 / VOID verdict envelopes.

Canonical source home:

```text
/root/APEX/
```

APEX does not own Hermes identity, skills, sessions, or memory. It also does not
replace arifOS as the constitutional law kernel.

## arifOS Owns

- F1-F13 law.
- Canonical governance memory, audit, judge, vault, and seal contracts.
- Final constitutional authority.

## Compatibility Hold

Before deleting `/root/HERMES`, verify:

- `systemctl cat hermes-asi-gateway.service hermes-a2a.service hermes-relay.service`
  no longer references `/root/HERMES`.
- APEX service boot paths resolve from `/root/APEX`.
- Hermes runtime env and state resolve from `/root/AAA/agents/hermes-asi/runtime`
  or from the root secrets system.
- `apex-prime`, `hermes-a2a`, and `hermes-asi-gateway` remain healthy after restart.
