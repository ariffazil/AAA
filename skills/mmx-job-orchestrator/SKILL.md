---
name: mmx-job-orchestrator
description: Supervisor for all async MMX jobs (video, music, batch image). Handles: submit → poll → retry → download → clean. Activates when Arif asks to generate video, music, or batch images. Uses mmx exit codes, stderr for progress, and implements agentic retry semantics — not human retry.
metadata: {"openclaw": {"emoji": "🎬"}}
---

# MMX Job Orchestrator — Async Supervisor for MMX

Async MMX jobs (video, music, batch image) are fire-and-forget for humans. For an ASI agent, they need a supervisor loop: submit → track → retry on failure → download → confirm → clean up.

## Async Job Types

| Job | Command | Poll Method | Max Retries |
|---|---|---|---|
| Video | `mmx video generate --async --prompt "..."` | `mmx video task get --task-id <id>` | 3 |
| Music | `mmx music generate --out song.mp3` (sync but slow) | N/A | 2 |
| Image Batch | `mmx image generate --prompt "..." --n 3` | N/A | 2 |
| Vision File | `mmx vision describe --file-id <id>` | N/A | 2 |

## The Supervisor Loop

### 1. SUBMIT
```bash
# Video — use async to get task-id immediately
mmx video generate --prompt "..." --async
# Returns: { task-id: "..." } or similar — capture the ID

# Music — run in background with timeout
timeout 120 mmx music generate --prompt "..." --out /tmp/song.mp3
```

### 2. TRACK (poll for video)
```bash
# Poll every 30s for up to 10 minutes
mmx video task get --task-id <task-id>
# Check status: pending / processing / complete / failed
```

### 3. RETRY (on failure)
```
Exit code 0 + status complete → proceed to download
Exit code 0 + status pending/processing → re-poll
Exit code non-zero → retry up to max retries
Exit code failure + no progress after max retries → abort, announce failure
```

### 4. DOWNLOAD
```bash
# For video
mmx video download --file-id <file-id> --out <destination>

# For music (if sync)
# Already at --out path
```

### 5. CONFIRM
- Verify file exists and size > 0
- Report: `[type] ready: <path>`

### 6. CLEAN
- Remove temp files from /tmp/
- Log completion to vault999

## Exit Code Reference

| Exit Code | Meaning | Action |
|---|---|---|
| `0` | Success | Proceed |
| `1` | General error | Retry once, then abort |
| `2` | Invalid arguments | Abort — fix prompt |
| `3` | Auth/token error | Abort — token issue |
| `124` | Timeout (from `timeout` cmd) | Retry once with same prompt |
| Any other non-zero | Unknown error | Retry, log stderr |

## Progress Tracking (stderr)

Many MMX async jobs stream progress to stderr, not stdout. Capture stderr for diagnostics:
```bash
mmx video generate --prompt "..." --async 2>&1 | tee /tmp/mmx-job.log
```

## Multi-Job Parallel Supervisor

For batch image jobs:
```bash
# Submit all at once (background)
for i in {1..3}; do
  mmx image generate --prompt "image $i" --out /tmp/img_$i.png &
done
wait  # wait all complete

# Check all exist
for f in /tmp/img_*.png; do
  [ -s "$f" ] || echo "MISSING: $f"
done
```

## Output Format for Job Completion

```
MMX JOB COMPLETE:
Type: [video/music/image]
Task-ID: [if async]
Output: [path or URL]
Duration: [time from submit to ready]
Retries: [0 if clean, N if retried]
Status: [SUCCESS / FAILED]
```

## Error Format

```
MMX JOB FAILED:
Type: [video/music/image]
Task-ID: [if async]
Error: [stderr or exit code]
Retries attempted: [N]
Action: [aborted / escalated to Arif]
```
