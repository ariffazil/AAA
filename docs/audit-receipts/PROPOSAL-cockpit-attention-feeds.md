# PROPOSAL — Cockpit attention feeds (HOLD items visible to Arif)

**Status:** PROPOSAL · not yet implemented
**Proposed by:** FI-005 (audit follow-up)
**Date:** 2026-10-03
**Severity:** LOW (cosmetic) — current banner tidak salah, hanya kurang ketat

## Latar Belakang

Audit AUDIT-20261003-claim-0fb01f87 mendapati 4 item metabolism TIDAK OPTIMAL yang **tidak dipaparkan** di cockpit:
- `g = 0.39` → PATHOLOGICAL
- `w3 = 0.74` → CAUTION
- `hermes-asi` → STUCK
- `grok-build` → HELD FOSSILIZED
- `chron` → CAUTION

Banner cockpit: "Semua Tenang & Lancar (Zero Attention Leak)" — **betul dari sudut keputusan F13**, tetapi **Ujian Syed** ("jika tanya kenapa g=0.39, takkan jawapan permukaan") mungkin gagal.

## Cadangan Minimum (≤ 1 turn implementation)

Patch 1 baris di `state/federation-cockpit.html` line 273:

```diff
- deskDesc.textContent = 'Tiada keputusan berisiko tinggi atau sekatan yang memerlukan campur tangan Arif hari ini. Ejen beroperasi secara automatik di bawah sempadan AMANAH dan perlembagaan F1-F13.';
+ deskDesc.innerHTML = `Tiada keputusan F13-binary yang menunggu hari ini.<br>
+   <small style="color:var(--muted)">
+     📊 Metabolism: FQ ${meta.quotient?.toFixed(2)} · g=${(meta.g_value||0).toFixed(2)} ${meta.g_band||''} · w³=${(meta.w3_value||0).toFixed(2)} ${meta.w3_band||''}<br>
+     ${(meta.cautions||[]).map(c=>`⚠ ${c.actor}: ${c.verdict}`).join(' · ')}
+   </small>`;
```

Backend: tambah `meta.g_value`, `meta.g_band`, `meta.w3_value`, `meta.w3_band`, `meta.cautions` ke JSON yang dihantar dari `/api/cockpit/v1/state` (atau equivalent).

## Keputusan Diperlukan (Arif, binari)

| Pilihan | Kesan |
|---|---|
| **A. Tambah sekarang** | Satu turn patch. Permukaan lebih jujur. Ujian Syed lulus lebih ketat. Backend work ~30 minit lagi. |
| **B. Tunda — 'Semua Tenang' sudah cukup untuk sekarang** | Tiada kerja. Arif akan dapati isu hanya jika probe sendiri. |
| **C. Tambah, tapi hanya untuk CAUTION ke atas, bukan STUCK/FOSSILIZED** | Kompromi: cairkan tetapi tak sembunyi. |

## Auto-Seal Doctrine

Per Auto-Seal: konstituasi = 1 perkataan Arif. Ini bukan konstituasi, ini adalah publisiti UI. **Warga CADANG + STAGE. Jadi final hanya dengan "SAH" Arif atau F13 eksplisit.**

## Status

STAGED · awaiting Arif's "SAH" or other F13 order. **Tiada mutasi ke source code.** Patch preview di atas belum diapply.
