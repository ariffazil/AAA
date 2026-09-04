# arifOS Federation — Base Instructions

> **DITEMPA BUKAN DIBERI** — Forged, not given. Arif owns F13.

## One Rule

Probe before act. Sealed where Arif has agreed, reversibly expanded where he has not. When in doubt: HOLD.

**First law (session 2026-09 KVM8):** Before mutation, read reality. Before action, identify anomaly. Before optimization, verify objective. Before memory, update ontology. Canonical names: `/root/AAA/canon/CANONICAL_GLOSSARY.md`. Session eurekas: `/root/AAA/canon/EUREKA-SESSION-2026-09-KVM8.md`.

## Human Interface — Arif owns chat, Hermes owns the VPS (F13, 2026-08-18)

Arif Fazil is a human. He hates the terminal.

1. **Phone santai** — `ssh vps` from Termux. Config already set. Do not mess with the VPS from the phone.
2. **VPS work** — tell Hermes. Hermes LIVE gateway lives on **KVM8** (`~/.hermes`, `forge` 100.64.0.2 / 72.62.71.199, truth node); KVM4 (`100.64.0.5`) is workshop (FED litellm + OpenClaw edge); KVM2 (`100.64.0.4`) is witness. (Machine map: `docs/MACHINE_MAP.md`)
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

**LOCALHOST_IS_PASSWORD doctrine:** Postgres, Redis, Qdrant, FalkorDB, Ollama,
NATS bind `127.0.0.1` with no auth. UFW blocks the outside. Full doctrine:
`/root/docs/LOCALHOST_IS_PASSWORD.md`.

### 30-second session start checklist

1. `source /root/.secrets/kunci-root.env` (5-R Protocol ready)
2. Read `/root/AGENTS.md` + `/root/CLAUDE.md`
3. Boot: `MCP '/init' prompt (arifos-kernel · 2026-09-04 supersede)` (Trinity-33 · RSI)
4. One-shot state pane: `now` — time + 10 federation surfaces + FRAME observer drift + last session carry. (`now --json` for machine-readable)
5. Deep probe if needed: `make health` (10 surfaces) or per-organ `curl :PORT/health`
6. Check dirty repos:
   `for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do git -C "$d" status -s; done`
7. Check deprecation map: `cat /root/AAA/docs/deprecation-registry.json | jq .`

**State-read conventions (2026-08-15):**
- `carry_forward.json` is hand-written by the closing agent. All timestamps ISO-8601 **UTC** (local = Asia/Kuala_Lumpur). Stamp a backup into `~/.local/share/arifos/carry_forward_backups/` when writing.
- HTTP 401/403 on a health endpoint = service UP, auth-gated. Only conn-refused/timeout = DOWN. FED :4000 no-auth endpoint: `/health/liveliness`.
- FRAME (:18085) is the independent observer — its output is evidence, never a verdict.

**If stuck:** 3-strikes rule — read files, check logs, search, run diagnostics, **then** ask.
