# PETRONAS Intelligence Atlas

> Canonical organized file structure for all PETRONAS-related assets.
> Location: `/root/petronas/`

## Directory Structure

```
/root/petronas/
├── ATLAS.md                    ← Master index + link graph
├── 01-research/     (13 files) ← Institutional analysis, forensic, case building
├── 02-articles/      (4 files) ← MakcikGPT published articles
├── 03-intelligence/  (5 files) ← Briefings, vitals, crisis maps
├── 04-letters/       (2 files) ← Surat terbuka (attested) + mailing list
├── 05-data/          (3 files) ← Collapse models, vitals source
├── 07-constitutional (2 files) ← GENESIS canon
├── 08-deployed/      (3 files) ← arif-fazil.com live PDFs
```

## Key Files

| File | Path | Attested Hash |
|---|---|---|
| Surat v3 (attested) | `04-letters/surat-v3-attested.pdf` | `e5273614df3b25c1...` |
| Mailing list v4 (99 MPs) | `04-letters/mailing-list-v4-99.csv` | — |
| Petronas DNA | `02-articles/petronas-dna.md` | — |
| GENESIS canon | `07-constitutional/006_PETRONAS_PARADOX.md` | — |

## Link Graph

```
GENESIS canon → feeds → Research articles → feeds → Surat terbuka
Research articles → feeds → Deployed on arif-fazil.com
Collapse trajectory → feeds → Intelligence briefings
Vitals.json → feeds → Live API on arif-fazil.com
```

## Attestation

All outputs verified via `/root/HERMES/attestation-ledger.jsonl`
Verification: `python3 /root/HERMES/scripts/output-verify.py <file>`
