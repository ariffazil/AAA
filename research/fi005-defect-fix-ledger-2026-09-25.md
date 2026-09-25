# FI-005 Defect Fix Ledger — 2026-09-25

> **Arahan F13:** "fix this for codex as well" · **Pelaksana:** FI-003 (Qwen Code) · **Sumber:** self-audit FI-005 `/root/AAA/research/FI-005-SELF-AUDIT-2026-09-25.md`
> **Kaedah:** probe dahulu, kemudian perbaiki punca umbi. Backup boot surface sebelum edit: `/root/.codex/AGENTS.md.bak-20260925-fi003-witnessfix`

## Keputusan kecacatan

| Defect | Punca umbi (diprobes) | Penetapan | Status |
|---|---|---|---|
| **A — metadata drift (26-vs-14)** | Angka "26" TERTULIS dalam boot surface sendiri: `/root/.codex/AGENTS.md` "MCP servers (26 in config.toml)" — Codex memetik dari fail boot-nya, bukan memorinya | Baris boot diganti dengan penunjuk SOT + disiplin probe; runtime v0.154.0→v0.156.1 (lapuk, cacat kelas sama) turut diperbaiki | **DIBAIKI pada sumber** |
| **C — reachability tak diuji** | Tiada probe langsung pernah dijalankan | Probe hidup 2026-09-25: **14/14 server menjawab** — 200 (aforge, arifos, geox), 400=UP (fed, frame, hermes-mcp), 405=UP (firecrawl, wealth, well), stdio PRESENT (arifflow, brave-search, context7, fetch, github). Sifar conn-refused/timeout | **DIUJI — dinaik taraf daripada "not-exercised" kepada OBSERVED** |
| **B — percanggahan naratif sahaja** | Enjin berstruktur TIDAK berwayar adalah SALAH — `hermes-mcp` SUDAH berwayar (config.toml L181); tiada mandat menggunakannya | Mandat kontrak §3: percanggahan load-bearing → `hermes_contradiction_scan`, hasil berstruktur dikeluarkan | **DIBAiki (mandat)** — pematuhan masih aras-arahan |
| **D — tiada resit berstruktur** | Tiada kontrak `{trace_id, actor, claim, state, evidence, supersedes}` pada permukaan boot FI-005 | Kontrak "STRUCTURED WITNESS CONTRACT" ditulis dalam `/root/.codex/AGENTS.md` (4 peraturan mengikat) | **DIADDRES (aras arahan)** — penguatkuasaan aras harness kekal TERBUKA |

## Pembetulan kendiri semasa kerja (kejujuran F2)

Skrip probe pertama saya melaporkan "11/14" — **salah klasifikasi oleh skrip sendiri**: HTTP 400/405 dikira sebagai turun. Sebenarnya pelayan MENJAWAB (bentuk permintaan salah). Dibetulkan kepada 14/14. Contoh hidup kelas kecacatan yang sedang dibaiki — nombor salah hampir memasuki ledger.

## Residual (terbuka, memerlukan kuasa/kerja berasingan)

1. **Promosi Banner SOT ke canon** (`/root/AAA/canon/`): pokok kanon dikunci `chattr +i` (lsattr disahkan 2026-09-25) → laluan `canon-mutate` + undian F13. Buat masa ini SOT tinggal di `/root/AAA/research/codex-banners/` dan wajib dirujuk dari permukaan boot.
2. **Penguatkuasaan aras harness Defect D**: auto-stamp `trace_id` memerlukan pembungkus wrapper CLI atau sokongan hook aras atas Codex — melebihi skop aras doktrin. Didaftarkan, belum ditutup.
3. **Spawn-level MCP probe**: probe hari ini = aras kehadiran/HTTP. Pelancaran penuh setiap pelayan stdio + senarai alat = kerja berasingan (L05 agent yang dihantar sedang mengaudit wayar hooks — permukaan berbeza).
4. `config.toml` TIDAK disentuh, trust registry TIDAK disentuh (F13-only), tiada push.

## Bukti

- Backup: `/root/.codex/AGENTS.md.bak-20260925-fi003-witnessfix`
- Boot surface selepas: `/root/.codex/AGENTS.md` (91 baris; §STRUCTURED WITNESS CONTRACT)
- Banner SOT: `/root/AAA/research/codex-banners/CODEX-FEDERATION-BANNER-SOT.toml` (14 server, senarai nama disemak semula = padan dengan probe)
- Self-audit asal: `/root/AAA/research/FI-005-SELF-AUDIT-2026-09-25.md`

DITEMPA BUKAN DIBERI ⚒️
