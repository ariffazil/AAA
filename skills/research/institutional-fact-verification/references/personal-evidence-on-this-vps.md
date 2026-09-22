# Personal Evidence on This VPS — Probe Pattern

When the F13 SOVEREIGN (Arif) asks for evidence about his own life — manager dossiers,
reprimand emails, town hall records, the rightsizing/MSS cycle, scar timeline, the sealed
articles, witness observations — the **VPS filesystem is the primary substrate**. Curated
canon (HAMPA cards, scar files, EVIDENCE.md narratives, sealed artisan pages) is the
*bridge layer*, written after the event by humans or agents, and may itself embed the very
institutional narrative being audited.

## The failure shape (what this file exists to prevent)

You reach for `HAMPA/human-laletha-jeevachandran.md` and quote it back as evidence. That is
the bridge quoting the bridge, narrated in the curator's voice. The user lives inside that
institutional narrative and is asking you to find the *raw* signals. Quoting the curator
makes you look like an extension of the curator.

## The five-step probe

Run these in order. Stop and report at each step; do not chain narratively.

### Step 1 — Grep the substrate for the named entity or event

```bash
# Personal/institutional entities (people the F13 is dealing with)
find /root -type f \( -iname "*<name>*" -o -iname "*<name>*.eml" \) 2>/dev/null | head -40

# Specific event classes
find /root -type f -iname "*sb412*"                # the biostrat reassessment file
find /root -type f -iname "*rightsiz*"             # rightsizing artefacts
find /root -type f -iname "*townhall*" -o -iname "*town_hall*"
find /root -type f -iname "*propa*"                # Tengku Taufik propaganda artefacts
```

If `find` returns multiple paths under `forge_work/` mirror trees, list all of them —
`/root/forge_work/<branch>/GEOX/...` is an in-flight git worktree, *not* a backup, and its
contents may differ from `/root/...`. Do not assume equivalence.

### Step 2 — Grep the corpus for the named signal

```bash
grep -l -r -i "<name>" /root/memory/ /root/.hermes/ /root/HAMPA/ 2>/dev/null | head -20
grep -l -r -i "<name>" /root/forge_work/ 2>/dev/null | head -20
```

`grep -l` lists file *paths* that contain the match — the inventory before the read. Then
`cat` only those paths. Do not start with `cat`; a single `cat` does not show you which
neighbours exist.

### Step 3 — When the user named a specific source

If the user said "the Laletha 11 May memo" or "the Kak Su 12 June email", the probe
narrows to those exact paths. Common locations to check first:

| Source class | Likely paths |
|---|---|
| Original emails (`.eml`) | `/root/memory/evidence/<case>/<date>-cycle/` |
| Outbound emails (drafts) | `/root/.hermes/outbox/email-<recipient>-DRAFT.md` |
| Inbound coordination | `/root/.hermes/inbox/*.md` |
| HAMPA human cards | `/root/ariffazil/HAMPA/human-<slug>.md` |
| Scar files | `/root/memory/H5-scars/SCAR_<TOPIC>.md` |
| SCAR registry | `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` |
| Knowledge graph nodes | `/root/AAA/wiki/KNOWLEDGE_GRAPH.json` |
| GEOX scar memory (semantic claims) | `/root/GEOX/contracts/schemas/scar_memory.py` |

If the named source is missing from its expected path, **say so**. Then surface the closest
bridge (e.g. the HAMPA card that cites the email) and label it `[OSS via bridge]`.

### Step 4 — Order by increasing curation, label each tier

```
[OSS]   raw .eml / .txt / .docx found on disk, cited verbatim
[OSS via bridge]  raw artefact not on disk; bridge layer (HAMPA card, scar narrative) quotes it
[DER]    bridge interpretation written by human or agent curator
[INT]    your synthesis across artefacts
[UNK]    named source not located anywhere on this VPS
```

Never quote a bridge as if it were the source. A HAMPA card that says "Laletha's email dated
11 May 2026 contains 5 numbered points" is `[DER]` (the bridge author summarises an email
you have not read) — not `[OBS]` (you have read the email).

### Step 5 — Cite file path on every claim

Every personal/institutional claim in the response must end with the file path (and SHA
where the artefact is sealed). Example shape:

> "Kak Su's email dated 12 Jun 2026 cites three CRITICAL points. Source: `HAMPA/human-kak-su-siti-suhana.md` lines 35–44. The original email itself was not located on this VPS (`[UNK]`)."

If you do not know the path, you do not know the claim. Search before stating.

## Worked example — the exact session that built this file

User asked: *"I'm Arif — tell me everything about Kinabalu scars. Relate to Layang2 scars and
MSS rightsizing propaganda REALITY > EVERYTHING."*

What went wrong first time: narrated from `forensic_memory/EVIDENCE.md`, scar files, and
scar_memory.py canon without running `find` for the underlying `.eml` files. The HAMPA
cards and scar narratives are bridges; they are necessary but not the raw substrate.

The corrected sequence was:

1. `find /root -type f \( -iname "*laletha*" -o -iname "*kak_su*" -o -iname "*sitishana*" \)`
2. `cat /root/ariffazil/HAMPA/human-laletha-jeevachandran.md`
3. `cat /root/ariffazil/HAMPA/human-kak-su-siti-suhana.md`
4. Report what is raw (`[OSS]`) vs bridged (`[OSS via bridge]`) vs interpreted (`[DER]`).
5. State the gap: original Laletha 11 May `.eml` and Kak Su 12 Jun `.eml` not on this VPS.

After this sequence the user could read the verbatim dossier text and judge for himself
whether the bridge had smoothed anything. Which is the entire point.

## Anti-pattern summary

- **Narrating from canon before probing**: the failure that produced this file.
- **Quoting a card quoting an email**: two bridges, no substrate.
- **Picking one path from `find` because the user asked about "the file"**: the user
  usually wants all sibling artefacts, not just the one named file. List them all.
- **Forging a source path because "the user expected one"**: forbidden. `[UNK]` is always
  preferable to "I think it's in `/root/...`".
- **Skipping the gap declaration**: if the named source is missing, the *gap* is the finding.
  Say it. Do not paper over it with the bridge as if the gap didn't exist.

## Related skills

- `observe-ground` — substrate-level evidence discipline (OBS/DER/INT/SPEC, F2 truth).
- `institutional-language-audit` — when the institution talks about itself, this is how to read
  what it avoided.
- `live-probe-audit-pattern` — sibling probe; canonical probe-pattern for live systems.
- `forge-repo-intelligence` — same discipline applied to repos, not personal lives.
