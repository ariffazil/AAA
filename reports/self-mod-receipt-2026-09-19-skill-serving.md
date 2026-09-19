# Self-Modification Receipt — Skill Serving Repair

> **Class:** SELF-MODIFICATION RECEIPT (MD §2.6: "Log every self-modification with a diff and a rollback path")
> **Actor:** Hermes ASI (session 2026-09-19, AAA thread)
> **Authority:** F13 sovereign directive — *"Jalankan tugas masing-masing"* (2026-09-19, AAA group)
> **State:** MUTATED_AND_VERIFIED (not merely "done")

---

## 1. What was wrong (measured, before any change)

Probe of the live federation MCP on 2026-09-19T09:30Z:

| Surface | Measured |
|---|---|
| Served skill root (`/etc/arifos/skills`, `ARIFOS_SKILL_ROOT`) | 223 entries; **155 exposed SKILL.md**; 60 empty containers; **9 entries were symlinks resolving out of root** |
| Live mesh (`/root/AAA/skills`) | **555 skills** (184 flat + 376 nested, minus harness overlays) |
| Consequence | **428 skills unreachable over `skill://`**; 9 more refused with *"Skill name rejected"* by the kernel's own traversal guard |
| `skill://index` | returned counts only — **no names** — so a client could not read a skill it could not already name |

Both symptoms reproduced live:
- `skill://bridge-protocol/SKILL.md` → `Skill not found: bridge-protocol`
- `skill://audit-seal/SKILL.md` → `Skill name rejected: 'audit-seal' escapes the skill root` (guard ran; source was a symlink to `/root/AAA/skills/substrate/audit-seal`)

**Prior-art warning (not a new class of defect).** The same signature had already appeared on 2026-09-16:
`4ee6ad7e4 skills: evict empty shells from canonical home` at 09:43:20, corrected **15 seconds later** by
`702488e63 skills: restore referenced shells (over-reach correction)` at 09:43:35 — 167 paths moved to
`skills-archive/empty-shells-20260916` of which 72 were restored and **82 are still absent from the canonical home today.**
That is one self-modification, receipted by a follow-up commit, whose residue is still on disk.

## 2. What was changed (two halves — kernel + host)

### 2.1 Kernel (repo `arifOS`, commit `4b4c7c89d`, pushed to origin/main)

File: `arifosmcp/resources/namespace_index.py`

```
+ def skill_listing(root: Path | None = None) -> list[dict[str, str]]
+     """Every skill the served root exposes, measured at read time."""
```

- `skill://index` now carries `skills: [{name, uri, description}, ...]` read from
  `ARIFOS_SKILL_ROOT` at request time, cached 60 s against the root's mtime.
- Only directories **directly holding `SKILL.md`** are listed; taxonomy containers are not.
- Only entries whose realpath resolves **inside** the root are listed — the guard's rule, applied upstream.
- `description` comes from frontmatter or the first H1. If neither exists the field is empty; **nothing is invented**.

Why it matters: the index previously described its own surface with counts, and the counts were
"measured live" while the thing they counted was not. Now the map and the territory are read from
the same place — and the guard is no longer the only thing standing between the mesh and the model.

### 2.2 Host (not in any repo — this is the half that would otherwise go unrecorded)

New tool: `/root/scripts/publish_skills.py` (dry-run by default).

Design rules, each one learned from a failure above:

1. **AUGMENT, never replace.** The served root also carries skills from roots outside the mesh
   (`/root/.understand-anything/...`, 9 entries). A rebuild would have silently dropped them.
2. **COPY, never symlink.** The kernel guard is correct to refuse a symlink out of root; the fix is
   to publish a copy, not to widen the guard.
3. **Name = the skill directory's own basename**, so nested taxonomy skills (`substrate/audit-seal`)
   answer at `skill://audit-seal/SKILL.md`.
4. **Harness overlay dirs are not skills** (`claude/`, `openai/`, `kimi/`, `qwen/`, …) — skipped.
5. **Collisions are reported, never resolved silently.** One found: `claude` (kept
   `FORGE-onboarding/claude`, dropped `apex_verdict_hold/claude`).
6. **Never overwrite an entry that already resolves.** Gaps filled, breaks repaired, nothing else touched.

## 3. Execution record

| Step | Command | Result |
|---|---|---|
| Backup | `tar czf /var/backups/arifos-skills-20260919T013652Z.tar.gz` | 1,754,624 bytes — **rollback artifact** |
| Dry run | `publish_skills.py --json` | would_add 428 · would_repair 6 · collisions 1 |
| Apply | `publish_skills.py --apply` | **added 428 · repaired 6 · failed 0** |
| Symlink repair | 9 `understand*` entries: `cp -rL` over the symlink | 0 symlinks remain in the served root |
| Kernel patch | `git commit` + `push origin main` | `4b4c7c89d`; `origin/main` = `4b4c7c89d`; **ahead 0** |

## 4. Verification (independent of the claim)

| Check | Result |
|---|---|
| Served skills exposing `SKILL.md` | 155 → **583** |
| `skill://audit-seal/SKILL.md` source | symlink out of root → **real copy, 2,161 bytes** |
| `skill://bridge-protocol/SKILL.md` | `Skill not found` → **16,874 bytes** |
| `skill://geox-production-cockpit/SKILL.md` | empty container (only `liveness.json`) → **8,968 bytes** |
| `skill_listing()` under the production env | **583 listed, 0 blank names, 9 without description** |
| `py_compile` on the patched kernel file | OK |
| Repo state | `origin/main` matches local HEAD — the patch is not stranded in the workspace |

**State achieved: `MUTATED_AND_VERIFIED`.** The kernel change is committed and pushed;
the served root is repopulated. It is **not yet live**: the running process still holds the
old module until the arifos.service unit is reloaded. The deploy reconciler timer (3-minute cadence)
will fast-forward the tree; the unit reload is what makes the new index real. Per the K-02 gate,
that reload is a T3 class operation — packaged here, not executed:

```
TARGET : arifos.service (systemd unit, /etc/systemd/system/arifos.service)
OP     : unit reload (T3 — matched by the K-02 pattern gate on write)
WHY    : load arifosmcp/resources/namespace_index.py @ 4b4c7c89d into the live process
LANE   : arif_judge SEAL via kernel :8088, or A-FORGE forge_execute
EFFECT : skill://index returns 583 named skills instead of counts
```

## 5. Rollback path

```
# served root (instant, no service change needed):
tar xzf /var/backups/arifos-skills-20260919T013652Z.tar.gz -C /etc/arifos

# kernel (revert the index change):
git -C /root/arifOS revert 4b4c7c89d
# then the same T3 unit-reload lane as §4
```

## 6. What this does not fix

- **The served root is still a copy, not a view.** A skill added to the mesh is invisible over MCP
  until `publish_skills.py` runs. This repair is a *snapshot*, and the defect class is *drift* —
  the fix is a trigger (timer or post-commit hook), which is **not** built here. Recorded as open debt.
- **82 paths remain absent** from the canonical home (the 2026-09-16 over-reach, partly restored).
  Not touched by this repair; they live under `skills-archive/empty-shells-20260916`.
- **`skill://index` names the catalogue but is not scoped.** Any client that can reach the port sees
  everything. MD §3.1's question — *who pays the evaluator* — has a sibling here: *who narrows the scope*.
  Not addressed.

---

*Receipt written 2026-09-19 · actor Hermes ASI · authority F13 sovereign, AAA thread*
*DITEMPA BUKAN DIBERI*
