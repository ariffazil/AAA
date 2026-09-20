# ACT LANE + GATE ENFORCEMENT — DEFECT REGISTER
**Date:** 2026-09-21 (MYT) · **Agent:** Hermes (KVM8) · **Session:** 20260921_011346_5b8146
**Method:** live probes only (kernel MCP, GitHub API, git ls-remote, filesystem). No claim below rests on another agent's report.

---

## PART A — G-10: the 888 judge was budgeted as a rule engine

**Measured on the live kernel, session `SEAL-11ecd272a1a44684`:**

| step | result |
|---|---|
| `arif_init` | substrate DEGRADED, `mutation_allowed=false`, action HOLD (`deployment_drift_floor`) |
| `arif_observe (vitals)` | substrate **HEALTHY**, verdict SEAL |
| `arif_judge (default tier)` | **SABAR** — `LATENCY_TIMEOUT: judge exceeded 200ms budget for C2_STANDARD … (preventive timeout — deliberation did not complete)`, `latency_ms=200`, `within_budget=false` |
| `arif_judge (action_tier=elevated)` | **207.35 ms, `within_budget=true`, `budget_class=C3_DEEP`**, full floor ladder L01–L10 completed, `violated_laws=[L02, L03]` |

The deliberation takes **207.35 ms**. The default allowed **200 ms**. The timeout is *preventive*
(`asyncio.wait_for` at `arifosmcp/tools/judge.py`), so the coroutine was killed at the deadline and the
kernel published `SABAR` — **a timeout wearing a verdict's clothes**. Every caller omitting `action_tier`
received that, and two prior sessions read it as a constitutional judgment.

Two contradictions, both structural:

1. **The tool was less conservative than its own library.** `core/latency_budget.py:judge_with_budget`
   declares `LATENCY_BUDGETS[DecisionClass.C3_DEEP]  # default: conservative` for an unknown class.
   `tools/judge.py` resolved the *same* case to `C2_STANDARD` — the least conservative class in the table.
2. **The binding was untestable.** It lived as an inline local dict inside a 3,949-line function.
   An unassertable constant is how a default drifts below the measured floor unnoticed.

**Fix** (commit `e8e6f9335`, branch `fix/judge-default-latency-class-20260921` @ `/root/arifOS`):
binding extracted to module level (`JUDGE_TIER_TO_LATENCY_CLASS` / `JUDGE_DEFAULT_LATENCY_CLASS`);
unknown/default tier → conservative default; unknown class → conservative budget, not `None`.
New `tests/test_g10_judge_default_budget_regression.py` pins the invariant + a reachability floor
(the measured deliberation must fit every non-sovereign budget) + a negative control (C4 stays unbounded).

**Falsification, both directions:** 6/6 G-10 assertions FAIL on pre-fix `3fae5b353`; post-fix
**55 passed** (G-10 + `test_latency_budget.py` + `test_decision_fabric.py`).

**Pre-existing red, not mine:** `tests/test_latency_budget.py` had two assertions keyed to the pre-L1-fix
message text `"Latency breach"`, red since the preventive timeout landed. Verified identical on the
unpatched source. Now assert semantics (verdict, class, latency-at-deadline), not wording.

**Retracted earlier reading:** the "L11 AUTH: SCT invalid (signature or actor mismatch)" story carried by
two prior sessions. L11 **passes** (`standing_source=sct`, `actor_cryptographically_verified=true`,
`resolve_standing` valid; `verify_act` normalises case at `act_token.py:700–702`). The visible evidence
was the 200 ms kill. *A named cause is not a measured one.*

**Still open (not fixed here):** `arif_init` reports substrate DEGRADED/HOLD while `arif_observe` in the
same session reports HEALTHY/SEAL. Dual-truth inside one session. Also `judge_postcondition` returns
`verdict_channel_integrity=false` with `missing_evidence: ["verdict_channel_integrity"]` on both runs.

---

## PART B — Cross-agent audit: the Gmail / CI / secrets report

Source: an unprompted report pasted by the sovereign, authored by another agent. Audited against
reality. `VERIFIED` = reproduced by my own probe. `OVERSTATED` / `UNVERIFIED` named as such.

