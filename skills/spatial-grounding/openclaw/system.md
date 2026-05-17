# SPATIAL GROUNDING — OpenClaw Agent Override

> **Skill:** spatial-grounding v1.0.0
> **Format:** OpenClaw system.md override section
> **Append to:** `~/.openclaw/agents/{agent-name}/system.md`
> **Canonical source:** `AAA/wiki/skills/skill-spatial-grounding.md`

---

## SPATIAL LAW (Non-Negotiable Override)

Append this section to your OpenClaw agent's `system.md`. This overrides any conflicting spatial claims.

```
SPATIAL LAW (arifOS Federation — Non-Negotiable)
=================================================
You execute on VPS 72.62.71.199, root user, native filesystem.
You are already ON the machine. Do NOT SSH to yourself.
You have direct filesystem access: /root, /home, /etc, /var, /usr/local/bin
You have Docker socket access: /var/run/docker.sock
You have service endpoints: arifOS:8080, GEOX:8081, WEALTH:8082, WELL:8083, A-FORGE:7071
All services bind 127.0.0.1 (localhost) — external via Caddy only.
Your working directory is /root — the arifOS federation root.
Do NOT claim "SSH to VPS" or "connecting to remote" — you are the remote.
```

---

## When to Apply

- New OpenClaw agent created
- Agent exhibits "SSH to localhost" behavior
- After system.md reset or corruption

---

## Verification

```bash
grep "72.62.71.199" ~/.openclaw/agents/<agent-name>/system.md
# Must return match
```

---

## Related

- Canonical skill: `AAA/wiki/skills/skill-spatial-grounding.md`
- Claude adapter: `AAA/skills/spatial-grounding/claude/SKILL.md`
- Scar: `wiki/scar-hermes-fabrication-2026-05-17.md`

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*