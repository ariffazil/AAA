# HERMES ↔ UPSTREAM NOUS — CONTRAST & HARDENING MAP
**Date:** 2026-09-29 · **Agent:** HERMES (CLI seat) · **Filing:** report, not doctrine
**Local:** `v0.21.5+4028.gad72f95` (2026.9.24) · upstream `1243fccb` · local `ad72f95d` · **+9 carried commits · 0 behind**
**Upstream canon:** hermes-agent.nousresearch.com/docs (fetched fresh this session, llms.txt + 4 feature pages)

---

## 0. VERDICT (one line)

The harness is not behind upstream — it is **carrying upstream's debt on two surfaces it does not own**: a
skills catalogue 8× upstream's design budget (25,000 tok paid every turn, 63.5% of it never opened) and a
tool mesh 10× its demonstrated use (27 servers, 1.64% of all calls). Meanwhile the **maintenance machine
that upstream ships to fix exactly this is green and idle** — the curator runs, the usage sensor records,
and nothing ever transitions. The fork's 9 carried commits are *ahead* of upstream and should be sent back.

---

## 1. MEASURED REALITY (every figure re-derivable from the printed command)

### 1.1 Fixed prompt tax — paid every turn of every session
```
hermes prompt-size --json
```
| Line item | chars | ≈tokens |
|---|---|---|
| **system_prompt total** | **211,502** | **52,875** |
| — skills index | 99,922 | 24,980 |
| — memory | 2,330 | 582 |
| — user profile | 1,478 | 369 |
| tools (25 loaded) | 44,661 JSON bytes | ~11,165 |

Tier split:
| Tier | chars | % of prompt |
|---|---|---|
| stable (identity/guidance/skills) | 68,491 | 32.4% |
| context (AGENTS.md/cwd) | 37,671 | 17.8% |
| **volatile (memory/profile/timestamp + skills index)** | **105,336** | **49.8%** |

**The skills index alone is 47.2% of the entire system prompt.**
Upstream's stated design budget for the same surface: *"Level 0: skills_list() → ~3k tokens"*.
We pay **8.3×** that.

### 1.2 Skills estate
```
find -L /root/.hermes/skills -name SKILL.md | wc -l      # 911  (incl. dot-dirs)
find -L /root/AAA/skills   -name SKILL.md | wc -l        # 1354 (incl. dot-dirs)
find /usr/local/lib/hermes-agent/skills -name SKILL.md | wc -l  # 294 — UNREACHABLE (loader never reads install tree)
```
| Measure | Value |
|---|---|
| Indexed skill names (dot-dirs excluded, both roots) | **706** |
| Distinct skills ever loaded (`skill_view` targets, all time) | **406** |
| Intersection (indexed **and** ever loaded) | **258** |
| **Indexed but NEVER loaded** | **448 = 63.5% of index** |
| **Loaded by a name the index does not carry** | **148 = 21% of index** |
| SKILL.md body text across both live roots | 30.1 MB |
| Skills packaged with `references/` (tier-2 disclosure) | 247 AAA + 2 local |
| Archive sediment inside live root | `/root/AAA/skills/.archive` = **380 SKILL.md** |

Top loaded (of 406): bridge-protocol 40 · hermes-agent 33 · governed-uncertainty 25 ·
abang-sado-creative-lane 25 · relationship-kernel 24 · image-gen-fallback-chain 22 · alpha-zen-lanes 22.

### 1.3 The maintenance machine — green, and idle
```
hermes curator status
```
```
curator: ENABLED   runs: 6   last run: 1d ago
last summary:  auto: no changes; llm: skipped (consolidation off)
curator-managed skills: 2 total   (agent-created=2  bundled=0)
unmanaged (no provenance marker): 8 total
```
- Upstream ships: usage telemetry, auto-transition `active → stale(14d) → archived(30d)`, pin, ledger,
  backup/rollback, archive-TTL purge, `adopt --all-unmanaged`.
- Live: `.usage.json` = **912 entries, 164 with zero use AND zero views, all `state: "active"`**.
- **Zero transitions have ever occurred.** The sensor is alive; the actuator is not connected to the estate
  (it manages 2 skills out of 706). Curator reports `no changes` and reads green.

