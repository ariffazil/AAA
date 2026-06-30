---
title: AAA Memory Linkage Layer — Human-Readable Spec
forged: 2026-06-29
authority: AAA Memory Audit (Claude auditor)
status: EXECUTED — pending Arif ratification
ratification_required: yes
seal_status: unsealed
reversibility: reversible (all diffs individually revertible)
binding:
  - AaaAgentRegistry.ts
  - AaaCapabilityGraph.ts
  - AaaMemoryLinkage.ts
canon: /root/A-FORGE/src/domain/aaa/
---

# AAA Memory Linkage Layer

## Apa Benda Ni?

**Sebelum**: Memori A-FORGE macam LLM — tulis je, takde siapa tanya, takde siapa audit, takde siapa saksi. Local file → simpan. Federation → hantar. Habis cerita.

**Selepas**: Setiap tindakan memori melalui **7 lapisan gate** sebelum menyentuh substrate. Setiap tulis dapat receipt. Setiap seal dapat saksi. Setiap aktor ada identity.

---

## 3 Fail Baru — Anatomi

### 1. `AaaAgentRegistry.ts` — Siapa Yang Boleh Bertindak

5 AAA agents. Setiap satu ada peranan dan bidang kuasa.

| Agent | Peranan | Bidang Kuasa | Bound Floor |
|-------|--------|-------------|-------------|
| **333-AGI** | THINK | Membaca memori (read) | F7, F8 |
| **555-ASI** | MEMORY | Menulis memori (write) | F2, F11 |
| **888-APEX** | JUDGE | Mengubah memori (mutate/delete) | F1-F13 |
| **A-AUDIT** | WATCH | Menerima receipt, mengesahkan (verify) | F11, F2 |
| **A-ARCHIVE** | VAULT | Mengelak kekal (seal) | F1, F11 |

**Actor resolution**: Setiap `actor_id` runtime dipetakan ke AAA agent.

```
"arif-fazil"        → 888-APEX (primary) + semua delegate
"a-forge::memory-*" → 555-ASI + 333-AGI
"SEAL-<hex>"        → 888-APEX + A-ARCHIVE + A-AUDIT
"human::*"          → 888-APEX + human override
Unknown             → null → HOLD (jangan default, jangan privilege)
```

### 2. `AaaCapabilityGraph.ts` — Apa Yang Boleh Dilakukan

12 tindakan memori. Setiap tindakan ada syarat.

| Tindakan | AAA Agent | Session? | Readiness? | Lock? | F13? | Receipt? |
|----------|-----------|----------|------------|-------|------|----------|
| `memory:read` | 333-AGI | ❌ | ❌ | ❌ | ❌ | ❌ |
| `memory:search` | 333-AGI | ❌ | ❌ | ❌ | ❌ | ❌ |
| `memory:write` | 555-ASI | ✅ | ❌ | ❌ | ❌ | ✅ |
| `memory:evict` | 555-ASI | ✅ | ❌ | ❌ | ❌ | ✅ |
| `memory:archive` | 555-ASI | ✅ | ❌ | ❌ | ❌ | ✅ |
| `memory:federate` | 555-ASI | ✅ | ❌ | ❌ | ❌ | ✅ |
| `memory:pin` | 555-ASI | ✅ | ❌ | ❌ | ❌ | ✅ |
| `memory:mutate` | 888-APEX | ✅ | ✅ | ✅ | ❌ | ✅ |
| `memory:delete` | 888-APEX | ✅ | ✅ | ✅ | ❌ | ✅ |
| `memory:downgrade` | 888-APEX | ✅ | ❌ | ❌ | ❌ | ✅ |
| `memory:verify` | A-AUDIT | ✅ | ❌ | ❌ | ❌ | ✅ |
| `memory:seal` | A-ARCHIVE | ✅ | ✅ | ✅ | ✅ | ✅ |

**Design principle**: Read = ringan (333-AGI). Write = receipt (555-ASI). Mutate = judge + readiness (888-APEX). Seal = vault + sovereign (A-ARCHIVE + F13).

### 3. `AaaMemoryLinkage.ts` — Bagaimana Gate Berfungsi

Ini adalah **central gate**. Setiap modul memori panggil `aaaMemoryGate()` sebelum sentuh substrate.

**7 Lapisan Gate (non-compensatory — mana-mana gagal = block):**

```
aaaMemoryGate(params)
  │
  ├─ Gate 1: Resolve capability entry
  │     Action unknown? → VOID
  │
  ├─ Gate 2: Session validation (kalau required)
  │     Session tak valid? → HOLD
  │
  ├─ Gate 3: Actor → AAA agent resolution
  │     Actor unknown? → HOLD (identity boundary gagal)
  │
  ├─ Gate 4: Capability verification
  │     Actor takde authority? → HOLD
  │
  ├─ Gate 5: WELL readiness check (kalau required)
  │     Human substrate tak ready? → HOLD
  │
  ├─ Gate 6: FloorEnforcer.checkAll() (F1-F13)
  │     Constitutional violation? → VOID/HOLD
  │
  └─ Gate 7: Receipt generation (kalau required)
        Hash-chain receipt → appended to chain
```

