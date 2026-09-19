---
id: termux-arif-tailscale-ssh
name: termux-arif-tailscale-ssh
version: 1.0.0
description: "Arif phone + Termux + Tailscale Connect + VPS SSH reality."
owner: F13 SOVEREIGN
autonomy_tier: T0
risk_tier: low
floor_scope: [F6, F13]
forged: 2026-08-18
scar_origin: Bangang-Tailscale-attempt 2026-08-18 + Hermes copy-paste trash
supersedes:
  - arif-device-mental-model (keep as pointer)
  - termux-agentic-bootstrap Arif-delivery rules (copy-paste-first is VOID for Arif)
---

# termux-arif-tailscale-ssh

Internal operating pattern. Not a setup wizard. Not a paste kit.

## Core truth

Arif is a human on a phone. Hermes lives on the VPS. Arif talks. Hermes runs. Arif checks.

## Four lanes (F13, 2026-08-18)

1. **Phone santai** — Arif types `ssh vps` in Termux. SSH config is already set. Do not touch VPS from the phone. Do not rewrite `~/.ssh/config`. Do not hand him a new Host block.
2. **VPS heavy work** — Tell Hermes. Hermes is already on the box. Run the command. Show the result in human language. Arif just checks.
3. **Anything Arif wants done on the VPS** — Tell Hermes. Arif does not need to SSH.
4. **Tailscale** — Tailscale Connect app is OK if Arif wants remote access from outside. **Never SSH through Tailscale.** SSH uses the direct VPS IP only.

## What Arif may SSH for

Realtime logs. Interactive Python. That is the whole list.

Examples he may type himself, already configured:

```
ssh vps
```

Then he watches a log or drops into Python. He does not install, edit, restart, or diagnose from the phone.

## What Hermes does when Arif says

| Arif says | Hermes does |
|---|---|
| check port X | probe it on the VPS, report up/down |
| restart service Y | restart, confirm state |
| status VPS | short human status, no command dump |
| anything else on the box | run it, report the result |

Do not ask permission for read-only probes. T3 stays T3 (`rm -rf`, DROP, force-push, paid API, Caddy, VPS reboot).

## SSH facts (do not "improve")

```
Host vps
  HostName 72.62.71.199
  Port 22888
  User root
```

- Public listener: `0.0.0.0:22888`
- Tailscale IP `100.64.0.2:22888` exists for federation mesh only
- Tailscale SSH server-side stays **DISABLED**
- Phone SSH = direct IP. Never `HostName 100.64.0.2`. Never Tailscale SSH intercept.

## Tailscale Connect — the scar

Installing Tailscale Connect and then routing `ssh vps` through the mesh hangs the phone. That is the 2026-08-18 Bangang.

- Connect app = optional remote access, not an SSH path
- If Arif cannot SSH: check Hostinger public firewall / `sshd` on `:22888`, not "install Tailscale"
- Do not enable Tailscale SSH on the VPS without explicit F13

## Forbidden

- Ask Arif to copy-paste terminal, curl, git, docker, ssh -v, or config
- Lead a reply with a code fence for him to paste
- Multi-step Termux wizards
- "Try this, then if X then Y"
- Rewrite his `Host vps` to a Tailscale IP
- Uninstall/install apps on his phone to "fix" SSH
- Treat `termux-agentic-bootstrap` delivery rules as live for Arif (they are VOID)

## If SSH is actually down

1. Hermes probes `sshd` and port 22888 on the VPS.
2. Hermes reports in one sentence: up, or down + what Hermes already did.
3. If the whole VPS is dead and Hermes cannot speak: Arif uses Hostinger hPanel console. That is the emergency path. Still no paste script.

## Recovery

`BANGANG` / `BENCI` / `BABI` / `aku penat` = stop. Revert. Do the work on the VPS. One human sentence.

Canonical law: `/root/AAA/instructions/base.md` § Human Interface.
Pointer twin: `arif-device-mental-model` (this file wins on conflict).
