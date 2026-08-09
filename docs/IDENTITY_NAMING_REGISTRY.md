# Identity naming registry — Gemini research → AAA sovereign names

> **Sealed by F13 answers:** 2026-08-09  
> **Source research:** AIMS / SPIFFE / WIMSE / VC / HDP (landscape only)  
> **Rule:** External standards may **map**; they do not **rename** the institution.

## Locked decisions

| # | Domain | Decision | Wire / field |
|---|--------|----------|----------------|
| 1 | Session / action capability | **ACT only** — retire SCT as primary name | `act_v1.*` |
| 2 | Agent identity string | **Keep** `agentId` + `did:web` | cards, registry |
| 3 | Human→agent citizen proof | **warga_status / passport** (planned) | not W3C VC brand |
| 4 | Multi-hop delegation | **ACT chain / hop receipts** — no HDP/IBCT brand | defer build |
| 5 | Workload attestation stack | **Map to existing** — `arif_init` + ACT + organ keys | no SPIRE organ |

## Translation table (research → ours)

| Gemini / industry term | AAA / arifOS name | Status |
|------------------------|-------------------|--------|
| AIMS (IETF agent identity stack) | *Landscape only* — “AIMS-like” if needed in prose | **Not adopted as name** |
| SPIFFE ID / WIMSE URI | `agentId` + `did:web:…` | **Already named** — no primary rename |
| SPIRE / X.509-SVID | `arif_init` session mint + organ Ed25519 keys | **Map**, do not install SPIRE as doctrine |
| WIMSE Proof Token (WPT) | **ACT** (`act_v1.*`) | **Already named** (was SCT) |
| OAuth 2.0 for agents | Out of band / optional client; not sovereign root | Not core |
| W3C Verifiable Credential | **warga passport** / `warga_status` | **Already planned name** |
| DID (W3C) | **`did:web:arif-fazil.com`** (+ organ DIDs) | **Already named** |
| HDP (Human Delegation Provenance) | *Research alias only* | **No brand** |
| IBCT (Invocation-Bound Capability Token) | **ACT** / future **ACT hop receipt** | **No IBCT name** |
| Delegation chain | **ACT chain** (multi-hop deferred) | Name reserved, build later |
| Issuer / holder / verifier (VC) | Sovereign (Arif) / agent (holder) / counterparty (verifier) | Roles only, not VC product name |
| Static API keys (anti-pattern) | KUNCI-MAS + short-lived ACT — not agent identity | Hygiene, not rename |

## What we rename (docs debt)

| Old / mixed | New canonical | Action |
|-------------|---------------|--------|
| SCT · `sct_v1.*` | **ACT** · `act_v1.*` | Prefer ACT in new docs; dual-read during transition |
| “Session Capability Token” in new prose | **Action Capability Token** | Same object, one name |
| SPIFFE/AIMS as “must implement” | **Do not** | External interop may add **optional** alias field later — not primary |

## What we do **not** create

- No new AAA organ: SPIRE, AIMS server, VC issuer ministry  
- No `spiffe://` as directory primary  
- No HDP/IBCT identifiers in code until multi-hop is deliberately forged  
- No replacement of Ed25519 + ACT with X.509-SVID as **doctrine** (substrate may use TLS elsewhere without renaming identity)

## Optional later (alias only — not decided)

If external parsers require SPIFFE-shaped strings:

```text
agentId: hermes-asi
did: did:web:arif-fazil.com#hermes-asi   # or organ-specific
# OPTIONAL alias only:
# spiffe_id: spiffe://aaa.arif-fazil.com/agents/hermes-asi
```

Requires separate F13 nod. Default: **no alias field**.

## Alignment with AAA_NEXT_90D

- P1 external telephone uses **agentId + did + ACT** on the wire story  
- P2 citizens use **warga_status / passport**  
- Multi-hop ACT chain remains **deferred** (name held, not HDP)

DITEMPA BUKAN DIBERI.
