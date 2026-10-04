/**
 * <PanelName> — <Description>
 * ═══════════════════════════════════════════════════════════════════════════════
 * DITEMPA BUKAN DIBERI
 *
 * <Purpose description>
 */

import React, { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import * as d3 from 'd3';
import { Layers, RefreshCw, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import { useMcpTool } from '../../hooks/useMcpTool';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

interface PanelProps {
  // Define props here
}

interface McpResult {
  // Define MCP response shape here
}

// ─────────────────────────────────────────────────────────────────────────────
// Layout constants
// ─────────────────────────────────────────────────────────────────────────────

const HEADER_HEIGHT = 44;
const STATUS_BAR_HEIGHT = 28;
const MARGIN = { top: 8, right: 4, bottom: 16, left: 4 };
const PLOT_HEIGHT = 600;

// ─────────────────────────────────────────────────────────────────────────────
// Styles (inline CSS-in-JS)
// ─────────────────────────────────────────────────────────────────────────────

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex', flexDirection: 'column', height: '100%',
    backgroundColor: '#0a0a0f', color: '#e2e8f0',
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
    overflow: 'hidden', userSelect: 'none',
  },
  header: {
    display: 'flex', alignItems: 'center', height: HEADER_HEIGHT, minHeight: HEADER_HEIGHT,
    padding: '0 16px', backgroundColor: '#0d0d14',
    borderBottom: '1px solid #1a1a2e', gap: 12,
  },
  headerTitle: {
    fontSize: 13, fontWeight: 700, color: '#00d4aa', letterSpacing: '0.05em',
  },
  statusBar: {
    height: STATUS_BAR_HEIGHT, minHeight: STATUS_BAR_HEIGHT,
    display: 'flex', alignItems: 'center', padding: '0 16px',
    backgroundColor: '#0a0a0f', borderTop: '1px solid #1a1a2e',
    fontSize: 9, color: '#475569', gap: 16,
    fontFamily: "'JetBrains Mono', monospace",
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// Canvas renderer sub-component
// ─────────────────────────────────────────────────────────────────────────────

interface CanvasRendererProps {
  // Define sub-component props
  width: number;
  height: number;
}

const CanvasRenderer: React.FC<CanvasRendererProps> = ({ width, height }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const plotHeight = height - MARGIN.top - MARGIN.bottom;

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // High-DPI
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    // Background
    ctx.fillStyle = '#0a0a0f';
    ctx.fillRect(0, 0, width, height);

    // TODO: draw content

  }, [width, height, plotHeight]);

  useEffect(() => { draw(); }, [draw]);

  return (
    <canvas
      ref={canvasRef}
      style={{ width, height, cursor: 'crosshair' }}
    />
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Data loading hook
// ─────────────────────────────────────────────────────────────────────────────

function usePanelData(id: string) {
  const tool = useMcpTool<{ id: string; mode: string }, McpResult>('geox_tool_name');

  const [data, setData] = useState<McpResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await tool.call({ id, mode: 'auto' });
      if (!result) throw new Error('No data returned');
      setData(result);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }, [id, tool]);

  useEffect(() => { load(); }, [load]);

  return { data, loading, error, reload: load };
}

// ─────────────────────────────────────────────────────────────────────────────
// Main component
// ─────────────────────────────────────────────────────────────────────────────

export const PanelName: React.FC<PanelProps> = (props) => {
  const { data, loading, error, reload } = usePanelData('some-id');

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <Layers size={14} color="#00d4aa" />
        <span style={styles.headerTitle}>Panel Title</span>
        <div style={{ flex: 1 }} />
      </div>

      {/* Main content */}
      <div style={{ flex: 1, position: 'relative' }}>
        {!loading && data && (
          <CanvasRenderer width={800} height={PLOT_HEIGHT} />
        )}

        {loading && (
          <div style={{
            position: 'absolute', inset: 0, display: 'flex',
            flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            backgroundColor: 'rgba(10, 10, 15, 0.85)', gap: 8,
          }}>
            <Loader2 size={24} color="#00d4aa" className="animate-spin" />
            <span style={{ fontSize: 10, color: '#64748b' }}>Loading…</span>
          </div>
        )}

        {!loading && error && (
          <div style={{
            position: 'absolute', inset: 0, display: 'flex',
            flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            backgroundColor: 'rgba(10, 10, 15, 0.85)', gap: 6,
          }}>
            <AlertTriangle size={18} color="#ef4444" />
            <span style={{ fontSize: 10, color: '#ef4444', textAlign: 'center', maxWidth: 300 }}>
              {error}
            </span>
            <button onClick={reload} style={{
              marginTop: 4, padding: '3px 10px', fontSize: 9, color: '#00d4aa',
              background: 'rgba(0, 212, 170, 0.1)', border: '1px solid rgba(0, 212, 170, 0.3)',
              borderRadius: 4, cursor: 'pointer', fontFamily: 'inherit',
            }}>
              Retry
            </button>
          </div>
        )}
      </div>

      {/* Status bar */}
      <div style={styles.statusBar}>
        <span>
          {loading ? <span style={{ color: '#d4af37' }}>●</span> : <span style={{ color: '#22c55e' }}>●</span>}
          {' '}Status text
        </span>
        <div style={{ flex: 1 }} />
        <span style={{ color: '#d4af37', opacity: 0.5 }}>DITEMPA BUKAN DIBERI</span>
      </div>
    </div>
  );
};
