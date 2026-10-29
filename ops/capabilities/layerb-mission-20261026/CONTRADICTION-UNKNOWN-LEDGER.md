# CONTRADICTION & UNKNOWN LEDGER

Mission `LAYER_B_DISCOVERY_CLOSURE_AND_FED_CALIBRATION` · 2026-10-26 · actor 333-AGI
Every entry states what was observed, what was concluded, and what remains unestablished.
Nothing here is resolved by assertion.

## C1 — baseline assertion `response_schema declarations: 0/258` was FALSE

- **Observed:** compiler v1.0 emitted a hard-coded `response_schema: {state: undeclared, reason:
  "MCP tools/list exposes no outputSchema"}` without ever reading `t["outputSchema"]`.
- **Measured:** 138/258 tools DO declare `outputSchema` — arifos 8/9, geox 26/27, wealth 15/15,
  well 10/10, chron 22/22, claim-ledger 10/10, filings 8/8, media-ingest 4/4, numeric-audit 7/7,
  session-federation 6/6, fed 7/7, hermes 15/15. A-FORGE declares 0/118.
  Of the 138: **32 field-level** (arifos 8, wealth 15, well 7, geox 2) and **106 bare**
  `{type:object, additionalProperties:true}`.
- **Resolution:** compiler v1.1 reads the live field. The frozen baseline value is preserved as
  *recorded*, and corrected here rather than silently overwritten.
- **Class:** measurement-instrument defect (my own), not a runtime defect.

## C2 — I falsely accused WEALTH of over-advertising (retracted, must not be regenerated)

- **Claim made:** "WEALTH publishes 18 against 15 live — advertises tools that no longer answer."
- **Why it was wrong:** a name-only diff against the live MCP tool set, over a `capabilities` list
  that mixes `mcp`, `http` and `webmcp` protocols in one flat array.
- **Measured:** 15 entries `confirmed_live` (MCP) + 3 `confirmed_reachable` (HTTP) = **18/18 valid**.
- **Resolution:** every published claim is now verified **under its own declared protocol**.
  Acceptance gate 8 pins this permanently.

## C3 — I nearly published a false death claim for `observatory_snapshot`

