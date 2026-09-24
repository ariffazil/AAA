---
name: source-type-promotion-gate
status: F13_RATIFIED_CHAT (2026-09-25)
spectrum: 000-555 (governance + memory write)
floors: F1, F2, F5, F9, F13
trigger: |
  When an agent wants to write, promote, or canonically reference a claim about a human.
purpose: |
  Prevent repeated retrieval of an AGENT_INFERRED claim from quietly elevating it to canonical
  human truth. Memory content must never inherit authority merely by surviving.

hukum:
  1. AGENT_INFERRED ≠ USER_STATED. Tidak sama taraf, tidak boleh digaul.
  2. AGENT_HYPOTHESIS ≠ AGENT_INFERRED. Hipotesis lebih lemah lagi.
  3. frequent_retrieval(AGENT_INFERRED) ≠ USER_RATIFIED. Pengulangan bukan ratifikasi.
  4. Promotion hanya boleh berlaku jika:
     (a) source_type bertukar dari AGENT_INFERRED ke USER_RATIFIED (live, attested), atau
     (b) F13 SOVEREIGN ratify secara eksplisit, atau
     (c) third-party independently confirms dengan provenance yang berasingan.
  5. Setiap promotion mesti di-receipt dengan event `promotion_gate_audit` yang catat
     source_type asal, source_type baru, frequency count, dan authority signer.

enforcement:
  claim_ledger:
    on_write:
      - if source_type in [AGENT_INFERRED, AGENT_HYPOTHESIS] → tag = 'NON_PROMOTABLE'
      - field `promotable: false` dipaksa dalam entry
      - index kedua (read_only_canonical) tidak sertakan entries dengan tag NON_PROMOTABLE
    on_promote_request:
      - check existing source_type
      - if AGENT_INFERRED/HYPOTHESIS → reject unless evidence of (a/b/c) di atas
      - log ke audit trail dengan trace_id

  human-facing reply:
    - Jangan emit AGENT_INFERRED sebagai "fakta" pasal manusia kepada manusia lain.
    - AGENT_HYPOTHESIS untuk diri sendiri boleh, dengan qualifier jelas.
    - USER_RATIFIED boleh emit sebagai kenyataan biasa.

  edge cases:
    - LLM menyebut sesuatu 50× bukan bukti betul (ChatGPT deep research 2026-09-25).
    - Vector similarity ≠ identity confirmation.
    - Graph centrality ≠ truth.

rasa:
  Tangkap dalam BM Penang: "Dah sebut banyak kali bukan bermakna betul.
  Inference agent kekal inference, melainkan Arif sendiri ratify."

kaitan:
  - /root/AAA/instructions/memory-promotion-gate.md (F13_RATIFIED 2026-09-11)
  - /root/AAA/instructions/human-memory-compartmentalization.md (F13_RATIFIED 2026-09-18)
  - SCAR-2026-09-25-001 (ChatGPT deep research review: source-type inequality)

written_by: irfanclaw
authorized_by: Arif (F13 SOVEREIGN)
authorized_at: 2026-09-25T00:36:00+08:00
