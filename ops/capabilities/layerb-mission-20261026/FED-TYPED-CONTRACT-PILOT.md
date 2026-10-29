# FED-TYPED-CONTRACT-PILOT — Phase 3/4/5

Scope: **FED only** (`fed-router.service`, `:7074`, `FED — Federation Router 4.1.2`, ceiling
`ADVISORY_ONLY`). No other organ was calibrated. Candidate **not deployed, not published**.
Envelope schema: `machine-contract-extension.schema.json` (v1.0-candidate).
Candidate data: `fed-typed-contract.candidate.json` — 7/7 capabilities conform (Draft 2020-12).
Raw evidence: `fed-pilot-raw.json` · runner: `fed_pilot_probe.py`.

## Phase 3 — the declaration envelope

Four fields, each carrying its own evidence state. The three states are kept strictly apart:

- **DECLARED** — explicitly supplied by the organ runtime or its typed registry.
- **OBSERVED** — derived from a captured runtime response or deployment configuration; *not*
  declared by the organ. Never promoted to DECLARED.
- **UNKNOWN** — neither declared nor safely established. `null` + UNKNOWN is valid; fabricated
  completeness is invalid.

Guardrails encoded in the schema and honoured in the data: tool descriptions are prose, not typed
declarations · an HTTP 200 does not by itself prove a public boundary · a receipt identifier does
not prove a verification URI exists · possible outcomes are not the verdict of one call.

Schema refinement made during the pilot: v1.0 initially set `additionalProperties: false`, which
rejected the provenance fields (`evidence_class`, `reason`, `does_not_imply`, `observed_shape`,
`richness`). The mission specifies a *minimum* shape, so those fields were **typed into the schema**
rather than stripped from the data — evidence is carried, and `additionalProperties` stays closed.

A second, later correction (555 verify lane, 2026-10-26): the pilot originally stated "7/7
capabilities conform (Draft 2020-12)" unqualified. That was true only for the 4-field **envelope
slice**; validating each per-tool object as written failed 0/7, because the extension schema closes
`additionalProperties` while each entry carries 10 keys. The claim was not false, but it was
unqualified. Two fixes, both applied:

1. `fed-typed-contract.candidate.schema.json` — a document-level schema that `$ref`s the extension
   envelope unchanged and types the per-tool keys that are *not* part of the envelope. Both scopes
   are now separately testable and both pass.
2. `validate_candidate.py` — a runnable validator that reports **SCOPE A (envelope) 7/7** and
   **SCOPE B (document) 1/1**, plus six controls in two directions. Reproduce with
   `/usr/bin/python3 validate_candidate.py <dir>` (exit 0 = pass).

Control behaviour, corrected: the schema REJECTS a bad state enum, an asserted `class` beside
`state: UNKNOWN`, an asserted `schema` beside `UNKNOWN`, and an asserted `allowed` beside
`UNKNOWN` — the last three are enforced by a new `if/then` rule: **when a field's state is
UNKNOWN, its value must be null**; a field that is not declared cannot carry an asserted value.
The schema ACCEPTS a null `evidence_ref` and a null `class` beside `UNKNOWN`, because the mission
rule is explicit that null plus UNKNOWN is valid. An earlier draft of this report claimed a
`class` beside UNKNOWN was rejected — that rejection actually came from a different control
(a bad enum in another field), and the claim was wrong until the conditional was added.

Structural validity is still not truth: a `state: "DECLARED"` carrying invented content validates
cleanly. Only re-probing the runtime catches that (ledger C7).

## Phase 4 — per-tool result

