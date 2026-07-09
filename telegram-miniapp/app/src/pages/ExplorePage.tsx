import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MapPin, Search, Globe, Layers, Mountain, Droplets, Zap, ChevronRight, Navigation } from "lucide-react";
import { getUser } from "../lib/telegram";
import { getAtlas, getBasin, getEarthquakes } from "../lib/api";

interface AtlasResult {
  country?: string;
  land?: boolean;
  water?: boolean;
  context?: string;
}

interface Earthquake {
  id: string;
  properties: {
    place: string;
    mag: number;
    time: number;
    url: string;
  };
  geometry: {
    coordinates: [number, number, number];
  };
}

const PRESET_LOCATIONS = [
  { name: "Kuala Lumpur", lat: 3.139, lon: 101.687, icon: "🏙️" },
  { name: "Kota Kinabalu", lat: 5.980, lon: 116.073, icon: "🏔️" },
  { name: "Miri, Sarawak", lat: 4.399, lon: 113.991, icon: "🛢️" },
  { name: "South China Sea", lat: 7.5, lon: 112.0, icon: "🌊" },
  { name: "Taranaki Basin", lat: -39.0, lon: 174.0, icon: "🪨" },
  { name: "Niger Delta", lat: 5.0, lon: 5.5, icon: "⛽" },
];

