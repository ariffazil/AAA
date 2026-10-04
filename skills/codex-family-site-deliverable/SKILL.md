---
name: codex-family-site-deliverable
description: "Verify Codex / Claude Code / OpenCode / sibling-agent builds against the live arif-fazil.com surface — the gap between sibling-self-report-Done and live-URL-actually-changed. Companion to the codex skill for arif-fazil.com delivery. Trigger: a sibling report references an artifact (the WB Tire, the NYBSite output, the Codex build), user says 'stafford agentically' / 'use the file as context' / 'deploy lagi' / 'use the artifact', or a delegation prompt to a coding agent targets a /mnt/agents/output or forge_work path."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Codex, arif-fazil.com, Site-Deploy, F11, F13, file-authority]
    related_skills: [codex, claude-code, opencode, federation-runtime-forensics, verify-nested-sibling-reports]
---

# Codex & Sibling-Built Sites on arif-fazil.com — Deliverable Protocol

> **Use when:** delegating a web build (atlas, dashboard, page) to Codex, Claude Code, OpenCode, or any sibling coding agent that writes to `/mnt/agents/output/app/` or `forge_work/`, and the real deliverable is the **live** arif-fazil.com page.
>
> **Class of bug this prevents:** "Codex reports Done ✅. Live `/world` is still the 77-line link directory." — the gap between sibling self-report and observable federation state.

## The pattern (use as a checklist before AND after spawning)

### 1. Before spawning the agent — confirm the artifact actually exists

If the user references "the WB Tire artifact we built," "the NYBSite output," "the Codex build," etc. **do not trust the name.** Verify with a probe first:

```bash
ls -la /mnt/agents/output/app/ 2>/dev/null
find /mnt/agents -maxdepth 4 -type d 2>/dev/null
```

If the path doesn't exist, the artifact is a **plan**, not a build. Surface this to the user with three options:

