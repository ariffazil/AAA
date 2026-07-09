# AAA — Repo Layout (canonical)

> **Forged:** 2026-07-09  
> **Purpose:** One map of where things live. Lower entropy. Disk wins over prose.  
> **Status:** L2 live structure after root organize pass.

---

## What AAA is

**Cockpit + state + A2A mesh.** Display, route, register, queue.  
**Not** law (arifOS), **not** hands (A-FORGE), **not** domain truth (GEOX/WEALTH/WELL).

Live service: `aaa-a2a.service` → `a2a-server/server.js` on `:3001`.

---

## Root (keep thin)

| Path | Role |
|------|------|
| `README.md` | Public SOT |
| `AGENTS.md` | Agent landing for this repo |
| `CLAUDE.md` | Agent instruction surface |
| `BOOT.md` / `RUNBOOK.md` / `CONTEXT.md` | Ops entry |
| `FEDERATION_CONTRACT.md` | Federation contract pointer |
| `ROOT_AGENT_CONFIG.yaml` | Machine agent registry config |
| `art_binding.canonical.yaml` | ART binding |
| `package.json` / `Makefile` / configs | Build & tooling |
| `GENESIS/` | Mandate + dual language + truth |

Everything else that used to clutter root is under `archive/root-sprawl-2026-07-09/`.

---

## Live spine (do not scatter)

```text
src/                 React 19 cockpit UI
a2a-server/          Live A2A gateway (systemd)
a2a/                 A2A specs, policies, static registry
agents/              Identities + runtime citizens
  hermes-asi/        Runtime incarnation (Telegram mind)
  openclaw/          Hands / gateway operator
  opencode/          Forge worker identity
  _external/         FI coding harnesses (grok, claude, …)
  _lanes/            Constitutional *lanes* (not live organs)
    333-AGI/         Reasoning mode
    555-ASI/         Critique / long-horizon mode
    888-APEX/        Verdict geometry (legacy top service absorbed)
    A-AUDIT/         Audit function (kernel/vault/forge paths)
    A-ARCHIVE/       Archive function (VAULT999 paths)
    777-forge/       Witness / forge instrument anchor
  _docs/             Agent meta prose
  _archive/          Dead agent trees
prompts/             AGENT_INIT (active init surface)
docs/                Architecture + organ map + invariants
docs/repo/           This layout + hygiene
contracts/           Governance YAML
registries/          Canonical registries (+ AAA_AGENTS_REGISTRY.json)
schemas/             JSON schemas
governance/          Human speech, adat, floor docs
public/ + dist/      Static / built cockpit assets
scripts/             Validate, export, ops scripts
tests/ + eval/       Tests and eval harness
forge_work/          Session work products (ephemeral-ish)
archive/             Historical / junk / root sprawl
```

Compat: `agents/333-AGI` → symlink → `agents/_lanes/333-AGI` (same for other lanes).

---

## Not separate live organs

| Name | Correct reading |
|------|-----------------|
| 333-AGI, 555-ASI | Reasoning **lanes** under `agents/_lanes/` |
| 888-APEX | Legacy top service; deliberation in AAA `a2a-server` / gateway |
| A-AUDIT, A-ARCHIVE | **Functions** on kernel / vault / forge paths |
| VAULT999 in this repo | Mirror / writer helpers only — canonical ledger is VPS + arifOS write |

Live federation organs: **arifOS · AAA · A-FORGE · GEOX · WEALTH · WELL · VAULT999**.

---

## Archive map

| Path | Contents |
|------|----------|
| `archive/root-sprawl-2026-07-09/` | Former root MD clutter |
| `archive/junk-2026-07-09/` | `.deb`, one-shot ingest |
| `archive/backups-2026-07-09/` | File backups (e.g. seal_chain.bak) |
| `archive/nested-AAA-2026-07-09/` | Mistaken nested `AAA/` folder |
| `_quarantine/` | Quarantined agent cards |

---

## Hygiene rules

1. **Root stays thin** — entry docs only; new prose goes to `docs/` or `forge_work/`.
2. **No runtime blobs in git** — `agents/*/runtime/` gitignored.
3. **No binary junk** — `*.deb` gitignored; use `archive/junk-*` if needed short-term.
4. **Lanes ≠ organs** — never describe `_lanes/*` as live systemd organs.
5. **Validate before claim:** `npm run validate:aaa`

---

## Verify

```bash
curl -sf http://127.0.0.1:3001/health
npm run validate:aaa
npm run validate:root-agents
```

---

*Organize pass 2026-07-09 — Grok Build. DRAFT layout receipt until sovereign SEAL if desired.*
