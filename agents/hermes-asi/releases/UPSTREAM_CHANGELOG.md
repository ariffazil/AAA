# Hermes Agent — Upstream Drift Changelog | 2026-06-22

**Forged by:** FORGE (000Ω) at 888 directive (Arif, 2026-06-22)
**Scope:** `agents/hermes-asi/` documentation sync with installed runtime
**Severity:** T1 autonomous (metadata only) — no production runtime change
**Reversibility:** `git revert <this-commit>` (1 step)

---

## TL;DR

Our Hermes runtime is **installed at v0.16.0** but **documented at head 2517917d** (a 10-day-stale reference). Upstream has shipped **v0.17.0** since. This PR closes the metadata gap and documents the v0.16.0 → v0.17.0 delta so the next agent knows exactly where we stand.

**No code change. No runtime change. No risk.**

---

## 1. T1 State Observed (2026-06-22)

### Installed runtime

```
$ /usr/local/bin/hermes --version
Hermes Agent v0.16.0 (2026.6.5) · upstream 1ec4fcf6
Project: /usr/local/lib/hermes-agent
Python: 3.13.7
```

| Field | Value |
|-------|-------|
| Binary path | `/usr/local/lib/hermes-agent/` |
| Version | **v0.16.0** (`v2026.6.5`) |
| Upstream commit pinned | `1ec4fcf6` |
| Released | 2026-06-05 |
| Live processes | PID 1845310 (gateway), PID 1096661 (federation-memory-broker) |
| Constitutional binding | F1–F13 floors preserved (arifOS MCP :8088) |
| ART reflex | Permanent fixture in `SOUL.md §0` (per IDENTITY.md) |

### Documentation claim (BEFORE this PR)

| File | Claimed |
|------|---------|
| `IDENTITY.md` line 28 | `Binary \| Hermes Agent (Nous Research fork, head 2517917d)` |
| `agent-card.json` `provider.runtime` | `"Hermes Agent (Nous Research fork, head 2517917d)"` |
| Agent card version | `3.0.0` (unchanged — version is agent-spec version, not hermes-version) |

**`2517917d` is between v0.14.0 (May 16) and v0.15.0 (May 28)** — ~10 days stale.

### Upstream latest

| Field | Value |
|-------|-------|
| Latest tag | **v0.17.0** (`v2026.6.19`) |
| Released | 2026-06-19 |
| Main HEAD | `5ff11a68` |
| Commits since our pin | 2,936 (from `2517917d` → main) |
| Commits since our installed | ~1,476 (from `1ec4fcf6` → main) |

---

## 2. v0.16.0 → v0.17.0 Delta (the 1,476-commit gap)

Total: **1,476 commits** between `v2026.6.5` and `v2026.6.19`. Selected security/reliability fixes of interest to arifOS:

| SHA | Date | Type | Why it matters to arifOS |
|-----|------|------|--------------------------|
| `2e5c04a` | 2026-06-07 | `fix(#37878): scrub operator environment before launching cua-driver MCP` | **F12 INJECTION floor aligned** — upstream now scrubs operator env before MCP launch. Constitutional cousin to our `arifos-untrusted-sandbox` skill. |
| `020e59d` | 2026-06-18 | `fix(agent): dampen empty-name phantom tool-call loop` | Reliability — prevents infinite tool-call loops from empty names. |
| `fcf6cb3` | 2026-06-18 | `fix(docker): supervised gateway uses --replace to take over stale holder (NS-505)` | Affects our `hermes-asi-gateway.service` systemd unit if/when we move to supervised docker. Currently NOT relevant (we use systemd directly). |
| `9c3c5da` | 2026-06-18 | `fix(backup): hermes import never overwrites volatile gateway runtime state (NS-501)` | Protects `state.db` from being clobbered during import — relevant if we ever run a backup-restore cycle. |
| `c661634` | 2026-06-18 | `fix(dashboard): stream file uploads via multipart instead of base64 JSON (NS-501)` | N/A — we use Telegram relay, not the upstream dashboard. |
| `0fa7d6f` | 2026-06-18 | `fix(desktop): never persist or restore a named custom provider as bare "custom"` | Model stack integrity — relevant to our `model_stack` field. |
| `07e785d` | 2026-06-18 | `fix(prompt): dedupe parallel-tool-call steer; correct its rationale` | Tool-call reliability — relevant to all F1-F13 tool invocations. |

### What we are NOT picking up (and why)

