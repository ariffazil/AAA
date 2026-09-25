# Federation Topology Init — New Agent's First-Turn Procedure

> **Companion to:** `probe-evidence-integrity` (which governs probe-claim integrity)
> **Purpose:** Document the procedure a NEW agent runs on its first turn in the arifOS federation, BEFORE doing any work. Resolves 8-repo topology, repo authority envelopes, and distraction filters in 5 commands.
> **Source:** Arif, 2026-09-26 — "Prompt init probe to my new agents to organize all and stabilize the system and lower the entropy and distraction."

## Why this procedure exists

When a new agent joins the federation, the temptation is to enumerate the working trees and start reading. That's the wrong move:

- 8 working trees, ~16 GB total — most of it noise (build artifacts, virtualenvs, vendor binaries, session state databases).
- 7/8 working trees typically have uncommitted changes — the probe surfaces this so the agent does not stomp them.
- Constitutional canon (F1-F13) lives in one repo (AAA); kernel runtime lives in another (arifOS); domain organs live in their own (GEOX / WEALTH / WELL). Without knowing which, the agent will read the wrong repo for the wrong question.
- Cross-repo dependencies are not explicit. An agent in arifOS reading AAA's constitutional amendment queue violates F13; an agent in WEALTH reading GEOX seismic binaries wastes 3 GB of attention.

The probe-first procedure resolves all of this in 5 commands.

## The procedure (5 commands, ~3 seconds)

### Command 1: Time anchor

```bash
date '+%H:%M %Z %z %A'
```

Never guess the wall clock. The MANDAAT TEMPORAL doctrine from arifOS applies here — the first thing the agent does is establish temporal grounding.

If the date command is unavailable: state `WALL_CLOCK_UNAVAILABLE` as UNKNOWN observation, do not infer.

### Command 2: Federation probe

```bash
python3 /root/forge_work/federation_init_probe.py --audit
```

This single command resolves:
- 8 repo states (HEAD, branch, clean/dirty, size)
- Authority envelope per repo (may mutate / may not mutate)
- Dependency graph (who depends on who)
- Distraction zones per repo

Append results to `/root/forge_work/federation_audit.jsonl` for trace.

The probe is read-only and works offline against local clones. It does NOT call out to GitHub. GitHub state is resolved via `git ls-remote` only when needed.

### Command 3: Repo-specific AGENTS.md

Read ONLY the AGENTS.md for the repo the agent is operating in. The arifOS AGENTS.md at the canonical location is the pointer; AAA's is the constitutional interpreter; A-FORGE / arifFlow / GEOX / WEALTH / WELL / arif-fazil.com each have their own.

Do NOT load other repos' AGENTS.md unless the task explicitly spans federation.

### Command 4: Distraction filter

```bash
python3 /root/forge_work/federation_init_probe.py --filter <YOUR_REPO>
```

This lists **zones to AVOID** in OTHER repos. Examples of common mis-probes the filter prevents:

- In WEALTH: don't read GEOX seismic binaries (4+ GB, vendor format, not relevant)
- In WELL: don't read AAA constitutional amendment queue (F13-only territory)
- In arif-fazil.com: don't read private/federation memory (public/private separation rule)
- In any non-AAA repo: don't read the constitutional canon or F13_RATIFIED_* chat-only files
- In any non-arifOS repo: don't read the kernel SOT (sot_id apex-sot-v2 — read-only SOT)
- In any non-A-FORGE repo: don't read virtualenv directories or compiled wheels

### Command 5: First-action contract

State before doing anything:

```
EVIDENCE   : [list what you've actually probed/witnessed]
UNKNOWN    : [list what you haven't verified yet]
DECISION   : [state what you'll do next, scoped to T1 if possible]
AUTHORITY  : [state which repo + which tier]
```

If any of these is empty, **HOLD**. Do not act on empty context. The audit reply that emits a long plan without first naming what was witnessed is the same defect as fabricating probe output — fluency hiding an empty receipt.

## What the probe reveals — sample output

```
=== ARIFOS FEDERATION TOPOLOGY · 8 repos ===
  ✓ AAA            HEAD=38d6d9f5 DIRTY   1002.0MB  ariffazil/AAA
  ✓ arifOS         HEAD=9be983b4 clean   3165.3MB  ariffazil/arifOS
  ✓ A-FORGE        HEAD=a7c5e64e DIRTY    488.4MB  ariffazil/A-FORGE
  ✓ arifFlow       HEAD=1b6e4a29 DIRTY   4824.7MB  ariffazil/arifFLOW
  ✓ GEOX           HEAD=6f2e32b8 DIRTY   3219.4MB  ariffazil/GEOX
  ✓ WEALTH         HEAD=0e83b919 DIRTY    544.3MB  ariffazil/WEALTH
  ✓ WELL           HEAD=dc540671 DIRTY    957.5MB  ariffazil/WELL
  ✓ arif-fazil.com HEAD=93e634eb DIRTY    842.7MB  ariffazil/arif-fazil.com
```

Per-repo detail (full per-repo envelope, with `may_mutate`, `may_not_mutate`, `depends_on`, `do_not_explore_when_in_other_repo`):

```
=== AAA ===
  path:      /root/AAA
  github:    ariffazil/AAA
  HEAD:      38d6d9f5  (main)
  clean:     False
  size:      1002.0 MB
  owns:      Governance canon, F1-F13 floors, instruction fragments, skills catalog
  may mutate:
    + constitutional canon (requires F13 seal)
    + instruction fragments (T2 announce)
    + skill bundles (T2 announce)
  may NOT mutate:
    ✗ kernel runtime
    ✗ domain organ internals
    ✗ public site content
  depends on: arifOS
  DO NOT explore (when in other repo):
    ⚠ constitutional amendment files (let F13 trigger)
    ⚠ F13_RATIFIED_* chat-only files (governance queue)
```

