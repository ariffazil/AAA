---
name: federation-mcp-drift-audit
id: federation-mcp-drift-audit
version: 1.0.0
owner: HERMES
risk_tier: low
description: Use when auditing arifOS MCP federation drift or bypass, or inventorying which MCP tools exist versus which are actually used.
when_to_use: After a deploy, when Arif brings an external audit/contrast report, before any "is the federation governed or just running?" question, or before answering "what should we upgrade / cut / add" about the MCP tool surface.
floor_scope:
- F2
- F4
- F11
autonomy_tier: T0
capability_tier: fed-long-context
ecology_state: WARM
---
# Federation MCP Drift Audit

Run this when asked to inspect or "apex-zen" the federation's MCP tools. The deliverable is a diagnosis grounded in what actually executed, plus a fix plan split by substrate (safe, reversible) vs authority (F13 architectural seal).

## Baseline: run the inspector, then distrust it

`python3 /root/scripts/mcp_federation_inspector.py` (tests arifOS, GEOX, WEALTH, WELL). Two traps:

- Its TOTAL row hardcodes "GREEN" and it `exit 0` even when organs report ERROR. Read the per-organ `Status:` lines and the JSON at `/root/AAA/registries/MCP_INSPECTOR_AUDIT.json` — never trust the aggregate scorecard or exit code.
- It imports each organ's SOURCE module (`from geox_mcp.server import mcp`), not the live HTTP surface, so its tool counts reflect source, not what is deployed. Cross-check live `tools/list` (MCP probe) for source→runtime drift.

## Surface ≠ usage: measure the ledger before proposing a cut or an upgrade

A tool list is a claim about capability; the invocation record is evidence about work. Never answer "which tools need upgrading / which are dead" from the surface alone — enumerate both sides.

1. **Enumerate the live surface across organs, not the source tree.** The baseline inspector imports source modules and over-reports. Run `scripts/mcp_surface_usage_audit.py` from this skill: it does `initialize` → `notifications/initialized` → `tools/list` against each HTTP organ, drives the A-FORGE stdio server through its own CLI, then cross-references the usage ledger.
2. **Measure real usage from the session store, not from history files.**
   ```bash
   sqlite3 /root/.hermes/state.db "select tool_name, count(*) from messages \
     where tool_name is not null and tool_name<>'' group by tool_name order by 2 desc"
   ```
   MCP tools are recorded **prefixed** as `mcp__<server>__<toolname>` — match on that prefix or every MCP tool reads as zero-call. `.hermes_history` records typed text and transcripts, not invocations; scoring against it produces a false "nothing is used" reading.
3. **Report zero-call share per organ as a measurement, not a verdict.** "Unexercised" is the finding; "useless" is a conclusion F13 draws. A zero-call tool may be a rare-but-critical fallback — say which reading you mean.
4. **Protocol era is a separate axis from the tool list.** Test stateless `2026-07-28` with a `server/discover` POST carrying `MCP-Protocol-Version: 2026-07-28`, `Mcp-Method: server/discover`, and the `_meta.io.modelcontextprotocol/*` envelope. A 400 there means the organ is still on the legacy stateful handshake even while its tool list looks healthy.
5. **Hygiene findings outrank tool counts.** Report these first — a tool inventory never shows them, and they silently corrupt downstream output: freshness expiry in an organ's `/health`, cached snapshot files that a cron prompt tells agents to read instead of probing live, and cron prompts naming tools, ports, or versions that no longer exist.

## Many tools failing at once = dependency-pin drift, not per-organ breakage

Import errors like `cannot import name 'McpError'` or `StreamableHTTPServerTransport has no attribute '_check_accept_headers'` across several organs mean a package version drifted off the pin. mcp 2.0.0 renamed `McpError`→`MCPError` and dropped `_check_accept_headers`, silently breaking every transport built against 1.x.

**Never quote a pin from memory, a doc, or this skill — read both sides.** The declared pin and the installed version drift independently, per organ, and the mismatch is itself the finding:

```bash
grep -E '^(mcp|fastmcp)==' /root/arifOS/requirements.txt        # declared intent
/root/<organ>/.venv/bin/python -c 'import importlib.metadata as m; print(m.version("mcp"), m.version("fastmcp"))'   # installed reality
```

Compare organ to organ too — each organ runs its own venv, so a partial upgrade leaves one on a different mcp than the rest. When declared and installed disagree, align one to the other as a single conscious step (raise the install to the pin, or correct the pin if the upgrade was intended and verified); never assume the higher number is the right one, and do not patch each broken organ's transport code.

## Surface ≠ Surface: one server, several disagreeing views

Before believing any capability rate ("only 1 of 17 tools work", "phantom tools", "the surface is broken"), enumerate every surface that advertises capability and diff the SAME field per verb across them:

