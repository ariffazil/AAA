---
name: arifos-mcp-resource-surface
description: "Operate the arifOS MCP resource registry — add, remove, or consolidate arifos:// resources under arifosmcp/resources/, and sync the locked canonical-surface enforcement test. Trigger: 'reduce resources', 'remove deprecated resources', 'merge resource X into Y', 'registry cleanup', or any edit touching CANONICAL_RESOURCES / register_resources() / _RESOURCE_PROVENANCE. Adjacent to arifos-kernel-e2e-testing (surface gate tests) and arifos-integration-recon (code-path tracing)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [arifos, mcp, resources, registry, consolidation, surface]
    related_skills: [arifos-kernel-e2e-testing, arifos-integration-recon, canon-integrity-check]
---

# arifOS MCP Resource Surface Operations

The resource surface is the set of `arifos://`, `tree777://`, `skill://` URIs
exposed by the MCP server. It lives in `/root/arifOS/arifosmcp/resources/` and is
**reduced/consolidated periodically** (2026-06-28 zen removal, 2026-07-16/19
atlas333, 2026-08-08 48→30). Expect this pattern to recur — the namespace_index
migration map still lists aspirational URIs with no handlers (`skill://index`,
`arifos://init/agent_init`, `arifos://flow-state`, `arifos://carry-forward`).

## Architecture map — where registrations actually live

`resources/__init__.py` exposes `register_resources(mcp)` (~line 540) which calls
one `register_xxx(mcp)` per family. **Removal targets are NOT all in `__init__.py`.**
Trace each target URI to its module first:

```bash
rg -n '@mcp\.resource\("TARGET"' arifosmcp/resources/     # the handler
rg -n 'TARGET' arifosmcp/resources/*.py                   # append + embedded lists
```

Known homes (verified 2026-08-08):
- `atlas333/*` (index, paradox, zones, organs, quote, seal/head…) → `atlas333.py` `attach_to_mcp_resource` (single function registers ALL of them)
- `wisdom/*` → `wisdom_resources.py` `register_wisdom_resources`
- `resources/index` + `resources/audit` → `resources_index.py` `register_resources_index` (usually already commented out — but its import may still linger)
- `resources/index` **ALIAS** → `namespace_index.py` `register_namespace_index` (shares one handler with `arifos://index` — removing the alias means editing the return list, not just __init__)
- `mcp-alignment` → `mcp_alignment.py`; `seal-readiness` → `seal_readiness.py`; `mcp/surface-map` → `surface_map.py`
- dynamic-number indices (`aaa-index`, `aforge-index`, `atlas-repo`, `vault999-index`) → own modules, pure import-and-call removals

## Workflows

There are two distinct workflows under this skill. **Pick the right one:**

### A. Reduce / consolidate (existing workflow)

When the task is to remove or merge existing resources. Steps below.

### B. Add a new ontology-style resource (this skill's other workflow)

When the task is to forge a *new* resource (typically an ontology / institutional
/ civilizational canon document). Pattern: read the closest existing resource
in the same family as a template, draft a `_TEXT` constant + `register_xxx(mcp)`,
verify, then wire into `__init__.py`. Pitfalls below are additive to the reduce
workflow. **Use `templates/ontology_resource.py.j2` as a known-good scaffold.**

Concrete recipe (proven 2026-08-08 when forking `civilization.py` →
`institution.py`):

1. **Read the family template fully** — pick the closest analogue (`civilization.py`
   for ontology/canon, `jurisdiction.py` for legal frame, `seal_readiness.py` for
   state-bearing surfaces, `trinity.py` for cross-organ composites). The shape
   (TextResource + `register_xxx(mcp) -> list[str]`) is uniform.
2. **Define a `*_TEXT` constant** with the brief's content constraints baked in:
   - **Byte budget** (typically ≤1200) — measure `len(text.encode())`, NOT `len(text)`.
     Em-dashes (—) and non-ASCII glyphs are 2–3 bytes each in UTF-8 and silently
     blow the budget.
   - **Forbidden content** for canon-style resources: no dates, no "version 2026.x",
     no tool names (e.g. `arif_judge`, `geox_evidence`), no dynamic numbers.
   - **Institutional voice** — use "the institution that decides", not "arifOS";
     organs earn voice only after the institution is named.
   - **Mandatory closer** (e.g. `DITEMPA BUKAN DIBERI — ...`) — verify the *last
     line* starts with the slogan, not just that it appears anywhere.
3. **`register_xxx(mcp) -> list[str]`** returning `[uri]` — match the existing
   return-type contract (the call site in `__init__.py` flattens these).
4. **Tag set** is exactly the three required keys: `{"resource", "<domain>", "ontology"}`
   for canon resources. Do not invent extra tags; the surface gate test asserts
   the canonical set.
