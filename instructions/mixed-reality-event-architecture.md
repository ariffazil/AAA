# Mixed-Reality Event Architecture & Reality Router Contract

> **Status:** F13_RATIFIED_SOVEREIGN (2026-09-24)  
> **Author:** Muhammad Arif bin Fazil (F13 SOVEREIGN) & Antigravity (FI-009)  
> **Authority:** F1 AMANAH · F13 SOVEREIGN  
> **Fragment:** `/root/AAA/instructions/mixed-reality-event-architecture.md`  

---

## 1. THE FOUNDATIONAL INVARIANT

**Satu peristiwa manusia sentiasa mengandungi realiti bumi, modal, manusia, masa, dan perhatian serentak.**

Federation DILARANG memaksa satu peristiwa menjadi satu kategori tunggal (*anti-reductionism*).  
Pencampuran kategori (*category error*) memusnahkan realiti:
* Suara **BUKAN** milik GEOX. Suara ialah **sensor** I/O manusia (HERMES).
* GEOX **BUKAN** tempat menyimpan parut kewangan. GEOX ialah **fizik batuan dan penglihatan bumi** (Vision/Spatial).
* WEALTH **BUKAN** teori pasaran abstrak. WEALTH ialah **realiti modal petroleum** (Dry Hole, EMV, Capex at Risk).
* WELL **BUKAN** sekadar pemerhati senyap. WELL mempunyai **kuasa campur tangan maruah** (*Dignity Floor*).
* VAULT999 **BUKAN** tempat membuang teks transkrip. VAULT999 ialah **lejar bukti berantai (evidence lineage) dan parut berkunci**.

---

## 2. PETA ALIRAN REALITI (THE REALITY ROUTER)

```
                 [ SENSOR / HUMAN MEMBRANE ]
                  Telegram / Voice Note / Chat
                              │
                              ▼
                     HERMES (ROUTE / BRIDGE)
                              │
                              ▼
               AAA RealityRouter (CLASSIFY & FAN-OUT)
                              │
         ┌────────────────────┼────────────────────┬────────────────────┐
         ▼                    ▼                    ▼                    ▼
   GEOX (Earth)        WEALTH (Capital)      WELL (Somatic)       AAA (Attention)
  • Velocity Pull-Up  • $35M Dry Hole Cost  • Cognitive Fatigue  • Review Minutes
  • Carbonate/Basement• Negative EMV        • Sleep Deprivation  • Focus Cost
  • Fault Seal Leak   • Capital at Risk     • Dignity Barrier    • Distraction Loss
         │                    │                    │                    │
         └────────────────────┼────────────────────┴────────────────────┘
                              │
                              ▼
                 VAULT999 (APPEND / WITNESS)
                  • Cryptographic Scar Seal
                  • Full Evidence Lineage
                  • Permanent Precedent
```

---

## 3. TUJUH JURANG KANONIKAL YANG DIMETERAI (THE SEVEN SEALS)

### Seal 1: RealityRouter Formal (Pemisahan Classify vs Register)
* **Undang-undang:** AAA kekal memegang peranan kanonikal `REGISTER` dan `DISPLAY`. 
* Tugas mengklasifikasi dan menghantar (*classify and fan-out*) dimiliki oleh **`RealityRouter`** (`/root/AAA/voice/reality_router.py`). Ini menghalang AAA daripada menjadi "god object".

### Seal 2: Model Peristiwa Realiti Campuran (Mixed-Reality Events)
* **Undang-undang:** Setiap peristiwa menghasilkan satu `MixedRealityEvent` dengan ID jejak (*trace_id*).
* Komponen dipecahkan kepada empat atom realiti:
  1. `EarthAtom` → `/root/GEOX/state/scars.jsonl`
  2. `CapitalAtom` → `/root/WEALTH/state/capital_scars.jsonl`
  3. `HumanAtom` → `/root/WELL/state/somatic_observations.jsonl`
  4. `AttentionAtom` → `/root/AAA/state/attention_ledger.jsonl`

