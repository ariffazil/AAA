---
name: mapbox-cartography-gis
description: Mapbox developer API suite, cartographic design, style management, GeoJSON validation/preview, coordinate conversion, and token security via Mapbox DevKit MCP server (mcp-devkit.mapbox.com).
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Mapbox Cartography & GIS Developer Skill (`mapbox`)

This skill provides direct access to Mapbox Developer APIs, style building, GeoJSON validation/previews, token management, color contrast checking, and coordinate reference system conversion via `https://mcp-devkit.mapbox.com/mcp`.

## Available Tools & Signatures

### 1. Style Management Tools

- `ListStylesTool`: Lists all styles for a Mapbox account.
- `CreateStyleTool`: Creates a new Mapbox style from specification JSON.
- `RetrieveStyleTool` / `UpdateStyleTool` / `DeleteStyleTool`: Manages styles by ID.
- `PreviewStyleTool`: Generates interactive browser preview URLs for Mapbox styles.
- `ValidateStyleTool`: Performs offline validation of Mapbox style JSON against style specification.
- `compare_styles_tool`: Deep diff comparison between two Mapbox styles.
- `Style Optimization tool`: Removes unused sources, duplicate layers, and empty layers to optimize style payload size.

### 2. GeoJSON & Local Processing Tools

- `GeoJSON Preview tool`: Generates a geojson.io URL for instant visualization.
- `Validate GeoJSON tool`: Offline validation of GeoJSON structure, coordinate bounds, ring closure, and feature properties.
- `Validate Expression tool`: Validates Mapbox GL JS expressions syntax, operators, and return types.
- `Coordinate Conversion tool`: Converts coordinates between WGS84 (`EPSG:4326`) and Web Mercator (`EPSG:3857`).
- `Bounding Box tool`: Calculates GeoJSON bounding box `[minX, minY, maxX, maxY]`.
- `Color Contrast Checker tool`: Checks WCAG 2.1 compliance (AA/AAA) for map text foreground and background colors.

### 3. Token Management Tools

- `create-token`: Creates access tokens with granular scopes (`styles:read`, `styles:write`, `fonts:read`, etc.) and URL restrictions.
- `list-tokens`: Lists access tokens with usage filtering.

---

## Usage Guidelines & Best Practices

1. **Token Security**: Always specify `allowedUrls` when creating tokens for browser deployments.
2. **WCAG Compliance**: Run `Color Contrast Checker tool` on custom font/label paint properties to ensure map text meets WCAG AA standards.
3. Requires `MAPBOX_ACCESS_TOKEN` with appropriate scopes (`styles:read`, `styles:write`, `tokens:read`).
