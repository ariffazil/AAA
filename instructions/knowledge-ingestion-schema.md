# Unified Knowledge Ingestion Schema (Braindump & URL-Dump)

> **PURPOSE:** Standardize frontmatter metadata across all notes, web captures, and braindumps for automated ingestion into **VAULT999**, **FalkorDB**, and **Qdrant**.

## 1. Braindump Frontmatter Template

```yaml
---
type: braindump
id: "bd-YYYYMMDD-HHMMSS"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
author: "Arif Fazil"
status: "raw | triaged | crystallized"
domain: "arifos | geox | wealth | well | aaa | personal"
tags:
  - second-brain
  - strategy
falkor_nodes:
  - "EntityName"
confidence: 1.0
last_verified: "YYYY-MM-DDTHH:MM:SSZ"
---

# Title / Summary

Raw content here...
```

## 2. URL-Dump Frontmatter Template

```yaml
---
type: url_dump
id: "url-YYYYMMDD-HHMMSS"
url: "https://example.com/source"
title: "Article or Resource Title"
captured_at: "YYYY-MM-DDTHH:MM:SSZ"
distilled_insights:
  - "Key takeaway 1"
  - "Key takeaway 2"
tags:
  - reference
  - external-intelligence
ingested_into:
  vault999: true
  falkordb: true
  qdrant: true
---

# Summary & Core Quotations

Distilled content...
```
