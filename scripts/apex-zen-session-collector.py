#!/usr/bin/env python3
"""
APEX-ZEN Session Collector — wires telemetry to live session feeds.

Reads session JSONL files, extracts conversation text, runs telemetry,
appends results to /root/VAULT999/apex-zen-telemetry.jsonl.

Doctrine ref: /root/AAA/governance/APEX-ZEN-EXECUTION-DOCTRINE.md § 13
"""
import json
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

DEFAULT_SESSIONS_DIR = Path('/root/.kimi-code/sessions')
TELEMETRY_OUTPUT = Path('/root/VAULT999/apex-zen-telemetry.jsonl')
COLLECTOR_STATE = Path('/root/VAULT999/apex-zen-collector-state.json')
TELEMETRY_SCRIPT = Path('/root/AAA/scripts/apex-zen-telemetry.py')


def get_processed_files() -> set:
    if COLLECTOR_STATE.exists():
        try:
            return set(json.loads(COLLECTOR_STATE.read_text()).get('processed', []))
        except (json.JSONDecodeError, OSError):
            return set()
    return set()


def save_processed_files(processed: set) -> None:
    COLLECTOR_STATE.parent.mkdir(parents=True, exist_ok=True)
    COLLECTOR_STATE.write_text(json.dumps({
        'processed': sorted(processed),
        'updated_at': datetime.now(timezone.utc).isoformat(),
        'total_processed': len(processed),
    }))


def find_session_files(sessions_dir: Path, since: timedelta | None = None) -> list:
    if not sessions_dir.exists():
        return []
    files = list(sessions_dir.rglob('*.jsonl'))
    if since is None:
        return files
    cutoff = datetime.now(timezone.utc) - since
    result = []
    for f in files:
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            if mtime >= cutoff:
                result.append(f)
        except OSError:
            continue
    return result


def extract_conversation(session_path: Path) -> str:
    """Extract conversation text from session JSONL — calibrated.
    Filters: type=context.append_message, role=user|assistant, origin not injection.
    Dedupes by message id. Strips <system-reminder> blocks.
    """
    import re as _re
    texts = []
    seen_ids = set()
    try:
        content = session_path.read_text(errors='ignore')
    except OSError:
        return ''
    for line in content.splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Artifact signal: surface mutating tool calls for the artifact counter
        if record.get('type') == 'context.append_loop_event':
            ev = record.get('event') or {}
            if ev.get('type') == 'tool.call':
                name = str(ev.get('name') or '')
                low = name.lower()
                if low in ('edit', 'write', 'multiedit', 'notebookedit', 'apply_patch'):
                    texts.append(f'[TOOL_ARTIFACT: {name}]')
                elif low == 'bash':
                    cmd = str((ev.get('args') or {}).get('command') or '')
                    if any(k in cmd for k in ('git commit', 'git push', 'apply_patch', 'git apply')):
                        texts.append('[TOOL_ARTIFACT: Bash-git]')
            continue

        # Only context.append_message records
        if record.get('type') != 'context.append_message':
            continue

        msg = record.get('message') or {}
        role = msg.get('role', '')
        if role not in ('user', 'assistant', 'human'):
            continue

        # Skip system-injected context (date reminders, AGENTS.md auto-load, etc.)
        origin = msg.get('origin') or {}
        if isinstance(origin, dict) and origin.get('kind') == 'injection':
            continue

        # Dedup by id
        msg_id = record.get('id') or msg.get('id')
        if msg_id:
            if msg_id in seen_ids:
                continue
            seen_ids.add(msg_id)

        # Extract text parts from content array
        c = msg.get('content') or ''
        if isinstance(c, list):
            for part in c:
                if isinstance(part, dict) and part.get('type') == 'text':
                    text = part.get('text', '')
                    # Strip <system-reminder>...</system-reminder> blocks
                    text = _re.sub(r'<system-reminder>.*?</system-reminder>', '', text, flags=_re.DOTALL)
                    text = _re.sub(r'<git-context[^/]*/>', '', text)
                    text = text.strip()
                    if text:
                        texts.append(text)
        elif isinstance(c, str):
            text = _re.sub(r'<system-reminder>.*?</system-reminder>', '', c, flags=_re.DOTALL)
            text = text.strip()
            if text:
                texts.append(text)

        # Extract tool calls — emit synthetic lines for artifact detection
        ARTIFACT_TOOLS = {'Edit', 'Write', 'MultiEdit', 'Create', 'NotebookEdit'}
        tool_calls = msg.get('toolCalls') or msg.get('tool_calls') or []
        if isinstance(tool_calls, list):
            for tc in tool_calls:
                if isinstance(tc, dict):
                    name = tc.get('name') or tc.get('tool') or ''
                    if isinstance(tc.get('function'), dict):
                        name = name or tc['function'].get('name', '')
                    if name in ARTIFACT_TOOLS:
                        # Try to extract file path for richer signal
                        args = tc.get('input') or tc.get('args') or tc.get('function', {}).get('arguments', {}) or {}
                        file_path = args.get('file_path') or args.get('path') or args.get('notebook_path') or ''
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                                file_path = args.get('file_path') or args.get('path') or ''
                            except (json.JSONDecodeError, TypeError):
                                pass
                        texts.append(f"tool_call: {name} {file_path}".strip())
    return '\n'.join(texts)


def run_telemetry(source: str, text: str) -> int:
    """Run apex-zen-telemetry.py on extracted text via subprocess."""
    TELEMETRY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ['python3', str(TELEMETRY_SCRIPT),
             '--stdin', '--quiet', '--output', str(TELEMETRY_OUTPUT)],
            input=text, capture_output=True, text=True, timeout=120
        )
        return result.returncode
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  telemetry error: {e}")
        return -1


def parse_since(s: str) -> timedelta:
    unit = s[-1]
    value = int(s[:-1])
    return {'h': timedelta(hours=value), 'd': timedelta(days=value), 'm': timedelta(minutes=value)}[unit]


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN Session Collector')
    parser.add_argument('--sessions-dir', default=str(DEFAULT_SESSIONS_DIR))
    parser.add_argument('--since', help='Time window: e.g., 1h, 24h, 7d')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--limit', type=int, default=50, help='Max files per run')
    args = parser.parse_args()

    sessions_dir = Path(args.sessions_dir)
    since = parse_since(args.since) if args.since else None

    processed = get_processed_files()
    files = find_session_files(sessions_dir, since)
    new_files = [f for f in files if str(f) not in processed][:args.limit]

    print(f"[collector] sessions_dir={sessions_dir}")
    print(f"[collector] found={len(files)} new={len(new_files)} already_processed={len(processed)}")

    if not new_files:
        print("[collector] nothing new to process")
        return

    if args.dry_run:
        for f in new_files[:5]:
            print(f"  would process: {f.name}")
        return

    success = 0
    for session_path in new_files:
        text = extract_conversation(session_path)
        if not text.strip():
            processed.add(str(session_path))
            continue
        rc = run_telemetry(str(session_path), text)
        processed.add(str(session_path))
        if rc == 0:
            success += 1

    save_processed_files(processed)
    print(f"[collector] processed {success}/{len(new_files)} new files")
    print(f"[collector] telemetry → {TELEMETRY_OUTPUT}")


if __name__ == '__main__':
    main()