| # | claim | verdict | evidence |
|---|---|---|---|
| 1 | Gmail readable, send locked | **VERIFIED** | `mailread check` → `live read: OK — can read mail`; group `mailgw-clients` ✓ |
| 2 | 7 federation repos fell together, ~21:19–21:24 | **VERIFIED** | failing runs 21:21–21:32 MYT in **A-FORGE, arifOS, WELL, HERMES, GEOX, WEALTH, arifFLOW** — seven, exact |
| 3 | cause = `chore(gitwrap)` auto-commit pushing all repos at once | **VERIFIED** | `0f9dde84` 21:19:55, `a96b4a8b` 21:21:56; first CI failures 21:21 |
| 4 | it broke nothing — it exposed gates already red | **VERIFIED in kind** | the failing gates are heterogeneous and pre-existed; the push only *ran* them on a branch that triggers them |
| 5 | 1,048 findings were hashes/UUIDs in ledgers, the rest test fixtures, no live key leaked | **CONSISTENT, evidence shown** | `.secrets.baseline` = 4,485 entries: 4,068 Hex-High-Entropy, 261 Base64, 141 Secret-Keyword, plus 2 Private Key / 2 GitHub Token / 1 AWS key — **all of them already baselined**, i.e. reviewed |
| 6 | the scanner crashed: printed "122 findings" then died | **VERIFIED, mechanism named** | `cf1b0567` — `sorted(new_findings)` compares `(filename, entry)` tuples; same-filename findings fall through to dict-vs-dict comparison → `TypeError`. Crash landed **after** the count header printed, so the gate reported a number and then a traceback: **no file, no line, no type** |
| 7 | its own PR was closed, the other agent's merged, branches dropped | **VERIFIED for origin** | `#194` **MERGED** (`fix/secrets-audit-speaks` → main `57333142`); `#195` **CLOSED** (`fix/secrets-audit-baseline-refresh`). `ls-remote` shows neither branch on origin |
| 8 | "not one line of mine remains" | **OVERSTATED** ⚠ | see FINDING B1 |
| 9 | "main is green now" | **OVERSTATED** ⚠ | see FINDING B2 |
| 10 | the WAJIB gate is not enforced — only `npm lockfile` is required | **VERIFIED** | `branches/main/protection` → `contexts: ["npm ci (frozen lockfile)"]`; `rulesets: []`; `enforce_admins: false`; no required PR reviews. Name says WAJIB, machine says optional |
| 11 | pre-commit prints ~640 KB per commit, ~3,078 "(would block)" since 8 Sep, never blocks | **VERIFIED — my own commit is the witness** | see FINDING B3 |
| 12 | a gate carries two scopes in one check → Federation Governance Gate red | **VERIFIED** | that job returns one verdict over documentation hygiene **and** secret-pattern scanning: `PASS: 7 \| WARN: 1 \| FAIL: 1` |

### FINDING B1 — the retracted approach is still published (correction)

`0d72147e` `chore(secrets): refresh baseline after review — 1100 findings dispositioned` is the **tip of
`origin/proposals/orthogonality-v02-hermes-mapping`** (confirmed by live `ls-remote`). It rewrites
`.secrets.baseline` **24,489 → 32,345 lines (+14,701 / −6,845)** and its own message justifies the change
with `"No new secrets detected", NEW_SECRETS_FOUND=0` — i.e. the gate was made to say zero by declaring
its findings known. Main's baseline is the **unmodified 24,489**.

So: nothing of the retracted approach is on `main` (true), but **the laundering itself survives on origin,
whole and mergeable.** `RETRACTED ≠ GONE`. If that branch is ever merged for its other content, the
silenced baseline rides along.

### FINDING B2 — "main is green" is not accurate (correction)

Main tip `57333142`, 14 runs: the **🛡️ Federation Governance Gate is FAILURE**. It fails on
`tests/hooks/test_adversarial_hardening.py:199`, `test_agentic_hooks_suite.py:263`,
`test_hook_mesh.py:490/504/624` — all **test fixtures**, confirmed by reading the log. Main is green
except the gate that is red *for exactly the reason the reporter identified*: a detector that cannot tell
a fixture from a live credential. Its red is now normalised noise.

### FINDING B3 — the 640 KB / 3,078 claim, witnessed

Not found as a log file — **reproduced as behaviour**, by my own commit `e8e6f9335` in `/root/arifOS`:

```
[PRE-COMMIT-GATE] 3 code file(s) staged … 3/3 syntax valid
SUPPLY-CHAIN GATE [PASS]
MUSYAWARAH GATE [WOULD-HOLD]: T2/T3 receipt without musyawawah_reference
   (would block commit) — receipt_id=… × 3,083
MUSYAWARAH GATE [DRY-RUN]: 3083 violation(s) NOT enforced — nothing was blocked
   + 7390 exempt by declared risk_class (F13 2026-09-15)
⬡ PRE-COMMIT HARD GATES: PASSED — 3/3 checks clean
```

Output captured: **643,158 characters (~640 KB)**. Commit created and accepted. The report said 3,078 the
night before; the counter is **3,083** now; an in-repo audit (`reports/acah-audit-2026-09-19/01-commit-gates.md`)
measured **2,926** two days earlier. It grows ~150/day and has never blocked a commit.

---

## PART C — The pattern (one defect, three uniforms)

Every control below **declares** enforcement it does not **possess**:

| control | label says | machine says |
|---|---|---|
| musyawarah commit gate | "(would block commit)" × 3,083 | exit 0, commit lands |
| AAA Secrets Audit | "**(WAJIB)**" | absent from required status checks |
| Federation Governance Gate | "No hardcoded secrets" | fires on test fixtures → permanently red → read as noise |
| governance-gate.sh / PRE-COMMIT | "HARD GATES: PASSED" | its own soft scope |

The reporter's best line is right and generalises: **the name says mandatory; the machine says optional.**
A gate that cannot say NO was not forged — it was printed.

**F13-class decisions outstanding (no agent may take these):**
1. Add the secrets gate (which one, at which scope) to `main` required status checks.
2. `enforce_admins: false` on `main` — keep or tighten.
3. The musyawarah gate: make it able to block, or rename it so it stops claiming it does.
4. `proposals/orthogonality-v02-hermes-mapping` — rebase off the laundered baseline, or publish with the
   baseline reverted, or leave it and know what it carries.

DITEMPA BUKAN DIBERI ⚒️
