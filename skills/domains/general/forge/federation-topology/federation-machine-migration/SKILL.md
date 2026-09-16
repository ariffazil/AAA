---
name: federation-machine-migration
description: "Use when moving the federation to a new machine."
version: 1.0.0
author: Hermes (i-ARIF)
license: internal
owner: Hermes (curator-managed)
risk_tier: medium
autonomy_tier: T1
tags: [migration, vps, federation, backup, handover, carry-forward]
triggers:
  - "move to new machine"
  - "migrate the federation"
  - "new VPS"
  - "machine migration"
  - "zen my HERMES / close session before move"
  - "prepare for handover"
---

# Federation Machine Migration — Readiness, Zen-Close, Verification

Class-level playbook for moving the arifOS federation (Hermes + ~30 systemd services + Docker data stores) from one machine to another. Forged from the 2026-09-02 KVM8 → new-host prep, which ran under severe hypervisor throttle (%st 76.3) — so the protocol is built for doing the right small things while the box is dying, and deferring the heavy things to a calm window.

## When to Use

- Sovereign says "move to new machine" / "get ready to migrate" / "zen and prepare for handover".
- Recurring throttle has triggered the capacity verdict (see `vps-cpu-throttle-triage` Step 6) and the sovereign chose machine isolation over cleanup.
- Any session that must end with a state a DIFFERENT machine can resume from.

## The tri-split manifest (core pattern)

Split everything into three buckets — never treat migration as one blob:

1. **Moves via git** — repos with GitHub remotes. Verify with `git remote -v` per repo. These need a clean push before move, nothing else.
2. **Moves manually, NEVER via git** — secrets, identity keys, runtime state, private lanes. List every path explicitly.
3. **Deferred heavy ops** — data dumps, full scans, service restarts. Run only when %st < 15.

The manifest goes INTO carry_forward.json (not a new file) so the target machine session inherits the plan.

## Step 1 — Inventory (read-only, safe under any load)

```bash
# repos + remotes
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do git -C "$d" status -s | head -5; done
git -C /root/.hermes status -s
# services + data
systemctl list-units --type=service --no-pager | grep -iE "arifos|forge|fed|apa|well|geo|wealth"
docker ps --format "{{.Names}}"
# machine identity + health
hostname; hostname -I; df -h / | tail -1; top -bn1 | grep %Cpu
tailscale status   # note: often NoState after provider issues — must re-auth on target
```

## Step 2 — Zen-close (the closing ritual, per AGENTS.md)

1. Commit verified changes; push. PITFALL: do NOT commit unverified half-finished work (e.g. an empty `skills/<name>/` dir with deleted source files) just to get a clean tree — flag it in carry_forward instead.
2. Write `/root/AAA/carry_forward.json`: session_close (ISO-8601 UTC), zen_state (verdict/FQ/known_issues), migration_manifest (target, what_moves_via_git, what_moves_manually, verification_after_move, deferred_heavy_ops), next_session.
3. Stamp backup: `cp /root/AAA/carry_forward.json /root/.local/share/arifos/carry_forward_backups/cf-pre-migration_$(date -u +%Y%m%dT%H%M%SZ).json`.

## Step 3 — What moves manually (the critical list)

- `/root/.secrets/` — kunci-root.env, ALL provider tokens, `aaa-identity/keys/*.pem` (Ed25519 **federation identity** — losing it breaks SOVEREIGN auth and every agent binding), `*.env`, `backups/`. NEVER in git.
- Hermes runtime: `/root/.hermes/config.yaml`, `SOUL.md`, `prompts/`, `agents/`, `memories/` (MEMORY.md, USER.md, SESSION.md, episodic/, governed.json, provenance-log.md), `lanes/private/` (0600 — relationship memory), `cron/jobs.json` (28+ jobs), `skills/`.
- Data volumes: postgres (decision_ledger, governed records), qdrant (vector), minio (artifacts), falkordb (graph), redis — pg_dump + qdrant snapshot + minio mirror.
- systemd unit files + env references for the ~30 services; docker compose stacks (searxng, minio, falkordb, qdrant, postgres).
- carry_forward backups dir.
- Tailscale/Headscale re-auth (identity is machine-bound; NoState on the source does not transfer).

## Step 4 — Verification after move (never trust the copy)

- `make health` (10 federation surfaces) — HTTP 401/403 = UP auth-gated; conn-refused/timeout = DOWN.
- `arif-bind --mode init` → SOVEREIGN FULL authority (or the MCP 2-step challenge-response per `arifos-auto-init`).
- ssh keys + `git push` works to github.com/ariffazil.
- Telegram gateway live (ASI_arifos_bot token).
- Restored data counts: pg_dump restore verify, qdrant point count, minio object count.
- Baseline %st < 5 on the new host (the whole reason for moving).

## Pitfalls

- DO NOT run the data dump during throttle — it extends the throttle window and can time out mid-dump. Defer to %st < 15.
- DO NOT restart services during a throttle storm (2026-09-01 openclaw restart-storm x52 scar).
- DO NOT push secrets to git "for convenience of migration" — 5-R protocol: never hardcode, never commit, never paste.
- DO NOT declare "migrated" without running Step 4 — a copy that was never verified is a guess.
- Hermes cron jobs are LOCAL-ONLY per session; jobs.json must be re-registered on the target.

## References

- `references/2026-09-02-kvm8-migration-prep.md` — the executed manifest from the first run: exact inventory, what was committed/pushed, deferred ops, known issues (fq-probe failed, tailscale NoState, disk 79%).
