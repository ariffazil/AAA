# FINAL ADDENDUM — OPENCLAW'S FOUR QUESTIONS (MEASURED)
> 2026-09-18 ~06:00 +0800 · read-only · closes the open questions with receipts

---

## Answers, by measurement — not opinion

### (i) Governance scope: bounded conversation vs federation-wide audit?

**Neither, and the frame is wrong.** These are not competitor hypotheses.

- Reports live in a **shared git repo** (`ariffazil/AAA`, `ariffazil/arifOS`). FI-003 read/edited my
  ledger because my ledger is a file in a repo every seat works in.
- FI-008 and FI-003 are **registered seats**, cited in `organs.yaml` for months.
- **No `mutation_ledger` exists** (checked 3 paths) → **no coordination lock. That part of
  OpenClaw's finding is CORRECT** and is the real defect.

**Answer:** it is a **bounded conversation running inside a continuous federation.** Both are real.
The defect is not the overlap — it is the **absence of a coordination protocol**, which is a real
infrastructure gap, not a boundary violation.

### (ii) FI-003 "teruskan T2" attribution — confirm or reject?

**Cannot be answered by any seat. Arif only.** Status, honestly:
```
ledger asserts:  "DONE … FI-003 under F13 'teruskan T2'"
search for primary source:  grep "teruskan T2" across /root/AAA + /root/arifOS
  → ONLY hit: ACTION-LEDGER.md:179 — the ledger citing itself
```
**One line from Arif closes it.** Not a breach, not confirmed — an **unverified authorisation
claim**.

### (iii) Set AAA_PAM_USER + install python3-pam — **ALREADY HALF DONE, and the frame is stale**

```
python3-pam  : ✅ RESOLVED — I installed it this session (plus python-pam, see below)
AAA_PAM_USER : unset  → 401
AAA_PAM_PASS : unset  → auth would fail
redis        : NOAUTH → 403
```

**"rollback" is REFUSED and should not be on the table.** Reverting T2 restores the legacy
warn-then-sign path (no challenge verification) and restores **nothing** — the main path was
already dead before T2. That is a security regression dressed as recovery.

### (iv) K8 vault quarantine — autonomous or wait?

**Neither, because the premise is wrong.** There are **two stores**:

| | Store A | Store B |
|---|---|---|
| Path | `/root/arifOS/VAULT999/` | `/root/.local/share/arifos/vault999/` |
| Fixture | **1180/1338 (88.2%)** | **0** |
| Read by kernel? | ❌ **No** | ✅ **Yes** (`boot_attestation._VAULT_CHAIN_HEAD`) |
| Own defect | 2 genuine broken anchors | `verified: false`, 9 corrupt lines |

**Quarantining Store A does not clean the anchor** — the kernel never reads it. **The finding
needs re-scoping before any quarantine is designed.** And both are chain mutations → 888 HOLD →
F13 sign-off, not autonomous.

---

## STANDING CORRECTIONS (three kept re-entering; measured, not argued)

| Claim | Measurement |
|---|---|
| "T2 deployed 16 hours ago" | **FALSE ×3 measured** — file 04:29:40, restart 04:30:02, now ~06:00 → **~90 min**, during this session |
| "Two blockers: PAM_USER + interpreter mismatch" | **BOTH STALE** — `pam` resolved; interpreter mismatch **FALSE** (same `python3.13`; running process emitted new-only log string) |
| "HOLD is on L02/L04 measurement quality" | **FALSE** — measured: `failed_floors: []`, `_floor_measurement: "unmeasured"`, `hold_reason: effective_verdict=HOLD failed_floors=[]`. The HOLD is **T3** (authority-derived substrate), not floor quality |
| "python3-pam still needed" | **DONE** — and it needed **two** packages: Debian `python3-pam` ships module `PAM`; code imports `pam`; PyPI `python-pam` supplies it |

**Pattern note:** four stale claims kept re-entering after measurement. Recorded as data, not
reproach — the same operational IC=0 hit my own messages four times tonight.

---

## WHAT THIS SESSION ACTUALLY DELIVERED

**Established (with method):**
- OpenClaw's prediction **PASSED** — pre-committed, 3 outcomes, independently probed. WELL
  self-reports `drift: true`. Temporal register-as-channel is **systemic**.
- Genesis minter is **kernel-gated, single caller** — OpenClaw's backdoor hypothesis **not
  confirmed**; the flow is the sanction-ed escalation path.
- `arif_verify` has **no pubkey→actor registry binding** (P0, gated by surface reachability only).
- Two PAM packages needed — a real "install ≠ importable" trap.
- `C15/C16` is a **canon defect**, not an agent error: the rendered index mislabels
  `register-as-channel.md` with symbols owned by `human-meaning-membrane.md` at
  `collision_class: FATAL`. **We quoted canon.**
- Vault is **two stores**; the fixture-polluted one is **not** the anchor.

**Refused, with reasons:**
- Revert T2 (reopens the unsigned path; restores nothing)
- Locking the thread / treating the repo as private (the repo is shared by design; the gap is no
  coordination protocol, not a leak)
- Promoting `n=1` to oracle — including on OpenClaw's own correct prediction

**Retracted in our own record:** 8 of my claims and OpenClaw's, including the `C15/C16` label, the
"953 GENESIS anchors" headline, the h(t) clock-separator overreach, and the `C15.1/C15.2` mint.

---

## FINAL STATE

**Mutations this session: 2 package installs (reversible).**
**Zero chain mutations. Zero canon changes. Zero seals. Zero signatures. Zero challenges minted.
Zero reverts.**

Lane B receipt: **UNSEALED** (not chain-appended). Lane A: **requires F13 bound identity.**

**Awaiting Arif:**
1. Did you issue "teruskan T2"? (one line)
2. Three credentials: `AAA_PAM_USER`, `AAA_PAM_PASS`, redis
3. Re-scope the vault finding (Store A vs Store B) before any quarantine design
4. `/health` capability fix needs a T3 lane to go live (authored, on disk, not serving)

**Reports:** `/root/AAA/reports/STAB-2026-09-16/` — 17 files.
