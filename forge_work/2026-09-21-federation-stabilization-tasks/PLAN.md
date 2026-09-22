# FEDERATION STABILIZATION — REMAINING TASKS

> **Forged:** 2026-09-21 · FI-008 (Kimi Code)
> **Trigger:** F13 directive "compile all remaining task and execute agentically"
> **Authority:** session = OBSERVE_ONLY (no SCT); F13 verbal authorization for T0/T1.5/T2; T3 surfaced as binaries
> **Doctrine:** AGENTS-AUTONOMY.md action tiers · State-Transition Discipline · anti-collapse (F13 2026-09-14)

---

## STATE — multiplier map (honest, no false green)

```
Capability          HIGH       (208 federation tools, MCP 2026-07-28 wire)
Reality Coherence   IN PROGRESS (G0c delivered today; G1/G2 pending)
Authority Integrity PARTIAL    (Capability ≠ Authority doctrine; ACT/lease/seal mid-build)
Temporal Learning   LOW        (CHRON witness, not governor; 0.01% verify→learn)
```

G0c (`/etc/arifos/canon/federation-release.json`) — **DELIVERED this session**.
Receipt: `/root/VAULT999/RECEIPTS/2026-09-21-federation-runtime-id-mint-receipt.md`.

---

## A. AUTO-DO (T0 / T1 / T1.5) — execute now, no narration needed

### A1 — Compile remaining tasks as PLAN.md
**Status:** in progress (this file)
**Path:** `/root/AAA/forge_work/2026-09-21-federation-stabilization-tasks/PLAN.md`

### A2 — Reap zombies
**Why:** 3 defunct processes (`rm` PID 866826, 2× `node-MainThread` PIDs 867498, 867588).
**Tier:** T0 (process hygiene)
**Risk:** none — they are already <defunct>; parent reaping releases the PID.
**Action:** `kill -SIGCHLD 1` (parent PID 1 reaps) OR `kill -9 <pids>` directly.
**Verification:** `ps aux | awk '$8 ~ /Z/' | wc -l` → 0

### A3 — Investigate swap churn
**Why:** swap 7.3/8.0 = 91.25% used while 14Gi RAM available — paging for unclear reason.
**Tier:** T0 (observation)
**Action:** sample `vmstat 1 10` × 3 windows; correlate with cron / planning subagent activity.
**Output:** `/root/AAA/forge_work/2026-09-21-federation-stabilization-tasks/swap-investigation.md`

### A4 — surface.json schema template
**Why:** G1 (Registry Truth) needs one canonical schema per organ.
**Tier:** T1 (doc-only)
**Path:** `/etc/arifos/federation/surface-schema.json`
**Schema fields:** `canonical` · `compat` · `private` · `deprecated` · `metadata { last_verified, last_verifier, contract_drift_status }`
**Per-tool contract:** `name`, `signature`, `aliases`, `deprecation_since`, `remove_after`, `reachability_check`

### A5 — CHRON schema observation
**Why:** `function` field ≠ `step_type` (200 sample showed 100% `?`). CHRON lifecycle closed loop requires a stable discriminator.
**Tier:** T0 (observation; the fix is T2).
**Output:** distribution table + 1-paragraph migration proposal (NOT YET a migration).
**Path:** `/root/AAA/forge_work/2026-09-21-federation-stabilization-tasks/chron-shape.md`

### A6 — Draft per-organ surface.json contracts (DRAFTS only)
**Why:** G1 needs `S_declared = S_exported = S_callable = S_observed`. Drafts are not yet wired into organs.
**Tier:** T1 (draft docs)
**Paths:**
- `/root/AAA/forge_work/2026-09-21-federation-stabilization-tasks/draft-arifos-surface.json`
- `…/draft-aforge-surface.json` (131 live registry, 127 affordances, 4 missing declarations per session prior)
- `…/draft-geox-surface.json` (25 canonical)
- `…/draft-wealth-surface.json` (14 tools)
- `…/draft-well-surface.json` (intended=10, registered=40, callable=10, exported=19 — classify)
**Note:** DRAFTS are advisory; promote to canonical only after each organ's team ratifies.

### A7 — A-FORGE /health gap report
**Why:** A-FORGE /health lacks `build_commit`, `surface_hash`, `runtime_path`. Need a one-page gap list to send to the A-FORGE lane.
**Tier:** T1 (audit doc)
**Output:** `/root/AAA/forge_work/2026-09-21-federation-stabilization-tasks/aforge-health-gap.md`

