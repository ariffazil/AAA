---
title: "Scar — Kimi Site Audit Fabrication (Trusted Docs Over Runtime)"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: scar
status: canonical
tags: [kimi, fabrication, site-architecture, audit, documentation-drift, caddy, deployment]
confidence: high
domain: infra/agent-behavior
severity: medium
actors: [kimi-agent]
sources:
  - /root/.config/caddy/Caddyfile
  - /root/arif-sites/infra/domains.yml
  - /root/arif-sites/.github/workflows/deploy.yml
  - /root/.arifos/agents/kimi/skills/site-architecture/SKILL.md
  - session-log-2026-05-17
---

# Scar — Kimi Site Audit Fabrication (Trusted Docs Over Runtime)

## What Happened

On 2026-05-17, user asked about three subdomains: `arif-fazil.com`, `arifos.arif-fazil.com`, `aaa.arif-fazil.com`.

Kimi agent (Constitutional Clerk) responded by reading the `site-architecture` skill table and `domains.yml`, then claimed:

> "All three subdomains are online (HTTP 200)."
> `arif-fazil.com` — "The primary human-facing landing page" (backend: Static / Cloudflare Pages)
> `arifos.arif-fazil.com` — "Documentation / static docs for the arifOS constitutional kernel" (backend: Static docs / Cloudflare Pages)
> `aaa.arif-fazil.com` — "The interactive cockpit (React dashboard) for the AAA control plane" (backend: AAA React + A2A API)

**The user challenged the deployment backend claim:** "why not out vps machine here the deployment backend? are u sure its cloudflare pages?"

## The Failure Chain

```
1. User asks about three subdomains
2. Agent reads skill table → sees "Cloudflare Pages" for arif-fazil.com and arifos.arif-fazil.com
3. Agent reads domains.yml → confirms "deploy: cloudflare-pages"
4. Agent answers: deployment backend is Cloudflare Pages
5. User challenges: asks about VPS
6. Agent investigates live runtime → discovers Caddyfile serves from /var/www/html/
7. Agent verifies headers → Last-Modified matches VPS file mtime exactly
8. Agent discovers cf-cache-status: DYNAMIC (Cloudflare proxying to VPS origin, not Pages edge)
9. Agent corrects answer: VPS is the live origin
```

## Root Cause

**Three systemic failures:**

1. **Trusted documentation over runtime evidence:** The agent read `domains.yml` and the skill table — both claim Cloudflare Pages — and answered without verifying the live system. Documentation drifted from reality.

2. **No header verification before claiming deployment backend:** A single `curl -sI` would have revealed:
   - `last-modified: Sat, 16 May 2026 14:39:27 GMT` — matches `/var/www/html/arif/index.html` mtime on disk
   - `cf-cache-status: DYNAMIC` — Cloudflare is proxying to origin, not serving from Pages edge cache
   - `server: cloudflare` — only means Cloudflare is proxying, not that Pages is serving

3. **Skill table was stale:** The skill listed removed subdomains (`travel`, `waw`, `apex`, `arifosmcp`) as "Active" and omitted live subdomains (`wealth`, `well`, `ollama`).

## The Real State (Verified After)

Live runtime evidence:

| Check | Result |
|-------|--------|
| Caddyfile | `arif-fazil.com` → `root * /var/www/html/arif` + `file_server` |
| Caddyfile | `arifos.arif-fazil.com` → `root * /var/www/html/arifos` + `file_server` + `/mcp*` proxy |
| Caddyfile | `aaa.arif-fazil.com` → `root * /var/www/html/aaa` + `file_server` + `/a2a/*` proxy |
| File mtime | `/var/www/html/arif/index.html` modified 2026-05-16 14:39:27 |
| HTTP header | `last-modified: Sat, 16 May 2026 14:39:27 GMT` — exact match |
| HTTP header | `cf-cache-status: DYNAMIC` — origin served, not edge cached |
| DNS | Resolves to Cloudflare proxy IPs (104.21.25.142, 172.67.134.76) |
| Deploy script | `deploy-site.sh` references `/opt/arifos/src/arif-sites/` — path does not exist |