### 1.4 Tool / mesh surface
```
python3 -c "... messages where tool_name like 'mcp__%' ..."
```
| Measure | Value |
|---|---|
| MCP servers configured | **31** (27 enabled, 4 disabled) |
| Deferred tools behind `tool_search` | **352** |
| Eager tools in the model-visible array | **25** |
| Total tool calls, all time | 76,049 |
| **MCP calls** | **1,247 = 1.64% of all calls** |
| Built-in calls | 74,802 = 98.36% |
| Servers ever called | 26 of 27 |
| Top-3 share of all MCP calls (aforge 234 · arifos 223 · wealth 184) | **51%** |
| Servers with ≤5 lifetime calls | chrome-devtools, chron, context7, deepwiki, frame, numeric-audit, postgres, zai-reader |
| Servers never called | **doc-tables** |

### 1.5 Context contract — declared vs binding
```
model.context_length: 1000000      provider: custom:fed-federation
config keys tools / compression / lsp / checkpoints / auxiliary: ** ALL ABSENT **
```
All five control blocks are absent → upstream defaults in force, **un-owned by any doctrine**.
Harness declares a **1,000,000-token window**. If the local router (`127.0.0.1:4012` LISTEN) or the
upstream model clamps lower, the harness compressor **never reaches threshold and never fires**, and the
proxy silently drops older turns. UNKNOWN until the clamp is read. This is the highest-severity unverified
item in the report — a wrong window is self-consistent and silent.

### 1.6 Fork, cron, host
```
git log origin/main..HEAD --oneline    # 9 carries, 695 insertions / 14 files
hermes cron / jobs.json                # 18 jobs: 7 enabled, 11 disabled
cron/executions.db                     # 778 completed, 120 failed (13.4%)
```
- All 9 carries are **gateway delivery-integrity fixes** upstream does not have:
  delivery-ledger proof (`produced vs sent vs transport receipt`), bot→bot loop guard,
  mode propagation across the prepare→send seam (SCAR-2026-09-28-008), 403-is-final (no inline retry),
  sender identity on triggered group turns (SCAR-2026-09-28-006), retained-jargon guard.
- Cron deliver targets: A2A group 9 · Arif DM 3 · SADO 3 · origin 2.
- Only 4 distinct skills bound to cron jobs.
- Governance: `hooks.pre_tool_call` → `arifos-hermes-gate-hook.py`, `fail_closed: true`;
  **47,759 receipt lines** (the gate is deciding). 5 gateway hooks deployed.
- Host: 31 GB RAM (13 used) · disk **80% (308/387 G)** · load avg **6.02** · uptime 27 d ·
  `state.db` **1.16 GB**.
- AAA fleet: **40 agent cards** (23 FI), plus duplicate identities in `_lanes/_archive` and `_external`.

---

## 2. CONTRAST — 12 DIMENSIONS

| # | Dimension | Upstream | HERMES | Verdict |
|---|---|---|---|---|
| D1 | Prompt/index economy | ~90 bundled + ~60 optional skills; `skills_list ≈ 3k tok` | 706 indexed → 24,980 tok/turn (8.3× budget) | **BEHIND** |
| D2 | Skills maintenance loop | curator auto-transitions, ledger, rollback, adopt | enabled, 6 runs, manages **2**, 0 transitions | **WIRED, NOT OWNED** |
| D3 | Capability addressing | index label = loadable name | 148/706 loaded by names the index lacks | **BEHIND** |
| D4 | Tool disclosure | tiered `tool_search` (3 tiers, listing budget) | 352 deferred behind the bridge, 25 eager | **AT PAR** |
| D5 | Tool surface economy | — | 27 servers, 1.64% of calls, 8 servers ≤5 calls | **BEHIND** |
| D6 | Memory | 8 provider plugins (honcho, mem0, …) + dialectic user model | `mem0` active (309 search / 146 add) + federation memory | **AT PAR** |
| D7 | Delegation | subagent lifecycle API, durable completions | 388 `delegate_task` calls, working | **AT PAR** |
| D8 | Context/compression contract | micro-compaction (opt-in, cache trade declared) | all keys absent; 1M declared vs router clamp UNVERIFIED | **UNKNOWN-RISK** |
| D9 | Enforcement mechanism | native middleware for LLM **and** tool calls | shell hook text-classifier (`fail_closed`) | **DOCTRINE AHEAD / MECHANISM BEHIND** |
| D10 | Gateway delivery integrity | baseline | 9 carried commits upstream lacks (ledger proof, loop guard, mode propagation) | **AHEAD** |
| D11 | Federation mesh | none (single-agent product) | 31 MCP servers, 43 services, 40 agent cards, VAULT/WELL/WEALTH/GEOX organs | **AHEAD (no upstream equivalent)** |
| D12 | Drift | — | 0 behind, 9 carries, clean | **AT PAR** |

