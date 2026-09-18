# arifOS Surface Inventory

Concrete projections, SOT locations and known drift sites. Re-probe before quoting — paths
and stage maps move.

## Canonical sources

| What | Where |
|---|---|
| Stage map (SOT) | `arifosmcp/constitutional_map.py` → `CORE_NINE_STAGE_MAP` |
| Public tool set | `KERNEL_ABI_8` — 8 canonical public verbs |
| Generated surface | `tools_sot.yaml` (generated from `constitutional_map.py`; never hand-edit) |
| Peer contract | `static/.well-known/peer-contract.json` — carries the canonical set + a semantic capability hash (RFC8785-JCS + SHA256 over sorted semantic records) |
| Machine/topology roles | `/root/AAA/docs/MACHINE_MAP.md` (F13-ratified) |

## Projections to enumerate

```bash
# wire surface — canonical for clients
#   POST /mcp: initialize -> tools/list
# HTTP convenience projection — may be stale
curl -s http://127.0.0.1:8088/tools
# public projection
curl -s https://mcp.arif-fazil.com/tools
# session verb list — returned by arif_init, also inside the capability token
# registry/manifest files
ls arifosmcp/constitutional_map.py tools_sot.yaml contracts/tools.yaml \
   static/.well-known/peer-contract.json
```

## Known drift sites (all observed live)

- **HTTP `/tools` stage column** — disagreed with both the canonical stage map and the wire
  surface on 4 of 8 tools (route, memory, judge, forge), including printing a stage value
  that canon marks DEPRECATED. The wire surface was correct; the convenience endpoint was
  stale.
- **`contracts/tools.yaml`** — described itself as the federation SINGLE SOURCE OF TRUTH for
  a 25-capability universe while `tools_sot.yaml` declared its own SOT to be
  `constitutional_map.py` with 8 public tools. Two documents claiming SOT.
- **Legacy alias residue** — a partial old-name → canonical-name dispatch layer: one legacy
  name resolved to a canonical handler with an untranslated contract (validation error on
  every call), another resolved but returned HOLD with an empty actor, and the rest returned
  `Unknown tool`. Inconsistent by construction.
- **Public package distribution** — an older package identity remained publicly installable
  with a superseded architecture after the rename, while repo metadata ran ahead of the
  published release. A dependency-level source of stale surfaces.
- **Substrate triple-contradiction** — one response carried `substrate.state` at three
  nesting levels reporting two different values (top-level HEALTHY vs `result` and
  `effective_state` DEGRADED). Count the readings first.
- **Boot attestation** — `session_authority_state=BOOT_ATTESTATION_FAILED` returned while
  `source_commit == deployed_commit` and `drift=false`. Commit equality is not the whole
  attestation chain; probe wheel hash, runtime manifest hash and canon version before
  concluding, and treat the root cause as UNMEASURED until pinned.

## Patching arifOS safely

- The checkout under `/root/` is **not** the served artifact. The served code is under
  `/opt/arifos/current/venv/.../site-packages/`. Land fixes via build → wheel → deploy.
- Repo HEAD moves while you work — other seats commit to the same checkout. Re-pin HEAD
  immediately before the patch and hash inputs at build time.
- Governance-affecting findings (substrate contradiction, attestation failure, floor
  semantics, chain-count reconciliation) are **HOLD territory**: prepare a proposal and
  route the decision to F13. Do not self-patch them.
