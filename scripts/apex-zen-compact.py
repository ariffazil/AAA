#!/usr/bin/env python3
"""
APEX-ZEN Ledger Compaction — retention + archival for telemetry and receipts.

Telemetry: deduplicates to latest snapshot per source, drops stale entries.
Receipts: archives entries older than RETENTION_DAYS, keeps recent.

Run from apex-zen-run-loop.sh or standalone.
"""
import json
import gzip
import os
import fcntl
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

TELEMETRY = Path('/root/VAULT999/apex-zen-telemetry.jsonl')
RECEIPTS = Path('/root/VAULT999/apex-zen-receipts.jsonl')
RECEIPTS_STATE = Path('/root/VAULT999/apex-zen-receipts.state.json')
ARCHIVE_DIR = Path('/root/VAULT999/apex-zen-archive')

# Retention: keep receipts for this many days
RETENTION_DAYS = 7
# Keep at most this many telemetry snapshots per source (most recent N)
TELEMETRY_KEEP_PER_SOURCE = 3


def compact_telemetry(dry_run: bool = False) -> dict:
    """Deduplicate telemetry to latest N snapshots per source."""
    if not TELEMETRY.exists():
        return {'action': 'skip', 'reason': 'no_telemetry'}

    lines = TELEMETRY.read_text().strip().split('\n')
    original_count = len(lines)

    # Parse and group by source
    by_source: dict[str, list[tuple[str, dict]]] = {}
    parse_errors = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            source = record.get('source', 'unknown')
            by_source.setdefault(source, []).append((line, record))
        except json.JSONDecodeError:
            parse_errors += 1

    # Keep latest N per source
    kept_lines = []
    dropped = 0
    for source, entries in by_source.items():
        # Sort by timestamp descending, keep latest N
        entries.sort(key=lambda x: x[1].get('timestamp', ''), reverse=True)
        keep = entries[:TELEMETRY_KEEP_PER_SOURCE]
        drop = entries[TELEMETRY_KEEP_PER_SOURCE:]
        kept_lines.extend(line for line, _ in keep)
        dropped += len(drop)

    # Sort by timestamp to maintain chronological order
    def sort_key(line):
        try:
            return json.loads(line).get('timestamp', '')
        except (json.JSONDecodeError, AttributeError):
            return ''
    kept_lines.sort(key=sort_key)

    if not dry_run:
        lock_file = TELEMETRY.with_suffix(".lock")
        with open(lock_file, "w") as lock_fd:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
            try:
                tmp = TELEMETRY.with_suffix(".tmp")
                tmp.write_text('\n'.join(kept_lines) + '\n' if kept_lines else '')
                try:
                    os.replace(tmp, TELEMETRY)
                except PermissionError:
                    # The telemetry file carries the append-only attribute
                    # (chattr +a). Compaction REWRITES that file, which an
                    # append-only vault forbids BY DESIGN. So this is not a
                    # transient fault to retry — it is a permanent conflict
                    # between two deliberate rules, and it had already failed
                    # 169 times before anyone looked, every five minutes, with
                    # a traceback the caller swallowed.
                    #
                    # The honest outcome is a clean SKIP that names the
                    # conflict. Rewriting an append-only ledger to tidy it
                    # would destroy the guarantee the ledger exists to provide.
                    try:
                        tmp.unlink()
                    except OSError:
                        pass
                    return {
                        'action': 'skip',
                        'reason': 'target is append-only (immutable); compaction '
                                  'requires a rewrite the vault forbids by design',
                        'original': original_count,
                        'kept': original_count,
                        'dropped': 0,
                        'parse_errors': 0,
                    }
            finally:
                fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)

    return {
        'action': 'compact_telemetry',
        'original': original_count,
        'kept': len(kept_lines),
        'dropped': dropped,
        'parse_errors': parse_errors,
        'sources': len(by_source),
        'dry_run': dry_run,
    }


def compact_receipts(dry_run: bool = False) -> dict:
    """Archive old receipts, keep recent."""
    if not RECEIPTS.exists():
        return {'action': 'skip', 'reason': 'no_receipts'}

    lines = RECEIPTS.read_text().strip().split('\n')
    original_count = len(lines)

    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    cutoff_str = cutoff.isoformat()

    kept = []
    archived = []
    parse_errors = 0

    for line in lines:
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            ts = record.get('timestamp', '')
            if ts >= cutoff_str:
                kept.append(line)
            else:
                archived.append(line)
        except json.JSONDecodeError:
            parse_errors += 1
            kept.append(line)  # keep unparseable lines (don't lose data)

    if archived and not dry_run:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        archive_name = f"receipts-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.jsonl.gz"
        archive_path = ARCHIVE_DIR / archive_name
        with gzip.open(archive_path, 'wt') as f:
            f.write('\n'.join(archived) + '\n')

        lock_file = RECEIPTS.with_suffix(".lock")
        with open(lock_file, "w") as lock_fd:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
            try:
                tmp = RECEIPTS.with_suffix(".tmp")
                tmp.write_text('\n'.join(kept) + '\n' if kept else '')
                os.replace(tmp, RECEIPTS)
            finally:
                fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)

        # Reset the watermark state so the next run re-processes from scratch
        if RECEIPTS_STATE.exists():
            RECEIPTS_STATE.unlink()

    return {
        'action': 'compact_receipts',
        'original': original_count,
        'kept': len(kept),
        'archived': len(archived),
        'parse_errors': parse_errors,
        'retention_days': RETENTION_DAYS,
        'cutoff': cutoff_str,
        'archive': str(ARCHIVE_DIR / f"receipts-{datetime.now(timezone.utc).strftime('%Y%m%d')}*.gz") if archived else None,
        'dry_run': dry_run,
    }


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN Ledger Compaction')
    parser.add_argument('--dry-run', action='store_true', help='Show what would happen without writing')
    parser.add_argument('--telemetry-only', action='store_true')
    parser.add_argument('--receipts-only', action='store_true')
    args = parser.parse_args()

    results = {}

    if not args.receipts_only:
        results['telemetry'] = compact_telemetry(args.dry_run)
    if not args.telemetry_only:
        results['receipts'] = compact_receipts(args.dry_run)

    print(f"\n=== APEX-ZEN Compaction {'(DRY RUN)' if args.dry_run else ''} ===")
    for section, r in results.items():
        print(f"\n  {section}:")
        for k, v in r.items():
            print(f"    {k}: {v}")


if __name__ == '__main__':
    main()
