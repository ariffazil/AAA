# ORTHOGONAL ORGANIZATION — Skills × Tools × Agents
## Reka Bentuk Keputusan · 2026-08-13 · Hermes · DITEMPA BUKAN DIBERI
> Status: PROPOSAL (T1.5). Bukan mutation. Grounded pada probe live disk.
> Soalan: macam mana organise skills, tools, agents secara orthogonal, based on current constraints.

## 1. APA MAKSUD "ORTHOGONAL" DI SINI
Tiga paksi BEBAS (tak bertindih, tak saling mewarisi):
- SKILL  = DOKRIN (SOP/declaratif) → "bagaimana cara" — terletak dalam SKILL.md
- TOOL   = AKTUATOR (API/eksekutabel) → "dengan apa" — terletak dalam TOOL_INVENTORY / MCP registry
- AGENT  = PELAKSANA (lane+boundary) → "siapa, dengan kuasa apa" — agent-cards (333/555/777/888)

Orthogonality = sebuah skill TIDAK kolektif bawa tool-state; sebuah tool TIDAK menyimpan doktrin;
sebuah agent TIDAK menganggap skill. Yang mengikat ialah ROUTER (compass layer) secara eksplisit,
bukan dengan pengedaran tersirat dalam setiap fail.

Kesilapan kegemini: mencampur dua paksi (skill bawa tool, agent tak ada boundary) → bukan orthogonal.
Kesilapan kita sekarang: TREE777 (topologi) cuba jadi skills dir (penyimpanan) — arrow putus sebab dua peranan ditimbun.

## 2. STRUKTUR YANG BETUL (3 lapis, 1 router)
```
   LAPIS PENYIMPANAN (storage)          LAPIS PENGKATALOGAN (discovery)      LAPIS PELAKSANAAN (execution)
   ───────────────────────              ──────────────────────                ──────────────────────
   /root/AAA/skills/  (194 SKILL.md)  → TREE777 (topologi/DAG URI)          → AGENT (lane terpilih)
   /root/tool-registry (62 tools)    → /root/forge_work/.../TOOL_INVENTORY → A-FORGE (mutasi)
                                        /root/arifOS tool-registry.json
                                       ↓
                              COMPASS LAYER (pagar fail-closed)
                              baca frontmatter SKILL.md → hasilkan
                              per-agent tool allowlist → suntik ke system prompt
```
Prinsip: penyimpanan ≠ katalog ≠ eksekusi. Tiga paksi, satu router.

## 3. BINDING VIA FRONTMATTER (Laluan A — disahkan)
Setiap SKILL.md membawa metadata kontrak:
```yaml
id: ocr-processing
required_tools: [forge_fetch, browser_exec]   # aktuator yang dibenarkan
tool_gate: strict|permissive                    # strict=allowlist sahaja
risk_tier: moderate                             # dah wujud (145 skill)
floor_scope: [F1, F2, F7]                       # dah wujud (144 skill)
capability_tier: 3                              # dah wujud (185 skill)
autonomy_tier: T1                               # dah wujud
```
Kontrak ini BUKAN "skill pegang tool-state" mutlak – ia DEKLARASI yang compass baca untuk
menghasilkan allowlist. Skill tak panggil tool; AGENT panggil tool, agent DIPANDU compass.

## 4. COMPASS LAYER (pagar fail-closed) — REKA BENTUK
```
input : SKILL.md yang agent nak guna (contoh: ocr-processing)
logic : baca frontmatter → required_tools + tool_gate
hasil :
  - gate = strict  → ONLY tools dalam required_tools
  - gate = permissive → tools dalam required_tools + subset observe (forge_fetch, arif_observe)
  - TIADA field   → FAIL-CLOSED → strict, default subset OBSERVE_ONLY sahaja
net hasil: dari 62 tools → 2-6 tools relevan disuntik. ΔS < 0 besar.

Sifat wajib (F1):
  - fail-closed (default ketat, bukan longgar)
  - tak menukar tool definition sebenar (baca sahaja, tak mutate)
  - output deterministik (tiada LLM dalam gate)
```

## 5. MEMBETULKAN TREE777 — BUKAN TUKAR PATH, SAMBUNG ARROW BETUL
Dua pilihan wiring (pilih satu, kedua-duanya reversible):
- OPSI-A: Ubah `_list_wiki_skills()` dalam tree777.py untuk walk `/root/AAA/skills` structure
          (`{name}/SKILL.md`) — 1 fungsi, padan topologi sebenar. TAPI mutasi arifOS source (rutin deployment).
- OPSI-B (cadang): Simpan TREE777 sebagai discovery layer PISAH — genarate `/root/AAA/skills_index.json`
          dari `find /root/AAA/skills -name SKILL.md` (satu skrip jana), dan TREE777 baca index itu.
          Tak sentuh resolver lama, tak ubah source arifOS. Menambah build step, bukan mengubah enjin.
Opsi-B lebih "sambung anak panah, jangan tambah L7" — ia menambah SCRIPT yang wiring index,
bukan mutate tree777.py. Kesannya: `tree777://skills/{category}/{name}` resolve ke SKILL.md sebenar
tanpa menukar struktur penyimpanan AAA/skills.

## 6. KESAN AGENT (bagaimana mereka minum)
- OpenClaw/OpenCode/Kimi = baca via TREE777 MCP resource ATAU `skills.external_dirs` point ke AAA/skills
  (read-only gravity, BUKAN symlink — elak permission bleed)
- Setiap agent dapat allowlist dari compass (bukan 62 tools pukal)
- Agent card declare skills; compass validate skill→tool contract ada

## 7. METRIK KEJAYAAN (bukan benchmark, E2E nyata)
1. Satu task 'ocr' → compass keluarkan {forge_fetch, browser_exec} sahaja, bukan 62 → token drop = %
2. `tree777://skills/...` resolve ke SKILL.md sebenar (194), bukan 0
3. OpenClaw baca TREE777 → nampak skill AAA (bukan 4 silo)
4. Sifar amaran F13 baru

## 8. URUTAN PELAKSANAAN (fasa, reversible)
- F1: Ops-B index script (jana skills_index.json dari find) — T1, tiada mutasi arifOS
- F2: Compass layer (baca frontmatter → allowlist, fail-closed) — T1/T2, skrip baharu
- F3: TREE777 baca index (ops-B wiring) — T2, test resolve
- F4: Wire agent external_dirs → AAA (Hermes/Kimi/OpenClaw/OpenCode) — T2
- F5: Registry V3 auto-gen dari live index — T2 (HOLD sampai F1-F4 bukti)

## KEPUTUSAN YANG DIPERLUKAN 888
- Sahkan Opsi-B (index script + TREE777 baca index) berbanding Opsi-A (mutate tree777.py source).
  Cadang: OPSI-B — kerana ia sambungkan arrow tanpa ubah enjin arifOS, paling reversible, paling selari
  dengan doktrin "jangan tambah L7, sambungkan anak panah".

*Proposal. F13 masih jawab. DITEMPA BUKAN DIBERI.*