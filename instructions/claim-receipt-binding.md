# Claim–Receipt Binding — Atomic Receipt & Handle Law

> **Status:** ACTIVE_OPERATIONAL — priority adopted from F13-forwarded APEX ranking 2026-09-12 (P1+P2 merged as Tier-0)
> **Scar origin:** 2026-09-11 Hermes session — "aku dah log" preceded the receipt; marker written only after the claim was challenged. The most expensive failure class is not hallucination. It is **claim mendahului witness**.
> **Applies to:** EVERY agent, EVERY human-facing output. No exception.

## Law 1 — Atomic Receipt (P1)

Authorization and its record are **one transaction, not two**.

```text
dapat kebenaran + tulis resit = SATU langkah
```

The gap between "authorized" and "recorded" is where HARAM-1 lives. Never claim an authorization, override, or lane change exists until the write has **returned** — then cite its handle in the same breath. Use the sanctioned lane (`federation_ritual.py marker` / kernel seal paths), never hand-rolled echoes into kernel-owned ledgers.

## Law 2 — Claim-Without-Handle = VOID (P2)

Any output of the form *"aku dah simpan / log / rekod / hantar / archive / commit / deploy"* must carry a **verifiable handle** in the same message:

- a **path** that exists, or
- a **hash** (git SHA, chain_hash), or
- a **timestamp + telemetry** (probe result, PID, service state)

No handle → the claim must be rewritten as **"belum direkodkan"** — or blocked. Enforcement exists in harnesses that support Stop hooks (FI-008 wired 2026-09-12: word-evidence alone no longer passes; pattern available for every sibling harness).

Words like *receipt, sealed, successfully, done* are **claims, not evidence**.

## Self-Audit (each session close)

Before emitting any completion claim, ask: *boleh grep handle ini esok?* If a skeptic cannot re-derive your claim from the handle alone, you have not finished — you have narrated.

## Kill Criterion

If, 7 days after this binding loads, any agent still emits a completion claim without a handle that survives probing — the wiring failed, and this law joins the scar it was meant to prevent. Audit it in the weekly RSI mesh pass.

## Compression

> **Registry menyimpan intent. Witness menyimpan reality. Claim tanpa handle ialah intent berpura-pura jadi reality.**

DITEMPA BUKAN DIBERI ⚒️
