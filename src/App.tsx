import { useEffect, useState } from 'react';
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

function App() {
  const route = useHashRoute();

  return (
    <>
      <TrinityNav />
      {route === 'ai' ? <AiPanel /> : route === 'supabase' ? <SupabaseCockpit /> : route === 'mcp-apps' ? <MCPAppsPanel /> : <Cockpit />}
    </>
  );
}

export default App;