---

## 3. THE FIVE STRUCTURAL DEFECTS

**F1 — Attention tax on a catalogue two-thirds dead.**
24,980 tokens/turn for 706 names, 448 of which have never been opened once. Paid in *every* session,
on *every* turn, including the 98% of turns that use built-in tools only.

**F2 — A green maintenance machine with no actuator.**
The curator's transitions only apply to skills it *owns*. It owns 2. The estate lives in
`external_dirs: /root/AAA/skills` and in hand-authored dirs with no provenance marker. Upstream's fix for
the exact failure we have — catalogue obesity — is installed, running, and pointing at nothing.
`hermes curator status` reports success while 164 zero-use skills sit un-transitioned.

**F3 — The index lies about names (148 instances).**
A skill can appear in the index under one label and be loadable only under another
(`github-ops` in the index vs `FORGE-github-ops` at load). This is *capability addressing drift*:
the agent reads the selection surface, then calls a name the surface did not offer. Phantom/ghost pair —
the same defect class as a dead symlink, sign flipped.
(`apex_verdict_hold` is additionally present in **both** roots — LAW 8 violation.)

**F4 — Tool mesh 10× its demonstration.**
27 enabled servers, 352 deferred schemas, 1,247 MCP calls lifetime = 1.64% of all tool calls.
Half the MCP traffic goes to 3 servers. 8 servers have ≤5 calls. This is not free: the deferred
listing, the per-server degradation logic, the supervision surface, and the 4 parked/28 enabled split
are all *loaded doctrine that never executes*.

**F5 — Un-owned defaults on the highest-consequence knob.**
`tools`, `compression`, `lsp`, `checkpoints`, `auxiliary` are absent from config. Upstream defaults apply,
so we do not know what our compression threshold is, and we declare a 1M window we have not reconciled
against the router. §2 (runtime-audit) exists precisely because this failure is silent.

---

## 4. QUANTUM PATHWAYS (step-change, not incremental)

Ordered by leverage per unit of irreversible change. Each is reversible.

### Q1 — ATTENTION THERMOMETER (index diet) — *the single biggest distraction lever*
**Mechanism:** wire upstream's own archive transition to the live usage sensor, then archive the tail.
`active → stale → .archive/` is *out of the index* and *restorable by one command* — it is a shelf, not a
deletion. Target: hot set ≈ 120–150 skills (the 258 ever-loaded ∩ indexed, minus the tail), index ≈ 5k tok.
**Evidence:** 448 never loaded · 164 zero-use in `.usage.json` · 380 already sitting in `.archive`.
**Yield:** ~20,000 tok/turn reclaimed (index 25k → ~5k). Applies to every session, every agent.
**Cost:** one policy + one script. **Reversal:** `hermes curator restore <name>`.

### Q2 — CAPABILITY ADDRESSING TRUTH (one name, one door)
**Mechanism:** frontmatter `name:` becomes the only loadable identity; the index is generated from it;
a lint fails CI when index label ≠ loadable name. Run the rename wave once, then gate it.
**Evidence:** 148 loaded names absent from the index; 1 duplicate across roots.
**Yield:** removes the class of failure where a capable agent declares a capability missing, or loads
the wrong skill, because the selection surface and the load surface disagree.
**Cost:** lint + one rename wave. **Reversal:** renames are file-level, git-reversible.