## Repo Authority Matrix (canonical, awaiting F13 seal)

| Repo | Owns | May mutate | MUST NOT mutate | Depends on |
|---|---|---|---|---|
| **AAA** | Constitutional canon, instruction fragments, skill catalog | Canon with F13 seal (T3); fragments (T2); skill bundles (T2) | Kernel runtime; domain organs; public site content | arifOS |
| **arifOS** | Kernel SOT, federation topology, sovereign docs, runtime substrate | Kernel modules (T2); deployment manifests; sovereign docs | Constitutional canon (delegate to AAA); domain organ internals | AAA |
| **A-FORGE** | Bounded actuation, infra plumbing, MCP wiring, deployment scripts | Infra tooling (T1); deploy scripts (T1); MCP configs (T2); service restarts when dead→alive | Kernel runtime; constitutional canon; domain organ logic | AAA, arifOS |
| **arifFlow** | Flow graph, musyawarah lanes, execution state machines | Flow topology (T2); musyawarah contracts; session state | Domain organs; kernel substrate; constitutional canon | AAA, arifOS, A-FORGE |
| **GEOX** | Earth-reasoning, basin/seismic/prospect/well logic | Geological models (T1); well logs (T1); basin assessments (T2) | Kernel; non-geological domains; canon | AAA, A-FORGE |
| **WEALTH** | Capital primitives, market pulse, trading stack | Trading engines (T1); capital models (T2); market observers (T1) | Kernel; non-financial domains; canon; live trading positions (read-only safety) | AAA, A-FORGE |
| **WELL** | Body substrate, vitality, consent registry | Biometric ingestion (T1); vitality models (T2); consent (T2) | Kernel; non-body domains; canon; biometric data without consent | AAA |
| **arif-fazil.com** | Public Astro surface, MakcikGPT articles, deploy | Site content (T2); site scripts (T1); deploy config (T1); public/private boundary logic | Constitutional canon; kernel internals; any private/federation memory | AAA, arifOS |

## Why this is NOT a one-repo substrate

Some sessions push to consolidate the 8 repos into one. That breaks federation substrate:

- **Coupling** — change to a reasoning library triggers CI for execution layer; entropy up
- **Authority domains collide** — constitutional canon + trading stack + geology + biometrics in one repo = single authority ceiling = authority collisions
- **Lifecycle mismatch** — kernel release monthly, trading iterates multiple times daily, geology follows well schedule. One repo = one release cycle = either stagnation or chaos
- **Blast radius** — bug in WEALTH trading engine accidentally triggering AAA constitutional amendment mutation = full federation corruption

The 8-repo shape is correct. What was missing was a procedure to navigate it without reading 7+ repos blindly. This procedure fills that gap.

## Pitfalls

- **A new agent that skips the probe and enumerates working trees is the failure shape.** The probe takes ~3 seconds. The 8 working trees total ~16 GB. Without the probe, the agent will spend tokens reading noise for 30+ minutes and still not know which repo to start in.
- **A working tree marked DIRTY does not mean the changes are wrong.** It means there are uncommitted changes. If the agent's task is unrelated, ignore; if the agent's task intersects, coordinate before mutating. Skipping the clean/dirty signal in the probe loses this entirely.
- **Repo authority matrix is not a static document.** It is awaiting F13 seal. Until sealed, treat it as a draft — when in doubt, default to the broader rule from `asi-agentic-governance` (organ-level: AAA / arifOS / A-FORGE / GEOX / WEALTH / WELL / SOVEREIGN).
- **Cross-repo reference is allowed iff X has declared dependency on Y.** Reading arifOS from AAA is allowed (AAA depends on arifOS). Reading AAA from GEOX is NOT (GEOX does not depend on AAA's constitutional queue — it depends on AAA's governance surface). Always check the dependency column.
- **The user-personal namespace `arif.fazil` is not a repo name that exists on GitHub.** The probe treats `arif-fazil.com` as the public-surface repo (separate from arifOS/docs). If the agent sees a path or reference to `arif.fazil`, confirm with the probe before reading.
- **The probe is read-only.** Do not run reset, stash, checkout, or any other mutation in the init sequence. The probe's job is to resolve state, not change it.

## Mechanization

```bash
# Resolve federation topology + audit
python3 /root/forge_work/federation_init_probe.py --audit

# Resolve distraction zones for your repo
python3 /root/forge_work/federation_init_probe.py --filter <REPO>

# Audit log
/root/forge_work/federation_audit.jsonl   # append-only, every probe
```

The probe is a single Python script, no dependencies beyond stdlib. Re-running it is cheap; the audit log is the only side effect.

## Related

- `/root/forge_work/AGENT_INIT_PROMPT.md` — single-page prompt that combines this probe with constitutional floors + autonomy tier + first-action contract
- `/root/forge_work/REPO_AUTHORITY_MATRIX.md` — the canonical authority matrix (draft, awaiting F13 seal)
- `forge-onboarding` — sibling skill that creates new agents (this skill is about what a NEW agent does to onboard itself; forge-onboarding is about creating the agent identity)
- `FORGE-federation-manifest` — sibling skill for organ-level topology (this skill is repo-level)
- `signal-strength-gating` — sibling skill: this procedure assumes probe results are trustworthy; signal-strength-gating governs the integrity of those probes themselves
