#!/usr/bin/env python3
"""
nav-kuala-lumpur — KL Transit Router
BFS shortest-path routing on station graph.
Usage: python kl_transit_router.py "Serdang" "TRX"
"""
import sys
import yaml
from collections import deque
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
STATIONS_YAML = SKILL_DIR / "references" / "kl_stations.yaml"


def load_data():
    with open(STATIONS_YAML) as f:
        data = yaml.safe_load(f)
    return data["stations"], data.get("lines", {})


def normalize(s: str) -> str:
    """Slugify: lowercase, collapse whitespace."""
    return "_".join(s.lower().strip().split())


def find_station(query: str, stations: dict) -> tuple[str, dict] | None:
    """Fuzzy find station by name or alias. Returns (station_key, info_dict)."""
    q = normalize(query)
    # Exact name match
    if q in stations:
        return q, stations[q]
    # Alias match
    for name, info in stations.items():
        if q in [normalize(a) for a in info.get("aliases", [])]:
            return name, stations[name]
        if normalize(info["code"]) == q:
            return name, stations[name]
    # Partial match
    for name, info in stations.items():
        if q in name.lower() or name.lower() in q:
            return name, stations[name]
    return None


def build_graph(stations: dict) -> dict:
    """Adjacency list from stations dict."""
    graph = {}
    for name, info in stations.items():
        graph[name] = info.get("neighbors", [])
    return graph


def bfs_route(start_name: str, end_name: str, stations: dict, graph: dict):
    """BFS shortest path by station count. Returns (path_names, num_transfers)."""
    from collections import deque

    start = stations.get(start_name)
    end = stations.get(end_name)
    if not start or not end:
        return None, None

    queue = deque([(start_name, [start_name], start["lines"])])
    visited = {start_name}

    while queue:
        current, path, current_lines = queue.popleft()
        if current == end_name:
            # Count transfers
            transfers = 0
            for i in range(1, len(path)):
                prev_lines = stations[path[i-1]]["lines"]
                curr_lines = stations[path[i]]["lines"]
                if not set(prev_lines) & set(curr_lines):
                    transfers += 1
            return path, transfers

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], stations[neighbor]["lines"]))

    return None, None


def haversine_km(lat1, lon1, lat2, lon2):
    import math
    R = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def estimate_fare(num_stops: int, num_transfers: int) -> float:
    """Zone-based flat fare approximation."""
    base = 1.00
    per_stop = 0.15
    transfer_fee = 0.00  # integrated fare
    return round(base + num_stops * per_stop, 2)


def estimate_time(num_stops: int, num_transfers: int) -> float:
    """Approximate minutes."""
    dwell = 0.5
    running = 2.0
    transfer = 5.0
    return round(num_stops * (dwell + running) + num_transfers * transfer, 1)


def format_route(path: list, stations: dict, lines: dict, num_transfers: int):
    """Human-readable route output."""
    if not path:
        return "No route found."

    num_stops = len(path) - 1
    fare = estimate_fare(num_stops, num_transfers)
    duration = estimate_time(num_stops, num_transfers)

    # Determine line colors
    line_colors = {
        "SBK": "🔴", "KG": "🟣", "PH": "⚪", "PE": "⚪",
        "SP": "🟠", "KT": "🔵", "MO": "🟢"
    }
    line_names = {
        "SBK": "MRT Kajang", "KG": "MRT Putrajaya",
        "PH": "LRT Ampang", "PE": "LRT Kelana Jaya",
        "SP": "LRT Sri Petaling", "KT": "KTM Komuter", "MO": "KL Monorail"
    }

    origin = stations[path[0]]
    dest = stations[path[-1]]
    origin_line = origin["lines"][0]
    dest_line = dest["lines"][0]

    output = []
    output.append(f"🚇 ROUTE: {origin['code']} {path[0].replace('_', ' ')} → {dest['code']} {path[-1].replace('_', ' ')}")
    output.append(f"")
    output.append(f"  {line_colors.get(origin_line, '⚫')} Line: {line_names.get(origin_line, origin_line)}")
    output.append(f"  Stops: {num_stops}")
    output.append(f"  Duration: ~{duration} min")
    output.append(f"  Fare: ~RM {fare:.2f}")
    output.append(f"  Transfers: {num_transfers}")
    output.append(f"")
    output.append("  Station sequence:")
    for i, name in enumerate(path):
        info = stations[name]
        marker = "🚉" if i == 0 else ("🏁" if i == len(path) - 1 else "  |")
        output.append(f"  {marker} {info['code']} {name.replace('_', ' ')}")
        # Check for transfer at next station
        if i < len(path) - 1:
            next_info = stations[path[i + 1]]
            if not set(info["lines"]) & set(next_info["lines"]):
                # No shared line = transfer
                transfer_line = next_info["lines"][0]
                output.append(f"      ↳ {line_colors.get(transfer_line, '⚫')} Change to {line_names.get(transfer_line, transfer_line)}")

    return "\n".join(output)


def nearest_station(lat: float, lon: float, stations: dict) -> tuple[str, float]:
    """Find nearest station to coordinates."""
    best_name = None
    best_dist = float("inf")
    for name, info in stations.items():
        d = haversine_km(lat, lon, info["lat"], info["lon"])
        if d < best_dist:
            best_dist = d
            best_name = name
    return best_name, best_dist


def main():
    if len(sys.argv) < 3:
        # Self-test
        stations, lines = load_data()
        print("=== Self-Test: Serdang Raya Utara → TRX City ===\n")

        # Find Serdang Raya Utara (Maluri is closest on SBK line)
        start_key, start = find_station("maluri", stations)
        end_key, end = find_station("trx city", stations)
        print(f"Start: {start['code']} Maluri")
        print(f"End: {end['code']} TRX City")

        graph = build_graph(stations)
        path, transfers = bfs_route(start_key, end_key, stations, graph)
        if path:
            print(f"\n{format_route(path, stations, lines, transfers)}")
        return

    origin_query = sys.argv[1]
    dest_query = sys.argv[2]

    stations, lines = load_data()
    graph = build_graph(stations)

    origin_key, origin = find_station(origin_query, stations) or (None, None)
    dest_key, dest = find_station(dest_query, stations) or (None, None)

    if not origin:
        print(f"ERROR: Cannot find station '{origin_query}'")
        suggestions = [n for n in stations if origin_query.lower() in n.lower()]
        if suggestions:
            print(f"Did you mean: {', '.join(suggestions[:5])}")
        return

    if not dest:
        print(f"ERROR: Cannot find station '{dest_query}'")
        suggestions = [n for n in stations if dest_query.lower() in n.lower()]
        if suggestions:
            print(f"Did you mean: {', '.join(suggestions[:5])}")
        return

    path, transfers = bfs_route(origin_key, dest_key, stations, graph)
    if path:
        print(format_route(path, stations, lines, transfers))
    else:
        print("No route found between these stations.")


if __name__ == "__main__":
    main()
