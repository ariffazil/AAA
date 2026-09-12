# SCAR-AGY-005 - Canonical Path Hallucination

Scar ID: SCAR-AGY-005 (catalog: Scar #22)
Domain: Path Probing / Canonical Reference / Pre-flight Reality Check
Severity: P2 (204 errors in 60 days, single file)
Status: SEALED (autonomous scar extraction, 2026-09-12)
Confidence: 0.88

---

## 1. Failure Pattern

The OpenCode `read` tool returned 204 errors with the message:
  "File not found: /root/AAA/LOOP.md"

Single hot file. Agent assumes the canonical loop file lives at /root/AAA/LOOP.md but the actual location differs (or the file does not exist on this substrate).

## 2. The Echo

Agent uses "remembered paths" from training or prior sessions. The /root/AAA/LOOP.md reference appears in:
- /root/.opencode/skills/*.md (mentioned in some agentic skills)
- Old carry-forward documents
- A prior session's protocol narrative

But the file may have been renamed, moved, or never existed on this substrate.

## 3. The Law

Before any `read` call on a path the agent has not verified in this session:

1. `ls -la <parent_dir>` first - confirm the directory exists
2. `glob **/*` - search for similar names
3. `grep -r "" /root/AAA/scars/` - check if referenced canonically
4. Only then `read` with the exact verified path

Forbidden:
- Reading a path based on memory or training recall
- Reading without first probing the parent directory
- Assuming path constants survive session boundaries

## 4. The Eureka (unused capability)

- `glob` (ripgrep-backed) - find by pattern in seconds
- `bash` with `ls -la` - direct filesystem probe
- `aforge_forge_filesystem(mode=list)` - structured directory listing
- `aforge_forge_vault(mode=list)` - VAULT999 canonical file lookup

## 5. Verified Fix

```bash
# Step 1: Probe parent
ls -la /root/AAA/ | head -30

# Step 2: Glob for variants
glob /root/AAA/**/*.md

# Step 3: Read with the exact on-disk path
read <verified_path>
```

## 6. Hardening

- **A-FORGE skill adapter**: wrap `read` calls in `path_exists?` check
- **OPENCODE skill: preflight-probe**: trigger before any "I know the path" claim
- **arifos_arif_observe(mode=compass)**: returns canonical paths for known entities

```yaml
scar_id: SCAR-AGY-005
n_incidents: 204
severity: P2
law: Probe parent directory with ls or glob before read. Never trust remembered paths.
eureka: glob + ls + forge_filesystem(mode=list) + vault(mode=list)
confidence: 0.88
```
