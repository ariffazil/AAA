# SCAR-AGY-003 - Edit Drift Cascade (Stale oldString)

Scar ID: SCAR-AGY-003 (catalog: Scar #19)
Domain: File Mutation / Stale Context / Edit Discipline
Severity: P1 (High Frequency - 463 errors in 60 days)
Status: SEALED (autonomous scar extraction, 2026-09-12)
Confidence: 0.92

---

## 1. Failure Pattern

The OpenCode `edit` tool returned 463 errors with the message:
  "Could not find oldString in the file. It must match exactly, including whitespace"

Top hit files (60d window):
  - /root/arif-fazil.com/sites/arif-fazil.com/public/klci/index.html  - 5 hits (same file, sequential edits)
  - /root/arifOS/arifosmcp/server.py                                  - 3 hits (critical kernel)
  - /root/WEALTH/wealth_mcp/tools/institutional.py                   - 3 hits
  - /usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py - 4 hits (runtime)
  - /tmp/t3_patch.py                                                   - 2 hits

## 2. The Echo

Agent assumes the file state matches the original training memory or prior context. Three failure modes:

- **Pre-edit drift**: another tool already changed the file before the edit arrives
- **Stale paste**: agent copy-pastes a snippet from memory that no longer matches the on-disk file
- **Multi-edit collision**: agent applies 3 sequential edits with `oldString` from the BEFORE-state of edit 1, but edit 1 already changed it

## 3. The Law

**Before any edit tool call:**
1. `read` the file (with offset/limit) within last 30 seconds
2. Verify `oldString` matches the CURRENT disk state byte-for-byte
3. For multi-edit, either batch via `forge_filesystem(mode=patch, mode=multi_patch)` or do read-between-edits

Forbidden pattern:
  - Edit a file you have not Read in this session
  - Use `oldString` from a prior tool output as if it were ground truth
  - Apply 2+ sequential edits without re-reading

## 4. The Eureka (unused capability)

- `aforge_forge_filesystem(mode=patch)` — atomic patch with validation
- `aforge_forge_filesystem(mode=read, offset=N, limit=M)` — read region only
- `aforge_forge_vault(mode=read)` — read protected file with receipt

## 5. Verified Fix

```bash
# Step 1: Read current state
content=$(aforge_forge_filesystem(mode=read, path=$file))

# Step 2: Verify oldString in content
if ! echo "$content" | grep -F "$oldString" > /dev/null; then
  echo "SCAR-AGY-003: oldString not in current file state. Re-read."
  exit 1
fi

# Step 3: Apply via forge_filesystem patch (atomic)
aforge_forge_filesystem(mode=patch, path=$file, old_text="$oldString", new_text="$newString")
```

## 6. Hardening

- **FORGE-lsp-pre-edit-gate**: enforce LSP read-before-edit
- **OPENCODE edit tool**: refuse if last `read` for this path > 60s ago
- **OPENCODE multi-edit**: combine into single atomic patch call

```yaml
scar_id: SCAR-AGY-003
n_incidents: 463
severity: P1
law: Read current file state before edit. Verify oldString matches. Use forge_filesystem patch.
eureka: forge_filesystem(mode=patch) + forge_filesystem(mode=read, offset/limit)
confidence: 0.92
```
