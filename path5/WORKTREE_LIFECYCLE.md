# Path-5 Worktree Fabric & Lifecycle Specification
**Document:** `WORKTREE_LIFECYCLE.md`  
**Standard:** QQQ Protocol · F1 Truth · Physical Isolation  
**Date:** 2026-09-14T09:48:00+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::PATH5_OPERATIONALIZATION::v1`

---

## 1. Principles of Physical Isolation

1. **Main is Sanctuary:** The root working directory (`/root/<REPO>`) is a read-only canonical reference for swarm workers. Direct mutations to main working directories are forbidden in swarm mode.
2. **One Agent, One Substrate:** Every agent operation executes inside a dedicated Git Worktree rooted at `/root/forge_work/worktrees/<lease-id>`.
3. **Collision Impossibility:** Two agents mutating identical relative file paths (e.g., `tests/test_mesh.py`) operate on distinct inode structures on disk. Zero filesystem collisions can occur.

---

## 2. Directory Layout

```text
/root/forge_work/worktrees/
├── lease_01a2b3c4d5e6/          ← Agent A (FI-008 / Kimi)
│   ├── .git                     ← Git worktree pointer
│   ├── AAA/
│   └── tests/
├── lease_02f7e8d9c0b1/          ← Agent B (FI-009 / Antigravity)
│   ├── .git
│   ├── AAA/
│   └── tests/
└── .archive/                    ← Archived worktree tarballs
```

---

## 3. Four Lifecycle Verbs

### 3.1 `create`
```bash
git -C <repo_path> worktree add -b "swarm/<lease_id>" "/root/forge_work/worktrees/<lease_id>" <base_ref>
```
- Validates active lease before creation.
- Binds `<lease_id>` to worktree directory.
- Creates isolated branch `swarm/<lease_id>`.

### 3.2 `resume`
- Validates lease has not expired.
- Checks `git status -s` in `/root/forge_work/worktrees/<lease_id>`.
- Allows re-entry for multi-turn execution.

### 3.3 `archive`
- Captures uncommitted diff or branch commit into `/root/forge_work/worktrees/.archive/<lease_id>.bundle`.
- Preserves full audit history if reconciliation is postponed.

### 3.4 `destroy`
```bash
git -C <repo_path> worktree remove --force "/root/forge_work/worktrees/<lease_id>"
git -C <repo_path> branch -D "swarm/<lease_id>"
```
- Invoked automatically after successful reconciliation or upon lease expiry/revocation.
- Cleans disk space without leaving orphaned git metadata.
