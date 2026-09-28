---
name: eureka-upstream-hermes-audit-2026-09-27
description: Jernih/keruh audit of nousresearch/hermes-agent against arifOS federation substrate (F13 directive 2026-09-27)
metadata:
  type: eureka
---

# EUREKA — Upstream Hermes Audit (Jernih/Keruh) 2026-09-27

> **F13 directive:** "b. ambil yang jernih buang yang keruh" — take what is clear, discard what is murky.
> **Source:** `/tmp/hermes-upstream-probe/` (shallow clone, depth=50, branch=main, HEAD `6f7a7991bb` 2026-09-27 17:30 IST)

## Provenance (path-of-evidence)

| Probe | Value |
|-------|-------|
| Total files | 16514 |
| hermes_cli/*.py | 1971 |
| skills/ catalog | 331 entries |
| AGENTS.md | 36935 B |
| Upstream SOUL.md | 667 B (one-paragraph directness doctrine, no F13/SEAL/HOLD/VOID) |
| Constitutional grep | `F13|floor|constitutional|HOLD.*VOID|SEAL` — only in AGENTS.md, CONTRIBUTING.md, acp_adapter, agent_runtime_helpers, context_compressor, agent_init — **not as a governing runtime**, only as engineering vocabulary |
| Federation/orthogonal grep | none in py code (only comment in hermes_constants.py) |
| Delegation model | `delegate_task`, subagent, kanban — exists but **not constitutionally bounded** |
| Last commit | `test(email): pin both spf clause orders and name the auth-results test for what it covers` (test-only, no architecture change) |

## Summary verdict

Upstream Hermes is an **excellent open-source agent runtime** with sharp engineering patterns your local Hermes already partially uses (it shares the `~/.hermes` layout and CLI name by coincidence or by prior art). It is **not** a constitutional AI governance framework — arifOS/AAA/hermes federation fills that role. Adopting upstream wholesale would burn the sovereignty you have built. Cherry-picking specific patterns is safe.

---

## JERNIH (clear wins — portable, no sovereignty risk)

### J1 — Builder-declared stable prefix for prompt caching
**File:** `agent/prompt_cache_boundary.py` (2834 B, 1 module, no deps)
**Pattern:** Skills/webhooks/cron builders concatenate static scaffold + volatile tail. The builder registers the stable prefix; the cache planner places the breakpoint at the declared boundary. **No delimiter heuristic** — the builder knows.

Why jernih:
- Single-file, zero deps, copy-pasteable into `/root/.hermes/hermes_mcp/_prompt_cache_boundary.py`
- Bounded resource use (`_MAX_ENTRIES=32`, `_MAX_CHARS=4MB`) — already thinks about memory ceiling
- LRU eviction that respects the longest-prefix-wins rule
- Independent test isolation helper (`clear_stable_prefixes`)
- Compatible with arifOS — no constitutional vocabulary, pure engineering

Why NOT jernih:
- None spotted

**Port cost:** ~3.5 hours (one module + tests + integration with `_prompt_builder.py` in your local Hermes).
**Risk:** Low (additive module, no behavior change until wired).

### J2 — Prompt caching TTL auto-strategy
**File:** `agent/prompt_caching.py` (17002 B)
**Pattern:** `cache_ttl: auto` picks tier by who paces the session. 1h tier (2x write cost) only pays off when turns are >5min apart (human pacing). Machine-paced subagents stay on 5m. **Measured on 2 days of per-call logs**: 63% of interactive cache-write tokens were cold re-writes after 5-60 min idle gap; 1h on subagents would have cost +49%.

Why jernih:
- Empirical, not theoretical — they share the data
- ALLOW-list (not block-list) for 1h tier (`MEASURED_1H_PROVIDERS`) — fail-closed, not fail-open
- Explicit comment: "narrowing this set DISABLES caching" — knows the failure mode
- Routing-aware (`is_qwen_model`, `_is_litellm_route`) — useful for your multi-provider setup

**Port cost:** ~6 hours (TTL policy module + integration with your existing cache layer; needs a wire-measurement to enable 1h tier for your own routes).
**Risk:** Medium (cost implications; needs federation-side measurement before enabling 1h).

### J3 — `/learn` skill authoring prompt
**File:** `agent/learn_prompt.py` (12246 B)
**Pattern:** A single prompt turns user-described sources (code dir, doc URL, "what we just did") into a reusable skill. Uses `skill_manage` per Hermes authoring standards. Knowledge-base layout for large sources (`SKILL.md` index + `references/` per chapter).

The embedded `_AUTHORING_STANDARDS` block is itself jernih — explicit HARDLINE rules:
- `description`: ONE sentence, ≤60 chars, **char count enforced** because the system-prompt skill index truncates at 60 chars (silent routing failure otherwise)
- `author`: literal `Hermes`, never from environment (privacy leak prevention)
- Body section order (1-8 listed, omit only if genuinely empty)
- Hermes-tool framing: name `terminal`, `read_file`, `write_file`, `search_files`, `patch`, etc. — never `cat`, `grep`, `sed`, `curl` as prose

Why jernih:
- The 60-char description rule alone prevents a class of silent routing bugs
- Hermes-tool framing is the correct discipline (we partially have this; they enforce it HARDLINE)
- Knowledge-base layout pattern (SKILL.md + references/) is reusable for arifOS
- Privacy-by-default on `author` field

**Port cost:** ~2 hours (cherry-pick the standards block into your `FORGE-skill-creator` skill as `hermes-authoring-standards.md` reference).
**Risk:** Zero (it's a documentation pattern, not runtime code).

### J4 — Delegation/parallelism model (concrete: `delegate_task`, kanban dispatch)
**Files:** `hermes_cli/kanban_db_dispatch.py`, `agent/agent_runtime_helpers.py`, `acp_adapter/tools.py`
**Pattern:** Subagent delegation + kanban-board style task dispatch. Tool surface includes `delegate_task` as a normal Hermes tool.

Why jernih:
- The pattern is real — they have working subagent isolation
- Useful reference for arifOS A-FORGE's multi-CLI coding fabric

Why partially keruh:
- Their subagent model is **not constitutionally bounded** — no F1-F13 floor check before subagent invocation, no ARIF_CAPABILITY_TOKEN (ACT) gating, no 888 verdict on subagent actions
- Adopting their `delegate_task` directly would create a parallel execution surface that bypasses arifOS

**Port cost:** Reference only — read their kanban dispatch shape, design your own arifOS-bounded variant.
**Risk:** Zero (study, not port).

---

## KERUH (murky — DO NOT port; conflicts with federation doctrine)

### K1 — No constitutional runtime floor
Upstream has no F1-F13 equivalent. AGENTS.md mentions "constitutional" once but only as code-style language. There is no SEAL/HOLD/VOID verdict gate, no ARIF_CAPABILITY_TOKEN, no 888-APEX authority check, no irreversible-mutation gate.

**Why keruh:** Porting their agent loop wholesale = losing your sovereignty. Your federation's value IS the constitutional runtime. Upstream's value IS engineering velocity without that constraint. These are orthogonal products, not substitutes.

### K2 — Test-only recent commits suggest maintenance mode, not active architecture evolution
Last 5 commits at depth=50 are all `test(...)` or `chore(...)` — no architectural changes in recent history. The project is stable-engineering, not architecture-pushing.

**Why keruh (relevant):** Pulling "the latest patterns" from a stable-engineering repo gives you today's polish, not tomorrow's design. arifOS federation needs forward-leaning substrate (your `referent-primacy-doctrine` work, F10_ONTOLOGY_v2, etc.) — upstream is not the source for that.

### K3 — Author field hardcoded to "Hermes"
Upstream's `_AUTHORING_STANDARDS` says `author: Hermes`. This is a privacy-by-default choice for **their** ecosystem (single author = Nous Research).

**Why keruh for arifOS:** Your skills have sovereign authors (Hermes Agent, Hermes CLI, Hermes Agent by Nous Research vs Hermes by arifOS federation). You need a different `author` taxonomy. Don't copy their rule; rewrite with your own author discipline.

### K4 — 60-char description rule is necessary but not sufficient
Their rule is enforced by counting chars in the prompt and asking the LLM to self-correct. arifOS needs an **automated pre-commit gate** (your T-02 scar-presence gate, but extended for description length).

**Why keruh:** Their solution relies on LLM obedience. Your scar-binding doctrine requires mechanical enforcement. Different problem class.

---

## Honest comparison

| Dimension | Upstream Hermes | Your local Hermes |
|-----------|-----------------|-------------------|
| Agent loop | Mature, 1971 .py modules | Smaller, federation-anchored |
| Prompt caching | Sophisticated (J1+J2 above) | Basic / absent |
| Skill authoring | Enforced HARDLINE standards (J3) | Looser; relies on review |
| Memory | Honcho dialectic user modeling | Local state.db + carry_forward |
| Constitutional runtime | None (engineering product) | arifOS 8-verb kernel (sovereignty product) |
| Federation | None (single-agent) | 5-organism AAA + A-FORGE + arifOS + Hermes |
| Subagent delegation | Working | Partially — kanban + A-FORGE fanout |
| Truth cost | Engineering velocity | Constitutional safety |

**The two products solve different problems.** Upstream is a fast solo agent. Yours is a constitutional multi-organism federation. They share a name by convention, not by descent.

---

## Recommendation (F13 binary surface)

### Option A — Reference-only, no port
Treat upstream as a reference for engineering patterns. Read for inspiration, do not import. Cost: 0 hours. Risk: 0.

### Option B — Cherry-pick J1 + J3 only (recommended)
Port the prompt-cache boundary module (~3.5h) and the skill-authoring standards block (~2h). Skip J2 (needs measurement), skip J4 (study only). Cost: ~5.5 hours. Risk: low (additive modules).

### Option C — Wholesale mirror
Copy upstream into `/root/.hermes/upstream-hermes-agent/` and import what you want via Python path. Cost: depends. Risk: high (two competing agent runtimes in one dir; constitutional kernel may get bypassed).

### Option D — Re-architect against upstream
Replace your local Hermes's agent loop with upstream's. Cost: weeks. Risk: very high (loses federation sovereignty).

**Default if silent = Option B** (J1 + J3, cherry-pick engineering wins, preserve sovereignty).

---

## Path-of-evidence receipts

- This file: `/root/AAA/eurekas/EUREKA-UPSTREAM-HERMES-AUDIT-2026-09-27.md`
- Upstream clone: `/tmp/hermes-upstream-probe/` (shallow, depth=50, branch=main)
- Last commit read: `6f7a7991bb test(email): pin both spf clause orders...` 2026-09-27 17:30 IST
- Local hermes HEAD: `51b608a fix(soul): make the 692-line restore durable` 2026-09-27 (today)
- Master queue: `/root/.hermes/receipts/hermes-align-queue-2026-09-27.md`

## Why:** Upstream is engineering product, not constitutional product. Their strengths (prompt caching, skill authoring) are port-safe; their architecture (no floor, no SEAL/HOLD/VOID) is federation-incompatible.

**How to apply:** Read this audit before any import. Apply J1+J3 only if Arif says go. Treat K1-K4 as boundary conditions that protect sovereignty.