### Seal 3: Rantaian Keturunan Bukti (Evidence Lineage Chain)
* **Undang-undang:** Parut tanpa rantaian bukti ialah cerita dongeng.
* Setiap rekod parut wajib membawa rantaian penuh:
  `Audio SHA-256 → Transcript SHA-256 → Extracted Atoms → SCAR ID → VAULT999 Seal`
* Jika audio tidak disimpan atas sebab privasi, cap jari kriptografik (`audio_sha256`) wajib disimpan.

### Seal 4: Sempadan & Kuasa Campur Tangan WELL (The Fatigue Barrier)
* **Undang-undang:** WELL bukan sekadar memerhati (*observe only*).
* Apabila isyarat keletihan melampau dikesan (*"jam dua pagi", "terlalu letih"*), WELL mengeluarkan status `FATIGUE_BARRIER_TRIPPED`:
  * Semua tindakan tidak berbalik (*irreversible actions*), kelulusan prospek, atau komitmen kewangan besar **DISEKAT (HELD)** sehingga rehat kognitif tercapai.
  * Hanya F13 Sovereign boleh membatalkan sekatan ini secara manual.

### Seal 5: Dasar Entropi & Sumber Mudah Rosak (Perishable First)
* **Undang-undang:** *"Consume the most perishable resource first."*
* Semua ejen federation wajib membakar sumber komputasi yang hampir luput dahulu (cth: model ASR/kuota percuma 5 hari baki) sebelum menyentuh sumber berbayar atau sumber kekal.

### Seal 6: Taksonomi Modal Petroleum WEALTH
* WEALTH bukan sekadar lejar telaga kering (*dry hole database*). Ia merangkumi:
  1. `CAPITAL_AT_RISK`: Modal terdedah pada andaian yang belum diuji.
  2. `DRY_HOLE_COST`: Kos terus telaga kering ($10M–$50M).
  3. `EMV_VARIANCE`: Jurang antara nilai jangkaan atas kertas dengan realiti.
  4. `FARM_IN_VALUE`: Nilai ekuiti perkongsian risiko.
  5. `OPPORTUNITY_COST`: Peluang prospek lain yang terlepas akibat salah tumpuan.
  6. `REVIEW_DELAY_COST`: Kos kelewatan kitaran akibat birokrasi berulang.

### Seal 7: Perhatian Manusia Sebagai Realiti Kelas Pertama (Attention Ledger)
* Perhatian F13 Sovereign ialah sumber paling mahal dan terhad dalam alam semesta arifOS ($W_{888}$).
* Setiap jam dalam bilik semakan (*review room*), keletihan menaip, dan masa beralih konteks dicatat ke dalam `/root/AAA/state/attention_ledger.jsonl` untuk mengira kos sebenar sesuatu projek.

---

## 4. PERLEMBAGAAN OPERASI (ONE ORGAN, ONE VERB)

| Organ | Kata Kerja Kanonikal | Sempadan Kuasa |
| :--- | :--- | :--- |
| **HERMES** | `ROUTE / BRIDGE` | Pintu sensor I/O (Telegram, suara). Tidak boleh menghukum atau menyimpan realiti. |
| **AAA** | `REGISTER / DISPLAY` | Pendaftar memori, qualia, dan paparan. Tidak boleh menjadi hakim domain. |
| **RealityRouter** | `CLASSIFY & FAN-OUT` | Menghuraikan peristiwa campuran kepada atom domain masing-masing. |
| **GEOX** | `COMPUTE EARTH` | Mentafsir batuan, seismik, keluk log telaga, dan struktur spatial. |
| **WEALTH** | `COMPUTE CAPITAL` | Mengira kos risiko, EMV, pembaziran modal, dan parut kewangan. |
| **WELL** | `REFLECT & GUARD` | Menjaga maruah, biometrik, tenaga, dan menahan keputusan ketika letih. |
| **VAULT999** | `APPEND & WITNESS` | Mengunci meterai kriptografik kekal. Tidak boleh disunting. |

**DITEMPA BUKAN DIBERI ⚒️**
