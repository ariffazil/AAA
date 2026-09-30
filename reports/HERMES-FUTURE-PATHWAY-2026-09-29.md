# THE PATHWAY — firm answer, measured, and what was executed
**2026-09-29 · HERMES · second research loop (experiments on live runtime, not reading)**
Artifact of record: `HERMES-UPSTREAM-CONTRAST-2026-09-29.md` (loop 1) · this file is loop 2 and **supersedes its numbers where they disagree**

---

## 0. THE ANSWER

The best pathway for future HERMES, AAA agents and humans is **not** a diet, a prune, or a harder fork.
It is three moves, in this order:

1. **Fix the address layer** — every instrument we own measures something it cannot cleanly name.
2. **Route capability, don't delete it** — one corpus, many declared views per seat.
3. **One inheritance path, one convergence path** — birth new seats with the constitution; send the carries home.

Everything below that pattern was measured, and every cheap win dissolved under measurement. The
surviving levers are structural, and they are all about **the join between instruments, not the size of
the estate.**

---

## 1. CORRECTIONS TO LOOP 1 (own them plainly)

| Loop-1 claim | Measured reality (loop 2) |
|---|---|
| "~20,000 tok/turn reclaimable by archiving the dead class" | **354–1,891 tok/turn.** The safely-archivable class is 13 skills unprotected, 68 including referenced-but-cold. Diet is dead as a lever. |
| "63.5% of the index never loaded" | Misleading. That counted skills with **no telemetry row** as zero. Honest split: 573 of 914 usage rows match a live skill; 337 match nothing; 134 live skills have no row. Unmeasured ≠ unused. |
| "148 skills loaded by names the index does not carry" | Only **27** frontmatter↔directory mismatches exist (4%). The 148 came from the index *format* — the injected index prints `category: skill-name`, which reads as a single name. A presentation defect, cheap to fix. |
| "Context window P0 — silent truncation risk" | The 1,000,000 declaration is **our own `custom_providers` entry**, not the model's. Behind it: HAProxy :4012 → LiteLLM. Sessions sit at ~7% occupancy. Exposure LOW. Downgraded to P1-verify. |
| "25 skills budget / prune to ~150" | 708 skills **is** this federation's real surface (40 agent cards, 43 services, 7 domains, GEOX/WEALTH/WELL/court/apex). Upstream's 3k index budget assumes one agent and ~90 skills. Copying that number would be copying the wrong thing. |

---

## 2. THE LOAD-BEARING DISCOVERY

```
$ hermes curator adopt probe-lifecycle-test
curator: 'probe-lifecycle-test' lives in skills.external_dirs and is read-only to the curator
```

