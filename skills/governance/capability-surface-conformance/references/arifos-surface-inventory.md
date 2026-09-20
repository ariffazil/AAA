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
# wire surface — canonical for clients. Session-negotiating servers need the FULL lifecycle:
#   initialize (session id returns in the RESPONSE HEADER)
#   -> notifications/initialized
#   -> tools/list / tools/call  WITH `Mcp-Session-Id`
# Use scripts/mcp_session_probe.py; a bare single POST returns SESSION_MISSING on every organ
# that enforces the lifecycle, and that is a client gap, not a surface defect.
python3 scripts/mcp_session_probe.py --scan 8088,7071,8081,18082,18083,7073 --list

# HTTP convenience projection — may be stale, and some organs do not serve it at all
curl -s http://127.0.0.1:8088/tools
# public projection
curl -s https://mcp.arif-fazil.com/tools

# session verb list — returned by arif_init, also inside the capability token
# registry/manifest files
ls arifosmcp/constitutional_map.py tools_sot.yaml contracts/tools.yaml \
   static/.well-known/peer-contract.json
```

**Transport differs per organ — do not assume one probe shape fits all.** Measured: arifOS answers
`tools/list` over a single POST; WEALTH, WELL and GEOX refuse until `notifications/initialized` has
been sent; A-FORGE and FLOW would not answer `/mcp` at all. Derive the listening port from the
systemd unit (`systemctl cat <unit>.service` names it in a header comment) rather than guessing — a
wrong port yields an empty response that is easily misread as a dead service. Record, per organ,
which transport and which lifecycle steps it needs. `/tools` counts and session counts can disagree
(measured 25 declared vs 27 over the session) — count both before calling either authoritative.

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
  concluding, and treat the root cause as UNMEASURED until pinned. **And read every nesting level of
  the SAME payload before believing any of it** — one `arif_init` response carried
  `session_birth.actor_cryptographically_verified: false` beside
  `result.actor_cryptographically_verified: true` (same actor, same question, two answers), and
  `authority_band: LIMITED_MUTATE` granted while that same session's attestation was marked
  FAILED. So two defects coexist here and must be reported separately: (a) the intra-payload
  contradiction, and (b) **authority granted on a session whose own gate reports failure** — the
  fail-closed claim is not held end-to-end. Fix (b) by making the authority decision a reader of
  the attestation result, not a sibling of it.
- **Attestation-scope mismatch** — two components answering "which code is running?" from
  different paths. Measured: the kernel attests
  `<venv>/lib/python3.*/site-packages/arifosmcp` (exists), while a verifier inspects
  `/usr/local/lib/python3.*/dist-packages/arifosmcp` (**does not exist** — the directory holds only
  an `arifosmcp-deprecated/` stub and an editable-install `.pth` for a different package). Every
  DRIFT verdict from that witness describes an empty target. This is a *measurement* defect, not a
  parity defect, and it must be fixed before any drift number from that source is quoted.
- **Registry-as-materialised-copy** — the kernel serves skills from `ARIFOS_SKILL_ROOT`
  (`/etc/arifos/skills` in production), a *copy* whose entries are symlinks back into the live
  mesh (`/root/AAA/skills`, via `/root/.agents/skills`), while the live tree keeps growing.
  Measured: 223 names in the served root vs 638 on disk → `skill://{name}/SKILL.md` answers
  "Skill not found" for every skill added since the copy. Generalise: **any served registry that
  is a materialised copy (rsync/bake/snapshot/ConfigMap) of a live tree drifts monotonically.**
  Check `stat` mtime of the served root against the live root, name the sync job that is supposed
  to close the gap, and if no such job exists call it a one-time bake, not a registry.
- **Non-enumerable index** — `skill://index` reports counts and metadata but **no per-skill
  names**, so a client cannot enumerate the catalogue and must guess names to read anything. That
  is a conformance defect of its own: *a registry that cannot be enumerated cannot be conformed
  against.* Grade an index by whether a caller can derive the full name set from it.
- **Guard rejection count** — the same surface carries a path-traversal containment guard that
  rejects entries whose resolved path leaves the skill root. 18 *legitimately* symlinked skills
  are refused ("Skill name rejected") even though containment is satisfied by the resolved path.
  When a guard's rejection count is non-zero, read the guard's stated **intent** before treating
  its refusals as correct enforcement — a guard can pass its own tests and still refuse valid
  inputs. Related, same evening: the kernel's `skill://{name}` template resolves **only the
  top-level directory name** of its root, so a skill nested under a category folder is
  unreachable by its bare name.

## Patching arifOS safely

- The checkout under `/root/` is **not** the served artifact. The served code is under
  `/opt/arifos/current/venv/.../site-packages/`. Land fixes via build → wheel → deploy.
- Repo HEAD moves while you work — other seats commit to the same checkout. Re-pin HEAD
  immediately before the patch and hash inputs at build time.
- Governance-affecting findings (substrate contradiction, attestation failure, floor
  semantics, chain-count reconciliation) are **HOLD territory**: prepare a proposal and
  route the decision to F13. Do not self-patch them.
