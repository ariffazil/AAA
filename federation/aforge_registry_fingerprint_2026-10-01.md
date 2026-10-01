# A-FORGE Registry Fingerprint + Live MCP Health — DRAFT 2026-10-01
# Lane: 555b
# Status: read-only receipt, no production change

> Probed 2026-10-01 by 555-ASI Φ SENSE (Lane 555b, sensory / read-only).
> Every hash below is sha256 of the literal bytes on disk at probe time, or of a
> canonical sorted name list. Re-probe before trusting — the AAA repo had an active
> concurrent writer during this session (see DRIFT-3).

## 0. Headline

The A-FORGE tool surface is **122 tools**, and three independent sources CONVERGE on
that number and on the identical sorted name list. The canonical A-FORGE-scoped
registry fingerprint is:

```
AFORGE_REGISTRY_FINGERPRINT (sorted 122 tool names, newline-terminated)
sha256 = aa39ecd5cc2a282a511379c9f789daad1e60356b0e0266aac45c58428f6f03c7   [OBS]
```

This is the value a boot sequence should diff against to decide whether to reload the
capability map. It is A-FORGE-scoped. It is NOT the federation-wide CAPABILITY_INDEX
digest (see DRIFT-1 — a peer file conflates the two).

## 1. Probe 1 — sources read, counts, fingerprints

Normalization: tool/skill names lowercased-preserved-as-authored, deduplicated, sorted,
one per line, trailing newline, no other whitespace. Raw-bytes hash = sha256 of the file
as it sits on disk.

| # | Source path | Scope | Count | sha256(sorted name list) | sha256(raw file bytes) |
|---|---|---|---|---|---|
| S1 | /root/A-FORGE/.registry/fingerprints.json | A-FORGE live registry snapshot (generated_at 2026-10-01T10:49:06Z) | 122 | aa39ecd5cc2a282a511379c9f789daad1e60356b0e0266aac45c58428f6f03c7 | 38da51a480fb131757854a7787f426e57efd78c9f22d4ca9abdd0b5943f39492 |
| S2 | /root/AAA/registries/CAPABILITY_INDEX.json (server=aforge subset) | federation index, aforge rows only | 122 | aa39ecd5cc2a282a511379c9f789daad1e60356b0e0266aac45c58428f6f03c7 | 5ca6c2c00dd40505858c900cd4bf67b9305671122210d8c3a3a0b30f5131c42b (whole file, 343 tools, 14 servers) |
| S3 | /root/A-FORGE/a_think/affordances.yaml | semantic affordance cards | 132 | 46afff6926ddf53e81028bce5c360946d86c25bcb5bd36758cf7f8f6bcf8801e | cbe99c455e7c9924540d8d79e79ed63bdbb28c2d922ca719413969d117de1190 |
| S4 | /root/A-FORGE/tools_sot.yaml | DEPRECATED (own header says 59 days stale) | 51 | 438ab153f872492d95b30973fafe5582dda4e802f82a951abb69a0085c0476aa | 22c669915c5c3c8182cf548631da504ccaae806f433c05213720ac05b4ec5f27 |
| S5 | /root/A-FORGE/contracts/tools.yaml | stale (last verified 2026-05-19); NOT forge_* named | 0 forge_* | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty set) | 71fbb2511827dad21df7c220146d6db7d7086a83bfac046960593b15e3109b61 |
| S6 | /root/AAA/federation/organs.yaml (a-forge public_tools) | curated public subset, not full registry | 4 | 80ce3d27842ed64ebe7e9f7faf966f9bc549f1f2449e378157b44d6d2244b9ee | dcb707c4d770639deb7ba7f2991bc9c971c26364de35c762ead2a84c0c641344 |

S6 public_tools = forge_browser_navigate, forge_fetch, forge_search, forge_web_extract.

### Agreement / disagreement

- **S1 == S2 EXACTLY** (both 122, both sha256 aa39ecd5…). The live A-FORGE registry
  snapshot and the federation index's aforge subset are byte-identical as name sets. [OBS]
- **S3 (affordances.yaml, 132) is a strict superset of the live 122.** The 10 extra are
  design-surface cards with no live registration: forge_calendar, forge_cool_pattern,
  forge_docs_lookup, forge_drive, forge_gmail, forge_minimax_search, forge_proxy_call,
  forge_research, forge_sheets, forge_whoami. This is NOT drift — affordances.yaml's own
  header (lines 1-6) warns it is "broader design surface" and instructs "compare to live
  tools/list before claiming tool exists." intersection(S1,S3)=122, only_in_S1=0. [OBS]
- **S4 (tools_sot.yaml) is deprecated and wrong** — 51 tools, self-flagged stale, 38 overlap
  with live, 84 live tools absent from it, 13 of its entries absent from live. Do not use. [OBS]
