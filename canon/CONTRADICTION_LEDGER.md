# Contradiction Ledger — Living Document

> **Created:** 2026-09-04 | **Source:** APEX ART probe of VPS state
> **Principle:** Max 3 active contradictions at any time
> **Closure Rule:** A contradiction is CLOSED only when a falsifiable receipt proves the gap reduced

---

## Active Contradictions (3 max)

### C-001: Verification > Execution
**Compressed:** Scripts exist but don't run autonomously — verification debt accumulates
**Cost:** HIGH | **Status:** OPEN | **Owner:** A-AUDIT lane

**Evidence:** 30+ audit/verify scripts found on VPS, but only 6 cron jobs scheduled. 80% of verification capability is manual, not automated.

**Pattern:** Discover → build script → never schedule → drift re-accumulates

**Closure Test:** What evidence shows decision cycles shortened? (e.g., audit scripts auto-running, findings auto-resolved without manual trigger)

**Proposed Action:** Convert top 5 audit scripts into scheduled cron jobs with auto-deliver on contradiction found.

**Receipt Required:** Cron execution log showing N audits completed + 0 manual triggers needed

---

### C-002: Doctrine ≠ Runtime
**Compressed:** Declared topology drifts from live state — governance on stale maps
**Cost:** HIGH | **Status:** OPEN | **Owner:** FORGE-spatial-grounding / ASI-drift-watch

**Evidence:** 9 ports declared in AAA_CAPABILITY_REGISTRY.yaml and fleet maps. No continuous reconciliation with `ss -tlnp` live state.

**Pattern:** Docs updated → containers restart/move → drift silent → decisions on stale map

**Closure Test:** What evidence shows drift reduced? (e.g., drift detection auto-corrects or flags within 1 hour of change)

**Proposed Action:** Schedule hourly drift probe: compare declared ports vs live ports.

**Receipt Required:** Drift report showing 0 mismatches over 7 consecutive days

---

### C-003: Capability > Attention
**Compressed:** All 332 skills treated equally alive — no dormancy classification
**Cost:** MEDIUM-HIGH | **Status:** OPEN | **Owner:** Selection lane (888-APEX)

**Evidence:** 332 total skills. 314 modified in 30 days (95%), 27 in 3 days (8%), only 10 stale >90 days. High activity ≠ high value. No dormancy classification exists.

**Pattern:** New skill added → never classified → becomes maintenance debt

**Closure Test:** What evidence shows fewer priorities active? (e.g., skill count classified: <50 Alive, rest Archived/Dormant/Constitutional)

**Proposed Action:** Run dormancy classification on all 332 skills → bucket into Alive/Dormant/Constitutional/Vanity → prune Vanity.

**Receipt Required:** Classification report + Arif ratification of buckets

---

## Selection Function

| Rule | Detail |
|------|--------|
| Max Active | 3 contradictions at any time |
| Promotion | New enters only when one CLOSED or demoted |
| Demotion | Unresolved after 30 days → SCAR (pattern recorded, not tracked) |
| Monthly Scan | Auto-scan 1st of month — probe surfaces, compare against 3, deliver 1-page verdict |

---

## Closed Contradictions

*(empty — none closed yet)*

---

## Scar Archive

*(empty — none scarred yet)*
