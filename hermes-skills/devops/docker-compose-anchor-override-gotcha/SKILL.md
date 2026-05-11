---
name: docker-compose-anchor-override-gotcha
description: Docker Compose YAML anchor override gotcha — << merge key already defined error when using anchors with per-service overrides
triggers:
  - "yaml construct errors mapping key already defined"
  - "docker-compose yaml >> already defined"
  - "yaml merge key duplicate"
category: devops
---

# Docker Compose YAML Anchor Override Gotcha

## Problem
When using YAML anchors with Docker Compose merge keys (`<<: *anchor`), you cannot
override individual sub-keys in a service — the entire anchor must be referenced
once, and you cannot merge the same key twice.

## Error
```
yaml: construct errors
line 13: line 54: mapping key "<<" already defined at line 36
```

## Root Cause
If you define `x-resource-limits: &resource-limits` with `mem_limit: 512m` and
`x-log-config: &log-config` with `logging: {driver: json-file}`, then use both in
a service:

```yaml
services:
  loki:
    <<: *resource-limits    # line 36 — defines mem_limit
    mem_limit: 512m          # line 13 — OK, no conflict
    <<: *log-config          # line 54 — CONFLICT: << already defined at line 36
```

The `<<` merge key can only appear ONCE per mapping. Even though the actual values
are different (mem_limit vs logging), the YAML merge operator itself is a duplicate
mapping key.

## Solution
Expand anchors inline per service instead of using merge keys for multiple
annotations:

```yaml
services:
  loki:
    # Expanded from x-resource-limits
    mem_limit: 512m
    memswap_limit: 512m
    pids_limit: 128
    # Expanded from x-log-config
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

OR use a single anchor that combines all shared fields:

```yaml
x-shared: &shared
  mem_limit: 512m
  logging:
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"

services:
  loki:
    <<: *shared
    # override specific values
    mem_limit: 256m
```

## Never Do These
- Use `<<: *anchor1` then `<<: *anchor2` in the same service mapping
- Use multiple YAML merge keys in a single mapping block

## Trigger
When writing docker-compose.yml with multiple annotation anchors (x-*) and
services that need to use more than one anchor.
