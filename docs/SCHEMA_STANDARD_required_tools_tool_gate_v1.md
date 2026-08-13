# SCHEMA STANDARD — required_tools & tool_gate
## Orthogonal Routing Contract v1.0.0 · 2026-08-13 · Hermes · DITEMPA BUKAN DIBERI
> Kontrak ini rigid & deterministik. Compass baca field ini SEBAGAI-KOD, bukan sebagai teks bebas.
> Rajah: TOOL_INVENTORY.jsonl (sumber nama tool) + tool-registry.json (sumber id organ)
> Status: DRAFT-untuk-approve → 888 approve → inject ke 10 pilot.

## 1. tool_gate — ENUM TERTUTUP (2 nilai sahaja)
| Nilai   | Maksud | Kelakuan Compass |
|---------|--------|------------------|
| permissive | Skill boleh guna required_tools + subset OBSERVE pasif | lepaskan allowlist luas |
| strict     | ONLY required_tools. Tiada tool luar. | lepaskan allowlist minima |
FAIL-CLOSED: tiada nilai / invalid → JANGAN default longgar. → strict (OBSERVE_ONLY minima).

Allowed values: ['permissive', 'strict']
Default (tiada field): strict (fail-closed).
Validator regex: ^(strict|permissive)$

## 2. required_tools — ARRAY OF STRINGS, match TEPAT ke nama tool
- Setiap elemen MESTI match sama dengan `tool` name dalam TOOL_INVENTORY.jsonl (atau id dalam tool-registry.json).
- Tiada alias, tiada fuzzy, tiada wildcard. Compass verification = exact set membership.
- Empty array [] = tiada aktuator khusus (skill doktrin tulen).
- Format YAML:
  required_tools:
    - forge_fetch
    - browser_exec
- Validator: setiap elemen ≠ kosong, tiada regex char, mesti wujud dalam registry.

## 3. Integrasi dengan field sedia ada (jangan pecahkan)
| Field sedia ada | Peranan | Hubung dengan required_tools |
|-----------------|---------|------------------------------|
| dependencies.mcp_servers | organ MCP yang diperlukan (aforge/arifos/geox...) | SUPERSET — mcp_servers adalah server, required_tools adalah tool dalam server |
| risk_tier | low/medium/high | Gate PRINSIP: high risk → tool_gate wajib strict |
| floor_scope [F1,F2...] | floor constitutional | WARNAI: floor ketat → tool_gate strict |
| capability_tier | 1-5 | Boleh mula: >3 → permissive dibenar |
| autonomy_tier T0-T3 | kuasa auto | T2+ TIDAK dibenar bersama tool_gate=permissive (T3 mutation perlu F13) |

## 4. Contoh PILOT (10 fail) — cadangan nilai
| Skill | tool_gate | required_tools |
|-------|-----------|----------------|
| ocr | strict | [vision_analyze, arif_observe] |
| ocr-and-documents | strict | [vision_analyze, forge_fetch] |
| image-text-editing | strict | [image_generate, vision_analyze] |
| aaa-image-editing | strict | [image_generate, vision_analyze] |
| AGI-agentic-web | permissive | [forge_fetch, forge_search] |
| AGI-plan-dag | strict | [terminal] |
| FORGE-mcp-lifeguard | strict | [forge_health_check, forge_mcp_* ] |
| ASI-drift-watch | permissive | [arif_observe, forge_fetch] |
| observe-ground | strict | [arif_observe, arif_think] |
| memory-manage | strict | [arif_memory] |

## 5. Compass Layer output (fail-closed)
```
input : {skill_id, agent_lane, agent_autonomy_tier}
steps :
  1. baca frontmatter skill (cari required_tools + tool_gate)
  2. tool_gate missing/invalid → strict (fail-closed)
  3. high risk_tier dan tool_gate != strict → paksa strict  (F1 over-ride)
  4. verify setiap required_tools terhadap TOOL_INVENTORY.jsonl exact match
  5. tool tak jumpa dalam registry → DROP + warn (tiada leak)
  6. hasil = allowlist tool yang DIHALAL untuk skill ini
output : {"skill": id, "gate": strict|permissive, "tools": [nama-sah], "denied": [...], "default": "fail_closed"}
net : dari 62 tools → 2-6 tools sahaja disuntik ke system prompt skill itu
```

## 6. Kenapa field TIDAK boleh nama lain
- required_tools fixed (bukan tools/needs) → Compass baca SAMA dari semua 179 fail, satu source-of-truth.
- tool_gate fixed enum → tiada interpretasi. Kalau ada fail guna `gate: open`, ia IGNORE (invalid) → fail-closed.
- Nama tool dalam required_tools mesti match TOOL_INVENTORY.jsonl — tiada "forge_fetch()" atau "forge fetch".

*Kontrak v1.0.0. 888 approve → pilot inject. DRAFT.*