### Q3 — GOVERNANCE FROM TEXT-CLASSIFIER TO TYPED MIDDLEWARE
**Mechanism:** port the `pre_tool_call` decision into an upstream **plugin middleware** (typed
call fields: tool name, argument object) and keep the shell hook as a fail-closed backstop, not the
primary. Upstream supports behavior-changing middleware for LLM calls and tool calls — the native surface
for exactly what `arifos-hermes-gate-hook.py` is approximating with regex over serialized JSON.
**Evidence:** the gate is *running* (47,759 receipts, `fail_closed: true`) but its error directions are
known: a file **path** containing a trigger word was read as a claim (refused a doctrine patch twice);
a **citation-shaped word** satisfied provenance. Text over `json.dumps` cannot tell an id, a path or an
enum from prose.
**Yield:** enforcement that cannot be fooled by a directory name, and 47,759 prose receipts become typed
records. This is the difference between a control that *runs* and a control that *catches*.
**Cost:** pilot one rule (provenance verification) in middleware, keep the hook as backstop.
**Reversal:** disable the plugin; hook unchanged.

### Q4 — TOOL SURFACE → CAPABILITY DOMAINS
**Mechanism:** 27 servers → ~8 hot domains + one **cold shelf** (implementation kept on disk, disabled in
config). Fewer deferred schemas → smaller listing → fewer wrong-tool substitutions and fewer
"capability not found" answers.
**Evidence:** 3 servers = 51% of MCP traffic; 8 servers ≤5 calls; `doc-tables` = 0.
**Yield:** smaller disclosure surface, fewer supervision units, less doctrine that never executes.
**Cost:** one config edit per server (yaml roundtrip, never string surgery — scar 2026-08-27).
**Reversal:** flip `enabled` back; nothing deleted.

### Q5 — CONVERGE THE FORK (send the 9 carries upstream; package our governance as a profile distribution)
**Mechanism (two halves):**
- **Outbound:** the 9 carried commits are delivery-integrity fixes upstream lacks (ledger evidence row,
  bot-loop guard, mode propagation across prepare→send, 403-final, sender identity). Sending them upstream
  moves our drift from *"we re-apply a patch drill every update"* to *"we pull main"*.
- **Inbound:** our governance plugins (`mode_first_gate`, `lane_switch`, `hermes-snapcompact`,
  `web-aaa-state`, `well_3baik_capture`, `well_human9_route`) + 5 gateway hooks are not fork patches —
  they are a **profile distribution**. Upstream ships exactly that primitive. Packaging them means any
  future AAA agent inherits the constitution instead of rebuilding it (LAW 8: one problem, one owner).
**Evidence:** 695 insertions / 14 files, 0 behind; 6 plugins + 5 hooks deployed locally.
**Yield:** a fork that carries nothing is a fork that cannot rot. Drift becomes `git pull`.
**Cost:** PR + one distribution manifest. **Reversal:** the fork stays authoritative until merged.

### Q6 — CONTEXT CONTRACT SEAL (do this first — it is the only one that can be *wrong silently*)
**Mechanism:** read the three numbers and take the minimum.
```
harness  model.context_length              = 1,000,000   (declared)
proxy    request-size clamp constant        = read the middleware source
upstream real window (provider /v1/models)  = read the local registry cache
truth    = min(all three)  → write THAT into config
```
If the harness believes a window larger than the clamp, its compressor never fires and the proxy truncates
without a log line. Fix by lowering the declared window to the binding floor: **compression you can read
beats truncation you cannot.**
**Cost:** one probe + one config edit. **Reversal:** trivial.

---

## 5. HARDENING QUEUE

### P0 — reversible, do now (no F13 gate)
1. **Reconcile the context window** → Q6. Highest severity because it is silent.
2. **Fix memory-provider drift:** the update path warns *"Memory provider 'local' is configured but not
   installed"* while config says `provider: mem0` (and mem0 is live — 455 calls). Two readers, two answers.