- **First measurement:** verdict `advertised_but_not_live` (absent from arifOS's 9 MCP tools).
- **Contradicting evidence:** its path `/api/observatory/v1/snapshot` answers **HTTP 200**.
- **Resolution:** new class `protocol_mislabel_http_ok` — a labelling defect, **not** a dead
  capability. Acceptance gate 9 forbids any cross-transport death claim.

## C4 — my own patch corrupted 24 unrelated lines

- **Observed:** patching `capabilities.json` via `json.load` → `json.dump(indent=2)` re-escaped
  every non-ASCII character (`—` → `\u2014`, `Ω` → `\u03a9`) across 24 lines, while the intended
  change was one field.
- **Resolution:** `git checkout --` reverted it; redone as a surgical single-field text edit.
  Final diff **+1/−1**. Caught by reading the diff, not by a test.
- **Lesson:** "minimum correction" is a byte-level claim. Always read the diff.

## C5 — organs.yaml is narrower than the running system

- **Observed:** `fed :7074` answers MCP live with 7 tools but declared no MCP surface. `geox`,
  `wealth`, `well` declared `public_mcp` with no `mcp_port` and no `interfaces`.
- **Consequence demonstrated:** the first cut of the compiler selected MCP targets from those
  fields and silently lost 3 organs = **52 of 258 tools**.
- **Resolution:** all four repaired (+16/−0, canonical vocabulary copied from `components[id=arifos]`).
  The compiler now probes **every** declared port and lets the probe classify, so the sweep measures
  SOT completeness instead of trusting it.

## C6 — GEOX tool count disagrees across sources

- **Observed:** organs.yaml `live_probe_2026_09_06.tools = 26`; live handshake 2026-10-26 = **27**;
  `live_probe_2026_07_30.tools = 33` with its own note that live SOT is `:8081/health tools_loaded`.
- **Status:** UNRESOLVED, out of mission scope. The compiler reports the live measurement (27) and
  leaves the historical snapshots untouched. Three numbers for one organ in one file is drift, not
  a contradiction to adjudicate here.

## C7 — the extension schema cannot detect a semantic lie

- **Observed:** negative control `{state: "DECLARED", schema: {type: object}, evidence_ref: null}`
  for all four fields **validates cleanly**. The schema rejects bad enums (`state: "MAYBE"`) and
  `class` supplied alongside `state: "UNKNOWN"`, but cannot detect invented content.
- **Status:** OPEN by design. Structural validation ≠ truth. Only re-probing the runtime catches it,
  which is why `evidence_ref` is mandatory in the envelope.

## C8 — F7 overclaim gate is lexical, not semantic

- **Observed:** `arif_report` was held twice for the words `verified` then `confirmed`, even though
  OBS/DER/INT labels, a confidence band and on-disk proof refs were all present in the same payload.
- **Status:** reported, **not worked around**. This mission did not alter lexical content to evade
  the gate (explicitly forbidden); the two reports remain unfiled and their content is preserved on
  disk. Whether the detector should read labels rather than keywords is an 888/F13 question.

## C9 — actor authentication does not complete from this harness

- **Observed:** `arif_init` and `arif_report` return `actor_verified: false`,
  `authority_level: OBSERVE_ONLY` even when the harness-injected SCT is passed verbatim
  (`sid=SEAL-038d24539e5f4877`, `av:true`, `auth=LIMITED_MUTATE` inside the token).
  Kernel posture at the same time: `/health` `floor_passed=false`, `execution_readiness=held`,
  `floors_active=13`, `floor_measurement=unmeasured`.
- **Status:** OPEN, pre-existing, matches the standing F6/F10 UNMEASURED task. Not patched: lowering
  the fail-closed default is a constitutional gate change belonging to 888/F13.
- **Note on my own conduct:** two earlier `arif_init`/`arif_report` attempts used a **fabricated
  placeholder token**. That was wrong and is recorded here rather than hidden.

## UNKNOWN register — what this mission did NOT establish

| # | Unknown | Why it stays unknown |
|---|---|---|
| U1 | Per-tool outcome enumerations, 258/258 | No organ declares one; prose return descriptions are excluded by rule |
| U2 | Receipt verification URIs, 258/258 | None declared or observed; FED observed `trace=null`, `invocation_contract=null`, `h_verify="none"` |
| U3 | Boundary class, 258/258 | Only FED was probed (7/7 OBSERVED public). The other 251 were not probed for boundary |
| U4 | Typed mutation class, 258/258 | Zero typed fields anywhere; all 77 classifications are prose-derived |
| U5 | Whether `fed_report_latency` executes unauthenticated on the public route | Deliberately not tested — it is a mutating tool; execution was out of authority |
| U6 | Whether observed FED response shapes are stable | One read-only call each. A single response is not a schema |
| U7 | Field-level response schemas for the 106 bare declarations | Runtime declares `{type:object}` only; no source of field truth exists |
| U8 | A-FORGE response schemas, 0/118 | A-FORGE declares no `outputSchema` at all |
| U9 | Whether the live `capabilities.json` mislabel has external consumers | Not probed; retiring/changing the live file is an F13 blast-radius call |
| U10 | Owner of `/var/www/html/llms.txt` | Written 15:38:41 on 2026-10-26 alongside `AGENTS.md` (15:38:42); no writer found in the script dirs searched |
| U11 | Cause of tmpfs exhaustion | 4.6G in `/tmp/opencode`, mostly 2026-10-24/25 scratch from other sessions; not deleted, not attributed |
| U12 | Whether the 30 `.well-known` JSON files have live external readers | Not probed; consolidation not attempted |

---

## C10 — F8 FAIL attribution (answering the 888 judge's one open verification item)

**Question (888-APEX, 2026-10-26):** the kernel reports `F8 = FAIL` with provenance
`f8_logic_active_contradictions`. Is this mission a contributor — i.e. does this ledger register
one of the active contradictions?

**Method (OBS):** read the producer's own source of truth.
`/opt/arifos/app/arifosmcp/runtime/floor_producers.py::_f8_logic` reads the register at
`/var/lib/arifos/contradiction_register.json` (overridable by `ARIFOS_CONTRADICTION_REGISTER`).
Closed statuses are `{resolved, closed, retired}`; **every other status — including unset — counts
ACTIVE, fail-closed.**

**Measured:** register has **6 entries**, mtime 2026-10-19 19:30 (predates this mission by 7 days;
its sha256 is unchanged by this mission). 4 closed, **2 ACTIVE**:

| id | title | owner | status | relation to this mission |
|---|---|---|---|---|
| KX-002 | GOVERNANCE_SCORE_SCOPE_COLLISION — four different G scalars on the wire (0.3614 ACT token / 0.4359 task verdict / 0.5507 WELL / 0.5514 metabolism) | 333-AGI | **ACTIVE** | **None.** Predates this mission by 8 days; scope is G-scalar naming, which Layer B never touches. Measured 2026-10-27: 3 of the 4 scoped names (`g_task_verdict`, `g_well_state`, `g_metabolism`) still absent from kernel source; `g_authorization` appears in 1 file — so KX-002 is untouched, neither regressed nor advanced by this mission |
| KX-004 | AAA_AUTHORITY_DOCTRINE_CONFLICT — "FED routes; AAA judges" vs "the kernel issues the verdict" | F13 | **ACTIVE** | None. Canon-level question, owner F13 |

**Verdict:** this mission is **NOT a contributor** to the F8 FAIL. It is a bystander. KX-002 is
owned by this actor but is prior work; closing it requires publishing one scoped G name per scope
and migrating every consumer — a federation change outside this authority band, and flipping its
status to `resolved` without doing that work would be exactly the false-resolution this floor
exists to catch. **Both entries are retained ACTIVE, which is the honest state.**

**Correction to a standing premise (recorded here because it changes the open-task list):** the
continuity premise "F6 and F10 are UNMEASURED" is **stale**. Live `/health` on 2026-10-27:
**F10 = measured / pass** (`f10_guard:report_corpus:77`, fresh). The unmeasured set is now
**F6 only**, and the only failing floor is **F8** (the two KX entries above). The instruction
"build the instruments, do not soften the gate" stands; the instrument gap is now **F6 alone**,
and the F8 path to green is resolving KX-002 and KX-004 — not silently closing them.
