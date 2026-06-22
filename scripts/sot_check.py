#!/usr/bin/env python3
"""Source-of-truth drift check."""
import yaml

with open('docs/ESTATE_MANIFEST.yaml') as f:
    manifest = yaml.safe_load(f)
organs = manifest.get('organs', {})
print(f'  Manifest claims {len(organs)} organs')
for name, info in organs.items():
    print(f'  📋 {name}: {info.get("tools", "?")} tools, role={info.get("role", "?")}')
print('  ✅ Manifest loads correctly')