| Surface | Advertises | Probe |
|---|---|---|
| MCP `tools/list` | the callable tool set | JSON-RPC `tools/list` |
| MCP `prompts/list` | the stage / prompt ladder | JSON-RPC `prompts/list` |
| HTTP convenience route | a projection of the set | `curl :port/tools` |
| Repo canon module | the declared source of truth | grep the registry module |
| Peer / contract manifest | the federated view | read the manifest file |

A server can contradict itself across its own live endpoints. Names matching is not semantics matching — a name-only hash certifies a divergent surface as consistent. Capability hashes must cover `{name, kind, schema, stage, authority, ...}` under canonical serialization, never names alone.

**Client cache vs server divergence — decide before reporting:**

- A name returning `Unknown tool` that appears in **no** live surface is a **cached** pre-migration tool list. Not a server defect. Have the client re-initialise; do not "fix" dispatch.
- Two **live** surfaces disagreeing on one field for the same verb is a **server-side split-brain**. That is the real finding.

**Check the argument surface before calling a schema defect.** Compare the args you sent against `inputSchema.properties` and `required`. A probe-author error looks identical to a schema mismatch — an unexpected-keyword error naming an argument the schema does not declare is a caller error. Re-probe with a documented argument before reporting.

**Sweep before believing a rate.** Call every advertised tool with its safest read-only mode (read it from the live schema, do not guess) and count `phantom` / `mismatch` / `resolved`; `CapabilityTruthRate = resolved / advertised`. Zero phantom over the live `tools/list` is a legitimate PASS even when a client reports most tools dead. Runnable probe: `scripts/mcp_surface_conformance_sweep.py`.

**Root-cause a split-brain — it is rarely build skew.** Test the cheap hypotheses, then look for the real cause:

1. Hash canon vs deployed. Identical sha256 proves the deploy is fine — "server stale" and "canon not deployed" are both dead.
2. Read the **import block** of each surface's file. If the prompt/registry module does not import the canon module, that ladder is hardcoded literals. Zero coupling means no deploy will ever reconcile them.
3. Confirm both files ship in the **same build** (same mtime / same package). Same build + no import = **missing gate, not missing release**.
4. Find the commit that last moved one side only. A one-sided move with no paired update is the divergence point.

Verdict shape: *two sources of truth in one artifact with no consistency gate*. The fix is a single ontology plus a CI gate comparing every surface per verb — not a redeploy.

**Reclassify a mis-framed scar rather than inheriting it.** "Advertised != callable" is the wrong pair when the live surface is clean — the true scar is the semantic split between surfaces. Fixing dispatch when dispatch is already correct wastes the whole wave.

### Which side is authoritative — the split tells you there is a conflict, not who wins

The root-cause steps above establish *that* two surfaces disagree. They do not decide which is
correct, and silently picking one is the commonest way this audit goes wrong. Work the questions in
order; most apparent canon disputes dissolve before reaching F13.

**1. Namespace collision first — confirm both sides describe the same KIND of object.** A token can be
a stage code, a role/lane name, an agent name, or a verdict value, and they are all bare numbers.
Measured: `666` as a tool stage, `888-APEX` as an agent/organ name, `888_JUDGE` as a prompt meta,
`888_HOLD` as a verdict token. A doctrine line reading "888-APEX · constitutional judge |
`arif_judge`" binds an AGENT to a tool — it is not a stage assignment, and reading it as one
manufactures a conflict that does not exist. Before adjudicating, say what type each side names.

**2. Receipt decides, not chronology.** When doctrine and code disagree, do not award precedence to
the newer document on date alone — find the ratification artifact:

```bash
grep -c '<seal-marker-or-chain-id>' /root/VAULT999/SEALED_EVENTS.jsonl   # 0 = not in the ledger
```

A code comment asserting `F13 RATIFIED <date>` with no ledger row behind it, and a doctrine marked
`F13_SEAL` whose own record says *"WAIVED on the record, not satisfied — SEALED_EVENTS.jsonl has no
entry"*, are both **ABSENT**. Report absent on both sides and hand it up. A seal that was waived is
not a ratification, and a comment is not a receipt.

**3. Doctrine that names the ARTIFACT outranks doctrine that names a ROLE.** A doc binding
`arif_judge` (the callable tool) to a number is stronger evidence about the tool than a doc binding
"JUDGE" (the function/lane) — the latter may be describing the cognitive ladder, not the tool's.
Prefer the explicit artifact binding, and quote it.

**4. If both ladders are real and never disambiguated, the defect is NAMESPACE, not canon.** Two
parallel stage ladders (a cognitive one and a tool one) sharing the word *stage* and bare numbers
will always read as contradictory. The cheapest correct fix is qualifying every reference
(`cog:888` vs `verb:666`), not renumbering either ladder — and it needs no canon change. Lead with
that option before proposing a renumber.