export default function ExplorePage() {
  const [lat, setLat] = useState<number | null>(null);
  const [lon, setLon] = useState<number | null>(null);
  const [searchText, setSearchText] = useState("");
  const [atlasResult, setAtlasResult] = useState<AtlasResult | null>(null);
  const [earthquakes, setEarthquakes] = useState<Earthquake[]>([]);
  const [loading, setLoading] = useState(false);
  const [eqLoading, setEqLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"atlas" | "seismic">("atlas");
  const [error, setError] = useState<string | null>(null);

  // Auto-load earthquakes on mount
  useEffect(() => {
    loadEarthquakes();
  }, []);

  const loadEarthquakes = async () => {
    setEqLoading(true);
    try {
      const data = await getEarthquakes(4.5);
      setEarthquakes(data?.features || data?.result?.features || []);
    } catch (e) {
      console.warn("Earthquake fetch failed:", e);
    } finally {
      setEqLoading(false);
    }
  };

  const exploreLocation = useCallback(async (latitude: number, longitude: number) => {
    setLat(latitude);
    setLon(longitude);
    setLoading(true);
    setError(null);
    setAtlasResult(null);

    try {
      const data = await getAtlas(latitude, longitude);
      // Handle MCP response envelope — unwrap nested results
      let result = data?.result || data;
      if (result?.result) result = result.result;
      setAtlasResult(result);
    } catch (e: any) {
      setError(e.message || "Failed to fetch atlas data");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleSearch = () => {
    // Try to parse as "lat,lon"
    const parts = searchText.split(",").map(Number);
    if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
      exploreLocation(parts[0], parts[1]);
    } else {
      setError("Enter coordinates as: lat,lon (e.g., 3.139,101.687)");
    }
  };

  const useMyLocation = () => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => exploreLocation(pos.coords.latitude, pos.coords.longitude),
        () => setError("Location access denied. Search manually.")
      );
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <motion.div
        className="page-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="globe-container">
          <div className="globe" />
          <div className="globe-ring" />
        </div>
        <h1>🌍 Earth Explorer</h1>
        <p className="subtitle">Powered by GEOX Federation</p>
      </motion.div>

      {/* Search */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="search-box">
          <input
            className="search-input"
            placeholder="lat,lon (e.g., 3.139,101.687)"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            inputMode="decimal"
          />
          <button className="btn btn-primary" style={{ width: "auto", padding: "12px 16px" }} onClick={handleSearch}>
            <Search size={18} />
          </button>
        </div>

        {/* Quick location buttons */}
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "16px" }}>
          <button className="btn btn-ghost" style={{ width: "auto", padding: "8px 14px", fontSize: "13px" }} onClick={useMyLocation}>
            <Navigation size={14} /> My Location
          </button>
          {PRESET_LOCATIONS.map((loc) => (
            <button
              key={loc.name}
              className="btn btn-ghost"
              style={{ width: "auto", padding: "8px 14px", fontSize: "13px" }}
              onClick={() => exploreLocation(loc.lat, loc.lon)}
            >
              {loc.icon} {loc.name}
            </button>
          ))}
        </div>
      </motion.div>

      {/* Tabs */}
      <div className="nav-tabs">
        <button className={`nav-tab ${activeTab === "atlas" ? "active" : ""}`} onClick={() => setActiveTab("atlas")}>
          🌍 Atlas
        </button>
        <button className={`nav-tab ${activeTab === "seismic" ? "active" : ""}`} onClick={() => setActiveTab("seismic")}>
          ⚡ Seismic
        </button>
      </div>

      {/* Error */}
      <AnimatePresence>
        {error && (
          <motion.div
            className="card"
            style={{ borderLeft: "3px solid var(--red)", marginBottom: "12px" }}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
          >
            <p style={{ fontSize: "13px", color: "var(--red)" }}>⚠️ {error}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Atlas Tab */}
      {activeTab === "atlas" && (
        <>
          {loading && (
            <div className="loading-container">
              <div className="spinner" />
              <p style={{ fontSize: "14px", color: "var(--hint)" }}>Querying GEOX atlas...</p>
            </div>
          )}

          {atlasResult && !loading && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
              {/* Location Card */}
              <div className="card">
                <div className="card-header">
                  <div className="card-icon">📍</div>
                  <div>
                    <div className="card-title">{lat?.toFixed(4)}°, {lon?.toFixed(4)}°</div>
                    <div className="card-subtitle">
                      {atlasResult.land ? "Land" : atlasResult.water ? "Water" : "Unknown"} surface
                    </div>
                  </div>
                  <span className={`badge ${atlasResult.land ? "badge-green" : "badge-blue"}`}>
                    <span className="badge-dot" />
                    {atlasResult.land ? "LAND" : "OCEAN"}
                  </span>
                </div>

                {atlasResult.country && (
                  <div className="result-item">
                    <div className="result-icon">🏳️</div>
                    <div className="result-content">
                      <div className="result-title">Country</div>
                      <div className="result-desc">Sovereign territory</div>
                    </div>
                    <div className="result-value">{atlasResult.country}</div>
                  </div>
                )}

                {atlasResult.context && (
                  <div style={{ marginTop: "12px", padding: "12px", background: "rgba(59,130,246,0.08)", borderRadius: "10px" }}>
                    <p style={{ fontSize: "13px", lineHeight: "1.6", color: "var(--hint)" }}>
                      {typeof atlasResult.context === "string" ? atlasResult.context : JSON.stringify(atlasResult.context)}
                    </p>
                  </div>
                )}
              </div>

              {/* Quick Actions */}
              <div className="section-title">Quick Actions</div>
              <div style={{ display: "flex", gap: "10px" }}>
                <button className="btn btn-ghost" style={{ flex: 1 }} onClick={() => {
                  const q = PRESET_LOCATIONS.find(l => l.name.includes("Miri"));
                  if (q) exploreLocation(q.lat, q.lon);
                }}>
                  <Layers size={16} /> Basin Profile
                </button>
                <button className="btn btn-ghost" style={{ flex: 1 }} onClick={() => setActiveTab("seismic")}>
                  <Zap size={16} /> Seismic Activity
                </button>
              </div>
            </motion.div>
          )}

          {!atlasResult && !loading && (
            <div className="empty-state">
              <div className="emoji">🌏</div>
              <p>Tap a location or search coordinates<br/>to explore Earth intelligence.</p>
            </div>
          )}
        </>
      )}

      {/* Seismic Tab */}
      {activeTab === "seismic" && (
        <>
          {eqLoading && (
            <div className="loading-container">
              <div className="spinner" />
              <p style={{ fontSize: "14px", color: "var(--hint)" }}>Loading seismic data...</p>
            </div>
          )}

          {!eqLoading && earthquakes.length > 0 && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <div className="card">
                <div className="card-header">
                  <div className="card-icon">⚡</div>
                  <div>
                    <div className="card-title">Recent Earthquakes</div>
                    <div className="card-subtitle">M4.5+ — Last 7 days (USGS)</div>
                  </div>
                  <span className="badge badge-yellow">
                    <span className="badge-dot" />
                    LIVE
                  </span>
                </div>

                <div className="stat-grid" style={{ marginBottom: "16px" }}>
                  <div className="stat-item">
                    <div className="stat-value">{earthquakes.length}</div>
                    <div className="stat-label">Events</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-value">
                      {Math.max(...earthquakes.map(e => e.properties.mag)).toFixed(1)}
                    </div>
                    <div className="stat-label">Max Magnitude</div>
                  </div>
                </div>
              </div>

              {earthquakes.slice(0, 10).map((eq, i) => (
                <motion.div
                  key={eq.id}
                  className="card"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  style={{ cursor: "pointer" }}
                  onClick={() => exploreLocation(eq.geometry.coordinates[1], eq.geometry.coordinates[0])}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                    <div style={{
                      width: "44px",
                      height: "44px",
                      borderRadius: "12px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "18px",
                      fontWeight: "700",
                      background: eq.properties.mag >= 6 ? "rgba(239,68,68,0.15)" :
                                  eq.properties.mag >= 5 ? "rgba(249,115,22,0.15)" :
                                  "rgba(234,179,8,0.15)",
                      color: eq.properties.mag >= 6 ? "var(--red)" :
                             eq.properties.mag >= 5 ? "var(--orange)" :
                             "var(--yellow)",
                    }}>
                      {eq.properties.mag.toFixed(1)}
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: "14px", fontWeight: 600 }}>{eq.properties.place}</div>
                      <div style={{ fontSize: "12px", color: "var(--hint)", marginTop: "2px" }}>
                        {new Date(eq.properties.time).toLocaleDateString()} • Depth: {eq.geometry.coordinates[2]?.toFixed(0)}km
                      </div>
                    </div>
                    <ChevronRight size={16} style={{ color: "var(--hint)" }} />
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}

          {!eqLoading && earthquakes.length === 0 && (
            <div className="empty-state">
              <div className="emoji">✅</div>
              <p>No significant seismic events in the past 7 days.</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