Execution rule applied: `tools/call` was issued **only** for read/compute-safe tools.
`fed_report_latency` was **not executed** — its own description states it writes the
`route_latency` table ("Agents call this after every API call to populate route_latency table with
live telemetry"), so sampling it would be a mutation. Its runtime response is recorded as
`OBSERVATION_NOT_EXECUTED` and its response shape stays UNKNOWN.

6 of 7 tools executed read-only; 1 not executed.

| tool | response_schema | outcomes | receipt URI | boundary | evidence class | gap |
|---|---|---|---|---|---|---|
| `fed_route` | DECLARED (bare `{type:object}`) + shape OBSERVED | UNKNOWN | UNKNOWN | OBSERVED `public` | DECLARED_TYPED | no field-level response schema; no outcome enum; no receipt path |
| `fed_status` | DECLARED (bare) + shape OBSERVED | UNKNOWN | UNKNOWN | OBSERVED `public` | DECLARED_TYPED | same |
| `fed_probe` | DECLARED (bare) + shape OBSERVED | UNKNOWN | UNKNOWN | OBSERVED `public` | DECLARED_TYPED | same |
| `fed_classify` | DECLARED (bare) + shape OBSERVED | UNKNOWN | UNKNOWN | OBSERVED `public` | DECLARED_TYPED | same |
| `fed_contrast` | DECLARED (bare) + shape OBSERVED | UNKNOWN | UNKNOWN | OBSERVED `public` | DECLARED_TYPED | same |
| `fed_health` | DECLARED (bare) + shape OBSERVED | UNKNOWN | UNKNOWN | OBSERVED `public` | DECLARED_TYPED | same |
| `fed_report_latency` | DECLARED (bare); response **OBSERVATION_NOT_EXECUTED** | UNKNOWN | UNKNOWN | OBSERVED `public` route exists; public **mutability UNPROBED** | DECLARED_TYPED | mutating tool on an unauthenticated public route — not executed, so not established |

Evidence class per field (only `DECLARED_TYPED` counts toward typed coverage):

    field            DECLARED_TYPED   OBSERVED_RUNTIME   DECLARED_PROSE   UNKNOWN
    request_schema        7/7               –                 –            0/7
    response_schema       7/7 (all bare)   6/7 shapes         –            0/7
    outcomes              0/7               –                 0/7          7/7
    receipt URI           0/7              7/7 (absence)      –            7/7 value
    boundary              0/7              7/7                –            0/7
    mutation.class        0/7               –                 7/7          0/7

### What the runtime actually declares

`request_schema` — DECLARED_TYPED 7/7. Live `inputSchema` with typed properties and defaults, e.g.
`fed_route`: `task:string`, `model:string=deepseek-v4-pro`, `modality:string=text`,
`agent_id:string=opencode`, `constitutional_tier:integer=333`, `effort_level:string`,
`tokens_in_estimate:integer=0`, `tokens_out_estimate:integer=0`, `operation:string=auto`.
`fed_contrast` requires `route_a`, `route_b`; `fed_classify` requires `task`;
`fed_report_latency` requires `provider`, `model`, `latency_ms`.

Input validation is **enforced**, and this mission produced the evidence by accident: a first
`fed_route` call passed `constitutional_tier: "advisory"` (string) and the runtime returned
`isError: true` with `1 validation error for call[fed_route] … Input should be a valid integer`.
The corrected call (`constitutional_tier: 333`) succeeded. Both attempts are preserved in
`fed-pilot-raw.json`.

`response_schema` — DECLARED_TYPED 7/7 but **every one is bare**: `{type: object,
additionalProperties: true}`, zero properties. Source: FastMCP generated it from the `-> dict`
return annotations in `/root/AAA/scripts/fed_router.py`. FED has no `tools_sot.yaml` and no
pydantic `response_model`, so nothing supplies field-level shape. `_meta` carries only
`{"fastmcp": {"tags": []}}`.

Observed shapes are recorded **separately** from the declared schema and never promoted:

    fed_health    status, port, version, tables, state_db
    fed_status    providers, latency, health, spend_summary, state_db, generated_at
    fed_probe     gateways, db_providers, route_health, note
    fed_classify  capability, signature, confidence, matched
    fed_contrast  route_a, route_b, hcsvog
    fed_route     routes, meta, emd, jit, trace, invocation_contract

A single response is not a schema. Each observed shape is labelled `OBSERVED` with the note
"observed top-level keys from ONE read-only call".

`outcomes` — UNKNOWN 7/7. No typed outcome enumeration exists in `tools/list`, `outputSchema` or
`_meta`. Descriptions state only what is returned, in prose, which the mission explicitly excludes
from typed declaration. Values seen in single calls are recorded under
`observed_single_call_values_NOT_outcomes` and are **not** treated as the outcome set:
`fed_route` → `emd.verdict: EMD_ALIGNED`, `meta.hcsvog.h_verify: none`,
`latency_flag: INSUFFICIENT_TELEMETRY`, `health: LIVE`; `fed_contrast` → `hcsvog.h_verify: none`;
`fed_classify` → `signature: fed-conversational`.

`receipt` — UNKNOWN 7/7, with observed absence as evidence. FED emits no receipt identifier and no
verification URI. Observed in the captured responses: `fed_route.trace = null`,
`fed_route.invocation_contract = null`, `h_verify = "none"` in both `fed_route` and `fed_contrast`.
Recorded as OBSERVED evidence of absence — which does not prove no verification path exists
elsewhere (UNPROBED).

`boundary` — OBSERVED `public` 7/7, from deployment configuration plus a live probe, not from an
HTTP 200 alone:

1. `/etc/caddy/vhosts/fed.arif-fazil.com.conf:6` → `reverse_proxy 127.0.0.1:7074`
2. live unauthenticated `POST https://fed.arif-fazil.com/mcp` `initialize` + `tools/list` returned
   **all 7 tool names** with no credential presented.

`does_not_imply` recorded on every entry: an unauthenticated `tools/list` does not prove every tool
*executes* unauthenticated. `fed_report_latency` was not executed, so its public mutability is
**UNPROBED** — flagged for F13, not asserted.

`mutation.class` — DECLARED_PROSE 7/7, typed 0/7. `fed_report_latency` → MUTATE (description states
it populates a table); the other six → OBSERVE (read/compute language, no write language). FED
declares no typed mutation field.

## Phase 5 — measure, do not market

Four separate numbers. **Never combined into one percentage.**

### A · Discovery coverage

    live governed tools                    258 across 13 live MCP organs (31 ports probed)
    present in the compiled contract       258/258  (100%)
    present in the legacy public surface    40/258  (15.5%), 40/40 matching runtime after repair

### B · Typed contract coverage (DECLARED_TYPED only, federation-wide, n = 258)

    request schema typed              258/258   (field-level 224/258)
    mutation class typed                0/258
    response schema typed             138/258   (field-level 32/258)
    outcomes typed                      0/258
    receipt verification URI typed      0/258
    boundary typed                      0/258

### C · Observed but undeclared

    response schema bare {type:object}       106/258
    mutation class prose-derived              77/258
    FED boundary OBSERVED (candidate only)      7/7 fed tools — not counted as typed
    FED response shapes captured              6/7 executed read-only

### D · Unknown coverage

    mutation class                 181/258
    response schema                120/258
    outcomes                       258/258
    receipt verification URI       258/258
    boundary                       258/258
    FED outcomes / receipt            7/7 each

### Effect of the FED pilot on federation-wide typed coverage

**Increase = 0 typed declarations.** The pilot produced a validated *candidate* envelope
(7 tools × 4 fields), not runtime declarations. FED's 7 `outputSchema`s were already inside the
138/258 measured before the pilot ran. Nothing was promoted from OBSERVED to DECLARED, and no
inferred or observed field is reported as completed coverage.

## F13 decisions required for the next gate

1. **Deploy the 1A repair?** The site source is patched (+1/−1); the live
   `/var/www/html/.well-known/capabilities.json` still mislabels `observatory_snapshot` as `mcp`.
   Deploying is a public-surface action outside this authority band.
2. **Public unauthenticated FED MCP route.** `https://fed.arif-fazil.com/mcp` answers `tools/list`
   with all 7 tools and no credential, including the mutating `fed_report_latency`. Whether that is
   intended exposure is an F13 call. This mission probed read-only and did **not** test whether the
   mutating tool executes publicly.
3. **Adopt the extension envelope?** `machine-contract-extension.v1` is validated on FED only.
   Extending it means organ runtime work (typed mutation class, field-level response schemas,
   outcome enums, receipt URIs, boundary declarations) — 4 declarations currently at 0/258.
4. **Retire or merge the 30 `.well-known` JSON files** (incl. the byte-identical pair
   `ard.json` ≡ `ai-catalog.json`, md5 `be362765…`). Irreversible for external readers; not taken.
5. **`llms.txt` pointer.** One line is needed or the compiled contract stays an orphan. The file was
   written 15:38:41 on 2026-10-26 by another lane; not edited here.
6. **tmpfs exhaustion (P0, found during this mission).** `/tmp` is a 16G tmpfs that reached **100%**
   during this mission, of which `/tmp/opencode` held 4.6G — mostly stale scratch from 2026-10-24/25
   belonging to other sessions (`arifflow-final-2` 1.1G, `arifflow-head` 780M, `aaa-c778952b` 587M,
   `aaa-parent` 376M, `scratch-postimage-C`/`gate-base.kzIe`/`base-check`/`aaa-baseline` 372M each).
   Writes to `/tmp` failed with `ENOSPC` (one written artifact truncated to 0 bytes). Those 8 dirs
   were **moved, not deleted**, to `/root/work/tmpfs-quarantine-20261026/` (4.3G, 0 open FDs at move
   time, owner lane UNKNOWN, restore = `mv` back). tmpfs went to 34%; the relief was *transferred*,
   not eliminated — `/dev/sda1` is now 95% (21G free).

---

## Verification lane (555-ASI) — findings and fixes applied

An independent verify lane probed this mission live. It reproduced every load-bearing number
exactly (258 / 13 / 118 / 7 · 138 declared, 32 field-level, 106 bare · +16/−0 · +1/−1 · 41
components · 40/40 published · 0 defects · recompile byte-identical `sha256 6ff7b67dac0641c0…`
equal to this mission's own after-hash) and confirmed the stop condition held: nothing deployed
(live still `protocol:"mcp"`, `generated_at 2026-10-23T13:18:13Z`, `/var/www/html` contract still
`7921e5bf…`), and the mutating FED tool was not executed (it confirmed
`/root/.local/share/arifos/fed_state.db` mtime unchanged at 2026-10-14).

It raised two label defects and two precision notes. All four are addressed:

| finding | class | action taken |
|---|---|---|
| "7/7 conform" true only for the envelope slice, not the document | overclaim (precision) | document schema added + validator now reports both scopes: A 7/7, B 1/1 |
| `protocol-probe.{before,after}.json` were full coverage snapshots, not protocol probes; `.after` was a byte-duplicate of `after/contract-coverage.json` | labelling | regenerated as true protocol records (per-protocol claim tallies + per-organ transport table); full coverage kept under `contract-coverage.{before,after}.json` |
| "a class beside UNKNOWN is rejected" was not actually true — the rejection came from a different control | false claim (mine) | conditional `if/then` added: UNKNOWN forces a null value; the claim is now true and tested |
| "10 gates passed" was self-attested in a file with no receipts | under-evidenced | the lane independently re-ran all ten and reproduced the byte-identical hash; recorded here rather than as a bare assertion |

It also independently corroborated prior tmpfs exhaustion from `journalctl` (3 × ENOSPC on
`/tmp/runc-process…` at 21:08, before the 21:42 move) while noting the exact "100%" figure is
not recoverable from any retained time-series — recorded as corroborated-by-testimony, not
independently witnessed.
