#!/usr/bin/env python3
"""S1 — the placement tag, as data rather than a risky bulk move.

Why not move: `hermes update` re-seeds bundled skills at the updater's one-level path,
so moving those creates duplicates the updater keeps undoing; and 472 of the 509
storage skills are NOT in .bundled_manifest, so "tag as bundled" is factually wrong
for them. What is left is the honest action: publish, per skill, where it actually
lives, which generation of layout it sits in, whether its body is even held here,
and which address already points at it. One artifact, machine-readable, version
controlled. Moves then happen per entry, on touch, with a receipt.

Writes /root/AAA/skills/PLACEMENT_MANIFEST.json (read-only with respect to skills).
"""
import os, json, collections

A = '/root/AAA/skills'
H = '/root/.hermes/skills'
OUT = os.path.join(A, 'PLACEMENT_MANIFEST.json')
EXCL = {'.git', '.archive', '.system', '__pycache__', 'references', 'templates',
        'assets', 'scripts', '.archive-20260912', '.curator_backups', '.hub',
        'node_modules', '.venv'}

bundled = set()
with open(os.path.join(H, '.bundled_manifest')) as f:
    for line in f:
        if ':' in line:
            bundled.add(line.split(':', 1)[0].strip())

# addresses already published in the addressing tree
address_of = {}
for dp, dn, fn in os.walk(H, followlinks=True):
    rel = os.path.relpath(dp, H)
    if EXCL.intersection(set(rel.split(os.sep))):
        dn[:] = []
        continue
    if 'SKILL.md' in fn:
        address_of.setdefault(os.path.basename(os.path.realpath(dp)), rel)

rows = collections.OrderedDict()


def add(name, rel, kind, is_link, target):
    body_here = not is_link or (target or '').startswith(A + os.sep)
    rows[name] = dict(
        storage=os.path.join(A, rel), rel=rel, generation=kind,
        bundled=name in bundled,
        body_held_here=body_here,
        borrowed_from=None if body_here else target,
        address=address_of.get(name),
        placed=bool(address_of.get(name)),
    )


for dp, dn, fn in os.walk(A, followlinks=False):
    if EXCL.intersection(set(dp.split(os.sep))):
        dn[:] = []
        continue
    if 'SKILL.md' in fn:
        rel = os.path.relpath(dp, A)
        parts = rel.split(os.sep)
        kind = 'flat-root' if len(parts) == 1 else ('taxonomy' if parts[0] == 'domains' else 'bucket')
        add(os.path.basename(dp), rel, kind, False, None)

for e in sorted(os.listdir(A)):
    p = os.path.join(A, e)
    if os.path.islink(p) and os.path.exists(os.path.join(p, 'SKILL.md')):
        add(e, e, 'flat-root', True, os.path.realpath(p))

kinds = collections.Counter(r['generation'] for r in rows.values())
summary = dict(
    rule=('a placement tag, not a move: bundled skills keep the updater path, moved skills '
          'move one at a time with a receipt'),
    total_storage_skills=len(rows),
    generations=dict(kinds),
    bundled_in_manifest=sum(1 for r in rows.values() if r['bundled']),
    authored_not_in_bundled_manifest=sum(1 for r in rows.values() if not r['bundled']),
    body_borrowed_outside_canonical=sum(1 for r in rows.values() if not r['body_held_here']),
    placed=sum(1 for r in rows.values() if r['placed']),
    unplaced=sum(1 for r in rows.values() if not r['placed']),
)
json.dump({**summary, 'skills': rows}, open(OUT, 'w'), indent=1)

print(json.dumps(summary, indent=1))
print('\nborrowed bodies (canonical holds a link, not a body):')
for n, r in sorted(rows.items()):
    if not r['body_held_here']:
        print(f"   {n:<40} -> {r['borrowed_from']}")
print('\ngeneration sample (bucket):')
seen = set()
for n, r in sorted(rows.items()):
    if r['generation'] == 'bucket' and r['rel'].split(os.sep)[0] not in seen:
        seen.add(r['rel'].split(os.sep)[0])
        print(f"   {r['rel'].split(os.sep)[0]:<22} e.g. {n}")
print(f"\nwrote {OUT}")