5. **Verify before wiring** — run `ruff check` + `ruff format --check` on the new
   module. Then run the resource round-trip (see Verification, below). **Only
   after** both pass, import the function in `__init__.py` and add it to
   `register_resources()`.
6. **Wire into `__init__.py`** — add the import, add the `register_xxx(mcp)` call
   in the right alphabetical/by-family block, update `CANONICAL_RESOURCES` tuple,
   update module docstring count.
7. **Run the full verification checklist** at the bottom of this skill.

### A. Reduce / consolidate (existing workflow)

1. **Read `__init__.py` fully** — register_resources starts ~line 540; provenance dict ~line 92.
2. **Map every removal target** to its register call AND module (see map above). Group targets by module so you edit each file once.
3. **Edit `__init__.py`:**
   - comment out the `register_xxx(mcp)` calls (keep them as `# REMOVED <date> — reason` comments — the codebase convention)
   - remove the imports (comment with the URI they served)
   - delete `_RESOURCE_PROVENANCE` entries for removed URIs
   - update `CANONICAL_RESOURCES` tuple + module docstring (count must match the target)
4. **Edit source modules** where targets live: delete handler blocks (decorator + function + `registered.append`), update module docstrings, **and strip removed URIs from embedded lists inside KEPT resources** — e.g. `atlas333_index`'s `resources_mcp` array, `wisdom/contract`'s `resources` array, `mcp_alignment.py`'s surface table.
5. **Sync the enforcement test** — `arifosmcp/tests/test_canonical_resources_enforcement.py` mirrors the surface as machine-enforced law (see Pitfalls).
6. **Verify** (checklist below). Never stop at AST-parse; run the actual suite.

## Pitfalls

- **`list_resources()` is async.** In FastMCP 2.x, `mcp.list_resources()` returns
  a coroutine, not a list. You cannot iterate it synchronously. Use
  `await mcp.list_resources()` inside an `async def`, or just read the text from
  the `TextResource` directly (`resource.text`).
- **`await resource.read()` returns `ResourceResult`, not the text.** The `.text`
  property on the `TextResource` object is what holds the string. Verification
  scripts must use `resource.text`, not `(await resource.read())`.
- **There is no `_resource_manager`.** FastMCP 2.x exposes resources through
  `mcp.list_resources()` and `mcp.get_resource()` only — do not reach for private
  attributes that don't exist on the current version.

- **KEEP-list URIs may be aspirational.** `skill://index`, `arifos://init/agent_init`, `arifos://flow-state`, `arifos://carry-forward` appear in `namespace_index.py`'s migration DATA but have no handler module. They still belong in `CANONICAL_RESOURCES` (the keep-list says so), and the enforcement test must NOT map them to source files — `test_all_resource_source_files_exist` iterates `CANONICAL_RESOURCE_FILES`, so omit them from that dict or it fails.
- **`skill` is a valid URI scheme** — `test_resource_uri_is_valid` has an allowed-schemes tuple; add `skill` or the scheme check fails.
- **namespace_index.py is a data record, not a registry** — entries for removed URIs are historical/diagnostic migration data; leave them. Don't churn it during a registry reduction.
- **Removed URIs legitimately appear in docstring REMOVED sections** — that's documentation, not active code. When leak-checking, flag only non-comment code.
- **Never delete the module .py files** — the task convention is "remove from the registry, keep the file" (handlers stay importable for future restoration).
- **Count discipline:** task lists give exact keep/remove counts. Reconcile: keep-list URIs + unlisted-still-registered (e.g. `arifos://index`, `arifos://trinity`, `arifos://affordances`) = target total. Recount twice before declaring done.

## Verification checklist

```bash
cd /root/arifOS
# 1. parse
python3 -c "import ast; ast.parse(open('arifosmcp/resources/__init__.py').read())"
# 2. import + end-to-end registration against a real FastMCP instance
python3 -c "
from fastmcp import FastMCP
from arifosmcp.resources import register_resources, _RESOURCE_PROVENANCE, CANONICAL_RESOURCES
reg = register_resources(FastMCP('t'))
removed = {...the removed URIs...}
assert not (set(reg) & removed), 'removed URI still registered'
assert not (set(_RESOURCE_PROVENANCE) & removed), 'provenance leak'
print(len(CANONICAL_RESOURCES), 'canonical')
"
# 3. suite (logfire plugin is broken in this workspace — see arifos-kernel-e2e-testing)
python3 -m pytest arifosmcp/tests/test_canonical_resources_enforcement.py -p no:logfire
```

Use the venv python (`/root/arifOS/.venv/bin/python`) for the suite; global python lacks deps.

## References

- `references/2026-08-08-reduction.md` — the 48→30 reduction: full URI↔module map, keep-list chambers, enforcement-test sync details, leak-check script.
