# Layer B — Machine Contract: measured state

Generated 2026-10-26 by `compile_machine_contract.py` (read-only). Reproduce:
`/usr/bin/python3 /root/AAA/ops/capabilities/compile_machine_contract.py`

## DELTA (what changed today)

| | before | after |
|---|---|---|
| Governed capabilities an agent can discover | 40 claims, mixed protocols, 5 surfaces | **258**, one shape, 13 organs |
| A-FORGE (the executor) in the public contract | **0 tools** | **118 tools** |
| Public claims verified against runtime | never | **40/40 probed** (39 confirmed, 1 defect) |
| Where the contract comes from | hand-written prose + 2 generators | compiled from live `tools/list` |

Published additively (no existing file touched, both were HTTP 404 before):
- `https://arif-fazil.com/.well-known/machine-contract.json` — 938,594 B, sha256 `7921e5bf…`, HTTP 200 verified
- `https://arif-fazil.com/.well-known/contract-coverage.json` — 23,081 B, sha256 `6b5182fe…`, HTTP 200 verified

## The measured gap

Live surface (OBS, probed 2026-10-26, MCP `initialize` handshake + `tools/list`):

    organ              live  published  ceiling
    a-forge             118          0  EXECUTE_AFTER_SEAL
    geox                 27          1  COMPUTE_ONLY
    chron                22          0  COMPUTE_ONLY
    wealth               15         18  COMPUTE_ONLY
    hermes               15          0  RELAY_ONLY
    well                 10          1  REFLECT_ONLY
    claim-ledger         10          0  APPEND_ONLY
    arifos                9          2  JUDGE_ONLY
    filings               8          0  READ_ONLY
    numeric-audit         7          0  ADVISORY_ONLY
    fed                   7          0  ADVISORY_ONLY
    session-federation    6          0  READ_ONLY
    media-ingest          4          0  OBSERVE_AND_GENERATE
    TOTAL               258         40

`published` counts are per-organ claims mapped from `capabilities.json`; wealth's 18 = 15 MCP
tools + 3 HTTP routes, so it is **not** an over-claim (see retraction below).
Coverage = 40/258 = **15.5%**. 258/258 tools carry a valid `inputSchema` (100%).

## Two real defects, both verified

1. **PUB** `arifos.arif-fazil.com / observatory_snapshot` declares `protocol: "mcp"` but is not in
   arifOS's live 9 MCP tools; its path `/api/observatory/v1/snapshot` answers **HTTP 200**.
   Classification: `protocol_mislabel_http_ok` — a labelling defect, **not** a dead capability.
2. **SOT** `fed :7074` answers MCP live with 7 tools but `organs.yaml` declares no MCP surface for
   it. Classification: `mcp_live_but_undeclared_in_organs_yaml`. Consequence, demonstrated: any
   consumer that selects MCP targets from `organs.yaml` silently drops organs — this is exactly how
   the first cut of this compiler lost `geox`, `wealth` and `well` (52 tools), because those three
   declare `public_mcp` but no `mcp_port` and no `interfaces` block.

## Layer B: what the runtime gives free vs what it does not

This is the actual work list. It is measured, not estimated.

    field                          free from runtime     needs new runtime declaration
    capability_id                        258/258
    transport (local + public)           258/258
    request_schema (live inputSchema)    258/258
    authority.organ_ceiling              258/258
    status.liveness                      258/258
    mutation.class                        77/258 (30%)
    response_schema                             0        0/258
    outcomes (per-tool verdict enum)             0        0/258
    receipt.verification_uri                     0        0/258
    boundary (public|internal|governed)          0        0/258

`mutation.class` is 77/258 **and all 77 are `declared_in_prose`** — parsed from description text
(`ACTUATOR · shell · MUTATE`), zero from a typed field. Distribution: OBSERVE 58, MUTATE 9,
EXECUTE 9, DEPLOY 1, undeclared 181 (70%).

So the shape Arif specified is ~60% free today and ~40% blocked on organs declaring four things
they currently do not: response schema, per-tool outcomes, receipt URI, boundary class. Every one
of those is emitted as `{"state": "undeclared", "reason": …}` in the contract — never invented.

## Surface entropy (named, not fixed)

`/var/www/html/.well-known/` holds **30 JSON files**. At least four publish a capability vocabulary
and they disagree: `capability.json` (4 caps, 2026-07-27), `capabilities.json` (40 caps, generated
2026-10-23 by WEALTH `scripts/sync_manifest.py`), `ai-catalog.json` ≡ `ard.json` (byte-identical,
md5 `be362765…`), plus `agent-registry.json`, `webmcp.json`, `mcp.json`. Internal SOTs add three
more: `organs.yaml` (41 components), `capability-ledger.yaml` (17 caps, updated 2026-09-12, whose
probe harness has ever probed exactly **1** capability, twice, on 2026-09-12), and
`state/ir/capability-graph/` (2 organs, emitted 2026-10-18).

## Retraction (honesty record)

Mid-session I stated WEALTH "publishes 18 against 15 live — advertises tools that no longer
answer." **That was wrong.** It came from comparing published names against live MCP tool names
while `capabilities.json` mixes `mcp`, `http` and `webmcp` in one flat list. Verified under each
entry's own declared protocol: 15 `confirmed_live` + 3 `confirmed_reachable` = 18/18 correct. The
compiler now verifies per-protocol precisely so this class of false accusation cannot ship.

## Deliberately NOT done (authority, not ability)

- **Retiring/merging the 30 `.well-known` files.** Public surface, external consumers unknown,
  irreversible for anyone already reading them. That is an F13 blast-radius call.
- **Editing `capabilities.json`.** It is generated by the WEALTH lane (`sync_manifest.py`);
  writing it here would be clobbered and would cross lanes.
- **Adding a discovery pointer to `/var/www/html/llms.txt`.** That file was written at 15:38:41
  today by another lane (`AGENTS.md` 15:38:42, same writer, not in any script dir I searched).
  Concurrent-writer hazard. One line is needed there or the contract stays an orphan:
  `- [Machine contract](https://arif-fazil.com/.well-known/machine-contract.json)`.
- **Executing any mutating verb.** `tools/list` is read-only by construction; HTTP verification
  is GET-only. The contract states this in every entry: `enumerated != callable != authorized`.

## Reading this contract correctly

It is a **Declared** surface. Declared ≠ Enforced ≠ Observed consequence. Nothing here proves an
organ refuses what it forbids; it proves what an organ says it accepts, verified live at probe time.
Reading it grants no authority.
