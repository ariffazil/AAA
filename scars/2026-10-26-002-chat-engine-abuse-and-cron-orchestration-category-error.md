# SCAR: CHAT ENGINE ABUSE & CRON ORCHESTRATION CATEGORY ERROR

> **Scar ID:** SCAR-2026-10-26-002  
> **Forged:** 2026-10-26 20:20 MYT  
> **Sovereign Authority:** F13 ARIF  
> **Status:** RATIFIED CONSTITUTIONAL SCAR  
> **Core Maxim:** Hermes = Think · arifFlow = Flow · A-FORGE = Execute · VAULT999 = Witness  
> **EUREKA:** Control the runtime, not the model.

---

## 1. THE OBSERVED PATHOLOGY (WHAT BROKE)

A scheduled cron job in Hermes (`Agent report digest 351387f88502`, and sibling jobs `ALPHA-ZEN 2 3e40c50f0ca2`, `muse-memory-upkeep 742c31132184`) repeatedly failed with:
`RuntimeError: No reply: the turn stopped while a tool result was still pending and the model produced no follow-up text.`
Or collapsed into refusal sinks when arifOS kernel gate-brakes tripped.

**Root Cause:**
Hermes treated **scheduled work as a conversation**.
Scheduled work is NOT a conversation problem; it is an **orchestration problem**.

Instead of executing a 5-second deterministic Python check:
`check file hash -> compare checksum -> emit receipt if changed -> exit(0)`
The system forced a conversational LLM into a multi-turn discursive loop:
`reason -> reflect -> tool search (across 454 MCP tools) -> select tool -> execute tool -> parse result -> write response -> close turn`
This burnt tokens, caused timeout/turn exhaustion, and flooded the human with error notifications.

---

## 2. THE FOUR CONSTITUTIONAL SCARS

### SCAR 1: CHAT ENGINE ABUSE
**Definition:** Menggunakan conversational intelligence untuk deterministic automation.
* **Sesuai untuk LLM (Hermes):** Analisis emel, brainstorm, audit architecture, writing, dialog manusia, meaning synthesis.
* **Tidak sesuai untuk LLM (Chat Abuse):** Hash file, check disk, ping URL, compare JSON, monitor sijil, watch cron status.
* **Ketetapan:** Semua deterministic scheduled monitoring mesti jadi **arifFlow DAG**, bukan Hermes chat prompt.

### SCAR 2: TOOL DISCOVERY EXPLOSION
**Definition:** Mengimbas dan menilai katalog alatan pada waktu laksana untuk tugasan yang sudah tetap.
* Known capability != discovered capability.
* Scheduled execution sepatutnya: `Capability ID -> Function -> Execute -> Receipt`.
* Haram melakukan lazy discovery ke atas 454 alatan MCP setiap pusingan.

### SCAR 3: NO REALITY DELTA FILTER
**Definition:** Menjana hingar dan amaran kerana model menganggap setiap kebangkitan adalah kewajipan bercakap.
* `Reality unchanged` adalah output yang sah dan elegan.
* Jika Delta S = 0 (tiada perubahan realiti), keluar bersih (exit 0) tanpa mengeluarkan naratif. Hanya beri amaran jika ada delta yang disaksikan.

### SCAR 4: LANGUAGE USED AS EXECUTION BUS
**Definition:** Menggunakan prosa bahasa tabii sebagai wire protocol untuk orkestrasi dalaman sistem-ke-sistem.
* Bahasa simpan untuk: `Human <-> System`.
* Orkestrasi dalaman (`System <-> System`) wajib menggunakan kontrak berstruktur dan bertaip (JSON/DAG/Protobuf).

---

## 3. PEMBAHAGIAN KUASA KEDAULATAN FEDERATION

```text
┌────────────────────────────────────────────────────────┐
│  HERMES   =  THINK    (Human Interface, Meaning, RASA) │
│  arifFlow =  FLOW     (Orchestration, Typed DAGs, Crons)│
│  A-FORGE  =  EXECUTE  (Hands, Fast Mutation, Builds)   │
│  VAULT999 =  WITNESS  (Immutable Receipts, Seals)      │
└────────────────────────────────────────────────────────┘
```

**Kesimpulan:**
Model tak rosak. Architecture yang suruh model buat kerja cron yang rosak.
Control the runtime, not the model.
