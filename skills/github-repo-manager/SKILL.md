---
name: github-repo-manager
description: Manage GitHub repositories for arifOS ecosystem. Use when users ask to check repo status, sync repos, manage issues, create releases, track dependencies across arifOS/GEOX/arifosmcp/arif-sites/waw/agent-workbench/arifOS-model-registry/APEX repos, or perform GitHub operations for ariffazil's projects.
---

# GitHub Repository Manager for arifOS Ecosystem

Manage and orchestrate GitHub repositories in the arifOS ecosystem.

## Context

Owner: **ariffazil** (https://github.com/ariffazil)

### Primary Repositories

| Repo | Language | Purpose | License |
|------|----------|---------|---------|
| [arifOS](https://github.com/ariffazil/arifOS) | Python | Constitutional MCP kernel for governed AI execution. AAA architecture: Architect · Auditor · Agent | AGPL-3.0 |
| [GEOX](https://github.com/ariffazil/GEOX) | Python | Governed, agentic geological intelligence coprocessor for arifOS | AGPL-3.0 |
| [arifosmcp](https://github.com/ariffazil/arifosmcp) | Python | arifOS MCP Server — Constitutional Intelligence Kernel (deployable unit) | - |
| [arif-sites](https://github.com/ariffazil/arif-sites) | TypeScript | Trinity static sites — BODY (arif-fazil.com), SOUL (apex.arif-fazil.com), DOCS (arifos.arif-fazil.com) | - |
| [waw](https://github.com/ariffazil/waw) | TypeScript | OpenClaw workspace config for arifOS — AGENTS, SOUL, TOOLS, USER, IDENTITY, skills | AGPL-3.0 |
| [agent-workbench](https://github.com/ariffazil/agent-workbench) | TypeScript | arifOS Coding Agent CLI — TypeScript ESM package for constitutional agent operations | Private |
| [arifOS-model-registry](https://github.com/ariffazil/arifOS-model-registry) | Python | Governed self-reference frame for AI agents | - |
| [APEX](https://github.com/ariffazil/APEX) | HTML | The Physics of Governed Intelligence. Thermodynamic AI governance framework | CC0 |

## Supported Operations

### 1. Repository Status Overview
- List all repos with last update time
- Show commit activity
- Display open issues/PRs count
- Check for outdated dependencies

### 2. Repository Operations
- Clone repositories
- Pull latest changes
- Create/switch branches
- Commit and push changes
- Create pull requests

### 3. Issue Management
- List open issues
- Create new issues
- Add labels
- Close resolved issues

### 4. Release Management
- Create releases with changelog
- Upload release assets
- Manage release notes

### 5. Cross-Repository Coordination
- Track dependencies between repos
- Sync configuration across related repos
- Coordinate version releases

## Workflow

### Quick Status Check
```
1. Use GitHub API to fetch repo metadata
2. Display summary table of all repos
3. Highlight recently updated repos
4. Flag any issues needing attention
```

### Repository Sync
```
1. Clone/pull specified repos
2. Check for local changes
3. Pull remote updates
4. Resolve any merge conflicts
5. Report sync status
```

### Release Workflow
```
1. Determine version bump type (major/minor/patch)
2. Update CHANGELOG.md
3. Tag release
4. Create GitHub release
5. Publish to package registries if applicable
```

## Configuration

### GitHub Token
Set `GITHUB_TOKEN` environment variable for API access.

### Default Branches
- Primary: `main`
- Development: `develop` (if exists)

## Examples

**"Show status of all my repos"**
→ Fetch GitHub API, display repo overview table

**"Sync arifOS and arifosmcp"**
→ Clone/pull both repos, check for changes

**"Create a release for arifOS"**
→ Follow release workflow for version bump

**"Check for issues in GEOX"**
→ List open issues with labels and assignees

**"Update dependencies across all Python repos"**
→ Scan requirements.txt/pyproject.toml in each Python repo
