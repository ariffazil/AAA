# REMAINING TASKS — Federation Stabilization Session · 2026-09-21

> **Forged:** FI-008 (Kimi Code) · 2026-09-21 ~02:38 MYT
> **Authority scope:** T0/T1/T1.5 auto-do; T2 with 10s veto; T3 = F13 binary

---

## ALREADY DELIVERED THIS SESSION (no further action)

| ID | Task | Artifact |
|---|---|---|
| G0c | Federation identity vector | `/etc/arifos/canon/federation-release.json` |
| A1 | Compile remaining tasks as PLAN | `…/PLAN.md` |
| A4 | surface.json schema | `/etc/arifos/federation/surface-schema.json` |
| A5 | CHRON schema observation | `…/chron-shape.md` |
| A6 | 5 organ surface.json drafts | `…/draft-*.json` |
| A7 | A-FORGE /health gap report | `…/aforge-health-gap.md` |
| B3 | CHRON step_type alias migration | executed · 55,810 records · 63MB backup |
| C2 prep | arifOS dirty capture script | `/root/scripts/capture_arifos_dirty_state.sh` |
| C5 prep | verifier script + systemd unit + timer | script + `/etc/systemd/system/federation-verifier.{service,timer}` |
| C6 prep | zombie reap script | `/root/scripts/reap_zombies.sh` |
| fed-002 | DRAFT (annotated DO_NOT_RATIFY per machine law #6) | `…/fed-002-DRAFT.json` |
| Quiet detector | `/root/scripts/federation_quiet_detector.py` |
| Receipts | 5× VAULT999/RECEIPTS/2026-09-21-*.md + 2× ledger .jsonl |

---

## AUTO-DO BATCH (T0 / T1 / T1.5) — executing now in this turn

| ID | Task | Why auto-do |
|---|---|---|
| **T0-A** | Run verifier × 3 more times to build drift history | Read-only probe |
| **T0-B** | Run quiet detector × 3 to test quiet-detection logic | Read-only probe |
| **T0-C** | Inspect dirty working tree on /opt/arifos/current (read-only) | Observation; capture script will use this |
| **T1-D** | Write 7-machine-laws canon fragment to `/root/AAA/canon/` | Doc-only |
| **T1-E** | Write 13-constitutional-laws (A2A layer) canon fragment | Doc-only |
| **T1-F** | Write A2A constitutional-layer spec — the "missing layer above A2A" | Doc-only |
| **T1-G** | Write session receipt index — single nav for all 2026-09-21-* receipts | Doc-only |
| **T1-H** | Test surface-schema invariants against drafts (declared_eq_exported_eq_callable, compat_lifecycle, unclassified_eq_zero, reachability_zero) | Doc-only validation |

---

## F13 BINARIES (surface as ONE binary each, never a menu)

| # | Task | Why F13 |
|---|---|---|
| **C1** | Mint fresh SCT for this session to enable `arif_seal` ratification | Kernel session authority = F13 only |
| **C2** | Capture arifOS 95-file dirty state on topic branch + push as admin-PR to ariffazil/arifOS | `--admin` merge required (billing-locked CI); cross-repo mutation |
| **C3** | Restart `a-forge.service` after A-FORGE lane ships `/health` surface fix | Service restart = operational mutation |
| **C4** | Merge draft surface.json into each organ's `/health` code path (one organ at a time, feature-flagged) | Cross-organ code mutation |
| **C5** | `systemctl enable --now federation-verifier.timer` to start hourly drift verification | New persistent service activation |
| **C6** | Reap 3 defunct processes (kill parents `docker` 866800 + `litellm` 866924) | High blast radius (federation-wide impact) |
| **C7** | Promote fed-002 DRAFT to canonical | NOW BLOCKED by annotation; requires (a) quiet interval ≥ 1h AND (b) A-FORGE /health gap closed (C3) |

---

## DEFERRED (D-stream, not in scope this session)

- CHRON closed-loop learning (G9) — needs many verified outcomes first; CHRON remains witness
- arif_seal ratification of constitutional seals beyond what the kernel permits
- A2A constitutional-layer implementation (currently spec-only; needs design + F13 review)
- Cross-organ MUTATE federation activation (gated on G0-G8 all green)
- Full machine-law #6 enforcement (currently manual quiet-detection; needs scheduled cron + auto-block-on-drift)

---

## GATING MATRIX (what unblocks what)

```
C7 (promote fed-002)
  ├─ requires ΔS_federation = 0 for ≥ 1 hour   ← T0-B (quiet detector) tracks this
  └─ requires A-FORGE /health gap closed       ← C3 unblocks this

G1 (registry truth) fully closed
  ├─ requires each organ's surface.json ratified   ← C4
  └─ requires A-FORGE /health exposes full identity ← C3

G2 (auth continuity) closed
  └─ requires WEALTH schema/session parity fixed    ← needs C-stream item (not yet enumerated)

G3 (physical stability) fully closed
  └─ requires zombies reaped                       ← C6

G6 (provenance) fully closed
  └─ requires verifier timer active                ← C5

G7 (canary) — only after C5
```

---

## OPERATING CONSTITUTION (carried forward from prior turn)

### 7 Machine Laws

\[
\boxed{
\begin{aligned}
&1.\ \text{Reality} > \text{declaration} \\
&2.\ \text{Observation} \neq \text{authority} \\
&3.\ \text{Source} \neq \text{build} \neq \text{deployed} \neq \text{observed} \;\text{(until proven equal)} \\
&4.\ \text{No mutation without identity + scope + receipt} \\
&5.\ \text{No success without behavioral verification} \\
&6.\ \text{No irreversible action without rollback or sovereign boundary} \\
&7.\ \text{Never destroy evidence to make system look clean}
\end{aligned}
}
\]

### 13 Constitutional Laws (A2A layer above)

```
1.  Identity ≠ Claim
2.  Capability ≠ Authority
3.  Authentication ≠ Trust
4.  Message ≠ Evidence
5.  Consensus ≠ Truth
6.  DelegatedAuthority_{n+1} ⊆ DelegatedAuthority_n
7.  State_{terminal} ¬→ State_{working}
8.  Retry ≠ Replay
9.  Provenance_{out} ⊇ Provenance_{material}
10. Unknown ≠ Invented
11. Time_{evidence} ≠ Time_{now}
12. Agent_Internality ≠ Trust
13. Federation ≠ Sovereignty
```

### Deepest invariant

> Agents may exchange work freely. They may not exchange truth, trust, authority, identity, or sovereignty implicitly.

⚒️ DITEMPA BUKAN DIBERI
