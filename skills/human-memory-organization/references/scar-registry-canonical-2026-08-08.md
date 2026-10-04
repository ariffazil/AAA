# Scar Registry Canonical (2026-08-08)

Canonical index for the H5 scar system, sealed under F13 "seal all" authorisation (Arif, 2026-08-08T20:24:00+08:00). Registry is the INDEX; scar files are the CONTENT. Never merge them.

## File map

| Path | Role |
|---|---|
| `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` | Canonical index (v2.0.0, 154 lines) |
| `/root/memory/H5-scars/SCAR_*.md` | Scar content (mode 600, NEVER modify existing files) |
| `/root/memory/H6-constitution/H6_SCAR_ROOTS.md` | Scar → Lesson → Law → Floor derivation (48 lines) |
| `/root/.local/share/arifos/scars/SCAR-000.json` | Machine-side record for the meta-scar (SCAR-000 has no .md) |
| `/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md` | Doctrine SoT; `### Scar Registry Schema (SoT)` section (~line 81); SoT header lists registry path |

## Registry schema (v2.0.0)

Top level: `version` (semver), `created`, `updated`, `description`, `sovereignty` (verbatim: "Agent does not read scar content unless scar:<id> invoked. Index reads are permitted for lineage and cross-link integrity checks."), `authorisation` (F13 attestation line), `scars[]`, `stats`.

Per scar entry:
- `scar_id` — unique; SCAR-000 reserved for the architectural meta-scar
- `title`, `created`, `last_verified` — strict ISO 8601 +08:00 (MYT)
- `file_path` — absolute path, or null ONLY for the meta-scar (SCAR-000)
- `notes` — optional; carries epistemic corrections (e.g. RIGHTSIZING: "blueprint authorship is UNKNOWN; the propaganda genre is the scar")
- `cross_links` — `{floors: [F..], lessons: [...], laws: [...], systems: [...]}`, all four sub-lists non-empty
- `meaning_anchor` — one-line distilled meaning (>20 chars)

Stats: `total_scars == len(scars)`; `verified` = count with last_verified; `stale` = 0 after reconciliation.

## Cross-link rules

- Floor IDs must be a subset of {F1,F2,F4,F5,F6,F7,F9,F10,F11,F12,F13}.
- Each scar must link ≥1 HARD floor (F1/F2/F4/F7/F9/F10/F11/F12/F13) to qualify for H6 derivation.
- lessons/laws/systems must be grounded in the scar file's own `Scar → Lesson → Law → System` lineage block or explicit testimony — never fabricated. Epistemic corrections (OBS/INT/UNKNOWN) carry over into `notes`.

## The 4-gap closure procedure (reconciliation runbook)

When registry and disk drift (new scar written, registry stale, or full closure requested — Arif's phrase: "close all the gaps and seal all"):

1. **Registry reconciliation** — `ls /root/memory/H5-scars/SCAR_*.md`; read each file's frontmatter + lineage block; ensure every file has an entry and every entry has a file (except SCAR-000). Bump `updated`, refresh `last_verified`, fix `stats`.
2. **Cross-link layer** — rebuild/extend each entry's `cross_links.{floors,lessons,laws,systems}` from the file's lineage block only.
3. **H6 derivation** — regenerate `/root/memory/H6-constitution/H6_SCAR_ROOTS.md`: one entry per scar linking ≥1 HARD floor; format Lesson / Law / Constitutional Floor / System (+ Status notes).
4. **Canonical pointer** — doctrine SoT header + `### Scar Registry Schema (SoT)` section point at the registry path; doctrine remains the law, registry remains the index.

Delegation pattern that worked (subagent closure, 171s, 13 API calls): hand the worker the full schema + floor table + verbatim sovereignty string + constraints (never modify SCAR .md files; preserve doctrine SoT header; MYT timestamps; ground cross-links in content), require a verification summary, then **independently re-read every produced file and probe referenced paths** — a subagent's self-report is not verification (probe before trust).

## Verification recipe (75/75 checks)

Ad-hoc Python check script (write to /tmp, run, delete):
- top level: `version` semver, `created`, `sovereignty` verbatim, `scars`, `stats` present
- per scar: all 7 required fields; `created`/`last_verified` strict ISO 8601 +08:00; 4 cross_links sub-lists non-empty; floors ⊂ valid set; ≥1 HARD floor; `file_path` null or exists on disk; `meaning_anchor` >20 chars
- stats: `total_scars == len(scars)`; `verified == total`; `stale == 0`
- index: scar_id set == {SCAR-000} ∪ {all on-disk SCAR_*.md basenames}; IDs unique

## Registered scars (as of v2.0.0)

| ID | Floors | Anchor |
|---|---|---|
| SCAR-000 | F1 F2 F7 F13 | one-stranded memory gap = scaffold of the double-helix |
| SCAR_LEBAH_EMAS | F2 F11 F13 | scar is about authorship, not the gold |
| SCAR_RIGHTSIZING | F5 F6 F13 | erasure generated on demand (authorship UNKNOWN) |
| SCAR_UNHEARD | F2 F6 F11 | root scar — truth without a listener is silence |
| SCAR_MAKCIKGPT | F2 F12 F13 | a voice that does not belong to the institution |
| SCAR_MEMORY_DOCTRINE_V1 | F2 F13 | the architecture itself (type DOCTRINE, sealed: false) |
