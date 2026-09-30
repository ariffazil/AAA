# AAA Agent × GEOX MCP Wiring Map (2026-09-29)

**For:** all AAA agents (hermes, fi-003, claude, kimi, opencode, copilot, cursor, antigravity, gemini, forge, shared)
**Purpose:** explain how each agent family can discover, route, and use the GEOX MCP surface
**Status:** PRODUCED; awaiting F13 ratification

---

## 1. GEOX MCP endpoints (the link)

| Endpoint | Use |
|---|---|
| **`https://geox.arif-fazil.com/mcp`** | **Public URL** — production GEOX MCP server (HTTPS, public-facing) |
| `http://127.0.0.1:8081/mcp` | Localhost (VPS-bound, port 8081, systemd `geox-mcp.service`) |
| `http://127.0.0.1:8081/health` | Health check (already wired in `/root/AAA/AGENTS-AUTONOMY.md` §2 federation-reality probe) |
| `https://geox.arif-fazil.com/.well-known/agent-card.json` | Agent Card (A2A discovery) |
| `https://geox.arif-fazil.com/.well-known/agent.json` | Agent metadata (identity, provider) |

The MCP link you asked for is **`https://geox.arif-fazil.com/mcp`**.

---

## 2. GEOX MCP tool surface (canonical, live)

Per the live `/health` endpoint (snapshot at 09:14:49 UTC, 2026-09-29):
- **26 canonical tools** registered (live-witnessed, zero drift)
- `authority_ceiling: 555_COMPUTE_ONLY`
- `domain_law: NATURAL_LAW`

**9 forge additions (this session, branch `forge/amplitude-gates-a-family`):**

| Tool | evidence_class | claim_ceiling | Used for |
|---|---|---|---|
| `geox_seismic_polarity_register.v1` | OBSERVATION | REGISTRATION | Declare polarity/phase for a volume or trace |
| `geox_seismic_artifact_get.v1` | OBSERVATION | READ | Retrieve any artifact by `geox://...` URI |
| `geox_seismic_attribute_compute.v1` | OBSERVATION | HYPOTHESIS | Compute 13 L0 attributes (envelope, GST dip, coherence, curvature, spectral, etc.) |
| `geox_seismic_display_trace.v1` | DISPLAY_PROXY | GEOMETRY | PNG → Polyline artifacts (color-mask + Chaikin smoothing) |
| `geox_seismic_age_assign.v1` | OBSERVATION | HYPOTHESIS | Assign Morley 2023 ages; thickness gate > 400 ms → HOLD |
| `geox_seismic_render_publication.v1` | DISPLAY_PROXY | GEOMETRY | Deterministic image render |
| `geox_seismic_alternative_interpret.v1` | DISPLAY_PROXY | HYPOTHESIS | ≥3 hypothesis cards, all HOLD |
| `geox_seismic_volume_register.v1` | OBSERVATION | REGISTRATION | SEG-Y Rev 2 → VolumeManifest (segyio-backed) |
| `geox_seismic_horizon_track.v1` | OBSERVATION | HYPOTHESIS | Seed-based 3D horizon tracker → SurfaceMesh |
| `geox_seismic_display_spectral_character.v1` | DISPLAY_PROXY | CHARACTER (cannot promote) | Ordinal zone table; no absolute Hz; refuses PETRONAS on VPS |

**5 forge resources (resources are discoverable via MCP `resources/read`):**

| URI | Content |
|---|---|
| `geox://conventions/seismic_display` | Display conventions (palettes, dash styles, line widths) |
| `geox://stratigraphy/nw_sabah/surfaces` | DRU/LIU/UIU/SRU/H-III/TOP_IVC ages + citations (Morley 2023) |
| `geox://discriminators/north_sabah/diapir_thrust_miiec` | 3-way discriminator set with falsifiers |
| `geox://survey_segments/registry` | Survey-segment registry (mandatory before display_spectral_character) |
| `geox://conventions/colormaps/registry` | Colormap registration |

---

## 3. AAA agent → GEOX routing map

| Agent family | Role | How to call GEOX |
|---|---|---|
| **hermes** | Witness / classify / route (does NOT judge per `/root/.hermes/AGENTS.md`) | Use `mcp__hermes__hermes_claim_validate` and `hermes_handoff_package(claims, target_organ="GEOX")` |
| **fi-003** (555-ASI) | Verify; 13 consecutive exec_no_verify=HELD (autonomous loop guard) | Use `mcp__hermes__*` for evidence; route through hermes-gateway |
| **claude** (Copilot-like) | Synthetic-data generation; prototype scripts | Direct MCP client to `https://geox.arif-fazil.com/mcp` |
| **kimi** (this session) | 333-AGI role; forge executor | `mcp__geox__geox_seismic_*` tools via local MCP |
| **opencode** | Code editor; review | Same as kimi |
| **copilot** | Synthetic-data prototype scripts (per Madon 2022 re-interpretation) | Reference Copilot fixtures at `tests/fixtures/copilot_prototypes/` |
| **cursor** | Code editor | Direct MCP |
| **antigravity** | Antigravity-cli; brain artifacts at `/root/.arifos/agents/gemini/AAA/antigravity-cli/brain/` | See existing GEOX artifacts there |
| **gemini** | Brain artifacts (per antigravity branch above) | See existing GEOX knowledge-graph artifacts |
| **forge** | A-FORGE executor | `mcp__aforge__*`; receives GEOX outputs as evidence |
| **shared** | Federation-wide shared state | Per `/root/AAA/dist/` |

---

## 4. Routing pattern (canonical, 2026-09-29)

Per `/root/AAA/AGENTS-AUTONOMY.md` §2 (federation-reality probe):

```python
GEOX = "https://geox.arif-fazil.com/mcp"   # GEOX public endpoint
# Per-agent discovery: agent-card.json at /.well-known/
# Per-claim workflow: agent calls GEOX tool → claim is hermes_claim_validated → AGI flow
```

**5-step pattern for any AAA agent:**

1. **Discover:** GET `https://geox.arif-fazil.com/.well-known/agent-card.json`
2. **Initialize:** POST to `/mcp` with `initialize` JSON-RPC
3. **Tools/list:** GET `/mcp/tools/list` to see all 26 canonical tools (incl. 9 forge additions after merge)
4. **Call:** POST `/mcp` with `tools/call {name, arguments}`
5. **Receipt:** `mcp__hermes__hermes_claim_validate(claim=...)` for witness-layer validation

---

## 5. Authority gates (must respect)

| Authority | Action |
|---|---|
| `555_COMPUTE_ONLY` (GEOX) | Computation, evidence emission only — **NO mutation, NO judgment** |
| `arifOS JUDGE` (888-APEX) | Verdict, evaluation |
| `arifOS SEAL` (F13) | Final ratification — **HUMAN ONLY** |
| `A-FORGE ACT` | Production mutation |
| Classification gate (in display_spectral_character.v1) | **Refuses PETRONAS data on VPS** |

---

## 6. What I did NOT do (per sovereign directive; explicit HOLD gates)

- ❌ Did NOT modify AAA agent configs in place (would require sovereign ratification)
- ❌ Did NOT trigger GEOX production restart (requires A-FORGE apply)
- ❌ Did NOT push to remote (DONE earlier in this session — branch forge/amplitude-gates-a-family at HEAD 18181be8)
- ❌ Did NOT merge forge branch to main (HOLD on F13 SAH)
- ❌ Did NOT SEAL the session (arif_seal blocked on authority band + constitutional chain)

---

DITEMPA BUKAN DIBERI ⚒️
