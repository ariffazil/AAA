# GROK AAA NEXT INIT — GEOX ZEN + MCP APPS / GUI READY

> **Load this first.** Then zen SOT. Then act. Do not re-litigate sealed eureka.

```bash
set -a && source /root/.secrets/vault.env && set +a
curl -sf http://127.0.0.1:8081/health | python3 -m json.tool | head -25
cd /root/GEOX && git log --oneline -6 && git status -sb
# optional: restart if tip identity lag
# systemctl restart geox-mcp && sleep 2 && curl -sf :8081/health | python3 -m json.tool | head -15
```

**Session seal:** `/root/forge_work/2026-07-23/SESSION-SEAL-GEOX-EUREKA-MCP-APPS-2026-07-23T2112Z.md`  
**Zen SOT:** `/root/GEOX/docs/SEISMIC_SECTION_INTERPRET_ZEN.md`  
**Eureka note:** `/root/forge_work/2026-07-23/GEOX-EUREKA-ADJOUDICATION-MOAT-2026-07-23.md`  
**Tip expected:** `32af0d61` (or newer) · **31 tools** · healthy  

---

## Locked posture (NEVER reopen as narrative)

| Lock | Rule |
|------|------|
| Eureka | Adjudication moat > proposal theatre |
| Product input | **Section image first** · SEG-Y optional |
| Propose | Hostile witness · INT_SEISMIC / SPEC only |
| Local verdict | QUALIFIED_CANDIDATE max · preferred_hypothesis **null** |
| Seal | arifOS only · TRANSPORT_OK ≠ SEAL |
| Surface | **31 public** · 48 internal/ghost intentional |
| Tools | Modes on `geox_seismic_interpret` — no new public tools |

---

## DONE (do not re-forge)

- [x] B contract: modes, attribute_data+depth, honest HOLD, QUALIFIED_CANDIDATE  
- [x] C gates: K-DIP/THROW/DL/G2/RESTORE/VEL/GROWTH · UNMEASURED · receipt_hash  
- [x] Multi-hypothesis bundle · multi-KILL impossible pack  
- [x] Image-first classical_section (structure tensor + DP)  
- [x] Eureka doctrine in zen SOT  
- [x] MCP GUI PR1–3 (Well Witness path) · bridge polish `32af0d61`  
- [x] Focused tests green at finish-all (43)  

**Call shapes already live:**

```python
# PRIMARY product
await geox_seismic_interpret(mode="classical_section", image_path=".../section.jpg")
await geox_seismic_interpret(mode="interpret", image_path="...")
await geox_seismic_interpret(mode="structure_validate", framework={...})
await geox_falsify(claim_type="structural_fault", context={...})
```

---

## MISSION THIS SESSION — ZEN + MCP.APPS + GUI READY

### Goal

Package GEOX seismic + adjudication for **MCP Apps hosts** (Claude Desktop, MCPJam, ChatGPT Apps):  
self-contained UI resources, real HTML (no stubs), tool↔app binding, smoke checklist, one zen package map.

### P0 deliverables (ordered)

| ID | Task | Exit |
|----|------|------|
| **Z1** | Zen package map: list all seismic/gate/UI files + SOT pointers into one `forge_work/.../GEOX-MCP-APPS-PACKAGE-MAP.md` | single map |
| **G1** | Audit `GEOX_APPS` + `resources/read` for primary URIs ≥1KB real HTML | table PASS/FAIL |
| **G2** | Ensure `geox_seismic_interpret` + `geox_falsify` carry `_meta.ui.resourceUri` + `openai/outputTemplate` | tools/list proof |
| **G3** | **seismic_vision** app: section-image upload/path → call classical_section/interpret → draw candidates + gate panel | self-contained HTML |
| **G4** | **judge_console**: structural gate matrix (PASS/KILL/UNMEASURED + receipt) from falsify/structure_validate | host-readable |
| **G5** | Run `tests/test_mcp_apps_readiness.py` (+ fix until green) | green |
| **G6** | Smoke script: initialize → tools/list → resources/list → resources/read × primary → tools/call interpret + falsify | receipt in forge_work |
| **G7** | Package note: host how-to (MCPJam/Claude) one page | docs or forge_work |

### Parallel optional (moat only if GUI P0 green or blocked)

| ID | Task |
|----|------|
| C+ | Golden impossible packs; Barnett taper refine — **no new public tools** |

### Explicit non-goals

- New public MCP tools  
- Full SEG-Y required path  
- ONNX production weights / field ML claim  
- Promote ghost tools to public  
- Local SEAL · preferred_hypothesis from GEOX  
- Re-argue Bond/capability narrative without code  

---

## Skills to load

```
geox-grounding
observe-ground
FORGE-fastmcp
FORGE-mcp-gui
FORGE-visual-qa-w3
FORGE-precommit-review
FORGE-verify-runtime
asi-fabrication-prevention
apex_floor_check
verify-gate
```

---

## File pointers

| What | Path |
|------|------|
| Zen SOT | `GEOX/docs/SEISMIC_SECTION_INTERPRET_ZEN.md` |
| Gates K* | `GEOX/docs/SEISMIC_FAULT_PHYSICS_GATES_K_SPEC.md` |
| Gates G0–G10 | `GEOX/docs/SEISMIC_STRUCTURAL_VALIDATION_GATES_G0_G10.md` |
| Classical propose | `src/geox_mcp/tools/classical_section_propose.py` |
| Structure gates | `src/geox_mcp/tools/structure_gates/` |
| Interpret | `src/geox_mcp/tools/seismic_interpret.py` |
| MCP Apps bridge | `src/geox_mcp/tools/mcp_apps_bridge.py` |
| Apps HTML | `GEOX/apps/` · `static/gui/seismic_viewer/` |
| Readiness tests | `tests/test_mcp_apps_readiness.py` |
| Surface JSON | `GEOX_MCP_APPS_SURFACE.json` |

---

## First command (if no F13 special order)

> **Zen + package GEOX for MCP Apps GUI READY.**  
> Start G1 inventory of ui://geox/* resources + tool meta bindings.  
> Then G3 seismic_vision section-interpret loop (image-first classical).  
> Then G4 judge_console structural gates.  
> Green `test_mcp_apps_readiness`.  
> Receipt in forge_work. Do not add public tools. Do not claim autonomous interpreter.

---

## Done definition (this next session)

- [ ] Package map written  
- [ ] Primary UI URIs real HTML (no stubs)  
- [ ] interpret + falsify host-bound with resourceUri  
- [ ] seismic_vision shows section → candidates → gates (even if minimal)  
- [ ] readiness tests green  
- [ ] Host smoke receipt  
- [ ] Next INIT updated  

DITEMPA BUKAN DIBERI
