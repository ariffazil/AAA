---
name: arifos-external-api-mcp-tool
description: Wire an external API (Google Maps, weather, flight tracker, etc.) as an MCP tool in arifOS so Hermes can call it — key in env, handler in tools.py, registered in CANONICAL_TOOLS. Discovered 2026-05-08 during Google Maps spatial intelligence integration.
category: devops
tags: [arifOS, MCP, Google-Maps, external-API, tool-expansion]
---

# arifOS External API → MCP Tool Integration Pattern

## Trigger

When you want Hermes/ASI to call an external API (Google Maps, weather, flight tracker, etc.) through arifOS MCP tools — without exposing the API key to the agent, without rebuilding the Docker image, and following arifOS constitutional governance.

**Core principle:** Hermes knows the tool, not the secret. The key lives in env vars inside the container.

## Architecture

```
Hermes (ASI reasoning)
    ↓ AAA Protocol / A2A
arifOS MCP (arif_spatial_* tool)
    ↓ os.getenv("GOOGLE_MAPS_API_KEY")
Google Maps API (Places, Routes, Geocoding)
    ↓
Structured result back to Hermes (no raw key)
```

## Prerequisites Discovered

1. **arifOS container uses `env_file: [.env]`** from `/root/compose/.env` — env vars are injected at container boot
2. **tools.py is bind-mounted** into the running container via compose:
   ```
   /root/arifOS/arifosmcp/runtime/tools.py → /app/arifosmcp/runtime/tools.py:ro
   ```
   Editing the source file on disk immediately affects the running container (no rebuild needed)
3. **CANONICAL_TOOLS** in `constitutional_map.py` controls what appears on the MCP surface — tools must be registered there to be discoverable
4. **Compose `.env`** is the correct place for API keys — NOT in git, NOT in prompt files, NOT in chat

## Step-by-Step Implementation

### Step 1 — Add API key to compose `.env`

```bash
sudo nano /root/compose/.env
```

Add:
```
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX
```

Restart container to pick up:
```bash
cd /root/compose
docker compose restart arifosmcp
```

Verify:
```bash
docker exec arifosmcp env | grep GOOGLE
# Expected: GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 2 — Implement tool handlers in `tools.py`

File: `/root/arifOS/arifosmcp/runtime/tools.py`

Add handlers using the standard async pattern. Example for Places Nearby Search:

```python
import os, json, urllib.request, urllib.parse

async def handle_arif_spatial_places_nearby(
    location: str,   # "7.0128,100.5408"
    radius: int = 1000,
    keyword: str = None,
    type: str = None,
) -> dict:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not configured", "status": "CONFIG_ERROR"}
    
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": location, "radius": radius, "key": api_key}
    if keyword: params["keyword"] = keyword
    if type: params["type"] = type
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            result = json.loads(r.read())
    except Exception as e:
        return {"error": str(e), "status": "API_ERROR"}
    
    if result.get("status") != "OK":
        return {"error": result.get("status"), "status": "API_ERROR"}
    
    return {
        "status": "OK",
        "count": len(result.get("results", [])),
        "places": [
            {
                "name": p.get("name"),
                "place_id": p.get("place_id"),
                "lat": p["geometry"]["location"]["lat"],
                "lng": p["geometry"]["location"]["lng"],
                "rating": p.get("rating"),
                "open_now": p.get("opening_hours", {}).get("open_now"),
                "vicinity": p.get("vicinity"),
                "types": p.get("types", []),
            }
            for p in result.get("results", [])[:5]
        ]
    }
```

Same pattern for:
- `handle_arif_spatial_route_compute` → Routes API
- `handle_arif_spatial_place_details` → Place Details API
- `handle_arif_spatial_geocode` → Geocoding API

### Step 3 — Register in CANONICAL_TOOLS

File: `/root/arifOS/arifosmcp/constitutional_map.py`

Add to `CANONICAL_TOOLS` dict (keep alphabetical order):

```python
"arif_spatial_places_nearby": {
    "stage": "111",
    "lane": "AGI",
    "floors": ["F02", "F03", "F07"],  # TRUTH, WITNESS, HUMILITY
    "access": "public",
    "risk_tier": "low",
    "irreversible": False,
    "description": "Find places near a lat/lng using Google Places API",
},
"arif_spatial_route_compute": {
    "stage": "333",
    "lane": "AGI",
    "floors": ["F02", "F07", "F08"],
    "access": "public",
    "risk_tier": "low",
    "irreversible": False,
    "description": "Compute driving/walking route via Google Routes API",
},
```

### Step 4 — Register handlers in tools.py

In `tools.py`, add to `_CANONICAL_HANDLERS` dict:

```python
_CANONICAL_HANDLERS = {
    # ... existing handlers ...
    "arif_spatial_places_nearby": handle_arif_spatial_places_nearby,
    "arif_spatial_route_compute": handle_arif_spatial_route_compute,
    "arif_spatial_place_details": handle_arif_spatial_place_details,
}
```

### Step 5 — Add trigger rules to Hermes USER profile

Add a `## Spatial Intelligence Triggers` block in USER profile:

```markdown
## Spatial Intelligence Triggers

When Arif asks about:
- "nearby" / "around me" / "close to" / "nearest" → call `arif_spatial_places_nearby`
- "route to" / "how far" / "drive time" / "directions" → call `arif_spatial_route_compute`
- "what is this place" / "details of" / "reviews for" → call `arif_spatial_place_details`

NEVER fabricate coordinates, distances, or place names when these tools are available.
If the tool returns error, say "I couldn't reach the maps service" — do not guess.
```

### Step 6 — Verify

Test the tool directly:
```bash
curl -s "http://127.0.0.1:8080/mcp" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "arif_spatial_places_nearby",
      "arguments": {"location": "7.0128,100.5408", "radius": 2000, "type": "restaurant", "keyword": "halal"}
    }
  }'
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `/root/compose/.env` | API key storage (container reads at boot) |
| `/root/arifOS/arifosmcp/runtime/tools.py` | Tool handler implementations |
| `/root/arifOS/arifosmcp/constitutional_map.py` | CANONICAL_TOOLS registry |
| `/root/arifOS/arifOSMCP/tool_registry.json` | Auto-generated (do not edit manually) |

## Google Maps API Quick Reference

| API | Endpoint | Use Case |
|-----|----------|----------|
| Places Nearby Search | `.../place/nearbysearch/json` | "restaurants near me" |
| Places Text Search | `.../place/textsearch/json` | "best coffee shop Hat Yai" |
| Place Details | `.../place/details/json` | "reviews for this place" |
| Routes Compute Routes | `.../routes.googleapis.com/directions/v2:computeRoutes` | Route with traffic/tolls |
| Geocoding | `.../geocode/json` | lat/lng ↔ address |

**Routes API replaced Directions API + Distance Matrix as of March 2025.**
