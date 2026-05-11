# arifOS Ecosystem Repository Reference

## Repository Architecture

```
arifOS Ecosystem
├── Core (Constitutional AI Kernel)
│   ├── arifOS              # Main kernel
│   ├── arifosmcp          # MCP Server deployment
│   └── arifOS-model-registry  # Model governance
├── Applications
│   ├── GEOX               # Geological intelligence
│   └── agent-workbench    # Coding agent CLI (Private)
├── Infrastructure
│   ├── waw                # OpenClaw workspace config
│   └── arif-sites         # Static sites
└── Research
    └── APEX               # Thermodynamic AI theory
```

## Dependency Graph

```
arifOS (core)
├── arifosmcp (depends on arifOS)
├── GEOX (integrates with arifOS)
├── waw (configures agents for arifOS)
└── agent-workbench (uses arifOS APIs)

arif-sites
├── apex.arif-fazil.com (APEX project site)
└── arifos.arif-fazil.com (Documentation)

arifOS-model-registry
└── Shared by all arifOS agents
```

## Technology Stack

| Repository | Primary Language | Framework | Package Manager |
|------------|-------------------|-----------|-----------------|
| arifOS | Python | MCP | pip/pyproject |
| GEOX | Python | - | pip |
| arifosmcp | Python | MCP Server | pip |
| arif-sites | TypeScript | Static Site | npm |
| waw | TypeScript | OpenClaw | npm |
| agent-workbench | TypeScript | CLI | npm |
| arifOS-model-registry | Python | - | pip |
| APEX | HTML | - | - |

## GitHub Workflows

### Standard Branch Strategy
- `main` - Production releases
- `develop` - Integration testing (if applicable)
- Feature branches: `feat/<feature-name>`

### Release Process
1. Update version in `__version__.py` or `pyproject.toml`
2. Update CHANGELOG.md with changes
3. Create git tag: `v<x.y.z>`
4. Create GitHub Release
5. Push to PyPI (Python repos) or npm (TypeScript repos)

### Commit Convention
```
<type>(<scope>): <description>

Types: feat, fix, docs, refactor, test, chore
Scopes: os, mcp, geo, sites, waw, bench, registry, apex
```
