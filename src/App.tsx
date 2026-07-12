import React, { useEffect, useState } from 'react';
import TrinityNav from './components/TrinityNav';
import Cockpit from './Cockpit';
import AiPanel from './ai/AiPanel';
import SupabaseCockpit from './components/SupabaseCockpit';
import MCPAppsPanel from './components/MCPAppsPanel';

function useHashRoute() {
  const [hash, setHash] = useState(() => window.location.hash.slice(1));

  useEffect(() => {
    const handler = () => setHash(window.location.hash.slice(1));
    window.addEventListener('hashchange', handler);
    return () => window.removeEventListener('hashchange', handler);
  }, []);

  return hash;
}

class CockpitRouteErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '2rem', color: '#9b9995', fontFamily: 'monospace', minHeight: '100vh', background: '#0d0c0b' }}>
          <h1 style={{ color: '#D4A853', marginBottom: '1rem' }}>AAA Cockpit</h1>
          <p style={{ fontSize: '0.875rem' }}>Panel failed to load. Cockpit core is operational — try refreshing.</p>
          <button
            onClick={() => { this.setState({ hasError: false }); window.location.reload(); }}
            style={{ marginTop: '1rem', padding: '0.5rem 1rem', background: '#D4A853', color: '#0d0c0b', border: 'none', cursor: 'pointer', fontFamily: 'monospace' }}
          >
            RELOAD
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  const route = useHashRoute();

  return (
    <>
      <TrinityNav />
      {route === 'ai' ? <AiPanel /> : route === 'supabase' ? <SupabaseCockpit /> : route === 'mcp-apps' ? <MCPAppsPanel /> : <CockpitRouteErrorBoundary><Cockpit /></CockpitRouteErrorBoundary>}
    </>
  );
}

export default App;