**5. Do not pick silently.** If it survives 1-4, write the hypotheses with their evidence weights and
mark it an F13 decision. "Unresolved on purpose" is a valid and honest output; a build spec that
silently assumes one numbering propagates the ambiguity into everything built on it.

### A false paradox is usually two orthogonal measures

Measured: *"attestation FAILED while `source_commit == deployed_commit` and `drift == false`"* reads
as a self-contradiction and is not one. Commit drift measures the **artifact chain** (source → build
→ deployed). Boot attestation measures a set of **governance questions** (identity, substrate,
refusal surface, and so on). Both were correct and always independent — the equality was true and
irrelevant.

Before publishing a paradox, state what each measure is *of*. If the axes differ, the finding is
"two independent checks, both honest, different objects" — not a defect. Reporting it as a
contradiction sends the next session hunting a bug that does not exist, and it is the same error as
reading a health endpoint's `deployed_commit` against a kernel's repo-attested `organ_shas` and
calling one of them a lie.

### Probe an attestation function per-question, never as a single boolean

A flat `BOOT_ATTESTATION_FAILED` / `attestation: false` hides which questions failed and why. Call
the module's own verify function from inside the deployed interpreter — it returns a per-question
answer with `method`, `evidence_ref` and a `note`:

```bash
cd <deploy-root> && ./venv/bin/python -c \
  "import sys; sys.path.insert(0,'<site-packages>'); \
   from <pkg>.runtime.<attestation_mod> import verify_<x>_attestation as v; \
   print(v())" | python3 -m json.tool
```

The dispatch rule is usually a count (`if no > 0: FAIL`), so a single `NO` fails the whole gate.
Three shapes recur:

- **Dead candidate paths.** An evidence check that iterates candidate files with
  `except OSError: continue` hides that one entry is a **directory** — `open()` on a directory can
  never succeed, so that candidate is structurally dead and the list is shorter than it looks.
  Enumerate the candidates and test each for the *type* the check requires, not just existence.
- **Candidates deleted by a later cleanup.** A canonical document removed by a 'chore: stage
  deletions' commit silently kills every check that named it. Grep the check's candidate list
  against the current tree — a path in the code is not a path on disk.
- **A proof path that is impossible for the caller class.** A question whose only `YES` is a
  cryptographic signature cannot pass an unsigned caller *by construction*, and its name-match
  fallback may be capped at `PARTIAL` by doctrine. That is the control working, not a broken gate —
  report it as "structurally unsatisfiable for unsigned sessions", never as a defect to fix.

Distinguish three verdicts for a failing gate: **broken** (a reachable path exists and the check is
wrong), **impossible for this caller** (the control is correct; the caller lacks the credential),
and **stale** (the evidence it looks for was renamed, moved, or deleted). Only the third is a repair.

## Verify an external audit artifact before acting on it

An external audit (human or another model) is a claim, and its vantage is part of the claim.

1. **Confirm the artifact exists and matches its own stated identity** before evaluating any finding: read the file, check its claimed hash/HEAD against the live repo, and check its timestamp against the commits it describes.
2. **Host-pin every existence verdict.** An absence reported from a stale mirror node is not evidence of absence on the truth node. Re-probe on the node the artifact's owner names before accepting *or* disputing.
3. **Split "the audit is wrong" from "my seat cannot see it".** A negative finding carries the same warrant burden as a positive one. Declaring a peer's audit fabricated from a partial view is the same defect with the sign flipped.
4. **Audit artifacts may reach you through a cache or a connector, not the wire.** Names that appear nowhere in the live surface came from the client's cached tool list — that is a finding about the client, not the server.
5. **Grade the report by its own genre.** A document that marks plan as plan is not the same as one narrating unimplemented subsystems in the present tense. Probe the concrete anchors (named files, counts, declared invariants) and leave the prose alone.
6. **Check whether the audit's own premise has gone stale while it ran** — re-read HEAD; a multi-writer repo can move under the auditor.

## Authority failures are silent (feedback asymmetry)

Broken substrate screams (timeout, EROFS, load). Broken authority seals quietly — a bypassed ACT scope token or an advisory 888_HOLD still returns `status: SEAL` and increments the sequence number, looking like success in the ledger. Re-run the probe and read what actually executed (`action_class`, `allowed[]`, `exit_code`), never what the verdict claims.

## The three authority surfaces are disconnected

Declarative capability graph, `gate_action` judgment, and the tool execution path are separate surfaces with no hard interceptor between judgment and execution — that gap IS the scope bypass. `gate_action` lives in `arifOS/arifosmcp/boot/internal_rasa.py`; `/root/scripts/constitutional_guard.py` imports a `core.constitutional_gate` module that does not exist (dead CLI). To close the bypass, wire the gate into the execution path (`forge_shell`, `forge_seal_lane_a`), not beside it.
