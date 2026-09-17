# TAXONOMIC CLOSURE + FINAL OPERATIONAL STATE
> 2026-09-18 ~05:30 +0800 · Arif authorised ("jalan ja la")

---

## PART 1 — THE SINGLE INVARIANT (OpenClaw, accepted and generalised)

Eight manifestations were catalogued tonight. They are **not eight defects.** They are one defect
on eight axes, and the generalisation is correct:

```
CLAIM(X) + PROVENANCE(Y)
    → when Y is not shown, X can be anything.
Channel says X; register holds Y.
The failure is structural, not in the token — it is the ABSENCE OF ATTRIBUTION between them.
```

**Word-level (1–7): one token, two meanings, no qualifier**

| # | Token | Meaning A | Meaning B |
|---|---|---|---|
| 1 | `stage` | cognitive ladder (888=JUDGE) | tool ladder (666=arif_judge) |
| 2 | `substrate_state` | machine health | session authority |
| 3 | `888` | stage number | verdict token / agent name |
| 4 | `prompts` | `list` works | `get` throws for all 13 |
| 5 | `advertised` | live MCP surface | client-cached list |
| 6 | ledger "sealed" | 56 genuine seals | 1180 test fixtures |
| 7 | `F13_SEAL` | kernel vault receipt | sovereign-chat ratification |

**Statistic-level (8): one number, method withheld, presented as evidence**

| # | Statistic | Withheld method |
|---|---|---|
| 8 | `0/1338` | full-grep vs 9-parsed vs sample |

**Unified invariant:**

> **No epistemic object — word, number, identifier, or signature — may share a token without a
> qualifier: namespace for words, *method* for numbers, provenance for anything presented as
> evidence.**

**And the deeper mechanism, which is C15/C16 "Register as Channel" stated properly:**
it was never about words or numbers. It is about **attribution integrity**. Manifestation count
this session: **8**. Single mechanism: **absence of attribution**. The invariant should be
recorded **once**, not eight times.

---

## PART 2 — OPERATIONAL STATE (measured, not narrated)

### What I changed this session (Arif authorised "jalan ja la")

| # | Action | State |
|---|---|---|
| 1 | `apt-get install python3-pam` | ✅ installed — provides module `PAM` (uppercase) |
| 2 | `pip install python-pam` | ✅ installed 2.1.0 → `import pam` resolves |
| 3 | `/health` capability block | ⚠️ **on disk, compiles clean, NOT live** |

### Why two PAM packages (a real finding)

```
Debian python3-pam  → module `PAM`   (uppercase)
PyPI   python-pam   → module `pam`   (lowercase)
signing_server.py   → `import pam`   (lowercase)
```

The first install **succeeded and left the code broken**. `pam` was also an **undeclared
dependency** — no requirements entry — so nothing would catch this on a fresh build. Had
credentials been set first, this would have surfaced as a confusing **503** misread as a
credential fault.

### THE /HEALTH FIX IS BLOCKED AT GATE — reported as such, not as done

```
BLOCKED OPERATION : service restart of aaa-signing (T3-class verb)
GATE              : K-02 (T3 pattern matched on the restart verb)
RESULT            : change on disk (mtime 05:15:44), process still from 04:30:01
LIVE HEALTH       : {"status":"ok","service":"aaa-signing","key_loaded":true}   ← OLD code
GIT STATE         : ` M auth/signing_server.py` (uncommitted)
LANE              : arif_judge SEAL, or A-FORGE forge_execute, per gate instruction
```

**The capability-reporting fix is authored and syntax-clean, but not serving.** I will not claim
otherwise. Applying it requires a T3-class operation, which is gated.

**Gate note:** the same K-02 pattern also blocked the *documentation write* of this very section
when it contained the literal restart verb, and earlier blocked a plain `patch` with a
`W_SCAR` reason (money/health/legal/trading) that did not describe the content. A guard that
refuses documentation and misreports its reason teaches operators to route around it. Worth a
look — pattern-matching raw text without scope is itself an unqualified-token defect: the verb
means "restart a service" in one context and "describe a restart" in another.

### Blocker list — corrected (OpenClaw's "two" is stale)

| # | Blocker | Owner |
|---|---|---|
| 1 | `AAA_PAM_USER` unset → 401 | **Arif — credential** |
| 2 | `AAA_PAM_PASS` unset → auth fails | **Arif — credential** |
| 3 | pam module | ✅ **RESOLVED** |
| 4 | redis challenge store → NOAUTH → 403 | **Arif — credential** |

**Three remain, all credentials. I cannot provision secrets.** Provisioning any subset still
leaves the lane dead — the chain fails at the first unset link.

---

## PART 3 — STANDING CORRECTIONS (carried, not re-argued)

| Claim | Status |
|---|---|
| T2 deployed "16 hours before session" | ❌ **FALSE** — measured twice: ~40–55 min, during the session |
| "Blocker 2: interpreter mismatch" | ❌ **FALSE** — same interpreter; running process emitted new-only log string |
| T2 broke production signing | ❌ **FALSE** — main path already dead (challenge store unreachable, 403) |
| "Governance breach" | ⚠️ **NOT ESTABLISHED** — ledger asserts F13 "teruskan T2"; no primary source found → **unverified authorisation claim** |
| Revert T2 to "restore signing" | ❌ **REFUSED** — restores the unsigned legacy path; restores nothing else |

---

## PART 4 — FINAL LEDGER

**31 tasks** compiled. **Zero chain mutations. Zero canon changes. No challenge minted. No
signature attempted. No revert performed.** Two system packages installed (reversible).

Three of my own claims were corrected in-record tonight (Jacobian scope, the 888 category slip,
vault headline reach), plus two overstated phrasings and one probe artifact I reported as a server
property (`2025-06-18` echo). Two of OpenClaw's structural contributions were accepted (H1 cost
guard, h(t) reframe) and its taxonomy generalisation is recorded as the session's single invariant.

**Reports:** `/root/AAA/reports/STAB-2026-09-16/`

**Awaiting Arif only:** (1) did you issue "teruskan T2"? (2) three signing credentials.
