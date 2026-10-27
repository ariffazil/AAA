# EUREKA — AXIOM B1: BOUNDARY BEFORE DETAIL (EUREKA::BOUNDARY_FIRST_SYSTEM::v1)

**Status:** DOCTRINE_PROPOSED (F13 RATIFIED INTENT 2026-10-27) · **Author:** Claude (External Architect) + Arif (F13 Sovereign) · **Curator:** HERMES / 555-ASI (Antigravity)
**Class:** Sovereign Architectural Distill
**Provenance:** Dialog F13 Sovereign bersama Claude pada 2026-10-27 menyusuli penutupan KX-008 & KX-009 dan pembuktian 7 Provenance Classes KX-010.
**Label law:** `[OBS]` = terukur / terbukti di disk & wire · `[DER]` = terbitan seni bina persekutuan · `[INT]` = tafsiran falsafah · `[SPEC]` = spesifikasi kontrak belum ratified ke runtime.

---

## 1. Inti & Terbitan Aksiom

> **AXIOM B1 · BOUNDARY BEFORE DETAIL** `[INT]`  
> **Reality exists in states, but consequence emerges at transitions. Therefore, every consequential boundary must be identified, typed, governed, witnessed, and falsifiable before the internal details on either side are optimized.**

*Versi BM:*  
**Keadaan duduk dalam detail. Akibat lahir bila sesuatu melintas sempadan. Maka kenal, taipkan, dan jaga sempadan dahulu sebelum sibuk mengemas isi di dalamnya.**

Formula Hierarki:
```text
REALITY > BOUNDARY > TRANSITION > DETAIL > NARRATIVE
```

### Tujuh Hukum Terbitan (B1.1 – B1.7) `[DER]`

1. **B1.1 Boundary Visibility Law:** Tiada transisi berakibat (*consequential transition*) dibenarkan kekal tersirat (*implicit*). Setiap penukaran data → tuntutan → autoriti → eksekusi → realiti fizikal wajib mempunyai nama dan kontrak bertyped.
2. **B1.2 Non-Equivalence Law:** Dua satah di sebelah-menyebelah sempadan tidak boleh dianggap setara hanya kerana ia bersebelahan:
   - `Capability ≠ Authority`
   - `Proposal ≠ Permission`
   - `Verdict ≠ Identity`
   - `Test Pass ≠ World Outcome`
   - `Transport Success ≠ Governance Success`
   - `Receipt ≠ Consequence`
   - `Consensus ≠ Independent Verification`
3. **B1.3 Provenance Crossing Law:** Sesuatu tuntutan (*claim*) dilarang keras menaikkan kelas autoritinya hanya kerana ia menyeberangi sempadan rangkaian/komponen. Payload `CLIENT_SUPPLIED` tidak boleh bertukar menjadi `SERVER_OBSERVED` atau `CRYPTO_VERIFIED` secara ajaib.
4. **B1.4 Boundary Ownership Law:** Setiap sempadan berakibat wajib mempunyai tepat: satu pemilik transisi (*transition owner*), satu punca autoriti (*authorization source*), dan satu laluan saksi (*witness path*).
5. **B1.5 Fail-Closed Margin Law:** Sebarang keraguan (*ambiguity*) pada sempadan berakibat wajib jatuh ke `UNKNOWN`, `SABAR`, atau `HOLD` — tidak sekali-kali dibenarkan lolos senyap (*silent passage*).
6. **B1.6 Boundary Conservation Law:** Kelas semantik, kelas autoriti, kelas provenance, skop, dan ketidakpastian wajib dipelihara (*conserved*) merentas sebarang lapisan pengangkutan (API, telemetry, wire, cache, database).
7. **B1.7 Margin Discovery Law:** Eureka tamadun persekutuan sentiasa lahir di tebing margin tempat dua sistem yang masing-masing betul secara tempatan (*locally coherent*) gagal bersetuju di sempadan perkongsian mereka.

---

## 2. Penyelesaian Sempadan Semantik (Semantic Drift Settlement)