- **S5 (contracts/tools.yaml) uses a different naming scheme entirely** (ReadFileTool,
  WriteFileTool, … — TypeScript class names, not forge_* MCP tool ids). It is a stale
  2026-05-19 contract doc, not the live surface. Zero forge_* names. [OBS]
- **S6 (organs.yaml) is a deliberate 4-tool public projection**, not a registry. [OBS]

Canonical choice: **S1 == S2 == the live truth (122)**. Fingerprint aa39ecd5… is the
boot-drift key.

## 2. Probe 4 — live MCP health

Probed read-only (curl GET /health only; no tools/list mutation, no tool calls).

| Item | Value | Class |
|---|---|---|
| A-FORGE API port | 7071 (LISTEN 127.0.0.1, node pid 758985) | OBS |
| A-FORGE MCP port | 7072 (LISTEN 127.0.0.1, node pid 759843) | OBS |
| GET :7071/health | HTTP 200 | OBS |
| GET :7072/mcp | HTTP 200 | OBS |
| GET :7072/health | HTTP 200 | OBS |
| Ports also mirrored | tailscaled DNAT on 100.64.0.2 + fd7a:115c:a1e0::2 (7071/7072/8088/3001) | OBS |

### Health payload (selected fields, verbatim) [OBS]

```json
{
  "ok": true,
  "degraded_mode": false,
  "service": "A-FORGE-sense",
  "version": "v2026.07.24",
  "federation_schema_version": "2.0.0",
  "tool_count": 122,
  "tools_loaded": 122,
  "profile": "enterprise",
  "authority_ceiling": "777_FORGE",
  "identity_hash": "fb3c88911e6c3a53e91863ec0cb1908621d9083ea2fdea0503f84d19a003d5c4",
  "deployed_commit": "f4a0a33",
  "source_commit": "f4a0a33",
  "deployment_drift": false,
  "status": "healthy"
}
```

- **surface_hash / contract_epoch:** ABSENT from the health payload. Full key set has no
  surface_hash and no contract_epoch key. The self-reported identity_hash above is the
  closest analogue. Health payload keys observed: act_mutation_gate, apex_scalars,
  apex_scalars_policy, authority_ceiling, contract_url, degraded_mode, deployed_commit,
  deployment_drift, federation_geometry, federation_schema_version, final_authority,
  freshness, identity, identity_hash, ok, owner_summary, profile, service, source_commit,
  status, timestamp, tool_count, tools_loaded, version. [OBS]
- **tool_count:122 == tools_loaded:122** — internal consistency, agrees with S1/S2. [OBS]

### A-FORGE server status: **ALIVE** (both API :7071 and MCP :7072 healthy, 200/200/200) [OBS]

## 3. Source-truth chain for the WARGA projection (verified on disk)

The redirect asked for a GENERATOR spec (C_warga = C_live ∩ C_affordance ∩ C_kernel ∩
C_authority), not a hand-map. That generator ALREADY EXISTS (shipped by peer FI-008,
commit b339b494). This section records the verified source chain so the fingerprint can
be regenerated and audited. I do NOT re-author the spec; I document what is on disk.

| Set | Read from | sha256(bytes) | Count | Verified |
|---|---|---|---|---|
| C_live | /root/AAA/registries/CAPABILITY_INDEX.json (server=aforge) — the generator's live input | 5ca6c2c00dd40505858c900cd4bf67b9305671122210d8c3a3a0b30f5131c42b | 122 | verified-on-disk |
| C_affordance | /root/A-FORGE/a_think/affordances.yaml | cbe99c455e7c9924540d8d79e79ed63bdbb28c2d922ca719413969d117de1190 | 132 | verified-on-disk |
| C_kernel (ABI) | /root/arifOS/docs/KERNEL_CAPABILITY_ABI.md (8 stable verbs) | cf1c7f6dd55c7fd61901514a0a84038d4811c684759eea8ca9862d58e1e802c8 | 8 | verified-on-disk |
| C_kernel (bindings) | /root/arifOS/static/manifest/tools.json (capability_id per verb) | 28caffc433013a236dceb45278517eb541402dd64e7fff4bc55b61d28b700434 | 8 capability_id | verified-on-disk |
| verb schema (cold) | /root/AAA/registries/AFORGE_VERB_SCHEMA.json | 40ef03c576a56e20533dbf48771a1031f562d39736751420e6b9e9e0c0ded2f7 | 7 verbs | verified-on-disk |
| generator | /root/AAA/scripts/aforge_warga_view_generator.py | 505a3e99d9e88281763e37ec09b399d7f92ba477d0641594f70fc0f91049f14a | 274 lines | verified-on-disk |
| projection output | /root/AAA/state/aforge/warga-capabilities.json | 2ba53183df00d1cf1765ce0d70324d18a237fd2ee2723739e4376099759762bc | 7 verbs, 44 candidates | verified-on-disk |

