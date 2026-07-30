---
id: FORGE-agentic-web-builder
name: FORGE-agentic-web-builder
version: 1.1.0-2026.07.30
description: >
  Build, deploy, audit, and repair arif-fazil.com constellation sites
  autonomously. Class-level umbrella: DOCTOR (web_zen CLI), DEPLOY, AUDIT,
  REPAIR, SEAL, EPHEMERAL. Humans use six missions — not tool menus.
  USE WHEN: "deploy site", "site down", "audit all pages", "404 on
  arif-fazil.com", "deploy-vps.sh", "makcikgpt broken", "web zen",
  "missions 404", "vitals proxies", "rsync --delete", "ephemeral tool".
  DO NOT USE FOR: Caddy SSL/DNS/tunnel (FORGE-infra-guardian), LLM SEO
  (AGI-web-optimization), generic CI/CD (FORGE-cicd-docker-deploy).
owner: FORGE (000Ω)
risk_tier: T2
floor_scope: [F1, F2, F4, F11]
autonomy_tier: ANNOUNCE
forged_from: INCIDENT-2026-07-23 + MISSIONS-ZEN-2026-07-30
---

# 🌐 FORGE — Agentic Web Builder

> One night, three identical failures: `organ_proxy.py` (code), `999/index.html`
> (doctrine), `static/wealth.html` (renderer output) — all lived ONLY in the
> deployed tree, all destroyed or nearly destroyed by deploys. This skill is
> the metabolized scar. **Nothing generated lives only in the deployed tree.**
>
> **2026-07-30:** Stop inventory cosplay. Humans → `/missions`. Agents →
> `web_zen.py doctor` before inventing a new deploy path.

## The One Law

```
VERSION CONTROL FIRST. LIVE TREE SECOND.
If a file must exist on a public site, it must exist in git first.
rsync --delete is an executioner — anything not in source is sentenced.
Capability ≠ authority. Ephemeral tools die. Permission stays with arifOS/Arif.
```

---

## OP 0 — DOCTOR (always first · anti-chaos)

```bash
python3 /root/arif-fazil.com/scripts/web-zen/web_zen.py doctor
```

| Mode | Band | Purpose |
|------|------|---------|
| `sense` | GREEN | source/live, Caddy missions routes, commodity :3456–3458 |
| `verify` | GREEN | content-truth crawl (SPA checks JS bundle, not shell HTML only) |
| `orphan` | YELLOW | dry-run `rsync --delete` — fail closed if deletes listed |
| `ephemeral` | GREEN | generate → test → destroy disposable script (no secrets) |
| `caddy-reload-hint` | ORANGE | systemd reload often fails NAMESPACE — use in-process `caddy reload` |

README: `/root/arif-fazil.com/scripts/web-zen/README.md`  
Human cockpit: `https://arif-fazil.com/missions` · Machine: `/missions.json`  
MCP: `forge_web_zen(mode=doctor)` · Kernel: `arif_route(mission_id=…)`  
Caddy reload: `systemctl reload caddy` (PrivateTmp=false fixed 2026-07-30)

### Known failure → fix (do not re-diagnose from zero)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `/missions` 404 | not in Caddy `@spa_routes` | add `/missions*`; `caddy validate`; `/usr/bin/caddy reload --config /etc/caddy/Caddyfile --force` |
| `/missions.json` 404 | not in `@root_static` | add path; reload as above |
| VITALS proxies UNAVAILABLE | gold/oil/gas API down | `systemctl start gold-api oil-api gas-api` (not API keys) |
| `systemctl reload caddy` fail NAMESPACE | host /tmp mount bug | in-process caddy reload (above) |
| Doctor fails SPA markers | checking HTML shell only | web_zen reads live `/assets/index-*.js` |

---

## OP 1 — DEPLOY (canonical path)

Canonical source: `/root/arif-sites/sites/` → built/synced to `/var/www/html/<site>/`
Canonical script: `/var/www/html/deploy-vps.sh` (mirrored in repo root)

**Pre-deploy checklist (mandatory):**
1. `cp -a /var/www/html /root/backups/www-html-$(date +%Y%m%d)-pre-<reason>` — snapshot BEFORE mutation. Tonight this snapshot saved two restores.
2. **Orphan detection** — before any `rsync --delete`, list what will die:
   ```bash
   rsync -avzn --delete SRC/ DEST/ | grep '^deleting' | head -50
   ```
   Any file you don't recognize = HOLD. Either seed it into source or quarantine it.
3. Verify the deploy script covers the site you're touching (oil/gas/gold/mcp/well were missing until 2026-07-23 — check `grep <site> deploy-vps.sh`).
4. Post-deploy: run OP 2 audit on affected hosts. "Deployed" ≠ "live". Verified = live.

