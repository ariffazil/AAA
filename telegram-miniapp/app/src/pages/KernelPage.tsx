import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Scale, Shield, Eye, Lock, AlertTriangle, CheckCircle } from "lucide-react";

export default function KernelPage() {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadHealth = async () => {
    try {
      const resp = await fetch("/api/kernel/health");
      const data = await resp.json();
      setHealth(data?.result || data);
    } catch (e) {
      console.warn("Kernel fetch failed:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHealth();
    const interval = setInterval(loadHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const floors = [
    { id: "F1", name: "AMANAH", rule: "Reversible-first. Irreversible → 888_HOLD", icon: "🔒" },
    { id: "F2", name: "TRUTH", rule: "Label OBS/DER/INT/SPEC. Cap 0.90", icon: "📐" },
    { id: "F3", name: "WITNESS", rule: "Tri-witness required for SEAL", icon: "👁️" },
    { id: "F4", name: "CLARITY", rule: "ΔS ≤ 0. Reduce entropy.", icon: "💎" },
    { id: "F5", name: "PEACE²", rule: "De-escalate. Guard weakest.", icon: "☮️" },
    { id: "F6", name: "MARUAH", rule: "Dignity-first. ASEAN/MY.", icon: "⚖️" },
    { id: "F7", name: "HUMILITY", rule: "Cap 0.90. Declare unknowns.", icon: "🙏" },
    { id: "F8", name: "GENIUS", rule: "Simplest correct path.", icon: "💡" },
    { id: "F9", name: "ANTI-HANTU", rule: "No hallucination. No soul claims.", icon: "👻" },
    { id: "F10", name: "ONTOLOGY", rule: "AI-only ontology.", icon: "🧠" },
    { id: "F11", name: "AUDIT", rule: "Every decision logged.", icon: "📋" },
    { id: "F12", name: "INJECTION", rule: "Sanitize inputs.", icon: "🛡️" },
    { id: "F13", name: "SOVEREIGN", rule: "Arif holds final veto.", icon: "👑" },
  ];

  return (
    <div className="app-container">
      <motion.div className="page-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1>⚖️ arifOS</h1>
        <p className="subtitle">Constitutional Kernel — F1 through F13</p>
      </motion.div>

      {loading && (
        <div className="loading-container">
          <div className="spinner" />
          <p style={{ fontSize: "14px", color: "var(--hint)" }}>Loading kernel state...</p>
        </div>
      )}

      {!loading && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          {/* Kernel Status */}
          <div className="card" style={{ textAlign: "center", padding: "28px" }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>⚖️</div>
            <div style={{
              fontSize: "22px", fontWeight: "700",
              color: health?.thermodynamic?.verdict === "SEAL" ? "var(--green)" : "var(--yellow)",
            }}>
              {health?.thermodynamic?.verdict || "UNKNOWN"}
            </div>
            <div style={{ fontSize: "13px", color: "var(--hint)", marginTop: "6px" }}>
              {health?.floors_active || 13} floors active • Runtime drift: {health?.runtime_drift || "?"}
            </div>
            {health?.vault999_health && (
              <div style={{ marginTop: "8px" }}>
                <span className="badge badge-green"><span className="badge-dot" /> VAULT999 {health.vault999_health}</span>
              </div>
            )}
          </div>

          {/* Identity */}
          {health?.identity_hash && (
            <div className="card">
              <div className="card-header">
                <div className="card-icon">🔐</div>
                <div>
                  <div className="card-title">Identity</div>
                  <div className="card-subtitle">Constitutional identity hash</div>
                </div>
              </div>
              <div style={{
                padding: "10px 14px", background: "rgba(255,255,255,0.03)",
                borderRadius: "8px", fontFamily: "monospace", fontSize: "12px",
                color: "var(--hint)", wordBreak: "break-all",
              }}>
                {health.identity_hash.b3_prefix || health.identity_hash}
              </div>
            </div>
          )}

          {/* 13 Floors */}
          <div className="section-title">Constitutional Floors</div>
          {floors.map((floor, i) => (
            <motion.div
              key={floor.id}
              className="card"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.03 }}
              style={{ padding: "14px 16px", marginBottom: "6px" }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <div style={{ fontSize: "20px", width: "32px", textAlign: "center" }}>{floor.icon}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span style={{ fontSize: "12px", fontWeight: "700", color: "var(--accent)", fontFamily: "monospace" }}>{floor.id}</span>
                    <span style={{ fontSize: "14px", fontWeight: "600" }}>{floor.name}</span>
                  </div>
                  <div style={{ fontSize: "12px", color: "var(--hint)", marginTop: "2px" }}>{floor.rule}</div>
                </div>
                <span className="badge badge-green"><span className="badge-dot" /></span>
              </div>
            </motion.div>
          ))}

          {/* Doctrine */}
          <div className="card" style={{ textAlign: "center", padding: "24px", borderTop: "2px solid var(--purple)" }}>
            <p style={{ fontSize: "14px", fontWeight: "600", color: "var(--purple)" }}>
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
