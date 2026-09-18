#!/usr/bin/env python3
"""apex-zen conformance survey over the canonical skill home.

Measures, per SKILL.md, which of the Seven Laws (agi-asi-skills-fundamentals)
the artifact can currently prove. Read-only. No mutation.

Outputs JSON to stdout and to /root/AAA/reports/apex-zen-skill-survey-20260918.json
"""
import os, re, json, hashlib, collections, datetime

HOME = '/root/AAA/skills'
OUT = '/root/AAA/reports/apex-zen-skill-survey-20260918.json'
EXCL = {'.git', '.archive', '.system', '__pycache__', 'references', 'templates', 'assets', 'scripts', 'node_modules'}

FM = re.compile(r'^---\s*\n(.*?)\n---', re.S)

# Law 4 FULL — side effect class, blast radius, reversibility, may-not list
L4_FULL = ('side_effect', 'side-effect', 'effect_class', 'consequence_class', 'blast_radius',
           'reversibility', 'undo', 'may_not', 'may-not', 'maynot')
# Law 4 PARTIAL — the weaker proxy fields already widespread in this library
L4_PARTIAL = ('risk_tier', 'autonomy_tier', 'floor_scope', 'authority_tier')
L4_FIELDS = L4_FULL + L4_PARTIAL
# Law 7 — provenance / verification / kill
L7_FIELDS = ('forged', 'provenance', 'owner', 'supersedes', 'last_verified', 'verified',
             'kill', 'kill_criterion', 'expires', 'sunset')

def parse(p):
    txt = open(p, encoding='utf-8', errors='replace').read()
    m = FM.match(txt)
    fm = m.group(1) if m else ''
    keys = {}
    for line in fm.splitlines():
        mm = re.match(r'^([A-Za-z_][A-Za-z0-9_\-]*)\s*:', line)
        if mm:
            keys[mm.group(1).lower()] = True
    return keys, fm, txt

rows = []
for dp, dn, fn in os.walk(HOME):
    dn[:] = [d for d in dn if d not in EXCL]
    if 'SKILL.md' not in fn:
        continue
    p = os.path.join(dp, 'SKILL.md')
    keys, fm, txt = parse(p)
    desc = ''
    md = re.search(r'^description:\s*(.*?)(?=\n[a-z_]+:|\n---)', fm, re.S | re.M)
    if md:
        desc = ' '.join(md.group(1).split())
    if not desc:
        md = re.search(r'^description:\s*(.+)$', fm, re.M)
        desc = md.group(1).strip() if md else ''
    rows.append(dict(
        skill=os.path.basename(dp), rel=os.path.relpath(dp, HOME),
        sha=hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12],
        window=desc[:57].lower(),
        l4_full=any(k in keys for k in L4_FULL),
        l4_partial=any(k in keys for k in L4_PARTIAL),
        l7_owner='owner' in keys,
        l7_forged='forged' in keys,
        l7_verified=any(k in keys for k in ('last_verified', 'verified')),
        l7_kill=any(k in keys for k in ('kill', 'kill_criterion', 'expires', 'sunset')),
    ))

n = len(rows)
r_full = sum(r['l4_full'] for r in rows)
r_part = sum(r['l4_partial'] for r in rows)
r_owner = sum(r['l7_owner'] for r in rows)
r_forged = sum(r['l7_forged'] for r in rows)
r_ver = sum(r['l7_verified'] for r in rows)
r_kill = sum(r['l7_kill'] for r in rows)

win = collections.Counter(r['window'] for r in rows if r['window'])
clusters = {w: c for w, c in win.items() if c > 1}
rows_in = sum(clusters.values())
openers = collections.Counter()
for r in rows:
    openers[re.sub(r'\s+', ' ', r['window'][:20]).strip()] += 1

report = dict(
    generated=datetime.datetime.now(datetime.UTC).isoformat(),
    home=HOME, total_skills=n,
    law4_full_consequence_class=r_full, law4_partial_proxy=r_part, law4_absent=n - r_part - (r_full if r_full else 0),
    law7_owner=r_owner, law7_forged=r_forged,
    law7_last_verified=r_ver, law7_kill_criterion=r_kill,
    law5_duplicate_57char_windows=len(clusters),
    law5_skills_in_collision_clusters=rows_in,
    law5_no_description=sum(1 for r in rows if not r['window']),
)
json.dump({**report, 'rows': rows,
           'collision_clusters': [{'window': w, 'count': c} for w, c in sorted(clusters.items(), key=lambda x: -x[1])[:40]],
           'top_openers': openers.most_common(15)},
          open(OUT, 'w'), indent=1)

print(json.dumps(report, indent=1))
print('\ntop 57-char collision windows:')
for w, c in sorted(clusters.items(), key=lambda x: -x[1])[:15]:
    print(f'  {c:>3}x  "{w}"')
print('\nskills with NO Law-4 field of any kind (first 30):')
miss = [r['skill'] for r in rows if not (r['l4_full'] or r['l4_partial'])]
print(f'  count={len(miss)}')
print('  ' + ', '.join(miss[:30]))
print(f'\nwrote {OUT}')