3. **Park the cold tool tail** → Q4 (start with the 8 servers ≤5 lifetime calls + `doc-tables`).
4. **Cron triage:** 11 disabled jobs out of 18. Disabled-but-resident is inventory, not capability —
   delete or resurrect, never linger. 13.4% failure rate worth a read.
5. **Disk:** `state.db` 1.16 GB on an 80%-full disk. Run upstream's own maintenance
   (`hermes sessions optimize-storage` / `prune` / `archive`) — check before building anything custom.
6. **Decide the install-tree sediment:** 294 SKILL.md in `/usr/local/lib/hermes-agent/skills` are
   unreachable by design (loader reads `SKILLS_DIR` + `external_dirs` only). Either wire it or stop
   counting it — right now every "duplicate" comparison is contaminated by it.
7. **Verify curator × external_dirs:** one probe — does `hermes curator adopt --all-unmanaged` reach
   `/root/AAA/skills`, or only `~/.hermes/skills`? Everything in Q1 depends on this answer.

### P1 — this week
8. **Index diet** → Q1, in waves (archive the 448 never-loaded; keep the 258 hot; re-measure `hermes prompt-size`).
9. **Name-drift lint + rename wave** → Q2.
10. **Governance middleware pilot** → Q3, one rule.
11. **Re-measure everything** (an audit without a second reading has no proof the fix landed).

### P2 — roadmap
12. **Package the governance layer as a profile distribution** → Q5 inbound, so AAA agents inherit.
13. **Upstream the 9 carries** → Q5 outbound; then switch the update drill to a plain pull.
14. **Federation-side parity:** the same estate laws (owner · retention · writer · last_reviewed) applied
    to the 40 AAA agent cards and 43 running services — 11 of the agent cards are `_archive`/`_external`
    duplicates of live identities.

---

## 6. F13 BINARIES ONLY (everything else above is mine to execute)

- **B1 — One estate or two?** Move the AAA skill corpus under `~/.hermes/skills` so upstream's curator
  owns it, **or** keep two sovereign roots and give `/root/AAA/skills` its own 60-line transition script
  driven by the same `.usage.json` sensor. (Owner: Arif. Irreversible-ish: it changes who may archive.)
- **B2 — Archive the 448 never-loaded skills now, or keep the whole catalogue hot?** Reversible, but it
  is the one change that visibly shrinks what every agent can see without searching.
- **B3 — Push the 9 carried commits upstream** (public) **or** keep them sovereign-only?

---

## 7. WHAT UPSTREAM HAS THAT WE DO NOT LEVERAGE (and should)

| Upstream feature | Local status | Why it matters here |
|---|---|---|
| Curator auto-transitions + usage telemetry | installed, unwired | the direct fix for F1/F2 |
| `skills opt-out` / `.no-bundled-skills` marker | marker absent; seeding ON | stops 294 unreachable copies accumulating |
| `/learn` knowledge-base skills (refs on demand) | already adopted — 247 AAA skills carry `references/` | keep doing this; it is the correct shape |
| Plugin middleware (LLM + tool calls) | unused | the native surface for D9/Q3 |
| `tool_search` tier config (`defer`, `threshold_pct`, `listing_max_tokens`) | all defaults, un-owned | governs how 352 schemas disclose |
| Profile distributions | unused | ship the constitution to AAA agents (Q5) |
| Micro-compaction | off (default) | legitimately off — the cache-prefix cost is real and declared |
| Managed scope (admin-pinned config) | unused | an un-overridable policy layer for AAA seats |
| Checkpoints & rollback, LSP diagnostics | keys absent | un-owned; verify before claiming either way |

---

## 8. ONE-LINE LEDGER

> 706 skills indexed, 448 never opened, 24,980 tokens a turn for a catalogue two-thirds dead;
> 27 tool servers for 1.64% of calls; a curator running green against 2 of 706;
> a 1,000,000-token window declared and never reconciled; and 9 commits of delivery integrity
> we are ahead on and have not sent back.

*DITEMPA BUKAN DIBERI — but a machine that buys attention with a dead catalogue is not forging, it is paying rent.*
