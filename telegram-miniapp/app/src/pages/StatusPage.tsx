import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { getFederationHealth } from "../lib/api";

const ORGAN_META: Record<string, { icon: string; desc: string; color: string }> = {
  arifOS: { icon: "⚖️", desc: "Constitutional Kernel", color: "var(--purple)" },
  GEOX: { icon: "🌍", desc: "Earth Intelligence", color: "var(--green)" },
  WEALTH: { icon: "💰", desc: "Capital Intelligence", color: "var(--yellow)" },
  WELL: { icon: "🫀", desc: "Human Readiness", color: "var(--accent)" },
};

export default function StatusPage() {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadHealth = async () => {
    try {
      const data = await getFederationHealth();
      setHealth(data);
    } catch (e) {
      console.warn("Health fetch failed:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHealth();
    const interval = setInterval(loadHealth, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const aliveCount = health?.organs?.filter((o: any) => o.status === "alive").length || 0;
  const totalCount = health?.organs?.length || 0;

  return (
    <div className="app-container">
      <motion.div className="page-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1>🏥 Federation Status</h1>
        <p className="subtitle">arifOS Constitutional Kernel</p>
      </motion.div>

      {loading && (
        <div className="loading-container">
          <div className="spinner" />
          <p style={{ fontSize: "14px", color: "var(--hint)" }}>Probing organs...</p>
        </div>
      )}

      {!loading && health && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          {/* Overall Status */}
          <div className="card" style={{ textAlign: "center", padding: "24px" }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>
              {aliveCount === totalCount ? "🟢" : aliveCount > 0 ? "🟡" : "🔴"}
            </div>
            <div style={{
              fontSize: "24px",
              fontWeight: "700",
              color: aliveCount === totalCount ? "var(--green)" : "var(--yellow)",
            }}>
              {aliveCount}/{totalCount} Organs Alive
            </div>
            <div style={{ fontSize: "12px", color: "var(--hint)", marginTop: "4px" }}>
              Last checked: {new Date(health.timestamp).toLocaleTimeString()}
            </div>
          </div>

          {/* Organ Grid */}
          <div className="section-title">Organs</div>
          <div className="organ-grid">
            {health.organs?.map((organ: any) => {
              const meta = ORGAN_META[organ.name] || { icon: "❓", desc: organ.name, color: "var(--hint)" };
              return (
                <motion.div
                  key={organ.name}
                  className="organ-card"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.05 }}
                >
                  <div className="organ-icon">{meta.icon}</div>
                  <div className="organ-name">{organ.name}</div>
                  <div className="organ-status">
                    <span className={`badge ${organ.status === "alive" ? "badge-green" : "badge-red"}`}>
                      <span className="badge-dot" />
                      {organ.status === "alive" ? "ALIVE" : "DOWN"}
                    </span>
                  </div>
                  <div style={{ fontSize: "11px", color: "var(--hint)", marginTop: "6px" }}>
                    :{organ.port}
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Architecture */}
          <div className="section-title">Architecture</div>
          <div className="card">
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {["arifOS → Constitutional Kernel (F1-F13)", "GEOX → Earth Intelligence (46 tools)", "WEALTH → Capital Intelligence (27 tools)", "WELL → Human Readiness (22 tools)"].map((line, i) => (
                <div key={i} style={{
                  padding: "10px 14px",
                  background: "rgba(255,255,255,0.03)",
                  borderRadius: "8px",
                  fontSize: "13px",
                  color: "var(--hint)",
                }}>
                  {line}
                </div>
              ))}
            </div>
          </div>

          {/* Doctrine */}
          <div className="card" style={{ textAlign: "center", padding: "24px", borderTop: "2px solid var(--accent)" }}>
            <p style={{
              fontSize: "14px",
              fontWeight: "600",
              fontStyle: "italic",
              color: "var(--accent)",
              letterSpacing: "0.5px",
            }}>
              DITEMPA BUKAN DIBERI
            </p>
            <p style={{ fontSize: "12px", color: "var(--hint)", marginTop: "6px" }}>
              Forged, Not Given
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
