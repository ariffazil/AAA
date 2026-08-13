# LIVE ORPHAN SKILL INVENTORY — 2026-08-13
# [OBS] dijana oleh Hermes (probe before act). Bukan angka audit, angka disk.
# SOT: /root/AAA/skills (sovereign core). Setiap skill hidup di luar = orphan/SPOF.
# DITEMPA BUKAN DIBERI

## COUNTS (nama-skill unik, live disk)
- AAA            : 194 (termasuk 2 promote baru: image-text-editing, aaa-image-editing)
- Hermes ~/.hermes: 418 (271 bukan di AAA)
- Hermes profile : 436 (262 bukan di AAA — profile aaa-hermes)
- Kimi           : 254 (67 bukan di AAA)
- OpenClaw       : 4
- OpenCode       : 5

## PROMOTED HARI INI (SPOF dihapus)
- image-text-editing  : ~/.hermes/skills/creative/ → AAA/skills/creative/ ✅
- aaa-image-editing   : profiles/aaa-hermes/skills/media/ → AAA/skills/media/ ✅
  (NOTA: audit kata path ~/.hermes/skills/media/ — SALAH. Lokasi sebenar profile aaa-hermes. Nama betul, path salah)

## LAPISAN YANG PATUT TIDAK FEDERATED (jangan buang, jangan promote — profile/agent-specific)
Hidup di profile kerana ia identity/agent/multiuser-specific — mempromote = mencemarkan F13/multiuser isolation:
- hermes-multi-user-isolation, hermes-multi-human-lanes, person-lane-operator, syedos-ops,
  nasi-lemak-*, syedos, hermes-persona-alignment
- (Senarai penuh 262 profile-orphan dalam output terminal)

## ORPHAN TULEN (Hermes-only yang patut dipusatkan — subset)
Ini jati umum yang sepatutnya di KANON, bukan tersekat di Hermes. Kategori:
- Infra/federation: federation-* (25+), arifos-* (15+), agentic-infrastructure-ops, caddy-reverse-proxy
- Doktrin/governance: constitutional-floors, claim-receipt-discipline, governance-patterns, three-agent-flow-doctrine
- Kemampuan umum: ocr, pdf, docx, xlsx, maps, notion, obsidian, powerpoint, google-workspace
- Domain Arif: petronas-petros-shell-dispute, energy-upstream-org-benchmarking, rasa-derita, crisis-shadow-decode

## LANGKAH SETERUSNYA (jangan jalankan tanpa 888)
1. Pilih subset orphan tulin untuk promote (perlu keputusan: mana federated vs mana profile-only)
2. Symlink OpenClaw/OpenCode → AAA/skills (HOLD per directive)
3. Registry V3 reconcile guna live-disk count ini (bukan 95, bukan 168)