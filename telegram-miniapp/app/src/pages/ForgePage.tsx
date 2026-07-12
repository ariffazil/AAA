import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Hammer, GitBranch, Docker, Server, Activity, Clock, CheckCircle, AlertCircle, Package, Terminal } from "lucide-react";

interface ForgeStatus {
  jobs?: any[];
  leases?: any[];
  agents?: any[];
  health?: any;
}

export default function ForgePage() {
  const [status, setStatus] = useState<ForgeStatus | null>(null);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [h, s] = await Promise.allSettled([
        fetch("/api/forge/health").then(r => r.json()),
        fetch("/api/forge/status").then(r => r.json()),
      ]);
      if (h.status === "fulfilled") setHealth(h.value?.result || h.value);
      if (s.status === "fulfilled") setStatus(s.value?.result || s.value);
    } catch (e) {
      console.warn("Forge fetch failed:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <motion.div className="page-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1>⚒️ A-FORGE</h1>
        <p className="subtitle">Execution Shell — Build, Deploy, Execute</p>
      </motion.div>

      {loading && (
        <div className="loading-container">
          <div className="spinner" />
          <p style={{ fontSize: "14px", color: "var(--hint)" }}>Probing A-FORGE...</p>
        </div>
      )}

      {!loading && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          {/* Health Card */}
          <div className="card" style={{ textAlign: "center", padding: "28px" }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>
              {health?.status === "ok" ? "⚒️" : "⚠️"}
            </div>
            <div style={{
              fontSize: "22px", fontWeight: "700",
              color: health?.status === "ok" ? "var(--green)" : "var(--yellow)",
            }}>
              {health?.status === "ok" ? "OPERATIONAL" : "DEGRADED"}
            </div>
            <div style={{ fontSize: "13px", color: "var(--hint)", marginTop: "6px" }}>
              Execution Shell — Constitutional Genome v2.0
            </div>
          </div>

          {/* Capabilities */}
          <div className="section-title">Capabilities</div>
          <div className="card">
            {[
              { icon: "🔨", name: "forge_execute", desc: "Governed execution with blast radius" },
              { icon: "🧪", name: "forge_dry_run", desc: "Preview before mutation" },
              { icon: "🐳", name: "forge_docker", desc: "Container lifecycle" },
              { icon: "📦", name: "forge_git", desc: "Git operations (status, diff, commit)" },
              { icon: "🖥️", name: "forge_shell", desc: "Governed shell execution" },
              { icon: "📊", name: "forge_status", desc: "Active jobs, leases, agents" },
              { icon: "🔒", name: "forge_lock", desc: "F1 Amanah lock primitive" },
              { icon: "🧪", name: "forge_sandbox", desc: "Isolated test execution" },
            ].map((cap, i) => (
              <div key={i} className="result-item">
                <div className="result-icon">{cap.icon}</div>
                <div className="result-content">
                  <div className="result-title" style={{ fontFamily: "monospace", fontSize: "13px" }}>{cap.name}</div>
                  <div className="result-desc">{cap.desc}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Governance */}
          <div className="section-title">Governance</div>
          <div className="card">
            <div className="stat-grid">
              <div className="stat-item">
                <div className="stat-value" style={{ fontSize: "18px" }}>T1</div>
                <div className="stat-label">AUTO-DO</div>
              </div>
              <div className="stat-item">
                <div className="stat-value" style={{ fontSize: "18px" }}>T2</div>
                <div className="stat-label">ANNOUNCE</div>
              </div>
              <div className="stat-item">
                <div className="stat-value" style={{ fontSize: "18px" }}>T3</div>
                <div className="stat-label">888_HOLD</div>
              </div>
              <div className="stat-item">
                <div className="stat-value" style={{ fontSize: "18px" }}>F1-F13</div>
                <div className="stat-label">FLOORS</div>
              </div>
            </div>
          </div>

          {/* Doctrine */}
          <div className="card" style={{ textAlign: "center", padding: "24px", borderTop: "2px solid var(--orange)" }}>
            <p style={{ fontSize: "14px", fontWeight: "600", color: "var(--orange)" }}>
              A-FORGE never adjudicates.
            </p>
            <p style={{ fontSize: "12px", color: "var(--hint)", marginTop: "6px" }}>
              arifOS judges. A-FORGE executes. Arif decides.
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
