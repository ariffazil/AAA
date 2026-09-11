# Memory Promotion Gate — Witness ≠ Seal ≠ Memory

> **Status:** F13_RATIFIED_CHAT (2026-09-11)
> **Origin:** Arif — forged from the autonomous-memory-seal thread. Bug exposed: *autonomous memory seal tanpa autonomous memory judgment menghasilkan memory inflation.*
> **Applies to:** ALL agents in arifOS federation. Every memory write. No exception.
> **Supersedes:** `MEMORY_ENGINEERING_SPEC_v2.md` §4.2 `archive_to_memory` criteria (confidence ≥ 0.7 + witness_count ≥ 1 = memory — that IS the bug).

---

## The Bug

Current shape:

```text
Observe → Interesting → SEAL → Store → Vault → Memory
```

The flaw:

```text
Interesting ≠ Memory-worthy
```

Vault membesar. Memory membesar. Doctrine membesar. Tetapi runtime belum semestinya bertambah baik.

## Three Layers — Fungsi Berbeza

Banyak sistem campur tiga benda ini. Padahal fungsi berbeza.

| Layer | Fungsi | Kos |
|---|---|---|
| **Witness** | Catat bahawa sesuatu berlaku | Murah |
| **Seal** | Attestation: "aku yakin benda ini berlaku" | Murah |
| **Memory** | Primitive yang mengubah future judgement | Mahal |

```text
SEAL ≠ MEMORY
SEAL = attestation sahaja
```

Kesilapan biasa: treat `SEAL = MEMORY` (simpan selama-lamanya). Seal murah. Memory mahal.

## Canonical Flow

```text
Observe
↓
Witness
↓
Seal
↓
Promotion Review
      │
      ├─ Primitive baru?
      │      YES → Memory
      │
      └─ NO → Evidence Ledger / Compress / Discard
```

## The Four Gates (mandatori sebelum SETIAP memory write)

**Gate A — Derivation**
```text
Boleh derive daripada primitive sedia ada?
YES → Reject memory
```

**Gate B — Deletion Test**
```text
Jika memory ini dipadam esok, adakah capability hilang?
NO → Reject memory
```

**Gate C — Decision Test**
```text
Adakah ini mengubah future decision?
NO → Witness only
```

**Gate D — Novelty Class**
```text
Contoh baharu atau primitive baharu?
Contoh baharu  → Witness
Primitive baharu → Memory candidate
```

Semua gate mesti lulus. Satu gagal → witness / compress / discard.

## Target Metric

```text
Hari ini:  100 insights → 80 memory writes
Future:    100 insights → 100 witnesses → ≤5 memory promotions
```

Yang tinggal dalam memory hanya perkara yang benar-benar mengubah judgement.

## Operational Binding

- Semua memory-write path lalu gate yang sama: `arif_memory` store, skill seal, doctrine fragment, agent_state, session carry-forward.
- **Default = witness.** Memory adalah exception, bukan default.
- VAULT999 seal TIDAK automatik menjadi memory. Seal = attestation; promotion review berasingan.
- Primitive baharu mesti dapat nama sebelum disimpan (ontology before memory — first law).
- Gagal gate → compress ke evidence ledger. Bukan simpan penuh. Bukan buang senyap.
- Setelah classifier ini matang, memory akan menjaga dirinya sendiri.

## Compression

> Jangan bina `autonomous seal memory`. Bina `autonomous promotion gate`.

> Problem utama federation bukan kekurangan seal. Problem utama: **apa yang layak melepasi sempadan Witness → Memory.**

DITEMPA BUKAN DIBERI ⚒️