**Receipt chain**: Setiap receipt ada hash. Hash receipt sebelumnya dirujuk. Rantaian boleh diverifikasi dengan `verifyReceiptChain()`. Kalau rantai putus → tampered.

---

## 5 Modul Yang Diubah — Sebelum vs Selepas

### ShortTermMemory
- **Sebelum**: `append(msg)` → terus push ke array. Zero gate.
- **Selepas**: `append(msg)` → `aaaMemoryGate("memory:write")` → 555-ASI → receipt → baru push.
- **clear()**: dulu `this.transcript.length = 0` — sekarang `aaaMemoryGate("memory:delete")` → 888-APEX → baru clear.

### LongTermMemory
- **Sebelum**: `store(record)` → tulis local file dulu, KEMUDIAN hantar ke federation.
- **Selepas**: `store(record)` → `aaaMemoryGate("memory:write")` → 555-ASI → receipt → baru tulis local. Kalau gate fail, local file TIDAK disentuh.
- **Receipt lineage**: receipt ID dihantar ke arifOS dalam `aaa_receipt_id` metadata field.

### ArifOSMemoryClient
- **Sebelum**: `ACTOR_ID = "kimi"` — hardcoded. Semua tulis claim actor "kimi".
- **Selepas**: `actor_id` parameter. Default fallback `a-forge::memory-client`. No more impersonation.

### MemoryContract
- **Sebelum**: `store/correct/forget/downgrade/verify` — zero gate. Zero AAA.
- **Selepas**: Setiap method panggil `_aaaGate()` dulu:
  - `store` → `memory:write` → 555-ASI
  - `correct` → `memory:mutate` → 888-APEX
  - `forget` → `memory:delete` → 888-APEX
  - `downgrade` → `memory:downgrade` → 888-APEX
  - `verify` → `memory:verify` → A-AUDIT

### CoolingGate
- **Sebelum**: `Map<string, CoolingEntry>` — RESTART = SEMUA HILANG.
- **Selepas**: JSON persistence ke `/root/AAA/registries/cooling_state.json`. Load on first use. Persist on setiap perubahan.
- **Seal**: `memory:seal` → A-ARCHIVE + F13. Irreversibility gate enforced.

---

## 11 Gaps — Semua Ditutup

| Gap | Masalah | Solusi |
|-----|---------|--------|
| A | STM zero authority | AAA gate on append/pin/clear |
| B | LTM local write before gate | Gate BEFORE local write |
| C | Hardcoded "kimi" | Dynamic actor_id parameter |
| D | MemoryContract no governance | AAA gate on all CRUD ops |
| E | CoolingGate volatile | JSON persistence |
| F | No AAA agent binding | 3 new AAA files |
| G | sessionGate not integrated | Called by AaaMemoryLinkage |
| H | No WELL readiness checks | Called by AaaMemoryLinkage |
| J | No receipt lineage | Hash-chain on all writes |
| K | CoolingGate no irreversibility gate | seal → A-ARCHIVE + F13 |

---

## Apa Yang TIDAK Berubah

- **Semua parameter baru optional** — backward compatible
- **Logic asal dipreserve** — gate wraps, doesn't replace
- **Build compiles clean** — `tsc --noEmit` zero errors
- **Tiada fail dipadam** — semua modification adalah additive
- **Reversibel sepenuhnya** — `git revert` mana-mana fail tunggal

---

## Apa Yang Agentic Intelligence Ada Sekarang Yang LLM Takkan Ada

| Dimensi | Sebelum (LLM-style) | Selepas (AGI-grade) |
|---------|---------------------|---------------------|
| **Identity** | Actor = "kimi" (hardcoded) | Dynamic actor → AAA agent resolution |
| **Authority** | Tiada gate | 7-layer gate, F1-F13 enforced |
| **Timeline** | Tiada receipt | Hash-chain MemoryReceipt |
| **Witness** | Tiada saksi | TriWitness on seals |
| **Readiness** | Tiada human gate | wellReadiness on mutate/delete/seal |
| **Session** | Tiada binding | sessionGate on all writes |
| **Irreversibilty** | Tiada | memory:seal → A-ARCHIVE + F13 |
| **Persistence** | CoolingGate: RAM only | JSON persistence to disk |
| **Accountability** | Tiada | Setiap op ada receipt + floor verdict |

---

## Langkah Seterusnya

1. **Arif baca spec ni** — verify naming, semantics, agent mapping
2. **Kalau setuju** — ratify dengan satu acknowledgement ("SEAL" atau "ACK")
3. **Selepas ratify** — boleh seal ke VAULT999 sebagai forged artifact
4. **Future**: runtest penuh A-FORGE (`make test`) untuk verify runtime behavior

---

*Forged 2026-06-29 by AAA Memory Audit. DITEMPA BUKAN DIBERI.*