The 8 kernel ABI verbs (C_kernel), verbatim from KERNEL_CAPABILITY_ABI.md [OBS]:
session.bind(arif_init), reality.observe(arif_observe), cognition.think(arif_think),
intent.route(arif_route), memory.govern(arif_memory), authority.judge(arif_judge),
action.execute(arif_forge), history.seal(arif_seal).

## 4. DRIFT findings

**DRIFT-1 — registry_fingerprint scope conflation. Severity: MEDIUM.**
/root/AAA/state/aforge/competency/FI-008-kimi-code.json records
`registry_fingerprint: 16e78b27fbe030f7801d2b109cf5cf4cca7195ef07227c28bb80779b4e81a1b6`.
That value is the **federation-wide CAPABILITY_INDEX digest** (all 343 tools, 14 servers),
NOT an A-FORGE-scoped hash. Expected: an A-FORGE-scoped fingerprint (aa39ecd5… or the
aforge-subset sha). Observed: whole-federation digest. A boot sequence diffing this value
would reload the A-FORGE map whenever ANY of the 14 servers changes, not only when A-FORGE
changes. [OBS — provenance: FI-008-kimi-code.json field registry_fingerprint vs
CAPABILITY_INDEX.json .digest, both hashed above.]

**DRIFT-2 — projection drops 78 of 122 live tools. Severity: MEDIUM.**
The generator's map_affordance_class_to_verb() maps only 44 of 122 live aforge tools to a
verb; 78 return None (reason MAPS_NONE, not missing-affordance) and are silently dropped
from the projection. Per-verb: forge_inspect=26, forge_run=17, forge_control=1, and ZERO
candidates for forge_plan / forge_change / forge_verify / forge_extend. Dropped sample
includes the entire browser_* family and all apex_* tools. Expected: every live tool routes
to exactly one of the 7 verbs, or is explicitly UNCLASSIFIED. Observed: 64% of the live
surface is invisible to the WARGA projection, and 4 of 7 verbs are empty. This is a
coverage gap in a heuristic classifier, not a data gap — the affordance cards exist. [DER —
ran the shipped generator's mapping function over the 122 live names.]

**DRIFT-3 — concurrent-writer churn during probe. Severity: LOW (methodology note).**
/root/AAA/ROOT_AGENT_CONFIG.yaml changed hash mid-session: e9d98851cf353a88056578e5ac78de617e5430a55c3f218a333b15aeb7004ba9
→ 99c44616e176bcac9ff45288b7bd4a9b1d005a5f4601eb0a4af61ef4697ee9a1. AAA git HEAD advanced
b339b494 → 6e3bc8c2 while I probed. All config hashes in THIS receipt are the latest read.
A-FORGE source repo HEAD (237a7999) is also ahead of runtime (f4a0a336) — see receipt 2. [OBS]

**DRIFT-4 — A-FORGE source ahead of runtime by 25 commits, touching tool surface. Severity: MEDIUM.**
/root/A-FORGE HEAD = 237a7999f0aa2a817899efe6bf5f1e89a704e9af. Runtime /opt/a-forge/app
.git_commit = f4a0a336. Health self-reports deployed_commit=f4a0a33, source_commit=f4a0a33,
deployment_drift:false — but that "source_commit" is the RUNTIME's view, not the repo HEAD.
`git merge-base --is-ancestor f4a0a336 237a7999` = not-ancestor (divergent or rewritten).
25 commits between them; the delta touches a_think/affordances.yaml,
src/interfaces/mcp/policyTools.ts, parallelTools.ts, runtimeVerify.ts, surfaceAuditTools.ts,
shell/forgeShell.ts, shell/arifSeal.ts. So the on-disk affordances.yaml I hashed (cbe99c…)
may not equal what the f4a0a33 runtime loaded. Health's deployment_drift:false is measuring
runtime-vs-runtime, not repo-HEAD-vs-runtime. [OBS + DER]

## 5. Reproduce

```
sha256sum /root/A-FORGE/.registry/fingerprints.json
python3 - <<'PY'
import json,hashlib
d=json.load(open('/root/A-FORGE/.registry/fingerprints.json'))
n=sorted(set(d['tools']))
print(len(n), hashlib.sha256(('\n'.join(n)+'\n').encode()).hexdigest())
PY
curl -sS http://127.0.0.1:7071/health | python3 -c "import sys,json;print(json.load(sys.stdin)['tool_count'])"
```
Expected: 122 aa39ecd5cc2a282a511379c9f789daad1e60356b0e0266aac45c58428f6f03c7 / 122.

— 555-ASI Φ SENSE, Lane 555b. Read-only. No production artifact mutated.