**Host → source map:**
| Host | Live root | Source |
|---|---|---|
| arif-fazil.com | /var/www/html/arif | sites/arif-fazil.com (build → dist → rsync) |
| aaa | /var/www/html/aaa | sites/aaa.arif-fazil.com |
| arifos / geox / wealth | /var/www/html/<organ> | sites/<organ>.arif-fazil.com |
| mcp | /var/www/html/mcp | sites/mcp.arif-fazil.com (rsync, no --delete — .well-known live assets) |
| well | /var/www/html/well | sites/well.arif-fazil.com (llms.txt only) |
| /oil /gas /gold (apex paths) | /var/www/html/{oil,gas,gold} | dist/{oil,gas,gold} — exclude live api/ + vendor/ |

---

## OP 2 — AUDIT (full-crawl methodology)

74-URL method, proven 2026-07-23. Evidence dir pattern:
`/root/A-FORGE/forge_work/<date>/site-audit/`

1. **Enumerate hosts:** `grep -oE "^[a-z0-9.-]+\.arif-fazil\.com \{" /etc/caddy/Caddyfile | sort -u`
2. **Enumerate pages:** sitemap.xml `<loc>` entries + Caddy `@spa_routes` path list + every `handle` target + static handles (`@root_static`).
3. **Probe each:** `curl -s -o body -w "%{http_code}|%{size_download}" -L url`. 0-byte 404 = catch-all respond; 17-byte 404 = explicit respond directive. Both are failures for content pages.
4. **Content truth, not status codes** — a 200 with wrong content is a lie (F2):
   - /000 → BLAKE3 identity hash present
   - /999 → §8 Audit Path + grandfather rule
   - /economics → F2 bands + VOID tiles (patched renderer, not SPA shell)
   - dashboards → price/commodity markers
   - /data/wealth/latest.json → fresh date
5. **Dual-lane bot surfaces** (makcikgpt): test with bot UA (`GPTBot/1.0`, `curl/x`) AND browser UA (`Mozilla` + `Accept: text/html`). Bot lane serves .md/.html from `makcikgpt-md/`; browser lane gets SPA. Both must 200.
6. **404 triage:** file missing from live tree? handler missing from Caddy? matcher gap (`@root_static` list)? file never built (pre-existing gap — label it, don't fake-fix)?

---

## OP 3 — REPAIR (source/live convergence)

The drift detector for deployed content:

```bash
diff -rq <snapshot-or-source>/ <live>/ | grep "^Only in"
```

- **"Only in live"** = orphan. Seed into `public/` (survives build) → commit → redeploy. Never hand-edit live-only.
- **"Only in source"** = deploy gap. Check deploy script covers it.
- **Dual-copy divergence** (e.g. `999/index.html` vs `public/999/index.html`): converge to one canonical, sync, commit. Both copies must carry both truths.
- **Nested-dir restore error** (`cp -a src dst` when dst exists → `dst/src`): verify with `ls dst` after every restore; flatten with `cp -a dst/src/. dst/` then `mv dst/src quarantine/`.
- **Never `rm -rf`** — F1 tripwire will (correctly) block. Quarantine: `mkdir -p /root/backups/quarantine-<date> && mv target quarantine-<date>/`.
- **Caddy edits:** python exact-string patch → `caddy validate` → `systemctl reload` → verify affected URLs. Backup exists at `/etc/caddy/Caddyfile.bak.*`. Reload is T3-class: only under sovereign directive or incident repair with immediate verification.

---

## OP 4 — SEAL (evidence discipline)

1. Prefer `web_zen.py doctor --json` receipt under `forge_work/<date>/web-zen/`.
2. Crawl data (`results.tsv`), URL list, truth-check output → `forge_work/<date>/site-audit/AUDIT-REPORT.md`.
3. Source commits BEFORE seal (seal references commit hashes, not intentions).
4. `forge_vault(mode="seal")` with: scope, pass count, content-truth table, gaps closed, commits, skill.
5. Session-end: one seal, not two. F4.

## OP 5 — EPHEMERAL TOOL GENESIS (capability ≠ authority)

```bash
python3 /root/arif-fazil.com/scripts/web-zen/web_zen.py ephemeral \
  --task "mission gap: why needed" \
  --code-file /path/to/temp_tool.py
```

Loop: gap → search existing → reuse → generate → sandbox test → invoke → verify → **destroy** → promote only if repeated + human-approved.

GREEN: parsers, converters, disposable analysis. RED never self-grant: secrets, production deploy, persistent MCP, force-push, Caddy authority, payments. No `arif_create_random_tool` — modes under forge only.

## Anti-patterns (each cost real breakage)

- ❌ `rsync --delete` without orphan preview — destroyed 36 files 2026-07-23
- ❌ "Deployed" claimed without crawl verification — 7 landing pages were 404
- ❌ Generated content living only in live tree — organ_proxy/999/wealth.html
- ❌ Hand-editing live tree to "fix" — fix source, redeploy
- ❌ Status-200 audit without content grep — SPA soft-404 lies
- ❌ `rm -rf` for cleanup — quarantine instead
- ❌ Advertising 128 tools as intelligence — six missions + Canonical 8
- ❌ Skipping `web_zen.py doctor` and reinventing the deploy path every session

DITEMPA BUKAN DIBERI.
