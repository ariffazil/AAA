# ROADMAP: SUBSTRATE HARMONIZATION & HARDENING (WAVE 2)
**For**: Next AGY CLI / Warga Federation Agents  
**Authority**: F13 Constitutional Scaffolding  
**Date**: 2026-10-10  

---

## 1. SUMMARY OF WAVE 1 ACHIEVEMENTS (GROUND TRUTH)
1. **T01 MCP Connector Gate**: Lulus 100% dari vantage KVM4 ke KVM8 (`http://100.64.0.2:8088`). Handshake `initialize` dan `tools/list` mengesahkan 8 alat kanonikal kernel wujud dan boleh dipanggil.
2. **T05 FRAME Conservation Gate**: Pepijat agregat diperbaiki di `/root/AAA/federation/frame/src/frame_organ/probe.py`. Invarian `healthy + degraded + down == total` kini dipelihara (`assert` aktif). Output semasa: 10/10 organ terpulihara.
3. **@arifOS_bot (Gateway 3)**:
   - Pepijat pertembungan import `URLRequest` dibaiki.
   - Fasa 1 aktif: Kod bahaya `forge_shell()` dibuang, perbualan teks dialirkan terus ke otak LLM FED (`:4000`), kawalan keselamatan kedaulatan F13 mengehadkan akses kepada Arif (`267378578`).
4. **F1 Degradation Root Cause**: Dikenal pasti berpunca daripada 7 ejen latar belakang yang tertahan dalam arifFlow (`quotient=0.8113`, `Hold` actors).
5. **KVM8 Disk (83%)**: 24.4 GB cache selamat dikenal pasti (`/root/.cache/huggingface`, `/root/.cache/uv`, `/root/.npm`, dll.).

---

## 2. SCAFFOLDING THE REMAINING SUBSTRATE TO NEXT AGY CLI AGENTS

### Task 1: Pelepasan Sekatan F1 arifFlow (T1 - Reversible)
* **Pemerhatian**: F1 gagal kerana nisbah verifikasi/pelaksanaan arifFlow rendah pada aktor tertentu (`morning-briefing`, `codex`, `qwen-code`).
* **Tindakan Seterusnya**: Picu kitaran metabolik arifFlow melalui `POST http://127.0.0.1:7073/cycle` atau jalankan kitaran verifikasi bagi aktor yang tertahan untuk menaikkan semula skor FQ ke `>= 0.90`.

### Task 2: Pembersihan Disk KVM8 Berjadual (T2 - Sovereign Consent)
* **Sasaran**: Bebaskan ruang daripada 83% kepada bawah 70%.
* **Direktori Sasaran**:
  - `rm -rf /root/.cache/huggingface/*` (~14 GB)
  - `rm -rf /root/.cache/uv/*` (~3.9 GB)
  - `npm cache clean --force` (~2.7 GB)
* **Kekangan**: Jangan sentuh `/root/arifOS/VAULT999/` atau `/root/AAA/canon/`.

### Task 3: Kriptografi Ed25519 & RFC 8785 Canonicalization (T1.5)
* **Pemerhatian Semasa**: 1,346 entri di `SEALED_EVENTS.jsonl` tidak mempunyai `actor_signature` berasingan (hanya `actor_id`).
* **Tindakan Seterusnya**: Pasang modul Ed25519 standard bagi menandatangani event JSON mengikut RFC 8785 (JCS) sebelum diserahkan kepada `arif_seal`.

### Task 4: Pemulihan Telemetri WELL (L13 Seal Blocker)
* **Pemerhatian Semasa**: Panggilan `arif_seal` mengembalikan `HOLD` kerana kegagalan lantai L13: `WELL telemetry unavailable (well_score=None, backend_status=PIPELINE_FEEDING)`.
* **Tindakan Seterusnya**: Semak servis WELL di port 18083 (`systemctl status well.service`). Pastikan saluran data biometrik/vitaliti selesai proses pipeline feeding supaya `well_score` dapat dikira dan dilaporkan ke kernel.

### Task 5: Penggabungan PR #205 (AAA Control Plane)
* **Status**: PR #205 dibuka oleh KVM4 untuk menetapkan kesemua 9 organ ke alamat mesh `100.64.0.2`.
* **Tindakan Seterusnya**: Kaji semula perbezaan 9 baris dan gabungkan PR ke cawangan `main` selepas verifikasi.

---
*DITEMPA BUKAN DIBERI ⚒️*
