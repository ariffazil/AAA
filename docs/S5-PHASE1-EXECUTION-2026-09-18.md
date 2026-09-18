<!-- SOT: execution record. Tier: S5 PHASE 1 EXECUTED under F13 greenlight 2026-09-18 — one item BLOCKED_AT_GATE. -->
# S5 PHASE 1 — JITU WIRED · GEOX WALL LOADED ON DISK, NOT IN FORCE
> Forged: 2026-09-18 · KVM8 · Hermes ASI session · branch `proposals/orthogonality-v02-hermes-mapping`
> Authority: F13 — *"Kolaps 3 implementasi jadi SATU butang kuasa mutlak. Wayarkan terus ke urat saraf
> enforcement semua lane automatik… wayarkan K-DIP, K-SCALE, K-TAPER ke actuation paths organ GeoX."*

> **Disclosure, first line, because it is itself a finding.** The literal command line that this document
> needs to quote — the unit-restart of `geox-mcp.service` — is the exact string the K-02 gate blocks on.
> A first attempt to write this file was refused. The operation is therefore identified **by receipt**:
> the exact blocked text is preserved verbatim in the gate receipt trail
> (`~/.local/share/arifos/hermes_hook_receipts.jsonl`, event `hermes-gate.blocked`).
> I am not rephrasing to get around the gate; I am naming the block as part of the record. The gate cannot
> distinguish "a document that mentions an operation" from "the operation", which is the same
> content-shape-stands-in-for-a-capability-judge defect F13 named earlier tonight.

---

## 1. JITU — one brake, wired into the nerve (DONE)

**The single authority:** `/root/AAA/federation/kernel/jitu.py`
Nothing else implements a brake. It carries the authority tuple and an append-only event trail.

```
trip.json  { tripped_at, by, scope[], reason, until, trace_id }
events     /root/.local/share/arifos/jitu/jitu_events.jsonl   (trip · release · check_denied · refusals)
```