**Conclusion:** The VPS is the active origin. Caddy serves static files from `/var/www/html/`. Cloudflare is a proxy layer, not the Pages edge. Whether a Cloudflare Pages project also deploys these sites is unverified — but it is not the live backend.

## TREE777 Lesson

**Documentation is a hypothesis. Runtime is the verdict.**

When asked about deployment, infrastructure, or active architecture:

1. **Read the Caddyfile first** — `/root/.config/caddy/Caddyfile` is the live routing truth
2. **Probe the headers** — `curl -sI` reveals origin vs edge, cache status, and timestamp matching
3. **Check the filesystem** — `/var/www/html/` contents and mtimes prove what is actually being served
4. **Cross-reference last** — `domains.yml`, skill tables, and CI comments are aspirations, not evidence

**Rule from TREE777 — Evidence-First Protocol:**
> Ask: 1) What does the live config say?
>     2) What do the HTTP headers say?
>     3) What does the filesystem say?
>     4) Only then consult documentation — and flag discrepancies.

## What Should Have Happened

```
1. User: "arif-fazil.com, arifos.arif-fazil.com, aaa.arif-fazil.com"
2. Agent: Read Caddyfile → sees file_server from /var/www/html/
3. Agent: curl -sI https://arif-fazil.com → checks last-modified + cf-cache-status
4. Agent: stat /var/www/html/arif/index.html → confirms mtime match
5. Agent answer: "All three are online (HTTP 200). Live origin is this VPS — Caddy serves from /var/www/html/. Cloudflare is proxying (not Pages edge). Note: domains.yml claims Cloudflare Pages, but runtime evidence contradicts this."
```

**Why this is better:**
- States the verified fact first (VPS origin)
- Notes the documentation discrepancy honestly
- Prevents the user from having to correct the agent
- Preserves trust in agent architectural assessments

## Anti-Pattern to Avoid

**The Documentation-First Fabrication Loop:**
```
read_skill_table → trust_claim → answer_user → user_corrects → investigate_runtime → admit_error
```

This pattern damages credibility because:
1. The agent presents documentation as fact
2. The user, who knows the ground truth, is forced to challenge it
3. The agent only verifies after being challenged
4. Future architectural answers from this agent are treated with suspicion

## Meta-Skill: Scar-Distill Pattern

This scar demonstrates the **scar-distill** pattern in TREE777:

1. **Event**: Agent answered deployment question from stale skill table → false claim → user correction
2. **Evidence**: Caddyfile, HTTP headers, filesystem mtimes, DNS resolution
3. **Pattern**: Documentation-first reasoning without runtime verification
4. **Lesson**: Runtime evidence > documentation claims; headers and filesystems are ground truth
5. **Promote**: Add `evidence-first-infrastructure` to skill verification protocols

## Confidence: HIGH

All facts verified against:
- Live Caddyfile (`/root/.config/caddy/Caddyfile`)
- HTTP response headers (`curl -sI`)
- Filesystem state (`/var/www/html/`)
- DNS resolution (`dig`)

## Related Scars

- `scar-hermes-fabrication-2026-05-17` (fabrication pattern — agents claiming things they haven't verified)
- `scar-openclaw-diagnostic-cascade-2026-05-17` (diagnostic without evidence-first check)

## TREE777 Update Required

1. Update `/root/.arifos/agents/kimi/skills/site-architecture/SKILL.md` → version 2.1.0 ✅
2. Update `/root/AAA/wiki/skills/federation/skill-site-architecture.md` → version 1.1.0 ✅
3. Add `evidence-first-infrastructure` checkpoint to all infrastructure skills

---

*DITEMPA BUKAN DIBERI — Scars are forged from failure, not from comfort.*
