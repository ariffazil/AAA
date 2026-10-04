#!/usr/bin/env python3
"""
opencode-dynamic-builder.py — Build opencode.json from dynamic registry.

DOCTRINE: No static literals in arifOS substrate. Every dynamic value
flows from this registry, not from hardcoded config.

Usage:
    python3 opencode-dynamic-builder.py           # build to stdout
    python3 opencode-dynamic-builder.py --apply    # write to opencode.json
    python3 opencode-dynamic-builder.py --diff      # show diff vs current

Forged: 2026-08-12 by F13 Sovereign Override.
"""

import json
import os
import sys
import argparse
from datetime import datetime

REGISTRY_PATH = os.environ.get(
    'OPENCODE_REGISTRY',
    os.path.expanduser('~/.config/opencode/dynamic-registry.yaml')
)
CURRENT_CONFIG = os.path.expanduser('~/.config/opencode/opencode.json')


def load_registry():
    """Load the dynamic registry (JSON or YAML)."""
    with open(REGISTRY_PATH) as f:
        if REGISTRY_PATH.endswith('.json'):
            return json.load(f)
        else:
            try:
                import yaml
                return yaml.safe_load(f)
            except ImportError:
                # Fallback: JSON-only registry
                return json.load(f)


def build_config(reg):
    """Build opencode.json from registry values."""
    cfg = {}

    # D1: MODELS — from registry, never hardcoded
    cfg['model'] = reg['models']['primary']
    cfg['small_model'] = reg['models']['small']

    # D1: Providers — fully data-driven
    cfg['provider'] = {}
    for prov_name, prov_data in reg['models']['providers'].items():
        cfg['provider'][prov_name] = {
            "npm": prov_data.get('npm', prov_name),
            "name": prov_name,
            "options": {},
            "models": {m: {} for m in prov_data.get('models', [])}
        }

    cfg['enabled_providers'] = list(reg['models']['providers'].keys())
    cfg['default_agent'] = '333-AGI'

    # D2+D3: MCP SERVERS — ports from registry, URLs templated
    cfg['mcp'] = {}
    ports = reg['network']['ports']
    localhost = reg['network']['localhost']

    for mcp_name, mcp_data in reg['mcp']['servers'].items():
        if mcp_data['type'] == 'http':
            cfg['mcp'][mcp_name] = {
                'type': 'http',
                'url': mcp_data.get(
                    'url_full',
                    f'http://{localhost}:{ports.get(mcp_name, "8080")}/mcp'
                )
            }
        elif mcp_data['type'] == 'stdio':
            cfg['mcp'][mcp_name] = {
                'type': 'local',
                'command': mcp_data.get('command'),
                'args': mcp_data.get('args', []),
            }

    # D4: HUMAN — permission from registry
    cfg['permission'] = {
        '*': reg['human'].get('permission_default', 'allow')
    }

    # D5: THRESHOLDS — from registry
    cfg['compaction'] = reg['thresholds'].get(
        'compaction', {'auto': True, 'prune': True}
    )
    cfg['subagent_depth'] = reg['thresholds'].get('subagent_depth', 3)
    cfg['autoupdate'] = False

    # D6: PATHS — canonical instruction paths from registry
    cfg['instructions'] = reg['paths'].get('instructions', [])
    cfg['plugin'] = reg['paths'].get('plugins', [])

    # INVARIANT — static, not dynamic
    cfg['$schema'] = 'https://opencode.ai/config.json'
    cfg['lsp'] = True
    cfg['formatter'] = True

    # Agent configs
    cfg['agent'] = {
        '333-AGI': {
            'model': reg['models']['primary'],
            'mode': 'subagent'
        },
        '555-ASI': {
            'model': reg['models']['primary'],
            'mode': 'subagent'
        },
        '777-FORGE': {
            'model': reg['models']['small'],
            'mode': 'subagent'
        },
        '888-APEX': {
            'model': reg['models']['primary'],
            'mode': 'subagent'
        }
    }

    cfg['command'] = {
        'init': {'file': 'command/init.md'},
        'seal': {'file': 'command/seal.md'}
    }

    cfg['references'] = {
        'registry': REGISTRY_PATH,
        'secrets': '/root/.secrets/kunci-mas.env',
        'skills': '/root/AAA/skills/',
        'scars': '/root/memory/H5-scars/'
    }

    return cfg


def main():
    parser = argparse.ArgumentParser(
        description='Build opencode.json from dynamic registry'
    )
    parser.add_argument(
        '--apply', action='store_true',
        help='Write to opencode.json'
    )
    parser.add_argument(
        '--diff', action='store_true',
        help='Show diff vs current config'
    )
    args = parser.parse_args()

    reg = load_registry()
    new_cfg = build_config(reg)

    if args.apply:
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        if os.path.exists(CURRENT_CONFIG):
            backup = f'{CURRENT_CONFIG}.bak-dynamic-{ts}'
            os.rename(CURRENT_CONFIG, backup)
            print(f'Backup: {backup}')

        with open(CURRENT_CONFIG, 'w') as f:
            json.dump(new_cfg, f, indent=2, ensure_ascii=False)

        print(f'Written: {CURRENT_CONFIG}')
        print(f'Registry: {REGISTRY_PATH}')

    elif args.diff:
        try:
            with open(CURRENT_CONFIG) as f:
                current = json.load(f)
        except FileNotFoundError:
            print('No existing config to diff against.')
            sys.exit(1)

        all_keys = set(list(current.keys()) + list(new_cfg.keys()))
        changed = 0
        for key in sorted(all_keys):
            old_val = current.get(key, '<MISSING>')
            new_val = new_cfg.get(key, '<REMOVED>')
            if old_val != new_val:
                changed += 1
                old_s = json.dumps(old_val, ensure_ascii=False)[:60]
                new_s = json.dumps(new_val, ensure_ascii=False)[:60]
                print(f'  {key:20s} {old_s} -> {new_s}')

        print(f'\n{changed} keys changed out of {len(all_keys)} total')

    else:
        print(json.dumps(new_cfg, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
