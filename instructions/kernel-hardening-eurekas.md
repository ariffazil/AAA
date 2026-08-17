# 4 Eureka Margin Discoveries — Kernel Hardening Sphere

> **Canon:** `/root/arifOS/arifosmcp/runtime/kernel_hardening_eurekas.py`  
> **Ratified:** 2026-08-16 by F13 SOVEREIGN  
> **Doctrine:** *Kecerdasan = Fluid (boleh berubah & berkembang). Kernel = Rigid (berpaut pada bukti & batas).*

---

### 1. Eureka Kemerosotan Model (The Silent Model Demotion Trap)

- **Masalah:** Bila fallback model berlaku daripada model besar (contoh: Claude Opus/Sonnet, Gemini Pro) ke model kecil (contoh: Qwen-7B, Ollama), model kecil sering hilang disiplin perlembagaan walaupun HTTP memulangkan 200 OK.
- **Pengerasan Kernel:**
  - Pasang **Model Capability Floor Gate** (`clamp_model_autonomy`).
  - Model dengan skor kapasiti $< 0.80$ dihadkan secara automatik ke **T0 (Read-Only / OBSERVE)**.
  - Model kecil dilarang memegang token mutasi T1/T2 tanpa sokongan model penilai bebas.

---

### 2. Eureka Firewall Parut Manusia (The Anti-Weaponization Scar Firewall)

- **Masalah:** Naratif emosi dan trauma peribadi manusia (H5) yang disimpan secara mentah dalam Vector DB terdedah kepada serangan *prompt injection* luar untuk memanipulasi emosi.
- **Pengerasan Kernel:**
  - Pasang **One-Way Metabolic Digest** (`ingest_h5_scar_digest`).
  - Teks mentah disimpan eksklusif dalam `/root/.private/scars/` (`chmod 0600`).
  - Memori operasi agen hanya menerima *Constraint Invariant Rule* (contoh: *"Jangan sentuh kawasan X kerana ada parut H5"*), bukan naratif peribadi mentah.

---

### 3. Eureka Kunci Zaman Merkle (Merkle Epoch Lock / Anti-Race Condition)

- **Masalah:** Apabila pelbagai agen serentak (OpenCode, Hermes, Kimi, Codex) mencadangkan mutasi serentak, mutasi boleh bertindih dan mencetuskan *race condition*.
- **Pengerasan Kernel:**
  - Dalam transaksi pengedap `arif_seal`, semak `parent_seal_hash` (`check_merkle_epoch_lock`).
  - Jika kepala VAULT999 telah bergerak ke hadapan semasa agen berfikir, serahan ditolak dengan kod `STALE_EPOCH_RETRY`.
  - Agen dipaksa untuk menjalankan `arif_observe` semula sebelum boleh meneruskan `arif_judge`.

```
  Transaction Request
           ↓
  parent_seal_hash check
           ↓
  STALE_EPOCH_RETRY? YES → arif_observe restart
           ↓
  current epoch valid? → arif_judge proceed
           ↓
  SEAL appended to VAULT999
```

---

### 4. Eureka Resit Berbalik (Proof-Before-Prompt Doctrine)

- **Masalah:** Agen yang sering bertanya *"Boleh saya teruskan?"* membebankan perhatian manusia (*Attention Tax*). Sebaliknya, agen yang bertindak tanpa kawalan menjadi bahaya.
- **Pengerasan Kernel:**
  - **Hukum Resit Sebelum Tindakan:** Agen tidak meminta izin melalui kata-kata kosong. Agen membina skrip rollback dan melepaskan ujian hijau terlebih dahulu.
  - **T0/T1:** Auto-laksana dengan resit bukti (*Auto-proceed with receipt*).
  - **T2:** Umumkan resit rollback dengan tetingkap veto 10 saat (*Announce in 10s, proceed if no veto*).
  - **T3 (F13 mutlak):** Tahan di `888_HOLD` dengan laporan diagnostik lengkap untuk keputusan manusia.

```
  Action Requested
           ↓
  Can I proceed? (self-assessment)
           ↓
  T0/T1: Auto-proceed (with receipt)
           ↓
  T2: Announce in 10s, proceed if no veto
           ↓
  T3: Human decision required (F13)
           ↓
  Execute with receipt
```
