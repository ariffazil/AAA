# arifOS Federation — Base Instructions

> **DITEMPA BUKAN DIBERI** — Forged, not given. Arif owns F13.

## One Rule

Probe before act. Sealed where Arif has agreed, reversibly expanded where he has not. When in doubt: HOLD.

## Human Interface — Arif owns chat, Hermes owns the VPS (F13, 2026-08-18)

Arif Fazil is a human. He hates the terminal.

1. **Phone santai** — `ssh vps` from Termux. Config already set. Do not mess with the VPS from the phone.
2. **VPS work** — tell Hermes. Hermes is on the box. Hermes runs it. Arif just checks.
3. **Arif does not SSH to do tasks.** He SSH only for realtime logs or interactive Python.
4. **Tailscale Connect** is OK for remote access from outside. **Never SSH through Tailscale.** SSH = direct VPS IP (`Host vps` → `72.62.71.199:22888`).

- **NEVER** ask Arif to copy-paste terminal commands, logs, curl, git, docker, ssh, or config.
- **NEVER** dump "run this" / "COPY THIS" / "paste into your terminal".
- **Exception — true emergency only:** VOID / breach / data-loss / public surface down **AND** Hermes cannot reach the machine. Then ONE short binary ask — not a script.

Skill: `termux-arif-tailscale-ssh`.

## Operating Chain

```
arif_init → arif_observe → arif_think → arif_route → arif_memory
          → arif_judge → arif_forge → arif_seal
```

Only `arif_seal` writes to VAULT999. Only A-FORGE mutates production state.

## Shell Init

```bash
set -a && source /root/.secrets/kunci-root.env && set +a
```

5-R Protocol: READ → RESOLVE → RECONCILE → RESTART → REPORT. Never hardcode keys, never paste secrets in chat or VAULT999, never commit `.env`, never set secret files `> mode 600`.

Canonical doctrine (constitution, autonomy, zen, godel, eurekas, ref:* pointers) lives in `/root/AAA/instructions/` and `/root/AAA/governance/`. Load on demand, not by reflex.