| Property | How it is enforced |
|---|---|
| Only F13 trips or releases | `--by` must be a sovereign identity; any other actor is REFUSED and the refusal is receipted |
| Hard interrupt | `check` exits **3** (distinct from the gate's T3 exit 2) — `&&` chains stop |
| Fail-closed | unreadable or corrupt state = TRIPPED, not "probably fine" |
| Scope | `all` or a named lane list; an unlabelled caller is treated as in-scope |
| Deadline | `--until` ISO8601; an unparseable deadline never auto-expires |
| Receipt | trip, release and every denial are appended with a trace_id |

**Self-test proves it stops things — 8/8:**
```
PASS idle -> allowed · PASS non-sovereign trip refused · PASS tripped -> denied
PASS scoped trip spares out-of-scope lane · PASS expired trip -> allowed
PASS non-sovereign release refused · PASS sovereign release -> idle
PASS corrupt state -> fail-closed denied
```
It runs against a scratch directory, so the live brake state is never touched by its own test.

### 1a. Wired into the tool path
`/root/AAA/federation/protocols/arifos-hermes-gate-hook.py` — JITU is now decision step **0**, ahead of
W_scar and ahead of the T3 patterns. Verified by running the real hook with real payloads:

| Test | Result |
|---|---|
| brake idle, T2 mutation | allowed, witness receipt written |
| **brake tripped, same T2 mutation** | **blocked, exit 3, reason = JITU, receipt `hermes-gate.jitu_tripped`** |
| brake tripped, `read_file` | still allowed — a brake that blinds the operator cannot be released safely |
| released, mutation again | allowed |

### 1b. Wired into every automated lane — 47 cron entries
Each active line became `jitu-guard <lane> && <original command>`, using the absolute path
(`/root/.local/bin/jitu-guard`) because cron's PATH does not include `/root/.local/bin`.

Verified in a **cron-like environment** (`env -i PATH=/usr/bin:/bin SHELL=/bin/sh`):
```
brake idle    -> LANE WOULD RUN
brake tripped -> HARD INTERRUPT, LANE STOPPED (correct)
released      -> LANE RUNS AGAIN
```
`jitu-guard` fails closed if the authority file is missing or returns an unexpected status.

### 1c. The three implementations collapsed
```
core/paradox/circuit_breakers.py   LIVE DETECTOR — designated, not retired
    It REPORTS (CB1-CB5 return states); it does not stop anything. Consumed by core/judgment.py
    and arifosmcp/tools/paradox.py (11 tests pass). The designation header records the asymmetry:
    DETECTION may be automated, STOPPING is sovereign. Two things named "circuit breaker" that
    can both stop work is not redundancy — it is a shared blind spot.
scripts/governance/circuit-breaker.sh    RETIRED (0 cron, 0 systemd, 0 live callers)
arifOS/scripts/wire/arif-circuit-breaker RETIRED (same)
    Copies kept at backups/skill-collapse-20260918/jitu-collapse/ with RETIRED.md.
    Restoring the file does NOT restore the brake — the wiring never existed.
```

---

## 2. GEOX physical wall — the gates fired, the door still opened (FOUND, FIXED ON DISK)

### The defect
The gates are live code (`structure_gates/`, 12 modules) and they DO kill:
a normal-fault regime with an 8° dip and a constant throw profile →
`kills: ['K-THROW', 'K-DL']`, `hypothesis_status: REJECTED`.

But the **propose path did not carry the verdict**:

```
mode="interpret"  (the proposer an agent actually calls)   BEFORE
  combined_gate_verdict : "KILL"
  gate_summary          : {"pass":1,"warn":1,"kill":2,"unmeasured":5}
  local_verdict         : "QUALIFIED_CANDIDATE"     <-- a KILLed structure, labelled a candidate
  governance_status     : None
  rendered PNG title    : "... · HYP-001 · QUALIFIED_CANDIDATE"
  ok                    : true
```
Two hardcoded strings were overwriting the physics: `compact_interpret_envelope(verdict="QUALIFIED_CANDIDATE")`
and `_stamp_qualified()` setting `local_verdict = "QUALIFIED_CANDIDATE"` unconditionally.
**A wall that does not change the output is a wall beside the road.**

### The fix (4 edits, source + live tree)
```
seismic_interpret.py  _stamp_qualified()      — refuses to relabel a falsified result
seismic_interpret.py  interpret branch        — derives gov_status / local_verdict / render title from sv
seismic_interpret.py  both payload shapes     — carry combined_gate_verdict, kills, governance_status
section_render.py     compact_interpret_envelope() — accepts the real verdict instead of hardcoding
```
Also corrected the naming: **K-TAPER = K-THROW** (throw tapers to elliptical tip-line, Barnett 1987) and
**K-SCALE = K-DL** (D/L 10⁻³–10⁻¹; Earth bulk 0.005–0.05). Both were live all along.

**Verified in-process, both directions:**
```
IMPOSSIBLE (normal regime, dip 8°, constant throw)
   combined_gate_verdict: KILL | governance_status: HOLD | local_verdict: FALSIFIED
   kills: ['K-THROW','K-DL'] | gate_summary: pass 1, kill 2
PLAUSIBLE (normal regime, dip 60°, tapered throw)
   combined_gate_verdict: PARTIAL | governance_status: QUALIFY | local_verdict: QUALIFIED_CANDIDATE
   kills: [] | gate_summary: pass 4, kill 0
```
The gates discriminate; it is not a blanket refusal.

### Deploy status — honest, and this is the part that matters
* `/root/GEOX/src/...` — fixed (source of truth).
* `/opt/geox/src/...` — **the same 4 edits applied to the LIVE tree**, originals backed up
  (`backups/.../geox-deploy/*.pre-jitu`), both files compile, import verified against the live tree.
* **`/opt/geox` is 38 commits behind `origin/main`** (at `8c6c7f2d`, 2026-09-09) and carries its own local
  modifications. Promoting the whole tree is a different, much larger change and not this session's mandate —
  so only the two files were touched.
* **The running process still holds the pre-fix module.** A live MCP call right now still returns
  `local_verdict: QUALIFIED_CANDIDATE`. The wall is correct on disk and **not in force**.

**BLOCKED_AT_GATE.** The service-restart that would activate the fix was refused by the K-02 T3 gate
(pattern `systemctl\s+(restart|stop|disable)`). It was refused again when I packaged the mutation for
`arif_judge` — because the *description* of the operation contains the same string — so the gate blocks the
request for authorization together with the action. Reported as the gate instructs: state + exact blocked
operation, not retried, not routed around.

> **A related finding, recorded because it is the same defect twice.** The gate classifies
> `execute_code` as a T2 mutation and **witnessed** the `/opt/geox` file writes (this window: 40×
> execute_code, 12× patch, 7× write_file receipts). That is the gate working as designed — but it means a
> file-level deploy into a live runtime passes as T2 while the restart that activates it is T3. The gate's
> model of "the mutation" is the restart, not the write. Which one carries the consequence is an F13 ruling.

---

## 3. What F13 asked for, item by item

| Directive | State |
|---|---|
| Collapse 3 implementations into ONE absolute power button | **DONE** — one authority, 2 retired, 1 designated detector |
| Wire into the enforcement nerve of all automated lanes | **DONE** — gate hook (step 0) + 47 cron lanes, both verified |
| JITU = hard interrupt + clear receipt | **DONE** — exit 3, `jitu_tripped` receipt, fail-closed |
| Wire K-DIP / K-SCALE(K-DL) / K-TAPER(K-THROW) into GEOX actuation | **FIXED ON DISK · NOT IN FORCE** — restart BLOCKED_AT_GATE |

## 4. Reversal
```
/root/AAA/backups/skill-collapse-20260918/
  jitu-collapse/      retired implementations + RETIRED.md
  geox-deploy/        the two pre-patch /opt/geox files
  crontab-root.bak-20260918 · crontab-pre-jitu.txt
  cron-guard-record.json · retire-record.json
/root/AAA/federation/protocols/arifos-hermes-gate-hook.py.bak-20260918-pre-jitu
```

---

*Detection may be automated. Stopping is sovereign. A wall beside the road is scenery.
DITEMPA BUKAN DIBERI ⚒️*
