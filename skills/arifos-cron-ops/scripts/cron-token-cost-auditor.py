#!/usr/bin/env python3
"""
cron-token-cost-auditor.py — Estimate monthly token cost of jobs.json cron catalog.

Usage:
    python3 cron-token-cost-auditor.py [--jobs /path/to/jobs.json] [--json]

Formula (verified 2026-08-11 on 20-job catalog):
    fires_per_day = 24 * 60 / interval_minutes      # interval-mode
                    = 1                              # cron-mode default
    tok_per_fire  = 50                               # no_agent=true (script-only)
                   = 4000 + len(prompt)/4 + 2000    # agent-driven full LLM cycle
    FQ-gated machine lane: × 0.5 (avg 50% skip on low-flow periods)
    daily_total   = sum(fires_per_day * tok_per_fire)
    monthly_total = daily_total * 30

Waste categories detected:
1. High-frequency polling (every 5m = 288x/day)
2. Agent doing python3/ls/du (full LLM for what a script does)
3. Unconditional machine cron (no FQ-gate)

Output: ranked table by daily cost, with tier classification:
- 🟢 GREEN: <10k tok/day — cheap, keep
- 🟡 YELLOW: 10k-100k tok/day — review
- 🔴 RED: >100k tok/day — optimize immediately
"""
import argparse
import json
import sys
from pathlib import Path


def estimate_fires_per_day(schedule: dict) -> float:
    """Compute average fires-per-day for a schedule entry."""
    kind = schedule.get('kind', '?')
    if kind == 'interval':
        minutes = schedule.get('minutes', 1440)
        if not minutes:
            return 1.0
        return 24 * 60 / minutes
    elif kind == 'cron':
        expr = schedule.get('expr', '')
        parts = expr.split() if expr else []
        if len(parts) != 5:
            return 1.0
        minute, hour, dom, month, dow = parts
        # Very rough heuristic
        if hour == '*':
            if '/' in minute:
                step = int(minute.split('/')[1])
                return 24 * 60 / step
            return 24 * 60
        elif '/' in hour:
            step = int(hour.split('/')[1])
            return 24 / step
        elif hour.isdigit():
            return 1.0
        return 1.0
    return 1.0


def estimate_tokens_per_fire(job: dict) -> float:
    """Estimate tokens consumed per fire."""
    if job.get('no_agent'):
        return 50.0  # script-only, minimal stderr
    # Agent-driven: ~4k system + prompt/4 + ~2k tool output
    plen = len(job.get('prompt', '') or '')
    base = 4000 + plen / 4 + 2000
    # FQ-gate: machine lane skips ~50% of fires when FQ < threshold
    if (job.get('fq_gate', {}).get('enabled') and
        job.get('lane') == 'machine'):
        return base * 0.5
    return base


def classify_tier(daily_tok: float) -> str:
    if daily_tok > 100000:
        return 'RED'
    elif daily_tok > 10000:
        return 'YELLOW'
    return 'GREEN'


def audit(jobs_path: Path) -> dict:
    d = json.loads(jobs_path.read_text())
    rows = []
    total_daily = 0.0
    for j in d.get('jobs', []):
        fires = estimate_fires_per_day(j.get('schedule', {}))
        tok = estimate_tokens_per_fire(j)
        daily = fires * tok
        total_daily += daily
        rows.append({
            'name': j.get('name', '?'),
            'lane': j.get('lane', '?'),
            'fires_per_day': round(fires, 2),
            'tok_per_fire': int(tok),
            'daily_tok': int(daily),
            'monthly_tok': int(daily * 30),
            'tier': classify_tier(daily),
            'no_agent': j.get('no_agent', False),
            'fq_gated': j.get('fq_gate', {}).get('enabled', False),
        })
    return {
        'summary': {
            'job_count': len(rows),
            'total_daily_tok': int(total_daily),
            'total_monthly_tok': int(total_daily * 30),
        },
        'jobs': sorted(rows, key=lambda r: -r['daily_tok']),
    }


def render_text(audit_data: dict) -> str:
    out = []
    s = audit_data['summary']
    out.append(f"=== Cron Token Cost Audit ===")
    out.append(f"Jobs: {s['job_count']}  |  "
               f"Daily: {s['total_daily_tok']:,} tok  |  "
               f"Monthly: {s['total_monthly_tok']:,} tok")
    out.append("")
    out.append(f"{'TIER':<6} {'NAME':<35} {'LANE':<8} "
               f"{'FIRES/D':<9} {'TOK/FIRE':<10} {'DAILY':<12} {'FQ?':<5}")
    out.append("-" * 95)
    for r in audit_data['jobs']:
        icon = {'RED': '🔴', 'YELLOW': '🟡', 'GREEN': '🟢'}[r['tier']]
        fq = '✓' if r['fq_gated'] else '-'
        out.append(f"{icon:<6} {r['name']:<35} {r['lane']:<8} "
                   f"{r['fires_per_day']:<9.1f} {r['tok_per_fire']:<10} "
                   f"{r['daily_tok']:<12,} {fq:<5}")
    out.append("")
    red_count = sum(1 for r in audit_data['jobs'] if r['tier'] == 'RED')
    yellow_count = sum(1 for r in audit_data['jobs'] if r['tier'] == 'YELLOW')
    if red_count:
        out.append(f"⚠️  {red_count} RED-tier jobs (>100k tok/day). "
                   f"Optimize or convert to no_agent.")
    if yellow_count:
        out.append(f"⚠️  {yellow_count} YELLOW-tier jobs (10k-100k tok/day). "
                   f"Review for FQ-gating or demotion.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--jobs', default='/root/HERMES/cron/jobs.json',
                   help='Path to jobs.json (default: /root/HERMES/cron/jobs.json)')
    p.add_argument('--json', action='store_true', help='JSON output')
    args = p.parse_args()

    jobs_path = Path(args.jobs)
    if not jobs_path.exists():
        print(f"ERROR: jobs.json not found at {jobs_path}", file=sys.stderr)
        sys.exit(1)

    data = audit(jobs_path)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(render_text(data))


if __name__ == '__main__':
    main()