- **Dashboard / web UI changes** — we use Telegram relay, not upstream's web dashboard.
- **Provider-specific OAuth fixes** (`6f89e17`, `c5eb64b` for xAI) — we don't use xAI.
- **Desktop app fixes** — we don't run the desktop binary.
- **WhatsApp bridge** — we use Telegram only.

---

## 3. Decision — HOLD AT v0.16.0

| Question | Answer | Rationale |
|----------|--------|-----------|
| Upgrade to v0.17.0 now? | **NO** | 1,476 commits = breaking-change risk. Our constitutional binding (F1–F13 via arifOS MCP) + federation broker plugin (`federation-memory-broker/broker.py`) need staging test before production. |
| Cherry-pick critical fixes? | **DEFERRED** | Need `git log` audit on `/usr/local/lib/hermes-agent/` to confirm whether these were already pulled via pip/source update. If yes, no cherry-pick needed. If no, evaluate per-fix blast radius. |
| Document the gap? | **YES (this PR)** | F2 TRUTH — labels drift explicitly so future agents don't make decisions on stale metadata. |

### What this PR does

1. **`IDENTITY.md` line 28:** `head 2517917d` → `head 1ec4fcf6, v0.16.0`
2. **`agent-card.json` `provider.runtime`:** same string update
3. **`agent-card.json` new field:** `upstream_drift` — full audit structure (installed, documented_prior, upstream_latest, drift_metrics, decision, changelog_ref)
4. **New file:** `releases/UPSTREAM_CHANGELOG.md` (this file)

### What this PR does NOT do

- Does not modify installed binary
- Does not modify systemd units
- Does not modify SOUL.md, AGENTS.md, or any constitutional document
- Does not touch the live Telegram bot state
- Does not push to upstream NousResearch (that's a 888_HOLD action)

---

## 4. Risks + Reversibility

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| JSON schema drift (agent card breaks A2A discovery) | very low | low | Field added is purely additive; existing keys unchanged; JSON validated before commit |
| Documentation regresses on merge | low | low | This file + the upstream_drift field preserve the old value as `documented_prior` |
| Future agent reads `head 2517917d` from stale docs | low | low | Greppable: `1ec4fcf6` is the new canonical string; `documented_prior` field preserves history |

### Reversibility

- **Per-file:** `git checkout main -- agents/hermes-asi/IDENTITY.md agents/hermes-asi/agent-card.json && git rm agents/hermes-asi/releases/UPSTREAM_CHANGELOG.md` (3 commands, no merge conflicts)
- **Whole-commit:** `git revert <sha>` (1 command, automatic 3-way merge)
- **Whole-PR:** `git reset --hard origin/main` on the branch (1 command, discards all 3 changes)

---

## 5. Next-cycle Recommendations

These are NOT executed in this PR — surface for 888_HOLD:

1. **v0.17.0 upgrade staging test** — spin up v0.17.0 in a sandbox, run federation-broker against it, verify F1-F13 binding survives.
2. **Cherry-pick `2e5c04a` (operator env scrub)** — independently verify if it's in our v0.16.0 (since 2e5c04a is dated 2026-06-07, AFTER v0.16.0 release 2026-06-05, so it's NOT in our installed binary).
3. **Cherry-pick `020e59d` (phantom tool-call loop)** — same logic, dated 2026-06-18.
4. **External PR to NousResearch** — submit `optional-skills/arifos-constitutional-reflex/` if cultural fit confirmed.
5. **Daily drift check** — add cron line `0 6 * * * /usr/local/bin/hermes --version > /var/log/hermes-version.log 2>&1` to detect upstream drift the day it happens.

---

## 6. Evidence Paths

- This file: `/root/AAA/agents/hermes-asi/releases/UPSTREAM_CHANGELOG.md`
- Branch: `chore/hermes-upstream-drift-2026-06-22`
- Modified files:
  - `agents/hermes-asi/IDENTITY.md` (line 28)
  - `agents/hermes-asi/agent-card.json` (line 15 + new `upstream_drift` field)
  - `agents/hermes-asi/releases/UPSTREAM_CHANGELOG.md` (new)
- Audit receipt: `/root/forge_work/hermes-upstream-drift-audit-2026-06-22.md`

---

*Forged by FORGE (000Ω) — 000_INIT → 111_SENSE → 333_REASON → 555_JUDGE → 666_CRITIQUE → 777_FORGE → 999_SEAL compressed into one autonomous metadata PR.*
*DITEMPA BUKAN DIBERI.*
