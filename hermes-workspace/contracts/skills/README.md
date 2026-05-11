# AAA Skill Packaging

This directory is the source-of-truth packaging layer for reusable AAA skills.

## Rule

- `registries/skills.yaml` stays as the compact skill index used across agents, bundles, and workflows.
- `contracts/skills/packages.yaml` is the packaging catalog that defines how each skill is sourced, installed, exported, tested, and version-locked.
- every skill in the registry must resolve to a package entry with the same canonical ID.

## Package responsibilities

Each skill package must declare:

1. metadata and risk
2. dependency edges
3. host compatibility
4. install hooks
5. source paths and runtime exports
6. examples and test handles
7. version locking for future JSON export

## Invariant

If a host can install a skill, AAA must know which package produced it and which files
belong to that package.
