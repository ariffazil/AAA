# F2 CORRECTION #6 — round two: the recorded decisions executed, three bodies promoted, two held

**Date:** 2026-09-16T03:35Z · **Actor:** HERMES · **Session:** `20260916_103651_63c575`
**Consequence class (C18):** more store convergence + overlay promotion, all reversible
(quarantine + git + accumulating manifest). **No kernel floor, FLOOR_TABLE, or arifOS surface touched.**

---

## 1. WHAT "GO" UNLOCKED — EVIDENCE, NOT JUDGEMENT

Round 1 held five pairs because *"name = routing = agent behaviour"*. The correct next move was not
to ask: it was to check whether **the federation had already written the decision down.** Two had.

```
SYMLINK  FORGE-act-federation-ingress → forge-act-federation-ingress
  reason: SKILL_ALIAS_TABLE.json entry `dev-sct-ingress-deprecated` carries tombstone:true and
          related[FORGE-sct-federation-ingress].note = "LEGACY — renamed SCT→ACT".
          The tombstone maps the loser's routing name exactly onto the survivor's.
          A tombstone is the registry saying the old name is retired → executing a record.

SYMLINK  KERNEL-trinity-33 → kernel-trinity-33
  reason: alias entry v3_name KERNEL-trinity-33, renamed_from trinity-33-canonical.
```

`FORGE-artifact-publisher → forge-artifact-publisher` (round 1) was the case/spelling variant; the
surviving spelling equals the recorded `v3_name`.

**Still HELD, and now with a sharper reason:**
- `RSI-federation-mesh` vs `rsi-federation-mesh` — two live routing names, and **no registry record
  anywhere** (alias table, V3 registry, genealogy, manifest all silent). Nothing to execute.
- `forge-onboarding` vs `forge-onboarding/agent-onboarding` — not a duplicate at all: 35 lines and
  6 files exist only in the loser. That is a merge, and the alias table's `primary_disk_name` for
  it (`agent-onboarding`) matches *neither* body's routing name, so the registry cannot arbitrate.

## 2. THE OVERLAY INVERSION — REAL THIS TIME, AND I HAD IT BACKWARDS ON TRINITY

Round 1 I wrongly claimed canon was "behind the harness" for trinity. It was not. For the opencode
overlay it **is** true, and it is measured:

```
/root/.config/opencode/skills  — 9 real dirs (not symlinks) + 22 symlinks onto canon/organ trees

of the 9 real dirs:
  5 are upstream-bundled  (.bundled_manifest) → belong to `hermes update` → NOT TOUCHED
      FORGE-mcp-probe · institutional-epistemic-sink-forensics · opencode-forge · opencode-init
      · opencode-propose-seal
  3 are federation-authored with NO canon body anywhere:
      opencode-meta-mesa · opencode-zen-router · opencode-agentic-state
  1 was a stale duplicate of a canon skill:
      FORGE-mcp-testing (d6754c26, 08-09) → replaced by a symlink to canon 53dd7c0f (09-15)
```

The three were **promoted**, and the placement was derived rather than chosen: the corpus already
keeps the same stem under other harness prefixes at canon root — `claude-meta-mesa` + `qwen-meta-mesa`,
`claude-zen-router` + `qwen-zen-router` + `COPILOT-zen-router`, `claude-agentic-state` +
`qwen-agentic-state` + `kimi-agentic-state`. Two or more canonical siblings ⇒ the canon-root home
with this harness's prefix is the established shape, not a naming decision.

## 3. VERIFICATION

```
canon find -L      507 → 510   (+3 promoted, nothing removed)
canon plain find   457 → 459
overlay real dirs    9 → 5
loader (Hermes)    409 → 409   (.hermes scans itself; canon is not in its table)
sweep             fail=0 · warn=4 → 2
   C15 canonical_id_duplicate   6 → 2
   C17 canonical_route_duplicate 4 → 0
   C16 canonical_case_twin      5 → 1
```

Remaining WARNs are exactly the two real decisions (§1). Quarantine holds every original body;
`store-converge-manifest.json` holds the reverse operation for all 7 entries; AAA commit `1e3f2017b`,
scripts commit `481bb8b`.

## 4. THREE BUGS THE DRY RUNS CAUGHT (none shipped)

1. basename-keyed grouping merged `apex_verdict_hold/hermes` with `apex_verdict_seal/hermes` — two
   different skills whose *variant* subdirs share a name. Would have replaced one skill's body with a
   link to another's.
2. `shutil.copy2` on a **directory** (files-only API) made all three promotions fail with `Errno 21`
   — caught because the run reported `symlinked=1` when the plan said 4. Fixed to `copytree`.
3. the manifest was rewritten each run, erasing the previous run's reverse operations. It now
   accumulates.

## 5. STILL OPEN — NOT MINE TO CLOSE

1. **`RSI-federation-mesh`** — one routing name must win. No registry record exists to execute.
2. **`forge-onboarding` / `agent-onboarding`** — a merge (35 lines + 6 files), with the registry's
   recorded name matching neither body.
3. **Hermes's own routing table** is `.hermes`-only, so canon's convergence is invisible to it. Its
   trinity entry still reads `trinity-33-canonical`; whether Hermes should scan canon at all is a
   routing decision, not a cleanup.
4. **Four eureka ledgers, four schemas** (canon 104 · eurekas 3 · .local/arifos 6 · atlas333 1).
   Consolidation touches canon, so it is F13-class and NOT executed here.

DITEMPA BUKAN DIBERI ⚒️