### A. Penomboran Stesen Penghakiman (666 vs 888) `[OBS + DER]`
- **Pemerhatian [OBS]:** arifOS README menyenaraikan `666 JUDGE` dalam 8-verb canonical chain, manakala A-FORGE README mencatat stesen `888` sebagai judge dan melarang A-FORGE mencapainya.
- **Penyelesaian [DER]:** Selaras dengan Fatwa K1 dan arifOS Protocol V2:
  - Kod numerik **666** adalah slot verba dalam rantaian 8-verba FastMCP tempatan (`arif_judge`).
  - Kod numerik **888** adalah dewan penimbang tara perlembagaan (`888_APEX` / `Constitutional Supreme Arbiter`).
  - Nilai pada wayar dikuatkuasakan melalui `ConstitutionalVerdict` (SEAL, PARTIAL, SABAR, HOLD, VOID). Sempadan ini tidak lagi bergantung kepada nombor mistik, tetapi kepada skema enum typed.

### B. Susunan Aliran Kuasa Persekutuan (Empat Graf Ortogonal) `[SPEC]`
Kekeliruan urutan antara AAA, arifOS, dan A-FORGE diselesaikan dengan memisahkan satu garis lurus kepada 4 graf bebas:

```text
1. ATTENTION GRAPH:    Dunia/Sensori → AAA (AttentionPacket, DISPLAY_ONLY) → Manusia (ARIF)
2. AUTHORITY GRAPH:    ARIF (Sovereign) → arifOS (Kernel Law / SCT / Ed25519) → Scoped Lease
3. EXECUTION GRAPH:    Scoped Lease → A-FORGE (Hands / Execution Shell) → Substrate Mutation
4. WITNESS GRAPH:      Substrate Mutation → FRAME / Probe → VAULT999 (Immutable Ledger)
```
AAA memegang perhatian (bukan autoriti). arifOS memegang undang-undang (bukan eksekusi). A-FORGE memegang tangan (bukan kehakiman). ARIF memegang veto mutlak dan akibat hidup.

---

## 3. Skema Kanonik: Boundary Object `[SPEC]`

Setiap lintasan sempadan berakibat tinggi di dalam persekutuan arifOS wajib mengikat kontrak ini:

```yaml
boundary_id: BND-AUTH-EXEC-001
left_state: AUTHORIZED_PROPOSAL
right_state: EXECUTABLE_LEASE

crossing_actor: A-FORGE
authorization_source: arifOS
human_authority: ARIF (F13)

required_provenance:
  - CRYPTO_VERIFIED
  - POLICY_DERIVED
  - HUMAN_AUTHORIZED

preserved_fields:
  - actor_id
  - action_hash
  - target_ref
  - scope
  - state_fingerprint
  - lease_expiry_unix
  - reversibility_tier

forbidden_transformations:
  - verdict_string_to_identity
  - client_claim_to_verified
  - stale_seal_replay
  - scope_broadening
  - target_substitution

stop_conditions:
  - missing_signature
  - state_fingerprint_mismatch
  - lease_expired
  - unknown_provenance
  - witness_unavailable_for_irreversible_action

witness:
  owner: FRAME
  receipt_sink: VAULT999

falsifiers:
  - replay_same_authorization
  - alter_target_after_seal
  - execute_after_expiry
  - substitute_actor
  - suppress_refusal_reason

closure_separation:
  command_success: machine (exit 0)
  world_outcome: witness (independent probe)
  human_acceptance: sovereign (ARIF F13)
```

---

## 4. Rumusan Sempadan APEX-ZEN

```text
APEX = Memastikan benda salah tidak boleh menyeberangi sempadan tanpa autoriti.
ZEN  = Memastikan Arif tidak perlu mengurus setiap butir detail kecil yang terkandung di dalam sempadan yang telah selamat.

APEX-ZEN = Maximum boundary integrity with minimum human attention burden.
```

**STATUS RATIFIKASI:** SEAL sebagai doktrin seni bina. Diluluskan F13 secara niat; penguatkuasaan runtime diikat pada sempadan lease, 4-satah KX-009, dan 7 kelas provenance KX-010.