**Upstream's maintenance machine is structurally barred from the sovereign corpus.**
`/root/AAA/skills` is an `external_dirs` root — outside the curator's write envelope, permanently.
Its telemetry still records usage (558 AAA keys in `.usage.json`), so the *sensor* covers the estate
while the *actuator* cannot reach it. That is why `curator status` reads green with zero transitions:
it manages 2 skills (now 10, after tonight's adopt) out of 708.

The same shape recurs across the estate — **sensor present, actuator absent**:
| Artifact class | Sensor | Actuator | Result |
|---|---|---|---|
| skills (AAA root) | `.usage.json` live | curator barred | 0 transitions ever |
| skills (local root) | live | curator live | 8 adopted tonight |
| MCP servers | lifetime calls | none | 8 servers ≤5 calls, 1 never |
| cron jobs | executions.db (778 ok / 120 fail) | none | 11 of 18 dead-but-resident |
| agent cards | 40 cards | none | 11 are `_archive`/`_external` duplicates |
| gate receipts | 47,759 lines | prose only | unauditable at scale |
| usage↔library join | 914 rows | — | **337 unattributable** |

**The catalogue is not the disease. The join is.**

---

## 3. WHAT THE INDEX ACTUALLY IS

```
708 skills · index 99,460 B ≈ 24,865 tok/turn
  /root/AAA/skills   95,762 B ≈ 23,940 tok   (96%)
  /root/.hermes/skills 3,698 B ≈    924 tok   (4%)
composition:  name 15,037 B  |  description 60,277 B  |  path 23,843 B
```
- **96% of every session's index is the AAA corpus.** Every cron run, every subagent, every Telegram
  turn pays 23,940 tokens for the federation's whole skill library.
- Distribution read by seat (measured, 1,303 attributed loads): telegram 293 skills ≈ 7,126 tok ·
  cli 177 ≈ 4,281 · subagent 99 ≈ 2,066 · cron 8 ≈ 249. Edge union = **373 skills ≈ 9,240 tok (37%)**.
- 39% of descriptions exceed upstream's own 60-char house standard. The theoretical reclaim is
  5,446 tok/turn — **but it is not mechanically reachable**: of 8 worst offenders sampled, 6 carry
  information the body does not have (scar IDs, concept names), and auto-shortening the 58 that start
  with a trigger clause produces ellipsis fragments that select *worse* than the full sentence.
  **This is an authoring queue, not a script.**

---

## 4. EXECUTED TONIGHT (all reversible, all verified)

| # | Action | Evidence |
|---|---|---|
| 1 | Probe skill removed | `_probe-lifecycle` gone |
| 2 | **Adopted 8 unmanaged skills** into the curator | `adopted 8/8`; local root now has a live maintenance loop |
| 3 | **Parked 5 cold MCP servers** (chrome-devtools, context7, deepwiki, doc-tables, zai_reader) | 27→22 enabled; config diff = exactly 5 keys; backup `config.yaml.bak-preskill-*`; model/memory/plugins/hooks/telegram invariants all intact |
| 4 | **Wrote the missing law**: `/root/AAA/governance/SKILL-ESTATE.yaml` | owner · retention · writer · curated_by · protection · selection budget · routing · inheritance. Parses. |
| 5 | **Built the instrument**: `/root/scripts/skill-estate.py` | `sense · lint · plan · archive · restore · ledger`. Dry-run by default, snapshot before apply, append-only ledger, never deletes. Proven live. |

Parking was doctrine-safe: exact-token check found **0** MCP-tool references in skill doctrine for 8 of
the 9 candidates (zai_reader: 1, in a GEOX reference file — so it was parked too, and re-enabling is one
config line). Note honestly: parking saved ~0 prompt tokens (the deferred listing is capped at 4,000
tokens). It is a **governance** win — fewer phantom surfaces — claimed as such, not as a token win.

---

## 5. NOT EXECUTED, AND WHY (the reasoning is the deliverable here)

- **Archive the 68 cold skills** → 1,891 tok/turn (7.6%) bought with a real capability-visibility risk,
  on a corpus where 27 top-level dirs were written in the last 24 hours by other agents. The instrument
  exists and is proven; **the first transition should be deliberate, not automatic.**
- **Trim 275 descriptions** → 5,446 tok/turn theoretical, unreachable without authoring 217 triggers.
  Queue it against the agents that own each skill; keep the lint so it cannot regress.
- **Per-seat index scoping** → the lever is real and large (96% of the index is another seat's corpus).
  But upstream has no tier between *indexed+loadable* and *disabled+refused*, so scoping is a genuine
  visibility decision per seat. **Do not build a view mechanism until a seat can name the capability it
  is missing.** Routing is a doctrine, not a config flag.

---

## 6. THE PATHWAY, IN FULL

### P1 — Fix the address layer (highest leverage, cheapest)
Every instrument must agree on one name per artifact. Tonight's instrument reports the drift:
337 unattributable usage rows · 134 skills with no row · 27 name mismatches · 1 duplicate across roots ·
914 usage keys for 708 skills.
**Move:** canonical name = directory basename = frontmatter `name:`; lint it in `skill-estate.py lint`;
make the injected index print the loadable name unambiguously (kill the `category: name` collision).
**Consequence:** the curator can adopt/consolidate, the sensor can decide, the ledger can be read.
Cost: a lint + one rename wave. Reversal: git.

### P2 — Capability routing (the real "lower distraction" lever)
One sovereign corpus · many declared views. The edge seat reads 373 of 708 skills; the forge seat reads a
different slice; the court seat another. Nothing is deleted; each seat's index is its own surface.
**The honest prerequisite:** name the capability each seat would lose first. Until then, routing stays a
declaration, not a mechanism.

### P3 — The selection surface is a trigger, never a spec
A description states *when to load me*. Procedure belongs in the body, which costs nothing until loaded.
Lint the 60-char budget; alert on **index tokens per used capability**, never on an absolute number.

### P4 — Inheritance: ship the constitution, don't rebuild it
Six plugins + five gateway hooks + 708-skill corpus + SOUL + cron jobs + MCP wiring **are already a
product.** Upstream's profile distribution (`hermes profile install <repo>`) ships exactly that —
SOUL, config, skills, cron, mcp.json — and never ships memories, sessions or credentials.
**This is how future AAA agents stop re-deriving the constitution.** Status: STAGED, not published.

### P5 — Convergence: send the 9 carries home
Delivery-ledger proof (`produced vs sent vs transport receipt`), bot-loop guard, mode propagation across
the prepare→send seam, 403-is-final, sender identity on triggered turns — upstream does not have these.
Merged upstream, our update drill becomes `git pull`. **A fork that carries nothing cannot rot.**

### P6 — The joining discipline (the doctrine that makes the rest self-maintaining)
> An artifact without an owner, a retention rule and a declared writer is sediment, not architecture.
> Nothing is deleted. Cold means moved, sealed, restorable. Sensor beats seniority.

Applied to all seven classes in §2. That is the difference between a system that grows and a system that
accrues.

---

## 7. WHAT REMAINS F13-CLASS (three, and they are all "ship it outward")

1. **P4 publish** — a profile distribution leaves the box.
2. **P5 push** — the 9 carries go to a public repo.
3. **P2 view** — whether any seat's capability visibility is narrowed.

Everything else above is executable by any AAA agent holding `skill-estate.py`.

---

*Loop 1 found the shape. Loop 2 killed four of its numbers and found the joint. The estate is not too
big — it is badly addressed, and its maintenance machine cannot reach it. Fix the join and every
instrument we already own starts working.*