---

## B. ANNOUNCE-THEN-EXECUTE (T2) — 10s veto window per AGENTS-AUTONOMY.md §3

### B1 — Atomic-write draft surface.json to staging
**Why:** drafts are reversible (just delete the file) but write to canonical-style path under /etc/arifos/federation/.
**Action:** write drafts as `*.draft.json` (suffix marks them as not-yet-canonical).
**Risk:** low — naming convention prevents accidental promotion.

### B2 — Zombie reap
**Why:** 3 defunct processes. While A2 marks it T0 (reap), terminating the parent reaper or sending signals to specific PIDs is T2 (operational consequence).
**Action:** `kill -SIGCHLD 1` and if needed `kill -9 <pids>`.
**Risk:** minimal — defunct processes cannot run; reap only releases PID.

### B3 — CHRON schema migration (function → step_type)
**Why:** observation shows CHRON episodes field is `function`, not `step_type` as expected by the canonical lifecycle. This blocks G9 verify→learn closure analysis.
**Action:** write a CHRON migration script that renames the field on /root/chron/data/episodes.jsonl, with backup.
**Risk:** medium — touches CHRON's primary data file. Backup is mandatory. Reversible via restore from backup.
**Backup path:** `/root/chron/data/.backup-episodes-<timestamp>.jsonl`

---

## C. SURFACE AS F13 BINARY (T3) — stop, ask, wait

### C1 — Re-mint arifOS SCT to enable arif_seal ratification
**Why:** current session is OBSERVE_ONLY; L11 SCT mismatch was observed. Without an SCT, G0c manifest is agent-witnessed (Lane B), not kernel-sealed.
**Binary ask:** "Mint a fresh SCT for this session so arif_seal can ratify today's G0c manifest?" (Yes / No)

### C2 — Capture arifOS 95-file dirty state on topic branch
**Why:** per AGENTS-AUTONOMY.md §4, dirty state should never be discarded. The 95 dirty files in `/opt/arifos/current` represent pending work that needs topic-branch capture + PR.
**Binary ask:** "Create topic branch `chore/2026-09-21-arifos-dirty-capture` on /opt/arifos/current and push to ariffazil/arifOS as a PR?" (Yes / No)
**Note:** this is admin merge territory given billing-locked CI; --admin auto-merge would be required.

### C3 — Restart A-FORGE service to refresh /health surface
**Why:** A-FORGE /health returns minimal fields. A-FORGE runtime_verify strict returns UNKNOWN on source_vs_wheel / source_vs_import. Need a fresh process to load updated module that exposes build_commit/surface_hash/runtime_path.
**Binary ask:** "Restart `a-forge.service` (known-safe per AGENTS-AUTONOMY.md §7) so /health exposes the full identity tuple?" (Yes / No)

### C4 — Wire canonical surface.json into each organ's /health response
**Why:** G1's invariant `S_declared = S_exported = S_callable = S_observed` requires the surface.json schema to be enforced by each organ at /health emission time. Cross-organ mutation.
**Binary ask:** "Merge the draft surface.json into each organ's /health code path, one organ at a time, behind feature flags?" (Yes / No)

### C5 — Deploy federation identity verifier as a systemd service
**Why:** G0c manifest needs continuous verification (every restart, every deploy). Currently the manifest is a passive file. The verifier should be a service that re-probes all 5 organs on schedule and compares against the expected vector.
**Binary ask:** "Mint `/root/forge_work/federation-verifier.service` as a systemd timer that probes the 5 organs hourly and writes receipts on drift?" (Yes / No)

---

## D. DEFERRED — not in this session scope

- CHRON closed-loop learning (G9 beyond observer role) — needs many verified outcomes first
- arif_seal ratification of constitutional seals beyond what the kernel permits
- Cross-organ MUTATE federation activation (gated on all of G0–G8 being green)

---

## Execution plan

1. Execute A1–A7 in parallel now (this turn)
2. Announce B1–B3 with 10s veto window
3. Surface C1–C5 as F13 binaries
4. Write final session receipt to /root/VAULT999/RECEIPTS/2026-09-21-federation-stabilization-tasks-receipt.md

⚒️ DITEMPA BUKAN DIBERI