| Option | What you do |
|---|---|
| A. Spawn Codex now | Write the prompt yourself (don't paste the alias), bind to arif-fazil.com paths, add the verifications below |
| B. Build it yourself | Scaffolds in-session, direct to `public/<path>/` |
| C. User pastes the artifact | Don't fire agents at unknowns |

### 2. The prompt → binding contract

Codex's natural output target is `/mnt/agents/output/app/`. The real arif-fazil.com target is `/root/arif-fazil.com/sites/arif-fazil.com/public/<path>/`. **Make the binding explicit in the prompt.** Without it, Codex delivers to a worktree nobody wires up.

```bash
# Codex prompt must include:
# (a) absolute target path inside arif-fazil.com
# (b) build command that produces dist/
# (c) the verify-pages gate
# (d) commit + receipt expectation
codex exec "Build <feature>. Output to /root/arif-fazil.com/sites/arif-fazil.com/public/<path>/. \
After build: run npm run build, then run \`make verify-pages\` from /root/arif-fazil.com. \
Report: build status, dist size, verify-pages result, 1-screenshot visual check. \
If verify-pages fails, fix routing before reporting Done."
```

### 3. The three lifecycle gates Codex skips if you don't require them

Non-negotiable on arif-fazil.com:

| Gate | Command | Why |
|---|---|---|
| **File-authority probe** | `cat /root/arif-fazil.com/canon/file-authority.yaml` | F11/F13 fail-closed: every target file must declare authority (CANON/DERIVED/SCRATCH/PROPOSAL/RECEIPT). Codex in `--full-auto` will write anywhere. |
| **Build verification** | `npm run build` (or equivalent) | Sibling self-reports "Built ✅" without running the build. |
| **Site deploy gate** | `make verify-pages` from `/root/arif-fazil.com/` | AGENTS.md §"SITE DEPLOY GATE" — every `dist/*/index.html` must HTTP 200 on the live site. 49 pages were built-but-404'd on 2026-08-03 because nobody wired `@spa_routes`. |

### 4. Verifying the sibling's claim yourself

The user's voice on this is consistent: *"he IS the integration layer."* When a sibling reports done, never relay. Probe:

```bash
# 1. Does the artifact exist at the claimed path?
ls -la /root/arif-fazil.com/sites/arif-fazil.com/public/<path>/

# 2. Does the live URL actually serve?
curl -sI https://arif-fazil.com/<path>/ | head -1   # expect HTTP 200

# 3. Does the build artifact exist?
test -f /root/arif-fazil.com/dist/<path>/index.html && echo OK

# 4. Sibling-report-vox probe (only if the live URL is 200)
curl -s https://arif-fazil.com/<path>/ | head -50
```

If any of these fail, **the sibling is wrong**. Reply:

> "Verdict: VOID. No `<path>` exists at `<expected>`. No action. Here is the gap: `<probe output>`."

Do not paper over with philosophy. Do not re-summarize the sibling's severity matrix.

### 5. The "Codex says Done" auto-stall case

When the user says "X deploy lagi" / "Stafford agentically" / "use the file as context, distill it" — and the referenced artifact doesn't exist — the agent (you) stalls in a clarifying-question loop. **Don't.**

- Surface the gap (1-line, with the probe output).
- Offer the three paths (A/B/C above).
- Stop. Wait for the user's path choice.

Expected reply shape: *"Codex doesn't exist. `/mnt/agents/output/app/` is empty. Pick A or B."*

## 6. The "Stafford agentically + build internal, no deploy" case (2026-08-06)

Distinct from §5. Pattern that arrives **after** §1 has resolved (artifact exists, user
sees the plan, and now gives a separate instruction set):

```
"Just use the file AS Context. Distill it to our agentic sistem. Make it arif-fazil.com. Stafford agentically"
"yes sebelum deploy Hang Check dulu segala benda aligned. Aku nak pi lunch. No need my approved Here. Just build internal ja. Nak deploy Roger."
```

Three load-bearing directives in this compound instruction:

| Directive | What it means | Default action |
|---|---|---|
| **"use the file as context"** | The plan + the sibling artifact together are the spec. Do not re-derive intent from scratch. | Read both, wire the deliverables together. |
| **"Stafford agentically"** | Delegate the build work to the right executor (sibling CLI / sub-agent / in-session). Don't second-guess. | Spawn it OR do it yourself if in-session is faster than coordination overhead. |
| **"Yes sebelum deploy hang check dulu segala benda aligned"** | Hang-check (alignment probe) BEFORE any `make deploy` or `cp dist/`. "Roger" is the user's deploy ack — not yet given. | Run the alignment probe, surface verdict, STOP. Do not deploy. |

**Hang-check is the iron rule.** Even when the build is GREEN and the URL would
obviously serve, hold position. The user's "Roger" arrives as a separate message,
in their own time, often hours later (e.g. after lunch). Deploying without it =
F1 AMANAH violation (irreversible consent missing).

**Alignment probes** (run before any deploy):

```bash
# 1. Does the build artifact exist at the staged path?
ls -la /mnt/agents/output/app/dist/
test -f /mnt/agents/output/app/dist/index.html && echo BUILD_OK

# 2. Does the bundle reference the live data sources (no API keys, CORS-friendly)?
grep -c "api.gdeltproject.org\|api.worldbank.org" /mnt/agents/output/app/dist/assets/*.js

# 3. Is the agent-readable layer present?
test -f /mnt/agents/output/app/dist/llms.txt && test -f /mnt/agents/output/app/dist/agent.json

# 4. Does the host's vhost routing know about the path?
grep "<path>" /etc/caddy/Caddyfile 2>/dev/null
```

Reply shape after hang-check (NO preamble, NO options menu, NO "Roger?" prompt):

```
✅ Hang-check passed. Build: <dist path>. Bundles: <hash>. Data sources: <probe output>.
Deploy is on your Roger. Standing down.
```

**Pitfalls — auto-stall patterns to break out of:**

- ❌ Asking "Should I deploy now?" or "Proceed with deploy?" — user has already
  said "Nak deploy Roger." Deploy happens on Roger, not on autopilot.
- ❌ Treating sibling Done as authority — re-probe the build exists, the bundle
  is valid, the agent.json is shipping. Sibling self-report is evidence, not
  verdict.
- ❌ Re-deriving the plan from scratch when the user said "use the file as
  context." The plan + the artifact ARE the spec. Read both, do not re-think.
- ❌ Spawning a sub-agent when in-session can do it in 5 tool calls. Stafford
  means delegating across capability boundaries (sibling CLI, external review,
  structured background work) — not burning tokens on coordination overhead for
  trivial tasks.

## Common file paths on arif-fazil.com

| Purpose | Path |
|---|---|
| Staging build target | `/mnt/agents/output/app/` (worktree, non-canonical) |
| Live site source | `/root/arif-fazil.com/sites/arif-fazil.com/public/<path>/` |
| Live site served | `https://arif-fazil.com/<path>/` |
| Build output | `/root/arif-fazil.com/dist/` |
| File-authority registry | `/root/arif-fazil.com/canon/file-authority.yaml` |
| Deploy gate | `make verify-pages` from `/root/arif-fazil.com/` |
| Caddy routing | `/etc/caddy/Caddyfile` (add `@spa_routes` entry for new pages) |
| Cloudflare fallback | `/root/arif-fazil.com/sites/arif-fazil.com/public/_redirects` |
| Latency evidence (freshness) | `find /root/arif-fazil.com -type f -newermt "2026-08-05" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*"` |

## What this is NOT

- ❌ A replacement for the `codex` SKILL.md (call-signs, flags, sandbox escape — those stay there).
- ❌ A general "verify any agent" skill (see `verify-nested-sibling-reports` / `federation-runtime-forensics` for that).
- ❌ A "deploy arif-fazil.com" runbook (see `/root/RUNBOOK.md` and the SITE DEPLOY GATE in `/root/arif-fazil.com/AGENTS.md`).

## When to update this skill

- A sibling agent claims "Built" but the live URL is 404 / unchanged → add the probe that would have caught it.
- The `make verify-pages` command changes → update the gate table.
- A new agent type (Kimi, Cursor, etc.) starts being delegated to → add a sibling-specific subsection.
- The user changes his mind about his own codenames (sign that the codename hygiene is drifting) → flag to memory, never assume persistence.
